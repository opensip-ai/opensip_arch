//! Native-frame retained-byte diagnostics, separate from Plan and replay.
use crate::native_universe::{array, field, sha256_text, text};
use crate::{
    NativeUniverseError, inspect_native_context, inspect_rust_universe, inspect_syntax_universe,
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
};
/// Retained native-frame diagnostics. This covers the registered frame's nested
/// inputs, member bytes, snapshot joins and local native owners. It is not a Run,
/// Plan-selection, security-custody or evaluator-replay admission token.
pub struct NativeRetentionChecks {
    frames: BTreeSet<(String, [u8; 32])>,
    blobs: usize,
    closures: usize,
}
impl NativeRetentionChecks {
    pub fn frame_count(&self) -> usize {
        self.frames.len()
    }
    // Actual nested traversal census for the closed evaluator composition.
    pub(crate) fn frame_digests(&self, set: NativeFrameSet) -> impl Iterator<Item = [u8; 32]> + '_ {
        self.frames.iter().filter(move |(name, _)| name == set.name()).map(|(_, digest)| *digest)
    }
    pub fn blob_count(&self) -> usize {
        self.blobs
    }
    pub fn closure_count(&self) -> usize {
        self.closures
    }
}
#[derive(Debug, PartialEq, Eq)]
pub enum NativeRetentionError {
    Owner(NativeUniverseError),
    Refused(Vec<String>),
    Law,
    Limit,
    SnapshotPath(String),
    SnapshotSource(String),
    ClosureKind,
}
impl From<NativeUniverseError> for NativeRetentionError {
    fn from(e: NativeUniverseError) -> Self {
        Self::Owner(e)
    }
}
/// Traverse exactly one registered native root and its selected dependencies.
/// `steps` counts native-frame/closure/blob visits and registry-path expansions;
/// `depth` bounds nested frames. `descriptor_work` separately bounds each schema
/// admission. This does not interpret either budget as elapsed time or CPU work.
pub fn inspect_native_retention(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    set: NativeFrameSet,
    snapshot_id: &str,
    budget: TraversalBudget,
) -> Result<NativeRetentionChecks, NativeRetentionError> {
    inspect_retention(inputs, digest, set, snapshot_id, budget, true)
}
// Plan selection owns the later universe binding. This crate-only operation
// retains frame joins and admits contexts without resolving a universe's named
// context early. It cannot supply a Run or universe admission token.
pub(crate) fn inspect_native_frame_inputs(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    set: NativeFrameSet,
    snapshot_id: &str,
    budget: TraversalBudget,
) -> Result<NativeRetentionChecks, NativeRetentionError> {
    inspect_retention(inputs, digest, set, snapshot_id, budget, false)
}
fn inspect_retention(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    set: NativeFrameSet,
    snapshot_id: &str,
    budget: TraversalBudget,
    bind_universe: bool,
) -> Result<NativeRetentionChecks, NativeRetentionError> {
    if budget.steps == 0 || budget.depth == 0 {
        return Err(NativeRetentionError::Limit);
    }
    let snapshot = inputs
        .object(
            snapshot_id,
            IdentityDomain::Snapshot,
            budget.descriptor_work,
        )
        .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
    let inventory = array(field(snapshot.descriptor(), "sourceInventory")?)?
        .iter()
        .map(|r| Ok((text(field(r, "path")?)?.into(), r.clone())))
        .collect::<Result<BTreeMap<String, V>, NativeUniverseError>>()?;
    let mut walk = NativeRetention {
        inputs,
        snapshot_id,
        inventory,
        budget,
        bind_universe,
        frames: BTreeSet::new(),
        blobs: BTreeSet::new(),
        closures: BTreeSet::new(),
    };
    walk.frame(digest, set, 0)?;
    Ok(NativeRetentionChecks {
        frames: walk.frames,
        blobs: walk.blobs.len(),
        closures: walk.closures.len(),
    })
}
struct NativeRetention<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    snapshot_id: &'s str,
    inventory: BTreeMap<String, V>,
    budget: TraversalBudget,
    bind_universe: bool,
    frames: BTreeSet<(String, [u8; 32])>,
    blobs: BTreeSet<[u8; 32]>,
    closures: BTreeSet<String>,
}
fn optional_rows<'a>(v: &'a V, key: &str) -> Result<&'a [V], NativeRetentionError> {
    let V::Object(o) = v else {
        return Err(NativeRetentionError::Law);
    };
    match o.get(key) {
        None => Ok(&[]),
        Some(v) => Ok(array(v)?),
    }
}
fn raw_digest(v: &V) -> Result<[u8; 32], NativeUniverseError> {
    sha256_text(&format!("sha256:{}", text(v)?))
}
impl NativeRetention<'_, '_> {
    fn spend(&mut self, depth: usize) -> Result<(), NativeRetentionError> {
        if depth > self.budget.depth || self.budget.steps == 0 {
            return Err(NativeRetentionError::Limit);
        }
        self.budget.steps -= 1;
        Ok(())
    }
    fn path<'v>(&mut self, value: &'v V, path: &V) -> Result<Vec<&'v V>, NativeRetentionError> {
        let mut current = alloc::vec![value];
        for step in array(path)? {
            let step = text(step)?;
            let mut next = Vec::new();
            for v in current {
                self.spend(0)?;
                if step == "[]" {
                    next.extend(array(v)?.iter());
                } else {
                    next.push(field(v, step)?);
                }
            }
            current = next;
        }
        Ok(current)
    }
    fn blob(&mut self, digest: [u8; 32], length: Option<&V>) -> Result<(), NativeRetentionError> {
        self.spend(0)?;
        let blob = self
            .inputs
            .blob(digest)
            .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
        if let Some(length) = length {
            let V::Integer(n) = length else {
                return Err(NativeRetentionError::Law);
            };
            let n = u64::try_from(n.get()).map_err(|_| NativeRetentionError::Law)?;
            blob.require_length(n)
                .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
        }
        self.blobs.insert(digest);
        Ok(())
    }
    fn blob_joins(&mut self, value: &V, row: &V) -> Result<(), NativeRetentionError> {
        for join in optional_rows(row, "blobJoins")? {
            let V::Object(j) = join else {
                return Err(NativeRetentionError::Law);
            };
            for node in self.path(value, field(join, "path")?)? {
                let digest = raw_digest(field(node, text(field(join, "digestField")?)?)?)?;
                let length = j
                    .get("lengthField")
                    .map(|v| field(node, text(v)?))
                    .transpose()?;
                self.blob(digest, length)?;
            }
        }
        Ok(())
    }
    fn snapshot_joins(&mut self, value: &V, row: &V) -> Result<(), NativeRetentionError> {
        for join in optional_rows(row, "snapshotJoins")? {
            let V::Object(j) = join else {
                return Err(NativeRetentionError::Law);
            };
            for node in self.path(value, field(join, "path")?)? {
                if node == &V::Null {
                    if j.get("nullable") != Some(&V::Bool(true)) {
                        return Err(NativeRetentionError::Law);
                    }
                    continue;
                }
                match text(field(join, "form")?)? {
                    "inventoried-paths" => {
                        for item in array(node)? {
                            self.spend(0)?;
                            let p = if let Some(k) = j.get("pathField") {
                                field(item, text(k)?)?
                            } else {
                                item
                            };
                            let p = text(p)?;
                            if !self.inventory.contains_key(p) {
                                return Err(NativeRetentionError::SnapshotPath(p.into()));
                            }
                        }
                    }
                    "inventoried-path-and-digest" => {
                        let p = text(field(node, text(field(join, "pathField")?)?)?)?;
                        let d = field(node, text(field(join, "digestField")?)?)?;
                        if self
                            .inventory
                            .get(p)
                            .map(|r| field(r, "sha256"))
                            .transpose()?
                            != Some(d)
                        {
                            return Err(NativeRetentionError::SnapshotSource(p.into()));
                        }
                    }
                    _ => return Err(NativeRetentionError::Law),
                }
            }
        }
        Ok(())
    }
    fn closure(&mut self, key: &str, kind: &str, depth: usize) -> Result<(), NativeRetentionError> {
        self.spend(depth)?;
        let c = self
            .inputs
            .object(key, IdentityDomain::Closure, self.budget.descriptor_work)
            .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
        if text(field(c.descriptor(), "kind")?)? != kind {
            return Err(NativeRetentionError::ClosureKind);
        }
        // A cached retention walk never suppresses the reference's kind check.
        if !self.closures.insert(key.into()) {
            return Ok(());
        }
        self.blob(raw_digest(field(c.descriptor(), "manifestDigest")?)?, None)?;
        for member in array(field(c.descriptor(), "tree")?)? {
            self.blob(
                raw_digest(field(member, "sha256")?)?,
                Some(field(member, "bytes")?),
            )?;
        }
        Ok(())
    }
    fn frame(
        &mut self,
        digest: [u8; 32],
        set: NativeFrameSet,
        depth: usize,
    ) -> Result<(), NativeRetentionError> {
        self.spend(depth)?;
        let frame = self
            .inputs
            .frame_candidate(digest, set, self.budget.descriptor_work)
            .map_err(NativeUniverseError::Frame)?;
        let row = frame.registry_row();
        let value = frame.descriptor();
        // The inputs are immutable during the borrow. Memoization saves only
        // retention traversal; each externally requested owner is still run.
        if self.frames.insert((set.name().into(), digest)) {
            self.blobs.insert(digest);
            self.snapshot_joins(value, row)?;
            self.blob_joins(value, row)?;
            for join in optional_rows(row, "nestedRecords")? {
                let V::Object(j) = join else {
                    return Err(NativeRetentionError::Law);
                };
                if text(field(join, "form")?)? != "canonical-record" {
                    return Err(NativeRetentionError::Law);
                }
                for reference in self.path(value, field(join, "path")?)? {
                    if reference == &V::Null {
                        if j.get("nullable") != Some(&V::Bool(true)) {
                            return Err(NativeRetentionError::Law);
                        }
                        continue;
                    }
                    let d = raw_digest(reference)?;
                    self.blob(d, None)?;
                    self.inputs
                        .inspect_current_record(
                            d,
                            text(field(join, "document")?)?,
                            text(field(join, "selector")?)?,
                            TraversalBudget {
                                steps: self.budget.steps,
                                depth: self.budget.depth,
                                descriptor_work: self.budget.descriptor_work,
                            },
                        )
                        .map_err(NativeUniverseError::Frame)?;
                    let child = self
                        .inputs
                        .blob(d)
                        .and_then(|b| b.canonical_record())
                        .map_err(|e| NativeUniverseError::Frame(GraphError::Input(e)))?;
                    self.blob_joins(&child, join)?;
                }
            }
            for join in optional_rows(row, "nestedIdentities")? {
                let V::Object(j) = join else {
                    return Err(NativeRetentionError::Law);
                };
                if text(field(join, "domainSet")?)? != "native-nested" {
                    return Err(NativeRetentionError::Law);
                }
                for reference in self.path(value, field(join, "path")?)? {
                    if reference == &V::Null {
                        if j.get("nullable") != Some(&V::Bool(true)) {
                            return Err(NativeRetentionError::Law);
                        }
                        continue;
                    }
                    let d = match text(field(join, "form")?)? {
                        "sha256-text" => sha256_text(text(reference)?)?,
                        "bare-hex" => raw_digest(reference)?,
                        _ => return Err(NativeRetentionError::Law),
                    };
                    self.frame(d, NativeFrameSet::Nested, depth + 1)?;
                }
            }
            for join in optional_rows(row, "closureJoins")? {
                for reference in self.path(value, field(join, "path")?)? {
                    let key = match text(field(join, "form")?)? {
                        "closure2-identity" => text(reference)?.into(),
                        "closure2-suffix" => format!("closure2:{}", text(reference)?),
                        _ => return Err(NativeRetentionError::Law),
                    };
                    self.closure(&key, text(field(join, "kind")?)?, depth + 1)?;
                }
            }
            if set == NativeFrameSet::SemanticUniverse && self.bind_universe {
                let refs = self.path(value, field(row, "contextField")?)?;
                if refs.len() != 1 || text(field(row, "contextForm")?)? != "sha256-text" {
                    return Err(NativeRetentionError::Law);
                }
                self.frame(
                    sha256_text(text(refs[0])?)?,
                    NativeFrameSet::Context,
                    depth + 1,
                )?;
            }
        }
        match set {
            NativeFrameSet::Context => {
                let owner =
                    inspect_native_context(self.inputs, digest, self.budget.descriptor_work)
                        .map_err(NativeUniverseError::Context)?;
                if !owner.refusals().is_empty() {
                    return Err(NativeRetentionError::Refused(owner.refusals().into()));
                }
            }
            NativeFrameSet::SemanticUniverse if self.bind_universe => {
                let owner = match frame.domain() {
                    "native.semantic-universe.syntax.v2" => {
                        inspect_syntax_universe(self.inputs, digest, self.budget.descriptor_work)
                    }
                    "native.semantic-universe.typescript.v2" => inspect_typescript_universe(
                        self.inputs,
                        digest,
                        self.snapshot_id,
                        self.budget.descriptor_work,
                    ),
                    "native.semantic-universe.rust.v2" => inspect_rust_universe(
                        self.inputs,
                        digest,
                        self.snapshot_id,
                        self.budget.descriptor_work,
                    ),
                    _ => return Err(NativeRetentionError::Law),
                }?;
                if !owner.refusals().is_empty() {
                    return Err(NativeRetentionError::Refused(owner.refusals().into()));
                }
            }
            NativeFrameSet::Nested | NativeFrameSet::SemanticUniverse => {}
        }
        Ok(())
    }
}
