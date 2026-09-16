//! One native Coverage producer result over explicit retained host inputs.
//! Success is a local candidate, never complete view/Plan/Run or replay authority.
use crate::NativeUniverseError;
use crate::native_universe::{array, field, sha256_text, text};
use alloc::{collections::BTreeSet, format, string::String, vec, vec::Vec};
use opensip_identity::{
    GraphError, IdentityDomain, JsonInteger, JsonValue as V, RetainedInputs, TraversalBudget,
    canonical_bytes, digest_hex, hash_canonical_value, parse_json,
};
#[derive(Debug, PartialEq, Eq)]
pub enum CoverageProducerError {
    Owner(NativeUniverseError),
    Record(GraphError),
    Limit,
}
impl From<NativeUniverseError> for CoverageProducerError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
/// Explicit unresolved observation supplied by the owning host view. This local
/// API cannot establish that the observation census is complete or Plan-bound.
pub struct CoverageUnresolvedEdge<'a> {
    pub relation: &'a str,
    pub referrer: &'a str,
    pub edge_kind: &'a str,
}
pub struct CoverageProducerInput<'a> {
    pub scope_id: &'a str,
    pub payload_digest: [u8; 32],
    pub payload_schema_digest: Option<[u8; 32]>,
    pub unresolved: &'a [CoverageUnresolvedEdge<'a>],
    /// Host universe context, not a field of the provider's payload. None skips
    /// only this producer slice; full Run still owes its unconditional guard.
    pub universe_dialect: Option<&'a V>,
}
pub struct CoverageProducerChecks {
    value: V,
}
impl CoverageProducerChecks {
    pub fn value(&self) -> &V {
        &self.value
    }
}
fn obj<const N: usize>(items: [(&str, V); N]) -> V {
    V::Object(items.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn strv(s: impl Into<String>) -> V {
    V::String(s.into())
}
fn get<'a>(v: &'a V, k: &str) -> Option<&'a V> {
    if let V::Object(o) = v { o.get(k) } else { None }
}
fn strings(v: &V) -> Result<Vec<&str>, NativeUniverseError> {
    array(v)?.iter().map(text).collect()
}
fn flag(v: &V, k: &str) -> bool {
    get(v, k) == Some(&V::Bool(true))
}
fn integer(v: &V) -> Result<i128, NativeUniverseError> {
    if let V::Integer(n) = v {
        Ok(n.get())
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
fn number(n: usize) -> V {
    V::Integer(JsonInteger::new(n as i128).expect("bounded cardinality"))
}
fn optional_text<'a>(v: &'a V, k: &str) -> Result<Option<&'a str>, NativeUniverseError> {
    match get(v, k) {
        None | Some(V::Null) => Ok(None),
        Some(v) => Ok(Some(text(v)?)),
    }
}
fn at<'a>(mut v: &'a V, p: &V) -> Result<Option<&'a V>, NativeUniverseError> {
    for k in strings(p)? {
        let Some(n) = get(v, k) else { return Ok(None) };
        v = n;
    }
    Ok(Some(v))
}
// These carrier values are closed ASCII enums, booleans or arrays thereof.
// Python json.dumps separates array items with a space; preserve its diagnostics.
fn carrier_json(v: Option<&V>) -> Result<String, NativeUniverseError> {
    match v {
        None => Ok("null".into()),
        Some(V::Array(a)) => Ok(format!(
            "[{}]",
            a.iter()
                .map(|x| carrier_json(Some(x)))
                .collect::<Result<Vec<_>, _>>()?
                .join(", ")
        )),
        Some(v) => {
            String::from_utf8(canonical_bytes(v).map_err(|_| NativeUniverseError::RegistryLaw)?)
                .map_err(|_| NativeUniverseError::RegistryLaw)
        }
    }
}
fn deficiency_faults(law: &V, e: &V) -> Result<Vec<String>, NativeUniverseError> {
    let deficiency = optional_text(e, "deficiency")?;
    let cause = optional_text(e, "nativeCause")?;
    let Some(d) = deficiency else {
        return Ok(cause
            .map(|c| vec![format!("native.coverage-cause-without-deficiency:{c}")])
            .unwrap_or_default());
    };
    let registry = field(field(law, "deficiencyCause")?, "deficiencies")?;
    let Some(row) = get(registry, d) else {
        return Ok(vec![format!(
            "native.coverage-cause-registry-row-missing:{d}"
        )]);
    };
    let mut out = Vec::new();
    let rel = text(field(e, "relation")?)?;
    if let Some(rels) = get(row, "relations") {
        let rs = strings(rels)?;
        if !rs.contains(&rel) {
            out.push(format!(
                "native.coverage-cause-relation-not-in-scope:{d}:{rel}:owned-by={}",
                rs.join(",")
            ));
        }
    }
    let rule = text(field(row, "nativeCause")?)?;
    let carrier = text(field(row, "carrier")?)?;
    if rule == "must-be-null" {
        if let Some(c) = cause {
            out.push(format!(
                "native.coverage-cause-must-be-null:{d}:{c}:carrier={carrier}"
            ));
        }
    } else {
        if cause.is_none() && rule == "required" {
            out.push(format!("native.coverage-cause-required:{d}"));
        }
        if let Some(c) = cause
            && !strings(field(row, "allowedCauses")?)?.contains(&c)
        {
            out.push(format!("native.coverage-cause-not-for-deficiency:{d}:{c}"));
        }
    }
    for kind in ["requires", "oneOf", "contains"] {
        if let Some(test) = get(row, kind) {
            let value = at(e, field(test, "path")?)?;
            let bad = match kind {
                "requires" => value.unwrap_or(&V::Null) != field(test, "equals")?,
                "oneOf" => !array(field(test, "members")?)?.contains(value.unwrap_or(&V::Null)),
                _ => match value {
                    Some(V::Array(a)) => !a.contains(field(test, "member")?),
                    _ => true,
                },
            };
            if bad {
                out.push(format!(
                    "native.coverage-cause-carrier-unsupported:{d}:{carrier}:declared={}",
                    carrier_json(value)?
                ));
            }
        }
    }
    Ok(out)
}
fn bijection(
    law: &V,
    e: &V,
    subjects: &[&str],
    edges: &[CoverageUnresolvedEdge<'_>],
) -> Result<Vec<V>, NativeUniverseError> {
    let rel = text(field(e, "relation")?)?;
    let rung = text(field(e, "resolution")?)?;
    let rc = field(e, "resolutionCompleteness")?;
    let name = format!("{rel}@{rung}");
    let mut faults = Vec::new();
    let mut add = |s: String| faults.push(obj([("entry", strv(&name)), ("fault", strv(s))]));
    if !get(field(law, "ladders")?, rel)
        .map(strings)
        .transpose()?
        .unwrap_or_default()
        .contains(&rung)
    {
        add("RC-0: rung is not a member of this relation's own ladder".into());
        return Ok(faults);
    }
    let state = text(field(rc, "state")?)?;
    if !strings(field(law, "resolutionStates")?)?.contains(&state) {
        add("RC-0: state outside closed enum".into());
        return Ok(faults);
    }
    if text(field(e, "coverage")?)? == "complete" && !flag(rc, "examinedExhaustive") {
        add("RC-6: coverage=complete claims the examined partition is total, so examinedExhaustive must be true".into());
    }
    let claimed = integer(field(rc, "unresolvedEdgeCount")?)?;
    let claimed_classes = strings(field(rc, "unresolvedEdgeClasses")?)?;
    if !strings(field(law, "resolvedRungs")?)?.contains(&rung) {
        if state != "not-applicable" || claimed != 0 {
            add("RC-1: not-applicable rung carries a completeness claim".into());
        } else if flag(rc, "attempted") || !claimed_classes.is_empty() {
            add("RC-1: not-applicable makes no resolution claim, so attempted must be false and the class list empty".into());
        }
        return Ok(faults);
    }
    if state == "not-applicable" {
        add("RC-1: resolved rung must not claim not-applicable".into());
        return Ok(faults);
    }
    let observed: Vec<_> = edges
        .iter()
        .filter(|f| {
            (f.relation == rel || (rel == "reachability" && f.relation == "calls"))
                && subjects.contains(&f.referrer)
        })
        .collect();
    let count = observed.len();
    let classes: Vec<_> = observed
        .iter()
        .map(|f| f.edge_kind)
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    match state {
        "complete" => {
            if !flag(rc, "attempted")
                || !flag(rc, "examinedExhaustive")
                || optional_text(rc, "stageTerminal")? != Some("complete")
            {
                add("RC-2: complete requires attempted, exhaustive examination and a complete stage".into());
            } else if count != 0 || claimed != 0 {
                add(format!(
                    "RC-2: complete claimed but {count} unresolved-edge facts admitted"
                ));
            } else if !claimed_classes.is_empty() {
                add(
                    "RC-2: complete claims zero unresolved edges, so the class list must be empty"
                        .into(),
                );
            }
        }
        "not-attempted" => {
            if flag(rc, "attempted") || claimed != 0 {
                add("RC-2: not-attempted cannot carry counts or attempted=true".into());
            } else if !claimed_classes.is_empty() {
                add("RC-2: not-attempted observed nothing, so the class list must be empty".into());
            }
        }
        "incomplete" | "partial" => {
            let mut sorted = claimed_classes;
            sorted.sort();
            if claimed != count as i128 || sorted != classes {
                add(format!(
                    "RC-2: {state} claims {claimed} but {count} facts admitted"
                ));
            }
            if state == "incomplete"
                && (count == 0
                    || optional_text(rc, "stageTerminal")? != Some("complete")
                    || !flag(rc, "examinedExhaustive"))
            {
                add("RC-2: incomplete needs >=1 edge, complete stage and exhaustive examination; else partial".into());
            }
        }
        _ => {}
    }
    Ok(faults)
}
fn source_variant_owed(
    law: &V,
    scope: &V,
    dialect: Option<&V>,
    subjects: &[&str],
) -> Result<bool, NativeUniverseError> {
    let Some(dialect) = dialect else {
        return Ok(false);
    };
    let rel = text(field(scope, "relation")?)?;
    let rung = text(field(scope, "resolution")?)?;
    let Some(row) = get(field(law, "relations")?, rel) else {
        return Ok(false);
    };
    if get(row, "bodyIdentityJoin") != Some(&V::Bool(true))
        || optional_text(row, "subjectKind")? != Some("source-path")
        || strings(field(law, "inventoryCapabilities")?)?
            .contains(&format!("{rel}@{rung}").as_str())
    {
        return Ok(false);
    }
    // The selected producer helper treats a missing/non-map/empty optional table
    // as no producer predicate. Full Run supplies its independently derived table.
    let Some(V::Object(table)) = get(dialect, "table") else {
        return Ok(false);
    };
    if table.is_empty() {
        return Ok(false);
    }
    Ok(subjects.is_empty()
        || subjects.iter().any(|p| {
            table
                .iter()
                .filter(|(suffix, _)| p.ends_with(suffix.as_str()))
                .max_by_key(|(suffix, _)| suffix.len())
                .is_none_or(|(_, variant)| variant == &V::Null)
        }))
}
/// Compare one retained provider payload with explicit host scope/observations.
/// Rehash/shape failures and work limits remain errors; protocol disagreements
/// retain the selected producer's separate refusals and bijection faults.
/// This local candidate cannot authorize storage, a view, Plan or replay.
pub fn inspect_coverage_producer(
    inputs: &RetainedInputs<'_>,
    request: CoverageProducerInput<'_>,
    budget: TraversalBudget,
) -> Result<CoverageProducerChecks, CoverageProducerError> {
    if budget.steps == 0 || budget.depth == 0 {
        return Err(CoverageProducerError::Limit);
    }
    let law = parse_json(include_bytes!("coverage-registry.json"))
        .map_err(|_| NativeUniverseError::RegistryLaw)?;
    let schema_sha = sha256_text(&format!(
        "sha256:{}",
        text(field(&law, "nativeSchemaSha256")?)?
    ))?;
    let payload = inputs
        .registered_record_shape(
            request.payload_digest,
            schema_sha,
            "native/native-evidence.schemas.v2.json",
            "#/$defs/CoverageResultV3",
            budget.descriptor_work,
        )
        .map_err(CoverageProducerError::Record)?;
    let scope = inputs
        .object(
            request.scope_id,
            IdentityDomain::SubjectScope,
            budget.descriptor_work,
        )
        .map_err(|e| CoverageProducerError::Record(GraphError::Input(e)))?;
    let scope = scope.descriptor();
    let subjects = strings(field(scope, "subjects")?)?;
    if subjects
        .len()
        .checked_add(request.unresolved.len())
        .is_none_or(|n| n > budget.steps)
    {
        return Err(CoverageProducerError::Limit);
    }
    let commitment = format!(
        "sha256:{}",
        request
            .scope_id
            .strip_prefix("scope2:")
            .ok_or(NativeUniverseError::RegistryLaw)?
    );
    let key = field(&payload, "key")?;
    let entry = field(&payload, "entry")?;
    let mut refusals = Vec::new();
    for k in ["relation", "resolution", "sourceUniverse", "targetUniverse"] {
        if field(key, k)? != field(scope, k)? {
            refusals.push(format!("native.coverage-key-scope-mismatch:{k}"));
        }
    }
    if text(field(key, "subjectScopeCommitment")?)? != commitment {
        refusals.push("native.subject-scope-commitment-mismatch".into());
    }
    if field(entry, "relation")? != field(key, "relation")?
        || field(entry, "resolution")? != field(key, "resolution")?
    {
        refusals.push("native.coverage-entry-key-mismatch".into());
    }
    let examined = field(entry, "examinedUniverse")?;
    if text(field(examined, "subjectScopeCommitment")?)? != commitment {
        refusals.push("native.examined-universe-commitment-mismatch".into());
    }
    if integer(field(examined, "subjectCount")?)? != subjects.len() as i128 {
        refusals.push("native.examined-universe-subject-count-mismatch".into());
    }
    let faults = bijection(&law, entry, &subjects, request.unresolved)?;
    refusals.extend(deficiency_faults(&law, entry)?);
    if source_variant_owed(&law, scope, request.universe_dialect, &subjects)? {
        let pair = field(&law, "sourceVariantUnavailable")?;
        let cause = text(field(pair, "nativeCause")?)?;
        let deficiency = text(field(pair, "deficiency")?)?;
        let label = format!(
            "{}@{}",
            text(field(scope, "relation")?)?,
            text(field(scope, "resolution")?)?
        );
        if text(field(entry, "coverage")?)? == "complete" {
            refusals.push(format!(
                "native.coverage-source-variant-unsupported-complete:{label}:{cause}"
            ));
        }
        if optional_text(entry, "deficiency")? != Some(deficiency) {
            refusals.push(format!("native.coverage-source-variant-deficiency-mismatch:{label}:expected={deficiency}:declared={}",optional_text(entry,"deficiency")?.unwrap_or("None")));
        }
        if optional_text(entry, "nativeCause")? != Some(cause) {
            refusals.push(format!("native.coverage-source-variant-cause-mismatch:{label}:expected={cause}:declared={}",optional_text(entry,"nativeCause")?.unwrap_or("None")));
        }
    }
    let declared = request.payload_schema_digest.unwrap_or(schema_sha);
    if declared != schema_sha {
        refusals.push("native.coverage-payload-schema-not-registered".into());
    }
    refusals.sort();
    refusals.dedup();
    let admitted = refusals.is_empty() && faults.is_empty();
    let coverage_id = if admitted {
        let descriptor = obj([
            ("schemaVersion", number(2)),
            ("scopeId", strv(request.scope_id)),
            ("payloadSchemaDigest", strv(digest_hex(&declared))),
            ("payloadDigest", strv(digest_hex(&request.payload_digest))),
        ]);
        inputs
            .check_identity_value_shape(&descriptor, "coverage", budget.descriptor_work)
            .map_err(CoverageProducerError::Record)?;
        let id = hash_canonical_value("coverage", &descriptor)
            .map_err(|_| NativeUniverseError::RegistryLaw)?;
        strv(format!("coverage2:{}", digest_hex(&id)))
    } else {
        V::Null
    };
    Ok(CoverageProducerChecks {
        value: obj([
            ("result", strv(if admitted { "ADMIT" } else { "REFUSE" })),
            (
                "scopeId",
                if admitted {
                    strv(request.scope_id)
                } else {
                    V::Null
                },
            ),
            ("coverageId", coverage_id),
            (
                "subjectScopeCommitment",
                if admitted { strv(commitment) } else { V::Null },
            ),
            (
                "subjectCount",
                if admitted {
                    number(subjects.len())
                } else {
                    V::Null
                },
            ),
            (
                "refusals",
                V::Array(refusals.into_iter().map(strv).collect()),
            ),
            ("faults", V::Array(faults)),
        ]),
    })
}
