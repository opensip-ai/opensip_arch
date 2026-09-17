//! Closed structural composition. Independent evaluator replay and publication
//! custody remain separate; no callback or caller-provided census is accepted.
use crate::native_universe::{array, field, sha256_text, text};
use crate::{
    BodyIdentityError, ImportJoinError, ImportPayloadError, NativeRetentionError,
    NativeSupportError, NativeUniverseError, PlanNativeError, PolicyAdmissionError,
    PredicateError, RunLinkError, StageOutputError, ViewJoinError,
};
use alloc::{borrow::ToOwned, collections::BTreeSet, format, string::String, vec::Vec};
use opensip_identity::{
    GraphError, IdentityDomain as D, JsonValue as V, NativeFrameSet,
    RetainedInputs, StructuralChecks, StructuralObligation, StructuralOwner, TraversalBudget,
    digest_hex, hash_canonical_value,
};

/// Explicit development resource controls, not Plan work units or M6 limits.
/// Walk steps, owner invocation count, and EACH owner's local limits are
/// separate bounds. Copied local budgets are never described as one counter.
#[derive(Clone, Copy)]
pub struct RetainedWalkLimits {
    pub walk: TraversalBudget,
    pub owner: TraversalBudget,
    pub owner_invocations: usize,
}
#[derive(Debug, PartialEq, Eq)]
pub enum RetainedWalkError {
    Graph(GraphError),
    Owner(NativeUniverseError),
    Retention(NativeRetentionError),
    Syntax(NativeSupportError),
    Body(BodyIdentityError),
    Run(RunLinkError),
    Plan(PlanNativeError),
    Policy(PolicyAdmissionError),
    Stage(StageOutputError),
    Predicate(PredicateError),
    View(ViewJoinError),
    Import(ImportJoinError),
    Payload(ImportPayloadError),
    Refused(&'static str),
    Limit,
    Law,
}
impl From<NativeUniverseError> for RetainedWalkError {
    fn from(e: NativeUniverseError) -> Self { Self::Owner(e) }
}
impl From<GraphError> for RetainedWalkError {
    fn from(e: GraphError) -> Self { Self::Graph(e) }
}
/// Diagnostic counts only. Does not mint a Run, replay result or publication
/// ledger; it is not an exact census of all raw bytes consumed by local owners.
pub struct RetainedWalkChecks {
    structural: StructuralChecks,
    contexts: usize,
    universes: usize,
    owner_invocations: usize,
}
impl RetainedWalkChecks {
    pub fn object_count(&self) -> usize { self.structural.object_count() }
    pub fn context_count(&self) -> usize { self.contexts }
    pub fn universe_count(&self) -> usize { self.universes }
    pub fn owner_invocations(&self) -> usize { self.owner_invocations }
}
fn bare(v: &V) -> Result<[u8; 32], RetainedWalkError> {
    Ok(sha256_text(&format!("sha256:{}", text(v)?))?)
}
fn identity(domain: D, value: &V) -> Result<String, RetainedWalkError> {
    let digest = hash_canonical_value(domain.name(), value).map_err(GraphError::Frame)?;
    Ok(format!("{}:{}", domain.prefix(), digest_hex(&digest)))
}
struct ClosedOwner<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    run: V,
    limits: RetainedWalkLimits,
    remaining: usize,
    frames: BTreeSet<(String, [u8; 32])>,
    contexts: BTreeSet<[u8; 32]>,
    universes: BTreeSet<[u8; 32]>,
    referenced_universes: BTreeSet<[u8; 32]>,
    capabilities: BTreeSet<String>,
    failure: Option<RetainedWalkError>,
}
impl ClosedOwner<'_, '_> {
    fn budget(&mut self) -> Result<TraversalBudget, RetainedWalkError> {
        self.remaining = self.remaining.checked_sub(1).ok_or(RetainedWalkError::Limit)?;
        Ok(self.limits.owner)
    }
    fn object_join(&mut self, domain: D, value: &V) -> Result<(), RetainedWalkError> {
        let V::Object(v) = value else { return Err(RetainedWalkError::Law) };
        if matches!(domain, D::Snapshot | D::Fact | D::SubjectScope) {
            for key in ["snapshotId", "projectId"] {
                if v.get(key).unwrap_or(field(&self.run, key)?) != field(&self.run, key)? {
                    return Err(RetainedWalkError::Refused("REFERENCE_SOURCE_JOIN"));
                }
            }
        }
        if matches!(domain, D::View | D::ProofBundle | D::SemanticEvidence | D::EvaluationSeal | D::ExecutionPlan)
            && field(value, "planId")? != field(&self.run, "planId")?
        {
            return Err(RetainedWalkError::Refused("REFERENCE_PLAN_JOIN"));
        }
        if matches!(domain, D::Fact | D::SubjectScope) {
            for name in ["sourceUniverse", "targetUniverse"] {
                self.referenced_universes.insert(bare(field(value, name)?)?);
            }
        }
        Ok(())
    }
    fn resolve_owned(&mut self, obligation: StructuralObligation<'_>) -> Result<(), RetainedWalkError> {
        let budget = self.budget()?;
        match obligation {
            // These are deferred only inside this fixed composition, whose
            // policy/stage/native/body joins cannot be disabled by a caller.
            StructuralObligation::Retention { .. } | StructuralObligation::StageSchema { .. } => Ok(()),
            StructuralObligation::Capability(id) => { self.capabilities.insert(id.into()); Ok(()) }
            StructuralObligation::NativeFrame { value, set } => {
                let set = match set {
                    "native-context" => NativeFrameSet::Context,
                    "native-semantic-universe" => NativeFrameSet::SemanticUniverse,
                    "native-nested" => NativeFrameSet::Nested,
                    _ => return Err(RetainedWalkError::Law),
                };
                let digest = sha256_text(&format!("sha256:{value}"))?;
                if self.frames.contains(&(set.name().into(), digest)) { return Ok(()); }
                let checked = crate::native_retention::inspect_native_frame_inputs(
                    self.inputs, digest, set, text(field(&self.run, "snapshotId")?)?, budget,
                ).map_err(RetainedWalkError::Retention)?;
                for completed_set in [NativeFrameSet::Context, NativeFrameSet::SemanticUniverse, NativeFrameSet::Nested] {
                    self.frames.extend(checked.frame_digests(completed_set).map(|d| (completed_set.name().into(), d)));
                }
                self.contexts.extend(checked.frame_digests(NativeFrameSet::Context));
                self.universes.extend(checked.frame_digests(NativeFrameSet::SemanticUniverse));
                Ok(())
            }
            StructuralObligation::Payload { digest, record, siblings } => {
                // The reference decodes before registry/schema selection.
                self.inputs.blob(digest).and_then(|b| b.canonical_record()).map_err(GraphError::Input)?;
                match text(field(record, "payloadClass")?)? {
                    "import" => {
                        let id = identity(D::Import, siblings)?;
                        crate::inspect_import_payload(self.inputs, &id, budget).map_err(RetainedWalkError::Payload)?;
                    }
                    "relation" => {
                        let id = identity(D::Fact, siblings)?;
                        let schema = bare(field(siblings, "payloadSchemaDigest")?)?;
                        self.inputs.inspect_relation_prefix(digest, schema, siblings, budget)?;
                        crate::inspect_syntax_fact(self.inputs, &id, self.budget()?).map_err(RetainedWalkError::Syntax)?;
                        self.inputs.inspect_relation_snapshot(digest, schema, siblings, self.budget()?)?;
                        if text(field(siblings, "relation")?)? == "clones" {
                            crate::inspect_body_identity(self.inputs, &id, self.budget()?).map_err(RetainedWalkError::Body)?;
                        }
                    }
                    _ => return Err(RetainedWalkError::Law),
                }
                Ok(())
            }
        }
    }
    fn capture(&mut self, result: Result<(), RetainedWalkError>) -> Result<(), GraphError> {
        match result {
            Ok(()) => Ok(()),
            Err(error) => { self.failure = Some(error); Err(GraphError::OwnerJoin) }
        }
    }
}
impl StructuralOwner for ClosedOwner<'_, '_> {
    fn object(&mut self, _key: &str, domain: D, value: &V) -> Result<(), GraphError> {
        let result = self.object_join(domain, value); self.capture(result)
    }
    fn resolve(&mut self, obligation: StructuralObligation<'_>) -> Result<(), GraphError> {
        let result = self.resolve_owned(obligation); self.capture(result)
    }
}

/// Run the fixed structural composition over retained inputs. No caller-provided
/// owner, registry, frame census or ADMIT flag can skip an owner here. Independent
/// complete evaluation/replay and security/publication custody remain mandatory.
pub fn inspect_retained_walk(
    inputs: &RetainedInputs<'_>, run_id: &str, limits: RetainedWalkLimits,
) -> Result<RetainedWalkChecks, RetainedWalkError> {
    if limits.walk.steps == 0 || limits.walk.depth == 0 || limits.owner.steps == 0
        || limits.owner.depth == 0 || limits.owner_invocations == 0
    { return Err(RetainedWalkError::Limit); }
    let run = inputs.object(run_id, D::Run, limits.owner.descriptor_work).map_err(GraphError::Input)?.descriptor().clone();
    let mut owner = ClosedOwner {
        inputs, run, limits, remaining: limits.owner_invocations,
        frames: BTreeSet::new(), contexts: BTreeSet::new(), universes: BTreeSet::new(),
        referenced_universes: BTreeSet::new(), capabilities: BTreeSet::new(), failure: None,
    };
    let structural = match inputs.inspect_structure_with_owner(run_id, D::Run, limits.walk, &mut owner) {
        Ok(value) => value,
        Err(GraphError::OwnerJoin) => return Err(owner.failure.take().ok_or(RetainedWalkError::Law)?),
        Err(e) => return Err(e.into()),
    };
    let caps: Vec<String> = owner.capabilities.iter().cloned().collect();
    crate::run_links::inspect_run_links_with_capabilities(inputs, run_id, owner.budget()?, &caps).map_err(RetainedWalkError::Run)?;
    let contexts: Vec<_> = owner.contexts.iter().copied().collect();
    let universes: Vec<_> = owner.universes.iter().copied().collect();
    let plan_id = text(field(&owner.run, "planId")?)?.to_owned();
    crate::inspect_plan_native(inputs, &plan_id, &contexts, &universes, owner.budget()?).map_err(RetainedWalkError::Plan)?;
    if !owner.referenced_universes.is_subset(&owner.universes) {
        return Err(RetainedWalkError::Refused("UNIVERSE_FRAME_UNRETAINED"));
    }
    crate::inspect_policy_program(inputs, run_id, owner.budget()?).map_err(RetainedWalkError::Policy)?;
    crate::inspect_stage_specs(inputs, run_id, owner.budget()?).map_err(RetainedWalkError::Stage)?;
    crate::inspect_evidence_roots(inputs, run_id, owner.budget()?).map_err(RetainedWalkError::Run)?;
    crate::inspect_predicate_witnesses(inputs, run_id, owner.budget()?).map_err(RetainedWalkError::Predicate)?;
    let evidence_id = text(field(&owner.run, "evidenceId")?)?;
    let evidence = inputs.object(evidence_id, D::SemanticEvidence, limits.owner.descriptor_work).map_err(GraphError::Input)?;
    for view in array(field(evidence.descriptor(), "viewIds")?)? {
        crate::inspect_view_joins(inputs, run_id, text(view)?, owner.budget()?).map_err(RetainedWalkError::View)?;
    }
    crate::inspect_import_joins(inputs, run_id, owner.budget()?).map_err(RetainedWalkError::Import)?;
    Ok(RetainedWalkChecks { structural, contexts: contexts.len(), universes: universes.len(), owner_invocations: limits.owner_invocations - owner.remaining })
}
