// M3-B r9 item 16 (unit B2-d2): host-side framework recognition against its
// cross-implementation vectors (tools/host/framework_recognition_vectors.py,
// from the bound B2-d0 reference), and FR-4's bounds exercised directly.
use super::framework_recognition::{
    ENTRY_POINTS_OVER_BOUND, MAX_ENTRY_POINTS, MAX_EVIDENCE, MAX_RECOGNIZERS, RecognitionError,
    RecognitionInputs, Recognized, cargo_workspace_fact, discovered_provenance, entry_bound,
    recognize, structural_bounds, unit_recognition,
};
use opensip_identity::{JsonValue as V, canonical_bytes, parse_json};
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
        let row = unit_recognition(0, "", "package.json", got).unwrap();
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
