// M3-B r9 item 16 (unit B2-d2): host-side framework recognition against its
// cross-implementation vectors (tools/host/framework_recognition_vectors.py,
// from the bound B2-d0 reference), and FR-4's bounds exercised directly.
use super::framework_recognition::{
    ENTRY_POINTS_OVER_BOUND, EVIDENCE_FILES, MAX_ENTRY_POINTS, MAX_EVIDENCE, MAX_RECOGNIZERS,
    RecognitionError, RecognitionInputs, Recognized, cargo_workspace_fact, discovered_provenance,
    entry_bound, recognize, structural_bounds, unit_recognition,
};
use opensip_identity::{
    JsonInteger, JsonValue as V, RegisteredSchemas, canonical_bytes, parse_json,
};
use std::collections::{BTreeMap, BTreeSet};

const VECTORS: &[u8] = include_bytes!("framework_recognition_vectors.json");

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    fields.get(key).unwrap_or(&V::Null)
}
fn text(value: &V) -> &str {
    let V::String(s) = value else {
        panic!("{value:?}")
    };
    s
}
fn items(value: &V) -> &[V] {
    let V::Array(items) = value else {
        panic!("{value:?}")
    };
    items
}
fn number(value: &V) -> usize {
    let V::Integer(n) = value else {
        panic!("{value:?}")
    };
    usize::try_from(n.get()).unwrap()
}
fn bytes(hex: &str) -> Vec<u8> {
    (0..hex.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
        .collect()
}
/// `"absent"`, or the explicit list.
fn explicit(value: &V) -> Option<Vec<String>> {
    match value {
        V::String(s) if s == "absent" => None,
        list => Some(items(list).iter().map(|v| text(v).to_owned()).collect()),
    }
}
fn route_tree(routes: usize, vite: bool) -> BTreeMap<String, Vec<u8>> {
    let mut files = BTreeMap::new();
    files.insert("next.config.js".to_owned(), b"x".to_vec());
    for i in 0..routes {
        files.insert(format!("pages/r{i:05}.tsx"), Vec::new());
    }
    if vite {
        files.insert("vite.config.ts".to_owned(), b"x".to_vec());
        files.insert("index.html".to_owned(), Vec::new());
    }
    files
}
fn schemas() -> RegisteredSchemas {
    crate::embedded_schema_registry().unwrap()
}
fn run(files: &BTreeMap<String, Vec<u8>>, explicit: Option<&[String]>) -> V {
    let paths: BTreeSet<String> = files.keys().cloned().collect();
    recognize(&RecognitionInputs {
        paths: &paths,
        bytes: files,
        explicit_entry_points: explicit,
    })
    .unwrap()
}

#[test]
fn every_unit_vector_matches_the_reference() {
    let body = parse_json(VECTORS).unwrap();
    let registry = schemas();
    let units = items(field(&body, "units"));
    assert!(units.len() >= 40, "{}", units.len());
    for unit in units {
        let name = text(field(unit, "name"));
        let V::Object(hexes) = field(unit, "files") else {
            panic!("{name}")
        };
        let files: BTreeMap<String, Vec<u8>> = hexes
            .iter()
            .map(|(p, h)| (p.clone(), bytes(text(h))))
            .collect();
        let explicit = explicit(field(unit, "explicit"));
        let got = run(&files, explicit.as_deref());
        assert_eq!(&got, field(unit, "recognition"), "{name}");
        let shape = field(unit, "unit");
        let row = unit_recognition(
            &registry,
            number(field(shape, "unitOrdinal")) as u64,
            text(field(shape, "rootPath")),
            text(field(shape, "markerPath")),
            got.clone(),
        )
        .unwrap();
        assert_eq!(
            row.recognition_id,
            text(field(unit, "recognitionId")),
            "{name}"
        );
        // FW-01: a configuration naming a path is hashed, never read for it.
        let rendered = String::from_utf8_lossy(&canonical_bytes(&got).unwrap()).into_owned();
        assert!(!rendered.contains("opensip-canary"), "{name}");
    }
}

#[test]
fn every_bound_vector_matches_the_reference() {
    let body = parse_json(VECTORS).unwrap();
    let registry = schemas();
    let bounds = items(field(&body, "bounds"));
    assert_eq!(bounds.len(), 12);
    for case in bounds {
        let name = text(field(case, "name"));
        let files = route_tree(
            number(field(case, "routes")),
            matches!(field(case, "vite"), V::Bool(true)),
        );
        let explicit = explicit(field(case, "explicit"));
        let got = run(&files, explicit.as_deref());
        assert_eq!(
            field(&got, "entryPoints"),
            field(case, "entryPoints"),
            "{name}"
        );
        for result in items(field(&got, "recognized")) {
            let id = text(field(result, "recognizerId"));
            assert_eq!(
                field(result, "unresolvedChoices"),
                field(field(case, "unresolved"), id),
                "{name} {id}"
            );
            assert_eq!(
                items(field(field(result, "effects"), "entryPoints")).len(),
                number(field(field(case, "entryCounts"), id)),
                "{name} {id}"
            );
        }
        let row = unit_recognition(&registry, 0, "", "package.json", got).unwrap();
        assert_eq!(
            row.recognition_id,
            text(field(case, "recognitionId")),
            "{name}"
        );
    }
}

#[test]
fn the_cargo_workspace_fact_and_provenance_match_the_reference() {
    let body = parse_json(VECTORS).unwrap();
    for fact in items(field(&body, "cargoWorkspaceFacts")) {
        let expected = match field(fact, "fact") {
            V::Null => None,
            V::Bool(b) => Some(*b),
            other => panic!("{other:?}"),
        };
        let raw = bytes(text(field(fact, "hex")));
        assert_eq!(cargo_workspace_fact(&raw), expected, "{raw:?}");
    }
    for row in items(field(&body, "provenance")) {
        assert_eq!(
            discovered_provenance(text(field(row, "recognizerId")), 1),
            text(field(row, "rendered"))
        );
    }
}

#[test]
fn a_present_evidence_file_without_bytes_is_refused() {
    let paths: BTreeSet<String> = ["package.json".to_owned()].into_iter().collect();
    let none = BTreeMap::new();
    let refused = recognize(&RecognitionInputs {
        paths: &paths,
        bytes: &none,
        explicit_entry_points: None,
    });
    assert_eq!(
        refused,
        Err(RecognitionError::MissingEvidenceBytes(
            "package.json".to_owned()
        ))
    );
}

fn result(id: &'static str, evidence: usize, entry: &[String]) -> Recognized {
    Recognized {
        id,
        evidence: (0..evidence)
            .map(|i| (format!("p{i}"), "0".repeat(64), "f"))
            .collect(),
        assurance: "declared",
        entry: entry.to_vec(),
        tests: Vec::new(),
        ignore: Vec::new(),
        unresolved: Vec::new(),
    }
}

#[test]
fn the_structural_bounds_hold_at_the_bound_and_refuse_one_past() {
    let many = |n: usize| (0..n).map(|_| result("vite", 1, &[])).collect::<Vec<_>>();
    assert_eq!(structural_bounds(&many(MAX_RECOGNIZERS)), Ok(()));
    assert!(structural_bounds(&many(MAX_RECOGNIZERS + 1)).is_err());
    assert_eq!(
        structural_bounds(&[result("vite", MAX_EVIDENCE, &[])]),
        Ok(())
    );
    assert!(structural_bounds(&[result("vite", MAX_EVIDENCE + 1, &[])]).is_err());
    assert!(structural_bounds(&[result("vite", 0, &[])]).is_err());
}

#[test]
fn the_entry_bound_counts_the_distinct_union() {
    let routes: Vec<String> = (0..MAX_ENTRY_POINTS).map(|i| format!("r{i}")).collect();
    // Overlapping entries: 65,536 distinct, kept.
    let mut kept = vec![
        result("nextjs", 1, &routes),
        result("cargo-package", 1, &routes[..2]),
    ];
    entry_bound(&mut kept);
    assert!(
        kept.iter()
            .all(|r| !r.entry.is_empty() && r.unresolved.is_empty())
    );
    // One more distinct entry in another result: none kept, both disclose.
    let mut over = vec![
        result("nextjs", 1, &routes),
        result("vite", 1, &["index.html".to_owned()]),
        result("node-package", 1, &[]),
    ];
    entry_bound(&mut over);
    assert!(over.iter().all(|r| r.entry.is_empty()));
    assert_eq!(over[0].unresolved, [ENTRY_POINTS_OVER_BOUND]);
    assert_eq!(over[1].unresolved, [ENTRY_POINTS_OVER_BOUND]);
    assert!(over[2].unresolved.is_empty());
}

/// r2 (B2D2-R1-RF-3): one TOML profile document, as the vector tool builds it.
fn toml_document(prefix: &[u8], form: &str, n: usize) -> Vec<u8> {
    let mut raw = prefix.to_vec();
    match form {
        "comment" => {
            raw.push(b'#');
            raw.resize(n - 1, b'#');
            raw.push(b'\n');
        }
        "array" => {
            raw.extend_from_slice(b"x = [");
            for _ in 0..n {
                raw.extend_from_slice(b"0,");
            }
            raw.extend_from_slice(b"]\n");
        }
        "nested" => {
            raw.extend_from_slice(b"x = ");
            raw.extend(std::iter::repeat_n(b'[', n));
            raw.push(b'0');
            raw.extend(std::iter::repeat_n(b']', n));
            raw.push(b'\n');
        }
        _ => {
            let keys = vec!["a"; n].join(".");
            raw.extend_from_slice(keys.as_bytes());
            raw.extend_from_slice(b" = 1\n");
        }
    }
    raw
}

#[test]
fn the_toml_profile_controls_hold_and_the_recursion_divergence_is_product_only() {
    let body = parse_json(VECTORS).unwrap();
    let registry = schemas();
    let cases = items(field(&body, "tomlProfile"));
    assert_eq!(cases.len(), 7);
    for case in cases {
        let name = text(field(case, "name"));
        let raw = toml_document(
            &bytes(text(field(case, "prefix"))),
            text(field(case, "form")),
            number(field(case, "n")),
        );
        assert_eq!(raw.len(), number(field(case, "length")), "{name}");
        let mut files = BTreeMap::new();
        files.insert("Cargo.toml".to_owned(), raw.clone());
        files.insert("src/main.rs".to_owned(), Vec::new());
        let got = run(&files, None);
        assert_eq!(
            field(&got, "entryPoints"),
            field(case, "entryPoints"),
            "{name}"
        );
        for result in items(field(&got, "recognized")) {
            let id = text(field(result, "recognizerId"));
            assert_eq!(
                field(result, "unresolvedChoices"),
                field(field(case, "unresolved"), id),
                "{name} {id}"
            );
            assert_eq!(
                items(field(field(result, "effects"), "entryPoints")).len(),
                number(field(field(case, "entryCounts"), id)),
                "{name} {id}"
            );
        }
        let expected_fact = match field(case, "fact") {
            V::Null => None,
            V::Bool(b) => Some(*b),
            other => panic!("{other:?}"),
        };
        assert_eq!(cargo_workspace_fact(&raw), expected_fact, "{name}");
        let row = unit_recognition(&registry, 0, "", "Cargo.toml", got).unwrap();
        if !matches!(field(case, "productOnly"), V::Bool(true)) {
            assert_eq!(
                row.recognition_id,
                text(field(case, "recognitionId")),
                "{name}"
            );
        }
    }
}

#[test]
fn every_present_evidence_file_needs_its_bytes() {
    // r2 (B2D2-R1-RF-1): each of the fifteen names alone, without bytes.
    for name in EVIDENCE_FILES {
        let paths: BTreeSet<String> = [name.to_owned()].into_iter().collect();
        for explicit in [None, Some(&[][..])] {
            let refused = recognize(&RecognitionInputs {
                paths: &paths,
                bytes: &BTreeMap::new(),
                explicit_entry_points: explicit,
            });
            assert_eq!(
                refused,
                Err(RecognitionError::MissingEvidenceBytes(name.to_owned())),
                "{name}"
            );
        }
    }
    // An unselected lower-priority file still needs its bytes.
    for (present, supplied, missing) in [
        (
            &["tsconfig.json", "jsconfig.json"][..],
            "tsconfig.json",
            "jsconfig.json",
        ),
        (
            &["next.config.js", "next.config.ts"][..],
            "next.config.js",
            "next.config.ts",
        ),
        (
            &["vite.config.ts", "vite.config.mjs"][..],
            "vite.config.ts",
            "vite.config.mjs",
        ),
        (
            &["jest.config.js", "Cargo.toml"][..],
            "Cargo.toml",
            "jest.config.js",
        ),
    ] {
        let paths: BTreeSet<String> = present.iter().map(|p| (*p).to_owned()).collect();
        let mut bytes = BTreeMap::new();
        bytes.insert(supplied.to_owned(), b"{}".to_vec());
        let refused = recognize(&RecognitionInputs {
            paths: &paths,
            bytes: &bytes,
            explicit_entry_points: Some(&[]),
        });
        assert_eq!(
            refused,
            Err(RecognitionError::MissingEvidenceBytes(missing.to_owned())),
            "{present:?}"
        );
    }
    // Other member content stays optional.
    let paths: BTreeSet<String> = ["Cargo.toml".to_owned(), "src/main.rs".to_owned()]
        .into_iter()
        .collect();
    let mut bytes = BTreeMap::new();
    bytes.insert(
        "Cargo.toml".to_owned(),
        b"[package]\nname = \"a\"\n".to_vec(),
    );
    assert!(
        recognize(&RecognitionInputs {
            paths: &paths,
            bytes: &bytes,
            explicit_entry_points: None,
        })
        .is_ok()
    );
}

fn set(value: &mut V, path: &[&str], replacement: V) {
    let mut at = value;
    for key in path {
        at = match at {
            V::Object(fields) => fields.get_mut(*key).unwrap(),
            V::Array(list) => &mut list[key.parse::<usize>().unwrap()],
            other => panic!("{other:?}"),
        };
    }
    *at = replacement;
}

#[test]
fn a_row_outside_the_schema_is_refused() {
    // r2 (B2D2-R1-RF-2): the bound schema's constants, patterns, bounds and
    // uniqueness, beyond what the generated type checks.
    let body = parse_json(VECTORS).unwrap();
    let registry = schemas();
    let mixed = items(field(&body, "units"))
        .iter()
        .find(|u| text(field(u, "name")) == "mixed")
        .unwrap();
    let valid = field(mixed, "recognition").clone();
    assert!(unit_recognition(&registry, 4, "apps/web", "package.json", valid.clone()).is_ok());
    let one = |n: i128| V::Integer(JsonInteger::new(n).unwrap());
    let mut mutants: Vec<(&str, V)> = Vec::new();
    let mut m = valid.clone();
    set(&mut m, &["schemaVersion"], one(2));
    mutants.push(("schema-version-2", m));
    let mut m = valid.clone();
    set(&mut m, &["recognized", "0", "recognizerVersion"], one(2));
    mutants.push(("recognizer-version-2", m));
    let mut m = valid.clone();
    set(
        &mut m,
        &["recognized", "0", "evidence"],
        V::Array(Vec::new()),
    );
    mutants.push(("empty-evidence", m));
    let mut m = valid.clone();
    if let V::Object(fields) = &mut m
        && let Some(V::Array(list)) = fields.get_mut("recognized")
    {
        let first = list[0].clone();
        list.push(first);
    }
    mutants.push(("duplicate-result", m));
    let mut m = valid.clone();
    set(
        &mut m,
        &["recognized", "0", "effects", "entryPoints"],
        V::Array(vec![V::String("/abs".to_owned())]),
    );
    mutants.push(("absolute-entry-path", m));
    let mut m = valid.clone();
    set(
        &mut m,
        &["recognized", "0", "unresolvedChoices"],
        V::Array((0..17).map(|i| V::String(format!("c{i}"))).collect()),
    );
    mutants.push(("seventeen-unresolved", m));
    let mut m = valid.clone();
    set(
        &mut m,
        &["entryPoints", "state"],
        V::String("some".to_owned()),
    );
    mutants.push(("unknown-state", m));
    for (name, recognition) in mutants {
        assert_eq!(
            unit_recognition(&registry, 4, "apps/web", "package.json", recognition).err(),
            Some(RecognitionError::Shape),
            "{name}"
        );
    }
    for root in ["..", "/abs", "a/../b"] {
        assert_eq!(
            unit_recognition(&registry, 0, root, "package.json", valid.clone()).err(),
            Some(RecognitionError::Shape),
            "{root}"
        );
    }
}
