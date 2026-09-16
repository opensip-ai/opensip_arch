//! Compiled metadata producer and private asset-pin channel agreement.
//! Fixture assets are labelled development bytes, never a production selection.
use std::{
    fs,
    path::PathBuf,
    process::Command,
    sync::atomic::{AtomicU64, Ordering},
};

const FIXTURE_SCRIPT: &[u8] = &[
    47, 47, 32, 79, 112, 101, 110, 83, 73, 80, 32, 100, 101, 118, 101, 108, 111, 112, 109, 101,
    110, 116, 45, 111, 110, 108, 121, 32, 99, 104, 97, 110, 110, 101, 108, 32, 116, 101, 115, 116,
    32, 102, 105, 120, 116, 117, 114, 101, 46, 10, 101, 120, 112, 111, 114, 116, 32, 99, 111, 110,
    115, 116, 32, 102, 105, 120, 116, 117, 114, 101, 32, 61, 32, 116, 114, 117, 101, 59, 10,
];
const FIXTURE_MANIFEST: &[u8] = &[
    123, 34, 97, 115, 115, 101, 116, 115, 34, 58, 91, 123, 34, 98, 121, 116, 101, 115, 34, 58, 55,
    57, 44, 34, 112, 97, 116, 104, 34, 58, 34, 102, 105, 120, 116, 117, 114, 101, 45, 97, 115, 115,
    101, 116, 115, 47, 102, 105, 120, 116, 117, 114, 101, 46, 106, 115, 34, 44, 34, 114, 111, 108,
    101, 34, 58, 34, 115, 99, 114, 105, 112, 116, 34, 44, 34, 115, 104, 97, 50, 53, 54, 34, 58, 34,
    50, 54, 54, 57, 102, 53, 97, 101, 52, 49, 56, 51, 101, 98, 55, 50, 102, 55, 54, 54, 97, 98,
    101, 57, 49, 57, 102, 51, 101, 56, 55, 99, 54, 100, 100, 51, 56, 52, 53, 55, 51, 100, 48, 50,
    53, 54, 50, 101, 100, 51, 101, 100, 102, 102, 98, 102, 55, 53, 54, 97, 49, 100, 52, 57, 34,
    125, 93, 44, 34, 112, 114, 111, 106, 101, 99, 116, 105, 111, 110, 83, 99, 104, 101, 109, 97,
    83, 104, 97, 50, 53, 54, 115, 34, 58, 91, 34, 98, 98, 98, 53, 99, 97, 57, 50, 48, 102, 100, 50,
    98, 50, 54, 99, 56, 99, 99, 101, 50, 99, 54, 99, 50, 53, 100, 100, 52, 101, 100, 98, 48, 51,
    51, 56, 54, 53, 57, 52, 102, 57, 54, 52, 53, 97, 53, 100, 48, 55, 48, 101, 100, 54, 49, 97, 53,
    53, 57, 97, 99, 99, 57, 55, 34, 93, 44, 34, 115, 99, 104, 101, 109, 97, 86, 101, 114, 115, 105,
    111, 110, 34, 58, 49, 125, 10,
];
const FIXTURE_SHA256: &str = "d8870ab533155cd0fe020daae148f091abdd93bf1a35e45f02de47936aaf99ef";
static NEXT: AtomicU64 = AtomicU64::new(0);
struct Temp(PathBuf);
impl Temp {
    fn new() -> Self {
        let path = std::env::temp_dir().join(format!(
            "opensip-channel-test-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&path).unwrap();
        Self(path)
    }
}
impl Drop for Temp {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}

#[test]
fn metadata_has_one_compiled_development_selection_without_asset_loading() {
    let value = opensip_reporting::development_metadata(env!("CARGO_PKG_VERSION")).unwrap();
    assert_eq!(value.host_release.as_str(), env!("CARGO_PKG_VERSION"));
    assert_eq!(value.build_channel.to_string(), "development");
    assert!(value.closure_ids.is_empty());
    for invalid in ["01.2.3", "1.2", "1.2.3\n", "1.2.3-01", "1.2.3+", "1.2.3-α"] {
        assert!(
            opensip_reporting::development_metadata(invalid).is_err(),
            "{invalid}"
        );
    }
}

#[test]
fn actual_asset_source_refuses_explicit_channel_mismatch_during_compilation() {
    // Compile the exact production source in a disposable package. Private pin
    // types stay private in the real reporting library; this is not a public
    // constructor, cfg bypass or alternate admission implementation.
    let tmp = Temp::new();
    let src = tmp.0.join("src");
    fs::create_dir(&src).unwrap();
    let fixture_root = tmp.0.join("fixture-assets");
    fs::create_dir(&fixture_root).unwrap();
    fs::write(fixture_root.join("fixture.js"), FIXTURE_SCRIPT).unwrap();
    fs::write(fixture_root.join("manifest.json"), FIXTURE_MANIFEST).unwrap();
    assert_eq!(
        fs::read(fixture_root.join("manifest.json")).unwrap(),
        FIXTURE_MANIFEST
    );
    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let production_source = manifest_dir.join("src/assets.rs");
    let contracts = manifest_dir.parent().unwrap().join("contracts");
    let dependency = serde_json::to_string(contracts.to_str().unwrap()).unwrap();
    fs::write(tmp.0.join("Cargo.toml"), format!("[workspace]\n[package]\nname=\"opensip-channel-compile-probe\"\nversion=\"0.0.0\"\nedition=\"2024\"\npublish=false\n[dependencies]\nopensip-contracts={{path={dependency}}}\n")).unwrap();
    let source_path = serde_json::to_string(production_source.to_str().unwrap()).unwrap();
    let include = format!("include!({source_path});\n");
    let template = format!(
        r#"
const TEST_PIN: HostAssetPinV1 = HostAssetPinV1 {{
    schema_version: 1,
    asset_root: "fixture-assets",
    asset_manifest_path: "fixture-assets/manifest.json",
    asset_manifest_sha256: "{}",
    asset_manifest_bytes: {},
    build_channel: BUILD_CHANNEL,
}};
const TEST_SELECTION: CompiledBuildSelection = CompiledBuildSelection::new(BUILD_CHANNEL, Some(TEST_PIN));
pub fn selected() -> Metadata1BuildMetadataV1BuildChannel {{ TEST_SELECTION.channel() }}
"#,
        FIXTURE_SHA256,
        FIXTURE_MANIFEST.len()
    );
    let cases = [
        ("matching-real-fixture", template.clone(), None),
        (
            "channel-mismatch",
            template.replace(
                "build_channel: BUILD_CHANNEL,",
                "build_channel: Metadata1BuildMetadataV1BuildChannel::Release,",
            ),
            Some("asset pin build channel differs from compiled metadata"),
        ),
        (
            "manifest-outside-root",
            template.replace("fixture-assets/manifest.json", "other-assets/manifest.json"),
            Some("manifest must be under asset root"),
        ),
        (
            "zero-byte-manifest",
            template.replace(
                &format!("asset_manifest_bytes: {},", FIXTURE_MANIFEST.len()),
                "asset_manifest_bytes: 0,",
            ),
            Some("invalid manifest byte length"),
        ),
        (
            "invalid-raw-digest",
            template.replace(FIXTURE_SHA256, "not-a-raw-digest"),
            Some("invalid raw manifest digest"),
        ),
    ];
    let mut retained_lock = None;
    for (index, (name, body, failure)) in cases.into_iter().enumerate() {
        fs::write(src.join("lib.rs"), format!("{include}{body}")).unwrap();
        let mut command = Command::new(env!("CARGO"));
        command
            .args(["check", "--offline", "--manifest-path"])
            .arg(tmp.0.join("Cargo.toml"));
        if index > 0 {
            command.arg("--locked");
        }
        let result = command
            .env("CARGO_TARGET_DIR", tmp.0.join("target"))
            .output()
            .unwrap();
        let stderr = String::from_utf8_lossy(&result.stderr);
        if let Some(message) = failure {
            assert!(!result.status.success(), "{name} unexpectedly compiled");
            assert!(
                stderr.contains("E0080") && stderr.contains(message),
                "{name}: {stderr}"
            );
        } else {
            assert!(result.status.success(), "{name}: {stderr}");
        }
        let lock = fs::read(tmp.0.join("Cargo.lock")).unwrap();
        if let Some(prior) = &retained_lock {
            assert_eq!(prior, &lock);
        } else {
            retained_lock = Some(lock);
        }
    }
}
