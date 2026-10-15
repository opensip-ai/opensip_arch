// Law M3-B r4, unit B1-a (plan r2 sections 5 and 6): the configuration
// resolver's controls. PCM byte vectors from tools/host/configuration_vectors.py
// pin every shared case; the cases PCM cannot express (layer allowlists,
// host-built layers, pin/hold conflicts, the X12 order) are Rust only.

const VECTORS: &str = include_str!("configuration_vectors.json");
const CLASSES: &str = include_str!("configuration_classes.json");
const PCS_SOURCE: &[u8] =
    include_bytes!("../../../schemas/sources/product-configuration-v2.schema.json");
const IDENTITY_SOURCE: &[u8] = include_bytes!("../../../schemas/sources/identity-v3.schema.json");
/// B-S9's remedy: 706 ASCII bytes and this SHA-256 (BS9, "The change").
const S9_SHA256: &str = "7ba6e8e50dc3c52f595caf01236019d2cfac6d8f0fd2e40d0dd3644fb0692565";
const STABLE_A: &str = "0f0e0d0c-0b0a-4908-8706-050403020100";
const STABLE_B: &str = "1f1e1d1c-1b1a-4918-9716-151413121110";

fn strs(value: &Value) -> Vec<String> {
    value
        .as_array()
        .unwrap()
        .iter()
        .map(|v| v.as_str().unwrap().to_owned())
        .collect()
}
fn component_version(value: &Value) -> ComponentVersionV1 {
    ComponentVersionV1 {
        stable_id: value["stableId"].as_str().unwrap().to_owned(),
        version: value["version"].as_str().unwrap().to_owned(),
    }
}
fn component_request(value: &Value) -> ComponentRequestV1 {
    let stable_id = value["stableId"].as_str().unwrap().to_owned();
    match &value["versionConstraint"] {
        Value::Null => ComponentRequestV1::Version(component_version(value)),
        Value::String(constraint) => ComponentRequestV1::Constraint {
            stable_id,
            constraint: constraint.clone(),
        },
        range => ComponentRequestV1::Range {
            stable_id,
            min: range["min"].as_str().unwrap().to_owned(),
            max: range["max"].as_str().unwrap().to_owned(),
            include_min: range["includeMin"].as_bool().unwrap(),
            include_max: range["includeMax"].as_bool().unwrap(),
        },
    }
}
/// A fixture's defaults document as the typed layer. Only the fields layer 1
/// admits may appear, so the conversion is lossless.
fn defaults_from(value: &Value) -> CompiledDefaultsV1 {
    let sections: Vec<&str> = value
        .as_object()
        .unwrap()
        .keys()
        .map(String::as_str)
        .collect();
    assert!(
        sections
            .iter()
            .all(|s| ["schemaVersion", "analysis", "components", "policy"].contains(s)),
        "{sections:?}"
    );
    let analysis = &value["analysis"];
    let components = &value["components"];
    CompiledDefaultsV1 {
        profile_id: analysis
            .get("profileId")
            .map(|v| v.as_str().unwrap().to_owned()),
        capabilities: analysis.get("capabilities").map(strs),
        budget_limit: analysis.get("budget").map(|b| b["limit"].as_u64().unwrap()),
        request: components.get("request").map(|r| {
            r.as_array()
                .unwrap()
                .iter()
                .map(component_request)
                .collect()
        }),
        pins: components.get("pins").map(|r| {
            r.as_array()
                .unwrap()
                .iter()
                .map(component_version)
                .collect()
        }),
        holds: components.get("holds").map(|r| {
            r.as_array()
                .unwrap()
                .iter()
                .map(component_version)
                .collect()
        }),
        allowed_scopes: components.get("allowedScopes").map(strs),
        pack_ids: value.get("policy").and_then(|p| p.get("packIds")).map(strs),
    }
}
fn carrier(name: &str, bytes: &[u8]) -> CapturedCarrierV1 {
    CapturedCarrierV1 {
        path: format!("{name}.json"),
        bytes: bytes.to_vec(),
    }
}
fn input_from(case: &Value) -> ResolverInputV1 {
    let layers = &case["layers"];
    let external = |name: &str| {
        layers
            .get(name)
            .map(|v| carrier(name, v.as_str().unwrap().as_bytes()))
    };
    ResolverInputV1 {
        defaults: defaults_from(&layers["defaults"]),
        global: external("global"),
        project: external("project"),
        local: external("local"),
        flags: FlagLayerV1 {
            workspace_roots: layers
                .get("flags")
                .map(|f| strs(&f["discovery"]["workspaceRoots"])),
        },
        mode: InvocationModeV1 {
            interactive: case["interactive"].as_bool().unwrap(),
        },
    }
}
fn vector_cases() -> Vec<Value> {
    let vectors: Value = serde_json::from_str(VECTORS).unwrap();
    vectors["cases"].as_array().unwrap().clone()
}
fn vector(id: &str) -> Value {
    vector_cases()
        .into_iter()
        .find(|c| c["id"] == id)
        .unwrap_or_else(|| panic!("{id}"))
}
fn as_serde(value: &V) -> Value {
    serde_json::from_slice(&canonical_bytes(value).unwrap()).unwrap()
}
/// The PCM refusal class a product refusal corresponds to.
fn pcm_class(refusal: &ConfigurationRefusal) -> &'static str {
    match refusal.step() {
        ConfigurationStep::Lexical => "LEXICAL",
        ConfigurationStep::Schema | ConfigurationStep::SchemaOne => "SCHEMA",
        ConfigurationStep::LogicalPath => "CONFIG_LOGICAL_PATH",
        ConfigurationStep::Profile => match refusal {
            ConfigurationRefusal::Invalid { subject, .. } if subject == "profile:missing" => {
                "CONFIG_PROFILE_MISSING"
            }
            _ => "CONFIG_PROFILE_UNREGISTERED",
        },
        ConfigurationStep::Capability => "CONFIG_CAPABILITY_UNREGISTERED",
        ConfigurationStep::Waiver => "CONFIG_WAIVER_UNREGISTERED",
        ConfigurationStep::Component => "CONFIG_DUPLICATE_COMPONENT",
        ConfigurationStep::DefaultsComplete => "CONFIG_DEFAULTS_INCOMPLETE",
        ConfigurationStep::Allowlist | ConfigurationStep::Semantic => "PRODUCT-ONLY",
    }
}
fn resolve_ok(input: &ResolverInputV1) -> ResolvedConfigurationV1 {
    resolve(input).unwrap_or_else(|r| panic!("{r:?}"))
}
fn base() -> ResolverInputV1 {
    input_from(&vector("base"))
}
fn invalid(step: ConfigurationStep, subject: &str) -> ConfigurationRefusal {
    ConfigurationRefusal::Invalid {
        step,
        subject: subject.to_owned(),
    }
}
fn invariant(step: ConfigurationStep, subject: &str) -> ConfigurationRefusal {
    ConfigurationRefusal::HostInvariant {
        step,
        subject: subject.to_owned(),
    }
}
fn with_project(text: &str) -> ResolverInputV1 {
    ResolverInputV1 {
        project: Some(carrier("project", text.as_bytes())),
        ..base()
    }
}
fn with_layer(layer: Layer, text: &str) -> ResolverInputV1 {
    let mut input = base();
    let c = Some(carrier(layer.as_str(), text.as_bytes()));
    match layer {
        Layer::Global => input.global = c,
        Layer::Project => input.project = c,
        Layer::Local => {
            input.local = c;
            input.mode.interactive = true;
        }
        Layer::Defaults | Layer::Flags => panic!("{layer:?} is host-built"),
    }
    input
}
fn semantic_leaf<'a>(resolved: &'a ResolvedConfigurationV1, section: &str, field: &str) -> &'a V {
    let V::Object(sections) = &resolved.semantic else {
        panic!()
    };
    let V::Object(fields) = &sections[section] else {
        panic!()
    };
    &fields[field]
}

#[test]
fn every_pcm_vector_is_reproduced_byte_for_byte() {
    let vectors: Value = serde_json::from_str(VECTORS).unwrap();
    // The vectors were computed by PCM at its accepted bytes.
    let pcm = &vectors["sources"][0];
    assert_eq!(
        pcm["path"],
        "docs/coop/design-corrections/foundation/product-configuration-model.py"
    );
    assert_eq!(
        pcm["sha256"],
        "055ab34c76f3d241633dd8e0d0a0b017c29747056a9d8de75b29bf57bd79fa8b"
    );
    let cases = vector_cases();
    assert!(cases.len() >= 50, "{}", cases.len());
    for case in &cases {
        let id = case["id"].as_str().unwrap();
        let expected = &case["pcm"];
        match resolve(&input_from(case)) {
            Ok(resolved) => {
                assert_eq!(
                    expected["digest"].as_str(),
                    Some(resolved.resolved_config_digest.as_str()),
                    "{id}: {expected}"
                );
                assert_eq!(as_serde(&resolved.semantic), expected["semantic"], "{id}");
                let layers: BTreeMap<&str, &str> = resolved
                    .provenance
                    .iter()
                    .map(|(leaf, p)| (leaf.as_str(), p.layer.as_str()))
                    .collect();
                let pcm_layers: BTreeMap<&str, &str> = expected["provenance"]
                    .as_object()
                    .unwrap()
                    .iter()
                    .map(|(leaf, layer)| (leaf.as_str(), layer.as_str().unwrap()))
                    .collect();
                assert_eq!(layers, pcm_layers, "{id}");
            }
            Err(refusal) => {
                assert_eq!(
                    expected["refusal"].as_str(),
                    Some(pcm_class(&refusal)),
                    "{id}: {refusal:?}"
                );
            }
        }
    }
}

#[test]
fn the_digest_is_the_raw_sha256_of_the_canonical_semantic_record() {
    let resolved = resolve_ok(&base());
    let raw = canonical_bytes(&resolved.semantic).unwrap();
    assert_eq!(
        resolved.resolved_config_digest,
        digest_hex(&raw_sha256(&raw))
    );
    assert_eq!(resolved.resolved_config_digest.len(), 64);
    assert!(
        resolved
            .resolved_config_digest
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    );
    // All five sections, always; the operational record holds the rest.
    let V::Object(sections) = &resolved.semantic else {
        panic!()
    };
    assert_eq!(
        sections.keys().map(String::as_str).collect::<Vec<_>>(),
        ["analysis", "components", "discovery", "evidence", "policy"]
    );
    let V::Object(operational) = &resolved.operational else {
        panic!()
    };
    assert_eq!(
        operational.keys().map(String::as_str).collect::<Vec<_>>(),
        ["retention", "ui"]
    );
}

#[test]
fn each_step_refuses_on_its_own_row_with_the_layer_and_pointer() {
    use ConfigurationStep as S;
    let cases: Vec<(&str, ResolverInputV1, ConfigurationRefusal)> = vec![
        (
            "lexical",
            with_project("{\"schemaVersion\":2.0}"),
            invalid(S::Lexical, "layer:project:"),
        ),
        (
            "schema",
            with_project("{\"schemaVersion\":2,\"shell\":1}"),
            invalid(S::Schema, "layer:project:"),
        ),
        (
            "schema-one carrier schema",
            with_project("{\"schemaVersion\":1,\"discovery\":{}}"),
            invalid(S::Schema, "layer:project:"),
        ),
        (
            "allowlist",
            with_layer(
                Layer::Global,
                "{\"schemaVersion\":2,\"discovery\":{\"entryPoints\":[\"a.rs\"]}}",
            ),
            invalid(S::Allowlist, "layer:global:/discovery/entryPoints"),
        ),
        (
            "logical path",
            with_project(
                "{\"schemaVersion\":2,\"discovery\":{\"ignorePaths\":[\"ok\",\"a/../b\"]}}",
            ),
            invalid(S::LogicalPath, "layer:project:/discovery/ignorePaths/1"),
        ),
        (
            "profile",
            with_project("{\"schemaVersion\":2,\"analysis\":{\"profileId\":\"other\"}}"),
            invalid(S::Profile, "profile:other"),
        ),
        (
            "capability",
            with_project(
                "{\"schemaVersion\":2,\"analysis\":{\"capabilities\":[\"syntax\",\"rust.imports\"]}}",
            ),
            invalid(S::Capability, "layer:project:/analysis/capabilities/1"),
        ),
        (
            "waiver",
            with_project("{\"schemaVersion\":2,\"policy\":{\"waiverIds\":[\"w\"]}}"),
            invalid(S::Waiver, "layer:project:/policy/waiverIds/0"),
        ),
    ];
    for (name, input, expected) in cases {
        assert_eq!(resolve(&input), Err(expected), "{name}");
    }
    // Profile missing is the caller's: the defaults supply no profile.
    let mut input = base();
    input.defaults.profile_id = None;
    assert_eq!(resolve(&input), Err(invalid(S::Profile, "profile:missing")));
    // Defaults completeness is the host's.
    for (field, clear) in [
        (
            "capabilities",
            (|d: &mut CompiledDefaultsV1| d.capabilities = None) as fn(&mut CompiledDefaultsV1),
        ),
        ("budget", |d: &mut CompiledDefaultsV1| d.budget_limit = None),
    ] {
        let mut input = base();
        clear(&mut input.defaults);
        assert_eq!(
            resolve(&input),
            Err(invariant(
                S::DefaultsComplete,
                &format!("layer:defaults:/analysis/{field}")
            )),
            "{field}"
        );
    }
}

#[test]
fn components_are_stated_once_with_no_conflicting_pin_and_hold() {
    use ConfigurationStep::Component;
    let request =
        |items: &str| format!("{{\"schemaVersion\":2,\"components\":{{\"request\":[{items}]}}}}");
    let a = format!("{{\"stableId\":\"{STABLE_A}\",\"version\":\"1.0.0\"}}");
    let a2 = format!("{{\"stableId\":\"{STABLE_A}\",\"version\":\"2.0.0\"}}");
    let b = format!("{{\"stableId\":\"{STABLE_B}\",\"version\":\"1.0.0\"}}");
    // Byte-identical duplicates refuse before normalization could merge them.
    assert_eq!(
        resolve(&with_project(&request(&format!("{a},{b},{a}")))),
        Err(invalid(Component, "layer:project:/components/request/2"))
    );
    assert_eq!(
        resolve(&with_project(&request(&format!("{a},{a2}")))),
        Err(invalid(Component, "layer:project:/components/request/1"))
    );
    // Across pins and holds: a duplicate (same version) and a conflict
    // (another version) both refuse, at the second appearance.
    let pins_holds = |pins: &str, holds: &str| {
        format!("{{\"schemaVersion\":2,\"components\":{{\"pins\":[{pins}],\"holds\":[{holds}]}}}}")
    };
    for (pins, holds, pointer) in [
        (a.clone(), a.clone(), "/components/holds/0"),
        (a.clone(), a2.clone(), "/components/holds/0"),
        (format!("{a},{a2}"), String::new(), "/components/pins/1"),
        (b.clone(), format!("{a},{a2}"), "/components/holds/1"),
    ] {
        assert_eq!(
            resolve(&with_project(&pins_holds(&pins, &holds))),
            Err(invalid(Component, &format!("layer:project:{pointer}"))),
            "{pins} | {holds}"
        );
    }
    // Pins and holds from different layers meet after the merge.
    let mut input = with_project(&format!(
        "{{\"schemaVersion\":2,\"components\":{{\"pins\":[{a}]}}}}"
    ));
    input.local = Some(carrier(
        "local",
        format!("{{\"schemaVersion\":2,\"components\":{{\"holds\":[{a2}]}}}}").as_bytes(),
    ));
    input.mode.interactive = true;
    assert_eq!(
        resolve(&input),
        Err(invalid(Component, "layer:local:/components/holds/0"))
    );
    resolve_ok(&with_project(&pins_holds(&a, &b)));
}

#[test]
fn an_external_value_cannot_repair_incomplete_compiled_defaults() {
    // Codex B1A-R1-RF-01: completeness is of the compiled defaults themselves.
    let capabilities = "{\"schemaVersion\":2,\"analysis\":{\"capabilities\":[\"imports\"]}}";
    let budget =
        "{\"schemaVersion\":2,\"analysis\":{\"budget\":{\"unit\":\"work-units\",\"limit\":7}}}";
    for (field, layer, document) in [
        ("capabilities", Layer::Project, capabilities),
        ("capabilities", Layer::Local, capabilities),
        ("budget", Layer::Global, budget),
        ("budget", Layer::Project, budget),
    ] {
        let mut input = with_layer(layer, document);
        match field {
            "capabilities" => input.defaults.capabilities = None,
            _ => input.defaults.budget_limit = None,
        }
        assert_eq!(
            resolve(&input),
            Err(invariant(
                ConfigurationStep::DefaultsComplete,
                &format!("layer:defaults:/analysis/{field}")
            )),
            "{field} {layer:?}"
        );
        // The same override of complete defaults is lawful.
        let resolved = resolve_ok(&with_layer(layer, document));
        assert_eq!(
            resolved.provenance[&format!("analysis.{field}")].layer,
            layer
        );
    }
}

#[test]
fn a_conflict_an_external_layer_introduces_is_the_callers() {
    // Codex B1A-R1-RF-02: pins and holds can win from different layers. An
    // external occurrence is named whenever one is involved; the conflict is
    // the host's only when both occurrences are host-built.
    use ConfigurationStep::Component;
    let item = |version: &str| ComponentVersionV1 {
        stable_id: STABLE_A.into(),
        version: version.into(),
    };
    let external = |field: &str, version: &str| {
        format!(
            "{{\"schemaVersion\":2,\"components\":{{\"{field}\":[{{\"stableId\":\"{STABLE_A}\",\"version\":\"{version}\"}}]}}}}"
        )
    };
    for version in ["1.0.0", "2.0.0"] {
        // Default holds, project pins: the project's pin is named.
        let mut input = with_project(&external("pins", version));
        input.defaults.holds = Some(vec![item("1.0.0")]);
        assert_eq!(
            resolve(&input),
            Err(invalid(Component, "layer:project:/components/pins/0")),
            "{version}"
        );
        // Default pins, project holds: the project's hold is named.
        let mut input = with_project(&external("holds", version));
        input.defaults.pins = Some(vec![item("1.0.0")]);
        assert_eq!(
            resolve(&input),
            Err(invalid(Component, "layer:project:/components/holds/0")),
            "{version}"
        );
        // Both occurrences host-built: the host's.
        let mut input = base();
        input.defaults.pins = Some(vec![item("1.0.0")]);
        input.defaults.holds = Some(vec![item(version)]);
        assert_eq!(
            resolve(&input),
            Err(invariant(Component, "layer:defaults:/components/holds/0")),
            "{version}"
        );
    }
}

#[test]
fn swapped_order_mutations_fail_their_controls() {
    // Schema per layer before the merge: an invalid project leaf refuses even
    // when the local layer would override it.
    let mut input = with_project("{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[]}}");
    input.local = Some(carrier(
        "local",
        b"{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[\"a\"]}}",
    ));
    input.mode.interactive = true;
    assert_eq!(
        resolve(&input),
        Err(invalid(ConfigurationStep::Schema, "layer:project:"))
    );
    // The allowlist per layer before the merge: a global leaf the layer does not
    // admit refuses even when the project overrides it.
    let mut input = with_layer(
        Layer::Global,
        "{\"schemaVersion\":2,\"discovery\":{\"entryPoints\":[\"a.rs\"]}}",
    );
    input.project = Some(carrier(
        "project",
        b"{\"schemaVersion\":2,\"discovery\":{\"entryPoints\":[\"b.rs\"]}}",
    ));
    assert_eq!(
        resolve(&input),
        Err(invalid(
            ConfigurationStep::Allowlist,
            "layer:global:/discovery/entryPoints"
        ))
    );
    // Lexical before schema: a duplicate key is lexical even though the
    // document would also fail the schema.
    assert_eq!(
        resolve(&with_project(
            "{\"schemaVersion\":2,\"shell\":1,\"shell\":2}"
        )),
        Err(invalid(ConfigurationStep::Lexical, "layer:project:"))
    );
    // Every layer is admitted before any merge: a later layer's defect wins
    // over an earlier layer's post-merge (registry) defect.
    let mut input = with_project("{\"schemaVersion\":2,\"analysis\":{\"profileId\":\"other\"}}");
    input.global = Some(carrier("global", b"not json"));
    assert_eq!(
        resolve(&input),
        Err(invalid(ConfigurationStep::Lexical, "layer:global:"))
    );
}

/// One valid sample value for every PCS leaf, and a second, different one.
fn samples(section: &str, field: &str) -> [String; 2] {
    let version = |id: &str, v: &str| format!("[{{\"stableId\":\"{id}\",\"version\":\"{v}\"}}]");
    let pair = |a: &str, b: &str| [a.to_owned(), b.to_owned()];
    match (section, field) {
        ("analysis", "profileId") => pair("\"default\"", "\"default\""),
        ("analysis", "capabilities") => pair("[\"imports\"]", "[\"calls\",\"types\"]"),
        ("analysis", "budget") => pair(
            "{\"unit\":\"work-units\",\"limit\":5}",
            "{\"unit\":\"work-units\",\"limit\":6}",
        ),
        ("components", "request") => [version(STABLE_A, "1.0.0"), version(STABLE_B, "1.0.0")],
        ("components", "pins") => [version(STABLE_B, "1.0.0"), version(STABLE_B, "1.0.1")],
        ("components", "holds") => [version(STABLE_B, "2.0.0"), version(STABLE_A, "2.0.0")],
        ("components", "allowedScopes") => pair("[\"global\"]", "[\"project\",\"global\"]"),
        ("discovery", "entryPoints") => pair("[\"src/a.rs\"]", "[]"),
        ("discovery", "workspaceRoots") => pair("[\"lib\"]", "[\".\"]"),
        ("discovery", "ignorePaths") => pair("[\"dist\"]", "[\"dist\",\"out\"]"),
        ("policy", "packIds") => pair("[\"opensip.preview.typescript.pack:1\"]", "[]"),
        ("policy", "waiverIds") => pair("[]", "[]"),
        ("evidence", "importIds") => pair(
            "[]",
            "[\"import2:0000000000000000000000000000000000000000000000000000000000000000\"]",
        ),
        ("retention", _) => pair("1", "null"),
        ("ui", "color") => pair("\"never\"", "\"always\""),
        other => panic!("no sample for {other:?}"),
    }
}
fn leaf_document(section: &str, field: &str, value: &str) -> String {
    format!("{{\"schemaVersion\":2,\"{section}\":{{\"{field}\":{value}}}}}")
}

#[test]
fn the_per_layer_allowlist_matrix_covers_every_pcs_leaf_and_layer() {
    for (section, field, _, layers) in FIELDS {
        for layer in [Layer::Global, Layer::Project, Layer::Local] {
            // Without the base project file, so it cannot mask the leaf.
            let mut input = with_layer(
                layer,
                &leaf_document(section, field, &samples(section, field)[0]),
            );
            if layer != Layer::Project {
                input.project = None;
            }
            let result = resolve(&input);
            if layers.contains(&layer) {
                let resolved =
                    result.unwrap_or_else(|r| panic!("{section}.{field} {layer:?}: {r:?}"));
                assert_eq!(
                    resolved.provenance[&format!("{section}.{field}")].layer,
                    layer
                );
            } else {
                assert_eq!(
                    result,
                    Err(invalid(
                        ConfigurationStep::Allowlist,
                        &format!("layer:{}:/{section}/{field}", layer.as_str())
                    )),
                    "{section}.{field} {layer:?}"
                );
            }
        }
    }
    // The host-built layers: every leaf the typed defaults can set is exactly
    // the defaults allowlist, and the flags layer sets only workspaceRoots.
    let full = CompiledDefaultsV1 {
        request: Some(vec![ComponentRequestV1::Version(ComponentVersionV1 {
            stable_id: STABLE_A.into(),
            version: "1.0.0".into(),
        })]),
        pins: Some(vec![]),
        holds: Some(vec![]),
        ..base().defaults
    };
    let resolved = resolve_ok(&ResolverInputV1 {
        defaults: full,
        global: None,
        project: None,
        local: None,
        flags: FlagLayerV1 {
            workspace_roots: Some(vec!["src".into()]),
        },
        mode: InvocationModeV1 { interactive: false },
    });
    for (section, field, _, layers) in FIELDS {
        let won = resolved
            .provenance
            .get(&format!("{section}.{field}"))
            .map(|p| p.layer);
        let expected = if layers.contains(&Layer::Defaults) {
            Some(Layer::Defaults)
        } else if layers.contains(&Layer::Flags) {
            Some(Layer::Flags)
        } else {
            None
        };
        assert_eq!(won, expected, "{section}.{field}");
    }
    // The environment admits nothing and is no parameter: no row names it.
    assert!(Layer::ALL.iter().all(|l| l.as_str() != "environment"));
}

#[test]
fn ci_never_consumes_the_local_carrier() {
    let reference = resolve_ok(&base());
    let oversized = vec![b' '; 5 * 1024 * 1024];
    for hostile in [
        b"invalid".to_vec(),
        oversized,
        b"{\"schemaVersion\":2,\"shell\":\"rm -rf /\"}".to_vec(),
        b"{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[\"elsewhere\"]}}".to_vec(),
    ] {
        let mut input = base();
        input.local = Some(carrier("local", &hostile));
        input.mode.interactive = false;
        assert_eq!(resolve_ok(&input), reference);
        input.mode.interactive = true;
        let interactive = resolve(&input);
        assert_ne!(interactive.as_ref().ok(), Some(&reference));
    }
    // An interactive run consumes a valid local file with layer-4 provenance.
    let mut input = base();
    input.local = Some(carrier(
        "local",
        b"{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[\"lib\"]}}",
    ));
    input.mode.interactive = true;
    let resolved = resolve_ok(&input);
    let won = &resolved.provenance["discovery.workspaceRoots"];
    assert_eq!(won.layer, Layer::Local);
    assert_eq!(
        won.source,
        ProvenanceSourceV1::Carrier {
            path: "local.json".into(),
            sha256: digest_hex(&raw_sha256(&input.local.as_ref().unwrap().bytes)),
            source_schema_version: 2,
        }
    );
}

#[test]
fn the_digest_is_invariant_and_sensitive_as_item_6_requires() {
    let reference = resolve_ok(&base()).resolved_config_digest;
    // Provenance-only moves: the same winning value from another layer.
    for (layer, document) in [
        (
            Layer::Global,
            "{\"schemaVersion\":2,\"analysis\":{\"budget\":{\"unit\":\"work-units\",\"limit\":1000}}}",
        ),
        (
            Layer::Local,
            "{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[\"src\"]}}",
        ),
        (
            Layer::Local,
            "{\"schemaVersion\":2,\"analysis\":{\"profileId\":\"default\"}}",
        ),
    ] {
        let resolved = resolve_ok(&with_layer(layer, document));
        assert_eq!(resolved.resolved_config_digest, reference, "{document}");
    }
    // --workspace-root naming the roots the project names: same digest.
    let mut input = base();
    input.flags.workspace_roots = Some(vec!["src".into()]);
    let same = resolve_ok(&input);
    assert_eq!(same.resolved_config_digest, reference);
    assert_eq!(
        same.provenance["discovery.workspaceRoots"].layer,
        Layer::Flags
    );
    assert_eq!(
        same.provenance["discovery.workspaceRoots"].source,
        ProvenanceSourceV1::Flags
    );
    // --workspace-root changing the winning set is semantic.
    input.flags.workspace_roots = Some(vec!["src".into(), "lib".into()]);
    assert_ne!(resolve_ok(&input).resolved_config_digest, reference);
    // Of the seven shared flags only --workspace-root is configuration: the
    // other six (and --format, which is no shared flag) never reach the
    // resolver, so they cannot reach the digest.
    assert_eq!(SharedFlag::ALL.len(), 7);
    for flag in SharedFlag::ALL {
        let leaf = configuration_leaf(flag);
        if flag == SharedFlag::WorkspaceRoot {
            assert_eq!(leaf, Some(("discovery", "workspaceRoots")));
            assert_eq!(flag.class(), tables::SharedFlagClass::Selection);
        } else {
            assert_eq!(leaf, None, "{flag:?}");
        }
    }
    assert!(SharedFlag::parse("--format").is_none());
    // Sensitivity: two different values of any semantic leaf, set by the
    // project, give different digests; the operational leaves never do.
    for (section, field, class, _) in FIELDS {
        let [a, b] = samples(section, field);
        let one = resolve(&with_project(&leaf_document(section, field, &a)));
        let two = resolve(&with_project(&leaf_document(section, field, &b)));
        let (one, two) = (one.unwrap(), two.unwrap());
        let changed = one.resolved_config_digest != two.resolved_config_digest;
        match class {
            FieldClass::HostAnalysisSemantic => assert_eq!(changed, a != b, "{section}.{field}"),
            FieldClass::HostOperabilityNonsemantic => assert!(!changed, "{section}.{field}"),
        }
    }
}

#[test]
fn canonical_sets_sort_and_allowed_scopes_keep_their_priority() {
    let permuted = with_project(
        "{\"schemaVersion\":2,\"analysis\":{\"capabilities\":[\"types\",\"calls\",\"imports\"]},\"discovery\":{\"ignorePaths\":[\"z\",\"a\"]}}",
    );
    let resolved = resolve_ok(&permuted);
    assert_eq!(
        as_serde(semantic_leaf(&resolved, "analysis", "capabilities")),
        serde_json::json!(["calls", "imports", "types"])
    );
    assert_eq!(
        as_serde(semantic_leaf(&resolved, "discovery", "ignorePaths")),
        serde_json::json!(["a", "z"])
    );
    // Provenance keeps the winning value exactly as the layer gave it.
    assert_eq!(
        as_serde(&resolved.provenance["discovery.ignorePaths"].value),
        serde_json::json!(["z", "a"])
    );
    let scopes = resolve_ok(&base());
    assert_eq!(
        as_serde(semantic_leaf(&scopes, "components", "allowedScopes")),
        serde_json::json!(["project", "global"])
    );
}

#[test]
fn host_built_layers_refuse_on_the_host_invariant_row() {
    use ConfigurationStep as S;
    let mut input = base();
    input.flags.workspace_roots = Some(vec![]);
    assert_eq!(resolve(&input), Err(invariant(S::Schema, "layer:flags:")));
    input.flags.workspace_roots = Some(vec!["ok".into(), "../escape".into()]);
    assert_eq!(
        resolve(&input),
        Err(invariant(
            S::LogicalPath,
            "layer:flags:/discovery/workspaceRoots/1"
        ))
    );
    let mut input = base();
    input.defaults.profile_id = Some("Default".into());
    assert_eq!(
        resolve(&input),
        Err(invariant(S::Schema, "layer:defaults:"))
    );
    let mut input = base();
    input.defaults.profile_id = Some("other".into());
    assert_eq!(
        resolve(&input),
        Err(invariant(S::Profile, "layer:defaults:/analysis/profileId"))
    );
    let mut input = base();
    input.defaults.capabilities = Some(vec!["imports".into(), "magic".into()]);
    assert_eq!(
        resolve(&input),
        Err(invariant(
            S::Capability,
            "layer:defaults:/analysis/capabilities/1"
        ))
    );
    let mut input = base();
    input.defaults.budget_limit = Some(0);
    assert_eq!(
        resolve(&input),
        Err(invariant(S::Schema, "layer:defaults:"))
    );
    // A host-built document with an unknown key (unrepresentable through the
    // typed layer) is the host's, at the schema step.
    let schemas = crate::embedded_schema_registry().unwrap();
    let unknown =
        parse_json(b"{\"schemaVersion\":2,\"analysis\":{\"profileId\":\"default\"},\"shell\":1}")
            .unwrap();
    assert!(matches!(
        admit_internal(&schemas, Layer::Defaults, unknown),
        Err(ConfigurationRefusal::HostInvariant {
            step: S::Schema,
            ..
        })
    ));
    // A document the schema admits but whose leaf the layer does not: the host's.
    let discovery =
        parse_json(b"{\"schemaVersion\":2,\"discovery\":{\"entryPoints\":[\"a\"]}}").unwrap();
    assert!(matches!(
        admit_internal(&schemas, Layer::Defaults, discovery),
        Err(ConfigurationRefusal::HostInvariant {
            step: S::Allowlist,
            ..
        })
    ));
}

#[test]
fn an_invalid_resolved_record_is_the_host_invariant() {
    let schemas = crate::embedded_schema_registry().unwrap();
    let resolved = resolve_ok(&base());
    assert!(semantic_shape(&schemas, &resolved.semantic).is_ok());
    let V::Object(sections) = &resolved.semantic else {
        panic!()
    };
    for missing in ["analysis", "components", "discovery", "policy", "evidence"] {
        let mut broken = sections.clone();
        broken.remove(missing);
        assert_eq!(
            semantic_shape(&schemas, &V::Object(broken)),
            Err(invariant(
                ConfigurationStep::Semantic,
                "resolved:semantic-configuration"
            )),
            "{missing}"
        );
    }
    // Un-normalized arrays are not the resolved record.
    let mut unsorted = sections.clone();
    let V::Object(analysis) = unsorted.get_mut("analysis").unwrap() else {
        panic!()
    };
    analysis.insert(
        "capabilities".into(),
        V::Array(vec![s("types"), s("calls")]),
    );
    assert!(semantic_shape(&schemas, &V::Object(unsorted)).is_err());
}

#[test]
fn schema_one_files_project_onto_version_two_without_rewriting() {
    // Each mapped field round-trips: a version-1 file and its version-2
    // projection resolve to the same semantic record and digest.
    let fields = [
        (Layer::Project, "analysis", "budget"),
        (Layer::Project, "components", "request"),
        (Layer::Project, "components", "pins"),
        (Layer::Project, "components", "holds"),
        (Layer::Project, "components", "allowedScopes"),
        (Layer::Local, "analysis", "budget"),
        (Layer::Local, "components", "pins"),
        (Layer::Global, "analysis", "budget"),
        (Layer::Global, "ui", "color"),
    ];
    for (layer, section, field) in fields {
        let value = &samples(section, field)[0];
        let one = leaf_document(section, field, value)
            .replace("\"schemaVersion\":2", "\"schemaVersion\":1");
        let two = leaf_document(section, field, value);
        // Without the base project file, so no higher file can mask the value.
        let bare = |text: &str| {
            let mut input = with_layer(layer, text);
            if layer != Layer::Project {
                input.project = None;
            }
            input
        };
        let input = bare(&one);
        let bytes = input.clone();
        let resolved_one = resolve_ok(&input);
        let resolved_two = resolve_ok(&bare(&two));
        assert_eq!(
            resolved_one.semantic, resolved_two.semantic,
            "{section}.{field}"
        );
        assert_eq!(
            resolved_one.operational, resolved_two.operational,
            "{section}.{field}"
        );
        let source = &resolved_one.provenance[&format!("{section}.{field}")].source;
        assert!(
            matches!(
                source,
                ProvenanceSourceV1::Carrier {
                    source_schema_version: 1,
                    ..
                }
            ),
            "{source:?}"
        );
        // No file is rewritten: the captured bytes are unchanged.
        assert_eq!(input, bytes);
    }
    // An unmapped version-1 field refuses: every field outside the closed
    // preview carrier, including a version-2-only section.
    for (layer, document) in [
        (
            Layer::Project,
            "{\"schemaVersion\":1,\"discovery\":{\"entryPoints\":[\"a\"]}}",
        ),
        (
            Layer::Project,
            "{\"schemaVersion\":1,\"ui\":{\"color\":\"never\"}}",
        ),
        (
            Layer::Global,
            "{\"schemaVersion\":1,\"components\":{\"pins\":[]}}",
        ),
        (
            Layer::Local,
            "{\"schemaVersion\":1,\"policy\":{\"packIds\":[]}}",
        ),
        (
            Layer::Project,
            "{\"schemaVersion\":1,\"analysis\":{\"profileId\":\"default\"}}",
        ),
    ] {
        assert_eq!(
            resolve(&with_layer(layer, document)),
            Err(invalid(
                ConfigurationStep::Schema,
                &format!("layer:{}:", layer.as_str())
            )),
            "{document}"
        );
    }
}

#[test]
fn x12_order_admits_the_resolved_pack_selection_once_after_resolution() {
    let (resolved, pack) = resolve_analysis_configuration(&base()).unwrap();
    assert_eq!(resolved.pack_ids(), ["opensip.preview.typescript.pack:1"]);
    drop(pack);
    // A refused project-layer pack ID: resolution succeeds, then X12 row 1.
    let input = with_project("{\"schemaVersion\":2,\"policy\":{\"packIds\":[\"other.pack:1\"]}}");
    assert!(resolve(&input).is_ok());
    let refusal = resolve_analysis_configuration(&input).unwrap_err();
    assert!(matches!(
        &refusal,
        AnalysisConfigurationRefusal::Policy(PolicySelectionRefusal::Pack(
            PackRefusal::NotBundled { .. }
        ))
    ));
    let t = analysis_configuration_termination(&refusal);
    assert_eq!(t, rejected(Detail::ConfigInvalid, "other.pack:1"));
    // No pack selected at all is X12 row 1's count.
    let input = with_project("{\"schemaVersion\":2,\"policy\":{\"packIds\":[]}}");
    assert_eq!(
        resolve_analysis_configuration(&input).unwrap_err(),
        AnalysisConfigurationRefusal::Policy(PolicySelectionRefusal::Count(0))
    );
    // A configuration refusal never reaches admission.
    let input = with_project(
        "{\"schemaVersion\":2,\"policy\":{\"waiverIds\":[\"w\"],\"packIds\":[\"other.pack:1\"]}}",
    );
    assert!(matches!(
        resolve_analysis_configuration(&input).unwrap_err(),
        AnalysisConfigurationRefusal::Configuration(_)
    ));
    // In the source, resolution precedes admission with nothing between.
    let source = production_source();
    let body = &source[source
        .find("pub(crate) fn resolve_analysis_configuration")
        .unwrap()..];
    let body = &body[..body.find("\n}\n").unwrap()];
    let resolve_at = body.find("resolve(input)").unwrap();
    let admit_at = body.find("admit_policy_selection(&selection)").unwrap();
    assert!(resolve_at < admit_at);
    assert_eq!(body.matches("admit_policy_selection(").count(), 1);
}

#[test]
fn configuration_rows_carry_the_s9_remedy_and_the_published_routes() {
    assert_eq!(REMEDY_CONFIG_INVALID.len(), 706);
    assert!(REMEDY_CONFIG_INVALID.is_ascii());
    assert_eq!(
        digest_hex(&raw_sha256(REMEDY_CONFIG_INVALID.as_bytes())),
        S9_SHA256
    );
    // The profile names AQ:334 uses are reference refusal names, not generated
    // codes: both are CONFIG.INVALID with their subjects.
    for name in ["CONFIG.PROFILE_MISSING", "CONFIG.PROFILE_UNREGISTERED"] {
        assert!(name.parse::<Detail>().is_err(), "{name}");
    }
    let rows = [
        (
            invalid(ConfigurationStep::Profile, "profile:missing"),
            false,
        ),
        (invalid(ConfigurationStep::Profile, "profile:other"), false),
        (
            invalid(
                ConfigurationStep::LogicalPath,
                "layer:project:/discovery/entryPoints/0",
            ),
            false,
        ),
        (
            invariant(
                ConfigurationStep::DefaultsComplete,
                "layer:defaults:/analysis/budget",
            ),
            true,
        ),
        (invariant(ConfigurationStep::Schema, "layer:flags:"), true),
    ];
    for (refusal, host_fault) in rows {
        let t = configuration_termination(&refusal);
        let (value, _) = envelope(&t);
        let subject = match &refusal {
            ConfigurationRefusal::Invalid { subject, .. }
            | ConfigurationRefusal::HostInvariant { subject, .. } => subject.clone(),
        };
        let (detail, remedy) = if host_fault {
            (
                Detail::HostInvariantViolated,
                crate::doctor_ingress::REMEDY_INVARIANT,
            )
        } else {
            (Detail::ConfigInvalid, REMEDY_CONFIG_INVALID)
        };
        assert_eq!(
            value["termination"]["domainDetail"],
            serde_json::json!({"code": detail.to_string(), "remedy": remedy, "subject": subject}),
            "{refusal:?}"
        );
        assert_eq!(value["exitCode"], if host_fault { 4 } else { 2 });
        assert_eq!(value["termination"].get("faultCause").is_some(), host_fault);
        if !host_fault {
            assert_eq!(t, rejected(Detail::ConfigInvalid, &subject));
        }
    }
}

/// The O-4 invariance-control template (item 7): an operational field is
/// nonsemantic only if every admitted value leaves the semantic record and the
/// digest unchanged. S-OP-5's unit instantiates it per field it admits.
fn assert_operational_invariance(section: &str, field: &str, values: &[&str]) {
    assert!(
        FIELDS.iter().any(|r| r.0 == section
            && r.1 == field
            && r.2 == FieldClass::HostOperabilityNonsemantic),
        "{section}.{field} is not classified host.operability.nonsemantic"
    );
    let reference = resolve_ok(&base());
    let mut operational = Vec::new();
    for value in values {
        // The highest external layer, so no lower file can mask the value.
        let resolved = resolve_ok(&with_layer(
            Layer::Local,
            &leaf_document(section, field, value),
        ));
        assert_eq!(
            resolved.semantic, reference.semantic,
            "{section}.{field}={value}"
        );
        assert_eq!(
            resolved.resolved_config_digest,
            reference.resolved_config_digest
        );
        operational.push(resolved.operational);
    }
    operational.dedup();
    assert_eq!(
        operational.len(),
        values.len(),
        "{section}.{field} values must differ"
    );
}

#[test]
fn the_operational_fields_pass_the_o4_invariance_template() {
    assert_operational_invariance("ui", "color", &["\"auto\"", "\"always\"", "\"never\""]);
    for field in ["maxBytes", "maxRuns", "maxAgeSeconds"] {
        assert_operational_invariance("retention", field, &["null", "1", "18446744073709551615"]);
    }
}

/// The PCS leaves (section.field) of a closed schema value, in order.
fn schema_leaves(schema: &Value) -> Result<Vec<String>, String> {
    let mut out = Vec::new();
    for (section, record) in schema["properties"].as_object().ok_or("no properties")? {
        if section == "schemaVersion" {
            continue;
        }
        let fields = record["properties"]
            .as_object()
            .ok_or(format!("section {section} has no properties"))?;
        out.extend(fields.keys().map(|f| format!("{section}.{f}")));
    }
    Ok(out)
}
/// Every PCS leaf has exactly one row, and no row names a non-leaf.
fn classification_covers(pcs: &Value) -> Result<(), String> {
    let mut leaves = schema_leaves(pcs)?;
    leaves.sort();
    let mut rows: Vec<String> = FIELDS.iter().map(|r| format!("{}.{}", r.0, r.1)).collect();
    rows.sort();
    rows.dedup();
    if rows.len() == FIELDS.len() && leaves == rows {
        Ok(())
    } else {
        Err(format!("{leaves:?} != {rows:?}"))
    }
}

#[test]
fn the_classification_table_is_the_reviewed_mapping_over_every_pcs_leaf() {
    let pcs: Value = serde_json::from_slice(PCS_SOURCE).unwrap();
    assert_eq!(
        digest_hex(&raw_sha256(PCS_SOURCE)),
        "591a66e5dc35c4be516eaf68bacc62f9a82260b0c1698665dd85f7613b78e14d"
    );
    let leaves = schema_leaves(&pcs).unwrap();
    let rows: Vec<String> = FIELDS.iter().map(|r| format!("{}.{}", r.0, r.1)).collect();
    let mut sorted_leaves = leaves.clone();
    sorted_leaves.sort();
    let mut sorted_rows = rows.clone();
    sorted_rows.sort();
    assert_eq!(sorted_leaves, sorted_rows);
    assert_eq!(classification_covers(&pcs), Ok(()));
    // Mutation: a PCS leaf with no class fails the coverage check.
    let mut grown = pcs.clone();
    grown["properties"]["ui"]["properties"]["theme"] = serde_json::json!({"type": "string"});
    assert!(classification_covers(&grown).is_err());
    let mut shrunk = pcs.clone();
    shrunk["properties"]["ui"]["properties"]
        .as_object_mut()
        .unwrap()
        .remove("color");
    assert!(classification_covers(&shrunk).is_err());
    // The semantic rows are exactly identity-v3 semantic-configuration's leaves.
    let identity: Value = serde_json::from_slice(IDENTITY_SOURCE).unwrap();
    let mut semantic = schema_leaves(&identity["$defs"]["semantic-configuration"]).unwrap();
    semantic.sort();
    let mut semantic_rows: Vec<String> = FIELDS
        .iter()
        .filter(|r| r.2 == FieldClass::HostAnalysisSemantic)
        .map(|r| format!("{}.{}", r.0, r.1))
        .collect();
    semantic_rows.sort();
    assert_eq!(semantic, semantic_rows);
    // The generated table is the reviewed mapping file, row for row.
    let mapping: Value = serde_json::from_str(CLASSES).unwrap();
    let mapped: Vec<(String, String, Vec<String>)> = mapping["rows"]
        .as_array()
        .unwrap()
        .iter()
        .map(|r| {
            (
                r["leaf"].as_str().unwrap().to_owned(),
                r["class"].as_str().unwrap().to_owned(),
                strs(&r["layers"]),
            )
        })
        .collect();
    let generated: Vec<(String, String, Vec<String>)> = FIELDS
        .iter()
        .map(|r| {
            (
                format!("{}.{}", r.0, r.1),
                r.2.as_str().to_owned(),
                r.3.iter().map(|l| l.as_str().to_owned()).collect(),
            )
        })
        .collect();
    assert_eq!(mapped, generated);
    assert_eq!(
        mapping["source"]["sha256"],
        digest_hex(&raw_sha256(PCS_SOURCE))
    );
}

#[test]
fn the_registries_refuse_unknown_values_typed() {
    // Profiles: the closed one-member registry (AQ:56).
    assert_eq!(PROFILE_IDS, ["default"]);
    // Capabilities: the matrix vocabulary; every member has a selectable mode,
    // and the NOT-SELECTED cells are kept for the analysis spec.
    assert_eq!(CapabilityId::ALL.len(), 11);
    assert!(CapabilityId::ALL.into_iter().all(selectable));
    assert!(CapabilityId::parse("rust.imports").is_none());
    assert!(CapabilityId::parse("imports@resolved").is_none());
    assert_eq!(NOT_SELECTED_CELLS.len(), 3);
    assert!(
        NOT_SELECTED_CELLS
            .iter()
            .all(|(c, _)| *c == CapabilityId::ClonesCrossTsjs)
    );
    resolve_ok(&with_project(
        "{\"schemaVersion\":2,\"analysis\":{\"capabilities\":[\"clones-cross-tsjs\"]}}",
    ));
    for capability in CapabilityId::ALL {
        assert_eq!(CapabilityId::parse(capability.as_str()), Some(capability));
    }
    for mode in LanguageMode::ALL {
        assert_eq!(LanguageMode::parse(mode.as_str()), Some(mode));
    }
    // Waivers: empty at M3. Recognizers: the existing generated enum, no copy.
    assert_eq!(
        resolve(&with_project(
            "{\"schemaVersion\":2,\"policy\":{\"waiverIds\":[\"opensip.waiver:1\"]}}"
        ))
        .unwrap_err()
        .step(),
        ConfigurationStep::Waiver
    );
    // Shared flags: the seven CINV flags with their classes.
    let classes: Vec<(&str, &str)> = SharedFlag::ALL
        .iter()
        .map(|f| (f.as_str(), f.class().as_str()))
        .collect();
    assert_eq!(
        classes,
        [
            ("--allow-backup-custody", "authorization"),
            ("--project", "selection"),
            ("--trust-group", "authorization"),
            ("--trust-project-owner", "authorization"),
            ("--ephemeral", "selection"),
            ("--yes-policy", "authorization"),
            ("--workspace-root", "selection"),
        ]
    );
}

#[test]
fn source_pin_resolution_is_pure_and_reaches_only_its_registries() {
    let source = production_source();
    // The one std import is the ordered map; no I/O, environment, process,
    // threads, time, synchronization or globals.
    let code = |text: &'static str| -> Vec<&'static str> {
        text.lines()
            .filter(|l| !l.trim_start().starts_with("//"))
            .collect()
    };
    let lines = code(source);
    let std_uses: Vec<&str> = lines
        .iter()
        .copied()
        .filter(|l| l.contains("std::"))
        .collect();
    assert_eq!(std_uses, ["use std::collections::BTreeMap;"]);
    for forbidden in [
        "static mut",
        " static ",
        "env!",
        "env::",
        "include_bytes!",
        "include_str!",
        "thread",
        "Instant",
        "SystemTime",
        "unsafe",
    ] {
        let hits: Vec<&&str> = lines.iter().filter(|l| l.contains(forbidden)).collect();
        assert!(hits.is_empty(), "{forbidden}: {hits:?}");
    }
    // The generated tables are constants and functions only.
    let tables = code(include_str!("configuration_tables.rs"));
    for forbidden in [
        "std::",
        "static mut",
        " static ",
        "unsafe",
        "crate::",
        "env::",
        "env!",
    ] {
        let hits: Vec<&&str> = tables.iter().filter(|l| l.contains(forbidden)).collect();
        assert!(hits.is_empty(), "{forbidden}: {hits:?}");
    }
}

/// The hostile-environment control's resolver child (M3-B r5 item 9; unit
/// B1-b, LD-B1B-4 and LD-B1B-5). Ignored: run only by the parent below. It
/// resolves every PCM vector and prints each outcome in full: the canonical
/// semantic and operational records, the digest, and every provenance entry
/// with its layer, winning value and source.
#[test]
#[ignore = "child of the hostile-environment control"]
fn b1b_environment_child_resolve() {
    let text = |value: &V| String::from_utf8(canonical_bytes(value).unwrap()).unwrap();
    for case in vector_cases() {
        let id = case["id"].as_str().unwrap().to_owned();
        match resolve_analysis_configuration(&input_from(&case)) {
            Ok((resolved, _)) => {
                let provenance: Vec<String> = resolved
                    .provenance
                    .iter()
                    .map(|(leaf, won)| {
                        format!(
                            "{leaf}={}|{}|{:?}",
                            won.layer.as_str(),
                            text(&won.value),
                            won.source
                        )
                    })
                    .collect();
                println!(
                    "B1B-ENV:{id}:{}:{}:{}:{}",
                    resolved.resolved_config_digest,
                    text(&resolved.semantic),
                    text(&resolved.operational),
                    provenance.join(";")
                );
            }
            Err(refusal) => println!("B1B-ENV:{id}:refused:{refusal:?}"),
        }
    }
}

#[test]
fn resolution_is_identical_under_a_hostile_environment() {
    // A cleared environment (only TMPDIR kept), then hostile values.
    let run = |hostile: bool| -> Vec<String> {
        let mut command = std::process::Command::new(std::env::current_exe().unwrap());
        command
            .args([
                "--ignored",
                "--exact",
                "configuration::tests::b1b_environment_child_resolve",
                "--nocapture",
                "--test-threads=1",
            ])
            .env_clear()
            .env("TMPDIR", std::env::temp_dir());
        if hostile {
            command
                .env("HOME", "/nonexistent/opensip-hostile-home")
                .env("PATH", "/nonexistent/opensip-hostile-bin")
                .env("CI", "1")
                .env("TERM", "dumb")
                .env("NO_COLOR", "1")
                .env("XDG_CONFIG_HOME", "/nonexistent/opensip-hostile-xdg")
                .env("XDG_DATA_HOME", "/nonexistent/opensip-hostile-xdg-data")
                .env("XDG_CACHE_HOME", "/nonexistent/opensip-hostile-xdg-cache");
        }
        let output = command.output().unwrap();
        assert!(
            output.status.success(),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
        String::from_utf8(output.stdout)
            .unwrap()
            .lines()
            .filter_map(|line| line.find("B1B-ENV:").map(|at| line[at..].to_owned()))
            .collect()
    };
    let clean = run(false);
    assert_eq!(clean.len(), vector_cases().len());
    assert_eq!(clean, run(true));
}

#[test]
fn a_refused_project_pack_stops_before_the_registry_composed_across_crates() {
    // Codex B1B-R2-RF-02 (MB item 10's control): security's analysis first
    // phase on a writer's gate, this crate's resolver and X12 pack admission
    // over the captured bytes, and item 5 only on admission (through
    // security's test-only scenario seam; no production facade).
    use std::os::unix::fs::PermissionsExt;
    let home = opensip_security::scenario::ScenarioHome::create(&std::env::temp_dir());
    let project = home.project("b1b-pack");
    let write = |bytes: &[u8]| {
        let path = project.join("opensip.json");
        std::fs::write(&path, bytes).unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o644)).unwrap();
    };
    let decide = |project_bytes: Option<&[u8]>, local_bytes: Option<&[u8]>| {
        let mut input = base();
        input.project = project_bytes.map(|bytes| carrier("project", bytes));
        input.local = local_bytes.map(|bytes| carrier("local", bytes));
        resolve_analysis_configuration(&input).is_ok()
    };
    write(b"{\"schemaVersion\":2,\"policy\":{\"packIds\":[\"other.pack:1\"]}}");
    let refused = home
        .compose_analysis_carriers(&project, false, decide)
        .unwrap();
    assert!(
        !refused.admitted && !refused.registry_captured,
        "{refused:?}"
    );
    assert!(
        refused.registry_unchanged && refused.members_unchanged && refused.writer_released,
        "{refused:?}"
    );
    // The same project selecting the bundled pack: item 5 runs, and still
    // nothing is registered or written.
    write(b"{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[\"src\"]}}");
    let admitted = home
        .compose_analysis_carriers(&project, false, decide)
        .unwrap();
    assert!(
        admitted.admitted && admitted.registry_captured,
        "{admitted:?}"
    );
    assert!(
        admitted.registry_unchanged && admitted.members_unchanged && admitted.writer_released,
        "{admitted:?}"
    );
}
