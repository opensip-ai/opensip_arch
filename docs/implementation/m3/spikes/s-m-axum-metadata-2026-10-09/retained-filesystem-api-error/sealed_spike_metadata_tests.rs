// Outside-product public-T2 metadata harness; no production profile admission.
use super::GlobalContext;
use crate::core::resolver::CliFeatures;
use crate::core::{Shell, Workspace};
use crate::ops::{OutputMetadataOptions, output_metadata};
use std::collections::HashMap;
use std::path::PathBuf;
#[test]
#[ignore = "explicit outside-product harness packet only"]
fn opensip_spike_metadata_collect() {
    let packet =
        std::env::var_os("OPENSIP_SPIKE_METADATA_PACKET").expect("explicit harness packet");
    let input: serde_json::Value = serde_json::from_slice(&std::fs::read(packet).unwrap()).unwrap();
    let cwd = PathBuf::from(input["cwd"].as_str().unwrap());
    let home = PathBuf::from(input["privateCargoHome"].as_str().unwrap());
    let manifest = PathBuf::from(input["manifestPath"].as_str().unwrap());
    let output = PathBuf::from(input["output"].as_str().unwrap());
    assert!(cwd.is_absolute() && home.is_absolute() && manifest.is_absolute());
    let mut gctx =
        GlobalContext::new_with_projected_values_data(Shell::new(), cwd, home, HashMap::new())
            .unwrap();
    gctx.set_env(HashMap::from([
        ("RUSTC".into(), input["rustc"].as_str().unwrap().into()),
        ("CARGO_HOME".into(), "/Users/sb/.cargo".into()),
    ]));
    gctx.configure(0, false, Some("never"), true, true, true, &None, &[], &[])
        .unwrap();
    if let Some(receipt_path) = input["dependencyCacheReceipt"].as_str() {
        let receipt: serde_json::Value =
            serde_json::from_slice(&std::fs::read(receipt_path).unwrap()).unwrap();
        let source = crate::core::SourceId::crates_io_maybe_sparse_http(&gctx).unwrap();
        let name = crate::sources::registry::spike_registry_cache_name(source);
        let index_root = gctx.home().join("registry/index").join(&name);
        let archive_root = gctx.home().join("registry/cache").join(&name);
        std::fs::create_dir_all(&index_root).unwrap();
        std::fs::create_dir_all(&archive_root).unwrap();
        let registry_config =
            std::fs::read(receipt["registryConfigPath"].as_str().unwrap()).unwrap();
        std::fs::write(index_root.join("config.json"), registry_config).unwrap();
        for row in receipt["indexFiles"].as_array().unwrap() {
            let raw = std::fs::read(row["path"].as_str().unwrap()).unwrap();
            let mut versions = Vec::new();
            for line in raw
                .split(|byte| *byte == b'\n')
                .filter(|line| !line.is_empty())
            {
                let record: serde_json::Value = serde_json::from_slice(line).unwrap();
                assert_eq!(record["name"].as_str(), row["name"].as_str());
                versions.push((
                    semver::Version::parse(record["vers"].as_str().unwrap()).unwrap(),
                    line,
                ));
            }
            let cache = crate::sources::registry::index::SpikeSummariesCache {
                versions,
                index_version: "Unknown",
            };
            let path = index_root
                .join(".cache")
                .join(row["indexRelativePath"].as_str().unwrap());
            std::fs::create_dir_all(path.parent().unwrap()).unwrap();
            std::fs::write(path, cache.serialize("Unknown")).unwrap();
        }
        for row in receipt["packages"].as_array().unwrap() {
            let file = format!(
                "{}-{}.crate",
                row["name"].as_str().unwrap(),
                row["version"].as_str().unwrap()
            );
            std::fs::copy(row["archive"].as_str().unwrap(), archive_root.join(file)).unwrap();
        }
    }
    let workspace = Workspace::new(&manifest, &gctx).unwrap();
    let options = OutputMetadataOptions {
        cli_features: CliFeatures::new_all(false),
        no_deps: input["noDeps"].as_bool().unwrap_or(true),
        version: 1,
        filter_platforms: input["filterPlatform"]
            .as_str()
            .map(|p| vec![p.to_owned()])
            .unwrap_or_default(),
    };
    let metadata = output_metadata(&workspace, &options).unwrap();
    std::fs::write(output, serde_json::to_vec_pretty(&metadata).unwrap()).unwrap();
}
