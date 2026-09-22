// Full-reference native reads under a borrowed supplied installation fence.
// No digest-only search, mutable current capture, semantic admission or authority.
use super::{
    directory_record_capture,
    retained_metadata_index::{self as M, Budget, Collection},
};
use crate::{
    custody::{
        DirectoryPathRefusal, NativeRefusal, directory_policy, inspect_operational_file,
        installation_fence::{self, SuppliedInstallationFence},
    },
    trust::trust_record_shapes::{self as shapes, Definition},
};
use opensip_identity::{JsonValue as V, canonical_bytes};
use opensip_platform::{DescriptorObservation, RetainedChildDirectory};
use std::{collections::BTreeMap, ffi::OsStr, fs::File, io, sync::Arc};
#[derive(Debug)]
pub(super) enum Error {
    Budget(M::Error),
    Reference,
    Shape(shapes::Error),
    Fence(installation_fence::Error),
    Directory(DirectoryPathRefusal),
    File(NativeRefusal),
    Capture(directory_record_capture::Error),
    Native(io::Error),
    Length,
    Changed,
}
impl From<M::Error> for Error {
    fn from(e: M::Error) -> Self {
        Self::Budget(e)
    }
}
struct Locator {
    collection: Collection,
    reference: V,
    initial_store: Option<V>,
    digest: [u8; 32],
    length: usize,
    parents: Vec<String>,
    leaf: String,
}
fn object(v: &V) -> Result<&BTreeMap<String, V>, Error> {
    if let V::Object(o) = v {
        Ok(o)
    } else {
        Err(Error::Reference)
    }
}
fn string(v: &V) -> Result<&str, Error> {
    if let V::String(s) = v {
        Ok(s)
    } else {
        Err(Error::Reference)
    }
}
fn shape(d: Definition, v: &V) -> Result<(), Error> {
    shapes::admit(d, &canonical_bytes(v).map_err(|_| Error::Reference)?)
        .map(|_| ())
        .map_err(Error::Shape)
}
pub(super) fn reference_parts(
    collection: Collection,
    reference: &V,
    initial_store: Option<&V>,
) -> Result<([u8; 32], usize), Error> {
    let o = object(reference)?;
    let (definition, keys): (_, &[&str]) = match collection {
        Collection::Objects => (Definition::BlobRef, &["sha256", "bytes"]),
        Collection::Records => (Definition::NodeRef, &["sha256", "bytes"]),
        Collection::Events => (
            Definition::EventRef,
            &["sha256", "bytes", "storeInstanceId", "sequence"],
        ),
        Collection::Publications => (
            Definition::PublicationRef,
            &["sha256", "bytes", "previousCapsule"],
        ),
    };
    // Bound the materialized reference's shape before encoding it. No large
    // extra field or unbounded string can cause a reference allocation here.
    if o.len() != keys.len() || keys.iter().any(|k| !o.contains_key(*k)) {
        return Err(Error::Reference);
    }
    let sha = string(&o["sha256"])?;
    if sha.len() != 64 || !matches!(&o["bytes"], V::Integer(_)) {
        return Err(Error::Reference);
    }
    if collection == Collection::Events
        && (string(&o["storeInstanceId"])?.len() != 32 || !matches!(&o["sequence"], V::Integer(_)))
    {
        return Err(Error::Reference);
    }
    if collection == Collection::Publications
        && o["previousCapsule"] != V::Null
        && string(&o["previousCapsule"])?.len() != 64
    {
        return Err(Error::Reference);
    }
    if let Some(store) = initial_store {
        if string(store)?.len() != 32 {
            return Err(Error::Reference);
        }
        shape(Definition::StoreId, store)?;
    }
    shape(definition, reference)?;
    let physical = V::Object(
        [
            ("sha256".into(), o["sha256"].clone()),
            ("bytes".into(), o["bytes"].clone()),
        ]
        .into(),
    );
    let (digest, length) = M::reference_fields(&physical).ok_or(Error::Reference)?;
    if initial_store.is_some()
        && !(collection == Collection::Publications && o["previousCapsule"] == V::Null)
    {
        return Err(Error::Reference);
    }
    Ok((digest, length))
}
impl Locator {
    fn new(
        collection: Collection,
        reference: &V,
        initial_store: Option<&V>,
    ) -> Result<Self, Error> {
        let (digest, length) = reference_parts(collection, reference, initial_store)?;
        let o = object(reference)?;
        let sha = string(&o["sha256"])?;
        let mut parents = vec!["trust".into()];
        let mut leaf = sha.to_owned();
        match collection {
            Collection::Objects => parents.push("objects".into()),
            Collection::Records => parents.push("records".into()),
            Collection::Events => {
                parents.extend([
                    "stores".into(),
                    string(&o["storeInstanceId"])?.into(),
                    "events".into(),
                ]);
                let V::Integer(sequence) = &o["sequence"] else {
                    unreachable!()
                };
                leaf = format!("{}-{sha}", sequence.get());
            }
            Collection::Publications => {
                parents.push("publications".into());
                if o["previousCapsule"] == V::Null {
                    let store = initial_store.ok_or(Error::Reference)?;
                    parents.extend(["initial".into(), string(store)?.into()]);
                } else {
                    parents.extend([
                        "by-predecessor".into(),
                        string(&o["previousCapsule"])?.into(),
                    ]);
                }
            }
        }
        if initial_store.is_some()
            && !(collection == Collection::Publications && o["previousCapsule"] == V::Null)
        {
            return Err(Error::Reference);
        }
        Ok(Self {
            collection,
            reference: reference.clone(),
            initial_store: initial_store.cloned(),
            digest,
            length,
            parents,
            leaf,
        })
    }
}
pub(super) struct Captured<'f> {
    fence: &'f SuppliedInstallationFence,
    locator: Locator,
    directories: Vec<Arc<RetainedChildDirectory>>,
    file: File,
    raw: Arc<[u8]>,
    observation: DescriptorObservation,
}
fn check_prefix(
    fence: &SuppliedInstallationFence,
    dirs: &[Arc<RetainedChildDirectory>],
) -> Result<(), Error> {
    fence.recheck().map_err(Error::Fence)?;
    let (uid, groups) = fence.supplied_actor();
    for edge in dirs {
        directory_policy::inspect(edge, uid, groups).map_err(Error::Directory)?;
    }
    fence.recheck().map_err(Error::Fence)?;
    Ok(())
}
impl Captured<'_> {
    pub(super) fn visit_filesystems(
        &self,
        visit: &mut impl FnMut(&opensip_platform::DescriptorFilesystem) -> std::io::Result<()>,
    ) -> Result<(), Error> {
        self.recheck()?;
        for edge in &self.directories {
            for fs in edge.observe_filesystems().map_err(Error::Native)? {
                visit(&fs).map_err(Error::Native)?;
            }
        }
        visit(&opensip_platform::observe_filesystem(&self.file).map_err(Error::Native)?)
            .map_err(Error::Native)?;
        self.recheck()
    }
    pub(super) fn shared_raw(&self) -> Arc<[u8]> {
        Arc::clone(&self.raw)
    }
    pub(super) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(super) fn file(&self) -> &File {
        &self.file
    }
    pub(super) fn reference(&self) -> &V {
        &self.locator.reference
    }
    pub(super) fn initial_store(&self) -> Option<&V> {
        self.locator.initial_store.as_ref()
    }
    pub(super) fn collection(&self) -> Collection {
        self.locator.collection
    }
    pub(super) fn recheck(&self) -> Result<(), Error> {
        check_prefix(self.fence, &self.directories)?;
        let (uid, groups) = self.fence.supplied_actor();
        let observed = inspect_operational_file(&self.file, uid, groups).map_err(Error::File)?;
        directory_record_capture::check_name(
            self.directories.last().ok_or(Error::Reference)?,
            &self.locator.leaf,
            &self.file,
        )
        .map_err(Error::Capture)?;
        if observed.metadata != self.observation.metadata
            || observed.possible_acl_writers != self.observation.possible_acl_writers
        {
            return Err(Error::Changed);
        }
        check_prefix(self.fence, &self.directories)?;
        Ok(())
    }
}
pub(super) fn capture<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    collection: Collection,
    reference: &V,
    initial_store: Option<&V>,
) -> Result<Captured<'f>, Error> {
    capture_with(b, fence, collection, reference, initial_store, || {})
}
fn capture_with<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    collection: Collection,
    reference: &V,
    initial_store: Option<&V>,
    after_read: impl FnOnce(),
) -> Result<Captured<'f>, Error> {
    b.scope(|b| {
        let locator = Locator::new(collection, reference, initial_store)?;
        let (uid, groups) = fence.supplied_actor();
        let mut dirs: Vec<Arc<RetainedChildDirectory>> = Vec::new();
        check_prefix(fence, &dirs)?;
        for name in &locator.parents {
            b.edge(1)?;
            let parent = dirs
                .last()
                .map(|d| d.directory())
                .unwrap_or_else(|| fence.root().directory());
            let opened = parent.bind_child_directory(OsStr::new(name));
            check_prefix(fence, &dirs)?;
            let edge = Arc::new(opened.map_err(Error::Native)?);
            directory_policy::inspect(&edge, uid, groups).map_err(Error::Directory)?;
            b.directory(Arc::clone(&edge))?;
            dirs.push(edge);
        }
        b.edge(1)?;
        let mut retained = None;
        let mut failure = None;
        let captured = b.capture(collection, locator.digest, true, |cap| {
            match directory_record_capture::read_one(
                dirs.last().unwrap(),
                &locator.leaf,
                cap.min(locator.length),
                uid,
                groups,
                |_| {},
            ) {
                Ok((file, raw, observation)) => {
                    retained = Some((file, observation));
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
        if raw.len() != locator.length {
            return Err(Error::Length);
        }
        let (file, observation) = retained.ok_or(Error::Reference)?;
        after_read();
        let captured = Captured {
            fence,
            locator,
            directories: dirs,
            file,
            raw,
            observation,
        };
        captured.recheck()?;
        Ok(captured)
    })
}
/// Operation-local adapter; retained files and borrowed fence must live through
/// the caller's evidence consumption. Returned structural values are not grants.
#[derive(Debug)]
pub(super) enum ReadCompletionError<E> {
    Native(Error),
    Logical(E),
}
pub(super) struct NativeStore<'f> {
    fence: &'f SuppliedInstallationFence,
    captures: Vec<Captured<'f>>,
    read_failure: Option<Error>,
}
impl<'f> NativeStore<'f> {
    // The pure generic reader keeps its Capture category. Its native owner must
    // complete each operation here BEFORE returning/dropping the store, preserving
    // the original typed cause. One first failure only; no diagnostic IO or retry.
    pub(super) fn complete<T, E>(
        &mut self,
        result: Result<T, E>,
    ) -> Result<T, ReadCompletionError<E>> {
        if let Some(source) = self.read_failure.take() {
            return Err(ReadCompletionError::Native(source));
        }
        result.map_err(ReadCompletionError::Logical)
    }
    pub(super) fn visit_filesystems(
        &self,
        visit: &mut impl FnMut(&opensip_platform::DescriptorFilesystem) -> std::io::Result<()>,
    ) -> Result<(), Error> {
        self.recheck()?;
        for captured in &self.captures {
            captured.visit_filesystems(visit)?;
        }
        self.recheck()
    }
    pub(super) fn new(fence: &'f SuppliedInstallationFence) -> Self {
        Self {
            fence,
            captures: Vec::new(),
            read_failure: None,
        }
    }
    pub(super) fn recheck(&self) -> Result<(), Error> {
        self.fence.recheck().map_err(Error::Fence)?;
        for captured in &self.captures {
            captured.recheck()?;
        }
        self.fence.recheck().map_err(Error::Fence)
    }
}
impl M::Store for NativeStore<'_> {
    fn read(&mut self, b: &mut Budget, r: M::ReadRequest<'_>) -> Result<Arc<[u8]>, M::Error> {
        let captured = match capture(
            b,
            self.fence,
            r.collection(),
            r.reference(),
            r.initial_store(),
        ) {
            Ok(captured) => captured,
            Err(source) => {
                if self.read_failure.is_none() {
                    self.read_failure = Some(source);
                }
                return Err(M::Error::Capture);
            }
        };
        let raw = captured.shared_raw();
        self.captures.push(captured);
        Ok(raw)
    }
}
#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use opensip_identity::{JsonInteger, digest_hex, raw_sha256};
    use opensip_platform::RetainedDirectoryPath;
    use std::{
        fs::{self, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt, symlink},
        path::{Path, PathBuf},
    };
    const STORE: &str = "11111111111111111111111111111111";
    const PREVIOUS: &str = "2222222222222222222222222222222222222222222222222222222222222222";
    fn integer(n: usize) -> V {
        V::Integer(JsonInteger::new(n as i128).unwrap())
    }
    fn reference(c: Collection, raw: &[u8], initial: bool) -> V {
        let mut r = BTreeMap::from([
            ("sha256".into(), V::String(digest_hex(&raw_sha256(raw)))),
            ("bytes".into(), integer(raw.len())),
        ]);
        if c == Collection::Events {
            r.insert("storeInstanceId".into(), V::String(STORE.into()));
            r.insert("sequence".into(), integer(7));
        }
        if c == Collection::Publications {
            r.insert(
                "previousCapsule".into(),
                if initial {
                    V::Null
                } else {
                    V::String(PREVIOUS.into())
                },
            );
        }
        V::Object(r)
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
            let root = std::env::temp_dir().join(format!("opensip-native-locations-{id}"));
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
            let parent = Path::new(rel).parent().unwrap();
            let mut dir = self.root.clone();
            for part in parent.components() {
                dir.push(part);
                if !dir.exists() {
                    fs::create_dir(&dir).unwrap();
                }
                fs::set_permissions(&dir, Permissions::from_mode(0o700)).unwrap();
            }
            let file = self.root.join(rel);
            fs::write(&file, raw).unwrap();
            fs::set_permissions(&file, Permissions::from_mode(0o600)).unwrap();
            file
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
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    use std::collections::BTreeSet;
    #[test]
    fn native_locations_all_five_exact_routes_and_accounting() {
        let raw = b"abc";
        let digest = digest_hex(&raw_sha256(raw));
        let store = V::String(STORE.into());
        // These independent physical routes are not generated by Locator::new.
        let routes = [
            (
                Collection::Objects,
                format!("trust/objects/{digest}"),
                false,
                (3, 5, 3),
            ),
            (
                Collection::Records,
                format!("trust/records/{digest}"),
                false,
                (3, 5, 3),
            ),
            (
                Collection::Events,
                format!("trust/stores/{STORE}/events/7-{digest}"),
                false,
                (5, 9, 3),
            ),
            (
                Collection::Publications,
                format!("trust/publications/by-predecessor/{PREVIOUS}/{digest}"),
                false,
                (5, 9, 3),
            ),
            (
                Collection::Publications,
                format!("trust/publications/initial/{STORE}/{digest}"),
                true,
                (5, 9, 3),
            ),
        ];
        for (c, route, initial, counts) in routes {
            let f = Fixture::new();
            let file = f.write(&route, raw);
            let guard = f.fence();
            let r = reference(c, raw, initial);
            let mut b = budget();
            let got = capture(
                &mut b,
                &guard,
                c,
                &r,
                if initial { Some(&store) } else { None },
            )
            .unwrap();
            assert_eq!(got.raw(), raw);
            assert_eq!(got.reference(), &r);
            assert_eq!(got.collection(), c);
            assert_eq!(
                got.initial_store(),
                if initial { Some(&store) } else { None }
            );
            assert_eq!(
                got.file().metadata().unwrap().ino(),
                fs::metadata(file).unwrap().ino()
            );
            assert_eq!(b.counters(), counts);
            got.recheck().unwrap();
        }
    }
    #[test]
    fn native_locations_full_reference_and_initial_context_before_io() {
        let f = Fixture::new();
        let guard = f.fence();
        let raw = b"abc";
        let mut bad = reference(Collection::Events, raw, false);
        let V::Object(ref mut o) = bad else {
            unreachable!()
        };
        o.remove("sequence");
        let mut extra = reference(Collection::Records, raw, false);
        let V::Object(ref mut o) = extra else {
            unreachable!()
        };
        o.insert("path".into(), V::String("x".repeat(1048576)));
        let mut invalid_sequence = reference(Collection::Events, raw, false);
        let V::Object(ref mut o) = invalid_sequence else {
            unreachable!()
        };
        o.insert("sequence".into(), integer(0));
        let mut invalid_store = reference(Collection::Events, raw, false);
        let V::Object(ref mut o) = invalid_store else {
            unreachable!()
        };
        o.insert("storeInstanceId".into(), V::String("g".repeat(32)));
        let cases = [
            (Collection::Records, V::Null, None),
            (Collection::Events, invalid_sequence, None),
            (Collection::Events, invalid_store, None),
            (
                Collection::Publications,
                reference(Collection::Publications, raw, true),
                Some(V::String("g".repeat(32))),
            ),
            (Collection::Events, bad, None),
            (Collection::Records, extra, None),
            (
                Collection::Publications,
                reference(Collection::Publications, raw, true),
                None,
            ),
            (
                Collection::Publications,
                reference(Collection::Publications, raw, false),
                Some(V::String(STORE.into())),
            ),
            (
                Collection::Publications,
                reference(Collection::Publications, raw, true),
                Some(V::String("../escape".into())),
            ),
            (
                Collection::Records,
                reference(Collection::Records, raw, false),
                Some(V::String(STORE.into())),
            ),
        ];
        for (c, r, initial) in cases {
            let mut b = budget();
            assert!(matches!(
                capture(&mut b, &guard, c, &r, initial.as_ref()),
                Err(Error::Reference) | Err(Error::Shape(_))
            ));
            assert_eq!(b.counters(), (0, 0, 0));
            assert_eq!(b.edge(1), Err(M::Error::Closed));
        }
    }
    #[test]
    fn native_locations_no_cross_collection_predecessor_store_or_sequence_fallback() {
        let raw = b"abc";
        let digest = digest_hex(&raw_sha256(raw));
        let f = Fixture::new();
        f.write(&format!("trust/objects/{digest}"), raw);
        f.write(&format!("trust/stores/{STORE}/events/7-{digest}"), raw);
        f.write(
            &format!("trust/publications/by-predecessor/{PREVIOUS}/{digest}"),
            raw,
        );
        let guard = f.fence();
        let mut event = reference(Collection::Events, raw, false);
        let V::Object(ref mut o) = event else {
            unreachable!()
        };
        o.insert("sequence".into(), integer(8));
        let mut wrong_store = reference(Collection::Events, raw, false);
        let V::Object(ref mut o) = wrong_store else {
            unreachable!()
        };
        o.insert("storeInstanceId".into(), V::String("3".repeat(32)));
        let mut publication = reference(Collection::Publications, raw, false);
        let V::Object(ref mut o) = publication else {
            unreachable!()
        };
        o.insert("previousCapsule".into(), V::String("4".repeat(64)));
        for (c, r) in [
            (
                Collection::Records,
                reference(Collection::Records, raw, false),
            ),
            (Collection::Events, event),
            (Collection::Events, wrong_store),
            (Collection::Publications, publication),
        ] {
            let mut b = budget();
            b.retain(c, raw).unwrap();
            assert!(capture(&mut b, &guard, c, &r, None).is_err());
            assert_eq!(b.edge(1), Err(M::Error::Closed));
        }
    }
    #[test]
    fn native_locations_cached_bytes_still_require_actual_file_presence() {
        let raw = b"abc";
        let f = Fixture::new();
        let path = f.write(
            &format!("trust/records/{}", digest_hex(&raw_sha256(raw))),
            raw,
        );
        let guard = f.fence();
        let r = reference(Collection::Records, raw, false);
        let mut b = budget();
        let first = capture(&mut b, &guard, Collection::Records, &r, None).unwrap();
        let second = capture(&mut b, &guard, Collection::Records, &r, None).unwrap();
        assert!(Arc::ptr_eq(&first.raw, &second.raw));
        assert_eq!(b.counters(), (3, 10, 3));
        fs::remove_file(path).unwrap();
        assert!(capture(&mut b, &guard, Collection::Records, &r, None).is_err());
        assert_eq!(b.edge(1), Err(M::Error::Closed));
    }
    #[test]
    fn native_locations_exact_work_limits_lengths_and_hash_are_not_caller_claims() {
        let raw = b"abc";
        let f = Fixture::new();
        let path = f.write(
            &format!("trust/records/{}", digest_hex(&raw_sha256(raw))),
            raw,
        );
        let guard = f.fence();
        let r = reference(Collection::Records, raw, false);
        for (o, e, n) in [(2, 5, 3), (3, 4, 3), (3, 5, 2)] {
            let mut b = Budget::new(o, e, n).unwrap();
            assert!(capture(&mut b, &guard, Collection::Records, &r, None).is_err());
            assert_eq!(b.edge(1), Err(M::Error::Closed));
        }
        let mut exact = Budget::new(3, 5, 3).unwrap();
        capture(&mut exact, &guard, Collection::Records, &r, None).unwrap();
        for length in [2, 4] {
            let mut wrong = r.clone();
            let V::Object(ref mut o) = wrong else {
                unreachable!()
            };
            o.insert("bytes".into(), integer(length));
            let mut b = budget();
            let got = capture(&mut b, &guard, Collection::Records, &wrong, None);
            if length == 2 {
                assert!(matches!(
                    got,
                    Err(Error::Capture(directory_record_capture::Error::Read(
                        crate::journal_store::OperationalReadFailure::Bound
                    )))
                ));
            } else {
                assert!(matches!(got, Err(Error::Length)));
            }
        }
        fs::write(path, b"bad").unwrap();
        let mut b = budget();
        assert!(capture(&mut b, &guard, Collection::Records, &r, None).is_err());
        assert_eq!(b.edge(1), Err(M::Error::Closed));
    }
    #[test]
    fn native_locations_prefix_and_original_file_are_rechecked_after_read() {
        let raw = b"abc";
        for change in ["prefix", "leaf-parent", "file", "root", "carrier"] {
            let f = Fixture::new();
            let path = f.write(
                &format!("trust/records/{}", digest_hex(&raw_sha256(raw))),
                raw,
            );
            let guard = f.fence();
            let r = reference(Collection::Records, raw, false);
            let mut b = budget();
            let got = capture_with(
                &mut b,
                &guard,
                Collection::Records,
                &r,
                None,
                || match change {
                    "prefix" => {
                        fs::rename(f.root.join("trust"), f.root.join("old")).unwrap();
                        fs::create_dir(f.root.join("trust")).unwrap();
                    }
                    "leaf-parent" => {
                        fs::rename(f.root.join("trust/records"), f.root.join("trust/old")).unwrap();
                        fs::create_dir(f.root.join("trust/records")).unwrap();
                    }
                    "carrier" => {
                        fs::rename(f.root.join("lifecycle.fence"), f.root.join("old-fence"))
                            .unwrap();
                        fs::write(f.root.join("lifecycle.fence"), b"").unwrap();
                        fs::set_permissions(
                            f.root.join("lifecycle.fence"),
                            Permissions::from_mode(0o600),
                        )
                        .unwrap();
                    }
                    "file" => fs::write(&path, b"more").unwrap(),
                    "root" => fs::set_permissions(&f.root, Permissions::from_mode(0o777)).unwrap(),
                    _ => unreachable!(),
                },
            );
            assert!(got.is_err(), "{change}");
            assert_eq!(b.edge(1), Err(M::Error::Closed));
        }
    }
    #[test]
    fn native_locations_symlink_and_case_alias_do_not_supply_evidence() {
        let raw = b"abc";
        for change in ["symlink", "case", "parent-case"] {
            let f = Fixture::new();
            let digest = digest_hex(&raw_sha256(raw));
            let path = f.write(&format!("trust/records/{digest}"), raw);
            let guard = f.fence();
            match change {
                "symlink" => {
                    fs::rename(&path, f.root.join("raw")).unwrap();
                    symlink("../../raw", &path).unwrap();
                }
                "case" => fs::rename(&path, path.with_file_name(digest.to_uppercase())).unwrap(),
                "parent-case" => {
                    fs::rename(f.root.join("trust/records"), f.root.join("trust/RECORDS")).unwrap()
                }
                _ => unreachable!(),
            }
            let mut b = budget();
            assert!(
                capture(
                    &mut b,
                    &guard,
                    Collection::Records,
                    &reference(Collection::Records, raw, false),
                    None
                )
                .is_err(),
                "{change}"
            );
        }
    }
    #[test]
    fn native_store_all_full_locations_refresh_cached_files_and_share_budget() {
        let raw = b"abc";
        let hash = digest_hex(&raw_sha256(raw));
        let initial = V::String(STORE.into());
        for (c, path, is_initial, counts) in [
            (
                Collection::Objects,
                format!("trust/objects/{hash}"),
                false,
                (3, 6, 3),
            ),
            (
                Collection::Records,
                format!("trust/records/{hash}"),
                false,
                (3, 6, 3),
            ),
            (
                Collection::Events,
                format!("trust/stores/{STORE}/events/7-{hash}"),
                false,
                (5, 10, 3),
            ),
            (
                Collection::Publications,
                format!("trust/publications/by-predecessor/{PREVIOUS}/{hash}"),
                false,
                (5, 10, 3),
            ),
            (
                Collection::Publications,
                format!("trust/publications/initial/{STORE}/{hash}"),
                true,
                (5, 10, 3),
            ),
        ] {
            let f = Fixture::new();
            let file = f.write(&path, raw);
            let fence = f.fence();
            let mut store = NativeStore::new(&fence);
            let r = reference(c, raw, is_initial);
            let context = is_initial.then_some(&initial);
            let mut b = Budget::new(counts.0, counts.1 * 3, counts.2).unwrap();
            let a = b.load_at(c, &r, context, &mut store).unwrap();
            assert_eq!(b.counters(), counts);
            let second = b.load_at(c, &r, context, &mut store).unwrap();
            assert!(Arc::ptr_eq(&a, &second));
            assert_eq!(b.counters(), (counts.0, counts.1 * 2, counts.2));
            assert_eq!(store.captures.len(), 2);
            store.recheck().unwrap();
            fs::remove_file(file).unwrap();
            assert!(b.load_at(c, &r, context, &mut store).is_err());
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
            assert!(store.recheck().is_err());
        }
    }
    #[test]
    fn native_store_full_shape_and_context_fail_before_store_io() {
        let raw = b"abc";
        let mut calls = 0;
        let mut fixture = |_, _, _| {
            calls += 1;
            Ok(raw.to_vec())
        };
        for c in [Collection::Events, Collection::Publications] {
            let r = reference(Collection::Records, raw, false);
            let mut b = budget();
            assert!(matches!(
                b.load(c, &r, &mut fixture),
                Err(M::Error::Reference)
            ));
            assert_eq!(b.counters(), (0, 1, 0));
        }
        assert_eq!(calls, 0);
        let f = Fixture::new();
        let hash = digest_hex(&raw_sha256(raw));
        f.write(&format!("trust/publications/initial/{STORE}/{hash}"), raw);
        let fence = f.fence();
        let mut store = NativeStore::new(&fence);
        let r = reference(Collection::Publications, raw, true);
        let mut b = budget();
        assert!(
            b.load_at(Collection::Publications, &r, None, &mut store)
                .is_err()
        );
        assert_eq!(b.counters(), (0, 1, 0));
        assert!(store.captures.is_empty());
    }
    #[test]
    fn native_store_logical_and_physical_work_have_one_budget() {
        let raw = b"abc";
        let hash = digest_hex(&raw_sha256(raw));
        let f = Fixture::new();
        f.write(&format!("trust/records/{hash}"), raw);
        let fence = f.fence();
        let r = reference(Collection::Records, raw, false);
        for (limits, okay) in [
            ((3, 6, 3), true),
            ((2, 6, 3), false),
            ((3, 5, 3), false),
            ((3, 6, 2), false),
        ] {
            let mut b = Budget::new(limits.0, limits.1, limits.2).unwrap();
            let mut store = NativeStore::new(&fence);
            assert_eq!(
                b.load(Collection::Records, &r, &mut store).is_ok(),
                okay,
                "{limits:?}"
            );
            if !okay {
                assert!(matches!(b.edge(1), Err(M::Error::Closed)));
            }
        }
        let mut b = Budget::new(3, 6, 4).unwrap();
        b.retain(Collection::Objects, b"x").unwrap();
        let mut store = NativeStore::new(&fence);
        assert!(b.load(Collection::Records, &r, &mut store).is_err());
    }
    fn array343(v: &V) -> &[V] {
        let V::Array(a) = v else { panic!("array") };
        a
    }
    fn text343(v: &V) -> &str {
        let V::String(s) = v else { panic!("string") };
        s
    }
    fn hex343(v: &V) -> Vec<u8> {
        text343(v)
            .as_bytes()
            .chunks_exact(2)
            .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
            .collect()
    }
    // Independent fixture writer derives native paths from actual fixture record
    // content, not the production request/Locator path builder.
    fn write_rows343(f: &Fixture, rows: &V) {
        for row in array343(rows) {
            let r = object(row).unwrap();
            let raw = hex343(r.get("raw").or_else(|| r.get("rawHex")).unwrap());
            let hash = text343(&r["sha256"]);
            let rel = match text343(&r["collection"]) {
                "objects" => format!("trust/objects/{hash}"),
                "records" => format!("trust/records/{hash}"),
                kind => {
                    let v = opensip_identity::parse_json(&raw).unwrap();
                    let v = object(&v).unwrap();
                    let id = if kind == "events" {
                        text343(&v["store"])
                    } else {
                        text343(&object(&v["store"]).unwrap()["storeInstanceId"])
                    };
                    match kind {
                        "events" => {
                            let V::Integer(seq) = &v["sequence"] else {
                                panic!("sequence")
                            };
                            format!("trust/stores/{id}/events/{}-{hash}", seq.get())
                        }
                        "publications" => {
                            if v["previousCapsule"] == V::Null {
                                format!("trust/publications/initial/{id}/{hash}")
                            } else {
                                format!(
                                    "trust/publications/by-predecessor/{}/{hash}",
                                    text343(&v["previousCapsule"])
                                )
                            }
                        }
                        _ => panic!("collection"),
                    }
                }
            };
            f.write(&rel, &raw);
        }
    }
    #[test]
    fn native_store_actual_initial_capsule_uses_its_source_store_and_original_files() {
        let line = include_bytes!("../../tests/fixtures/captured-capsule306.ndjson")
            .split(|b| *b == b'\n')
            .find(|l| !l.is_empty())
            .unwrap();
        let q = opensip_identity::parse_json(line).unwrap();
        let q = object(&q).unwrap();
        let f = Fixture::new();
        write_rows343(&f, &q["store"]);
        let fence = f.fence();
        let mut store = NativeStore::new(&fence);
        let mut b = budget();
        let captured = super::super::captured_capsule_clock::capture(
            &mut b,
            &q["reference"],
            None,
            &mut store,
        )
        .unwrap();
        let expected = object(&array343(&q["outcomes"])[0]).unwrap();
        let expected = object(&expected["expected"]).unwrap();
        assert_eq!(captured.image().value(), &expected["capsule"]);
        assert_eq!(captured.descriptor().value(), &expected["descriptor"]);
        assert_eq!(store.captures.len(), 2);
        assert_eq!(b.counters(), (7, 16, 3234));
        store.recheck().unwrap();
        let c = object(captured.image().value()).unwrap();
        let publication = object(&c["publication"]).unwrap();
        let hash = text343(&publication["sha256"]);
        let carrier = f
            .root
            .join(format!("trust/publications/initial/{STORE}/{hash}"));
        fs::remove_file(carrier).unwrap();
        assert!(store.recheck().is_err());
        assert!(
            super::super::captured_capsule_clock::capture(
                &mut b,
                &q["reference"],
                None,
                &mut store
            )
            .is_err()
        );
    }
    #[test]
    fn native_store_actual_event_trace_preserves_sequence_locations() {
        let mut done = 0;
        for line in include_bytes!("../../tests/fixtures/event-trace325.ndjson")
            .split(|b| *b == b'\n')
            .filter(|l| !l.is_empty())
        {
            let q = opensip_identity::parse_json(line).unwrap();
            let q = object(&q).unwrap();
            let result = object(&array343(&q["outcomes"])[0]).unwrap();
            if result["ok"] != V::Bool(true) {
                continue;
            }
            let f = Fixture::new();
            write_rows343(&f, &q["store"]);
            let fence = f.fence();
            let mut store = NativeStore::new(&fence);
            let mut b = budget();
            super::super::current_event_trace::bind_trace(&mut b, &q["descriptor"], &mut store)
                .unwrap();
            store.recheck().unwrap();
            assert!(!store.captures.is_empty());
            done += 1;
            if done == 3 {
                break;
            }
        }
        assert_eq!(done, 3);
    }
    #[test]
    fn native_store_typed_graph_uses_full_events_and_source_owned_initial_store() {
        use super::super::retained_trust_graph as graph;
        use crate::trust::trust_record_reader::RecordKind;
        let mut done = 0;
        for line in include_bytes!("../../tests/fixtures/graph272.ndjson")
            .split(|b| *b == b'\n')
            .filter(|l| !l.is_empty())
        {
            let q = opensip_identity::parse_json(line).unwrap();
            let q = object(&q).unwrap();
            let label = text343(&q["label"]);
            let kind = match label {
                "original-18" => RecordKind::TrustEventV1,
                "original-19" => RecordKind::PublicationDescriptorV1,
                "original-20" => RecordKind::TrustCapsuleV1,
                _ => continue,
            };
            let f = Fixture::new();
            write_rows343(&f, &q["store"]);
            let fence = f.fence();
            let mut store = NativeStore::new(&fence);
            let mut b = budget();
            let sid = V::String(STORE.into());
            let initial = (kind == RecordKind::PublicationDescriptorV1).then_some(&sid);
            let result =
                graph::walk_at(&mut b, kind, &q["reference"], initial, &mut store).unwrap();
            let expected = object(&q["result"]).unwrap();
            assert_eq!(result.visits().len(), array343(&expected["visits"]).len());
            store.recheck().unwrap();
            assert!(
                store
                    .captures
                    .iter()
                    .any(|c| c.collection() == Collection::Events)
            );
            if kind == RecordKind::PublicationDescriptorV1 {
                let mut outer_budget = budget();
                let mut outer_store = NativeStore::new(&fence);
                let outer = super::super::prepared_trust_outcomes::walk_at(
                    &mut outer_budget,
                    kind,
                    &q["reference"],
                    Some(&sid),
                    &mut outer_store,
                )
                .unwrap();
                assert_eq!(outer.graph().visits().len(), result.visits().len());
                outer_store.recheck().unwrap();
                // Even a previously cached descriptor does not supply missing S.
                let mut missing = NativeStore::new(&fence);
                assert!(graph::walk(&mut b, kind, &q["reference"], &mut missing).is_err());
                assert!(missing.captures.is_empty());
                let mut b = budget();
                let mut wrong = NativeStore::new(&fence);
                let other = V::String("9".repeat(32));
                assert!(
                    graph::walk_at(&mut b, kind, &q["reference"], Some(&other), &mut wrong)
                        .is_err()
                );
            }
            if kind == RecordKind::TrustCapsuleV1 {
                let captured = store
                    .captures
                    .iter()
                    .find(|c| c.collection() == Collection::Publications)
                    .unwrap();
                assert_eq!(captured.initial_store(), Some(&sid));
            }
            done += 1;
        }
        assert_eq!(done, 3);
    }
    #[test]
    fn native_diagnostics_completion_preserves_actual_cause_and_cannot_swallow_failure() {
        for swallowed in [false, true] {
            let f = Fixture::new();
            let raw = b"abc";
            let hash = digest_hex(&raw_sha256(raw));
            let file = f.write(&format!("trust/records/{hash}"), raw);
            let fence = f.fence();
            fs::remove_file(file).unwrap();
            let mut store = NativeStore::new(&fence);
            let mut b = budget();
            let result = b.load(
                Collection::Records,
                &reference(Collection::Records, raw, false),
                &mut store,
            );
            assert!(matches!(result, Err(M::Error::Capture)));
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
            let result = if swallowed {
                Ok(Arc::<[u8]>::from(&b"fake"[..]))
            } else {
                result
            };
            let done = store.complete(result);
            assert!(
                matches!(done,Err(ReadCompletionError::Native(Error::Capture(directory_record_capture::Error::Open(ref e))))if e.kind()==std::io::ErrorKind::NotFound),
                "{done:?}"
            );
            assert!(store.read_failure.is_none());
            assert!(store.captures.is_empty());
        }
    }
    #[test]
    fn native_diagnostics_success_and_logical_failure_do_not_invent_native_error() {
        let f = Fixture::new();
        let raw = b"abc";
        let hash = digest_hex(&raw_sha256(raw));
        f.write(&format!("trust/records/{hash}"), raw);
        let fence = f.fence();
        let mut store = NativeStore::new(&fence);
        let mut b = budget();
        let result = b.load(
            Collection::Records,
            &reference(Collection::Records, raw, false),
            &mut store,
        );
        let before = b.counters();
        assert_eq!(&*store.complete(result).unwrap(), raw);
        assert_eq!(before, b.counters());
        assert!(store.read_failure.is_none());
        assert!(matches!(
            store.complete::<(), _>(Err(M::Error::Reference)),
            Err(ReadCompletionError::Logical(M::Error::Reference))
        ));
    }
}
