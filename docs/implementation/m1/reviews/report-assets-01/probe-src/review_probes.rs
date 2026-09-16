//! Independent reviewer probes. Review copy only; never part of subject bytes.
use super::*;
use opensip_identity::{MAX_BYTES, digest_hex};
use std::io::Cursor;

const ROOT: &str = "share/report";
const MANIFEST: &str = "share/report/manifest.json";
const ASSET: &str = "share/report/report.js";
const DATA: &[u8] = b"console.log('offline');";
const OTHER_DATA: &[u8] = b"console.log('online!');";
const SCHEMA: [u8; 32] = [0x12; 32];

#[derive(Default)]
struct Mem {
    files: BTreeMap<String, Vec<u8>>,
    opens: Vec<String>,
    after_manifest: Option<(String, Vec<u8>)>,
}

impl AssetSource for Mem {
    type Reader = Cursor<Vec<u8>>;
    fn open_regular(&mut self, path: &str) -> io::Result<Self::Reader> {
        self.opens.push(path.into());
        let reader = self
            .files
            .get(path)
            .cloned()
            .map(Cursor::new)
            .ok_or(io::Error::from(io::ErrorKind::NotFound));
        if path == MANIFEST {
            if let Some((p, b)) = self.after_manifest.take() {
                self.files.insert(p, b);
            }
        }
        reader
    }
}

fn row(path: &str, data: &[u8], role: &str) -> String {
    format!(
        r#"{{"path":"{path}","sha256":"{}","bytes":{},"role":"{role}"}}"#,
        digest_hex(&raw_sha256(data)),
        data.len()
    )
}
fn doc(schemas: &[[u8; 32]], rows: &str) -> String {
    let list: Vec<String> = schemas
        .iter()
        .map(|s| format!("\"{}\"", digest_hex(s)))
        .collect();
    format!(
        r#"{{"schemaVersion":1,"projectionSchemaSha256s":[{}],"assets":[{rows}]}}"#,
        list.join(",")
    )
}
fn base() -> String {
    doc(&[SCHEMA], &row(ASSET, DATA, "script"))
}
fn pin_for(raw: &[u8]) -> FixturePin {
    FixturePin {
        root: ROOT.into(),
        manifest_path: MANIFEST.into(),
        manifest_bytes: raw.len() as u64,
        manifest_sha256: raw_sha256(raw),
    }
}
fn source(raw: &[u8]) -> Mem {
    let mut m = Mem::default();
    m.files.insert(MANIFEST.into(), raw.to_vec());
    m.files.insert(ASSET.into(), DATA.to_vec());
    m
}
fn run(raw: &[u8]) -> (Result<VerifiedBundle, AssetError>, Vec<String>) {
    let mut s = source(raw);
    let r = verify_fixture_assets(&mut s, &pin_for(raw), &SCHEMA);
    (r, s.opens)
}

#[test]
fn probe_valid_control_each_path_opened_once_manifest_first() {
    let (r, opens) = run(base().as_bytes());
    let b = r.unwrap();
    assert_eq!(opens, [MANIFEST, ASSET]);
    assert_eq!(b.assets().len(), 1);
    assert_eq!(b.assets()[0].bytes(), DATA);
    assert_eq!(b.manifest_sha256(), &raw_sha256(base().as_bytes()));
    // Whitespace and JSON escapes are admitted: the raw pin binds exact bytes.
    let spaced = format!(" \n{}\t\r\n", base());
    assert!(run(spaced.as_bytes()).0.is_ok());
    let escaped = base().replace(ASSET, "share\\/report\\u002freport.js");
    assert_ne!(escaped, base());
    let (r, opens) = run(escaped.as_bytes());
    assert!(r.is_ok());
    assert_eq!(opens, [MANIFEST, ASSET]);
    // Projection accepted in any sorted position.
    for schemas in [[[0x01; 32], SCHEMA], [SCHEMA, [0x13; 32]]] {
        let raw = doc(&schemas, &row(ASSET, DATA, "script"));
        assert!(run(raw.as_bytes()).0.is_ok(), "{schemas:?}");
    }
}

#[test]
fn probe_pin_admission_refuses_before_any_open() {
    let raw = base();
    let good = pin_for(raw.as_bytes());
    let mut cases: Vec<(FixturePin, AssetError)> = Vec::new();
    let long_root = "a".repeat(4097);
    for root in [
        "",
        "/share/report",
        "share/report/",
        "share//report",
        "share/./report",
        "share/../report",
        "share\\report",
        "c:/share",
        "share/re\0port",
        long_root.as_str(),
    ] {
        let mut p = good.clone();
        p.root = root.into();
        cases.push((p, AssetError::Path));
    }
    // Scheme-bearing root whose manifest is otherwise lexically under it.
    let mut p = good.clone();
    p.root = "https:".into();
    p.manifest_path = "https:/manifest.json".into();
    cases.push((p, AssetError::Path));
    for manifest in [
        "share/other/manifest.json",
        "share/report",
        "share/reportx/manifest.json",
        "manifest.json",
        "share/report/../report/manifest.json",
        "share/report/",
    ] {
        let mut p = good.clone();
        p.manifest_path = manifest.into();
        cases.push((p, AssetError::Path));
    }
    for bytes in [0, MAX_BYTES as u64 + 1, u64::MAX] {
        let mut p = good.clone();
        p.manifest_bytes = bytes;
        cases.push((p, AssetError::Length));
    }
    for (pin, expected) in cases {
        let mut s = source(raw.as_bytes());
        assert_eq!(
            verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
            expected,
            "{pin:?}"
        );
        assert!(s.opens.is_empty(), "{pin:?}");
    }
    let mut p = good.clone();
    p.manifest_bytes = MAX_BYTES as u64;
    let mut s = source(raw.as_bytes());
    assert_eq!(
        verify_fixture_assets(&mut s, &p, &SCHEMA).unwrap_err(),
        AssetError::Length
    );
    assert_eq!(s.opens, [MANIFEST]);
}

#[test]
fn probe_raw_pin_length_then_digest_bind_exact_stored_bytes() {
    let raw = base();
    let good = pin_for(raw.as_bytes());
    // Same-length, independently valid manifest never gets parsed under the wrong pin.
    let other = raw.replace("\"script\"", "\"notice\"");
    assert_eq!(other.len(), raw.len());
    assert!(run(other.as_bytes()).0.is_ok());
    let served: [(&[u8], FixturePin, AssetError); 6] = [
        (other.as_bytes(), good.clone(), AssetError::Digest),
        (raw.as_bytes(), pin_for(other.as_bytes()), AssetError::Digest),
        (
            raw.as_bytes(),
            FixturePin {
                manifest_bytes: good.manifest_bytes + 1,
                ..good.clone()
            },
            AssetError::Length,
        ),
        (
            raw.as_bytes(),
            FixturePin {
                manifest_bytes: good.manifest_bytes - 1,
                ..good.clone()
            },
            AssetError::Length,
        ),
        (b"", good.clone(), AssetError::Length),
        (
            format!("{raw} ").as_bytes().to_vec().leak(),
            good.clone(),
            AssetError::Length,
        ),
    ];
    for (bytes, pin, expected) in served {
        let mut s = source(bytes);
        assert_eq!(
            verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
            expected
        );
        assert_eq!(s.opens, [MANIFEST]);
    }
}

#[test]
fn probe_closed_shape_numeric_digest_role_path_order_matrix() {
    use AssetError::*;
    let b = base();
    let d = digest_hex(&SCHEMA);
    let asset_hex = digest_hex(&raw_sha256(DATA));
    assert!(asset_hex.bytes().any(|c| c.is_ascii_lowercase()));
    let long_ok = format!("{ROOT}/{}", "a".repeat(4096 - ROOT.len() - 1));
    let long_bad = format!("{ROOT}/{}", "a".repeat(4096 - ROOT.len()));
    let wide_ok = format!("{ROOT}/{}", "é".repeat(4096 - ROOT.len() - 1));
    assert_eq!(long_ok.chars().count(), 4096);
    assert_eq!(wide_ok.chars().count(), 4096);
    let deep = format!("{}{}", "[".repeat(40), "]".repeat(40));
    let one = |p: &str| doc(&[SCHEMA], &row(p, DATA, "script"));
    let two = |p: &str, q: &str| {
        doc(
            &[SCHEMA],
            &format!("{},{}", row(p, DATA, "script"), row(q, DATA, "script")),
        )
    };
    let sv = |v: &str| b.replace("\"schemaVersion\":1", &format!("\"schemaVersion\":{v}"));
    let role = |v: &str| b.replace("\"role\":\"script\"", v);
    let bytes = |v: &str| b.replace("\"bytes\":23", &format!("\"bytes\":{v}"));
    let upper_schema = doc(&[[0xab; 32]], &row(ASSET, DATA, "script")).replace("abab", "ABAB");
    // (document, error, second path opened if parsing admitted it)
    let cases: Vec<(String, AssetError, Option<String>)> = vec![
        ("[]".into(), Shape, None),
        ("{}".into(), Shape, None),
        ("null".into(), Shape, None),
        (b.replace("\"assets\"", "\"asset\""), Shape, None),
        (sv("2"), Shape, None),
        (sv("0"), Shape, None),
        (sv("\"1\""), Shape, None),
        (sv("01"), Shape, None),
        (sv("-1"), Shape, None),
        (sv("null"), Shape, None),
        (sv("18446744073709551616"), Shape, None),
        (format!("\u{feff}{b}"), Shape, None),
        (format!("{b}x"), Shape, None),
        (format!("{b}{b}"), Shape, None),
        (
            b.replace("\"schemaVersion\":1", &format!("\"schemaVersion\":1,\"x\":{deep}")),
            Shape,
            None,
        ),
        (
            format!(r#"{{"schemaVersion":1,"projectionSchemaSha256s":["{d}"],"assets":{{}}}}"#),
            Shape,
            None,
        ),
        (doc(&[SCHEMA], "[]"), Shape, None),
        (doc(&[SCHEMA], "null"), Shape, None),
        (doc(&[SCHEMA], ""), Shape, None),
        (role(""), Shape, None),
        (role("\"role\":\"script\",\"url\":\"x\""), Shape, None),
        (role("\"role\":\"script\",\"role\":\"script\""), Shape, None),
        (role("\"role\":\"Script\""), Shape, None),
        (role("\"role\":\"SCRIPT\""), Shape, None),
        (role("\"role\":\"script \""), Shape, None),
        (role("\"role\":\"license\""), Shape, None),
        (role("\"role\":\"\""), Shape, None),
        (role("\"role\":null"), Shape, None),
        (b.replace(",\"role\":\"script\"", ""), Shape, None),
        (bytes("\"23\""), Shape, None),
        (bytes("-1"), Shape, None),
        (bytes("-0"), Shape, None),
        (bytes("23.0"), Shape, None),
        (bytes("2.3e1"), Shape, None),
        (bytes("023"), Shape, None),
        (bytes("9007199254740991"), Shape, None),
        (bytes("18446744073709551615"), Shape, None),
        (bytes("9007199254740990"), Length, Some(ASSET.into())),
        (bytes("22"), Length, Some(ASSET.into())),
        (bytes("0"), Length, Some(ASSET.into())),
        (b.replace(&asset_hex, &asset_hex.to_uppercase()), Shape, None),
        (b.replace(&asset_hex, &asset_hex[..63]), Shape, None),
        (b.replace(&asset_hex, &format!("{asset_hex}0")), Shape, None),
        (b.replace(&asset_hex, &format!("g{}", &asset_hex[1..])), Shape, None),
        (b.replace(&asset_hex, &format!(" {}", &asset_hex[1..])), Shape, None),
        (b.replace(&format!("\"{asset_hex}\""), "1"), Shape, None),
        (b.replace(&asset_hex, &"0".repeat(64)), Digest, Some(ASSET.into())),
        (upper_schema, Shape, None),
        (b.replace(&format!("[\"{d}\"]"), &format!("\"{d}\"")), Shape, None),
        (doc(&[], &row(ASSET, DATA, "script")), Shape, None),
        (doc(&[[0x13; 32], SCHEMA], &row(ASSET, DATA, "script")), Order, None),
        (doc(&[SCHEMA, SCHEMA], &row(ASSET, DATA, "script")), Order, None),
        (
            doc(&[[0x01; 32], [0x13; 32]], &row(ASSET, DATA, "script")),
            Incompatible,
            None,
        ),
        (one(ROOT), Path, None),
        (one("share"), Path, None),
        (one("share/report/a\\u0000b"), Path, None),
        (one("share/report/a\\\\b"), Path, None),
        (one("share/report/.."), Path, None),
        (one("share/report/sub/./a"), Path, None),
        (one(&long_bad), Path, None),
        (one(&long_ok), Io, Some(long_ok.clone())),
        (one(&wide_ok), Io, Some(wide_ok.clone())),
        (
            one("share/report/https:x"),
            Io,
            Some("share/report/https:x".into()),
        ),
        (
            one("share/report/manifest.json.bak"),
            Io,
            Some("share/report/manifest.json.bak".into()),
        ),
        (
            one("share/report/MANIFEST.json"),
            Io,
            Some("share/report/MANIFEST.json".into()),
        ),
        (one(MANIFEST), SelfListed, None),
        (two(ASSET, MANIFEST), SelfListed, None),
        (two(MANIFEST, ASSET), SelfListed, None),
        (
            two("share/report/Z", "share/report/a"),
            Io,
            Some("share/report/Z".into()),
        ),
        (two("share/report/a", "share/report/Z"), Order, None),
        (
            two("share/report/z", "share/report/é"),
            Io,
            Some("share/report/z".into()),
        ),
        (two("share/report/é", "share/report/z"), Order, None),
        (two(ASSET, ASSET), Order, None),
    ];
    for (raw, expected, second) in cases {
        let (r, opens) = run(raw.as_bytes());
        let label = if raw.len() > 300 { &raw[..300] } else { &raw };
        assert_eq!(r.unwrap_err(), expected, "{label}");
        let mut want = vec![MANIFEST.to_string()];
        want.extend(second);
        assert_eq!(opens, want, "{label}");
    }
}

struct Growing {
    prefix: Vec<u8>,
    consumed: u64,
    calls: usize,
}
impl Read for Growing {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        if self.calls % 2 == 1 {
            return Err(io::ErrorKind::Interrupted.into());
        }
        let n = buf.len().min(7);
        for slot in &mut buf[..n] {
            *slot = self
                .prefix
                .get(self.consumed as usize)
                .copied()
                .unwrap_or(0xaa);
            self.consumed += 1;
        }
        Ok(n)
    }
}
struct Finite {
    data: Vec<u8>,
    pos: usize,
    calls: usize,
}
impl Read for Finite {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        if self.calls % 3 == 0 {
            return Err(io::ErrorKind::Interrupted.into());
        }
        let n = buf.len().min(5).min(self.data.len() - self.pos);
        buf[..n].copy_from_slice(&self.data[self.pos..self.pos + n]);
        self.pos += n;
        Ok(n)
    }
}

#[test]
fn probe_zero_growing_interrupted_failing_and_lying_streams() {
    let pattern = |n: usize| (0..n).map(|i| (i * 31 % 251) as u8).collect::<Vec<u8>>();
    for expected in [0usize, 1, 7, 16_384, 16_385, 100_000] {
        let prefix = pattern(expected);
        let digest = raw_sha256(&prefix);
        let mut grow = Growing {
            prefix: prefix.clone(),
            consumed: 0,
            calls: 0,
        };
        assert_eq!(
            checked_read(&mut grow, expected as u64, &digest).unwrap_err(),
            AssetError::Length
        );
        assert_eq!(grow.consumed, expected as u64 + 1, "{expected}");
        let mut exact = Finite {
            data: prefix.clone(),
            pos: 0,
            calls: 0,
        };
        assert_eq!(
            checked_read(&mut exact, expected as u64, &digest).unwrap(),
            prefix
        );
        let mut exact = Finite {
            data: prefix.clone(),
            pos: 0,
            calls: 0,
        };
        let mut wrong = digest;
        wrong[31] ^= 1;
        assert_eq!(
            checked_read(&mut exact, expected as u64, &wrong).unwrap_err(),
            AssetError::Digest
        );
    }
    assert_eq!(
        checked_read(Cursor::new(Vec::<u8>::new()), 0, &raw_sha256(b"")).unwrap(),
        Vec::<u8>::new()
    );
    assert_eq!(
        checked_read(Cursor::new(Vec::<u8>::new()), 0, &[0; 32]).unwrap_err(),
        AssetError::Digest
    );
    assert_eq!(
        checked_read(Cursor::new(vec![1u8]), 0, &raw_sha256(b"")).unwrap_err(),
        AssetError::Length
    );
    struct Fails(io::ErrorKind, usize);
    impl Read for Fails {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            if self.1 == 0 {
                return Err(self.0.into());
            }
            self.1 -= 1;
            buf[0] = 1;
            Ok(1)
        }
    }
    for kind in [io::ErrorKind::WouldBlock, io::ErrorKind::Other, io::ErrorKind::UnexpectedEof] {
        assert_eq!(
            checked_read(Fails(kind, 3), 10, &[0; 32]).unwrap_err(),
            AssetError::Io
        );
    }
    struct Lies(usize);
    impl Read for Lies {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            Ok(buf.len() + self.0)
        }
    }
    for extra in [1, 100, 1 << 20] {
        assert_eq!(
            checked_read(Lies(extra), 0, &raw_sha256(b"")).unwrap_err(),
            AssetError::Io
        );
    }
    let mut never = Growing {
        prefix: Vec::new(),
        consumed: 0,
        calls: 0,
    };
    assert_eq!(
        checked_read(&mut never, MAX_LENGTH + 1, &[0; 32]).unwrap_err(),
        AssetError::Length
    );
    assert_eq!(never.calls, 0);
}

#[test]
fn probe_multi_member_failure_is_fail_fast_and_total() {
    let files: [(&str, &[u8]); 3] = [
        ("share/report/a.js", b"aaa"),
        ("share/report/b.css", b"bbb"),
        ("share/report/c.png", b"ccc"),
    ];
    let rows: Vec<String> = files.iter().map(|(p, d)| row(p, d, "script")).collect();
    let raw = doc(&[SCHEMA], &rows.join(","));
    let setup = || {
        let mut s = Mem::default();
        s.files.insert(MANIFEST.into(), raw.clone().into_bytes());
        for (p, d) in files {
            s.files.insert(p.into(), d.to_vec());
        }
        s
    };
    let pin = pin_for(raw.as_bytes());
    let mut s = setup();
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &SCHEMA)
            .unwrap()
            .assets()
            .len(),
        3
    );
    let mut s = setup();
    s.files.get_mut(files[2].0).unwrap()[2] ^= 1;
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
        AssetError::Digest
    );
    assert_eq!(s.opens, [MANIFEST, files[0].0, files[1].0, files[2].0]);
    let mut s = setup();
    s.files.remove(files[1].0);
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
        AssetError::Io
    );
    assert_eq!(s.opens, [MANIFEST, files[0].0, files[1].0]);
    let mut s = setup();
    s.files.get_mut(files[1].0).unwrap().push(b'!');
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
        AssetError::Length
    );
}

#[test]
fn probe_identity_mix_and_mutation_between_manifest_and_member() {
    let raw = base();
    let pin = pin_for(raw.as_bytes());
    // Same-length asset from another bundle.
    assert_eq!(OTHER_DATA.len(), DATA.len());
    let mut s = source(raw.as_bytes());
    s.files.insert(ASSET.into(), OTHER_DATA.to_vec());
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
        AssetError::Digest
    );
    // Mutation after the manifest was read and before the member is opened.
    let mut s = source(raw.as_bytes());
    s.after_manifest = Some((ASSET.into(), OTHER_DATA.to_vec()));
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap_err(),
        AssetError::Digest
    );
    // Two independently valid bundles under different roots cannot cross-complete.
    let other_raw = doc(
        &[SCHEMA],
        &row("share/other/report.js", OTHER_DATA, "script"),
    );
    let other_pin = FixturePin {
        root: "share/other".into(),
        manifest_path: "share/other/manifest.json".into(),
        ..pin_for(other_raw.as_bytes())
    };
    let mut s2 = Mem::default();
    s2.files
        .insert("share/other/manifest.json".into(), other_raw.into_bytes());
    s2.files
        .insert("share/other/report.js".into(), OTHER_DATA.to_vec());
    let second = verify_fixture_assets(&mut s2, &other_pin, &SCHEMA).unwrap();
    let mut s = source(raw.as_bytes());
    let first = verify_fixture_assets(&mut s, &pin, &SCHEMA).unwrap();
    let first_enum = vec![MANIFEST.to_string(), ASSET.to_string()];
    let second_enum = vec![
        "share/other/manifest.json".to_string(),
        "share/other/report.js".to_string(),
    ];
    assert_eq!(fixture_completeness(&first, &first_enum), Ok(()));
    assert_eq!(fixture_completeness(&second, &second_enum), Ok(()));
    assert_eq!(
        fixture_completeness(&first, &second_enum),
        Err(AssetError::Path)
    );
    assert_eq!(
        fixture_completeness(&second, &first_enum),
        Err(AssetError::Path)
    );
    // Other pin over the same source: the pinned manifest does not exist there.
    let mut s = source(raw.as_bytes());
    assert_eq!(
        verify_fixture_assets(&mut s, &other_pin, &SCHEMA).unwrap_err(),
        AssetError::Io
    );
    assert_eq!(s.opens, ["share/other/manifest.json"]);
}

#[test]
fn probe_completeness_matrix() {
    let raw = base();
    let mut s = source(raw.as_bytes());
    let bundle = verify_fixture_assets(&mut s, &pin_for(raw.as_bytes()), &SCHEMA).unwrap();
    let v = |items: &[&str]| items.iter().map(|x| x.to_string()).collect::<Vec<_>>();
    assert_eq!(fixture_completeness(&bundle, &v(&[ASSET, MANIFEST])), Ok(()));
    assert_eq!(fixture_completeness(&bundle, &v(&[MANIFEST, ASSET])), Ok(()));
    for (paths, expected) in [
        (v(&[]), AssetError::Unlisted),
        (v(&[ASSET]), AssetError::Unlisted),
        (v(&[MANIFEST]), AssetError::Unlisted),
        (v(&[ASSET, MANIFEST, MANIFEST]), AssetError::Unlisted),
        (v(&[ASSET, ASSET, MANIFEST]), AssetError::Unlisted),
        (v(&[ASSET, "share/report/MANIFEST.json"]), AssetError::Unlisted),
        (
            v(&[ASSET, MANIFEST, "share/report/.hidden"]),
            AssetError::Unlisted,
        ),
        (v(&[ASSET, MANIFEST, "share/other/x"]), AssetError::Path),
        (v(&[ASSET, MANIFEST, ROOT]), AssetError::Path),
        (v(&[ASSET, MANIFEST, "share/report/"]), AssetError::Path),
        (v(&[ASSET, MANIFEST, "share/report/../x"]), AssetError::Path),
        (v(&[ASSET, MANIFEST, "/share/report/x"]), AssetError::Path),
    ] {
        assert_eq!(fixture_completeness(&bundle, &paths), Err(expected), "{paths:?}");
    }
}

#[test]
#[ignore]
fn probe_hash_and_read_throughput() {
    for mib in [1usize, 8, 32] {
        let data = vec![0x5a_u8; mib << 20];
        let t = std::time::Instant::now();
        let digest = raw_sha256(&data);
        let hash = t.elapsed();
        let t = std::time::Instant::now();
        let out = checked_read(Cursor::new(&data), data.len() as u64, &digest).unwrap();
        eprintln!(
            "PROBE throughput {mib} MiB: raw_sha256 {hash:?}; checked_read+hash {:?}; capacity {}",
            t.elapsed(),
            out.capacity()
        );
    }
}
