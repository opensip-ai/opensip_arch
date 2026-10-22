use super::{JsonValue as V, metadata_bytes, retained_root_semantics};
use crate::trust_time::timestamp_seconds;
use std::collections::{BTreeMap, BTreeSet};
type Object = BTreeMap<String, V>;
const FIELDS: [&str; 12] = [
    "rootSchema",
    "rootVersion",
    "previousRootVersion",
    "issuedAt",
    "expiresAt",
    "keys",
    "rootKeys",
    "rootThreshold",
    "roles",
    "recoveryAuthority",
    "kernelAttestationKeys",
    "indexOrigin",
];
const ROLES: [&str; 6] = [
    "TR-CORE",
    "TR-INDEX",
    "TR-COMPONENT",
    "TR-BUNDLE",
    "TR-REPAIR",
    "TR-PROFILE",
];
#[derive(Debug, PartialEq, Eq)]
enum Error {
    Shape,
    SchemaConstant,
    Unsupported,
    Metadata,
    PreviousVersion,
    Timestamp,
    Expiry,
    KeyId,
    RootKeys,
    Recovery,
    RoleThreshold,
    RepairUnderSchema1,
    UnknownKey,
    KeyReuse,
    RetainedPolicy,
}
// Only this child can construct or mutate an admitted root payload.
mod admitted_roots {
    include!("admitted_roots.rs");
}
use admitted_roots::{ValidatedRootPayload, admit};
fn object(v: &V) -> Option<&Object> {
    if let V::Object(o) = v { Some(o) } else { None }
}
fn string(v: &V) -> Option<&str> {
    if let V::String(s) = v { Some(s) } else { None }
}
fn array(v: &V) -> Option<&[V]> {
    if let V::Array(a) = v { Some(a) } else { None }
}
fn integer(v: &V) -> Option<i64> {
    if let V::Integer(i) = v {
        i64::try_from(i.get()).ok()
    } else {
        None
    }
}
fn closed(o: &Object, required: &[&str], optional: &[&str]) -> bool {
    required.iter().all(|k| o.contains_key(*k))
        && o.keys()
            .all(|k| required.contains(&k.as_str()) || optional.contains(&k.as_str()))
}
fn int_range(v: &V, lo: i64, hi: i64) -> bool {
    integer(v).is_some_and(|i| (lo..=hi).contains(&i))
}
fn str_range(v: &V, lo: usize, hi: usize) -> bool {
    string(v).is_some_and(|s| (lo..=hi).contains(&s.chars().count()))
}
fn hex(v: &V) -> bool {
    string(v).is_some_and(|s| {
        s.len() == 64
            && s.bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    })
}
fn list(v: &V, lo: usize, hi: usize, item: impl Fn(&V) -> bool) -> bool {
    array(v).is_some_and(|a| {
        (lo..=hi).contains(&a.len())
            && a.iter()
                .enumerate()
                .all(|(i, v)| item(v) && !a[..i].contains(v))
    })
}
fn namespace(v: &V) -> bool {
    string(v).is_some_and(|s| {
        !s.is_empty()
            && s.len() <= 4_194_304
            && lower_or_digit(s.as_bytes()[0])
            && s.bytes()
                .all(|b| lower_or_digit(b) || b == b'.' || b == b'-')
    })
}
fn lower_or_digit(b: u8) -> bool {
    b.is_ascii_lowercase() || b.is_ascii_digit()
}
fn timestamp_shape(v: &V) -> bool {
    string(v).is_some_and(|s| {
        let b = s.as_bytes();
        b.len() == 20
            && b.iter().enumerate().all(|(i, &c)| match i {
                4 | 7 => c == b'-',
                10 => c == b'T',
                13 | 16 => c == b':',
                19 => c == b'Z',
                _ => c.is_ascii_digit(),
            })
    })
}
fn url(v: &V) -> bool {
    string(v).is_some_and(|s| {
        if s.len() > 512 {
            return false;
        }
        let Some(rest) = s.strip_prefix("https://") else {
            return false;
        };
        let (host, path) = rest
            .split_once('/')
            .map_or((rest, None), |(h, p)| (h, Some(p)));
        !host.is_empty()
            && host
                .bytes()
                .all(|b| lower_or_digit(b) || b == b'.' || b == b'-')
            && path.is_none_or(|p| {
                p.bytes()
                    .all(|b| b.is_ascii_alphanumeric() || b"._~/-".contains(&b))
            })
    })
}
fn role_shape(v: &V) -> bool {
    let Some(o) = object(v) else { return false };
    closed(o, &["keys", "threshold", "namespaces"], &["standing"])
        && list(&o["keys"], 0, 8, hex)
        && int_range(&o["threshold"], 0, 8)
        && list(&o["namespaces"], 0, 16, namespace)
        && o.get("standing")
            .is_none_or(|v| matches!(string(v), Some("active" | "typed-absence-DR-110")))
}
fn shape(root: &Object, schema: u8) -> bool {
    int_range(&root["rootVersion"], 1, i64::MAX)
        && (root["previousRootVersion"] == V::Null
            || int_range(&root["previousRootVersion"], 1, i64::MAX))
        && timestamp_shape(&root["issuedAt"])
        && timestamp_shape(&root["expiresAt"])
        && list(&root["keys"], 1, 64, |v| {
            object(v).is_some_and(|o| {
                closed(o, &["keyId", "publicKey", "label"], &[])
                    && hex(&o["keyId"])
                    && hex(&o["publicKey"])
                    && str_range(&o["label"], 1, 64)
            })
        })
        && list(&root["rootKeys"], 3, 8, hex)
        && int_range(&root["rootThreshold"], 2, 8)
        && object(&root["recoveryAuthority"]).is_some_and(|o| {
            closed(o, &["keys", "threshold"], &[])
                && list(&o["keys"], 5, 16, hex)
                && int_range(&o["threshold"], 3, 16)
        })
        && object(&root["indexOrigin"]).is_some_and(|o| {
            closed(o, &["url", "spkiSha256"], &[]) && url(&o["url"]) && hex(&o["spkiSha256"])
        })
        && object(&root["roles"]).is_some_and(|o| {
            closed(o, &ROLES[..if schema == 1 { 5 } else { 6 }], &[]) && o.values().all(role_shape)
        })
        && list(
            &root["kernelAttestationKeys"],
            0,
            if schema == 1 { 0 } else { 8 },
            hex,
        )
}
fn keys(v: &V) -> Result<Vec<&str>, Error> {
    array(v)
        .ok_or(Error::Shape)?
        .iter()
        .map(|v| string(v).ok_or(Error::Shape))
        .collect()
}
fn number(o: &Object, name: &str) -> Result<i64, Error> {
    o.get(name).and_then(integer).ok_or(Error::Shape)
}
fn active_or_absent(o: &Object) -> Result<bool, Error> {
    let ks = keys(&o["keys"])?;
    let t = number(o, "threshold")?;
    let namespaces = array(&o["namespaces"]).ok_or(Error::Shape)?;
    let standing = o.get("standing").and_then(string);
    Ok(if ks.is_empty() {
        t == 0 && namespaces.is_empty() && standing == Some("typed-absence-DR-110")
    } else {
        t >= 2 && ks.len() as i64 > t && !namespaces.is_empty() && standing == Some("active")
    })
}
#[cfg(test)]
mod tests {
    include!("root_payload_tests.rs");
}
// A quorum report binds cryptographic facts to a validated root payload and
// message. It is NOT an admitted envelope/root chain or current permission.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum QuorumRole {
    Root,
    Recovery,
    Core,
    Index,
    Component,
    Bundle,
    Repair,
    Profile,
}
#[derive(Debug, PartialEq, Eq)]
enum QuorumState {
    NoValidSignatures,
    BelowThreshold,
    Met,
}
#[derive(Debug, PartialEq, Eq)]
enum QuorumError {
    Limit,
    Namespace,
    RoleUnavailable,
    InternalShape,
}
struct SignatureRecord {
    key_id: [u8; 32],
    signature: [u8; 64],
}
mod verified_envelopes {
    include!("verified_envelopes.rs");
}
use verified_envelopes::{
    EnvelopeEvidence, QuorumReport, filter_envelope_revoked, filter_revoked, verify_envelope,
};
#[cfg(test)]
use verified_envelopes::{raw_quorum_state, verify_quorum};
fn decode_hex32(s: &str) -> Result<[u8; 32], QuorumError> {
    if s.len() != 64
        || !s
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(QuorumError::InternalShape);
    }
    let mut out = [0; 32];
    for (i, b) in out.iter_mut().enumerate() {
        *b = u8::from_str_radix(&s[i * 2..i * 2 + 2], 16).map_err(|_| QuorumError::InternalShape)?
    }
    Ok(out)
}
#[cfg(test)]
mod quorum_tests {
    include!("quorum_tests.rs");
}
// Carrier parity with reviewed233: nine kinds and explicit payload1/2 domains. This is an
// inert cryptographic observation over a validated payload, not root-chain
// authentication, payload schema admission or current operational authority.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum EnvelopeKind {
    Manifest,
    Catalog,
    Root,
    Revocation,
    Inventory,
    Payload,
    RecoveryEpoch,
    ProfileSet,
    RootRecoveryAuthorization,
}
impl EnvelopeKind {
    fn route(self) -> (&'static str, &'static str, &'static str, QuorumRole) {
        match self {
            Self::Manifest => (
                "manifest",
                "opensip.metadata.manifest.1",
                "TR-COMPONENT",
                QuorumRole::Component,
            ),
            Self::Catalog => (
                "catalog",
                "opensip.metadata.catalog.1",
                "TR-INDEX",
                QuorumRole::Index,
            ),
            Self::Root => ("root", "opensip.metadata.root.1", "ROOT", QuorumRole::Root),
            Self::Revocation => (
                "revocation",
                "opensip.metadata.revocation.1",
                "ROOT",
                QuorumRole::Root,
            ),
            Self::Inventory => (
                "inventory",
                "opensip.metadata.inventory.1",
                "TR-CORE",
                QuorumRole::Core,
            ),
            Self::RecoveryEpoch => (
                "trust-recovery-epoch",
                "opensip.metadata.recovery-epoch.1",
                "RECOVERY",
                QuorumRole::Recovery,
            ),
            Self::ProfileSet => (
                "platform-profile-set",
                "opensip.metadata.platform-profile-set.1",
                "TR-PROFILE",
                QuorumRole::Profile,
            ),
            Self::RootRecoveryAuthorization => (
                "root-recovery-authorization",
                "opensip.metadata.root-recovery.1",
                "RECOVERY",
                QuorumRole::Recovery,
            ),
            Self::Payload => (
                "payload",
                "opensip.metadata.payload.1",
                "TR-BUNDLE",
                QuorumRole::Bundle,
            ),
        }
    }
    fn from_name(s: &str) -> Option<Self> {
        match s {
            "manifest" => Some(Self::Manifest),
            "catalog" => Some(Self::Catalog),
            "root" => Some(Self::Root),
            "revocation" => Some(Self::Revocation),
            "inventory" => Some(Self::Inventory),
            "payload" => Some(Self::Payload),
            "trust-recovery-epoch" => Some(Self::RecoveryEpoch),
            "platform-profile-set" => Some(Self::ProfileSet),
            "root-recovery-authorization" => Some(Self::RootRecoveryAuthorization),
            _ => None,
        }
    }
}
/// Private build/caller capability declaration, not signed input or authority.
#[derive(Clone, Copy)]
struct EnvelopeReader {
    root_schemas: [bool; 2],
    kinds: [bool; 9],
    payload_schemas: [bool; 2],
}
const CURRENT_ENVELOPE_READER: EnvelopeReader = EnvelopeReader {
    root_schemas: [true, true],
    kinds: [true; 9],
    // Capability is a private caller choice. Existing callers do not opt into payload2.
    payload_schemas: [true, false],
};
impl EnvelopeReader {
    fn supports(self, kind: EnvelopeKind) -> bool {
        let index = match kind {
            EnvelopeKind::Manifest => 0,
            EnvelopeKind::Catalog => 1,
            EnvelopeKind::Root => 2,
            EnvelopeKind::Revocation => 3,
            EnvelopeKind::Inventory => 4,
            EnvelopeKind::Payload => 5,
            EnvelopeKind::RecoveryEpoch => 6,
            EnvelopeKind::ProfileSet => 7,
            EnvelopeKind::RootRecoveryAuthorization => 8,
        };
        self.kinds[index]
    }
    fn supports_payload(self, schema: i64) -> bool {
        match schema {
            1 => self.payload_schemas[0],
            2 => self.payload_schemas[1],
            _ => false,
        }
    }
    fn supports_root(self, schema: i64) -> bool {
        match schema {
            1 => self.root_schemas[0],
            2 => self.root_schemas[1],
            _ => false,
        }
    }
}
#[derive(Debug, PartialEq, Eq)]
enum EnvelopeError {
    ReaderDeclaration,
    UnsupportedKind,
    UnsupportedRootSchema,
    UnsupportedPayloadSchema,
    PayloadSchema,
    Limit,
    Unsigned,
    Routing,
    StoredDigest,
    PayloadMetadata,
    PreimageDigest,
    PublisherNamespace,
    NoValidSignature,
    RoleUnavailable,
    RootSchema,
    Quorum,
}
fn signature64(value: &V) -> Option<[u8; 64]> {
    let s = string(value)?;
    if s.len() != 128
        || !s
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return None;
    }
    let mut out = [0; 64];
    for (i, b) in out.iter_mut().enumerate() {
        *b = u8::from_str_radix(&s[i * 2..i * 2 + 2], 16).ok()?;
    }
    Some(out)
}
#[cfg(test)]
mod envelope_tests {
    include!("envelope_tests.rs");
}
// Conditional recovery-authorization evidence. Held-root selection, complete
// current revocation population, ancestry/floors and S4 remain host owners.
// This cannot stage, mutate roles, publish, or grant command authority.
mod verified_root_recovery {
    include!("verified_root_recovery.rs");
}

mod admitted_payload_paths {
    include!("admitted_payload_paths.rs");
}

/// Conditional retained-byte accounting and listed metadata pairing. No
/// signature verification, filesystem custody, or current-authority claim.
/// Full structural dependency mode only. No caller skip list or implied
/// admission of old T for scoped S4.5/safe ABORT operations.
/// Conditional creation, declaration and host-admission input joins. These
/// own recorded values, not native observations, live census or role effects.
mod trust_input_bindings {
    include!("trust_input_bindings.rs");
}

/// Literal event replay from a supplied logical base. Accepted role events
/// remain pending authenticated effects; neither base selection nor native
/// durability is established by the returned structural evidence.
mod publication_events {
    include!("publication_events.rs");
}

/// The P0 trust publication of a new installation, built in memory and
/// checked by the creation, event and capsule verifiers. Not creator authority.
// Law 467's manifest reaches it from custody; its refusal payloads stay
// private to this module and are carried only for diagnostics.
#[allow(private_interfaces)]
mod initial_publication {
    include!("initial_publication.rs");
}
pub(crate) use initial_publication::{
    Error as InitialPublicationError, Inputs as InitialPublicationInputs, TrustFile,
    build as build_initial_publication, verify_files as verify_initial_publication_files,
};

/// Current structural operation walk plus prepared outcome bindings. These
/// validate claimed decisions; no requested effect or publication is proven.
mod prepared_trust_outcomes {
    include!("prepared_trust_outcomes.rs");
}

mod retained_trust_graph {
    include!("retained_trust_graph.rs");
}

mod retained_metadata_index {
    include!("retained_metadata_index.rs");
}

/// Retained recovery inventory and actual authorization/replacement/BUNDLE
/// signatures. Artifact observations remain asserted facts, not captures.
mod ordinary_bundle {
    include!("../trust_ordinary_bundle.rs");
}
mod ordinary_roots {
    include!("../trust_ordinary_roots.rs");
}
pub(crate) use captured_capsule_clock::CapturedImage;
pub(crate) use ordinary_targets::{CapturedOrdinaryInput, OrdinaryClockInput};
#[cfg(target_os = "macos")]
pub(crate) use ordinary_targets::ConfirmedCurrent;
#[cfg(all(test, target_os = "macos"))]
pub(crate) use ordinary_targets::{RetainedCurrentTrust, publish as publish_trust};

// Law X4 r7 (unit X4a): the live guards' trust side.
#[cfg(all(test, target_os = "macos"))]
pub(crate) use ordinary_targets::ObservationPoint;
#[cfg(target_os = "macos")]
pub(crate) use ordinary_targets::{
    AdmittedCurrentTrust, BootstrapSource, LiveObservation, ObservationHook, Observed,
    RetainedTrustHandles, TrustInvocation, TrustRefusal, TrustRow, fenced_operation_read,
};
#[cfg(all(any(test, feature = "crash-matrix", feature = "scenario-fixtures"), target_os = "macos"))]
pub(crate) use ordinary_targets::publish_store_fenced;
mod ordinary_targets {
    use super::super::role_machine::State;
    include!("ordinary_targets.rs");
}
mod role_availability {
    include!("../trust_role_availability.rs");
}
mod ordinary_policy {
    include!("../trust_ordinary_policy.rs");
}
mod ordinary_metadata {
    include!("../trust_ordinary_metadata.rs");
}
mod ordinary_quorums {
    include!("../trust_ordinary_quorums.rs");
}
mod ordinary_inventory {
    include!("../trust_ordinary_inventory.rs");
}
mod retained_recovery_payload {
    include!("retained_recovery_payload.rs");
}

/// One finite incoming-key union; every signature group, including the
/// incoming list's own group, must survive. No current authority/effects.
/// Catalog structural semantics over the actual incoming signed recovery.
/// Required root/list versions remain minimum activation requirements, not
/// equality assertions against this candidate's currently supplied context.
/// Complete component structure and exact authenticated catalog bindings.
/// External context is still supplied, not an admitted host registry view.
/// Packaged raw policy is inventory evidence, never an adopted private
/// policy, effective grant or operational consent.
mod effective_permission_policy {
    include!("../trust_policy.rs");
}
mod packaged_recovery_policies {
    include!("packaged_recovery_policies.rs");
}

mod recovery_metadata {
    include!("recovery_metadata.rs");
}

mod recovery_catalog {
    include!("recovery_catalog.rs");
}

mod incoming_recovery_quorums {
    include!("incoming_recovery_quorums.rs");
}

// Owned exact metadata documents and conditional payload2 binding. Paths and
// complete retained member inventory still require the native index owner.
mod verified_recovery_bundle {
    include!("verified_recovery_bundle.rs");
}

// Conditional chain evidence: the anchor must later come from authenticated
// install custody. This private function never persists or grants authority.
struct WireRootLink<'a> {
    stored: &'a [u8],
    envelope: &'a V,
}
struct ChainContext<'a> {
    accepted_version: i64,
    evaluation_time: &'a str,
    wall: &'a str,
    revoked: &'a BTreeSet<[u8; 32]>,
    readers: [bool; 2],
}
// Authentication has no evaluation instant or wall-clock premise.
struct ChainAuthenticationContext<'a> {
    accepted_version: i64,
    revoked: &'a BTreeSet<[u8; 32]>,
    readers: [bool; 2],
}
struct ChainBudget {
    max_links: usize,
    max_stored_bytes: usize,
}
#[derive(Debug, PartialEq, Eq)]
enum ChainError {
    AnchorUnsupported,
    Limit,
    Time,
    StateInconsistent,
    ExpiredNoChain,
    Unsupported(usize),
    Payload(usize),
    Envelope(usize),
    Gap(usize),
    Backdated(usize),
    OldThreshold(usize),
    NewThreshold(usize),
    FinalExpired,
    FinalFuture,
}
mod verified_root_chains {
    include!("verified_root_chains.rs");
}
#[cfg(test)]
use verified_root_chains::verify_root_chain;
mod admitted_recovery_proposals {
    include!("admitted_recovery_proposals.rs");
}
#[cfg(test)]
use admitted_recovery_proposals::{issue_recovery_challenge, propose_recovery};
mod admitted_platform_decisions {
    include!("admitted_platform_decisions.rs");
}
#[cfg(test)]
use admitted_platform_decisions::evaluate_platform;
#[cfg(test)]
use admitted_recovery_proposals::draw_fixture as issue_challenge_with_draw;
fn chain_root_number(root: &ValidatedRootPayload, key: &str) -> Result<i64, ChainError> {
    object(root.value())
        .and_then(|o| o.get(key))
        .and_then(integer)
        .ok_or(ChainError::StateInconsistent)
}
fn chain_root_text<'a>(root: &'a ValidatedRootPayload, key: &str) -> Result<&'a str, ChainError> {
    object(root.value())
        .and_then(|o| o.get(key))
        .and_then(string)
        .ok_or(ChainError::StateInconsistent)
}
#[cfg(test)]
mod chain_tests {
    include!("chain_tests.rs");
}
const RECOVERY_COUNTERS: [&str; 3] = ["rootVersion", "revocationVersion", "indexSnapshotVersion"];
const RECOVERY_BOUND: [&str; 6] = [
    "evalHighWater",
    "lastAccepted",
    "rootVersion",
    "revocationVersion",
    "indexSnapshotVersion",
    "recoveryEpochSerial",
];
#[derive(Debug, PartialEq, Eq)]
enum RecoveryError {
    Input(&'static str),
    Refused(&'static str),
    Envelope,
    Context,
    Limit,
    Entropy,
}
struct RecoveryEpoch {
    serial: i64,
    issued: i64,
    issued_text: String,
    nonce: [u8; 32],
    record_digest: [u8; 32],
    counters: [i64; 3],
}
struct RecoveryPending {
    nonce: [u8; 32],
    record_digest: [u8; 32],
    boot: String,
    created: i64,
    expires: i64,
}
struct RecoveryObservation {
    wall: i64,
    mono: i64,
    boot: String,
}
fn recovery_hex(o: &Object, key: &str) -> Option<[u8; 32]> {
    o.get(key)
        .and_then(string)
        .and_then(|s| decode_hex32(s).ok())
}
fn admit_recovery_epoch(value: &V) -> Result<RecoveryEpoch, RecoveryError> {
    let fail = |s| RecoveryError::Refused(s);
    let o = object(value).ok_or(fail("SHAPE"))?;
    if !closed(
        o,
        &[
            "recoverySchema",
            "kind",
            "epochSerial",
            "issuedAt",
            "challenge",
            "counters",
            "installBinding",
        ],
        &[],
    ) {
        return Err(fail("SHAPE"));
    }
    if o.get("recoverySchema").and_then(integer) != Some(1) {
        return Err(fail("SHAPE:recoverySchema"));
    }
    if o.get("kind").and_then(string) != Some("trust-recovery-epoch") {
        return Err(fail("SHAPE:kind"));
    }
    let serial = o
        .get("epochSerial")
        .and_then(integer)
        .filter(|n| *n >= 1)
        .ok_or(fail("SHAPE:epochSerial"))?;
    let issued_text = o
        .get("issuedAt")
        .and_then(string)
        .ok_or(fail("SHAPE:issuedAt"))?;
    let issued = timestamp_seconds(issued_text).map_err(|_| fail("SHAPE:issuedAt"))?;
    let challenge = o
        .get("challenge")
        .and_then(object)
        .ok_or(fail("SHAPE:challenge"))?;
    if !closed(challenge, &["nonce", "recordDigest"], &[]) {
        return Err(fail("SHAPE:challenge"));
    }
    let nonce = recovery_hex(challenge, "nonce").ok_or(fail("SHAPE:challenge"))?;
    let record_digest = recovery_hex(challenge, "recordDigest").ok_or(fail("SHAPE:challenge"))?;
    let c = o
        .get("counters")
        .and_then(object)
        .ok_or(fail("SHAPE:counters"))?;
    if !closed(c, &RECOVERY_COUNTERS, &[]) {
        return Err(fail("SHAPE:counters"));
    }
    let mut counters = [0; 3];
    for (i, key) in RECOVERY_COUNTERS.iter().enumerate() {
        counters[i] = c
            .get(*key)
            .and_then(integer)
            .filter(|n| *n >= 1)
            .ok_or(fail("SHAPE:counters"))?;
    }
    if o.get("installBinding").and_then(string) != Some("challenge") {
        return Err(fail("SHAPE:installBinding"));
    }
    Ok(RecoveryEpoch {
        serial,
        issued,
        issued_text: issued_text.into(),
        nonce,
        record_digest,
        counters,
    })
}
fn admit_recovery_pending(value: &V) -> Result<RecoveryPending, RecoveryError> {
    let fail = RecoveryError::Refused("PENDING_SHAPE");
    let o = object(value).ok_or(fail)?;
    if !closed(
        o,
        &[
            "nonce",
            "recordDigest",
            "bootId",
            "createdMono",
            "expiresMono",
            "createdWall",
        ],
        &[],
    ) {
        return Err(RecoveryError::Refused("PENDING_SHAPE"));
    }
    let parse = || -> Option<RecoveryPending> {
        let nonce = recovery_hex(o, "nonce")?;
        let record_digest = recovery_hex(o, "recordDigest")?;
        let boot = o.get("bootId").and_then(string)?;
        if boot.is_empty() || boot.chars().count() > 256 {
            return None;
        }
        let created = o.get("createdMono").and_then(integer)?;
        let expires = o.get("expiresMono").and_then(integer)?;
        if created < 0 || created.checked_add(86_400) != Some(expires) {
            return None;
        }
        timestamp_seconds(o.get("createdWall").and_then(string)?).ok()?;
        Some(RecoveryPending {
            nonce,
            record_digest,
            boot: boot.into(),
            created,
            expires,
        })
    };
    parse().ok_or(RecoveryError::Refused("PENDING_SHAPE"))
}
fn recovery_observation(value: &V) -> Result<RecoveryObservation, RecoveryError> {
    let parse = || -> Option<RecoveryObservation> {
        let o = object(value)?;
        if !closed(o, &["wall", "mono", "bootId"], &[]) {
            return None;
        }
        let wall = timestamp_seconds(o.get("wall").and_then(string)?).ok()?;
        let mono = o.get("mono").and_then(integer)?;
        let boot = o.get("bootId").and_then(string)?;
        if mono < 0 || boot.is_empty() || boot.chars().count() > 256 {
            return None;
        }
        Some(RecoveryObservation {
            wall,
            mono,
            boot: boot.into(),
        })
    };
    parse().ok_or(RecoveryError::Input("OBSERVATION_SHAPE"))
}
// This owner admits the entire retained value. An immutable six-member
// projection does not confer storage custody or persistence authority.
pub(crate) use admitted_trust_records::ClockProjection;
#[cfg(test)]
pub(super) fn clock_fixture_projection(value: &V) -> Result<ClockProjection, String> {
    admitted_trust_records::admit(value)
        .map(|record| record.into_clock_projection())
        .map_err(|e| format!("{e:?}"))
}
mod successor_record_bindings {
    include!("successor_record_bindings.rs");
}
mod directory_name_scan {
    include!("directory_name_scan.rs");
}
mod directory_record_capture {
    include!("directory_record_capture.rs");
}
mod directory_successors {
    include!("directory_successors.rs");
}
mod directory_provers {
    include!("directory_provers.rs");
}
mod native_record_capture {
    include!("native_record_capture.rs");
}
#[cfg(target_os = "macos")]
pub use native_read_session::{
    NativeTrustReadError, NativeTrustReadSession, ProvisionalSuccessorCounts,
};
#[cfg(target_os = "macos")]
mod native_read_session {
    include!("native_read_session.rs");
}
mod native_current {
    include!("native_current.rs");
}
pub(crate) use native_current::{CURRENT_STATE_CAP, decode_current_store};
#[cfg(target_os = "macos")]
mod native_platform {
    include!("native_platform.rs");
}
#[cfg(target_os = "macos")]
mod native_profile_census {
    include!("native_profile_census.rs");
}
mod native_census {
    include!("native_census.rs");
}
mod current_record_bindings {
    include!("current_record_bindings.rs");
}
mod current_event_trace {
    include!("current_event_trace.rs");
}
mod core_authentication {
    include!("core_authentication.rs");
}
mod core_anchor {
    include!("core_anchor.rs");
}
mod core_inventory {
    include!("core_inventory.rs");
}
mod core_release_embedding {
    include!("core_release_embedding.rs");
}
// Law 465 reaches this receipt from custody; its refusal payloads stay
// private to this module and are carried only for diagnostics.
#[cfg(target_os = "macos")]
#[allow(private_interfaces)]
mod initial_core {
    include!("initial_core.rs");
}
#[cfg(target_os = "macos")]
pub(crate) use initial_core::{InitialCore, InitialCoreRefusal, StateWriter, produce_initial_core};
#[cfg(target_os = "macos")]
pub(crate) use initial_platform::AclOmissionPremise;
#[cfg(target_os = "macos")]
pub(crate) use initial_platform::{
    InitialPlatform, InitialPlatformRefusal, PrimitivePolicy, produce_initial_platform,
};
#[cfg(all(any(test, feature = "crash-matrix", feature = "scenario-fixtures"), target_os = "macos"))]
pub(crate) use initial_platform::tests::{
    ReadProducers, Receipts as InitialReceipts, read_producers, receipts_at,
};
// Law 465 reaches this receipt from custody; its refusal payloads stay
// private to this module and are carried only for diagnostics.
#[cfg(target_os = "macos")]
#[allow(private_interfaces)]
mod initial_platform {
    include!("initial_platform.rs");
}
mod captured_time_context {
    include!("captured_time_context.rs");
}
mod proposed_time_input {
    include!("proposed_time_input.rs");
}
mod captured_capsule_clock {
    include!("captured_capsule_clock.rs");
}
mod admitted_trust_records {
    include!("admitted_trust_records.rs");
}
// Law X4T r4 item 13 (X4T-0): a test-only signed accepted-store generator.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
mod accepted_store_fixture {
    include!("accepted_store_fixture.rs");
}
/// Unit X4a's tests: X4T-0's signed accepted store for S and K, with the
/// given revocation entries and list version, written under I (state.v1
/// last, each file in place). Returns the running core closure the store's
/// P0 names. Test-only, as the generator.
#[cfg(test)]
pub(crate) fn write_accepted_trust(
    installation: &std::path::Path,
    store: &str,
    state_schema: i128,
    revocations: Vec<(&'static str, String)>,
    revocation_version: i128,
) -> &'static str {
    write_accepted_trust_issued(
        installation,
        store,
        state_schema,
        revocations,
        revocation_version,
        None,
        None,
    )
}
/// Unit X4-F2 (law X4T r12 item 12): the same store, with its bootstrap
/// manifest issued at `manifest_issued` when given (X4T-0's knob), so that a
/// first read's tEval can pass the list's staleness within S4's plausibility
/// bound.
#[cfg(test)]
pub(crate) fn write_accepted_trust_issued(
    installation: &std::path::Path,
    store: &str,
    state_schema: i128,
    revocations: Vec<(&'static str, String)>,
    revocation_version: i128,
    manifest_issued: Option<&'static str>,
    accepted_seconds: Option<i64>,
) -> &'static str {
    use accepted_store_fixture::{CORE_CLOSURE, Spec, generate, generate_at};
    let spec = Spec {
        store: Some(store.to_owned()),
        state_schema,
        revocations,
        revocation_version,
        manifest_issued,
        ..Spec::default()
    };
    let generated = match accepted_seconds {
        Some(seconds) => generate_at(&spec, seconds),
        None => generate(&spec),
    };
    generated.write(installation);
    CORE_CLOSURE
}
/// Law X9 r1 item 6 / X8 r3 item 4b: X4T-0's signed accepted store for S
/// and K, with these revocation entries and list version, as each file's
/// path under I and its bytes (`state.v1` last), and the core closure its P0
/// names. The generator itself stays private to this module.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub(crate) fn accepted_store_files(
    store: &str,
    state_schema: i128,
    revocations: Vec<(&'static str, String)>,
    revocation_version: i128,
    accepted_seconds: Option<i64>,
) -> (Vec<(String, Vec<u8>)>, &'static str) {
    use accepted_store_fixture::{CORE_CLOSURE, Spec, generate, generate_at};
    let spec = Spec {
        store: Some(store.to_owned()),
        state_schema,
        revocations,
        revocation_version,
        ..Spec::default()
    };
    let generated = match accepted_seconds {
        Some(seconds) => generate_at(&spec, seconds),
        None => generate(&spec),
    };
    let files = generated
        .files
        .into_iter()
        .map(|file| (file.path, file.bytes))
        .collect();
    (files, CORE_CLOSURE)
}
#[cfg(test)]
mod trust_record_owner_tests {
    include!("trust_record_owner_tests.rs");
}
struct RecoveryInputs<'a> {
    record: &'a V,
    stored: &'a [u8],
    envelope: &'a V,
    observation: &'a V,
    revoked: &'a BTreeSet<[u8; 32]>,
}
#[cfg(test)]
mod recovery_tests {
    include!("recovery_tests.rs");
}
#[cfg(test)]
mod challenge_tests {
    include!("challenge_tests.rs");
}
#[derive(Debug, PartialEq, Eq)]
enum ProfileError {
    Metadata,
    Shape,
    CorePin,
    NoProfileRole,
    SignatureThreshold,
    Envelope,
}

fn profile_strings(value: &V, minimum: usize, predicate: impl Fn(&str) -> bool) -> bool {
    array(value)
        .is_some_and(|a| a.len() >= minimum && a.iter().all(|v| string(v).is_some_and(&predicate)))
}
fn mac_build(s: &str) -> bool {
    let b = s.as_bytes();
    if !(4..=9).contains(&b.len())
        || !b[..2].iter().all(u8::is_ascii_digit)
        || !b[2].is_ascii_uppercase()
    {
        return false;
    }
    let end = if b.last().is_some_and(u8::is_ascii_lowercase) {
        b.len() - 1
    } else {
        b.len()
    };
    (1..=5).contains(&(end - 3)) && b[3..end].iter().all(u8::is_ascii_digit)
}
fn upper_uuid(s: &str) -> bool {
    s.len() == 36
        && s.bytes().enumerate().all(|(i, b)| {
            if [8, 13, 18, 23].contains(&i) {
                b == b'-'
            } else {
                b.is_ascii_digit() || (b'A'..=b'F').contains(&b)
            }
        })
}
fn lower_hex_width(s: &str, width: usize) -> bool {
    s.len() == width
        && s.bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}
fn kernel_line(s: &str) -> bool {
    let mut n = 0;
    for part in s.split('.') {
        if part.is_empty() || !part.bytes().all(|b| b.is_ascii_digit()) {
            return false;
        }
        n += 1;
    }
    n == 3
}
fn kernel_flavor(s: &str) -> bool {
    !s.is_empty() && s.bytes().all(lower_or_digit)
}
fn mac_profile(value: &V, schema: i64) -> bool {
    let Some(o) = object(value) else {
        return false;
    };
    if !closed(
        o,
        &[
            "installRootFilesystems",
            "projectRootFilesystems",
            "supportedMajors",
            "measuredProfiles",
        ],
        &[],
    ) {
        return false;
    }
    if !["installRootFilesystems", "projectRootFilesystems"]
        .iter()
        .all(|k| profile_strings(&o[*k], 1, |s| s == "apfs"))
    {
        return false;
    }
    let Some(majors) = object(&o["supportedMajors"]) else {
        return false;
    };
    if !majors.values().all(|v| {
        object(v).is_some_and(|r| {
            closed(r, &["minBuild", "marketing"], &[])
                && r.get("minBuild").and_then(string).is_some_and(mac_build)
                && r.get("marketing").and_then(string).is_some()
        })
    }) {
        return false;
    }
    array(&o["measuredProfiles"]).is_some_and(|rows| {
        rows.iter().all(|v| {
            object(v).is_some_and(|r| {
                // Law 458b: only a V2 macOS measured row may carry the
                // omission qualification, and only as the one const value.
                let optional: &[&str] = if schema == 2 {
                    &["installAclOmission"]
                } else {
                    &[]
                };
                closed(r, &["build", "kernUuid", "dyldCdhash", "lane"], optional)
                    && r.get("installAclOmission")
                        .is_none_or(|v| string(v) == Some("no-acl-stored"))
                    && r.get("build").and_then(string).is_some_and(mac_build)
                    && r.get("kernUuid").and_then(string).is_some_and(upper_uuid)
                    && r.get("dyldCdhash")
                        .and_then(string)
                        .is_some_and(|s| lower_hex_width(s, 40))
                    && r.get("lane")
                        .and_then(string)
                        .is_some_and(|s| ["macos-15", "macos-15-intel"].contains(&s))
            })
        })
    })
}
fn linux_profile(value: &V) -> bool {
    let Some(o) = object(value) else {
        return false;
    };
    if !closed(
        o,
        &[
            "distro",
            "series",
            "installRootFilesystems",
            "projectRootFilesystems",
            "archiveSigningKeyDigest",
            "bootAttestation",
            "supportedKernelLines",
            "baselineFlavors",
            "measuredProfiles",
        ],
        &[],
    ) {
        return false;
    }
    if o.get("distro").and_then(string) != Some("ubuntu")
        || !profile_strings(&o["series"], 1, |s| s == "24.04")
        || !o
            .get("archiveSigningKeyDigest")
            .and_then(string)
            .is_some_and(|s| lower_hex_width(s, 64))
        || !o
            .get("bootAttestation")
            .and_then(string)
            .is_some_and(|s| ["secure-boot-lockdown", "package-db-declared"].contains(&s))
    {
        return false;
    }
    if !["installRootFilesystems", "projectRootFilesystems"]
        .iter()
        .all(|k| profile_strings(&o[*k], 1, |s| ["ext4", "xfs", "btrfs"].contains(&s)))
        || !profile_strings(&o["supportedKernelLines"], 1, kernel_line)
        || !profile_strings(&o["baselineFlavors"], 1, kernel_flavor)
    {
        return false;
    }
    array(&o["measuredProfiles"]).is_some_and(|rows| {
        rows.iter().all(|v| {
            object(v).is_some_and(|r| {
                closed(r, &["line", "flavor", "lane"], &[])
                    && r.get("line").and_then(string).is_some_and(kernel_line)
                    && r.get("flavor").and_then(string).is_some_and(kernel_flavor)
                    && r.get("lane")
                        .and_then(string)
                        .is_some_and(|s| ["ubuntu-24.04", "ubuntu-24.04-arm"].contains(&s))
            })
        })
    })
}
/// `PlatformProfileSetV1`, the shape every existing reader admits.
fn profile_shape(value: &V) -> bool {
    profile_shape_version(value, 1)
}
/// `PlatformProfileSetV2` (law 458b), for a reader that opts into it.
fn profile_shape_v2(value: &V) -> bool {
    profile_shape_version(value, 2)
}
fn profile_shape_version(value: &V, schema: i64) -> bool {
    let Some(o) = object(value) else {
        return false;
    };
    if !closed(o, &["profileSetSchema", "standing", "platforms"], &[])
        || o.get("profileSetSchema").and_then(integer) != Some(schema)
        || o.get("standing").and_then(string).is_none()
    {
        return false;
    }
    object(&o["platforms"]).is_some_and(|platforms| {
        platforms.iter().all(|(id, v)| match id.as_str() {
            "macos-aarch64" | "macos-x86_64" => mac_profile(v, schema),
            "linux-x86_64-gnu" | "linux-aarch64-gnu" => linux_profile(v),
            _ => false,
        })
    })
}
// Keep validated payloads immutable outside the verifier's own module.
// There is no raw-value constructor, mutable accessor or public field.
mod admitted_profiles {
    include!("admitted_profiles.rs");
}
use admitted_profiles::{InitialProfile, ProfileSetEvidence};
#[cfg(test)]
use admitted_profiles::{ProfileReader, verify_profile_set, verify_profile_set_with};
#[cfg(test)]
mod profile_tests {
    include!("profile_tests.rs");
}
// Pure decisions over conditional signed profile evidence and supplied observations.
// No OS measurement, execution grant or durable authority is created here.
#[derive(Debug, PartialEq, Eq)]
enum PlatformError {
    Observation,
    Metadata,
}
#[derive(Debug, PartialEq, Eq)]
enum PlatformTier {
    ExactMeasured,
    BaselineAttested,
}
#[derive(Debug)]
struct PlatformDecision {
    platform: Option<String>,
    tier: Option<PlatformTier>,
    lane: Option<String>,
    refusals: Vec<String>,
    drift: std::collections::BTreeMap<String, V>,
    /// The selected (last-duplicate) measured row carried law 458b's
    /// `installAclOmission`. Read only through `install_acl_omission`.
    matched_acl_omission: bool,
}
impl PlatformDecision {
    /// Law 458b decision 5: the matched measured row's qualification, only for
    /// an admitted exact-measured decision with no refusals. Never a scan of
    /// other rows and never at BASELINE-ATTESTED.
    fn install_acl_omission(&self) -> bool {
        self.matched_acl_omission
            && self.tier == Some(PlatformTier::ExactMeasured)
            && self.lane.is_some()
            && self.refusals.is_empty()
    }
}
// The raw platform helper cannot accept an arbitrary metadata value. The
// child module owns the field, so production callers can only borrow a
// profile already admitted by the signed-profile verifier. The unsigned
// fixture constructor exists exclusively in test builds and checks shape
// and metadata limits; it conveys no signature or execution authority.
mod platform_profile {
    use super::*;
    pub(super) struct AdmittedProfile<'a>(&'a V);
    impl<'a> AdmittedProfile<'a> {
        pub(super) fn from_verified(profile: &'a ProfileSetEvidence) -> Self {
            Self(profile.envelope().payload())
        }
        /// Law 462: a profile authenticated under the initial release context.
        pub(super) fn from_initial(profile: &'a InitialProfile) -> Self {
            Self(profile.payload())
        }
        pub(super) fn value(&self) -> &'a V {
            self.0
        }
        #[cfg(test)]
        pub(super) fn unsigned_fixture(value: &'a V) -> Option<Self> {
            if super::super::metadata_bytes(value, 5_000_000).is_err() || !profile_shape(value) {
                return None;
            }
            Some(Self(value))
        }
        /// Test-only V2 counterpart (law 458b), with the same checks.
        #[cfg(test)]
        pub(super) fn unsigned_fixture_v2(value: &'a V) -> Option<Self> {
            if super::super::metadata_bytes(value, 5_000_000).is_err() || !profile_shape_v2(value)
            {
                return None;
            }
            Some(Self(value))
        }
    }
}
fn platform_decision(
    profile: platform_profile::AdmittedProfile<'_>,
    observed: &V,
) -> Result<PlatformDecision, PlatformError> {
    let profile = profile.value();
    let o = object(observed).ok_or(PlatformError::Observation)?;
    let platform = o
        .get("platform")
        .and_then(string)
        .filter(|s| s.chars().count() <= 64);
    let mut d = PlatformDecision {
        platform: platform.map(str::to_owned),
        tier: None,
        lane: None,
        refusals: Vec::new(),
        drift: std::collections::BTreeMap::new(),
        matched_acl_omission: false,
    };
    let Some(platform) = platform else {
        d.refusals
            .push("NT-TCB-PROFILE-UNQUALIFIED:platform-not-in-population".into());
        return Ok(d);
    };
    let alias = match platform {
        "macos-arm64" => Some("macos-aarch64"),
        "linux-x86_64" => Some("linux-x86_64-gnu"),
        "linux-arm64" => Some("linux-aarch64-gnu"),
        _ => None,
    };
    if let Some(id) = alias {
        d.refusals.push(format!(
            "NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:{id}"
        ));
        return Ok(d);
    }
    let lane = match platform {
        "macos-aarch64" => "macos-15",
        "macos-x86_64" => "macos-15-intel",
        "linux-x86_64-gnu" => "ubuntu-24.04",
        "linux-aarch64-gnu" => "ubuntu-24.04-arm",
        _ => "",
    };
    let ps = object(profile)
        .and_then(|p| p.get("platforms"))
        .and_then(object)
        .and_then(|p| p.get(platform))
        .and_then(object);
    let Some(ps) = ps.filter(|_| !lane.is_empty()) else {
        d.refusals
            .push("NT-TCB-PROFILE-UNQUALIFIED:platform-not-in-population".into());
        return Ok(d);
    };
    let text = |key: &str| o.get(key).and_then(string);
    let yes = |key: &str| o.get(key) == Some(&V::Bool(true));
    let contains = |key: &str, value: Option<&str>| {
        array(&ps[key])
            .is_some_and(|a| value.is_some_and(|s| a.iter().any(|v| string(v) == Some(s))))
    };
    // Non-string filesystem observations cannot match the admitted set and
    // receive the same fixed refusal as absent or unrecognized filesystems.
    let fs = text("fsType");
    if !contains("installRootFilesystems", fs) {
        // Never copy arbitrary observed text into a refusal.
        d.refusals.push("NT-TCB-BOOT:INSTALL_ROOT_FS".into());
    }
    if platform.starts_with("macos") {
        if text("authenticatedRoot") != Some("enabled") {
            d.refusals
                .push("NT-TCB-BOOT:AUTHENTICATED_ROOT_DISABLED".into());
        }
        if !yes("sip") {
            d.refusals.push("NT-TCB-BOOT:SIP_DISABLED".into());
        }
        if !d.refusals.is_empty() {
            return Ok(d);
        }
        let build = text("osversion");
        let Some(bk) = build.and_then(mac_build_key) else {
            d.refusals.push("NT-TCB-IDENTITY:BUILD_GRAMMAR".into());
            return Ok(d);
        };
        let build = build.unwrap();
        // Both tiers admit the same closed identity fields before retaining drift.
        for (key, valid) in [
            ("kernUuid", text("kernUuid").is_some_and(upper_uuid)),
            (
                "dyldCdhash",
                text("dyldCdhash").is_some_and(|s| {
                    s.len() == 40
                        && s.bytes()
                            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
                }),
            ),
        ] {
            if !valid {
                d.refusals.push(format!("NT-TCB-IDENTITY:{key}"));
                return Ok(d);
            }
        }
        // Reference semantics deliberately select the last duplicate macOS build.
        let measured = array(&ps["measuredProfiles"])
            .unwrap()
            .iter()
            .rev()
            .filter_map(object)
            .find(|m| m.get("build").and_then(string) == Some(build));
        if let Some(m) = measured {
            let selected = string(&m["lane"]).unwrap();
            if selected != lane {
                d.refusals.push(format!(
                    "NT-TCB-PROFILE-UNQUALIFIED:MEASURED_ON_UNLISTED_LANE_{selected}"
                ));
                return Ok(d);
            }
            for key in ["kernUuid", "dyldCdhash"] {
                if o.get(key) != m.get(key) {
                    d.refusals.push(format!("NT-TCB-IDENTITY:{key}"));
                }
            }
            d.tier = Some(PlatformTier::ExactMeasured);
            if d.refusals.is_empty() {
                d.lane = Some(selected.into());
                // Only a V2 body can carry the member; V1 shape refuses it.
                d.matched_acl_omission = m.get("installAclOmission").and_then(string)
                    == Some("no-acl-stored")
                    && object(profile)
                        .and_then(|p| p.get("profileSetSchema"))
                        .and_then(integer)
                        == Some(2);
            }
            return Ok(d);
        }
        let major = bk.0.to_string();
        let Some(sup) = object(&ps["supportedMajors"])
            .unwrap()
            .get(&major)
            .and_then(object)
        else {
            d.refusals
                .push(format!("NT-TCB-PROFILE-UNQUALIFIED:MACOS_MAJOR_{major}"));
            return Ok(d);
        };
        let minimum = string(&sup["minBuild"]).unwrap();
        if bk < mac_build_key(minimum).unwrap() {
            d.refusals.push(format!(
                "NT-TCB-PROFILE-UNQUALIFIED:BUILD_BELOW_FLOOR_{minimum}"
            ));
            return Ok(d);
        }
        d.tier = Some(PlatformTier::BaselineAttested);
        for key in ["kernUuid", "dyldCdhash", "osversion"] {
            d.drift
                .insert(key.into(), o.get(key).cloned().unwrap_or(V::Null));
        }
        d.drift.insert(
            "standing".into(),
            V::String("recorded-never-allow-refuse".into()),
        );
        return Ok(d);
    }
    if text("osReleaseId") != string(&ps["distro"]) || !contains("series", text("versionId")) {
        d.refusals = vec!["NT-TCB-PROFILE-UNQUALIFIED:DISTRO_SERIES".into()];
        return Ok(d);
    }
    if !yes("procVersionUbuntu") {
        d.refusals
            .push("NT-TCB-BOOT:PROC_VERSION_NOT_UBUNTU".into());
    }
    if !yes("dpkgInstalled") || !yes("dpkgMaintainerUbuntu") {
        d.refusals
            .push("NT-TCB-BOOT:KERNEL_PACKAGE_NOT_INSTALLED_BY_UBUNTU".into());
    }
    if o.get("archiveKeyDigest") != ps.get("archiveSigningKeyDigest") {
        d.refusals.push("NT-TCB-BOOT:ARCHIVE_KEY_DIGEST".into());
    }
    if string(&ps["bootAttestation"]) == Some("secure-boot-lockdown") {
        if o.get("secureBoot").and_then(integer) != Some(1) {
            d.refusals.push("NT-TCB-BOOT:SECURE_BOOT_OFF".into());
        }
        if !matches!(text("lockdown"), Some("integrity" | "confidentiality")) {
            d.refusals.push("NT-TCB-BOOT:LOCKDOWN_NONE".into());
        }
        if !yes("uefiSignerPresent") {
            d.refusals.push("NT-TCB-BOOT:UEFI_SIGNER_ABSENT".into());
        }
    }
    if !yes("nsUnchanged") {
        d.refusals
            .push("NT-TCB-BOOT:MOUNT_NAMESPACE_CHANGED_DURING_READ".into());
    }
    if !d.refusals.is_empty() {
        return Ok(d);
    }
    let Some((line, abi, flavor)) = text("osrelease").and_then(kernel_release_parts) else {
        d.refusals.push("NT-TCB-IDENTITY:OSRELEASE_GRAMMAR".into());
        return Ok(d);
    };
    // Linux selects the first matching line/flavor, and deliberately records ABI drift.
    for m in array(&ps["measuredProfiles"])
        .unwrap()
        .iter()
        .filter_map(object)
    {
        if string(&m["line"]) == Some(line) && string(&m["flavor"]) == Some(flavor) {
            let selected = string(&m["lane"]).unwrap();
            if selected != lane {
                d.refusals.push(format!(
                    "NT-TCB-PROFILE-UNQUALIFIED:MEASURED_ON_UNLISTED_LANE_{selected}"
                ));
                return Ok(d);
            }
            d.tier = Some(PlatformTier::ExactMeasured);
            d.lane = Some(selected.into());
            d.drift.insert("abi".into(), V::String(abi.into()));
            return Ok(d);
        }
    }
    if contains("supportedKernelLines", Some(line)) && contains("baselineFlavors", Some(flavor)) {
        d.tier = Some(PlatformTier::BaselineAttested);
        for (k, v) in [("line", line), ("abi", abi), ("flavor", flavor)] {
            d.drift.insert(k.into(), V::String(v.into()));
        }
    } else {
        d.refusals.push(format!(
            "NT-TCB-PROFILE-UNQUALIFIED:KERNEL_LINE_OR_FLAVOR_{line}-{flavor}"
        ));
    }
    Ok(d)
}
fn mac_build_key(s: &str) -> Option<(u32, u8, u32)> {
    if !mac_build(s) {
        return None;
    }
    let b = s.as_bytes();
    let end = if b.last()?.is_ascii_lowercase() {
        b.len() - 1
    } else {
        b.len()
    };
    Some((s[..2].parse().ok()?, b[2], s[3..end].parse().ok()?))
}
fn kernel_release_parts(s: &str) -> Option<(&str, &str, &str)> {
    // The complete ASCII observation is bounded before reflecting any
    // line, ABI or flavor in diagnostics/drift (reference122).
    if s.len() > 256 {
        return None;
    }
    let mut parts = s.split('-');
    let line = parts.next()?;
    let abi = parts.next()?;
    let flavor = parts.next()?;
    if parts.next().is_some()
        || !kernel_line(line)
        || abi.is_empty()
        || !abi.bytes().all(|b| b.is_ascii_digit())
        || !kernel_flavor(flavor)
    {
        return None;
    }
    Some((line, abi, flavor))
}
#[cfg(test)]
mod platform_tests {
    include!("platform_tests.rs");
}
#[derive(Debug, PartialEq, Eq)]
enum RevocationError {
    Metadata,
    Shape,
    RootVersion,
    Envelope,
    SignatureThreshold,
}

fn revocation_schema_shape(v: &V) -> bool {
    let Some(o) = object(v) else { return false };
    if !closed(
        o,
        &[
            "revocationSchema",
            "revocationVersion",
            "issuedAt",
            "rootVersion",
            "entries",
        ],
        &[],
    ) || o.get("revocationSchema").and_then(integer) != Some(1)
        || !["revocationVersion", "rootVersion"]
            .iter()
            .all(|k| o.get(*k).and_then(integer).is_some_and(|n| n > 0))
        || o.get("issuedAt").is_none_or(|v| !timestamp_shape(v))
    {
        return false;
    }
    array(&o["entries"]).is_some_and(|rows| {
        rows.len() <= 4096
            && rows.iter().all(|v| {
                object(v).is_some_and(|r| {
                    closed(r, &["subjectKind", "subject", "reason", "revokedAt"], &[])
                        && r.get("subjectKind").and_then(string).is_some_and(|s| {
                            ["keyId", "namespace", "release", "catalogSnapshot"].contains(&s)
                        })
                        && r.get("subject")
                            .and_then(string)
                            .is_some_and(|s| (1..=256).contains(&s.chars().count()))
                        && r.get("reason").and_then(string).is_some_and(|s| {
                            ["key-compromise", "superseded", "defect", "policy"].contains(&s)
                        })
                        && r.get("revokedAt").is_some_and(timestamp_shape)
                })
            })
    })
}
fn revocation_shape(v: &V) -> bool {
    if !revocation_schema_shape(v) {
        return false;
    }
    let o = object(v).expect("schema admitted");
    timestamp_seconds(string(&o["issuedAt"]).expect("schema admitted")).is_ok()
        && array(&o["entries"])
            .expect("schema admitted")
            .iter()
            .all(|v| {
                timestamp_seconds(
                    string(&object(v).expect("schema admitted")["revokedAt"])
                        .expect("schema admitted"),
                )
                .is_ok()
            })
}
// A verified document, not a current revocation view: callers still need
// admitted time, durable monotonic counters and authenticated root custody.
// Keep validated payloads immutable outside the verifier's own module.
// There is no raw-value constructor, mutable accessor or public field.
mod admitted_revocations {
    include!("admitted_revocations.rs");
}
use admitted_revocations::RevocationEvidence;
#[cfg(test)]
use admitted_revocations::verify_revocation;
#[cfg(test)]
mod revocation_tests {
    include!("revocation_tests.rs");
}
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct PermissionPair {
    stable_id: String,
    token: String,
}
struct ClosureSubjects {
    releases: BTreeSet<String>,
    signing_keys: BTreeSet<String>,
    namespaces: BTreeSet<String>,
    catalog_snapshot: Option<i64>,
}
// The caller obtains this epoch from the first successful counter read of
// the SAME FreshnessMonitor used by the operation, before any effect. An
// older captured epoch cannot seed a newly created monitor: its initial
// read only bounds that read's duration, not an unobserved earlier gap.
struct EpochAtStart {
    revocation_version: i64,
    permission_policy_digest: [u8; 32],
}
#[derive(Debug, PartialEq, Eq)]
enum RevocationAction {
    Continue,
    Revoke,
}
struct ConditionalRevocationObservation {
    source_digest: [u8; 32],
    source_root_digest: [u8; 32],
    source_version: i64,
    action: RevocationAction,
    reason: &'static str,
    matches: Vec<V>,
}
fn observe_revocation(
    current: &RevocationEvidence,
    start: &EpochAtStart,
    closure: &ClosureSubjects,
    current_policy: [u8; 32],
    allowed: &BTreeSet<PermissionPair>,
    required: Option<&[PermissionPair]>,
) -> ConditionalRevocationObservation {
    let mut out = ConditionalRevocationObservation {
        source_digest: current.envelope().preimage_digest(),
        source_root_digest: current.envelope().quorum().root_digest(),
        source_version: current.version(),
        action: RevocationAction::Continue,
        reason: "no-change",
        matches: Vec::new(),
    };
    // This is the selected observation predicate, not rollback admission.
    // A lower counter must be refused by custody/current-view admission.
    if current.version() < start.revocation_version {
        out.reason =
            "counter-below-start (rollback is detected elsewhere; never revoke on a lower counter)";
        return out;
    }
    if current.version() > start.revocation_version {
        for v in array(&object(current.envelope().payload()).unwrap()["entries"]).unwrap() {
            let e = object(v).unwrap();
            let subject = string(&e["subject"]).unwrap();
            let matched = match string(&e["subjectKind"]).unwrap() {
                "release" => closure.releases.contains(subject),
                "keyId" => closure.signing_keys.contains(subject),
                "namespace" => closure.namespaces.contains(subject),
                "catalogSnapshot" => closure
                    .catalog_snapshot
                    .is_some_and(|n| n.to_string() == subject),
                _ => false,
            };
            if matched {
                out.matches.push(v.clone());
            }
        }
        if !out.matches.is_empty() {
            out.action = RevocationAction::Revoke;
            out.reason = "trust-revoked";
            return out;
        }
    }
    let policy_changed = current_policy != start.permission_policy_digest;
    if policy_changed && let Some(required) = required {
        for grant in required {
            if !allowed.contains(grant) {
                out.matches
                    .push(V::Object(std::collections::BTreeMap::from([
                        ("stableId".into(), V::String(grant.stable_id.clone())),
                        ("token".into(), V::String(grant.token.clone())),
                    ])));
            }
        }
        if !out.matches.is_empty() {
            out.action = RevocationAction::Revoke;
            out.reason = "policy";
            return out;
        }
    }
    out.reason = match (
        current.version() != start.revocation_version,
        policy_changed,
    ) {
        (false, false) => "no-change",
        (true, false) => "revocation-unrelated",
        (false, true) => "policy-unrelated",
        (true, true) => "revocation-unrelated,policy-unrelated",
    };
    out
}

#[cfg(test)]
mod revocation_observe_tests {
    include!("revocation_observe_tests.rs");
}
#[cfg(test)]
mod signed112_tests {
    include!("signed112_tests.rs");
}

// M3-D r5 item 24 (unit D4-2): the shared synthetic component bodies for
// R10a's judge's fixtures, under the joint fixture predicate only: every
// role (C2a-2's `every_role`), then an analyzer at 1.0.5 whose provenance
// says `explicitly-trusted`.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub(crate) fn admission_fixture_bodies() -> Vec<Vec<u8>> {
    use core_authentication::tests::components::{Synthetic, body, every_role};
    let mut bodies = every_role();
    let raw = body(&Synthetic::of("analyzer", "1.0.5"));
    let mut v = opensip_identity::parse_json(&raw).unwrap();
    if let V::Object(m) = &mut v
        && let Some(V::Object(provenance)) = m.get_mut("provenance")
    {
        provenance.insert("sourceClass".to_owned(), V::String("explicitly-trusted".to_owned()));
    }
    bodies.push(opensip_identity::canonical_bytes(&v).unwrap());
    bodies
}
