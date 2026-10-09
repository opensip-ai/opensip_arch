#![allow(dead_code)]
mod archive_decoder;mod dependency_counters;mod acquisition_guard;mod raw_stream_copy;
fn main(){let mut b=acquisition_guard::CandidateBudget::new();let a=acquisition_guard::begin_source_attempt(&mut b).unwrap();let _second=acquisition_guard::begin_source_attempt(&mut b);drop(a);}
