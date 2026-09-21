//! Private store-marker observations under supplied retained root custody.
//! Neither exact bytes, a marker/name match nor a directory handle admits a store,
//! selection pair or lease. The caller still owes those joins and native custody.
use opensip_identity::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
#[cfg(test)]
use opensip_security::{OperationalFileObservation, OperationalFileReadFailure};
const MARKER_NAME: &str = "store-instance.v1";
const MARKER_LIMIT: usize = 128;
#[derive(Clone, Debug, PartialEq, Eq)]
struct StoreInstance(String);
#[derive(Clone, Debug, PartialEq, Eq)]
enum MarkerError {
    Bound,
    Decode(CanonicalError),
    Shape,
    Instance,
    NonCanonical,
    Binding,
}
impl StoreInstance {
    fn parse(value: &str) -> Result<Self, MarkerError> {
        if value.len() != 32
            || !value
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        {
            return Err(MarkerError::Instance);
        }
        Ok(Self(value.into()))
    }
}
#[derive(Debug)]
struct DecodedMarker {
    instance: StoreInstance,
    bytes: Vec<u8>,
}
impl DecodedMarker {
    fn decode(raw: Vec<u8>, expected: &StoreInstance) -> Result<Self, MarkerError> {
        if raw.len() > MARKER_LIMIT {
            return Err(MarkerError::Bound);
        }
        let value = parse_json(&raw).map_err(MarkerError::Decode)?;
        let V::Object(ref fields) = value else {
            return Err(MarkerError::Shape);
        };
        if fields.len() != 2
            || !matches!(fields.get("schemaVersion"),Some(V::Integer(n))if n.get()==1)
        {
            return Err(MarkerError::Shape);
        }
        let Some(V::String(id)) = fields.get("storeInstanceId") else {
            return Err(MarkerError::Shape);
        };
        let instance = StoreInstance::parse(id)?;
        if canonical_bytes(&value).map_err(MarkerError::Decode)? != raw {
            return Err(MarkerError::NonCanonical);
        }
        if &instance != expected {
            return Err(MarkerError::Binding);
        }
        Ok(Self {
            instance,
            bytes: raw,
        })
    }
}
/// An observation retaining the exact descriptor used for these decoded bytes.
/// The consuming host still owes policy checks, binding and a held lease.
#[derive(Debug)]
#[cfg(test)]
struct CapturedMarker {
    marker: DecodedMarker,
    file: std::fs::File,
}
#[cfg(test)]
impl CapturedMarker {
    /// Sample policy on the descriptor that supplied the marker bytes. This is
    /// not store admission: actor provenance, all parent checks, name binding,
    /// filesystem qualification and exclusion through use remain caller duties.
    fn inspect_file_policy(
        &self,
        invoking_uid: u32,
        authorized_groups: &std::collections::BTreeSet<u32>,
    ) -> Result<
        opensip_platform::DescriptorObservation,
        opensip_security::OperationalFilePolicyFailure,
    > {
        opensip_security::inspect_operational_file_policy(
            &self.file,
            invoking_uid,
            authorized_groups,
        )
    }
}
#[derive(Debug)]
#[cfg(test)]
enum MarkerReadFailure {
    File(OperationalFileReadFailure),
    Marker(MarkerError),
}
#[derive(Debug)]
#[cfg(test)]
enum MarkerObservation {
    Absent,
    Present(CapturedMarker),
    Unavailable(MarkerReadFailure),
}
/// Existing root only: no creation, identity minting, retry, repair or selection.
/// Expected S must originate from an admitted store binding in a future host
/// facade; its private syntax type is not such a binding. Returned bytes describe
/// the read, not current custody after a consuming lease is released.
#[cfg(test)]
fn observe_unchecked_marker(
    root: &opensip_platform::RetainedDirectoryPath,
    expected: &StoreInstance,
) -> MarkerObservation {
    match opensip_security::observe_bound_operational_file(root, MARKER_NAME, MARKER_LIMIT) {
        OperationalFileObservation::Absent => MarkerObservation::Absent,
        OperationalFileObservation::Unreadable(e) => {
            MarkerObservation::Unavailable(MarkerReadFailure::File(e))
        }
        OperationalFileObservation::Present(capture) => {
            let (file, bytes) = capture.into_parts();
            match DecodedMarker::decode(bytes, expected) {
                Ok(marker) => MarkerObservation::Present(CapturedMarker { marker, file }),
                Err(e) => MarkerObservation::Unavailable(MarkerReadFailure::Marker(e)),
            }
        }
    }
}
/// A decoded marker retaining the exact policy-checked capture. The sample is
/// after the read, not proof of policy during it or exclusion through later use.
/// Directory samples were checked, not retained as an audit history.
#[derive(Debug)]
struct PolicyCapturedMarker {
    marker: DecodedMarker,
    capture: opensip_security::PolicyObservedOperationalFile,
}
#[derive(Debug)]
enum PolicyMarkerReadFailure {
    Capture(opensip_security::PolicyCaptureFailure),
    Marker(MarkerError),
}
#[derive(Debug)]
enum PolicyMarkerObservation {
    Absent,
    Present(PolicyCapturedMarker),
    Unavailable(PolicyMarkerReadFailure),
}
/// Existing root only. Full ancestor/file policy capture precedes marker decoding;
/// failed policy/read is not absence or an admitted marker. UID/groups and expected
/// instance remain assertions requiring a host owner, native qualification and
/// held exclusion/lease. This fixed composition creates, repairs and retries nothing.
/// The unchecked reader below is test-only and cannot be a production entry point.
fn observe_marker(
    root: &opensip_platform::RetainedDirectoryPath,
    expected: &StoreInstance,
    invoking_uid: u32,
    authorized_groups: &std::collections::BTreeSet<u32>,
) -> PolicyMarkerObservation {
    use opensip_security::PolicyOperationalFileObservation as Observation;
    match opensip_security::observe_bound_operational_file_with_policy(
        root,
        MARKER_NAME,
        MARKER_LIMIT,
        invoking_uid,
        authorized_groups,
    ) {
        Observation::Absent => PolicyMarkerObservation::Absent,
        Observation::Unavailable(error) => {
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(error))
        }
        Observation::Present(capture) => {
            // Marker bytes are bounded to128; keep the original File and its sample
            // in capture while the pure codec owns its own exact byte copy.
            match DecodedMarker::decode(capture.captured().bytes().to_vec(), expected) {
                Ok(marker) => {
                    PolicyMarkerObservation::Present(PolicyCapturedMarker { marker, capture })
                }
                Err(error) => {
                    PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Marker(error))
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{
        fs,
        os::unix::fs::{PermissionsExt, symlink},
        path::PathBuf,
    };
    fn id() -> StoreInstance {
        StoreInstance::parse(&"a".repeat(32)).unwrap()
    }
    fn raw(s: &str) -> Vec<u8> {
        format!("{{\"schemaVersion\":1,\"storeInstanceId\":\"{s}\"}}").into_bytes()
    }
    fn valid() -> Vec<u8> {
        raw(&id().0)
    }
    #[test]
    fn exact_product_marker_needs_shape_grammar_canonical_bytes_and_binding() {
        assert_eq!(MARKER_NAME, "store-instance.v1"); //201 fixed leaf; independent of fixtures
        let bytes = valid();
        assert_eq!(bytes.len(), 72);
        let m = DecodedMarker::decode(bytes.clone(), &id()).unwrap();
        assert_eq!(m.instance, id());
        assert_eq!(m.bytes, bytes);
        assert_eq!(
            DecodedMarker::decode(raw(&"b".repeat(32)), &id()).unwrap_err(),
            MarkerError::Binding
        );
        assert_eq!(
            DecodedMarker::decode(raw(&"A".repeat(32)), &id()).unwrap_err(),
            MarkerError::Instance
        );
        for bad in [
            format!("{{\"storeInstanceId\":\"{}\",\"schemaVersion\":1}}", id().0).into_bytes(),
            [bytes.clone(), b"\n".to_vec()].concat(),
            [b" ".to_vec(), bytes.clone()].concat(),
            String::from_utf8(bytes.clone())
                .unwrap()
                .replace("schemaVersion", "\\u0073chemaVersion")
                .into_bytes(),
            String::from_utf8(bytes.clone())
                .unwrap()
                .replacen(":\"a", ":\"\\u0061", 1)
                .into_bytes(),
        ] {
            assert_eq!(
                DecodedMarker::decode(bad, &id()).unwrap_err(),
                MarkerError::NonCanonical
            );
        }
        for s in [
            "",
            "0",
            "null",
            "[]",
            "{}",
            "{\"schemaVersion\":true}",
            "{\"schemaVersion\":1,\"storeInstanceId\":false}",
        ] {
            assert!(DecodedMarker::decode(s.as_bytes().to_vec(), &id()).is_err());
        }
        for s in ["1.0", "2", "0", "true", "null", "-1", "\"1\""] {
            let bad = String::from_utf8(bytes.clone())
                .unwrap()
                .replace(":1,", &format!(":{s},"));
            assert!(DecodedMarker::decode(bad.into_bytes(), &id()).is_err());
        }
        let unknown = String::from_utf8(bytes.clone())
            .unwrap()
            .replace("{", "{\"extra\":0,");
        assert_eq!(
            DecodedMarker::decode(unknown.into_bytes(), &id()).unwrap_err(),
            MarkerError::Shape
        );
        let duplicate = String::from_utf8(bytes.clone())
            .unwrap()
            .replace("{", "{\"schemaVersion\":1,");
        assert_eq!(
            DecodedMarker::decode(duplicate.into_bytes(), &id()).unwrap_err(),
            MarkerError::Decode(CanonicalError::DuplicateKey)
        );
        for raw in [
            vec![0xff],
            vec![0xef, 0xbb, 0xbf],
            vec![b'{', 0, b'}'],
            [bytes.clone(), vec![0]].concat(),
        ] {
            assert!(DecodedMarker::decode(raw, &id()).is_err());
        }
        for n in [127, 128] {
            let mut padded = bytes.clone();
            padded.resize(n, b' ');
            assert_eq!(
                DecodedMarker::decode(padded, &id()).unwrap_err(),
                MarkerError::NonCanonical
            );
        }
        assert_eq!(
            DecodedMarker::decode(vec![b' '; 129], &id()).unwrap_err(),
            MarkerError::Bound
        );
        for s in [
            "".to_owned(),
            "a".repeat(31),
            "a".repeat(33),
            "g".repeat(32),
            "é".repeat(16),
            format!("{}\0", "a".repeat(31)),
            "../".repeat(10),
        ] {
            assert!(StoreInstance::parse(&s).is_err());
        }
    }
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let tag = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
                &opensip_platform::request_entropy().unwrap(),
            ));
            let p = std::env::temp_dir().join(format!("opensip-marker202-{tag}"));
            fs::create_dir(&p).unwrap();
            fs::set_permissions(&p, fs::Permissions::from_mode(0o700)).unwrap();
            Self(fs::canonicalize(p).unwrap())
        }
        fn binding(&self) -> opensip_platform::RetainedDirectoryPath {
            opensip_platform::RetainedDirectoryPath::open(&self.0, 128).unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn actual_marker_reads_preserve_absence_shape_binding_and_bound_causes() {
        let f = Fixture::new();
        let binding = f.binding();
        let path = f.0.join(MARKER_NAME);
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Absent
        ));
        assert!(!path.exists());
        fs::write(&path, valid()).unwrap();
        match observe_unchecked_marker(&binding, &id()) {
            MarkerObservation::Present(m) => {
                assert_eq!(m.marker.bytes, valid());
                assert_eq!(m.marker.instance, id());
            }
            e => panic!("{e:?}"),
        }
        fs::write(&path, raw(&"b".repeat(32))).unwrap();
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::Marker(MarkerError::Binding))
        ));
        fs::write(&path, []).unwrap();
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::Marker(MarkerError::Decode(_)))
        ));
        fs::write(&path, vec![b' '; 129]).unwrap();
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::File(
                OperationalFileReadFailure::Bound
            ))
        ));
        fs::remove_file(&path).unwrap();
        fs::write(f.0.join("other"), valid()).unwrap();
        symlink("other", &path).unwrap();
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::File(
                OperationalFileReadFailure::Io(_)
            ))
        ));
        fs::remove_file(&path).unwrap();
        fs::create_dir(&path).unwrap();
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::File(
                OperationalFileReadFailure::Io(_)
            ))
        ));
    }
    #[test]
    fn renamed_root_cannot_turn_missing_marker_into_absence_or_read_replacement() {
        let f = Fixture::new();
        let binding = f.binding();
        let moved = f.0.with_extension("moved");
        fs::rename(&f.0, &moved).unwrap();
        let _moved = Fixture(moved);
        fs::create_dir(&f.0).unwrap();
        fs::write(f.0.join(MARKER_NAME), valid()).unwrap();
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::File(
                OperationalFileReadFailure::Context
            ))
        ));
    }
    #[test]
    fn captured_marker_keeps_the_read_descriptor_when_the_name_is_replaced() {
        use std::os::unix::fs::MetadataExt;
        let f = Fixture::new();
        let binding = f.binding();
        let path = f.0.join(MARKER_NAME);
        fs::write(&path, valid()).unwrap();
        let original = fs::metadata(&path).unwrap();
        let MarkerObservation::Present(captured) = observe_unchecked_marker(&binding, &id()) else {
            panic!("valid marker observation required");
        };
        // The same EOF-offset oracle covers the marker wrapper as well as the
        // public capture path; it detects a reopen before this method returns.
        use std::io::Seek;
        let mut descriptor = &captured.file;
        assert_eq!(
            descriptor.stream_position().unwrap(),
            captured.marker.bytes.len() as u64
        );
        fs::rename(&path, f.0.join("original-marker")).unwrap();
        fs::write(&path, raw(&"b".repeat(32))).unwrap();
        let retained = captured.file.metadata().unwrap();
        let replacement = fs::metadata(&path).unwrap();
        assert_eq!(
            (retained.dev(), retained.ino()),
            (original.dev(), original.ino())
        );
        assert_ne!(
            (retained.dev(), retained.ino()),
            (replacement.dev(), replacement.ino())
        );
        assert_eq!(captured.marker.bytes, valid());
        assert_eq!(captured.marker.instance, id());
        assert!(matches!(
            observe_unchecked_marker(&binding, &id()),
            MarkerObservation::Unavailable(MarkerReadFailure::Marker(MarkerError::Binding))
        ));
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn marker_policy_uses_original_descriptor_and_supplied_actor() {
        use opensip_security::{CustodyPredicateFailure as P, OperationalFilePolicyFailure as F};
        use std::{collections::BTreeSet, os::unix::fs::MetadataExt};
        let f = Fixture::new();
        let path = f.0.join(MARKER_NAME);
        fs::write(&path, valid()).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o600)).unwrap();
        let MarkerObservation::Present(captured) = observe_unchecked_marker(&f.binding(), &id())
        else {
            panic!("marker capture");
        };
        // Test fixture's uid only: production provenance must be the actor.
        let uid = captured.file.metadata().unwrap().uid();
        let gid = captured.file.metadata().unwrap().gid();
        assert_ne!(uid, 0);
        let groups = BTreeSet::new();
        captured.inspect_file_policy(uid, &groups).unwrap();
        assert!(matches!(
            captured.inspect_file_policy(uid.checked_add(1).unwrap(), &groups),
            Err(F::Predicate(P::ForeignOwner))
        ));
        let moved = f.0.join("retained-marker");
        fs::rename(&path, &moved).unwrap();
        fs::write(&path, valid()).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o600)).unwrap();
        fs::set_permissions(&moved, fs::Permissions::from_mode(0o602)).unwrap();
        assert!(matches!(
            captured.inspect_file_policy(uid, &groups),
            Err(F::Predicate(P::OthersWrite))
        ));
        fs::set_permissions(&moved, fs::Permissions::from_mode(0o620)).unwrap();
        assert!(matches!(
            captured.inspect_file_policy(uid, &groups),
            Err(F::Predicate(P::GroupWrite))
        ));
        captured
            .inspect_file_policy(uid, &BTreeSet::from([gid]))
            .unwrap();
        fs::set_permissions(&moved, fs::Permissions::from_mode(0o600)).unwrap();
        fs::hard_link(&moved, f.0.join("alias")).unwrap();
        assert!(matches!(
            captured.inspect_file_policy(uid, &groups),
            Err(F::Predicate(P::HardLinked))
        ));
        fs::remove_file(f.0.join("alias")).unwrap();
        fs::remove_file(&moved).unwrap();
        assert!(matches!(
            captured.inspect_file_policy(uid, &groups),
            Err(F::Predicate(P::Unlinked))
        ));
        // A fresh replacement is admissible, but cannot stand in for old bytes.
        let MarkerObservation::Present(replacement) = observe_unchecked_marker(&f.binding(), &id())
        else {
            panic!("replacement");
        };
        replacement.inspect_file_policy(uid, &groups).unwrap();
        assert_eq!(captured.marker.bytes, valid());
    }
    #[cfg(target_os = "macos")]
    fn observe_marker_fixture(
        root: &opensip_platform::RetainedDirectoryPath,
        expected: &StoreInstance,
        uid: u32,
        groups: &std::collections::BTreeSet<u32>,
    ) -> PolicyMarkerObservation {
        // Test setup shares OS ancestors with unrelated processes and sibling
        // fixtures. Retry ONLY their sampled descriptor-change refusal, bounded
        // as in the retained-path fixture tests. Production remains one attempt;
        // no policy, name-change, file-read or decoder refusal is retried here.
        for _ in 0..256 {
            let result = observe_marker(root, expected, uid, groups);
            if matches!(
                &result,
                PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(
                    opensip_security::PolicyCaptureFailure::Directory(
                        opensip_security::DirectoryPathPolicyFailure::Descriptor(
                            opensip_platform::DescriptorObservationError::ChangedDuringRead
                        )
                    )
                ))
            ) {
                std::thread::sleep(std::time::Duration::from_millis(1));
                continue;
            }
            return result;
        }
        panic!("shared test ancestors remained unstable within fixture retry bound");
    }
    #[cfg(target_os = "macos")]
    fn policy_fixture() -> Fixture {
        // This OS helper may create its temp directory; used only in test setup.
        let parent = opensip_platform::account_temporary_directory().unwrap();
        let tag = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            &opensip_platform::request_entropy().unwrap(),
        ));
        let path = parent.join(format!("opensip-policy-marker221-{tag}"));
        fs::create_dir(&path).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o700)).unwrap();
        Fixture(fs::canonicalize(path).unwrap())
    }
    #[test]
    #[cfg(target_os = "macos")]
    fn marker_policy_composes_actor_groups_parent_file_and_decode_causes() {
        use opensip_security::{
            CustodyPredicateFailure as R, DirectoryPathPolicyFailure as D,
            OperationalFilePolicyFailure as F, PolicyCaptureFailure as C,
        };
        use std::{collections::BTreeSet, os::unix::fs::MetadataExt};
        let fixture = policy_fixture();
        let root = fixture.binding();
        let account = opensip_platform::observe_account().unwrap();
        // Actual account producer supplies this test's uid; still not a host grant.
        let uid = account.real_uid();
        assert_eq!(uid, account.effective_uid());
        assert_ne!(uid, 0);
        let groups = BTreeSet::new();
        let expected = id();
        let observe =
            |uid, groups: &BTreeSet<u32>| observe_marker_fixture(&root, &expected, uid, groups);
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Absent
        ));
        let file = fixture.0.join("store-instance.v1");
        fs::write(&file, valid()).unwrap();
        fs::set_permissions(&file, fs::Permissions::from_mode(0o600)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Present(_)
        ));
        assert!(matches!(
            observe(uid.checked_add(1).unwrap(), &groups),
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(C::Directory(
                D::Predicate {
                    refusal: R::ForeignOwner,
                    ..
                }
            )))
        ));
        fs::set_permissions(&file, fs::Permissions::from_mode(0o602)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(C::File(
                F::Predicate(R::OthersWrite)
            )))
        ));
        fs::set_permissions(&file, fs::Permissions::from_mode(0o620)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(C::File(
                F::Predicate(R::GroupWrite)
            )))
        ));
        let allowed = BTreeSet::from([fs::metadata(&file).unwrap().gid()]);
        assert!(matches!(
            observe(uid, &allowed),
            PolicyMarkerObservation::Present(_)
        ));
        fs::set_permissions(&file, fs::Permissions::from_mode(0o600)).unwrap();
        fs::write(&file, raw(&"b".repeat(32))).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Marker(
                MarkerError::Binding
            ))
        ));
        // Pin the composition's exact128-byte read budget independently of its
        // constant: below/equal limit reaches the decoder;129 fails the read.
        for length in [73, 127, 128] {
            let mut padded = valid();
            padded.resize(length, b' ');
            fs::write(&file, padded).unwrap();
            assert!(matches!(
                observe(uid, &groups),
                PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Marker(
                    MarkerError::NonCanonical
                ))
            ));
        }
        fs::write(&file, vec![b'x'; 129]).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(C::Read(_)))
        ));
        fs::remove_file(&file).unwrap();
        fs::set_permissions(&fixture.0, fs::Permissions::from_mode(0o770)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyMarkerObservation::Unavailable(PolicyMarkerReadFailure::Capture(C::Directory(
                D::Predicate {
                    refusal: R::GroupWrite,
                    ..
                }
            )))
        ));
        let directory_groups = BTreeSet::from([fs::metadata(&fixture.0).unwrap().gid()]);
        assert!(matches!(
            observe(uid, &directory_groups),
            PolicyMarkerObservation::Absent
        ));
        fs::set_permissions(&fixture.0, fs::Permissions::from_mode(0o700)).unwrap();
    }
    #[test]
    #[cfg(target_os = "macos")]
    fn policy_marker_retains_original_file_bytes_sample_and_shared_offset() {
        use std::{collections::BTreeSet, io::Seek, os::unix::fs::MetadataExt};
        let fixture = policy_fixture();
        let root = fixture.binding();
        let path = fixture.0.join("store-instance.v1");
        fs::write(&path, valid()).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o600)).unwrap();
        let account = opensip_platform::observe_account().unwrap();
        let PolicyMarkerObservation::Present(observed) =
            observe_marker_fixture(&root, &id(), account.real_uid(), &BTreeSet::new())
        else {
            panic!("owned marker must pass")
        };
        assert_eq!(observed.marker.instance, id());
        assert_eq!(observed.marker.bytes, valid());
        assert_eq!(observed.capture.captured().bytes(), valid());
        assert_eq!(
            observed
                .capture
                .captured()
                .file()
                .try_clone()
                .unwrap()
                .stream_position()
                .unwrap(),
            72
        );
        let ino = observed.capture.descriptor().metadata.inode;
        fs::rename(&path, fixture.0.join("old-marker")).unwrap();
        fs::write(&path, raw(&"b".repeat(32))).unwrap();
        assert_ne!(fs::metadata(&path).unwrap().ino(), ino);
        assert_eq!(
            observed.capture.captured().file().metadata().unwrap().ino(),
            ino
        );
        assert_eq!(observed.capture.captured().bytes(), valid());
    }
}

#[cfg(target_os = "macos")]
pub(crate) mod native_marker;
