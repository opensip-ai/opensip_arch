//! Retained per-view joins. Earlier walk/Plan/proof census and later replay are
//! separate obligations; these private diagnostics cannot mint a Run token.
use crate::native_universe::{array, field, sha256_text, text};
use crate::{
    CoverageProducerError, CoverageProducerInput, CoverageUnresolvedEdge, NativeSupportError,
    NativeUniverseError, inspect_coverage_prerequisites, inspect_coverage_producer,
    inspect_syntax_fact,
};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
    vec::Vec,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, NativeFrameSet, RetainedInputs, TraversalBudget,
    parse_json,
};
#[derive(Debug, PartialEq, Eq)]
pub enum ViewJoinError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Support(NativeSupportError),
    Producer(CoverageProducerError),
    Refused(String),
    Limit,
    ViewNotSelected,
}
impl From<NativeUniverseError> for ViewJoinError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
pub struct ViewJoinChecks {
    scopes: usize,
    facts: usize,
    coverage: usize,
}
impl ViewJoinChecks {
    pub fn scope_count(&self) -> usize {
        self.scopes
    }
    pub fn fact_count(&self) -> usize {
        self.facts
    }
    pub fn coverage_count(&self) -> usize {
        self.coverage
    }
}
fn charge(steps: &mut usize) -> Result<(), ViewJoinError> {
    *steps = steps.checked_sub(1).ok_or(ViewJoinError::Limit)?;
    Ok(())
}
fn no<T>(s: impl Into<String>) -> Result<T, ViewJoinError> {
    Err(ViewJoinError::Refused(s.into()))
}
fn get<'a>(v: &'a V, k: &str) -> Option<&'a V> {
    if let V::Object(o) = v { o.get(k) } else { None }
}
fn strings(v: &V) -> Result<Vec<&str>, NativeUniverseError> {
    array(v)?.iter().map(text).collect()
}
fn bare(v: &V) -> Result<[u8; 32], NativeUniverseError> {
    sha256_text(&format!("sha256:{}", text(v)?))
}
fn record(
    inputs: &RetainedInputs<'_>,
    id: &str,
    domain: IdentityDomain,
    budget: TraversalBudget,
    steps: &mut usize,
) -> Result<V, ViewJoinError> {
    charge(steps)?;
    Ok(inputs
        .object(id, domain, budget.descriptor_work)
        .map_err(|e| ViewJoinError::Record(GraphError::Input(e)))?
        .descriptor()
        .clone())
}
fn offset(v: &V) -> Result<usize, ViewJoinError> {
    let V::Integer(n) = v else {
        return Err(NativeUniverseError::RegistryLaw.into());
    };
    usize::try_from(n.get()).map_err(|_| ViewJoinError::Refused("ANCHOR_RANGE".into()))
}
fn relation_payload(
    inputs: &RetainedInputs<'_>,
    fact: &V,
    budget: TraversalBudget,
) -> Result<V, ViewJoinError> {
    let sha = bare(field(fact, "payloadDigest")?)?;
    let schema = bare(field(fact, "payloadSchemaDigest")?)?;
    inputs
        .inspect_relation_snapshot(sha, schema, fact, budget)
        .map_err(ViewJoinError::Record)?;
    // The actual registered relation owner also owes syntax support. No body
    // relation reaches this helper: callers select unresolved-edge or file only.
    let fact_id = opensip_identity::hash_canonical_value("fact", fact)
        .map_err(|_| NativeUniverseError::RegistryLaw)?;
    inspect_syntax_fact(
        inputs,
        &format!("fact2:{}", opensip_identity::digest_hex(&fact_id)),
        budget,
    )
    .map_err(ViewJoinError::Support)?;
    inputs
        .blob(sha)
        .map_err(|e| ViewJoinError::Record(GraphError::Input(e)))?
        .canonical_record()
        .map_err(|e| ViewJoinError::Record(GraphError::Input(e)))
}
fn pyrepr(s: &str) -> String {
    let quote = if s.contains('\'') && !s.contains('"') {
        '"'
    } else {
        '\''
    };
    let mut out = String::new();
    out.push(quote);
    for c in s.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if c == quote => {
                out.push('\\');
                out.push(c);
            }
            c => out.push(c),
        }
    }
    out.push(quote);
    out
}
fn producer_message(value: &V) -> Result<String, NativeUniverseError> {
    let mut causes = strings(field(value, "refusals")?)?
        .into_iter()
        .map(String::from)
        .collect::<Vec<_>>();
    for f in array(field(value, "faults")?)? {
        causes.push(format!(
            "{{'entry': {}, 'fault': {}}}",
            pyrepr(text(field(f, "entry")?)?),
            pyrepr(text(field(f, "fault")?)?)
        ));
    }
    Ok(format!("COVERAGE_PRODUCER_ADMISSION:{}", causes.join(",")))
}
/// Inspect one view actually named by a retained Run's evidence. Rehash named
/// Plan/snapshot/evidence objects rather than trusting caller-provided arrays.
/// This does not establish prior graph traversal, proof-root equality, native
/// Plan selection or completeness of evidence roots. Frame owners use separate
/// copied budgets; the local loop work counter is not a global Run CPU promise.
pub fn inspect_view_joins(
    inputs: &RetainedInputs<'_>,
    run_id: &str,
    view_id: &str,
    budget: TraversalBudget,
) -> Result<ViewJoinChecks, ViewJoinError> {
    if budget.steps == 0 || budget.depth == 0 {
        return Err(ViewJoinError::Limit);
    }
    let mut steps = budget.steps;
    let law = parse_json(include_bytes!("view-joins-registry.json"))
        .map_err(|_| NativeUniverseError::RegistryLaw)?;
    let run = record(inputs, run_id, IdentityDomain::Run, budget, &mut steps)?;
    let plan_id = text(field(&run, "planId")?)?;
    let snapshot_id = text(field(&run, "snapshotId")?)?;
    let plan = record(inputs, plan_id, IdentityDomain::Plan, budget, &mut steps)?;
    let snapshot = record(
        inputs,
        snapshot_id,
        IdentityDomain::Snapshot,
        budget,
        &mut steps,
    )?;
    let evidence = record(
        inputs,
        text(field(&run, "evidenceId")?)?,
        IdentityDomain::SemanticEvidence,
        budget,
        &mut steps,
    )?;
    if !strings(field(&evidence, "viewIds")?)?.contains(&view_id) {
        return Err(ViewJoinError::ViewNotSelected);
    }
    let view = record(inputs, view_id, IdentityDomain::View, budget, &mut steps)?;
    if field(&view, "planId")? != field(&run, "planId")? {
        return no("VIEW_PLAN_JOIN");
    }
    let selected = strings(field(&plan, "semanticClosures")?)?;
    if !selected.contains(&text(field(&view, "producerClosure")?)?) {
        return no("UNSELECTED_PRODUCER");
    }
    let mut scopes = Vec::new();
    let scope_ids = strings(field(&view, "scopeIds")?)?;
    for sid in &scope_ids {
        let s = record(
            inputs,
            sid,
            IdentityDomain::SubjectScope,
            budget,
            &mut steps,
        )?;
        if text(field(&s, "snapshotId")?)? != snapshot_id {
            return no("SCOPE_SOURCE_JOIN");
        };
        let enumerator = text(field(&s, "enumeratorClosure")?)?;
        if !selected.contains(&enumerator) {
            return no("UNSELECTED_ENUMERATOR");
        };
        let c = record(
            inputs,
            enumerator,
            IdentityDomain::Closure,
            budget,
            &mut steps,
        )?;
        if field(&c, "kind")?
            != field(
                field(&law, "closureKinds")?,
                "subject-scope.enumeratorClosure",
            )?
        {
            return no("ENUMERATOR_CLOSURE_KIND");
        };
        scopes.push(s);
    }
    let partition_law = field(&law, "partitionLaw")?;
    let keys = strings(field(partition_law, "partitionKey")?)?;
    let mut partitions: BTreeMap<Vec<String>, BTreeSet<String>> = BTreeMap::new();
    for scope in &scopes {
        charge(&mut steps)?;
        let key = keys
            .iter()
            .map(|k| Ok(String::from(text(field(scope, k)?)?)))
            .collect::<Result<Vec<_>, NativeUniverseError>>()?;
        let seen = partitions.entry(key).or_default();
        let subjects = strings(field(scope, "subjects")?)?;
        let mut overlap = BTreeSet::new();
        for subject in &subjects {
            charge(&mut steps)?;
            if seen.contains(*subject) {
                overlap.insert(*subject);
            }
        }
        if let Some(first) = overlap.first() {
            return no(format!(
                "{}:{}@{}:{first}",
                text(field(partition_law, "refusal")?)?,
                text(field(scope, "relation")?)?,
                text(field(scope, "resolution")?)?
            ));
        }
        seen.extend(subjects.into_iter().map(String::from));
    }
    let mut inventory = BTreeMap::new();
    for item in array(field(&snapshot, "sourceInventory")?)? {
        charge(&mut steps)?;
        inventory.insert(text(field(item, "path")?)?, item);
    }
    let mut facts = Vec::new();
    for fid in strings(field(&view, "facts")?)? {
        let f = record(inputs, fid, IdentityDomain::Fact, budget, &mut steps)?;
        if text(field(&f, "snapshotId")?)? != snapshot_id
            || field(&f, "producerClosure")? != field(&view, "producerClosure")?
        {
            return no("FACT_SOURCE_PRODUCER_JOIN");
        };
        let mut joined = false;
        for s in &scopes {
            charge(&mut steps)?;
            if ["relation", "resolution", "sourceUniverse", "targetUniverse"]
                .iter()
                .all(|k| get(&f, k) == get(s, k))
            {
                joined = true;
                break;
            }
        }
        if !joined {
            return no("FACT_SCOPE_JOIN");
        }
        for a in array(field(&f, "anchors")?)? {
            charge(&mut steps)?;
            let item = inventory.get(text(field(a, "path")?)?);
            if item.is_none() || field(item.unwrap(), "sha256")? != field(a, "blobDigest")? {
                return no("ANCHOR_SOURCE");
            };
            let blob = inputs
                .blob(bare(field(a, "blobDigest")?)?)
                .map_err(|e| ViewJoinError::Record(GraphError::Input(e)))?;
            let raw = blob.bytes();
            let start = offset(field(a, "startByte")?)?;
            let end = offset(field(a, "endByte")?)?;
            if start > end || end > raw.len() {
                return no("ANCHOR_RANGE");
            };
            if core::str::from_utf8(&raw[..start]).is_err()
                || core::str::from_utf8(&raw[start..end]).is_err()
            {
                return no("ANCHOR_UTF8");
            }
        }
        facts.push(f);
    }
    let coverage_ids = strings(field(&view, "coverageIds")?)?;
    let evidence_coverage = strings(field(&evidence, "coverageIds")?)?;
    for cid in &coverage_ids {
        charge(&mut steps)?;
        if !evidence_coverage.contains(cid) {
            return no("VIEW_COVERAGE_JOIN");
        }
    }
    for scope in &scopes {
        charge(&mut steps)?;
        let rel = text(field(scope, "relation")?)?;
        let rung = text(field(scope, "resolution")?)?;
        if !get(field(&law, "ladders")?, rel)
            .map(strings)
            .transpose()?
            .unwrap_or_default()
            .contains(&rung)
        {
            return no(format!(
                "SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:{rel}@{rung}"
            ));
        }
    }
    for cid in &coverage_ids {
        let coverage = record(inputs, cid, IdentityDomain::Coverage, budget, &mut steps)?;
        let sid = text(field(&coverage, "scopeId")?)?;
        let Some(index) = scope_ids.iter().position(|v| *v == sid) else {
            return no("COVERAGE_SCOPE_JOIN");
        };
        let scope = &scopes[index];
        let payload = inputs
            .registered_record_shape(
                bare(field(&coverage, "payloadDigest")?)?,
                bare(field(&coverage, "payloadSchemaDigest")?)?,
                "native/native-evidence.schemas.v2.json",
                "#/$defs/CoverageResultV3",
                budget.descriptor_work,
            )
            .map_err(ViewJoinError::Record)?;
        let mut unresolved_payloads = Vec::new();
        for fact in &facts {
            charge(&mut steps)?;
            if text(field(fact, "relation")?)? == "unresolved-edge" {
                unresolved_payloads.push(relation_payload(inputs, fact, budget)?);
            }
        }
        let edges = unresolved_payloads
            .iter()
            .map(|v| {
                Ok(CoverageUnresolvedEdge {
                    relation: text(field(v, "relation")?)?,
                    referrer: text(field(v, "referrer")?)?,
                    edge_kind: text(field(v, "edgeKind")?)?,
                })
            })
            .collect::<Result<Vec<_>, NativeUniverseError>>()?;
        // Full walk retains these universe frames before the per-view block. This
        // local API rehashes the actual frame to derive its closed schema row; no
        // caller-supplied cache/row or Plan counts can choose the eligibility table.
        let frame = inputs
            .frame_candidate(
                bare(field(scope, "sourceUniverse")?)?,
                NativeFrameSet::SemanticUniverse,
                budget.descriptor_work,
            )
            .map_err(ViewJoinError::Record)?;
        let table = crate::capability_support::eligibility(frame.registry_row())
            .map_err(ViewJoinError::Support)?;
        let dialect = V::Object(BTreeMap::from([(String::from("table"), table)]));
        let admitted = inspect_coverage_producer(
            inputs,
            CoverageProducerInput {
                scope_id: sid,
                payload_digest: bare(field(&coverage, "payloadDigest")?)?,
                payload_schema_digest: Some(bare(field(&coverage, "payloadSchemaDigest")?)?),
                unresolved: &edges,
                universe_dialect: Some(&dialect),
            },
            budget,
        )
        .map_err(ViewJoinError::Producer)?;
        if text(field(admitted.value(), "result")?)? != "ADMIT" {
            return no(producer_message(admitted.value())?);
        }
        if text(field(admitted.value(), "coverageId")?)? != *cid {
            return no("COVERAGE_ADMITTED_IDENTITY");
        }
        inspect_coverage_prerequisites(inputs, cid, budget).map_err(ViewJoinError::Support)?;
        let rel = text(field(scope, "relation")?)?;
        let Some(totality) =
            get(field(&law, "relations")?, rel).and_then(|r| get(r, "coverageTotality"))
        else {
            continue;
        };
        if field(scope, "resolution")? != field(totality, "rung")?
            || text(field(field(&payload, "entry")?, "coverage")?)? != "complete"
        {
            continue;
        }
        let match_on = strings(field(totality, "matchOn")?)?;
        let mut claimed = BTreeSet::new();
        for fact in &facts {
            charge(&mut steps)?;
            if match_on.iter().any(|k| get(fact, k) != get(scope, k)) {
                continue;
            }
            let p = relation_payload(inputs, fact, budget)?;
            claimed.insert(String::from(text(field(
                &p,
                text(field(totality, "pathField")?)?,
            )?)?));
        }
        for subject in strings(field(scope, "subjects")?)? {
            charge(&mut steps)?;
            if inventory.contains_key(subject) && !claimed.contains(subject) {
                return no(format!(
                    "{}:{rel}@{}:{subject}",
                    text(field(totality, "refusal")?)?,
                    text(field(scope, "resolution")?)?
                ));
            }
        }
    }
    Ok(ViewJoinChecks {
        scopes: scopes.len(),
        facts: facts.len(),
        coverage: coverage_ids.len(),
    })
}
