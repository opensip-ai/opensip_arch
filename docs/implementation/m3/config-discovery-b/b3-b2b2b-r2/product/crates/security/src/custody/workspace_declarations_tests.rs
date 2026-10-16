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
/// `markers` as `_markers` consults), every listing and every read.
struct Synthetic<'v> {
    fs: &'v BTreeMap<String, V>,
    contents: &'v BTreeMap<String, V>,
    markers: &'v BTreeMap<String, V>,
    observations: &'v BTreeMap<String, V>,
    consulted: BTreeSet<String>,
    read: BTreeSet<String>,
    /// Every directory listed (r2, Codex B3B2B1-R1-RF-3).
    listed: BTreeSet<String>,
    /// A forbidden lookup to make before anything else (the mutation
    /// control's seam): it must be caught, changing no output.
    probe: Option<String>,
    /// Item 6b's verdicts a control substitutes, by candidate.
    verdicts: BTreeMap<String, Option<String>>,
    /// Once armed, observing this candidate's directory or its 6b verdict is
    /// an observation error: the short-circuit control's tripwire.
    tripwire: Option<String>,
    armed: bool,
}
/// The tripwire, as an observation error.
#[derive(Debug, PartialEq, Eq)]
struct Tripped(String);
impl Synthetic<'_> {
    fn trip(&self, rel: &str) -> Result<(), Tripped> {
        match &self.tripwire {
            Some(wire) if self.armed && wire == rel => Err(Tripped(rel.to_owned())),
            _ => Ok(()),
        }
    }
}
impl WorkspaceObservation for Synthetic<'_> {
    type Error = Tripped;
    fn entry(&mut self, rel: &str) -> Result<Option<ObservedEntry>, Self::Error> {
        self.trip(rel)?;
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
                let path = join(rel, name);
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
        self.listed.insert(rel.to_owned());
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
    fn custody_entry(
        &mut self,
        rel: &str,
        _object: ProjectObject,
    ) -> Result<Option<ObservedEntry>, Self::Error> {
        self.entry(rel)
    }
    fn member_verdict(&mut self, candidate: &str) -> Result<MemberOutcome, Self::Error> {
        self.trip(candidate)?;
        let refused = match self.verdicts.get(candidate) {
            Some(verdict) => verdict.clone(),
            None => match self.observations.get(candidate) {
                Some(V::String(v)) if v != "admitted" => Some(v.clone()),
                _ => None,
            },
        };
        Ok(refused.map_or(
            MemberOutcome::Admitted {
                gitlinks: Vec::new(),
            },
            MemberOutcome::Refused,
        ))
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
            ..
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

/// What one run returned and touched.
struct Ran {
    outcome: Result<V, Tripped>,
    consulted: BTreeSet<String>,
    read: BTreeSet<String>,
    listed: BTreeSet<String>,
}

/// A control's changes to a case's observation.
#[derive(Default)]
struct Control {
    probe: Option<String>,
    verdicts: BTreeMap<String, Option<String>>,
    tripwire: Option<String>,
}

/// One case through both phases; its outcome and what it touched.
fn run(case: &V, control: Control) -> Ran {
    let observation = field(case, "observation");
    let facts = field(case, "facts");
    let mut obs = Synthetic {
        fs: object(field(observation, "fs")),
        contents: object(field(observation, "contents")),
        markers: object(field(observation, "vcsMarkers")),
        observations: object(field(observation, "memberObservations")),
        consulted: BTreeSet::new(),
        read: BTreeSet::new(),
        listed: BTreeSet::new(),
        probe: control.probe,
        verdicts: control.verdicts,
        tripwire: control.tripwire,
        armed: false,
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
    let outcome = phase_one(&mut obs, &inputs).and_then(|first| match first {
        PhaseOne::Decided(d) => {
            assert_eq!(
                field(case, "trial"),
                &V::Null,
                "{}",
                text(field(case, "id"))
            );
            Ok(d)
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
            obs.armed = true;
            phase_two(&mut obs, trial, text(field(expected, "status")) == "ACCEPT")
        }
    });
    Ran {
        outcome: outcome.map(|d| decision(&d)),
        consulted: obs.consulted,
        read: obs.read,
        listed: obs.listed,
    }
}

fn paths(value: &V) -> BTreeSet<String> {
    items(value).iter().map(|p| text(p).to_owned()).collect()
}
fn cases(body: &V) -> &[V] {
    items(field(body, "cases"))
}
fn case<'v>(body: &'v V, id: &str) -> &'v V {
    cases(body)
        .iter()
        .find(|c| text(field(c, "id")) == id)
        .unwrap()
}

#[test]
fn every_reference_case_and_parser_control_is_reproduced_within_the_references_access() {
    let body = parse_json(VECTORS).unwrap();
    assert_eq!(cases(&body).len(), 154);
    assert_eq!(items(field(&body, "noSelectedRoot")).len(), 20);
    let (mut controls, mut forbidden, mut listing) = (0, 0, 0);
    for case in cases(&body) {
        let id = text(field(case, "id"));
        let ran = run(case, Control::default());
        assert_eq!(ran.outcome.as_ref(), Ok(field(case, "expected")), "{id}");
        for (what, mine, theirs) in [
            ("looked up", &ran.consulted, paths(field(case, "consulted"))),
            ("read", &ran.read, paths(field(case, "read"))),
            ("listed", &ran.listed, paths(field(case, "listed"))),
        ] {
            let extra: Vec<&String> = mine.difference(&theirs).collect();
            assert!(
                extra.is_empty(),
                "{id}: the core {what} {extra:?}, which the reference never did"
            );
        }
        let banned = paths(field(case, "forbidden"));
        forbidden += usize::from(!banned.is_empty());
        listing += usize::from(!ran.listed.is_empty());
        let touched: Vec<&String> = banned
            .iter()
            .filter(|p| {
                ran.consulted.contains(*p) || ran.read.contains(*p) || ran.listed.contains(*p)
            })
            .collect();
        assert!(
            touched.is_empty(),
            "{id}: the core touched forbidden {touched:?}"
        );
        controls += usize::from(id.starts_with("control:"));
    }
    assert_eq!((controls, forbidden, listing), (38, 9, 8));
}

#[test]
fn a_forbidden_lookup_is_caught_even_when_no_output_changes() {
    // The checker's pruned-anchor case: a lookup of a path below a member's
    // SX-1 anchor, made and discarded, changes nothing the core returns.
    let body = parse_json(VECTORS).unwrap();
    let case = case(&body, "rf1-npm-anchors-never-read");
    let probe = paths(field(case, "forbidden")).into_iter().next().unwrap();
    let ran = run(
        case,
        Control {
            probe: Some(probe.clone()),
            ..Control::default()
        },
    );
    assert_eq!(
        ran.outcome.as_ref(),
        Ok(field(case, "expected")),
        "the output does not change"
    );
    assert!(
        ran.consulted.contains(&probe),
        "the forbidden lookup is recorded"
    );
    assert!(!paths(field(case, "consulted")).contains(&probe));
}

#[test]
fn branch_a_stops_at_the_first_refusal_in_path_order_and_observes_no_later_member() {
    // r2 (Codex B3B2B1-R1-RF-2): members `a` and `b` (array `b`, `a`). Item
    // 6b refuses `a`; observing `b`'s directory or its 6b verdict would be an
    // error. The decision is `a`'s refusal, and `b` is never observed.
    let body = parse_json(VECTORS).unwrap();
    let case = case(
        &body,
        "rf2-configWorkspaceRoots-member-decisions-in-path-order",
    );
    let subject = "member-vcs-unsupported:index-split-or-sparse".to_owned();
    let ran = run(
        case,
        Control {
            verdicts: BTreeMap::from([("a".to_owned(), Some(subject.clone()))]),
            tripwire: Some("b".to_owned()),
            ..Control::default()
        },
    );
    let outcome = ran.outcome.expect("b is never observed after a refuses");
    assert_eq!(field(&outcome, "kind"), &string("refuse"));
    assert_eq!(field(&outcome, "path"), &string("a"));
    assert_eq!(field(&outcome, "detail"), &string(&subject));
    // Without the substitution, `a` is admitted and `b` is observed: the
    // tripwire fires, so the control is live.
    let ran = run(
        case,
        Control {
            tripwire: Some("b".to_owned()),
            ..Control::default()
        },
    );
    assert_eq!(ran.outcome, Err(Tripped("b".to_owned())));
}

#[test]
fn toml_resource_bounds_are_the_existing_parse_disposition_where_tomllib_reads() {
    let body = parse_json(VECTORS).unwrap();
    let toml: Vec<&V> = cases(&body)
        .iter()
        .filter(|c| {
            text(field(c, "id")).starts_with("control:toml-")
                && field(c, "referenceExpected") != &V::Null
        })
        .collect();
    assert_eq!(toml.len(), 4);
    for case in toml {
        let id = text(field(case, "id"));
        assert_ne!(
            field(case, "referenceExpected"),
            field(case, "expected"),
            "{id}: tomllib reads it"
        );
        let ran = run(case, Control::default());
        assert_eq!(ran.outcome.as_ref(), Ok(field(case, "expected")), "{id}");
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

#[test]
fn colliding_cargo_entries_keep_the_first_in_document_order() {
    // r2 (Codex B3B2B1-R1-RF-1): `[patch."a.b"] c` and `[patch.a] "b.c"` are
    // both `patch.a.b.c`; the first defined wins, in either document order.
    let body = parse_json(VECTORS).unwrap();
    for (id, member) in [
        ("control:toml-collision-dotted-source-first", "repos/x"),
        ("control:toml-collision-dotted-name-first", "repos/y"),
    ] {
        let case = case(&body, id);
        let ran = run(case, Control::default());
        let outcome = ran.outcome.unwrap();
        assert_eq!(&outcome, field(case, "expected"), "{id}");
        let members: Vec<&str> = items(field(&outcome, "members"))
            .iter()
            .map(|m| text(field(m, "path")))
            .collect();
        assert_eq!(members, vec![member], "{id}");
    }
}
