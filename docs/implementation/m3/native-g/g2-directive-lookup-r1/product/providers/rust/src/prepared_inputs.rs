//! Pure observations over selected inert prepared-output bytes.
//! No row here becomes admitted, usable compiler input or an execution grant.

use crate::universe_inputs::{
    UniverseInputChecks, UniverseInputError, UniverseInputRequest, check_declared_universe_inputs,
};
use opensip_identity::{
    CanonicalError, GraphError, JsonValue, NativeFrameSet, RetainedInputError, RetainedInputs,
    canonical_bytes, raw_sha256,
};
use std::collections::BTreeMap;

#[derive(Debug)]
pub enum PreparedInputError {
    Universe(UniverseInputError),
    Frame(GraphError),
    Retained(RetainedInputError),
    Canonical(CanonicalError),
    Representation,
    NonInert { row: usize },
    Binding { row: usize, field: &'static str },
    GeneratedBound { row: usize, field: &'static str },
}

/// Owner selections must come from the caller's independent host input boundary.
/// Comparing these digests and retaining their bytes does not admit security's
/// owner manifest semantics, ownership, signatures or execution authorization.
pub struct PreparedInputRequest<'a> {
    pub universe: UniverseInputRequest<'a>,
    pub owner_manifests: &'a BTreeMap<String, [u8; 32]>,
}

/// Inert observations; failed rows remain recorded and no usable-row token exists.
#[derive(Debug)]
pub struct PreparedInputChecks {
    universe: UniverseInputChecks,
    prepared_digest: Option<[u8; 32]>,
    row_count: usize,
    failed_rows: usize,
    generated_rows: usize,
}
impl PreparedInputChecks {
    pub fn universe_checks(&self) -> &UniverseInputChecks {
        &self.universe
    }
    pub fn prepared_digest(&self) -> Option<[u8; 32]> {
        self.prepared_digest
    }
    pub fn row_count(&self) -> usize {
        self.row_count
    }
    pub fn failed_rows(&self) -> usize {
        self.failed_rows
    }
    pub fn generated_rows(&self) -> usize {
        self.generated_rows
    }
}

/// Check the selected set's PO-0 inert kinds/media, PO-1 declared binding
/// equality and exact retained bytes, including generated and token references.
/// The mandatory universe/context/retained-record joins run first. Every row,
/// including failed rows, keeps its referenced bytes; none is executed or loaded.
/// The toolchain digest is raw SHA-256 of its retained canonical record, while
/// dependency identity remains the registered H identity. Each owner hash must
/// equal the caller-selected manifest hash and its raw bytes must be retained.
/// PO-4's published path-byte, file, per-owner and total generated bounds apply
/// to the declared generated references before their bytes are consumed.
///
/// A stale binding is a diagnostic error. The caller still owns PO-1's explicit
/// refusal/defaulted fallback and disclosure, full context/owner/import admission,
/// capture/producer correctness and any worker lookup. This returns neither
/// bind_rust_universe nor NativeContextVerified, Plan or host execution authority.
pub fn check_declared_prepared_inputs(
    inputs: &RetainedInputs<'_>,
    request: &PreparedInputRequest<'_>,
    schema_work: usize,
) -> Result<PreparedInputChecks, PreparedInputError> {
    let universe = check_declared_universe_inputs(inputs, &request.universe, schema_work)
        .map_err(PreparedInputError::Universe)?;
    let Some(prepared_digest) = request.universe.prepared_digest else {
        return Ok(PreparedInputChecks {
            universe,
            prepared_digest: None,
            row_count: 0,
            failed_rows: 0,
            generated_rows: 0,
        });
    };
    let frame = inputs
        .frame_candidate(prepared_digest, NativeFrameSet::Nested, schema_work)
        .map_err(PreparedInputError::Frame)?;
    // Mandatory universe checks already verified the exact selected domain/H.
    let set = map(frame.descriptor())?;
    let preparation = map(field(set, "preparation")?)?;
    let toolchain =
        canonical_bytes(field(preparation, "toolchain")?).map_err(PreparedInputError::Canonical)?;
    let toolchain_digest = raw_sha256(&toolchain);
    inputs
        .blob(toolchain_digest)
        .map_err(PreparedInputError::Retained)?;
    let rows = array(field(set, "rows")?)?;
    let mut failed_rows = 0;
    let mut generated_rows = 0;
    let mut per_owner = BTreeMap::<&str, usize>::new();
    let mut generated_bytes = 0u64;
    // A repeated reference is still checked for exact length, without hashing
    // the same immutable retained payload once per generated row.
    let mut retained_lengths = BTreeMap::new();
    for (index, row) in rows.iter().enumerate() {
        let row = map(row)?;
        let kind = text(field(row, "kind")?)?;
        let blob = map(field(row, "blob")?)?;
        if !inert_media(kind, text(field(blob, "mediaType")?)?) {
            return Err(PreparedInputError::NonInert { row: index });
        }
        let owner = text(field(row, "ownerKey")?)?;
        let binding = map(field(row, "inputBinding")?)?;
        let expected_owner =
            request
                .owner_manifests
                .get(owner)
                .ok_or(PreparedInputError::Binding {
                    row: index,
                    field: "ownerFileManifestSha256",
                })?;
        if digest(field(binding, "ownerFileManifestSha256")?)? != *expected_owner {
            return Err(PreparedInputError::Binding {
                row: index,
                field: "ownerFileManifestSha256",
            });
        }
        if digest(field(binding, "toolchainDigest")?)? != toolchain_digest {
            return Err(PreparedInputError::Binding {
                row: index,
                field: "toolchainDigest",
            });
        }
        for name in ["dependencySourceSetId", "cfgSetId"] {
            if field(binding, name)? != field(preparation, name)? {
                return Err(PreparedInputError::Binding {
                    row: index,
                    field: name,
                });
            }
        }
        inputs
            .blob(*expected_owner)
            .map_err(PreparedInputError::Retained)?;
        let generated = field(row, "generated")?;
        if kind == "generated-file" {
            let generated =
                map(generated).map_err(|_| PreparedInputError::NonInert { row: index })?;
            let path = text(field(generated, "logicalPath")?)?;
            if path.is_empty()
                || path.len() > 1024
                || path.starts_with('/')
                || path.contains(['\0', '\\'])
                || path.split('/').any(|part| part == "." || part == "..")
            {
                return Err(PreparedInputError::GeneratedBound {
                    row: index,
                    field: "maxLogicalPathBytes",
                });
            }
            let generated_blob = map(field(generated, "blob")?)?;
            if !inert_media(kind, text(field(generated_blob, "mediaType")?)?) {
                return Err(PreparedInputError::NonInert { row: index });
            }
            let bytes = length(field(generated_blob, "byteLength")?)?;
            if bytes > 67_108_864 {
                return Err(PreparedInputError::GeneratedBound {
                    row: index,
                    field: "maxGeneratedFileBytes",
                });
            }
            let count = per_owner.entry(owner).or_default();
            *count += 1;
            if *count > 4096 {
                return Err(PreparedInputError::GeneratedBound {
                    row: index,
                    field: "maxGeneratedFilesPerOwner",
                });
            }
            generated_bytes =
                generated_bytes
                    .checked_add(bytes)
                    .ok_or(PreparedInputError::GeneratedBound {
                        row: index,
                        field: "maxGeneratedTotalBytes",
                    })?;
            if generated_bytes > 1_073_741_824 {
                return Err(PreparedInputError::GeneratedBound {
                    row: index,
                    field: "maxGeneratedTotalBytes",
                });
            }
            retain_blob(inputs, generated_blob, &mut retained_lengths)?;
            generated_rows += 1;
        } else if !matches!(generated, JsonValue::Null) {
            return Err(PreparedInputError::NonInert { row: index });
        }
        retain_blob(inputs, blob, &mut retained_lengths)?;
        if let JsonValue::Object(site) = field(row, "site")? {
            inputs
                .blob(digest(field(site, "inputTokenDigest")?)?)
                .map_err(PreparedInputError::Retained)?;
        }
        if text(field(row, "status")?)? == "failed" {
            failed_rows += 1;
        }
    }
    Ok(PreparedInputChecks {
        universe,
        prepared_digest: Some(prepared_digest),
        row_count: rows.len(),
        failed_rows,
        generated_rows,
    })
}

/// Observation over declared inert bytes; not a worker input or admission token.
#[derive(Debug)]
pub enum DeclaredGeneratedFile {
    Missing,
    OutOfBounds,
    Bytes(std::sync::Arc<[u8]>),
}
#[derive(Debug)]
pub enum GeneratedLookupError {
    Prepared(PreparedInputError),
    Ambiguous,
}

impl From<PreparedInputError> for GeneratedLookupError {
    fn from(value: PreparedInputError) -> Self {
        Self::Prepared(value)
    }
}

/// Join a generated file by exact owner and OUT_DIR-relative logical path.
/// Existing mandatory prepared/universe/context/binding/inert/byte/bound checks
/// run first; stale records remain diagnostic errors, never usable blobs.
/// Failed build-script owners and failed generated rows supply no bytes. An
/// exact miss remains Missing; escaping/oversized request paths are OutOfBounds.
/// Duplicate matching rows are an ambiguous local input error, never first/last
/// selection. Success owns retained immutable inner generated blob bytes only.
///
/// Caller still admits the owner/context/import and implements PO-1 fallback,
/// PO-2 typed unknown edges, and PO-4 read-only VFS and the three include channels.
/// This does not construct a virtual or host path, decode/compile/load/execute
/// data, authorize a worker, mint identities, or turn media labels into trust.
pub fn lookup_declared_generated_file(
    inputs: &RetainedInputs<'_>,
    request: &PreparedInputRequest<'_>,
    owner_key: &str,
    logical_path: &str,
    schema_work: usize,
) -> Result<DeclaredGeneratedFile, GeneratedLookupError> {
    check_declared_prepared_inputs(inputs, request, schema_work)
        .map_err(GeneratedLookupError::Prepared)?;
    if logical_path.is_empty()
        || logical_path.len() > 1024
        || logical_path.starts_with('/')
        || logical_path.contains(['\0', '\\'])
        || logical_path
            .split('/')
            .any(|part| part == "." || part == "..")
    {
        return Ok(DeclaredGeneratedFile::OutOfBounds);
    }
    let Some(prepared_digest) = request.universe.prepared_digest else {
        return Ok(DeclaredGeneratedFile::Missing);
    };

    let frame = inputs
        .frame_candidate(prepared_digest, NativeFrameSet::Nested, schema_work)
        .map_err(PreparedInputError::Frame)?;
    let rows = array(field(map(frame.descriptor())?, "rows")?)?;
    // Whole-set pass: a later failed script must not be hidden by an earlier
    // generated row. Configuration/binding admission is owned by the caller.
    for row in rows {
        let row = map(row)?;
        if text(field(row, "ownerKey")?)? == owner_key
            && text(field(row, "kind")?)? == "build-script-directives"
            && text(field(row, "status")?)? == "failed"
        {
            return Ok(DeclaredGeneratedFile::Missing);
        }
    }
    let mut selected = None;

    for row in rows {
        let row = map(row)?;
        if text(field(row, "ownerKey")?)? != owner_key
            || text(field(row, "kind")?)? != "generated-file"
            || text(field(row, "status")?)? != "ok"
        {
            continue;
        }
        let generated = map(field(row, "generated")?)?;
        if text(field(generated, "logicalPath")?)? == logical_path {
            if selected.is_some() {
                // Distinct rows can share a lookup tuple despite uniqueItems.
                return Err(GeneratedLookupError::Ambiguous);
            }
            selected = Some(digest(field(map(field(generated, "blob")?)?, "sha256")?)?);
        }
    }
    match selected {
        Some(sha) => Ok(DeclaredGeneratedFile::Bytes(std::sync::Arc::from(
            inputs
                .blob(sha)
                .map_err(PreparedInputError::Retained)?
                .bytes(),
        ))),
        None => Ok(DeclaredGeneratedFile::Missing),
    }
}

/// Caller-selected site observations, not a verified parser or macro invocation.
pub struct DeclaredExpansionSite<'a> {
    pub path: &'a str,
    pub start_byte: u64,
    pub end_byte: u64,
    pub input_token_digest: [u8; 32],
    pub macro_crate_manifest_sha256: [u8; 32],
}
/// Inert candidate bytes; caller owns admission and compiler consumption.
#[derive(Debug)]
pub enum DeclaredMacroExpansion {
    Missing,
    Bytes(std::sync::Arc<[u8]>),
}

#[derive(Debug)]
pub enum MacroLookupError {
    Prepared(PreparedInputError),
    Ambiguous,
}
impl From<PreparedInputError> for MacroLookupError {
    fn from(value: PreparedInputError) -> Self {
        Self::Prepared(value)
    }
}

/// Join by the published exact (path, span, input token digest, macro manifest)
/// tuple after all mandatory declared prepared checks. Only ok expansion rows
/// can select bytes; failed rows stay retained observations. Distinct matching
/// rows give the local Ambiguous error instead of choosing by order.
/// No parser/span/token provenance, macro ownership producer, worker admission,
/// typed unresolved edge, compilation, process or identity authority is granted.
pub fn lookup_declared_macro_expansion(
    inputs: &RetainedInputs<'_>,
    request: &PreparedInputRequest<'_>,
    site: &DeclaredExpansionSite<'_>,
    schema_work: usize,
) -> Result<DeclaredMacroExpansion, MacroLookupError> {
    check_declared_prepared_inputs(inputs, request, schema_work)
        .map_err(MacroLookupError::Prepared)?;
    let Some(prepared_digest) = request.universe.prepared_digest else {
        return Ok(DeclaredMacroExpansion::Missing);
    };
    let frame = inputs
        .frame_candidate(prepared_digest, NativeFrameSet::Nested, schema_work)
        .map_err(PreparedInputError::Frame)?;
    let rows = array(field(map(frame.descriptor())?, "rows")?)?;
    let mut selected = None;
    for row in rows {
        let row = map(row)?;
        if text(field(row, "kind")?)? != "macro-expansion" || text(field(row, "status")?)? != "ok" {
            continue;
        }
        let JsonValue::Object(candidate) = field(row, "site")? else {
            continue;
        };
        let binding = map(field(row, "inputBinding")?)?;
        if text(field(candidate, "path")?)? != site.path
            || length(field(candidate, "startByte")?)? != site.start_byte
            || length(field(candidate, "endByte")?)? != site.end_byte
            || digest(field(candidate, "inputTokenDigest")?)? != site.input_token_digest
            || digest(field(binding, "ownerFileManifestSha256")?)?
                != site.macro_crate_manifest_sha256
        {
            continue;
        }
        if selected.is_some() {
            return Err(MacroLookupError::Ambiguous);
        }
        selected = Some(digest(field(map(field(row, "blob")?)?, "sha256")?)?);
    }
    match selected {
        Some(sha) => Ok(DeclaredMacroExpansion::Bytes(std::sync::Arc::from(
            inputs
                .blob(sha)
                .map_err(PreparedInputError::Retained)?
                .bytes(),
        ))),
        None => Ok(DeclaredMacroExpansion::Missing),
    }
}

/// Inert declared directive output, not admitted cfg or environment settings.
#[derive(Debug)]
pub enum DeclaredBuildScriptDirectives {
    Missing,
    Bytes(std::sync::Arc<[u8]>),
}
#[derive(Debug)]
pub enum DirectiveLookupError {
    Prepared(PreparedInputError),
    Ambiguous,
}
impl From<PreparedInputError> for DirectiveLookupError {
    fn from(value: PreparedInputError) -> Self {
        Self::Prepared(value)
    }
}

/// Observe retained directive bytes for an exact owner after whole-set checks.
/// PO-2 failed build-script owners supply no directive bytes, irrespective of
/// row order. Only ok build-script-directives rows match. Multiple matching ok
/// rows are a local ambiguity error, never an implicit concatenation or priority.
/// Bytes remain uninterpreted: no directive parser, cfg/env application, Cargo
/// execution, faithful producer, owner/context/import admission, fallback or
/// worker authority is supplied by this observation.
pub fn lookup_declared_build_script_directives(
    inputs: &RetainedInputs<'_>,
    request: &PreparedInputRequest<'_>,
    owner_key: &str,
    schema_work: usize,
) -> Result<DeclaredBuildScriptDirectives, DirectiveLookupError> {
    check_declared_prepared_inputs(inputs, request, schema_work)
        .map_err(DirectiveLookupError::Prepared)?;
    let Some(prepared_digest) = request.universe.prepared_digest else {
        return Ok(DeclaredBuildScriptDirectives::Missing);
    };
    let frame = inputs
        .frame_candidate(prepared_digest, NativeFrameSet::Nested, schema_work)
        .map_err(PreparedInputError::Frame)?;
    let rows = array(field(map(frame.descriptor())?, "rows")?)?;
    for row in rows {
        let row = map(row)?;
        if text(field(row, "ownerKey")?)? == owner_key
            && text(field(row, "kind")?)? == "build-script-directives"
            && text(field(row, "status")?)? == "failed"
        {
            return Ok(DeclaredBuildScriptDirectives::Missing);
        }
    }
    let mut selected = None;
    for row in rows {
        let row = map(row)?;
        if text(field(row, "ownerKey")?)? != owner_key
            || text(field(row, "kind")?)? != "build-script-directives"
            || text(field(row, "status")?)? != "ok"
        {
            continue;
        }
        if selected.is_some() {
            return Err(DirectiveLookupError::Ambiguous);
        }
        selected = Some(digest(field(map(field(row, "blob")?)?, "sha256")?)?);
    }
    match selected {
        Some(sha) => Ok(DeclaredBuildScriptDirectives::Bytes(std::sync::Arc::from(
            inputs
                .blob(sha)
                .map_err(PreparedInputError::Retained)?
                .bytes(),
        ))),
        None => Ok(DeclaredBuildScriptDirectives::Missing),
    }
}

fn inert_media(kind: &str, media: &str) -> bool {
    match kind {
        "build-script-directives" => media == "text/x-cargo-directives",
        "macro-expansion" => media == "text/x-rust-expansion",
        "generated-file" => matches!(
            media,
            "text/x-rust-source" | "text/plain" | "application/octet-stream"
        ),
        _ => false,
    }
}
fn retain_blob(
    inputs: &RetainedInputs<'_>,
    blob: &BTreeMap<String, JsonValue>,
    checked: &mut BTreeMap<[u8; 32], u64>,
) -> Result<(), PreparedInputError> {
    let sha = digest(field(blob, "sha256")?)?;
    let bytes = length(field(blob, "byteLength")?)?;
    if let Some(previous) = checked.get(&sha) {
        if *previous != bytes {
            return Err(PreparedInputError::Retained(RetainedInputError::BlobLength));
        }
    } else {
        inputs
            .blob(sha)
            .map_err(PreparedInputError::Retained)?
            .require_length(bytes)
            .map_err(PreparedInputError::Retained)?;
        checked.insert(sha, bytes);
    }
    Ok(())
}
fn map(value: &JsonValue) -> Result<&BTreeMap<String, JsonValue>, PreparedInputError> {
    match value {
        JsonValue::Object(value) => Ok(value),
        _ => Err(PreparedInputError::Representation),
    }
}
fn field<'a>(
    value: &'a BTreeMap<String, JsonValue>,
    key: &str,
) -> Result<&'a JsonValue, PreparedInputError> {
    value.get(key).ok_or(PreparedInputError::Representation)
}
fn text(value: &JsonValue) -> Result<&str, PreparedInputError> {
    match value {
        JsonValue::String(value) => Ok(value),
        _ => Err(PreparedInputError::Representation),
    }
}
fn array(value: &JsonValue) -> Result<&[JsonValue], PreparedInputError> {
    match value {
        JsonValue::Array(value) => Ok(value),
        _ => Err(PreparedInputError::Representation),
    }
}
fn length(value: &JsonValue) -> Result<u64, PreparedInputError> {
    match value {
        JsonValue::Integer(value) => {
            u64::try_from(value.get()).map_err(|_| PreparedInputError::Representation)
        }
        _ => Err(PreparedInputError::Representation),
    }
}
fn digest(value: &JsonValue) -> Result<[u8; 32], PreparedInputError> {
    let value = text(value)?;
    if value.len() != 64 {
        return Err(PreparedInputError::Representation);
    }
    let mut digest = [0; 32];
    for (i, pair) in value.as_bytes().chunks_exact(2).enumerate() {
        let digit = |b| match b {
            b'0'..=b'9' => Ok(b - b'0'),
            b'a'..=b'f' => Ok(b - b'a' + 10),
            _ => Err(PreparedInputError::Representation),
        };
        digest[i] = digit(pair[0])? << 4 | digit(pair[1])?;
    }
    Ok(digest)
}

#[cfg(test)]
#[path = "prepared_inputs_tests.rs"]
mod tests;
