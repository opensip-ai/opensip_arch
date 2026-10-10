from pathlib import Path
import hashlib,shutil
B=Path('/tmp/opensip-implementation');BASE=B/'sm-graph-typecheck-2026-10-10';V=B/'sm-analysis-timing-2026-10-10';assert not V.exists();V.mkdir();p=BASE/'driver.rs';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='035471c402ce39815c817b838d16cdee0747eb877e3549a42a5a3596024f2aac';s=raw.decode();s=s.replace('use std::{','use std::time::Instant;\nuse std::io::Write;\nuse std::{',1)
helper=r'''
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
'''
s=s.replace('struct PreparedFiles',helper+'\nstruct PreparedFiles',1)
needle='  self.reads.fetch_add(1,Ordering::Relaxed);\n  match';assert s.count(needle)==2
s=s.replace(needle,'  self.reads.fetch_add(1,Ordering::Relaxed);\n  source_event(&normalized(path,&self.cwd),self.files.get(&normalized(path,&self.cwd)).map(|v|v.len()),false);\n  match',1)
s=s.replace(needle,'  self.reads.fetch_add(1,Ordering::Relaxed);\n  source_event(&normalized(path,&self.cwd),self.files.get(&normalized(path,&self.cwd)).map(|v|v.len()),true);\n  match',1)
s=s.replace('struct Probe {loader:Option<PreparedFiles>,reads:Arc<AtomicU64>,denied:Arc<AtomicU64>}','struct Probe {loader:Option<PreparedFiles>,reads:Arc<AtomicU64>,denied:Arc<AtomicU64>,started:Instant}',1)
old='  println!("{{\\\"event\\\":\\\"after_analysis\\\",\\\"readCalls\\\":{},\\\"deniedReadCalls\\\":{}}}",self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Continue'
assert old in s
new='  let elapsed=u64::try_from(self.started.elapsed().as_nanos()).expect("analysis interval fits u64");\n  println!("{{\\\"event\\\":\\\"after_analysis\\\",\\\"analysisElapsedNanos\\\":{},\\\"readCalls\\\":{},\\\"deniedReadCalls\\\":{}}}",elapsed,self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Continue'
s=s.replace(old,new,1)
old='let mut callbacks=Probe{loader:Some(loader),reads,denied};rustc_driver::run_compiler(&args,&mut callbacks);';assert old in s
s=s.replace(old,'println!("{{\\\"event\\\":\\\"analysis_span_started\\\",\\\"mapDecodingExcluded\\\":true,\\\"instrumentationIncluded\\\":true}}");std::io::stdout().flush().unwrap();let mut callbacks=Probe{loader:Some(loader),reads,denied,started:Instant::now()};rustc_driver::run_compiler(&args,&mut callbacks);',1)
(V/'driver.rs').write_text(s);shutil.copyfile(BASE/'build_driver.py',V/'build_driver.py');print('Separate timed/source-observation driver authored; accepted source unchanged.')
