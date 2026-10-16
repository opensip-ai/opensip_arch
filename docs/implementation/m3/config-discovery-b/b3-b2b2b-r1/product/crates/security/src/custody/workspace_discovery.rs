// The D15 discovery composition (M3-B r9 items 19 to 24; unit B3-b2b2b,
// B3-b plan r2 amendment A3): B3-b0's `discover` over the product's parts.
// The decision core (`workspace_declarations.rs`) decides over the native
// observation (`workspace_observation.rs`); the S3 walk and core
// (`discovery_walk.rs`, `discovery_scan.rs`, B3-b2a) observe W with the
// decided members entered as ordinary directories. In branch A the trial
// walk runs with the provisional members first, and only an accepted trial
// reaches the member decisions; its result is the final walk's, since the
// members are the provisional ones. A member rule's refusal carries the
// provenance of the walk without members (LD-B3B0-5). The result is the
// complete `DiscoveryResultV3`: `memberRepositories` rows with `declaredBy`,
// `memberConfigs` and `workspaceDeclarations`, spelled under W, the only
// emittable discovery record. The core's pending provenance is its partial,
// never emitted.
use super::discovery_scan::{
    DiscoveryD9, DiscoveryInvocation, DiscoveryProvenancePending, DiscoveryRefusal,
    DiscoveryResultPending, UnitSourceRequest, UpwardProvenance,
};
use super::discovery_walk::discover_downward;
use super::project_chain::DiscoveryRoot;
use super::workspace_declarations::{
    ArraySource, Decision, DecisionInputs, DeclarationRow, Declarer, LinkRow, MemberRefusal,
    PhaseOne, phase_one, phase_two,
};
use super::workspace_observation::{
    Failure, MemberObservation, NativeObservation, WorkspaceRefusal,
};
use opensip_identity::{JsonInteger, JsonValue};
use opensip_platform::{WorkFailure, WorkScope};
use std::collections::BTreeSet;

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
/// The invocation's own `member_roots` is ignored: the decision supplies them.
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
    let walk = |members: &BTreeSet<String>, work: &mut WorkScope<'_>| {
        let request = DiscoveryInvocation {
            invoking_uid: invocation.invoking_uid,
            ci: invocation.ci,
            groups: invocation.groups,
            waiver: invocation.waiver,
            source: invocation.source.clone(),
            basis: invocation.basis,
            member_roots: members,
        };
        discover_downward(root, upward.clone(), &request, work).map_err(walk_failure)
    };
    let first = {
        let mut obs = NativeObservation::new(
            root,
            invocation.invoking_uid,
            groups,
            invocation.waiver,
            members,
            work,
        );
        phase_one(&mut obs, &inputs)?
    };
    let (decision, walked) = match first {
        PhaseOne::Decided(decision) => (decision, None),
        PhaseOne::Trial(trial) => {
            let provisional: BTreeSet<String> = trial.provisional().iter().cloned().collect();
            let walked = walk(&provisional, work)?;
            let accepted = matches!(walked, DiscoveryResultPending::Accept(_));
            let mut obs = NativeObservation::new(
                root,
                invocation.invoking_uid,
                groups,
                invocation.waiver,
                members,
                work,
            );
            (phase_two(&mut obs, trial, accepted)?, Some(walked))
        }
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
    let none = BTreeSet::new();
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
    Ok(match decision {
        Decision::Members {
            members: rows,
            declarations,
            links,
        } => {
            let roots: BTreeSet<String> = rows.iter().map(|m| m.path.clone()).collect();
            let walked = match walked {
                Some(walked) => walked,
                None => walk(&roots, work)?,
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
        Decision::TrialRefused { declarations } => WorkspaceDiscovery {
            result: record(
                walked.ok_or(WorkFailure::Operation(WorkspaceRefusal::Invariant(
                    "trial-without-walk",
                )))?,
                Vec::new(),
                spell_rows(declarations),
                false,
            ),
            links: Vec::new(),
        },
        Decision::Refuse {
            refusal,
            path,
            detail,
            declarations,
        } => {
            let plain = walk(&none, work)?;
            let provenance = match record(plain, Vec::new(), spell_rows(declarations), false) {
                DiscoveryResultV3::Accept(p) | DiscoveryResultV3::Refuse { provenance: p, .. } => p,
            };
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
}
