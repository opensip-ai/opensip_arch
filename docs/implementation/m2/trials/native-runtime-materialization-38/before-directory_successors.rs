#[cfg(test)]
use super::retained_metadata_index::Collection;
// Native bucket bytes335 + full known-logical-before STRUCTURAL relation329.
// NOT qualified census, proven publication, action authentication or authority.
use super::{
    directory_record_capture::{self, Captured},
    retained_metadata_index::{Budget, Error as BudgetError},
    successor_record_bindings::{self, SuccessorRecordBindings},
};
use crate::trust::trust_record_shapes::{self as shapes, Definition};
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes, digest_hex, raw_sha256};
use opensip_platform::RetainedChildDirectory;
use std::{collections::BTreeSet, os::unix::ffi::OsStrExt, sync::Arc};
#[derive(Debug)]
pub(super) enum Error {
    Budget(BudgetError),
    Shape(shapes::Error),
    Canonical,
    BucketName,
    Native(directory_record_capture::Error),
    Relation(successor_record_bindings::Error),
    Binding,
}
impl From<BudgetError> for Error {
    fn from(e: BudgetError) -> Self {
        Self::Budget(e)
    }
}
pub(super) struct Candidates {
    before: V,
    captured: Captured,
    links: Vec<SuccessorRecordBindings>,
}
impl Candidates {
    pub(super) fn before(&self) -> &V {
        &self.before
    }
    pub(super) fn captured(&self) -> &Captured {
        &self.captured
    }
    pub(super) fn links(&self) -> &[SuccessorRecordBindings] {
        &self.links
    }
}
/// Caller materialized BEFORE and retained the directory edge. Neither is a
/// qualified native current source here. The relative component must be the
/// canonical BEFORE digest; its ancestors/selected collection still need native
/// admission. Dependent-record store custody/authentication remains external.
pub(super) fn inspect(
    budget: &mut Budget,
    before: &V,
    directory: Arc<RetainedChildDirectory>,
    uid: u32,
    groups: &BTreeSet<u32>,
    store: &mut impl crate::trust::root_payload::retained_metadata_index::Store,
    foreign: impl FnMut(&[u8]) -> Result<(), ()>,
) -> Result<Candidates, Error> {
    budget.scope(|b| {
        // Even an empty bucket cannot bypass full BEFORE shape admission.
        let raw_before = canonical_bytes(before).map_err(|_| Error::Canonical)?;
        shapes::admit(Definition::TrustCapsuleV1, &raw_before).map_err(Error::Shape)?;
        let previous = digest_hex(&raw_sha256(&raw_before));
        if directory.component().as_bytes() != previous.as_bytes() {
            return Err(Error::BucketName);
        }
        let captured = directory_record_capture::capture(b, directory, uid, groups, foreign)
            .map_err(Error::Native)?;
        let mut links = Vec::new();
        for record in captured.records() {
            let reference = V::Object(
                [
                    ("previousCapsule".into(), V::String(previous.clone())),
                    ("sha256".into(), V::String(digest_hex(&record.digest()))),
                    (
                        "bytes".into(),
                        V::Integer(
                            JsonInteger::new(record.raw().len() as i128)
                                .map_err(|_| Error::Canonical)?,
                        ),
                    ),
                ]
                .into(),
            );
            let link = successor_record_bindings::bind(b, before, &reference, store)
                .map_err(Error::Relation)?;
            if link.raw() != record.raw() {
                return Err(Error::Binding);
            }
            links.push(link);
        }
        Ok(Candidates {
            before: before.clone(),
            captured,
            links,
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
        ffi::OsStr,
        fs::{self, File, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt},
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
    fn collection(v: &V) -> Collection {
        match text(v) {
            "publications" => Collection::Publications,
            "records" => Collection::Records,
            "events" => Collection::Events,
            "objects" => Collection::Objects,
            _ => panic!(),
        }
    }
    fn rows() -> Vec<V> {
        include_bytes!("../../tests/fixtures/successor-link329.ndjson")
            .split(|x| *x == b'\n')
            .filter(|x| !x.is_empty())
            .map(|x| parse_json(x).unwrap())
            .collect()
    }
    fn files(q: &BTreeMap<String, V>) -> BTreeMap<(Collection, [u8; 32]), Vec<u8>> {
        array(&q["store"])
            .iter()
            .map(|r| {
                let r = obj(r);
                (
                    (
                        collection(&r["collection"]),
                        bytes(&r["sha256"]).try_into().unwrap(),
                    ),
                    bytes(r.get("rawHex").or_else(|| r.get("raw")).unwrap()),
                )
            })
            .collect()
    }
    fn primary(
        q: &BTreeMap<String, V>,
        files: &BTreeMap<(Collection, [u8; 32]), Vec<u8>>,
    ) -> Vec<u8> {
        files[&(
            Collection::Publications,
            bytes(&obj(&q["reference"])["sha256"]).try_into().unwrap(),
        )]
            .clone()
    }
    fn budget() -> Budget {
        Budget::new(65536, 131072, 268435456).unwrap()
    }
    struct Fixture {
        root: PathBuf,
        bucket: PathBuf,
        edge: Arc<RetainedChildDirectory>,
        uid: u32,
    }
    impl Fixture {
        fn new(before: &V, wrong: bool) -> Self {
            let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
            let root = std::env::temp_dir().join(format!("opensip-directory-successors-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let name = if wrong {
                "wrong".to_owned()
            } else {
                digest_hex(&raw_sha256(&canonical_bytes(before).unwrap()))
            };
            let bucket = root.join(&name);
            fs::create_dir(&bucket).unwrap();
            fs::set_permissions(&bucket, Permissions::from_mode(0o700)).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            let edge = Arc::new(
                RetainedDirectory::from_retained_handle(File::open(&root).unwrap())
                    .unwrap()
                    .bind_child_directory(OsStr::new(&name))
                    .unwrap(),
            );
            Self {
                root,
                bucket,
                edge,
                uid,
            }
        }
        fn write(&self, raw: &[u8]) {
            let path = self.bucket.join(digest_hex(&raw_sha256(raw)));
            fs::write(&path, raw).unwrap();
            fs::set_permissions(path, Permissions::from_mode(0o600)).unwrap();
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    fn run(
        b: &mut Budget,
        before: &V,
        f: &Fixture,
        files: &BTreeMap<(Collection, [u8; 32]), Vec<u8>>,
    ) -> Result<Candidates, Error> {
        inspect(
            b,
            before,
            Arc::clone(&f.edge),
            f.uid,
            &BTreeSet::new(),
            &mut |c, h, cap| {
                let raw = files.get(&(c, h)).ok_or(())?;
                if raw.len() > cap {
                    return Err(());
                }
                Ok(raw.clone())
            },
            |_| Ok(()),
        )
    }
    #[test]
    fn directory_successors_native_joins_all_sixty_one_positive_reference_cases() {
        let mut count = 0;
        for q in rows() {
            let q = obj(&q);
            let expected = obj(&array(&q["outcomes"])[0]);
            if expected["ok"] != V::Bool(true) {
                continue;
            }
            let files = files(q);
            let raw = primary(q, &files);
            let f = Fixture::new(&q["before"], false);
            f.write(&raw);
            let mut b = budget();
            let got = run(&mut b, &q["before"], &f, &files)
                .unwrap_or_else(|e| panic!("{} {e:?}", text(&q["label"])));
            assert_eq!(got.before(), &q["before"]);
            assert_eq!(got.links().len(), 1);
            assert_eq!(got.captured().records().len(), 1);
            let counts = array(&expected["counters"]);
            let as_count = |v: &V| {
                let V::Integer(n) = v else { panic!() };
                usize::try_from(n.get()).unwrap()
            };
            assert_eq!(
                b.counters(),
                (
                    as_count(&counts[0]) + 1,
                    as_count(&counts[1]) + 5,
                    as_count(&counts[2]) + 67
                ),
                "{} shared native increments",
                text(&q["label"])
            );
            let want = obj(&expected["expected"]);
            assert_eq!(got.links()[0].reference(), &want["reference"]);
            assert_eq!(got.links()[0].clock().bound().capsule(), &want["capsule"]);
            assert_eq!(got.links()[0].clock().bound().before(), Some(&q["before"]));
            assert_eq!(got.links()[0].raw(), raw);
            assert_eq!(
                got.captured().records()[0].file().metadata().unwrap().ino(),
                got.captured().records()[0].observation().metadata.inode
            );
            drop(files);
            drop(b);
            drop(f);
            assert_eq!(got.captured().records()[0].raw(), got.links()[0].raw());
            count += 1;
        }
        assert_eq!(count, 61);
    }
    #[test]
    fn directory_successors_empty_still_binds_before_shape_and_component_before_io() {
        let rows = rows();
        let before = &obj(&rows[0])["before"];
        let f = Fixture::new(before, false);
        let mut b = budget();
        let got = run(&mut b, before, &f, &BTreeMap::new()).unwrap();
        assert!(got.links().is_empty());
        assert_eq!(got.before(), before);
        assert_eq!(b.counters(), (1, 3, 3));
        for (v, wrong) in [(before.clone(), true), (V::Null, false)] {
            let f = Fixture::new(&v, wrong);
            let mut b = budget();
            assert!(run(&mut b, &v, &f, &BTreeMap::new()).is_err());
            assert_eq!(b.counters(), (0, 0, 0));
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
    }
    #[test]
    fn directory_successors_hashed_but_malformed_or_misbound_candidates_refuse() {
        let rows = rows();
        let q = obj(&rows[0]);
        let before = &q["before"];
        let files = files(q);
        let original = primary(q, &files);
        for change in ["not-json", "revision", "previous", "operation"] {
            let f = Fixture::new(before, false);
            let mut value = parse_json(&original).unwrap();
            let raw = if change == "not-json" {
                b"not-json".to_vec()
            } else {
                let V::Object(ref mut o) = value else {
                    panic!()
                };
                match change {
                    "revision" => {
                        o.insert(
                            "revision".into(),
                            V::Integer(JsonInteger::new(999).unwrap()),
                        );
                    }
                    "previous" => {
                        o.insert("previousCapsule".into(), V::String("0".repeat(64)));
                    }
                    _ => {
                        let V::Object(op) = o.get_mut("operation").unwrap() else {
                            panic!()
                        };
                        op.insert("sha256".into(), V::String("0".repeat(64)));
                    }
                }
                canonical_bytes(&value).unwrap()
            };
            f.write(&raw);
            let mut b = budget();
            assert!(
                matches!(run(&mut b, before, &f, &files), Err(Error::Relation(_))),
                "{change}"
            );
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
    }
    #[test]
    fn directory_successors_all_candidates_and_missing_evidence_are_not_partial_success() {
        let rows = rows();
        let q = obj(&rows[0]);
        let before = &q["before"];
        let files = files(q);
        let raw = primary(q, &files);
        let good = raw_sha256(&raw);
        let invalid = (0..4096)
            .map(|i| format!("not-json-{i}").into_bytes())
            .find(|b| raw_sha256(b) > good)
            .unwrap();
        let f = Fixture::new(before, false);
        f.write(&raw);
        f.write(&invalid);
        let mut b = budget();
        assert!(matches!(
            run(&mut b, before, &f, &files),
            Err(Error::Relation(_))
        ));
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
        let f = Fixture::new(before, false);
        f.write(&raw);
        let mut b = budget();
        assert!(matches!(
            run(&mut b, before, &f, &BTreeMap::new()),
            Err(Error::Relation(_))
        ));
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
    }
}
