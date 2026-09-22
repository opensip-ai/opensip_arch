// Supplied-path native state.v1 capture and P2-local joins. This does not select
// I/S, qualify a filesystem, complete a successor census or grant authority.
use super::{
    current_record_bindings::{self, CurrentRecordBindings},
    directory_record_capture as files,
    native_record_capture::{self as immutable, NativeStore},
    retained_metadata_index::{self as M, Budget, Collection},
};
use crate::{
    custody::{
        directory_policy, inspect_operational_file, installation_fence::SuppliedInstallationFence,
    },
    trust::{
        trust_record_reader::{self, Record, RecordKind},
        trust_record_shapes::{self as shapes, Definition},
    },
};
use opensip_identity::{JsonValue as V, canonical_bytes};
use opensip_platform::{DescriptorObservation, RetainedChildDirectory};
use std::{collections::BTreeMap, ffi::OsStr, fs::File, sync::Arc};
#[derive(Debug)]
pub(super) enum Error {
    Budget(M::Error),
    Reference,
    Shape(shapes::Error),
    Record(trust_record_reader::Error),
    Fence(crate::custody::installation_fence::Error),
    Directory(crate::custody::DirectoryPathRefusal),
    Native(std::io::Error),
    File(crate::custody::NativeRefusal),
    Capture(files::Error),
    Changed,
    Store,
    Immutable(immutable::Error),
    Bindings(current_record_bindings::Error),
    Successors(super::directory_provers::Error),
}
impl From<M::Error> for Error {
    fn from(e: M::Error) -> Self {
        Self::Budget(e)
    }
}
fn object(v: &V) -> Result<&BTreeMap<String, V>, Error> {
    if let V::Object(o) = v {
        Ok(o)
    } else {
        Err(Error::Reference)
    }
}
pub(super) fn store_id(expected: &V) -> Result<&str, Error> {
    let o = object(expected)?;
    if o.len() != 3
        || !matches!(o.get("stateSchema"), Some(V::Integer(_)))
        || !matches!(o.get("storeGeneration"), Some(V::Integer(_)))
    {
        return Err(Error::Reference);
    }
    let Some(V::String(id)) = o.get("storeInstanceId") else {
        return Err(Error::Reference);
    };
    if id.len() != 32 {
        return Err(Error::Reference);
    }
    shapes::admit(
        Definition::StoreBinding,
        &canonical_bytes(expected).map_err(|_| Error::Reference)?,
    )
    .map_err(Error::Shape)?;
    Ok(id)
}
fn check(
    fence: &SuppliedInstallationFence,
    dirs: &[Arc<RetainedChildDirectory>],
) -> Result<(), Error> {
    fence.recheck().map_err(Error::Fence)?;
    let (uid, groups) = fence.supplied_actor();
    for dir in dirs {
        directory_policy::inspect(dir, uid, groups).map_err(Error::Directory)?;
    }
    fence.recheck().map_err(Error::Fence)
}
pub(super) struct Head<'f> {
    fence: &'f SuppliedInstallationFence,
    dirs: Vec<Arc<RetainedChildDirectory>>,
    file: File,
    observation: DescriptorObservation,
    raw: Arc<[u8]>,
    record: Record,
}
impl Head<'_> {
    pub(super) fn visit_filesystems(
        &self,
        visit: &mut impl FnMut(&opensip_platform::DescriptorFilesystem) -> std::io::Result<()>,
    ) -> Result<(), Error> {
        self.recheck()?;
        for edge in &self.dirs {
            for fs in edge.observe_filesystems().map_err(Error::Native)? {
                visit(&fs).map_err(Error::Native)?;
            }
        }
        visit(&opensip_platform::observe_filesystem(&self.file).map_err(Error::Native)?)
            .map_err(Error::Native)?;
        self.recheck()
    }
    pub(super) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(super) fn value(&self) -> &V {
        self.record.value()
    }
    pub(super) fn recheck(&self) -> Result<(), Error> {
        check(self.fence, &self.dirs)?;
        let (uid, groups) = self.fence.supplied_actor();
        let now = inspect_operational_file(&self.file, uid, groups).map_err(Error::File)?;
        files::check_name(
            self.dirs.last().ok_or(Error::Reference)?,
            "state.v1",
            &self.file,
        )
        .map_err(Error::Capture)?;
        if now.metadata != self.observation.metadata
            || now.possible_acl_writers != self.observation.possible_acl_writers
        {
            return Err(Error::Changed);
        }
        check(self.fence, &self.dirs)
    }
}
pub(super) fn capture_head<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    expected_store: &V,
) -> Result<Head<'f>, Error> {
    capture_head_with(b, fence, expected_store, || {})
}
fn capture_head_with<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    expected_store: &V,
    after_read: impl FnOnce(),
) -> Result<Head<'f>, Error> {
    b.scope(|b| {
        let sid = store_id(expected_store)?;
        let (uid, groups) = fence.supplied_actor();
        let mut dirs: Vec<Arc<RetainedChildDirectory>> = Vec::new();
        check(fence, &dirs)?;
        for component in ["trust", "stores", sid] {
            b.edge(1)?;
            let parent = dirs
                .last()
                .map(|d| d.directory())
                .unwrap_or_else(|| fence.root().directory());
            let opened = parent.bind_child_directory(OsStr::new(component));
            check(fence, &dirs)?;
            let dir = Arc::new(opened.map_err(Error::Native)?);
            directory_policy::inspect(&dir, uid, groups).map_err(Error::Directory)?;
            b.directory(Arc::clone(&dir))?;
            dirs.push(dir);
        }
        b.edge(1)?;
        let parent = dirs.last().ok_or(Error::Reference)?;
        let mut held = None;
        let mut failure = None;
        let captured = b.capture_current(parent, |cap| {
            match files::read_one(parent, "state.v1", cap, uid, groups, |_| {}) {
                Ok((file, raw, observation)) => {
                    held = Some((file, observation));
                    Ok(raw)
                }
                Err(e) => {
                    failure = Some(e);
                    Err(())
                }
            }
        });
        let raw = match captured {
            Ok(raw) => raw,
            Err(e) => return Err(failure.map(Error::Capture).unwrap_or(Error::Budget(e))),
        };
        let (file, observation) = held.ok_or(Error::Reference)?;
        after_read();
        let record =
            Record::parse(RecordKind::TrustCapsuleV1, &raw, 131072).map_err(Error::Record)?;
        if object(record.value())?.get("store") != Some(expected_store) {
            return Err(Error::Store);
        }
        let head = Head {
            fence,
            dirs,
            file,
            observation,
            raw,
            record,
        };
        head.recheck()?;
        Ok(head)
    })
}
/// Keeps native current and immutable dependency Files with the borrowed fence.
/// Local P2 joins only; complete qualified census and authority remain separate.
pub(super) struct SuppliedP2Current<'f> {
    head: Head<'f>,
    store: NativeStore<'f>,
    descriptor: Record,
    bindings: CurrentRecordBindings,
}
impl SuppliedP2Current<'_> {
    pub(super) fn visit_filesystems(
        &self,
        visit: &mut impl FnMut(&opensip_platform::DescriptorFilesystem) -> std::io::Result<()>,
    ) -> Result<(), Error> {
        self.recheck()?;
        self.head.visit_filesystems(visit)?;
        self.store
            .visit_filesystems(visit)
            .map_err(Error::Immutable)?;
        self.recheck()
    }
    /// Uses this actual current head and its owned native dependency store; does
    /// not accept a replacement materialized BEFORE or foreign byte callback.
    pub(super) fn observe_successors(
        &mut self,
        b: &mut Budget,
        root: Arc<RetainedChildDirectory>,
        foreign: impl FnMut(&[u8]) -> Result<(), ()>,
    ) -> Result<super::directory_provers::Observed, Error> {
        b.scope(|b| {
            self.recheck()?;
            let (uid, groups) = self.head.fence.supplied_actor();
            let observed = super::directory_provers::observe(
                b,
                self.head.value(),
                root,
                uid,
                groups,
                &mut self.store,
                foreign,
            )
            .map_err(Error::Successors)?;
            self.recheck()?;
            Ok(observed)
        })
    }

    pub(super) fn head(&self) -> &Head<'_> {
        &self.head
    }
    pub(super) fn descriptor(&self) -> &Record {
        &self.descriptor
    }
    pub(super) fn bindings(&self) -> &CurrentRecordBindings {
        &self.bindings
    }
    pub(super) fn recheck(&self) -> Result<(), Error> {
        self.head.recheck()?;
        self.store.recheck().map_err(Error::Immutable)?;
        self.head.recheck()
    }
}
pub(super) fn capture_p2<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    expected_store: &V,
) -> Result<SuppliedP2Current<'f>, Error> {
    b.scope(|b| {
        let head = capture_head(b, fence, expected_store)?;
        let c = object(head.value())?;
        let publication = &c["publication"];
        let initial = (object(publication)?["previousCapsule"] == V::Null)
            .then_some(&object(&c["store"])?["storeInstanceId"]);
        let mut store = immutable::NativeStore::new(fence);
        let loaded = b.load_at(Collection::Publications, publication, initial, &mut store);
        let raw = store.complete(loaded).map_err(|e| match e {
            immutable::ReadCompletionError::Native(source) => Error::Immutable(source),
            immutable::ReadCompletionError::Logical(source) => Error::Budget(source),
        })?;
        let trust_record_reader::Decoded::Record(descriptor) = head
            .record
            .decode_at("/publication", &raw)
            .map_err(Error::Record)?
        else {
            return Err(Error::Reference);
        };
        let bindings = current_record_bindings::bind(
            b,
            expected_store,
            head.value(),
            descriptor.value(),
            &mut store,
        );
        let bindings = store.complete(bindings).map_err(|e| match e {
            immutable::ReadCompletionError::Native(source) => Error::Immutable(source),
            immutable::ReadCompletionError::Logical(source) => Error::Bindings(source),
        })?;
        let result = SuppliedP2Current {
            head,
            store,
            descriptor,
            bindings,
        };
        result.recheck()?;
        Ok(result)
    })
}

#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use opensip_identity::{JsonInteger, digest_hex, parse_json, raw_sha256};
    use opensip_platform::RetainedDirectoryPath;
    use std::{
        collections::BTreeSet,
        fs::{self, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt, symlink},
        path::{Path, PathBuf},
    };
    const SID: &str = "11111111111111111111111111111111";
    fn o(v: &V) -> &BTreeMap<String, V> {
        object(v).unwrap()
    }
    fn arr(v: &V) -> &[V] {
        let V::Array(a) = v else { panic!("array") };
        a
    }
    fn text(v: &V) -> &str {
        let V::String(s) = v else { panic!("string") };
        s
    }
    fn bytes(v: &V) -> Vec<u8> {
        text(v)
            .as_bytes()
            .chunks_exact(2)
            .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
            .collect()
    }
    fn budget() -> Budget {
        Budget::new(65536, 131072, 268435456).unwrap()
    }
    struct Fixture {
        root: PathBuf,
        path: Arc<RetainedDirectoryPath>,
        uid: u32,
    }
    impl Fixture {
        fn new() -> Self {
            let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
            let root = std::env::temp_dir().join(format!("opensip-native-current-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let root = fs::canonicalize(root).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            fs::write(root.join("lifecycle.fence"), b"").unwrap();
            fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600))
                .unwrap();
            let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
            Self { root, path, uid }
        }
        fn write(&self, rel: &str, raw: &[u8]) -> PathBuf {
            let mut p = self.root.clone();
            for component in Path::new(rel).parent().unwrap().components() {
                p.push(component);
                if !p.exists() {
                    fs::create_dir(&p).unwrap();
                }
                fs::set_permissions(&p, Permissions::from_mode(0o700)).unwrap();
            }
            let p = self.root.join(rel);
            fs::write(&p, raw).unwrap();
            fs::set_permissions(&p, Permissions::from_mode(0o600)).unwrap();
            p
        }
        fn fence(&self) -> SuppliedInstallationFence {
            SuppliedInstallationFence::try_acquire(
                Arc::clone(&self.path),
                self.uid,
                &BTreeSet::new(),
            )
            .unwrap()
            .unwrap()
        }
        fn current(&self, raw: &[u8]) -> PathBuf {
            self.write(&format!("trust/stores/{SID}/state.v1"), raw)
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    fn sample() -> (Vec<u8>, V) {
        let q = parse_json(
            include_bytes!("../../tests/fixtures/captured-capsule306.ndjson")
                .split(|b| *b == b'\n')
                .find(|l| !l.is_empty())
                .unwrap(),
        )
        .unwrap();
        let q = o(&q);
        let expected = o(&o(&arr(&q["outcomes"])[0])["expected"]);
        let c = &expected["capsule"];
        (canonical_bytes(c).unwrap(), o(c)["store"].clone())
    }
    #[test]
    fn native_current_exact_path_original_file_and_shared_capacity() {
        let (raw, expected) = sample();
        assert_eq!(raw.len(), 1435);
        let f = Fixture::new();
        f.current(&raw);
        let fence = f.fence();
        for (limits, okay) in [
            ((4, 7, 1435), true),
            ((3, 7, 1435), false),
            ((4, 6, 1435), false),
            ((4, 7, 1434), false),
        ] {
            let mut b = Budget::new(limits.0, limits.1, limits.2).unwrap();
            let got = capture_head(&mut b, &fence, &expected);
            assert_eq!(got.is_ok(), okay, "{limits:?}: {:?}", got.as_ref().err());
            if let Ok(head) = got {
                assert_eq!(head.raw(), raw);
                assert_eq!(o(head.value())["store"], expected);
                head.recheck().unwrap();
                assert_eq!(b.counters(), limits);
            } else {
                assert!(matches!(b.edge(1), Err(M::Error::Closed)));
            }
        }
        let mut b = budget();
        b.retain(Collection::Objects, b"x").unwrap();
        let head = capture_head(&mut b, &fence, &expected).unwrap();
        assert_eq!(b.counters(), (5, 7, 1436));
        head.recheck().unwrap();
    }
    #[test]
    fn native_current_is_distinct_from_historical_records_and_cache_never_proves_presence() {
        let (raw, expected) = sample();
        let f = Fixture::new();
        let file = f.current(&raw);
        f.write(
            &format!("trust/records/{}", digest_hex(&raw_sha256(&raw))),
            &raw,
        );
        let fence = f.fence();
        let mut b = budget();
        let first = capture_head(&mut b, &fence, &expected).unwrap();
        let second = capture_head(&mut b, &fence, &expected).unwrap();
        assert!(Arc::ptr_eq(&first.raw, &second.raw));
        assert_eq!(b.counters(), (4, 14, 1435));
        b.retain(Collection::Records, &raw).unwrap();
        assert_eq!(b.counters(), (5, 14, 2870));
        fs::remove_file(file).unwrap();
        assert!(capture_head(&mut b, &fence, &expected).is_err());
        assert!(first.recheck().is_err());
        assert!(matches!(b.edge(1), Err(M::Error::Closed)));
    }
    #[test]
    fn native_current_shape_full_store_and_changed_cached_bytes_refuse() {
        let (raw, expected) = sample();
        let f = Fixture::new();
        let file = f.current(&raw);
        let fence = f.fence();
        let mut malformed = o(&expected).clone();
        malformed.insert("extra".into(), V::String("x".repeat(1048576)));
        let mut b = budget();
        assert!(capture_head(&mut b, &fence, &V::Object(malformed)).is_err());
        assert_eq!(b.counters(), (0, 0, 0));
        let mut invalid = o(&expected).clone();
        invalid.insert("storeInstanceId".into(), V::String("g".repeat(32)));
        let mut b = budget();
        assert!(capture_head(&mut b, &fence, &V::Object(invalid)).is_err());
        assert_eq!(b.counters(), (0, 0, 0));
        // Current entries consume the same capacity as later immutable reads.
        let mut capped = Budget::new(4, 20, 1436).unwrap();
        capture_head(&mut capped, &fence, &expected).unwrap();
        assert!(matches!(
            capped.retain(Collection::Objects, b"x"),
            Err(M::Error::ObjectLimit)
        ));
        let mut other = o(&expected).clone();
        other.insert(
            "storeGeneration".into(),
            V::Integer(JsonInteger::new(1).unwrap()),
        );
        let mut b = budget();
        assert!(matches!(
            capture_head(&mut b, &fence, &V::Object(other)),
            Err(Error::Store)
        ));
        let mut b = budget();
        let head = capture_head(&mut b, &fence, &expected).unwrap();
        fs::write(file, b"bad").unwrap();
        assert!(matches!(
            capture_head(&mut b, &fence, &expected),
            Err(Error::Budget(M::Error::Digest))
        ));
        assert!(head.recheck().is_err());
    }
    #[test]
    fn native_current_postread_file_parent_root_and_fence_changes_refuse() {
        let (raw, expected) = sample();
        for change in ["file", "parent", "root", "fence"] {
            let f = Fixture::new();
            let file = f.current(&raw);
            let fence = f.fence();
            let mut b = budget();
            let result = capture_head_with(&mut b, &fence, &expected, || match change {
                "file" => fs::write(&file, b"bad").unwrap(),
                "parent" => {
                    let parent = file.parent().unwrap();
                    fs::rename(parent, f.root.join("old-store")).unwrap();
                    fs::create_dir(parent).unwrap();
                    fs::set_permissions(parent, Permissions::from_mode(0o700)).unwrap();
                }
                "root" => fs::set_permissions(&f.root, Permissions::from_mode(0o777)).unwrap(),
                "fence" => {
                    fs::rename(f.root.join("lifecycle.fence"), f.root.join("old-fence")).unwrap();
                    fs::write(f.root.join("lifecycle.fence"), b"").unwrap();
                    fs::set_permissions(
                        f.root.join("lifecycle.fence"),
                        Permissions::from_mode(0o600),
                    )
                    .unwrap();
                }
                _ => unreachable!(),
            });
            assert!(result.is_err(), "{change}");
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
        }
    }
    #[test]
    fn native_current_absence_case_alias_symlink_mode_and_hardlink_never_become_genesis() {
        let (raw, expected) = sample();
        for change in ["absent", "case", "symlink", "mode", "hardlink"] {
            let f = Fixture::new();
            let file = f.current(&raw);
            match change {
                "absent" => fs::remove_file(&file).unwrap(),
                "case" => fs::rename(&file, file.with_file_name("STATE.V1")).unwrap(),
                "symlink" => {
                    fs::remove_file(&file).unwrap();
                    symlink("missing", &file).unwrap();
                }
                "mode" => fs::set_permissions(&file, Permissions::from_mode(0o666)).unwrap(),
                "hardlink" => fs::hard_link(&file, file.with_file_name("other")).unwrap(),
                _ => unreachable!(),
            }
            let fence = f.fence();
            let mut b = budget();
            assert!(capture_head(&mut b, &fence, &expected).is_err(), "{change}");
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
        }
    }
    fn write_rows(f: &Fixture, rows: &V) {
        for row in arr(rows) {
            let r = o(row);
            let raw = bytes(&r["rawHex"]);
            let hash = text(&r["sha256"]);
            let rel = match text(&r["collection"]) {
                "records" => format!("trust/records/{hash}"),
                "objects" => format!("trust/objects/{hash}"),
                "events" => {
                    let v = parse_json(&raw).unwrap();
                    let v = o(&v);
                    let V::Integer(n) = &v["sequence"] else {
                        panic!()
                    };
                    format!(
                        "trust/stores/{}/events/{}-{hash}",
                        text(&v["store"]),
                        n.get()
                    )
                }
                _ => panic!("unexpected collection"),
            };
            f.write(&rel, &raw);
        }
    }
    #[test]
    fn native_current_p2_composite_joins_actual_head_descriptor_events_and_keeps_custody() {
        let mut positives = 0;
        for line in include_bytes!("../../tests/fixtures/current-bindings328.ndjson")
            .split(|b| *b == b'\n')
            .filter(|l| !l.is_empty())
        {
            let q = parse_json(line).unwrap();
            let q = o(&q);
            if o(&arr(&q["outcomes"])[0])["ok"] != V::Bool(true) {
                continue;
            }
            let f = Fixture::new();
            let raw = canonical_bytes(&q["capsule"]).unwrap();
            let sid = text(&o(&q["expectedStore"])["storeInstanceId"]);
            let current = f.write(&format!("trust/stores/{sid}/state.v1"), &raw);
            write_rows(&f, &q["store"]);
            let d = canonical_bytes(&q["descriptor"]).unwrap();
            let h = digest_hex(&raw_sha256(&d));
            let previous = &o(&q["descriptor"])["previousCapsule"];
            let rel = if previous == &V::Null {
                format!("trust/publications/initial/{sid}/{h}")
            } else {
                format!("trust/publications/by-predecessor/{}/{h}", text(previous))
            };
            let descriptor = f.write(&rel, &d);
            let fence = f.fence();
            let mut b = budget();
            let result = capture_p2(&mut b, &fence, &q["expectedStore"]).unwrap();
            assert_eq!(result.head().raw(), raw);
            assert_eq!(result.descriptor().value(), &q["descriptor"]);
            assert_eq!(result.bindings().projection().capsule(), &q["capsule"]);
            result.recheck().unwrap();
            if positives == 0 {
                // Eight unique directories plus current/D/operation/event. Work:
                // current7 + D10 + operation6 once + event10. Bytes are fixed
                // fixture lengths 4206+4957+402+789, not measured from this result.
                assert_eq!(b.counters(), (12, 33, 10354));
                for (limits, okay) in [
                    ((12, 33, 10354), true),
                    ((11, 33, 10354), false),
                    ((12, 32, 10354), false),
                    ((12, 33, 10353), false),
                ] {
                    let mut limited = Budget::new(limits.0, limits.1, limits.2).unwrap();
                    let got = capture_p2(&mut limited, &fence, &q["expectedStore"]);
                    assert_eq!(got.is_ok(), okay, "{limits:?}: {:?}", got.as_ref().err());
                }
            }
            if positives % 2 == 0 {
                fs::remove_file(current).unwrap();
            } else {
                fs::remove_file(descriptor).unwrap();
            }
            assert!(result.recheck().is_err());
            positives += 1;
            if positives == 3 {
                break;
            }
        }
        assert_eq!(positives, 3);
        let (raw, expected) = sample();
        let f = Fixture::new();
        f.current(&raw);
        let q = parse_json(
            include_bytes!("../../tests/fixtures/captured-capsule306.ndjson")
                .split(|b| *b == b'\n')
                .find(|l| !l.is_empty())
                .unwrap(),
        )
        .unwrap();
        let result = o(&o(&arr(&o(&q)["outcomes"])[0])["expected"]);
        let descriptor = canonical_bytes(&result["descriptor"]).unwrap();
        f.write(
            &format!(
                "trust/publications/initial/{SID}/{}",
                digest_hex(&raw_sha256(&descriptor))
            ),
            &descriptor,
        );
        let fence = f.fence();
        let mut b = budget();
        assert!(matches!(
            capture_p2(&mut b, &fence, &expected),
            Err(Error::Bindings(current_record_bindings::Error::Phase))
        ));
    }
}
