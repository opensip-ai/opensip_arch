// Unit B2-c1's controls (B2-c plan r2 section 2.1): every recorded call of the
// bound B2-c0 reference (contract successor 166) is replayed through the host
// instrument and compared byte for byte in canonical JSON; a refusal by its
// internal key. The alias map is the registry's rows, and the embedded
// capability matrix the architecture's bytes. Pure: no filesystem tree.
use super::discovery::{
    INTERNAL_DETAIL_ALIASES, MarkerFact, ReleaseDeclaration, ScopeFault, SelectionFault,
    WorkspaceUnit, assign_membership, default_capability_selection, discover_units, public_detail,
    require_admitted_boundaries, standalone, unit_scope_descriptor,
};
use opensip_identity::{JsonValue as V, canonical_bytes, digest_hex, parse_json, raw_sha256};
use opensip_security::discovery_export::{
    AdmittedBoundaries, InventoryRecordRefusal, MarkerCountBasis, PruneReason, PrunedAnchor,
    PrunedTreeRow,
};
use std::collections::BTreeMap;

const VECTORS: &[u8] = include_bytes!("discovery_vectors.json");
const MATRIX: &[u8] = include_bytes!("native_capability_matrix.v2.json");

fn field<'v>(v: &'v V, key: &str) -> &'v V {
    let V::Object(m) = v else {
        panic!("not an object: {v:?}")
    };
    m.get(key).unwrap_or(&V::Null)
}
fn text(v: &V) -> String {
    match v {
        V::String(s) => s.clone(),
        other => panic!("not a string: {other:?}"),
    }
}
fn items(v: &V) -> &[V] {
    match v {
        V::Array(a) => a,
        other => panic!("not an array: {other:?}"),
    }
}
fn texts(v: &V) -> Vec<String> {
    items(v).iter().map(text).collect()
}
fn opt_texts(v: &V) -> Option<Vec<String>> {
    match v {
        V::Null => None,
        other => Some(texts(other)),
    }
}
fn flag(v: &V) -> Option<bool> {
    match v {
        V::Bool(b) => Some(*b),
        V::Null => None,
        other => panic!("not a bool: {other:?}"),
    }
}
fn number(v: &V) -> usize {
    match v {
        V::Integer(n) => usize::try_from(n.get()).expect("count"),
        other => panic!("not an integer: {other:?}"),
    }
}

/// The reference's `synthetic_marker_set`, for the generator form.
fn synthetic(spec: &V) -> BTreeMap<String, MarkerFact> {
    let fact = |c: char| MarkerFact {
        sha256: c.to_string().repeat(64),
        is_cargo_workspace: None,
        allow_js: None,
    };
    let mut out = BTreeMap::new();
    if flag(field(spec, "rootMarker")) == Some(true) {
        out.insert("package.json".to_owned(), fact('b'));
    }
    for i in 0..number(field(spec, "firstParty")) {
        out.insert(format!("pkg{i:04}/package.json"), fact('1'));
    }
    for i in 0..number(field(spec, "installed")) {
        out.insert(format!("node_modules/dep{i:04}/package.json"), fact('1'));
    }
    out
}

fn markers(v: &V) -> BTreeMap<String, MarkerFact> {
    let V::Object(m) = v else { panic!("markers") };
    if let Some(spec) = m.get("$synthetic") {
        return synthetic(spec);
    }
    m.iter()
        .map(|(path, info)| {
            (
                path.clone(),
                MarkerFact {
                    sha256: text(field(info, "sha256")),
                    is_cargo_workspace: flag(field(info, "isCargoWorkspace")),
                    allow_js: flag(field(info, "allowJs")),
                },
            )
        })
        .collect()
}

fn unit(v: &V) -> WorkspaceUnit {
    let family = match text(field(v, "languageFamily")).as_str() {
        "rust" => super::discovery::Family::Rust,
        "tsjs" => super::discovery::Family::Tsjs,
        _ => super::discovery::Family::None,
    };
    WorkspaceUnit {
        unit_ordinal: number(field(v, "unitOrdinal")),
        root_path: text(field(v, "rootPath")),
        language_family: family,
        language_mode: text(field(v, "languageMode")),
        unit_kind: text(field(v, "unitKind")),
        marker_path: text(field(v, "markerPath")),
        marker_sha256: match field(v, "markerSha256") {
            V::Null => None,
            other => Some(text(other)),
        },
        recognizer_id: text(field(v, "recognizerId")),
        recognizer_version: u32::try_from(number(field(v, "recognizerVersion"))).expect("version"),
        provenance: text(field(v, "provenance")),
        member_package_roots: texts(field(v, "memberPackageRoots")),
    }
}

fn pruned(v: &V) -> PrunedTreeRow {
    let reason = match text(field(v, "reason")).as_str() {
        "dependency-tree" => PruneReason::DependencyTree,
        "vcs-tree" => PruneReason::VcsTree,
        "cargo-build-output" => PruneReason::CargoBuildOutput,
        "opensip-custody-state" => PruneReason::OpensipCustodyState,
        other => panic!("reason {other}"),
    };
    let basis = match text(field(v, "markerCountBasis")).as_str() {
        "observed-inventory" => MarkerCountBasis::ObservedInventory,
        _ => MarkerCountBasis::NotEnumerated,
    };
    let marker_count = match field(v, "markerCount") {
        V::Null => None,
        n => Some(u64::try_from(number(n)).expect("count")),
    };
    PrunedTreeRow {
        anchor: PrunedAnchor {
            path: text(field(v, "path")),
            reason,
        },
        marker_count,
        basis,
    }
}

/// The inventory argument: `Ok(None)` for the standalone lane, or the
/// recorded refusal key when the record is not an admitted V3 inventory.
fn boundaries(v: &V) -> Result<Option<AdmittedBoundaries>, String> {
    match v {
        V::Null => Ok(None),
        record => opensip_security::scenario::admitted_boundaries(record)
            .map(Some)
            .map_err(|e| match e {
                InventoryRecordRefusal::VersionUnsupported(n) => {
                    format!("native.boundary-inventory-version-unsupported:{n}")
                }
                InventoryRecordRefusal::SchemaInvalid => "schema-invalid".to_owned(),
            }),
    }
}

fn canonical(v: &V) -> Vec<u8> {
    canonical_bytes(v).expect("canonical")
}

/// One recorded step: the host's result or refusal key.
fn replay(step: &V) -> Result<V, String> {
    let args = field(step, "args");
    let b = boundaries(field(args, "boundaries"))?;
    match text(field(step, "fn")).as_str() {
        "discover_units" => {
            let roots = opt_texts(field(args, "explicit_workspace_roots"));
            let m = markers(field(args, "markers"));
            Ok(match &b {
                Some(b) => discover_units(&m, roots.as_deref(), b),
                None => standalone::discover_units(&m, roots.as_deref()),
            }
            .to_json())
        }
        "assign_membership" => {
            let units: Vec<WorkspaceUnit> = items(field(args, "units")).iter().map(unit).collect();
            let files = texts(field(args, "files"));
            match &b {
                Some(b) => assign_membership(&units, &files, b),
                None => standalone::assign_membership(&units, &files),
            }
            .map_err(|f| f.0)
        }
        "unit_scope_descriptor" => {
            let units: Vec<WorkspaceUnit> = items(field(args, "units")).iter().map(unit).collect();
            let prefixes = opt_texts(field(args, "explicit_path_prefixes"));
            let trees: Option<Vec<PrunedTreeRow>> = match field(args, "pruned_trees") {
                V::Null => None,
                rows => Some(items(rows).iter().map(pruned).collect()),
            };
            let ignore = texts(field(args, "ignore_paths"));
            match &b {
                Some(b) => {
                    unit_scope_descriptor(&units, &ignore, prefixes.as_deref(), trees.as_deref(), b)
                }
                None => standalone::unit_scope_descriptor(
                    &units,
                    &ignore,
                    prefixes.as_deref(),
                    trees.as_deref(),
                ),
            }
            .map_err(|f| match f {
                ScopeFault::Limit(r) => r.key(),
                ScopeFault::Internal(i) => i.0,
            })
        }
        "default_capability_selection" => {
            let units: Vec<WorkspaceUnit> = items(field(args, "units")).iter().map(unit).collect();
            let registry: Vec<ReleaseDeclaration> = items(field(args, "registry"))
                .iter()
                .map(|r| ReleaseDeclaration {
                    capability_id: text(field(r, "capabilityId")),
                    language_modes: texts(field(r, "languageModes")),
                })
                .collect();
            default_capability_selection(&units, &registry).map_err(|f| match f {
                SelectionFault::Key(k) => k,
                SelectionFault::Limit(r) => r.key(),
                SelectionFault::SchemaInvalid => "schema-invalid".to_owned(),
            })
        }
        other => panic!("unexpected function {other}"),
    }
}

#[test]
fn every_recorded_reference_call_replays_byte_for_byte() {
    let body = parse_json(VECTORS).expect("vectors");
    let steps = items(field(&body, "steps"));
    assert!(steps.len() >= 100, "{}", steps.len());
    let mut failures = Vec::new();
    for (i, step) in steps.iter().enumerate() {
        let label = format!(
            "{i} {} {}",
            text(field(step, "case")),
            text(field(step, "fn"))
        );
        let got = replay(step);
        match (text(field(step, "outcome")).as_str(), got) {
            ("result", Ok(v)) if canonical(&v) == canonical(field(step, "result")) => {}
            ("refused", Err(key)) if key == text(field(step, "key")) => {}
            (outcome, got) => failures.push(format!(
                "{label}: recorded {outcome}, got {}",
                match got {
                    Ok(v) => String::from_utf8_lossy(&canonical(&v))
                        .chars()
                        .take(600)
                        .collect::<String>(),
                    Err(k) => k,
                }
            )),
        }
    }
    assert!(
        failures.is_empty(),
        "{} of {} steps differ:\n{}",
        failures.len(),
        steps.len(),
        failures.join("\n")
    );
}

#[test]
fn the_alias_map_is_the_registry_rows_and_unknown_keys_refuse() {
    let body = parse_json(VECTORS).expect("vectors");
    let recorded: Vec<(String, String)> = items(field(&body, "aliases"))
        .iter()
        .map(|row| (text(&items(row)[0]), text(&items(row)[1])))
        .collect();
    let ours: Vec<(String, String)> = INTERNAL_DETAIL_ALIASES
        .iter()
        .map(|(a, b)| ((*a).to_owned(), (*b).to_owned()))
        .collect();
    assert_eq!(ours, recorded);
    for (internal, public) in INTERNAL_DETAIL_ALIASES {
        assert_eq!(public_detail(internal), Ok(public));
    }
    assert_eq!(
        public_detail("native.explicit-root-without-marker"),
        Ok("native.explicit-root-without-marker")
    );
    assert_eq!(
        public_detail("PROJECT.SCOPE_LIMIT"),
        Ok("PROJECT.SCOPE_LIMIT")
    );
    assert!(public_detail("native.admitted-boundaries-required").is_err());
    assert!(public_detail("native.unknown").is_err());
}

#[test]
fn the_embedded_capability_matrix_is_the_architecture_bytes() {
    let body = parse_json(VECTORS).expect("vectors");
    let pin = items(field(&body, "reference"))
        .iter()
        .find(|row| text(field(row, "path")).ends_with("native-capability-matrix.v2.json"))
        .expect("matrix pin");
    assert_eq!(number(field(pin, "bytes")), MATRIX.len());
    assert_eq!(text(field(pin, "sha256")), digest_hex(&raw_sha256(MATRIX)));
}

#[test]
fn only_a_closed_v3_record_is_an_admitted_inventory() {
    let good = r#"{"schemaVersion":3,"source":"security.discovery","selectedRoot":"/h/w","nestedRepositories":["vendor/lib"],"nestedProjects":[],"custodyExcludedUnits":[{"path":"blocked","reason":"DIRECTORY_CUSTODY:ACL_UNREADABLE"}],"prunedTrees":[{"path":".git","reason":"vcs-tree","markerCount":null,"markerCountBasis":"not-enumerated"}],"memberRepositories":["a","b"]}"#;
    let parse = |raw: &str| {
        opensip_security::scenario::admitted_boundaries(&parse_json(raw.as_bytes()).expect("json"))
    };
    let b = parse(good).expect("admitted");
    assert!(b.is_boundary("vendor/lib/x") && b.is_boundary("blocked") && !b.is_boundary("src"));
    assert_eq!(b.excluded_prefixes(), ["blocked", "vendor/lib"]);
    for (from, to) in [
        (r#""schemaVersion":3"#, r#""schemaVersion":2"#),
        (r#""security.discovery""#, r#""caller-ignores""#),
        (
            r#""memberRepositories":["a","b"]"#,
            r#""memberRepositories":["b","a"]"#,
        ),
        (
            r#""memberRepositories":["a","b"]"#,
            r#""memberRepositories":["a","a"]"#,
        ),
        (r#"["vendor/lib"]"#, r#"["/vendor/lib"]"#),
        (r#"["vendor/lib"]"#, r#"["vendor/../lib"]"#),
        ("DIRECTORY_CUSTODY:ACL_UNREADABLE", "IGNORED"),
        (r#""markerCount":null"#, r#""markerCount":1"#),
        (r#""reason":"vcs-tree""#, r#""reason":"ignored""#),
        (
            r#""memberRepositories":["a","b"]}"#,
            r#""memberRepositories":["a","b"],"extra":1}"#,
        ),
    ] {
        assert!(good.contains(from), "{from}");
        let raw = good.replace(from, to);
        let expected = if to == r#""schemaVersion":2"# {
            InventoryRecordRefusal::VersionUnsupported(2)
        } else {
            InventoryRecordRefusal::SchemaInvalid
        };
        assert_eq!(parse(&raw), Err(expected), "{to}");
    }
}

/// r2 (Codex B2C1-R1-RF-1): the production entries take the admitted
/// inventory, a missing one refuses with the internal key, and the
/// standalone lane is compiled only under `cfg(test)`.
#[test]
fn production_composition_cannot_take_the_standalone_lane() {
    assert_eq!(
        require_admitted_boundaries(None).map(|_| ()),
        Err(super::discovery::InternalFault(
            "native.admitted-boundaries-required".to_owned()
        ))
    );
    let source = include_str!("discovery.rs");
    let at = source
        .find("pub(crate) mod standalone")
        .expect("standalone module");
    assert!(
        source[..at].trim_end().ends_with("#[cfg(test)]"),
        "the standalone lane is test-only"
    );
    // Outside that module, no crate-visible function takes an optional inventory.
    let (before, after) = source.split_at(at);
    let tail = &after[after.find("\n}\n").expect("module end")..];
    for chunk in [before, tail] {
        for (i, _) in chunk.match_indices("pub(crate) fn ") {
            let signature = &chunk[i..i + chunk[i..].find('{').expect("body")];
            // The gate itself takes the optional inventory and refuses its absence.
            if signature.starts_with("pub(crate) fn require_admitted_boundaries(") {
                continue;
            }
            assert!(
                !signature.contains("Option<&AdmittedBoundaries>"),
                "{signature}"
            );
        }
    }
}
