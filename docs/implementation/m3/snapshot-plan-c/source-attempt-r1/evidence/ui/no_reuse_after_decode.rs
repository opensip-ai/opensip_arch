#![allow(dead_code)]
mod archive_decoder;mod dependency_counters;mod acquisition_guard;mod raw_stream_copy;
struct Consumer; impl archive_decoder::ArchiveConsumer for Consumer {type Error=();fn checkpoint(&mut self)->Result<(),()>{Ok(())}fn begin(&mut self,_:&opensip_identity::LogicalPath,_:u128)->Result<(),()>{Ok(())}fn content(&mut self,_:&[u8])->Result<(),()>{Ok(())}fn end(&mut self,_:&archive_decoder::FileRecord)->Result<(),()>{Ok(())}}
fn main(){let mut b=acquisition_guard::CandidateBudget::new();let a=acquisition_guard::begin_source_attempt(&mut b).unwrap();let _=a.decode(&[][..],"unit","1.0.0",&mut Consumer);drop(a);}
