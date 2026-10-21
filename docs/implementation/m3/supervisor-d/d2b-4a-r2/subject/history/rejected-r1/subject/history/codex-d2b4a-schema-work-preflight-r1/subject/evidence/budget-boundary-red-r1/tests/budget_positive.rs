use opensip_components::provider_protocol::{cbor::{self, Value}, rust3::Rust3PayloadSchemas, MAX_FRAME_PAYLOAD_BYTES};
use opensip_identity::{JsonValue as J, parse_json};
fn wire(v: &J) -> Value {
    match v {
        J::Null => Value::Null, J::Bool(x) => Value::Bool(*x),
        J::Integer(x) => Value::Unsigned(u64::try_from(x.get()).unwrap()),
        J::String(x) => Value::Text(x.clone()),
        J::Array(xs) => Value::Array(xs.iter().map(wire).collect()),
        J::Object(xs) => Value::Map(xs.iter().map(|(k,v)|(k.clone(),wire(v))).collect()),
    }
}
fn get_mut<'a>(v: &'a mut Value, name: &str) -> &'a mut Value {
    let Value::Map(fields) = v else { panic!("map") };
    &mut fields.iter_mut().find(|(k,_)|k==name).unwrap().1
}
#[test]
fn legal_wire_must_not_hit_an_unrelated_schema_work_cap() {
    let schemas = Rust3PayloadSchemas::load().unwrap();
    let fixture=parse_json(include_bytes!("/Users/sb/code/opensip-ai/opensip-d2b4a-takeover/crates/components/tests/data/rust3-startup-shape.v1.json")).unwrap();
    let J::Object(fields)=fixture else {panic!("fixture")};
    let mut value=wire(fields.get("universeAccepted").unwrap());
    let size=33_554_433;
    *get_mut(get_mut(&mut value,"universe"),"standardLibraryComponentDigests")=Value::Map(vec![("\0".repeat(size),Value::Text("a".repeat(64)))]);
    let raw=cbor::encode(&value);assert!((raw.len()as u64)<MAX_FRAME_PAYLOAD_BYTES);
    drop(value);
    let decoded=cbor::decode(&raw,cbor::Profile::Rust3,7).unwrap();
    let got=schemas.check_payload("UniverseAccepted",&decoded,"WAIT_UNIVERSE_ACCEPTED",false);
    println!("keyBytes={size} strictCborBytes={} schemaResult={got:?}",raw.len());
    assert!(got.is_ok(),"legal wire must not hit an unrelated schema work cap: {got:?}");
}
