//! Exact execution-input capture joins over private retained-derived maps.
//! Late semantic refusals retain diagnostics; no result mints Run authority.
use alloc::{borrow::ToOwned, collections::BTreeSet, string::String, vec::Vec};
use opensip_identity::{JsonValue as V, canonical_bytes};

#[derive(Debug, PartialEq, Eq)]
enum Error {
    Shape,
    Limit,
    Record(opensip_identity::GraphError),
}
fn field<'a>(v: &'a V, key: &str) -> &'a V {
    match v {
        V::Object(o) => o.get(key).unwrap_or(&V::Null),
        _ => &V::Null,
    }
}
fn list(v: &V) -> Result<&[V], Error> {
    match v {
        V::Array(a) => Ok(a),
        V::Null => Ok(&[]),
        _ => Err(Error::Shape),
    }
}
fn is(v: &V, s: &str) -> bool {
    matches!(v, V::String(v) if v == s)
}
fn present(v: &V) -> bool {
    !matches!(v, V::Null)
}
fn text(s: &str) -> V {
    V::String(s.into())
}
fn obj<const N: usize>(rows: [(&str, V); N]) -> V {
    V::Object(
        rows.into_iter()
            .map(|(k, v)| (String::from(k), v))
            .collect(),
    )
}
fn maybe_one(v: &V) -> V {
    V::Array(if present(v) {
        alloc::vec![v.clone()]
    } else {
        Vec::new()
    })
}
fn charge(work: &mut usize) -> Result<(), Error> {
    *work = work.checked_sub(1).ok_or(Error::Limit)?;
    Ok(())
}
fn input_ref(domain: &str, digest: &V) -> V {
    obj([("domain", text(domain)), ("digest", digest.clone())])
}
fn carrier(source: &str, deficiency: &V, cause: &V, refs: V) -> V {
    obj([
        ("source", text(source)),
        ("deficiency", deficiency.clone()),
        ("nativeCause", cause.clone()),
        ("nativeCauses", maybe_one(cause)),
        ("inputRefs", refs),
    ])
}
fn applicability(
    relation: &str,
    universe: &V,
    enumerator: &str,
    matrix: &V,
    vcs: &V,
) -> &'static str {
    if relation == "vcs-change" && is(vcs, "none") {
        "inapplicable-vcs"
    } else if is(matrix, "UNSUPPORTED-TYPED") {
        "unsupported-typed"
    } else if enumerator == "unselected" {
        "unavailable-unselected"
    } else if !present(universe) {
        "unavailable-null-universe"
    } else {
        "supported-available"
    }
}
struct OutcomeInput<'a> {
    enumerator: &'a str,
    universe: &'a V,
    required: bool,
    inventories: &'a [V],
    accounts: &'a [V],
    candidate: &'a V,
    candidate_digest: &'a V,
    candidate_capability: bool,
    binding: &'a V,
}
fn outcome(input: OutcomeInput<'_>, work: &mut usize) -> Result<V, Error> {
    charge(work)?;
    let mut items = Vec::new();
    for inventory in input.inventories {
        charge(work)?;
        if !is(field(inventory, "state"), "complete") {
            items.push(carrier(
                "inventory",
                field(inventory, "deficiency"),
                field(inventory, "nativeCause"),
                V::Array(alloc::vec![input_ref(
                    "subject-inventory",
                    field(inventory, "digest")
                )]),
            ));
        }
    }
    let own_def = field(input.binding, "deficiency");
    let own_cause = field(input.binding, "nativeCause");
    if input.enumerator == "unselected" || !present(input.universe) {
        let default = text("provider-unavailable");
        let deficiency = if present(own_def) { own_def } else { &default };
        let (source, reason) = if input.enumerator == "unselected" {
            (
                "enumerator",
                if input.required {
                    "unavailable-binding"
                } else {
                    "optional-unselected"
                },
            )
        } else {
            ("binding", "unavailable-binding")
        };
        items.insert(
            0,
            carrier(source, deficiency, own_cause, V::Array(Vec::new())),
        );
        return finish_outcome("unavailable", text(reason), items, work);
    }
    if input.candidate_capability {
        if !present(input.candidate) {
            items.push(carrier(
                "candidate",
                own_def,
                own_cause,
                V::Array(Vec::new()),
            ));
        } else if !is(field(input.candidate, "state"), "complete") {
            let refs = if present(input.candidate_digest) {
                alloc::vec![input_ref(
                    "candidate-producer-result",
                    input.candidate_digest
                )]
            } else {
                Vec::new()
            };
            let def = field(input.candidate, "deficiency");
            let cause = field(input.candidate, "nativeCause");
            let mut item = carrier(
                "candidate",
                if present(def) { def } else { own_def },
                if present(cause) { cause } else { own_cause },
                V::Array(refs),
            );
            let causes = [cause, own_cause]
                .into_iter()
                .filter(|v| present(v))
                .cloned()
                .collect();
            if let V::Object(o) = &mut item {
                o.insert("nativeCauses".into(), V::Array(causes));
            }
            items.push(item);
        }
    }
    for account in input.accounts {
        charge(work)?;
        if ["complete", "inapplicable", "unsupported"]
            .iter()
            .any(|s| is(field(account, "accountState"), s))
        {
            continue;
        }
        let mut typed = false;
        for record in list(field(account, "coverageRecords"))? {
            charge(work)?;
            let def = field(record, "deficiency");
            let cause = field(record, "nativeCause");
            if !present(def) && !present(cause) {
                continue;
            }
            typed = true;
            let refs = if present(field(record, "inputRef")) {
                maybe_one(field(record, "inputRef"))
            } else {
                V::Array(list(field(account, "inputRefs"))?.to_vec())
            };
            let mut item = carrier("coverage", def, cause, refs);
            if let V::Object(o) = &mut item {
                for key in ["relation", "resolution"] {
                    o.insert(key.into(), field(account, key).clone());
                }
                o.insert("coverageId".into(), field(record, "coverageId").clone());
            }
            items.push(item);
        }
        if !typed {
            let mut item = carrier(
                "account",
                field(account, "deficiency"),
                field(account, "nativeCause"),
                V::Array(list(field(account, "inputRefs"))?.to_vec()),
            );
            if let V::Object(o) = &mut item {
                o.insert(
                    "nativeCauses".into(),
                    V::Array(list(field(account, "nativeCauses"))?.to_vec()),
                );
                for key in ["relation", "resolution"] {
                    o.insert(key.into(), field(account, key).clone());
                }
            }
            items.push(item);
        }
    }
    let state = if input.candidate_capability {
        if !present(input.candidate) || is(field(input.candidate, "state"), "unavailable") {
            "unavailable"
        } else if !items.is_empty() {
            "partial"
        } else {
            "complete"
        }
    } else if input
        .inventories
        .iter()
        .any(|v| is(field(v, "state"), "unavailable"))
        && !input
            .inventories
            .iter()
            .any(|v| is(field(v, "state"), "complete") || is(field(v, "state"), "partial"))
    {
        "unavailable"
    } else if !items.is_empty() {
        "partial"
    } else {
        "complete"
    };
    finish_outcome(state, V::Null, items, work)
}
fn finish_outcome(state: &str, reason: V, items: Vec<V>, work: &mut usize) -> Result<V, Error> {
    let mut primary = None;
    let mut causes = Vec::new();
    let mut refs = Vec::new();
    for item in &items {
        charge(work)?;
        if primary.is_none()
            && (present(field(item, "deficiency")) || present(field(item, "nativeCause")))
        {
            primary = Some(item);
        }
        let cause = field(item, "nativeCause");
        if present(cause) && !causes.contains(cause) {
            causes.push(cause.clone());
        }
        for cause in list(field(item, "nativeCauses"))? {
            charge(work)?;
            if !causes.contains(cause) {
                causes.push(cause.clone());
            }
        }
        for r in list(field(item, "inputRefs"))? {
            charge(work)?;
            refs.push(r.clone());
        }
    }
    let get = |key| {
        if state == "complete" {
            V::Null
        } else {
            primary.map(|p| field(p, key).clone()).unwrap_or(V::Null)
        }
    };
    Ok(obj([
        ("state", text(state)),
        ("stageOrdinalNullReason", reason),
        ("deficiency", get("deficiency")),
        ("nativeCause", get("nativeCause")),
        ("nativeCauses", V::Array(causes)),
        ("inputRefs", V::Array(refs)),
        ("sources", V::Array(items)),
    ]))
}
fn summarize_coverage(
    records: &[V],
    expected: &BTreeSet<String>,
    covered: &BTreeSet<String>,
    work: &mut usize,
) -> Result<V, Error> {
    charge(work)?;
    let mut missing = Vec::new();
    for s in expected.difference(covered) {
        charge(work)?;
        let v = text(s);
        let key = canonical_bytes(&v).map_err(|_| Error::Shape)?;
        missing.push((key, v));
    }
    missing.sort_by(|a, b| a.0.cmp(&b.0));
    let mut coverage = Vec::new();
    for record in records {
        charge(work)?;
        let entry = field(record, "entry");
        let rc = field(entry, "resolutionCompleteness");
        coverage.push(obj([
            ("coverageId", field(record, "id").clone()),
            ("deficiency", field(entry, "deficiency").clone()),
            ("nativeCause", field(entry, "nativeCause").clone()),
            ("inputRef", input_ref("coverage", field(record, "id"))),
            ("coverage", field(entry, "coverage").clone()),
            ("resolutionCompletenessState", field(rc, "state").clone()),
            (
                "examinedExhaustive",
                field(rc, "examinedExhaustive").clone(),
            ),
        ]));
    }
    let mut rc_states = Vec::new();
    let mut causes = Vec::new();
    let mut defs = Vec::new();
    let mut primary = None;
    let mut complete = !coverage.is_empty() && missing.is_empty();
    let mut exhaustive = true;
    for record in &coverage {
        charge(work)?;
        complete &= is(field(record, "coverage"), "complete")
            && field(record, "examinedExhaustive") == &V::Bool(true);
        exhaustive &= field(record, "examinedExhaustive") == &V::Bool(true);
        rc_states.push(field(record, "resolutionCompletenessState"));
        let def = field(record, "deficiency");
        let cause = field(record, "nativeCause");
        if present(def) {
            defs.push(def.clone());
        }
        if present(cause) {
            causes.push(cause.clone());
        }
        if primary.is_none() && (present(def) || present(cause)) {
            primary = Some((def.clone(), cause.clone()));
        }
    }
    let rc_state = if let Some(first) = rc_states.first() {
        if rc_states.iter().all(|s| s == first) {
            (*first).clone()
        } else if rc_states.iter().any(|s| {
            ["incomplete", "partial", "not-attempted"]
                .iter()
                .any(|n| is(s, n))
        }) {
            text("incomplete")
        } else {
            (*first).clone()
        }
    } else {
        V::Null
    };
    let (def, cause) = if complete {
        (V::Null, V::Null)
    } else {
        primary.unwrap_or((V::Null, V::Null))
    };
    Ok(obj([
        (
            "accountState",
            text(if complete { "complete" } else { "incomplete" }),
        ),
        (
            "coverage",
            text(if complete { "complete" } else { "unknown" }),
        ),
        ("resolutionCompletenessState", rc_state),
        (
            "examinedExhaustive",
            if coverage.is_empty() {
                V::Null
            } else {
                V::Bool(exhaustive)
            },
        ),
        ("deficiency", def),
        ("nativeCause", cause),
        ("nativeCauses", V::Array(causes)),
        ("deficiencies", V::Array(defs)),
        (
            "censusMissing",
            V::Array(missing.into_iter().map(|(_, v)| v).collect()),
        ),
        ("coverageRecords", V::Array(coverage)),
    ]))
}

/// Logical promises only. The future retained reader will derive these maps;
/// this helper and its input maps are private and confer no owner authority.
struct PromiseInput<'a> {
    manifest: &'a V,
    plan: &'a V,
    execution: &'a V,
    enumeration: &'a V,
    objects: &'a alloc::collections::BTreeMap<String, (String, V)>,
    blobs: &'a alloc::collections::BTreeMap<String, Vec<u8>>,
}
fn add_string(set: &mut BTreeSet<String>, value: &V) {
    if let V::String(s) = value
        && !s.is_empty()
    {
        set.insert(s.clone());
    }
}
fn prefix(domain: &str, value: &V) -> V {
    let V::String(s) = value else {
        return value.clone();
    };
    let p = match domain {
        "view" => "view2",
        "coverage" => "coverage2",
        "import" => "import2",
        _ => return value.clone(),
    };
    if s.starts_with(&alloc::format!("{p}:")) {
        value.clone()
    } else {
        text(&alloc::format!("{p}:{s}"))
    }
}
fn ref_domain(reference: &V) -> &str {
    if let V::String(s) = field(reference, "domain") {
        s
    } else {
        ""
    }
}
fn blob_domain(domain: &str) -> bool {
    matches!(
        domain,
        "subject-inventory"
            | "candidate-producer-result"
            | "target-attribution"
            | "incoming-search"
    )
}
fn promises(input: PromiseInput<'_>, work: &mut usize) -> Result<V, Error> {
    charge(work)?;
    let mut objects = BTreeSet::new();
    let mut blobs = BTreeSet::new();
    for key in ["planId", "executionPlanId", "evaluatorClosure"] {
        add_string(&mut objects, field(input.manifest, key));
    }
    for key in ["analysisSpecDigest", "enumerationPlanDigest"] {
        add_string(&mut blobs, field(input.manifest, key));
    }
    for reference in list(field(input.manifest, "selectedRefs"))? {
        charge(work)?;
        let domain = ref_domain(reference);
        let digest = field(reference, "digest");
        if !matches!(digest, V::String(_)) {
            continue;
        }
        if matches!(domain, "view" | "coverage" | "import") {
            add_string(&mut objects, &prefix(domain, digest));
        } else if blob_domain(domain) {
            add_string(&mut blobs, digest);
        }
    }
    for row in list(field(input.manifest, "cellOutcomes"))? {
        charge(work)?;
        add_string(&mut objects, field(row, "enumeratorClosure"));
        for d in list(field(row, "inventoryDigests"))? {
            charge(work)?;
            add_string(&mut blobs, d);
        }
        add_string(&mut blobs, field(row, "candidateResultDigest"));
        for d in list(field(row, "viewDigests"))? {
            charge(work)?;
            add_string(&mut objects, &prefix("view", d));
        }
    }
    let capture = field(input.manifest, "hostCapture");
    for receipt in list(field(capture, "stageReceipts"))? {
        charge(work)?;
        add_string(&mut blobs, field(receipt, "stageSpecDigest"));
        add_string(&mut objects, field(receipt, "producerClosure"));
        for reference in list(field(receipt, "outputRefs"))? {
            charge(work)?;
            let domain = ref_domain(reference);
            let digest = field(reference, "digest");
            if matches!(domain, "view" | "coverage" | "import") && matches!(digest, V::String(_)) {
                add_string(&mut objects, &prefix(domain, digest));
            }
        }
    }
    for reference in list(field(capture, "hostDerivedRefs"))? {
        charge(work)?;
        if blob_domain(ref_domain(reference)) {
            add_string(&mut blobs, field(reference, "digest"));
        }
    }
    for digest in list(field(input.manifest, "candidateResultRefs"))? {
        charge(work)?;
        add_string(&mut blobs, digest);
    }
    add_string(&mut objects, field(input.plan, "snapshotId"));
    for id in list(field(input.plan, "importIds"))? {
        charge(work)?;
        add_string(&mut objects, id);
    }
    for key in ["analysisSpecDigest", "vcsDigest"] {
        add_string(&mut blobs, field(input.plan, key));
    }
    for stage in list(field(input.execution, "stages"))? {
        charge(work)?;
        add_string(&mut blobs, field(stage, "stageSpecDigest"));
    }
    add_string(&mut objects, field(input.enumeration, "snapshotId"));
    for key in ["membershipDigest", "scopeDigest"] {
        add_string(&mut blobs, field(input.enumeration, key));
    }
    // Exactly one pass of the initial object set, as selected X specifies.
    // Newly discovered keys are promises but are not recursively walked here.
    let initial: Vec<_> = objects.iter().cloned().collect();
    for key in initial {
        charge(work)?;
        let Some((domain, value)) = input.objects.get(&key) else {
            continue;
        };
        if !matches!(value, V::Object(_)) {
            continue;
        }
        match domain.as_str() {
            "view" => {
                add_string(&mut objects, field(value, "producerClosure"));
                add_string(&mut objects, field(value, "planId"));
                for id in list(field(value, "coverageIds"))? {
                    charge(work)?;
                    if matches!(id,V::String(s) if s.contains(':')) {
                        add_string(&mut objects, id);
                    } else {
                        add_string(&mut objects, &prefix("coverage", id));
                    }
                }
                for id in list(field(value, "scopeIds"))? {
                    charge(work)?;
                    add_string(&mut objects, id);
                }
            }
            "coverage" => {
                add_string(&mut blobs, field(value, "payloadDigest"));
                add_string(&mut objects, field(value, "scopeId"));
            }
            "snapshot" => add_string(&mut blobs, field(value, "vcsDigest")),
            "plan" => {
                add_string(&mut objects, field(value, "snapshotId"));
                add_string(&mut blobs, field(value, "analysisSpecDigest"));
            }
            _ => (),
        }
    }
    let initial: Vec<_> = blobs.iter().cloned().collect();
    for digest in initial {
        charge(work)?;
        let Some(raw) = input.blobs.get(&digest) else {
            continue;
        };
        let Ok(parsed) = opensip_identity::parse_json(raw) else {
            continue;
        };
        let V::Object(value) = &parsed else {
            continue;
        };
        if value.contains_key("groupDigests") || value.contains_key("sourceBodies") {
            for d in list(field(&parsed, "groupDigests"))? {
                charge(work)?;
                add_string(&mut blobs, d);
            }
            for body in list(field(&parsed, "sourceBodies"))? {
                charge(work)?;
                add_string(&mut blobs, field(body, "contentSha256"));
            }
        }
    }
    let object_keys: Vec<_> = objects.into_iter().map(V::String).collect();
    let mut blob_keys = Vec::new();
    for b in blobs {
        charge(work)?;
        let value = V::String(b);
        let key = canonical_bytes(&value).map_err(|_| Error::Shape)?;
        blob_keys.push((key, value));
    }
    blob_keys.sort_by(|a, b| a.0.cmp(&b.0));
    let blob_keys: Vec<_> = blob_keys.into_iter().map(|(_, v)| v).collect();
    let pointers = object_keys.iter().chain(&blob_keys).cloned().collect();
    Ok(obj([
        ("objectKeys", V::Array(object_keys)),
        ("blobDigests", V::Array(blob_keys)),
        ("store_pointers", V::Array(pointers)),
    ]))
}

fn add_fault(faults: &mut Vec<String>, name: &str) {
    if !faults.iter().any(|s| s == name) {
        faults.push(name.into());
    }
}
fn canonical_set(values: &[V], work: &mut usize) -> Result<Vec<Vec<u8>>, Error> {
    let mut out = Vec::new();
    for v in values {
        charge(work)?;
        out.push(canonical_bytes(v).map_err(|_| Error::Shape)?);
    }
    out.sort();
    out.dedup();
    Ok(out)
}
fn canonical_set_ok(values: &V, work: &mut usize) -> Result<bool, Error> {
    let V::Array(values) = values else {
        return Ok(false);
    };
    let mut prior = None;
    for value in values {
        charge(work)?;
        let key = canonical_bytes(value).map_err(|_| Error::Shape)?;
        if prior.as_ref().is_some_and(|p| p >= &key) {
            return Ok(false);
        }
        prior = Some(key);
    }
    Ok(true)
}
fn ordinal(value: &V) -> Result<usize, Error> {
    let V::Integer(n) = value else {
        return Err(Error::Shape);
    };
    usize::try_from(n.get()).map_err(|_| Error::Shape)
}
fn string_value(value: &V) -> Result<&str, Error> {
    let V::String(s) = value else {
        return Err(Error::Shape);
    };
    Ok(s)
}
fn ref_pair(reference: &V) -> Result<(String, String), Error> {
    Ok((
        string_value(field(reference, "domain"))?.into(),
        string_value(field(reference, "digest"))?.into(),
    ))
}
fn canonical_digest(value: &V) -> Result<V, Error> {
    let bytes = canonical_bytes(value).map_err(|_| Error::Shape)?;
    Ok(text(&opensip_identity::digest_hex(
        &opensip_identity::raw_sha256(&bytes),
    )))
}
struct CaptureInput<'a> {
    plan_id: &'a str,
    execution_id: &'a str,
    plan: &'a V,
    execution: &'a V,
    enumeration: &'a V,
    analysis: &'a V,
    manifest: &'a V,
    closures: &'a alloc::collections::BTreeMap<String, V>,
    stages: &'a alloc::collections::BTreeMap<String, V>,
}
/// Header and receipt joins assume retained/schema owner checks have completed.
/// Raw input-selection admission and the full account/candidate join are separate.
fn capture_header(
    input: &CaptureInput<'_>,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<(), Error> {
    charge(work)?;
    if !is(field(input.manifest, "planId"), input.plan_id)
        || field(input.manifest, "analysisSpecDigest") != field(input.plan, "analysisSpecDigest")
        || field(input.manifest, "analysisSpecDigest") != &canonical_digest(input.analysis)?
    {
        add_fault(faults, "EXECUTION_INPUTS_PLAN_JOIN");
    }
    if field(input.manifest, "enumerationPlanDigest") != &canonical_digest(input.enumeration)? {
        add_fault(faults, "EXECUTION_INPUTS_ENUMERATION_DIGEST");
    }
    if !is(field(input.manifest, "executionPlanId"), input.execution_id)
        || !is(field(input.execution, "planId"), input.plan_id)
    {
        add_fault(faults, "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN");
    }
    let evaluator = field(input.manifest, "evaluatorClosure");
    if !list(field(input.plan, "semanticClosures"))?.contains(evaluator)
        || !input
            .closures
            .get(string_value(evaluator)?)
            .is_some_and(|v| is(field(v, "kind"), "evaluator"))
    {
        add_fault(faults, "EXECUTION_INPUTS_EVALUATOR_CLOSURE");
    }
    let tuple = |v: &V| {
        obj([
            ("capabilityId", field(v, "capabilityId").clone()),
            ("languageMode", field(v, "languageMode").clone()),
            ("workspaceRoot", field(v, "workspaceRoot").clone()),
            ("required", field(v, "required").clone()),
        ])
    };
    let requested = list(field(input.analysis, "requestedCapabilities"))?;
    let cells = list(field(input.enumeration, "cells"))?;
    let mut a = Vec::new();
    let mut b = Vec::new();
    for v in requested {
        charge(work)?;
        a.push(canonical_bytes(&tuple(v)).map_err(|_| Error::Shape)?);
    }
    for v in cells {
        charge(work)?;
        b.push(canonical_bytes(&tuple(v)).map_err(|_| Error::Shape)?);
    }
    a.sort();
    b.sort();
    if a != b {
        add_fault(faults, "EXECUTION_INPUTS_CELL_TOTALITY");
    }
    if !canonical_set_ok(field(input.manifest, "selectedRefs"), work)?
        || !canonical_set_ok(field(input.manifest, "candidateResultRefs"), work)?
    {
        add_fault(faults, "EXECUTION_INPUTS_ORDER");
    }
    for reference in list(field(input.manifest, "selectedRefs"))? {
        charge(work)?;
        if matches!(
            ref_domain(reference),
            "proof-bundle" | "finding" | "evaluation-seal" | "run" | "semantic-evidence"
        ) {
            add_fault(faults, "EXECUTION_INPUTS_OUTPUT_BACKLINK");
        }
    }
    Ok(())
}
struct ReceiptChecks {
    captured: Vec<V>,
    by_ordinal: alloc::collections::BTreeMap<usize, V>,
}
fn capture_receipts(
    input: &CaptureInput<'_>,
    store: &ExecutionStore<'_>,
    views: &mut alloc::collections::BTreeMap<String, V>,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<ReceiptChecks, Error> {
    charge(work)?;
    let receipts = list(field(field(input.manifest, "hostCapture"), "stageReceipts"))?;
    let stages = list(field(input.execution, "stages"))?;
    let mut stage_ord = Vec::new();
    let mut receipt_ord = Vec::new();
    for s in stages {
        charge(work)?;
        stage_ord.push(ordinal(field(s, "ordinal"))?);
    }
    for r in receipts {
        charge(work)?;
        receipt_ord.push(ordinal(field(r, "ordinal"))?);
    }
    let ordered = receipt_ord.iter().copied().eq(0..receipts.len());
    stage_ord.sort();
    receipt_ord.sort();
    if !ordered || stage_ord != receipt_ord || receipt_ord.windows(2).any(|p| p[0] == p[1]) {
        add_fault(faults, "EXECUTION_INPUTS_RECEIPT_TOTALITY");
    }
    let mut captured = Vec::new();
    let mut by_ordinal = alloc::collections::BTreeMap::new();
    for receipt in receipts {
        charge(work)?;
        if !canonical_set_ok(field(receipt, "outputRefs"), work)?
            || !canonical_set_ok(field(receipt, "outputDomains"), work)?
        {
            add_fault(faults, "EXECUTION_INPUTS_ORDER");
        }
        let so = ordinal(field(receipt, "ordinal"))?;
        by_ordinal.insert(so, receipt.clone());
        let Some(stage) = stages
            .get(so)
            .filter(|s| ordinal(field(s, "ordinal")) == Ok(so))
        else {
            add_fault(faults, "EXECUTION_INPUTS_RECEIPT_TOTALITY");
            continue;
        };
        if field(stage, "stageSpecDigest") != field(receipt, "stageSpecDigest") {
            add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
        }
        let digest = string_value(field(receipt, "stageSpecDigest"))?;
        let fallback = if input.stages.get(digest).is_none_or(|v| v == &V::Null) {
            store.blobs.get(digest).and_then(|raw| {
                (opensip_identity::digest_hex(&opensip_identity::raw_sha256(raw)) == digest)
                    .then(|| opensip_identity::parse_json(raw).ok())
                    .flatten()
            })
        } else {
            None
        };
        let spec = input
            .stages
            .get(digest)
            .filter(|v| *v != &V::Null)
            .or(fallback.as_ref());
        if let Some(spec) = spec.filter(|v| matches!(v, V::Object(_))) {
            if field(receipt, "producerClosure") != field(spec, "producerClosure")
                || field(receipt, "outputDomains") != field(spec, "outputDomains")
                || field(spec, "outputDomains") != field(stage, "outputDomains")
            {
                add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
            }
        } else {
            add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
        }
        let refs = list(field(receipt, "outputRefs"))?;
        if is(field(receipt, "state"), "unavailable") && !refs.is_empty() {
            add_fault(faults, "EXECUTION_INPUTS_RECEIPT_TOTALITY");
        }
        for reference in refs {
            charge(work)?;
            if !list(field(receipt, "outputDomains"))?.contains(field(reference, "domain")) {
                add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
            }
            if is(field(receipt, "state"), "complete") {
                captured.push(reference.clone());
            }
            if ref_domain(reference) == "view" {
                let digest = string_value(field(reference, "digest"))?;
                if !views.contains_key(digest)
                    && let Some(value) = locate_object(store, "view", digest, faults, work)?
                {
                    views.insert(digest.into(), value);
                }
            }
        }
    }
    Ok(ReceiptChecks {
        captured,
        by_ordinal,
    })
}
/// Final exact semantic selection, never ambient store census. `views` must
/// have been resolved by the retained owner; its map is not a public argument.
fn selected_cover(
    input: &CaptureInput<'_>,
    captured: &[V],
    inventories: &BTreeSet<String>,
    candidates: &[String],
    views: &alloc::collections::BTreeMap<String, V>,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<(), Error> {
    charge(work)?;
    let host = list(field(
        field(input.manifest, "hostCapture"),
        "hostDerivedRefs",
    ))?;
    if !canonical_set_ok(
        field(field(input.manifest, "hostCapture"), "hostDerivedRefs"),
        work,
    )? {
        add_fault(faults, "EXECUTION_INPUTS_ORDER");
    }
    let mut host_set = BTreeSet::new();
    for r in host {
        charge(work)?;
        host_set.insert(ref_pair(r)?);
    }
    for (domain, digest) in &host_set {
        charge(work)?;
        if !blob_domain(domain) {
            add_fault(faults, "EXECUTION_INPUTS_HOST_DERIVED");
        }
        for receipt in list(field(field(input.manifest, "hostCapture"), "stageReceipts"))? {
            charge(work)?;
            if !is(field(receipt, "state"), "complete") {
                continue;
            }
            for r in list(field(receipt, "outputRefs"))? {
                charge(work)?;
                if ref_pair(r)? == (domain.clone(), digest.clone())
                    && !list(field(receipt, "outputDomains"))?.contains(&text(domain))
                {
                    add_fault(faults, "EXECUTION_INPUTS_HOST_DERIVED");
                }
            }
        }
    }
    let mut owed = BTreeSet::new();
    for d in inventories {
        charge(work)?;
        owed.insert((String::from("subject-inventory"), d.clone()));
    }
    for d in candidates {
        charge(work)?;
        owed.insert((String::from("candidate-producer-result"), d.clone()));
    }
    if host_set
        .difference(&owed)
        .any(|(domain, _)| !matches!(domain.as_str(), "target-attribution" | "incoming-search"))
        || owed.difference(&host_set).next().is_some()
    {
        add_fault(faults, "EXECUTION_INPUTS_HOST_DERIVED");
    }
    let mut expected = BTreeSet::new();
    let mut captured_views = BTreeSet::new();
    for r in captured {
        charge(work)?;
        let pair = ref_pair(r)?;
        if pair.0 == "view" {
            captured_views.insert(pair.1.clone());
        }
        expected.insert(pair);
    }
    for id in captured_views {
        charge(work)?;
        expected.insert((String::from("view"), id.clone()));
        if let Some(view) = views.get(&id) {
            for cid in list(field(view, "coverageIds"))? {
                charge(work)?;
                let cid = string_value(cid)?;
                expected.insert((
                    String::from("coverage"),
                    cid.split_once(':').map_or(cid, |(_, h)| h).into(),
                ));
            }
        }
    }
    expected.extend(host_set.iter().cloned());
    for iid in list(field(input.plan, "importIds"))? {
        charge(work)?;
        let iid = string_value(iid)?;
        expected.insert((
            String::from("import"),
            iid.split_once(':').map_or(iid, |(_, h)| h).into(),
        ));
    }
    let mut actual = BTreeSet::new();
    for r in list(field(input.manifest, "selectedRefs"))? {
        charge(work)?;
        actual.insert(ref_pair(r)?);
    }
    if actual != expected {
        add_fault(faults, "EXECUTION_INPUTS_SELECTED_COVER");
    }
    let selected_blob = actual
        .into_iter()
        .filter(|(d, _)| blob_domain(d))
        .collect::<BTreeSet<_>>();
    if selected_blob != host_set {
        add_fault(faults, "EXECUTION_INPUTS_HOST_DERIVED");
    }
    Ok(())
}

fn registry() -> Result<V, Error> {
    opensip_identity::parse_json(include_bytes!("execution-registry.json"))
        .map_err(|_| Error::Shape)
}
fn canonical_strings(
    values: impl IntoIterator<Item = String>,
    work: &mut usize,
) -> Result<Vec<String>, Error> {
    let mut ordered = alloc::collections::BTreeMap::new();
    for s in values {
        charge(work)?;
        let key = canonical_bytes(&text(&s)).map_err(|_| Error::Shape)?;
        ordered.insert(key, s);
    }
    Ok(ordered.into_values().collect())
}
fn capability_kinds(law: &V, cap: &V, work: &mut usize) -> Result<Vec<String>, Error> {
    let values = field(field(law, "kindMap"), string_value(cap)?);
    canonical_strings(
        list(values)?.iter().filter_map(|v| {
            if let V::String(s) = v {
                Some(s.clone())
            } else {
                None
            }
        }),
        work,
    )
}
fn matrix_pairs<'a>(law: &'a V, cap: &V) -> Result<&'a [V], Error> {
    for row in list(field(law, "capabilities"))? {
        if field(row, "id") == cap {
            return list(field(row, "relations"));
        }
    }
    Ok(&[])
}
struct Binding<'a> {
    ci: usize,
    pi: usize,
    cell: &'a V,
    binding: &'a V,
}
fn bindings<'a>(enumeration: &'a V, work: &mut usize) -> Result<Vec<Binding<'a>>, Error> {
    let mut out = Vec::new();
    for (ci, cell) in list(field(enumeration, "cells"))?.iter().enumerate() {
        charge(work)?;
        for binding in list(field(cell, "programBindings"))? {
            charge(work)?;
            out.push(Binding {
                ci,
                pi: ordinal(field(binding, "ordinal"))?,
                cell,
                binding,
            });
        }
    }
    Ok(out)
}
struct CellInputs<'a> {
    views: &'a alloc::collections::BTreeMap<String, V>,
    objects: &'a alloc::collections::BTreeMap<String, (String, V)>,
    inventories: &'a alloc::collections::BTreeMap<String, V>,
}
struct CellChecks {
    view_hexes: alloc::collections::BTreeMap<(usize, usize), Vec<String>>,
    inventory_records: alloc::collections::BTreeMap<(usize, usize), Vec<V>>,
    inventory_named: BTreeSet<String>,
    candidates: Vec<String>,
}
fn candidate_capability(cap: &V) -> bool {
    is(cap, "clones-near") || is(cap, "clones-cross-tsjs")
}
fn check_cell_rows(
    input: &CaptureInput<'_>,
    records: &CellInputs<'_>,
    bindings: &[Binding<'_>],
    law: &V,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<CellChecks, Error> {
    let rows = list(field(input.manifest, "cellOutcomes"))?;
    let mut out = CellChecks {
        view_hexes: alloc::collections::BTreeMap::new(),
        inventory_records: alloc::collections::BTreeMap::new(),
        inventory_named: BTreeSet::new(),
        candidates: Vec::new(),
    };
    // Count and ordinal checks occur before stage receipt checks in full X.
    // The orchestration must call check_outcome_ordinals at that position.
    for (row, b) in rows.iter().zip(bindings) {
        charge(work)?;
        if ordinal(field(row, "cellOrdinal"))? != b.ci
            || ordinal(field(row, "programOrdinal"))? != b.pi
            || ["capabilityId", "languageMode", "workspaceRoot", "required"]
                .iter()
                .any(|k| field(row, k) != field(b.cell, k))
        {
            add_fault(faults, "EXECUTION_INPUTS_CELL_TOTALITY");
        }
        let kinds = capability_kinds(law, field(b.cell, "capabilityId"), work)?;
        let kinds_v = V::Array(kinds.iter().map(|s| text(s)).collect());
        if field(row, "kinds") != &kinds_v || field(b.cell, "kinds") != &kinds_v {
            add_fault(faults, "EXECUTION_INPUTS_KIND_MAP");
        }
        let universe = field(b.binding, "universe");
        let enumerator = field(b.binding, "enumerator");
        let closure = field(enumerator, "closureId");
        if field(row, "universe") != universe {
            add_fault(faults, "EXECUTION_INPUTS_CELL_TOTALITY");
        }
        if field(row, "enumeratorStatus") != field(enumerator, "status") {
            add_fault(faults, "EXECUTION_INPUTS_ENUMERATOR");
        }
        if is(field(enumerator, "status"), "selected")
            && (field(row, "enumeratorClosure") != closure
                || !list(field(input.plan, "semanticClosures"))?.contains(closure)
                || !string_value(closure)
                    .ok()
                    .and_then(|k| input.closures.get(k))
                    .is_some_and(|v| is(field(v, "kind"), "provider")))
        {
            add_fault(faults, "EXECUTION_INPUTS_ENUMERATOR");
        }
        let mut relations = Vec::new();
        for pair in matrix_pairs(law, field(b.cell, "capabilityId"))? {
            charge(work)?;
            let pair = list(pair)?;
            if pair.len() == 2 {
                relations.push(pair[0].clone());
            }
        }
        let producer = field(row, "enumeratorClosure");
        let mut attributed = Vec::new();
        for (hx, view) in records.views {
            charge(work)?;
            if present(producer) && field(view, "producerClosure") != producer {
                continue;
            }
            if !is(field(view, "planId"), input.plan_id) {
                add_fault(faults, "EXECUTION_INPUTS_PLAN_JOIN");
                continue;
            }
            if !present(universe) {
                continue;
            }
            let mut same_scope = false;
            for sid in list(field(view, "scopeIds"))? {
                charge(work)?;
                if let Some((domain, scope)) = records.objects.get(string_value(sid)?)
                    && domain == "subject-scope"
                    && field(scope, "sourceUniverse") == universe
                    && (relations.is_empty() || relations.contains(field(scope, "relation")))
                {
                    same_scope = true;
                }
            }
            if !same_scope {
                continue;
            }
            attributed.push(hx.clone());
            for sid in list(field(view, "scopeIds"))? {
                charge(work)?;
                if let Some((domain, scope)) = records.objects.get(string_value(sid)?)
                    && domain == "subject-scope"
                    && field(scope, "sourceUniverse") != universe
                {
                    add_fault(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE");
                }
            }
        }
        let attributed = canonical_strings(attributed, work)?;
        if field(row, "viewDigests") != &V::Array(attributed.iter().map(|s| text(s)).collect()) {
            add_fault(faults, "EXECUTION_INPUTS_VIEW_TOTALITY");
        }
        out.view_hexes.insert((b.ci, b.pi), attributed);
        let mut inventories = Vec::new();
        if !kinds.is_empty() {
            if present(field(row, "candidateResultDigest")) {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED");
            }
            let mut got = Vec::new();
            for digest in list(field(row, "inventoryDigests"))? {
                charge(work)?;
                let key = string_value(digest)?;
                let Some(inv) = records.inventories.get(key) else {
                    add_fault(faults, "EXECUTION_INPUTS_INVENTORY_KIND");
                    continue;
                };
                let kind = string_value(field(inv, "kind"))?;
                got.push(String::from(kind));
                if !kinds.iter().any(|k| k == kind)
                    || ordinal(field(inv, "cellOrdinal"))? != b.ci
                    || ordinal(field(inv, "programOrdinal"))? != b.pi
                    || (present(field(inv, "planId")) && !is(field(inv, "planId"), input.plan_id))
                {
                    add_fault(faults, "EXECUTION_INPUTS_INVENTORY_KIND");
                }
                let mut row = match inv {
                    V::Object(v) => v.clone(),
                    _ => return Err(Error::Shape),
                };
                row.entry("digest".into()).or_insert_with(|| digest.clone());
                inventories.push(V::Object(row));
                out.inventory_named.insert(key.into());
            }
            got.sort();
            if got != kinds || got.windows(2).any(|p| p[0] == p[1]) {
                add_fault(faults, "EXECUTION_INPUTS_INVENTORY_KIND");
            }
        } else {
            if !list(field(row, "inventoryDigests"))?.is_empty() {
                add_fault(faults, "EXECUTION_INPUTS_INVENTORY_KIND");
            }
            let candidate = field(row, "candidateResultDigest");
            if field(b.cell, "required") == &V::Bool(true)
                && candidate_capability(field(b.cell, "capabilityId"))
                && !present(candidate)
            {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED");
            }
            if let V::String(d) = candidate {
                out.candidates.push(d.clone());
            }
        }
        out.inventory_records.insert((b.ci, b.pi), inventories);
    }
    Ok(out)
}
fn check_outcome_ordinals(
    manifest: &V,
    bindings: &[Binding<'_>],
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<(), Error> {
    let rows = list(field(manifest, "cellOutcomes"))?;
    if rows.len() != bindings.len() {
        add_fault(faults, "EXECUTION_INPUTS_CELL_TOTALITY");
    }
    for (i, row) in rows.iter().enumerate() {
        charge(work)?;
        if ordinal(field(row, "ordinal"))? != i {
            add_fault(faults, "EXECUTION_INPUTS_CELL_TOTALITY");
        }
    }
    Ok(())
}
fn expected_source_census(
    relation: &str,
    cell: &V,
    binding: &V,
    inventories: &[V],
    law: &V,
    work: &mut usize,
) -> Result<BTreeSet<String>, Error> {
    charge(work)?;
    if relation == "vcs-change" {
        return Ok(BTreeSet::new());
    }
    let relation_row = field(field(law, "relations"), relation);
    let kind = field(relation_row, "subjectKind");
    let primary = if is(kind, "source-path") {
        "file"
    } else if is(kind, "package-name") {
        "package"
    } else if is(kind, "symbol") {
        "symbol"
    } else {
        return Ok(BTreeSet::new());
    };
    let selected = inventories.iter().find(|v| is(field(v, "kind"), primary));
    let mut subjects = BTreeSet::new();
    if let Some(inv) = selected {
        for row in list(field(inv, "rows"))? {
            charge(work)?;
            let id = field(row, "nativeSubjectId");
            if primary == "file" && !present(id) {
                add_string(&mut subjects, field(row, "path"));
            } else {
                add_string(&mut subjects, id);
            }
        }
    } else if primary == "file" {
        for extent in list(field(binding, "extents"))? {
            charge(work)?;
            if is(field(extent, "kind"), "file") {
                for path in list(field(extent, "paths"))? {
                    charge(work)?;
                    add_string(&mut subjects, path);
                }
                break;
            }
        }
    }
    if primary == "file" && present(field(relation_row, "bodyIdentityJoin")) {
        let language = field(
            field(law, "languageModes"),
            string_value(field(cell, "languageMode"))?,
        );
        if let V::String(language) = language
            && let V::Object(suffixes) = field(field(law, "bodyEligibility"), language)
        {
            subjects.retain(|s| suffixes.keys().any(|suffix| s.ends_with(suffix)));
        }
    }
    Ok(subjects)
}

struct ExecutionStore<'a> {
    objects: &'a alloc::collections::BTreeMap<String, (String, V)>,
    blobs: &'a alloc::collections::BTreeMap<String, Vec<u8>>,
    pointers: &'a BTreeSet<String>,
}
fn locate_object(
    store: &ExecutionStore<'_>,
    domain: &str,
    digest: &str,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<Option<V>, Error> {
    charge(work)?;
    let key = string_value(&prefix(domain, &text(digest)))?.to_owned();
    if !store.pointers.contains(&key) && !store.pointers.contains(digest) {
        add_fault(faults, "EXECUTION_INPUTS_REF_POINTER");
        return Ok(None);
    }
    let Some((actual, value)) = store.objects.get(&key) else {
        add_fault(faults, "EXECUTION_INPUTS_REF_LOST_BYTES");
        return Ok(None);
    };
    if actual != domain {
        add_fault(faults, "EXECUTION_INPUTS_REF_MISMATCH");
        return Ok(None);
    }
    let minted = opensip_identity::hash_canonical_value(domain, value)
        .map(|h| prefix(domain, &text(&opensip_identity::digest_hex(&h))));
    if minted.as_ref() != Ok(&text(&key)) {
        add_fault(faults, "EXECUTION_INPUTS_REF_MISMATCH");
        return Ok(None);
    }
    Ok(Some(value.clone()))
}
fn parse_blob(
    store: &ExecutionStore<'_>,
    digest: &str,
    missing: &str,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<Option<V>, Error> {
    charge(work)?;
    let Some(raw) = store.blobs.get(digest) else {
        add_fault(faults, missing);
        return Ok(None);
    };
    if opensip_identity::digest_hex(&opensip_identity::raw_sha256(raw)) != digest {
        add_fault(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES");
        return Ok(None);
    }
    match opensip_identity::parse_json(raw) {
        Ok(value) => Ok(Some(value)),
        Err(_) => {
            add_fault(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES");
            Ok(None)
        }
    }
}
fn load_coverage(
    store: &ExecutionStore<'_>,
    hex: &str,
    universe: &V,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<Option<(V, V)>, Error> {
    let Some(envelope) = locate_object(store, "coverage", hex, faults, work)? else {
        return Ok(None);
    };
    let V::String(digest) = field(&envelope, "payloadDigest") else {
        add_fault(faults, "EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE");
        return Ok(None);
    };
    let Some(payload) = parse_blob(
        store,
        digest,
        "EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE",
        faults,
        work,
    )?
    else {
        return Ok(None);
    };
    if let Some((domain, scope)) = store
        .objects
        .get(string_value(field(&envelope, "scopeId"))?)
        && domain == "subject-scope"
        && present(universe)
        && field(scope, "sourceUniverse") != universe
    {
        add_fault(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE");
    }
    Ok(Some((envelope, payload)))
}
fn check_carrier(
    deficiency: &V,
    cause: &V,
    law: &V,
    faults: &mut Vec<String>,
) -> Result<(), Error> {
    if !present(deficiency) {
        if present(cause) {
            add_fault(faults, "EXECUTION_INPUTS_CAUSE_CARRIER");
        }
        return Ok(());
    }
    let row = field(field(law, "causeRegistry"), string_value(deficiency)?);
    if !present(row) {
        add_fault(faults, "EXECUTION_INPUTS_CAUSE_CARRIER");
        return Ok(());
    }
    let rule = field(row, "nativeCause");
    let allowed = list(field(row, "allowedCauses"))?;
    if (is(rule, "must-be-null") && present(cause))
        || (is(rule, "required") && !allowed.contains(cause))
        || (is(rule, "optional") && present(cause) && !allowed.contains(cause))
    {
        add_fault(faults, "EXECUTION_INPUTS_CAUSE_CARRIER");
    }
    Ok(())
}
struct AccountContext<'a> {
    input: &'a CaptureInput<'a>,
    records: &'a CellInputs<'a>,
    cells: &'a CellChecks,
    store: &'a ExecutionStore<'a>,
    law: &'a V,
    vcs_kind: &'a V,
}
fn returned_partitions(
    context: &AccountContext<'_>,
    b: &Binding<'_>,
    relation: &V,
    resolution: &V,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<Vec<(String, V, V)>, Error> {
    let mut found = alloc::collections::BTreeMap::new();
    let universe = field(b.binding, "universe");
    let producer = field(field(b.binding, "enumerator"), "closureId");
    for hx in context
        .cells
        .view_hexes
        .get(&(b.ci, b.pi))
        .into_iter()
        .flatten()
    {
        charge(work)?;
        let Some(view) = context.records.views.get(hx) else {
            continue;
        };
        if present(producer) && field(view, "producerClosure") != producer {
            continue;
        }
        for cid in list(field(view, "coverageIds"))? {
            charge(work)?;
            let cid = string_value(cid)?;
            let chx = cid.split_once(':').map_or(cid, |(_, h)| h);
            let Some((env, payload)) = load_coverage(context.store, chx, universe, faults, work)?
            else {
                continue;
            };
            let key = field(&payload, "key");
            if field(key, "relation") != relation
                || field(key, "resolution") != resolution
                || (present(universe) && field(key, "sourceUniverse") != universe)
            {
                continue;
            }
            if let Some((domain, scope)) = context
                .store
                .objects
                .get(string_value(field(&env, "scopeId"))?)
                && domain == "subject-scope"
            {
                let enumerator = field(scope, "enumeratorClosure");
                if present(producer) && present(enumerator) && enumerator != producer {
                    continue;
                }
                if present(universe) && field(scope, "sourceUniverse") != universe {
                    continue;
                }
            }
            found.insert(String::from(chx), (env, payload));
        }
    }
    let keys = canonical_strings(found.keys().cloned(), work)?;
    let mut out = Vec::new();
    for key in keys {
        let (env, payload) = found.remove(&key).ok_or(Error::Shape)?;
        out.push((key, env, payload));
    }
    Ok(out)
}
fn integer(n: usize) -> Result<V, Error> {
    Ok(V::Integer(
        opensip_identity::JsonInteger::new(n as i128).map_err(|_| Error::Shape)?,
    ))
}
fn merge(base: V, items: impl IntoIterator<Item = (&'static str, V)>) -> Result<V, Error> {
    let V::Object(mut base) = base else {
        return Err(Error::Shape);
    };
    for (k, v) in items {
        base.insert(k.into(), v);
    }
    Ok(V::Object(base))
}
fn account_coordinates(b: &Binding<'_>, relation: &V, resolution: &V) -> Result<V, Error> {
    Ok(obj([
        ("cellOrdinal", integer(b.ci)?),
        ("programOrdinal", integer(b.pi)?),
        ("relation", relation.clone()),
        ("resolution", resolution.clone()),
    ]))
}
fn deficiency_base(b: &Binding<'_>, cause: &str) -> Result<V, Error> {
    Ok(obj([
        ("source", text("execution")),
        ("cause", text(cause)),
        ("cellOrdinal", integer(b.ci)?),
        ("programOrdinal", integer(b.pi)?),
        ("capabilityId", field(b.cell, "capabilityId").clone()),
        ("required", V::Bool(true)),
    ]))
}
fn special_account(state: &str, def: &V, cause: &V) -> V {
    obj([
        ("accountState", text(state)),
        ("coverage", V::Null),
        ("resolutionCompletenessState", V::Null),
        ("examinedExhaustive", V::Null),
        ("deficiency", def.clone()),
        ("nativeCause", cause.clone()),
        ("nativeCauses", maybe_one(cause)),
        ("deficiencies", maybe_one(def)),
        ("scopeIds", V::Array(Vec::new())),
        ("coverageRecords", V::Array(Vec::new())),
    ])
}
fn check_accounts(
    context: &AccountContext<'_>,
    bindings: &[Binding<'_>],
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<(Vec<V>, Vec<V>), Error> {
    let accounts = list(field(context.input.manifest, "nativeCoverageAccounts"))?;
    let mut have = Vec::new();
    let mut by_key = alloc::collections::BTreeMap::new();
    for account in accounts {
        charge(work)?;
        let key = (
            ordinal(field(account, "cellOrdinal"))?,
            ordinal(field(account, "programOrdinal"))?,
            string_value(field(account, "relation"))?.to_owned(),
            string_value(field(account, "resolution"))?.to_owned(),
        );
        have.push(key.clone());
        by_key.insert(key, account);
    }
    let mut owed = Vec::new();
    for b in bindings {
        charge(work)?;
        if candidate_capability(field(b.cell, "capabilityId")) {
            continue;
        }
        for pair in matrix_pairs(context.law, field(b.cell, "capabilityId"))? {
            charge(work)?;
            let pair = list(pair)?;
            if pair.len() == 2 {
                owed.push((b, &pair[0], &pair[1]));
            }
        }
    }
    let mut keys = owed
        .iter()
        .map(|(b, r, s)| {
            Ok((
                b.ci,
                b.pi,
                string_value(r)?.to_owned(),
                string_value(s)?.to_owned(),
            ))
        })
        .collect::<Result<Vec<_>, Error>>()?;
    keys.sort();
    have.sort();
    if keys != have {
        add_fault(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY");
    }
    let mut derived = Vec::new();
    let mut deficiencies = Vec::new();
    for (b, relation, resolution) in owed {
        charge(work)?;
        let key = (
            b.ci,
            b.pi,
            string_value(relation)?.to_owned(),
            string_value(resolution)?.to_owned(),
        );
        let Some(account) = by_key.get(&key) else {
            continue;
        };
        let matrix = list(field(context.law, "cells"))?
            .iter()
            .find(|row| {
                field(row, "capability") == field(b.cell, "capabilityId")
                    && field(row, "mode") == field(b.cell, "languageMode")
            })
            .unwrap_or(&V::Null);
        let universe = field(b.binding, "universe");
        let en = string_value(field(field(b.binding, "enumerator"), "status"))?;
        let want = applicability(
            string_value(relation)?,
            universe,
            en,
            field(matrix, "state"),
            context.vcs_kind,
        );
        if !is(field(account, "applicability"), want) {
            add_fault(
                faults,
                if want == "inapplicable-vcs"
                    || is(field(account, "applicability"), "inapplicable-vcs")
                {
                    "EXECUTION_INPUTS_VCS_APPLICABILITY"
                } else {
                    "EXECUTION_INPUTS_COVERAGE_DERIVE"
                },
            );
        }
        if field(account, "sourceUniverse") != universe {
            add_fault(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE");
        }
        let required = field(b.cell, "required") == &V::Bool(true);
        if want != "supported-available" {
            if !list(field(account, "coverageIds"))?.is_empty() {
                add_fault(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE");
            }
            let (state, def, cause, deficiency_cause) = if want == "unsupported-typed" {
                let def = field(matrix, "deficiency").clone();
                let rule = field(field(context.law, "causeRegistry"), string_value(&def)?);
                let allowed = list(field(rule, "allowedCauses"))?;
                let cause = if is(field(rule, "nativeCause"), "required") && allowed.len() == 1 {
                    allowed[0].clone()
                } else {
                    V::Null
                };
                check_carrier(&def, &cause, context.law, faults)?;
                ("unsupported", def, cause, Some("unsupported-typed"))
            } else if want == "inapplicable-vcs" {
                ("inapplicable", V::Null, V::Null, None)
            } else {
                let def = field(b.binding, "deficiency");
                (
                    "unavailable",
                    if present(def) {
                        def.clone()
                    } else {
                        text("provider-unavailable")
                    },
                    field(b.binding, "nativeCause").clone(),
                    Some("required-cell-unsatisfied"),
                )
            };
            if required && let Some(c) = deficiency_cause {
                deficiencies.push(merge(
                    deficiency_base(b, c)?,
                    [
                        ("relation", relation.clone()),
                        ("resolution", resolution.clone()),
                        ("deficiency", def.clone()),
                        ("nativeCause", cause.clone()),
                        ("inputRefs", V::Array(Vec::new())),
                    ],
                )?);
            }
            let V::Object(summary) = special_account(state, &def, &cause) else {
                return Err(Error::Shape);
            };
            let V::Object(mut full) = account_coordinates(b, relation, resolution)? else {
                return Err(Error::Shape);
            };
            full.extend(summary);
            derived.push(V::Object(full));
            continue;
        }
        let returned = returned_partitions(context, b, relation, resolution, faults, work)?;
        let returned_ids = returned
            .iter()
            .map(|(h, _, _)| h.clone())
            .collect::<Vec<_>>();
        let named = list(field(account, "coverageIds"))?;
        let named_strings = named
            .iter()
            .map(|v| string_value(v).map(String::from))
            .collect::<Result<Vec<_>, _>>()?;
        if canonical_strings(named_strings.clone(), work)?
            != canonical_strings(returned_ids.clone(), work)?
        {
            add_fault(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE");
        }
        let mut records = Vec::new();
        let mut scopes = Vec::new();
        let mut covered = BTreeSet::new();
        for (hx, env, payload) in &returned {
            charge(work)?;
            let entry = field(payload, "entry");
            let key = field(payload, "key");
            if field(key, "relation") != relation
                || field(key, "resolution") != resolution
                || field(key, "sourceUniverse") != universe
            {
                add_fault(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE");
            }
            check_carrier(
                field(entry, "deficiency"),
                field(entry, "nativeCause"),
                context.law,
                faults,
            )?;
            records.push(obj([("id", text(hx)), ("entry", entry.clone())]));
            scopes.push(string_value(field(env, "scopeId"))?.to_owned());
        }
        for hx in &named_strings {
            charge(work)?;
            if !returned_ids.contains(hx)
                && let Some((_, payload)) =
                    load_coverage(context.store, hx, universe, faults, work)?
            {
                let entry = field(&payload, "entry");
                check_carrier(
                    field(entry, "deficiency"),
                    field(entry, "nativeCause"),
                    context.law,
                    faults,
                )?;
                records.push(obj([("id", text(hx)), ("entry", entry.clone())]));
            }
        }
        let inv = context
            .cells
            .inventory_records
            .get(&(b.ci, b.pi))
            .map_or(&[][..], Vec::as_slice);
        let expected = expected_source_census(
            string_value(relation)?,
            b.cell,
            b.binding,
            inv,
            context.law,
            work,
        )?;
        for (_, env, _) in &returned {
            charge(work)?;
            if let Some((domain, scope)) = context
                .store
                .objects
                .get(string_value(field(env, "scopeId"))?)
                && domain == "subject-scope"
            {
                for subject in list(field(scope, "subjects"))? {
                    charge(work)?;
                    if let V::String(s) = subject {
                        covered.insert(s.clone());
                    }
                }
            }
        }
        let summary = summarize_coverage(&records, &expected, &covered, work)?;
        let refs = V::Array(named.iter().map(|h| input_ref("coverage", h)).collect());
        let summary = merge(
            summary,
            [
                (
                    "scopeIds",
                    V::Array(
                        canonical_strings(scopes, work)?
                            .iter()
                            .map(|s| text(s))
                            .collect(),
                    ),
                ),
                ("inputRefs", refs.clone()),
                ("relation", relation.clone()),
                ("resolution", resolution.clone()),
            ],
        )?;
        if !is(field(&summary, "accountState"), "complete") && required {
            let records = list(field(&summary, "coverageRecords"))?;
            if records.is_empty() {
                deficiencies.push(merge(
                    deficiency_base(b, "native-work-incomplete")?,
                    [
                        ("relation", relation.clone()),
                        ("resolution", resolution.clone()),
                        ("deficiency", field(&summary, "deficiency").clone()),
                        ("nativeCause", field(&summary, "nativeCause").clone()),
                        ("inputRefs", refs),
                    ],
                )?);
            } else {
                for record in records {
                    charge(work)?;
                    deficiencies.push(merge(
                        deficiency_base(b, "native-work-incomplete")?,
                        [
                            ("relation", relation.clone()),
                            ("resolution", resolution.clone()),
                            ("deficiency", field(record, "deficiency").clone()),
                            ("nativeCause", field(record, "nativeCause").clone()),
                            ("inputRefs", maybe_one(field(record, "inputRef"))),
                        ],
                    )?);
                }
            }
        }
        let V::Object(summary) = summary else {
            return Err(Error::Shape);
        };
        let V::Object(mut full) = account_coordinates(b, relation, resolution)? else {
            return Err(Error::Shape);
        };
        full.extend(summary);
        derived.push(V::Object(full));
    }
    Ok((derived, deficiencies))
}

fn shape(
    inputs: &opensip_identity::RetainedInputs<'_>,
    value: &V,
    document: &str,
    selector: &str,
    work: usize,
) -> Result<bool, Error> {
    use opensip_identity::{GraphError, SchemaAdmissionError, SchemaError};
    match inputs.check_current_value_shape(value, document, selector, work) {
        Ok(()) => Ok(true),
        Err(GraphError::Schema(SchemaAdmissionError::Mismatch)) => Ok(false),
        Err(GraphError::Schema(SchemaAdmissionError::Schema(SchemaError::Limit))) => {
            Err(Error::Limit)
        }
        Err(e) => Err(Error::Record(e)),
    }
}
fn locate_blob(
    store: &ExecutionStore<'_>,
    digest: &str,
    supplied: &alloc::collections::BTreeMap<String, V>,
    required: bool,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<Option<V>, Error> {
    charge(work)?;
    if !store.pointers.contains(digest) {
        add_fault(faults, "EXECUTION_INPUTS_REF_POINTER");
        return Ok(None);
    }
    let Some(value) = parse_blob(
        store,
        digest,
        "EXECUTION_INPUTS_REF_LOST_BYTES",
        faults,
        work,
    )?
    else {
        return Ok(None);
    };
    let mapped = supplied.get(digest);
    if required && mapped.is_none() {
        add_fault(faults, "EXECUTION_INPUTS_REF_POINTER");
        return Ok(None);
    }
    if mapped.is_some_and(|m| m != &value) {
        add_fault(faults, "EXECUTION_INPUTS_REF_MISMATCH");
        return Ok(None);
    }
    Ok(Some(value))
}
struct CandidateContext<'a> {
    input: &'a CaptureInput<'a>,
    store: &'a ExecutionStore<'a>,
    candidates: &'a alloc::collections::BTreeMap<String, V>,
    groups: &'a alloc::collections::BTreeMap<String, V>,
    snapshot: &'a alloc::collections::BTreeMap<String, V>,
    bindings: &'a [Binding<'a>],
    cells: &'a CellChecks,
    inputs: &'a opensip_identity::RetainedInputs<'a>,
    law: &'a V,
    schema_work: usize,
}
struct CandidateChecks {
    records: alloc::collections::BTreeMap<(usize, usize), V>,
    digests: alloc::collections::BTreeMap<(usize, usize), V>,
    deficiencies: Vec<V>,
}
fn candidate_extent(
    binding: &V,
    needed: &mut Vec<String>,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<Option<Vec<String>>, Error> {
    let value = field(binding, "candidateSourcePaths");
    let V::Object(object) = binding else {
        needed.push("EnumerationPlanV1.programBindings[].candidateSourcePaths on clones-near/clones-cross-tsjs (Plan-selected source census; empty kinds/extents is not complete-empty work)".into());
        add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
        return Ok(None);
    };
    if !object.contains_key("candidateSourcePaths") {
        needed.push("EnumerationPlanV1.programBindings[].candidateSourcePaths on clones-near/clones-cross-tsjs (Plan-selected source census; empty kinds/extents is not complete-empty work)".into());
        add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
        return Ok(None);
    }
    let V::Array(values) = value else {
        needed.push("candidateSourcePaths must be a canonical-set of LogicalPath".into());
        add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
        return Ok(None);
    };
    Ok(Some(canonical_strings(
        values.iter().filter_map(|v| {
            if let V::String(s) = v {
                Some(s.clone())
            } else {
                None
            }
        }),
        work,
    )?))
}
fn check_candidates(
    context: &CandidateContext<'_>,
    needed: &mut Vec<String>,
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<CandidateChecks, Error> {
    let refs = list(field(context.input.manifest, "candidateResultRefs"))?;
    let names = refs
        .iter()
        .map(|v| string_value(v).map(String::from))
        .collect::<Result<Vec<_>, _>>()?;
    if canonical_strings(names, work)? != canonical_strings(context.cells.candidates.clone(), work)?
    {
        add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED");
    }
    let mut out = CandidateChecks {
        records: alloc::collections::BTreeMap::new(),
        digests: alloc::collections::BTreeMap::new(),
        deficiencies: Vec::new(),
    };
    let rows = list(field(context.input.manifest, "cellOutcomes"))?;
    for digest in refs {
        charge(work)?;
        let key = string_value(digest)?;
        let Some(record) = locate_blob(context.store, key, context.candidates, true, faults, work)?
        else {
            continue;
        };
        if !shape(
            context.inputs,
            &record,
            "foundation/execution-inputs.schema.v1.json",
            "#/$defs/CandidateProducerResultV1",
            context.schema_work,
        )? {
            add_fault(faults, "EXECUTION_INPUTS_SCHEMA");
            continue;
        }
        if canonical_digest(&record)? != *digest {
            add_fault(faults, "EXECUTION_INPUTS_REF_MISMATCH");
        }
        if !is(field(&record, "planId"), context.input.plan_id)
            || !is(
                field(&record, "executionPlanId"),
                context.input.execution_id,
            )
        {
            add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_BIND");
        }
        let matches = rows
            .iter()
            .filter(|r| field(r, "candidateResultDigest") == digest)
            .collect::<Vec<_>>();
        let matched = matches.first().copied();
        if matches.len() != 1 {
            add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_BIND");
        } else if let Some(row) = matched {
            let index = (
                ordinal(field(row, "cellOrdinal"))?,
                ordinal(field(row, "programOrdinal"))?,
            );
            if out.records.insert(index, record.clone()).is_some() {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_BIND");
            }
            out.digests.insert(index, digest.clone());
            if [
                "cellOrdinal",
                "programOrdinal",
                "capabilityId",
                "languageMode",
                "universe",
            ]
            .iter()
            .any(|f| field(&record, f) != field(row, f))
                || field(&record, "producerClosure") != field(row, "enumeratorClosure")
                || field(&record, "stageOrdinal") != field(row, "stageOrdinal")
            {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_BIND");
            }
            check_carrier(
                field(&record, "deficiency"),
                field(&record, "nativeCause"),
                context.law,
                faults,
            )?;
        }
        let cap = field(&record, "capabilityId");
        let want_mode = if is(cap, "clones-near") {
            Some("near")
        } else if is(cap, "clones-cross-tsjs") {
            Some("cross-tsjs")
        } else {
            None
        };
        let binding = matched
            .and_then(|r| {
                context.bindings.iter().find(|b| {
                    ordinal(field(r, "cellOrdinal")) == Ok(b.ci)
                        && ordinal(field(r, "programOrdinal")) == Ok(b.pi)
                })
            })
            .map(|b| b.binding)
            .unwrap_or(&V::Null);
        let extent = candidate_extent(binding, needed, faults, work)?;
        if is(field(&record, "state"), "complete") {
            if let Some(extent) = &extent {
                let paths = list(field(&record, "examinedPaths"))?
                    .iter()
                    .map(|v| string_value(v).map(String::from))
                    .collect::<Result<Vec<_>, _>>()?;
                if canonical_strings(paths, work)? != canonical_strings(extent.clone(), work)? {
                    add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_BIND");
                }
            } else {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
            }
        }
        let mut bodies = alloc::collections::BTreeMap::new();
        for body in list(field(&record, "sourceBodies"))? {
            charge(work)?;
            let V::String(id) = field(body, "id") else {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
                continue;
            };
            if bodies.contains_key(id) {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
                continue;
            }
            bodies.insert(id.clone(), body);
            if field(body, "universe") != field(&record, "universe") {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
            }
            let path = field(body, "path");
            if extent
                .as_ref()
                .is_some_and(|paths| !paths.iter().any(|p| is(path, p)))
            {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
            }
            let row = string_value(path)
                .ok()
                .and_then(|p| context.snapshot.get(p));
            let Some(row) = row else {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
                continue;
            };
            if field(body, "contentSha256") != field(row, "sha256")
                || field(body, "byteLength") != field(row, "bytes")
            {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_SOURCE");
            }
            if let V::String(sha) = field(row, "sha256") {
                if !context.store.pointers.contains(sha) {
                    add_fault(faults, "EXECUTION_INPUTS_REF_POINTER");
                } else if let Some(raw) = context.store.blobs.get(sha) {
                    let n = match field(row, "bytes") {
                        V::Integer(n) => usize::try_from(n.get()).ok(),
                        _ => None,
                    };
                    if opensip_identity::digest_hex(&opensip_identity::raw_sha256(raw)) != *sha
                        || Some(raw.len()) != n
                    {
                        add_fault(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES");
                    }
                } else {
                    add_fault(faults, "EXECUTION_INPUTS_REF_LOST_BYTES");
                }
            }
        }
        for gd in list(field(&record, "groupDigests"))? {
            charge(work)?;
            let key = string_value(gd)?;
            let Some(group) = locate_blob(context.store, key, context.groups, false, faults, work)?
            else {
                continue;
            };
            if !shape(
                context.inputs,
                &group,
                "native/native-evidence.schemas.v2.json",
                "#/$defs/CloneCandidateGroupV2",
                context.schema_work,
            )? {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP");
                continue;
            }
            if !is(field(&group, "authority"), "candidate-only")
                || want_mode.is_some_and(|m| !is(field(&group, "mode"), m))
                || field(&group, "automaticDeletionEligible") == &V::Bool(true)
            {
                add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP");
            }
            for member in list(field(&group, "members"))? {
                charge(work)?;
                if !bodies.contains_key(string_value(member)?) {
                    add_fault(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP");
                }
            }
        }
        if (is(field(&record, "state"), "unavailable") || is(field(&record, "state"), "partial"))
            && matched.is_some_and(|r| field(r, "required") == &V::Bool(true))
        {
            out.deficiencies.push(obj([
                ("source", text("execution")),
                ("cause", text("required-cell-unsatisfied")),
                ("cellOrdinal", field(&record, "cellOrdinal").clone()),
                ("programOrdinal", field(&record, "programOrdinal").clone()),
                ("capabilityId", cap.clone()),
                ("required", V::Bool(true)),
                ("deficiency", field(&record, "deficiency").clone()),
                ("nativeCause", field(&record, "nativeCause").clone()),
                (
                    "inputRefs",
                    V::Array(alloc::vec![input_ref("candidate-producer-result", digest)]),
                ),
            ]));
        }
    }
    Ok(out)
}

fn check_outcomes(
    context: &AccountContext<'_>,
    bindings: &[Binding<'_>],
    receipts: &ReceiptChecks,
    candidates: &CandidateChecks,
    accounts: &[V],
    faults: &mut Vec<String>,
    work: &mut usize,
) -> Result<(Vec<V>, Vec<V>), Error> {
    let mut values = Vec::new();
    let mut deficiencies = Vec::new();
    for (row, b) in list(field(context.input.manifest, "cellOutcomes"))?
        .iter()
        .zip(bindings)
    {
        charge(work)?;
        let key = (b.ci, b.pi);
        let inv = context
            .cells
            .inventory_records
            .get(&key)
            .map_or(&[][..], Vec::as_slice);
        let acc = accounts
            .iter()
            .filter(|a| {
                ordinal(field(a, "cellOrdinal")) == Ok(b.ci)
                    && ordinal(field(a, "programOrdinal")) == Ok(b.pi)
            })
            .cloned()
            .collect::<Vec<_>>();
        let derived = outcome(
            OutcomeInput {
                enumerator: string_value(field(row, "enumeratorStatus"))?,
                universe: field(row, "universe"),
                required: field(b.cell, "required") == &V::Bool(true),
                inventories: inv,
                accounts: &acc,
                candidate: candidates.records.get(&key).unwrap_or(&V::Null),
                candidate_digest: candidates.digests.get(&key).unwrap_or(&V::Null),
                candidate_capability: candidate_capability(field(b.cell, "capabilityId")),
                binding: b.binding,
            },
            work,
        )?;
        let mut value = alloc::collections::BTreeMap::from([
            (String::from("ordinal"), field(row, "ordinal").clone()),
            (String::from("cellOrdinal"), integer(b.ci)?),
            (String::from("programOrdinal"), integer(b.pi)?),
        ]);
        for k in [
            "state",
            "stageOrdinalNullReason",
            "deficiency",
            "nativeCause",
            "nativeCauses",
            "inputRefs",
            "sources",
        ] {
            value.insert(k.into(), field(&derived, k).clone());
        }
        values.push(V::Object(value));
        if field(row, "state") != field(&derived, "state") {
            add_fault(faults, "EXECUTION_INPUTS_OUTCOME_DERIVE");
        }
        if is(field(&derived, "state"), "complete") {
            if present(field(row, "deficiency")) || present(field(row, "nativeCause")) {
                add_fault(faults, "EXECUTION_INPUTS_CAUSE_CARRIER");
            }
            if !present(field(row, "stageOrdinal")) {
                add_fault(faults, "EXECUTION_INPUTS_STAGE_ORDINAL");
            }
        } else {
            let sources = list(field(&derived, "sources"))?;
            let same_pair = |s: &V| {
                field(s, "deficiency") == field(row, "deficiency")
                    && field(s, "nativeCause") == field(row, "nativeCause")
            };
            if !same_pair(&derived) || (!sources.is_empty() && !sources.iter().any(same_pair)) {
                add_fault(faults, "EXECUTION_INPUTS_OUTCOME_DERIVE");
            }
            check_carrier(
                field(row, "deficiency"),
                field(row, "nativeCause"),
                context.law,
                faults,
            )?;
            if field(b.cell, "required") == &V::Bool(true) {
                for source in sources {
                    charge(work)?;
                    if ["inventory", "candidate", "enumerator", "binding"]
                        .iter()
                        .any(|s| is(field(source, "source"), s))
                    {
                        deficiencies.push(merge(
                            deficiency_base(b, "required-cell-unsatisfied")?,
                            [
                                ("deficiency", field(source, "deficiency").clone()),
                                ("nativeCause", field(source, "nativeCause").clone()),
                                (
                                    "nativeCauses",
                                    V::Array(list(field(source, "nativeCauses"))?.to_vec()),
                                ),
                                (
                                    "inputRefs",
                                    V::Array(list(field(source, "inputRefs"))?.to_vec()),
                                ),
                            ],
                        )?);
                    }
                }
            }
        }
        if !present(field(row, "stageOrdinal")) {
            if !["unavailable-binding", "optional-unselected"]
                .iter()
                .any(|s| is(field(row, "stageOrdinalNullReason"), s))
                || (is(field(row, "enumeratorStatus"), "selected")
                    && present(field(row, "universe"))
                    && !is(field(&derived, "state"), "unavailable"))
            {
                add_fault(faults, "EXECUTION_INPUTS_STAGE_ORDINAL");
            }
        } else {
            if present(field(row, "stageOrdinalNullReason")) {
                add_fault(faults, "EXECUTION_INPUTS_STAGE_ORDINAL");
            }
            let so = ordinal(field(row, "stageOrdinal"))?;
            if let Some(receipt) = receipts.by_ordinal.get(&so) {
                if present(field(row, "enumeratorClosure"))
                    && field(receipt, "producerClosure") != field(row, "enumeratorClosure")
                {
                    add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
                }
                if is(field(&derived, "state"), "complete")
                    && !is(field(receipt, "state"), "complete")
                {
                    add_fault(faults, "EXECUTION_INPUTS_OUTCOME_DERIVE");
                }
                if let Some(spec) = context
                    .input
                    .stages
                    .get(string_value(field(receipt, "stageSpecDigest"))?)
                {
                    for vd in list(field(row, "viewDigests"))? {
                        charge(work)?;
                        if let Some(view) = context.records.views.get(string_value(vd)?)
                            && field(view, "producerClosure") != field(spec, "producerClosure")
                        {
                            add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
                        }
                    }
                }
            } else {
                add_fault(faults, "EXECUTION_INPUTS_STAGE_PRODUCER");
            }
        }
    }
    Ok((values, deficiencies))
}
struct KernelInput<'a> {
    capture: CaptureInput<'a>,
    store: ExecutionStore<'a>,
    inventories: &'a alloc::collections::BTreeMap<String, V>,
    imports: &'a alloc::collections::BTreeMap<String, V>,
    candidates: &'a alloc::collections::BTreeMap<String, V>,
    targets: &'a alloc::collections::BTreeMap<String, V>,
    incoming: &'a alloc::collections::BTreeMap<String, V>,
    groups: &'a alloc::collections::BTreeMap<String, V>,
    vcs: &'a V,
    inputs: &'a opensip_identity::RetainedInputs<'a>,
    schema_work: usize,
}
fn empty_result(law: &V, faults: Vec<String>) -> V {
    obj([
        ("result", text("REFUSE")),
        (
            "refusals",
            V::Array(faults.iter().map(|s| text(s)).collect()),
        ),
        ("digest", V::Null),
        ("requiredCellDeficiencies", V::Array(Vec::new())),
        ("derivedAccounts", V::Array(Vec::new())),
        ("derivedOutcomes", V::Array(Vec::new())),
        ("neededRootInputs", field(law, "neededRootInputs").clone()),
        ("causeRetention", field(law, "causeRetention").clone()),
        ("internalFaults", field(law, "internalFaults").clone()),
        ("standing", field(law, "standing").clone()),
    ])
}
fn join_execution(q: KernelInput<'_>, work: &mut usize) -> Result<V, Error> {
    charge(work)?;
    let law = registry()?;
    let mut faults = Vec::new();
    let mut needed = list(field(&law, "neededRootInputs"))?
        .iter()
        .map(|v| string_value(v).map(String::from))
        .collect::<Result<Vec<_>, _>>()?;
    if field(&law, "ownerDeficiency") != field(&law, "schemaDeficiency")
        || field(&law, "ownerNativeCause") != field(&law, "schemaNativeCause")
    {
        return Ok(empty_result(
            &law,
            alloc::vec!["EXECUTION_INPUTS_CAUSE_ENUM_DRIFT".into()],
        ));
    }
    if !shape(
        q.inputs,
        q.capture.manifest,
        "foundation/execution-inputs.schema.v1.json",
        "#",
        q.schema_work,
    )? {
        return Ok(empty_result(
            &law,
            alloc::vec!["EXECUTION_INPUTS_SCHEMA".into()],
        ));
    }
    capture_header(&q.capture, &mut faults, work)?;
    let selected = list(field(q.capture.manifest, "selectedRefs"))?;
    let mut views = alloc::collections::BTreeMap::new();
    for reference in selected {
        charge(work)?;
        let domain = ref_domain(reference);
        let digest = string_value(field(reference, "digest"))?;
        match domain {
            "view" => {
                if let Some(v) = locate_object(&q.store, "view", digest, &mut faults, work)? {
                    views.insert(String::from(digest), v);
                }
            }
            "coverage" => {
                locate_object(&q.store, "coverage", digest, &mut faults, work)?;
            }
            "import" => {
                if let Some(value) = locate_object(&q.store, "import", digest, &mut faults, work)? {
                    match q.imports.get(digest) {
                        None => add_fault(&mut faults, "EXECUTION_INPUTS_REF_POINTER"),
                        Some(v) if v != &value => {
                            add_fault(&mut faults, "EXECUTION_INPUTS_REF_MISMATCH")
                        }
                        _ => (),
                    }
                }
            }
            "subject-inventory" => {
                locate_blob(&q.store, digest, q.inventories, true, &mut faults, work)?;
            }
            "candidate-producer-result" => {
                locate_blob(&q.store, digest, q.candidates, true, &mut faults, work)?;
            }
            "target-attribution" => {
                locate_blob(&q.store, digest, q.targets, true, &mut faults, work)?;
            }
            "incoming-search" => {
                locate_blob(&q.store, digest, q.incoming, true, &mut faults, work)?;
            }
            _ => (),
        }
    }
    let mut facts = alloc::collections::BTreeMap::new();
    for view in views.values() {
        charge(work)?;
        for fid in list(field(view, "facts"))? {
            charge(work)?;
            if let Some((domain, value)) = q.store.objects.get(string_value(fid)?)
                && domain == "fact"
            {
                facts.insert(string_value(fid)?.to_owned(), value);
            }
        }
    }
    for reference in selected {
        charge(work)?;
        if ref_domain(reference) != "target-attribution" {
            continue;
        }
        let Some(target) = q.targets.get(string_value(field(reference, "digest"))?) else {
            continue;
        };
        if field(target, "schemaVersion") != &integer(2)? {
            add_fault(&mut faults, "EXECUTION_INPUTS_TARGET_ATTRIBUTION_JOIN");
            continue;
        }
        let fact = string_value(field(target, "sourceFactId"))
            .ok()
            .and_then(|id| facts.get(id));
        let Some(fact) = fact else {
            add_fault(&mut faults, "EXECUTION_INPUTS_TARGET_ATTRIBUTION_JOIN");
            continue;
        };
        if field(target, "producerClosure") != field(fact, "producerClosure")
            || !is(field(target, "planId"), q.capture.plan_id)
        {
            add_fault(&mut faults, "EXECUTION_INPUTS_TARGET_ATTRIBUTION_JOIN");
        }
    }
    let bindings = bindings(q.capture.enumeration, work)?;
    check_outcome_ordinals(q.capture.manifest, &bindings, &mut faults, work)?;
    let receipts = capture_receipts(&q.capture, &q.store, &mut views, &mut faults, work)?;
    let mut snapshot = alloc::collections::BTreeMap::new();
    if let Some((domain, value)) = q
        .store
        .objects
        .get(string_value(field(q.capture.enumeration, "snapshotId"))?)
        && domain == "snapshot"
    {
        for row in list(field(value, "sourceInventory"))? {
            charge(work)?;
            if let V::String(path) = field(row, "path") {
                snapshot.insert(path.clone(), row.clone());
            }
        }
    }
    if snapshot.is_empty() {
        needed.push("objects[enumerationPlan.snapshotId].sourceInventory".into());
    }
    let records = CellInputs {
        views: &views,
        objects: q.store.objects,
        inventories: q.inventories,
    };
    let cells = check_cell_rows(&q.capture, &records, &bindings, &law, &mut faults, work)?;
    let context = AccountContext {
        input: &q.capture,
        records: &records,
        cells: &cells,
        store: &q.store,
        law: &law,
        vcs_kind: field(q.vcs, "kind"),
    };
    let (accounts, mut deficiencies) = check_accounts(&context, &bindings, &mut faults, work)?;
    let candidate_context = CandidateContext {
        input: &q.capture,
        store: &q.store,
        candidates: q.candidates,
        groups: q.groups,
        snapshot: &snapshot,
        bindings: &bindings,
        cells: &cells,
        inputs: q.inputs,
        law: &law,
        schema_work: q.schema_work,
    };
    let candidates = check_candidates(&candidate_context, &mut needed, &mut faults, work)?;
    deficiencies.extend(candidates.deficiencies.clone());
    let (outcomes, more) = check_outcomes(
        &context,
        &bindings,
        &receipts,
        &candidates,
        &accounts,
        &mut faults,
        work,
    )?;
    deficiencies.extend(more);
    selected_cover(
        &q.capture,
        &receipts.captured,
        &cells.inventory_named,
        &cells.candidates,
        &views,
        &mut faults,
        work,
    )?;
    let mut seen = BTreeSet::new();
    let mut uniq = Vec::new();
    for d in deficiencies {
        charge(work)?;
        let key = canonical_bytes(&d).map_err(|_| Error::Shape)?;
        if seen.insert(key) {
            uniq.push(d);
        }
    }
    let mut seen = BTreeSet::new();
    needed.retain(|s| seen.insert(s.clone()));
    let mut result = empty_result(&law, faults.clone());
    result = merge(
        result,
        [
            ("requiredCellDeficiencies", V::Array(uniq)),
            ("derivedAccounts", V::Array(accounts)),
            ("derivedOutcomes", V::Array(outcomes)),
            (
                "neededRootInputs",
                V::Array(needed.iter().map(|s| text(s)).collect()),
            ),
        ],
    )?;
    if faults.is_empty() {
        let view_count = cells
            .view_hexes
            .values()
            .flatten()
            .collect::<BTreeSet<_>>()
            .len();
        result = merge(
            result,
            [
                ("result", text("ADMIT")),
                ("digest", canonical_digest(q.capture.manifest)?),
                (
                    "cellCount",
                    integer(list(field(q.capture.manifest, "cellOutcomes"))?.len())?,
                ),
                ("viewCount", integer(view_count)?),
                (
                    "coverageAccountCount",
                    integer(list(field(q.capture.manifest, "nativeCoverageAccounts"))?.len())?,
                ),
                (
                    "candidateCount",
                    integer(list(field(q.capture.manifest, "candidateResultRefs"))?.len())?,
                ),
            ],
        )?;
    }
    Ok(result)
}

#[path = "execution_reader.rs"]
mod retained;
pub use retained::{ExecutionInputChecks, ExecutionInputError, inspect_execution_input_join};
