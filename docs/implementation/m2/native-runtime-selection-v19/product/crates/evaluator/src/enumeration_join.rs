//! Reconstruct and join enumeration inputs from immutable retained bytes.
//! This is a bounded enumeration diagnostic, not complete evaluator replay.
use crate::native_universe::{array, field, sha256_text, text};
use crate::{NativeRetentionError, NativeUniverseError, PlanNativeError};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
    vec::Vec,
};
use opensip_identity::{
    GraphError, IdentityDomain as D, JsonValue as V, NativeFrameSet, RetainedInputs,
    TraversalBudget, digest_hex, parse_json,
};

#[derive(Debug, PartialEq, Eq)]
pub enum EnumerationJoinError {
    Record(GraphError),
    Native(NativeUniverseError),
    Retention(NativeRetentionError),
    Plan(PlanNativeError),
    Refused(String),
    Limit,
    Law,
}
impl From<NativeUniverseError> for EnumerationJoinError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Native(e)
    }
}
fn bare(v: &V) -> Result<[u8; 32], EnumerationJoinError> {
    Ok(sha256_text(&format!("sha256:{}", text(v)?))?)
}
fn object(
    inputs: &RetainedInputs<'_>,
    id: &str,
    domain: D,
    work: usize,
) -> Result<V, EnumerationJoinError> {
    Ok(inputs
        .object(id, domain, work)
        .map_err(|e| EnumerationJoinError::Record(GraphError::Input(e)))?
        .descriptor()
        .clone())
}
fn record(inputs: &RetainedInputs<'_>, digest: [u8; 32]) -> Result<V, EnumerationJoinError> {
    inputs
        .blob(digest)
        .and_then(|b| b.canonical_record())
        .map_err(|e| EnumerationJoinError::Record(GraphError::Input(e)))
}
fn step(remaining: &mut usize) -> Result<(), EnumerationJoinError> {
    *remaining = remaining
        .checked_sub(1)
        .ok_or(EnumerationJoinError::Limit)?;
    Ok(())
}
/// Private maps produced only by the retained reader. No constructor or public
/// caller-supplied ADMIT, bindResult or membership derivation witness.
struct JoinInputs {
    plan: V,
    analysis: V,
    scope: V,
    enumeration: V,
    membership: V,
    snapshot_paths: Vec<String>,
    snapshot_index: BTreeMap<String, V>,
    source_blobs: BTreeMap<String, Vec<u8>>,
    contexts: BTreeMap<String, V>,
    universes: BTreeMap<String, V>,
    universe_domains: BTreeMap<String, String>,
    retained: BTreeMap<String, V>,
    closures: BTreeMap<String, V>,
    inventories: Vec<V>,
}
/// Local reader budget counts visits; each native owner/schema receives a
/// separate copied bound. This is not a global CPU or Plan work-unit bound.
fn read_inputs(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    inventory_refs: &[[u8; 32]],
    budget: TraversalBudget,
) -> Result<JoinInputs, EnumerationJoinError> {
    if budget.depth == 0 {
        return Err(EnumerationJoinError::Limit);
    }
    let mut remaining = budget.steps;
    step(&mut remaining)?;
    let plan = object(inputs, plan_id, D::Plan, budget.descriptor_work)?;
    let snapshot_id = text(field(&plan, "snapshotId")?)?;
    let snapshot = object(inputs, snapshot_id, D::Snapshot, budget.descriptor_work)?;
    let analysis = inputs
        .identity_record_shape(
            bare(field(&plan, "analysisSpecDigest")?)?,
            "analysis-spec",
            budget.descriptor_work,
        )
        .map_err(EnumerationJoinError::Record)?;
    let scope = record(inputs, bare(field(&plan, "scopeDigest")?)?)?;
    // Registry bytes are source-bound, shared with the already selected
    // parameter owner; unknown/duplicate rows cannot supply an enum payload.
    let registry = parse_json(include_bytes!("import-registry.json"))
        .map_err(|_| EnumerationJoinError::Law)?;
    let mut selected = BTreeMap::new();
    for parameter in array(field(&analysis, "parameters")?)? {
        step(&mut remaining)?;
        let mut matched = None;
        for row in array(field(&registry, "rows")?)? {
            step(&mut remaining)?;
            if field(row, "sha256")? == field(parameter, "schemaDigest")? {
                if matched.is_some() {
                    return Err(EnumerationJoinError::Law);
                }
                matched = Some(row);
            }
        }
        let row = matched.ok_or_else(|| {
            EnumerationJoinError::Refused("EVALUATOR_PARAMETER_UNREGISTERED".into())
        })?;
        let key = text(field(row, "key")?)?;
        if selected.contains_key(key) {
            return Err(EnumerationJoinError::Refused(
                "EVALUATOR_PARAMETER_DUPLICATE".into(),
            ));
        }
        let value = inputs
            .registered_record_shape(
                bare(field(parameter, "payloadDigest")?)?,
                bare(field(parameter, "schemaDigest")?)?,
                text(field(row, "document")?)?,
                text(field(row, "selector")?)?,
                budget.descriptor_work,
            )
            .map_err(EnumerationJoinError::Record)?;
        selected.insert(String::from(key), value);
    }
    let enumeration = selected
        .remove("foundation/enumeration-plan.schema.v1.json")
        .ok_or_else(|| {
            EnumerationJoinError::Refused(
                "EVALUATOR_REQUIRED_PARAMETER_MISSING:foundation/enumeration-plan.schema.v1.json"
                    .into(),
            )
        })?;
    // Emission/policy binding belongs to complete reconstruct, not this join.
    let membership = inputs
        .current_record_shape(
            bare(field(&enumeration, "membershipDigest")?)?,
            "native/native-evidence.schemas.v2.json",
            "#/$defs/UnitMembershipV1",
            budget.descriptor_work,
        )
        .map_err(EnumerationJoinError::Record)?;
    let snapshot_inventory = field(&snapshot, "sourceInventory")?.clone();
    let mut snapshot_paths = Vec::new();
    let mut snapshot_index = BTreeMap::new();
    let mut source_blobs = BTreeMap::new();
    for row in array(&snapshot_inventory)? {
        step(&mut remaining)?;
        let path = text(field(row, "path")?)?;
        if snapshot_index
            .insert(String::from(path), row.clone())
            .is_some()
        {
            return Err(EnumerationJoinError::Refused(
                "ENUMERATION_ADMISSION_PRECONDITION".into(),
            ));
        }
        snapshot_paths.push(String::from(path));
        // Reconstruct requires all source bytes; no host-claimed path->bytes
        // table and no missing-manifest fallback enter the evaluator.
        let blob = inputs
            .blob(bare(field(row, "sha256")?)?)
            .map_err(|e| EnumerationJoinError::Record(GraphError::Input(e)))?;
        let V::Integer(n) = field(row, "bytes")? else {
            return Err(EnumerationJoinError::Law);
        };
        blob.require_length(u64::try_from(n.get()).map_err(|_| EnumerationJoinError::Law)?)
            .map_err(|e| EnumerationJoinError::Record(GraphError::Input(e)))?;
        source_blobs.insert(String::from(path), blob.bytes().to_vec());
    }
    let mut contexts = BTreeMap::new();
    let mut context_digests = Vec::new();
    for value in array(field(&plan, "nativeContextDigests")?)? {
        step(&mut remaining)?;
        let d = bare(value)?;
        crate::inspect_native_retention(inputs, d, NativeFrameSet::Context, snapshot_id, budget)
            .map_err(EnumerationJoinError::Retention)?;
        let frame = inputs
            .frame_candidate(d, NativeFrameSet::Context, budget.descriptor_work)
            .map_err(EnumerationJoinError::Record)?;
        context_digests.push(d);
        contexts.insert(digest_hex(&d), frame.descriptor().clone());
    }
    let mut universe_digests = Vec::new();
    let mut seen = BTreeSet::new();
    for cell in array(field(&enumeration, "cells")?)? {
        step(&mut remaining)?;
        for binding in array(field(cell, "programBindings")?)? {
            step(&mut remaining)?;
            let value = field(binding, "universe")?;
            if value != &V::Null {
                let d = bare(value)?;
                if seen.insert(d) {
                    universe_digests.push(d)
                }
            }
        }
    }
    // Selection precedes universe binding in this fixed composition. The census
    // is derived from Plan/enum refs, not supplied by the API caller. Complete
    // Run traversal must still account for other retained universe references.
    crate::inspect_plan_native(inputs, plan_id, &context_digests, &universe_digests, budget)
        .map_err(EnumerationJoinError::Plan)?;
    let mut universes = BTreeMap::new();
    let mut universe_domains = BTreeMap::new();
    let mut retained = BTreeMap::new();
    for d in universe_digests {
        step(&mut remaining)?;
        crate::inspect_native_retention(
            inputs,
            d,
            NativeFrameSet::SemanticUniverse,
            snapshot_id,
            budget,
        )
        .map_err(EnumerationJoinError::Retention)?;
        let frame = inputs
            .frame_candidate(d, NativeFrameSet::SemanticUniverse, budget.descriptor_work)
            .map_err(EnumerationJoinError::Record)?;
        let V::Object(value) = frame.descriptor() else {
            return Err(EnumerationJoinError::Law);
        };
        if value.contains_key("bindResult") {
            return Err(EnumerationJoinError::Refused(
                "ENUMERATION_ADMISSION_PRECONDITION".into(),
            ));
        }
        let mut nested = BTreeMap::new();
        let pair = match frame.domain() {
            "native.semantic-universe.typescript.v2" => Some((
                "configGraph",
                crate::native_universe::nested_record(
                    inputs,
                    frame.descriptor(),
                    frame.registry_row(),
                    "configGraph",
                    budget.descriptor_work,
                )?,
            )),
            "native.semantic-universe.rust.v2" => Some((
                "sourceUnitOwnership",
                crate::native_universe::nested_frame(
                    inputs,
                    frame.descriptor(),
                    frame.registry_row(),
                    "sourceUnitOwnership",
                    "native.source-unit-ownership.v1",
                    budget.descriptor_work,
                )?,
            )),
            "native.semantic-universe.syntax.v2" => None,
            _ => return Err(EnumerationJoinError::Law),
        };
        if let Some((key, Some(value))) = pair {
            nested.insert(String::from(key), value);
        }
        let key = digest_hex(&d);
        universe_domains.insert(key.clone(), String::from(frame.domain()));
        retained.insert(key.clone(), V::Object(nested));
        universes.insert(key, frame.descriptor().clone());
    }
    let mut closures = BTreeMap::new();
    for reference in array(field(&plan, "semanticClosures")?)? {
        step(&mut remaining)?;
        let id = text(reference)?;
        closures.insert(
            String::from(id),
            object(inputs, id, D::Closure, budget.descriptor_work)?,
        );
    }
    let mut inventories = Vec::new();
    for digest in inventory_refs {
        step(&mut remaining)?;
        inventories.push(record(inputs, *digest)?);
    }
    Ok(JoinInputs {
        plan,
        analysis,
        scope,
        enumeration,
        membership,
        snapshot_paths,
        snapshot_index,
        source_blobs,
        contexts,
        universes,
        universe_domains,
        retained,
        closures,
        inventories,
    })
}

fn optional<'a>(v: &'a V, key: &str) -> &'a V {
    if let V::Object(o) = v {
        o.get(key).unwrap_or(&V::Null)
    } else {
        &V::Null
    }
}
fn strs(v: &V) -> Result<Vec<String>, EnumerationJoinError> {
    array(v)?
        .iter()
        .map(|v| Ok(String::from(text(v)?)))
        .collect()
}
fn number(v: &V) -> Result<i128, EnumerationJoinError> {
    if let V::Integer(n) = v {
        Ok(n.get())
    } else {
        Err(EnumerationJoinError::Law)
    }
}
fn json_number(n: usize) -> Result<V, EnumerationJoinError> {
    Ok(V::Integer(
        opensip_identity::JsonInteger::new(n as i128).map_err(|_| EnumerationJoinError::Law)?,
    ))
}
fn jstr(s: &str) -> V {
    V::String(String::from(s))
}
fn jobj<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(
        pairs
            .into_iter()
            .map(|(k, v)| (String::from(k), v))
            .collect(),
    )
}
fn fault(faults: &mut Vec<&'static str>, cause: &'static str) {
    if !faults.contains(&cause) {
        faults.push(cause)
    }
}
fn raw_digest(value: &V) -> Result<String, EnumerationJoinError> {
    let bytes = opensip_identity::canonical_bytes(value).map_err(|_| EnumerationJoinError::Law)?;
    Ok(digest_hex(&opensip_identity::raw_sha256(&bytes)))
}
fn canonical_strings(values: Vec<String>) -> Result<Vec<String>, EnumerationJoinError> {
    let mut keyed = values
        .into_iter()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .map(|s| {
            Ok((
                opensip_identity::canonical_bytes(&jstr(&s))
                    .map_err(|_| EnumerationJoinError::Law)?,
                s,
            ))
        })
        .collect::<Result<Vec<_>, EnumerationJoinError>>()?;
    keyed.sort_by(|a, b| a.0.cmp(&b.0));
    Ok(keyed.into_iter().map(|(_, s)| s).collect())
}
fn string_array(values: Vec<String>) -> V {
    V::Array(values.into_iter().map(V::String).collect())
}
fn external_root(s: &str) -> &str {
    if s == "." { "" } else { s }
}
fn under(path: &str, root: &str) -> bool {
    root.is_empty()
        || path == root
        || path
            .strip_prefix(root)
            .is_some_and(|tail| tail.starts_with('/'))
}
fn logical_path(v: &V) -> bool {
    let V::String(s) = v else { return false };
    !s.is_empty()
        && !s.contains(['\\', '\0'])
        && s.split('/')
            .all(|p| !p.is_empty() && p != "." && p != ".." && p.chars().count() <= 255)
}
fn carrier(
    def: &V,
    cause: &V,
    law: &V,
    faults: &mut Vec<&'static str>,
) -> Result<(), EnumerationJoinError> {
    let bad = if def == &V::Null || def == &jstr("source-syntax-invalid") {
        cause != &V::Null
    } else {
        let row = optional(field(law, "causes")?, text(def)?);
        if row == &V::Null {
            true
        } else {
            let allowed = optional(row, "allowedCauses");
            let has = if allowed == &V::Null {
                false
            } else {
                array(allowed)?.contains(cause)
            };
            match text(field(row, "nativeCause")?)? {
                "must-be-null" => cause != &V::Null,
                "required" => !has,
                "optional" => cause != &V::Null && !has,
                _ => false,
            }
        }
    };
    if bad {
        fault(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
    }
    Ok(())
}
fn projected<T>(v: Result<T, crate::EnumerationExtentError>) -> Result<T, EnumerationJoinError> {
    v.map_err(|e| match e {
        crate::EnumerationExtentError::Limit => EnumerationJoinError::Limit,
        _ => EnumerationJoinError::Law,
    })
}
fn shape(
    inputs: &RetainedInputs<'_>,
    value: &V,
    doc: &str,
    work: usize,
) -> Result<bool, EnumerationJoinError> {
    match inputs.check_current_value_shape(value, doc, "#", work) {
        Ok(()) => Ok(true),
        Err(GraphError::Schema(opensip_identity::SchemaAdmissionError::Mismatch)) => Ok(false),
        Err(GraphError::Schema(opensip_identity::SchemaAdmissionError::Schema(
            opensip_identity::SchemaError::Limit,
        ))) => Err(EnumerationJoinError::Limit),
        Err(e) => Err(EnumerationJoinError::Record(e)),
    }
}
type Locator = (usize, i128, String);
struct CellJoin<'a> {
    bindings: BTreeMap<Locator, (&'a V, &'a V)>,
    expected: Vec<Locator>,
    packages: BTreeMap<String, V>,
}
fn join_cells<'a>(
    q: &'a JoinInputs,
    law: &V,
    budget: TraversalBudget,
    remaining: &mut usize,
    faults: &mut Vec<&'static str>,
) -> Result<CellJoin<'a>, EnumerationJoinError> {
    let cells = array(field(&q.enumeration, "cells")?)?;
    let requested = array(field(&q.analysis, "requestedCapabilities")?)?;
    let tuple = |r: &V| -> Result<(String, String, String, bool), EnumerationJoinError> {
        Ok((
            text(field(r, "capabilityId")?)?.into(),
            text(field(r, "languageMode")?)?.into(),
            text(field(r, "workspaceRoot")?)?.into(),
            field(r, "required")? == &V::Bool(true),
        ))
    };
    let mut req = requested.iter().map(tuple).collect::<Result<Vec<_>, _>>()?;
    let mut actual = cells.iter().map(tuple).collect::<Result<Vec<_>, _>>()?;
    req.sort();
    actual.sort();
    if req != actual {
        fault(faults, "ENUMERATION_PLAN_CELL_TUPLE_MISMATCH")
    }
    let needs_package = cells
        .iter()
        .any(|c| array(optional(c, "kinds")).is_ok_and(|a| a.contains(&jstr("package"))));
    let modes = parse_json(include_bytes!("native-plan-registry.json"))
        .map_err(|_| EnumerationJoinError::Law)?;
    let mut out = CellJoin {
        bindings: BTreeMap::new(),
        expected: Vec::new(),
        packages: BTreeMap::new(),
    };
    for (ci, cell) in cells.iter().enumerate() {
        step(remaining)?;
        let cap = text(field(cell, "capabilityId")?)?;
        let mode = text(field(cell, "languageMode")?)?;
        let root = text(field(cell, "workspaceRoot")?)?;
        let empty = V::Array(Vec::new());
        let expected_kinds = match optional(field(law, "kindMap")?, cap) {
            v @ V::Array(_) => v,
            _ => &empty,
        };
        if field(cell, "kinds")? != expected_kinds {
            fault(faults, "ENUMERATION_PLAN_KIND_MAP")
        }
        let roots = optional(&q.scope, "workspaceRoots");
        let allowed = roots != &V::Null
            && array(roots)?
                .iter()
                .any(|v| text(v).is_ok_and(|r| under(external_root(root), external_root(r))));
        if !allowed {
            fault(faults, "ENUMERATION_SCOPE_WORKSPACE_ROOT")
        }
        let bindings = array(field(cell, "programBindings")?)?;
        if bindings.len() > 128 {
            fault(faults, "ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW")
        }
        let defaults = bindings
            .iter()
            .filter(|b| optional(b, "provenance") == &jstr("default-unit"))
            .collect::<Vec<_>>();
        if defaults.len() > 1
            || defaults
                .first()
                .is_some_and(|b| number(optional(b, "ordinal")).ok() != Some(0))
        {
            fault(faults, "ENUMERATION_PLAN_DEFAULT_UNIT")
        }
        let base = crate::EnumerationExtentInputs {
            membership: &q.membership,
            snapshot_paths: &q.snapshot_paths,
            scope: &q.scope,
            workspace_root: root,
            language_mode: mode,
            universe: None,
            retained: None,
        };
        if needs_package && !out.packages.contains_key(root) {
            let p = projected(crate::project_enumeration_packages(
                &base,
                &q.source_blobs,
                Some(&q.snapshot_index),
                budget.steps,
            ))?;
            for f in p.refusals() {
                fault(faults, f)
            }
            out.packages.insert(root.into(), p.value().clone());
        }
        let file = projected(crate::project_enumeration_extent(
            &base,
            crate::EnumerationExtentKind::File,
            budget.steps,
        ))?;
        for f in file.refusals() {
            fault(faults, f)
        }
        let file_paths = file.paths();
        let file_set = file_paths.iter().collect::<BTreeSet<_>>();
        let package_paths = out
            .packages
            .get(root)
            .map(|p| strs(optional(p, "candidatePaths")))
            .transpose()?
            .unwrap_or_default();
        let mut seen_u = BTreeSet::new();
        for b in bindings {
            step(remaining)?;
            let en = optional(b, "enumerator");
            let ctx = optional(b, "nativeContextDigest");
            let uni = optional(b, "universe");
            let available = uni != &V::Null;
            match optional(en, "status") {
                V::String(s) if s == "unselected" => {
                    if optional(en, "reason") != &jstr("optional-unselected")
                        || field(cell, "required")? == &V::Bool(true)
                        || available
                    {
                        fault(faults, "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
                    }
                }
                V::String(s) if s == "selected" => {
                    let id = optional(en, "closureId");
                    if id == &V::Null
                        || !array(field(&q.plan, "semanticClosures")?)?.contains(id)
                        || !q.closures.contains_key(text(id)?)
                    {
                        fault(faults, "ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN")
                    } else if optional(&q.closures[text(id)?], "kind") != &jstr("provider") {
                        fault(faults, "ENUMERATION_BINDING_ENUMERATOR_KIND")
                    }
                }
                _ => fault(faults, "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR"),
            }
            if ctx != &V::Null
                && (!array(field(&q.plan, "nativeContextDigests")?)?.contains(ctx)
                    || !q.contexts.contains_key(text(ctx)?))
            {
                fault(faults, "ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN")
            }
            let extents = array(field(b, "extents")?)?;
            let kinds = canonical_strings(
                extents
                    .iter()
                    .map(|e| Ok(String::from(text(field(e, "kind")?)?)))
                    .collect::<Result<Vec<_>, EnumerationJoinError>>()?,
            )?;
            if string_array(kinds) != *expected_kinds {
                fault(faults, "ENUMERATION_BINDING_EXTENT_KINDS")
            }
            let candidates = optional(b, "candidateSourcePaths");
            if ["clones-near", "clones-cross-tsjs"].contains(&cap) {
                if let V::Array(a) = candidates {
                    let paths = a
                        .iter()
                        .filter_map(|v| {
                            if let V::String(s) = v {
                                Some(s.clone())
                            } else {
                                None
                            }
                        })
                        .collect::<Vec<_>>();
                    if string_array(canonical_strings(paths.clone())?) != *candidates
                        || paths
                            .iter()
                            .any(|p| !q.snapshot_paths.contains(p) || !file_set.contains(p))
                    {
                        fault(faults, "ENUMERATION_CANDIDATE_SOURCE_PATHS")
                    }
                } else {
                    fault(faults, "ENUMERATION_CANDIDATE_SOURCE_PATHS")
                }
            } else if candidates != &V::Null {
                fault(faults, "ENUMERATION_CANDIDATE_SOURCE_PATHS")
            }
            let mut universe = None;
            let mut nested = None;
            let entry = optional(b, "programEntry");
            let provenance = optional(b, "provenance");
            if available {
                let key = text(uni)?;
                if !seen_u.insert(key) {
                    fault(faults, "ENUMERATION_BINDING_DUPLICATE_UNIVERSE")
                }
                universe = q.universes.get(key);
                if universe.is_none() {
                    fault(faults, "ENUMERATION_BINDING_UNIVERSE_NOT_IN_INPUTS")
                }
                let empty = V::Object(BTreeMap::new());
                let u = universe.unwrap_or(&empty);
                if let V::Object(o) = u
                    && o.contains_key("bindResult")
                {
                    fault(faults, "ENUMERATION_ADMISSION_PRECONDITION")
                }
                let nc = optional(u, "nativeContextId");
                let suffix = if let V::String(s) = nc {
                    Some(s.strip_prefix("sha256:").unwrap_or(s))
                } else {
                    None
                };
                if ctx == &V::Null || suffix != Some(text(ctx)?) {
                    fault(
                        faults,
                        "ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT",
                    )
                }
                let engine = optional(field(field(&modes, "languageModes")?, "map")?, mode);
                let domain = if let V::String(s) = engine {
                    Some(format!("native.semantic-universe.{s}.v2"))
                } else {
                    None
                };
                if domain.is_none() || q.universe_domains.get(key) != domain.as_ref() {
                    fault(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                }
                let ts = ["ts-tsconfig", "js-allowjs", "js-synthesized"].contains(&mode);
                if ts {
                    if optional(u, "languageMode") != &jstr(mode) {
                        fault(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                    }
                    if let V::String(c) = ctx
                        && let Some(v) = q.contexts.get(c)
                    {
                        let cm = optional(v, "languageMode");
                        if cm != &V::Null && cm != &jstr(mode) {
                            fault(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                        }
                    }
                }
                nested = q.retained.get(key);
                if entry != &V::Null {
                    if !logical_path(entry)
                        || !q.snapshot_paths.contains(&String::from(text(entry)?))
                    {
                        fault(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                    }
                    if provenance == &jstr("default-unit") {
                        fault(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                    }
                } else if provenance == &jstr("explicit-plan-selection") && ts {
                    fault(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                }
                if ts {
                    let graph = nested
                        .map(|n| optional(n, "configGraph"))
                        .unwrap_or(&V::Null);
                    if graph == &V::Null {
                        fault(faults, "ENUMERATION_ADMISSION_PRECONDITION")
                    } else {
                        let unit = array(field(&q.membership, "units")?)?.iter().find(|u| {
                            optional(u, "rootPath") == &jstr(external_root(root))
                                && optional(u, "languageMode") == &jstr(mode)
                        });
                        let derived = if mode == "js-synthesized" {
                            &V::Null
                        } else {
                            unit.map(|u| optional(u, "markerPath")).unwrap_or(&V::Null)
                        };
                        let wanted = if entry != &V::Null { entry } else { derived };
                        if optional(graph, "entryConfigPath") != wanted {
                            fault(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                        }
                    }
                }
            } else {
                carrier(
                    optional(b, "deficiency"),
                    optional(b, "nativeCause"),
                    law,
                    faults,
                )?;
                if optional(b, "deficiency") == &V::Null {
                    fault(faults, "ENUMERATION_BINDING_CAUSE")
                }
                if entry != &V::Null
                    && (!logical_path(entry)
                        || !q.snapshot_paths.contains(&String::from(text(entry)?)))
                {
                    fault(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                }
            }
            let symbols = if array(expected_kinds)?.contains(&jstr("symbol")) {
                let input = crate::EnumerationExtentInputs {
                    universe,
                    retained: nested,
                    ..base
                };
                let s = projected(crate::project_enumeration_extent(
                    &input,
                    crate::EnumerationExtentKind::Symbol,
                    budget.steps,
                ))?;
                for f in s.refusals() {
                    fault(faults, f)
                }
                s.paths().to_vec()
            } else {
                Vec::new()
            };
            for extent in extents {
                step(remaining)?;
                let paths = strs(field(extent, "paths")?)?;
                if paths
                    .iter()
                    .any(|p| !q.snapshot_paths.contains(p) || !file_set.contains(p))
                {
                    fault(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
                }
                let derived = match text(field(extent, "kind")?)? {
                    "file" => file_paths,
                    "symbol" => &symbols,
                    "package" => &package_paths,
                    _ => &[],
                };
                if paths != derived {
                    fault(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
                }
            }
        }
        for b in bindings {
            for kind in array(field(cell, "kinds")?)? {
                step(remaining)?;
                let key = (ci, number(field(b, "ordinal")?)?, String::from(text(kind)?));
                out.expected.push(key.clone());
                out.bindings.insert(key, (cell, b));
            }
        }
    }
    Ok(out)
}

struct SubjectSlot {
    payloads: Vec<V>,
    references: Vec<V>,
    id: String,
    universe: String,
    kind: String,
    native: String,
    path: Option<String>,
}
fn suffix_language(path: &str, law: &V) -> Result<String, EnumerationJoinError> {
    let name = path.rsplit('/').next().ok_or(EnumerationJoinError::Law)?;
    let mut best = 0;
    let mut language = String::from("unspecified");
    for row in array(field(law, "languageTable")?)? {
        for s in array(field(row, "suffixes")?)? {
            let s = text(s)?;
            if name.ends_with(s) && s.len() >= best {
                best = s.len();
                language = text(field(row, "languageId")?)?.into()
            }
        }
    }
    Ok(language)
}
fn symbol_id(id: &str) -> bool {
    let Some((prefix, suffix)) = id.split_once(':') else {
        return false;
    };
    !prefix.is_empty()
        && prefix.as_bytes()[0].is_ascii_lowercase()
        && prefix
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
        && !suffix.is_empty()
        && suffix
            .chars()
            .all(|c| !('\u{0}'..='\u{1f}').contains(&c) && !('\u{7f}'..='\u{9f}').contains(&c))
}
fn locator(inv: &V) -> Option<Locator> {
    Some((
        usize::try_from(number(optional(inv, "cellOrdinal")).ok()?).ok()?,
        number(optional(inv, "programOrdinal")).ok()?,
        text(optional(inv, "kind")).ok()?.into(),
    ))
}
// The selected reference uses Python scalar equality only for tracking which
// expected slot already has a schema failure. Preserve bool/int aliases here
// so that invalid booleans do not add a spurious missing-record diagnostic.
// This path never admits an inventory; valid rows still use typed `locator`.
fn failed_locator(inv: &V) -> Option<Locator> {
    let ordinal = |v: &V| match v {
        V::Bool(false) => Some(0),
        V::Bool(true) => Some(1),
        _ => number(v).ok(),
    };
    Some((
        usize::try_from(ordinal(optional(inv, "cellOrdinal"))?).ok()?,
        ordinal(optional(inv, "programOrdinal"))?,
        text(optional(inv, "kind")).ok()?.into(),
    ))
}
fn mint(
    inputs: &RetainedInputs<'_>,
    universe: &str,
    kind: &str,
    native: &str,
    path: &str,
    work: usize,
) -> Result<String, EnumerationJoinError> {
    let mut desc = jobj([
        ("schemaVersion", json_number(3)?),
        ("universe", jstr(universe)),
        ("kind", jstr(kind)),
        ("nativeSubjectId", jstr(native)),
    ]);
    if kind == "package" {
        let V::Object(o) = &mut desc else {
            unreachable!()
        };
        o.insert("packageManifestPath".into(), jstr(path));
    }
    inputs
        .check_identity_value_shape(&desc, "evaluation-subject", work)
        .map_err(EnumerationJoinError::Record)?;
    let hash = opensip_identity::hash_canonical_value("evaluation-subject", &desc)
        .map_err(|e| EnumerationJoinError::Record(GraphError::Frame(e)))?;
    Ok(format!("subject3:{}", digest_hex(&hash)))
}
type SubjectKey = (String, String, String, String);
struct JoinContext<'a, 'b> {
    inputs: &'a RetainedInputs<'b>,
    plan_id: &'a str,
    law: &'a V,
}
fn join_inventories(
    context: JoinContext<'_, '_>,
    q: &JoinInputs,
    cells: &CellJoin<'_>,
    budget: TraversalBudget,
    remaining: &mut usize,
    faults: &mut Vec<&'static str>,
) -> Result<BTreeMap<SubjectKey, SubjectSlot>, EnumerationJoinError> {
    let JoinContext {
        inputs,
        plan_id,
        law,
    } = context;
    let mut seen = BTreeSet::new();
    let mut schema_failed = BTreeSet::new();
    let mut subjects: BTreeMap<SubjectKey, SubjectSlot> = BTreeMap::new();
    let parameter_digest = raw_digest(&q.enumeration)?;
    for inv in &q.inventories {
        step(remaining)?;
        if !shape(
            inputs,
            inv,
            "foundation/subject-inventory.schema.v1.json",
            budget.descriptor_work,
        )? {
            fault(faults, "ENUMERATION_INVENTORY_SCHEMA");
            if let Some(loc) = failed_locator(inv)
                && cells.bindings.contains_key(&loc)
            {
                schema_failed.insert(loc);
            }
            continue;
        }
        if field(inv, "parameterDigest")? != &jstr(&parameter_digest)
            || field(inv, "planId")? != &jstr(plan_id)
        {
            fault(faults, "ENUMERATION_INVENTORY_ORDINAL_UNBOUND")
        }
        let key = locator(inv).ok_or(EnumerationJoinError::Law)?;
        if !seen.insert(key.clone()) {
            fault(faults, "ENUMERATION_INVENTORY_DUPLICATE")
        }
        let Some((cell, binding)) = cells.bindings.get(&key) else {
            fault(faults, "ENUMERATION_INVENTORY_UNEXPECTED_RECORD");
            continue;
        };
        let kind = text(field(inv, "kind")?)?;
        let state = text(field(inv, "state")?)?;
        let extent = array(field(binding, "extents")?)?
            .iter()
            .find(|e| optional(e, "kind") == &jstr(kind))
            .map(|e| field(e, "paths"))
            .transpose()?;
        let Some(extent) = extent else {
            fault(faults, "ENUMERATION_BINDING_EXTENT_KINDS");
            continue;
        };
        let ext = strs(extent)?;
        let extent_set = ext.iter().collect::<BTreeSet<_>>();
        let uni = optional(binding, "universe");
        let deficiency = optional(inv, "deficiency");
        let native_cause = optional(inv, "nativeCause");
        if uni == &V::Null {
            if state != "unavailable" {
                fault(faults, "ENUMERATION_BINDING_UNAVAILABLE_INVENTORY")
            }
            if deficiency != optional(binding, "deficiency")
                || native_cause != optional(binding, "nativeCause")
            {
                fault(faults, "ENUMERATION_BINDING_CAUSE")
            }
        }
        let package = cells.packages.get(text(field(cell, "workspaceRoot")?)?);
        let parse_bad =
            package.is_some_and(|p| array(optional(p, "parseFailed")).is_ok_and(|a| !a.is_empty()));
        if kind == "package"
            && package.is_some()
            && uni != &V::Null
            && ((parse_bad && (state != "partial" || deficiency != &jstr("source-syntax-invalid")))
                || (!parse_bad && deficiency == &jstr("source-syntax-invalid")))
        {
            fault(faults, "ENUMERATION_PACKAGE_PARSE")
        }
        let examined = field(inv, "examinedPaths")?;
        let examined_paths = strs(examined)?;
        if examined_paths.iter().any(|p| !extent_set.contains(p)) {
            fault(faults, "ENUMERATION_INVENTORY_EXAMINED_OUTSIDE_EXTENT")
        }
        if state == "complete" {
            if deficiency != &V::Null || native_cause != &V::Null {
                fault(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
            }
            if examined != extent {
                fault(
                    faults,
                    match kind {
                        "file" => "ENUMERATION_INVENTORY_FILE_TOTALITY",
                        "symbol" => "ENUMERATION_INVENTORY_SYMBOL_EXAMINED",
                        _ => "ENUMERATION_INVENTORY_PACKAGE_TOTALITY",
                    },
                )
            }
        } else {
            if deficiency == &V::Null {
                fault(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
            }
            carrier(deficiency, native_cause, law, faults)?;
        }
        let rows = array(field(inv, "rows")?)?;
        if state == "unavailable" {
            if !rows.is_empty() || !examined_paths.is_empty() {
                fault(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            }
            continue;
        }
        let row_paths = rows
            .iter()
            .map(|r| Ok(String::from(text(field(r, "path")?)?)))
            .collect::<Result<BTreeSet<_>, EnumerationJoinError>>()?;
        if state == "complete"
            && kind == "file"
            && row_paths.iter().collect::<BTreeSet<_>>() != extent_set
        {
            fault(faults, "ENUMERATION_INVENTORY_FILE_TOTALITY")
        }
        if kind == "package"
            && let Some(package) = package
        {
            let named = strs(field(package, "namedPaths")?)?;
            let named_set = named.iter().collect::<BTreeSet<_>>();
            if state == "complete" && row_paths.iter().collect::<BTreeSet<_>>() != extent_set {
                fault(faults, "ENUMERATION_INVENTORY_PACKAGE_TOTALITY")
            }
            if parse_bad
                && uni != &V::Null
                && named
                    .iter()
                    .any(|p| !row_paths.contains(p) || !examined_paths.contains(p))
            {
                fault(faults, "ENUMERATION_PACKAGE_PARSE")
            }
            let by_path = array(field(package, "named")?)?
                .iter()
                .map(|r| Ok((text(field(r, "path")?)?, field(r, "packageName")?)))
                .collect::<Result<BTreeMap<_, _>, EnumerationJoinError>>()?;
            for row in rows {
                step(remaining)?;
                let path = text(field(row, "path")?)?;
                let expected = by_path.get(path);
                if expected.is_none()
                    || Some(&field(row, "nativeSubjectId")?) != expected
                    || Some(&field(row, "qualifiedName")?) != expected
                    || !named_set.contains(&String::from(path))
                {
                    fault(faults, "ENUMERATION_INVENTORY_PACKAGE_NAME")
                }
            }
        }
        let mut ids = BTreeSet::new();
        let mut paths = BTreeSet::new();
        let inv_digest = raw_digest(inv)?;
        for (row_index, row) in rows.iter().enumerate() {
            step(remaining)?;
            let path = text(field(row, "path")?)?;
            let native = text(field(row, "nativeSubjectId")?)?;
            if field(row, "kind")? != &jstr(kind)
                || !ext.iter().any(|p| p == path)
                || !examined_paths.iter().any(|p| p == path)
            {
                fault(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            }
            if !q.snapshot_paths.iter().any(|p| p == path) {
                fault(faults, "ENUMERATION_INVENTORY_EXTERNAL_PATH")
            }
            if kind != "package" && !ids.insert(native) {
                fault(faults, "ENUMERATION_INVENTORY_DUPLICATE")
            }
            if ["file", "package"].contains(&kind) && !paths.insert(path) {
                fault(faults, "ENUMERATION_INVENTORY_DUPLICATE")
            }
            let want = suffix_language(path, law)?;
            if kind == "file" && (field(row, "qualifiedName")? != &jstr(path) || native != path) {
                fault(faults, "ENUMERATION_INVENTORY_FILE_NAME")
            }
            if kind == "symbol" && !symbol_id(native) {
                fault(faults, "ENUMERATION_INVENTORY_SYMBOL_ID")
            }
            if field(row, "subjectLanguage")? != &jstr(&want)
                || (kind == "package" && !["json", "toml"].contains(&want.as_str()))
            {
                fault(faults, "ENUMERATION_INVENTORY_LANGUAGE")
            }
            let mut projection_ids = BTreeSet::new();
            let projections = optional(row, "projections");
            if projections != &V::Null {
                for projection in array(projections)? {
                    step(remaining)?;
                    let id = text(field(projection, "closureId")?)?;
                    if !projection_ids.insert(id) {
                        fault(faults, "ENUMERATION_INVENTORY_DUPLICATE")
                    }
                    if !array(field(&q.plan, "semanticClosures")?)?.contains(&jstr(id))
                        || q.closures.get(id).map(|c| optional(c, "kind"))
                            != Some(&jstr("detector"))
                    {
                        fault(faults, "ENUMERATION_PROJECTION_DETECTOR")
                    }
                }
            }
            if uni != &V::Null {
                let universe = text(uni)?;
                let key = (
                    universe.into(),
                    kind.into(),
                    native.into(),
                    if kind == "package" {
                        path.into()
                    } else {
                        String::new()
                    },
                );
                let loc = jobj([
                    ("cellOrdinal", field(inv, "cellOrdinal")?.clone()),
                    ("programOrdinal", field(inv, "programOrdinal")?.clone()),
                    ("kind", jstr(kind)),
                    ("state", jstr(state)),
                    ("planId", field(inv, "planId")?.clone()),
                    ("parameterDigest", field(inv, "parameterDigest")?.clone()),
                    ("inventoryDigest", jstr(&inv_digest)),
                    ("rowIndex", json_number(row_index)?),
                ]);
                if !subjects.contains_key(&key) {
                    let id =
                        match mint(inputs, universe, kind, native, path, budget.descriptor_work) {
                            Ok(id) => id,
                            Err(EnumerationJoinError::Record(GraphError::Schema(
                                opensip_identity::SchemaAdmissionError::Mismatch,
                            ))) => {
                                fault(faults, "ENUMERATION_ADMISSION_PRECONDITION");
                                String::new()
                            }
                            Err(e) => return Err(e),
                        };
                    subjects.insert(
                        key.clone(),
                        SubjectSlot {
                            payloads: Vec::new(),
                            references: Vec::new(),
                            id,
                            universe: universe.into(),
                            kind: kind.into(),
                            native: native.into(),
                            path: if kind == "package" {
                                Some(path.into())
                            } else {
                                None
                            },
                        },
                    );
                }
                let slot = subjects.get_mut(&key).ok_or(EnumerationJoinError::Law)?;
                slot.references.push(loc);
                if !slot.payloads.is_empty() && !slot.payloads.contains(row) {
                    fault(faults, "ENUMERATION_INVENTORY_RECONCILE")
                }
                if !slot.payloads.contains(row) {
                    slot.payloads.push(row.clone())
                }
            }
        }
    }
    for key in &cells.expected {
        step(remaining)?;
        if !seen.contains(key) && !schema_failed.contains(key) {
            fault(faults, "ENUMERATION_INVENTORY_MISSING_RECORD")
        }
    }
    Ok(subjects)
}
fn refuse_result(faults: Vec<&'static str>, law: &V) -> Result<V, EnumerationJoinError> {
    Ok(jobj([
        ("result", jstr("REFUSE")),
        ("refusals", V::Array(faults.into_iter().map(jstr).collect())),
        ("index", V::Array(Vec::new())),
        ("population", V::Object(BTreeMap::new())),
        ("evaluationSubjects", V::Array(Vec::new())),
        ("subjects", V::Object(BTreeMap::new())),
        ("packageProjection", V::Null),
        ("expectedRecords", json_number(0)?),
        ("internalFaults", field(law, "internalFaults")?.clone()),
        (
            "standing",
            jstr("enumeration-join admission only; not a Run"),
        ),
    ]))
}
fn complete_join(
    inputs: &RetainedInputs<'_>,
    q: &JoinInputs,
    plan_id: &str,
    budget: TraversalBudget,
) -> Result<V, EnumerationJoinError> {
    let mut remaining = budget.steps;
    step(&mut remaining)?;
    let law = parse_json(include_bytes!("enumeration-registry.json"))
        .map_err(|_| EnumerationJoinError::Law)?;
    let mut faults = Vec::new();
    if !shape(
        inputs,
        &q.enumeration,
        "foundation/enumeration-plan.schema.v1.json",
        budget.descriptor_work,
    )? {
        return refuse_result(alloc::vec!["ENUMERATION_PLAN_SCHEMA"], &law);
    }
    let membership = projected(crate::enumeration::retained_membership_checks(
        inputs,
        &q.membership,
        &q.snapshot_paths,
        budget.steps,
    ))?;
    for cause in membership.refusals() {
        fault(&mut faults, cause)
    }
    if faults.contains(&"ENUMERATION_MEMBERSHIP_UNIT_ROOT") {
        return refuse_result(faults, &law);
    }
    if field(&q.enumeration, "snapshotId")? != field(&q.plan, "snapshotId")? {
        fault(&mut faults, "ENUMERATION_PLAN_SNAPSHOT_MISMATCH")
    }
    if field(&q.enumeration, "scopeDigest")? != &jstr(&raw_digest(&q.scope)?)
        || field(&q.enumeration, "scopeDigest")? != field(&q.plan, "scopeDigest")?
    {
        fault(&mut faults, "ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH")
    }
    if field(&q.enumeration, "membershipDigest")? != &jstr(&raw_digest(&q.membership)?) {
        fault(&mut faults, "ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH")
    }
    let cells = join_cells(q, &law, budget, &mut remaining, &mut faults)?;
    let subjects = join_inventories(
        JoinContext {
            inputs,
            plan_id,
            law: &law,
        },
        q,
        &cells,
        budget,
        &mut remaining,
        &mut faults,
    )?;
    if !faults.is_empty() {
        return refuse_result(faults, &law);
    }
    let count = subjects.len();
    let mut by_kind = BTreeMap::from([
        (String::from("file"), 0usize),
        (String::from("symbol"), 0),
        (String::from("package"), 0),
    ]);
    let mut index = Vec::new();
    let mut output = BTreeMap::new();
    let mut ids = Vec::new();
    for slot in subjects.into_values() {
        step(&mut remaining)?;
        *by_kind
            .get_mut(&slot.kind)
            .ok_or(EnumerationJoinError::Law)? += 1;
        let states = slot
            .references
            .iter()
            .map(|r| text(optional(r, "state")))
            .collect::<Result<Vec<_>, _>>()?;
        let state = if !states.is_empty() && states.iter().all(|s| *s == "complete") {
            "complete"
        } else if states.contains(&"partial") {
            "partial"
        } else {
            states.first().copied().unwrap_or("unavailable")
        };
        let mut item = jobj([
            ("evaluationSubject", jstr(&slot.id)),
            ("universe", jstr(&slot.universe)),
            ("kind", jstr(&slot.kind)),
            ("nativeSubjectId", jstr(&slot.native)),
            ("inventoryRefs", V::Array(slot.references.clone())),
            ("state", jstr(state)),
        ]);
        let V::Object(o) = &mut item else {
            unreachable!()
        };
        if let Some(path) = slot.path {
            o.insert("packageManifestPath".into(), jstr(&path));
        }
        index.push(item.clone());
        ids.push(slot.id.clone());
        let V::Object(o) = &mut item else {
            unreachable!()
        };
        o.insert("payloads".into(), V::Array(slot.payloads));
        output.insert(slot.id, item);
    }
    let mut keyed = index
        .into_iter()
        .map(|v| {
            Ok((
                opensip_identity::canonical_bytes(field(&v, "evaluationSubject")?)
                    .map_err(|_| EnumerationJoinError::Law)?,
                v,
            ))
        })
        .collect::<Result<Vec<_>, EnumerationJoinError>>()?;
    keyed.sort_by(|a, b| a.0.cmp(&b.0));
    let by_kind = by_kind
        .into_iter()
        .map(|(k, n)| Ok((k, json_number(n)?)))
        .collect::<Result<BTreeMap<_, _>, EnumerationJoinError>>()?;
    Ok(jobj([
        ("result", jstr("ADMIT")),
        ("refusals", V::Array(Vec::new())),
        (
            "index",
            V::Array(keyed.into_iter().map(|(_, v)| v).collect()),
        ),
        (
            "population",
            jobj([
                ("distinct", json_number(count)?),
                ("byKind", V::Object(by_kind)),
                ("collisions", V::Array(Vec::new())),
            ]),
        ),
        ("evaluationSubjects", string_array(canonical_strings(ids)?)),
        ("subjects", V::Object(output)),
        ("packageProjection", V::Object(cells.packages)),
        ("expectedRecords", json_number(cells.expected.len())?),
        ("internalFaults", field(&law, "internalFaults")?.clone()),
        (
            "standing",
            jstr("enumeration-join admission only; not a Run"),
        ),
    ]))
}

/// Enumeration join data, not a complete Run, execution selection or replay
/// token. Fields are derived from retained Plan, snapshot, native and inventory
/// inputs. Refusals never expose a partial population as an admitted result.
pub struct EnumerationJoinChecks {
    value: V,
}
impl EnumerationJoinChecks {
    pub fn value(&self) -> &V {
        &self.value
    }
}
/// Inspect the Plan-bound enumeration join. The complete evaluator supplies its
/// evaluation input references; this entry rechecks their closed reference
/// shape and derives the subject-inventory digest list itself. Inventory bytes
/// are rehashed, schema-admitted and bound to the Plan/parameter and every
/// expected cell/program/kind. It does not establish the complete execution
/// input selection, independent predicate truth, or Run/custody authority.
///
/// Retained-input, schema, native-owner and local resource failures return a
/// typed `Err` before a join result exists. Once those preconditions hold,
/// `Ok` contains the reference enumeration ADMIT/REFUSE document. This is not
/// a promise to reproduce the raw map-based reference's document for inputs
/// rejected earlier by their retained owner. Neither outcome is a Run token.
pub fn inspect_enumeration_join(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    evaluation_refs: &[V],
    budget: TraversalBudget,
) -> Result<EnumerationJoinChecks, EnumerationJoinError> {
    let mut remaining = budget.steps;
    let mut inventories = Vec::new();
    for reference in evaluation_refs {
        step(&mut remaining)?;
        inputs
            .check_identity_value_shape(reference, "ProofInputRef", budget.descriptor_work)
            .map_err(EnumerationJoinError::Record)?;
        if field(reference, "domain")? == &jstr("subject-inventory") {
            inventories.push(bare(field(reference, "digest")?)?);
        }
    }
    let q = read_inputs(inputs, plan_id, &inventories, budget)?;
    Ok(EnumerationJoinChecks {
        value: complete_join(inputs, &q, plan_id, budget)?,
    })
}
