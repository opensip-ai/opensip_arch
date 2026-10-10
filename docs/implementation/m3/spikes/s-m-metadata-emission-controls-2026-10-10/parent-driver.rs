#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;
extern crate rustc_span;
use std::{collections::BTreeMap, io, path::{Path,PathBuf,Component}, sync::{Arc,atomic::{AtomicU64,Ordering}}};
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
  match self.files.get(&normalized(path,&self.cwd)) {Some(bytes)=>String::from_utf8(bytes.clone()).map_err(|_|io::Error::new(io::ErrorKind::InvalidData,"prepared source is not UTF8")),None=>{self.denied.fetch_add(1,Ordering::Relaxed);Err(io::Error::new(io::ErrorKind::NotFound,"source read outside prepared map"))}}
 }
 fn read_binary_file(&self,path:&Path)->io::Result<Arc<[u8]>> {
  self.reads.fetch_add(1,Ordering::Relaxed);
  match self.files.get(&normalized(path,&self.cwd)){Some(bytes)=>Ok(Arc::from(bytes.clone())),None=>{self.denied.fetch_add(1,Ordering::Relaxed);Err(io::Error::new(io::ErrorKind::NotFound,"binary source read outside prepared map"))}}
 }
}
struct Probe {loader:Option<PreparedFiles>,reads:Arc<AtomicU64>,denied:Arc<AtomicU64>}
impl rustc_driver::Callbacks for Probe {
 fn config(&mut self,config:&mut rustc_interface::interface::Config){config.file_loader=Some(Box::new(self.loader.take().unwrap()));}
 fn after_expansion<'tcx>(&mut self,_:&rustc_interface::interface::Compiler,_:rustc_middle::ty::TyCtxt<'tcx>)->rustc_driver::Compilation {
  println!("{{\"event\":\"after_expansion\",\"readCalls\":{},\"deniedReadCalls\":{}}}",self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Continue
 }
 fn after_analysis<'tcx>(&mut self,_:&rustc_interface::interface::Compiler,_:rustc_middle::ty::TyCtxt<'tcx>)->rustc_driver::Compilation {
  println!("{{\"event\":\"after_analysis\",\"readCalls\":{},\"deniedReadCalls\":{}}}",self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Stop
 }
}
fn number(raw:&[u8],at:&mut usize)->usize {let end=at.checked_add(8).unwrap();let n=u64::from_be_bytes(raw[*at..end].try_into().unwrap());*at=end;usize::try_from(n).unwrap()}
fn bytes<'a>(raw:&'a[u8],at:&mut usize,n:usize)->&'a[u8]{let end=at.checked_add(n).unwrap();let value=&raw[*at..end];*at=end;value}
fn main(){
 let mut args:Vec<String>=std::env::args().collect();assert_eq!(args.get(1).map(String::as_str),Some("--prepared-map"));let raw=std::fs::read(&args[2]).unwrap();args.drain(1..3);assert!(raw.starts_with(b"OPSMRUST1\0"));let mut at=10;let count=number(&raw,&mut at);assert!(count<=raw.len()/16);let cwd=std::env::current_dir().unwrap();let mut files=BTreeMap::new();
 for _ in 0..count {let n=number(&raw,&mut at);let name=std::str::from_utf8(bytes(&raw,&mut at,n)).unwrap();let n=number(&raw,&mut at);let content=bytes(&raw,&mut at,n).to_vec();let name=PathBuf::from(name);assert!(name.is_absolute());assert_eq!(normalized(&name,&cwd),name);assert!(files.insert(name,content).is_none());}assert_eq!(at,raw.len());let reads=Arc::new(AtomicU64::new(0));let denied=Arc::new(AtomicU64::new(0));let loader=PreparedFiles{files:Arc::new(files),cwd,reads:reads.clone(),denied:denied.clone()};let mut callbacks=Probe{loader:Some(loader),reads,denied};rustc_driver::run_compiler(&args,&mut callbacks);
}
