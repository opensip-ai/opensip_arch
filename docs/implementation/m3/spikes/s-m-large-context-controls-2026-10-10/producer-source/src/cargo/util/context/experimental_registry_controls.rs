//! First-party synthetic registry bytes, offline only, never public admission.
use super::*;
use crate::core::compiler::{CompileKind, CompileTarget, UnitInterner, UserIntent};
use crate::core::{SourceId, Workspace};
use std::ffi::OsString;

fn fixture(valid_checksum: bool) {
    let root = tempfile::Builder::new()
        .prefix("opensip-offline-registry-control-")
        .tempdir()
        .unwrap()
        .keep();
    let project = root.join("project");
    std::fs::create_dir_all(project.join("src")).unwrap();
    std::fs::write(project.join("Cargo.toml"), "[package]\nname='app'\nversion='1.0.0'\nedition='2024'\n[dependencies]\nrenamed={package='opensip-fixture-dep',version='=1.0.0',features=['chosen']}\n").unwrap();
    std::fs::write(
        project.join("src/lib.rs"),
        "compile_error!(\"fixture app must not compile\");\n",
    )
    .unwrap();
    let home = root.join("home");
    let queries = root.join("queries");
    std::fs::create_dir(&home).unwrap();
    std::fs::create_dir(&queries).unwrap();
    let head = ["-", "--crate-name", "___", "--print=file-names"];
    let tail = [
        "--crate-type",
        "bin",
        "--crate-type",
        "rlib",
        "--crate-type",
        "dylib",
        "--crate-type",
        "cdylib",
        "--crate-type",
        "staticlib",
        "--crate-type",
        "proc-macro",
        "--print=sysroot",
        "--print=split-debuginfo",
        "--print=crate-name",
        "--print=cfg",
        "-Wwarnings",
    ];
    let host_args = head.iter().chain(tail.iter()).map(OsString::from).collect();
    let target_args = head
        .iter()
        .chain(["--target", "aarch64-apple-darwin"].iter())
        .chain(tail.iter())
        .map(OsString::from)
        .collect();
    let base = cargo_util::ProcessBuilder::experimental_information_queries(
        Path::new("/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc"),
        &project,
        vec![vec!["-vV".into()], host_args, target_args],
        "b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c".into(),
        &queries,
    );
    let mut context = GlobalContext::new_experimental_query_context(
        Shell::new(),
        project.clone(),
        home.clone(),
        HashMap::new(),
        base,
    );
    context
        .configure(0, false, Some("never"), false, false, true, &None, &[], &[])
        .unwrap();
    let source = SourceId::crates_io_maybe_sparse_http(&context).unwrap();
    let name = crate::sources::registry::spike_registry_cache_name(source);
    let index = home.join("registry/index").join(&name);
    let archives = home.join("registry/cache").join(&name);
    std::fs::create_dir_all(index.join(".cache/op/en")).unwrap();
    std::fs::create_dir_all(&archives).unwrap();
    std::fs::write(
        index.join("config.json"),
        "{\"dl\":\"https://static.crates.io/crates\",\"api\":\"https://crates.io\"}\n",
    )
    .unwrap();
    let checksum = if valid_checksum {
        "f80bd6cd78496f09859be6aa643535b020e35e2f25d78ede91eb874dcfeca3de".to_string()
    } else {
        "0".repeat(64)
    };
    let record = serde_json::json!({"name":"opensip-fixture-dep","vers":"1.0.0","deps":[],"cksum":checksum,"features":{"default":[],"chosen":[]},"yanked":false});
    let raw = serde_json::to_vec(&record).unwrap();
    let cache = crate::sources::registry::index::SpikeSummariesCache {
        versions: vec![(semver::Version::parse("1.0.0").unwrap(), raw.as_slice())],
        index_version: "Unknown",
    };
    std::fs::write(
        index.join(".cache/op/en/opensip-fixture-dep"),
        cache.serialize("Unknown"),
    )
    .unwrap();
    let archive = std::fs::read("/tmp/opensip-implementation/sm-offline-registry-controls-2026-10-10/first-party-fixture.crate").unwrap();
    let mut hasher = cargo_util::Sha256::new();
    hasher.update(&archive);
    let actual_checksum = hasher.finish_hex();
    if actual_checksum != checksum {
        assert!(!valid_checksum);
        assert_eq!(std::fs::read_dir(&queries).unwrap().count(), 0);
        assert_eq!(std::fs::read_dir(&archives).unwrap().count(), 0);
        let observation = serde_json::json!({"root":root,"validChecksum":false,
            "expectedChecksum":checksum,"actualChecksum":actual_checksum,
            "wholeArchiveMatch":false,"archiveCopied":false,"resolverInvoked":false,
            "syntheticFirstPartyRegistry":true,"publicCrate":false,"nativeAdmission":false,"fullSM":false});
        std::fs::write(
            root.join("control.json"),
            serde_json::to_vec_pretty(&observation).unwrap(),
        )
        .unwrap();
        eprintln!("ACTUAL_EXPERIMENT_REGISTRY_CONTROL={}", root.display());
        return;
    }
    assert!(valid_checksum);
    std::fs::write(archives.join("opensip-fixture-dep-1.0.0.crate"), &archive).unwrap();
    let mut workspace = Workspace::new(&project.join("Cargo.toml"), &context).unwrap();
    workspace.set_target_dir(Filesystem::new(root.join("target")));
    let mut options =
        crate::ops::CompileOptions::new(&context, UserIntent::Check { test: false }).unwrap();
    options.spec = crate::ops::Packages::Default;
    options.build_config.requested_kinds = vec![CompileKind::Target(
        CompileTarget::new("aarch64-apple-darwin", false).unwrap(),
    )];
    options.build_config.unit_graph = true;
    let interner = UnitInterner::new();
    let result = crate::ops::create_bcx(&workspace, &options, &interner, None);
    if valid_checksum {
        let bcx = result.unwrap();
        assert_eq!(bcx.roots.len(), 1);
        assert_eq!(bcx.unit_graph.len(), 2);
        let deps = bcx.unit_graph.get(&bcx.roots[0]).unwrap();
        assert!(
            deps.iter()
                .any(|d| d.unit.pkg.name().to_string() == "opensip-fixture-dep"
                    && d.extern_crate_name.to_string() == "renamed")
        );
        let dep = bcx
            .unit_graph
            .keys()
            .find(|u| u.pkg.name().to_string() == "opensip-fixture-dep")
            .unwrap();
        assert!(dep.features.iter().any(|f| f.to_string() == "chosen"));
        *context.shell() = Shell::from_write(Box::new(
            std::fs::File::create(root.join("unit-graph.json")).unwrap(),
        ));
        crate::core::compiler::unit_graph::emit_serialized_unit_graph(
            &bcx.roots,
            &bcx.unit_graph,
            &context,
        )
        .unwrap();
        *context.shell() = Shell::new();
        let lock = std::fs::read_to_string(project.join("Cargo.lock")).unwrap();
        assert!(lock.contains(&checksum));
    } else {
        assert!(result.is_err());
        // This is a private first-party test diagnostic, never a public route.
        std::fs::write(
            root.join("private-error.txt"),
            format!("{:#}", result.err().unwrap()),
        )
        .unwrap();
        assert!(!root.join("unit-graph.json").exists());
    }
    let observation = serde_json::json!({"root":root,"validChecksum":valid_checksum,"offline":true,
        "syntheticFirstPartyRegistry":true,"publicCrate":false,"fixtureSourceExecuted":false,
        "corpusResolutionRun":false,"nativeAdmission":false,"fullSM":false});
    std::fs::write(
        root.join("control.json"),
        serde_json::to_vec_pretty(&observation).unwrap(),
    )
    .unwrap();
    eprintln!("ACTUAL_EXPERIMENT_REGISTRY_CONTROL={}", root.display());
}

#[test]
fn offline_archive_index_lock_and_renamed_edge() {
    fixture(true);
}
#[test]
fn incorrect_archive_checksum_refuses_before_cache_intake_or_resolver() {
    fixture(false);
}

#[test]
fn actual_owned_public_cache_archive_hashes_against_exact_cache_parser() {
    use std::collections::{BTreeMap, BTreeSet};
    let metadata_path = Path::new(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/public-registry-cache-copy-r1.json",
    );
    let raw_metadata = std::fs::read(metadata_path).unwrap();
    let mut metadata_hash = cargo_util::Sha256::new();
    metadata_hash.update(&raw_metadata);
    assert_eq!(
        metadata_hash.finish_hex(),
        "c84fa1cad1fee40b03c633c70a0bfd2fe3f097f2c863c3696a9b46f3b622ab1e"
    );
    let metadata: serde_json::Value = serde_json::from_slice(&raw_metadata).unwrap();
    let cache_root = PathBuf::from(metadata["ownedCache"].as_str().unwrap());
    let mut expected: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    let mut records = 0;
    for row in metadata["files"].as_array().unwrap() {
        let relative = row["path"].as_str().unwrap();
        if !relative.starts_with("index/") || !relative.contains("/.cache/") {
            continue;
        }
        let raw = std::fs::read(cache_root.join(relative)).unwrap();
        let mut hasher = cargo_util::Sha256::new();
        hasher.update(&raw);
        assert_eq!(hasher.finish_hex(), row["sha256"].as_str().unwrap());
        assert_eq!(raw.len() as u64, row["bytes"].as_u64().unwrap());
        let cache = crate::sources::registry::index::SpikeSummariesCache::parse(&raw).unwrap();
        for (version, raw) in cache.versions {
            let record: serde_json::Value = serde_json::from_slice(raw).unwrap();
            assert_eq!(version.to_string(), record["vers"].as_str().unwrap());
            let filename = format!(
                "{}-{}.crate",
                record["name"].as_str().unwrap(),
                record["vers"].as_str().unwrap()
            );
            expected
                .entry(filename)
                .or_default()
                .insert(record["cksum"].as_str().unwrap().to_string());
            records += 1;
        }
    }
    let mut archive_rows = Vec::new();
    for row in metadata["files"].as_array().unwrap() {
        let relative = row["path"].as_str().unwrap();
        if !relative.starts_with("cache/") || !relative.ends_with(".crate") {
            continue;
        }
        let raw = std::fs::read(cache_root.join(relative)).unwrap();
        let mut hasher = cargo_util::Sha256::new();
        hasher.update(&raw);
        let digest = hasher.finish_hex();
        assert_eq!(digest, row["sha256"].as_str().unwrap());
        assert_eq!(raw.len() as u64, row["bytes"].as_u64().unwrap());
        let name = Path::new(relative).file_name().unwrap().to_str().unwrap();
        let expected_checksums = expected.get(name).unwrap();
        assert_eq!(expected_checksums.len(), 1);
        assert!(expected_checksums.contains(&digest));
        archive_rows.push(serde_json::json!({"path":relative,"bytes":raw.len(),"sha256":digest,"expectedChecksums":expected_checksums}));
    }
    assert_eq!(archive_rows.len(), 234);
    assert_eq!(records, 11110);
    let root = tempfile::Builder::new()
        .prefix("opensip-public-cache-integrity-control-")
        .tempdir()
        .unwrap()
        .keep();
    let result = serde_json::json!({"root":root,"metadataPath":metadata_path,"cacheRoot":cache_root,"indexRecords":records,
        "archiveRows":archive_rows,"suppliedMetadataAndIndexOnly":true,"sourceAuthentication":false,
        "credentialRead":false,"resolverInvoked":false,"corpusResolutionRun":false,"nativeAdmission":false,"fullSM":false});
    std::fs::write(
        root.join("control.json"),
        serde_json::to_vec_pretty(&result).unwrap(),
    )
    .unwrap();
    eprintln!(
        "ACTUAL_EXPERIMENT_CACHE_INTEGRITY_CONTROL={}",
        root.display()
    );
}
