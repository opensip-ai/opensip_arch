// One provisional native-current read session. Not current authority, profile
// admission, durable standing, a full store binding, or permission to write.
use super::{
    native_census, native_current,
    retained_metadata_index::{self as M, Budget},
};
use crate::installation_observation::{InstallationReadFence, same_filesystem};
use opensip_identity::JsonValue;
use opensip_platform::DescriptorFilesystem;

#[derive(Debug)]
pub struct NativeTrustReadError(Reason);
#[allow(dead_code)]
#[derive(Debug)]
enum Reason {
    Budget(M::Error),
    Current(native_current::Error),
    Census(native_census::Error),
    Fence(crate::installation_observation::Error),
    Native(std::io::Error),
    Filesystem,
    MissingHead,
}
impl From<M::Error> for NativeTrustReadError {
    fn from(error: M::Error) -> Self {
        Self(Reason::Budget(error))
    }
}
impl std::fmt::Display for NativeTrustReadError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.0)
    }
}
impl std::error::Error for NativeTrustReadError {}

/// Copied structural counts only, never clean/behind/fork or write authority.
/// Missing publication root differs from a missing immediate candidate bucket.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ProvisionalSuccessorCounts {
    pub publication_root_observed_missing: bool,
    pub immediate_bucket_observed_missing: Option<bool>,
    pub immediate_candidates: usize,
    pub following_buckets: usize,
    pub structurally_supported_candidates: usize,
}
/// Retains every original current File and one cumulative trust-read budget.
/// The requested three-field store is only an expected comparison against the
/// independently parsed current record. Namespace/registry/lineage, full binding,
/// core/profile and current authority remain unestablished. Structural census
/// observations do not confer those missing forms of admission.
/// No File/root/guard/budget escape, reset, or promotion to an admitted handle.
///
/// ```compile_fail,E0505
/// use opensip_security::{NativeTrustReadSession, installation_observation::InstallationReadFence};
/// use opensip_identity::JsonValue;
/// fn invalid(fence: InstallationReadFence, expected: &JsonValue) {
///     let mut session = NativeTrustReadSession::capture(&fence, expected).unwrap();
///     drop(fence);
///     session.raw_current().unwrap();
/// }
/// ```
/// ```compile_fail,E0515
/// use opensip_security::{NativeTrustReadSession, installation_observation::InstallationReadFence};
/// use opensip_identity::JsonValue;
/// fn escape(fence: InstallationReadFence, expected: &JsonValue) -> NativeTrustReadSession<'static> {
///     NativeTrustReadSession::capture(&fence, expected).unwrap()
/// }
/// ```
pub struct NativeTrustReadSession<'f> {
    fence: &'f InstallationReadFence,
    budget: Budget,
    heads: Vec<native_current::Head<'f>>,
    censuses: Vec<native_census::SuppliedCensus<'f>>,
}
impl<'f> NativeTrustReadSession<'f> {
    /// Fixed global bounds apply to this logical read, not separately per object.
    /// Caller JSON is validated by the existing full StoreBinding owner before IO.
    pub fn capture(
        fence: &'f InstallationReadFence,
        expected_store: &JsonValue,
    ) -> Result<Self, NativeTrustReadError> {
        let mut session = Self {
            fence,
            budget: Budget::new(65536, 131072, 268435456)?,
            heads: Vec::new(),
            censuses: Vec::new(),
        };
        session.append(expected_store)?;
        Ok(session)
    }
    fn append(&mut self, expected: &JsonValue) -> Result<(), NativeTrustReadError> {
        self.append_with(expected, || {})
    }
    fn append_with(
        &mut self,
        expected: &JsonValue,
        after_attempt: impl FnOnce(),
    ) -> Result<(), NativeTrustReadError> {
        let fence = self.fence;
        let heads = &self.heads;
        let censuses = &self.censuses;
        let head = self.budget.scope(|budget| {
            // Validate the complete bounded request before native IO or copying.
            native_current::store_id(expected)
                .map_err(|e| NativeTrustReadError(Reason::Current(e)))?;
            check_all(fence, heads, censuses)?;
            let attempted: Result<_, NativeTrustReadError> = (|| {
                let head = native_current::capture_head(
                    budget,
                    fence.native_guard().as_supplied(),
                    expected,
                )
                .map_err(|e| NativeTrustReadError(Reason::Current(e)))?;
                check_all(fence, std::slice::from_ref(&head), censuses)?;
                Ok(head)
            })();
            after_attempt();
            check_all(fence, heads, censuses)?; // Also after failed parse/read/store comparison.
            attempted
        })?;
        self.heads.push(head);
        Ok(())
    }
    /// Repeat actual path presence/capture under the SAME budget. Every old File
    /// remains retained and is rechecked before/after; a fresh open cannot replace
    /// earlier evidence. The store expectation comes from the first parsed C.
    pub fn observe_again(&mut self) -> Result<(), NativeTrustReadError> {
        self.recheck()?;
        let expected = self.store_claim()?.clone(); // Already validated bounded triple.
        self.append(&expected)
    }
    /// A failed read or recheck latches this entire session unavailable. Repairing
    /// the path afterward does not revive the session or reset its budget.
    pub fn recheck(&mut self) -> Result<(), NativeTrustReadError> {
        let fence = self.fence;
        let heads = &self.heads;
        let censuses = &self.censuses;
        self.budget.scope(|_| check_all(fence, heads, censuses))
    }
    /// Historical/provisional bytes, not an admitted current-authority token.
    pub fn raw_current(&mut self) -> Result<&[u8], NativeTrustReadError> {
        self.recheck()?;
        Ok(self
            .heads
            .first()
            .ok_or(NativeTrustReadError(Reason::MissingHead))?
            .raw())
    }
    /// Return the three fields from independently captured C, never request JSON.
    pub fn store_claim(&mut self) -> Result<&JsonValue, NativeTrustReadError> {
        self.recheck()?;
        let head = self
            .heads
            .first()
            .ok_or(NativeTrustReadError(Reason::MissingHead))?;
        match head.value() {
            JsonValue::Object(record) => record
                .get("store")
                .ok_or(NativeTrustReadError(Reason::MissingHead)),
            _ => Err(NativeTrustReadError(Reason::MissingHead)),
        }
    }
    /// Read the complete bounded immediate/following structural census through
    /// the same native fence and Budget. Keep every original file, including
    /// those from earlier calls. A callback failure closes this entire session.
    /// Foreign names have already been charged before the callback sees them.
    pub fn observe_successors(
        &mut self,
        foreign: impl FnMut(&[u8]) -> Result<(), ()>,
    ) -> Result<ProvisionalSuccessorCounts, NativeTrustReadError> {
        self.recheck()?;
        let expected = self.store_claim()?.clone();
        let fence = self.fence;
        let heads = &self.heads;
        let censuses = &self.censuses;
        let census = self.budget.scope(|budget| {
            check_all(fence, heads, censuses)?;
            let attempted: Result<_, NativeTrustReadError> = (|| {
                let census = native_census::capture(
                    budget,
                    fence.native_guard().as_supplied(),
                    &expected,
                    foreign,
                )
                .map_err(|e| NativeTrustReadError(Reason::Census(e)))?;
                check_all(fence, heads, std::slice::from_ref(&census))?;
                Ok(census)
            })();
            check_all(fence, heads, censuses)?; // Failed census still checks prior evidence.
            attempted
        })?;
        let counts = successor_counts(&census);
        self.censuses.push(census);
        Ok(counts)
    }
    /// None means no census has been requested, not an empty admitted universe.
    pub fn latest_successor_counts(
        &mut self,
    ) -> Result<Option<ProvisionalSuccessorCounts>, NativeTrustReadError> {
        self.recheck()?;
        Ok(self.censuses.last().map(successor_counts))
    }
    /// Diagnostic cumulative object/edge/byte use, not a remaining authority grant.
    pub fn counters(&self) -> (usize, usize, usize) {
        self.budget.counters()
    }
}
fn check_all(
    fence: &InstallationReadFence,
    heads: &[native_current::Head<'_>],
    censuses: &[native_census::SuppliedCensus<'_>],
) -> Result<(), NativeTrustReadError> {
    fence
        .recheck()
        .map_err(|e| NativeTrustReadError(Reason::Fence(e)))?;
    let checked = (|| {
        let held = fence.native_guard().as_supplied();
        let root = held
            .root()
            .directory()
            .observe_filesystem()
            .map_err(|e| NativeTrustReadError(Reason::Native(e)))?;
        let carrier = held
            .observe_filesystem()
            .map_err(|e| NativeTrustReadError(Reason::Current(native_current::Error::Fence(e))))?;
        if !same_filesystem(&root, &carrier) {
            return Err(NativeTrustReadError(Reason::Filesystem));
        }
        for head in heads {
            head.visit_filesystems(&mut |sample: &DescriptorFilesystem| {
                if same_filesystem(&root, sample) {
                    Ok(())
                } else {
                    Err(std::io::Error::other(
                        "provisional trust file outside installation filesystem",
                    ))
                }
            })
            .map_err(|e| NativeTrustReadError(Reason::Current(e)))?;
        }
        for census in censuses {
            census
                .visit_filesystems(&mut |sample: &DescriptorFilesystem| {
                    if same_filesystem(&root, sample) {
                        Ok(())
                    } else {
                        Err(std::io::Error::other(
                            "provisional census file outside installation filesystem",
                        ))
                    }
                })
                .map_err(|e| NativeTrustReadError(Reason::Census(e)))?;
        }
        Ok(())
    })();
    fence
        .recheck()
        .map_err(|e| NativeTrustReadError(Reason::Fence(e)))?;
    checked
}

fn successor_counts(census: &native_census::SuppliedCensus<'_>) -> ProvisionalSuccessorCounts {
    let observed = census.observed();
    ProvisionalSuccessorCounts {
        publication_root_observed_missing: observed.is_none(),
        immediate_bucket_observed_missing: observed.map(|o| o.current().is_observed_missing()),
        immediate_candidates: observed
            .and_then(|o| o.current().candidates())
            .map_or(0, |c| c.links().len()),
        following_buckets: observed.map_or(0, |o| o.following().len()),
        structurally_supported_candidates: observed.map_or(0, |o| o.structurally_supported().len()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use opensip_identity::{JsonInteger, canonical_bytes, parse_json};
    use std::{
        collections::BTreeMap,
        fs::{self, Permissions},
        os::unix::fs::PermissionsExt,
        path::{Path, PathBuf},
    };
    const SID: &str = "11111111111111111111111111111111";
    fn object(value: &JsonValue) -> &BTreeMap<String, JsonValue> {
        let JsonValue::Object(o) = value else {
            panic!("fixture object")
        };
        o
    }
    fn sample() -> (Vec<u8>, JsonValue) {
        let row = parse_json(
            include_bytes!("../../tests/fixtures/captured-capsule306.ndjson")
                .split(|b| *b == b'\n')
                .find(|s| !s.is_empty())
                .unwrap(),
        )
        .unwrap();
        let JsonValue::Array(outcomes) = &object(&row)["outcomes"] else {
            panic!("fixture outcomes")
        };
        let capsule = &object(&object(&outcomes[0])["expected"])["capsule"];
        (
            canonical_bytes(capsule).unwrap(),
            object(capsule)["store"].clone(),
        )
    }
    // Synthetic account-home fixture, same existing native source recheck seam.
    // Not evidence that the actual user's I is selected or admitted.
    struct Fixture {
        home: PathBuf,
        root: PathBuf,
    }
    impl Fixture {
        fn new() -> Self {
            let id = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
                &opensip_platform::request_entropy().unwrap(),
            ));
            let home = std::env::temp_dir().join(format!("opensip-trust-session361-{id}"));
            fs::create_dir(&home).unwrap();
            fs::set_permissions(&home, Permissions::from_mode(0o700)).unwrap();
            let home = fs::canonicalize(home).unwrap();
            let mut root = home.clone();
            for name in ["Library", "Application Support", "OpenSIP", "preview-v1"] {
                root.push(name);
                fs::create_dir(&root).unwrap();
                fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            }
            let s = Self { home, root };
            s.write("lifecycle.fence", b"");
            s
        }
        fn write(&self, rel: &str, bytes: &[u8]) -> PathBuf {
            let mut p = self.root.clone();
            for part in Path::new(rel).parent().unwrap().components() {
                p.push(part);
                if !p.exists() {
                    fs::create_dir(&p).unwrap();
                }
                fs::set_permissions(&p, Permissions::from_mode(0o700)).unwrap();
            }
            let p = self.root.join(rel);
            fs::write(&p, bytes).unwrap();
            fs::set_permissions(&p, Permissions::from_mode(0o600)).unwrap();
            p
        }
        fn current(&self, bytes: &[u8]) -> PathBuf {
            self.write(&format!("trust/stores/{SID}/state.v1"), bytes)
        }
        fn fence(&self) -> InstallationReadFence {
            InstallationReadFence::fixture_at(&self.home)
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.home);
        }
    }
    #[test]
    fn native_session_actual_current_and_repeated_reads_share_one_budget() {
        let f = Fixture::new();
        let (raw, expected) = sample();
        f.current(&raw);
        let fence = f.fence();
        let mut session = NativeTrustReadSession::capture(&fence, &expected).unwrap();
        assert_eq!(session.raw_current().unwrap(), raw);
        assert_eq!(session.store_claim().unwrap(), &expected);
        assert_eq!(session.counters(), (4, 7, 1435));
        session.observe_again().unwrap();
        assert_eq!(session.counters(), (4, 14, 1435));
        assert_eq!(session.heads.len(), 2);
        session.observe_again().unwrap();
        assert_eq!(session.counters(), (4, 21, 1435));
        assert_eq!(session.heads.len(), 3);
        assert_eq!(session.raw_current().unwrap(), raw);
    }
    #[test]
    fn native_session_missing_malformed_and_different_independent_store_refuse() {
        let (raw, expected) = sample();
        for case in [
            "missing",
            "malformed",
            "generation",
            "schema",
            "extra-request",
        ] {
            let f = Fixture::new();
            if case != "missing" {
                f.current(if case == "malformed" { b"{}" } else { &raw });
            }
            let fence = f.fence();
            let mut claim = expected.clone();
            if let JsonValue::Object(o) = &mut claim {
                if case == "generation" {
                    o.insert(
                        "storeGeneration".into(),
                        JsonValue::Integer(JsonInteger::new(999).unwrap()),
                    );
                }
                if case == "schema" {
                    o.insert(
                        "stateSchema".into(),
                        JsonValue::Integer(JsonInteger::new(2).unwrap()),
                    );
                }
                if case == "extra-request" {
                    o.insert("extra".into(), JsonValue::Null);
                }
            }
            assert!(
                NativeTrustReadSession::capture(&fence, &claim).is_err(),
                "{case}"
            );
            assert_eq!(
                f.root.join(format!("trust/stores/{SID}/state.v1")).exists(),
                case != "missing"
            );
        }
    }
    #[test]
    fn native_session_failed_read_latches_after_path_is_repaired() {
        let f = Fixture::new();
        let (raw, expected) = sample();
        let path = f.current(&raw);
        let fence = f.fence();
        let mut session = NativeTrustReadSession::capture(&fence, &expected).unwrap();
        fs::set_permissions(&path, Permissions::from_mode(0o666)).unwrap();
        assert!(session.raw_current().is_err());
        fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
        assert!(matches!(
            session.recheck().unwrap_err().0,
            Reason::Budget(M::Error::Closed)
        ));
        assert!(session.observe_again().is_err());
        assert!(session.store_claim().is_err());
    }
    #[test]
    fn native_session_original_file_and_every_ancestor_survive_repeated_capture() {
        let (raw, expected) = sample();
        for case in ["replace", "delete", "ancestor", "fence", "in-place"] {
            let f = Fixture::new();
            let path = f.current(&raw);
            let fence = f.fence();
            let mut session = NativeTrustReadSession::capture(&fence, &expected).unwrap();
            session.observe_again().unwrap();
            match case {
                "replace" => {
                    fs::rename(&path, path.with_extension("old")).unwrap();
                    f.current(&raw);
                }
                "delete" => fs::remove_file(&path).unwrap(),
                "ancestor" => {
                    fs::rename(f.root.join("trust"), f.root.join("old-trust")).unwrap();
                    f.current(&raw);
                }
                "fence" => fs::set_permissions(
                    f.root.join("lifecycle.fence"),
                    Permissions::from_mode(0o666),
                )
                .unwrap(),
                "in-place" => fs::write(&path, b"{}").unwrap(),
                _ => unreachable!(),
            }
            assert!(session.observe_again().is_err(), "{case}");
            assert!(session.raw_current().is_err(), "{case}");
        }
    }
    #[test]
    fn native_session_exhausted_cumulative_budget_cannot_be_reset_by_recapture() {
        let f = Fixture::new();
        let (raw, expected) = sample();
        f.current(&raw);
        let fence = f.fence();
        // Internal fixture lowers the same existing Budget's bound, not production defaults.
        let mut session = NativeTrustReadSession {
            fence: &fence,
            budget: Budget::new(65536, 14, 268435456).unwrap(),
            heads: Vec::new(),
            censuses: Vec::new(),
        };
        session.append(&expected).unwrap();
        session.observe_again().unwrap();
        assert_eq!(session.counters(), (4, 14, 1435));
        assert!(session.observe_again().is_err());
        assert!(matches!(
            session.recheck().unwrap_err().0,
            Reason::Budget(M::Error::Closed)
        ));
        assert_eq!(session.heads.len(), 2);
        assert_eq!(session.counters(), (4, 14, 1435));
    }
    #[test]
    fn native_session_invalid_request_precedes_native_io() {
        let f = Fixture::new();
        let fence = f.fence();
        fs::set_permissions(
            f.root.join("lifecycle.fence"),
            Permissions::from_mode(0o666),
        )
        .unwrap();
        let result = NativeTrustReadSession::capture(&fence, &JsonValue::Null);
        assert!(matches!(
            result.err().unwrap().0,
            Reason::Current(native_current::Error::Reference)
        ));
    }
    #[test]
    fn native_session_failed_capture_still_rechecks_original_fence_and_latches() {
        let (raw, expected) = sample();
        for malformed in [false, true] {
            let f = Fixture::new();
            f.current(if malformed { b"{}" } else { &raw });
            let fence = f.fence();
            let mut session = NativeTrustReadSession {
                fence: &fence,
                budget: Budget::new(65536, 131072, 268435456).unwrap(),
                heads: Vec::new(),
                censuses: Vec::new(),
            };
            let err = session
                .append_with(&expected, || {
                    fs::set_permissions(
                        f.root.join("lifecycle.fence"),
                        Permissions::from_mode(0o666),
                    )
                    .unwrap()
                })
                .unwrap_err();
            assert!(matches!(err.0, Reason::Fence(_)), "{err:?}");
            fs::set_permissions(
                f.root.join("lifecycle.fence"),
                Permissions::from_mode(0o600),
            )
            .unwrap();
            assert!(matches!(
                session.recheck().unwrap_err().0,
                Reason::Budget(M::Error::Closed)
            ));
        }
    }
    fn text(v: &JsonValue) -> &str {
        let JsonValue::String(s) = v else {
            panic!("text")
        };
        s
    }
    fn array(v: &JsonValue) -> &[JsonValue] {
        let JsonValue::Array(a) = v else {
            panic!("array")
        };
        a
    }
    fn decode_hex(v: &JsonValue) -> Vec<u8> {
        text(v)
            .as_bytes()
            .chunks_exact(2)
            .map(|b| u8::from_str_radix(std::str::from_utf8(b).unwrap(), 16).unwrap())
            .collect()
    }
    fn census_row(label: &str) -> JsonValue {
        include_bytes!("../../tests/fixtures/successor-link329.ndjson")
            .split(|b| *b == b'\n')
            .filter(|l| !l.is_empty())
            .map(|l| parse_json(l).unwrap())
            .find(|r| text(&object(r)["label"]) == label)
            .unwrap()
    }
    fn census_rows(f: &Fixture, before: &JsonValue, row: &JsonValue, include: Option<&str>) {
        let current = text(&object(&object(before)["publication"])["sha256"]);
        for r in array(&object(row)["store"]) {
            let r = object(r);
            let hash = text(&r["sha256"]);
            let kind = text(&r["collection"]);
            if kind == "publications" && hash != current && Some(hash) != include {
                continue;
            }
            let raw = decode_hex(r.get("rawHex").or_else(|| r.get("raw")).unwrap());
            let path = match kind {
                "records" => format!("trust/records/{hash}"),
                "objects" => format!("trust/objects/{hash}"),
                "events" => {
                    let v = parse_json(&raw).unwrap();
                    let v = object(&v);
                    let JsonValue::Integer(n) = &v["sequence"] else {
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
                    let v = object(&v);
                    if v["previousCapsule"] == JsonValue::Null {
                        format!(
                            "trust/publications/initial/{}/{hash}",
                            text(&object(&v["store"])["storeInstanceId"])
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
            f.write(&path, &raw);
        }
    }
    fn census_fixture() -> (Fixture, JsonValue) {
        let f = Fixture::new();
        let q = census_row("empty-link-0");
        let before = object(&q)["before"].clone();
        f.current(&canonical_bytes(&before).unwrap());
        census_rows(&f, &before, &q, None);
        (f, before)
    }
    fn bucket(f: &Fixture, before: &JsonValue) -> PathBuf {
        f.root
            .join("trust/publications/by-predecessor")
            .join(opensip_identity::digest_hex(&opensip_identity::raw_sha256(
                &canonical_bytes(before).unwrap(),
            )))
    }
    fn empty_bucket(f: &Fixture, before: &JsonValue) {
        let p = bucket(f, before);
        fs::create_dir(&p).unwrap();
        fs::set_permissions(p, Permissions::from_mode(0o700)).unwrap();
    }
    fn add_candidate(f: &Fixture, before: &JsonValue, label: &str) {
        let q = census_row(label);
        let hash = text(&object(&object(&q)["reference"])["sha256"]);
        census_rows(f, before, &q, Some(hash));
    }
    #[test]
    fn native_session_census_shares_current_budget_and_distinguishes_missing_from_empty() {
        for empty in [false, true] {
            let (f, before) = census_fixture();
            if empty {
                empty_bucket(&f, &before);
            }
            let fence = f.fence();
            let mut session =
                NativeTrustReadSession::capture(&fence, &object(&before)["store"]).unwrap();
            assert_eq!(session.counters(), (4, 7, 4207));
            assert_eq!(session.latest_successor_counts().unwrap(), None);
            let counts = session.observe_successors(|_| Ok(())).unwrap();
            assert!(!counts.publication_root_observed_missing);
            assert_eq!(counts.immediate_bucket_observed_missing, Some(!empty));
            assert_eq!(
                (
                    counts.immediate_candidates,
                    counts.following_buckets,
                    counts.structurally_supported_candidates
                ),
                (0, 0, 0)
            );
            assert_eq!(
                session.counters(),
                if empty {
                    (11, 41, 9108)
                } else {
                    (10, 38, 9105)
                }
            );
            assert_eq!(session.latest_successor_counts().unwrap(), Some(counts));
            if empty {
                assert_eq!(session.observe_successors(|_| Ok(())).unwrap(), counts);
                assert_eq!(session.counters(), (11, 75, 9111));
                assert_eq!(session.censuses.len(), 2);
            }
            assert_eq!(
                session.raw_current().unwrap(),
                canonical_bytes(&before).unwrap()
            );
        }
    }
    #[test]
    fn native_session_census_cumulative_edge_bound_includes_initial_current_capture() {
        for (limit, okay) in [(41, true), (40, false)] {
            let (f, before) = census_fixture();
            empty_bucket(&f, &before);
            let fence = f.fence();
            let mut session = NativeTrustReadSession {
                fence: &fence,
                budget: Budget::new(65536, limit, 268435456).unwrap(),
                heads: Vec::new(),
                censuses: Vec::new(),
            };
            session.append(&object(&before)["store"]).unwrap();
            assert_eq!(session.observe_successors(|_| Ok(())).is_ok(), okay);
            if okay {
                assert_eq!(session.counters(), (11, 41, 9108));
            } else {
                assert!(matches!(
                    session.recheck().unwrap_err().0,
                    Reason::Budget(M::Error::Closed)
                ));
            }
        }
    }
    #[test]
    fn native_session_census_every_following_branch_is_owned_before_counts() {
        for step in 0..3 {
            let (f, before) = census_fixture();
            add_candidate(&f, &before, "empty-link-0");
            if step >= 1 {
                add_candidate(&f, &before, "empty-link-1");
            }
            if step == 2 {
                add_candidate(&f, &before, "clock-link-0");
                add_candidate(&f, &before, "clock-link-1");
            }
            let fence = f.fence();
            let mut session =
                NativeTrustReadSession::capture(&fence, &object(&before)["store"]).unwrap();
            let counts = session.observe_successors(|_| Ok(())).unwrap();
            assert_eq!(counts.structurally_supported_candidates, step);
            assert_eq!(counts.immediate_candidates, if step == 2 { 2 } else { 1 });
            assert_eq!(counts.following_buckets, counts.immediate_candidates);
            assert_eq!(session.latest_successor_counts().unwrap(), Some(counts));
        }
    }
    #[test]
    fn native_session_census_later_dependency_and_bucket_changes_close_every_consumer() {
        for change in ["current", "dependency", "missing-bucket", "empty-addition"] {
            let (f, before) = census_fixture();
            if change != "missing-bucket" {
                empty_bucket(&f, &before);
            }
            let fence = f.fence();
            let mut session =
                NativeTrustReadSession::capture(&fence, &object(&before)["store"]).unwrap();
            session.observe_successors(|_| Ok(())).unwrap();
            match change {
                "current" => {
                    let p = f.root.join(format!("trust/stores/{SID}/state.v1"));
                    fs::rename(&p, p.with_extension("old")).unwrap();
                    f.current(&canonical_bytes(&before).unwrap());
                }
                "dependency" => {
                    let hash = text(&object(&object(&before)["publication"])["sha256"]);
                    let q = census_row("empty-link-0");
                    let row = array(&object(&q)["store"])
                        .iter()
                        .map(object)
                        .find(|r| {
                            text(&r["collection"]) == "publications" && text(&r["sha256"]) == hash
                        })
                        .unwrap();
                    let raw = decode_hex(row.get("rawHex").or_else(|| row.get("raw")).unwrap());
                    let d = parse_json(&raw).unwrap();
                    let d = object(&d);
                    let path = if d["previousCapsule"] == JsonValue::Null {
                        format!("trust/publications/initial/{SID}/{hash}")
                    } else {
                        format!(
                            "trust/publications/by-predecessor/{}/{hash}",
                            text(&d["previousCapsule"])
                        )
                    };
                    let p = f.root.join(&path);
                    fs::rename(&p, p.with_extension("old")).unwrap();
                    f.write(&path, &raw);
                }
                "missing-bucket" => empty_bucket(&f, &before),
                "empty-addition" => {
                    fs::write(bucket(&f, &before).join("0".repeat(64)), b"bad").unwrap();
                }
                _ => unreachable!(),
            }
            assert!(session.raw_current().is_err(), "{change}");
            assert!(session.store_claim().is_err());
            assert!(session.latest_successor_counts().is_err());
            assert!(session.observe_again().is_err());
        }
    }
    #[test]
    fn native_session_census_failed_foreign_callback_rechecks_prior_fence_and_latches() {
        let (f, before) = census_fixture();
        empty_bucket(&f, &before);
        fs::write(bucket(&f, &before).join("foreign"), b"unread").unwrap();
        let fence = f.fence();
        let mut session =
            NativeTrustReadSession::capture(&fence, &object(&before)["store"]).unwrap();
        let mut calls = 0;
        let err = session
            .observe_successors(|name| {
                assert_eq!(name, b"foreign");
                calls += 1;
                fs::set_permissions(
                    f.root.join("lifecycle.fence"),
                    Permissions::from_mode(0o666),
                )
                .unwrap();
                Err(())
            })
            .unwrap_err();
        assert_eq!(calls, 1);
        assert!(matches!(err.0, Reason::Fence(_)), "{err:?}");
        fs::set_permissions(
            f.root.join("lifecycle.fence"),
            Permissions::from_mode(0o600),
        )
        .unwrap();
        assert!(matches!(
            session.recheck().unwrap_err().0,
            Reason::Budget(M::Error::Closed)
        ));
        assert!(session.censuses.is_empty());
    }
    #[test]
    fn native_session_census_late_malformed_following_branch_returns_no_counts() {
        let (f, before) = census_fixture();
        for label in [
            "empty-link-0",
            "empty-link-1",
            "clock-link-0",
            "clock-link-1",
        ] {
            add_candidate(&f, &before, label);
        }
        let empty = census_row("empty-link-0");
        let clock = census_row("clock-link-0");
        let q = if text(&object(&object(&empty)["reference"])["sha256"])
            > text(&object(&object(&clock)["reference"])["sha256"])
        {
            empty
        } else {
            clock
        };
        let q = object(&q);
        let hash = text(&object(&q["reference"])["sha256"]);
        let row = array(&q["store"])
            .iter()
            .map(object)
            .find(|r| text(&r["collection"]) == "publications" && text(&r["sha256"]) == hash)
            .unwrap();
        let d = parse_json(&decode_hex(
            row.get("rawHex").or_else(|| row.get("raw")).unwrap(),
        ))
        .unwrap();
        let mut after = object(&object(&d)["afterProjection"]).clone();
        after.insert("publication".into(), q["reference"].clone());
        let parent = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            &canonical_bytes(&JsonValue::Object(after)).unwrap(),
        ));
        f.write(
            &format!(
                "trust/publications/by-predecessor/{parent}/{}",
                "f".repeat(64)
            ),
            b"malformed",
        );
        let fence = f.fence();
        let mut session =
            NativeTrustReadSession::capture(&fence, &object(&before)["store"]).unwrap();
        assert!(session.observe_successors(|_| Ok(())).is_err());
        assert!(session.censuses.is_empty());
        assert!(session.latest_successor_counts().is_err());
        assert!(session.raw_current().is_err());
        assert!(matches!(
            session.recheck().unwrap_err().0,
            Reason::Budget(M::Error::Closed)
        ));
    }
}
