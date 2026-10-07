// X4T-0 (law X4T r4 item 13): a TEST-ONLY generator of a signed accepted
// trust store. No product producer exists yet for the retained-phase records
// (that is X4B and S4.5), so this module constructs exactly these kinds:
// RootAdmissionNodeV1, MetadataAdmissionNodeV1, RevocationHistoryNodeV1,
// RoleEventV1 (with its RoleChangeV1 and PublicationEventV1 descriptor rows),
// TimeEvidenceV1 (an S4 evaluation input) with its SignedTimeSourceV1, the
// clock-write event the role events cite, and the retained-phase
// TrustCapsuleV1. Every record is canonically encoded and admitted by its
// closed shape here; every signed document (root, catalog, revocation, payload
// manifest) is signed with the public test-only quorum seeds. The store sits
// on a real P0 publication from `initial_publication`. This module is compiled
// only under `cfg(test)`; no production path can reach it. X4T-a3 (law X4T
// r10 item 13) adds a recorded rotation of n roots, the head at the last.
//
// X4B-c (law X4B r5 item 9): wherever X4B's producer can end the requested
// roles in their states (Trusted, Expired, StaleRevocation and Revoked,
// through item 4's sequences), `generate` builds the signed payload those
// states need and takes every retained-phase record from the producer
// (`trust_bootstrap::build_over_p0`) over the same P0. Only a store the
// producer cannot reach keeps this module's own construction: a state no
// acceptance sequence ends in (QuorumLost; Recovery is not offered), a role
// acceptance does not carry (TR-PROFILE, TR-REPAIR) or must carry (TR-BUNDLE,
// TR-CORE, TR-INDEX), a combination item 4's time and revocation inputs do
// not give, and the deliberately unlawful X4T-a3 stores (`ChainEnd` other
// than `Head`, replaced signers). `AcceptedStore::produced` says which.
//
// X4-F2 (law X4T r12 item 13): three test-only time knobs, so a fenced
// read's tEval can reach an expiry within S4's plausibility bound while the
// stored roles stay as accepted: the bootstrap manifest's later issue time
// (which raises A above the list's issue time), the signing root's
// `expiresAt` and the catalog's `expiresAt`. Each is signed into its document,
// never edited into stored bytes; with none set, every store is unchanged.
use super::core_authentication::tests::{quorum_root, sign};
use super::retained_metadata_index::Collection;
use crate::trust::trust_outcomes::reference;
use crate::trust::trust_record_shapes::{self as shapes, Definition};
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes, digest_hex, raw_sha256};
use std::collections::BTreeMap;
use std::path::Path;

pub(crate) const ROLES: [&str; 6] = [
    "TR-BUNDLE",
    "TR-COMPONENT",
    "TR-CORE",
    "TR-INDEX",
    "TR-PROFILE",
    "TR-REPAIR",
];
pub(crate) const STORE: &str = "11111111111111111111111111111111";
/// The P0 publication's delivering core, which the store's acceptance keeps.
pub(crate) const CORE_CLOSURE: &str =
    "closure2:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc";
/// The default issue time of every signed document but the root.
const ISSUED: &str = "2026-10-01T00:00:00Z";
/// The default catalog expiry.
const CATALOG_EXPIRES: &str = "2027-04-01T00:00:00Z";
/// The constructed store's acceptance wall (its tEval and L by default).
const ACCEPTED: &str = "2026-10-02T00:00:00Z";

/// The state a role ends in. Recovery is not offered: it needs a live
/// ceremony batch, which is not part of an accepted, retained store.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum RoleTarget {
    Unbootstrapped,
    Trusted,
    Expired,
    StaleRevocation,
    QuorumLost,
    Revoked,
}
impl RoleTarget {
    fn token(self) -> &'static str {
        match self {
            Self::Unbootstrapped => "ST-UNBOOTSTRAPPED",
            Self::Trusted => "ST-TRUSTED",
            Self::Expired => "ST-EXPIRED",
            Self::StaleRevocation => "ST-STALE-REVOCATION",
            Self::QuorumLost => "ST-QUORUM-LOST",
            Self::Revoked => "ST-REVOKED",
        }
    }
}

/// X4T-a3 (law X4T r10 item 13): the public test-only ROOT key sets a
/// recorded rotation cycles through. Root 1 holds the first (quorum root 1's
/// own `rootKeys`); root k+1 moves ROOT to the next set. The roles' keys never
/// change.
const ROOT_KEY_SETS: [[usize; 3]; 3] = [[0, 1, 2], [20, 21, 22], [23, 24, 25]];
fn root_keys(k: usize) -> &'static [usize] {
    &ROOT_KEY_SETS[k % ROOT_KEY_SETS.len()]
}

/// X4T-a3 (test-only): what the payload metadata closure's `rootChain`
/// records. Only `Head` is a lawful store.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum ChainEnd {
    /// The whole recorded chain, ending on `heads.root.document`.
    Head,
    /// The chain ends on the head's body with another stored envelope of it:
    /// a value-only match.
    OtherEnvelope,
    /// The chain without its last root (needs two roots or more).
    Short,
    /// No root at all. The closed shape refuses it, so this one record is
    /// written past the shape check.
    Empty,
}

/// Caller choices. `roles` is indexed like `ROLES`; at least one role must
/// leave `Unbootstrapped` (a retained capsule has accepted role history).
/// `revocations` are the signed list's (subjectKind, subject) entries, in
/// order; the list is otherwise empty. `store` is S (`STORE` when absent)
/// and `revocation_version` the signed list's version and the capsule's
/// revocation counter (X4a: a successor list for the same S).
pub(crate) struct Spec {
    pub(crate) roles: [RoleTarget; 6],
    pub(crate) state_schema: i128,
    pub(crate) revocations: Vec<(&'static str, String)>,
    pub(crate) store: Option<String>,
    pub(crate) revocation_version: i128,
    /// X4T-a3: the recorded root chain's length n (at least 1). Root k+1
    /// (version k+1) rotates ROOT to the next key set and its envelope is
    /// signed by the previous and the new set. `heads.root` is root n, every
    /// document is signed under it, and the closure's `rootChain` lists roots
    /// 1 to n.
    pub(crate) roots: usize,
    /// X4T-a3 (test-only): the seeds that sign root k's envelope (k from 0)
    /// in place of its defaults.
    pub(crate) root_signers: Vec<(usize, &'static [usize])>,
    /// X4T-a3 (test-only): the seeds that sign the revocation list in place
    /// of two of the signing root's ROOT keys.
    pub(crate) revocation_signers: Option<&'static [usize]>,
    /// X4T-a3 (test-only): what the closure's `rootChain` records.
    pub(crate) chain_end: ChainEnd,
    /// X4-F2 (test-only): the bootstrap manifest's `issuedAt` in place of
    /// 2026-10-01, the list's issue time. The acceptance's A, and so its L,
    /// is the newest issue time, so a later one moves S4's plausibility bound
    /// past the list's staleness.
    pub(crate) manifest_issued: Option<&'static str>,
    /// X4-F2 (test-only): the signing root's `expiresAt`.
    pub(crate) root_expires: Option<&'static str>,
    /// X4-F2 (test-only): the catalog's `expiresAt`.
    pub(crate) catalog_expires: Option<&'static str>,
}
impl Default for Spec {
    fn default() -> Self {
        let mut roles = [RoleTarget::Unbootstrapped; 6];
        for (i, r) in ROLES.iter().enumerate() {
            if ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE", "TR-INDEX"].contains(r) {
                roles[i] = RoleTarget::Trusted;
            }
        }
        Self {
            roles,
            state_schema: 1,
            revocations: Vec::new(),
            store: None,
            revocation_version: 1,
            roots: 1,
            root_signers: Vec::new(),
            revocation_signers: None,
            chain_end: ChainEnd::Head,
            manifest_issued: None,
            root_expires: None,
            catalog_expires: None,
        }
    }
}

/// One trust file: its path relative to I, collection (None for state.v1 and
/// the store marker), and exact bytes.
pub(crate) struct File {
    pub(crate) path: String,
    pub(crate) collection: Option<Collection>,
    pub(crate) bytes: Vec<u8>,
}

/// The generated store. `p0_*` are the real P0 publication's values, the
/// predecessor of the retained publication.
pub(crate) struct AcceptedStore {
    pub(crate) files: Vec<File>,
    pub(crate) store: V,
    pub(crate) capsule: V,
    pub(crate) descriptor: V,
    pub(crate) p0_capsule: V,
    pub(crate) root: V,
    pub(crate) root_body: Vec<u8>,
    /// X4B-c: true when every retained-phase record is X4B's producer's.
    pub(crate) produced: bool,
}
impl AcceptedStore {
    /// The bytes of one immutable record by collection and digest, as the
    /// reference-model stores supply them.
    pub(crate) fn lookup(&self, collection: Collection, hash: [u8; 32]) -> Option<Vec<u8>> {
        self.files
            .iter()
            .find(|f| f.collection == Some(collection) && raw_sha256(&f.bytes) == hash)
            .map(|f| f.bytes.clone())
    }
    /// Write every file under `root` (the installation I) with private modes.
    pub(crate) fn write(&self, root: &Path) {
        use std::fs::{self, Permissions};
        use std::os::unix::fs::PermissionsExt;
        for file in &self.files {
            let mut dir = root.to_path_buf();
            for component in Path::new(&file.path).parent().unwrap().components() {
                dir.push(component);
                if !dir.exists() {
                    fs::create_dir(&dir).unwrap();
                }
                fs::set_permissions(&dir, Permissions::from_mode(0o700)).unwrap();
            }
            let path = root.join(&file.path);
            fs::write(&path, &file.bytes).unwrap();
            fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
        }
    }
}

fn int(n: i128) -> V {
    V::Integer(JsonInteger::new(n).unwrap())
}
fn s(text: &str) -> V {
    V::String(text.into())
}
fn obj<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn o(v: &V) -> &BTreeMap<String, V> {
    let V::Object(o) = v else { panic!("object") };
    o
}

/// The constructor: canonical bytes of `value`, admitted by `definition`'s
/// closed shape. Any record this module writes passes here first.
pub(crate) fn encode(definition: Definition, value: &V) -> Vec<u8> {
    let raw = canonical_bytes(value).unwrap();
    shapes::admit(definition, &raw).unwrap_or_else(|e| {
        panic!(
            "{definition:?} shape: {e:?}: {}",
            String::from_utf8_lossy(&raw)
        )
    });
    raw
}
fn node(raw: &[u8]) -> V {
    reference(raw)
}
fn event_ref(raw: &[u8], sequence: i128, store: &str) -> V {
    let mut r = o(&node(raw)).clone();
    r.insert("storeInstanceId".into(), s(store));
    r.insert("sequence".into(), int(sequence));
    V::Object(r)
}
fn doc_ref(body: &[u8], envelope: &[u8]) -> V {
    obj([("body", node(body)), ("envelope", node(envelope))])
}
fn canonical_text(text: &str) -> Vec<u8> {
    canonical_bytes(&opensip_identity::parse_json(text.as_bytes()).unwrap()).unwrap()
}
fn blank_role() -> V {
    obj([
        ("state", s("ST-UNBOOTSTRAPPED")),
        ("accepted", V::Null),
        (
            "conditionEvidence",
            obj([("revokedBy", V::Null), ("quorumLostBy", V::Null)]),
        ),
        ("reset", V::Null),
        ("ceremony", V::Null),
    ])
}

struct Builder {
    files: Vec<File>,
    store: String,
}
impl Builder {
    fn record(&mut self, definition: Definition, value: &V) -> V {
        let raw = encode(definition, value);
        let r = node(&raw);
        self.files.push(File {
            path: format!("trust/records/{}", digest_hex(&raw_sha256(&raw))),
            collection: Some(Collection::Records),
            bytes: raw,
        });
        r
    }
    /// X4T-a3: a record written WITHOUT its closed-shape check, only for
    /// `ChainEnd::Empty`, whose refusal is the shape's.
    fn unshaped_record(&mut self, value: &V) -> V {
        let raw = canonical_bytes(value).unwrap();
        let r = node(&raw);
        self.files.push(File {
            path: format!("trust/records/{}", digest_hex(&raw_sha256(&raw))),
            collection: Some(Collection::Records),
            bytes: raw,
        });
        r
    }
    fn object(&mut self, raw: Vec<u8>) {
        self.files.push(File {
            path: format!("trust/objects/{}", digest_hex(&raw_sha256(&raw))),
            collection: Some(Collection::Objects),
            bytes: raw,
        });
    }
    fn event(&mut self, value: &V, sequence: i128) -> V {
        let raw = encode(Definition::TrustEventV1, value);
        let r = event_ref(&raw, sequence, &self.store);
        self.files.push(File {
            path: format!(
                "trust/stores/{}/events/{sequence}-{}",
                self.store,
                digest_hex(&raw_sha256(&raw))
            ),
            collection: Some(Collection::Events),
            bytes: raw,
        });
        r
    }
}

/// Generate a signed accepted store: P0 (revision 1) from the product
/// producer, then one retained publication (revision 2) that accepts the
/// chosen roles: X4B's producer's wherever it reaches them (X4B-c), this
/// module's construction otherwise.
pub(crate) fn generate(spec: &Spec) -> AcceptedStore {
    generate_with_calendar(spec, None)
}

// F9: explicit owned test dates. These reproduce the legacy calendar's
// relative offsets; they do not change production trust/freshness policy.
struct FixtureCalendar {
    issued: String,
    accepted: String,
    root_expires: String,
    catalog_expires: String,
    expired: String,
    stale: String,
}
impl FixtureCalendar {
    fn at(accepted_seconds: i64) -> Self {
        let issued = accepted_seconds
            .checked_sub(86_400)
            .expect("fixture issue time");
        let format =
            |seconds| crate::trust_time::format_timestamp(seconds).expect("fixture calendar");
        Self {
            issued: format(issued),
            accepted: format(accepted_seconds),
            root_expires: format(
                issued
                    .checked_add(365 * 86_400)
                    .expect("fixture root horizon"),
            ),
            catalog_expires: format(
                issued
                    .checked_add(182 * 86_400)
                    .expect("fixture catalog horizon"),
            ),
            expired: format(issued.checked_add(43_200).expect("fixture expired time")),
            stale: format(issued.checked_sub(92 * 86_400).expect("fixture stale time")),
        }
    }
}

/// F9 test-only signed store for an explicit clock instant, not a production
/// issuer or trusted clock constructor. Caller chooses native or scripted time.
/// Every dated source document is signed before retained records are computed.
pub(crate) fn generate_at(spec: &Spec, accepted_seconds: i64) -> AcceptedStore {
    let calendar = FixtureCalendar::at(accepted_seconds);
    generate_with_calendar(spec, Some(&calendar))
}

fn generate_with_calendar(spec: &Spec, calendar: Option<&FixtureCalendar>) -> AcceptedStore {
    assert!(
        spec.roles.iter().any(|r| *r != RoleTarget::Unbootstrapped),
        "a retained capsule needs accepted role history"
    );
    assert!(spec.roots >= 1, "a recorded chain has a root");
    assert!(
        spec.chain_end != ChainEnd::Short || spec.roots >= 2,
        "a short chain needs two roots"
    );
    #[cfg(target_os = "macos")]
    if let Some(store) = produce(spec, calendar) {
        return store;
    }
    construct(spec, calendar)
}

/// P0's files (the marker record, creation input, operation, event,
/// descriptor and capsule) in the producer's order, its capsule's bytes and
/// value, its store binding and its event head.
struct P0 {
    files: Vec<File>,
    capsule_raw: Vec<u8>,
    capsule: V,
    store: V,
    head: V,
}
fn p0_publication(spec: &Spec, sid: &str, calendar: Option<&FixtureCalendar>) -> P0 {
    let mut files = Vec::new();
    let inputs = super::initial_publication::Inputs {
        store: sid,
        state_schema: spec.state_schema,
        core_closure: CORE_CLOSURE,
        platform: "macos-aarch64",
        staging_name: "dddddddddddddddddddddddddddddddd",
        boot_id: "boot-1",
        mono: 5,
        wall: calendar.map(|c| c.issued.as_str()).unwrap_or(ISSUED),
        request_id: "req1_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        step_id: 0,
        execution_id: "exec1_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    };
    let mut ledger = opensip_platform::WorkLedger::new();
    let p0 = ledger
        .scope(|work| super::initial_publication::build(&inputs, work))
        .unwrap();
    let mut p0_capsule_raw = Vec::new();
    let mut p0_event_raw = Vec::new();
    for file in p0.files {
        let path = file.path.join("/");
        let collection = match file.path.get(1).map(String::as_str) {
            Some("records") => Some(Collection::Records),
            Some("objects") => Some(Collection::Objects),
            Some("publications") => Some(Collection::Publications),
            Some("stores") if file.path.get(3).map(String::as_str) == Some("events") => {
                p0_event_raw = file.bytes.clone();
                Some(Collection::Events)
            }
            _ => None,
        };
        if path.ends_with("/state.v1") {
            p0_capsule_raw = file.bytes.clone();
        }
        files.push(File {
            path,
            collection,
            bytes: file.bytes,
        });
    }
    let capsule = opensip_identity::parse_json(&p0_capsule_raw).unwrap();
    let store = o(&capsule)["store"].clone();
    let head = event_ref(&p0_event_raw, 1, sid);
    assert_eq!(o(&capsule)["eventHead"], head);
    P0 {
        files,
        capsule_raw: p0_capsule_raw,
        capsule,
        store,
        head,
    }
}

/// A stored body and its envelope.
type SignedPair = (Vec<u8>, Vec<u8>);

/// The recorded root chain, signed with the public test-only seeds
/// (quorum-roots.json schema 1): root 1 is quorum root 1; each later root
/// rotates ROOT to the next key set, signed by both (X4T-a3). The last root
/// is the signing root M. X4B-c: `final_expires` replaces M's `expiresAt`.
fn signed_chain(
    spec: &Spec,
    final_expires: Option<&str>,
    calendar: Option<&FixtureCalendar>,
) -> (Vec<V>, Vec<SignedPair>) {
    let mut first = quorum_root(1);
    if let Some(c) = calendar {
        let V::Object(root) = &mut first else {
            panic!("public fixture root");
        };
        root.insert("issuedAt".into(), s(&c.issued));
        root.insert("expiresAt".into(), s(&c.root_expires));
    }
    let key_id = |i: usize| match &o(&first)["keys"] {
        V::Array(keys) => o(&keys[i])["keyId"].clone(),
        _ => panic!("keys"),
    };
    let n = spec.roots;
    let mut chain: Vec<V> = (0..n)
        .map(|k| {
            if k == 0 {
                return first.clone();
            }
            let mut r = o(&first).clone();
            r.insert("rootVersion".into(), int(k as i128 + 1));
            r.insert("previousRootVersion".into(), int(k as i128));
            r.insert(
                "rootKeys".into(),
                V::Array(root_keys(k).iter().map(|&i| key_id(i)).collect()),
            );
            V::Object(r)
        })
        .collect();
    if let Some(expires) = final_expires {
        let mut r = o(&chain[n - 1]).clone();
        r.insert("expiresAt".into(), s(expires));
        chain[n - 1] = V::Object(r);
    }
    let mut chain_pairs = Vec::new();
    for (k, root_k) in chain.iter().enumerate() {
        let body = canonical_bytes(root_k).unwrap();
        let default: Vec<usize> = if k == 0 {
            root_keys(0).to_vec()
        } else {
            [root_keys(k - 1), root_keys(k)].concat()
        };
        let by = spec
            .root_signers
            .iter()
            .find(|(i, _)| *i == k)
            .map_or(default, |(_, by)| by.to_vec());
        let envelope = sign(
            &body,
            "root",
            "opensip.metadata.root.1",
            "ROOT",
            &first,
            &by,
        );
        chain_pairs.push((body, envelope));
    }
    (chain, chain_pairs)
}

/// This module's own construction of the retained publication (X4T-0), for
/// the stores X4B's producer cannot reach (X4B-c).
fn construct(spec: &Spec, calendar: Option<&FixtureCalendar>) -> AcceptedStore {
    let issued = calendar.map(|c| c.issued.as_str()).unwrap_or(ISSUED);
    let accepted = calendar.map(|c| c.accepted.as_str()).unwrap_or(ACCEPTED);
    let sid = spec.store.clone().unwrap_or_else(|| STORE.to_owned());
    let P0 {
        files,
        capsule_raw: p0_capsule_raw,
        capsule: p0_capsule,
        store,
        head: p0_head,
    } = p0_publication(spec, &sid, calendar);
    let mut b = Builder {
        files,
        store: sid.clone(),
    };
    // The P0 capsule image is also a record, so the time evidence can cite it.
    b.files.push(File {
        path: format!("trust/records/{}", digest_hex(&raw_sha256(&p0_capsule_raw))),
        collection: Some(Collection::Records),
        bytes: p0_capsule_raw.clone(),
    });
    let previous = digest_hex(&raw_sha256(&p0_capsule_raw));

    // Signed documents, public test-only seeds (quorum-roots.json schema 1).
    let n = spec.roots;
    let (chain, chain_pairs) = signed_chain(spec, spec.root_expires, calendar);
    let root = chain[n - 1].clone();
    let (root_body, root_env) = chain_pairs[n - 1].clone();
    let catalog_expires = spec.catalog_expires.unwrap_or_else(|| {
        calendar
            .map(|c| c.catalog_expires.as_str())
            .unwrap_or(CATALOG_EXPIRES)
    });
    let manifest_issued = spec.manifest_issued.unwrap_or(issued);
    // The acceptance's tEval and L: its wall, or a later manifest's issue time.
    let accepted_at = manifest_issued.max(accepted);
    let root_version = n as i128;
    let entries: Vec<String> = spec
        .revocations
        .iter()
        .map(|(kind, subject)| {
            format!(
                r#"{{"reason":"superseded","revokedAt":"{issued}","subject":"{subject}","subjectKind":"{kind}"}}"#
            )
        })
        .collect();
    let revocation = canonical_text(&format!(
        r#"{{"entries":[{}],"issuedAt":"{issued}","revocationSchema":1,"revocationVersion":{},"rootVersion":{root_version}}}"#,
        entries.join(","),
        spec.revocation_version
    ));
    // Law X4T r11 item 4: the list is signed under the signing root M.
    let revocation_env = sign(
        &revocation,
        "revocation",
        "opensip.metadata.revocation.1",
        "ROOT",
        &root,
        spec.revocation_signers.unwrap_or(&root_keys(n - 1)[..2]),
    );
    let catalog = canonical_text(&format!(
        r#"{{"catalogSchema":1,"expiresAt":"{catalog_expires}","issuedAt":"{issued}","releases":[],"reservedRootCommands":[],"revocationVersionRequired":1,"rootVersionRequired":{root_version},"snapshotVersion":1}}"#,
    ));
    let catalog_env = sign(
        &catalog,
        "catalog",
        "opensip.metadata.catalog.1",
        "TR-INDEX",
        &root,
        &[11, 12],
    );
    let member = |p: &str, raw: &[u8]| {
        format!(
            r#"{{"path":"{p}","sha256":"{}"}}"#,
            digest_hex(&raw_sha256(raw))
        )
    };
    // Envelopes sorted by path; the root chain in chain order.
    let mut envelopes = vec![
        member("catalog.sig.json", &catalog_env),
        member("revocation.sig.json", &revocation_env),
    ];
    let mut root_members = Vec::new();
    for (k, (body, envelope)) in chain_pairs.iter().enumerate() {
        envelopes.push(member(&format!("root-{k}.sig.json"), envelope));
        root_members.push(member(&format!("root-{k}.json"), body));
    }
    let manifest = canonical_text(&format!(
        r#"{{"issuedAt":"{manifest_issued}","members":{{"artifacts":[],"catalog":{},"envelopes":[{}],"manifests":[],"permissionPolicies":[],"repairMaterial":{{"ridesOn":"DR-110","standing":"absent-by-typed-absence"}},"revocation":{},"rootChain":[{}]}},"payloadKind":"ordinary","payloadSchema":1}}"#,
        member("catalog.json", &catalog),
        envelopes.join(","),
        member("revocation.json", &revocation),
        root_members.join(","),
    ));
    let manifest_env = sign(
        &manifest,
        "payload",
        "opensip.metadata.payload.1",
        "TR-BUNDLE",
        &root,
        &[17, 18],
    );
    let root_doc = doc_ref(&root_body, &root_env);
    let revocation_doc = doc_ref(&revocation, &revocation_env);
    let catalog_doc = doc_ref(&catalog, &catalog_env);
    let manifest_doc = doc_ref(&manifest, &manifest_env);
    let mut root_chain: Vec<V> = chain_pairs
        .iter()
        .map(|(body, envelope)| doc_ref(body, envelope))
        .collect();
    match spec.chain_end {
        ChainEnd::Head => {}
        ChainEnd::OtherEnvelope => {
            let other = sign(
                &root_body,
                "root",
                "opensip.metadata.root.1",
                "ROOT",
                &root,
                &root_keys(n - 1)[..2],
            );
            assert_ne!(other, root_env);
            *root_chain.last_mut().unwrap() = doc_ref(&root_body, &other);
            b.object(other);
        }
        ChainEnd::Short => {
            root_chain.pop();
        }
        ChainEnd::Empty => root_chain.clear(),
    }
    for (body, envelope) in &chain_pairs[..n - 1] {
        b.object(body.clone());
        b.object(envelope.clone());
    }
    for raw in [
        &root_body,
        &root_env,
        &revocation,
        &revocation_env,
        &catalog,
        &catalog_env,
        &manifest,
        &manifest_env,
    ] {
        b.object(raw.clone());
    }
    let validated = super::admit(&root, [true, true]).unwrap();
    let binding = obj([
        ("rootSchema", int(1)),
        ("rootVersion", int(root_version)),
        ("rootDigest", s(&digest_hex(&validated.digest()))),
    ]);

    // The payload metadata closure, the operation, the time evidence.
    let closure_value = obj([
        ("closureSchema", int(1)),
        ("scope", s("ordinary-inert")),
        ("manifest", manifest_doc),
        ("rootChain", V::Array(root_chain)),
        ("catalog", catalog_doc.clone()),
        ("revocation", revocation_doc.clone()),
        // X4T-a: the retained inventory binds each manifest envelope
        // slot to its stored blob, sorted by (slot, path).
        (
            "members",
            V::Array(
                [
                    ("catalog.sig.json".to_owned(), &catalog_env),
                    ("revocation.sig.json".to_owned(), &revocation_env),
                ]
                .into_iter()
                .chain(
                    chain_pairs
                        .iter()
                        .enumerate()
                        .map(|(k, (_, envelope))| (format!("root-{k}.sig.json"), envelope)),
                )
                .map(|(path, raw)| {
                    obj([
                        ("slot", s("envelopes")),
                        ("path", s(&path)),
                        ("blob", node(raw)),
                    ])
                })
                .collect(),
            ),
        ),
        ("artifactObservations", V::Array(vec![])),
        (
            "repairMaterial",
            obj([
                ("standing", s("absent-by-typed-absence")),
                ("ridesOn", s("DR-110")),
            ]),
        ),
    ]);
    let closure = if spec.chain_end == ChainEnd::Empty {
        b.unshaped_record(&closure_value)
    } else {
        b.record(Definition::PayloadMetadataClosureV1, &closure_value)
    };
    let invocation = invocation();
    let operation = b.record(
        Definition::OperationInputV1,
        &obj([
            ("operationSchema", int(1)),
            ("invocation", invocation.clone()),
            ("store", store.clone()),
            ("action", s("bootstrap")),
            (
                "input",
                obj([
                    ("kind", s("payload-metadata-closure")),
                    ("ref", closure.clone()),
                ]),
            ),
        ]),
    );
    let anchor = anchor(calendar);
    let source = obj([("kind", s("ordinary")), ("closure", closure.clone())]);
    encode(Definition::SignedTimeSourceV1, &source);
    let time = b.record(
        Definition::TimeEvidenceV1,
        &obj([
            ("inputSchema", int(1)),
            ("invocation", invocation),
            ("store", store.clone()),
            ("beforeImage", node(&p0_capsule_raw)),
            ("kind", s("s4-evaluation")),
            ("beforeClock", obj([("phase", s("unevaluated"))])),
            ("observation", anchor.clone()),
            ("source", source),
        ]),
    );

    // Admission records and the revocation history.
    let context = obj([
        ("time", time.clone()),
        ("priorRevocationHistory", V::Null),
        ("incomingRevocation", revocation_doc.clone()),
    ]);
    let root_admission = b.record(
        Definition::RootAdmissionNodeV1,
        &obj([
            ("admissionSchema", int(1)),
            ("kind", s("ordinary")),
            ("parent", closure.clone()),
            ("root", root_doc.clone()),
            ("binding", binding.clone()),
            ("context", context.clone()),
        ]),
    );
    let metadata_admission = |b: &mut Builder, kind: &str, document: &V| {
        b.record(
            Definition::MetadataAdmissionNodeV1,
            &obj([
                ("admissionSchema", int(1)),
                ("kind", s(kind)),
                ("document", document.clone()),
                ("admittingRoot", root_admission.clone()),
                ("closure", closure.clone()),
                ("context", context.clone()),
            ]),
        )
    };
    let catalog_admission = metadata_admission(&mut b, "catalog", &catalog_doc);
    let revocation_admission = metadata_admission(&mut b, "revocation", &revocation_doc);
    let history = b.record(
        Definition::RevocationHistoryNodeV1,
        &obj([
            ("historySchema", int(1)),
            ("kind", s("list")),
            ("list", revocation_doc.clone()),
            ("admittingRoot", root_admission.clone()),
            ("prior", V::Null),
        ]),
    );

    // Events: the S4 clock write (seq 2), then each role's acceptance and,
    // for a non-trusted target, its one conditioning event.
    let clock_write = b.event(
        &obj([
            ("eventSchema", int(1)),
            ("store", s(&sid)),
            ("sequence", int(2)),
            ("previous", p0_head.clone()),
            ("operation", operation.clone()),
            ("kind", s("clock-write")),
            ("source", s("s4")),
            ("evaluation", time.clone()),
            (
                "writes",
                V::Array(vec![s("anchor"), s("evalHighWater"), s("lastAccepted")]),
            ),
            ("phaseBefore", s("unevaluated")),
            ("phaseAfter", s("evaluated")),
            (
                "timeEvidence",
                obj([("kind", s("new")), ("proof", time.clone())]),
            ),
        ]),
        2,
    );
    let mut head = clock_write.clone();
    let mut sequence = 2;
    let mut roles: BTreeMap<String, V> =
        ROLES.iter().map(|r| ((*r).into(), blank_role())).collect();
    let mut events = vec![obj([
        ("event", clock_write.clone()),
        ("roleChange", V::Null),
    ])];
    let mut role_event = |b: &mut Builder,
                          roles: &mut BTreeMap<String, V>,
                          role: &str,
                          event: &str,
                          to: RoleTarget,
                          after: &dyn Fn(&V, &V) -> V|
     -> V {
        sequence += 1;
        let before = roles[role].clone();
        let from = o(&before)["state"].clone();
        let reference = b.event(
            &obj([
                ("eventSchema", int(1)),
                ("store", s(&sid)),
                ("sequence", int(sequence)),
                ("previous", head.clone()),
                ("operation", operation.clone()),
                ("kind", s("role-event")),
                ("role", s(role)),
                ("event", s(event)),
                ("from", from),
                ("to", s(to.token())),
                ("before", before.clone()),
                (
                    "payloadEvidence",
                    obj([("kind", s("closure")), ("ref", closure.clone())]),
                ),
                (
                    "clock",
                    obj([("kind", s("clock-write")), ("by", clock_write.clone())]),
                ),
                ("outcome", s("accepted")),
            ]),
            sequence,
        );
        let after = after(&before, &reference);
        let change = obj([
            ("role", s(role)),
            ("before", before),
            ("after", after.clone()),
        ]);
        encode(Definition::RoleChangeV1, &change);
        let row = obj([("event", reference.clone()), ("roleChange", change)]);
        encode(Definition::PublicationEventV1, &row);
        events.push(row);
        roles.insert(role.into(), after);
        head = reference.clone();
        reference
    };
    let namespaces = |role: &str| -> V {
        let roles = o(&o(&root)["roles"]);
        roles
            .get(role)
            .map_or(V::Array(vec![]), |d| o(d)["namespaces"].clone())
    };
    for (role, target) in ROLES.iter().zip(spec.roles) {
        if target == RoleTarget::Unbootstrapped {
            continue;
        }
        let standing = |by: &V| {
            obj([
                ("root", binding.clone()),
                ("rootAdmission", root_admission.clone()),
                ("namespaces", namespaces(role)),
                (
                    "catalog",
                    if *role == "TR-INDEX" {
                        catalog_doc.clone()
                    } else {
                        V::Null
                    },
                ),
                ("by", by.clone()),
            ])
        };
        role_event(
            &mut b,
            &mut roles,
            role,
            "EV-PRESENT-PAYLOAD",
            RoleTarget::Trusted,
            &|before, by| {
                let mut r = o(before).clone();
                r.insert("state".into(), s("ST-TRUSTED"));
                r.insert("accepted".into(), standing(by));
                V::Object(r)
            },
        );
        let (event, slot) = match target {
            RoleTarget::Trusted | RoleTarget::Unbootstrapped => continue,
            RoleTarget::Expired | RoleTarget::StaleRevocation => ("EV-CLOCK", None),
            RoleTarget::QuorumLost => ("EV-QUORUM-OBSERVE", Some("quorumLostBy")),
            RoleTarget::Revoked => ("EV-REVOKE", Some("revokedBy")),
        };
        role_event(&mut b, &mut roles, role, event, target, &|before, by| {
            let mut r = o(before).clone();
            r.insert("state".into(), s(target.token()));
            if let Some(slot) = slot {
                let mut c = o(&r["conditionEvidence"]).clone();
                c.insert(slot.into(), by.clone());
                r.insert("conditionEvidence".into(), V::Object(c));
            }
            V::Object(r)
        });
    }

    // The retained capsule and its publication descriptor.
    let head_doc = |version: Option<i128>, document: &V, admission: &V| {
        let mut h = BTreeMap::new();
        if let Some(v) = version {
            h.insert("version".into(), int(v));
        } else {
            h.insert("binding".into(), binding.clone());
        }
        h.insert("document".into(), document.clone());
        h.insert("admission".into(), admission.clone());
        V::Object(h)
    };
    let projection = obj([
        ("capsuleSchema", int(1)),
        ("store", store.clone()),
        ("revision", int(2)),
        ("previous", s(&previous)),
        (
            "clock",
            obj([
                ("phase", s("retained")),
                (
                    "record",
                    obj([
                        ("evalHighWater", s(accepted_at)),
                        ("lastAccepted", s(accepted_at)),
                        ("anchor", anchor),
                        ("rootVersion", int(root_version)),
                        ("indexSnapshotVersion", int(1)),
                        ("revocationVersion", int(spec.revocation_version)),
                        ("recoveryEpochSerial", int(0)),
                        ("pendingRecoveryChallenge", V::Null),
                        ("revocationIssuedAt", s(issued)),
                        ("catalogExpiresAt", s(catalog_expires)),
                        ("rootExpiresAt", o(&root)["expiresAt"].clone()),
                    ]),
                ),
                ("timeEvidence", time.clone()),
            ]),
        ),
        (
            "heads",
            obj([
                ("root", head_doc(None, &root_doc, &root_admission)),
                (
                    "catalog",
                    head_doc(Some(1), &catalog_doc, &catalog_admission),
                ),
                (
                    "revocation",
                    head_doc(
                        Some(spec.revocation_version),
                        &revocation_doc,
                        &revocation_admission,
                    ),
                ),
            ]),
        ),
        ("roles", V::Object(roles)),
        ("staged", V::Null),
        ("batch", V::Null),
        ("history", history),
        ("eventHead", head.clone()),
        ("sourceFence", V::Null),
    ]);
    let descriptor = obj([
        ("publicationSchema", int(1)),
        ("store", store.clone()),
        ("revision", int(2)),
        ("previousCapsule", s(&previous)),
        (
            "nativeBefore",
            obj([("revision", int(1)), ("sha256", s(&previous))]),
        ),
        ("operation", operation),
        ("events", V::Array(events)),
        ("afterProjection", projection.clone()),
    ]);
    let descriptor_raw = encode(Definition::PublicationDescriptorV1, &descriptor);
    let descriptor_ref = node(&descriptor_raw);
    let mut capsule = o(&projection).clone();
    capsule.insert(
        "publication".into(),
        obj([
            ("previousCapsule", s(&previous)),
            ("sha256", o(&descriptor_ref)["sha256"].clone()),
            ("bytes", o(&descriptor_ref)["bytes"].clone()),
        ]),
    );
    let capsule = V::Object(capsule);
    let capsule_raw = encode(Definition::TrustCapsuleV1, &capsule);
    b.files.push(File {
        path: format!(
            "trust/publications/by-predecessor/{previous}/{}",
            digest_hex(&raw_sha256(&descriptor_raw))
        ),
        collection: Some(Collection::Publications),
        bytes: descriptor_raw,
    });
    // The retained capsule replaces P0's current record.
    let current = format!("trust/stores/{sid}/state.v1");
    b.files.retain(|f| f.path != current);
    b.files.push(File {
        path: current,
        collection: None,
        bytes: capsule_raw,
    });
    AcceptedStore {
        files: b.files,
        store,
        capsule,
        descriptor,
        p0_capsule,
        root,
        root_body,
        produced: false,
    }
}

/// The acceptance's invocation (its operation input and time evidence).
fn invocation() -> V {
    obj([
        ("requestId", s("req1_cccccccccccccccccccccccccccccccc")),
        ("stepId", int(0)),
        ("executionId", s("exec1_dddddddddddddddddddddddddddddddd")),
    ])
}
/// The acceptance's one clock sample (W, M, B): the anchor it records.
fn anchor(calendar: Option<&FixtureCalendar>) -> V {
    obj([
        ("bootId", s("boot-1")),
        ("mono", int(7)),
        (
            "wall",
            s(calendar.map(|c| c.accepted.as_str()).unwrap_or(ACCEPTED)),
        ),
    ])
}

/// X4B-c: what the signed payload carries so that law X4B r5 item 4's
/// sequences end each carried role in its requested state. Index order is
/// `ROLES`' first four: TR-BUNDLE, TR-COMPONENT, TR-CORE, TR-INDEX.
#[cfg(target_os = "macos")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Knobs {
    /// The signing root expired at tEval: every carried role's `expired`.
    root_expired: bool,
    /// The catalog expired at tEval: TR-INDEX's `expired`.
    catalog_expired: bool,
    /// The list's revocation data stale at tEval.
    stale: bool,
    /// The list names one signer of that role's document by keyId, and
    /// the document's two other signers still meet its threshold.
    revoked: [bool; 4],
    /// A component manifest is carried (TR-COMPONENT leaves Unbootstrapped).
    component: bool,
}
#[cfg(target_os = "macos")]
impl Knobs {
    /// The quorum62 seeds that sign each carried role's documents; the third
    /// is the one a revoked role's list names.
    const SIGNERS: [[usize; 3]; 4] = [[17, 18, 19], [14, 15, 16], [8, 9, 10], [11, 12, 13]];
    /// The first knobs, time inputs in the order (root, catalog, stale) as
    /// a binary count, under which `role_machine::bootstrap_sequence` (the
    /// producer's own item 4 dispatch) ends every carried role in its
    /// requested state; `None` where no acceptance reaches the request.
    fn for_roles(roles: &[RoleTarget; 6]) -> Option<Self> {
        use crate::trust::role_machine::{BootstrapEntry, State, bootstrap_sequence};
        // TR-PROFILE and TR-REPAIR are never carried; every payload carries
        // the bootstrap manifest, the core inventory and the catalog.
        if roles[4] != RoleTarget::Unbootstrapped || roles[5] != RoleTarget::Unbootstrapped {
            return None;
        }
        if [0, 2, 3]
            .iter()
            .any(|&i| roles[i] == RoleTarget::Unbootstrapped)
        {
            return None;
        }
        let component = roles[1] != RoleTarget::Unbootstrapped;
        let revoked = [0, 1, 2, 3].map(|i| roles[i] == RoleTarget::Revoked);
        let token = |state: State| -> Option<RoleTarget> {
            Some(match state {
                State::Unbootstrapped => RoleTarget::Unbootstrapped,
                State::Trusted => RoleTarget::Trusted,
                State::Expired => RoleTarget::Expired,
                State::StaleRevocation => RoleTarget::StaleRevocation,
                State::QuorumLost => RoleTarget::QuorumLost,
                State::Revoked => RoleTarget::Revoked,
                State::Recovery => return None,
            })
        };
        (0u8..8).find_map(|bits| {
            let knobs = Self {
                root_expired: bits & 4 != 0,
                catalog_expired: bits & 2 != 0,
                stale: bits & 1 != 0,
                revoked,
                component,
            };
            let reached = (0..4).filter(|&i| i != 1 || component).all(|i| {
                let expired = knobs.root_expired || (i == 3 && knobs.catalog_expired);
                let sequence = bootstrap_sequence(
                    BootstrapEntry::Admissible,
                    expired,
                    knobs.stale,
                    revoked[i],
                );
                sequence.last().and_then(|(_, state)| token(*state)) == Some(roles[i])
            });
            reached.then_some(knobs)
        })
    }
}

/// X4B-c (law X4B r5 item 9): the accepted store through X4B's producer.
/// The payload is signed with the public test-only seeds as the knobs
/// require; P0 is 467's producer's; every retained-phase record, the
/// descriptor and `state.v1` are `build_over_p0`'s, placed where `publish`
/// writes them. `None` (the caller constructs) when the spec is not a
/// lawful store, no knobs reach its roles, or the producer refuses or ends
/// a role elsewhere (a caller's own list entry revoking a carried document).
#[cfg(target_os = "macos")]
fn produce(spec: &Spec, calendar: Option<&FixtureCalendar>) -> Option<AcceptedStore> {
    let normal_issued = calendar.map(|c| c.issued.as_str()).unwrap_or(ISSUED);
    use super::core_authentication::tests::{component_body, component_release, key};
    use super::ordinary_targets::current_trust_admission::trust_bootstrap::{
        BootstrapPayload, build_over_p0,
    };
    use opensip_platform::WorkFailure;
    if spec.chain_end != ChainEnd::Head
        || !spec.root_signers.is_empty()
        || spec.revocation_signers.is_some()
    {
        return None;
    }
    let knobs = Knobs::for_roles(&spec.roles)?;
    // Past at tEval (W is 2026-10-02), after every issue time.
    const EXPIRED: &str = "2026-10-01T12:00:00Z";
    let sid = spec.store.clone().unwrap_or_else(|| STORE.to_owned());
    let p0 = p0_publication(spec, &sid, calendar);
    let n = spec.roots;
    let (chain, chain_pairs) = signed_chain(
        spec,
        knobs
            .root_expired
            .then_some(calendar.map(|c| c.expired.as_str()).unwrap_or(EXPIRED))
            .or(spec.root_expires),
        calendar,
    );
    let root = chain[n - 1].clone();
    let root_version = n as i128;

    // The list: the caller's entries, then one signer of each revoked role.
    // Stale data is a list issued more than 90 days before tEval.
    let issued = if knobs.stale {
        calendar
            .map(|c| c.stale.as_str())
            .unwrap_or("2026-07-01T00:00:00Z")
    } else {
        normal_issued
    };
    let mut listed: Vec<(&str, String)> = spec
        .revocations
        .iter()
        .map(|(kind, subject)| (*kind, subject.clone()))
        .collect();
    for (role, revoked) in knobs.revoked.iter().enumerate() {
        if *revoked {
            listed.push(("keyId", digest_hex(&key(Knobs::SIGNERS[role][2]))));
        }
    }
    let entries: Vec<String> = listed
        .iter()
        .map(|(kind, subject)| {
            format!(
                r#"{{"reason":"superseded","revokedAt":"{issued}","subject":"{subject}","subjectKind":"{kind}"}}"#
            )
        })
        .collect();
    let revocation = canonical_text(&format!(
        r#"{{"entries":[{}],"issuedAt":"{issued}","revocationSchema":1,"revocationVersion":{},"rootVersion":{root_version}}}"#,
        entries.join(","),
        spec.revocation_version
    ));
    let revocation_env = sign(
        &revocation,
        "revocation",
        "opensip.metadata.revocation.1",
        "ROOT",
        &root,
        &root_keys(n - 1)[..2],
    );
    // One component manifest under TR-COMPONENT, joined by a catalog row.
    let component = knobs.component.then(|| {
        let body = component_body(0);
        let (envelope, release) =
            component_release(0, &body, ("TR-COMPONENT", &Knobs::SIGNERS[1]), &root);
        (body, envelope, release)
    });
    let catalog = canonical_text(&format!(
        r#"{{"catalogSchema":1,"expiresAt":"{}","issuedAt":"{normal_issued}","releases":[{}],"reservedRootCommands":[],"revocationVersionRequired":1,"rootVersionRequired":{root_version},"snapshotVersion":1}}"#,
        if knobs.catalog_expired {
            calendar.map(|c| c.expired.as_str()).unwrap_or(EXPIRED)
        } else {
            spec.catalog_expires.unwrap_or_else(|| {
                calendar
                    .map(|c| c.catalog_expires.as_str())
                    .unwrap_or(CATALOG_EXPIRES)
            })
        },
        component
            .as_ref()
            .map_or("", |(_, _, release)| release.as_str()),
    ));
    let catalog_env = sign(
        &catalog,
        "catalog",
        "opensip.metadata.catalog.1",
        "TR-INDEX",
        &root,
        &Knobs::SIGNERS[3],
    );
    let member = |p: &str, raw: &[u8]| {
        format!(
            r#"{{"path":"{p}","sha256":"{}"}}"#,
            digest_hex(&raw_sha256(raw))
        )
    };
    // Envelopes sorted by path; the root chain in chain order.
    let mut envelopes: BTreeMap<String, &[u8]> = BTreeMap::from([
        ("catalog.sig.json".to_owned(), catalog_env.as_slice()),
        ("revocation.sig.json".to_owned(), revocation_env.as_slice()),
    ]);
    let mut blobs = vec![
        revocation.clone(),
        revocation_env.clone(),
        catalog.clone(),
        catalog_env.clone(),
    ];
    let mut root_members = Vec::new();
    for (k, (body, envelope)) in chain_pairs.iter().enumerate() {
        envelopes.insert(format!("root-{k}.sig.json"), envelope);
        root_members.push(member(&format!("root-{k}.json"), body));
        blobs.extend([body.clone(), envelope.clone()]);
    }
    let mut manifests = Vec::new();
    if let Some((body, envelope, _)) = &component {
        envelopes.insert("component-0.sig.json".to_owned(), envelope);
        manifests.push(member("component-0.json", body));
        blobs.extend([body.clone(), envelope.clone()]);
    }
    let manifest = canonical_text(&format!(
        r#"{{"issuedAt":"{}","members":{{"artifacts":[],"catalog":{},"envelopes":[{}],"manifests":[{}],"permissionPolicies":[],"repairMaterial":{{"ridesOn":"DR-110","standing":"absent-by-typed-absence"}},"revocation":{},"rootChain":[{}]}},"payloadKind":"ordinary","payloadSchema":1}}"#,
        spec.manifest_issued.unwrap_or(normal_issued),
        member("catalog.json", &catalog),
        envelopes
            .iter()
            .map(|(p, raw)| member(p, raw))
            .collect::<Vec<_>>()
            .join(","),
        manifests.join(","),
        member("revocation.json", &revocation),
        root_members.join(","),
    ));
    let manifest_env = sign(
        &manifest,
        "payload",
        "opensip.metadata.payload.1",
        "TR-BUNDLE",
        &root,
        &Knobs::SIGNERS[0],
    );
    // The core inventory under TR-CORE, binding the embedded bootstrap pair.
    // The producer verifies its envelope and stores nothing of it; the
    // running core stays the synthetic `CORE_CLOSURE` P0 names.
    let bound = |p: &str, raw: &[u8]| {
        format!(
            r#"{{"bytes":{},"path":"trust/bootstrap/{p}","sha256":"{}"}}"#,
            raw.len(),
            digest_hex(&raw_sha256(raw))
        )
    };
    let inventory = canonical_text(&format!(
        r#"{{"embeddedBootstrap":{{"directory":"trust/bootstrap","envelope":{},"manifest":{}}},"inventorySchema":3}}"#,
        bound("payload.sig.json", &manifest_env),
        bound("payload.json", &manifest),
    ));
    let inventory_env = sign(
        &inventory,
        "inventory",
        "opensip.metadata.inventory.1",
        "TR-CORE",
        &root,
        &Knobs::SIGNERS[2],
    );
    // The embedded root binding names root 1.
    let anchor_root = super::admit(&chain[0], [true, true]).unwrap();
    let binding = obj([
        ("rootSchema", int(1)),
        ("rootVersion", int(1)),
        ("rootDigest", s(&digest_hex(&anchor_root.digest()))),
    ]);

    let acceptance = opensip_platform::WorkLedger::new()
        .scope(|work| {
            let payload = BootstrapPayload::from_parts(
                binding,
                (manifest, manifest_env),
                (inventory, inventory_env),
                CORE_CLOSURE,
                blobs,
                work,
            )
            .map_err(WorkFailure::Operation)?;
            build_over_p0(
                &p0.capsule,
                &p0.capsule_raw,
                &payload,
                &anchor(calendar),
                &invocation(),
                work,
            )
            .map_err(WorkFailure::Operation)
        })
        .ok()?;
    let capsule = opensip_identity::parse_json(acceptance.capsule_raw()).unwrap();
    if ROLES
        .iter()
        .zip(spec.roles)
        .any(|(role, target)| o(&o(&o(&capsule)["roles"])[*role])["state"] != s(target.token()))
    {
        return None;
    }
    let mut files = p0.files;
    let current = format!("trust/stores/{sid}/state.v1");
    files.retain(|f| f.path != current);
    let mut descriptor = None;
    for write in &acceptance.files {
        let path = write.path().unwrap().join("/");
        if write.collection() == Collection::Publications {
            descriptor = Some(opensip_identity::parse_json(write.bytes()).unwrap());
        }
        if files.iter().all(|f| f.path != path) {
            files.push(File {
                path,
                collection: Some(write.collection()),
                bytes: write.bytes().to_vec(),
            });
        }
    }
    files.push(File {
        path: current,
        collection: None,
        bytes: acceptance.capsule_raw().to_vec(),
    });
    Some(AcceptedStore {
        files,
        store: p0.store,
        capsule,
        descriptor: descriptor.expect("one publication"),
        p0_capsule: p0.capsule,
        root,
        root_body: chain_pairs[n - 1].0.clone(),
        produced: true,
    })
}

#[cfg(test)]
mod tests {
    include!("accepted_store_fixture_tests.rs");
}
