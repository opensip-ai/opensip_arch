//! Review02 independent delta probes over the public API. Review copy only.
use opensip_identity::{digest_hex, raw_sha256};
use opensip_report_asset_trial::{
    AssetError, AssetSource, FixturePin, Role, fixture_completeness, verify_fixture_assets,
};
use std::collections::BTreeMap;
use std::io::{self, Cursor, Read};

const MANIFEST: &str = "share/report/manifest.json";
const ASSET: &str = "share/report/app.js";
const DATA: &[u8] = b"offline bytes";
const A: [u8; 32] = [0x10; 32];
const B: [u8; 32] = [0x20; 32];
const C: [u8; 32] = [0x30; 32];
const D: [u8; 32] = [0x25; 32];

#[derive(Default)]
struct Mem {
    files: BTreeMap<String, Vec<u8>>,
    opens: Vec<String>,
}
impl AssetSource for Mem {
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

fn manifest(schemas: &[[u8; 32]]) -> String {
    let list: Vec<String> = schemas
        .iter()
        .map(|s| format!("\"{}\"", digest_hex(s)))
        .collect();
    format!(
        r#"{{"schemaVersion":1,"projectionSchemaSha256s":[{}],"assets":[{{"path":"{ASSET}","sha256":"{}","bytes":{},"role":"notice"}}]}}"#,
        list.join(","),
        digest_hex(&raw_sha256(DATA)),
        DATA.len()
    )
}
fn setup(raw: &str) -> (Mem, FixturePin) {
    let mut s = Mem::default();
    s.files.insert(MANIFEST.into(), raw.as_bytes().to_vec());
    s.files.insert(ASSET.into(), DATA.to_vec());
    let pin = FixturePin {
        root: "share/report".into(),
        manifest_path: MANIFEST.into(),
        manifest_bytes: raw.len() as u64,
        manifest_sha256: raw_sha256(raw.as_bytes()),
    };
    (s, pin)
}

#[test]
fn delta_projection_is_exactly_the_checked_member() {
    let raw = manifest(&[A, B, C]);
    for p in [A, B, C] {
        let (mut s, pin) = setup(&raw);
        let bundle = verify_fixture_assets(&mut s, &pin, &p).unwrap();
        assert_eq!(bundle.projection_sha256(), &p);
        assert_eq!(bundle.manifest_sha256(), &pin.manifest_sha256);
        assert_eq!(s.opens, [MANIFEST, ASSET]);
        assert_eq!(bundle.assets()[0].bytes(), DATA);
        assert_eq!(bundle.assets()[0].role(), Role::Notice);
    }
    let single = manifest(&[B]);
    let (mut s, pin) = setup(&single);
    assert_eq!(
        verify_fixture_assets(&mut s, &pin, &B)
            .unwrap()
            .projection_sha256(),
        &B
    );
    // Unlisted projections, including values equal to other bound digests, refuse
    // before any member open and expose no bundle.
    let (_, pin) = setup(&raw);
    for p in [D, [0; 32], [0xff; 32], pin.manifest_sha256, raw_sha256(DATA)] {
        let (mut s, pin) = setup(&raw);
        assert_eq!(
            verify_fixture_assets(&mut s, &pin, &p).unwrap_err(),
            AssetError::Incompatible
        );
        assert_eq!(s.opens, [MANIFEST]);
    }
    // Same source and pin under two projections: separate bundles, same bytes.
    let (mut s, pin) = setup(&raw);
    let first = verify_fixture_assets(&mut s, &pin, &A).unwrap();
    let third = verify_fixture_assets(&mut s, &pin, &C).unwrap();
    assert_eq!(first.projection_sha256(), &A);
    assert_eq!(third.projection_sha256(), &C);
    assert_eq!(first.manifest_sha256(), third.manifest_sha256());
    assert_eq!(first.assets()[0].bytes(), third.assets()[0].bytes());
    let paths = vec![ASSET.to_string(), MANIFEST.to_string()];
    assert_eq!(fixture_completeness(&first, &paths), Ok(()));
    assert_eq!(fixture_completeness(&third, &paths), Ok(()));
    assert_eq!(
        fixture_completeness(&first, &paths[..1]),
        Err(AssetError::Unlisted)
    );
}

struct ErrReader;
impl Read for ErrReader {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::other("device gone"))
    }
}

#[test]
fn delta_owned_bytes_and_trusted_source_behaviour_unchanged() {
    let raw = manifest(&[A]);
    let (mut s, pin) = setup(&raw);
    let bundle = verify_fixture_assets(&mut s, &pin, &A).unwrap();
    let before = bundle.assets()[0].bytes().to_vec();
    let address = bundle.assets()[0].bytes().as_ptr();
    s.files.clear();
    s.files.insert(ASSET.into(), b"replaced byte".to_vec());
    drop(s);
    assert_eq!(bundle.assets()[0].bytes(), &before[..]);
    assert_eq!(bundle.assets()[0].bytes().as_ptr(), address);
    assert_eq!(bundle.assets()[0].path(), ASSET);
    assert_eq!(bundle.projection_sha256(), &A);

    // Trusted-source boundary: identical bytes served from another backing name
    // are indistinguishable to the algorithm (declared, not a sandbox).
    struct Alias(Mem);
    impl AssetSource for Alias {
        type Reader = Cursor<Vec<u8>>;
        fn open_regular(&mut self, path: &str) -> io::Result<Self::Reader> {
            self.0
                .open_regular(if path == ASSET { "elsewhere" } else { path })
        }
    }
    let (mut inner, pin) = setup(&raw);
    let moved = inner.files.remove(ASSET).unwrap();
    inner.files.insert("elsewhere".into(), moved);
    let mut alias = Alias(inner);
    let aliased = verify_fixture_assets(&mut alias, &pin, &A).unwrap();
    assert_eq!(aliased.assets()[0].path(), ASSET);
    assert_eq!(alias.0.opens, [MANIFEST, "elsewhere"]);

    // Different bytes from a source still refuse; a reader failing after partial
    // data yields no bundle and so no projection.
    let (mut inner, pin) = setup(&raw);
    inner.files.insert(ASSET.into(), b"offline BYTES".to_vec());
    assert_eq!(
        verify_fixture_assets(&mut Alias(inner), &pin, &A).unwrap_err(),
        AssetError::Io
    );
    struct Flaky(Mem);
    impl AssetSource for Flaky {
        type Reader = Box<dyn Read>;
        fn open_regular(&mut self, path: &str) -> io::Result<Box<dyn Read>> {
            let reader = self.0.open_regular(path)?;
            if path == ASSET {
                Ok(Box::new(Cursor::new(DATA[..5].to_vec()).chain(ErrReader)))
            } else {
                Ok(Box::new(reader))
            }
        }
    }
    let (inner, pin) = setup(&raw);
    let mut flaky = Flaky(inner);
    assert_eq!(
        verify_fixture_assets(&mut flaky, &pin, &A).unwrap_err(),
        AssetError::Io
    );
    assert_eq!(flaky.0.opens, [MANIFEST, ASSET]);
    let (mut inner, pin) = setup(&raw);
    inner.files.insert(ASSET.into(), b"offline BYTES".to_vec());
    assert_eq!(
        verify_fixture_assets(&mut inner, &pin, &A).unwrap_err(),
        AssetError::Digest
    );
    let (mut inner, pin) = setup(&raw);
    inner.files.remove(MANIFEST);
    assert_eq!(
        verify_fixture_assets(&mut inner, &pin, &A).unwrap_err(),
        AssetError::Io
    );
    assert_eq!(inner.opens, [MANIFEST]);
}
