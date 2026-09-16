//! Plan-native diagnostics over an explicit observed frame census.
//! The eventual complete Run walker must supply that census. A caller choosing
//! a subset cannot obtain a complete-Run or replay token from this API.
use crate::native_retention::inspect_native_frame_inputs;
use crate::native_universe::{array, field, sha256_text, text};
use crate::{
    NativeRetentionError, NativeUniverseError, inspect_rust_universe, inspect_syntax_universe,
    inspect_typescript_universe,
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
pub enum PlanNativeError {
    Owner(NativeUniverseError),
    Retention(NativeRetentionError),
    Record(GraphError),
    Refused(String),
    Limit,
}
impl From<NativeUniverseError> for PlanNativeError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
impl From<NativeRetentionError> for PlanNativeError {
    fn from(e: NativeRetentionError) -> Self {
        Self::Retention(e)
    }
}
/// Local Plan-native results only. No complete graph, custody, execution or
/// evaluator replay authority is constructible from these private counts.
pub struct PlanNativeChecks {
    contexts: usize,
    universes: usize,
}
impl PlanNativeChecks {
    pub fn context_count(&self) -> usize {
        self.contexts
    }
    pub fn universe_count(&self) -> usize {
        self.universes
    }
}
fn refuse<T>(s: impl Into<String>) -> Result<T, PlanNativeError> {
    Err(PlanNativeError::Refused(s.into()))
}
fn get<'a>(v: &'a V, k: &str) -> Option<&'a V> {
    if let V::Object(o) = v { o.get(k) } else { None }
}
fn bare(v: &V) -> Result<[u8; 32], NativeUniverseError> {
    sha256_text(&format!("sha256:{}", text(v)?))
}
fn contains(a: &V, needle: &str) -> Result<bool, NativeUniverseError> {
    Ok(array(a)?
        .iter()
        .any(|v| matches!(v,V::String(s) if s==needle)))
}
/// Recompute Plan/snapshot identities and record shapes; retain observed frames,
/// then enforce selection before mandatory actual universe binding. `steps`
/// bounds the supplied census size and EACH retention walk independently; it is
/// not a global Run/CPU budget. `descriptor_work` bounds each schema operation.
/// This implements the native block only: the caller still owes earlier Plan,
/// grant/project, capability-manifest, graph-completeness and later replay joins.
pub fn inspect_plan_native(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    observed_contexts: &[[u8; 32]],
    observed_universes: &[[u8; 32]],
    budget: TraversalBudget,
) -> Result<PlanNativeChecks, PlanNativeError> {
    if budget.steps == 0
        || budget.depth == 0
        || observed_contexts
            .len()
            .saturating_add(observed_universes.len())
            > budget.steps
    {
        return Err(PlanNativeError::Limit);
    }
    let plan = inputs
        .object(plan_id, IdentityDomain::Plan, budget.descriptor_work)
        .map_err(|e| PlanNativeError::Record(GraphError::Input(e)))?;
    let p = plan.descriptor();
    let sid = text(field(p, "snapshotId")?)?;
    let snapshot = inputs
        .object(sid, IdentityDomain::Snapshot, budget.descriptor_work)
        .map_err(|e| PlanNativeError::Record(GraphError::Input(e)))?;
    let spec = inputs
        .identity_record_shape(
            bare(field(p, "analysisSpecDigest")?)?,
            "analysis-spec",
            budget.descriptor_work,
        )
        .map_err(PlanNativeError::Record)?;
    let grant = inputs
        .identity_record_shape(
            bare(field(p, "semanticGrantDigest")?)?,
            "semantic-grant",
            budget.descriptor_work,
        )
        .map_err(PlanNativeError::Record)?;
    let contexts: BTreeSet<_> = observed_contexts.iter().copied().collect();
    // Preserve first-observed universe order, as selected reference dictionaries do.
    let mut seen = BTreeSet::new();
    let universes: Vec<_> = observed_universes
        .iter()
        .copied()
        .filter(|d| seen.insert(*d))
        .collect();
    for (ds, set) in [
        (observed_contexts, NativeFrameSet::Context),
        (observed_universes, NativeFrameSet::SemanticUniverse),
    ] {
        let mut walked = BTreeSet::new();
        for d in ds {
            if walked.insert(*d) {
                inspect_native_frame_inputs(inputs, *d, set, sid, budget)?;
            }
        }
    }
    let selected = array(field(p, "nativeContextDigests")?)?
        .iter()
        .map(bare)
        .collect::<Result<BTreeSet<_>, _>>()?;
    if contexts != selected {
        return refuse("NATIVE_CONTEXT_SET_JOIN");
    }
    let law = parse_json(include_bytes!("native-plan-registry.json"))
        .map_err(|_| NativeUniverseError::RegistryLaw)?;
    let modes = field(&law, "languageModes")?;
    let mode_map = field(modes, "map")?;
    let requested = array(field(&spec, "requestedCapabilities")?)?;
    let mut req_modes = BTreeSet::new();
    let mut languages = BTreeSet::new();
    for r in requested {
        let mode = text(field(r, "languageMode")?)?;
        let Some(language) = get(mode_map, mode) else {
            return refuse(format!("ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED:{mode}"));
        };
        req_modes.insert(mode);
        if language != &V::Null {
            languages.insert(text(language)?);
        }
    }
    for r in requested {
        let cap = text(field(r, "capabilityId")?)?;
        let mode = text(field(r, "languageMode")?)?;
        let prefix = "ANALYSIS_SPEC_CAPABILITY:native.requested-capability-";
        if !contains(field(&law, "capabilityIds")?, cap)? {
            return refuse(format!("{prefix}unregistered:{cap}"));
        }
        if !contains(field(&law, "capabilityModes")?, mode)? {
            return refuse(format!("{prefix}mode-unregistered:{cap}:{mode}"));
        }
        for excluded in array(field(&law, "notSelected")?)? {
            if text(field(excluded, "capabilityId")?)? == cap
                && text(field(excluded, "languageMode")?)? == mode
            {
                return refuse(format!("{prefix}mode-not-selected:{cap}:{mode}"));
            }
        }
    }
    let mut owners = BTreeMap::new();
    for r in requested {
        *owners
            .entry((
                text(field(r, "capabilityId")?)?,
                text(field(r, "languageMode")?)?,
                text(field(r, "workspaceRoot")?)?,
            ))
            .or_insert(0usize) += 1;
    }
    for ((cap, mode, root), n) in owners {
        if n > 1 {
            return refuse(format!(
                "ANALYSIS_SPEC_CAPABILITY:native.requested-capability-duplicate-ownership-tuple:{cap}:{mode}:{root}"
            ));
        }
    }
    for d in &universes {
        let frame = inputs
            .frame_candidate(*d, NativeFrameSet::SemanticUniverse, budget.descriptor_work)
            .map_err(PlanNativeError::Record)?;
        let u = frame.descriptor();
        let row = frame.registry_row();
        let language = text(field(row, "language")?)?;
        if !languages.contains(language) {
            return refuse(format!("UNIVERSE_LANGUAGE_NOT_REQUESTED:{language}"));
        }
        let prepared = get(u, "preparedResolution")
            .map(text)
            .transpose()?
            .unwrap_or("none");
        if prepared != "none" {
            let mode = get(field(modes, "preparedModes")?, language)
                .map(text)
                .transpose()?;
            if !mode.is_some_and(|m| req_modes.contains(m)) {
                return refuse(format!(
                    "PREPARED_RESOLUTION_MODE_NOT_REQUESTED:{}",
                    mode.unwrap_or("None")
                ));
            }
        }
        let mut bound = u;
        for step in array(field(row, "contextField")?)? {
            bound = field(bound, text(step)?)?;
        }
        let context = sha256_text(text(bound)?)?;
        if text(field(row, "contextForm")?)? != "sha256-text" || !selected.contains(&context) {
            return refuse("UNIVERSE_CONTEXT_NOT_SELECTED");
        }
        let c = inputs
            .frame_candidate(context, NativeFrameSet::Context, budget.descriptor_work)
            .map_err(PlanNativeError::Record)?;
        if c.domain() != text(field(row, "contextDomain")?)? {
            return refuse(format!("NATIVE_UNIVERSE_CONTEXT_LANGUAGE:{}", c.domain()));
        }
        if let Some(fields) = get(row, "contextAgreementFields") {
            for name in array(fields)? {
                let name = text(name)?;
                if field(u, name)? != field(c.descriptor(), name)? {
                    return refuse(format!("NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH:{name}"));
                }
            }
        }
        let binding = match language {
            "syntax" => inspect_syntax_universe(inputs, *d, budget.descriptor_work),
            "typescript" => inspect_typescript_universe(inputs, *d, sid, budget.descriptor_work),
            "rust" => inspect_rust_universe(inputs, *d, sid, budget.descriptor_work),
            _ => {
                return refuse(format!(
                    "NATIVE_UNIVERSE_BINDING_UNAVAILABLE:{}",
                    text(field(field(row, "binding")?, "entryPoint")?)?
                ));
            }
        }?;
        if !binding.refusals().is_empty() {
            return refuse(format!(
                "NATIVE_UNIVERSE_BINDING:{}",
                binding.refusals().join(",")
            ));
        }
        if binding.digest() != *d {
            return refuse("NATIVE_UNIVERSE_ADMITTED_IDENTITY");
        }
        if let Some(operations) = get(row, "preparedResolutionGrantOperations")
            && let Some(V::String(operation)) = get(operations, prepared)
            && !contains(field(&grant, "analysisOperations")?, operation)?
        {
            return refuse(format!("PREPARED_RESOLUTION_GRANT_JOIN:{operation}"));
        }
    }
    let mut packages = BTreeSet::new();
    for d in &contexts {
        let c = inputs
            .frame_candidate(*d, NativeFrameSet::Context, budget.descriptor_work)
            .map_err(PlanNativeError::Record)?;
        if c.domain() != "native.context.typescript.v2" {
            continue;
        }
        if let Some(value) = get(c.descriptor(), "nodeModulesLayoutDigest") {
            if value == &V::Null {
                continue;
            }
            let layout = inputs
                .blob(bare(value)?)
                .and_then(|b| b.canonical_record())
                .map_err(|e| PlanNativeError::Record(GraphError::Input(e)))?;
            for entry in array(field(&layout, "entries")?)? {
                for f in ["installPath", "realPath"] {
                    packages.insert(text(field(entry, f)?)?.trim_end_matches('/').into());
                }
            }
        }
    }
    let paths = array(field(snapshot.descriptor(), "sourceInventory")?)?
        .iter()
        .map(|r| text(field(r, "path")?))
        .collect::<Result<Vec<_>, _>>()?;
    if let Some(path) = pruned_fault(&paths, &packages, field(&law, "discovery")?)? {
        return refuse(format!("SNAPSHOT_PRUNED_TREE_NOT_A_READ:{path}"));
    }
    Ok(PlanNativeChecks {
        contexts: contexts.len(),
        universes: universes.len(),
    })
}
fn pruned_fault<'a>(
    paths: &[&'a str],
    packages: &BTreeSet<String>,
    law: &V,
) -> Result<Option<&'a str>, NativeUniverseError> {
    let deps = array(field(law, "dependencySegments")?)?
        .iter()
        .map(text)
        .collect::<Result<BTreeSet<_>, _>>()?;
    let vcs = array(field(law, "vcsSegments")?)?
        .iter()
        .map(text)
        .collect::<Result<BTreeSet<_>, _>>()?;
    let marker = text(field(law, "cargoMarker")?)?;
    let target = text(field(law, "cargoBuildSegment")?)?;
    let mut roots = BTreeSet::new();
    for p in paths {
        if p.rsplit('/').next() == Some(marker)
            && !p.split('/').any(|s| deps.contains(s) || vcs.contains(s))
        {
            roots.insert(p.rsplit_once('/').map(|(a, _)| a).unwrap_or(""));
        }
    }
    let mut faults = BTreeSet::new();
    for p in paths {
        if p.split('/').any(|s| vcs.contains(s)) {
            faults.insert(*p);
            continue;
        }
        if p.split('/').any(|s| deps.contains(s)) {
            if !packages.iter().any(|package| {
                p.strip_prefix(package.as_str())
                    .and_then(|s| s.strip_prefix('/'))
                    .is_some_and(|suffix| !suffix.split('/').any(|s| deps.contains(s)))
            }) {
                faults.insert(*p);
            }
            continue;
        }
        let mut start = 0;
        for segment in p.split('/') {
            if segment == target && roots.contains(if start == 0 { "" } else { &p[..start - 1] }) {
                faults.insert(*p);
                break;
            }
            start += segment.len() + 1;
        }
    }
    Ok(faults.into_iter().next())
}
