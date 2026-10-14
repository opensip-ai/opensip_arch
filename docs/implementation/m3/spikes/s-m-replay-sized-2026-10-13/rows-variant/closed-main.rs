use std::{collections::BTreeMap,time::Instant};
use opensip_identity::{IdentityDomain as D,JsonValue as V,ObjectInput,RetainedInputs,TraversalBudget,parse_json};
use opensip_evaluator::{ReplayLimits,RetainedWalkLimits,replay_run};
fn field<'a>(v:&'a V,key:&str)->&'a V{match v{V::Object(o)=>o.get(key).unwrap(),_=>panic!("object")}}
fn text(v:&V)->&str{match v{V::String(s)=>s,_=>panic!("text")}}
fn array(v:&V)->&[V]{match v{V::Array(a)=>a,_=>panic!("array")}}
fn hex(s:&str)->Vec<u8>{assert_eq!(s.len()%2,0);s.as_bytes().chunks_exact(2).map(|p|u8::from_str_radix(std::str::from_utf8(p).unwrap(),16).unwrap()).collect()}
fn main(){
 let args:Vec<String>=std::env::args().collect();assert_eq!(args.len(),2);let raw=std::fs::read(&args[1]).unwrap();let packet=parse_json(&raw).unwrap();let mut objects=BTreeMap::new();let mut blobs=BTreeMap::new();
 for row in array(field(&packet,"objects")){let id=text(field(row,"id")).to_owned();let value=ObjectInput{domain:D::parse(text(field(row,"domain"))).unwrap(),descriptor:field(row,"descriptor").clone()};assert!(objects.insert(id,value).is_none());}
 for row in array(field(&packet,"blobs")){let key:[u8;32]=hex(text(field(row,"sha256"))).try_into().unwrap();assert!(blobs.insert(key,hex(text(field(row,"hex")))).is_none());}
 let registry=opensip_host::embedded_schema_registry().unwrap();let retained=RetainedInputs::new(&registry,&objects,&blobs);let run_id=text(field(&packet,"runId"));
 let work=TraversalBudget{steps:100_000_000,depth:96,descriptor_work:100_000_000};let limits=ReplayLimits{retained:RetainedWalkLimits{walk:work,owner:work,owner_invocations:1_000_000},capture_entries:1_000_000,retained_bytes:256*1024*1024};
 let start=Instant::now();let run=replay_run(&retained,run_id,limits).expect("synthetic complete native replay");let elapsed=start.elapsed().as_nanos();assert_eq!(run.run_id(),run_id);
 let findings=array(field(run.proof(),"findingIds")).len();
 println!("{{\"standing\":\"synthetic native complete replay; no qualification\",\"completeReplayNanos\":{elapsed},\"objects\":{},\"blobs\":{},\"findings\":{findings},\"fullReplayPassed\":true}}",objects.len(),blobs.len());
}
