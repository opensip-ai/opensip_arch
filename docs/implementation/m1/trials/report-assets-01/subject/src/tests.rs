use super::*;
use opensip_identity::digest_hex;
use std::io::Cursor;

const ROOT: &str = "share/report";
const MANIFEST: &str = "share/report/manifest.json";
const ASSET: &str = "share/report/report.js";
const SCHEMA: [u8; 32] = [0x12; 32];

#[derive(Default)]
struct MemorySource {
    files: BTreeMap<String, Vec<u8>>,
    opens: Vec<String>,
}
impl AssetSource for MemorySource {
    type Reader = Cursor<Vec<u8>>;
    fn open_regular(&mut self, path: &str) -> io::Result<Self::Reader> {
        self.opens.push(path.into());
        self.files
            .get(path)
            .cloned()
            .map(Cursor::new)
            .ok_or(io::ErrorKind::NotFound.into())
    }
}

fn row(path: &str, data: &[u8], role: &str) -> String {
    format!(
        r#"{{"path":"{path}","sha256":"{}","bytes":{},"role":"{role}"}}"#,
        digest_hex(&raw_sha256(data)),
        data.len()
    )
}
fn document(rows: &str) -> String {
    format!(
        r#"{{"schemaVersion":1,"projectionSchemaSha256s":["{}"],"assets":[{rows}]}}"#,
        digest_hex(&SCHEMA)
    )
}
fn fixture(raw: String) -> (MemorySource, FixturePin) {
    let pin = FixturePin {
        root: ROOT.into(),
        manifest_path: MANIFEST.into(),
        manifest_bytes: raw.len() as u64,
        manifest_sha256: raw_sha256(raw.as_bytes()),
    };
    let mut source = MemorySource::default();
    source.files.insert(MANIFEST.into(), raw.into_bytes());
    source
        .files
        .insert(ASSET.into(), b"console.log('offline');".to_vec());
    (source, pin)
}
fn baseline() -> String {
    document(&row(ASSET, b"console.log('offline');", "script"))
}

#[test]
fn verified_owned_bytes_roles_and_zero_length_notice() {
    let mut rows = Vec::new();
    let names = ["a.js", "b.css", "c.woff", "d.png", "e.NOTICE"];
    let roles = ["script", "style", "font", "image", "notice"];
    for (name, role) in names.iter().zip(roles) {
        rows.push(row(&format!("{ROOT}/{name}"), b"", role));
    }
    let (mut source, pin) = fixture(document(&rows.join(",")));
    for name in names {
        source.files.insert(format!("{ROOT}/{name}"), Vec::new());
    }
    let assets = verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap();
    assert_eq!(
        assets
            .assets()
            .iter()
            .map(VerifiedAsset::role)
            .collect::<Vec<_>>(),
        [
            Role::Script,
            Role::Style,
            Role::Font,
            Role::Image,
            Role::Notice
        ]
    );
    assert!(assets.assets().iter().all(|a| a.bytes().is_empty()));
    // Changing source after verification cannot change the bytes handed to HTML.
    source
        .files
        .insert(format!("{ROOT}/a.js"), b"replacement".to_vec());
    assert_eq!(assets.assets()[0].bytes(), b"");
}

#[test]
fn raw_pin_precedes_parsing_and_any_member_open() {
    for change in ["long", "short", "same-length", "missing"] {
        let (mut source, pin) = fixture(baseline());
        let bytes = source.files.get_mut(MANIFEST).unwrap();
        match change {
            "long" => bytes.push(b' '),
            "short" => {
                bytes.pop();
            }
            "same-length" => bytes[0] = b'[',
            _ => {
                source.files.remove(MANIFEST);
            }
        }
        let result = verify_fixture_assets(&mut source, &pin, &SCHEMA);
        let error = match change {
            "same-length" => AssetError::Digest,
            "missing" => AssetError::Io,
            _ => AssetError::Length,
        };
        assert_eq!(result.unwrap_err(), error);
        assert_eq!(source.opens, [MANIFEST]);
    }
    let (mut source, mut pin) = fixture(baseline());
    pin.manifest_bytes = u64::MAX;
    assert_eq!(
        verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap_err(),
        AssetError::Length
    );
    assert!(source.opens.is_empty());
}

#[test]
fn lexical_closed_shape_and_order_refuse_before_member_access() {
    let base = baseline();
    let digest_text = digest_hex(&SCHEMA);
    let bad = [
        base.replace(
            "\"schemaVersion\":1",
            "\"schemaVersion\":1,\"schemaVersion\":1",
        ),
        base.replace("\"schemaVersion\":1", "\"schemaVersion\":1,\"extra\":null"),
        base.replace("\"schemaVersion\":1", "\"schemaVersion\":1.0"),
        base.replace("\"schemaVersion\":1", "\"schemaVersion\":1e0"),
        base.replace("\"schemaVersion\":1", "\"schemaVersion\":true"),
        base.replace("\"bytes\":23", "\"bytes\":-0"),
        base.replace("\"bytes\":23", "\"bytes\":9007199254740991"),
        base.replace("\"role\":\"script\"", "\"role\":\"url\""),
        base.replace("\"role\":\"script\"", "\"role\":\"script\",\"unknown\":0"),
        base.replace(
            &format!("[\"{digest_text}\"]"),
            &format!("[\"{digest_text}\",\"{digest_text}\"]"),
        ),
        base.replace(&format!("[\"{digest_text}\"]"), "[]"),
        document(&format!(
            "{},{}",
            row(ASSET, b"", "script"),
            row(ASSET, b"", "script")
        )),
        document(&format!(
            "{},{}",
            row("share/report/z", b"", "script"),
            row("share/report/a", b"", "style")
        )),
        document(""),
    ];
    for raw in bad {
        assert_ne!(
            raw, base,
            "negative fixture must actually change its positive control"
        );
        let (mut source, pin) = fixture(raw);
        assert!(verify_fixture_assets(&mut source, &pin, &SCHEMA).is_err());
        assert_eq!(source.opens, [MANIFEST]);
    }
}

#[test]
fn schema_compatibility_and_manifest_path_rules() {
    for path in [
        "share/report2/a",
        "share/report/../a",
        "share/report//a",
        "/share/report/a",
        "https://remote/a",
        "share/report/a/",
        "share/report/./a",
        "share/report/a\\\\b",
    ] {
        let (mut source, pin) = fixture(document(&row(path, b"", "script")));
        assert_eq!(
            verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap_err(),
            AssetError::Path,
            "{path}"
        );
        assert_eq!(source.opens, [MANIFEST]);
    }
    let (mut source, pin) = fixture(document(&row(MANIFEST, b"", "script")));
    assert_eq!(
        verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap_err(),
        AssetError::SelfListed
    );
    let (mut source, pin) = fixture(baseline());
    assert_eq!(
        verify_fixture_assets(&mut source, &pin, &[0; 32]).unwrap_err(),
        AssetError::Incompatible
    );
    assert_eq!(source.opens, [MANIFEST]);
}

#[test]
fn member_corruption_never_returns_a_partial_report() {
    for change in ["long", "short", "corrupt", "missing"] {
        let (mut source, pin) = fixture(baseline());
        match change {
            "long" => source.files.get_mut(ASSET).unwrap().push(0),
            "short" => {
                source.files.get_mut(ASSET).unwrap().pop();
            }
            "corrupt" => source.files.get_mut(ASSET).unwrap()[0] ^= 1,
            _ => {
                source.files.remove(ASSET);
            }
        }
        assert!(verify_fixture_assets(&mut source, &pin, &SCHEMA).is_err());
    }
    let (mut source, pin) = fixture(baseline());
    let result = verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap();
    assert_eq!(result.assets()[0].path(), ASSET);
    assert_eq!(result.assets()[0].bytes(), b"console.log('offline');");
}

#[test]
fn completeness_excludes_exactly_one_manifest_file() {
    let (mut source, pin) = fixture(baseline());
    let result = verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap();
    let valid = vec![MANIFEST.into(), ASSET.into()];
    assert_eq!(fixture_completeness(&result, &valid), Ok(()));
    for extra in [
        "share/report/manifest.json.bak",
        "share/report/sub/manifest.json",
        ASSET,
        MANIFEST,
    ] {
        let mut paths = valid.clone();
        paths.push(extra.into());
        assert_eq!(
            fixture_completeness(&result, &paths),
            Err(AssetError::Unlisted)
        );
    }
    assert_eq!(
        fixture_completeness(&result, &[ASSET.into()]),
        Err(AssetError::Unlisted)
    );
}

#[test]
fn stream_reader_caps_actual_consumption_and_retries_interrupt() {
    struct Endless {
        count: u64,
        interrupt: bool,
    }
    impl Read for Endless {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            if self.interrupt {
                self.interrupt = false;
                return Err(io::ErrorKind::Interrupted.into());
            }
            self.count += buf.len() as u64;
            buf.fill(0);
            Ok(buf.len())
        }
    }
    for expected in [0, 1, 16_384, 17_000] {
        let mut reader = Endless {
            count: 0,
            interrupt: true,
        };
        assert_eq!(
            checked_read(&mut reader, expected, &[0; 32]).unwrap_err(),
            AssetError::Length
        );
        assert_eq!(reader.count, expected + 1);
    }
    assert_eq!(
        checked_read(Cursor::new([]), MAX_LENGTH, &[0; 32]).unwrap_err(),
        AssetError::Length
    );
}
