//! Diagnostic selection of a declared Rust body dialect.
//! No body identity, enumerator qualification or context admission is granted.

use crate::universe_inputs::{
    UniverseInputChecks, UniverseInputError, UniverseInputRequest, check_declared_universe_inputs,
};
use opensip_identity::{GraphError, JsonValue, NativeFrameSet, RetainedInputs};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug)]
pub enum BodyDialectError {
    Inputs(UniverseInputError),
    Frame(GraphError),
    Representation,
    MissingOwnership,
    PartialEnumeration,
    NotCompiled,
    NotSelected,
    AmbiguousEdition,
}

/// An observation over caller-declared ownership, not a language identity token.
#[derive(Debug)]
pub struct BodyDialectChecks {
    inputs: UniverseInputChecks,
    edition: u16,
    selected_owner_count: usize,
}
impl BodyDialectChecks {
    pub fn input_checks(&self) -> &UniverseInputChecks {
        &self.inputs
    }
    pub fn edition(&self) -> u16 {
        self.edition
    }
    pub fn selected_owner_count(&self) -> usize {
        self.selected_owner_count
    }
}

/// Apply the published exact-path/selected-owner dialect decision after the
/// mandatory retained universe/context/snapshot joins. Target overrides win;
/// null overrides use only that target's crate entry in the edition map.
/// Partial enumeration refuses before this selector inspects relation rows.
/// There is no single-edition shortcut, prefix lookup, nearest-directory rule,
/// first-owner rule or inference from the requested source filename.
///
/// The result describes a declared edition only. It does not qualify the table
/// producer, retain every raw source, bind compiler language-version bytes, mint
/// a clones identity or Coverage, admit a context/Plan, or execute anything.
/// Structural admission and retained joins independently precede this selector;
/// malformed retained records are not converted into dialect refusal causes.
pub fn check_declared_body_dialect(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    anchor_path: &str,
    schema_work: usize,
) -> Result<BodyDialectChecks, BodyDialectError> {
    let checked = check_declared_universe_inputs(inputs, request, schema_work)
        .map_err(BodyDialectError::Inputs)?;
    let ownership_digest = request
        .ownership_digest
        .ok_or(BodyDialectError::MissingOwnership)?;
    let ownership = inputs
        .frame_candidate(ownership_digest, NativeFrameSet::Nested, schema_work)
        .map_err(BodyDialectError::Frame)?;
    // The mandatory join already checks the domain and selected ownership id.
    let o = map(ownership.descriptor())?;
    if text(field(o, "enumeration")?)? == "partial" {
        return Err(BodyDialectError::PartialEnumeration);
    }
    let selected: BTreeSet<_> = array(field(o, "selectedUnitIds")?)?
        .iter()
        .map(text)
        .collect::<Result<_, _>>()?;
    let mut owners = BTreeSet::new();
    let mut compiled = false;
    for row in array(field(o, "ownership")?)? {
        let row = map(row)?;
        if text(field(row, "path")?)? == anchor_path {
            compiled = true;
            let unit = text(field(row, "unitId")?)?;
            if selected.contains(unit) {
                owners.insert(unit);
            }
        }
    }
    if !compiled {
        return Err(BodyDialectError::NotCompiled);
    }
    if owners.is_empty() {
        return Err(BodyDialectError::NotSelected);
    }
    let universe = inputs
        .frame_candidate(
            request.universe_digest,
            NativeFrameSet::SemanticUniverse,
            schema_work,
        )
        .map_err(BodyDialectError::Frame)?;
    let defaults = map(field(map(universe.descriptor())?, "edition")?)?;
    let mut editions = BTreeSet::new();
    for unit in array(field(o, "units")?)? {
        let unit = map(unit)?;
        if owners.contains(text(field(unit, "unitId")?)?) {
            let declared = field(unit, "targetEdition")?;
            let value = if matches!(declared, JsonValue::Null) {
                field(defaults, text(field(unit, "crateName")?)?)?
            } else {
                declared
            };
            let JsonValue::Integer(value) = value else {
                return Err(BodyDialectError::Representation);
            };
            let edition =
                u16::try_from(value.get()).map_err(|_| BodyDialectError::Representation)?;
            editions.insert(edition);
        }
    }
    if editions.len() != 1 {
        return Err(BodyDialectError::AmbiguousEdition);
    }
    Ok(BodyDialectChecks {
        inputs: checked,
        edition: *editions
            .iter()
            .next()
            .ok_or(BodyDialectError::Representation)?,
        selected_owner_count: owners.len(),
    })
}

/// A derived record candidate over declared inputs, not a FACT-IDENTITY token.
#[derive(Debug)]
pub struct DeclaredBodyLanguageVersion {
    dialect: BodyDialectChecks,
    tools: crate::compiler_tools::CompilerToolChecks,
    canonical_record: Vec<u8>,
    record_sha256: [u8; 32],
}
impl DeclaredBodyLanguageVersion {
    pub fn dialect_checks(&self) -> &BodyDialectChecks {
        &self.dialect
    }
    pub fn tool_checks(&self) -> &crate::compiler_tools::CompilerToolChecks {
        &self.tools
    }
    /// Canonical closed body-language-version candidate, not an admitted record.
    pub fn canonical_record(&self) -> &[u8] {
        &self.canonical_record
    }
    /// Raw SHA-256 of the canonical candidate; no H frame or textual prefix.
    pub fn record_sha256(&self) -> [u8; 32] {
        self.record_sha256
    }
}
#[derive(Debug)]
pub enum BodyLanguageVersionError {
    Dialect(BodyDialectError),
    Tools(crate::compiler_tools::CompilerToolError),
    Frame(GraphError),
    Record(opensip_identity::CanonicalError),
    Representation,
}

/// Derive the exact declared Rust body-language-version record and raw digest.
/// The mandatory retained universe/context/snapshot/ownership and exact-anchor
/// selected-owner edition checks run first, with no single-edition shortcut.
/// The declared compiler-tool/dev closure and expected host-context joins then
/// run; rustcVersion must equal the retained tool closure descriptor version.
/// CompilerName is rustc, languageId is rust, compilerVersion is rustcVersion,
/// compilerBuild is rustCommitHash, and dialect is the selected edition only.
///
/// Operational platforms, sysroot/stdlib/backend/build/resolution/configuration
/// fields, unrelated crates, paths and owner counts do not enter this record.
/// Their changes still require coherent current full context/universe inputs.
/// This candidate supplies the published canonical-byte recipe only: retained
/// declarations do not admit signed manifest semantics, context, ownership
/// producer or normalizer. No clones body frame, Coverage, NativeContextVerified,
/// Plan/Run or provider authority is minted or authorized here.
pub fn derive_declared_body_language_version(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    anchor_path: &str,
    schema_work: usize,
) -> Result<DeclaredBodyLanguageVersion, BodyLanguageVersionError> {
    let dialect = check_declared_body_dialect(inputs, request, anchor_path, schema_work)
        .map_err(BodyLanguageVersionError::Dialect)?;
    let tools = crate::compiler_tools::check_declared_tools(
        inputs,
        request.context_digest,
        request.expected_host_digest,
        schema_work,
    )
    .map_err(BodyLanguageVersionError::Tools)?;
    let context = inputs
        .frame_candidate(request.context_digest, NativeFrameSet::Context, schema_work)
        .map_err(BodyLanguageVersionError::Frame)?;
    let toolchain = map(field(
        map(context.descriptor()).map_err(BodyLanguageVersionError::Dialect)?,
        "toolchain",
    )
    .map_err(BodyLanguageVersionError::Dialect)?)
    .map_err(BodyLanguageVersionError::Dialect)?;
    let record = JsonValue::Object(BTreeMap::from([
        (
            "schemaVersion".into(),
            JsonValue::Integer(
                opensip_identity::JsonInteger::new(1)
                    .map_err(|_| BodyLanguageVersionError::Representation)?,
            ),
        ),
        ("languageId".into(), JsonValue::String("rust".into())),
        ("compilerName".into(), JsonValue::String("rustc".into())),
        (
            "compilerVersion".into(),
            field(toolchain, "rustcVersion")
                .map_err(BodyLanguageVersionError::Dialect)?
                .clone(),
        ),
        (
            "compilerBuild".into(),
            field(toolchain, "rustCommitHash")
                .map_err(BodyLanguageVersionError::Dialect)?
                .clone(),
        ),
        (
            "dialect".into(),
            JsonValue::Object(BTreeMap::from([(
                "edition".into(),
                JsonValue::Integer(
                    opensip_identity::JsonInteger::new(i128::from(dialect.edition()))
                        .map_err(|_| BodyLanguageVersionError::Representation)?,
                ),
            )])),
        ),
    ]));
    let canonical_record =
        opensip_identity::canonical_bytes(&record).map_err(BodyLanguageVersionError::Record)?;
    let record_sha256 = opensip_identity::raw_sha256(&canonical_record);
    Ok(DeclaredBodyLanguageVersion {
        dialect,
        tools,
        canonical_record,
        record_sha256,
    })
}

fn map(value: &JsonValue) -> Result<&BTreeMap<String, JsonValue>, BodyDialectError> {
    match value {
        JsonValue::Object(value) => Ok(value),
        _ => Err(BodyDialectError::Representation),
    }
}
fn field<'a>(
    value: &'a BTreeMap<String, JsonValue>,
    key: &str,
) -> Result<&'a JsonValue, BodyDialectError> {
    value.get(key).ok_or(BodyDialectError::Representation)
}
fn array(value: &JsonValue) -> Result<&[JsonValue], BodyDialectError> {
    match value {
        JsonValue::Array(value) => Ok(value),
        _ => Err(BodyDialectError::Representation),
    }
}
fn text(value: &JsonValue) -> Result<&str, BodyDialectError> {
    match value {
        JsonValue::String(value) => Ok(value),
        _ => Err(BodyDialectError::Representation),
    }
}

#[cfg(test)]
#[path = "body_dialect_tests.rs"]
mod tests;
