//! Retained import/source correspondence and parameter selection diagnostics.
//! These checks neither acquire evidence nor establish complete Run admission.
use crate::NativeUniverseError;
use crate::native_universe::{array, field, sha256_text, text};
use alloc::{collections::BTreeMap, format, string::String, vec::Vec};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, RetainedInputs, TraversalBudget, parse_json,
};
#[derive(Debug, PartialEq, Eq)]
pub enum ImportJoinError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Refused(String),
    Limit,
    Law,
}
impl From<NativeUniverseError> for ImportJoinError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
fn require(ok: bool, cause: &str) -> Result<(), ImportJoinError> {
    if ok {
        Ok(())
    } else {
        Err(ImportJoinError::Refused(cause.into()))
    }
}
fn sha(v: &V) -> Result<[u8; 32], ImportJoinError> {
    Ok(sha256_text(&format!("sha256:{}", text(v)?))?)
}
struct Reader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
}
impl Reader<'_, '_> {
    fn step(&mut self) -> Result<(), ImportJoinError> {
        if self.budget.depth == 0 {
            return Err(ImportJoinError::Limit);
        }
        self.budget.steps = self
            .budget
            .steps
            .checked_sub(1)
            .ok_or(ImportJoinError::Limit)?;
        Ok(())
    }
    fn object(&mut self, id: &str, domain: IdentityDomain) -> Result<V, ImportJoinError> {
        self.step()?;
        Ok(self
            .inputs
            .object(id, domain, self.budget.descriptor_work)
            .map_err(|e| match e {
                opensip_identity::RetainedInputError::ClosureRole { field, expected } => {
                    ImportJoinError::Refused(format!(
                        "CLOSURE_FIELD_KIND:{}.{}:{}",
                        domain.name(),
                        field,
                        expected
                    ))
                }
                e => ImportJoinError::Record(GraphError::Input(e)),
            })?
            .descriptor()
            .clone())
    }
    fn record(&mut self, digest: &V, kind: &str) -> Result<V, ImportJoinError> {
        self.step()?;
        self.inputs
            .identity_record_shape(sha(digest)?, kind, self.budget.descriptor_work)
            .map_err(ImportJoinError::Record)
    }
    fn foreign(
        &mut self,
        digest: &V,
        document: &str,
        selector: &str,
    ) -> Result<V, ImportJoinError> {
        self.step()?;
        self.inputs
            .current_record_shape(
                sha(digest)?,
                document,
                selector,
                self.budget.descriptor_work,
            )
            .map_err(ImportJoinError::Record)
    }
}
fn metadata() -> Result<V, ImportJoinError> {
    parse_json(include_bytes!("import-registry.json")).map_err(|_| ImportJoinError::Law)
}
fn parameter_selection(
    rd: &mut Reader<'_, '_>,
    parameters: &V,
    registry: &V,
) -> Result<(), ImportJoinError> {
    require(
        field(registry, "atMostOnePerSpec")? == &V::Bool(true),
        "PARAMETER_SELECTION_LAW_UNPUBLISHED",
    )?;
    let rows = array(field(registry, "rows")?)?;
    let mut seen: BTreeMap<&str, usize> = BTreeMap::new();
    for entry in array(parameters)? {
        rd.step()?;
        let mut selected = None;
        let mut count = 0;
        for row in rows {
            rd.step()?;
            if field(row, "sha256")? == field(entry, "schemaDigest")? {
                selected = Some(text(field(row, "key")?)?);
                count += 1;
            }
        }
        // Unregistered or ambiguous registry matches belong to payload admission.
        if count == 1 {
            *seen
                .entry(selected.ok_or(ImportJoinError::Law)?)
                .or_default() += 1;
        }
    }
    for (row, count) in &seen {
        if *count > 1 {
            return Err(ImportJoinError::Refused(format!(
                "ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:{row}"
            )));
        }
    }
    // Preserve source registry order for the first missing required row.
    for row in rows {
        rd.step()?;
        let key = text(field(row, "key")?)?;
        if field(row, "requiredForEvaluator3")? == &V::Bool(true) && seen.get(key) != Some(&1) {
            return Err(ImportJoinError::Refused(format!(
                "EVALUATOR_REQUIRED_PARAMETER_MISSING:{key}"
            )));
        }
    }
    Ok(())
}
/// Inspect a retained analysis-spec's closed parameter selection. Payload owner
/// admission remains separate, including unknown/ambiguous schema registration.
pub fn inspect_parameter_selection(
    inputs: &RetainedInputs<'_>,
    analysis_digest: [u8; 32],
    budget: TraversalBudget,
) -> Result<(), ImportJoinError> {
    let mut rd = Reader { inputs, budget };
    rd.step()?;
    let analysis = inputs
        .identity_record_shape(analysis_digest, "analysis-spec", budget.descriptor_work)
        .map_err(ImportJoinError::Record)?;
    parameter_selection(&mut rd, field(&analysis, "parameters")?, &metadata()?)
}
pub struct ImportJoinChecks {
    imports: usize,
}
impl ImportJoinChecks {
    pub fn import_count(&self) -> usize {
        self.imports
    }
}
/// Recheck selected import correspondence against retained snapshot, VCS and
/// analysis-spec context, then apply global parameter cardinality. No imported
/// payload execution, graph traversal, admission token or replay is provided.
pub fn inspect_import_joins(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    budget: TraversalBudget,
) -> Result<ImportJoinChecks, ImportJoinError> {
    let mut rd = Reader { inputs, budget };
    let registry = metadata()?;
    let run = rd.object(run_id, IdentityDomain::Run)?;
    let plan = rd.object(text(field(&run, "planId")?)?, IdentityDomain::Plan)?;
    let snapshot = rd.object(text(field(&run, "snapshotId")?)?, IdentityDomain::Snapshot)?;
    let analysis = rd.record(field(&plan, "analysisSpecDigest")?, "analysis-spec")?;
    let vcs = rd.record(field(&snapshot, "vcsDigest")?, "vcs-observation")?;
    let imports = array(field(&plan, "importIds")?)?;
    if !imports.is_empty() {
        let context_row = array(field(&registry, "rows")?)?
            .iter()
            .find(|r| {
                field(r, "document")
                    .is_ok_and(|v| text(v) == Ok("foundation/import-source-context.schema.json"))
            })
            .ok_or(ImportJoinError::Law)?;
        let mut contexts = Vec::new();
        for p in array(field(&analysis, "parameters")?)? {
            rd.step()?;
            if field(p, "schemaDigest")? == field(context_row, "sha256")? {
                contexts.push(p);
            }
        }
        require(contexts.len() <= 1, "IMPORT_SOURCE_CONTEXT_MULTIPLE")?;
        let mut builds = Vec::new();
        if let Some(p) = contexts.first() {
            rd.step()?;
            let digest = sha(field(p, "payloadDigest")?)?;
            // registered_payload decodes canonical retained bytes before requesting the
            // retained schema artifact. Preserve that order for compound store faults.
            inputs
                .blob(digest)
                .map_err(|e| ImportJoinError::Record(GraphError::Input(e)))?
                .canonical_record()
                .map_err(|e| ImportJoinError::Record(GraphError::Input(e)))?;
            let context = inputs
                .registered_record_shape(
                    digest,
                    sha(field(p, "schemaDigest")?)?,
                    text(field(context_row, "document")?)?,
                    text(field(context_row, "selector")?)?,
                    budget.descriptor_work,
                )
                .map_err(ImportJoinError::Record)?;
            builds = array(field(&context, "declaredBuildIds")?)?.to_vec();
        }
        for iid in imports {
            rd.step()?;
            let import = rd.object(text(iid)?, IdentityDomain::Import)?;
            // RetainedInputs::object already verifies the import closure roles.
            let corr = rd.foreign(
                field(&import, "sourceCorrespondenceDigest")?,
                "workflows/schemas/common.schema.json",
                "#/$defs/SourceCorrespondence",
            )?;
            if text(field(&corr, "kind")?)? == "exact-snapshot" {
                require(
                    field(&corr, "snapshotId")? == field(&run, "snapshotId")?,
                    "IMPORT_SOURCE_JOIN",
                )?;
            } else {
                let mapping_digest = field(&corr, "sourceMappingDigest")?;
                require(
                    !matches!(mapping_digest, V::Null),
                    "IMPORT_SOURCE_MAPPING_REQUIRED",
                )?;
                let mapping = rd.foreign(
                    mapping_digest,
                    "workflows/schemas/imported-evidence.schema.json",
                    "#/$defs/SourceMappingV1",
                )?;
                require(
                    field(&mapping, "snapshotId")? == field(&run, "snapshotId")?,
                    "IMPORT_CORRESPONDENCE_SHAPE",
                )?;
                let mut inventory = BTreeMap::new();
                for row in array(field(&snapshot, "sourceInventory")?)? {
                    rd.step()?;
                    inventory.insert(text(field(row, "path")?)?, field(row, "sha256")?);
                }
                let mut prior: Option<&str> = None;
                for row in array(field(&mapping, "entries")?)? {
                    rd.step()?;
                    let path = text(field(row, "generatedPath")?)?;
                    require(
                        prior.is_none_or(|p| p.as_bytes() < path.as_bytes()),
                        "IMPORT_CORRESPONDENCE_SHAPE",
                    )?;
                    prior = Some(path);
                }
                for row in array(field(&mapping, "entries")?)? {
                    rd.step()?;
                    require(
                        inventory.get(text(field(row, "sourcePath")?)?).copied()
                            == Some(field(row, "sourceSha256")?),
                        "IMPORT_CORRESPONDENCE_SHAPE",
                    )?;
                }
                let revision = field(&corr, "vcsRevision")?;
                let build = field(&corr, "buildIdentity")?;
                let consumable = text(field(&vcs, "kind")?)? != "none"
                    && field(&vcs, "commitId")? == field(revision, "commit")?
                    && (matches!(build, V::Null) || builds.contains(build))
                    && field(&vcs, "dirty")? == &V::Bool(false)
                    && field(revision, "dirty")? == &V::Bool(false);
                require(consumable, "IMPORT_VCS_JOIN")?;
            }
        }
    }
    parameter_selection(&mut rd, field(&analysis, "parameters")?, &registry)?;
    Ok(ImportJoinChecks {
        imports: imports.len(),
    })
}
