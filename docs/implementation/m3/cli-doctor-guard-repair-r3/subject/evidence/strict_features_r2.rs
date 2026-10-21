fn allowed_feature_declarations() -> [(&'static str, &'static str, Value); 8] {
    [
        ("opensip-cli", "apps/cli", serde_json::json!({
            "operability-dev-sinks": ["opensip-host/operability-dev-sinks"],
            "harness-instrumentation": ["opensip-host/harness-instrumentation"]
        })),
        ("opensip-reporting", "crates/reporting", serde_json::json!({})),
        ("opensip-host", "crates/host", serde_json::json!({
            "crash-matrix": ["opensip-storage/crash-matrix", "opensip-security/crash-matrix", "opensip-platform/crash-matrix"],
            "operability-dev-sinks": ["opensip-operability/operability-dev-sinks"],
            "harness-instrumentation": ["opensip-operability/harness-instrumentation"]
        })),
        ("opensip-security", "crates/security", serde_json::json!({
            "crash-matrix": ["opensip-platform/crash-matrix"], "scenario-fixtures": []
        })),
        ("opensip-storage", "crates/storage", serde_json::json!({
            "crash-matrix": ["opensip-security/crash-matrix", "opensip-platform/crash-matrix"],
            "scenario-fixtures": ["opensip-security/scenario-fixtures"]
        })),
        ("opensip-operability", "crates/operability", serde_json::json!({
            "operability-dev-sinks": [], "harness-instrumentation": [], "test-mints": []
        })),
        ("opensip-platform", "crates/platform", serde_json::json!({
            "crash-matrix": [], "test-fixture": []
        })),
        ("opensip-lifecycle", "crates/lifecycle", serde_json::json!({
            "crash-matrix": ["opensip-security/crash-matrix"],
            "scenario-fixtures": ["opensip-security/scenario-fixtures"]
        })),
    ]
}
fn guarded_feature(feature: &str) -> bool {
    matches!(feature, "operability-dev-sinks" | "harness-instrumentation" | "crash-matrix"
        | "scenario-fixtures" | "test-mints" | "test-fixture")
}
fn resolve_node<'a>(doc: &'a Value, id: &Value) -> Option<&'a Value> {
    id.as_str()?;
    let mut nodes = doc["resolve"]["nodes"].as_array()?.iter().filter(|n| n["id"] == *id);
    let node = nodes.next()?;
    if nodes.next().is_some() { return None; }
    Some(node)
}
fn resolved_dependency<'a>(doc: &'a Value, package: &Value, alias: &str) -> Option<&'a Value> {
    let node = resolve_node(doc, &package["id"])?;
    let normalized = alias.replace('-', "_");
    let mut edges = node["deps"].as_array()?.iter().filter(|d| d["name"] == normalized);
    let edge = edges.next()?;
    edge["pkg"].as_str()?;
    if edges.next().is_some() { return None; }
    Some(edge)
}
fn dependency_alias(dep: &Value) -> Option<&str> {
    dep["rename"].as_str().or_else(|| dep["name"].as_str())
}
fn edge_has_declaration(edge: &Value, dep: &Value) -> bool {
    let (Some(kind), Some(target)) = (dep.get("kind"), dep.get("target")) else { return false; };
    edge["dep_kinds"].as_array().is_some_and(|kinds| kinds.iter().any(|k| {
        k.get("kind") == Some(kind) && k.get("target") == Some(target)
    }))
}
fn metadata_declared_features_are_closed(root: &Path, doc: &Value) -> bool {
    let Some(packages) = doc["packages"].as_array() else { return false; };
    let mut selected = std::collections::BTreeMap::new();
    for (name, directory, expected_features) in allowed_feature_declarations() {
        let Ok(expected_manifest) = root.join(directory).join("Cargo.toml").canonicalize() else { return false; };
        let matching: Vec<_> = packages.iter().filter(|p| {
            p["name"] == name && p["manifest_path"].as_str()
                .and_then(|p| Path::new(p).canonicalize().ok())
                .is_some_and(|actual| actual == expected_manifest)
        }).collect();
        if matching.len() != 1 || matching[0]["features"] != expected_features { return false; }
        let package = matching[0];
        let (kind, source) = if name == "opensip-cli" { ("bin", "src/main.rs") } else { ("lib", "src/lib.rs") };
        let Ok(expected_source) = root.join(directory).join(source).canonicalize() else { return false; };
        let Some(targets) = package["targets"].as_array() else { return false; };
        let targets: Vec<_> = targets.iter().filter(|t| t["kind"].as_array()
            .is_some_and(|kinds| kinds.iter().any(|k| k == kind))).collect();
        if targets.len() != 1 || !targets[0]["src_path"].as_str()
            .and_then(|p| Path::new(p).canonicalize().ok())
            .is_some_and(|actual| actual == expected_source) { return false; }
        if resolve_node(doc, &package["id"]).is_none() { return false; }
        selected.insert(name, package);
    }
    // Bind each allowed forwarding spelling to its actual resolved package,
    // not a same-spelling alias or a package row merely present elsewhere.
    for package in selected.values() {
        let Some(features) = package["features"].as_object() else { return false; };
        for items in features.values() {
            let Some(items) = items.as_array() else { return false; };
            for item in items {
                let Some(item) = item.as_str() else { return false; };
                let Some((alias, _)) = item.split_once('/') else { continue; };
                let Some(target) = selected.get(alias) else { return false; };
                let Some(edge) = resolved_dependency(doc, package, alias) else { return false; };
                if edge["pkg"] != target["id"] { return false; }
                let Some(dependencies) = package["dependencies"].as_array() else { return false; };
                if !dependencies.iter().any(|d| dependency_alias(d) == Some(alias)
                    && d.get("kind").is_some_and(Value::is_null)
                    && d.get("target").is_some_and(Value::is_null)
                    && edge_has_declaration(edge, d)) { return false; }
            }
        }
    }
    for package in packages {
        // An unapproved intermediate package cannot invent another feature
        // name/default which forwards into one of these guarded endpoints.
        let Some(features) = package["features"].as_object() else { return false; };
        for items in features.values() {
            let Some(items) = items.as_array() else { return false; };
            for item in items {
                let Some(item) = item.as_str() else { return false; };
                let Some((alias, feature)) = item.split_once('/') else { continue; };
                if !guarded_feature(feature) { continue; }
                let alias = alias.strip_suffix('?').unwrap_or(alias);
                let Some(edge) = resolved_dependency(doc, package, alias) else { return false; };
                if selected.values().any(|target| target["id"] == edge["pkg"])
                    && !selected.values().any(|source| source["id"] == package["id"]) { return false; }
            }
        }
        let Some(dependencies) = package["dependencies"].as_array() else { return false; };
        for dep in dependencies {
            let Some(features) = dep["features"].as_array() else { return false; };
            for feature in features {
                let Some(feature) = feature.as_str() else { return false; };
                if !guarded_feature(feature) { continue; }
                let Some(alias) = dependency_alias(dep) else { return false; };
                let Some(edge) = resolved_dependency(doc, package, alias) else { return false; };
                if !selected.values().any(|p| p["id"] == edge["pkg"]) { continue; }
                if !edge_has_declaration(edge, dep) { return false; }
                let allowed_dev_feature = dep["kind"] == "dev"
                    && matches!(feature, "scenario-fixtures" | "test-mints" | "test-fixture");
                if !allowed_dev_feature { return false; }
            }
        }
    }
    true
}
fn actual_declared_features_are_closed(root: &Path) -> bool {
    let Ok(output) = Command::new(env!("CARGO"))
        .args(["metadata", "--locked", "--offline", "--format-version", "1"])
        .current_dir(root).output() else { return false; };
    if !output.status.success() { return false; }
    let Ok(doc) = serde_json::from_slice::<Value>(&output.stdout) else { return false; };
    metadata_declared_features_are_closed(root, &doc)
}
fn is_forbidden_selector_token(token: &str) -> bool {
    matches!(token, "cfg" | "cfg_attr" | "feature" | "macro_rules" | "macro" | "derive" | "forbid" | "allow")
}
fn production_feature_sites_are_closed(text: &str, outcomes: bool) -> bool {
    // Every accepted feature gate and its actual logging body are in this
    // exact prefix. Copying an allowed gate onto another item gains nothing.
    let text = if outcomes {
        let Some(rest) = text.strip_prefix(KNOWN_LOGGING_PREFIX)
            .and_then(|rest| rest.strip_prefix(KNOWN_LOGGING_TESTS)) else { return false; };
        rest
    } else { text };
    let unaccounted = strip_known_test_tail(text).lines().map(str::trim).filter(|line| {
        !line.starts_with("//") && ![
            "#![forbid(unsafe_code)]",
            r#"#[cfg(target_os = "macos")]"#,
            r#"#[cfg(not(target_os = "macos"))]"#,
            "#[cfg(unix)]", "#[cfg(not(unix))]",
            "#[derive(Debug, Clone, Copy, PartialEq, Eq)]",
            "#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]",
            "#[derive(Debug, Clone, PartialEq, Eq)]",
            "#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]",
            "#[derive(Debug, PartialEq, Eq)]", "#[derive(Default)]",
        ].contains(line)
    }).collect::<Vec<_>>().join("\n");
    !unaccounted.contains('#') && !unaccounted
        .split(|c: char| !(c.is_ascii_alphanumeric() || c == '_'))
        .any(is_forbidden_selector_token)
}
fn feature_metadata_fixture(root: &Path) -> Value {
    let declarations = allowed_feature_declarations();
    let mut packages = Vec::new();
    let mut nodes = Vec::new();
    for (name, directory, features) in &declarations {
        let mut aliases = std::collections::BTreeSet::new();
        for items in features.as_object().unwrap().values() {
            for item in items.as_array().unwrap() {
                if let Some((alias, _)) = item.as_str().unwrap().split_once('/') { aliases.insert(alias); }
            }
        }
        let dependencies: Vec<_> = aliases.iter().map(|alias| {
            let target = declarations.iter().find(|d| d.0 == *alias).unwrap();
            serde_json::json!({"name": alias, "rename": null, "kind": null, "target": null,
                "features": [], "path": root.join(target.1)})
        }).collect();
        let edges: Vec<_> = aliases.iter().map(|alias| serde_json::json!({
            "name": alias.replace('-', "_"), "pkg": format!("pkg:{alias}"),
            "dep_kinds": [{"kind": null, "target": null}]
        })).collect();
        let (kind, source) = if *name == "opensip-cli" { ("bin", "src/main.rs") } else { ("lib", "src/lib.rs") };
        packages.push(serde_json::json!({"name": name, "id": format!("pkg:{name}"),
            "manifest_path": root.join(directory).join("Cargo.toml"), "features": features,
            "dependencies": dependencies, "targets": [{"kind": [kind], "src_path": root.join(directory).join(source)}]}));
        nodes.push(serde_json::json!({"id": format!("pkg:{name}"), "deps": edges, "features": []}));
    }
    serde_json::json!({"packages": packages, "resolve": {"nodes": nodes}})
}
#[test]
fn doctor_feature_declarations_keep_the_accepted_opt_in_graph() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let valid = feature_metadata_fixture(&root);
    assert!(metadata_declared_features_are_closed(&root, &valid));
    for index in 0..8 {
        for (feature, value) in [("default", serde_json::json!([])), ("default", serde_json::json!(["harness-instrumentation"])), ("home-test-bridge", serde_json::json!([]))] {
            let mut changed = valid.clone();
            changed["packages"][index]["features"][feature] = value;
            assert!(!metadata_declared_features_are_closed(&root, &changed), "unknown or default features must remain refused");
        }
        let mut foreign = valid.clone();
        foreign["packages"][index]["manifest_path"] = serde_json::json!(root.join("not-the-selected-manifest"));
        assert!(!metadata_declared_features_are_closed(&root, &foreign));
        let mut source = valid.clone();
        source["packages"][index]["targets"][0]["src_path"] = serde_json::json!(root.join("not-the-selected-source"));
        assert!(!metadata_declared_features_are_closed(&root, &source));
    }
    let mut retarget = valid.clone();
    retarget["packages"][0]["dependencies"][0]["name"] = serde_json::json!("doctor-bridge");
    retarget["packages"][0]["dependencies"][0]["rename"] = serde_json::json!("opensip-host");
    retarget["packages"][0]["dependencies"][0]["path"] = serde_json::json!(root.join("foreign/doctor-bridge"));
    retarget["resolve"]["nodes"][0]["deps"][0]["pkg"] = serde_json::json!("foreign:doctor-bridge");
    retarget["packages"].as_array_mut().unwrap().push(serde_json::json!({
        "id": "foreign:doctor-bridge", "name": "doctor-bridge", "manifest_path": root.join("foreign/doctor-bridge/Cargo.toml"),
        "features": {"harness-instrumentation": [], "operability-dev-sinks": []}, "dependencies": [], "targets": []}));
    retarget["resolve"]["nodes"].as_array_mut().unwrap().push(serde_json::json!({"id":"foreign:doctor-bridge","deps":[],"features":[]}));
    assert!(!metadata_declared_features_are_closed(&root, &retarget), "forwarding alias must bind the intended resolved package");
    for kind in [Value::Null, serde_json::json!("dev"), serde_json::json!("build")] {
        let mut activated = valid.clone();
        activated["packages"][0]["dependencies"][0]["kind"] = kind.clone();
        activated["packages"][0]["dependencies"][0]["features"] = serde_json::json!(["harness-instrumentation"]);
        activated["resolve"]["nodes"][0]["deps"][0]["dep_kinds"] = serde_json::json!([{"kind":null,"target":null},{"kind":kind,"target":null}]);
        assert!(!metadata_declared_features_are_closed(&root, &activated), "direct dependency activation must remain refused");
    }
    let mut forwarding = valid.clone();
    forwarding["packages"][0]["features"]["harness-instrumentation"] = serde_json::json!(["opensip-host/crash-matrix"]);
    assert!(!metadata_declared_features_are_closed(&root, &forwarding));
    let mut duplicate = valid.clone();
    duplicate["packages"].as_array_mut().unwrap().push(valid["packages"][0].clone());
    assert!(!metadata_declared_features_are_closed(&root, &duplicate));
    let mut missing = valid.clone();
    missing.as_object_mut().unwrap().remove("resolve");
    assert!(!metadata_declared_features_are_closed(&root, &missing));
    assert!(!metadata_declared_features_are_closed(&root, &serde_json::json!({})));
}
#[test]
fn doctor_feature_sites_reject_other_cfg_spellings_and_copied_gates() {
    let trusted = format!("{KNOWN_LOGGING_PREFIX}{KNOWN_LOGGING_TESTS}fn ordinary() {{}}\n");
    assert!(production_feature_sites_are_closed(&trusted, true));
    assert!(production_feature_sites_are_closed("#[cfg(unix)]\nfn ordinary() {}", false));
    for gate in [
        r#"#[cfg(any(feature = "harness-instrumentation"))]"#,
        r#"#[cfg_attr(feature = "operability-dev-sinks", path = "bridge.rs")]"#,
        r#"# [ cfg ( feature = "harness-instrumentation" ) ]"#,
        "#\n[cfg/*separator*/(any(feature = \"harness-instrumentation\"))]",
        r#"if cfg! ( feature = "harness-instrumentation" ) {}"#,
        r#"#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]"#,
        "#[unapproved_attribute]",
    ] {
        for (text, outcomes) in [(format!("{gate}\nfn alternate() {{}}"), false), (format!("{trusted}\n{gate}\nfn alternate() {{}}"), true)] {
            assert!(!production_feature_sites_are_closed(&text, outcomes), "unapproved feature selector syntax/site must remain refused: {gate}");
        }
    }
}
