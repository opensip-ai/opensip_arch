// Units B2-c2 and B2-c2b (M3-B r8 item 14a, as r9 and r10 amend it):
// `jsonc.rs` and `typescript_config.rs` replay
// `typescript_config_vectors.json`, which
// `tools/host/typescript_config_vectors.py` generates from the law's
// controls, the S10b native model copy (contract successor 172) and the B2-c0
// reference (contract successor 166). Each case's tree is an in-memory
// source; the result, the graph, the refusal and every path the reader asked
// for are compared exactly. Row 59's termination is the model's D9 row,
// remedy and bounded subject. M3-B r10: every admitted graph is admitted by
// the embedded `TypeScriptConfigGraphV1` schema, whose own bounds are r10's.
use crate::discovery::{MarkerFact, standalone};
use crate::jsonc::{self, Node};
use crate::outcomes::{Observation, project};
use crate::typescript_config::{
    ConfigEntry, ConfigFault, ConfigGraph, ConfigRefusal, ConfigRefusalKey, ConfigSource,
    MAX_CONFIG_FILE_BYTES, MAX_EXTENDS_ENTRIES, MAX_NODE_PATH_CHARS, TYPESCRIPT_CONFIG_ALIASES,
    effective_allow_js, observe_effective_allow_js, public_detail,
};
use opensip_contracts::generated::evidence::Common4DomainDetailCode as Detail;
use opensip_identity::{JsonValue as V, canonical_bytes, parse_json};
use std::cell::RefCell;
use std::collections::BTreeMap;

const VECTORS: &[u8] = include_bytes!("typescript_config_vectors.json");
const NATIVE_SCHEMA: &[u8] = include_bytes!("../../../schemas/sources/native-v2.schema.json");
const NATIVE_SCHEMA_ID: &str = "urn:opensip:product-v1:native:evidence-schemas:v2";
const GRAPH_SELECTOR: &str = "/$defs/TypeScriptConfigGraphV1";
const SCHEMA_BUDGET: usize = 64 * 1024 * 1024;

/// M3-B r10: whether the embedded native schema admits `graph` as a
/// `TypeScriptConfigGraphV1` record.
fn admitted(graph: &ConfigGraph) -> bool {
    let raw = canonical(&graph_json(graph));
    crate::embedded_schema_registry()
        .expect("registry")
        .schema(NATIVE_SCHEMA_ID, GRAPH_SELECTOR)
        .expect("graph schema")
        .admit_json(&raw, SCHEMA_BUDGET)
        .is_ok()
}

fn field<'v>(v: &'v V, key: &str) -> &'v V {
    match v {
        V::Object(m) => m.get(key).unwrap_or_else(|| panic!("missing {key}")),
        _ => panic!("not an object at {key}"),
    }
}
fn get<'v>(v: &'v V, key: &str) -> Option<&'v V> {
    match v {
        V::Object(m) => m.get(key),
        _ => None,
    }
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
fn truth(v: &V) -> bool {
    match v {
        V::Bool(b) => *b,
        other => panic!("not a boolean: {other:?}"),
    }
}
fn count(v: &V) -> usize {
    match v {
        V::Integer(i) => usize::try_from(i.get()).expect("count"),
        other => panic!("not an integer: {other:?}"),
    }
}
fn s(t: &str) -> V {
    V::String(t.to_owned())
}
fn canonical(v: &V) -> Vec<u8> {
    canonical_bytes(v).expect("canonical")
}
fn unhex(t: &str) -> Vec<u8> {
    (0..t.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&t[i..i + 2], 16).expect("hex"))
        .collect()
}

/// One tree entry: a file (`text`, `hex` or `pad`), a directory or a link.
enum Entry {
    File(Vec<u8>),
    Dir,
    Link,
}

/// The vectors' in-memory project tree, read as the reference's `Tree`
/// reads it, with a log of every path asked for.
struct Tree {
    entries: BTreeMap<String, Entry>,
    log: RefCell<Vec<String>>,
}
impl Tree {
    fn of(v: &V) -> Self {
        let mut entries = BTreeMap::new();
        for e in items(v) {
            let entry = if get(e, "link").is_some() {
                Entry::Link
            } else if get(e, "dir").is_some() {
                Entry::Dir
            } else if let Some(t) = get(e, "text") {
                Entry::File(text(t).into_bytes())
            } else if let Some(h) = get(e, "hex") {
                Entry::File(unhex(&text(h)))
            } else {
                let pad = field(e, "pad");
                let mut t = text(field(pad, "prefix"));
                t.push_str(&text(field(pad, "repeat")).repeat(count(field(pad, "count"))));
                t.push_str(&text(field(pad, "suffix")));
                Entry::File(t.into_bytes())
            };
            entries.insert(text(field(e, "path")), entry);
        }
        Self {
            entries,
            log: RefCell::new(Vec::new()),
        }
    }
    fn reads(&self) -> V {
        V::Array(self.log.borrow().iter().map(|p| s(p)).collect())
    }
}
impl ConfigSource for Tree {
    fn read(&self, path: &str, limit: usize) -> ConfigEntry {
        self.log.borrow_mut().push(path.to_owned());
        let parts: Vec<&str> = path.split('/').collect();
        for k in 1..=parts.len() {
            match self.entries.get(&parts[..k].join("/")) {
                Some(Entry::Link) => return ConfigEntry::Link,
                Some(Entry::File(_)) if k < parts.len() => return ConfigEntry::NotAFile,
                _ => {}
            }
        }
        match self.entries.get(path) {
            Some(Entry::File(bytes)) => {
                ConfigEntry::File(bytes[..bytes.len().min(limit + 1)].to_vec())
            }
            _ => ConfigEntry::NotAFile,
        }
    }
}

/// `TypeScriptConfigGraphV1` as JSON.
fn graph_json(graph: &ConfigGraph) -> V {
    let nodes = graph
        .nodes
        .iter()
        .map(|n| {
            V::Object(
                [
                    ("path", s(&n.path)),
                    ("contentSha256", s(&n.content_sha256)),
                    ("kind", s(n.kind.as_str())),
                    (
                        "extendsResolved",
                        V::Array(n.extends_resolved.iter().map(|e| s(e)).collect()),
                    ),
                ]
                .into_iter()
                .map(|(k, v)| (k.to_owned(), v))
                .collect(),
            )
        })
        .collect();
    let one = opensip_identity::JsonInteger::new(1).expect("one");
    V::Object(
        [
            ("schemaVersion", V::Integer(one)),
            ("entryConfigPath", s(&graph.entry_config_path)),
            ("nodes", V::Array(nodes)),
        ]
        .into_iter()
        .map(|(k, v)| (k.to_owned(), v))
        .collect(),
    )
}

fn key_of(key: &str) -> ConfigRefusalKey {
    [
        ConfigRefusalKey::Bound,
        ConfigRefusalKey::ExtendsCycle,
        ConfigRefusalKey::ExtendsUnresolved,
        ConfigRefusalKey::Malformed,
    ]
    .into_iter()
    .find(|k| k.key() == key)
    .unwrap_or_else(|| panic!("unknown key {key}"))
}

#[test]
fn every_law_control_replays_with_its_graph_and_reads() {
    let body = parse_json(VECTORS).expect("vectors");
    let cases = items(field(&body, "cases"));
    assert!(cases.len() >= 100, "{}", cases.len());
    let mut failures = Vec::new();
    for case in cases {
        let id = text(field(case, "id"));
        let tree = Tree::of(field(case, "tree"));
        let got = effective_allow_js(&text(field(case, "entry")), &tree);
        let ok = match (text(field(case, "outcome")).as_str(), &got) {
            ("result", Ok(effective)) => {
                let want = field(case, "result");
                let work = field(want, "work");
                // B2C2-R1-RF-3: each node evaluated once, each edge merged
                // once, as the reference records.
                let linear = effective.work.node_evaluations == effective.graph.nodes.len()
                    && effective.work.edge_merges
                        == effective
                            .graph
                            .nodes
                            .iter()
                            .map(|n| n.extends_resolved.len())
                            .sum::<usize>();
                effective.allow_js == truth(field(want, "allowJs"))
                    && effective.check_js == truth(field(want, "checkJs"))
                    && canonical(&graph_json(&effective.graph)) == canonical(field(want, "graph"))
                    && linear
                    && admitted(&effective.graph)
                    && effective.work.node_evaluations == count(field(work, "nodeEvaluations"))
                    && effective.work.edge_merges == count(field(work, "edgeMerges"))
            }
            ("refused", Err(ConfigFault::Refused(r))) => {
                r.key.key() == text(field(case, "key")) && r.path == text(field(case, "path"))
            }
            _ => false,
        };
        let reads_ok = canonical(&tree.reads()) == canonical(field(case, "reads"));
        if !ok || !reads_ok {
            failures.push(format!("{id}: {got:?} reads_ok={reads_ok}"));
        }
    }
    assert!(failures.is_empty(), "{}", failures.join("\n"));
}

fn marker_facts(v: &V) -> BTreeMap<String, MarkerFact> {
    let V::Object(m) = v else { panic!("markers") };
    m.iter()
        .map(|(path, info)| {
            let flag = |k: &str| get(info, k).map(truth);
            (
                path.clone(),
                MarkerFact {
                    sha256: text(field(info, "sha256")),
                    is_cargo_workspace: flag("isCargoWorkspace"),
                    allow_js: flag("allowJs"),
                },
            )
        })
        .collect()
}

/// Item 14a's units controls: the seven `units-config-effective-allowjs-*`
/// cases from configuration bytes, discovery before and after the reading.
#[test]
fn the_units_cases_are_reproduced_from_configuration_bytes() {
    let body = parse_json(VECTORS).expect("vectors");
    let units = items(field(&body, "units"));
    assert_eq!(units.len(), 7);
    for u in units {
        let id = text(field(u, "id"));
        let raw = marker_facts(field(u, "markers"));
        let tree = Tree::of(field(u, "tree"));
        let first = standalone::discover_units(&raw, None);
        let observed = observe_effective_allow_js(&raw, &first, &tree).expect(&id);
        assert_eq!(observed, marker_facts(field(u, "observed")), "{id}");
        let last = standalone::discover_units(&observed, None);
        assert_eq!(
            canonical(&last.to_json()),
            canonical(field(u, "result")),
            "{id}"
        );
        assert_eq!(
            canonical(&tree.reads()),
            canonical(field(u, "reads")),
            "{id}"
        );
    }
}

/// A refused discovery reads nothing, and a refusal in the graph is the
/// composition's result.
#[test]
fn the_composition_reads_only_surviving_configuration_markers() {
    let fact = |allow_js| MarkerFact {
        sha256: "b".repeat(64),
        is_cargo_workspace: None,
        allow_js,
    };
    let markers: BTreeMap<String, MarkerFact> = [
        ("tsconfig.json".to_owned(), fact(None)),
        ("node_modules/dep/tsconfig.json".to_owned(), fact(None)),
    ]
    .into_iter()
    .collect();
    let tree = Tree {
        entries: [(
            "tsconfig.json".to_owned(),
            Entry::File(b"{\"extends\": \"./missing.json\"}".to_vec()),
        )]
        .into_iter()
        .collect(),
        log: RefCell::new(Vec::new()),
    };
    let first = standalone::discover_units(&markers, None);
    assert_eq!(first.units.len(), 1);
    assert_eq!(
        observe_effective_allow_js(&markers, &first, &tree),
        Err(ConfigFault::Refused(ConfigRefusal {
            key: ConfigRefusalKey::ExtendsUnresolved,
            path: "tsconfig.json".to_owned(),
        }))
    );
    // The installed manifest under the pruned tree is never read.
    assert!(
        tree.log
            .borrow()
            .iter()
            .all(|p| !p.starts_with("node_modules/dep"))
    );
    let refused = standalone::discover_units(&markers, Some(&["../x".to_owned()]));
    assert!(refused.refused.is_some());
    let quiet = Tree {
        entries: BTreeMap::new(),
        log: RefCell::new(Vec::new()),
    };
    assert_eq!(
        observe_effective_allow_js(&markers, &refused, &quiet),
        Ok(markers.clone())
    );
    assert!(quiet.log.borrow().is_empty());
}

#[test]
fn an_entry_the_source_does_not_hold_is_a_composition_fault() {
    let empty = Tree {
        entries: BTreeMap::new(),
        log: RefCell::new(Vec::new()),
    };
    for entry in [
        "tsconfig.json",
        "",
        "/tsconfig.json",
        "a//tsconfig.json",
        "./tsconfig.json",
    ] {
        assert!(
            matches!(
                effective_allow_js(entry, &empty),
                Err(ConfigFault::Internal(_))
            ),
            "{entry}"
        );
    }
}

#[test]
fn the_alias_map_is_the_s10_registry_rows_and_unknown_keys_refuse() {
    let body = parse_json(VECTORS).expect("vectors");
    let recorded: Vec<(String, String)> = items(field(&body, "aliases"))
        .iter()
        .map(|row| (text(&items(row)[0]), text(&items(row)[1])))
        .collect();
    let ours: Vec<(String, String)> = TYPESCRIPT_CONFIG_ALIASES
        .iter()
        .map(|(a, b)| ((*a).to_owned(), (*b).to_owned()))
        .collect();
    assert_eq!(ours, recorded);
    assert_eq!(
        text(field(field(&body, "publicRecord"), "code")),
        Detail::NativeTypescriptConfigUnresolved.to_string()
    );
    for (internal, public) in TYPESCRIPT_CONFIG_ALIASES {
        assert_eq!(public_detail(internal), Ok(public));
        assert_eq!(key_of(internal).key(), internal);
    }
    assert!(public_detail("native.typescript-config-unresolved").is_err());
    assert!(public_detail("CONFIG.INVALID").is_err());
}

/// M3-J1 r7 row 59: the projection is the S10 model's D9 row for the
/// public detail, its remedy keyed by that detail, and the model's bounded
/// subject (a long or non-ASCII path included).
#[test]
fn row_59_projects_the_s10_termination() {
    let body = parse_json(VECTORS).expect("vectors");
    let d9 = field(&body, "d9");
    let terminations = items(field(&body, "terminations"));
    assert_eq!(terminations.len(), 12);
    for t in terminations {
        let refusal = ConfigRefusal {
            key: key_of(&text(field(t, "key"))),
            path: text(field(t, "path")),
        };
        let projected = project(&Observation::TypescriptConfigUnresolved(refusal));
        assert_eq!(projected.class.to_string(), text(field(d9, "class")));
        assert_eq!(projected.exit() as usize, count(field(d9, "exitCode")));
        assert_eq!(
            projected.error_code.map(|c| c.to_string()),
            Some(text(field(d9, "code")))
        );
        assert_eq!(
            projected.detail,
            Some(Detail::NativeTypescriptConfigUnresolved)
        );
        assert_eq!(
            projected.remedy.map(str::to_owned),
            Some(text(field(d9, "remedy")))
        );
        assert_eq!(projected.subject, Some(text(field(t, "subject"))));
        assert!(projected.operational.is_empty());
        assert_eq!(projected.run_id, None);
        assert_eq!(projected.execution_id, None);
    }
}

/// The reader is iterative: a file at the bound nested 32768 deep parses,
/// and the document drops, on a test thread's stack.
#[test]
fn deep_nesting_at_the_file_bound_neither_overflows_nor_refuses() {
    let depth = MAX_CONFIG_FILE_BYTES / 2;
    let mut bytes = vec![b'['; depth];
    bytes.extend(std::iter::repeat_n(b']', depth));
    assert_eq!(bytes.len(), MAX_CONFIG_FILE_BYTES);
    let document = jsonc::parse(&bytes).expect("parses");
    assert!(matches!(document.root(), Some(Node::Array(_))));
    drop(document);
    let mut objects = Vec::new();
    for _ in 0..depth / 6 {
        objects.extend_from_slice(b"{\"a\":");
    }
    objects.extend_from_slice(b"1");
    objects.extend(std::iter::repeat_n(b'}', depth / 6));
    assert!(jsonc::parse(&objects).is_ok());
}

#[test]
fn a_duplicate_key_keeps_its_first_position_and_last_value() {
    let document = jsonc::parse(br#"{"a": 1, "b": 2, "a": 3,}"#).expect("parses");
    let Some(Node::Object(members)) = document.root() else {
        panic!("object")
    };
    let keys: Vec<&str> = members.iter().map(|(k, _)| k.as_str()).collect();
    assert_eq!(keys, ["a", "b"]);
    assert_eq!(
        document.member(document.root().unwrap(), "a"),
        Some(&Node::Number("3".to_owned()))
    );
    assert_eq!(jsonc::parse(b"  // only\n").expect("empty").root(), None);
    assert!(jsonc::parse(b"{} /* open").is_err());
}

/// The case's tree and entry from the vectors, by id.
fn vector_case(id: &str) -> (Tree, String) {
    let body = parse_json(VECTORS).expect("vectors");
    let case = items(field(&body, "cases"))
        .iter()
        .find(|c| text(field(c, "id")) == id)
        .unwrap_or_else(|| panic!("case {id}"));
    (Tree::of(field(case, "tree")), text(field(case, "entry")))
}

#[test]
fn the_record_bounds_are_the_graph_schemas_own() {
    // M3-B r10: the two bounds are the schema's numbers, read from its bytes.
    let schema = parse_json(NATIVE_SCHEMA).expect("schema");
    let defs = field(&schema, "$defs");
    let node = field(
        field(
            field(field(defs, "TypeScriptConfigGraphV1"), "properties"),
            "nodes",
        ),
        "items",
    );
    let edges = field(field(node, "properties"), "extendsResolved");
    assert_eq!(count(field(edges, "maxItems")), MAX_EXTENDS_ENTRIES);
    assert_eq!(
        count(field(field(defs, "CanonicalPath"), "maxLength")),
        MAX_NODE_PATH_CHARS
    );

    // At each bound the graph is admitted; one past it, the record could not
    // be written, which is why the reader refuses there.
    let (tree, entry) = vector_case("bound-extends-64-entries");
    let graph = effective_allow_js(&entry, &tree).expect("64 entries").graph;
    assert!(admitted(&graph));
    let mut wider = graph.clone();
    let at = wider
        .nodes
        .iter()
        .position(|n| n.path == entry)
        .expect("entry");
    let edge = wider.nodes[at].extends_resolved[0].clone();
    wider.nodes[at].extends_resolved.push(edge);
    assert_eq!(
        wider.nodes[at].extends_resolved.len(),
        MAX_EXTENDS_ENTRIES + 1
    );
    assert!(!admitted(&wider));

    for id in [
        "bound-base-path-4096-characters",
        "bound-base-path-4096-characters-non-ascii",
    ] {
        let (tree, entry) = vector_case(id);
        let graph = effective_allow_js(&entry, &tree)
            .expect("4,096 characters")
            .graph;
        assert!(admitted(&graph), "{id}");
        let base = graph
            .nodes
            .iter()
            .find(|n| n.path != entry)
            .expect("base")
            .path
            .clone();
        assert_eq!(base.chars().count(), MAX_NODE_PATH_CHARS, "{id}");
        let mut longer = graph.clone();
        let renamed = format!("{base}x");
        for n in &mut longer.nodes {
            if n.path == base {
                n.path = renamed.clone();
            }
            for e in &mut n.extends_resolved {
                if *e == base {
                    *e = renamed.clone();
                }
            }
        }
        longer.nodes.sort_by(|a, b| a.path.cmp(&b.path));
        assert!(!admitted(&longer), "{id}");
    }
}
