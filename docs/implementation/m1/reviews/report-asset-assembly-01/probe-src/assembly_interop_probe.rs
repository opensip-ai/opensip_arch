//! Resumed independent review: enumerator bundles through the unchanged accepted verifier.
use opensip_identity::{JsonValue, canonical_bytes, parse_json};
use opensip_platform_asset_trial::ReleaseDirectory;
use opensip_report_asset_trial::{
    AssetError, AssetSource, FixturePin, fixture_completeness, verify_fixture_assets,
};
use std::fs::{self, File};
use std::path::PathBuf;

struct Source(ReleaseDirectory);
impl AssetSource for Source {
    type Reader = File;
    fn open_regular(&mut self, path: &str) -> std::io::Result<File> {
        self.0.open_regular(path)
    }
}

fn field<'a>(value: &'a JsonValue, key: &str) -> &'a JsonValue {
    match value {
        JsonValue::Object(map) => &map[key],
        _ => panic!("expected object"),
    }
}
fn text(value: &JsonValue) -> String {
    match value {
        JsonValue::String(s) => s.clone(),
        _ => panic!("expected string"),
    }
}
fn hex(s: &str) -> [u8; 32] {
    assert_eq!(s.len(), 64);
    std::array::from_fn(|i| u8::from_str_radix(&s[i * 2..i * 2 + 2], 16).unwrap())
}
fn source(dir: &PathBuf) -> Source {
    Source(ReleaseDirectory::from_retained_handle(File::open(dir).unwrap()).unwrap())
}

#[test]
fn review_enumerator_bundles_verify_under_every_projection() {
    let base = PathBuf::from(std::env::var("ASSEMBLY_INTEROP_DIR").expect("ASSEMBLY_INTEROP_DIR"));
    let mut checked = Vec::new();
    for bundle in ["nested", "deep"] {
        let dir = base.join(bundle);
        let manifest = fs::read(dir.join("report/manifest.json")).unwrap();
        let parsed = parse_json(&manifest).unwrap();
        assert_eq!(
            canonical_bytes(&parsed).unwrap(),
            manifest,
            "{bundle}: enumerator bytes are identity canonical bytes"
        );
        let pin = parse_json(&fs::read(dir.join("pin.json")).unwrap()).unwrap();
        let JsonValue::Integer(length) = field(&pin, "assetManifestBytes") else {
            panic!("length")
        };
        let fixture = FixturePin {
            root: text(field(&pin, "assetRoot")),
            manifest_path: text(field(&pin, "assetManifestPath")),
            manifest_sha256: hex(&text(field(&pin, "assetManifestSha256"))),
            manifest_bytes: length.get() as u64,
        };
        assert_eq!(fixture.manifest_bytes, manifest.len() as u64);
        let JsonValue::Array(projections) = field(&parsed, "projectionSchemaSha256s") else {
            panic!("projections")
        };
        let JsonValue::Array(rows) = field(&parsed, "assets") else {
            panic!("assets")
        };
        let enumeration: Vec<String> =
            match parse_json(&fs::read(dir.join("enumeration.json")).unwrap()).unwrap() {
                JsonValue::Array(items) => items.iter().map(text).collect(),
                _ => panic!("enumeration"),
            };
        for projection in projections {
            let selected = hex(&text(projection));
            let verified = verify_fixture_assets(&mut source(&dir), &fixture, &selected).unwrap();
            assert_eq!(verified.projection_sha256(), &selected);
            assert_eq!(verified.assets().len(), rows.len());
            for (asset, row) in verified.assets().iter().zip(rows) {
                assert_eq!(asset.path(), text(field(row, "path")));
            }
            assert_eq!(fixture_completeness(&verified, &enumeration), Ok(()));
            checked.push(format!("{bundle}:{}", &text(projection)[..2]));
        }
        let wrong = FixturePin {
            manifest_bytes: fixture.manifest_bytes + 1,
            ..fixture.clone()
        };
        let first = hex(&text(&projections[0]));
        assert_eq!(
            verify_fixture_assets(&mut source(&dir), &wrong, &first).unwrap_err(),
            AssetError::Length
        );
    }
    eprintln!("REVIEW interop verified {} bundle/projection pairs: {checked:?}", checked.len());
    assert_eq!(checked.len(), 3 + 16);
}
