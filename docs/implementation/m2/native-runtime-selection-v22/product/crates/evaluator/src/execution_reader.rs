//! Retained reader for the execution capture diagnostic. All maps below are
//! derived from named immutable inputs; no caller census or ADMIT is accepted.
use super::*;
use alloc::collections::BTreeMap;
use opensip_identity::{GraphError, IdentityDomain as D, RetainedInputs, TraversalBudget};

#[derive(Debug, PartialEq, Eq)]
pub enum ExecutionInputError {
    Record(GraphError),
    Parameters(crate::PolicyAdmissionError),
    Enumeration(crate::EnumerationJoinError),
    View(crate::ViewJoinError),
    Import(crate::ImportJoinError),
    Stage(crate::StageOutputError),
    Refused(String),
    Limit,
    Law,
}
impl From<Error> for ExecutionInputError {
    fn from(value: Error) -> Self {
        match value {
            Error::Shape => Self::Law,
            Error::Limit => Self::Limit,
            Error::Record(e) => Self::Record(e),
        }
    }
}
/// Inert join diagnostics. `Ok` is not synonymous with ADMIT: semantic refusal
/// retains accounts/outcomes explaining why the capture failed. Neither result
/// establishes predicate truth, Run replay, or publication custody.
pub struct ExecutionInputChecks {
    value: V,
    digest: [u8; 32],
}
impl ExecutionInputChecks {
    pub fn value(&self) -> &V {
        &self.value
    }
    pub fn input_digest(&self) -> [u8; 32] {
        self.digest
    }
}
fn digest(v: &V) -> Result<[u8; 32], ExecutionInputError> {
    crate::native_universe::sha256_text(&alloc::format!("sha256:{}", string_value(v)?))
        .map_err(|_| ExecutionInputError::Law)
}
fn domain(id: &str) -> Result<D, ExecutionInputError> {
    [
        D::Plan,
        D::ExecutionPlan,
        D::Snapshot,
        D::Closure,
        D::Import,
        D::View,
        D::Coverage,
        D::SubjectScope,
        D::Fact,
    ]
    .into_iter()
    .find(|d| id.split_once(':').is_some_and(|(p, _)| p == d.prefix()))
    .ok_or(ExecutionInputError::Law)
}
struct Reader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
    work: usize,
    objects: BTreeMap<String, (String, V)>,
    blobs: BTreeMap<String, Vec<u8>>,
}
impl Reader<'_, '_> {
    fn step(&mut self) -> Result<(), ExecutionInputError> {
        charge(&mut self.work).map_err(Into::into)
    }
    fn object(&mut self, id: &str, d: D) -> Result<V, ExecutionInputError> {
        self.step()?;
        if let Some((actual, v)) = self.objects.get(id) {
            if actual != d.name() {
                return Err(ExecutionInputError::Law);
            }
            return Ok(v.clone());
        }
        let v = self
            .inputs
            .object(id, d, self.budget.descriptor_work)
            .map_err(|e| ExecutionInputError::Record(GraphError::Input(e)))?
            .descriptor()
            .clone();
        self.objects.insert(id.into(), (d.name().into(), v.clone()));
        Ok(v)
    }
    fn raw(&mut self, sha: &str) -> Result<Vec<u8>, ExecutionInputError> {
        self.step()?;
        if let Some(raw) = self.blobs.get(sha) {
            return Ok(raw.clone());
        }
        let raw = self
            .inputs
            .blob(digest(&text(sha))?)
            .map_err(|e| ExecutionInputError::Record(GraphError::Input(e)))?
            .bytes()
            .to_vec();
        self.blobs.insert(sha.into(), raw.clone());
        Ok(raw)
    }
    fn record(&mut self, sha: &str) -> Result<V, ExecutionInputError> {
        self.raw(sha)?;
        self.inputs
            .blob(digest(&text(sha))?)
            .and_then(|b| b.canonical_record())
            .map_err(|e| ExecutionInputError::Record(GraphError::Input(e)))
    }
    fn load_promises(&mut self, p: &V) -> Result<(), ExecutionInputError> {
        for id in list(field(p, "objectKeys"))? {
            let id = string_value(id)?;
            self.object(id, domain(id)?)?;
        }
        for sha in list(field(p, "blobDigests"))? {
            self.raw(string_value(sha)?)?;
        }
        Ok(())
    }
    fn selected_records(
        &mut self,
        refs: &[V],
        name: &str,
    ) -> Result<BTreeMap<String, V>, ExecutionInputError> {
        let mut result = BTreeMap::new();
        for r in refs {
            self.step()?;
            if ref_domain(r) == name {
                let sha = string_value(field(r, "digest"))?;
                result.insert(sha.into(), self.record(sha)?);
            }
        }
        Ok(result)
    }
}

/// Recheck the exact evaluator input selection and derive the capture join from
/// retained Plan/execution/parameter/view/import evidence before any Run exists.
/// The expected evaluator closure is a locator, rechecked against the retained
/// capture and selected Plan closure; it is never a caller claim of admission.
///
/// Owner/schema/missing-byte/local-limit failures return typed `Err`. With those
/// prerequisites satisfied, `value()` preserves X's complete ADMIT/REFUSE
/// diagnostic document. This bounded composition does not replace complete
/// first-evaluation structural admission or independent evaluator replay.
/// Each prerequisite owner receives its own copied local traversal budget;
/// reader and kernel have separate bounded visit counts, not a global CPU bound.
pub fn inspect_execution_input_join(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    execution_id: &str,
    evaluator_closure: &str,
    evaluation_refs: &[V],
    budget: TraversalBudget,
) -> Result<ExecutionInputChecks, ExecutionInputError> {
    if budget.depth == 0 || budget.steps == 0 || budget.descriptor_work == 0 {
        return Err(ExecutionInputError::Limit);
    }
    let mut r = Reader {
        inputs,
        budget,
        work: budget.steps,
        objects: BTreeMap::new(),
        blobs: BTreeMap::new(),
    };
    let mut captures = Vec::new();
    for reference in evaluation_refs {
        r.step()?;
        inputs
            .check_identity_value_shape(reference, "ProofInputRef", budget.descriptor_work)
            .map_err(ExecutionInputError::Record)?;
        if ref_domain(reference) == "execution-inputs" {
            captures.push(reference)
        }
    }
    if captures.len() != 1 {
        return Err(ExecutionInputError::Refused(
            "EVALUATOR_EXECUTION_INPUTS_REQUIRED".into(),
        ));
    }
    let capture_ref = captures[0];
    let capture_digest = digest(field(capture_ref, "digest"))?;
    let manifest = inputs
        .current_record_shape(
            capture_digest,
            "foundation/execution-inputs.schema.v1.json",
            "#",
            budget.descriptor_work,
        )
        .map_err(ExecutionInputError::Record)?;
    let selected = list(field(&manifest, "selectedRefs"))?;
    let mut exact = selected.to_vec();
    exact.push(capture_ref.clone());
    if canonical_set(&exact, &mut r.work)? != canonical_set(evaluation_refs, &mut r.work)? {
        return Err(ExecutionInputError::Refused(
            "EVALUATOR_EXECUTION_INPUT_SELECTION".into(),
        ));
    }
    if !is(field(&manifest, "evaluatorClosure"), evaluator_closure) {
        return Err(ExecutionInputError::Refused(
            "EVALUATOR_EXECUTION_INPUTS_CLOSURE".into(),
        ));
    }
    let plan = r.object(plan_id, D::Plan)?;
    let execution = r.object(execution_id, D::ExecutionPlan)?;
    let parameters = crate::inspect_evaluator_parameters(inputs, plan_id, budget)
        .map_err(ExecutionInputError::Parameters)?;
    let enumeration = parameters
        .selected()
        .get("foundation/enumeration-plan.schema.v1.json")
        .ok_or(ExecutionInputError::Law)?;
    let analysis = inputs
        .identity_record_shape(
            digest(field(&plan, "analysisSpecDigest"))?,
            "analysis-spec",
            budget.descriptor_work,
        )
        .map_err(ExecutionInputError::Record)?;
    let enum_check = crate::inspect_enumeration_join(inputs, plan_id, evaluation_refs, budget)
        .map_err(ExecutionInputError::Enumeration)?;
    if !is(field(enum_check.value(), "result"), "ADMIT") {
        return Err(ExecutionInputError::Refused(
            "EVALUATOR_ENUMERATION_JOIN".into(),
        ));
    }
    crate::inspect_plan_import_joins(inputs, plan_id, budget)
        .map_err(ExecutionInputError::Import)?;
    crate::inspect_plan_stage_specs(inputs, plan_id, execution_id, budget)
        .map_err(ExecutionInputError::Stage)?;
    // Obtain exactly the initial owner-selected roots with empty lookup maps.
    // Load them before the ONE selected reference hop; newly promised objects
    // are loaded but never recursively fed back into pointer derivation.
    let empty_objects = BTreeMap::new();
    let empty_blobs = BTreeMap::new();
    let seeds = promises(
        PromiseInput {
            manifest: &manifest,
            plan: &plan,
            execution: &execution,
            enumeration,
            objects: &empty_objects,
            blobs: &empty_blobs,
        },
        &mut r.work,
    )?;
    r.load_promises(&seeds)?;
    let promised = promises(
        PromiseInput {
            manifest: &manifest,
            plan: &plan,
            execution: &execution,
            enumeration,
            objects: &r.objects,
            blobs: &r.blobs,
        },
        &mut r.work,
    )?;
    r.load_promises(&promised)?;
    // Facts are read only from named views; their presence in storage cannot
    // add them to the capture's pointer set or semantic input selection.
    let view_ids = r
        .objects
        .iter()
        .filter(|(_, (d, _))| d == "view")
        .map(|(k, _)| k.clone())
        .collect::<Vec<_>>();
    for id in view_ids {
        let view = r.object(&id, D::View)?;
        for fid in list(field(&view, "facts"))? {
            r.object(string_value(fid)?, D::Fact)?;
        }
        if selected.iter().any(|rf| {
            ref_domain(rf) == "view"
                && id == alloc::format!("view2:{}", string_value(field(rf, "digest")).unwrap_or(""))
        }) {
            crate::inspect_plan_view_joins(inputs, plan_id, &id, evaluation_refs, budget)
                .map_err(ExecutionInputError::View)?;
        }
    }
    let inventories = r.selected_records(selected, "subject-inventory")?;
    let candidates = r.selected_records(selected, "candidate-producer-result")?;
    let targets = r.selected_records(selected, "target-attribution")?;
    let incoming = r.selected_records(selected, "incoming-search")?;
    let mut imports = BTreeMap::new();
    for id in list(field(&plan, "importIds"))? {
        let id = string_value(id)?;
        let v = r.object(id, D::Import)?;
        imports.insert(
            id.split_once(':').ok_or(ExecutionInputError::Law)?.1.into(),
            v,
        );
    }
    let mut closures = BTreeMap::new();
    for id in list(field(&plan, "semanticClosures"))? {
        let id = string_value(id)?;
        closures.insert(id.into(), r.object(id, D::Closure)?);
    }
    let mut stages = BTreeMap::new();
    for stage in list(field(&execution, "stages"))? {
        let sha = string_value(field(stage, "stageSpecDigest"))?;
        stages.insert(sha.into(), r.record(sha)?);
    }
    let snapshot = r.object(string_value(field(&plan, "snapshotId"))?, D::Snapshot)?;
    let vcs = r.record(string_value(field(&snapshot, "vcsDigest"))?)?;
    let groups = BTreeMap::new();
    let pointers = list(field(&promised, "store_pointers"))?
        .iter()
        .map(|v| string_value(v).map(String::from))
        .collect::<Result<BTreeSet<_>, _>>()?;
    let capture = CaptureInput {
        plan_id,
        execution_id,
        plan: &plan,
        execution: &execution,
        enumeration,
        analysis: &analysis,
        manifest: &manifest,
        closures: &closures,
        stages: &stages,
    };
    let mut work = budget.steps;
    let value = join_execution(
        KernelInput {
            capture,
            store: ExecutionStore {
                objects: &r.objects,
                blobs: &r.blobs,
                pointers: &pointers,
            },
            inventories: &inventories,
            imports: &imports,
            candidates: &candidates,
            targets: &targets,
            incoming: &incoming,
            groups: &groups,
            vcs: &vcs,
            inputs,
            schema_work: budget.descriptor_work,
        },
        &mut work,
    )?;
    Ok(ExecutionInputChecks {
        value,
        digest: capture_digest,
    })
}
