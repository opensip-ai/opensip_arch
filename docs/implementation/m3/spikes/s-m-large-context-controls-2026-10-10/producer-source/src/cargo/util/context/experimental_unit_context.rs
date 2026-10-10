//! Outside-product experiment only. Caller paths/pins/links are supplied data.
use super::*;
use crate::core::Workspace;
use crate::core::compiler::{CompileKind, CompileTarget, UnitInterner, UserIntent};
use std::ffi::OsString;

fn values(
    config: Option<(&Path, &str)>,
    links: &[(String, PathBuf)],
) -> CargoResult<HashMap<String, ConfigValue>> {
    let mut projected = HashMap::new();
    if let Some((path, expected)) = config {
        let raw = std::fs::read(path)?;
        let mut hasher = cargo_util::Sha256::new();
        hasher.update(&raw);
        anyhow::ensure!(
            hasher.finish_hex() == expected,
            "supplied original config pin mismatch"
        );
        let text = std::str::from_utf8(&raw)?;
        let parsed: toml::Value = toml::from_str(text)?;
        // Parse all bytes into Cargo's real CV before suppressing selectors.
        let original = ConfigValue::from_toml(Definition::Path(path.to_path_buf()), parsed)?;
        let ConfigValue::Table(top, _) = original else {
            anyhow::bail!("config is not a table")
        };
        anyhow::ensure!(top.len() == 1, "outside observed experiment config shape");
        let Some(ConfigValue::Table(targets, _)) = top.get("target") else {
            anyhow::bail!("outside observed experiment config shape")
        };
        anyhow::ensure!(targets.len() == 2, "outside observed experiment target set");
        for (target, runner) in [
            ("wasm32-wasip1-threads", "wasmtime run -S threads --"),
            ("wasm32-wasip1", "wasmtime run --"),
        ] {
            let Some(ConfigValue::Table(row, _)) = targets.get(target) else {
                anyhow::bail!("outside observed experiment target set")
            };
            anyhow::ensure!(row.len() == 1, "outside observed experiment target values");
            let Some(ConfigValue::String(value, def)) = row.get("runner") else {
                anyhow::bail!("outside observed experiment runner shape")
            };
            anyhow::ensure!(
                value == runner && def == &Definition::Path(path.to_path_buf()),
                "outside observed experiment runner value"
            );
        }
        // The two original runner values are retained externally, never operational.
    }
    if !links.is_empty() {
        let names: std::collections::BTreeSet<_> = links.iter().map(|(n, _)| n.as_str()).collect();
        anyhow::ensure!(
            links.len() == 3
                && names
                    == std::collections::BTreeSet::from(["serde", "serde_core", "serde_derive"]),
            "not exact selected overlay link set"
        );
        let mut patches = HashMap::new();
        for (name, path) in links {
            anyhow::ensure!(
                path.is_absolute(),
                "overlay path must be explicit absolute path"
            );
            let def = Definition::Cli(None);
            patches.insert(
                name.clone(),
                ConfigValue::Table(
                    HashMap::from([(
                        "path".into(),
                        ConfigValue::String(
                            path.to_str()
                                .ok_or_else(|| anyhow::anyhow!("non-UTF8 experimental link"))?
                                .into(),
                            def.clone(),
                        ),
                    )]),
                    def,
                ),
            );
        }
        // Experiment-only selected T2 association, separate from original config.
        projected.insert(
            "patch".into(),
            ConfigValue::Table(
                HashMap::from([(
                    "crates-io".into(),
                    ConfigValue::Table(patches, Definition::Cli(None)),
                )]),
                Definition::Cli(None),
            ),
        );
    }
    Ok(projected)
}

fn graph(
    root: &Path,
    project: &Path,
    supplied_values: HashMap<String, ConfigValue>,
    locked: bool,
) -> CargoResult<()> {
    let home = root.join("home");
    let queries = root.join("queries");
    std::fs::create_dir_all(&home)?;
    std::fs::create_dir(&queries)?;
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
    let host = head.iter().chain(tail.iter()).map(OsString::from).collect();
    let target = head
        .iter()
        .chain(["--target", "aarch64-apple-darwin"].iter())
        .chain(tail.iter())
        .map(OsString::from)
        .collect();
    let base = cargo_util::ProcessBuilder::experimental_information_queries(
        Path::new("/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc"),
        project,
        vec![vec!["-vV".into()], host, target],
        "b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c".into(),
        &queries,
    );
    let mut context = GlobalContext::new_experimental_query_context(
        Shell::new(),
        project.to_path_buf(),
        home,
        supplied_values,
        base,
    );
    context.configure(
        0,
        false,
        Some("never"),
        false,
        locked,
        true,
        &None,
        &[],
        &[],
    )?;
    let mut ws = Workspace::new(&project.join("Cargo.toml"), &context)?;
    ws.set_target_dir(Filesystem::new(root.join("target")));
    let mut options = crate::ops::CompileOptions::new(&context, UserIntent::Check { test: false })?;
    options.spec = crate::ops::Packages::Default;
    // Use the same no-selector filter constructor as the pinned Cargo CLI.
    options.filter = crate::ops::CompileFilter::from_raw_arguments(
        false,
        vec![],
        false,
        vec![],
        false,
        vec![],
        false,
        vec![],
        false,
        false,
    );
    options.build_config.requested_kinds = vec![CompileKind::Target(CompileTarget::new(
        "aarch64-apple-darwin",
        false,
    )?)];
    options.build_config.unit_graph = true;
    let interner = UnitInterner::new();
    let bcx = crate::ops::create_bcx(&ws, &options, &interner, None)?;
    crate::core::compiler::capture_experimental_unit_context(&bcx, root)?;
    *context.shell() = Shell::from_write(Box::new(std::fs::File::create(
        root.join("unit-graph.json"),
    )?));
    crate::core::compiler::unit_graph::emit_serialized_unit_graph(
        &bcx.roots,
        &bcx.unit_graph,
        &context,
    )?;
    *context.shell() = Shell::new();
    Ok(())
}
fn write(root: &Path, p: &str, s: &str) {
    let path = root.join(p);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(path, s).unwrap();
}
fn retained_root() -> PathBuf {
    tempfile::Builder::new()
        .prefix("opensip-corpus-association-control-")
        .tempdir()
        .unwrap()
        .keep()
}
#[test]
fn two_original_workspaces_exact_three_links_and_stripped_runner() {
    let root = retained_root();
    let serde = root.join("serde-member");
    let json = root.join("json-member");
    write(
        &serde,
        "Cargo.toml",
        "[workspace]\nmembers=['serde','serde_core','serde_derive']\nresolver='2'\n",
    );
    for name in ["serde", "serde_core", "serde_derive"] {
        write(
            &serde,
            &format!("{name}/Cargo.toml"),
            &format!("[package]\nname='{name}'\nversion='1.0.0'\nedition='2024'\n"),
        );
        write(
            &serde,
            &format!("{name}/src/lib.rs"),
            "compile_error!(\"firstparty fixture source must not compile\");\n",
        );
    }
    write(
        &json,
        "Cargo.toml",
        "[package]\nname='json'\nversion='1.0.0'\nedition='2024'\n[dependencies]\nserde='=1.0.0'\nserde_core='=1.0.0'\nserde_derive='=1.0.0'\n",
    );
    write(
        &json,
        "src/lib.rs",
        "compile_error!(\"firstparty json fixture source must not compile\");\n",
    );
    let cfg = root.join("original/.cargo/config.toml");
    write(
        &root,
        "original/.cargo/config.toml",
        "[target.wasm32-wasip1-threads]\nrunner='wasmtime run -S threads --'\n[target.wasm32-wasip1]\nrunner='wasmtime run --'\n",
    );
    let raw = std::fs::read(&cfg).unwrap();
    let mut h = cargo_util::Sha256::new();
    h.update(&raw);
    let sha = h.finish_hex();
    let links: Vec<_> = ["serde", "serde_core", "serde_derive"]
        .iter()
        .map(|n| (n.to_string(), serde.join(n)))
        .collect();
    let projection = values(Some((&cfg, &sha)), &links).unwrap();
    assert_eq!(projection.len(), 1);
    assert!(!projection.contains_key("target"));
    let first = root.join("serde-observation");
    let second = root.join("json-observation");
    std::fs::create_dir(&first).unwrap();
    std::fs::create_dir(&second).unwrap();
    graph(&first, &serde, HashMap::new(), false).unwrap();
    graph(&second, &json, projection, false).unwrap();
    let one: serde_json::Value =
        serde_json::from_slice(&std::fs::read(first.join("unit-graph.json")).unwrap()).unwrap();
    let two: serde_json::Value =
        serde_json::from_slice(&std::fs::read(second.join("unit-graph.json")).unwrap()).unwrap();
    assert_eq!(one["roots"].as_array().unwrap().len(), 3);
    assert_eq!(two["roots"].as_array().unwrap().len(), 1);
    assert_eq!(two["units"].as_array().unwrap().len(), 4);
    for n in ["serde", "serde_core", "serde_derive"] {
        assert!(two["units"].as_array().unwrap().iter().any(|u| {
            u["pkg_id"]
                .as_str()
                .unwrap()
                .contains(&format!("serde-member/{n}"))
        }));
    }
    let original_lock = std::fs::read(json.join("Cargo.lock")).unwrap();
    let locked_root = root.join("json-locked-observation");
    std::fs::create_dir(&locked_root).unwrap();
    let originals: Vec<_> = ["Cargo.toml", "src/lib.rs", "Cargo.lock"]
        .iter()
        .map(|rel| {
            let bytes = std::fs::read(json.join(rel)).unwrap();
            let mut h = cargo_util::Sha256::new();
            h.update(&bytes);
            serde_json::json!({"path":rel,"bytes":bytes.len(),"sha256":h.finish_hex()})
        })
        .collect();
    collect_packet(
        &serde_json::json!({"observationRoot":locked_root,"project":json,"memberRoot":json,"originalFiles":originals,"configuration":{"path":cfg,"sha256":sha},"overlayLinks":links.iter().map(|(name,path)|serde_json::json!({"name":name,"path":path})).collect::<Vec<_>>(),"preserveOriginalLock":true}),
    );
    let outcome: serde_json::Value = serde_json::from_slice(
        &std::fs::read(locked_root.join("experiment-outcome.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(outcome["success"], true);
    assert_eq!(outcome["originalBytePinsReobserved"], true);
    assert_eq!(
        std::fs::read(json.join("Cargo.lock")).unwrap(),
        original_lock
    );
    assert_eq!(std::fs::read(&cfg).unwrap(), raw);
    assert!(!root.join("Cargo.toml").exists());
    std::fs::write(root.join("control.json"),serde_json::to_vec_pretty(&serde_json::json!({"root":root,"originalWorkspaces":2,"syntheticRootManifest":false,"originalConfigSha256":sha,"runnerKeysStripped":2,"overlayLinks":links,"fixtureSourcesExecuted":false,"sourceAuthentication":false,"nativeAdmission":false,"fullSM":false})).unwrap()).unwrap();
    eprintln!("ACTUAL_CORPUS_ASSOCIATION_CONTROL={}", root.display());
}
#[test]
fn unexpected_original_values_wrong_pin_and_duplicate_links_refuse_before_queries() {
    let root = retained_root();
    let cfg = root.join(".cargo/config.toml");
    write(&root, ".cargo/config.toml", "[build]\nrustc='forbidden'\n");
    let raw = std::fs::read(&cfg).unwrap();
    let mut h = cargo_util::Sha256::new();
    h.update(&raw);
    let sha = h.finish_hex();
    assert!(values(Some((&cfg, &sha)), &[]).is_err());
    assert!(values(Some((&cfg, &"0".repeat(64))), &[]).is_err());
    assert!(
        values(
            None,
            &[
                ("serde".into(), root.clone()),
                ("serde".into(), root.clone()),
                ("serde_core".into(), root.clone())
            ]
        )
        .is_err()
    );
    assert!(!root.join("queries").exists());
    std::fs::write(
        root.join("control.json"),
        "{\"prelaunchRefusals\":3,\"actualChildInvocations\":0,\"nativeAdmission\":false}",
    )
    .unwrap();
    eprintln!("ACTUAL_CORPUS_ASSOCIATION_CONTROL={}", root.display());
}

/// Explicit private supplied packet. No production admission, cache or capability.
#[test]
#[ignore]
fn collect_explicit_experimental_corpus_graph() {
    let packet_path =
        std::env::var_os("OPENSIP_EXPERIMENT_GRAPH_PACKET").expect("explicit owned packet path");
    let packet: serde_json::Value =
        serde_json::from_slice(&std::fs::read(packet_path).unwrap()).unwrap();
    collect_packet(&packet);
}
fn collect_packet(packet: &serde_json::Value) {
    let root = PathBuf::from(packet["observationRoot"].as_str().unwrap());
    let project = PathBuf::from(packet["project"].as_str().unwrap());
    let member = PathBuf::from(packet["memberRoot"].as_str().unwrap());
    assert!(
        root.is_absolute()
            && project.is_absolute()
            && member.is_absolute()
            && project.starts_with(&member)
    );
    assert!(!root.join("queries").exists() && !root.join("unit-graph.json").exists());
    // Verify all original supplied regular byte pins before Cargo reads them.
    // This does not close ancestor/same-reader races or confer source authority.
    let check_originals = || {
        for f in packet["originalFiles"].as_array().unwrap() {
            let rel = Path::new(f["path"].as_str().unwrap());
            assert!(
                !rel.is_absolute()
                    && rel
                        .components()
                        .all(|c| matches!(c, std::path::Component::Normal(_)))
            );
            let path = member.join(rel);
            let meta = std::fs::symlink_metadata(&path).unwrap();
            assert!(meta.file_type().is_file());
            let raw = std::fs::read(&path).unwrap();
            assert_eq!(raw.len() as u64, f["bytes"].as_u64().unwrap());
            let mut h = cargo_util::Sha256::new();
            h.update(&raw);
            assert_eq!(h.finish_hex(), f["sha256"].as_str().unwrap());
        }
    };
    check_originals();
    let config = packet
        .get("configuration")
        .filter(|v| !v.is_null())
        .map(|v| {
            (
                Path::new(v["path"].as_str().unwrap()),
                v["sha256"].as_str().unwrap(),
            )
        });
    let links: Vec<_> = packet["overlayLinks"]
        .as_array()
        .unwrap()
        .iter()
        .map(|v| {
            (
                v["name"].as_str().unwrap().to_owned(),
                PathBuf::from(v["path"].as_str().unwrap()),
            )
        })
        .collect();
    let projected = values(config, &links).unwrap();
    let locked = packet["preserveOriginalLock"].as_bool().unwrap();
    let result = graph(&root, &project, projected, locked);
    check_originals();
    let outcome = serde_json::json!({"success":result.is_ok(),"error":result.err().map(|e|format!("{e:#}")),"originalBytePinsReobserved":true,"experimentalLockCreation":!locked,"unitGraphOnly":true,"sourceAuthentication":false,"fixtureOrCorpusCodeExecuted":false,"nativeAdmission":false,"SMComplete":false});
    std::fs::write(
        root.join("experiment-outcome.json"),
        serde_json::to_vec_pretty(&outcome).unwrap(),
    )
    .unwrap();
    eprintln!("ACTUAL_EXPERIMENT_CORPUS_GRAPH={}", root.display());
}

#[test]
fn actual_packet_failure_is_retained_as_incomplete_not_graph_success() {
    let root = retained_root();
    let project = root.join("missing-original-manifest");
    std::fs::create_dir(&project).unwrap();
    collect_packet(
        &serde_json::json!({"observationRoot":root,"project":project,"memberRoot":project,"originalFiles":[],"configuration":null,"overlayLinks":[],"preserveOriginalLock":false}),
    );
    let outcome: serde_json::Value =
        serde_json::from_slice(&std::fs::read(root.join("experiment-outcome.json")).unwrap())
            .unwrap();
    assert_eq!(outcome["success"], false);
    assert!(outcome["error"].is_string());
    assert!(!root.join("unit-graph.json").exists());
    assert_eq!(std::fs::read_dir(root.join("queries")).unwrap().count(), 0);
    std::fs::write(
        root.join("control.json"),
        "{\"packetFailureRetained\":true,\"actualChildInvocations\":0,\"nativeAdmission\":false}",
    )
    .unwrap();
    eprintln!("ACTUAL_CORPUS_ASSOCIATION_CONTROL={}", root.display());
}

#[test]
fn unit_context_actual_manifest_environment_cwd_and_local_lints() {
    let root = retained_root();
    let project = root.join("project");
    write(
        &project,
        "Cargo.toml",
        "[package]\nname='unit-context'\nversion='2.3.4-beta.1'\nedition='2024'\nauthors=['First','Second']\ndescription='owned fixture'\nlicense='MIT'\n[lib]\nname='selected_lib'\n",
    );
    write(
        &project,
        "src/lib.rs",
        "compile_error!(\"fixture must not execute\");\n",
    );
    let observation = root.join("observation");
    std::fs::create_dir(&observation).unwrap();
    graph(&observation, &project, HashMap::new(), false).unwrap();
    let data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(observation.join("unit-context-data.json")).unwrap())
            .unwrap();
    let units = data["units"].as_array().unwrap();
    assert_eq!(units.len(), 1);
    let row = &units[0];
    let env = &row["constructedEnvironment"];
    assert_eq!(row["index"], 0);
    assert_eq!(row["cwd"], project.to_str().unwrap());
    assert_eq!(env["CARGO_MANIFEST_DIR"], project.to_str().unwrap());
    assert_eq!(
        env["CARGO_MANIFEST_PATH"],
        project.join("Cargo.toml").to_str().unwrap()
    );
    assert_eq!(env["CARGO_PKG_VERSION"], "2.3.4-beta.1");
    assert_eq!(env["CARGO_PKG_VERSION_MAJOR"], "2");
    assert_eq!(env["CARGO_PKG_VERSION_MINOR"], "3");
    assert_eq!(env["CARGO_PKG_VERSION_PATCH"], "4");
    assert_eq!(env["CARGO_PKG_VERSION_PRE"], "beta.1");
    assert_eq!(env["CARGO_PKG_AUTHORS"], "First:Second");
    assert_eq!(env["CARGO_PKG_DESCRIPTION"], "owned fixture");
    assert_eq!(env["CARGO_PKG_LICENSE"], "MIT");
    assert_eq!(env["CARGO_CRATE_NAME"], "selected_lib");
    assert_eq!(row["capLintArguments"], serde_json::json!([]));
    assert_eq!(row["localPackageByActualCargo"], true);
    assert_eq!(row["completeCompilerCommand"], false);
    assert_eq!(data["BuildRunnerUsed"], false);
    assert_eq!(
        std::fs::read(project.join("src/lib.rs")).unwrap(),
        b"compile_error!(\"fixture must not execute\");\n"
    );
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}", root.display());
}
#[test]
fn unit_context_actual_two_package_index_join_and_renamed_edge() {
    let root = retained_root();
    let project = root.join("project");
    write(
        &project,
        "Cargo.toml",
        "[workspace]\nmembers=['one','two']\nresolver='2'\n",
    );
    write(
        &project,
        "one/Cargo.toml",
        "[package]\nname='one'\nversion='1.0.0'\nedition='2024'\n[dependencies]\nrenamed={package='two',path='../two'}\n",
    );
    write(
        &project,
        "two/Cargo.toml",
        "[package]\nname='two'\nversion='4.5.6'\nedition='2024'\n",
    );
    for name in ["one", "two"] {
        write(
            &project,
            &format!("{name}/src/lib.rs"),
            "compile_error!(\"not executed\");\n",
        );
    }
    let observation = root.join("observation");
    std::fs::create_dir(&observation).unwrap();
    graph(&observation, &project, HashMap::new(), false).unwrap();
    let data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(observation.join("unit-context-data.json")).unwrap())
            .unwrap();
    let graph: serde_json::Value =
        serde_json::from_slice(&std::fs::read(observation.join("unit-graph.json")).unwrap())
            .unwrap();
    assert_eq!(data["units"].as_array().unwrap().len(), 2);
    for (index, row) in data["units"].as_array().unwrap().iter().enumerate() {
        assert_eq!(row["index"], index);
        assert_eq!(row["packageId"], graph["units"][index]["pkg_id"]);
        assert_eq!(row["target"], graph["units"][index]["target"]);
        assert_eq!(row["profile"], graph["units"][index]["profile"]);
        assert_eq!(row["platform"], graph["units"][index]["platform"]);
        assert_eq!(row["features"], graph["units"][index]["features"]);
        assert_eq!(row["capLintArguments"], serde_json::json!([]));
    }
    assert!(graph["units"].as_array().unwrap().iter().any(|row| {
        row["dependencies"]
            .as_array()
            .unwrap()
            .iter()
            .any(|dep| dep["extern_crate_name"] == "renamed")
    }));
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}", root.display());
}

use crate::core::SourceId;
fn unit_context_registry_fixture(valid_checksum: bool) {
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
        eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}", root.display());
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
        crate::core::compiler::capture_experimental_unit_context(&bcx, &root).unwrap();
        let context_data: serde_json::Value =
            serde_json::from_slice(&std::fs::read(root.join("unit-context-data.json")).unwrap())
                .unwrap();
        let rows = context_data["units"].as_array().unwrap();
        assert_eq!(rows.len(), 2);
        let dependency = rows
            .iter()
            .find(|r| r["constructedEnvironment"]["CARGO_PKG_NAME"] == "opensip-fixture-dep")
            .unwrap();
        assert_eq!(
            dependency["capLintArguments"],
            serde_json::json!(["--cap-lints", "allow"])
        );
        assert_eq!(dependency["localPackageByActualCargo"], false);
        assert_eq!(dependency["showWarningsByActualCargo"], false);
        let app = rows
            .iter()
            .find(|r| r["constructedEnvironment"]["CARGO_PKG_NAME"] == "app")
            .unwrap();
        assert_eq!(app["capLintArguments"], serde_json::json!([]));
        assert_eq!(app["localPackageByActualCargo"], true);
        assert_eq!(
            dependency["constructedEnvironment"]["CARGO_CRATE_NAME"],
            "opensip_fixture_dep"
        );

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
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}", root.display());
}

#[test]
fn unit_context_registry_lint_cap_matches_actual_cargo() {
    unit_context_registry_fixture(true);
}

#[test]
fn unit_context_default_cli_target_filter_preserves_features() {
    let root = retained_root();
    let project = root.join("project");
    write(
        &project,
        "Cargo.toml",
        "[package]\nname='feature-filter'\nversion='1.0.0'\nedition='2024'\n[features]\nextra=[]\n[[bin]]\nname='feature-only'\npath='src/main.rs'\nrequired-features=['extra']\n",
    );
    write(
        &project,
        "src/lib.rs",
        "compile_error!(\"not executed\");\n",
    );
    write(
        &project,
        "src/main.rs",
        "compile_error!(\"feature-only target must not execute\");\n",
    );
    let observation = root.join("observation");
    std::fs::create_dir(&observation).unwrap();
    graph(&observation, &project, HashMap::new(), false).unwrap();
    let data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(observation.join("unit-context-data.json")).unwrap())
            .unwrap();
    let graph: serde_json::Value =
        serde_json::from_slice(&std::fs::read(observation.join("unit-graph.json")).unwrap())
            .unwrap();
    assert_eq!(graph["units"].as_array().unwrap().len(), 1);
    assert_eq!(graph["roots"].as_array().unwrap().len(), 1);
    assert_eq!(
        graph["units"][0]["target"]["kind"],
        serde_json::json!(["lib"])
    );
    assert_eq!(graph["units"][0]["features"], serde_json::json!([]));
    assert_eq!(data["units"][0]["target"], graph["units"][0]["target"]);
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}", root.display());
}
