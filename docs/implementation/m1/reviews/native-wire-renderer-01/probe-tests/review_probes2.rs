//! Reviewer scratch probe: required null versus empty map/array through serde buffering.
use opensip_native_wire_carrier_trial::wire::*;

fn show<T, E: std::fmt::Display>(label: &str, r: Result<T, E>) {
    match r { Ok(_) => println!("ACCEPT  {label}"), Err(e) => println!("refuse  {label}: {e}") }
}

#[test]
fn observe_required_null_empty_containers() {
    for v in ["null", "{}", "[]"] {
        show(&format!("tagged Ts2 file linkTarget {v}"), serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"file","path":"a","byteLength":1,"contentSha256":"b","linkTarget":{v}}}"#)));
        show(&format!("tagged Ts2 symlink contentSha256 {v}"), serde_json::from_str::<Ts2SnapshotEntryV1>(&format!(r#"{{"kind":"symlink","path":"a","byteLength":1,"contentSha256":{v},"linkTarget":"t"}}"#)));
        show(&format!("flat Option executionId {v}"), serde_json::from_str::<Ts2CancelledV1>(&format!(r#"{{"executionId":{v},"analysisOrdinal":null,"observedPhase":"snapshot"}}"#)));
    }
    let parsed: Ts2SnapshotEntryV1 = serde_json::from_str(r#"{"kind":"file","path":"a","byteLength":1,"contentSha256":"b","linkTarget":{}}"#).unwrap();
    println!("reserialized: {}", serde_json::to_string(&parsed).unwrap());
}
