use super::*;

fn unhex(text: &str) -> Vec<u8> {
    assert_eq!(text.len() % 2, 0);
    (0..text.len() / 2)
        .map(|i| u8::from_str_radix(&text[i * 2..i * 2 + 2], 16).unwrap())
        .collect()
}

#[test]
fn exact_reviewed_dt_md1_cbor_and_raw_digest_vectors() {
    let fixture: serde_json::Value = serde_json::from_slice(include_bytes!(
        "dependency_transport_digest/fixtures/vectors.json"
    ))
    .unwrap();
    for vector in fixture["vectors"].as_array().unwrap() {
        let rows = vector["entries"].as_array().unwrap();
        let paths: Vec<_> = rows
            .iter()
            .map(|row| LogicalPath::parse(row["path"].as_str().unwrap()).unwrap())
            .collect();
        let entries: Vec<_> = rows
            .iter()
            .zip(&paths)
            .map(|(row, path)| Entry {
                package_key: row["packageKey"].as_str().unwrap(),
                path,
                byte_length: row["byteLength"].as_u64().unwrap(),
                content_sha256: unhex(row["contentSha256"].as_str().unwrap())
                    .try_into()
                    .unwrap(),
            })
            .collect();
        let actual = compute(&entries).unwrap();
        assert_eq!(
            actual.canonical_entries,
            unhex(vector["cborHex"].as_str().unwrap())
        );
        assert_eq!(
            digest_hex(&actual.manifest_sha256),
            vector["manifestSha256"].as_str().unwrap()
        );
    }
}

#[test]
fn supplied_sequence_duplicates_and_all_uint64_bits_are_preserved() {
    let a = LogicalPath::parse("a.rs").unwrap();
    let z = LogicalPath::parse("z.rs").unwrap();
    let pkg = "pkg1-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    let entry = |path| Entry {
        package_key: pkg,
        path,
        byte_length: u64::MAX,
        content_sha256: [0xab; 32],
    };
    let forward = compute(&[entry(&a), entry(&z)]).unwrap();
    let reverse = compute(&[entry(&z), entry(&a)]).unwrap();
    assert_ne!(forward.manifest_sha256, reverse.manifest_sha256);
    assert_eq!(forward.canonical_entries[0], 0x82);
    assert!(
        forward
            .canonical_entries
            .windows(9)
            .any(|b| b == [0x1b, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
    );
    let duplicate = compute(&[entry(&a), entry(&a)]).unwrap();
    assert_eq!(duplicate.canonical_entries[0], 0x82);
    assert_ne!(
        duplicate.manifest_sha256,
        compute(&[entry(&a)]).unwrap().manifest_sha256
    );
    // Hashing an inert duplicate is not entry admission; the transport owner must refuse it.
}
