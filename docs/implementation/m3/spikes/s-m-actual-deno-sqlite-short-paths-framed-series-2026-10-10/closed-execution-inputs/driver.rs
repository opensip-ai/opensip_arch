#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;
extern crate rustc_span;
extern crate sha2_const_stable;
extern crate serde_json;
use std::io::Read;
use std::time::Instant;
use std::io::Write;
use std::{collections::BTreeMap, io, path::{Path,PathBuf,Component}, sync::{Arc,atomic::{AtomicU64,Ordering}}};

fn json_string(value:&str)->String {
 let mut result=String::from("\"");
 for ch in value.chars(){match ch{'"'=>result.push_str("\\\""),'\\'=>result.push_str("\\\\"),'\u{0000}'..='\u{001f}'=>result.push_str(&format!("\\u{:04x}",ch as u32)),_=>result.push(ch)}}
 result.push('"');result
}
fn source_event(path:&Path,bytes:Option<usize>,binary:bool){
 let name=path.to_str().map(json_string).unwrap_or_else(||String::from("null"));
 let size=bytes.map(|n|n.to_string()).unwrap_or_else(||String::from("null"));
 println!("{{\"event\":\"prepared_source_read\",\"normalizedPath\":{},\"contentBytes\":{},\"binary\":{},\"preparedMapEntryPresent\":{}}}",name,size,binary,bytes.is_some());
}


fn sha256_hex(raw:&[u8])->String {sha2_const_stable::Sha256::new().update(raw).finalize().iter().map(|b|format!("{b:02x}")).collect()}
fn frame(stream:&mut impl Read)->Vec<u8> {
 let mut length=[0u8;4];stream.read_exact(&mut length).expect("framed map truncated length");
 let length=u32::from_be_bytes(length) as usize;assert!((1..=1<<20).contains(&length),"framed map frame bound");
 let mut data=vec![0;length];stream.read_exact(&mut data).expect("framed map truncated payload");data
}
fn framed_map()->Vec<u8> {
 println!("{{\"event\":\"transfer_ready\"}}");std::io::stdout().flush().unwrap();
 let mut input=std::io::stdin().lock();let header:serde_json::Value=serde_json::from_slice(&frame(&mut input)).expect("framed map header JSON");
 let header=header.as_object().expect("framed map header object");assert_eq!(header.len(),3,"framed map header members");
 assert_eq!(header.get("format").and_then(|v|v.as_str()),Some("OPSMRUST1"));
 let expected=header.get("bytes").and_then(|v|v.as_u64()).expect("framed map bytes integer");
 // Derived wire overhead: content bound + descriptor bound + two u64 per row + magic/count.
 assert!((18..=((8u64<<30)+(4u64<<20)+16*100000+18)).contains(&expected),"framed map derived wire bound");
 let pin=header.get("sha256").and_then(|v|v.as_str()).expect("framed map hash text");
 assert!(pin.len()==64 && pin.bytes().all(|b|b.is_ascii_digit()||(b'a'..=b'f').contains(&b)),"framed map hash shape");
 let expected=usize::try_from(expected).unwrap();let mut raw=Vec::new();raw.try_reserve_exact(expected).expect("framed map allocation");let mut frames=0u64;
 while raw.len()<expected {let data=frame(&mut input);assert!(data.len()<=expected-raw.len(),"framed map extra content");raw.extend_from_slice(&data);frames=frames.checked_add(1).unwrap();}
 let mut tail=[0u8;1];assert_eq!(input.read(&mut tail).unwrap(),0,"framed map trailing input");
 let observed=sha256_hex(&raw);assert_eq!(observed,pin,"framed map whole hash differs");
 println!("{{\"event\":\"prepared_map_wire_verified\",\"mapBytes\":{},\"mapSha256\":{},\"contentFrames\":{}}}",raw.len(),json_string(&observed),frames);raw
}

struct PreparedFiles { files: Arc<BTreeMap<PathBuf,Vec<u8>>>, cwd:PathBuf, reads:Arc<AtomicU64>, denied:Arc<AtomicU64> }
fn normalized(path:&Path,cwd:&Path)->PathBuf {
 let absolute=if path.is_absolute(){path.to_owned()}else{cwd.join(path)};let mut out=PathBuf::new();
 for p in absolute.components(){match p{Component::CurDir=>{},Component::ParentDir=>{out.pop();},p=>out.push(p.as_os_str())}}
 out
}
impl rustc_span::source_map::FileLoader for PreparedFiles {
 fn current_directory(&self)->io::Result<PathBuf>{Ok(self.cwd.clone())}
 fn file_exists(&self,path:&Path)->bool {self.files.contains_key(&normalized(path,&self.cwd))}
 fn read_file(&self,path:&Path)->io::Result<String> {
  self.reads.fetch_add(1,Ordering::Relaxed);
  source_event(&normalized(path,&self.cwd),self.files.get(&normalized(path,&self.cwd)).map(|v|v.len()),false);
  match self.files.get(&normalized(path,&self.cwd)) {Some(bytes)=>String::from_utf8(bytes.clone()).map_err(|_|io::Error::new(io::ErrorKind::InvalidData,"prepared source is not UTF8")),None=>{self.denied.fetch_add(1,Ordering::Relaxed);Err(io::Error::new(io::ErrorKind::NotFound,"source read outside prepared map"))}}
 }
 fn read_binary_file(&self,path:&Path)->io::Result<Arc<[u8]>> {
  self.reads.fetch_add(1,Ordering::Relaxed);
  source_event(&normalized(path,&self.cwd),self.files.get(&normalized(path,&self.cwd)).map(|v|v.len()),true);
  match self.files.get(&normalized(path,&self.cwd)){Some(bytes)=>Ok(Arc::from(bytes.clone())),None=>{self.denied.fetch_add(1,Ordering::Relaxed);Err(io::Error::new(io::ErrorKind::NotFound,"binary source read outside prepared map"))}}
 }
}
struct Probe {loader:Option<PreparedFiles>,reads:Arc<AtomicU64>,denied:Arc<AtomicU64>,started:Instant}
impl rustc_driver::Callbacks for Probe {
 fn config(&mut self,config:&mut rustc_interface::interface::Config){config.file_loader=Some(Box::new(self.loader.take().unwrap()));}
 fn after_expansion<'tcx>(&mut self,_:&rustc_interface::interface::Compiler,_:rustc_middle::ty::TyCtxt<'tcx>)->rustc_driver::Compilation {
  println!("{{\"event\":\"after_expansion\",\"readCalls\":{},\"deniedReadCalls\":{}}}",self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Continue
 }
 fn after_analysis<'tcx>(&mut self,_:&rustc_interface::interface::Compiler,_:rustc_middle::ty::TyCtxt<'tcx>)->rustc_driver::Compilation {
  let elapsed=u64::try_from(self.started.elapsed().as_nanos()).expect("analysis interval fits u64");
  println!("{{\"event\":\"after_analysis\",\"analysisElapsedNanos\":{},\"readCalls\":{},\"deniedReadCalls\":{}}}",elapsed,self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Continue
 }
}
fn number(raw:&[u8],at:&mut usize)->usize {let end=at.checked_add(8).unwrap();let n=u64::from_be_bytes(raw[*at..end].try_into().unwrap());*at=end;usize::try_from(n).unwrap()}
fn bytes<'a>(raw:&'a[u8],at:&mut usize,n:usize)->&'a[u8]{let end=at.checked_add(n).unwrap();let value=&raw[*at..end];*at=end;value}
fn main(){
 let mut args:Vec<String>=std::env::args().collect();assert_eq!(args.get(1).map(String::as_str),Some("--prepared-map-framed-stdin"));args.remove(1);let raw=framed_map();assert!(raw.starts_with(b"OPSMRUST1\0"));let mut at=10;let count=number(&raw,&mut at);assert!(count<=100000 && count<=raw.len()/16);let cwd=std::env::current_dir().unwrap();let mut files=BTreeMap::new();let mut content_total=0u64;let mut descriptor_size=2usize;
 for _ in 0..count {let n=number(&raw,&mut at);let name=std::str::from_utf8(bytes(&raw,&mut at,n)).unwrap();let n=number(&raw,&mut at);content_total=content_total.checked_add(u64::try_from(n).unwrap()).unwrap();assert!(content_total<=8u64<<30,"prepared content bound");let content=bytes(&raw,&mut at,n).to_vec();
 let mut row=serde_json::Map::new();row.insert("bytes".into(),serde_json::Value::from(n));row.insert("path".into(),serde_json::Value::from(name));row.insert("sha256".into(),serde_json::Value::from(sha256_hex(&content)));let encoded=serde_json::to_vec(&serde_json::Value::Object(row)).unwrap();descriptor_size=descriptor_size.checked_add(encoded.len()).unwrap();if !files.is_empty(){descriptor_size=descriptor_size.checked_add(1).unwrap();}assert!(descriptor_size<=4<<20,"prepared descriptor bound");
 let name=PathBuf::from(name);assert!(name.is_absolute());assert_eq!(normalized(&name,&cwd),name);assert!(files.insert(name,content).is_none());}assert_eq!(at,raw.len());let reads=Arc::new(AtomicU64::new(0));let denied=Arc::new(AtomicU64::new(0));let loader=PreparedFiles{files:Arc::new(files),cwd,reads:reads.clone(),denied:denied.clone()};println!("{{\"event\":\"analysis_span_started\",\"mapDecodingExcluded\":true,\"instrumentationIncluded\":true}}");std::io::stdout().flush().unwrap();let mut callbacks=Probe{loader:Some(loader),reads,denied,started:Instant::now()};rustc_driver::run_compiler(&args,&mut callbacks);
}
