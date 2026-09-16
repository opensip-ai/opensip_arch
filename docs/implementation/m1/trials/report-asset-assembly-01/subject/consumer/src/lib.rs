//! Assembly-to-verifier interoperability fixture. Not host integration.
#[cfg(test)]
mod tests {
    use opensip_platform_asset_trial::ReleaseDirectory;
    use opensip_report_asset_trial::{AssetSource, FixturePin, Role, verify_fixture_assets};
    use std::fs::File;
    struct Source(ReleaseDirectory);
    impl AssetSource for Source {
        type Reader = File;
        fn open_regular(&mut self, path: &str) -> std::io::Result<File> {
            self.0.open_regular(path)
        }
    }
    #[test]
    fn exact_build_manifest_is_accepted_by_reviewed_runtime_verifier() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../fixtures/release");
        let mut source =
            Source(ReleaseDirectory::from_retained_handle(File::open(root).unwrap()).unwrap());
        let manifest = include_bytes!("../../fixtures/release/report/manifest.json");
        // This expected digest is emitted by the build fixture generator and is
        // deliberately independent of a digest computed from bytes at load.
        let expected: [u8; 32] = include!("../../fixtures/manifest-digest.rs");
        let pin = FixturePin {
            root: "report".into(),
            manifest_path: "report/manifest.json".into(),
            manifest_sha256: expected,
            manifest_bytes: manifest.len() as u64,
        };
        for selected in [[0x11; 32], [0x55; 32], [0xaa; 32]] {
            let bundle = verify_fixture_assets(&mut source, &pin, &selected).unwrap();
            assert_eq!(bundle.projection_sha256(), &selected);
            assert_eq!(bundle.assets().len(), 3);
            assert_eq!(bundle.assets()[0].path(), "report/app.js");
            assert_eq!(
                bundle.assets()[0].bytes(),
                include_bytes!("../../fixtures/release/report/app.js")
            );
            assert_eq!(bundle.assets()[1].role(), Role::Style);
            assert_eq!(bundle.assets()[2].role(), Role::Notice);
            assert_eq!(bundle.manifest_sha256(), &expected);
        }
    }
}
