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
            let def = Definition::BuiltIn;
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
                    ConfigValue::Table(patches, Definition::BuiltIn),
                )]),
                Definition::BuiltIn,
            ),
        );
    }
    Ok(projected)
}

fn graph(
    root: &Path,
    project: &Path,
    supplied_values: HashMap<String, ConfigValue>,
) -> CargoResult<()> {
    let home = root.join("home");
    let queries = root.join("queries");
    std::fs::create_dir(&home)?;
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
    context.configure(0, false, Some("never"), false, false, true, &None, &[], &[])?;
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
    graph(&first, &serde, HashMap::new()).unwrap();
    graph(&second, &json, projection).unwrap();
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
