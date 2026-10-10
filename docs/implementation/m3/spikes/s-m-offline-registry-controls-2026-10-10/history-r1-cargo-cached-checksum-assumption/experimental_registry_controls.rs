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
    std::fs::copy("/tmp/opensip-implementation/sm-offline-registry-controls-2026-10-10/first-party-fixture.crate",archives.join("opensip-fixture-dep-1.0.0.crate")).unwrap();
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
fn incorrect_archive_checksum_refuses_without_graph() {
    fixture(false);
}
