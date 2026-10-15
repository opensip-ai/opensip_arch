// M3-B unit B2-b4b1 (B2-b4 plan r4 section 2.1): the `libc` sizes the T2
// census's byte model names, asserted against this build. The security
// crate cannot name `libc`; its own test asserts the rest of the inventory
// (`custody/discovery_census_tests.rs`). The census records are generated
// with one key per line (`"name": size`).
#![cfg(target_os = "macos")]
const RECORDS: [(&str, &str); 2] = [
    (
        "discovery_census.json",
        include_str!("../../security/src/custody/discovery_census.json"),
    ),
    (
        "discovery_census_vectors.json",
        include_str!("../../security/src/custody/discovery_census_vectors.json"),
    ),
];

#[test]
fn the_census_libc_sizes_match_the_build() {
    let sizes = [
        ("libc::stat", std::mem::size_of::<libc::stat>()),
        ("libc::attrlist", std::mem::size_of::<libc::attrlist>()),
        ("libc::statfs", std::mem::size_of::<libc::statfs>()),
    ];
    for (record, text) in RECORDS {
        for (name, size) in sizes {
            assert_eq!(recorded(text, name), Some(size), "{record}: {name}");
        }
    }
}

/// The one size recorded under `name`: its key, then an unsigned integer
/// that is the whole JSON value (r2, Codex B2B4B1-R1-RF-1): no sign,
/// fraction or exponent, followed only by whitespace and `,` or `}`.
fn recorded(text: &str, name: &str) -> Option<usize> {
    let key = format!("\"{name}\":");
    let mut hits = text.match_indices(&key);
    let (at, _) = hits.next()?;
    assert!(
        hits.next().is_none(),
        "{name} is recorded twice in one record"
    );
    let rest = text[at + key.len()..].trim_start();
    let end = rest
        .find(|c: char| !c.is_ascii_digit())
        .unwrap_or(rest.len());
    let (digits, after) = rest.split_at(end);
    if digits.is_empty() || (digits.len() > 1 && digits.starts_with('0')) {
        return None;
    }
    if !(after.trim_start().starts_with(',') || after.trim_start().starts_with('}')) {
        return None;
    }
    digits.parse().ok()
}

#[test]
fn only_a_whole_unsigned_integer_is_a_recorded_size() {
    let at = |value: &str| recorded(&format!("{{\n \"libc::stat\": {value}\n}}"), "libc::stat");
    assert_eq!(at("144"), Some(144));
    assert_eq!(
        recorded("{\"libc::stat\":144,\"x\":1}", "libc::stat"),
        Some(144)
    );
    for refused in [
        "144.5", "144e9", "144E9", "144abc", "-144", "+144", "0144", "\"144\"", "", "1440x",
    ] {
        assert_eq!(at(refused), None, "{refused}");
    }
}
