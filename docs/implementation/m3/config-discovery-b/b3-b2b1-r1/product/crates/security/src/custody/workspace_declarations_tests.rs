// Unit B3-b2b1's controls (M3-B r9 items 19 to 24; B3-b plan r2 amendment
// A2). Vectors from tools/security/workspace_member_vectors.py: B3-b0's own
// checker cases and the parser controls, over synthetic observations. Every
// observation call is recorded and must stay within the reference's.
use super::super::discovery_scan::{ObservedAcl, ObservedVcs};
use super::*;
use opensip_identity::JsonValue as V;
use opensip_platform::{CapturedAclEntry, CapturedAclPrincipal, DescriptorMetadata};
use std::path::Path;

const VECTORS: &[u8] = include_bytes!("workspace_member_vectors.json");
/// An ACE with a write right (any right outside the read-only set).
const WRITE_ACE: (u32, u32) = (crate::private_access::ACE_PERMIT, 1 << 2);

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
fn int(value: &V) -> i128 {
    let V::Integer(i) = value else {
        panic!("{value:?}")
    };
    i.get()
}
fn object(value: &V) -> &BTreeMap<String, V> {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    fields
}
fn string(s: &str) -> V {
    V::String(s.to_owned())
}
fn optional(value: Option<&str>) -> V {
    value.map_or(V::Null, string)
}
fn json(pairs: Vec<(&str, V)>) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn integer(n: i128) -> V {
    V::Integer(opensip_identity::JsonInteger::new(n).unwrap())
}

/// SLM's synthetic `fs` entry as an observation hands it over (the scan
/// vectors' conversion).
fn entry(e: &V) -> ObservedEntry {
    let kind = match text(field(e, "kind")) {
        "dir" => 0o040000,
        "file" => 0o100000,
        "symlink" => 0o120000,
        _ => 0o010000,
    };
    let perm = match field(e, "mode") {
        V::String(s) => u32::from_str_radix(s, 8).unwrap(),
        V::Integer(i) => u32::try_from(i.get()).unwrap(),
        _ => 0,
    };
    let number = |key: &str, default: i128| match field(e, key) {
        V::Null => default,
        value => int(value),
    };
    let acl = if matches!(field(e, "aclUnreadable"), V::Bool(true)) {
        ObservedAcl::Unreadable
    } else {
        let entries = match field(e, "aclWrite") {
            V::Array(grants) => grants
                .iter()
                .map(|g| {
                    let (who, id) = text(g).split_once(':').unwrap();
                    let id: u32 = id.parse().unwrap();
                    CapturedAclEntry {
                        flags: WRITE_ACE.0,
                        rights: WRITE_ACE.1,
                        principal: if who == "uid" {
                            CapturedAclPrincipal::User(id)
                        } else {
                            CapturedAclPrincipal::Group(id)
                        },
                    }
                })
                .collect(),
            _ => Vec::new(),
        };
        ObservedAcl::Entries(entries)
    };
    let vcs = match field(e, "vcs") {
        V::Bool(true) => Some(ObservedVcs::Directory),
        V::Object(_) => Some(ObservedVcs::Indirection { target: None }),
        _ => None,
    };
    let absent = u32::MAX as i128;
    ObservedEntry {
        metadata: DescriptorMetadata {
            device: number("dev", 1) as u64,
            inode: 0,
            mode: kind | perm,
            uid: number("uid", absent) as u32,
            gid: number("gid", absent) as u32,
            links: number("nlink", if kind == 0o040000 { 2 } else { 1 }) as u64,
            size: number("size", 0) as u64,
            modified: (0, 0),
            changed: (0, 0),
            flags: 0,
        },
        acl,
        vcs,
    }
}

/// A content: text, `{"hex": ...}` or `{"parts": [text | [unit, count]]}`.
fn content(value: &V) -> Vec<u8> {
    match value {
        V::String(s) => s.as_bytes().to_vec(),
        V::Object(_) => match field(value, "hex") {
            V::String(hex) => (0..hex.len())
                .step_by(2)
                .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
                .collect(),
            _ => items(field(value, "parts"))
                .iter()
                .flat_map(|part| match part {
                    V::String(s) => s.as_bytes().to_vec(),
                    V::Array(pair) => text(&pair[0])
                        .repeat(usize::try_from(int(&pair[1])).unwrap())
                        .into_bytes(),
                    other => panic!("{other:?}"),
                })
                .collect(),
        },
        other => panic!("{other:?}"),
    }
}

/// B3-b0's synthetic observation, recording every lookup (`entry`, and
/// `markers` as `_markers` consults) and every read.
struct Synthetic<'v> {
    fs: &'v BTreeMap<String, V>,
    contents: &'v BTreeMap<String, V>,
    markers: &'v BTreeMap<String, V>,
    observations: &'v BTreeMap<String, V>,
    consulted: BTreeSet<String>,
    read: BTreeSet<String>,
    /// A forbidden lookup to make before anything else (the mutation
    /// control's seam): it must be caught, changing no output.
    probe: Option<String>,
}
impl WorkspaceObservation for Synthetic<'_> {
    type Error = std::convert::Infallible;
    fn entry(&mut self, rel: &str) -> Result<Option<ObservedEntry>, Self::Error> {
        if let Some(probe) = self.probe.take() {
            self.consulted.insert(probe);
        }
        self.consulted.insert(rel.to_owned());
        Ok(self.fs.get(rel).map(entry))
    }
    fn markers(&mut self, rel: &str) -> Result<Vec<(&'static str, bool)>, Self::Error> {
        if let Some(side) = self.markers.get(rel) {
            let mut out = Vec::new();
            for marker in items(side) {
                let name = [".git", ".hg", ".svn", ".jj"]
                    .into_iter()
                    .find(|m| *m == text(marker))
                    .unwrap();
                let path = format!(
                    "{}{name}",
                    if rel.is_empty() {
                        String::new()
                    } else {
                        format!("{rel}/")
                    }
                );
                self.consulted.insert(path.clone());
                let is_dir = self
                    .fs
                    .get(&path)
                    .is_some_and(|e| text(field(e, "kind")) == "dir");
                out.push((name, is_dir));
            }
            return Ok(out);
        }
        self.consulted.insert(rel.to_owned());
        Ok(match self.fs.get(rel).map(|e| field(e, "vcs")) {
            Some(V::Bool(true)) => vec![(".git", true)],
            Some(V::Object(_)) => vec![(".git", false)],
            _ => Vec::new(),
        })
    }
    fn children(&mut self, rel: &str) -> Result<Vec<String>, Self::Error> {
        Ok(self
            .fs
            .keys()
            .filter(|k| !k.is_empty() && parent(k) == rel)
            .map(|k| k.rsplit('/').next().unwrap().to_owned())
            .collect())
    }
    fn bytes(&mut self, rel: &str) -> Result<FileBytes, Self::Error> {
        self.read.insert(rel.to_owned());
        let raw = self.contents.get(rel).map(content).unwrap_or_default();
        Ok(if raw.len() > CARRIER_CAP {
            FileBytes::TooLarge
        } else {
            FileBytes::Read(raw)
        })
    }
    fn member_verdicts(
        &mut self,
        candidates: &[String],
    ) -> Result<Vec<Option<String>>, Self::Error> {
        Ok(candidates
            .iter()
            .map(|c| match self.observations.get(c) {
                Some(V::String(v)) if v != "admitted" => Some(v.clone()),
                _ => None,
            })
            .collect())
    }
}

fn rows(declarations: &[DeclarationRow]) -> V {
    V::Array(
        declarations
            .iter()
            .map(|r| {
                json(vec![
                    ("readerId", string(r.reader)),
                    ("readerVersion", integer(1)),
                    ("state", string(r.state.as_str())),
                    ("path", optional(r.path.as_deref())),
                    ("contentSha256", optional(r.content_sha256.as_deref())),
                    ("stateSubject", optional(r.state_subject.as_deref())),
                    (
                        "unresolved",
                        V::Array(
                            r.unresolved
                                .iter()
                                .map(|u| {
                                    json(vec![
                                        ("entry", string(&u.entry)),
                                        ("reason", string(u.reason)),
                                        ("subject", optional(u.subject.as_deref())),
                                    ])
                                })
                                .collect(),
                        ),
                    ),
                ])
            })
            .collect(),
    )
}

fn decision(d: &Decision) -> V {
    match d {
        Decision::Members {
            members,
            declarations,
            links,
        } => json(vec![
            ("kind", string("members")),
            (
                "members",
                V::Array(
                    members
                        .iter()
                        .map(|m| {
                            let by = m
                                .declared_by
                                .iter()
                                .map(|d| match d {
                                    Declarer::Reader {
                                        reader,
                                        path,
                                        content_sha256,
                                    } => json(vec![
                                        ("source", string("reader")),
                                        ("readerId", string(reader)),
                                        ("readerVersion", integer(1)),
                                        ("path", string(path)),
                                        ("contentSha256", string(content_sha256)),
                                    ]),
                                    Declarer::Array { source, path } => json(vec![
                                        ("source", string(source.as_str())),
                                        ("path", string(path)),
                                    ]),
                                })
                                .collect();
                            json(vec![
                                ("path", string(&m.path)),
                                ("declaredBy", V::Array(by)),
                            ])
                        })
                        .collect(),
                ),
            ),
            ("declarations", rows(declarations)),
            (
                "links",
                V::Array(
                    links
                        .iter()
                        .map(|l| {
                            let mut pairs = vec![
                                ("ecosystem", string(l.ecosystem)),
                                ("packageName", string(&l.package_name)),
                                ("providerMember", string(&l.provider_member)),
                                ("packageDir", string(&l.package_dir)),
                                ("providedVersion", string(&l.provided_version)),
                                ("declaredBy", string(l.declared_by)),
                            ];
                            if let Some(source) = &l.cargo_patch_source {
                                pairs.push(("cargoPatchSource", string(source)));
                            }
                            json(pairs)
                        })
                        .collect(),
                ),
            ),
        ]),
        Decision::Refuse {
            refusal,
            path,
            detail,
            declarations,
        } => json(vec![
            ("kind", string("refuse")),
            ("code", string(refusal.code())),
            ("path", string(path)),
            ("detail", string(detail)),
            ("declarations", rows(declarations)),
        ]),
        Decision::TrialRefused { declarations } => json(vec![
            ("kind", string("trial-refused")),
            ("declarations", rows(declarations)),
        ]),
    }
}

/// One case through both phases; its outcome and what it touched.
fn run(case: &V, probe: Option<String>) -> (V, BTreeSet<String>, BTreeSet<String>) {
    let observation = field(case, "observation");
    let facts = field(case, "facts");
    let mut obs = Synthetic {
        fs: object(field(observation, "fs")),
        contents: object(field(observation, "contents")),
        markers: object(field(observation, "vcsMarkers")),
        observations: object(field(observation, "memberObservations")),
        consulted: BTreeSet::new(),
        read: BTreeSet::new(),
        probe,
    };
    let groups: BTreeSet<u32> = items(field(facts, "groups"))
        .iter()
        .map(|g| u32::try_from(int(g)).unwrap())
        .collect();
    let root = text(field(facts, "root"));
    let waiver = ProjectOwnerWaiver::from_invocation(
        matches!(field(facts, "waive"), V::Bool(true)),
        Some(Path::new(root)),
    )
    .unwrap();
    let array: Vec<String> = items(field(facts, "array"))
        .iter()
        .map(|s| text(s).to_owned())
        .collect();
    let inputs = DecisionInputs {
        invoking_uid: u32::try_from(int(field(facts, "uid"))).unwrap(),
        groups: &groups,
        waiver: waiver.as_ref(),
        no_repository: matches!(field(facts, "w2"), V::Bool(true)),
        array: &array,
        array_source: if text(field(facts, "arraySource")) == "explicit-joins" {
            ArraySource::ExplicitJoins
        } else {
            ArraySource::ConfigWorkspaceRoots
        },
    };
    let Ok(first) = phase_one(&mut obs, &inputs);
    let outcome = match first {
        PhaseOne::Decided(d) => {
            assert_eq!(
                field(case, "trial"),
                &V::Null,
                "{}",
                text(field(case, "id"))
            );
            d
        }
        PhaseOne::Trial(trial) => {
            let expected = field(case, "trial");
            let provisional: Vec<V> = trial.provisional().iter().map(|p| string(p)).collect();
            assert_eq!(
                &V::Array(provisional),
                field(expected, "provisional"),
                "{}",
                text(field(case, "id"))
            );
            let Ok(d) = phase_two(&mut obs, trial, text(field(expected, "status")) == "ACCEPT");
            d
        }
    };
    (decision(&outcome), obs.consulted, obs.read)
}

fn paths(value: &V) -> BTreeSet<String> {
    items(value).iter().map(|p| text(p).to_owned()).collect()
}

#[test]
fn every_reference_case_and_parser_control_is_reproduced_within_the_references_access() {
    let body = parse_json(VECTORS).unwrap();
    let cases = items(field(&body, "cases"));
    assert_eq!(cases.len(), 146);
    assert_eq!(items(field(&body, "noSelectedRoot")).len(), 20);
    let (mut controls, mut forbidden) = (0, 0);
    for case in cases {
        let id = text(field(case, "id"));
        let (got, consulted, read) = run(case, None);
        assert_eq!(&got, field(case, "expected"), "{id}");
        let (reference_consulted, reference_read) =
            (paths(field(case, "consulted")), paths(field(case, "read")));
        let extra: Vec<&String> = consulted.difference(&reference_consulted).collect();
        assert!(
            extra.is_empty(),
            "{id}: the core looked up {extra:?}, which the reference never did"
        );
        let extra: Vec<&String> = read.difference(&reference_read).collect();
        assert!(
            extra.is_empty(),
            "{id}: the core read {extra:?}, which the reference never did"
        );
        let banned = paths(field(case, "forbidden"));
        forbidden += usize::from(!banned.is_empty());
        let touched: Vec<&String> = banned
            .iter()
            .filter(|p| consulted.contains(*p) || read.contains(*p))
            .collect();
        assert!(
            touched.is_empty(),
            "{id}: the core touched forbidden {touched:?}"
        );
        controls += usize::from(id.starts_with("control:"));
    }
    assert_eq!((controls, forbidden), (30, 9));
}

#[test]
fn a_forbidden_lookup_is_caught_even_when_no_output_changes() {
    // The checker's pruned-anchor case: a lookup of a path below a member's
    // SX-1 anchor, made and discarded, changes nothing the core returns.
    let body = parse_json(VECTORS).unwrap();
    let case = items(field(&body, "cases"))
        .iter()
        .find(|c| text(field(c, "id")) == "rf1-npm-anchors-never-read")
        .unwrap();
    let banned = paths(field(case, "forbidden"));
    let probe = banned.iter().next().unwrap().clone();
    let (got, consulted, _) = run(case, Some(probe.clone()));
    assert_eq!(&got, field(case, "expected"), "the output does not change");
    assert!(
        consulted.contains(&probe),
        "the forbidden lookup is recorded"
    );
    assert!(!paths(field(case, "consulted")).contains(&probe));
}

#[test]
fn toml_resource_bounds_are_the_existing_parse_disposition_where_tomllib_reads() {
    let body = parse_json(VECTORS).unwrap();
    let toml: Vec<&V> = items(field(&body, "cases"))
        .iter()
        .filter(|c| text(field(c, "id")).starts_with("control:toml-"))
        .collect();
    assert_eq!(toml.len(), 4);
    for case in toml {
        let id = text(field(case, "id"));
        let reference = field(case, "referenceExpected");
        assert_ne!(reference, field(case, "expected"), "{id}: tomllib reads it");
        let (got, _, _) = run(case, None);
        assert_eq!(&got, field(case, "expected"), "{id}");
    }
    // The bounds themselves: parse_toml's recursion and node limits.
    let deep = format!("[x]\ny = {}{}\n", "[".repeat(128), "]".repeat(128));
    assert!(matches!(
        parse_toml(deep.as_bytes()),
        Err(opensip_identity::TomlError::RecursionLimit)
    ));
    let wide = format!("[x]\ny = [{}1]\n", "1,".repeat(1_100_000));
    assert!(matches!(
        parse_toml(wide.as_bytes()),
        Err(opensip_identity::TomlError::NodeLimit)
    ));
}
