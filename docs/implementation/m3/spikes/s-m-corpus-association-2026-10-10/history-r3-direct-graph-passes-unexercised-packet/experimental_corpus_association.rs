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
    options.build_config.requested_kinds = vec![CompileKind::Target(CompileTarget::new(
        "aarch64-apple-darwin",
        false,
    )?)];
    options.build_config.unit_graph = true;
    let interner = UnitInterner::new();
    let bcx = crate::ops::create_bcx(&ws, &options, &interner, None)?;
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
    graph(
        &locked_root,
        &json,
        values(Some((&cfg, &sha)), &links).unwrap(),
        true,
    )
    .unwrap();
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
