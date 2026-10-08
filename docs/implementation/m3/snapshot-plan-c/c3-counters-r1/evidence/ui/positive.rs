#[allow(dead_code)]
#[path = "/Users/sb/code/opensip-ai/opensip-c3-counters/crates/host/src/dependency_counters.rs"]
mod dependency_counters;
fn main(){ let a=dependency_counters::Acquisition::new().source().unwrap().file(7).unwrap();assert_eq!(a.totals().content,7);assert!(dependency_counters::FinalPopulation::new().package(1,7).unwrap().check().is_ok());}
