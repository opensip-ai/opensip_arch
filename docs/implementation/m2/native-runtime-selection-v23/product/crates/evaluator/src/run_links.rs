//! Retained Run cross-links and evidence-root diagnostics. These separate
//! phases preserve the full closure caller order; neither establishes replay.
use crate::native_universe::{array, field, sha256_text, text};
use crate::{NativeUniverseError, PlanCapabilityError, admit_plan_capability};
use alloc::{collections::BTreeSet, format, string::String};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, RetainedInputs, TraversalBudget,
};
#[derive(Debug, PartialEq, Eq)]
pub enum RunLinkError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Capability(PlanCapabilityError),
    Refused(String),
    Limit,
}
impl From<NativeUniverseError> for RunLinkError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
pub struct RunLinkChecks {
    imports: usize,
}
impl RunLinkChecks {
    pub fn import_count(&self) -> usize {
        self.imports
    }
}
pub struct EvidenceRootChecks {
    views: usize,
    coverage: usize,
    findings: usize,
}
impl EvidenceRootChecks {
    pub fn view_count(&self) -> usize {
        self.views
    }
    pub fn coverage_count(&self) -> usize {
        self.coverage
    }
    pub fn finding_count(&self) -> usize {
        self.findings
    }
}
struct Reader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
}
impl Reader<'_, '_> {
    fn step(&mut self) -> Result<(), RunLinkError> {
        if self.budget.depth == 0 {
            return Err(RunLinkError::Limit);
        }
        self.budget.steps = self
            .budget
            .steps
            .checked_sub(1)
            .ok_or(RunLinkError::Limit)?;
        Ok(())
    }
    fn object(&mut self, id: &str, domain: IdentityDomain) -> Result<V, RunLinkError> {
        self.step()?;
        Ok(self
            .inputs
            .object(id, domain, self.budget.descriptor_work)
            .map_err(|e| RunLinkError::Record(GraphError::Input(e)))?
            .descriptor()
            .clone())
    }
    fn record(&mut self, sha: &V, kind: &str) -> Result<V, RunLinkError> {
        self.step()?;
        let d = sha256_text(&format!("sha256:{}", text(sha)?))?;
        self.inputs
            .identity_record_shape(d, kind, self.budget.descriptor_work)
            .map_err(RunLinkError::Record)
    }
    fn strings(&mut self, value: &V) -> Result<BTreeSet<String>, RunLinkError> {
        let mut out = BTreeSet::new();
        for v in array(value)? {
            self.step()?;
            out.insert(text(v)?.into());
        }
        Ok(out)
    }
}
fn require(yes: bool, cause: &str) -> Result<(), RunLinkError> {
    if yes {
        Ok(())
    } else {
        Err(RunLinkError::Refused(cause.into()))
    }
}
fn equal(a: &V, b: &V, k: &str) -> Result<bool, RunLinkError> {
    Ok(field(a, k)? == field(b, k)?)
}
fn selected(set: &V, value: &V) -> Result<bool, RunLinkError> {
    Ok(array(set)?.contains(value))
}
struct Roots {
    run: V,
    snapshot: V,
    plan: V,
    evidence: V,
    seal: V,
    proof: V,
    execution: V,
}
fn roots(reader: &mut Reader<'_, '_>, run_id: &str) -> Result<Roots, RunLinkError> {
    let run = reader.object(run_id, IdentityDomain::Run)?;
    let snapshot = reader.object(text(field(&run, "snapshotId")?)?, IdentityDomain::Snapshot)?;
    let plan = reader.object(text(field(&run, "planId")?)?, IdentityDomain::Plan)?;
    let evidence = reader.object(
        text(field(&run, "evidenceId")?)?,
        IdentityDomain::SemanticEvidence,
    )?;
    let seal = reader.object(
        text(field(&run, "evaluationSealId")?)?,
        IdentityDomain::EvaluationSeal,
    )?;
    let proof = reader.object(
        text(field(&seal, "proofBundleId")?)?,
        IdentityDomain::ProofBundle,
    )?;
    let execution = reader.object(
        text(field(&seal, "executionPlanId")?)?,
        IdentityDomain::ExecutionPlan,
    )?;
    Ok(Roots {
        run,
        snapshot,
        plan,
        evidence,
        seal,
        proof,
        execution,
    })
}
/// Rehash named root objects, capability bytes, configuration/grant and VCS
/// records, then check the selected pre-native Run joins. Does not traverse the
/// graph or establish the native-context census, policy, stages or proof roots.
pub fn inspect_run_links(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
) -> Result<RunLinkChecks, RunLinkError> {
    inspect_run_links_with_capabilities(inputs, run_id, budget, &[])
}
pub(crate) fn inspect_run_links_with_capabilities(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
    observed_capabilities: &[String],
) -> Result<RunLinkChecks, RunLinkError> {
    let mut rd = Reader { inputs, budget };
    let Roots {
        run,
        snapshot,
        plan,
        evidence,
        seal,
        proof,
        execution,
    } = roots(&mut rd, run_id)?;
    require(
        equal(&run, &snapshot, "projectId")? && equal(&plan, &run, "snapshotId")?,
        "PROJECT_SNAPSHOT_JOIN",
    )?;
    for v in [&evidence, &seal, &proof, &execution] {
        require(equal(v, &run, "planId")?, "PLAN_JOIN")?;
    }
    require(
        equal(&run, &plan, "capabilityManifestId")?,
        "CAPABILITY_JOIN",
    )?;
    rd.step()?;
    admit_plan_capability(
        inputs,
        text(field(&run, "planId")?)?,
        rd.budget.descriptor_work,
    )
    .map_err(RunLinkError::Capability)?;
    // Only the closed composition supplies its actually visited census.
    for id in observed_capabilities {
        rd.step()?;
        require(
            id == text(field(&plan, "capabilityManifestId")?)?,
            "FOREIGN_CAPABILITY_MANIFEST",
        )?;
    }
    require(
        equal(&seal, &run, "evidenceId")? && equal(&evidence, &seal, "proofBundleId")?,
        "PROOF_JOIN",
    )?;
    require(
        equal(&proof, &seal, "executionPlanId")? && equal(&proof, &seal, "evaluatorClosure")?,
        "EVALUATOR_JOIN",
    )?;
    require(
        equal(&proof, &evidence, "findingIds")?
            && equal(&proof, &seal, "verdict")?
            && equal(&plan, &seal, "policyDigest")?,
        "VERDICT_JOIN",
    )?;
    require(equal(&evidence, &plan, "importIds")?, "IMPORT_JOIN")?;
    inspect_snapshot_config(&mut rd, &plan, &snapshot)?;
    require(
        selected(
            field(&plan, "semanticClosures")?,
            field(&seal, "evaluatorClosure")?,
        )?,
        "UNSELECTED_EVALUATOR",
    )?;
    let imports = inspect_grant_vcs(&mut rd, &plan, &snapshot, field(&run, "projectId")?)?;
    Ok(RunLinkChecks { imports })
}
/// Rehash proof/evidence roots and finding evidence/message/producer joins.
/// This phase belongs after policy/stage admission in full closure. It does not
/// evaluate predicates, admit their program addresses or reconstruct findings.
pub fn inspect_evidence_roots(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
) -> Result<EvidenceRootChecks, RunLinkError> {
    let mut rd = Reader { inputs, budget };
    let Roots {
        run: _,
        snapshot: _,
        plan,
        evidence,
        seal: _,
        proof,
        execution: _,
    } = roots(&mut rd, run_id)?;
    let mut views = BTreeSet::new();
    let mut imports = BTreeSet::new();
    let mut blobs: BTreeSet<String> = BTreeSet::new();
    for reference in array(field(&proof, "evaluationInputRefs")?)? {
        rd.step()?;
        let d = text(field(reference, "digest")?)?;
        match text(field(reference, "domain")?)? {
            "view" => {
                views.insert(format!("view2:{d}"));
            }
            "import" => {
                imports.insert(format!("import2:{d}"));
            }
            "blob" => {
                blobs.insert(d.into());
            }
            _ => {}
        }
    }
    require(
        rd.strings(field(&evidence, "viewIds")?)? == views,
        "EVALUATION_VIEW_ROOTS",
    )?;
    let mut coverage = BTreeSet::new();
    let mut facts = BTreeSet::new();
    for id in &views {
        let view = rd.object(id, IdentityDomain::View)?;
        coverage.extend(rd.strings(field(&view, "coverageIds")?)?);
        facts.extend(rd.strings(field(&view, "facts")?)?);
    }
    require(
        rd.strings(field(&evidence, "coverageIds")?)? == coverage,
        "EVALUATION_COVERAGE_ROOTS",
    )?;
    require(
        imports.is_subset(&rd.strings(field(&plan, "importIds")?)?),
        "UNSELECTED_EVALUATION_IMPORT",
    )?;
    let mut witnesses = BTreeSet::new();
    for predicate in array(field(&proof, "predicateProofs")?)? {
        rd.step()?;
        witnesses.insert(String::from(text(field(predicate, "witnessDigest")?)?));
    }
    let finding_ids = array(field(&evidence, "findingIds")?)?;
    for id in finding_ids {
        let finding = rd.object(text(id)?, IdentityDomain::Finding)?;
        for reference in array(field(&finding, "evidenceRefs")?)? {
            rd.step()?;
            let d = text(field(reference, "digest")?)?;
            let visible = match text(field(reference, "domain")?)? {
                "fact" => facts.contains(&format!("fact2:{d}")),
                "coverage" => coverage.contains(&format!("coverage2:{d}")),
                "import" => imports.contains(&format!("import2:{d}")),
                "predicate-witness" => witnesses.contains(d),
                "blob" => blobs.contains(d),
                _ => return Err(NativeUniverseError::RegistryLaw.into()),
            };
            require(visible, "HIDDEN_FINDING_EVIDENCE")?;
        }
        let parameters = rd.record(field(&finding, "parameterDigest")?, "finding-parameters")?;
        require(
            equal(&parameters, &finding, "messageCode")?,
            "FINDING_PARAMETER_MESSAGE_JOIN",
        )?;
        require(
            selected(
                field(&plan, "semanticClosures")?,
                field(&finding, "ruleClosure")?,
            )?,
            "FINDING_RULE_CLOSURE_UNSELECTED",
        )?;
    }
    Ok(EvidenceRootChecks {
        views: views.len(),
        coverage: coverage.len(),
        findings: finding_ids.len(),
    })
}

fn inspect_snapshot_config(
    rd: &mut Reader<'_, '_>,
    plan: &V,
    snapshot: &V,
) -> Result<(), RunLinkError> {
    for k in ["resolvedConfigDigest", "scopeDigest"] {
        require(equal(snapshot, plan, k)?, "SNAPSHOT_INPUT_JOIN")?;
    }
    let config = rd.record(
        field(plan, "resolvedConfigDigest")?,
        "semantic-configuration",
    )?;
    require(
        field(plan, "budget")? == field(field(&config, "analysis")?, "budget")?,
        "PLAN_BUDGET_CONFIG_JOIN",
    )?;
    Ok(())
}
fn inspect_grant_vcs(
    rd: &mut Reader<'_, '_>,
    plan: &V,
    snapshot: &V,
    project_id: &V,
) -> Result<usize, RunLinkError> {
    rd.record(field(plan, "analysisSpecDigest")?, "analysis-spec")?;
    let grant = rd.record(field(plan, "semanticGrantDigest")?, "semantic-grant")?;
    let mut has_preparation = false;
    for principal in array(field(&grant, "principals")?)? {
        rd.step()?;
        let kind = text(field(principal, "kind")?)?;
        require(
            (kind == "first-party") == (*field(principal, "ownerSourceDigest")? == V::Null),
            "PRINCIPAL_OWNER_BINDING",
        )?;
        has_preparation |= kind == "trusted-repository-code";
    }
    require(
        field(&grant, "projectId")? == project_id && equal(&grant, plan, "scopeDigest")?,
        "SEMANTIC_GRANT_JOIN",
    )?;
    let operations = rd.strings(field(&grant, "analysisOperations")?)?;
    require(
        operations.contains("prepare-code") == has_preparation,
        "PREPARATION_OPERATION_JOIN",
    )?;
    let imports = array(field(plan, "importIds")?)?.len();
    require(
        imports == 0 || operations.contains("read-import"),
        "IMPORT_OPERATION_JOIN",
    )?;
    let vcs = rd.record(field(snapshot, "vcsDigest")?, "vcs-observation")?;
    let inventory = rd.record(field(&vcs, "sourceInventoryDigest")?, "source-inventory")?;
    require(
        &inventory == field(snapshot, "sourceInventory")?,
        "VCS_INVENTORY_JOIN",
    )?;
    require(
        (text(field(&vcs, "kind")?)? == "none") == (*field(&vcs, "commitId")? == V::Null),
        "VCS_KIND_JOIN",
    )?;
    Ok(imports)
}
/// Only the fixed first-evaluation composition supplies its visited capability
/// census. No public caller can substitute a claimed complete observation set.
pub(crate) fn inspect_plan_semantic_links(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    execution_id: &str,
    evaluator_closure: &str,
    observed_capabilities: &[String],
    budget: TraversalBudget,
) -> Result<RunLinkChecks, RunLinkError> {
    let mut rd = Reader { inputs, budget };
    let plan = rd.object(plan_id, IdentityDomain::Plan)?;
    let snapshot = rd.object(text(field(&plan, "snapshotId")?)?, IdentityDomain::Snapshot)?;
    let execution = rd.object(execution_id, IdentityDomain::ExecutionPlan)?;
    require(text(field(&execution, "planId")?)? == plan_id, "PLAN_JOIN")?;
    rd.step()?;
    admit_plan_capability(inputs, plan_id, rd.budget.descriptor_work)
        .map_err(RunLinkError::Capability)?;
    for id in observed_capabilities {
        rd.step()?;
        require(
            id == text(field(&plan, "capabilityManifestId")?)?,
            "FOREIGN_CAPABILITY_MANIFEST",
        )?;
    }
    inspect_snapshot_config(&mut rd, &plan, &snapshot)?;
    require(
        array(field(&plan, "semanticClosures")?)?.contains(&V::String(evaluator_closure.into())),
        "UNSELECTED_EVALUATOR",
    )?;
    let imports = inspect_grant_vcs(&mut rd, &plan, &snapshot, field(&snapshot, "projectId")?)?;
    Ok(RunLinkChecks { imports })
}
