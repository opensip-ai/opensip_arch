use super::*;
use opensip_identity::{LogicalPath, parse_hash_preimage};
fn record(path: &str, content: &[u8]) -> FileRecord {
    FileRecord {
        path: LogicalPath::parse(path).unwrap(),
        content_sha256: raw_sha256(content),
        byte_length: content.len() as u64,
    }
}
#[test]
fn independently_generated_complete_arrays_and_both_recipes_match() {
    let vectors: serde_json::Value =
        serde_json::from_str(include_str!("native_file_manifest/fixtures/golden.json")).unwrap();
    for vector in vectors.as_array().unwrap() {
        let files: Vec<_> = vector["files"]
            .as_array()
            .unwrap()
            .iter()
            .map(|r| FileRecord {
                path: LogicalPath::parse(r["path"].as_str().unwrap()).unwrap(),
                content_sha256: [r["digestByte"].as_u64().unwrap() as u8; 32],
                byte_length: r["byteLength"].as_u64().unwrap(),
            })
            .collect();
        let result = build(&files).unwrap();
        assert_eq!(
            result.canonical_array,
            vector["canonical"].as_str().unwrap().as_bytes()
        );
        assert_eq!(
            digest_hex(&result.raw_array_sha256),
            vector["rawArraySha256"].as_str().unwrap()
        );
        assert_eq!(
            digest_hex(&result.native_manifest_sha256),
            vector["nativeManifestSha256"].as_str().unwrap()
        );
        assert_ne!(result.raw_array_sha256, result.native_manifest_sha256);
        assert_eq!(
            canonical_bytes(
                &parse_hash_preimage("native.dependency-file-manifest.v1", &result.native_frame)
                    .unwrap()
            )
            .unwrap(),
            result.canonical_array
        );
        assert_eq!(result.file_count, files.len() as u64);
    }
}
#[test]
fn ordering_uses_raw_utf8_without_unicode_normalization_or_input_mutation() {
    let files = vec![
        record("é", b"a"),
        record("z", b"b"),
        record("e\u{301}", b"c"),
    ];
    let first = build(&files).unwrap();
    let second = build(&[
        record("e\u{301}", b"c"),
        record("é", b"a"),
        record("z", b"b"),
    ])
    .unwrap();
    assert_eq!(first.native_frame, second.native_frame);
    assert_eq!(first.file_count, 3);
    assert_eq!(first.total_bytes, 3);
    assert_eq!(files[0].path.as_str(), "é");
    let rows = opensip_identity::parse_json(&first.canonical_array).unwrap();
    let JsonValue::Array(rows) = rows else {
        panic!("not complete array")
    };
    let paths: Vec<_> = rows
        .iter()
        .map(|r| {
            let JsonValue::Object(o) = r else {
                panic!("not row")
            };
            let JsonValue::String(p) = &o["path"] else {
                panic!("not path")
            };
            p.as_str()
        })
        .collect();
    assert_eq!(paths, ["e\u{301}", "z", "é"]);
}
#[test]
fn duplicate_paths_refuse_even_with_different_bytes_and_lengths() {
    for rhs in [b"a".as_slice(), b"different".as_slice()] {
        assert!(matches!(
            build(&[record("same", b"a"), record("same", rhs)]),
            Err(ManifestError::DuplicatePath)
        ));
    }
}
#[test]
fn exact_u64_lengths_and_wide_total_are_not_floats_or_narrowed() {
    let mut a = record("a", b"");
    let mut b = record("b", b"");
    a.byte_length = u64::MAX;
    b.byte_length = u64::MAX;
    let data = build(&[a, b]).unwrap();
    assert_eq!(data.total_bytes, 2 * u128::from(u64::MAX));
    assert_eq!(
        String::from_utf8(data.canonical_array)
            .unwrap()
            .matches("18446744073709551615")
            .count(),
        2
    );
    // These deliberately supplied scalar lengths are not physical giant files.
}
#[test]
fn complete_canonical_array_accepts_exact_limit_and_never_splits_one_over() {
    const ROW: &str = r#"{"byteLength":0,"contentSha256":"0000000000000000000000000000000000000000000000000000000000000000","path":"f00000"}"#;
    let stride = ROW.len() + 1;
    let count = (opensip_identity::MAX_BYTES - 1) / stride;
    let extra = (opensip_identity::MAX_BYTES - 1) % stride;
    let mut files: Vec<_> = (0..count)
        .map(|i| FileRecord {
            path: LogicalPath::parse(&format!("f{i:05}")).unwrap(),
            content_sha256: [0; 32],
            byte_length: 0,
        })
        .collect();
    files[0].path = LogicalPath::parse(&format!("f00000{}", "z".repeat(extra))).unwrap();
    let exact = build(&files).unwrap();
    assert_eq!(exact.canonical_array.len(), opensip_identity::MAX_BYTES);
    assert_eq!(exact.file_count, count as u64);
    files[0].path = LogicalPath::parse(&format!("f00000{}", "z".repeat(extra + 1))).unwrap();
    assert!(matches!(
        build(&files),
        Err(ManifestError::Canonical(
            opensip_identity::CanonicalError::ByteLimit
        ))
    ));
}
struct Receiver;
impl crate::archive_decoder::ArchiveConsumer for Receiver {
    type Error = ();
    fn checkpoint(&mut self) -> Result<(), ()> {
        Ok(())
    }
    fn begin(&mut self, _: &LogicalPath, _: u128) -> Result<(), ()> {
        Ok(())
    }
    fn content(&mut self, _: &[u8]) -> Result<(), ()> {
        Ok(())
    }
    fn end(&mut self, _: &FileRecord) -> Result<(), ()> {
        Ok(())
    }
}
#[test]
fn actual_archive_decoder_file_observations_feed_complete_plain_manifest_data() {
    let bytes = include_bytes!("archive_decoder/fixtures/base.tar.gz");
    let archive =
        crate::archive_decoder::decode(bytes.as_slice(), "unit", "1.0.0", &mut Receiver).unwrap();
    let manifest = build(&archive.files).unwrap();
    assert_eq!(manifest.file_count, 3);
    assert_eq!(manifest.total_bytes, 17);
    assert_ne!(manifest.raw_array_sha256, archive.compressed_sha256);
    assert_ne!(manifest.native_manifest_sha256, archive.compressed_sha256);
    assert_ne!(manifest.raw_array_sha256, manifest.native_manifest_sha256);
    assert_eq!(
        manifest.raw_array_sha256,
        raw_sha256(&manifest.canonical_array)
    );
    assert_eq!(
        manifest.native_manifest_sha256,
        raw_sha256(&manifest.native_frame)
    );
    // Small actual decoder bytes and manifest data do not grant tree custody,
    // native descriptor admission, source provenance or activation.
}
