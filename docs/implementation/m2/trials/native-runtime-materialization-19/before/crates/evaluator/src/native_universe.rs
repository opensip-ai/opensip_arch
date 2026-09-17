//! Universe owner diagnostics over retained frames, not a selected Plan or Run.
use crate::{NativeContextError, inspect_native_context};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
    vec::Vec,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, NativeFrameSet, RetainedInputError, RetainedInputs,
    TraversalBudget,
};

#[derive(Debug, PartialEq, Eq)]
pub enum NativeUniverseError {
    Frame(GraphError),
    Context(NativeContextError),
    Unsupported(&'static str),
    RegistryLaw,
    ContextDomain,
}
/// Results of the universe owner's exact local binding. Even with no refusals,
/// this is not proof of Plan selection, transitive retention or semantic replay.
pub struct NativeUniverseChecks {
    digest: [u8; 32],
    context_digest: [u8; 32],
    refusals: Vec<String>,
}
impl NativeUniverseChecks {
    pub fn digest(&self) -> [u8; 32] {
        self.digest
    }
    pub fn context_digest(&self) -> [u8; 32] {
        self.context_digest
    }
    pub fn refusals(&self) -> &[String] {
        &self.refusals
    }
}
pub(crate) fn field<'a>(v: &'a V, k: &str) -> Result<&'a V, NativeUniverseError> {
    if let V::Object(o) = v {
        o.get(k).ok_or(NativeUniverseError::RegistryLaw)
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
pub(crate) fn text(v: &V) -> Result<&str, NativeUniverseError> {
    if let V::String(s) = v {
        Ok(s)
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
pub(crate) fn array(v: &V) -> Result<&[V], NativeUniverseError> {
    if let V::Array(a) = v {
        Ok(a)
    } else {
        Err(NativeUniverseError::RegistryLaw)
    }
}
pub(crate) fn sha256_text(s: &str) -> Result<[u8; 32], NativeUniverseError> {
    let s = s
        .strip_prefix("sha256:")
        .ok_or(NativeUniverseError::RegistryLaw)?;
    if s.len() != 64
        || !s
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let mut out = [0; 32];
    for (i, b) in out.iter_mut().enumerate() {
        *b = u8::from_str_radix(&s[i * 2..i * 2 + 2], 16)
            .map_err(|_| NativeUniverseError::RegistryLaw)?;
    }
    Ok(out)
}

/// Reconstruct the named syntax context's owner checks on every call, then bind
/// selected grammar IDs. The selected immutable universe row owns dispatch;
/// callers cannot supply an ADMIT result or substitute different context bytes.
/// Compiler-universe bindings remain Unsupported until their retained owners
/// and snapshot joins are implemented. Syntax names no such inputs.
pub fn inspect_syntax_universe(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    work: usize,
) -> Result<NativeUniverseChecks, NativeUniverseError> {
    let universe = inputs
        .frame_candidate(digest, NativeFrameSet::SemanticUniverse, work)
        .map_err(NativeUniverseError::Frame)?;
    if universe.domain() != "native.semantic-universe.syntax.v2" {
        return Err(NativeUniverseError::Unsupported(
            "compiler universe retained-input owners",
        ));
    }
    let row = universe.registry_row();
    if text(field(row, "language")?)? != "syntax"
        || text(field(row, "contextForm")?)? != "sha256-text"
        || text(field(field(row, "binding")?, "entryPoint")?)? != "bind_syntax_universe"
    {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let mut reference = universe.descriptor();
    for step in array(field(row, "contextField")?)? {
        reference = field(reference, text(step)?)?;
    }
    let context_digest = sha256_text(text(reference)?)?;
    let context = inputs
        .frame_candidate(context_digest, NativeFrameSet::Context, work)
        .map_err(NativeUniverseError::Frame)?;
    if context.domain() != text(field(row, "contextDomain")?)? {
        return Err(NativeUniverseError::ContextDomain);
    }
    let admission = inspect_native_context(inputs, context_digest, work)
        .map_err(NativeUniverseError::Context)?;
    let mut refusals: BTreeSet<String> = admission.refusals().iter().cloned().collect();
    let available = array(field(
        field(context.descriptor(), "grammarBundle")?,
        "grammars",
    )?)?
    .iter()
    .map(|g| text(field(g, "grammarId")?))
    .collect::<Result<BTreeSet<_>, _>>()?;
    for id in array(field(universe.descriptor(), "selectedGrammarIds")?)? {
        let id = text(id)?;
        if !available.contains(id) {
            refusals.insert(format!("native.syntax-grammar-not-in-bundle:{id}"));
        }
    }
    Ok(NativeUniverseChecks {
        digest,
        context_digest,
        refusals: refusals.into_iter().collect(),
    })
}

/// Bind a TypeScript universe to its named context, nested canonical records and
/// the explicitly named snapshot descriptor. The snapshot is rehashed and shape
/// checked; this API proves neither Plan selection nor retention of member bytes.
pub fn inspect_typescript_universe(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    snapshot_id: &str,
    work: usize,
) -> Result<NativeUniverseChecks, NativeUniverseError> {
    let universe = inputs
        .frame_candidate(digest, NativeFrameSet::SemanticUniverse, work)
        .map_err(NativeUniverseError::Frame)?;
    if universe.domain() != "native.semantic-universe.typescript.v2" {
        return Err(NativeUniverseError::Unsupported("non-TypeScript universe"));
    }
    let row = universe.registry_row();
    if text(field(row, "language")?)? != "typescript"
        || text(field(row, "contextForm")?)? != "sha256-text"
        || text(field(field(row, "binding")?, "entryPoint")?)? != "bind_typescript_universe"
    {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let u = universe.descriptor();
    let mut reference = u;
    for step in array(field(row, "contextField")?)? {
        reference = field(reference, text(step)?)?;
    }
    let context_digest = sha256_text(text(reference)?)?;
    let context = inputs
        .frame_candidate(context_digest, NativeFrameSet::Context, work)
        .map_err(NativeUniverseError::Frame)?;
    if context.domain() != text(field(row, "contextDomain")?)? {
        return Err(NativeUniverseError::ContextDomain);
    }
    let admission = inspect_native_context(inputs, context_digest, work)
        .map_err(NativeUniverseError::Context)?;
    let c = context.descriptor();
    let snapshot = inputs
        .object(snapshot_id, IdentityDomain::Snapshot, work)
        .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
    let inventory = array(field(snapshot.descriptor(), "sourceInventory")?)?
        .iter()
        .map(|r| Ok((text(field(r, "path")?)?, r)))
        .collect::<Result<BTreeMap<_, _>, NativeUniverseError>>()?;
    let mut checks = TsChecks {
        refusals: admission.refusals().iter().cloned().collect(),
    };
    checks.fields(u, c)?;
    let graph = nested_record(inputs, u, row, "configGraph", work)?;
    if let Some(graph) = graph {
        let nodes = array(field(&graph, "nodes")?)?;
        let paths = nodes
            .iter()
            .map(|n| text(field(n, "path")?))
            .collect::<Result<BTreeSet<_>, _>>()?;
        let context_paths = array(field(field(c, "configProjection")?, "configGraphPaths")?)?
            .iter()
            .map(text)
            .collect::<Result<BTreeSet<_>, _>>()?;
        if paths != context_paths {
            checks.fault("native.universe-retained-input-mismatch:configGraphPaths");
        }
        for n in nodes {
            let path = text(field(n, "path")?)?;
            if inventory
                .get(path)
                .map(|r| field(r, "sha256"))
                .transpose()?
                != Some(field(n, "contentSha256")?)
            {
                checks.fault(&format!("native.universe-source-mismatch:{path}"));
            }
        }
        checks.graph(&graph)?;
        let entry = field(&graph, "entryConfigPath")?;
        let origin = if entry == &V::Null {
            Some("synthesized")
        } else {
            let node = nodes.iter().find(|n| field(n, "path").ok() == Some(entry));
            if let Some(n) = node {
                Some(if text(field(n, "kind")?)? == "jsconfig" {
                    "jsconfig"
                } else {
                    "tsconfig"
                })
            } else {
                checks.fault("native.universe-context-field-mismatch:configOrigin:CONFIG_GRAPH_ENTRY_NOT_A_NODE");
                None
            }
        };
        if origin.is_some() && origin != Some(text(field(u, "configOrigin")?)?) {
            checks.fault("native.universe-context-field-mismatch:configOrigin");
        }
    } else {
        checks.fault("native.universe-retained-input-missing:configGraph");
    }
    let layout = nested_record(inputs, c, context.registry_row(), "nodeModulesLayout", work)?;
    if field(c, "nodeModulesLayoutDigest")? != &V::Null {
        if let Some(layout) = layout {
            let entries = array(field(&layout, "entries")?)?;
            let installed = entries
                .iter()
                .map(|r| text(field(r, "installPath")?))
                .collect::<Result<BTreeSet<_>, _>>()?;
            for r in entries {
                let real = text(field(r, "realPath")?)?;
                if real != text(field(r, "installPath")?)? && !installed.contains(real) {
                    checks.fault(&format!(
                        "native.universe-retained-input-mismatch:nodeModulesLayout.realPath:{real}"
                    ));
                }
            }
        } else {
            checks.fault("native.universe-retained-input-missing:nodeModulesLayout");
        }
    }
    for key in ["programRootFiles", "jsRootFiles"] {
        for p in array(field(u, key)?)? {
            let p = text(p)?;
            if !inventory.contains_key(p) {
                checks.fault(&format!("native.universe-path-not-inventoried:{p}"));
            }
        }
    }
    Ok(NativeUniverseChecks {
        digest,
        context_digest,
        refusals: checks.refusals.into_iter().collect(),
    })
}

// Only keys selected by the immutable native row are eligible. Unrelated blobs
// in a retained store are not extra caller-supplied semantic binding inputs.
fn nested_record(
    inputs: &RetainedInputs<'_>,
    descriptor: &V,
    row: &V,
    key: &str,
    work: usize,
) -> Result<Option<V>, NativeUniverseError> {
    let matches = array(field(row, "nestedRecords")?)?
        .iter()
        .filter(|r| field(r, "retainedAs").ok().and_then(|v| text(v).ok()) == Some(key))
        .collect::<Vec<_>>();
    if matches.len() != 1 {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let r = matches[0];
    let mut value = descriptor;
    for p in array(field(r, "path")?)? {
        value = field(value, text(p)?)?;
    }
    if value == &V::Null {
        return Ok(None);
    }
    let digest = sha256_text(&format!("sha256:{}", text(value)?))?;
    let blob = match inputs.blob(digest) {
        Ok(b) => b,
        Err(RetainedInputError::MissingBlob(_)) => return Ok(None),
        Err(e) => return Err(NativeUniverseError::Frame(GraphError::Input(e))),
    };
    inputs
        .inspect_current_record(
            digest,
            text(field(r, "document")?)?,
            text(field(r, "selector")?)?,
            TraversalBudget {
                steps: work,
                depth: 64,
                descriptor_work: work,
            },
        )
        .map_err(NativeUniverseError::Frame)?;
    blob.canonical_record()
        .map(Some)
        .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))
}
struct TsChecks {
    refusals: BTreeSet<String>,
}
impl TsChecks {
    fn fault(&mut self, s: &str) {
        self.refusals.insert(s.into());
    }
    fn fields(&mut self, u: &V, c: &V) -> Result<(), NativeUniverseError> {
        let projection = field(c, "configProjection")?;
        let options = field(projection, "honoredOptions")?;
        let lock = field(c, "lockfileIdentity")?;
        let none = V::String("none".into());
        let expected = [
            ("languageMode", field(c, "languageMode")?.clone()),
            ("packageModuleType", field(c, "packageModuleType")?.clone()),
            ("allowJs", field(options, "allowJs")?.clone()),
            ("checkJs", field(options, "checkJs")?.clone()),
            (
                "lockfileKind",
                if lock == &V::Null {
                    none
                } else {
                    field(lock, "kind")?.clone()
                },
            ),
            (
                "nodeModulesInReadSet",
                V::Bool(field(c, "nodeModulesLayoutDigest")? != &V::Null),
            ),
            ("jsDiagnosticsEnabled", field(options, "checkJs")?.clone()),
            (
                "jsAdmittedToProgram",
                V::Bool(
                    field(options, "allowJs")? == &V::Bool(true)
                        && !array(field(u, "jsRootFiles")?)?.is_empty(),
                ),
            ),
        ];
        for (k, v) in expected {
            if field(u, k)? != &v {
                self.fault(&format!("native.universe-context-field-mismatch:{k}"));
            }
        }
        let synth = text(field(u, "configOrigin")?)? == "synthesized";
        if synth != (text(field(u, "languageMode")?)? == "js-synthesized") {
            self.fault("native.universe-context-field-mismatch:configOrigin");
        }
        if synth != array(field(projection, "configGraphPaths")?)?.is_empty() {
            self.fault("native.universe-context-field-mismatch:configGraphPaths");
        }
        let synthopts = field(u, "synthesizedOptions")?;
        if synth != (field(u, "synthesizerVersion")? != &V::Null)
            || synth != (synthopts != &V::Null)
        {
            self.fault("native.universe-context-field-mismatch:synthesizedOptions");
        }
        if synth && synthopts != &V::Null {
            let V::Object(o) = synthopts else {
                return Err(NativeUniverseError::RegistryLaw);
            };
            for (k, v) in o {
                if field(options, k)? != v {
                    self.fault(&format!(
                        "native.universe-context-field-mismatch:synthesizedOptions.{k}"
                    ));
                }
            }
            if !o.contains_key("jsx") && field(options, "jsx")? != &V::Null {
                self.fault("native.universe-context-field-mismatch:synthesizedOptions.jsx");
            }
        }
        if field(u, "allowJs")? == &V::Bool(false) && !array(field(u, "jsRootFiles")?)?.is_empty() {
            self.fault("native.universe-context-field-mismatch:jsRootFiles");
        }
        Ok(())
    }
    fn graph(&mut self, g: &V) -> Result<(), NativeUniverseError> {
        let law = opensip_identity::parse_json(include_bytes!("native-context-registry.json"))
            .map_err(|_| NativeUniverseError::RegistryLaw)?;
        let law = field(&law, "configNodeKindLaw")?;
        let V::Object(basenames) = field(law, "basenames")? else {
            return Err(NativeUniverseError::RegistryLaw);
        };
        let nodes = array(field(g, "nodes")?)?;
        let by_path = nodes
            .iter()
            .map(|n| Ok((text(field(n, "path")?)?, n)))
            .collect::<Result<BTreeMap<_, _>, NativeUniverseError>>()?;
        for (path, n) in &by_path {
            let basename = path
                .rsplit('/')
                .next()
                .ok_or(NativeUniverseError::RegistryLaw)?;
            let expected = basenames.get(basename).unwrap_or(field(law, "otherwise")?);
            if field(n, "kind")? != expected {
                self.fault(&format!("native.config-graph-kind-contradicts-path:{path}"));
            }
            for e in array(field(n, "extendsResolved")?)? {
                let e = text(e)?;
                if !by_path.contains_key(e) {
                    self.fault(&format!("native.config-graph-edge-not-a-node:{e}"));
                }
            }
        }
        let entry = field(g, "entryConfigPath")?;
        if entry == &V::Null {
            if !nodes.is_empty() {
                self.fault("native.config-graph-synthesized-with-nodes");
            }
            return Ok(());
        }
        let entry = text(entry)?;
        if !by_path.contains_key(entry) {
            self.fault(&format!("native.config-graph-entry-not-a-node:{entry}"));
            return Ok(());
        }
        // Iterative DFS preserves the reference edge sequence and cycle diagnostic
        // without recursing on a configuration graph supplied by a producer.
        let mut state = BTreeMap::new();
        let mut stack = alloc::vec![(entry, false)];
        while let Some((p, done)) = stack.pop() {
            if done {
                state.insert(p, 2);
                continue;
            }
            match state.get(p) {
                Some(2) => continue,
                Some(1) => {
                    self.fault(&format!("native.config-graph-cycle:{p}"));
                    continue;
                }
                _ => {}
            }
            state.insert(p, 1);
            stack.push((p, true));
            if let Some(n) = by_path.get(p) {
                for e in array(field(n, "extendsResolved")?)?.iter().rev() {
                    stack.push((text(e)?, false));
                }
            }
        }
        for path in by_path.keys() {
            if !state.contains_key(path) {
                self.fault(&format!(
                    "native.config-graph-node-unreachable-from-entry:{path}"
                ));
            }
        }
        Ok(())
    }
}

/// Recheck Rust universe/context agreement and selected nested H-records against
/// one explicitly named snapshot. These local diagnostics neither execute Cargo
/// nor establish Plan grants, complete retention or producer observation truth.
pub fn inspect_rust_universe(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    snapshot_id: &str,
    work: usize,
) -> Result<NativeUniverseChecks, NativeUniverseError> {
    let universe = inputs
        .frame_candidate(digest, NativeFrameSet::SemanticUniverse, work)
        .map_err(NativeUniverseError::Frame)?;
    if universe.domain() != "native.semantic-universe.rust.v2" {
        return Err(NativeUniverseError::Unsupported("non-Rust universe"));
    }
    let row = universe.registry_row();
    if text(field(row, "language")?)? != "rust"
        || text(field(row, "contextForm")?)? != "sha256-text"
        || text(field(field(row, "binding")?, "entryPoint")?)? != "bind_rust_universe"
    {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let u = universe.descriptor();
    let mut reference = u;
    for p in array(field(row, "contextField")?)? {
        reference = field(reference, text(p)?)?;
    }
    let context_digest = sha256_text(text(reference)?)?;
    let context = inputs
        .frame_candidate(context_digest, NativeFrameSet::Context, work)
        .map_err(NativeUniverseError::Frame)?;
    if context.domain() != text(field(row, "contextDomain")?)? {
        return Err(NativeUniverseError::ContextDomain);
    }
    let c = context.descriptor();
    let admission = inspect_native_context(inputs, context_digest, work)
        .map_err(NativeUniverseError::Context)?;
    let snapshot = inputs
        .object(snapshot_id, IdentityDomain::Snapshot, work)
        .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
    let inventory = array(field(snapshot.descriptor(), "sourceInventory")?)?
        .iter()
        .map(|r| Ok((text(field(r, "path")?)?, r)))
        .collect::<Result<BTreeMap<_, _>, NativeUniverseError>>()?;
    let mut checks = RustChecks {
        refusals: admission.refusals().iter().cloned().collect(),
    };
    checks.fields(u, c)?;
    let dependency = nested_frame(
        inputs,
        u,
        row,
        "dependencySourceSet",
        "native.dependency-source-set.v1",
        work,
    )?;
    if let Some(d) = dependency {
        if field(&d, "lockfileIdentity")? != field(u, "lockfileIdentity")? {
            checks.fault("native.universe-retained-input-mismatch:lockfileIdentity");
        }
    } else {
        checks.fault("native.universe-retained-input-missing:dependencySourceSet");
    }
    let features = nested_frame(
        inputs,
        u,
        row,
        "unifiedFeatures",
        "native.unified-features.rust.v1",
        work,
    )?;
    if let Some(f) = features {
        for k in ["targetTriple", "resolverVersion"] {
            if field(&f, k)? != field(c, k)? {
                checks.fault(&format!(
                    "native.universe-retained-input-mismatch:unifiedFeatures.{k}"
                ));
            }
        }
    } else {
        checks.fault("native.universe-retained-input-missing:unifiedFeatures");
    }
    let prepared = nested_frame(
        inputs,
        u,
        row,
        "preparedOutputSet",
        "native.prepared-output-set.v3",
        work,
    )?;
    if field(u, "preparedOutputSetId")? != &V::Null {
        if let Some(p) = prepared {
            let prep = field(&p, "preparation")?;
            if field(prep, "dependencySourceSetId")? != field(u, "dependencySourceSetId")? {
                checks.fault("native.universe-retained-input-mismatch:preparedOutputSet.dependencySourceSetId");
            }
            if field(prep, "toolchain")? != field(c, "toolchain")? {
                checks.fault("native.universe-retained-input-mismatch:preparedOutputSet.toolchain");
            }
            if !array(field(u, "cfgSets")?)?
                .iter()
                .any(|r| field(r, "cfgSetId").ok() == field(prep, "cfgSetId").ok())
            {
                checks.fault("native.universe-retained-input-mismatch:preparedOutputSet.cfgSetId");
            }
            let expected = if text(field(prep, "kind")?)? == "imported-descriptor" {
                "imported-inert"
            } else {
                "host-prepared"
            };
            if text(field(u, "preparedResolution")?)? != expected {
                checks.fault("native.universe-retained-input-mismatch:preparedResolution");
            }
        } else {
            checks.fault("native.universe-retained-input-missing:preparedOutputSet");
        }
    }
    let ownership = nested_frame(
        inputs,
        u,
        row,
        "sourceUnitOwnership",
        "native.source-unit-ownership.v1",
        work,
    )?;
    if field(u, "sourceUnitOwnershipId")? != &V::Null {
        if let Some(o) = ownership {
            checks.ownership(&o, u, &inventory)?;
        } else {
            checks.fault("native.universe-retained-input-missing:sourceUnitOwnership");
        }
    }
    let lock = field(u, "lockfileIdentity")?;
    let path = text(field(lock, "path")?)?;
    if inventory
        .get(path)
        .map(|r| field(r, "sha256"))
        .transpose()?
        != Some(field(lock, "contentSha256")?)
    {
        checks.fault(&format!("native.universe-source-mismatch:{path}"));
    }
    for p in array(field(u, "crateRootPaths")?)? {
        let p = text(p)?;
        if !inventory.contains_key(p) {
            checks.fault(&format!("native.universe-path-not-inventoried:{p}"));
        }
    }
    for p in array(field(
        field(c, "configProjection")?,
        "replacedSnapshotConfigs",
    )?)? {
        let p = text(p)?;
        if !inventory.contains_key(p) {
            checks.fault(&format!("native.native-context-path-not-inventoried:{p}"));
        }
    }
    Ok(NativeUniverseChecks {
        digest,
        context_digest,
        refusals: checks.refusals.into_iter().collect(),
    })
}
fn nested_frame(
    inputs: &RetainedInputs<'_>,
    descriptor: &V,
    row: &V,
    key: &str,
    domain: &str,
    work: usize,
) -> Result<Option<V>, NativeUniverseError> {
    let matches = array(field(row, "nestedIdentities")?)?
        .iter()
        .filter(|r| field(r, "retainedAs").ok().and_then(|v| text(v).ok()) == Some(key))
        .collect::<Vec<_>>();
    if matches.len() != 1 {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let r = matches[0];
    if text(field(r, "form")?)? != "sha256-text" || text(field(r, "domainSet")?)? != "native-nested"
    {
        return Err(NativeUniverseError::RegistryLaw);
    }
    let mut value = descriptor;
    for p in array(field(r, "path")?)? {
        value = field(value, text(p)?)?;
    }
    if value == &V::Null {
        return Ok(None);
    }
    let digest = sha256_text(text(value)?)?;
    let frame = match inputs.frame_candidate(digest, NativeFrameSet::Nested, work) {
        Ok(f) => f,
        Err(GraphError::Input(RetainedInputError::MissingBlob(_))) => return Ok(None),
        Err(e) => return Err(NativeUniverseError::Frame(e)),
    };
    if frame.domain() != domain {
        return Err(NativeUniverseError::ContextDomain);
    }
    Ok(Some(frame.descriptor().clone()))
}
struct RustChecks {
    refusals: BTreeSet<String>,
}
impl RustChecks {
    fn fault(&mut self, s: &str) {
        self.refusals.insert(s.into());
    }
    fn fields(&mut self, u: &V, c: &V) -> Result<(), NativeUniverseError> {
        for k in [
            "dependencySourceSetId",
            "unifiedFeaturesId",
            "preparedOutputSetId",
        ] {
            if field(u, k)? != field(c, k)? {
                self.fault(&format!("native.universe-context-field-mismatch:{k}"));
            }
        }
        let projection = field(c, "configProjection")?;
        if field(u, "rustflags")? != field(projection, "rustflags")? {
            self.fault("native.universe-context-field-mismatch:rustflags");
        }
        let projection_hash =
            opensip_identity::hash_canonical_value("native.cargo-config-projection.v2", projection)
                .map_err(|e| NativeUniverseError::Frame(GraphError::Frame(e)))?;
        if text(field(u, "configProjectionSha256")?)?
            != opensip_identity::digest_hex(&projection_hash)
        {
            self.fault("native.universe-context-field-mismatch:configProjectionSha256");
        }
        let prepared = text(field(u, "preparedResolution")?)? != "none";
        if field(u, "executionCapableResolution")? != &V::Bool(prepared) {
            self.fault("native.universe-context-field-mismatch:executionCapableResolution");
        }
        if (field(u, "preparedOutputSetId")? == &V::Null) == prepared {
            self.fault("native.universe-context-field-mismatch:preparedOutputSetId");
        }
        let base = array(field(c, "baseCfg")?)?
            .iter()
            .map(text)
            .collect::<Result<BTreeSet<_>, _>>()?;
        let mut ids = BTreeSet::new();
        for row in array(field(u, "cfgSets")?)? {
            let cfg = array(field(row, "cfg")?)?
                .iter()
                .map(text)
                .collect::<Result<BTreeSet<_>, _>>()?;
            let id = text(field(row, "cfgSetId")?)?;
            if !base.is_subset(&cfg) {
                self.fault(&format!(
                    "native.universe-context-field-mismatch:cfgSets.{id}"
                ));
            }
            if !ids.insert(id) {
                self.fault("native.universe-context-field-mismatch:duplicate-cfg-set-id");
            }
        }
        Ok(())
    }
    fn ownership(
        &mut self,
        o: &V,
        u: &V,
        inventory: &BTreeMap<&str, &V>,
    ) -> Result<(), NativeUniverseError> {
        let units = array(field(o, "units")?)?;
        let declared = units
            .iter()
            .map(|r| text(field(r, "unitId")?))
            .collect::<Result<BTreeSet<_>, _>>()?;
        let V::Object(editions) = field(u, "edition")? else {
            return Err(NativeUniverseError::RegistryLaw);
        };
        for unit in units {
            let mut projection = BTreeMap::new();
            projection.insert(
                "schemaVersion".into(),
                opensip_identity::parse_json(b"1").map_err(|_| NativeUniverseError::RegistryLaw)?,
            );
            for k in ["markerPath", "targetKind", "targetName"] {
                projection.insert(k.into(), field(unit, k)?.clone());
            }
            let id = opensip_identity::hash_canonical_value(
                "native.compilation-unit.v1",
                &V::Object(projection),
            )
            .map_err(|e| NativeUniverseError::Frame(GraphError::Frame(e)))?;
            if text(field(unit, "unitId")?)?
                != format!("sha256:{}", opensip_identity::digest_hex(&id))
            {
                self.fault("native.universe-retained-input-mismatch:sourceUnitOwnership.unitId");
            }
            if !inventory.contains_key(text(field(unit, "markerPath")?)?) {
                self.fault(
                    "native.universe-retained-input-mismatch:sourceUnitOwnership.markerPath",
                );
            }
            if field(unit, "targetEdition")? == &V::Null
                && !editions.contains_key(text(field(unit, "crateName")?)?)
            {
                self.fault("native.universe-retained-input-mismatch:sourceUnitOwnership.crateName");
            }
        }
        for id in array(field(o, "selectedUnitIds")?)? {
            if !declared.contains(text(id)?) {
                self.fault(
                    "native.universe-retained-input-mismatch:sourceUnitOwnership.selectedUnitIds",
                );
            }
        }
        for row in array(field(o, "ownership")?)? {
            if !inventory.contains_key(text(field(row, "path")?)?) {
                self.fault("native.universe-retained-input-mismatch:sourceUnitOwnership.path");
            }
            if !declared.contains(text(field(row, "unitId")?)?) {
                self.fault("native.universe-retained-input-mismatch:sourceUnitOwnership.unitId");
            }
        }
        Ok(())
    }
}
