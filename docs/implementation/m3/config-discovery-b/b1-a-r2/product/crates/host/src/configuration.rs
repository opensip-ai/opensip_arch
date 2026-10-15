//! The configuration resolver. Law X12 r3 (unit X12b) gave it policy-pack
//! admission (item 1); law M3-B r4 (unit B1-a) adds the six-layer resolution
//! pipeline (items 1 to 8 and 11) and the X12 r4 order (item 10): `resolve`
//! runs first, then `admit_policy_selection` on the resolved pack IDs, once.
//! Discovery (B2), the carriers' capture and the invocation mode (B1-b) stay
//! outside: the resolver is pure over captured bytes and typed observations.
//!
//! X12 item 8: admission is pure. It does no I/O, takes no lock and charges no
//! ledger, so the analysis request (M3) can and must run it first, before any
//! write or project admission, fence, provider, snapshot, facts or Coverage
//! consumption, Plan construction or evaluation; a refusal has nothing to
//! clean up. Its only admission call is `admit_pack`; the host's part is the
//! selection count, the embedded schema registry and the public mapping
//! (item 7). Library only: no CLI command or analysis request calls it yet.
use crate::InstallationTerminationV1;
use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4D9ErrorCode as Code, Common4D9FaultCause as Fault,
    Common4DomainDetailCode as Detail,
};
use opensip_evaluator::{AdmittedPack, PackDefect, PackRefusal, PackSource, admit_pack};
use opensip_identity::{
    JsonInteger, JsonValue as V, RegisteredSchemas, canonical_bytes, digest_hex, parse_json,
    raw_sha256,
};
use std::collections::BTreeMap;

/// `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]`, byte for byte as contract
/// successor B-S9 widened it (line 1158 of its selected native reference copy,
/// superseding X12-0's text). The remedy is keyed by the public code, so X12
/// rows 1, 2 and 3a and every external configuration refusal (M3-B r4 item 4)
/// carry this one string.
pub(crate) const REMEDY_CONFIG_INVALID: &str = "the configuration or selection is invalid: make each configuration file, flag and request well-formed for its schema and layer, with no unknown key, a supported schemaVersion, canonical project-relative paths that exist, and a nonempty workspaceRoots when one is given; name only a registered profile and registered or admitted ids, and state each component once with no conflicting pin and hold; for capabilities, name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of your own or from a third party";
/// Row 3's caller remedy: the command inventory's `POLICY.IMPERATIVE_KEY_REFUSED`
/// row (workflows-and-surfaces §5).
pub(crate) const REMEDY_IMPERATIVE_KEY: &str = "the policy DSL is declarative data only";

/// Why a policy selection was not admitted. Every value maps to exactly one
/// row of item 7 through `policy_selection_termination`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum PolicySelectionRefusal {
    /// Row 1: a selection of zero, or more than one, sources.
    Count(usize),
    /// The evaluator's refusal of the one source, unchanged (rows 1 to 4).
    Pack(PackRefusal),
}

/// Admit the policy selection of an analysis request (items 5 and 8): exactly
/// one source, admitted by the evaluator against the bundled registry. The
/// result is the evaluator's own `AdmittedPack`, unwrapped.
pub(crate) fn admit_policy_selection(
    selection: &[PackSource<'_>],
) -> Result<AdmittedPack, PolicySelectionRefusal> {
    let [source] = selection else {
        return Err(PolicySelectionRefusal::Count(selection.len()));
    };
    // The host's exact pinned schema registry, for item 6.3 only. It cannot
    // fail on the embedded sources; if it does, that is the signed core's
    // fault (row 4), with the subject the evaluator gives its own faults.
    let schemas = crate::embedded_schema_registry().map_err(|_| {
        PolicySelectionRefusal::Pack(PackRefusal::HostInvariant {
            subject: host_fault_subject(source),
            defect: PackDefect::Registry,
        })
    })?;
    admit_pack(&schemas, source).map_err(PolicySelectionRefusal::Pack)
}

/// Row 4's subject for a fault found before the evaluator sees the source:
/// `pack:<presented id>`, or the supplied bytes' digest subject.
fn host_fault_subject(source: &PackSource<'_>) -> String {
    match source {
        PackSource::Named(id) => format!("pack:{id}"),
        PackSource::Supplied { bytes, provenance } => format!(
            "supplied:{}:sha256:{}",
            provenance.name(),
            digest_hex(&raw_sha256(bytes))
        ),
    }
}

/// Item 7: the one public termination of each refusal, in law 468 r5 item
/// 6's shape. The match is exhaustive with no wildcard arm, so a new refusal
/// cannot compile without its row. No new code: every code is an existing
/// generated member.
pub(crate) fn policy_selection_termination(
    refusal: &PolicySelectionRefusal,
) -> InstallationTerminationV1 {
    let rejected = |detail, subject| InstallationTerminationV1 {
        class: Class::RequestRejected,
        exit: 2,
        error_code: Code::ConfigInvalid,
        fault_cause: Fault::None,
        detail: Some(detail),
        subject: Some(subject),
    };
    match refusal {
        // Row 1, selection count.
        PolicySelectionRefusal::Count(n) => rejected(Detail::ConfigInvalid, format!("count:{n}")),
        PolicySelectionRefusal::Pack(pack) => match pack {
            // Row 1: the presented ID.
            PackRefusal::NotBundled { .. } => rejected(Detail::ConfigInvalid, pack.subject()),
            // Row 2: `supplied:<provenance>:sha256:<hex>`.
            PackRefusal::SuppliedPack { .. } => rejected(Detail::ConfigInvalid, pack.subject()),
            // Row 3: a caller document's imperative member, by its pointer.
            PackRefusal::ImperativeMember { .. } => {
                rejected(Detail::PolicyImperativeKeyRefused, pack.subject())
            }
            // Row 3a: `supplied:<provenance>:sha256:<hex>`.
            PackRefusal::SuppliedInvalid { .. } => rejected(Detail::ConfigInvalid, pack.subject()),
            // Row 4: a defect in the signed core, never the caller's input.
            PackRefusal::HostInvariant { .. } => InstallationTerminationV1 {
                class: Class::OperationalFailed,
                exit: 4,
                error_code: Code::SystemOutcomeIllegalState,
                fault_cause: Fault::HostInvariant,
                detail: Some(Detail::HostInvariantViolated),
                subject: Some(pack.subject()),
            },
        },
    }
}

// ---------------------------------------------------------------------------
// M3-B r4, unit B1-a: the configuration resolver (items 1 to 8 and 11).
// ---------------------------------------------------------------------------

// The generated registries (item 8): `tools/host/generate_configuration_tables.py`.
#[path = "configuration_tables.rs"]
mod tables;
use tables::{
    CapabilityId, FIELDS, FieldClass, LanguageMode, Layer, NOT_SELECTED_CELLS, PROFILE_IDS,
    SharedFlag,
};

/// The pinned product configuration schema (PCS) and the exact preview carrier
/// schema for schema-one files (item 11), as `SOURCE_PINS` admits them.
const PCS_ID: &str = "urn:opensip:product-configuration:2";
const PREVIEW_ID: &str = "urn:opensip:preview-configuration:1";
/// Step 10: the resolved shape, identity-v3 `semantic-configuration`.
const IDENTITY_ID: &str = "urn:opensip:product-v1:identity:v3";
const SEMANTIC_SELECTOR: &str = "/$defs/semantic-configuration";
/// The schema evaluator's work bound for one document, as the shared failure
/// envelope check uses it. Exhaustion refuses the document; it never passes.
const SCHEMA_BUDGET: usize = 64 * 1024 * 1024;

/// One captured configuration carrier (B1-b captures it by retained descriptor
/// after its custody judgment): its path relative to the project root or to
/// the installation, and its exact bytes. The resolver hashes the bytes itself.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct CapturedCarrierV1 {
    pub(crate) path: String,
    pub(crate) bytes: Vec<u8>,
}

/// One component's version, as PCS's `pins` and `holds` items spell it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ComponentVersionV1 {
    pub(crate) stable_id: String,
    pub(crate) version: String,
}

/// A component request: an exact version, an exact constraint string, or a
/// range (PCS `components.request` items).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ComponentRequestV1 {
    Version(ComponentVersionV1),
    Constraint {
        stable_id: String,
        constraint: String,
    },
    Range {
        stable_id: String,
        min: String,
        max: String,
        include_min: bool,
        include_max: bool,
    },
}

/// Layer 1, host-built from the authenticated release declaration and the
/// signed install profile (item 2). Every field is optional so that a missing
/// compiled value reaches step 7 as `CONFIG_DEFAULTS_INCOMPLETE`; B1-a fixes
/// no value. It is admitted as an internal layer (B1-a plan r2, RF-02).
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub(crate) struct CompiledDefaultsV1 {
    pub(crate) profile_id: Option<String>,
    pub(crate) capabilities: Option<Vec<String>>,
    pub(crate) budget_limit: Option<u64>,
    pub(crate) request: Option<Vec<ComponentRequestV1>>,
    pub(crate) pins: Option<Vec<ComponentVersionV1>>,
    pub(crate) holds: Option<Vec<ComponentVersionV1>>,
    pub(crate) allowed_scopes: Option<Vec<String>>,
    pub(crate) pack_ids: Option<Vec<String>>,
}

/// Layer 6, host-built from typed parsed flags. At M3 only `--workspace-root`
/// is configuration (item 2); the other six shared flags are not (item 23). A
/// plain typed carrier: the resolver's admission is its validity check.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub(crate) struct FlagLayerV1 {
    pub(crate) workspace_roots: Option<Vec<String>>,
}

/// Item 3: interactive exactly when standard input and standard error are both
/// terminals (computed once by the host entry, never from the environment).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct InvocationModeV1 {
    pub(crate) interactive: bool,
}

/// The resolver's whole input. Layer 5, the environment, is a typed constant:
/// empty. It is not a parameter.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ResolverInputV1 {
    pub(crate) defaults: CompiledDefaultsV1,
    pub(crate) global: Option<CapturedCarrierV1>,
    pub(crate) project: Option<CapturedCarrierV1>,
    /// Never read when `mode.interactive` is false.
    pub(crate) local: Option<CapturedCarrierV1>,
    pub(crate) flags: FlagLayerV1,
    pub(crate) mode: InvocationModeV1,
}

/// Where a winning leaf came from (item 5). Never part of any digest.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ProvenanceSourceV1 {
    /// Layer 1. At M3 the discovery fold is empty, so no leaf is `DISCOVERED`.
    Defaulted,
    /// A captured carrier, its exact bytes' SHA-256 and source schema version.
    Carrier {
        path: String,
        sha256: String,
        source_schema_version: u8,
    },
    /// The host-built flag layer.
    Flags,
}

/// Item 5: the deciding layer, the winning value as that layer gave it, and
/// its source.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct LeafProvenanceV1 {
    pub(crate) layer: Layer,
    pub(crate) value: V,
    pub(crate) source: ProvenanceSourceV1,
}

/// Item 5: the resolved configuration. `semantic` is the normalized record
/// identity-v3 `semantic-configuration` admits; `operational` holds the
/// `host.operability.nonsemantic` leaves (item 7); provenance is keyed by
/// `section.field`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ResolvedConfigurationV1 {
    pub(crate) semantic: V,
    pub(crate) operational: V,
    pub(crate) provenance: BTreeMap<String, LeafProvenanceV1>,
    /// Item 6: lowercase hex SHA-256 of the semantic record's canonical bytes.
    pub(crate) resolved_config_digest: String,
}

impl ResolvedConfigurationV1 {
    /// The resolved `policy.packIds`, in their normalized order (item 10).
    pub(crate) fn pack_ids(&self) -> Vec<&str> {
        if let V::Object(semantic) = &self.semantic
            && let Some(V::Object(policy)) = semantic.get("policy")
            && let Some(ids) = policy.get("packIds")
        {
            strings(ids)
        } else {
            Vec::new()
        }
    }
}

/// The pipeline step at which a refusal arose (item 4's order).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ConfigurationStep {
    Lexical,
    Schema,
    SchemaOne,
    Allowlist,
    LogicalPath,
    Profile,
    Capability,
    Waiver,
    Component,
    DefaultsComplete,
    Semantic,
}

/// Why a configuration did not resolve. The row is chosen by the layer's kind,
/// not by the step: an external carrier's defect is `CONFIG.INVALID`; a
/// host-built layer's defect, incomplete defaults or an invalid resolved record
/// is the host invariant (item 4; AQ section 1).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ConfigurationRefusal {
    Invalid {
        step: ConfigurationStep,
        subject: String,
    },
    HostInvariant {
        step: ConfigurationStep,
        subject: String,
    },
}

impl ConfigurationRefusal {
    pub(crate) fn step(&self) -> ConfigurationStep {
        match self {
            Self::Invalid { step, .. } | Self::HostInvariant { step, .. } => *step,
        }
    }
}

/// A refusal attributed to one layer and JSON pointer: `layer:<name>:<pointer>`.
fn refuse(layer: Layer, step: ConfigurationStep, pointer: &str) -> ConfigurationRefusal {
    let subject = format!("layer:{}:{pointer}", layer.as_str());
    if host_built(layer) {
        ConfigurationRefusal::HostInvariant { step, subject }
    } else {
        ConfigurationRefusal::Invalid { step, subject }
    }
}

/// The layers the host builds itself: their defects are host invariants.
fn host_built(layer: Layer) -> bool {
    match layer {
        Layer::Defaults | Layer::Flags => true,
        Layer::Global | Layer::Project | Layer::Local => false,
    }
}

/// A defect of the host's own schema registry or encoding, never the caller's.
fn host(step: ConfigurationStep, subject: &str) -> ConfigurationRefusal {
    ConfigurationRefusal::HostInvariant {
        step,
        subject: subject.to_owned(),
    }
}

/// Why an analysis request's configuration was not admitted: resolution, or
/// the X12 admission of its resolved pack selection (item 10).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum AnalysisConfigurationRefusal {
    Configuration(ConfigurationRefusal),
    Policy(PolicySelectionRefusal),
}

/// Item 10 (X12 r4 item 8): resolve, then admit the resolved pack selection
/// immediately, once, with nothing in between. Pure, like both halves.
pub(crate) fn resolve_analysis_configuration(
    input: &ResolverInputV1,
) -> Result<(ResolvedConfigurationV1, AdmittedPack), AnalysisConfigurationRefusal> {
    let resolved = resolve(input).map_err(AnalysisConfigurationRefusal::Configuration)?;
    let selection: Vec<PackSource<'_>> = resolved
        .pack_ids()
        .into_iter()
        .map(PackSource::Named)
        .collect();
    let pack = admit_policy_selection(&selection).map_err(AnalysisConfigurationRefusal::Policy)?;
    Ok((resolved, pack))
}

/// The public termination of an analysis configuration refusal: the X12 rows
/// for the pack selection, and the two configuration rows. No new code.
pub(crate) fn analysis_configuration_termination(
    refusal: &AnalysisConfigurationRefusal,
) -> InstallationTerminationV1 {
    match refusal {
        AnalysisConfigurationRefusal::Configuration(refusal) => configuration_termination(refusal),
        AnalysisConfigurationRefusal::Policy(refusal) => policy_selection_termination(refusal),
    }
}

/// Item 4's refusal rows: request-rejected `CONFIG.INVALID`, or the host
/// invariant as X12 row 4 shapes it. Exhaustive, with no wildcard arm.
pub(crate) fn configuration_termination(
    refusal: &ConfigurationRefusal,
) -> InstallationTerminationV1 {
    match refusal {
        ConfigurationRefusal::Invalid { subject, .. } => InstallationTerminationV1 {
            class: Class::RequestRejected,
            exit: 2,
            error_code: Code::ConfigInvalid,
            fault_cause: Fault::None,
            detail: Some(Detail::ConfigInvalid),
            subject: Some(subject.clone()),
        },
        ConfigurationRefusal::HostInvariant { subject, .. } => InstallationTerminationV1 {
            class: Class::OperationalFailed,
            exit: 4,
            error_code: Code::SystemOutcomeIllegalState,
            fault_cause: Fault::HostInvariant,
            detail: Some(Detail::HostInvariantViolated),
            subject: Some(subject.clone()),
        },
    }
}

/// One admitted layer: its PCS-shaped document and provenance source.
struct AdmittedLayer {
    layer: Layer,
    document: BTreeMap<String, V>,
    source: ProvenanceSourceV1,
}

/// Item 4: the resolution pipeline, steps 1 to 11, in order.
pub(crate) fn resolve(
    input: &ResolverInputV1,
) -> Result<ResolvedConfigurationV1, ConfigurationRefusal> {
    let schemas = crate::embedded_schema_registry()
        .map_err(|_| host(ConfigurationStep::Schema, "registry"))?;
    // Steps 1 to 3 for every layer, in precedence order, before any merge. In
    // CI the local carrier is never parsed.
    let local = if input.mode.interactive {
        input.local.as_ref()
    } else {
        None
    };
    let mut layers = vec![admit_internal(
        &schemas,
        Layer::Defaults,
        defaults_document(&input.defaults),
    )?];
    for (layer, carrier) in [
        (Layer::Global, input.global.as_ref()),
        (Layer::Project, input.project.as_ref()),
        (Layer::Local, local),
    ] {
        if let Some(carrier) = carrier {
            layers.push(admit_carrier(&schemas, layer, carrier)?);
        }
    }
    layers.push(admit_internal(
        &schemas,
        Layer::Flags,
        flags_document(&input.flags),
    )?);
    // Step 4: merge by leaf. A higher layer's value replaces the leaf whole.
    let mut winners: BTreeMap<(String, String), LeafProvenanceV1> = BTreeMap::new();
    for admitted in layers {
        for (section, record) in admitted.document {
            let V::Object(record) = record else {
                continue;
            };
            for (field, value) in record {
                winners.insert(
                    (section.clone(), field),
                    LeafProvenanceV1 {
                        layer: admitted.layer,
                        value,
                        source: admitted.source.clone(),
                    },
                );
            }
        }
    }
    let leaf = |section: &str, field: &str| winners.get(&(section.to_owned(), field.to_owned()));
    // Step 5: logical paths. `.` is the root sentinel only for workspaceRoots
    // and ignorePaths; explicit `workspaceRoots: []` already failed the schema.
    for field in ["entryPoints", "workspaceRoots", "ignorePaths"] {
        if let Some(won) = leaf("discovery", field) {
            for (index, path) in strings(&won.value).into_iter().enumerate() {
                let sentinel = path == "." && field != "entryPoints";
                if !sentinel && !logical_path(path) {
                    return Err(refuse(
                        won.layer,
                        ConfigurationStep::LogicalPath,
                        &format!("/discovery/{field}/{index}"),
                    ));
                }
            }
        }
    }
    // Step 6: registry admission. Packs are X12's, after resolution (item 10).
    match leaf("analysis", "profileId") {
        None => {
            return Err(ConfigurationRefusal::Invalid {
                step: ConfigurationStep::Profile,
                subject: "profile:missing".to_owned(),
            });
        }
        Some(won) => {
            let id = strings(&won.value).into_iter().next().unwrap_or_default();
            if !PROFILE_IDS.contains(&id) {
                return Err(match won.layer {
                    Layer::Global | Layer::Project | Layer::Local => {
                        ConfigurationRefusal::Invalid {
                            step: ConfigurationStep::Profile,
                            subject: format!("profile:{id}"),
                        }
                    }
                    Layer::Defaults | Layer::Flags => {
                        refuse(won.layer, ConfigurationStep::Profile, "/analysis/profileId")
                    }
                });
            }
        }
    }
    if let Some(won) = leaf("analysis", "capabilities") {
        for (index, id) in strings(&won.value).into_iter().enumerate() {
            if !CapabilityId::parse(id).is_some_and(selectable) {
                return Err(refuse(
                    won.layer,
                    ConfigurationStep::Capability,
                    &format!("/analysis/capabilities/{index}"),
                ));
            }
        }
    }
    if let Some(won) = leaf("policy", "waiverIds")
        && !strings(&won.value).is_empty()
    {
        // The waiver registry is empty at M3: any ID refuses.
        return Err(refuse(
            won.layer,
            ConfigurationStep::Waiver,
            "/policy/waiverIds/0",
        ));
    }
    if let Some(won) = leaf("components", "request") {
        let mut seen = Vec::new();
        for (index, item) in items(&won.value).iter().enumerate() {
            let id = member(item, "stableId");
            if seen.contains(&id) {
                return Err(refuse(
                    won.layer,
                    ConfigurationStep::Component,
                    &format!("/components/request/{index}"),
                ));
            }
            seen.push(id);
        }
    }
    // A stable ID may appear once across pins and holds: a second appearance
    // is a duplicate or, at another version, a conflict (compatibility
    // selection model v3, DUPLICATE-PIN-HOLD and PIN-HOLD-CONFLICT). Pins and
    // holds can win from different layers, so the refusal names an external
    // occurrence whenever one is involved (the second, when both are), and is
    // the host's only when both occurrences come from host-built layers.
    let mut exact: Vec<(&str, Layer, String)> = Vec::new();
    for field in ["pins", "holds"] {
        if let Some(won) = leaf("components", field) {
            for (index, item) in items(&won.value).iter().enumerate() {
                let id = member(item, "stableId");
                let pointer = format!("/components/{field}/{index}");
                if let Some((_, first_layer, first_pointer)) =
                    exact.iter().find(|seen| seen.0 == id)
                {
                    let (layer, pointer) = if host_built(won.layer) && !host_built(*first_layer) {
                        (*first_layer, first_pointer.as_str())
                    } else {
                        (won.layer, pointer.as_str())
                    };
                    return Err(refuse(layer, ConfigurationStep::Component, pointer));
                }
                exact.push((id, won.layer, pointer));
            }
        }
    }
    // Step 7: completeness of the compiled defaults themselves, a host
    // invariant (AQ:132-137). A higher layer's value cannot repair a missing
    // compiled capability list or budget.
    for (field, compiled) in [
        ("capabilities", input.defaults.capabilities.is_some()),
        ("budget", input.defaults.budget_limit.is_some()),
    ] {
        if !compiled || leaf("analysis", field).is_none() {
            return Err(host(
                ConfigurationStep::DefaultsComplete,
                &format!("layer:defaults:/analysis/{field}"),
            ));
        }
    }
    // Step 8: partition by the classification table, its only source. Every
    // semantic section is present, `{}` when empty (AQ:128-133).
    let mut semantic = BTreeMap::new();
    let mut operational = BTreeMap::new();
    for (section, field, class, _) in FIELDS {
        let record = match class {
            FieldClass::HostAnalysisSemantic => &mut semantic,
            FieldClass::HostOperabilityNonsemantic => &mut operational,
        };
        let V::Object(fields) = record
            .entry(section.to_owned())
            .or_insert_with(|| V::Object(BTreeMap::new()))
        else {
            continue;
        };
        if let Some(won) = leaf(section, field) {
            fields.insert(field.to_owned(), won.value.clone());
        }
    }
    // Step 9: canonical sets, except the declared allowedScopes priority.
    let semantic = normalize(&V::Object(semantic), "")?;
    // Step 10: the resolved shape.
    let raw = semantic_shape(&schemas, &semantic)?;
    // Step 11: the raw digest, not an H-identity (item 6).
    let resolved_config_digest = digest_hex(&raw_sha256(&raw));
    let provenance = winners
        .into_iter()
        .map(|((section, field), won)| (format!("{section}.{field}"), won))
        .collect();
    Ok(ResolvedConfigurationV1 {
        semantic,
        operational: V::Object(operational),
        provenance,
        resolved_config_digest,
    })
}

/// Step 10: the canonical bytes of a semantic record identity-v3
/// `semantic-configuration` admits. Any defect is the host's (AQ section 1).
fn semantic_shape(
    schemas: &RegisteredSchemas,
    semantic: &V,
) -> Result<Vec<u8>, ConfigurationRefusal> {
    let invalid = || {
        host(
            ConfigurationStep::Semantic,
            "resolved:semantic-configuration",
        )
    };
    let raw = canonical_bytes(semantic).map_err(|_| invalid())?;
    schemas
        .schema(IDENTITY_ID, SEMANTIC_SELECTOR)
        .map_err(|_| host(ConfigurationStep::Semantic, "registry"))?
        .admit_json(&raw, SCHEMA_BUDGET)
        .map_err(|_| invalid())?;
    Ok(raw)
}

/// Item 8, capabilities: a matrix member with at least one mode whose cell is
/// not `NOT-SELECTED`. The per-(capability, mode) judgment belongs to the
/// analysis spec, where the mode is known (NE:1005-1013, NE:3577).
fn selectable(capability: CapabilityId) -> bool {
    LanguageMode::ALL
        .into_iter()
        .any(|mode| !NOT_SELECTED_CELLS.contains(&(capability, mode)))
}

/// PCM:23-27: a canonical project-relative path: not absolute, no backslash
/// or NUL, and no empty, `.` or `..` segment.
fn logical_path(path: &str) -> bool {
    !path.starts_with('/')
        && !path.contains('\\')
        && !path.contains('\0')
        && path.split('/').all(|part| !matches!(part, "" | "." | ".."))
}

/// The string items of an admitted array (or the one admitted string).
fn strings(value: &V) -> Vec<&str> {
    match value {
        V::String(text) => vec![text.as_str()],
        V::Array(values) => values
            .iter()
            .filter_map(|value| {
                if let V::String(text) = value {
                    Some(text.as_str())
                } else {
                    None
                }
            })
            .collect(),
        V::Null | V::Bool(_) | V::Integer(_) | V::Object(_) => Vec::new(),
    }
}

fn items(value: &V) -> &[V] {
    if let V::Array(values) = value {
        values
    } else {
        &[]
    }
}

/// An admitted object's string member, or "" (the schema already required it).
fn member<'a>(value: &'a V, name: &str) -> &'a str {
    if let V::Object(fields) = value
        && let Some(V::String(text)) = fields.get(name)
    {
        text
    } else {
        ""
    }
}

/// Step 9 (PCM:42-48): sort every array by its items' canonical bytes, after
/// normalizing the items, except `allowedScopes`, whose order is a priority.
fn normalize(value: &V, key: &str) -> Result<V, ConfigurationRefusal> {
    Ok(match value {
        V::Object(fields) => V::Object(
            fields
                .iter()
                .map(|(name, value)| Ok((name.clone(), normalize(value, name)?)))
                .collect::<Result<_, ConfigurationRefusal>>()?,
        ),
        V::Array(values) if key == "allowedScopes" => V::Array(values.clone()),
        V::Array(values) => {
            let mut keyed = values
                .iter()
                .map(|value| {
                    let value = normalize(value, "")?;
                    let raw = canonical_bytes(&value).map_err(|_| {
                        host(
                            ConfigurationStep::Semantic,
                            "resolved:semantic-configuration",
                        )
                    })?;
                    Ok((raw, value))
                })
                .collect::<Result<Vec<_>, ConfigurationRefusal>>()?;
            keyed.sort_by(|a, b| a.0.cmp(&b.0));
            V::Array(keyed.into_iter().map(|(_, value)| value).collect())
        }
        other => other.clone(),
    })
}

/// Steps 1 to 3 for a captured carrier: lexical admission, the schema (PCS,
/// or the exact preview carrier for a `schemaVersion: 1` file, projected in
/// memory onto version 2; item 11), then the layer's allowlist.
fn admit_carrier(
    schemas: &RegisteredSchemas,
    layer: Layer,
    carrier: &CapturedCarrierV1,
) -> Result<AdmittedLayer, ConfigurationRefusal> {
    let value =
        parse_json(&carrier.bytes).map_err(|_| refuse(layer, ConfigurationStep::Lexical, ""))?;
    let schema_one = matches!(
        &value,
        V::Object(fields) if matches!(fields.get("schemaVersion"), Some(V::Integer(n)) if n.get() == 1)
    );
    let (document, source_schema_version) = if schema_one {
        let selector = format!("/$defs/{}", layer.as_str());
        admit_shape(
            schemas,
            PREVIEW_ID,
            &selector,
            &carrier.bytes,
            layer,
            ConfigurationStep::Schema,
        )?;
        // Every schema-one field maps 1:1 to the same version-2 path (HFC:163-168);
        // the closed preview carrier refuses any other field.
        let V::Object(mut fields) = value else {
            return Err(refuse(layer, ConfigurationStep::SchemaOne, ""));
        };
        fields.insert("schemaVersion".to_owned(), integer(2));
        let projected = V::Object(fields);
        let raw = canonical_bytes(&projected)
            .map_err(|_| refuse(layer, ConfigurationStep::SchemaOne, ""))?;
        admit_shape(
            schemas,
            PCS_ID,
            "",
            &raw,
            layer,
            ConfigurationStep::SchemaOne,
        )?;
        (projected, 1)
    } else {
        admit_shape(
            schemas,
            PCS_ID,
            "",
            &carrier.bytes,
            layer,
            ConfigurationStep::Schema,
        )?;
        (value, 2)
    };
    let source = ProvenanceSourceV1::Carrier {
        path: carrier.path.clone(),
        sha256: digest_hex(&raw_sha256(&carrier.bytes)),
        source_schema_version,
    };
    admit_layer(layer, document, source)
}

/// Steps 1 to 3 for a host-built layer: the same lexical, schema and
/// allowlist steps over its encoded document (B1-a plan r2, RF-02). Every
/// defect is the host invariant, by the layer's kind.
fn admit_internal(
    schemas: &RegisteredSchemas,
    layer: Layer,
    document: V,
) -> Result<AdmittedLayer, ConfigurationRefusal> {
    let raw =
        canonical_bytes(&document).map_err(|_| refuse(layer, ConfigurationStep::Lexical, ""))?;
    let document = parse_json(&raw).map_err(|_| refuse(layer, ConfigurationStep::Lexical, ""))?;
    admit_shape(schemas, PCS_ID, "", &raw, layer, ConfigurationStep::Schema)?;
    let source = match layer {
        Layer::Flags => ProvenanceSourceV1::Flags,
        Layer::Defaults | Layer::Global | Layer::Project | Layer::Local => {
            ProvenanceSourceV1::Defaulted
        }
    };
    admit_layer(layer, document, source)
}

/// One schema admission of exact bytes. A registry selection defect is the
/// host's; a document the schema refuses is the layer's.
fn admit_shape(
    schemas: &RegisteredSchemas,
    id: &str,
    selector: &str,
    raw: &[u8],
    layer: Layer,
    step: ConfigurationStep,
) -> Result<(), ConfigurationRefusal> {
    let handle = schemas
        .schema(id, selector)
        .map_err(|_| host(step, "registry"))?;
    handle
        .admit_json(raw, SCHEMA_BUDGET)
        .map(|_| ())
        .map_err(|_| refuse(layer, step, ""))
}

/// Step 3: every present leaf must be one the layer admits (item 2), by the
/// reviewed mapping. An unclassified leaf refuses: the default for a future
/// field without a row is refusal (item 7, O-2).
fn admit_layer(
    layer: Layer,
    document: V,
    source: ProvenanceSourceV1,
) -> Result<AdmittedLayer, ConfigurationRefusal> {
    let V::Object(mut document) = document else {
        return Err(refuse(layer, ConfigurationStep::Schema, ""));
    };
    document.remove("schemaVersion");
    for (section, record) in &document {
        let V::Object(fields) = record else {
            return Err(refuse(
                layer,
                ConfigurationStep::Schema,
                &format!("/{section}"),
            ));
        };
        for field in fields.keys() {
            let row = FIELDS
                .iter()
                .find(|row| row.0 == section.as_str() && row.1 == field.as_str());
            match row {
                None => {
                    return Err(host(
                        ConfigurationStep::Allowlist,
                        &format!("class:{section}.{field}"),
                    ));
                }
                Some(row) if !row.3.contains(&layer) => {
                    return Err(refuse(
                        layer,
                        ConfigurationStep::Allowlist,
                        &format!("/{section}/{field}"),
                    ));
                }
                Some(_) => {}
            }
        }
    }
    Ok(AdmittedLayer {
        layer,
        document,
        source,
    })
}

/// Every u64 is within the canonical profile's integer range; were it not,
/// the null would fail the schema as the layer's defect, never panic.
fn integer(value: u64) -> V {
    JsonInteger::new(i128::from(value)).map_or(V::Null, V::Integer)
}

fn text(value: &str) -> V {
    V::String(value.to_owned())
}

fn texts(values: &[String]) -> V {
    V::Array(values.iter().map(|value| text(value)).collect())
}

fn object<const N: usize>(fields: [(&str, Option<V>); N]) -> Option<V> {
    let fields: BTreeMap<String, V> = fields
        .into_iter()
        .filter_map(|(name, value)| value.map(|value| (name.to_owned(), value)))
        .collect();
    (!fields.is_empty()).then_some(V::Object(fields))
}

fn version(item: &ComponentVersionV1) -> V {
    V::Object(BTreeMap::from([
        ("stableId".to_owned(), text(&item.stable_id)),
        ("version".to_owned(), text(&item.version)),
    ]))
}

fn request(item: &ComponentRequestV1) -> V {
    match item {
        ComponentRequestV1::Version(item) => version(item),
        ComponentRequestV1::Constraint {
            stable_id,
            constraint,
        } => V::Object(BTreeMap::from([
            ("stableId".to_owned(), text(stable_id)),
            ("versionConstraint".to_owned(), text(constraint)),
        ])),
        ComponentRequestV1::Range {
            stable_id,
            min,
            max,
            include_min,
            include_max,
        } => V::Object(BTreeMap::from([
            ("stableId".to_owned(), text(stable_id)),
            (
                "versionConstraint".to_owned(),
                V::Object(BTreeMap::from([
                    ("min".to_owned(), text(min)),
                    ("max".to_owned(), text(max)),
                    ("includeMin".to_owned(), V::Bool(*include_min)),
                    ("includeMax".to_owned(), V::Bool(*include_max)),
                ])),
            ),
        ])),
    }
}

/// Layer 1's document. A section appears only when it selects a field.
fn defaults_document(defaults: &CompiledDefaultsV1) -> V {
    let budget = defaults.budget_limit.map(|limit| {
        V::Object(BTreeMap::from([
            ("unit".to_owned(), text("work-units")),
            ("limit".to_owned(), integer(limit)),
        ]))
    });
    let sections = [
        (
            "analysis",
            object([
                ("profileId", defaults.profile_id.as_deref().map(text)),
                ("capabilities", defaults.capabilities.as_deref().map(texts)),
                ("budget", budget),
            ]),
        ),
        (
            "components",
            object([
                (
                    "request",
                    defaults
                        .request
                        .as_ref()
                        .map(|items| V::Array(items.iter().map(request).collect())),
                ),
                (
                    "pins",
                    defaults
                        .pins
                        .as_ref()
                        .map(|items| V::Array(items.iter().map(version).collect())),
                ),
                (
                    "holds",
                    defaults
                        .holds
                        .as_ref()
                        .map(|items| V::Array(items.iter().map(version).collect())),
                ),
                (
                    "allowedScopes",
                    defaults.allowed_scopes.as_deref().map(texts),
                ),
            ]),
        ),
        (
            "policy",
            object([("packIds", defaults.pack_ids.as_deref().map(texts))]),
        ),
    ];
    document(sections)
}

/// Layer 6's document: `--workspace-root` maps to `discovery.workspaceRoots`.
fn flags_document(flags: &FlagLayerV1) -> V {
    document([(
        "discovery",
        object([(
            "workspaceRoots",
            flags.workspace_roots.as_deref().map(texts),
        )]),
    )])
}

fn document<const N: usize>(sections: [(&str, Option<V>); N]) -> V {
    let mut fields: BTreeMap<String, V> = sections
        .into_iter()
        .filter_map(|(name, value)| value.map(|value| (name.to_owned(), value)))
        .collect();
    fields.insert("schemaVersion".to_owned(), integer(2));
    V::Object(fields)
}

/// Item 23: of the seven shared flags, only `--workspace-root` is
/// configuration (layer 6, `discovery.workspaceRoots`). The others select or
/// authorize and never reach the resolver or the digest.
pub(crate) fn configuration_leaf(flag: SharedFlag) -> Option<(&'static str, &'static str)> {
    match flag {
        SharedFlag::WorkspaceRoot => Some(("discovery", "workspaceRoots")),
        SharedFlag::AllowBackupCustody
        | SharedFlag::Project
        | SharedFlag::TrustGroup
        | SharedFlag::TrustProjectOwner
        | SharedFlag::Ephemeral
        | SharedFlag::YesPolicy => None,
    }
}

#[cfg(test)]
mod tests {
    include!("configuration_tests.rs");
    include!("configuration_resolver_tests.rs");
}
