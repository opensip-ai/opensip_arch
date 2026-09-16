use opensip_named_contracts_trial::generated::output::Envelope4Root;
fn main() {
 let raw=std::fs::read("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/metadata-v2/fixtures.json").unwrap();
 let fixtures:serde_json::Value=serde_json::from_slice(&raw).unwrap();
 let expected:serde_json::Value=serde_json::from_slice(&std::fs::read("/tmp/opensip-implementation/m1-ts-runtime-subject-02/schema-differential-02.json").unwrap()).unwrap();
 let mut checked=0;
 for (i,case) in fixtures["cases"].as_array().unwrap().iter().enumerate() {
  if expected["expected"][i]["shape"] != true { continue; }
  let dto:Envelope4Root=serde_json::from_value(case["value"].clone()).unwrap();
  let roundtrip=serde_json::to_value(&dto).unwrap();
  assert_eq!(roundtrip,case["value"],"case {}",case["id"]); checked+=1;
 }
 println!("{} shape-valid metadata carrier roundtrips",checked);
}
