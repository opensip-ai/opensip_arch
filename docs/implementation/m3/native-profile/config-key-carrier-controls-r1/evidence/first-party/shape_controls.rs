use opensip_identity::{JsonValue, RegisteredSchemas, parse_json};
fn main() {
 let root=std::path::PathBuf::from(std::env::args_os().nth(1).expect("product root"));
 let cases=std::fs::read(std::env::args_os().nth(2).expect("cases")).unwrap();
 let sources:Vec<Vec<u8>>=RegisteredSchemas::source_requirements().iter().map(|p| std::fs::read(root.join(p.source_path())).unwrap()).collect();
 let borrowed:Vec<&[u8]>=sources.iter().map(Vec::as_slice).collect();
 let registry=RegisteredSchemas::from_sources(&borrowed).expect("exact complete current source registry");
 let JsonValue::Array(cases)=parse_json(&cases).unwrap()else{panic!("cases array")};
 let id=RegisteredSchemas::source_requirements().iter().find(|p|p.source_path()=="schemas/sources/native-v2.schema.json").unwrap().schema_id();
 for case in cases {
  let JsonValue::Object(case)=case else {panic!("case object")};
  let JsonValue::String(name)=&case["case"] else {panic!("case name")};
  let JsonValue::Bool(expected)=&case["expectedValid"] else {panic!("expected Boolean")};
  let bytes=opensip_identity::canonical_bytes(&case["record"]).unwrap();
  let observed=registry.schema(id,"/$defs/CargoConfigProjectionV2").unwrap().admit_json(&bytes,200_000_000);
  assert_eq!(observed.is_ok(),*expected,"{name}: {:?}",observed.err());
  println!("PASS {name}");
 }
}
