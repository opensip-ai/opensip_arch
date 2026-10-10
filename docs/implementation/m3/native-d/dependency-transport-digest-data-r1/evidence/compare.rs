#[allow(dead_code)]
#[path="/Users/sb/code/opensip-ai/opensip-dtmd1/crates/host/src/rust_scope_data.rs"]
mod rust_scope_data;
#[allow(dead_code)]
#[path="/Users/sb/code/opensip-ai/opensip-dtmd1/crates/host/src/dependency_transport_digest.rs"]
mod dependency_transport_digest;
use opensip_identity::{LogicalPath,digest_hex};
fn main(){
 let p=std::env::args().nth(1).unwrap();let v:serde_json::Value=serde_json::from_slice(&std::fs::read(p).unwrap()).unwrap();let rows=v.as_array().unwrap();
 let paths:Vec<_>=rows.iter().map(|r|LogicalPath::parse(r["path"].as_str().unwrap()).unwrap()).collect();
 let entries:Vec<_>=rows.iter().zip(&paths).map(|(r,path)|{let s=r["contentSha256"].as_str().unwrap();assert_eq!(s.len(),64);dependency_transport_digest::Entry{package_key:r["packageKey"].as_str().unwrap(),path,byte_length:r["byteLength"].as_u64().unwrap(),content_sha256:std::array::from_fn(|i|u8::from_str_radix(&s[i*2..i*2+2],16).unwrap())}}).collect();
 let r=dependency_transport_digest::compute(&entries).unwrap();println!("{}",serde_json::json!({"entries":entries.len(),"cborBytes":r.canonical_entries.len(),"cborHex":r.canonical_entries.iter().map(|b|format!("{b:02x}")).collect::<String>(),"manifestSha256":digest_hex(&r.manifest_sha256)}));
}
