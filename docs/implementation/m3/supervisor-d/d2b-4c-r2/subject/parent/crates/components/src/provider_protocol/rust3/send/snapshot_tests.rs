//! Inert sealed-inventory projections; byte custody is exercised by sender
//! controls, not established by these manifest/coordinate controls.
use super::*;
use opensip_identity::{digest_hex, raw_sha256};
fn snapshot() -> String {
    format!("snapshot2:{}", "1".repeat(64))
}
fn file(path: &str, length: u64) -> Entry {
    Entry::File {
        path: path.into(),
        byte_length: length,
        content_sha256: "a".repeat(64),
        executable: false,
    }
}
fn member<'a>(v: &'a Value, key: &str) -> &'a Value {
    let Value::Map(v) = v else { panic!() };
    v.iter().find(|(k, _)| k == key).map(|(_, v)| v).unwrap()
}

#[test]
fn snapshot_manifest_digest_and_seal_preserve_exact_file_and_link_types() {
    let policy = Policy::load().unwrap();
    let maximum = policy.limit("maxSnapshotChunkBytes").unwrap();
    let entries = vec![
        file("src/a.rs", 0),
        Entry::File {
            path: "src/b.rs".into(),
            byte_length: maximum + 1,
            content_sha256: "b".repeat(64),
            executable: true,
        },
        Entry::Symlink {
            path: "src/link".into(),
            target_bytes: vec![0xff, 0x00, b'a'],
        },
    ];
    let built = build(&policy, &snapshot(), &entries, 2).unwrap();
    let expected = Value::Array(vec![
        map(vec![
            ("path", t("src/a.rs")),
            ("kind", t("file")),
            ("byteLength", Value::Unsigned(0)),
            ("contentSha256", t(&"a".repeat(64))),
            ("executable", Value::Bool(false)),
            ("targetBytes", Value::Null),
        ]),
        map(vec![
            ("path", t("src/b.rs")),
            ("kind", t("file")),
            ("byteLength", Value::Unsigned(1_048_577)),
            ("contentSha256", t(&"b".repeat(64))),
            ("executable", Value::Bool(true)),
            ("targetBytes", Value::Null),
        ]),
        map(vec![
            ("path", t("src/link")),
            ("kind", t("symlink")),
            ("byteLength", Value::Null),
            ("contentSha256", Value::Null),
            ("executable", Value::Null),
            ("targetBytes", Value::Bytes(vec![0xff, 0x00, b'a'])),
        ]),
    ]);
    assert_eq!(member(&built.manifest, "entries"), &expected);
    let independent = digest_hex(&raw_sha256(&cbor::encode(&expected)));
    assert_eq!(member(&built.manifest, "manifestSha256"), &t(&independent));
    assert_eq!(member(&built.seal, "manifestSha256"), &t(&independent));
    assert_eq!(member(&built.seal, "entryCount"), &Value::Unsigned(3));
    assert_eq!(
        member(&built.seal, "totalFileBytes"),
        &Value::Unsigned(maximum + 1)
    );
    assert_eq!(member(&built.seal, "totalChunkCount"), &Value::Unsigned(2));
    assert_eq!((built.bytes, built.chunks), (maximum + 1, 2));
}

#[test]
fn snapshot_full_envelope_sizing_matches_cbor_heads_and_inclusive_bound() {
    for length in [1, 23, 24, 255, 256, 65_535, 65_536] {
        for sequence in [23, 24] {
            let mut policy = Policy::load().unwrap();
            let entries = vec![Entry::Symlink {
                path: "link".into(),
                target_bytes: vec![0xff; length],
            }];
            let built = build(&policy, &snapshot(), &entries, sequence).unwrap();
            let size = cbor::encode(&schedule::envelope(
                sequence,
                "SnapshotManifest",
                built.manifest,
            ))
            .len() as u64;
            policy.limits.insert("maxFramePayloadBytes".into(), size);
            assert!(build(&policy, &snapshot(), &entries, sequence).is_ok());
            policy
                .limits
                .insert("maxFramePayloadBytes".into(), size - 1);
            assert!(matches!(
                build(&policy, &snapshot(), &entries, sequence),
                Err(Refusal::Bound("snapshot manifest envelope"))
            ));
        }
    }
}

#[test]
fn snapshot_order_paths_count_and_checked_totals_refuse_before_manifest() {
    let mut policy = Policy::load().unwrap();
    assert!(build(&policy, &snapshot(), &[], 2).is_err());
    for entries in [
        vec![file("b", 1), file("a", 1)],
        vec![file("a", 1), file("a", 1)],
        vec![file("../outside", 1)],
        vec![Entry::Symlink {
            path: "link".into(),
            target_bytes: vec![],
        }],
    ] {
        assert!(build(&policy, &snapshot(), &entries, 2).is_err());
    }
    assert!(build(&policy, "not-snapshot2", &[file("a", 1)], 2).is_err());
    let maximum = policy.limit("maxSnapshotTotalFileBytes").unwrap();
    let built = build(&policy, &snapshot(), &[file("a", maximum)], 2).unwrap();
    assert_eq!(built.bytes, maximum);
    assert_eq!(built.chunks, 8192);
    assert!(matches!(
        build(&policy, &snapshot(), &[file("a", maximum), file("b", 1)], 2),
        Err(Refusal::Bound("snapshot file bytes"))
    ));
    policy.limits.insert("maxSnapshotEntries".into(), 1);
    assert!(build(&policy, &snapshot(), &[file("a", 0), file("b", 0)], 2).is_err());
    // Make only the arithmetic guard reachable: original production bounds
    // already refuse the first entry, without allocating declared bytes.
    policy.limits.insert("maxSnapshotEntries".into(), 200_000);
    policy
        .limits
        .insert("maxSnapshotTotalFileBytes".into(), u64::MAX);
    assert!(matches!(
        build(
            &policy,
            &snapshot(),
            &[file("a", u64::MAX), file("b", 1)],
            2
        ),
        Err(Refusal::Arithmetic)
    ));
}

#[test]
fn snapshot_chunks_are_exact_greedy_file_coordinates_and_never_link_or_empty() {
    let policy = Policy::load().unwrap();
    let max = policy.limit("maxSnapshotChunkBytes").unwrap();
    let entry = file("src/a.rs", max + 1);
    let first = chunk(&policy, &snapshot(), &entry, 0, 0, vec![3; max as usize]).unwrap();
    assert_eq!(member(&first, "byteOffset"), &Value::Unsigned(0));
    let last = chunk(&policy, &snapshot(), &entry, 1, max, vec![4]).unwrap();
    assert_eq!(member(&last, "bytes"), &Value::Bytes(vec![4]));
    for (index, offset, bytes) in [
        (0, 0, vec![0]),
        (1, max - 1, vec![0]),
        (2, 2 * max, vec![0]),
        (u64::MAX, 0, vec![0]),
        (1, max, vec![]),
    ] {
        assert!(chunk(&policy, &snapshot(), &entry, index, offset, bytes).is_err());
    }
    assert!(chunk(&policy, &snapshot(), &file("empty", 0), 0, 0, vec![]).is_err());
    let link = Entry::Symlink {
        path: "link".into(),
        target_bytes: vec![1],
    };
    assert!(chunk(&policy, &snapshot(), &link, 0, 0, vec![1]).is_err());
}
