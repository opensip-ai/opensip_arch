//! Reconstruct evaluator populations, evidence and per-rule enumeration from
//! retained input records after structural admission. No Run or replay authority.
use alloc::{collections::BTreeMap, format, string::String, vec, vec::Vec};
use opensip_identity::{
    JsonValue as V, canonical_bytes, digest_hex, hash_canonical_value, raw_sha256,
};

#[derive(Debug, PartialEq, Eq)]
pub enum ReconstructionError {
    Structure(crate::RetainedWalkError),
    Record(opensip_identity::GraphError),
    Parameters(crate::PolicyAdmissionError),
    Enumeration(crate::EnumerationJoinError),
    Law,
    Limit,
    Refused(String),
}
type Error = ReconstructionError;
fn obj(v: &V) -> Result<&BTreeMap<String, V>, Error> {
    if let V::Object(v) = v {
        Ok(v)
    } else {
        Err(Error::Law)
    }
}
fn arr(v: &V) -> Result<&[V], Error> {
    if let V::Array(v) = v {
        Ok(v)
    } else {
        Err(Error::Law)
    }
}
fn field<'a>(v: &'a V, k: &str) -> Result<&'a V, Error> {
    obj(v)?.get(k).ok_or(Error::Law)
}
fn text(v: &V) -> Result<&str, Error> {
    if let V::String(v) = v {
        Ok(v)
    } else {
        Err(Error::Law)
    }
}
fn index(v: &V) -> Result<usize, Error> {
    if let V::Integer(v) = v {
        usize::try_from(v.get()).map_err(|_| Error::Law)
    } else {
        Err(Error::Law)
    }
}
fn string(v: &str) -> V {
    V::String(v.into())
}
fn record<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn step(work: &mut usize) -> Result<(), Error> {
    *work = work.checked_sub(1).ok_or(Error::Limit)?;
    Ok(())
}
fn set(values: Vec<V>) -> Result<V, Error> {
    let mut entries = BTreeMap::new();
    for v in values {
        entries.insert(canonical_bytes(&v).map_err(|_| Error::Law)?, v);
    }
    Ok(V::Array(entries.into_values().collect()))
}
fn digest(v: &V) -> Result<String, Error> {
    Ok(digest_hex(&raw_sha256(
        &canonical_bytes(v).map_err(|_| Error::Law)?,
    )))
}
fn subject(universe: &V, kind: &str, row: &V) -> Result<String, Error> {
    let mut d = if let V::Object(v) = record([
        (
            "schemaVersion",
            V::Integer(opensip_identity::JsonInteger::new(3).map_err(|_| Error::Law)?),
        ),
        ("universe", universe.clone()),
        ("kind", string(kind)),
        ("nativeSubjectId", field(row, "nativeSubjectId")?.clone()),
    ]) {
        v
    } else {
        return Err(Error::Law);
    };
    if kind == "package" {
        d.insert("packageManifestPath".into(), field(row, "path")?.clone());
    }
    let sha = hash_canonical_value("evaluation-subject", &V::Object(d)).map_err(|_| Error::Law)?;
    Ok(format!("subject3:{}", digest_hex(&sha)))
}
fn deficiency(source: &str, cause: &str, refs: Vec<V>, sid: V, native: V) -> Result<V, Error> {
    Ok(record([
        ("source", string(source)),
        ("cause", string(cause)),
        ("subjectId", sid),
        ("predicateId", V::Null),
        ("inputRefs", set(refs)?),
        ("evidenceKind", V::Null),
        ("nativeCause", native),
        ("universe", V::Null),
    ]))
}
fn any_glob(
    patterns: &[V],
    path: &str,
    work: &mut usize,
    glob_budget: usize,
) -> Result<bool, Error> {
    for p in patterns {
        step(work)?;
        if crate::portable_glob_match(text(p)?, path, glob_budget).map_err(|_| Error::Limit)? {
            return Ok(true);
        }
    }
    Ok(false)
}
fn selected_path(
    rule: &V,
    path: &str,
    scope: Option<&V>,
    work: &mut usize,
    glob_budget: usize,
) -> Result<bool, Error> {
    let e = field(rule, "subjectEnumeration")?;
    let fallback = [string("**")];
    let empty = [];
    let include = match obj(e)?.get("include") {
        Some(v) if !arr(v)?.is_empty() => arr(v)?,
        _ => &fallback,
    };
    let exclude = match obj(e)?.get("exclude") {
        Some(v) => arr(v)?,
        None => &empty,
    };
    if !any_glob(include, path, work, glob_budget)? || any_glob(exclude, path, work, glob_budget)? {
        return Ok(false);
    }
    if let Some(s) = scope {
        return Ok(
            any_glob(arr(field(s, "include")?)?, path, work, glob_budget)?
                && !any_glob(arr(field(s, "exclude")?)?, path, work, glob_budget)?,
        );
    }
    Ok(true)
}
struct PopulationInputs<'a> {
    policy: &'a V,
    enumeration: &'a V,
    inventories: &'a [V],
    scope: Option<&'a V>,
}
/// Pure internal derivation. The future retained entry must run the fixed
/// first-evaluation owners; this private helper accepts no admission flags.
fn derive_population(
    q: PopulationInputs<'_>,
    mut work: usize,
    glob_budget: usize,
) -> Result<V, Error> {
    step(&mut work)?;
    let atoms = opensip_identity::parse_json(include_bytes!("atom-registry.json"))
        .map_err(|_| Error::Law)?;
    let execution = opensip_identity::parse_json(include_bytes!("execution-registry.json"))
        .map_err(|_| Error::Law)?;
    let universe_map = field(&atoms, "policyUniverseMap")?;
    let modes = field(&execution, "languageModes")?;
    let cells = arr(field(q.enumeration, "cells")?)?;
    let mut population: BTreeMap<String, V> = BTreeMap::new();
    let mut locators = BTreeMap::new();
    let mut inventory_refs = BTreeMap::new();
    let mut by_universe_kind: BTreeMap<(String, String), Vec<&V>> = BTreeMap::new();
    for inv in q.inventories {
        step(&mut work)?;
        let ci = index(field(inv, "cellOrdinal")?)?;
        let pi = index(field(inv, "programOrdinal")?)?;
        let kind = text(field(inv, "kind")?)?;
        let cell = cells.get(ci).ok_or(Error::Law)?;
        let binding = arr(field(cell, "programBindings")?)?
            .get(pi)
            .ok_or(Error::Law)?;
        let universe = field(binding, "universe")?;
        let loc = (ci, pi, String::from(kind));
        locators.insert(loc.clone(), inv);
        inventory_refs.insert(
            loc,
            record([
                ("domain", string("subject-inventory")),
                ("digest", string(&digest(inv)?)),
            ]),
        );
        if universe != &V::Null {
            by_universe_kind
                .entry((text(universe)?.into(), kind.into()))
                .or_default()
                .push(inv);
        }
        for row in arr(field(inv, "rows")?)? {
            step(&mut work)?;
            let sid = subject(universe, kind, row)?;
            if let Some(old) = population.get(&sid)
                && field(old, "row")? != row
            {
                return Err(Error::Refused(
                    "EVALUATOR_POPULATION_ATTRIBUTION_CONFLICT".into(),
                ));
            }
            population.insert(
                sid.clone(),
                record([
                    ("subjectId", string(&sid)),
                    ("universe", universe.clone()),
                    ("kind", string(kind)),
                    ("row", row.clone()),
                    ("collisionPopulationComplete", V::Bool(true)),
                ]),
            );
        }
    }
    for item in population.values_mut() {
        step(&mut work)?;
        if text(field(item, "kind")?)? == "symbol" {
            let key = (
                text(field(item, "universe")?)?.into(),
                String::from("symbol"),
            );
            let group = by_universe_kind.get(&key).ok_or(Error::Law)?;
            let mut complete = true;
            for inv in group {
                step(&mut work)?;
                if text(field(inv, "state")?)? != "complete" {
                    complete = false
                }
            }
            let V::Object(item) = item else {
                return Err(Error::Law);
            };
            item.insert("collisionPopulationComplete".into(), V::Bool(complete));
        }
    }
    let mut enumerations = BTreeMap::new();
    let mut deficiencies = BTreeMap::new();
    for rule in arr(field(q.policy, "rules")?)? {
        step(&mut work)?;
        let rid = text(field(rule, "ruleId")?)?;
        if field(rule, "enabled")? == &V::Bool(false) {
            enumerations.insert(
                rid.into(),
                record([
                    ("state", string("disabled")),
                    ("inventoryRefs", V::Array(vec![])),
                    ("selectedSubjectIds", V::Array(vec![])),
                    ("unresolvedSubjectIds", V::Array(vec![])),
                    ("incompleteInventoryRefs", V::Array(vec![])),
                ]),
            );
            deficiencies.insert(rid.into(), V::Array(vec![]));
            continue;
        }
        let e = field(rule, "subjectEnumeration")?;
        let kind = text(field(e, "subjectKind")?)?;
        let primary = if kind == "export" { "symbol" } else { kind };
        let domain = text(field(universe_map, text(field(e, "universe")?)?)?)?;
        let mut relevant = Vec::new();
        for (loc, inv) in &locators {
            step(&mut work)?;
            let mode = text(field(cells.get(loc.0).ok_or(Error::Law)?, "languageMode")?)?;
            let actual = format!("native.semantic-universe.{}.v2", text(field(modes, mode)?)?);
            if loc.2 == primary && actual == domain {
                relevant.push((loc, *inv));
            }
        }
        let mut refs = Vec::new();
        let mut incomplete = Vec::new();
        let mut known = Vec::new();
        let mut unresolved = Vec::new();
        let mut defs = Vec::new();
        if relevant.is_empty() {
            defs.push(deficiency(
                "enumeration",
                "no-covering-program",
                vec![],
                V::Null,
                V::Null,
            )?)
        }
        for (loc, inv) in relevant {
            step(&mut work)?;
            let ir = inventory_refs.get(loc).ok_or(Error::Law)?.clone();
            refs.push(ir.clone());
            if text(field(inv, "state")?)? != "complete" {
                incomplete.push(ir.clone());
                defs.push(deficiency(
                    "enumeration",
                    "incomplete-inventory",
                    vec![ir.clone()],
                    V::Null,
                    field(inv, "nativeCause")?.clone(),
                )?);
                if field(inv, "deficiency")? == &string("source-syntax-invalid") {
                    defs.push(deficiency(
                        "enumeration",
                        "source-syntax-invalid",
                        vec![ir.clone()],
                        V::Null,
                        V::Null,
                    )?)
                }
            }
            let binding = arr(field(
                cells.get(loc.0).ok_or(Error::Law)?,
                "programBindings",
            )?)?
            .get(loc.1)
            .ok_or(Error::Law)?;
            for row in arr(field(inv, "rows")?)? {
                step(&mut work)?;
                if !selected_path(
                    rule,
                    text(field(row, "path")?)?,
                    q.scope,
                    &mut work,
                    glob_budget,
                )? {
                    continue;
                }
                let sid = subject(field(binding, "universe")?, primary, row)?;
                if kind == "export" {
                    match text(field(row, "exported")?)? {
                        "unknown" => {
                            unresolved.push(string(&sid));
                            defs.push(deficiency(
                                "enumeration",
                                "unknown-export-membership",
                                vec![ir.clone()],
                                string(&sid),
                                V::Null,
                            )?);
                            continue;
                        }
                        "not-exported" => continue,
                        _ => {}
                    }
                }
                known.push(string(&sid));
            }
        }
        enumerations.insert(
            rid.into(),
            record([
                (
                    "state",
                    string(if defs.is_empty() {
                        "complete"
                    } else {
                        "incomplete"
                    }),
                ),
                ("inventoryRefs", set(refs)?),
                ("selectedSubjectIds", set(known)?),
                ("unresolvedSubjectIds", set(unresolved)?),
                ("incompleteInventoryRefs", set(incomplete)?),
            ]),
        );
        deficiencies.insert(rid.into(), set(defs)?);
    }
    Ok(record([
        ("population", V::Object(population)),
        ("enumerations", V::Object(enumerations)),
        ("enumerationDeficiencies", V::Object(deficiencies)),
    ]))
}

use opensip_identity::{
    GraphError, IdentityDomain as D, NativeFrameSet, RetainedInputs, TraversalBudget,
};
struct Reader<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
    work: usize,
}
fn bare(value: &V) -> Result<[u8; 32], Error> {
    crate::native_universe::sha256_text(&format!("sha256:{}", text(value)?)).map_err(|_| Error::Law)
}
impl Reader<'_, '_> {
    fn object(&mut self, id: &str, domain: D) -> Result<V, Error> {
        step(&mut self.work)?;
        Ok(self
            .inputs
            .object(id, domain, self.budget.descriptor_work)
            .map_err(|e| Error::Record(GraphError::Input(e)))?
            .descriptor()
            .clone())
    }
    fn record(&mut self, sha: &V) -> Result<V, Error> {
        step(&mut self.work)?;
        self.inputs
            .blob(bare(sha)?)
            .and_then(|b| b.canonical_record())
            .map_err(|e| Error::Record(GraphError::Input(e)))
    }
}
fn number(value: usize) -> Result<V, Error> {
    Ok(V::Integer(
        opensip_identity::JsonInteger::new(value as i128).map_err(|_| Error::Limit)?,
    ))
}
fn add_count(total: &mut usize, n: usize) -> Result<(), Error> {
    *total = total.checked_add(n).ok_or(Error::Limit)?;
    Ok(())
}
fn locator(reference: &V, domain: D) -> Result<String, Error> {
    Ok(format!(
        "{}:{}",
        domain.prefix(),
        text(field(reference, "digest")?)?
    ))
}
/// Inert reconstructed inputs for evaluator composition and its scanner. The
/// evidence document excludes the reference adapter's ambient raw-byte store;
/// scanners must resolve named retained bytes through RetainedInputs instead.
/// No constructor or caller-supplied admitted maps can create this result.
pub struct ReconstructedInputs {
    normalized: V,
    evidence: V,
}
impl ReconstructedInputs {
    pub fn normalized(&self) -> &V {
        &self.normalized
    }
    pub fn evidence(&self) -> &V {
        &self.evidence
    }
}
/// Derive rule populations, scanner records, counts and uncertainties after
/// fixed first-evaluation structural admission. No Run/proof/finding values are
/// read. Does not evaluate atoms or establish independent replay/publication.
/// All nested owners and globs retain separate local budgets; reader visits
/// use another local bound, not an aggregate Plan work or CPU budget.
pub fn reconstruct_evaluator_inputs(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    execution_id: &str,
    evaluator_closure: &str,
    evaluation_refs: &[V],
    limits: crate::RetainedWalkLimits,
) -> Result<ReconstructedInputs, ReconstructionError> {
    let checked = crate::inspect_first_evaluation_structure(
        inputs,
        plan_id,
        execution_id,
        evaluator_closure,
        evaluation_refs,
        limits,
    )
    .map_err(Error::Structure)?;
    let parameters = crate::inspect_evaluator_parameters(inputs, plan_id, limits.owner)
        .map_err(Error::Parameters)?;
    let enumeration_check =
        crate::inspect_enumeration_join(inputs, plan_id, evaluation_refs, limits.owner)
            .map_err(Error::Enumeration)?;
    if field(enumeration_check.value(), "result")? != &string("ADMIT") {
        return Err(Error::Law);
    }
    let mut r = Reader {
        inputs,
        budget: limits.owner,
        work: limits.owner.steps,
    };
    let plan = r.object(plan_id, D::Plan)?;
    let enumeration = parameters
        .selected()
        .get("foundation/enumeration-plan.schema.v1.json")
        .ok_or(Error::Law)?;
    let scope = parameters
        .selected()
        .get("workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1");
    let mut inventories = Vec::new();
    for rf in evaluation_refs {
        step(&mut r.work)?;
        if field(rf, "domain")? == &string("subject-inventory") {
            inventories.push(r.record(field(rf, "digest")?)?);
        }
    }
    let derived = derive_population(
        PopulationInputs {
            policy: checked.policy().policy(),
            enumeration,
            inventories: &inventories,
            scope,
        },
        limits.owner.steps,
        limits.owner.steps,
    )?;
    let mut universe_domains = BTreeMap::new();
    for d in checked.universe_digests() {
        step(&mut r.work)?;
        let frame = inputs
            .frame_candidate(
                *d,
                NativeFrameSet::SemanticUniverse,
                limits.owner.descriptor_work,
            )
            .map_err(Error::Record)?;
        universe_domains.insert(digest_hex(d), string(frame.domain()));
    }
    let modes = opensip_identity::parse_json(include_bytes!("execution-registry.json"))
        .map_err(|_| Error::Law)?;
    for cell in arr(field(enumeration, "cells")?)? {
        step(&mut r.work)?;
        for b in arr(field(cell, "programBindings")?)? {
            step(&mut r.work)?;
            let u = field(b, "universe")?;
            if u != &V::Null {
                let domain = format!(
                    "native.semantic-universe.{}.v2",
                    text(field(
                        field(&modes, "languageModes")?,
                        text(field(cell, "languageMode")?)?
                    )?)?
                );
                if universe_domains.get(text(u)?) != Some(&string(&domain)) {
                    return Err(Error::Refused("EVALUATOR_CELL_UNIVERSE_DOMAIN".into()));
                }
            }
        }
    }
    let mut closures = BTreeMap::new();
    for id in arr(field(&plan, "semanticClosures")?)? {
        let name = text(id)?;
        closures.insert(name.into(), r.object(name, D::Closure)?);
    }
    let mut facts = BTreeMap::new();
    let mut scopes = BTreeMap::new();
    let mut coverages = BTreeMap::new();
    let mut coverage_scopes = BTreeMap::new();
    for rf in evaluation_refs {
        step(&mut r.work)?;
        if field(rf, "domain")? != &string("view") {
            continue;
        }
        let view = r.object(&locator(rf, D::View)?, D::View)?;
        for id in arr(field(&view, "facts")?)? {
            step(&mut r.work)?;
            let id = text(id)?;
            if facts.contains_key(id) {
                continue;
            }
            let mut fact = obj(&r.object(id, D::Fact)?)?.clone();
            let payload = r.record(fact.get("payloadDigest").ok_or(Error::Law)?)?;
            fact.insert("factId".into(), string(id));
            fact.insert("payload".into(), payload);
            facts.insert(id.into(), V::Object(fact));
        }
        for id in arr(field(&view, "scopeIds")?)? {
            let id = text(id)?;
            scopes.insert(id.into(), r.object(id, D::SubjectScope)?);
        }
        for id in arr(field(&view, "coverageIds")?)? {
            let id = text(id)?;
            let desc = r.object(id, D::Coverage)?;
            coverages.insert(id.into(), r.record(field(&desc, "payloadDigest")?)?);
            coverage_scopes.insert(id.into(), field(&desc, "scopeId")?.clone());
        }
    }
    for rf in evaluation_refs {
        step(&mut r.work)?;
        if field(rf, "domain")? == &string("coverage")
            && !coverages.contains_key(&locator(rf, D::Coverage)?)
        {
            return Err(Error::Refused(
                "EVALUATOR_COVERAGE_INPUT_NOT_IN_VIEW".into(),
            ));
        }
    }
    let mut imports = BTreeMap::new();
    let mut payloads = BTreeMap::new();
    let mut observations = BTreeMap::new();
    let mut import_kinds = BTreeMap::new();
    let mut import_scopes = BTreeMap::new();
    let mut flags = BTreeMap::new();
    let mut expected_import_refs = Vec::new();
    let mut observation_count = 0usize;
    for id in arr(field(&plan, "importIds")?)? {
        let id = text(id)?;
        let wrapper = r.object(id, D::Import)?;
        let payload = r.record(field(&wrapper, "payloadDigest")?)?;
        let observation = r.record(field(&wrapper, "observationDigest")?)?;
        let kind = text(field(&wrapper, "kind")?)?;
        let scope_digest = text(field(&wrapper, "scopeDigest")?)?;
        import_scopes.insert(scope_digest.into(), r.record(&string(scope_digest))?);
        if field(&observation, "kind")? != field(&wrapper, "kind")? {
            return Err(Error::Refused(
                "EVALUATOR_IMPORT_OBSERVATION_KIND_JOIN".into(),
            ));
        }
        let joins = match kind {
            "runtime" => record([
                ("window", field(&payload, "observationWindow")?.clone()),
                ("population", field(&payload, "observedPopulation")?.clone()),
            ]),
            "test" => record([("selection", field(&payload, "selection")?.clone())]),
            "history" => {
                let range = field(&payload, "revisionRange")?;
                record([(
                    "revisionRange",
                    record([
                        ("from", field(range, "from")?.clone()),
                        ("to", field(range, "to")?.clone()),
                    ]),
                )])
            }
            _ => V::Object(BTreeMap::new()),
        };
        for key in ["window", "population", "selection", "revisionRange"] {
            step(&mut r.work)?;
            let v = field(&observation, key)?;
            if v != &V::Null && obj(&joins)?.get(key) != Some(v) {
                return Err(Error::Refused(format!(
                    "EVALUATOR_IMPORT_OBSERVATION_PAYLOAD_JOIN:{key}"
                )));
            }
        }
        match kind {
            "runtime" | "history" => add_count(
                &mut observation_count,
                arr(field(&payload, "subjects")?)?.len(),
            )?,
            "test" => {
                add_count(
                    &mut observation_count,
                    arr(field(&payload, "tests")?)?.len(),
                )?;
                add_count(&mut observation_count, 1)?
            }
            _ => {}
        }
        flags.insert(
            id.into(),
            record([
                ("staleness", string("current")),
                ("consumable", V::Bool(true)),
            ]),
        );
        import_kinds.insert(id.into(), string(kind));
        payloads.insert(id.into(), payload);
        observations.insert(id.into(), observation);
        imports.insert(id.into(), wrapper);
        expected_import_refs.push(record([
            ("domain", string("import")),
            ("digest", string(id.split_once(':').ok_or(Error::Law)?.1)),
        ]));
    }
    let mut actual_import_refs = Vec::new();
    for rf in evaluation_refs {
        step(&mut r.work)?;
        if field(rf, "domain")? == &string("import") {
            actual_import_refs.push(rf.clone());
        }
    }
    if set(actual_import_refs)? != set(expected_import_refs)? {
        return Err(Error::Refused("EVALUATOR_IMPORT_INPUT_TOTALITY".into()));
    }
    let mut required_evidence = BTreeMap::new();
    for rule in arr(field(checked.policy().policy(), "rules")?)? {
        step(&mut r.work)?;
        let mut defs = Vec::new();
        if field(rule, "enabled")? == &V::Bool(true) {
            for usage in arr(field(rule, "evidenceUse")?)? {
                step(&mut r.work)?;
                if field(usage, "requirement")? == &string("required")
                    && !import_kinds
                        .values()
                        .any(|v| Some(v) == obj(usage).ok().and_then(|u| u.get("kind")))
                {
                    let mut d = obj(&deficiency(
                        "import",
                        "evidence-kind-unavailable",
                        vec![],
                        V::Null,
                        V::Null,
                    )?)?
                    .clone();
                    d.insert("evidenceKind".into(), field(usage, "kind")?.clone());
                    defs.push(V::Object(d));
                }
            }
        }
        required_evidence.insert(text(field(rule, "ruleId")?)?.into(), V::Array(defs));
    }
    let capture = record([
        ("domain", string("execution-inputs")),
        (
            "digest",
            string(&digest_hex(&checked.execution_inputs().input_digest())),
        ),
    ]);
    let mut execution_deficiencies = Vec::new();
    for row in arr(field(
        checked.execution_inputs().value(),
        "requiredCellDeficiencies",
    )?)? {
        step(&mut r.work)?;
        let cell = arr(field(enumeration, "cells")?)?
            .get(index(field(row, "cellOrdinal")?)?)
            .ok_or(Error::Law)?;
        let binding = arr(field(cell, "programBindings")?)?
            .get(index(field(row, "programOrdinal")?)?)
            .ok_or(Error::Law)?;
        let cause = obj(row)?.get("deficiency").unwrap_or(&V::Null);
        let cause = if cause == &V::Null || cause == &string("source-syntax-invalid") {
            "required-cell-unsatisfied"
        } else {
            text(cause)?
        };
        if ![
            "budget-exhausted",
            "confidence-floor-unmet",
            "derivation-policy-unmet",
            "external-consumers-unknown",
            "input-closure-incomplete",
            "language-tier-unsupported",
            "provider-unavailable",
            "required-cell-unsatisfied",
            "required-relation-missing",
            "resolution-incomplete",
            "work-budget-exhausted",
        ]
        .contains(&cause)
        {
            return Err(Error::Refused(
                "EVALUATOR_EXECUTION_CAUSE_UNREGISTERED".into(),
            ));
        }
        let mut refs = vec![capture.clone()];
        refs.extend_from_slice(arr(field(row, "inputRefs")?)?);
        let mut d = obj(&deficiency(
            "execution",
            cause,
            refs,
            V::Null,
            field(row, "nativeCause")?.clone(),
        )?)?
        .clone();
        d.insert("universe".into(), field(binding, "universe")?.clone());
        execution_deficiencies.push(V::Object(d));
    }
    let mut targets = BTreeMap::new();
    let mut incoming = Vec::new();
    for rf in evaluation_refs {
        step(&mut r.work)?;
        match text(field(rf, "domain")?)? {
            "target-attribution" => {
                let value = r.record(field(rf, "digest")?)?;
                let fid = text(field(&value, "sourceFactId")?)?;
                if field(&value, "planId")? != &string(plan_id) || !facts.contains_key(fid) {
                    return Err(Error::Refused(
                        "EVALUATOR_TARGET_ATTRIBUTION_INPUT_JOIN".into(),
                    ));
                }
                if targets.insert(fid.into(), value).is_some() {
                    return Err(Error::Refused(
                        "EVALUATOR_TARGET_ATTRIBUTION_DUPLICATE".into(),
                    ));
                }
            }
            "incoming-search" => incoming.push(r.record(field(rf, "digest")?)?),
            _ => {}
        }
    }
    let mut row_count = 0;
    for inv in &inventories {
        step(&mut r.work)?;
        add_count(&mut row_count, arr(field(inv, "rows")?)?.len())?;
    }
    let refs = set(evaluation_refs.to_vec())?;
    let normalized = record([
        (
            "executionInputsDigest",
            string(&digest_hex(&checked.execution_inputs().input_digest())),
        ),
        ("plan", plan.clone()),
        ("planId", string(plan_id)),
        ("executionPlanId", string(execution_id)),
        ("evaluatorClosure", string(evaluator_closure)),
        ("policy", checked.policy().policy().clone()),
        ("effectiveWaivers", checked.policy().waiver().clone()),
        ("emissionPlan", parameters.emission().clone()),
        ("population", field(&derived, "population")?.clone()),
        ("enumerations", field(&derived, "enumerations")?.clone()),
        (
            "enumerationDeficiencies",
            field(&derived, "enumerationDeficiencies")?.clone(),
        ),
        ("requiredEvidenceDeficiencies", V::Object(required_evidence)),
        ("executionDeficiencies", set(execution_deficiencies)?),
        ("evaluationInputRefs", refs.clone()),
        ("inventoryRowCount", number(row_count)?),
        (
            "inventoryLocatorCount",
            field(enumeration_check.value(), "expectedRecords")?.clone(),
        ),
        ("factCount", number(facts.len())?),
        ("observationCount", number(observation_count)?),
        ("coverageCount", number(coverages.len())?),
        ("importKinds", V::Object(import_kinds)),
        ("closures", V::Object(closures.clone())),
    ]);
    let evidence = record([
        ("planId", string(plan_id)),
        ("enumerationPlan", enumeration.clone()),
        ("inventories", V::Array(inventories)),
        ("facts", V::Object(facts)),
        ("scopes", V::Object(scopes)),
        ("coverages", V::Object(coverages)),
        ("universeDomains", V::Object(universe_domains)),
        ("closures", V::Object(closures)),
        ("evaluationInputRefs", refs),
        ("planSelectedImportIds", field(&plan, "importIds")?.clone()),
        ("imports", V::Object(imports)),
        ("importPayloads", V::Object(payloads)),
        ("importObservations", V::Object(observations)),
        ("targetAttributions", V::Object(targets)),
        ("incomingSearchAttestations", V::Array(incoming)),
        ("importScopes", V::Object(import_scopes)),
        ("importFlagsAdapter", V::Object(flags)),
        ("coverageScopes", V::Object(coverage_scopes)),
    ]);
    Ok(ReconstructedInputs {
        normalized,
        evidence,
    })
}
