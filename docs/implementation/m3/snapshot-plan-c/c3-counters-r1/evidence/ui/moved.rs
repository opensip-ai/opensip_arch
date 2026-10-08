#[allow(dead_code)]
#[path = "/Users/sb/code/opensip-ai/opensip-c3-counters/crates/host/src/dependency_counters.rs"]
mod dependency_counters;
fn main(){let a=dependency_counters::Acquisition::new();let _next=a.source().unwrap();let _=a.totals();}
