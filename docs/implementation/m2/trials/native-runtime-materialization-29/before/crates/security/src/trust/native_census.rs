// Actual P2 current + all immediate/following structural candidate observations.
// Owned custody under a borrowed supplied fence; NOT clean/behind/fork authority.
use super::{
    directory_provers::Observed,
    directory_record_capture,
    native_current::{self, SuppliedP2Current},
    retained_metadata_index::{self as M, Budget},
};
use crate::custody::{directory_policy, installation_fence::SuppliedInstallationFence};
use opensip_identity::{JsonValue as V, canonical_bytes, digest_hex, raw_sha256};
use opensip_platform::RetainedChildDirectory;
use std::{ffi::OsStr, io, sync::Arc};
#[derive(Debug)]
pub(super) enum Error {
    Budget(M::Error),
    Current(native_current::Error),
    Directory(crate::custody::DirectoryPathRefusal),
    Native(io::Error),
    Files(directory_record_capture::Error),
    Changed,
    Canonical,
}
impl From<M::Error> for Error {
    fn from(e: M::Error) -> Self {
        Self::Budget(e)
    }
}
pub(super) struct SuppliedCensus<'f> {
    current: SuppliedP2Current<'f>,
    fence: &'f SuppliedInstallationFence,
    prefixes: Vec<Arc<RetainedChildDirectory>>,
    // None is an observed missing final by-predecessor directory only. Not
    // genesis or authority; missing higher ancestors is always an error.
    observed: Option<Observed>,
}
impl SuppliedCensus<'_> {
    pub(super) fn visit_filesystems(
        &self,
        visit: &mut impl FnMut(&opensip_platform::DescriptorFilesystem) -> std::io::Result<()>,
    ) -> Result<(), Error> {
        self.recheck()?;
        self.current
            .visit_filesystems(visit)
            .map_err(Error::Current)?;
        for edge in &self.prefixes {
            for fs in edge.observe_filesystems().map_err(Error::Native)? {
                visit(&fs).map_err(Error::Native)?;
            }
        }
        let (uid, groups) = self.fence.supplied_actor();
        if let Some(observed) = &self.observed {
            for bucket in std::iter::once(observed.current()).chain(observed.following()) {
                if let Some(candidates) = bucket.candidates() {
                    candidates
                        .captured()
                        .visit_filesystems(uid, groups, visit)
                        .map_err(Error::Files)?;
                }
            }
        }
        self.recheck()
    }
    pub(super) fn current(&self) -> &SuppliedP2Current<'_> {
        &self.current
    }
    pub(super) fn observed(&self) -> Option<&Observed> {
        self.observed.as_ref()
    }
    fn prefixes(&self) -> Result<(), Error> {
        self.current.recheck().map_err(Error::Current)?;
        let (uid, groups) = self.fence.supplied_actor();
        for prefix in &self.prefixes {
            directory_policy::inspect(prefix, uid, groups).map_err(Error::Directory)?;
        }
        self.current.recheck().map_err(Error::Current)
    }
    fn missing(parent: &RetainedChildDirectory, name: &str) -> Result<(), Error> {
        match parent.directory().bind_child_directory(OsStr::new(name)) {
            Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(()),
            Err(e) => Err(Error::Native(e)),
            Ok(_) => Err(Error::Changed),
        }
    }
    pub(super) fn recheck(&self) -> Result<(), Error> {
        self.prefixes()?;
        let (uid, groups) = self.fence.supplied_actor();
        if let Some(observed) = &self.observed {
            for bucket in std::iter::once(observed.current()).chain(observed.following()) {
                if let Some(candidates) = bucket.candidates() {
                    candidates
                        .captured()
                        .recheck(uid, groups)
                        .map_err(Error::Files)?;
                } else {
                    let raw = canonical_bytes(bucket.before()).map_err(|_| Error::Canonical)?;
                    Self::missing(observed.root(), &digest_hex(&raw_sha256(&raw)))?;
                }
            }
        } else {
            Self::missing(
                self.prefixes.last().ok_or(Error::Changed)?,
                "by-predecessor",
            )?;
        }
        self.prefixes()
    }
}
pub(super) fn capture<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    expected_store: &V,
    foreign: impl FnMut(&[u8]) -> Result<(), ()>,
) -> Result<SuppliedCensus<'f>, Error> {
    capture_with(b, fence, expected_store, foreign, || {})
}
fn capture_with<'f>(
    b: &mut Budget,
    fence: &'f SuppliedInstallationFence,
    expected_store: &V,
    foreign: impl FnMut(&[u8]) -> Result<(), ()>,
    after_observe: impl FnOnce(),
) -> Result<SuppliedCensus<'f>, Error> {
    b.scope(|b| {
        let current =
            native_current::capture_p2(b, fence, expected_store).map_err(Error::Current)?;
        let mut result = SuppliedCensus {
            current,
            fence,
            prefixes: Vec::new(),
            observed: None,
        };
        let (uid, groups) = fence.supplied_actor();
        let mut root = None;
        for component in ["trust", "publications", "by-predecessor"] {
            b.edge(1)?;
            result.prefixes()?;
            let parent = result
                .prefixes
                .last()
                .map(|p| p.directory())
                .unwrap_or_else(|| fence.root().directory());
            let opened = parent.bind_child_directory(OsStr::new(component));
            result.prefixes()?;
            let edge = match opened {
                Ok(edge) => Arc::new(edge),
                Err(e) if component == "by-predecessor" && e.kind() == io::ErrorKind::NotFound => {
                    break;
                }
                Err(e) => return Err(Error::Native(e)),
            };
            directory_policy::inspect(&edge, uid, groups).map_err(Error::Directory)?;
            b.directory(Arc::clone(&edge))?;
            if component == "by-predecessor" {
                root = Some(Arc::clone(&edge));
            }
            result.prefixes.push(edge);
        }
        if let Some(root) = root {
            result.observed = Some(
                result
                    .current
                    .observe_successors(b, root, foreign)
                    .map_err(Error::Current)?,
            );
        }
        after_observe();
        result.recheck()?;
        Ok(result)
    })
}

#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use opensip_identity::parse_json;
    use opensip_platform::RetainedDirectoryPath;
    use std::{
        collections::{BTreeMap, BTreeSet},
        fs::{self, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt},
        path::{Path, PathBuf},
    };
    fn o(v: &V) -> &BTreeMap<String, V> {
        let V::Object(o) = v else { panic!("object") };
        o
    }
    fn text(v: &V) -> &str {
        let V::String(s) = v else { panic!("string") };
        s
    }
    fn arr(v: &V) -> &[V] {
        let V::Array(a) = v else { panic!("array") };
        a
    }
    fn bytes(v: &V) -> Vec<u8> {
        text(v)
            .as_bytes()
            .chunks_exact(2)
            .map(|b| u8::from_str_radix(std::str::from_utf8(b).unwrap(), 16).unwrap())
            .collect()
    }
    fn row(label: &str) -> V {
        include_bytes!("../../tests/fixtures/successor-link329.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
            .map(|l| parse_json(l).unwrap())
            .find(|v| text(&o(v)["label"]) == label)
            .unwrap()
    }
    fn budget() -> Budget {
        Budget::new(65536, 131072, 268435456).unwrap()
    }
    struct Fixture {
        root: PathBuf,
        path: Arc<RetainedDirectoryPath>,
        uid: u32,
        before: V,
    }
    impl Fixture {
        fn new() -> Self {
            let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
            let root = std::env::temp_dir().join(format!("opensip-native-census-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let root = fs::canonicalize(root).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            fs::write(root.join("lifecycle.fence"), b"").unwrap();
            fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600))
                .unwrap();
            let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
            let q = row("empty-link-0");
            let before = o(&q)["before"].clone();
            let f = Self {
                root,
                path,
                uid,
                before,
            };
            let sid = text(&o(&o(&f.before)["store"])["storeInstanceId"]);
            f.write(
                &format!("trust/stores/{sid}/state.v1"),
                &canonical_bytes(&f.before).unwrap(),
            );
            f.rows(&q, None);
            f
        }
        fn write(&self, rel: &str, raw: &[u8]) -> PathBuf {
            let mut p = self.root.clone();
            for c in Path::new(rel).parent().unwrap().components() {
                p.push(c);
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
        fn rows(&self, q: &V, include: Option<&str>) {
            let current = text(&o(&o(&self.before)["publication"])["sha256"]);
            for row in arr(&o(q)["store"]) {
                let r = o(row);
                let hash = text(&r["sha256"]);
                let raw = bytes(r.get("rawHex").or_else(|| r.get("raw")).unwrap());
                let kind = text(&r["collection"]);
                if kind == "publications" && hash != current && Some(hash) != include {
                    continue;
                }
                let path = match kind {
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
                    "publications" => {
                        let v = parse_json(&raw).unwrap();
                        let v = o(&v);
                        if v["previousCapsule"] == V::Null {
                            format!(
                                "trust/publications/initial/{}/{hash}",
                                text(&o(&v["store"])["storeInstanceId"])
                            )
                        } else {
                            format!(
                                "trust/publications/by-predecessor/{}/{hash}",
                                text(&v["previousCapsule"])
                            )
                        }
                    }
                    _ => panic!("collection"),
                };
                self.write(&path, &raw);
            }
        }
        fn add(&self, label: &str) {
            let q = row(label);
            let h = text(&o(&o(&q)["reference"])["sha256"]);
            self.rows(&q, Some(h));
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
        fn bucket(&self) -> PathBuf {
            self.root
                .join("trust/publications/by-predecessor")
                .join(digest_hex(&raw_sha256(
                    &canonical_bytes(&self.before).unwrap(),
                )))
        }
        fn empty(&self) {
            fs::create_dir(self.bucket()).unwrap();
            fs::set_permissions(self.bucket(), Permissions::from_mode(0o700)).unwrap();
        }
        fn store(&self) -> &V {
            &o(&self.before)["store"]
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn native_census_actual_current_missing_and_empty_buckets_keep_shared_accounting() {
        let f = Fixture::new();
        {
            let fence = f.fence();
            let mut b = budget();
            let got = capture(&mut b, &fence, f.store(), |_| Ok(())).unwrap();
            assert_eq!(got.current().head().value(), &f.before);
            let observed = got.observed().unwrap();
            assert!(observed.current().is_observed_missing());
            assert!(observed.following().is_empty());
            got.recheck().unwrap();
            assert_eq!(b.counters(), (10, 31, 9105));
        }
        f.empty();
        let fence = f.fence();
        for (limits, okay) in [
            ((11, 34, 9108), true),
            ((10, 34, 9108), false),
            ((11, 33, 9108), false),
            ((11, 34, 9107), false),
        ] {
            let mut b = Budget::new(limits.0, limits.1, limits.2).unwrap();
            let got = capture(&mut b, &fence, f.store(), |_| Ok(()));
            assert_eq!(got.is_ok(), okay, "{limits:?}: {:?}", got.as_ref().err());
            if let Ok(got) = got {
                assert!(
                    got.observed()
                        .unwrap()
                        .current()
                        .candidates()
                        .unwrap()
                        .links()
                        .is_empty()
                );
                assert_eq!(b.counters(), limits);
                got.recheck().unwrap();
            } else {
                assert!(matches!(b.edge(1), Err(M::Error::Closed)));
            }
        }
    }
    #[test]
    fn native_census_all_following_branches_keep_zero_one_and_two_supported_observations() {
        let f = Fixture::new();
        f.add("empty-link-0");
        for step in 0..3 {
            if step == 1 {
                f.add("empty-link-1");
            }
            if step == 2 {
                f.add("clock-link-0");
                f.add("clock-link-1");
            }
            let fence = f.fence();
            let mut b = budget();
            let got = capture(&mut b, &fence, f.store(), |_| Ok(())).unwrap();
            let observed = got.observed().unwrap();
            assert_eq!(observed.structurally_supported().len(), step);
            assert_eq!(
                observed.current().candidates().unwrap().links().len(),
                if step == 2 { 2 } else { 1 }
            );
            assert_eq!(observed.following().len(), if step == 2 { 2 } else { 1 });
            got.recheck().unwrap();
        }
    }
    #[test]
    fn native_census_late_bad_following_branch_cannot_be_hidden_by_earlier_support() {
        let f = Fixture::new();
        for label in [
            "empty-link-0",
            "empty-link-1",
            "clock-link-0",
            "clock-link-1",
        ] {
            f.add(label);
        }
        let empty = row("empty-link-0");
        let clock = row("clock-link-0");
        let selected = if text(&o(&o(&empty)["reference"])["sha256"])
            > text(&o(&o(&clock)["reference"])["sha256"])
        {
            empty
        } else {
            clock
        };
        let q = o(&selected);
        let h = text(&o(&q["reference"])["sha256"]);
        let raw = arr(&q["store"])
            .iter()
            .map(o)
            .find(|r| text(&r["collection"]) == "publications" && text(&r["sha256"]) == h)
            .unwrap();
        let d = parse_json(&bytes(
            raw.get("rawHex").or_else(|| raw.get("raw")).unwrap(),
        ))
        .unwrap();
        let mut after = o(&o(&d)["afterProjection"]).clone();
        after.insert("publication".into(), q["reference"].clone());
        let parent = digest_hex(&raw_sha256(&canonical_bytes(&V::Object(after)).unwrap()));
        f.write(
            &format!(
                "trust/publications/by-predecessor/{parent}/{}",
                "f".repeat(64)
            ),
            b"malformed",
        );
        let fence = f.fence();
        let mut b = budget();
        assert!(capture(&mut b, &fence, f.store(), |_| Ok(())).is_err());
        assert!(matches!(b.edge(1), Err(M::Error::Closed)));
    }
    #[test]
    fn native_census_foreign_names_are_charged_reported_and_never_read() {
        let f = Fixture::new();
        f.empty();
        let foreign = f.bucket().join("foreign");
        fs::write(&foreign, b"untrusted").unwrap();
        fs::set_permissions(&foreign, Permissions::from_mode(0o777)).unwrap();
        let fence = f.fence();
        let mut b = budget();
        let mut names = Vec::new();
        let got = capture(&mut b, &fence, f.store(), |name| {
            names.push(name.to_vec());
            Ok(())
        })
        .unwrap();
        assert_eq!(names, vec![b"foreign".to_vec()]);
        assert_eq!(b.counters(), (11, 35, 9115));
        got.recheck().unwrap();
        assert_eq!(fs::read(foreign).unwrap(), b"untrusted");
    }
    #[test]
    fn native_census_postscan_additions_and_native_custody_changes_refuse() {
        for change in ["missing-bucket", "empty-addition", "root", "file", "fence"] {
            let f = Fixture::new();
            if change != "missing-bucket" {
                f.empty();
            }
            let fence = f.fence();
            let mut b = budget();
            let got = capture_with(
                &mut b,
                &fence,
                f.store(),
                |_| Ok(()),
                || match change {
                    "missing-bucket" => f.empty(),
                    "empty-addition" => {
                        fs::write(f.bucket().join("0".repeat(64)), b"new").unwrap();
                    }
                    "root" => {
                        fs::rename(
                            f.root.join("trust/publications/by-predecessor"),
                            f.root.join("old-root"),
                        )
                        .unwrap();
                        fs::create_dir(f.root.join("trust/publications/by-predecessor")).unwrap();
                        fs::set_permissions(
                            f.root.join("trust/publications/by-predecessor"),
                            Permissions::from_mode(0o700),
                        )
                        .unwrap();
                    }
                    "file" => {
                        let sid = text(&o(f.store())["storeInstanceId"]);
                        fs::write(f.root.join(format!("trust/stores/{sid}/state.v1")), b"bad")
                            .unwrap();
                    }
                    "fence" => {
                        fs::rename(f.root.join("lifecycle.fence"), f.root.join("old-fence"))
                            .unwrap();
                        fs::write(f.root.join("lifecycle.fence"), b"").unwrap();
                        fs::set_permissions(
                            f.root.join("lifecycle.fence"),
                            Permissions::from_mode(0o600),
                        )
                        .unwrap();
                    }
                    _ => unreachable!(),
                },
            );
            assert!(got.is_err(), "{change}");
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
        }
    }

    #[test]
    fn native_census_enumeration_rejects_a_sampled_change_during_foreign_callback() {
        let f = Fixture::new();
        f.empty();
        fs::write(f.bucket().join("foreign"), b"untouched").unwrap();
        let fence = f.fence();
        let mut b = budget();
        let got = capture(&mut b, &fence, f.store(), |_| {
            fs::set_permissions(f.bucket(), Permissions::from_mode(0o750)).unwrap();
            Ok(())
        });
        assert!(got.is_err());
        assert!(matches!(b.edge(1), Err(M::Error::Closed)));
    }

    #[test]
    fn native_census_missing_root_is_distinct_from_wrong_kind_and_later_appearance() {
        // A synthetic capsule-local P2 shape exercises the initial locator. This
        // does not assert lawful creation, original clock authority or standing.
        let f = Fixture::new();
        let q = row("empty-link-0");
        let old_hash = text(&o(&o(&f.before)["publication"])["sha256"]);
        let row = arr(&o(&q)["store"])
            .iter()
            .map(o)
            .find(|r| text(&r["collection"]) == "publications" && text(&r["sha256"]) == old_hash)
            .unwrap();
        let raw = bytes(row.get("rawHex").or_else(|| row.get("raw")).unwrap());
        let d = parse_json(&raw).unwrap();
        let mut d = o(&d).clone();
        let mut c = o(&f.before).clone();
        let one = V::Integer(opensip_identity::JsonInteger::new(1).unwrap());
        c.insert("revision".into(), one.clone());
        c.insert("previous".into(), V::Null);
        c.remove("publication");
        d.insert("revision".into(), one);
        d.insert("previousCapsule".into(), V::Null);
        d.insert("nativeBefore".into(), V::Null);
        d.insert("afterProjection".into(), V::Object(c.clone()));
        let raw = canonical_bytes(&V::Object(d)).unwrap();
        let hash = digest_hex(&raw_sha256(&raw));
        c.insert(
            "publication".into(),
            V::Object(
                [
                    ("previousCapsule".into(), V::Null),
                    ("sha256".into(), V::String(hash.clone())),
                    (
                        "bytes".into(),
                        V::Integer(opensip_identity::JsonInteger::new(raw.len() as i128).unwrap()),
                    ),
                ]
                .into(),
            ),
        );
        let sid = text(&o(f.store())["storeInstanceId"]);
        f.write(&format!("trust/publications/initial/{sid}/{hash}"), &raw);
        f.write(
            &format!("trust/stores/{sid}/state.v1"),
            &canonical_bytes(&V::Object(c)).unwrap(),
        );
        fs::remove_dir_all(f.root.join("trust/publications/by-predecessor")).unwrap();
        let fence = f.fence();
        let mut b = budget();
        let got = capture(&mut b, &fence, f.store(), |_| Ok(())).unwrap();
        assert!(got.observed().is_none());
        got.recheck().unwrap();
        let root = f.root.join("trust/publications/by-predecessor");
        fs::create_dir(&root).unwrap();
        fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
        assert!(got.recheck().is_err());
        fs::remove_dir(&root).unwrap();
        fs::write(&root, b"wrong kind").unwrap();
        let mut b = budget();
        assert!(capture(&mut b, &fence, f.store(), |_| Ok(())).is_err());
    }
    fn signed_profile350() -> super::super::ProfileSetEvidence {
        use super::super::{admit, admitted_profiles, decode_hex32};
        let q = include_bytes!("../../tests/fixtures/profile-signature-cases.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
            .map(|b| parse_json(b).unwrap())
            .find(|v| o(&o(v)["expected"]).contains_key("admit"))
            .unwrap();
        let q = o(&q);
        let roots = parse_json(include_bytes!("../../tests/fixtures/profile-roots.json")).unwrap();
        let root = admit(&o(&roots)[text(&q["root"])], [true, true]).unwrap();
        let revoked = arr(&q["revoked"])
            .iter()
            .map(|v| decode_hex32(text(v)).unwrap())
            .collect();
        admitted_profiles::verify_profile_set(
            &root,
            &bytes(&q["stored"]),
            &q["envelope"],
            Some(decode_hex32(text(&q["corePin"])).unwrap()),
            &revoked,
        )
        .unwrap()
    }
    #[test]
    fn native_profile_census_visits_current_dependencies_and_empty_bucket_with_exact_counts() {
        let f = Fixture::new();
        for empty in [false, true] {
            if empty {
                f.empty();
            }
            let fence = f.fence();
            let mut b = budget();
            let got = capture(&mut b, &fence, f.store(), |_| Ok(())).unwrap();
            let before = b.counters();
            let mut visits = 0;
            got.current()
                .visit_filesystems(&mut |fs| {
                    assert_eq!(fs.name(), b"apfs");
                    visits += 1;
                    Ok(())
                })
                .unwrap();
            // Current state.v1:3 parent/child pairs +File=7; actual D:
            //4 pairs+File=9; operation record:2 pairs+File=5. No events here.
            assert_eq!(visits, 21);
            visits = 0;
            got.visit_filesystems(&mut |_| {
                visits += 1;
                Ok(())
            })
            .unwrap();
            // Three census prefixes add6; present empty bucket adds2 even
            // with zero canonical files. Missing final child adds no handle.
            assert_eq!(visits, if empty { 29 } else { 27 });
            assert_eq!(b.counters(), before);
            for stop in 0..visits {
                let mut count = 0;
                assert!(
                    got.visit_filesystems(&mut |_| {
                        let at = count;
                        count += 1;
                        if at == stop {
                            Err(io::Error::other("injected visitor refusal"))
                        } else {
                            Ok(())
                        }
                    })
                    .is_err(),
                    "stop{stop}"
                );
                assert_eq!(count, stop + 1);
            }
        }
    }
    #[test]
    fn native_profile_census_same_fence_profile_and_all_following_candidates_remain_owned() {
        use super::super::native_profile_census as joined;
        let f = Fixture::new();
        f.add("empty-link-0");
        for step in 0..3 {
            if step == 1 {
                f.add("empty-link-1");
            }
            if step == 2 {
                f.add("clock-link-0");
                f.add("clock-link-1");
            }
            let fence = f.fence();
            let mut b = budget();
            let got = joined::capture(&mut b, signed_profile350(), &fence, f.store(), |_| Ok(()))
                .unwrap();
            assert_eq!(got.census().current().head().value(), &f.before);
            assert_eq!(
                got.census()
                    .observed()
                    .unwrap()
                    .structurally_supported()
                    .len(),
                step
            );
            assert!(got.platform().decision().refusals.is_empty());
            assert!(got.standing().contains("No current authority"));
            let mut visits = 0;
            got.census()
                .visit_filesystems(&mut |_| {
                    visits += 1;
                    Ok(())
                })
                .unwrap();
            // Base27 + each captured dependency's prefix pairs/File + each
            // present bucket pair/candidate File, including every following.
            assert_eq!(visits, [44, 61, 102][step]);
            println!(
                "profile census step{step}: visits{visits}, budget{:?}",
                b.counters()
            );
            got.recheck().unwrap();
        }
    }
    #[test]
    fn native_profile_census_profile_checker_rejects_foreign_filesystem() {
        use super::super::native_platform;
        let f = Fixture::new();
        let fence = f.fence();
        let got = native_platform::capture(signed_profile350(), &fence).unwrap();
        let dev = RetainedDirectoryPath::open(std::path::Path::new("/dev"), 128)
            .unwrap()
            .directory()
            .observe_filesystem()
            .unwrap();
        assert!(!got.qualifies_installation_filesystem(&dev));
        assert!(got.qualifies_installation_filesystem(got.install_filesystem()));
        // The actual readonly System and writable Data APFS volumes are both
        // supported types but not the same operational publication domain.
        let system = got.loader().filesystem().unwrap();
        assert_eq!(system.name(), b"apfs");
        assert!(system.is_local());
        assert!(!system.is_union());
        assert_ne!(system.native_id(), got.install_filesystem().native_id());
        assert!(!got.qualifies_installation_filesystem(&system));
    }
    #[test]
    fn native_profile_census_later_file_fence_and_missing_bucket_changes_refuse() {
        use super::super::native_profile_census as joined;
        for change in ["file", "fence", "bucket"] {
            let f = Fixture::new();
            let fence = f.fence();
            let mut b = budget();
            let got = joined::capture(&mut b, signed_profile350(), &fence, f.store(), |_| Ok(()))
                .unwrap();
            match change {
                "file" => {
                    let sid = text(&o(f.store())["storeInstanceId"]);
                    fs::write(f.root.join(format!("trust/stores/{sid}/state.v1")), b"bad").unwrap();
                }
                "fence" => {
                    fs::set_permissions(
                        f.root.join("lifecycle.fence"),
                        Permissions::from_mode(0o666),
                    )
                    .unwrap();
                }
                "bucket" => f.empty(),
                _ => unreachable!(),
            }
            assert!(got.recheck().is_err(), "{change}");
        }
    }
    #[test]
    fn native_profile_census_postcapture_changes_refuse_and_close_shared_budget() {
        use super::super::native_profile_census as joined;
        for change in ["bucket", "fence"] {
            let f = Fixture::new();
            let fence = f.fence();
            let mut b = budget();
            let got =
                joined::capture_interposed(&mut b, signed_profile350(), &fence, f.store(), || {
                    if change == "bucket" {
                        f.empty();
                    } else {
                        fs::set_permissions(
                            f.root.join("lifecycle.fence"),
                            Permissions::from_mode(0o666),
                        )
                        .unwrap();
                    }
                });
            assert!(got.is_err(), "{change}");
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
        }
    }
    #[test]
    fn native_profile_census_dependency_recheck_retains_typed_error_cause() {
        let f = Fixture::new();
        let fence = f.fence();
        let mut b = budget();
        let got = capture(&mut b, &fence, f.store(), |_| Ok(())).unwrap();
        let mut changed = 0;
        for entry in fs::read_dir(f.root.join("trust/records")).unwrap() {
            let path = entry.unwrap().path();
            if path.is_file() {
                fs::write(path, b"changed").unwrap();
                changed += 1;
            }
        }
        assert!(changed > 0);
        assert!(matches!(
            got.current().recheck(),
            Err(native_current::Error::Immutable(
                super::super::native_record_capture::Error::Changed
            ))
        ));
    }
    #[test]
    fn native_diagnostics_constructor_refuses_exact_measured_identity_failure_before_census() {
        use super::super::{
            PlatformTier, admit, admitted_profiles, native_platform, native_profile_census,
        };
        use ed25519_dalek::{Signer, SigningKey};
        fn map(v: &mut V) -> &mut std::collections::BTreeMap<String, V> {
            let V::Object(o) = v else { panic!("object") };
            o
        }
        let f = Fixture::new();
        let fence = f.fence();
        let actual = native_platform::capture(signed_profile350(), &fence).unwrap();
        let observed = o(actual.observed());
        let mut payload = actual.profile().envelope().payload().clone();
        let selected = map(map(&mut payload).get_mut("platforms").unwrap())
            .get_mut(text(&observed["platform"]))
            .unwrap();
        let V::Array(measured) = map(selected).get_mut("measuredProfiles").unwrap() else {
            panic!("profiles")
        };
        let mut row = o(&measured[0]).clone();
        row.insert("build".into(), observed["osversion"].clone());
        row.insert("kernUuid".into(), observed["kernUuid"].clone());
        let wrong = if text(&observed["dyldCdhash"]) == "0".repeat(40) {
            "1".repeat(40)
        } else {
            "0".repeat(40)
        };
        row.insert("dyldCdhash".into(), V::String(wrong));
        *measured = vec![V::Object(row)];
        // Freshly SIGNED SYNTHETIC profile. Public deterministic fixture keys,
        // never operational keys or a mutation of already-verified evidence.
        let stored = crate::trust::metadata_bytes(&payload, 5_000_000).unwrap();
        let pin = crate::trust::metadata_digest_for_domain(
            "opensip.metadata.platform-profile-set.1",
            &payload,
        )
        .unwrap();
        let roots = parse_json(include_bytes!("../../tests/fixtures/profile-roots.json")).unwrap();
        let root_value = &o(&roots)["2"];
        let root = admit(root_value, [true, true]).unwrap();
        let mut envelope = V::Object(
            [
                (
                    "envelopeSchema".into(),
                    V::Integer(opensip_identity::JsonInteger::new(2).unwrap()),
                ),
                (
                    "subject".into(),
                    V::Object(
                        [
                            ("kind".into(), V::String("platform-profile-set".into())),
                            (
                                "domain".into(),
                                V::String("opensip.metadata.platform-profile-set.1".into()),
                            ),
                            (
                                "storedSha256".into(),
                                V::String(digest_hex(&raw_sha256(&stored))),
                            ),
                            ("preimageSha256".into(), V::String(digest_hex(&pin))),
                        ]
                        .into(),
                    ),
                ),
                ("role".into(), V::String("TR-PROFILE".into())),
                ("namespace".into(), V::String("opensip".into())),
                ("signatures".into(), V::Array(vec![])),
            ]
            .into(),
        );
        let message = crate::trust::envelope_message(&envelope).unwrap();
        let keys = arr(&o(root_value)["keys"]);
        let mut signatures = vec![];
        for kid in arr(&o(&o(&o(root_value)["roles"])["TR-PROFILE"])["keys"]) {
            let i = keys.iter().position(|k| &o(k)["keyId"] == kid).unwrap();
            let mut public_seed = b"opensip-public-test-only-quorum62-seed-".to_vec();
            public_seed.push(u8::try_from(i).unwrap());
            let key = SigningKey::from_bytes(&raw_sha256(&public_seed));
            assert_eq!(
                digest_hex(&key.verifying_key().to_bytes()),
                text(&o(&keys[i])["publicKey"])
            );
            let signature = key
                .sign(&message)
                .to_bytes()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            signatures.push(V::Object(
                [
                    ("keyId".into(), kid.clone()),
                    ("alg".into(), V::String("ed25519".into())),
                    ("signature".into(), V::String(signature)),
                ]
                .into(),
            ));
        }
        map(&mut envelope).insert("signatures".into(), V::Array(signatures));
        let verify = || {
            admitted_profiles::verify_profile_set(
                &root,
                &stored,
                &envelope,
                Some(pin),
                &BTreeSet::new(),
            )
            .unwrap()
        };
        let denied = native_platform::capture(verify(), &fence).unwrap();
        assert_eq!(denied.decision().tier, Some(PlatformTier::ExactMeasured));
        assert!(
            denied
                .decision()
                .refusals
                .iter()
                .any(|s| s == "NT-TCB-IDENTITY:dyldCdhash")
        );
        let mut b = budget();
        let mut foreign_calls = 0;
        // Even removing current state cannot change the expected profile-first error.
        let sid = text(&o(f.store())["storeInstanceId"]);
        fs::remove_file(f.root.join(format!("trust/stores/{sid}/state.v1"))).unwrap();
        let result = native_profile_census::capture(&mut b, verify(), &fence, f.store(), |_| {
            foreign_calls += 1;
            Ok(())
        });
        assert!(
            matches!(result,Err(native_profile_census::Error::ProfileRefused(ref why))if why.iter().any(|s|s=="NT-TCB-IDENTITY:dyldCdhash"))
        );
        assert_eq!(foreign_calls, 0);
        assert_eq!(b.counters(), (0, 0, 0));
        assert!(matches!(b.edge(1), Err(M::Error::Closed)));
    }
    #[test]
    fn native_diagnostics_current_and_nested_dependency_propagate_original_native_failure() {
        use super::super::{native_current, native_record_capture};
        for path in ["trust/publications", "trust/records"] {
            let f = Fixture::new();
            let fence = f.fence();
            fs::remove_dir_all(f.root.join(path)).unwrap();
            let mut b = budget();
            let result = native_current::capture_p2(&mut b, &fence, f.store());
            assert!(
                matches!(result,Err(native_current::Error::Immutable(native_record_capture::Error::Native(ref e)))if e.kind()==std::io::ErrorKind::NotFound),
                "{path}"
            );
            assert!(matches!(b.edge(1), Err(M::Error::Closed)));
        }
    }
}
