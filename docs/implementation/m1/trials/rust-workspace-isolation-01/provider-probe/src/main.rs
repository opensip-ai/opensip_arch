// Disposable M1 shared-library build probe, not a provider implementation.
fn main() {
    let input = br#"{ "z":2, "a":1 }"#;
    let value = opensip_identity::parse_json(input).expect("probe input");
    assert_eq!(opensip_identity::canonical_bytes(&value).expect("probe canonical"), br#"{"a":1,"z":2}"#);
    println!("isolated shared-library probe passed");
}
