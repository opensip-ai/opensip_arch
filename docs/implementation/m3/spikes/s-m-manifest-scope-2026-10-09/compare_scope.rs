#[allow(dead_code)]
#[path="rust_scope_data.rs"]
mod scope;
use opensip_identity::{JsonValue as V,JsonInteger,LogicalPath,canonical_bytes,digest_hex,raw_sha256};
use serde_json::Value as J;
use std::collections::BTreeMap;
fn inert(v:&J)->V {match v {
 J::Null=>V::Null,J::Bool(b)=>V::Bool(*b),J::String(s)=>V::String(s.clone()),
 J::Number(n)=>V::Integer(JsonInteger::new(if let Some(u)=n.as_u64(){i128::from(u)}else{i128::from(n.as_i64().unwrap())}).unwrap()),
 J::Array(a)=>V::Array(a.iter().map(inert).collect()),J::Object(o)=>V::Object(o.iter().map(|(k,v)|(k.clone(),inert(v))).collect()),
}}
fn number(n:u64)->V {V::Integer(JsonInteger::new(i128::from(n)).unwrap())}
fn sha(s:&str)->[u8;32] {assert_eq!(s.len(),64);std::array::from_fn(|i|u8::from_str_radix(&s[i*2..i*2+2],16).unwrap())}
fn main(){
 let path=std::env::args().nth(1).unwrap();let j:J=serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();let rows=j["manifestEntries"].as_array().unwrap();
 let paths:Vec<_>=rows.iter().map(|r|LogicalPath::parse(r["path"].as_str().unwrap()).unwrap()).collect();
 let entries:Vec<_>=rows.iter().zip(&paths).map(|(r,path)|scope::Entry {kind:r["kind"].as_str().unwrap(),path,byte_length:r["byteLength"].as_u64(),content_sha256:r["contentSha256"].as_str().map(sha)}).collect();

 let start=std::time::Instant::now();let data=scope::rebuild(j["snapshotId"].as_str().unwrap(),&entries).unwrap();
 let elapsed=u64::try_from(start.elapsed().as_nanos()).unwrap();let out=V::Object(BTreeMap::from([
 ("elapsedNanos".into(),number(elapsed)),("subjects".into(),data.subjects),("subjectCount".into(),number(data.subject_count)),
 ("subjectScopeCommitment".into(),V::String(data.subject_scope_commitment)),
 ("subjectsCborBytes".into(),number(data.canonical_subjects.len()as u64)),("subjectsCborRawSha256".into(),V::String(digest_hex(&raw_sha256(&data.canonical_subjects))))]));
 println!("{}",String::from_utf8(canonical_bytes(&out).unwrap()).unwrap());
}
