//! Declared compiler-tool joins over an exactly retained Rust context frame.
//!
//! These diagnostic checks do not admit signatures, native context, system
//! library/configuration/dependency/prepared inputs, or process launch. Their
//! caller owns those admissions. No executable is discovered or run here.

use opensip_identity::{
    GraphError, IdentityDomain, JsonValue, NativeFrameSet, RetainedInputError, RetainedInputs,
};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug)]
pub enum CompilerToolError {
    Frame(GraphError),
    Retained(RetainedInputError),
    Representation,
    ForeignContext,
    ClosureKind(&'static str),
    ToolNotInClosure(&'static str),
    CompilerVersion,
    TargetTriple,
    HostContextMismatch,
}

impl From<RetainedInputError> for CompilerToolError {
    fn from(value: RetainedInputError) -> Self {
        Self::Retained(value)
    }
}

/// Observed joins only; neither an admitted context nor execution authority.
#[derive(Debug)]
pub struct CompilerToolChecks {
    context_digest: [u8; 32],
    linker_present: bool,
}
impl CompilerToolChecks {
    pub fn context_digest(&self) -> [u8; 32] {
        self.context_digest
    }

    /// Presence in the declared closure, not permission to prepare or link.
    pub fn linker_present(&self) -> bool {
        self.linker_present
    }
}

/// Check the Rust context's declared compiler-tool closure joins.
///
/// The entire current-schema context H preimage is retained and recomputed.
/// Both named closure records must recompute to their closure2 identities and
/// have their declared manifest/tree bytes retained with exact hashes/lengths.
/// Named tools must be members of the toolchain tree; null linker/ar remains
/// absent. The declared compiler version and target must agree. The expected
/// host digest covers the full context, including fields beyond these joins.
///
/// The host digest must come from the caller's admitted selection. Success
/// proves none of the context's other semantic/admission obligations and emits
/// no NativeContextVerified frame. In particular there is no ambient-tool
/// fallback or executable-path selection here.
pub fn check_declared_tools(
    inputs: &RetainedInputs<'_>,
    context_digest: [u8; 32],
    expected_host_digest: [u8; 32],
    schema_work: usize,
) -> Result<CompilerToolChecks, CompilerToolError> {
    let context = inputs
        .frame_candidate(context_digest, NativeFrameSet::Context, schema_work)
        .map_err(CompilerToolError::Frame)?;
    if context.domain() != "native.context.rust.v2" {
        return Err(CompilerToolError::ForeignContext);
    }
    let descriptor = map(context.descriptor())?;
    let toolchain = map(field(descriptor, "toolchain")?)?;
    let tools = map(field(descriptor, "toolClosure")?)?;
    let dev_id = format!(
        "closure2:{}",
        text(field(toolchain, "rustcDevLlvmDigest")?)?
    );
    let dev = inputs.object(&dev_id, IdentityDomain::Closure, schema_work)?;
    let dev = map(dev.descriptor())?;
    require_kind(dev, "rust-dev-llvm")?;
    retain_tree(inputs, dev)?;
    let tool_id = text(field(tools, "closureId")?)?;
    let closure = inputs.object(tool_id, IdentityDomain::Closure, schema_work)?;
    let closure = map(closure.descriptor())?;
    require_kind(closure, "toolchain")?;
    let members = retain_tree(inputs, closure)?;
    for role in ["rustc", "cargo", "procMacroServer", "linker", "ar"] {
        let selected = field(tools, role)?;
        if matches!(selected, JsonValue::Null) {
            // Current shape admits null for only linker and ar.
            continue;
        }
        if !members.contains(&digest(text(selected)?)?) {
            return Err(CompilerToolError::ToolNotInClosure(role));
        }
    }
    if text(field(closure, "semanticVersion")?)? != text(field(toolchain, "rustcVersion")?)? {
        return Err(CompilerToolError::CompilerVersion);
    }
    if text(field(descriptor, "targetTriple")?)? != text(field(toolchain, "targetTriple")?)? {
        return Err(CompilerToolError::TargetTriple);
    }
    if context.digest() != expected_host_digest {
        return Err(CompilerToolError::HostContextMismatch);
    }
    Ok(CompilerToolChecks {
        context_digest: context.digest(),
        linker_present: !matches!(field(tools, "linker")?, JsonValue::Null),
    })
}

/// Raw retained system-input observations, not an admitted sysroot or stdlib.
#[derive(Debug)]
pub struct SystemInputChecks {
    tools: CompilerToolChecks,
    sysroot_digest: [u8; 32],
    declared_components: usize,
}
impl SystemInputChecks {
    pub fn tool_checks(&self) -> &CompilerToolChecks {
        &self.tools
    }
    pub fn sysroot_digest(&self) -> [u8; 32] {
        self.sysroot_digest
    }
    pub fn declared_components(&self) -> usize {
        self.declared_components
    }
}

#[derive(Debug)]
pub enum SystemInputError {
    Tools(CompilerToolError),
    ComponentOrder,
}

/// Observe exact retained sysroot/component preimages and declared component order.
///
/// Mandatory declared compiler-tool and full selected-host-context joins run
/// first. The sysrootDigest preimage and every declared component's raw bytes
/// must be retained and hash exactly. Component names must be strictly ascending
/// by UTF-8 bytes, which also excludes repeated names with differing digests.
/// An empty component declaration remains an empty observation, not a complete
/// standard library. Shared raw digests do not merge distinct component rows.
///
/// This diagnostic does not parse or admit a sysroot manifest, choose a stdlib
/// closure, establish component membership or completeness, validate signatures,
/// materialize a sysroot, choose a compiler path, emit NativeContextVerified or
/// authorize a provider. Those separate owner duties remain with the caller.
pub fn check_declared_system_inputs(
    inputs: &RetainedInputs<'_>,
    context_digest: [u8; 32],
    expected_host_digest: [u8; 32],
    schema_work: usize,
) -> Result<SystemInputChecks, SystemInputError> {
    let tools = check_declared_tools(inputs, context_digest, expected_host_digest, schema_work)
        .map_err(SystemInputError::Tools)?;
    let context = inputs
        .frame_candidate(context_digest, NativeFrameSet::Context, schema_work)
        .map_err(|e| SystemInputError::Tools(CompilerToolError::Frame(e)))?;
    let toolchain = map(field(map(context.descriptor())?, "toolchain")?)?;
    let JsonValue::Array(rows) = field(toolchain, "standardLibraryComponentDigests")? else {
        return Err(CompilerToolError::Representation.into());
    };
    // The order law is not a schema sequence rewrite; never sort claimant rows.
    let mut previous: Option<&str> = None;
    for row in rows {
        let component = text(field(map(row)?, "component")?)?;
        if previous.is_some_and(|p| p.as_bytes() >= component.as_bytes()) {
            return Err(SystemInputError::ComponentOrder);
        }
        previous = Some(component);
    }
    let sysroot_digest = digest(text(field(toolchain, "sysrootDigest")?)?)?;
    inputs
        .blob(sysroot_digest)
        .map_err(CompilerToolError::from)?;
    for row in rows {
        inputs
            .blob(digest(text(field(map(row)?, "sha256")?)?)?)
            .map_err(CompilerToolError::from)?;
    }
    Ok(SystemInputChecks {
        tools,
        sysroot_digest,
        declared_components: rows.len(),
    })
}

impl From<CompilerToolError> for SystemInputError {
    fn from(error: CompilerToolError) -> Self {
        Self::Tools(error)
    }
}

fn require_kind(
    closure: &BTreeMap<String, JsonValue>,
    expected: &'static str,
) -> Result<(), CompilerToolError> {
    if text(field(closure, "kind")?)? != expected {
        return Err(CompilerToolError::ClosureKind(expected));
    }
    Ok(())
}

fn retain_tree(
    inputs: &RetainedInputs<'_>,
    closure: &BTreeMap<String, JsonValue>,
) -> Result<BTreeSet<[u8; 32]>, CompilerToolError> {
    inputs.blob(digest(text(field(closure, "manifestDigest")?)?)?)?;
    let JsonValue::Array(rows) = field(closure, "tree")? else {
        return Err(CompilerToolError::Representation);
    };
    let mut members = BTreeSet::new();
    let mut lengths = BTreeMap::new();
    for row in rows {
        let row = map(row)?;
        let sha = digest(text(field(row, "sha256")?)?)?;
        let JsonValue::Integer(length) = field(row, "bytes")? else {
            return Err(CompilerToolError::Representation);
        };
        let length = u64::try_from(length.get()).map_err(|_| CompilerToolError::Representation)?;
        if let Some(previous) = lengths.get(&sha) {
            if *previous != length {
                return Err(RetainedInputError::BlobLength.into());
            }
        } else {
            inputs.blob(sha)?.require_length(length)?;
            lengths.insert(sha, length);
        }
        members.insert(sha);
    }
    Ok(members)
}

fn map(value: &JsonValue) -> Result<&BTreeMap<String, JsonValue>, CompilerToolError> {
    match value {
        JsonValue::Object(value) => Ok(value),
        _ => Err(CompilerToolError::Representation),
    }
}
fn field<'a>(
    value: &'a BTreeMap<String, JsonValue>,
    name: &str,
) -> Result<&'a JsonValue, CompilerToolError> {
    value.get(name).ok_or(CompilerToolError::Representation)
}
fn text(value: &JsonValue) -> Result<&str, CompilerToolError> {
    match value {
        JsonValue::String(value) => Ok(value),
        _ => Err(CompilerToolError::Representation),
    }
}
fn digest(value: &str) -> Result<[u8; 32], CompilerToolError> {
    if value.len() != 64 {
        return Err(CompilerToolError::Representation);
    }
    let mut result = [0; 32];
    for (index, chunk) in value.as_bytes().chunks_exact(2).enumerate() {
        let mut byte = 0;
        for digit in chunk {
            byte = (byte << 4)
                | match digit {
                    b'0'..=b'9' => digit - b'0',
                    b'a'..=b'f' => digit - b'a' + 10,
                    _ => return Err(CompilerToolError::Representation),
                };
        }
        result[index] = byte;
    }
    Ok(result)
}

#[cfg(test)]
#[path = "compiler_tools_tests.rs"]
mod tests;
