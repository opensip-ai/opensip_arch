// M3-B r5 item 13 (unit B2-b2): the pure discovery core. The downward half of
// S3 discovery over an observed scope, exactly as the current discovery
// reference (B2-b0, contract successor 164) computes it: nested repositories
// and projects, the exclusive unit-source choice, exact explicit roots with
// every `JOIN_*` refusal, automatic enumeration through the shared rule,
// exclusions in their fixed order, the post-exclusion cap, and per-object
// custody through `check_project_object_waived`. The scope is what the walker
// (B2-b3) observed; this module reads nothing. Its records are version 3 with
// `workspaceDeclarations` pending B3-b's readers: the pending provenance has
// no serializer and no completion here, while the boundary inventory is
// complete. No public row is mapped here.
use super::discovery_rule::{
    self as rule, EnumerationInput, MarkerCountBasis, PruneReason, WORKSPACE_MARKERS,
};
use super::project_chain::{CustodyOrder, ProjectObject, check_project_object_ordered};
use crate::grants::{AuthorizedGroups, ProjectOwnerWaiver};
use opensip_identity::{JsonInteger, JsonValue};
use opensip_platform::{CapturedAclEntry, CapturedAclState, DescriptorMetadata};
use std::collections::{BTreeMap, BTreeSet};

/// S3's unit and walk depth bound (`MAX_WALK_DEPTH`).
const MAX_UNIT_DEPTH: usize = 256;

/// An object's ACL as the walker normalized it: readable entries (an
/// omission the premise admits is an empty list), or unreadable. An entry
/// the walker never opened carries `NotObserved` (M3-B unit B2-b3b,
/// LD-B2B3-3): an honest uncaptured state, never an empty list.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ObservedAcl {
    Entries(Vec<CapturedAclEntry>),
    Unreadable,
    NotObserved,
}

/// The walker handed the core an entry whose judgment reached its ACL
/// without capturing it (LD-B2B3-3): an instrument invariant fault, never a
/// public reason. It names the first such object.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UnobservedAcl {
    pub(crate) path: String,
}

/// VCS evidence the walker observed inside a probed directory.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ObservedVcs {
    Directory,
    Indirection { target: Option<String> },
}

/// One observed entry: its own status sample, ACL and, for a probed
/// directory, its VCS evidence.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ObservedEntry {
    pub(crate) metadata: DescriptorMetadata,
    pub(crate) acl: ObservedAcl,
    pub(crate) vcs: Option<ObservedVcs>,
}
impl ObservedEntry {
    fn is_dir(&self) -> bool {
        self.metadata.mode & 0o170000 == 0o040000
    }
    fn is_file(&self) -> bool {
        self.metadata.mode & 0o170000 == 0o100000
    }
}

/// What the walker observed, keyed by root-relative path: the root is `""`,
/// a descendant `a/b` (M3-B r6 item 12, unit B2-b3d). Every record path the
/// core reports is still absolute, spelled under the root it is given.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub(crate) struct ObservedScope {
    pub(crate) entries: BTreeMap<String, ObservedEntry>,
}

/// One upward walk row, as selection recorded it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct WalkRow {
    pub(crate) path: String,
    pub(crate) custody: String,
    pub(crate) candidate: String,
    pub(crate) boundary: Option<String>,
}

/// The provenance `vcs` record.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct VcsRecord {
    pub(crate) kind: &'static str,
    pub(crate) target: Option<String>,
}

/// What selection (X2b, extended by B2-b3) recorded: the upward provenance.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UpwardProvenance {
    pub(crate) mode: String,
    pub(crate) config_path: Option<String>,
    pub(crate) walked: Vec<WalkRow>,
    pub(crate) stop_reason: String,
    pub(crate) vcs: Option<VcsRecord>,
    pub(crate) explicit_path_was_symlink: Option<bool>,
}

/// The unit source, chosen before traversal (plan r4 LD-B2B-8).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum UnitSourceRequest {
    ExplicitJoins(Vec<String>),
    ConfigWorkspaceRoots(Vec<String>),
    Automatic,
}

/// The invocation facts the downward half consumes.
pub(crate) struct DiscoveryInvocation<'a> {
    pub(crate) invoking_uid: u32,
    pub(crate) ci: bool,
    pub(crate) groups: &'a AuthorizedGroups,
    /// `--trust-project-owner` with its explicit `--project` (B3-a).
    pub(crate) waiver: Option<&'a ProjectOwnerWaiver>,
    pub(crate) source: UnitSourceRequest,
    pub(crate) basis: MarkerCountBasis,
    /// Admitted D15 member roots; empty until B3-b.
    pub(crate) member_roots: &'a BTreeSet<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UnitRecord {
    pub(crate) path: String,
    pub(crate) kind: &'static str,
    pub(crate) markers: Vec<&'static str>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ExcludedUnit {
    pub(crate) path: String,
    pub(crate) reason: String,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct PrunedTree {
    pub(crate) path: String,
    pub(crate) reason: PruneReason,
    pub(crate) marker_count: Option<u64>,
    pub(crate) basis: MarkerCountBasis,
}

/// `DiscoveryProvenanceV3` without `workspaceDeclarations`, which only B3-b's
/// readers observe. It has no serializer and no completion in this module:
/// it cannot be emitted or accepted as current provenance (plan r4 LD-B2B-3).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct DiscoveryProvenancePending {
    pub(crate) upward: UpwardProvenance,
    pub(crate) ci: bool,
    pub(crate) selected_root: String,
    pub(crate) custody_waiver: Option<&'static str>,
    pub(crate) authorized_group_ids: Vec<u32>,
    pub(crate) nested_repositories: Vec<String>,
    pub(crate) nested_projects: Vec<String>,
    pub(crate) unit_source: &'static str,
    pub(crate) units: Vec<UnitRecord>,
    pub(crate) excluded_units: Vec<ExcludedUnit>,
    pub(crate) pruned_trees: Vec<PrunedTree>,
    pub(crate) warnings: Vec<String>,
    /// Empty until B3-b admits members.
    pub(crate) member_repositories: Vec<String>,
    pub(crate) member_configs: Vec<String>,
}

/// The D9 branch of a discovery refusal (`DiscoveryD9V1`; SLM `D9`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct DiscoveryD9 {
    pub(crate) class: &'static str,
    pub(crate) exit: u8,
    pub(crate) code: &'static str,
}

/// A discovery refusal code (`DiscoveryResultV3.refusal`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum DiscoveryRefusal {
    RootCustodyRefused,
    ExplicitPathInvalid,
    WorkspaceUnitLimit,
    /// Selection's configuration custody (SLM's upward refusal; unit B2-b3a).
    ConfigCustodyRefused,
}
impl DiscoveryRefusal {
    pub(crate) fn code(self) -> &'static str {
        match self {
            Self::RootCustodyRefused => "PROJECT.ROOT_CUSTODY_REFUSED",
            Self::ExplicitPathInvalid => "PROJECT.EXPLICIT_PATH_INVALID",
            Self::WorkspaceUnitLimit => "PROJECT.WORKSPACE_UNIT_LIMIT",
            Self::ConfigCustodyRefused => "CONFIG.CUSTODY_REFUSED",
        }
    }
    pub(crate) fn d9(self) -> DiscoveryD9 {
        let code = match self {
            Self::WorkspaceUnitLimit => "REQUEST.UNSATISFIABLE",
            Self::RootCustodyRefused | Self::ExplicitPathInvalid | Self::ConfigCustodyRefused => {
                "CONFIG.INVALID"
            }
        };
        DiscoveryD9 {
            class: "request-rejected",
            exit: 2,
            code,
        }
    }
}

/// `DiscoveryResultV3` with pending provenance.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum DiscoveryResultPending {
    Accept(DiscoveryProvenancePending),
    Refuse {
        refusal: DiscoveryRefusal,
        path: Option<String>,
        detail: String,
        provenance: DiscoveryProvenancePending,
    },
}

/// `AdmittedBoundaryInventoryV3`: complete, with members empty until B3-b.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct BoundaryInventory {
    pub(crate) selected_root: String,
    pub(crate) nested_repositories: Vec<String>,
    pub(crate) nested_projects: Vec<String>,
    pub(crate) custody_excluded_units: Vec<ExcludedUnit>,
    pub(crate) pruned_trees: Vec<PrunedTree>,
    pub(crate) member_repositories: Vec<String>,
}

impl BoundaryInventory {
    /// The closed `AdmittedBoundaryInventoryV3` record. Lists are already in
    /// their schema order.
    pub(crate) fn to_json(&self) -> JsonValue {
        let strings = |items: &[String]| {
            JsonValue::Array(items.iter().cloned().map(JsonValue::String).collect())
        };
        let object = |pairs: Vec<(&str, JsonValue)>| {
            JsonValue::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
        };
        let integer =
            |n: u64| JsonInteger::new(n as i128).map_or(JsonValue::Null, JsonValue::Integer);
        object(vec![
            ("schemaVersion", integer(3)),
            ("source", JsonValue::String("security.discovery".to_owned())),
            (
                "selectedRoot",
                JsonValue::String(self.selected_root.clone()),
            ),
            ("nestedRepositories", strings(&self.nested_repositories)),
            ("nestedProjects", strings(&self.nested_projects)),
            (
                "custodyExcludedUnits",
                JsonValue::Array(
                    self.custody_excluded_units
                        .iter()
                        .map(|r| {
                            object(vec![
                                ("path", JsonValue::String(r.path.clone())),
                                ("reason", JsonValue::String(r.reason.clone())),
                            ])
                        })
                        .collect(),
                ),
            ),
            (
                "prunedTrees",
                JsonValue::Array(
                    self.pruned_trees
                        .iter()
                        .map(|t| {
                            object(vec![
                                ("path", JsonValue::String(t.path.clone())),
                                ("reason", JsonValue::String(t.reason.as_str().to_owned())),
                                (
                                    "markerCount",
                                    t.marker_count.map_or(JsonValue::Null, integer),
                                ),
                                (
                                    "markerCountBasis",
                                    JsonValue::String(t.basis.as_str().to_owned()),
                                ),
                            ])
                        })
                        .collect(),
                ),
            ),
            ("memberRepositories", strings(&self.member_repositories)),
        ])
    }
}

/// A boundary inventory needs an accepted result whose locators lie under its
/// root; anything else is an instrument fault, never a public row.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum InventoryRefusal {
    NotAccepted,
    Locator(rule::LocatorRefusal),
}

fn join(dir: &str, name: &str) -> String {
    if dir == "/" {
        format!("/{name}")
    } else {
        format!("{dir}/{name}")
    }
}
/// A root-relative path's absolute spelling under `root` (unit B2-b3d).
fn spelled(root: &str, rel: &str) -> String {
    if rel.is_empty() {
        root.to_owned()
    } else {
        join(root, rel)
    }
}
fn join_rel(rel: &str, name: &str) -> String {
    if rel.is_empty() {
        name.to_owned()
    } else {
        format!("{rel}/{name}")
    }
}
/// A root-relative path's parent ("" for a top-level entry).
fn parent_rel(rel: &str) -> &str {
    rel.rfind('/').map_or("", |i| &rel[..i])
}

/// SLM `_dir_custody` / `_file_custody` order (r2, Codex B2B2-1): kind,
/// owner, mode and the real ACL first, then a file's link count and size
/// (`CustodyOrder::Reference`; moved to the chain module by B2-b3a, which
/// judges the upward configuration file in the same order).
fn reference_order(
    metadata: &DescriptorMetadata,
    state: CapturedAclState,
    entries: &[CapturedAclEntry],
    invoking_uid: u32,
    groups: &BTreeSet<u32>,
    object: ProjectObject,
    waiver: Option<&ProjectOwnerWaiver>,
) -> Result<(), super::Refusal> {
    check_project_object_ordered(
        metadata,
        state,
        |i| entries.get(i).copied(),
        invoking_uid,
        groups,
        object,
        waiver,
        CustodyOrder::Reference,
    )
}

struct Judge<'s, 'a> {
    scope: &'s ObservedScope,
    inv: &'s DiscoveryInvocation<'a>,
    /// The root's spelling, for the paths the core reports.
    root: &'s str,
    /// The first entry whose judgment reached an uncaptured ACL.
    unobserved: std::cell::RefCell<Option<String>>,
}
/// One entry's custody, as far as its observation goes (M3-B unit B2-b3b,
/// LD-B2B3-3; r2, Codex B2B3B-R1-RF-1): the core and the walker judge with
/// this one function, so the walker captures an ACL exactly where the core's
/// judgment would need it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum EntryJudgment {
    Passed,
    Refused(super::Refusal),
    /// The metadata-only rejection (kind, owner, mode) passed, and the
    /// judgment needs an ACL that was never captured.
    NeedsAcl,
}
/// SLM `_dir_custody` / `_file_custody` through the product's judge, in the
/// reference order. An absent entry is `ABSENT`. An entry carrying
/// `NotObserved` is judged by the metadata-only early rejection: its kind,
/// owner and mode, with an empty ACL, one link and no size standing in;
/// if that passes, the judgment needs the ACL.
pub(crate) fn judge_entry(
    entry: Option<&ObservedEntry>,
    object: ProjectObject,
    invoking_uid: u32,
    groups: &BTreeSet<u32>,
    waiver: Option<&ProjectOwnerWaiver>,
) -> EntryJudgment {
    let Some(e) = entry else {
        return EntryJudgment::Refused(super::Refusal::Absent);
    };
    let result = match &e.acl {
        ObservedAcl::NotObserved => {
            let metadata_only = DescriptorMetadata {
                links: 1,
                size: 0,
                ..e.metadata.clone()
            };
            match check_project_object_ordered(
                &metadata_only,
                CapturedAclState::Entries(0),
                |_| None,
                invoking_uid,
                groups,
                object,
                waiver,
                CustodyOrder::Reference,
            ) {
                Ok(()) => return EntryJudgment::NeedsAcl,
                Err(refusal) => Err(refusal),
            }
        }
        ObservedAcl::Entries(list) => reference_order(
            &e.metadata,
            CapturedAclState::Entries(list.len()),
            list,
            invoking_uid,
            groups,
            object,
            waiver,
        ),
        ObservedAcl::Unreadable => reference_order(
            &e.metadata,
            CapturedAclState::NotReturned,
            &[],
            invoking_uid,
            groups,
            object,
            waiver,
        ),
    };
    match result {
        Ok(()) => EntryJudgment::Passed,
        Err(refusal) => EntryJudgment::Refused(refusal),
    }
}

impl Judge<'_, '_> {
    /// `judge_entry` over the scope, for the root-relative `rel`. A judgment
    /// that needs an uncaptured ACL is recorded, spelled under the root, as
    /// the instrument fault (`discover_observed`).
    fn custody(&self, rel: &str, object: ProjectObject, waive: bool) -> Option<&'static str> {
        let judged = judge_entry(
            self.scope.entries.get(rel),
            object,
            self.inv.invoking_uid,
            self.inv.groups.as_set(),
            if waive { self.inv.waiver } else { None },
        );
        match judged {
            EntryJudgment::Passed => None,
            EntryJudgment::Refused(refusal) => Some(refusal.code()),
            EntryJudgment::NeedsAcl => {
                self.unobserved
                    .borrow_mut()
                    .get_or_insert_with(|| spelled(self.root, rel));
                Some(super::Refusal::AclUnreadable.code())
            }
        }
    }
    fn dir_custody(&self, rel: &str) -> Option<&'static str> {
        self.custody(rel, ProjectObject::Directory, true)
    }
    /// Markers present in the root-relative `dir` and passing file custody,
    /// and those failing it (`<marker>:<why>`). Markers are never waived.
    fn markers(&self, dir: &str) -> (Vec<&'static str>, Vec<String>) {
        let (mut found, mut bad) = (Vec::new(), Vec::new());
        for marker in WORKSPACE_MARKERS {
            let path = join_rel(dir, marker);
            if !self.scope.entries.contains_key(&path) {
                continue;
            }
            match self.custody(&path, ProjectObject::ConfigurationFile, false) {
                None => found.push(marker),
                Some(why) => bad.push(format!("{marker}:{why}")),
            }
        }
        (found, bad)
    }
    /// Every directory from the root to the unit passes directory custody.
    /// The refusing directory is reported spelled under the root.
    fn unit_custody(&self, root: &str, rel: &str) -> Option<(String, &'static str)> {
        if rel.is_empty() {
            return self.dir_custody("").map(|why| (root.to_owned(), why));
        }
        let parts: Vec<&str> = rel.split('/').collect();
        (1..=parts.len()).find_map(|i| {
            let sub = parts[..i].join("/");
            self.dir_custody(&sub).map(|why| (join(root, &sub), why))
        })
    }
}

/// S3's downward discovery from the selected root (SLM `finish`), over the
/// observed scope. For a scope with uncaptured ACLs use `discover_observed`:
/// here a judgment that reaches one reports `ACL_UNREADABLE`.
pub(crate) fn discover(
    scope: &ObservedScope,
    root: &str,
    upward: UpwardProvenance,
    inv: &DiscoveryInvocation<'_>,
) -> DiscoveryResultPending {
    let judge = Judge {
        scope,
        inv,
        root,
        unobserved: std::cell::RefCell::new(None),
    };
    run(&judge, root, upward)
}

/// `discover` over a walker's scope (M3-B unit B2-b3b, LD-B2B3-3): entries
/// the walker never opened carry `NotObserved`, and a judgment that reaches
/// one's ACL is the instrument fault `UnobservedAcl`, never a result.
pub(crate) fn discover_observed(
    scope: &ObservedScope,
    root: &str,
    upward: UpwardProvenance,
    inv: &DiscoveryInvocation<'_>,
) -> Result<DiscoveryResultPending, UnobservedAcl> {
    let judge = Judge {
        scope,
        inv,
        root,
        unobserved: std::cell::RefCell::new(None),
    };
    let result = run(&judge, root, upward);
    match judge.unobserved.into_inner() {
        Some(path) => Err(UnobservedAcl { path }),
        None => Ok(result),
    }
}

fn run(judge: &Judge<'_, '_>, root: &str, upward: UpwardProvenance) -> DiscoveryResultPending {
    let (scope, inv) = (judge.scope, judge.inv);
    let mut prov = DiscoveryProvenancePending {
        upward,
        ci: inv.ci,
        selected_root: root.to_owned(),
        custody_waiver: inv.waiver.map(|_| "trustProjectOwner"),
        authorized_group_ids: inv.groups.as_set().iter().copied().collect(),
        nested_repositories: Vec::new(),
        nested_projects: Vec::new(),
        unit_source: "automatic",
        units: Vec::new(),
        excluded_units: Vec::new(),
        pruned_trees: Vec::new(),
        warnings: Vec::new(),
        member_repositories: Vec::new(),
        member_configs: Vec::new(),
    };
    // Nested repositories: recorded, never entered.
    for (rel, entry) in &scope.entries {
        if !rel.is_empty() && entry.is_dir() && entry.vcs.is_some() {
            prov.nested_repositories.push(spelled(root, rel));
        }
    }
    let relative = |pred: &dyn Fn(&str, &ObservedEntry) -> bool| -> Vec<String> {
        scope
            .entries
            .iter()
            .filter(|(p, e)| !p.is_empty() && pred(p, e))
            .map(|(p, _)| p.clone())
            .collect()
    };
    let marker_paths = relative(&|p, e| {
        e.is_file() && WORKSPACE_MARKERS.contains(&p.rsplit('/').next().unwrap_or(""))
    });
    let cargo_roots = rule::cargo_roots_from_markers(&marker_paths, inv.member_roots);
    // Nested projects: a nested `opensip.json`, outside nested repositories
    // and pruned trees.
    for (rel, entry) in &scope.entries {
        if rel != "opensip.json"
            && !rel.is_empty()
            && rel.rsplit('/').next() == Some("opensip.json")
            && entry.is_file()
        {
            let dir = spelled(root, parent_rel(rel));
            if rule::classify_boundary(&dir, &prov.nested_repositories, &[] as &[String]).is_some()
                || rule::classify_path(rel, &cargo_roots, inv.member_roots).is_some()
            {
                continue;
            }
            prov.nested_projects.push(dir);
        }
    }
    match &inv.source {
        UnitSourceRequest::ExplicitJoins(paths) => {
            prov.unit_source = "explicit-joins";
            explicit_units(
                judge,
                &mut prov,
                root,
                paths,
                "explicit-join",
                "TOO_MANY_JOINS",
                &cargo_roots,
            )
        }
        UnitSourceRequest::ConfigWorkspaceRoots(paths) => {
            prov.unit_source = "config-workspace-roots";
            explicit_units(
                judge,
                &mut prov,
                root,
                paths,
                "config-workspace-root",
                "TOO_MANY_WORKSPACE_ROOTS",
                &cargo_roots,
            )
        }
        UnitSourceRequest::Automatic => {
            prov.unit_source = "automatic";
            automatic_units(judge, &mut prov, root, &marker_paths, &cargo_roots)
        }
    }
    .map_or(
        DiscoveryResultPending::Accept(prov.clone()),
        |(refusal, path, detail)| DiscoveryResultPending::Refuse {
            refusal,
            path,
            detail,
            provenance: prov,
        },
    )
}

type Refused = (DiscoveryRefusal, Option<String>, String);

fn explicit_units(
    judge: &Judge<'_, '_>,
    prov: &mut DiscoveryProvenancePending,
    root: &str,
    paths: &[String],
    kind: &'static str,
    too_many: &str,
    cargo_roots: &BTreeSet<String>,
) -> Option<Refused> {
    use DiscoveryRefusal::{ExplicitPathInvalid, RootCustodyRefused};
    if paths.len() > rule::MAX_WORKSPACE_UNITS {
        return Some((ExplicitPathInvalid, None, too_many.to_owned()));
    }
    for spec in paths {
        let Ok(rel) = rule::normalize_explicit_root(spec) else {
            return Some((
                ExplicitPathInvalid,
                Some(spec.clone()),
                "JOIN_PATH_GRAMMAR".to_owned(),
            ));
        };
        let at = if rel.is_empty() {
            root.to_owned()
        } else {
            join(root, &rel)
        };
        if rule::classify_boundary(&at, &prov.nested_repositories, &[] as &[String]).is_some() {
            return Some((
                ExplicitPathInvalid,
                Some(at),
                "JOIN_CROSSES_NESTED_REPOSITORY".to_owned(),
            ));
        }
        if rule::classify_boundary(&at, &[] as &[String], &prov.nested_projects).is_some() {
            return Some((
                ExplicitPathInvalid,
                Some(at),
                "JOIN_CROSSES_NESTED_PROJECT".to_owned(),
            ));
        }
        if !rel.is_empty()
            && let Some(anchor) = rule::classify_path(&rel, cargo_roots, judge.inv.member_roots)
        {
            let detail = format!(
                "JOIN_INSIDE_PRUNED_TREE:{}:{}",
                anchor.reason.as_str(),
                anchor.path
            );
            return Some((ExplicitPathInvalid, Some(at), detail));
        }
        if let Some((sub, why)) = judge.unit_custody(root, &rel) {
            let refusal = if matches!(why, "ABSENT" | "NOT_A_DIRECTORY") {
                ExplicitPathInvalid
            } else {
                RootCustodyRefused
            };
            return Some((refusal, Some(sub), why.to_owned()));
        }
        let (markers, bad) = judge.markers(&rel);
        for b in bad {
            prov.excluded_units.push(ExcludedUnit {
                path: at.clone(),
                reason: format!("MARKER_CUSTODY:{b}"),
            });
        }
        if markers.is_empty() {
            prov.warnings
                .push(format!("EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER:{at}"));
        }
        prov.units.push(UnitRecord {
            path: at,
            kind,
            markers,
        });
    }
    None
}

fn automatic_units(
    judge: &Judge<'_, '_>,
    prov: &mut DiscoveryProvenancePending,
    root: &str,
    marker_paths: &[String],
    cargo_roots: &BTreeSet<String>,
) -> Option<Refused> {
    let scope = judge.scope;
    let directories: Vec<String> = scope
        .entries
        .iter()
        .filter(|(p, e)| !p.is_empty() && e.is_dir())
        .map(|(p, _)| p.clone())
        .collect();
    let unreadable: Vec<String> = scope
        .entries
        .iter()
        .filter(|(p, e)| !p.is_empty() && e.is_dir() && e.acl == ObservedAcl::Unreadable)
        .filter_map(|(p, _)| {
            let rel = p.as_str();
            rule::classify_path(rel, cargo_roots, &BTreeSet::new())
                .filter(|a| a.path == rel)
                .map(|a| a.path)
        })
        .collect();
    let enumeration = rule::enumerate_units(
        marker_paths,
        &EnumerationInput {
            enforce_limit: false,
            observed_directories: Some(&directories),
            basis: judge.inv.basis,
            unreadable_anchors: &unreadable,
            member_roots: judge.inv.member_roots,
        },
    );
    prov.pruned_trees = enumeration
        .pruned_trees
        .iter()
        .map(|t| PrunedTree {
            path: join(root, &t.anchor.path),
            reason: t.anchor.reason,
            marker_count: t.marker_count,
            basis: t.basis,
        })
        .collect();
    for rel in &enumeration.unit_dirs {
        let dir = if rel.is_empty() {
            root.to_owned()
        } else {
            join(root, rel)
        };
        if rule::classify_boundary(&dir, &prov.nested_repositories, &[] as &[String]).is_some() {
            prov.excluded_units.push(ExcludedUnit {
                path: dir,
                reason: "INSIDE_NESTED_REPOSITORY".to_owned(),
            });
            continue;
        }
        if rule::classify_boundary(&dir, &[] as &[String], &prov.nested_projects).is_some() {
            prov.excluded_units.push(ExcludedUnit {
                path: dir,
                reason: "INSIDE_NESTED_PROJECT".to_owned(),
            });
            continue;
        }
        if dir != root {
            if rel.split('/').count() > MAX_UNIT_DEPTH {
                prov.excluded_units.push(ExcludedUnit {
                    path: dir,
                    reason: "DEPTH".to_owned(),
                });
                continue;
            }
            if let Some((sub, why)) = judge.unit_custody(root, rel) {
                prov.excluded_units.push(ExcludedUnit {
                    path: sub,
                    reason: format!("DIRECTORY_CUSTODY:{why}"),
                });
                continue;
            }
        }
        let (markers, bad) = judge.markers(rel);
        for b in bad {
            prov.excluded_units.push(ExcludedUnit {
                path: dir.clone(),
                reason: format!("MARKER_CUSTODY:{b}"),
            });
        }
        if markers.is_empty() {
            continue;
        }
        prov.units.push(UnitRecord {
            path: dir,
            kind: "workspace-auto",
            markers,
        });
    }
    let count = prov.units.len();
    if count > rule::MAX_WORKSPACE_UNITS {
        prov.units.clear();
        return Some((
            DiscoveryRefusal::WorkspaceUnitLimit,
            Some(root.to_owned()),
            format!("WORKSPACE_UNIT_LIMIT:{count}>{}", rule::MAX_WORKSPACE_UNITS),
        ));
    }
    None
}

/// The complete `AdmittedBoundaryInventoryV3` of an accepted result (SLM
/// `boundary_inventory`; the bound reference's V3 converter).
pub(crate) fn boundary_inventory(
    result: &DiscoveryResultPending,
) -> Result<BoundaryInventory, InventoryRefusal> {
    let DiscoveryResultPending::Accept(prov) = result else {
        return Err(InventoryRefusal::NotAccepted);
    };
    let root = &prov.selected_root;
    let rel = |p: &str| rule::relative_locator(root, p).map_err(InventoryRefusal::Locator);
    let relative_set = |paths: &[String]| -> Result<Vec<String>, InventoryRefusal> {
        Ok(paths
            .iter()
            .map(|p| rel(p))
            .collect::<Result<BTreeSet<_>, _>>()?
            .into_iter()
            .collect())
    };
    let mut custody = Vec::new();
    for row in &prov.excluded_units {
        if row.reason.starts_with("INSIDE_NESTED_") {
            continue;
        }
        custody.push(ExcludedUnit {
            path: rel(&row.path)?,
            reason: row.reason.clone(),
        });
    }
    custody.sort_by(|a, b| (&a.path, &a.reason).cmp(&(&b.path, &b.reason)));
    let mut pruned = Vec::new();
    for t in &prov.pruned_trees {
        pruned.push(PrunedTree {
            path: rel(&t.path)?,
            ..t.clone()
        });
    }
    pruned.sort_by(|a, b| (&a.path, a.reason.as_str()).cmp(&(&b.path, b.reason.as_str())));
    Ok(BoundaryInventory {
        selected_root: root.clone(),
        nested_repositories: relative_set(&prov.nested_repositories)?,
        nested_projects: relative_set(&prov.nested_projects)?,
        custody_excluded_units: custody,
        pruned_trees: pruned,
        member_repositories: relative_set(&prov.member_repositories)?,
    })
}

#[cfg(test)]
mod tests {
    include!("discovery_scan_tests.rs");
}
