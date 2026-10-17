// Ordinary full catalog/component semantics and exact authenticated joins.
// Supplied host contexts and unresolved root authority remain explicit.
use super::super::component_manifest as F;
#[cfg(test)]
use super::retained_metadata_index::Collection;
use super::retained_metadata_index::{self as M, Budget};
use super::*;
use catalog as C;
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Error {
    Input(M::Error),
    Catalog(C::Error),
    ContextSet,
    Manifest(F::Error),
    MissingRelease,
    Namespace,
    BodyDigest,
    Preimage,
    EnvelopeDigest,
    Compatibility,
    MissingProof,
}
impl From<M::Error> for Error {
    fn from(e: M::Error) -> Self {
        Self::Input(e)
    }
}
pub(super) use super::recovery_metadata::HostContext;
pub(super) struct Component {
    path: String,
    manifest: F::Validated,
    release: V,
}
impl Component {
    pub(super) fn path(&self) -> &str {
        &self.path
    }
    pub(super) fn manifest(&self) -> &V {
        self.manifest.value()
    }
    pub(super) fn release(&self) -> &V {
        &self.release
    }
}
pub(super) struct Evidence {
    catalog: C::Evidence,
    components: Vec<Component>,
}
impl Evidence {
    pub(super) fn catalog(&self) -> &C::Evidence {
        &self.catalog
    }
    pub(super) fn components(&self) -> &[Component] {
        &self.components
    }
}
pub(super) fn prepare(
    budget: &mut Budget,
    closure_ref: &V,
    signing_root_ref: &V,
    signing_root: &ValidatedRootPayload,
    revoked: &BTreeSet<[u8; 32]>,
    contexts: &BTreeMap<String, HostContext>,
    store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
) -> Result<Evidence, Error> {
    budget.scope(|b| {
        let catalog = C::prepare(
            b,
            closure_ref,
            signing_root_ref,
            signing_root,
            revoked,
            store,
        )
        .map_err(Error::Catalog)?;
        let retained = catalog.signed().retained();
        let manifest = object(retained.bundle().proof().payload()).unwrap();
        let members = object(&manifest["members"]).unwrap();
        let order = array(&members["manifests"]).unwrap();
        let paths: BTreeSet<_> = order
            .iter()
            .map(|v| string(&object(v).unwrap()["path"]).unwrap())
            .collect();
        if paths.len() != contexts.len() || paths.iter().any(|p| !contexts.contains_key(*p)) {
            return Err(Error::ContextSet);
        }
        let reserved_names: BTreeSet<_> =
            array(&object(catalog.catalog()).unwrap()["reservedRootCommands"])
                .unwrap()
                .iter()
                .map(|v| string(v).unwrap().to_owned())
                .collect();
        let mut components = Vec::new();
        for row in order {
            let path = string(&object(row).unwrap()["path"]).unwrap();
            let pair = retained.pairs().get(path).unwrap();
            let context = &contexts[path];
            let context = F::Context {
                approved_exceptions: context.approved_exceptions.clone(),
                host_classifications: context.host_classifications.clone(),
                live_names: context.live_names.clone(),
                reserved_names: reserved_names.clone(),
            };
            let validated = F::validate(pair.body(), &context).map_err(Error::Manifest)?;
            let body = object(validated.value()).unwrap();
            let provenance = object(&body["provenance"]).unwrap();
            let identity = [
                string(&body["stableId"]).unwrap().to_owned(),
                string(&provenance["publisher"]).unwrap().to_owned(),
                string(&provenance["sourceClass"]).unwrap().to_owned(),
                string(&body["version"]).unwrap().to_owned(),
            ];
            let release = catalog.release(&identity).ok_or(Error::MissingRelease)?;
            let r = object(release).unwrap();
            let group = catalog
                .signed()
                .groups()
                .iter()
                .find(|g| g.kind() == EnvelopeKind::Manifest && g.path() == Some(path))
                .ok_or(Error::MissingProof)?;
            if group.proof().namespace() != identity[1] {
                return Err(Error::Namespace);
            }
            if opensip_identity::raw_sha256(pair.body())
                != decode_hex32(string(&r["manifestDigest"]).unwrap()).unwrap()
            {
                return Err(Error::BodyDigest);
            }
            // The signature message also binds envelope role/namespace;
            // the catalog names the distinct metadata preimage digest.
            // This is the same immutable raw envelope already verified
            // by266, not a caller-supplied carrier or a fresh lookup.
            let envelope =
                super::super::metadata::parse(pair.envelope()).map_err(|_| Error::MissingProof)?;
            let carrier =
                verified_envelopes::parse_carrier(&envelope).map_err(|_| Error::MissingProof)?;
            if carrier.preimage_digest()
                != decode_hex32(string(&r["manifestPreimageSha256"]).unwrap()).unwrap()
            {
                return Err(Error::Preimage);
            }
            if opensip_identity::raw_sha256(pair.envelope())
                != decode_hex32(string(&r["envelopeDigest"]).unwrap()).unwrap()
            {
                return Err(Error::EnvelopeDigest);
            }
            if object(&body["compatibility"]).unwrap()["hostCore"] != r["hostCoreConstraint"] {
                return Err(Error::Compatibility);
            }
            components.push(Component {
                path: path.to_owned(),
                manifest: validated,
                release: release.clone(),
            });
        }
        Ok(Evidence {
            catalog,
            components,
        })
    })
}

// Visible to the root_payload tree so a caller can match its typed causes.
pub(in crate::trust::root_payload) mod catalog {
    use super::super::ordinary_quorums as Q;
    use super::super::recovery_catalog as Schema;
    use super::super::retained_metadata_index::{self as M, Budget};
    use super::*;
    type Identity = [String; 4];
    #[derive(Debug, PartialEq, Eq)]
    pub(in crate::trust::root_payload) enum Error {
        Input(M::Error),
        Quorums(Q::Error),
        MemberCount,
        Schema(Schema::Error),
    }
    impl From<M::Error> for Error {
        fn from(e: M::Error) -> Self {
            Self::Input(e)
        }
    }
    pub(in crate::trust::root_payload) struct Evidence {
        signed: Q::Evidence,
        catalog: V,
        releases: BTreeMap<Identity, usize>,
    }
    impl Evidence {
        pub(in crate::trust::root_payload) fn signed(&self) -> &Q::Evidence {
            &self.signed
        }
        pub(in crate::trust::root_payload) fn catalog(&self) -> &V {
            &self.catalog
        }
        pub(in crate::trust::root_payload) fn release(&self, identity: &Identity) -> Option<&V> {
            let index = *self.releases.get(identity)?;
            array(&object(&self.catalog)?["releases"])?.get(index)
        }
    }
    pub(in crate::trust::root_payload) fn prepare(
        budget: &mut Budget,
        closure_ref: &V,
        signing_root_ref: &V,
        signing_root: &ValidatedRootPayload,
        revoked: &BTreeSet<[u8; 32]>,
        store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
    ) -> Result<Evidence, Error> {
        budget.scope(|b| {
            let signed = Q::prepare(
                b,
                closure_ref,
                signing_root_ref,
                signing_root,
                revoked,
                store,
            )
            .map_err(Error::Quorums)?;
            let mut catalogs = signed
                .retained()
                .pairs()
                .values()
                .filter(|p| p.kind() == EnvelopeKind::Catalog);
            let pair = catalogs.next().ok_or(Error::MemberCount)?;
            if catalogs.next().is_some() {
                return Err(Error::MemberCount);
            }
            let catalog = super::super::super::metadata::parse(pair.body())
                .map_err(|_| Error::Schema(Schema::Error::Shape))?;
            let releases = Schema::validate(&catalog).map_err(Error::Schema)?;
            Ok(Evidence {
                signed,
                catalog,
                releases,
            })
        })
    }
}

// All component inventory-body and catalog joins, without host admission or
// component signature authority. Shared signatures remain mandatory.
pub(in crate::trust::root_payload) mod inventory {
    use super::super::ordinary_quorums as Q;
    use super::*;
    pub(in crate::trust::root_payload) struct Component {
        path: String,
        body: F::InventoryBody,
        release: V,
    }
    impl Component {
        pub(in crate::trust::root_payload) fn path(&self) -> &str {
            &self.path
        }
        pub(in crate::trust::root_payload) fn manifest(&self) -> &V {
            self.body.value()
        }
        pub(in crate::trust::root_payload) fn release(&self) -> &V {
            &self.release
        }
    }
    pub(in crate::trust::root_payload) struct Evidence {
        shared: Q::SharedEvidence,
        catalog: V,
        releases: BTreeMap<[String; 4], usize>,
        components: Vec<Component>,
    }
    impl Evidence {
        pub(in crate::trust::root_payload) fn shared(&self) -> &Q::SharedEvidence {
            &self.shared
        }
        pub(in crate::trust::root_payload) fn catalog(&self) -> &V {
            &self.catalog
        }
        pub(in crate::trust::root_payload) fn components(&self) -> &[Component] {
            &self.components
        }
        pub(in crate::trust::root_payload) fn release(&self, identity: &[String; 4]) -> Option<&V> {
            array(&object(&self.catalog)?["releases"])?.get(*self.releases.get(identity)?)
        }
    }
    pub(in crate::trust::root_payload) fn prepare(
        budget: &mut Budget,
        closure_ref: &V,
        signing_root_ref: &V,
        signing_root: &ValidatedRootPayload,
        revoked: &BTreeSet<[u8; 32]>,
        store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
    ) -> Result<Evidence, Error> {
        budget.scope(|b| {
            let shared = Q::prepare_shared(
                b,
                closure_ref,
                signing_root_ref,
                signing_root,
                revoked,
                store,
            )
            .map_err(|e| Error::Catalog(C::Error::Quorums(e)))?;
            let retained = shared.retained();
            let mut catalogs = retained
                .pairs()
                .values()
                .filter(|p| p.kind() == EnvelopeKind::Catalog);
            let pair = catalogs
                .next()
                .ok_or(Error::Catalog(C::Error::MemberCount))?;
            if catalogs.next().is_some() {
                return Err(Error::Catalog(C::Error::MemberCount));
            }
            let catalog = super::super::super::metadata::parse(pair.body()).map_err(|_| {
                Error::Catalog(C::Error::Schema(
                    super::super::recovery_catalog::Error::Shape,
                ))
            })?;
            let releases = super::super::recovery_catalog::validate(&catalog)
                .map_err(|e| Error::Catalog(C::Error::Schema(e)))?;
            let reserved: BTreeSet<_> = array(&object(&catalog).unwrap()["reservedRootCommands"])
                .unwrap()
                .iter()
                .map(|v| string(v).unwrap().to_owned())
                .collect();
            let mut components = Vec::new();
            for path in shared.pending_components() {
                let pair = retained.pairs().get(path).ok_or(Error::MissingProof)?;
                let validated =
                    F::validate_inventory(pair.body(), &reserved).map_err(Error::Manifest)?;
                let body = object(validated.value()).unwrap();
                let provenance = object(&body["provenance"]).unwrap();
                let identity = [
                    string(&body["stableId"]).unwrap().to_owned(),
                    string(&provenance["publisher"]).unwrap().to_owned(),
                    string(&provenance["sourceClass"]).unwrap().to_owned(),
                    string(&body["version"]).unwrap().to_owned(),
                ];
                let index = *releases.get(&identity).ok_or(Error::MissingRelease)?;
                let release = &array(&object(&catalog).unwrap()["releases"]).unwrap()[index];
                let r = object(release).unwrap();
                let envelope = super::super::super::metadata::parse(pair.envelope())
                    .map_err(|_| Error::MissingProof)?;
                let carrier = verified_envelopes::parse_carrier(&envelope)
                    .map_err(|_| Error::MissingProof)?;
                // Identity only: do not ask whether keys are delegated for it.
                if string(&object(&envelope).unwrap()["namespace"]) != Some(identity[1].as_str()) {
                    return Err(Error::Namespace);
                }
                if opensip_identity::raw_sha256(pair.body())
                    != decode_hex32(string(&r["manifestDigest"]).unwrap()).unwrap()
                {
                    return Err(Error::BodyDigest);
                }
                if carrier.preimage_digest()
                    != decode_hex32(string(&r["manifestPreimageSha256"]).unwrap()).unwrap()
                {
                    return Err(Error::Preimage);
                }
                if opensip_identity::raw_sha256(pair.envelope())
                    != decode_hex32(string(&r["envelopeDigest"]).unwrap()).unwrap()
                {
                    return Err(Error::EnvelopeDigest);
                }
                if object(&body["compatibility"]).unwrap()["hostCore"] != r["hostCoreConstraint"] {
                    return Err(Error::Compatibility);
                }
                components.push(Component {
                    path: path.clone(),
                    body: validated,
                    release: release.clone(),
                });
            }
            Ok(Evidence {
                shared,
                catalog,
                releases,
                components,
            })
        })
    }
}

// M3-C r8 item 7 (unit C2a-1): the trust owner's read-only bridge. Each
// verified component, in catalog order, with the body and envelope bytes the
// reader authenticated for it, borrowed from this evidence.
impl Evidence {
    pub(in crate::trust) fn admitted_components(
        &self,
    ) -> impl Iterator<Item = crate::trust::AuthenticatedComponent<'_>> {
        let pairs = self.catalog.signed().retained().pairs();
        self.components.iter().map(move |c| {
            let pair = &pairs[c.path.as_str()];
            crate::trust::AuthenticatedComponent::new(
                &c.path,
                pair.body(),
                pair.envelope(),
                &c.manifest,
                &c.release,
            )
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn text(v: &V) -> &str {
        string(v).unwrap()
    }
    fn hash(v: &V) -> [u8; 32] {
        decode_hex32(text(v)).unwrap()
    }
    fn bytes(v: &V) -> Vec<u8> {
        let s = text(v);
        (0..s.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
            .collect()
    }
    fn count(v: &V) -> usize {
        integer(v).unwrap() as usize
    }
    fn hex(h: [u8; 32]) -> String {
        h.iter().map(|b| format!("{b:02x}")).collect()
    }
    fn collection(v: &V) -> Collection {
        match text(v) {
            "objects" => Collection::Objects,
            "records" => Collection::Records,
            _ => panic!("unexpected collection"),
        }
    }
    #[test]
    fn full_ordinary_catalog_and_component_joins_match_exact_reference() {
        let mut counts = (0, 0, 0);
        let mut refused = Vec::new();
        for line in include_bytes!("../tests/fixtures/metadata285.ndjson")
            .split(|b| *b == b'\n')
            .filter(|l| !l.is_empty())
        {
            let value = opensip_identity::parse_json(line).unwrap();
            let q = object(&value).unwrap();
            let label = text(&q["label"]).to_owned();
            let root = admit(&q["root"], [true, true]).unwrap();
            let revoked: BTreeSet<_> = array(&q["revoked"]).unwrap().iter().map(hash).collect();
            let limits = array(&q["limits"]).unwrap();
            let mut budget =
                Budget::new(count(&limits[0]), count(&limits[1]), count(&limits[2])).unwrap();
            let contexts: BTreeMap<String, HostContext> = object(&q["contexts"])
                .unwrap()
                .iter()
                .map(|(path, v)| {
                    let o = object(v).unwrap();
                    assert!(o.keys().all(|k| {
                        ["approvedExceptions", "hostClassificationMap", "liveNames"]
                            .contains(&k.as_str())
                    }));
                    (
                        path.clone(),
                        HostContext {
                            approved_exceptions: o
                                .get("approvedExceptions")
                                .map(|v| {
                                    array(v)
                                        .unwrap()
                                        .iter()
                                        .map(|v| text(v).to_owned())
                                        .collect()
                                })
                                .unwrap_or_default(),
                            host_classifications: o
                                .get("hostClassificationMap")
                                .map(|v| {
                                    object(v)
                                        .unwrap()
                                        .iter()
                                        .map(|(k, v)| (k.clone(), text(v).to_owned()))
                                        .collect()
                                })
                                .unwrap_or_default(),
                            live_names: o
                                .get("liveNames")
                                .map(|v| {
                                    array(v)
                                        .unwrap()
                                        .iter()
                                        .map(|v| {
                                            let o = object(v).unwrap();
                                            F::LiveName {
                                                stable_id: text(&o["stableId"]).to_owned(),
                                                provenance: o["provenance"].clone(),
                                                names: array(&o["names"])
                                                    .unwrap()
                                                    .iter()
                                                    .map(|v| text(v).to_owned())
                                                    .collect(),
                                            }
                                        })
                                        .collect()
                                })
                                .unwrap_or_default(),
                        },
                    )
                })
                .collect();
            let files: BTreeMap<_, _> = array(&q["store"])
                .unwrap()
                .iter()
                .map(|v| {
                    let o = object(v).unwrap();
                    (
                        (collection(&o["collection"]), hash(&o["sha256"])),
                        bytes(&o["raw"]),
                    )
                })
                .collect();
            let mut captures = Vec::new();
            let mut owned = Vec::new();
            {
                let mut capture = |coll: Collection, h: [u8; 32], cap: usize| {
                    captures.push((coll, hex(h), cap));
                    files.get(&(coll, h)).cloned().ok_or(())
                };
                for (i, outcome) in array(&q["outcomes"]).unwrap().iter().enumerate() {
                    let expected = object(outcome).unwrap();
                    let result = prepare(
                        &mut budget,
                        &q["closureRef"],
                        &q["signingRootRef"],
                        &root,
                        &revoked,
                        &contexts,
                        &mut capture,
                    );
                    assert_eq!(
                        result.is_ok(),
                        expected["ok"] == V::Bool(true),
                        "{label} round{i}: {:?}",
                        result.as_ref().err()
                    );
                    let c = array(&expected["counters"]).unwrap();
                    assert_eq!(
                        budget.counters(),
                        (count(&c[0]), count(&c[1]), count(&c[2])),
                        "{label} round{i}"
                    );
                    if let Ok(e) = result {
                        owned.push((e, expected["expected"].clone()));
                        if i == 0 {
                            counts.1 += 1;
                        }
                        if i + 1 == array(&q["outcomes"]).unwrap().len() {
                            counts.2 += 1;
                        }
                    }
                }
                if q["failed"] == V::Bool(true) {
                    assert!(
                        matches!(
                            prepare(
                                &mut budget,
                                &q["closureRef"],
                                &q["signingRootRef"],
                                &root,
                                &revoked,
                                &contexts,
                                &mut capture
                            ),
                            Err(Error::Input(M::Error::Closed))
                        ),
                        "{label}"
                    );
                    assert!(matches!(budget.edge(1), Err(M::Error::Closed)), "{label}");
                }
            }
            let expected_captures: Vec<_> = array(&q["captures"])
                .unwrap()
                .iter()
                .map(|v| {
                    let a = array(v).unwrap();
                    (collection(&a[0]), text(&a[1]).to_owned(), count(&a[2]))
                })
                .collect();
            assert_eq!(captures, expected_captures, "{label} captures");
            let expected_root = q["root"].clone();
            let expected_revoked = revoked.clone();
            drop(value);
            drop(files);
            drop(root);
            drop(revoked);
            drop(contexts);
            drop(budget);
            for (e, v) in owned {
                let meta = object(&v).unwrap();
                assert_eq!(e.catalog().catalog(), &meta["catalog"], "{label} catalog");
                let components = array(&meta["components"]).unwrap();
                assert_eq!(
                    e.components().len(),
                    components.len(),
                    "{label} component count"
                );
                for (component, v) in e.components().iter().zip(components) {
                    let c = object(v).unwrap();
                    assert_eq!(component.path(), text(&c["path"]));
                    assert_eq!(component.manifest(), &c["body"]);
                    assert_eq!(component.release(), &c["release"]);
                    let key: [String; 4] = array(&c["identity"])
                        .unwrap()
                        .iter()
                        .map(|v| text(v).to_owned())
                        .collect::<Vec<_>>()
                        .try_into()
                        .unwrap();
                    assert_eq!(e.catalog().release(&key), Some(&c["release"]));
                }
                // C2a-1's bridge lends exactly the verified components, with
                // the body and envelope bytes their release rows bind. Every
                // M2 body here lacks C2PM-1's declaration, so none projects.
                let mut bridged = 0;
                for (b, c) in e.admitted_components().zip(e.components()) {
                    assert_eq!(b.path(), c.path(), "{label} bridge");
                    assert_eq!(b.manifest(), c.manifest(), "{label} bridge");
                    assert_eq!(b.release(), c.release(), "{label} bridge");
                    let r = object(c.release()).unwrap();
                    assert_eq!(
                        opensip_identity::raw_sha256(b.body()),
                        hash(&r["manifestDigest"]),
                        "{label} bridge"
                    );
                    assert_eq!(
                        opensip_identity::raw_sha256(b.envelope()),
                        hash(&r["envelopeDigest"]),
                        "{label} bridge"
                    );
                    let mut work = opensip_platform::WorkLedger::new();
                    let result = work.scope(|w| {
                        crate::component_closure::component_candidate(
                            &b,
                            crate::component_closure::SelectedPlatform {
                                os: "macos",
                                arch: "arm64",
                            },
                            None,
                            crate::component_closure::tests::registry(),
                            w,
                        )
                    });
                    match result {
                        Err(opensip_platform::WorkFailure::Operation(refusal)) => {
                            refused.push(refusal)
                        }
                        Err(budget) => panic!("{label}: {budget:?}"),
                        Ok(_) => panic!("{label}: an M2 body projected"),
                    }
                    bridged += 1;
                }
                assert_eq!(bridged, e.components().len(), "{label} bridge");
                let e = e.catalog().signed();
                let top = object(&meta["signed"]).unwrap();
                let expected_union: BTreeSet<_> =
                    array(&top["union"]).unwrap().iter().map(hash).collect();
                assert_eq!(e.union(), &expected_union, "{label} union");
                let expected_roots: Vec<_> = array(&top["unresolvedRoots"])
                    .unwrap()
                    .iter()
                    .map(|v| text(v).to_owned())
                    .collect();
                assert_eq!(
                    e.unresolved_roots(),
                    expected_roots,
                    "{label} unresolved roots"
                );
                assert_eq!(
                    e.revocation().envelope().payload(),
                    &top["revocation"],
                    "{label} list"
                );
                let rev = object(&top["revocation"]).unwrap();
                assert_eq!(
                    e.revocation().version(),
                    integer(&rev["revocationVersion"]).unwrap()
                );
                assert_eq!(
                    e.revocation().issued_at(),
                    timestamp_seconds(text(&rev["issuedAt"])).unwrap()
                );
                let expected_groups = array(&top["groups"]).unwrap();
                assert_eq!(e.groups().len(), expected_groups.len(), "{label} groups");
                for (g, x) in e.groups().iter().zip(expected_groups) {
                    let x = object(x).unwrap();
                    assert_eq!(g.kind().route().0, text(&x["kind"]));
                    assert_eq!(g.path(), string(&x["path"]));
                    assert_eq!(g.proof().required(), count(&x["threshold"]));
                    assert_eq!(g.proof().state(), &QuorumState::Met);
                    assert_eq!(hex(g.proof().message()), text(&x["message"]));
                    let signers: BTreeSet<_> = array(&x["survivingSigners"])
                        .unwrap()
                        .iter()
                        .map(hash)
                        .collect();
                    assert_eq!(
                        g.proof().valid(),
                        &signers,
                        "{label} group {}",
                        g.kind().route().0
                    );
                }
                let e = e.retained();
                let x = object(&top["retained"]).unwrap();
                assert_eq!(e.closure_raw(), bytes(&x["closureRaw"]), "{label}");
                assert_eq!(e.closure(), &x["closure"], "{label}");
                assert_eq!(e.signing_root_ref(), &x["signingRootRef"], "{label}");
                assert_eq!(
                    e.artifact_observations(),
                    &x["artifactObservations"],
                    "{label}"
                );
                let bundle = e.bundle();
                assert_eq!(bundle.root(), &expected_root, "{label}");
                assert_eq!(bundle.revoked(), &expected_revoked, "{label}");
                assert_eq!(bundle.proof().payload(), &x["manifest"], "{label}");
                assert_eq!(bundle.document().body(), bytes(&x["bundleBody"]), "{label}");
                assert_eq!(
                    bundle.document().envelope_bytes(),
                    bytes(&x["bundleEnvelope"]),
                    "{label}"
                );
                let quorum = bundle.proof().quorum();
                assert_eq!(quorum.state(), &QuorumState::Met);
                assert_eq!(quorum.required(), count(&x["bundleThreshold"]));
                assert_eq!(hex(quorum.message()), text(&x["bundleMessage"]));
                let signers: BTreeSet<_> = array(&x["bundleSigners"])
                    .unwrap()
                    .iter()
                    .map(hash)
                    .collect();
                assert_eq!(quorum.valid(), &signers, "{label}");
                let pairs = object(&x["metadataPairs"]).unwrap();
                assert_eq!(e.pairs().len(), pairs.len(), "{label}");
                for (path, pair) in e.pairs() {
                    let p = object(&pairs[path]).unwrap();
                    assert_eq!(pair.kind().route().0, text(&p["kind"]));
                    assert_eq!(pair.body_path(), text(&p["bodyPath"]));
                    assert_eq!(pair.envelope_path(), text(&p["envelopePath"]));
                    assert_eq!(pair.body(), bytes(&p["body"]));
                    assert_eq!(pair.envelope(), bytes(&p["envelope"]));
                }
                let retained = object(&x["retained"]).unwrap();
                assert_eq!(e.retained_members().len(), retained.len());
                for (path, raw) in e.retained_members() {
                    assert_eq!(
                        raw.as_ref(),
                        bytes(&retained[path]),
                        "{label} retained {path}"
                    );
                }
            }
            counts.0 += 1;
        }
        assert_eq!(counts, (40, 4, 4));
        assert_eq!(refused.len(), 8);
        assert!(refused.iter().all(|r| *r
            == crate::component_closure::ClosureRefusal::Protocol {
                key: crate::component_closure::ProtocolKey::DeclarationMissing,
                origin: crate::component_closure::ProtocolOrigin::AuthenticatedReleaseDeclaration,
            }));
    }
    #[test]
    fn inventory_component_joins_preserve_identity_without_host_or_signature_authority() {
        let mut counts = (0, 0, 0);
        for line in include_bytes!("../tests/fixtures/inventory293-signed.ndjson")
            .split(|b| *b == b'\n')
            .filter(|l| !l.is_empty())
        {
            let value = opensip_identity::parse_json(line).unwrap();
            let q = object(&value).unwrap();
            let label = text(&q["label"]).to_owned();
            let root = admit(&q["root"], [true, true]).unwrap();
            let revoked: BTreeSet<_> = array(&q["revoked"]).unwrap().iter().map(hash).collect();
            let limits = array(&q["limits"]).unwrap();
            let mut budget =
                Budget::new(count(&limits[0]), count(&limits[1]), count(&limits[2])).unwrap();
            let files: BTreeMap<_, _> = array(&q["store"])
                .unwrap()
                .iter()
                .map(|v| {
                    let o = object(v).unwrap();
                    (
                        (collection(&o["collection"]), hash(&o["sha256"])),
                        bytes(&o["raw"]),
                    )
                })
                .collect();
            let mut captures = Vec::new();
            let mut owned = Vec::new();
            {
                let mut capture = |coll: Collection, h: [u8; 32], cap: usize| {
                    captures.push((coll, hex(h), cap));
                    files.get(&(coll, h)).cloned().ok_or(())
                };
                for (i, outcome) in array(&q["outcomes"]).unwrap().iter().enumerate() {
                    let expected = object(outcome).unwrap();
                    let result = inventory::prepare(
                        &mut budget,
                        &q["closureRef"],
                        &q["signingRootRef"],
                        &root,
                        &revoked,
                        &mut capture,
                    );
                    assert_eq!(
                        result.is_ok(),
                        expected["ok"] == V::Bool(true),
                        "{label} round{i}: {:?}",
                        result.as_ref().err()
                    );
                    let c = array(&expected["counters"]).unwrap();
                    assert_eq!(
                        budget.counters(),
                        (count(&c[0]), count(&c[1]), count(&c[2])),
                        "{label} round{i}"
                    );
                    if let Ok(e) = result {
                        owned.push((e, expected["expected"].clone()));
                        if i == 0 {
                            counts.1 += 1;
                        }
                        if i + 1 == array(&q["outcomes"]).unwrap().len() {
                            counts.2 += 1;
                        }
                    }
                }
                if q["failed"] == V::Bool(true) {
                    assert!(
                        matches!(
                            inventory::prepare(
                                &mut budget,
                                &q["closureRef"],
                                &q["signingRootRef"],
                                &root,
                                &revoked,
                                &mut capture
                            ),
                            Err(Error::Input(M::Error::Closed))
                        ),
                        "{label}"
                    );
                    assert!(matches!(budget.edge(1), Err(M::Error::Closed)), "{label}");
                }
            }
            let expected_captures: Vec<_> = array(&q["captures"])
                .unwrap()
                .iter()
                .map(|v| {
                    let a = array(v).unwrap();
                    (collection(&a[0]), text(&a[1]).to_owned(), count(&a[2]))
                })
                .collect();
            assert_eq!(captures, expected_captures, "{label} captures");
            let expected_root = q["root"].clone();
            let expected_revoked = revoked.clone();
            drop(value);
            drop(files);
            drop(root);
            drop(revoked);
            drop(budget);
            for (e, v) in owned {
                let meta = object(&v).unwrap();
                assert_eq!(e.catalog(), &meta["catalog"], "{label} catalog");
                let components = array(&meta["components"]).unwrap();
                assert_eq!(
                    e.components().len(),
                    components.len(),
                    "{label} component count"
                );
                for (component, v) in e.components().iter().zip(components) {
                    let c = object(v).unwrap();
                    assert_eq!(component.path(), text(&c["path"]));
                    assert_eq!(component.manifest(), &c["body"]);
                    assert_eq!(component.release(), &c["release"]);
                    let key: [String; 4] = array(&c["identity"])
                        .unwrap()
                        .iter()
                        .map(|v| text(v).to_owned())
                        .collect::<Vec<_>>()
                        .try_into()
                        .unwrap();
                    assert_eq!(e.release(&key), Some(&c["release"]));
                }
                let e = e.shared();
                let top = object(&meta["signed"]).unwrap();
                let expected_union: BTreeSet<_> =
                    array(&top["union"]).unwrap().iter().map(hash).collect();
                assert_eq!(e.union(), &expected_union, "{label} union");
                let expected_roots: Vec<_> = array(&top["unresolvedRoots"])
                    .unwrap()
                    .iter()
                    .map(|v| text(v).to_owned())
                    .collect();
                assert_eq!(
                    e.unresolved_roots(),
                    expected_roots,
                    "{label} unresolved roots"
                );
                assert_eq!(
                    e.revocation().envelope().payload(),
                    &top["revocation"],
                    "{label} list"
                );
                let rev = object(&top["revocation"]).unwrap();
                assert_eq!(
                    e.revocation().version(),
                    integer(&rev["revocationVersion"]).unwrap()
                );
                assert_eq!(
                    e.revocation().issued_at(),
                    timestamp_seconds(text(&rev["issuedAt"])).unwrap()
                );
                let expected_groups = array(&top["groups"]).unwrap();
                assert_eq!(e.groups().len(), expected_groups.len(), "{label} groups");
                for (g, x) in e.groups().iter().zip(expected_groups) {
                    let x = object(x).unwrap();
                    assert_eq!(g.kind().route().0, text(&x["kind"]));
                    assert_eq!(g.path(), string(&x["path"]));
                    assert_eq!(g.proof().required(), count(&x["threshold"]));
                    assert_eq!(g.proof().state(), &QuorumState::Met);
                    assert_eq!(hex(g.proof().message()), text(&x["message"]));
                    let signers: BTreeSet<_> = array(&x["survivingSigners"])
                        .unwrap()
                        .iter()
                        .map(hash)
                        .collect();
                    assert_eq!(
                        g.proof().valid(),
                        &signers,
                        "{label} group {}",
                        g.kind().route().0
                    );
                }
                let e = e.retained();
                let x = object(&top["retained"]).unwrap();
                assert_eq!(e.closure_raw(), bytes(&x["closureRaw"]), "{label}");
                assert_eq!(e.closure(), &x["closure"], "{label}");
                assert_eq!(e.signing_root_ref(), &x["signingRootRef"], "{label}");
                assert_eq!(
                    e.artifact_observations(),
                    &x["artifactObservations"],
                    "{label}"
                );
                let bundle = e.bundle();
                assert_eq!(bundle.root(), &expected_root, "{label}");
                assert_eq!(bundle.revoked(), &expected_revoked, "{label}");
                assert_eq!(bundle.proof().payload(), &x["manifest"], "{label}");
                assert_eq!(bundle.document().body(), bytes(&x["bundleBody"]), "{label}");
                assert_eq!(
                    bundle.document().envelope_bytes(),
                    bytes(&x["bundleEnvelope"]),
                    "{label}"
                );
                let quorum = bundle.proof().quorum();
                assert_eq!(quorum.state(), &QuorumState::Met);
                assert_eq!(quorum.required(), count(&x["bundleThreshold"]));
                assert_eq!(hex(quorum.message()), text(&x["bundleMessage"]));
                let signers: BTreeSet<_> = array(&x["bundleSigners"])
                    .unwrap()
                    .iter()
                    .map(hash)
                    .collect();
                assert_eq!(quorum.valid(), &signers, "{label}");
                let pairs = object(&x["metadataPairs"]).unwrap();
                assert_eq!(e.pairs().len(), pairs.len(), "{label}");
                for (path, pair) in e.pairs() {
                    let p = object(&pairs[path]).unwrap();
                    assert_eq!(pair.kind().route().0, text(&p["kind"]));
                    assert_eq!(pair.body_path(), text(&p["bodyPath"]));
                    assert_eq!(pair.envelope_path(), text(&p["envelopePath"]));
                    assert_eq!(pair.body(), bytes(&p["body"]));
                    assert_eq!(pair.envelope(), bytes(&p["envelope"]));
                }
                let retained = object(&x["retained"]).unwrap();
                assert_eq!(e.retained_members().len(), retained.len());
                for (path, raw) in e.retained_members() {
                    assert_eq!(
                        raw.as_ref(),
                        bytes(&retained[path]),
                        "{label} retained {path}"
                    );
                }
            }
            counts.0 += 1;
        }
        assert_eq!(counts, (42, 11, 11));
    }
}
