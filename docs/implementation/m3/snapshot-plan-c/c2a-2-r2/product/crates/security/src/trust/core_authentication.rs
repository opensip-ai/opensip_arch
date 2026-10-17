// Cryptographic successor links relative to the original embedded anchor.
// Independent original-core TCB and revocation completeness are NOT produced.
use super::admitted_revocations::{self as L, RevocationEvidence};
use super::core_anchor::{self as Core, CapturedCore, InventorySchema};
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
use super::retained_metadata_index::Collection;
use super::retained_metadata_index::{self as M, Budget};
use super::verified_root_chains::{self as Chains, RootChainAuthentication};
use super::*;
#[derive(Debug, PartialEq, Eq)]
pub(super) enum AuthenticationError {
    Budget(M::Error),
    Core(Core::BindingError),
    Root,
    Envelope,
    Chain(ChainError),
    Head,
}
impl From<M::Error> for AuthenticationError {
    fn from(e: M::Error) -> Self {
        Self::Budget(e)
    }
}
pub(super) struct EmbeddedAuthentication {
    core: CapturedCore,
    anchor: ValidatedRootPayload,
    chain: RootChainAuthentication,
    original_revoked: BTreeSet<[u8; 32]>,
}
impl EmbeddedAuthentication {
    pub(super) fn core(&self) -> &CapturedCore {
        &self.core
    }
    pub(super) fn anchor(&self) -> &ValidatedRootPayload {
        &self.anchor
    }
    pub(super) fn chain(&self) -> &RootChainAuthentication {
        &self.chain
    }
    pub(super) fn original_revoked(&self) -> &BTreeSet<[u8; 32]> {
        &self.original_revoked
    }
}
pub(super) fn authenticate(
    budget: &mut Budget,
    anchor_ref: &V,
    original_revoked: &BTreeSet<[u8; 32]>,
    store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
) -> Result<EmbeddedAuthentication, AuthenticationError> {
    authenticate_with(budget, anchor_ref, original_revoked, store, InventorySchema::V2)
}
fn authenticate_with(
    budget: &mut Budget,
    anchor_ref: &V,
    original_revoked: &BTreeSet<[u8; 32]>,
    store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
    schema: InventorySchema,
) -> Result<EmbeddedAuthentication, AuthenticationError> {
    budget.scope(|b| {
        let core = Core::capture_with(b, anchor_ref, store, schema)
            .map_err(AuthenticationError::Core)?;
        let first = &core.roots()[0];
        let body =
            super::super::metadata::parse(first.body()).map_err(|_| AuthenticationError::Root)?;
        let anchor = admit(&body, [true, true]).map_err(|_| AuthenticationError::Root)?;
        let envelopes: Vec<_> = core
            .roots()
            .iter()
            .skip(1)
            .map(|p| {
                super::super::metadata::parse(p.envelope())
                    .map_err(|_| AuthenticationError::Envelope)
            })
            .collect::<Result<_, _>>()?;
        let links: Vec<_> = core
            .roots()
            .iter()
            .skip(1)
            .zip(&envelopes)
            .map(|(p, e)| WireRootLink {
                stored: p.body(),
                envelope: e,
            })
            .collect();
        let chain = Chains::authenticate_root_chain(
            &anchor,
            &links,
            ChainAuthenticationContext {
                accepted_version: chain_root_number(&anchor, "rootVersion")
                    .map_err(AuthenticationError::Chain)?,
                revoked: original_revoked,
                readers: [true, true],
            },
            ChainBudget {
                max_links: 63,
                max_stored_bytes: 268435456,
            },
        )
        .map_err(AuthenticationError::Chain)?;
        let final_root = chain.links().last().map_or(&anchor, |link| link.root());
        if !verified_root_recovery::binding_matches(core.final_binding(), final_root) {
            return Err(AuthenticationError::Head);
        }
        Ok(EmbeddedAuthentication {
            core,
            anchor,
            chain,
            original_revoked: original_revoked.clone(),
        })
    })
}
#[derive(Debug, PartialEq, Eq)]
pub(super) enum ReleaseError {
    Authentication(AuthenticationError),
    RevocationMember(Core::BindingError),
    Revocation(RevocationError),
    KeySubject,
    Envelope(EnvelopeKind),
    Quorum(EnvelopeKind),
}
impl From<M::Error> for ReleaseError {
    fn from(e: M::Error) -> Self {
        Self::Authentication(AuthenticationError::Budget(e))
    }
}
pub(super) struct EmbeddedRelease {
    authentication: EmbeddedAuthentication,
    revocation: RevocationEvidence,
    revocation_quorum: QuorumReport,
    revoked: BTreeSet<[u8; 32]>,
    inventory: EnvelopeEvidence<QuorumReport>,
    manifest: EnvelopeEvidence<QuorumReport>,
}
impl EmbeddedRelease {
    pub(super) fn authentication(&self) -> &EmbeddedAuthentication {
        &self.authentication
    }
    pub(super) fn revocation(&self) -> &RevocationEvidence {
        &self.revocation
    }
    pub(super) fn revocation_quorum(&self) -> &QuorumReport {
        &self.revocation_quorum
    }
    pub(super) fn revoked(&self) -> &BTreeSet<[u8; 32]> {
        &self.revoked
    }
    pub(super) fn inventory(&self) -> &EnvelopeEvidence<QuorumReport> {
        &self.inventory
    }
    pub(super) fn manifest(&self) -> &EnvelopeEvidence<QuorumReport> {
        &self.manifest
    }
}
fn met(
    report: &QuorumReport,
    revoked: &BTreeSet<[u8; 32]>,
    kind: EnvelopeKind,
) -> Result<QuorumReport, ReleaseError> {
    let report = report.filtered_again(revoked);
    if report.state() != &QuorumState::Met {
        return Err(ReleaseError::Quorum(kind));
    }
    Ok(report)
}
// 463 r4 item 5: no caller revoked set. The chain is authenticated with an
// internal empty set, then the manifest's own revocation, verified under the
// final root, re-filters every link, itself, TR-CORE and TR-BUNDLE. Item 6:
// the inventory is `CoreInventoryV3`; V2 bytes refuse at its shape.
pub(super) fn authenticate_embedded_release(
    budget: &mut Budget,
    anchor_ref: &V,
    store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
) -> Result<EmbeddedRelease, ReleaseError> {
    budget.scope(|b| {
        let authentication = authenticate_with(
            b,
            anchor_ref,
            &BTreeSet::new(),
            store,
            InventorySchema::V3,
        )
        .map_err(ReleaseError::Authentication)?;
        let core = authentication.core();
        let chain = authentication.chain();
        let root = chain
            .links()
            .last()
            .map_or(authentication.anchor(), |link| link.root());
        let pair = Core::revocation(b, core, store).map_err(ReleaseError::RevocationMember)?;
        let env = super::super::metadata::parse(pair.envelope())
            .map_err(|_| ReleaseError::Envelope(EnvelopeKind::Revocation))?;
        let revocation = L::verify_revocation(root, pair.body(), &env, &BTreeSet::new())
            .map_err(ReleaseError::Revocation)?;
        let mut revoked = BTreeSet::new();
        for row in array(&object(revocation.envelope().payload()).unwrap()["entries"]).unwrap() {
            let row = object(row).unwrap();
            if string(&row["subjectKind"]) == Some("keyId") {
                revoked.insert(
                    decode_hex32(string(&row["subject"]).unwrap())
                        .map_err(|_| ReleaseError::KeySubject)?,
                );
            }
        }
        let mut signed = Vec::new();
        for (name, kind) in [
            ("coreInventory", EnvelopeKind::Inventory),
            ("bootstrapManifest", EnvelopeKind::Payload),
        ] {
            let (body, envelope) = &core.initial()[name];
            let env = super::super::metadata::parse(envelope)
                .map_err(|_| ReleaseError::Envelope(kind))?;
            let evidence =
                verify_envelope(CURRENT_ENVELOPE_READER, root, body, Some(&env), kind, None)
                    .map_err(|_| ReleaseError::Envelope(kind))?;
            signed.push(filter_envelope_revoked(evidence, &revoked));
        }
        for link in chain.links() {
            met(link.continuity(), &revoked, EnvelopeKind::Root)?;
            met(link.possession(), &revoked, EnvelopeKind::Root)?;
        }
        let revocation_quorum = met(
            revocation.envelope().quorum(),
            &revoked,
            EnvelopeKind::Revocation,
        )?;
        for evidence in &signed {
            met(evidence.quorum(), &revoked, evidence.kind())?;
        }
        let manifest = signed.pop().unwrap();
        let inventory = signed.pop().unwrap();
        Ok(EmbeddedRelease {
            authentication,
            revocation,
            revocation_quorum,
            revoked,
            inventory,
            manifest,
        })
    })
}
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub(super) mod tests {
    use super::*;
    use opensip_identity::{canonical_bytes, digest_hex};
    fn o(v: &V) -> &Object {
        object(v).unwrap()
    }
    fn a(v: &V) -> &[V] {
        array(v).unwrap()
    }
    fn s(v: &V) -> &str {
        string(v).unwrap()
    }
    fn count(v: &V) -> usize {
        integer(v).unwrap().try_into().unwrap()
    }
    fn bytes(v: &V) -> Vec<u8> {
        s(v).as_bytes()
            .chunks_exact(2)
            .map(|v| u8::from_str_radix(std::str::from_utf8(v).unwrap(), 16).unwrap())
            .collect()
    }
    fn collection(v: &V) -> Collection {
        match s(v) {
            "records" => Collection::Records,
            "objects" => Collection::Objects,
            _ => panic!("collection"),
        }
    }
    #[test]
    fn original_embedded_successor_signatures_match_primary_and_own_all_evidence() {
        let mut counts = (0, 0, 0);
        let mut owned = Vec::new();
        for line in include_bytes!("../../tests/fixtures/core-auth323.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let row = opensip_identity::parse_json(line).unwrap();
            let q = o(&row);
            let label = s(&q["label"]).to_owned();
            let l = a(&q["limits"]);
            let mut budget = Budget::new(count(&l[0]), count(&l[1]), count(&l[2])).unwrap();
            let revoked: BTreeSet<_> = a(&q["revoked"])
                .iter()
                .map(|v| decode_hex32(s(v)).unwrap())
                .collect();
            let files: BTreeMap<_, _> = a(&q["store"])
                .iter()
                .map(|v| {
                    let v = o(v);
                    (
                        (
                            collection(&v["collection"]),
                            decode_hex32(s(&v["sha256"])).unwrap(),
                        ),
                        bytes(&v["raw"]),
                    )
                })
                .collect();
            let mut reads = Vec::new();
            {
                let mut store = |c: Collection, h: [u8; 32], cap: usize| {
                    assert!((1..=4_194_304).contains(&cap));
                    reads.push((c, digest_hex(&h)));
                    files.get(&(c, h)).cloned().ok_or(())
                };
                for (i, expected) in a(&q["outcomes"]).iter().enumerate() {
                    let expected = o(expected);
                    let got = authenticate(&mut budget, &q["reference"], &revoked, &mut store);
                    assert_eq!(
                        got.is_ok(),
                        expected["ok"] == V::Bool(true),
                        "{label} round{i}: {:?}",
                        got.as_ref().err()
                    );
                    let c = a(&expected["counters"]);
                    assert_eq!(
                        budget.counters(),
                        (count(&c[0]), count(&c[1]), count(&c[2])),
                        "{label} round{i} counters"
                    );
                    if let Ok(got) = got {
                        owned.push((got, expected["expected"].clone(), label.clone()));
                        if i == 0 {
                            counts.1 += 1;
                        } else {
                            counts.2 += 1;
                        }
                    }
                }
                if q["failed"] == V::Bool(true) {
                    assert!(
                        matches!(
                            authenticate(&mut budget, &q["reference"], &revoked, &mut store),
                            Err(AuthenticationError::Budget(M::Error::Closed))
                        ),
                        "{label} failure latch"
                    );
                    assert_eq!(budget.edge(1), Err(M::Error::Closed));
                }
            }
            let expected: Vec<_> = a(&q["captures"])
                .iter()
                .map(|v| {
                    let v = a(v);
                    (collection(&v[0]), s(&v[1]).to_owned())
                })
                .collect();
            assert_eq!(reads, expected, "{label} captures");
            drop(files);
            drop(revoked);
            drop(budget);
            drop(row);
            counts.0 += 1;
        }
        for (got, expected, label) in owned {
            let e = o(&expected);
            let captured = o(&e["captured"]);
            assert_eq!(got.core().reference(), &captured["anchor"]);
            assert_eq!(got.core().anchor().raw(), bytes(&captured["anchorRaw"]));
            assert_eq!(got.core().root_chain(), a(&captured["rootChain"]));
            assert_eq!(got.core().final_binding(), &captured["finalBinding"]);
            assert_eq!(got.anchor().value(), &e["anchor"]);
            assert_eq!(
                got.chain().anchor_canonical(),
                canonical_bytes(&e["anchor"]).unwrap()
            );
            assert_eq!(
                digest_hex(&got.chain().anchor_digest()),
                s(&e["anchorDigest"])
            );
            assert_eq!(
                got.chain().accepted_version(),
                integer(&e["finalVersion"]).unwrap()
            );
            assert_eq!(got.chain().last_accepted_issued_at(), s(&e["finalIssued"]));
            assert_eq!(
                got.original_revoked()
                    .iter()
                    .map(|v| V::String(digest_hex(v)))
                    .collect::<Vec<_>>(),
                a(&e["originalRevoked"])
            );
            assert_eq!(got.chain().links().len(), a(&e["links"]).len());
            for (link, expected) in got.chain().links().iter().zip(a(&e["links"])) {
                let expected = o(expected);
                assert_eq!(
                    link.stored(),
                    bytes(&expected["body"]),
                    "{label} exact root bytes"
                );
                for (q, key) in [(link.continuity(), "old"), (link.possession(), "new")] {
                    let want = o(&expected[key]);
                    assert_eq!(q.state(), &QuorumState::Met);
                    assert_eq!(q.required(), count(&want["threshold"]));
                    assert_eq!(digest_hex(&q.message()), s(&want["message"]));
                    assert_eq!(
                        q.valid()
                            .iter()
                            .map(|v| V::String(digest_hex(v)))
                            .collect::<Vec<_>>(),
                        a(&want["signers"]),
                        "{label} {key} actual signers"
                    );
                }
            }
            let members = o(&captured["members"]);
            assert_eq!(got.core().members().len(), members.len());
            for (path, raw) in got.core().members() {
                assert_eq!(
                    raw.as_ref(),
                    bytes(&members[path]),
                    "{label} retained {path}"
                );
            }
        }
        assert_eq!(counts, (38, 13, 12));
    }
    // 463c: a synthetic release signed with the public test-only seeds of
    // quorum-roots.json. Root-1 moves ROOT to unused keys 20..22, so a
    // revocation of root-0 keys breaks only the link, not its own quorum.
    struct Release {
        store: BTreeMap<(Collection, [u8; 32]), Vec<u8>>,
        reference: V,
        revocation: [u8; 32],
    }
    fn hex(b: &[u8]) -> String {
        b.iter().map(|b| format!("{b:02x}")).collect()
    }
    fn doc(raw: &[u8]) -> String {
        format!(
            r#"{{"bytes":{},"sha256":"{}"}}"#,
            raw.len(),
            digest_hex(&opensip_identity::raw_sha256(raw))
        )
    }
    fn canonical(text: &str) -> Vec<u8> {
        canonical_bytes(&opensip_identity::parse_json(text.as_bytes()).unwrap()).unwrap()
    }
    pub(crate) fn sign(
        body: &[u8],
        kind: &str,
        domain: &str,
        role: &str,
        root: &V,
        by: &[usize],
    ) -> Vec<u8> {
        use ed25519_dalek::{Signer, SigningKey};
        let value = opensip_identity::parse_json(body).unwrap();
        let pin = crate::trust::metadata_digest_for_domain(domain, &value).unwrap();
        let subject = format!(
            r#"{{"domain":"{domain}","kind":"{kind}","preimageSha256":"{}","storedSha256":"{}"}}"#,
            digest_hex(&pin),
            digest_hex(&opensip_identity::raw_sha256(body))
        );
        let unsigned = format!(
            r#"{{"envelopeSchema":2,"namespace":"opensip","role":"{role}","signatures":[],"subject":{subject}}}"#
        );
        let message = crate::trust::envelope_message(
            &opensip_identity::parse_json(unsigned.as_bytes()).unwrap(),
        )
        .unwrap();
        let keys = a(&o(root)["keys"]);
        let signatures: Vec<_> = by
            .iter()
            .map(|&i| {
                let mut seed = b"opensip-public-test-only-quorum62-seed-".to_vec();
                seed.push(u8::try_from(i).unwrap());
                let key = SigningKey::from_bytes(&opensip_identity::raw_sha256(&seed));
                assert_eq!(
                    hex(&key.verifying_key().to_bytes()),
                    s(&o(&keys[i])["publicKey"])
                );
                format!(
                    r#"{{"alg":"ed25519","keyId":"{}","signature":"{}"}}"#,
                    s(&o(&keys[i])["keyId"]),
                    hex(&key.sign(&message).to_bytes())
                )
            })
            .collect();
        canonical(&format!(
            r#"{{"envelopeSchema":2,"namespace":"opensip","role":"{role}","signatures":[{}],"subject":{subject}}}"#,
            signatures.join(",")
        ))
    }
    fn seeded_root() -> V {
        quorum_root(1)
    }
    /// quorum-roots.json: "1" is schema 1; "2" is schema 2 with an active
    /// TR-PROFILE (keys 23..25). Both list the same 27 seeded keys.
    pub(crate) fn quorum_root(schema: u8) -> V {
        let roots =
            opensip_identity::parse_json(include_bytes!("../../tests/fixtures/quorum-roots.json"))
                .unwrap();
        o(&roots)[&schema.to_string()].clone()
    }
    pub(crate) fn key(i: usize) -> [u8; 32] {
        decode_hex32(s(&o(&a(&o(&seeded_root())["keys"])[i])["keyId"])).unwrap()
    }
    fn release(link: bool, revoke: &[usize], revocation_root: Option<i64>) -> Release {
        release_as(3, link, revoke, revocation_root)
    }
    fn release_as(schema: u8, link: bool, revoke: &[usize], revocation_root: Option<i64>) -> Release {
        let signed = signed_release(&Spec {
            schema,
            link,
            revoke,
            revocation_root,
            ..Spec::default()
        });
        let mut store: BTreeMap<_, _> = signed
            .bootstrap
            .into_values()
            .chain([signed.exe, signed.inventory, signed.inventory_env])
            .map(|raw| ((Collection::Objects, opensip_identity::raw_sha256(&raw)), raw))
            .collect();
        store.insert(
            (Collection::Records, opensip_identity::raw_sha256(&signed.record)),
            signed.record,
        );
        Release {
            store,
            reference: signed.reference,
            revocation: signed.revocation,
        }
    }
    /// The release a synthetic signed tree carries. Schema 3 rows carry
    /// `state_writer` and `flags` (sorted XNU names).
    pub(crate) struct Spec<'a> {
        pub(crate) schema: u8,
        pub(crate) link: bool,
        pub(crate) revoke: &'a [usize],
        pub(crate) revocation_root: Option<i64>,
        pub(crate) platform: &'a str,
        pub(crate) entrypoint: &'a str,
        pub(crate) bootstrap: &'a str,
        pub(crate) exe: &'a [u8],
        pub(crate) flags: &'a [&'a str],
        pub(crate) state_writer: i64,
        /// A second listed envelope over the index-0 root body (law 463 item 9).
        pub(crate) extra_envelope: bool,
        /// quorum-roots.json key: 1, or 2 (active TR-PROFILE; no link).
        pub(crate) root_schema: u8,
        /// `platformProfileSetBodyDigest`; None is 32 bytes of 0xaa.
        pub(crate) profile_pin: Option<[u8; 32]>,
        /// More `file` rows of the platform's tree, by path under the tree root.
        pub(crate) tree_files: &'a [(&'a str, &'a [u8])],
        /// Law 463 r9: one listed catalog envelope per (role, seed indices);
        /// empty lists none, as an r8 release.
        pub(crate) catalog_signers: &'a [Signer<'a>],
        /// One component manifest each, with its envelope's (role, seed
        /// indices), or listed without an envelope when None.
        pub(crate) component_signers: &'a [Option<Signer<'a>>],
        /// M3-C r8 item 8 (unit C2a-2): the component bodies, by index, in
        /// place of `component_body`; empty keeps every pre-existing byte.
        /// Each listed body's release row is `components::release`'s.
        pub(crate) components: &'a [Vec<u8>],
        /// Law X4B r5 tests (X4B-a): the catalog's expiry, the revocation
        /// list's issue time and the roots' expiry, so acceptance can see
        /// an expired or stale document at tEval.
        pub(crate) catalog_expires: &'a str,
        pub(crate) revocation_issued: &'a str,
        pub(crate) root_expires: Option<&'a str>,
    }
    /// An envelope's header role and the quorum62 seed indices that sign it.
    pub(crate) type Signer<'a> = (&'a str, &'a [usize]);
    /// The public test-only TR-INDEX and TR-COMPONENT signers (quorum62 seeds).
    pub(crate) const INDEX_SIGNER: Signer<'static> = ("TR-INDEX", &[11, 12]);
    pub(crate) const COMPONENT_SIGNER: Signer<'static> = ("TR-COMPONENT", &[14, 15]);
    /// manifest268-semantic's `POS/empty-capabilities` body; the builder
    /// varies its version per component.
    const COMPONENT_MANIFEST: &str = r#"{"manifestSchemaVersion":1,"kind":"component","stableId":"6f1c2c3e-0b6a-4a1c-9c2d-1f0e2a3b4c5d","name":"typescript-analyzer","version":"1.0.0","role":"analyzer","commands":[{"name":"typescript-analyzer","description":"mounted root command of the TypeScript analyzer"}],"capabilities":[],"platforms":[{"os":"macos","arch":"arm64","tree":{"entries":[{"path":"bin","type":"dir","mode":"0755"},{"path":"bin/entry","type":"file","mode":"0755","length":91,"sha256":"dc854be9643a241b32c74ddd9545db6d25250f2c2cef3cb0879593fb42e381a7"},{"path":"lib","type":"dir","mode":"0755"},{"path":"lib/provider.js","type":"file","mode":"0644","length":30,"sha256":"b2c3576b7dcca113508cd56860bb2a88df4ea720c8579b75a3bd0a934016e6c0"},{"path":"runtime","type":"dir","mode":"0755"},{"path":"runtime/node","type":"file","mode":"0755","length":33,"sha256":"d2189c7fce3766cf320a8d6490afae9dd4c52218b5f751e00292cd9f9903ef5d"}]},"entrypoint":"bin/entry"}],"dependencies":[],"declarations":{"licenses":{"path":"declarations/licenses.json","sha256":"7d04ba339da1a52d73801c402049983db204aba87cf52047fc6b488b38894835"},"sbom":{"path":"declarations/sbom.json","sha256":"2f25499e7ad0bdcd26b5413a398c42ca0cf161ae8c7e2d5b2fc89768d90ee59f"},"attestation":{"path":"declarations/attestation.json","sha256":"34cdb3c6d0c1c1f39cda15e33f77879774526c298616b9cc182a5f273ae5b2b4"},"platformQualification":{"path":"declarations/platformQualification.json","sha256":"7cfad80cdd728bcd5ec49b1b17085510aa19c941315d9a11668b999681a60f34"},"capabilityParityEvidence":{"path":"declarations/capabilityParityEvidence.json","sha256":"4f134a79a5a81a364a622168ea98b748ba463664a8a256a4414a56e68bf2876f"},"performanceBaseline":{"path":"declarations/performanceBaseline.json","sha256":"f070f1cb480a4aef23c2d2a404ec7bf43a427e05e6e3b8c4c3e8069cb88d6d93"}},"permissions":[],"provenance":{"publisher":"opensip","sourceClass":"first-party"},"stateMigration":{"reserved":true,"ridesOn":["DR-124","DR-106","DR-109","DR-113"]},"updateData":{"reserved":true,"ridesOn":["DR-110","DR-112"]},"compatibility":{"manifest":1,"hostCore":{"min":"0.1.0","max":"0.2.0","includeMin":true,"includeMax":false},"control":1,"providerProtocol":1,"componentState":1}}"#;
    /// Component manifest `i`: `COMPONENT_MANIFEST` at version `1.0.i`.
    pub(crate) fn component_body(i: usize) -> Vec<u8> {
        canonical(&COMPONENT_MANIFEST.replace("\"1.0.0\"", &format!("\"1.0.{i}\"")))
    }
    /// Component manifest `i`'s envelope, signed by `signer` (role, seed
    /// indices) with the keys `root` lists, and the catalog release row that
    /// joins it (law 463 r9; X4B-a; X4B-c reuses it for X4T-0's payload).
    pub(crate) fn component_release(
        i: usize,
        body: &[u8],
        signer: Signer<'_>,
        root: &V,
    ) -> (Vec<u8>, String) {
        // M3-C r8 item 8 (unit C2a-2): through the shared module, with the
        // pre-existing `p1` artifact profile, byte for byte.
        let value = opensip_identity::parse_json(body).unwrap();
        assert_eq!(s(&o(&value)["version"]), format!("1.0.{i}"));
        components::release_row(body, signer, root, &["macos-arm64"], "p1")
    }
    /// M3-C r8 item 8 (unit C2a-2): the shared synthetic component fixtures.
    pub(crate) mod components {
        include!("component_fixtures.rs");
    }
    impl Default for Spec<'static> {
        fn default() -> Self {
            Self {
                schema: 3,
                link: true,
                revoke: &[],
                revocation_root: None,
                platform: "macos-aarch64",
                entrypoint: "bin/opensip",
                bootstrap: "trust/bootstrap",
                exe: b"TEST-ONLY-NOT-AN-EXECUTABLE",
                flags: &["CS_VALID"],
                state_writer: 2,
                extra_envelope: false,
                root_schema: 1,
                profile_pin: None,
                tree_files: &[],
                catalog_signers: &[INDEX_SIGNER],
                component_signers: &[Some(COMPONENT_SIGNER)],
                components: &[],
                catalog_expires: "2027-04-01T00:00:00Z",
                revocation_issued: "2026-10-01T00:00:00Z",
                root_expires: None,
            }
        }
    }
    /// Every byte of the release: the bootstrap directory's files by name
    /// (including the payload pair), the inventory pair, the entrypoint bytes,
    /// and the in-memory anchor record with its reference.
    pub(crate) struct Signed {
        pub(crate) bootstrap: BTreeMap<String, Vec<u8>>,
        pub(crate) inventory: Vec<u8>,
        pub(crate) inventory_env: Vec<u8>,
        pub(crate) exe: Vec<u8>,
        pub(crate) record: Vec<u8>,
        pub(crate) reference: V,
        pub(crate) root_digest: [u8; 32],
        pub(crate) revocation: [u8; 32],
    }
    pub(crate) fn signed_release(spec: &Spec) -> Signed {
        let int = |n| V::Integer(opensip_identity::JsonInteger::new(n).unwrap());
        let link = spec.link;
        let mut root0 = quorum_root(spec.root_schema);
        if let (Some(expires), V::Object(r)) = (spec.root_expires, &mut root0) {
            r.insert("expiresAt".into(), V::String(expires.into()));
        }
        let mut root1 = root0.clone();
        let V::Object(r) = &mut root1 else {
            unreachable!()
        };
        r.insert("rootVersion".into(), int(2));
        r.insert("previousRootVersion".into(), int(1));
        r.insert(
            "rootKeys".into(),
            V::Array((20..23).map(|i| V::String(digest_hex(&key(i)))).collect()),
        );
        let mut files: BTreeMap<String, Vec<u8>> = BTreeMap::new();
        let body0 = canonical_bytes(&root0).unwrap();
        let domain0 = format!("opensip.metadata.root.{}", spec.root_schema);
        let env0 = sign(&body0, "root", &domain0, "ROOT", &root0, &[0, 1, 2]);
        files.insert("root-0.json".into(), body0.clone());
        files.insert("root-0.sig.json".into(), env0.clone());
        if spec.extra_envelope {
            let extra = sign(&body0, "root", &domain0, "ROOT", &root0, &[0, 1]);
            files.insert("root-0x.sig.json".into(), extra);
        }
        let mut final_keys = [0, 1, 2];
        if link {
            let body1 = canonical_bytes(&root1).unwrap();
            let by = [0, 1, 2, 20, 21, 22];
            let env1 = sign(&body1, "root", "opensip.metadata.root.1", "ROOT", &root0, &by);
            files.insert("root-1.json".into(), body1);
            files.insert("root-1.sig.json".into(), env1);
            final_keys = [20, 21, 22];
        }
        let entries: Vec<_> = spec
            .revoke
            .iter()
            .map(|&i| {
                format!(
                    r#"{{"reason":"key-compromise","revokedAt":"2026-10-01T00:00:00Z","subject":"{}","subjectKind":"keyId"}}"#,
                    digest_hex(&key(i))
                )
            })
            .collect();
        let revocation = canonical(&format!(
            r#"{{"entries":[{}],"issuedAt":"{}","revocationSchema":1,"revocationVersion":1,"rootVersion":{}}}"#,
            entries.join(","),
            spec.revocation_issued,
            spec.revocation_root.unwrap_or(if link { 2 } else { 1 })
        ));
        let revocation_env = sign(
            &revocation,
            "revocation",
            "opensip.metadata.revocation.1",
            "ROOT",
            &root0,
            &final_keys,
        );
        files.insert("revocation.json".into(), revocation.clone());
        files.insert("revocation.sig.json".into(), revocation_env);
        // Law 463 r9: a catalog signed under TR-INDEX and component manifests
        // signed under TR-COMPONENT, each listed with its envelopes. X4B-a:
        // the catalog lists one release row per signed component manifest,
        // so the retained reader's catalog join (`MissingRelease`) admits it.
        let mut releases = Vec::new();
        for (i, signer) in spec.component_signers.iter().enumerate() {
            let body = spec.components.get(i).cloned().unwrap_or_else(|| component_body(i));
            if let Some(signer) = signer {
                let (env, release) = if spec.components.is_empty() {
                    component_release(i, &body, *signer, &root0)
                } else {
                    components::release(&body, *signer, &root0, &["macos-arm64"])
                };
                releases.push(release);
                files.insert(format!("component-{i}.sig.json"), env);
            }
            files.insert(format!("component-{i}.json"), body);
        }
        let catalog = canonical(&format!(
            r#"{{"catalogSchema":1,"expiresAt":"{}","issuedAt":"2026-10-01T00:00:00Z","releases":[{}],"reservedRootCommands":[],"revocationVersionRequired":1,"rootVersionRequired":{},"snapshotVersion":1}}"#,
            spec.catalog_expires,
            releases.join(","),
            if link { 2 } else { 1 }
        ));
        for (i, (role, by)) in spec.catalog_signers.iter().enumerate() {
            let env = sign(&catalog, "catalog", "opensip.metadata.catalog.1", role, &root0, by);
            let name = if i == 0 { "catalog.sig.json".into() } else { format!("catalog-{i}.sig.json") };
            files.insert(name, env);
        }
        files.insert("catalog.json".into(), catalog);
        let member = |p: &str| {
            format!(
                r#"{{"path":"{p}","sha256":"{}"}}"#,
                digest_hex(&opensip_identity::raw_sha256(&files[p]))
            )
        };
        let listed = |f: fn(&str) -> bool| {
            files
                .keys()
                .filter(|p| f(p))
                .map(|p| member(p))
                .collect::<Vec<_>>()
                .join(",")
        };
        let manifest = canonical(&format!(
            r#"{{"issuedAt":"2026-10-01T00:00:00Z","members":{{"artifacts":[],"catalog":{},"envelopes":[{}],"manifests":[{}],"permissionPolicies":[],"repairMaterial":{{"ridesOn":"DR-110","standing":"absent-by-typed-absence"}},"revocation":{},"rootChain":[{}]}},"payloadKind":"ordinary","payloadSchema":1}}"#,
            member("catalog.json"),
            listed(|p| p.ends_with(".sig.json")),
            listed(|p| p.starts_with("component-") && !p.ends_with(".sig.json")),
            member("revocation.json"),
            listed(|p| p.starts_with("root-") && !p.ends_with(".sig.json"))
        ));
        let manifest_env = sign(
            &manifest,
            "payload",
            "opensip.metadata.payload.1",
            "TR-BUNDLE",
            &root0,
            &[17, 18, 19],
        );
        files.insert("payload.json".into(), manifest.clone());
        files.insert("payload.sig.json".into(), manifest_env.clone());
        let exe = spec.exe.to_vec();
        let file = |p: &str, raw: &[u8]| {
            format!(
                r#"{{"length":{},"mode":"0644","path":"{p}","sha256":"{}","type":"file"}}"#,
                raw.len(),
                digest_hex(&opensip_identity::raw_sha256(raw))
            )
        };
        // Directory rows for every proper prefix, then the files, in path order.
        let mut tree: BTreeMap<String, String> = BTreeMap::new();
        let extra = spec.tree_files.iter().map(|(p, _)| *p);
        for path in [spec.entrypoint, spec.bootstrap].into_iter().chain(extra) {
            for (i, _) in path.match_indices('/') {
                tree.insert(
                    path[..i].into(),
                    format!(r#"{{"mode":"0755","path":"{}","type":"dir"}}"#, &path[..i]),
                );
            }
        }
        tree.insert(
            spec.bootstrap.into(),
            format!(r#"{{"mode":"0755","path":"{}","type":"dir"}}"#, spec.bootstrap),
        );
        tree.insert(spec.entrypoint.into(), file(spec.entrypoint, &exe));
        let mut layers = BTreeMap::from([(
            spec.entrypoint.to_owned(),
            format!(r#"{{"layers":["L-DIST","L-HOST"],"path":"{}"}}"#, spec.entrypoint),
        )]);
        let mut requires = Vec::new();
        for (p, raw) in &files {
            let path = format!("{}/{p}", spec.bootstrap);
            tree.insert(path.clone(), file(&path, raw));
            layers.insert(path.clone(), format!(r#"{{"layers":["L-DIST"],"path":"{path}"}}"#));
            requires.push(format!(r#"{{"from":"{}","to":"{path}"}}"#, spec.entrypoint));
        }
        for (path, raw) in spec.tree_files {
            tree.insert((*path).into(), file(path, raw));
            layers.insert(
                (*path).into(),
                format!(r#"{{"layers":["L-DIST"],"path":"{path}"}}"#),
            );
        }
        let tree: Vec<_> = tree.into_values().collect();
        let layers: Vec<_> = layers.into_values().collect();
        let release_members = if spec.schema == 3 {
            let flags: Vec<_> = spec.flags.iter().map(|f| format!(r#""{f}""#)).collect();
            format!(
                r#""requiredCodeSigningFlags":[{}],"stateWriter":{},"#,
                flags.join(","),
                spec.state_writer
            )
        } else {
            String::new()
        };
        let inventory = canonical(&format!(
            r#"{{"embeddedBootstrap":{{"directory":"{b}","envelope":{{"bytes":{},"path":"{b}/payload.sig.json","sha256":"{}"}},"manifest":{{"bytes":{},"path":"{b}/payload.json","sha256":"{}"}}}},"inventorySchema":{},"platformProfileBinding":{{"platformProfileSetBodyDigest":"{}","schemaVersion":2}},"platforms":[{{"entrypoint":"{}","layers":[{}],"platform":"{}","requires":[{}],{}"tree":{{"entries":[{}]}}}}],"protocolMajor":1,"semanticVersion":"1.0.0","servedProtocolMajors":[1,2],"tcbProfiles":[],"verifiedInstallRoot":"/"}}"#,
            manifest_env.len(),
            digest_hex(&opensip_identity::raw_sha256(&manifest_env)),
            manifest.len(),
            digest_hex(&opensip_identity::raw_sha256(&manifest)),
            spec.schema,
            digest_hex(&spec.profile_pin.unwrap_or([0xaa; 32])),
            spec.entrypoint,
            layers.join(","),
            spec.platform,
            requires.join(","),
            release_members,
            tree.join(","),
            b = spec.bootstrap,
        ));
        let inventory_env = sign(
            &inventory,
            "inventory",
            "opensip.metadata.inventory.1",
            "TR-CORE",
            &root0,
            &[8, 9, 10],
        );
        let closure = if spec.schema == 3 {
            super::super::core_inventory::project_v3(&inventory, spec.platform)
                .unwrap()
                .core()
                .closure()
                .to_owned()
        } else {
            super::super::core_inventory::project(&inventory, spec.platform)
                .unwrap()
                .closure()
                .to_owned()
        };
        let anchor = admit(&root0, [true, true]).unwrap();
        let record = canonical(&format!(
            r#"{{"admissionSchema":1,"binding":{{"rootDigest":"{}","rootSchema":{},"rootVersion":1}},"bootstrapManifest":{{"body":{},"envelope":{}}},"coreClosure":"{closure}","coreInventory":{{"body":{},"envelope":{}}},"kind":"anchor","platform":"{}","root":{{"body":{},"envelope":{}}}}}"#,
            digest_hex(&anchor.digest()),
            spec.root_schema,
            doc(&manifest),
            doc(&manifest_env),
            doc(&inventory),
            doc(&inventory_env),
            spec.platform,
            doc(&body0),
            doc(&env0)
        ));
        let reference = opensip_identity::parse_json(doc(&record).as_bytes()).unwrap();
        Signed {
            bootstrap: files,
            inventory,
            inventory_env,
            exe,
            record,
            reference,
            root_digest: anchor.digest(),
            revocation: opensip_identity::raw_sha256(&revocation),
        }
    }
    fn run(
        files: &BTreeMap<(Collection, [u8; 32]), Vec<u8>>,
        reference: &V,
    ) -> Result<EmbeddedRelease, ReleaseError> {
        let mut budget = Budget::new(65536, 131072, 268435456).unwrap();
        let mut store =
            |c: Collection, h: [u8; 32], _: usize| files.get(&(c, h)).cloned().ok_or(());
        authenticate_embedded_release(&mut budget, reference, &mut store)
    }
    #[test]
    fn embedded_release_applies_its_own_revocation_after_the_chain() {
        for (link, revoke) in [(true, vec![8, 17, 21]), (false, vec![]), (false, vec![0])] {
            let r = release(link, &revoke, None);
            let got = run(&r.store, &r.reference).unwrap();
            let revoked: BTreeSet<_> = revoke.iter().map(|&i| key(i)).collect();
            assert_eq!(got.revoked(), &revoked);
            let members = got.authentication().core().release().unwrap();
            assert_eq!(
                (members.state_writer(), members.required_code_signing_flags()),
                (2, 0x1)
            );
            assert!(got.authentication().original_revoked().is_empty());
            assert_eq!(
                got.authentication().chain().links().len(),
                usize::from(link)
            );
            assert_eq!(got.revocation().version(), 1);
            for (q, role) in [
                (got.revocation_quorum(), QuorumRole::Root),
                (got.inventory().quorum(), QuorumRole::Core),
                (got.manifest().quorum(), QuorumRole::Bundle),
            ] {
                assert_eq!(q.state(), &QuorumState::Met);
                assert_eq!(q.role(), role);
                assert!(q.valid().is_disjoint(&revoked));
            }
            let initial = got.authentication().core().initial();
            assert_eq!(got.inventory().kind(), EnvelopeKind::Inventory);
            assert_eq!(got.inventory().stored(), initial["coreInventory"].0.as_ref());
            assert_eq!(got.manifest().kind(), EnvelopeKind::Payload);
            assert_eq!(got.manifest().stored(), initial["bootstrapManifest"].0.as_ref());
            assert_eq!(
                got.inventory().quorum().valid().len(),
                if link { 2 } else { 3 }
            );
        }
    }
    #[test]
    fn embedded_release_refuses_every_quorum_its_revocation_breaks() {
        for (link, revoke, kind) in [
            // The revocation cannot make itself effective with keys it names.
            (false, vec![0, 1], EnvelopeKind::Revocation),
            (true, vec![20, 21], EnvelopeKind::Root),
            (true, vec![0, 1], EnvelopeKind::Root),
            (true, vec![8, 9], EnvelopeKind::Inventory),
            (false, vec![17, 18], EnvelopeKind::Payload),
        ] {
            let r = release(link, &revoke, None);
            assert_eq!(
                run(&r.store, &r.reference).err(),
                Some(ReleaseError::Quorum(kind)),
                "{revoke:?}"
            );
            // The inner step alone, with its internal empty set, still passes.
            let mut budget = Budget::new(65536, 131072, 268435456).unwrap();
            let mut store =
                |c: Collection, h: [u8; 32], _: usize| r.store.get(&(c, h)).cloned().ok_or(());
            let inner = authenticate_with(
                &mut budget,
                &r.reference,
                &BTreeSet::new(),
                &mut store,
                InventorySchema::V3,
            );
            assert!(inner.is_ok());
        }
    }
    #[test]
    fn embedded_release_refuses_a_missing_or_misbound_revocation() {
        let mut r = release(true, &[], None);
        r.store.remove(&(Collection::Objects, r.revocation));
        assert!(matches!(
            run(&r.store, &r.reference).err(),
            Some(ReleaseError::RevocationMember(Core::BindingError::Budget(_)))
        ));
        // Verified under the final root only, at that root's version.
        let r = release(true, &[], Some(1));
        assert_eq!(
            run(&r.store, &r.reference).err(),
            Some(ReleaseError::Revocation(RevocationError::RootVersion))
        );
    }
    fn v2_refusal() -> ReleaseError {
        ReleaseError::Authentication(AuthenticationError::Core(Core::BindingError::Core(
            super::super::core_inventory::Error::Shape(
                crate::trust::trust_record_shapes::Error::Shape,
            ),
        )))
    }
    #[test]
    fn embedded_release_requires_core_inventory_v3() {
        let r = release_as(2, true, &[], None);
        assert_eq!(run(&r.store, &r.reference).err(), Some(v2_refusal()));
        // The same V2 release authenticates through the unchanged V2 reader,
        // with no release members.
        let mut budget = Budget::new(65536, 131072, 268435456).unwrap();
        let mut store =
            |c: Collection, h: [u8; 32], _: usize| r.store.get(&(c, h)).cloned().ok_or(());
        let v2 = authenticate(&mut budget, &r.reference, &BTreeSet::new(), &mut store).unwrap();
        assert!(v2.core().release().is_none());
        // And a V3 release does not pass the V2 reader.
        let r = release(true, &[], None);
        let mut budget = Budget::new(65536, 131072, 268435456).unwrap();
        let mut store =
            |c: Collection, h: [u8; 32], _: usize| r.store.get(&(c, h)).cloned().ok_or(());
        assert_eq!(
            authenticate(&mut budget, &r.reference, &BTreeSet::new(), &mut store).err(),
            Some(AuthenticationError::Core(Core::BindingError::Core(
                super::super::core_inventory::Error::Shape(
                    crate::trust::trust_record_shapes::Error::Shape,
                ),
            )))
        );
    }
    #[test]
    fn placeholder_fixture_releases_refuse_without_a_signed_revocation() {
        let mut refused = 0;
        for line in include_bytes!("../../tests/fixtures/core-auth323.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let row = opensip_identity::parse_json(line).unwrap();
            let q = o(&row);
            if a(&q["outcomes"]).iter().all(|v| o(v)["ok"] != V::Bool(true)) {
                continue;
            }
            let files: BTreeMap<_, _> = a(&q["store"])
                .iter()
                .map(|v| {
                    let v = o(v);
                    (
                        (
                            collection(&v["collection"]),
                            decode_hex32(s(&v["sha256"])).unwrap(),
                        ),
                        bytes(&v["raw"]),
                    )
                })
                .collect();
            // Every 323 fixture is CoreInventoryV2, refused before revocation.
            assert_eq!(run(&files, &q["reference"]).err(), Some(v2_refusal()));
            refused += 1;
        }
        assert_eq!(refused, 13);
    }
}
