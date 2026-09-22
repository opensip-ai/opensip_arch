#[cfg(test)]
use super::retained_metadata_index::Collection;
// Immediate + every following bucket, using native opens and336 structural joins.
// Observations only: no qualified current/clean/behind/fork or write authority.
use super::{
    directory_successors::{self, Candidates},
    retained_metadata_index::{Budget, Error as BudgetError},
};
use crate::{
    custody::{DirectoryPathRefusal, directory_policy},
    trust::trust_record_shapes::{self as shapes, Definition},
};
use opensip_identity::{JsonValue as V, canonical_bytes, digest_hex, raw_sha256};
use opensip_platform::RetainedChildDirectory;
use std::{collections::BTreeSet, ffi::OsStr, io, sync::Arc};
#[derive(Debug)]
pub(super) enum Error {
    Budget(BudgetError),
    Shape(shapes::Error),
    Canonical,
    RootComponent,
    Root(DirectoryPathRefusal),
    Open(io::Error),
    Candidate(directory_successors::Error),
}
impl From<BudgetError> for Error {
    fn from(e: BudgetError) -> Self {
        Self::Budget(e)
    }
}
pub(super) struct Bucket {
    before: V,
    // None ONLY after actual NotFound under bracketing root policy/name samples.
    // It is not an admitted absence, and must not itself authorize creation.
    candidates: Option<Candidates>,
}
impl Bucket {
    pub(super) fn before(&self) -> &V {
        &self.before
    }
    pub(super) fn candidates(&self) -> Option<&Candidates> {
        self.candidates.as_ref()
    }
    pub(super) fn is_observed_missing(&self) -> bool {
        self.candidates.is_none()
    }
}
pub(super) struct Observed {
    root: Arc<RetainedChildDirectory>,
    current: Bucket,
    following: Vec<Bucket>,
    supported: Vec<usize>,
}
impl Observed {
    pub(super) fn root(&self) -> &RetainedChildDirectory {
        &self.root
    }
    pub(super) fn current(&self) -> &Bucket {
        &self.current
    }
    pub(super) fn following(&self) -> &[Bucket] {
        &self.following
    }
    /// Indices of immediate candidates with at least one structurally valid
    /// following descriptor, after ALL following buckets have been inspected.
    pub(super) fn structurally_supported(&self) -> &[usize] {
        &self.supported
    }
}
struct Context<'a, F> {
    root: &'a Arc<RetainedChildDirectory>,
    uid: u32,
    groups: &'a BTreeSet<u32>,
    store: &'a mut F,
}
fn bucket(
    b: &mut Budget,
    before: &V,
    ctx: &mut Context<'_, impl crate::trust::root_payload::retained_metadata_index::Store>,
    foreign: &mut impl FnMut(&[u8]) -> Result<(), ()>,
    after_open: impl FnOnce(),
) -> Result<Bucket, Error> {
    let raw = canonical_bytes(before).map_err(|_| Error::Canonical)?;
    shapes::admit(Definition::TrustCapsuleV1, &raw).map_err(Error::Shape)?;
    let name = digest_hex(&raw_sha256(&raw));
    b.edge(1)?; // Charge lookup BEFORE scheduling the native child open.
    directory_policy::inspect(ctx.root, ctx.uid, ctx.groups).map_err(Error::Root)?;
    let opened = ctx.root.directory().bind_child_directory(OsStr::new(&name));
    after_open();
    directory_policy::inspect(ctx.root, ctx.uid, ctx.groups).map_err(Error::Root)?;
    let candidates = match opened {
        Ok(edge) => Some(
            directory_successors::inspect(
                b,
                before,
                Arc::new(edge),
                ctx.uid,
                ctx.groups,
                ctx.store,
                foreign,
            )
            .map_err(Error::Candidate)?,
        ),
        Err(e) if e.kind() == io::ErrorKind::NotFound => None,
        Err(e) => return Err(Error::Open(e)),
    };
    Ok(Bucket {
        before: before.clone(),
        candidates,
    })
}
/// Root and materialized BEFORE are caller-supplied inputs, not sealed native
/// producers. Root must have saved component by-predecessor; selected ancestors,
/// supported profile and a held installation fence remain outside this helper.
pub(super) fn observe(
    b: &mut Budget,
    before: &V,
    root: Arc<RetainedChildDirectory>,
    uid: u32,
    groups: &BTreeSet<u32>,
    store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
    mut foreign: impl FnMut(&[u8]) -> Result<(), ()>,
) -> Result<Observed, Error> {
    b.scope(|b| {
        let raw = canonical_bytes(before).map_err(|_| Error::Canonical)?;
        shapes::admit(Definition::TrustCapsuleV1, &raw).map_err(Error::Shape)?;
        if root.component() != OsStr::new("by-predecessor") {
            return Err(Error::RootComponent);
        }
        directory_policy::inspect(&root, uid, groups).map_err(Error::Root)?;
        b.directory(Arc::clone(&root))?;
        let mut ctx = Context {
            root: &root,
            uid,
            groups,
            store,
        };
        let current = bucket(b, before, &mut ctx, &mut foreign, || {})?;
        let mut following = Vec::new();
        let mut supported = Vec::new();
        if let Some(candidates) = current.candidates() {
            for (index, link) in candidates.links().iter().enumerate() {
                let next = bucket(
                    b,
                    link.clock().bound().capsule(),
                    &mut ctx,
                    &mut foreign,
                    || {},
                )?;
                //336 binds EVERY next candidate, including a restore's ORIGINAL
                //278 structural proof/DIRECT terminal, before this existence test.
                if next.candidates().is_some_and(|c| !c.links().is_empty()) {
                    supported.push(index);
                }
                following.push(next);
            }
        }
        directory_policy::inspect(&root, uid, groups).map_err(Error::Root)?;
        Ok(Observed {
            root,
            current,
            following,
            supported,
        })
    })
}

#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use opensip_identity::parse_json;
    use opensip_platform::RetainedDirectory;
    use std::{
        collections::BTreeMap,
        fs::{self, File, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt, symlink},
        path::PathBuf,
    };
    fn obj(v: &V) -> &BTreeMap<String, V> {
        let V::Object(x) = v else { panic!() };
        x
    }
    fn array(v: &V) -> &[V] {
        let V::Array(x) = v else { panic!() };
        x
    }
    fn text(v: &V) -> &str {
        let V::String(x) = v else { panic!() };
        x
    }
    fn bytes(v: &V) -> Vec<u8> {
        text(v)
            .as_bytes()
            .chunks_exact(2)
            .map(|x| u8::from_str_radix(std::str::from_utf8(x).unwrap(), 16).unwrap())
            .collect()
    }
    fn col(v: &V) -> Collection {
        match text(v) {
            "publications" => Collection::Publications,
            "records" => Collection::Records,
            "events" => Collection::Events,
            "objects" => Collection::Objects,
            _ => panic!(),
        }
    }
    fn row(label: &str) -> V {
        include_bytes!("../../tests/fixtures/successor-link329.ndjson")
            .split(|x| *x == b'\n')
            .filter(|x| !x.is_empty())
            .map(|x| parse_json(x).unwrap())
            .find(|v| text(&obj(v)["label"]) == label)
            .unwrap()
    }
    type Files = BTreeMap<(Collection, [u8; 32]), Vec<u8>>;
    struct Fixture {
        root: PathBuf,
        edge: Arc<RetainedChildDirectory>,
        uid: u32,
        files: Files,
    }
    impl Fixture {
        fn new() -> Self {
            let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
            let root = std::env::temp_dir().join(format!("opensip-directory-provers-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            fs::create_dir(root.join("by-predecessor")).unwrap();
            fs::set_permissions(root.join("by-predecessor"), Permissions::from_mode(0o700))
                .unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            let edge = Arc::new(
                RetainedDirectory::from_retained_handle(File::open(&root).unwrap())
                    .unwrap()
                    .bind_child_directory(OsStr::new("by-predecessor"))
                    .unwrap(),
            );
            Self {
                root,
                edge,
                uid,
                files: BTreeMap::new(),
            }
        }
        fn path(&self, before: &V) -> PathBuf {
            self.root
                .join("by-predecessor")
                .join(digest_hex(&raw_sha256(&canonical_bytes(before).unwrap())))
        }
        fn empty(&self, before: &V) {
            let p = self.path(before);
            if !p.exists() {
                fs::create_dir(&p).unwrap();
                fs::set_permissions(&p, Permissions::from_mode(0o700)).unwrap();
            }
        }
        fn add(&mut self, label: &str) -> V {
            let q = row(label);
            let q = obj(&q);
            self.empty(&q["before"]);
            for r in array(&q["store"]) {
                let r = obj(r);
                let key = (
                    col(&r["collection"]),
                    bytes(&r["sha256"]).try_into().unwrap(),
                );
                let raw = bytes(r.get("rawHex").or_else(|| r.get("raw")).unwrap());
                if let Some(old) = self.files.insert(key, raw.clone()) {
                    assert_eq!(old, raw);
                }
            }
            let reference = obj(&q["reference"]);
            let digest = bytes(&reference["sha256"]).try_into().unwrap();
            let raw = &self.files[&(Collection::Publications, digest)];
            let p = self.path(&q["before"]).join(digest_hex(&digest));
            fs::write(&p, raw).unwrap();
            fs::set_permissions(&p, Permissions::from_mode(0o600)).unwrap();
            q["before"].clone()
        }
        fn run(&self, b: &mut Budget, before: &V) -> Result<Observed, Error> {
            observe(
                b,
                before,
                Arc::clone(&self.edge),
                self.uid,
                &BTreeSet::new(),
                &mut |c, h, cap| {
                    let raw = self.files.get(&(c, h)).ok_or(())?;
                    if raw.len() > cap {
                        return Err(());
                    }
                    Ok(raw.clone())
                },
                |_| Ok(()),
            )
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    fn budget() -> Budget {
        Budget::new(65536, 131072, 268435456).unwrap()
    }
    #[test]
    fn directory_provers_missing_empty_and_unproven_are_distinct_owned_observations() {
        let mut f = Fixture::new();
        let q = row("empty-link-0");
        let before = &obj(&q)["before"];
        let mut b = budget();
        let missing = f.run(&mut b, before).unwrap();
        assert!(missing.current().is_observed_missing());
        assert!(missing.following().is_empty());
        assert_eq!(b.counters(), (1, 2, 0));
        assert!(missing.root().recheck().unwrap());
        f.empty(before);
        let mut b = budget();
        let empty = f.run(&mut b, before).unwrap();
        assert!(!empty.current().is_observed_missing());
        assert!(empty.current().candidates().unwrap().links().is_empty());
        assert_eq!(b.counters(), (2, 5, 3));
        f.add("empty-link-0");
        let mut b = budget();
        let unproven = f.run(&mut b, before).unwrap();
        assert_eq!(unproven.current().candidates().unwrap().links().len(), 1);
        assert_eq!(unproven.following().len(), 1);
        assert!(unproven.following()[0].is_observed_missing());
        assert!(unproven.structurally_supported().is_empty());
        assert_eq!(unproven.current().before(), before);
        drop(f);
        assert_eq!(unproven.current().before(), before);
    }
    #[test]
    fn directory_provers_all_following_buckets_support_one_or_multiple_children() {
        let mut f = Fixture::new();
        let before = f.add("empty-link-0");
        f.add("empty-link-1");
        let mut b = budget();
        let one = f.run(&mut b, &before).unwrap();
        assert_eq!(one.structurally_supported(), &[0]);
        assert_eq!(one.following().len(), 1);
        f.add("clock-link-0");
        f.add("clock-link-1");
        let mut b = budget();
        let two = f.run(&mut b, &before).unwrap();
        assert_eq!(two.structurally_supported(), &[0, 1]);
        assert_eq!(two.following().len(), 2);
        for (i, next) in two.following().iter().enumerate() {
            assert_eq!(
                next.before(),
                two.current().candidates().unwrap().links()[i]
                    .clock()
                    .bound()
                    .capsule()
            );
        }
    }
    #[test]
    fn directory_provers_restore_following_requires_original_structural_proof() {
        let mut f = Fixture::new();
        let before = f.add("empty-link-0");
        f.add("empty-restored-structural-link");
        let mut b = budget();
        let got = f.run(&mut b, &before).unwrap();
        assert_eq!(got.structurally_supported(), &[0]);
        assert!(
            got.following()[0].candidates().unwrap().links()[0]
                .original_restore()
                .is_some()
        );
        // Remove ONLY the original restore proof's DIRECT terminal witness;
        // keep immediate operation and all unrelated dependencies available.
        let proof = got.following()[0].candidates().unwrap().links()[0]
            .original_restore()
            .unwrap()
            .proof();
        let terminal: [u8; 32] = bytes(&obj(&obj(proof)["terminalWitness"])["sha256"])
            .try_into()
            .unwrap();
        assert!(
            f.files
                .remove(&(Collection::Publications, terminal))
                .is_some()
        );
        let mut b = budget();
        assert!(f.run(&mut b, &before).is_err());
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
    }
    #[test]
    fn directory_provers_late_bad_following_refuses_even_after_a_supported_child() {
        let mut f = Fixture::new();
        let before = f.add("empty-link-0");
        f.add("empty-link-1");
        f.add("clock-link-0");
        f.add("clock-link-1");
        let mut b = budget();
        let good = f.run(&mut b, &before).unwrap();
        assert_eq!(good.structurally_supported().len(), 2);
        let last = good.following().last().unwrap().before();
        let raw = b"not-json";
        let path = f.path(last).join(digest_hex(&raw_sha256(raw)));
        fs::write(&path, raw).unwrap();
        fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
        let mut b = budget();
        assert!(f.run(&mut b, &before).is_err());
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
        assert_eq!(fs::read(path).unwrap(), raw);
    }
    #[test]
    fn directory_provers_wrong_kind_and_root_mutation_never_become_observed_missing() {
        let q = row("empty-link-0");
        let before = &obj(&q)["before"];
        for kind in ["regular", "symlink"] {
            let f = Fixture::new();
            let p = f.path(before);
            if kind == "regular" {
                fs::write(&p, b"keep").unwrap();
            } else {
                symlink("absent", &p).unwrap();
            }
            let mut b = budget();
            assert!(matches!(f.run(&mut b, before), Err(Error::Open(_))));
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
        let f = Fixture::new();
        let groups = BTreeSet::new();
        let mut store = |_, _, _| Err(());
        let mut ctx = Context {
            root: &f.edge,
            uid: f.uid,
            groups: &groups,
            store: &mut store,
        };
        let mut b = budget();
        let result = b.scope(|b| {
            bucket(b, before, &mut ctx, &mut |_| Ok(()), || {
                fs::rename(f.root.join("by-predecessor"), f.root.join("old")).unwrap();
                fs::create_dir(f.root.join("by-predecessor")).unwrap();
            })
        });
        assert!(matches!(result, Err(Error::Root(_))));
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
    }
    #[test]
    fn directory_provers_lookup_and_following_share_the_same_failure_budget() {
        let mut f = Fixture::new();
        let before = f.add("empty-link-0");
        f.add("empty-link-1");
        let mut full = budget();
        f.run(&mut full, &before).unwrap();
        // Independent fixed-fixture accounting: two 4478-byte descriptors,
        // one shared 421-byte operation, two sets of dot/hash names (67 each),
        // three native directories; root edge + two lookups + 2*(2+5) visits.
        // This is not derived from the producer being tested.
        assert_eq!(full.counters(), (6, 17, 9511));
        let (o, e, n) = full.counters();
        for limits in [(o - 1, e, n), (o, e - 1, n), (o, e, n - 1)] {
            let mut b = Budget::new(limits.0, limits.1, limits.2).unwrap();
            assert!(f.run(&mut b, &before).is_err(), "{limits:?}");
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
        let mut exact = Budget::new(o, e, n).unwrap();
        assert_eq!(
            f.run(&mut exact, &before).unwrap().structurally_supported(),
            &[0]
        );
        let mut b = budget();
        assert!(matches!(f.run(&mut b, &V::Null), Err(Error::Shape(_))));
        assert_eq!(b.counters(), (0, 0, 0));
    }
    #[test]
    fn directory_provers_wrong_root_component_refuses_before_any_budgeted_io() {
        let f = Fixture::new();
        fs::create_dir(f.root.join("wrong")).unwrap();
        let wrong = Arc::new(
            RetainedDirectory::from_retained_handle(File::open(&f.root).unwrap())
                .unwrap()
                .bind_child_directory(OsStr::new("wrong"))
                .unwrap(),
        );
        let q = row("empty-link-0");
        let before = &obj(&q)["before"];
        let mut b = budget();
        assert!(matches!(
            observe(
                &mut b,
                before,
                wrong,
                f.uid,
                &BTreeSet::new(),
                &mut |_, _, _| panic!("wrong root reached store"),
                |_| panic!("wrong root reached visitor")
            ),
            Err(Error::RootComponent)
        ));
        assert_eq!(b.counters(), (0, 0, 0));
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
    }
}
