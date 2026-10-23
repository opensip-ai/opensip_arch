// The D15 discovery composition (M3-B r9 items 19 to 24; unit B3-b2b2b,
// B3-b plan r2 amendment A3): B3-b0's `discover` over the product's parts.
// The decision core (`workspace_declarations.rs`) decides over the native
// observation (`workspace_observation.rs`); the S3 walk and core
// (`discovery_walk.rs`, `discovery_scan.rs`, B3-b2a) observe W with the
// decided members entered as ordinary directories. The walk runs once. In
// branch A (r3, B3-b plan r2 amendment A4) the members are decided before
// it, so their index gitlinks bound every descent: the array gate, the
// member decisions, the walk, and only after an accepted walk the links. A
// member rule's or the gate's refusal carries the provenance of the walk
// without members (LD-B3B0-5). The result is the
// complete `DiscoveryResultV3`: `memberRepositories` rows with `declaredBy`,
// `memberConfigs` and `workspaceDeclarations`, spelled under W, the only
// emittable discovery record. The core's pending provenance is its partial,
// never emitted.
use super::discovery_scan::{
    DiscoveryD9, DiscoveryInvocation, DiscoveryProvenancePending, DiscoveryRefusal,
    DiscoveryResultPending, UnitSourceRequest, UpwardProvenance,
};
use super::discovery_walk::discover_downward_bound;
use super::project_chain::DiscoveryRoot;
use super::workspace_declarations::{
    ArraySource, Decision, DecisionInputs, DeclarationRow, Declarer, LinkRow, MemberRefusal,
    PhaseOne, links, phase_one,
};
use super::workspace_observation::{
    Bindings, Failure, MemberObservation, NativeObservation, WorkspaceRefusal, hook,
};
use opensip_identity::{JsonInteger, JsonValue};
use opensip_platform::{WorkFailure, WorkScope};
use std::collections::{BTreeMap, BTreeSet};

/// `DiscoveryProvenanceV3`, complete.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct DiscoveryProvenanceV3 {
    /// The walk and core's provenance; its `member_repositories` paths are
    /// superseded by `members`.
    pub(crate) core: DiscoveryProvenancePending,
    pub(crate) members: Vec<MemberRepositoryRow>,
    pub(crate) declarations: Vec<DeclarationRow>,
}

/// A `memberRepositories` row, spelled under W.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct MemberRepositoryRow {
    pub(crate) path: String,
    pub(crate) declared_by: Vec<Declarer>,
}

/// `DiscoveryResultV3`, complete.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum DiscoveryResultV3 {
    Accept(DiscoveryProvenanceV3),
    Refuse {
        refusal: &'static str,
        d9: DiscoveryD9,
        path: Option<String>,
        detail: String,
        provenance: DiscoveryProvenanceV3,
    },
}

/// The composition's outcome: the record, and the declaration half of the
/// link set (typed rows, plan r2 LD-B3B-3).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct WorkspaceDiscovery {
    pub(crate) result: DiscoveryResultV3,
    pub(crate) links: Vec<LinkRow>,
}

/// The D9 branch of the member cap, which the SLM map predates
/// (`PROJECT.SCOPE_LIMIT`: request-rejected, exit 2, REQUEST.UNSATISFIABLE;
/// law M3-B item 24 row 5).
const SCOPE_LIMIT_D9: DiscoveryD9 = DiscoveryD9 {
    class: "request-rejected",
    exit: 2,
    code: "REQUEST.UNSATISFIABLE",
};

fn spelled(root: &str, rel: &str) -> String {
    if rel.is_empty() {
        root.to_owned()
    } else {
        format!("{}/{rel}", root.trim_end_matches('/'))
    }
}

fn walk_failure(failure: super::discovery_walk::Failure) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(WorkspaceRefusal::Walk(refusal)),
    }
}

/// D15 discovery over the lent root `root` (M3-B r9 items 19 to 24): the
/// readers and the member decisions, then the walk with the members.
/// `members` is item 6b's precondition and inputs: `None` when item 6a
/// observed W in a repository (W2 fails), so the readers declare nothing.
/// The invocation's own `member_roots` and `gitlinks` are ignored: the
/// decision supplies them.
///
/// One binding table (r2, Codex B3B2B2B-R1-RF-2 and RF-3) holds the object
/// identity of every path the decision, the walk and item 6b observe, from
/// phase one through the walk to the links: a path seen twice must be the
/// same object, or the discovery fails with a change. The admitted members'
/// index gitlinks are nested repositories (RF-1), known before the walk in
/// both branches (r3, A4-2), so the walk never enters one.
pub(crate) fn discover_with_members(
    root: &DiscoveryRoot<'_>,
    upward: &UpwardProvenance,
    invocation: &DiscoveryInvocation<'_>,
    members: Option<&MemberObservation<'_>>,
    work: &mut WorkScope<'_>,
) -> Result<WorkspaceDiscovery, Failure> {
    let root_abs = root
        .spelling()
        .to_str()
        .ok_or(WorkFailure::Operation(WorkspaceRefusal::Invariant(
            "root-not-utf8",
        )))?
        .to_owned();
    let (array, array_source) = match &invocation.source {
        UnitSourceRequest::ExplicitJoins(roots) => (roots.clone(), ArraySource::ExplicitJoins),
        UnitSourceRequest::ConfigWorkspaceRoots(roots) => {
            (roots.clone(), ArraySource::ConfigWorkspaceRoots)
        }
        UnitSourceRequest::Automatic => (Vec::new(), ArraySource::ConfigWorkspaceRoots),
    };
    let groups = invocation.groups.as_set();
    let inputs = DecisionInputs {
        invoking_uid: invocation.invoking_uid,
        groups,
        waiver: invocation.waiver,
        no_repository: members.is_some(),
        array: &array,
        array_source,
    };
    let bound: Bindings = std::cell::RefCell::new(BTreeMap::new());
    let walk =
        |members: &BTreeSet<String>, gitlinks: &BTreeSet<String>, work: &mut WorkScope<'_>| {
            let request = DiscoveryInvocation {
                invoking_uid: invocation.invoking_uid,
                ci: invocation.ci,
                groups: invocation.groups,
                waiver: invocation.waiver,
                source: invocation.source.clone(),
                basis: invocation.basis,
                member_roots: members,
                gitlinks,
            };
            discover_downward_bound(root, upward.clone(), &request, Some(&bound), work)
                .map_err(walk_failure)
        };
    let spell_rows = |rows: Vec<DeclarationRow>| -> Vec<DeclarationRow> {
        rows.into_iter()
            .map(|mut row| {
                row.path = row.path.map(|p| spelled(&root_abs, &p));
                row
            })
            .collect()
    };
    let spell_declarer = |d: Declarer| match d {
        Declarer::Reader {
            reader,
            path,
            content_sha256,
        } => Declarer::Reader {
            reader,
            path: spelled(&root_abs, &path),
            content_sha256,
        },
        Declarer::Array { source, path } => Declarer::Array {
            source,
            path: spelled(&root_abs, &path),
        },
    };
    let record = |pending: DiscoveryResultPending,
                  members: Vec<MemberRepositoryRow>,
                  declarations: Vec<DeclarationRow>,
                  keep: bool| {
        let complete = |mut core: DiscoveryProvenancePending| {
            if !keep {
                core.member_repositories.clear();
                core.member_configs.clear();
            }
            DiscoveryProvenanceV3 {
                core,
                members: members.clone(),
                declarations: declarations.clone(),
            }
        };
        match pending {
            DiscoveryResultPending::Accept(core) => DiscoveryResultV3::Accept(complete(core)),
            DiscoveryResultPending::Refuse {
                refusal,
                path,
                detail,
                provenance,
            } => DiscoveryResultV3::Refuse {
                refusal: refusal.code(),
                d9: refusal.d9(),
                path,
                detail,
                provenance: complete(provenance),
            },
        }
    };
    let none = BTreeSet::new();
    // The provenance of the discovery without members (LD-B3B0-5), which a
    // member rule's or the array gate's refusal carries.
    let plain = |declarations: Vec<DeclarationRow>,
                 work: &mut WorkScope<'_>|
     -> Result<DiscoveryProvenanceV3, Failure> {
        let walked = walk(&none, &none, work)?;
        Ok(
            match record(walked, Vec::new(), spell_rows(declarations), false) {
                DiscoveryResultV3::Accept(p) | DiscoveryResultV3::Refuse { provenance: p, .. } => p,
            },
        )
    };
    let first = {
        let mut obs = NativeObservation::new(
            root,
            invocation.invoking_uid,
            groups,
            invocation.waiver,
            members,
            &bound,
            work,
        );
        phase_one(&mut obs, &inputs)?
    };
    // Branch A walks once with its admitted members and their gitlinks, and
    // only an accepted walk reaches the links; its refusal is the result,
    // with no members and the rows as they stand (A4-2 step 3).
    let (decision, walked) = match first {
        PhaseOne::Decided(decision) => (decision, None),
        PhaseOne::Admitted(admitted) => {
            let roots: BTreeSet<String> = admitted.members().iter().cloned().collect();
            let gitlinks: BTreeSet<String> = admitted.gitlinks().into_iter().collect();
            hook("before-walk", "");
            let walked = walk(&roots, &gitlinks, work)?;
            hook("after-walk", "");
            if matches!(walked, DiscoveryResultPending::Refuse { .. }) {
                return Ok(WorkspaceDiscovery {
                    result: record(
                        walked,
                        Vec::new(),
                        spell_rows(admitted.declarations()),
                        false,
                    ),
                    links: Vec::new(),
                });
            }
            let mut obs = NativeObservation::new(
                root,
                invocation.invoking_uid,
                groups,
                invocation.waiver,
                members,
                &bound,
                work,
            );
            (links(&mut obs, admitted)?, Some(walked))
        }
    };
    Ok(match decision {
        Decision::Members {
            members: rows,
            gitlinks,
            declarations,
            links,
        } => {
            let roots: BTreeSet<String> = rows.iter().map(|m| m.path.clone()).collect();
            let gitlinks: BTreeSet<String> = gitlinks.into_iter().collect();
            let walked = match walked {
                // Branch A: its one walk, with these members and gitlinks.
                Some(walked) => walked,
                None => {
                    hook("before-walk", "");
                    walk(&roots, &gitlinks, work)?
                }
            };
            let members = rows
                .into_iter()
                .map(|m| MemberRepositoryRow {
                    path: spelled(&root_abs, &m.path),
                    declared_by: m.declared_by.into_iter().map(spell_declarer).collect(),
                })
                .collect();
            let links = links
                .into_iter()
                .map(|mut l| {
                    l.provider_member = spelled(&root_abs, &l.provider_member);
                    l
                })
                .collect();
            WorkspaceDiscovery {
                result: record(walked, members, spell_rows(declarations), true),
                links,
            }
        }
        Decision::ArrayRefused {
            path,
            detail,
            declarations,
        } => {
            // SLM's own record (A4-2 step 1): the root's raw text, unspelled.
            let provenance = plain(declarations, work)?;
            WorkspaceDiscovery {
                result: DiscoveryResultV3::Refuse {
                    refusal: DiscoveryRefusal::ExplicitPathInvalid.code(),
                    d9: DiscoveryRefusal::ExplicitPathInvalid.d9(),
                    path,
                    detail: detail.to_owned(),
                    provenance,
                },
                links: Vec::new(),
            }
        }
        Decision::Refuse {
            refusal,
            path,
            detail,
            declarations,
        } => {
            let provenance = plain(declarations, work)?;
            let (code, d9) = match refusal {
                MemberRefusal::RootCustodyRefused => {
                    (refusal.code(), DiscoveryRefusal::RootCustodyRefused.d9())
                }
                MemberRefusal::ScopeLimit => (refusal.code(), SCOPE_LIMIT_D9),
            };
            WorkspaceDiscovery {
                result: DiscoveryResultV3::Refuse {
                    refusal: code,
                    d9,
                    path: Some(spelled(&root_abs, &path)),
                    detail,
                    provenance,
                },
                links: Vec::new(),
            }
        }
    })
}

// ------------------------------------------------------------------ the record

fn string(s: &str) -> JsonValue {
    JsonValue::String(s.to_owned())
}
fn strings(values: &[String]) -> JsonValue {
    JsonValue::Array(values.iter().map(|s| string(s)).collect())
}
fn optional(value: Option<&str>) -> JsonValue {
    value.map_or(JsonValue::Null, string)
}
fn integer(n: i128) -> JsonValue {
    JsonInteger::new(n).map_or(JsonValue::Null, JsonValue::Integer)
}
fn object(pairs: Vec<(&str, JsonValue)>) -> JsonValue {
    JsonValue::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}

fn declarer(d: &Declarer) -> JsonValue {
    match d {
        Declarer::Reader {
            reader,
            path,
            content_sha256,
        } => object(vec![
            ("source", string("reader")),
            ("readerId", string(reader)),
            ("readerVersion", integer(1)),
            ("path", string(path)),
            ("contentSha256", string(content_sha256)),
        ]),
        Declarer::Array { source, path } => object(vec![
            ("source", string(source.as_str())),
            ("path", string(path)),
        ]),
    }
}

fn declaration(r: &DeclarationRow) -> JsonValue {
    object(vec![
        ("readerId", string(r.reader)),
        ("readerVersion", integer(1)),
        ("state", string(r.state.as_str())),
        ("path", optional(r.path.as_deref())),
        ("contentSha256", optional(r.content_sha256.as_deref())),
        ("stateSubject", optional(r.state_subject.as_deref())),
        (
            "unresolved",
            JsonValue::Array(
                r.unresolved
                    .iter()
                    .map(|u| {
                        object(vec![
                            ("entry", string(&u.entry)),
                            ("reason", string(u.reason)),
                            ("subject", optional(u.subject.as_deref())),
                        ])
                    })
                    .collect(),
            ),
        ),
    ])
}

impl DiscoveryProvenanceV3 {
    /// The provenance in `DiscoveryProvenanceV3`'s shape.
    pub(crate) fn to_json(&self) -> JsonValue {
        let p = &self.core;
        let u = &p.upward;
        object(vec![
            ("schemaVersion", integer(3)),
            ("mode", string(&u.mode)),
            ("ci", JsonValue::Bool(p.ci)),
            ("selectedRoot", string(&p.selected_root)),
            ("configPath", optional(u.config_path.as_deref())),
            (
                "walked",
                JsonValue::Array(
                    u.walked
                        .iter()
                        .map(|w| {
                            object(vec![
                                ("path", string(&w.path)),
                                ("custody", string(&w.custody)),
                                ("candidate", string(&w.candidate)),
                                ("boundary", optional(w.boundary.as_deref())),
                            ])
                        })
                        .collect(),
                ),
            ),
            ("stopReason", string(&u.stop_reason)),
            (
                "custodyWaiver",
                p.custody_waiver.map_or(JsonValue::Null, string),
            ),
            (
                "authorizedGroupIds",
                JsonValue::Array(
                    p.authorized_group_ids
                        .iter()
                        .map(|g| integer(*g as i128))
                        .collect(),
                ),
            ),
            (
                "vcs",
                u.vcs.as_ref().map_or(JsonValue::Null, |v| {
                    object(vec![
                        ("kind", string(v.kind)),
                        ("target", optional(v.target.as_deref())),
                        ("followed", JsonValue::Bool(false)),
                    ])
                }),
            ),
            ("nestedRepositories", strings(&p.nested_repositories)),
            ("nestedProjects", strings(&p.nested_projects)),
            ("unitSource", string(p.unit_source)),
            (
                "units",
                JsonValue::Array(
                    p.units
                        .iter()
                        .map(|r| {
                            object(vec![
                                ("path", string(&r.path)),
                                ("kind", string(r.kind)),
                                (
                                    "markers",
                                    JsonValue::Array(r.markers.iter().map(|m| string(m)).collect()),
                                ),
                            ])
                        })
                        .collect(),
                ),
            ),
            (
                "excludedUnits",
                JsonValue::Array(
                    p.excluded_units
                        .iter()
                        .map(|r| {
                            object(vec![
                                ("path", string(&r.path)),
                                ("reason", string(&r.reason)),
                            ])
                        })
                        .collect(),
                ),
            ),
            (
                "prunedTrees",
                JsonValue::Array(
                    p.pruned_trees
                        .iter()
                        .map(|t| {
                            object(vec![
                                ("path", string(&t.path)),
                                ("reason", string(t.reason.as_str())),
                                (
                                    "markerCount",
                                    t.marker_count
                                        .map_or(JsonValue::Null, |n| integer(n as i128)),
                                ),
                                ("markerCountBasis", string(t.basis.as_str())),
                            ])
                        })
                        .collect(),
                ),
            ),
            (
                "explicitPathWasSymlink",
                u.explicit_path_was_symlink
                    .map_or(JsonValue::Null, JsonValue::Bool),
            ),
            ("warnings", strings(&p.warnings)),
            (
                "memberRepositories",
                JsonValue::Array(
                    self.members
                        .iter()
                        .map(|m| {
                            object(vec![
                                ("path", string(&m.path)),
                                (
                                    "declaredBy",
                                    JsonValue::Array(m.declared_by.iter().map(declarer).collect()),
                                ),
                            ])
                        })
                        .collect(),
                ),
            ),
            ("memberConfigs", strings(&p.member_configs)),
            (
                "workspaceDeclarations",
                JsonValue::Array(self.declarations.iter().map(declaration).collect()),
            ),
        ])
    }
}

impl DiscoveryResultV3 {
    /// The record in `DiscoveryResultV3`'s shape.
    pub(crate) fn to_json(&self) -> JsonValue {
        match self {
            Self::Accept(p) => object(vec![
                ("status", string("ACCEPT")),
                ("provenance", p.to_json()),
            ]),
            Self::Refuse {
                refusal,
                d9,
                path,
                detail,
                provenance,
            } => object(vec![
                ("status", string("REFUSE")),
                ("refusal", string(refusal)),
                ("path", optional(path.as_deref())),
                ("detail", string(detail)),
                (
                    "d9",
                    object(vec![
                        ("class", string(d9.class)),
                        ("exit", integer(d9.exit as i128)),
                        ("code", string(d9.code)),
                    ]),
                ),
                ("provenance", provenance.to_json()),
            ]),
        }
    }
}

#[cfg(test)]
mod tests {
    include!("workspace_discovery_tests.rs");
    // Unit B3-b2b2c: the T2 link-map controls, run by the check lane.
    include!("workspace_t2_link_tests.rs");
}
