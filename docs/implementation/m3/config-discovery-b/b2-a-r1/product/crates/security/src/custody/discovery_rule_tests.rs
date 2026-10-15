// Unit B2-a's controls (M3-B r5 items 13 and 14; B-S1's B2-a controls).
// Reference vectors from tools/security/discovery_rule_vectors.py; synthetic
// supplied paths otherwise. No filesystem tree is read.
use super::*;
use opensip_identity::{JsonValue as V, parse_json};

const VECTORS: &[u8] = include_bytes!("discovery_rule_vectors.json");
const SOURCE: &str = include_str!("discovery_rule.rs");

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    &fields[key]
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
fn int(n: usize) -> V {
    V::Integer(opensip_identity::JsonInteger::new(n as i128).unwrap())
}
fn string(s: &str) -> V {
    V::String(s.to_owned())
}
fn list<S: AsRef<str>>(values: impl IntoIterator<Item = S>) -> V {
    V::Array(values.into_iter().map(|s| string(s.as_ref())).collect())
}
fn object(pairs: Vec<(&str, V)>) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
/// A supplied path list, expanding `{"range": [prefix, suffix, count]}`.
fn paths(value: &V) -> Vec<String> {
    let mut out = Vec::new();
    for item in items(value) {
        match item {
            V::String(s) => out.push(s.clone()),
            V::Object(range) => {
                let spec = items(&range["range"]);
                let V::Integer(count) = &spec[2] else {
                    panic!()
                };
                let count = usize::try_from(count.get()).unwrap();
                out.extend((0..count).map(|i| format!("{}{i}{}", text(&spec[0]), text(&spec[1]))));
            }
            other => panic!("{other:?}"),
        }
    }
    out
}
fn set(value: &V) -> BTreeSet<String> {
    paths(value).into_iter().collect()
}
fn anchor(found: Option<PrunedAnchor>) -> V {
    found.map_or(V::Null, |a| list([a.path.as_str(), a.reason.as_str()]))
}
fn row(row: &PrunedTreeRow) -> V {
    object(vec![
        ("path", string(&row.anchor.path)),
        ("reason", string(row.anchor.reason.as_str())),
        (
            "markerCount",
            row.marker_count.map_or(V::Null, |n| int(n as usize)),
        ),
        ("markerCountBasis", string(row.basis.as_str())),
    ])
}
fn custody_rows(value: &V) -> Vec<CustodyExcludedUnit> {
    items(value)
        .iter()
        .map(|r| CustodyExcludedUnit {
            path: text(field(r, "path")).to_owned(),
            reason: text(field(r, "reason")).to_owned(),
        })
        .collect()
}
fn kwarg<'v>(case: &'v V, key: &str) -> Option<&'v V> {
    let V::Object(kwargs) = field(case, "kwargs") else {
        panic!()
    };
    kwargs.get(key)
}

/// The product's result for one vector, in the reference's JSON shape.
fn product(case: &V) -> V {
    let args = items(field(case, "args"));
    let ok = |v: V| object(vec![("ok", v)]);
    let refusal = |s: &str| object(vec![("refusal", string(s))]);
    match text(field(case, "function")) {
        "normalize_explicit_root" => match normalize_explicit_root(text(&args[0])) {
            Ok(root) => ok(string(&root)),
            Err(RootGrammar) => refusal("ROOT_GRAMMAR"),
        },
        "spell_root" => ok(string(spell_root(text(&args[0])))),
        "classify_path" => ok(anchor(classify_path(
            text(&args[0]),
            &set(&args[1]),
            &set(&args[2]),
        ))),
        "cargo_roots_from_markers" => ok(list(cargo_roots_from_markers(
            &paths(&args[0]),
            &set(&args[1]),
        ))),
        "pruned_anchors_from_directories" => ok(V::Array(
            pruned_anchors_from_directories(&paths(&args[0]), &set(&args[1]), &set(&args[2]))
                .into_iter()
                .map(|a| anchor(Some(a)))
                .collect(),
        )),
        "enumerate_units" => {
            let observed = kwarg(case, "observed_directories").map(paths);
            let unreadable = kwarg(case, "unreadable_anchors")
                .map(paths)
                .unwrap_or_default();
            let members = kwarg(case, "member_roots").map(set).unwrap_or_default();
            let basis = match kwarg(case, "marker_inventory_basis").map(text) {
                None | Some("observed-inventory") => MarkerCountBasis::ObservedInventory,
                Some("not-enumerated") => MarkerCountBasis::NotEnumerated,
                Some(other) => panic!("{other}"),
            };
            let enforce_limit = !matches!(kwarg(case, "enforce_limit"), Some(V::Bool(false)));
            let result = enumerate_units(
                &paths(&args[0]),
                &EnumerationInput {
                    enforce_limit,
                    observed_directories: observed.as_deref(),
                    basis,
                    unreadable_anchors: &unreadable,
                    member_roots: &members,
                },
            );
            ok(object(vec![
                ("unitDirs", list(&result.unit_dirs)),
                (
                    "prunedTrees",
                    V::Array(result.pruned_trees.iter().map(row).collect()),
                ),
                (
                    "refusal",
                    result.refusal.map_or(V::Null, |r| {
                        object(vec![
                            ("detail", string("WORKSPACE_UNIT_LIMIT")),
                            ("unitCount", int(r.unit_count)),
                            ("limit", int(MAX_WORKSPACE_UNITS)),
                        ])
                    }),
                ),
            ]))
        }
        "relative_locator" => match relative_locator(text(&args[0]), text(&args[1])) {
            Ok(rel) => ok(string(&rel)),
            Err(LocatorRefusal::OutsideRoot) => refusal("LOCATOR_OUTSIDE_ROOT"),
            Err(LocatorRefusal::Grammar) => refusal("LOCATOR_GRAMMAR"),
        },
        "classify_boundary" => {
            let (repos, projects) = (paths(&args[1]), paths(&args[2]));
            ok(classify_boundary(text(&args[0]), &repos, &projects)
                .map_or(V::Null, |(a, r)| list([a, r.as_str()])))
        }
        "classify_custody_exclusion" => {
            let marker = match &args[1] {
                V::Null => None,
                value => Some(text(value)),
            };
            ok(
                classify_custody_exclusion(text(&args[0]), marker, &custody_rows(&args[2]))
                    .map_or(V::Null, |a| list([a, "custody-excluded"])),
            )
        }
        "boundary_excluded_prefixes" => {
            let inventory = &args[0];
            ok(list(boundary_excluded_prefixes(
                &paths(field(inventory, "nestedRepositories")),
                &paths(field(inventory, "nestedProjects")),
                &custody_rows(field(inventory, "custodyExcludedUnits")),
            )))
        }
        "conventional_excluded_prefixes" => ok(list(conventional_excluded_prefixes(
            &paths(&args[0]),
            &set(&args[1]),
            &set(&args[2]),
        ))),
        other => panic!("{other}"),
    }
}

#[test]
fn every_reference_vector_is_reproduced() {
    let vectors = parse_json(VECTORS).unwrap();
    // Generated by the B2-a reference refresh at its accepted bytes.
    let source = &items(field(&vectors, "sources"))[0];
    assert_eq!(
        text(field(source, "path")),
        "docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py"
    );
    assert_eq!(
        text(field(source, "sha256")),
        "4a104209af0ba89c76826ba7f6be4c4085f1eb7db90410f6bb731041562fdcc8"
    );
    let cases = items(field(&vectors, "cases"));
    assert!(cases.len() > 2500, "{}", cases.len());
    let mut functions = BTreeSet::new();
    for case in cases {
        functions.insert(text(field(case, "function")));
        assert_eq!(&product(case), field(case, "reference"), "{case:?}");
    }
    // Every entry point of the rule is cross-checked.
    assert_eq!(functions.len(), 11, "{functions:?}");
}

fn members(roots: &[&str]) -> BTreeSet<String> {
    roots.iter().map(|r| (*r).to_owned()).collect()
}

#[test]
fn every_entry_kind_at_an_anchor_is_never_entered_and_only_directories_are_recorded() {
    let none = BTreeSet::new();
    let m = members(&["m"]);
    for kind in [
        EntryKind::Directory,
        EntryKind::File,
        EntryKind::Symlink,
        EntryKind::Other,
    ] {
        for (path, members) in [
            (".opensip", &none),
            ("m/.opensip", &m),
            ("node_modules", &none),
            (".git", &none),
        ] {
            let EntryDisposition::NeverEnter { anchor, recorded } =
                classify_entry(path, kind, &none, members)
            else {
                panic!("{path}")
            };
            assert_eq!(anchor.path, path);
            assert_eq!(recorded, kind == EntryKind::Directory, "{path} {kind:?}");
        }
        // `.opensip` anywhere else is ordinary source, whatever its kind.
        for path in ["src/.opensip", "m/.opensip", "m/src/.opensip", ".OpenSIP"] {
            assert_eq!(
                classify_entry(path, kind, &none, &none),
                EntryDisposition::Ordinary,
                "{path}"
            );
        }
    }
    // An entry below an anchor is never reached by a walker that never
    // enters; supplied anyway, it is never entered and never recorded.
    assert_eq!(
        classify_entry(".opensip/local.json", EntryKind::Directory, &none, &none),
        EntryDisposition::NeverEnter {
            anchor: PrunedAnchor {
                path: ".opensip".to_owned(),
                reason: PruneReason::OpensipCustodyState
            },
            recorded: false
        }
    );
}

#[test]
fn classify_entry_agrees_with_classify_path_over_the_sweep() {
    let segments = [
        "a",
        "node_modules",
        ".git",
        "target",
        ".opensip",
        "src",
        "Cargo.toml",
    ];
    let mut paths: Vec<String> = segments.iter().map(|s| (*s).to_owned()).collect();
    for _ in 0..2 {
        let deeper: Vec<String> = paths
            .iter()
            .flat_map(|p| segments.iter().map(move |s| format!("{p}/{s}")))
            .collect();
        paths.extend(deeper);
    }
    for cargo in [members(&[]), members(&[""]), members(&["", "a"])] {
        for member_roots in [members(&[]), members(&["a"])] {
            for path in &paths {
                let expected = classify_path(path, &cargo, &member_roots);
                for kind in [EntryKind::Directory, EntryKind::File] {
                    match (classify_entry(path, kind, &cargo, &member_roots), &expected) {
                        (EntryDisposition::Ordinary, None) => {}
                        (EntryDisposition::NeverEnter { anchor, recorded }, Some(found)) => {
                            assert_eq!(&anchor, found);
                            assert_eq!(
                                recorded,
                                kind == EntryKind::Directory && found.path == *path
                            );
                        }
                        other => panic!("{path}: {other:?}"),
                    }
                }
            }
        }
    }
}

#[test]
fn the_cap_refuses_without_truncation_and_never_counts_dependencies() {
    let none = BTreeSet::new();
    let input = |enforce_limit| EnumerationInput::<String> {
        enforce_limit,
        observed_directories: None,
        basis: MarkerCountBasis::NotEnumerated,
        unreadable_anchors: &[],
        member_roots: &none,
    };
    let units = |n: usize| {
        (0..n)
            .map(|i| format!("p{i}/package.json"))
            .collect::<Vec<_>>()
    };
    let at = enumerate_units(&units(MAX_WORKSPACE_UNITS), &input(true));
    assert_eq!(
        (at.unit_dirs.len(), at.refusal),
        (MAX_WORKSPACE_UNITS, None)
    );
    let over = enumerate_units(&units(MAX_WORKSPACE_UNITS + 1), &input(true));
    assert!(over.unit_dirs.is_empty());
    assert_eq!(over.refusal, Some(WorkspaceUnitLimit { unit_count: 4097 }));
    let mut installed: Vec<String> = (0..5000)
        .map(|i| format!("node_modules/p{i}/package.json"))
        .collect();
    installed.push("package.json".to_owned());
    let result = enumerate_units(&installed, &input(true));
    assert_eq!(result.unit_dirs, [""]);
    assert_eq!(result.refusal, None);
    assert_eq!(result.pruned_trees.len(), 1);
    assert_eq!(result.pruned_trees[0].marker_count, None);
}

#[test]
fn rule_outputs_are_sorted_and_unique() {
    let none = BTreeSet::new();
    let dirs = [
        "target",
        "b/node_modules",
        "a/.git",
        "b/node_modules",
        "a/.git/x",
        ".opensip",
    ];
    let anchors = pruned_anchors_from_directories(&dirs, &members(&[""]), &none);
    let keys: Vec<(&str, &str)> = anchors
        .iter()
        .map(|a| (a.path.as_str(), a.reason.as_str()))
        .collect();
    let mut sorted = keys.clone();
    sorted.sort();
    sorted.dedup();
    assert_eq!(keys, sorted);
    assert_eq!(keys.len(), 4);
}

#[test]
fn the_module_is_pure() {
    let code: String = SOURCE
        .lines()
        .map(|line| line.split("//").next().unwrap())
        .collect::<Vec<_>>()
        .join("\n");
    for forbidden in [
        "std::fs",
        "std::io",
        "std::env",
        "std::process",
        "std::net",
        "opensip_platform",
        "unsafe",
        "pub fn",
        "pub struct",
        "pub enum",
    ] {
        assert!(!code.contains(forbidden), "{forbidden}");
    }
    let uses: Vec<&str> = SOURCE.lines().filter(|l| l.starts_with("use ")).collect();
    assert_eq!(uses, ["use std::collections::{BTreeMap, BTreeSet};"]);
}
