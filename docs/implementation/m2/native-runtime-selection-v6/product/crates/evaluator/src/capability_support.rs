//! Native fact support and three local Coverage prerequisites.
//! These checks do not replace Coverage producer admission or full Run replay.
use crate::native_retention::inspect_native_frame_inputs;
use crate::native_universe::{array, field, sha256_text, text};
use crate::{NativeRetentionError, NativeUniverseError};
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
pub enum NativeSupportError {
    Owner(NativeUniverseError),
    Retention(NativeRetentionError),
    Record(GraphError),
    Refused(String),
    Limit,
}
impl From<NativeUniverseError> for NativeSupportError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
impl From<NativeRetentionError> for NativeSupportError {
    fn from(e: NativeRetentionError) -> Self {
        Self::Retention(e)
    }
}
/// Private diagnostic gate count. Empty refusals do not establish complete
/// Coverage, a selected Plan, a complete graph or a ReplayedRun.
pub struct NativeSupportChecks {
    gates: usize,
}
impl NativeSupportChecks {
    pub fn gates_checked(&self) -> usize {
        self.gates
    }
}
fn no<T>(s: impl Into<String>) -> Result<T, NativeSupportError> {
    Err(NativeSupportError::Refused(s.into()))
}
fn get<'a>(v: &'a V, k: &str) -> Option<&'a V> {
    if let V::Object(o) = v { o.get(k) } else { None }
}
fn map(v: &V) -> Result<&BTreeMap<String, V>, NativeUniverseError> {
    if let V::Object(o) = v {
        Ok(o)
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
fn bare(v: &V) -> Result<[u8; 32], NativeUniverseError> {
    sha256_text(&format!("sha256:{}", text(v)?))
}
fn path<'a>(mut v: &'a V, p: &V) -> Result<&'a V, NativeUniverseError> {
    for k in array(p)? {
        v = field(v, text(k)?)?;
    }
    Ok(v)
}
fn strings(v: &V) -> Result<Vec<&str>, NativeUniverseError> {
    array(v)?.iter().map(text).collect()
}
fn law() -> Result<V, NativeUniverseError> {
    parse_json(include_bytes!("capability-support-registry.json"))
        .map_err(|_| NativeUniverseError::RegistryLaw)
}
fn inventory(law: &V, relation: &str, rung: &str) -> Result<bool, NativeUniverseError> {
    Ok(strings(field(law, "inventoryCapabilities")?)?
        .contains(&format!("{relation}@{rung}").as_str()))
}
fn syntax_unsupported(
    law: &V,
    selected: &[V],
    relation: &str,
    rung: &str,
    paths: &[&str],
    all: bool,
) -> Result<bool, NativeUniverseError> {
    if inventory(law, relation, rung)? {
        return Ok(false);
    }
    let registry = field(field(law, "grammarCapabilities")?, "languages")?;
    let capability = format!("{relation}@{rung}");
    let mut suffixes = Vec::new();
    for row in selected {
        let lang = text(field(row, "languageId")?)?;
        if let Some(entry) = get(registry, lang)
            && strings(field(entry, "capabilities")?)?.contains(&capability.as_str())
        {
            suffixes.extend(strings(field(row, "suffixes")?)?);
        }
    }
    if suffixes.is_empty() {
        return Ok(true);
    }
    let supported = |p: &&str| suffixes.iter().any(|suffix| p.ends_with(suffix));
    Ok(if all {
        paths.is_empty() || !paths.iter().all(supported)
    } else {
        !paths.iter().any(supported)
    })
}
fn variant_unsupported(
    law: &V,
    table: &V,
    relation: &str,
    rung: &str,
    paths: &[&str],
    all: bool,
) -> Result<bool, NativeUniverseError> {
    if inventory(law, relation, rung)? {
        return Ok(false);
    }
    let table = map(table)?;
    if table.is_empty() {
        return Ok(false);
    }
    let supported = |p: &&str| table.keys().any(|s| p.ends_with(s.as_str()));
    Ok(if all {
        paths.is_empty() || !paths.iter().all(supported)
    } else {
        !paths.iter().any(supported)
    })
}
fn ownership_disclosure<'a>(
    law: &'a V,
    ownership: Option<&V>,
    subjects: &[&str],
    editions: &V,
) -> Result<Option<&'a V>, NativeUniverseError> {
    let entries = field(law, "cloneOwnership")?;
    let Some(o) = ownership else {
        return Ok(Some(field(entries, "ownership-missing")?));
    };
    if get(o, "enumeration") != Some(&V::String("complete".into())) {
        return Ok(Some(field(entries, "owner-unenumerated")?));
    }
    let units = array(field(o, "units")?)?
        .iter()
        .map(|u| Ok((text(field(u, "unitId")?)?, u)))
        .collect::<Result<BTreeMap<_, _>, NativeUniverseError>>()?;
    let selected = strings(field(o, "selectedUnitIds")?)?;
    let editions = map(editions)?;
    for p in subjects {
        let mut effective = BTreeSet::new();
        for r in array(field(o, "ownership")?)? {
            if text(field(r, "path")?)? != *p {
                continue;
            }
            let id = text(field(r, "unitId")?)?;
            if !selected.contains(&id) {
                continue;
            }
            let Some(unit) = units.get(id) else {
                return Ok(Some(field(entries, "owner-ambiguous")?));
            };
            let edition = match get(unit, "targetEdition") {
                Some(v) if v != &V::Null => v,
                _ => {
                    let Some(v) = get(unit, "crateName")
                        .and_then(|v| text(v).ok())
                        .and_then(|name| editions.get(name))
                    else {
                        return Ok(Some(field(entries, "owner-ambiguous")?));
                    };
                    v
                }
            };
            let V::Integer(n) = edition else {
                return Err(NativeUniverseError::RegistryLaw);
            };
            effective.insert(n.get());
        }
        if effective.len() > 1 {
            return Ok(Some(field(entries, "owner-ambiguous")?));
        }
    }
    Ok(None)
}
fn selected_syntax(
    inputs: &RetainedInputs<'_>,
    uid: [u8; 32],
    sid: &str,
    budget: TraversalBudget,
) -> Result<Option<Vec<V>>, NativeSupportError> {
    inspect_native_frame_inputs(inputs, uid, NativeFrameSet::SemanticUniverse, sid, budget)?;
    let frame = inputs
        .frame_candidate(
            uid,
            NativeFrameSet::SemanticUniverse,
            budget.descriptor_work,
        )
        .map_err(NativeSupportError::Record)?;
    if frame.domain() != "native.semantic-universe.syntax.v2" {
        return Ok(None);
    }
    let u = frame.descriptor();
    let row = frame.registry_row();
    let cid = sha256_text(text(path(u, field(row, "contextField")?)?)?)?;
    inspect_native_frame_inputs(inputs, cid, NativeFrameSet::Context, sid, budget)?;
    let c = inputs
        .frame_candidate(cid, NativeFrameSet::Context, budget.descriptor_work)
        .map_err(NativeSupportError::Record)?;
    let selected = strings(field(u, "selectedGrammarIds")?)?;
    let mut rows = Vec::new();
    for g in array(field(field(c.descriptor(), "grammarBundle")?, "grammars")?)? {
        if selected.contains(&text(field(g, "grammarId")?)?) {
            rows.push(g.clone());
        }
    }
    Ok(Some(rows))
}
/// Fact-time syntax support follows the universe's context during the graph
/// walk, before the later Plan-native block. Compiler universes skip this gate.
/// Local relation ladder/anchor/body checks remain independent obligations.
pub fn inspect_syntax_fact(
    inputs: &RetainedInputs<'_>,
    fact_id: &str,
    budget: TraversalBudget,
) -> Result<NativeSupportChecks, NativeSupportError> {
    if budget.steps == 0 || budget.depth == 0 {
        return Err(NativeSupportError::Limit);
    }
    let f = inputs
        .object(fact_id, IdentityDomain::Fact, budget.descriptor_work)
        .map_err(|e| NativeSupportError::Record(GraphError::Input(e)))?;
    let f = f.descriptor();
    let Some(selected) = selected_syntax(
        inputs,
        bare(field(f, "sourceUniverse")?)?,
        text(field(f, "snapshotId")?)?,
        budget,
    )?
    else {
        return Ok(NativeSupportChecks { gates: 0 });
    };
    let paths = array(field(f, "anchors")?)?
        .iter()
        .map(|a| text(field(a, "path")?))
        .collect::<Result<Vec<_>, _>>()?;
    let relation = text(field(f, "relation")?)?;
    let rung = text(field(f, "resolution")?)?;
    let law = law()?;
    if syntax_unsupported(&law, &selected, relation, rung, &paths, true)? {
        return no(format!(
            "SYNTAX_CAPABILITY_UNSUPPORTED_FACT:{relation}@{rung}:{}",
            text(field(field(&law, "unavailable")?, "nativeCause")?)?
        ));
    }
    Ok(NativeSupportChecks { gates: 1 })
}
fn scope_paths<'a>(
    scope: &'a V,
    snapshot: &'a V,
    row: Option<&V>,
) -> Result<(Vec<&'a str>, bool), NativeUniverseError> {
    if row
        .and_then(|r| get(r, "subjectKind"))
        .map(text)
        .transpose()?
        == Some("source-path")
    {
        return Ok((strings(field(scope, "subjects")?)?, true));
    }
    Ok((
        array(field(snapshot, "sourceInventory")?)?
            .iter()
            .map(|r| text(field(r, "path")?))
            .collect::<Result<Vec<_>, _>>()?,
        false,
    ))
}
fn eligibility(row: &V) -> Result<V, NativeSupportError> {
    let language = text(field(row, "language")?)?;
    let binding = get(row, "languageVersionBinding");
    let e = binding.and_then(|b| get(b, "bodyEligibility"));
    let Some(e) = e else {
        return no(format!("BODY_ELIGIBILITY_UNDECLARED:{language}"));
    };
    match text(field(e, "form")?)? {
        "dialect-table" => {
            let d = field(binding.ok_or(NativeUniverseError::RegistryLaw)?, "dialect")?;
            if text(field(d, "form")?)? != "closed-suffix-table"
                || map(field(d, "table")?)?.is_empty()
            {
                return no(format!("BODY_ELIGIBILITY_FORM:{language}"));
            }
            Ok(field(d, "table")?.clone())
        }
        "closed-suffix-set" => {
            let suffixes = strings(field(e, "suffixes")?)?;
            if suffixes.is_empty() || suffixes.iter().any(|s| s.is_empty()) {
                return no(format!("BODY_ELIGIBILITY_FORM:{language}"));
            }
            Ok(V::Object(
                suffixes
                    .into_iter()
                    .map(|s| (s.into(), V::String(s.into())))
                    .collect(),
            ))
        }
        _ => no(format!("BODY_ELIGIBILITY_FORM:{language}")),
    }
}
fn declared(v: Option<&V>) -> Result<&str, NativeUniverseError> {
    match v {
        None | Some(V::Null) => Ok("None"),
        Some(v) => text(v),
    }
}
fn scope_disclosure(
    entry: &V,
    expected: &V,
    relation: &str,
    rung: &str,
    kind: &str,
) -> Result<(), NativeSupportError> {
    let cause = text(field(expected, "nativeCause")?)?;
    let deficiency = text(field(expected, "deficiency")?)?;
    let complete = text(field(entry, "coverage")?)? == "complete";
    match kind {
        "dialect" => {
            if complete {
                return no(format!("COVERAGE_DIALECT_PREREQUISITE:{relation}:{cause}"));
            }
            let actual = declared(get(entry, "deficiency"))?;
            if actual == "None" {
                return no(format!(
                    "COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED:{relation}:{cause}"
                ));
            }
            if actual != deficiency {
                return no(format!(
                    "COVERAGE_DIALECT_DEFICIENCY_MISMATCH:{relation}:expected={deficiency}:declared={actual}"
                ));
            }
            let actual = declared(get(entry, "nativeCause"))?;
            if actual != cause {
                return no(format!(
                    "COVERAGE_DIALECT_CAUSE_MISMATCH:{relation}:expected={cause}:declared={actual}"
                ));
            }
        }
        _ => {
            let prefix = if kind == "syntax" {
                "SYNTAX_CAPABILITY"
            } else {
                "COVERAGE_SOURCE_VARIANT"
            };
            let label = format!("{relation}@{rung}");
            if complete {
                return no(format!("{prefix}_UNSUPPORTED_SCOPE:{label}:{cause}"));
            }
            let actual = declared(get(entry, "deficiency"))?;
            if actual != deficiency {
                return no(format!(
                    "{prefix}_DEFICIENCY_MISMATCH:{label}:expected={deficiency}:declared={actual}"
                ));
            }
            let actual = declared(get(entry, "nativeCause"))?;
            if actual != cause {
                return no(format!(
                    "{prefix}_CAUSE_MISMATCH:{label}:expected={cause}:declared={actual}"
                ));
            }
        }
    }
    Ok(())
}
/// Check the three prerequisite guards in their reference order after rehashing
/// the Coverage carrier, its scope, payload/schema and native retained inputs.
/// This is NOT Coverage producer admission: commitment/count/RC-2/identity
/// producer checks, Plan joins, inventory totality and full Run remain owed.
/// Each frame walk has its own copied traversal budget, not a global Run budget.
pub fn inspect_coverage_prerequisites(
    inputs: &RetainedInputs<'_>,
    coverage_id: &str,
    budget: TraversalBudget,
) -> Result<NativeSupportChecks, NativeSupportError> {
    if budget.steps == 0 || budget.depth == 0 {
        return Err(NativeSupportError::Limit);
    }
    let coverage = inputs
        .object(
            coverage_id,
            IdentityDomain::Coverage,
            budget.descriptor_work,
        )
        .map_err(|e| NativeSupportError::Record(GraphError::Input(e)))?;
    let cv = coverage.descriptor();
    let scope = inputs
        .object(
            text(field(cv, "scopeId")?)?,
            IdentityDomain::SubjectScope,
            budget.descriptor_work,
        )
        .map_err(|e| NativeSupportError::Record(GraphError::Input(e)))?;
    let scope = scope.descriptor();
    let sid = text(field(scope, "snapshotId")?)?;
    let snapshot = inputs
        .object(sid, IdentityDomain::Snapshot, budget.descriptor_work)
        .map_err(|e| NativeSupportError::Record(GraphError::Input(e)))?;
    let payload = inputs
        .registered_record_shape(
            bare(field(cv, "payloadDigest")?)?,
            bare(field(cv, "payloadSchemaDigest")?)?,
            "native/native-evidence.schemas.v2.json",
            "#/$defs/CoverageResultV3",
            budget.descriptor_work,
        )
        .map_err(NativeSupportError::Record)?;
    let entry = field(&payload, "entry")?;
    let relation = text(field(scope, "relation")?)?;
    let rung = text(field(scope, "resolution")?)?;
    let law = law()?;
    let relation_row = get(field(&law, "relations")?, relation);
    let uid = bare(field(scope, "sourceUniverse")?)?;
    let body = relation_row.and_then(|r| get(r, "bodyIdentityJoin")) == Some(&V::Bool(true));
    if body {
        inspect_native_frame_inputs(inputs, uid, NativeFrameSet::SemanticUniverse, sid, budget)?;
        let frame = inputs
            .frame_candidate(
                uid,
                NativeFrameSet::SemanticUniverse,
                budget.descriptor_work,
            )
            .map_err(NativeSupportError::Record)?;
        let u = frame.descriptor();
        let row = frame.registry_row();
        if let Some(dialect) = get(row, "languageVersionBinding").and_then(|b| get(b, "dialect"))
            && let Some(spec) = get(dialect, "ownership")
        {
            let name = text(field(spec, "retainedAs")?)?;
            let mut ownership = None;
            for join in array(field(row, "nestedIdentities")?)? {
                if get(join, "retainedAs").map(text).transpose()? != Some(name) {
                    continue;
                }
                let reference = path(u, field(join, "path")?)?;
                if reference == &V::Null {
                    continue;
                }
                let id = sha256_text(text(reference)?)?;
                ownership = Some(
                    inputs
                        .frame_candidate(id, NativeFrameSet::Nested, budget.descriptor_work)
                        .map_err(NativeSupportError::Record)?
                        .descriptor()
                        .clone(),
                );
            }
            let subjects = strings(field(scope, "subjects")?)?;
            if let Some(owed) = ownership_disclosure(
                &law,
                ownership.as_ref(),
                &subjects,
                path(u, field(dialect, "path")?)?,
            )? {
                scope_disclosure(entry, owed, relation, rung, "dialect")?;
            }
        }
    }
    let (paths, all) = scope_paths(scope, snapshot.descriptor(), relation_row)?;
    if let Some(selected) = selected_syntax(inputs, uid, sid, budget)?
        && syntax_unsupported(&law, &selected, relation, rung, &paths, all)?
    {
        scope_disclosure(entry, field(&law, "unavailable")?, relation, rung, "syntax")?;
    }
    if body {
        let frame = inputs
            .frame_candidate(
                uid,
                NativeFrameSet::SemanticUniverse,
                budget.descriptor_work,
            )
            .map_err(NativeSupportError::Record)?;
        if variant_unsupported(
            &law,
            &eligibility(frame.registry_row())?,
            relation,
            rung,
            &paths,
            all,
        )? {
            scope_disclosure(
                entry,
                field(&law, "sourceVariantUnavailable")?,
                relation,
                rung,
                "variant",
            )?;
        }
    }
    Ok(NativeSupportChecks { gates: 3 })
}
