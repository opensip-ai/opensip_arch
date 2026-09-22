use super::*;
use std::sync::Arc;
const CAP: usize = 4_194_304;
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub(super) enum Collection {
    Objects,
    Records,
    Events,
    Publications,
}
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Error {
    Profile,
    Reference,
    Closed,
    ObjectLimit,
    ByteLimit,
    EdgeLimit,
    Capture,
    Cap,
    Digest,
    Json,
    Paths(super::admitted_payload_paths::PathError),
    Carrier(EnvelopeError),
    Route,
    UnownedBody,
    RootDispatch,
    Missing,
    Ambiguous,
    AuthorizationEnvelope,
    Preimage,
}
type Key = (Collection, [u8; 32]);
pub(super) struct Budget<'work, 'owner> {
    shared: Option<&'work mut opensip_platform::WorkScope<'owner>>,
    limits: (usize, usize, usize),
    raw: BTreeMap<Key, Arc<[u8]>>,
    // Mutable current paths are not immutable Records aliases. Parent
    // identity is kept alive by directories for this whole operation.
    current: BTreeMap<(u64, u64), Arc<[u8]>>,
    // Held native handles prevent inode reuse while this operation accounts
    // for directory identity. These are not immutable document hashes.
    directories: BTreeMap<(u64, u64), Arc<opensip_platform::RetainedChildDirectory>>,
    edges: usize,
    bytes: usize,
    failed: bool,
}
// Unsuccessful exit includes unwinding through the scope. Counts and retained
// objects remain owned by the same budget; no retry or reset is introduced.
struct BudgetScope<'a, 'work, 'owner> {
    budget: &'a mut Budget<'work, 'owner>,
    completed: bool,
}
impl Drop for BudgetScope<'_, '_, '_> {
    fn drop(&mut self) {
        if !self.completed {
            self.budget.failed = true;
            if let Some(work) = self.budget.shared.as_deref_mut() {
                // Close the original outer operation through its normal scope.
                let _: Result<(), opensip_platform::WorkFailure<()>> =
                    work.scope(|_| Err(opensip_platform::WorkFailure::Operation(())));
            }
        }
    }
}
impl Budget<'static, 'static> {
    pub(super) fn new(objects: usize, edges: usize, bytes: usize) -> Result<Self, Error> {
        if objects == 0
            || objects > 65536
            || edges == 0
            || edges > 131072
            || bytes == 0
            || bytes > 268435456
        {
            return Err(Error::Profile);
        }
        Ok(Self {
            shared: None,
            limits: (objects, edges, bytes),
            raw: BTreeMap::new(),
            current: BTreeMap::new(),
            directories: BTreeMap::new(),
            edges: 0,
            bytes: 0,
            failed: false,
        })
    }
}
impl<'work, 'owner> Budget<'work, 'owner> {
    /// Borrow one original operation scope; never allocate a replacement ledger.
    /// This joins retained accounting only. Native observers must separately
    /// charge their temporary captures before allocation and prove custody.
    pub(super) fn borrowed(work: &'work mut opensip_platform::WorkScope<'owner>) -> Self {
        Self {
            shared: Some(work),
            limits: (65536, 131072, 268435456),
            raw: BTreeMap::new(),
            current: BTreeMap::new(),
            directories: BTreeMap::new(),
            edges: 0,
            bytes: 0,
            failed: false,
        }
    }
    pub(super) fn work<T>(
        &mut self,
        action: impl FnOnce(
            &mut opensip_platform::WorkScope<'_>,
        ) -> Result<T, opensip_platform::WorkFailure<Error>>,
    ) -> Result<T, Error> {
        self.guard(|s| match s.shared.as_deref_mut() {
            Some(work) => work.scope(action).map_err(Self::work_error),
            None => Err(Error::Profile),
        })
    }
    fn work_error(error: opensip_platform::WorkFailure<Error>) -> Error {
        use opensip_platform::{WorkBudgetError as B, WorkFailure as F};
        match error {
            F::Operation(error) => error,
            F::Budget(B::Objects) => Error::ObjectLimit,
            F::Budget(B::Edges) => Error::EdgeLimit,
            F::Budget(B::Bytes) => Error::ByteLimit,
            F::Budget(B::Record) => Error::Cap,
            F::Budget(B::Closed) => Error::Closed,
            F::Budget(B::Profile | B::Arithmetic | B::ReservedPostcheck) => Error::Profile,
        }
    }
    fn account(&mut self, objects: usize, edges: usize, bytes: usize) -> Result<(), Error> {
        if let Some(work) = self.shared.as_deref_mut() {
            work.charge(opensip_platform::WorkCost {
                objects,
                edges,
                bytes,
            })
            .map_err(Self::work_error)?;
        }
        Ok(())
    }
    fn closed(&self) -> bool {
        self.failed || self.shared.as_deref().is_some_and(|w| w.is_failed())
    }
    fn guard<T>(&mut self, f: impl FnOnce(&mut Self) -> Result<T, Error>) -> Result<T, Error> {
        self.scope(f)
    }
    pub(super) fn scope<T, E: From<Error>>(
        &mut self,
        f: impl FnOnce(&mut Self) -> Result<T, E>,
    ) -> Result<T, E> {
        if self.closed() {
            return Err(Error::Closed.into());
        }
        let mut scope = BudgetScope {
            budget: self,
            completed: false,
        };
        let result = f(scope.budget);
        match result {
            Ok(value) if !scope.budget.closed() => {
                scope.completed = true;
                Ok(value)
            }
            // A caught nested error does not restore this operation's budget.
            Ok(_) => Err(Error::Closed.into()),
            Err(error) => Err(error),
        }
    }
    pub(super) fn counters(&self) -> (usize, usize, usize) {
        (
            self.raw.len() + self.directories.len() + self.current.len(),
            self.edges,
            self.bytes,
        )
    }
    pub(super) fn edge(&mut self, count: usize) -> Result<(), Error> {
        self.guard(|s| {
            if count > s.limits.1 - s.edges {
                return Err(Error::EdgeLimit);
            }
            s.account(0, count, 0)?;
            s.edges += count;
            Ok(())
        })
    }
    /// Account an already-retained native directory. This cannot retroactively
    /// bound its caller's prior open/ACL capture. Every visit charges an edge;
    /// each actual held device/inode consumes one shared object slot.
    pub(super) fn directory(
        &mut self,
        directory: Arc<opensip_platform::RetainedChildDirectory>,
    ) -> Result<(), Error> {
        self.guard(|s| {
            s.edge(1)?;
            let sample = directory
                .directory()
                .observe_directory()
                .map_err(|_| Error::Capture)?;
            let key = (sample.metadata.device, sample.metadata.inode);
            if !s.directories.contains_key(&key) {
                if s.raw.len() + s.directories.len() + s.current.len() >= s.limits.0 {
                    return Err(Error::ObjectLimit);
                }
                s.account(1, 0, 0)?;
                s.directories.insert(key, directory);
            }
            Ok(())
        })
    }
    /// Charge EVERY borrowed OS name before classification, allocation,
    /// diagnostics or file access. Repeated visits still consume work.
    pub(super) fn entry(&mut self, name: &[u8]) -> Result<(), Error> {
        self.guard(|s| {
            s.edge(1)?;
            if name.len() > s.limits.2 - s.bytes {
                return Err(Error::ByteLimit);
            }
            s.account(0, 0, name.len())?;
            s.bytes += name.len();
            Ok(())
        })
    }
    fn available(&self, key: Key) -> Result<usize, Error> {
        if let Some(raw) = self.raw.get(&key) {
            return Ok(raw.len());
        }
        if self.raw.len() + self.directories.len() + self.current.len() >= self.limits.0 {
            return Err(Error::ObjectLimit);
        }
        let cap = CAP.min(self.limits.2 - self.bytes);
        if cap == 0 {
            return Err(Error::ByteLimit);
        }
        Ok(cap)
    }
    /// Fresh bounded read of fixed state.v1 under an already charged,
    /// retained native store directory. This cache never proves presence.
    pub(super) fn capture_current(
        &mut self,
        parent: &Arc<opensip_platform::RetainedChildDirectory>,
        read: impl FnOnce(usize) -> Result<Vec<u8>, ()>,
    ) -> Result<Arc<[u8]>, Error> {
        self.guard(|s| {
            let metadata = parent
                .directory()
                .observe_directory()
                .map_err(|_| Error::Capture)?
                .metadata;
            let key = (metadata.device, metadata.inode);
            if !s.directories.contains_key(&key) {
                return Err(Error::Capture);
            }
            let cap = if let Some(raw) = s.current.get(&key) {
                raw.len()
            } else {
                if s.raw.len() + s.directories.len() + s.current.len() >= s.limits.0 {
                    return Err(Error::ObjectLimit);
                }
                let cap = CAP.min(s.limits.2 - s.bytes);
                if cap == 0 {
                    return Err(Error::ByteLimit);
                }
                cap
            };
            let raw = read(cap).map_err(|_| Error::Capture)?;
            if raw.is_empty() || raw.len() > cap {
                return Err(Error::Cap);
            }
            if let Some(old) = s.current.get(&key) {
                if old.as_ref() != raw.as_slice() {
                    return Err(Error::Digest);
                }
                return Ok(Arc::clone(old));
            }
            s.account(1, 0, raw.len())?;
            let raw: Arc<[u8]> = Arc::from(raw);
            s.bytes += raw.len();
            s.current.insert(key, Arc::clone(&raw));
            Ok(raw)
        })
    }
    /// For bytes already held by a trusted caller. This does not prove
    /// a pre-allocation bound on that caller's earlier capture.
    pub(super) fn retain(
        &mut self,
        collection: Collection,
        raw: &[u8],
    ) -> Result<Arc<[u8]>, Error> {
        self.guard(|s| {
            if raw.is_empty() || raw.len() > CAP {
                return Err(Error::Cap);
            }
            let key = (collection, opensip_identity::raw_sha256(raw));
            if raw.len() > s.available(key)? {
                return Err(Error::ByteLimit);
            }
            if let Some(old) = s.raw.get(&key) {
                if old.as_ref() != raw {
                    return Err(Error::Digest);
                }
                return Ok(Arc::clone(old));
            }
            s.account(1, 0, raw.len())?;
            let raw: Arc<[u8]> = Arc::from(raw);
            s.bytes += raw.len();
            s.raw.insert(key, Arc::clone(&raw));
            Ok(raw)
        })
    }
    /// The trusted capture adapter must enforce cap before allocation
    /// and independently establish custody. Every new path uses presence=true.
    pub(super) fn capture(
        &mut self,
        collection: Collection,
        digest: [u8; 32],
        presence: bool,
        capture: impl FnOnce(usize) -> Result<Vec<u8>, ()>,
    ) -> Result<Arc<[u8]>, Error> {
        self.capture_in(collection, digest, presence, |_, cap| {
            capture(cap).map(Arc::from).map_err(|_| Error::Capture)
        })
    }
    fn capture_in(
        &mut self,
        collection: Collection,
        digest: [u8; 32],
        presence: bool,
        capture: impl FnOnce(&mut Self, usize) -> Result<Arc<[u8]>, Error>,
    ) -> Result<Arc<[u8]>, Error> {
        self.guard(|s| {
            let key = (collection, digest);
            let cap = s.available(key)?;
            if !presence && let Some(raw) = s.raw.get(&key) {
                return Ok(Arc::clone(raw));
            }
            let raw = capture(s, cap)?;
            if raw.is_empty() || raw.len() > cap {
                return Err(Error::Cap);
            }
            if opensip_identity::raw_sha256(&raw) != digest {
                return Err(Error::Digest);
            }
            s.retain(collection, &raw)
        })
    }
    /// Bare NodeRef/BlobRef convenience. Native Event/Publication reads
    /// require load_at with their full typed reference.
    pub(super) fn load(
        &mut self,
        collection: Collection,
        reference: &V,
        store: &mut impl Store,
    ) -> Result<Arc<[u8]>, Error> {
        self.load_at(collection, reference, None, store)
    }
    pub(super) fn load_at(
        &mut self,
        collection: Collection,
        reference: &V,
        initial_store: Option<&V>,
        store: &mut impl Store,
    ) -> Result<Arc<[u8]>, Error> {
        self.guard(|s| {
            s.edge(1)?;
            let (digest, length) =
                super::native_record_capture::reference_parts(collection, reference, initial_store)
                    .map_err(|_| Error::Reference)?;
            let key = (collection, digest);
            let available = s.available(key)?;
            if let Some(raw) = s.raw.get(&key) {
                if raw.len() != length {
                    return Err(Error::Digest);
                }
                if !store.refresh_cached() {
                    return Ok(Arc::clone(raw));
                }
            }
            if length > available {
                return Err(Error::ByteLimit);
            }
            let request = ReadRequest {
                collection,
                reference,
                initial_store,
                digest,
                length,
            };
            let raw = store.read(s, request)?;
            if raw.len() != length || opensip_identity::raw_sha256(&raw) != digest {
                return Err(Error::Digest);
            }
            s.retain(collection, &raw)
        })
    }
}
/// Immutable full locator; only Budget can construct this after bounded
/// typed-shape admission. A supplied source remains short of authority.
pub(super) struct ReadRequest<'a> {
    collection: Collection,
    reference: &'a V,
    initial_store: Option<&'a V>,
    digest: [u8; 32],
    length: usize,
}
impl ReadRequest<'_> {
    pub(super) fn collection(&self) -> Collection {
        self.collection
    }
    pub(super) fn reference(&self) -> &V {
        self.reference
    }
    pub(super) fn initial_store(&self) -> Option<&V> {
        self.initial_store
    }
}
pub(super) trait Store {
    /// Native reads always revisit the requested physical location.
    fn refresh_cached(&self) -> bool {
        true
    }
    fn read(&mut self, budget: &mut Budget, request: ReadRequest<'_>) -> Result<Arc<[u8]>, Error>;
}
/// Digest closures model already supplied bytes in reference fixtures.
/// They make no native-location, fresh-presence or custody assertion.
impl<F: FnMut(Collection, [u8; 32], usize) -> Result<Vec<u8>, ()>> Store for F {
    fn refresh_cached(&self) -> bool {
        false
    }
    fn read(&mut self, _: &mut Budget, request: ReadRequest<'_>) -> Result<Arc<[u8]>, Error> {
        self(request.collection, request.digest, request.length)
            .map(Arc::from)
            .map_err(|_| Error::Capture)
    }
}

pub(super) fn reference_fields(v: &V) -> Option<([u8; 32], usize)> {
    let o = object(v)?;
    if !closed(o, &["sha256", "bytes"], &[]) {
        return None;
    }
    let digest = decode_hex32(string(&o["sha256"])?).ok()?;
    let length = integer(&o["bytes"])?;
    if !(1..=CAP as i64).contains(&length) {
        return None;
    }
    Some((digest, length as usize))
}
/// Context-aware adapters let nested retained reads charge this exact
/// operation. They cannot borrow an unrelated hidden budget from Index.
pub(super) trait Capture {
    fn read(&mut self, budget: &mut Budget, path: &str, cap: usize) -> Result<Arc<[u8]>, Error>;
}
pub(super) struct HostCapture<F>(F);
impl<F: FnMut(&str, usize) -> Result<Vec<u8>, ()>> Capture for HostCapture<F> {
    fn read(&mut self, _: &mut Budget, path: &str, cap: usize) -> Result<Arc<[u8]>, Error> {
        (self.0)(path, cap)
            .map(Arc::from)
            .map_err(|_| Error::Capture)
    }
}
struct Header {
    kind: EnvelopeKind,
    domain: String,
    stored: [u8; 32],
    preimage: [u8; 32],
}
type PairKey = (&'static str, String, [u8; 32]);
struct Data {
    paths: super::admitted_payload_paths::PayloadPaths,
    captured: BTreeMap<String, Arc<[u8]>>,
    headers: BTreeMap<[u8; 32], Header>,
    candidates: BTreeMap<PairKey, Vec<String>>,
    authorization_envelope: Option<String>,
}
pub(super) struct Pair {
    kind: EnvelopeKind,
    body: Arc<[u8]>,
    envelope: Arc<[u8]>,
    body_path: String,
    envelope_path: String,
}
impl Pair {
    pub(super) fn kind(&self) -> EnvelopeKind {
        self.kind
    }
    pub(super) fn body(&self) -> &[u8] {
        &self.body
    }
    pub(super) fn envelope(&self) -> &[u8] {
        &self.envelope
    }
    pub(super) fn body_path(&self) -> &str {
        &self.body_path
    }
    pub(super) fn envelope_path(&self) -> &str {
        &self.envelope_path
    }
}
pub(super) struct Index<'op, 'work, 'owner, F> {
    budget: &'op mut Budget<'work, 'owner>,
    capture: F,
    data: Data,
}
impl Data {
    fn load(
        &mut self,
        budget: &mut Budget,
        capture: &mut impl Capture,
        path: &str,
    ) -> Result<Arc<[u8]>, Error> {
        if let Some(raw) = self.captured.get(path) {
            return Ok(Arc::clone(raw));
        }
        let entry = self.paths.entries().get(path).ok_or(Error::UnownedBody)?;
        let raw = budget.capture_in(Collection::Objects, entry.digest(), true, |b, cap| {
            capture.read(b, path, cap)
        })?;
        self.captured.insert(path.into(), Arc::clone(&raw));
        Ok(raw)
    }
    fn build(raw: &[u8], budget: &mut Budget, capture: &mut impl Capture) -> Result<Self, Error> {
        budget.retain(Collection::Objects, raw)?;
        let manifest = super::super::metadata::parse(raw).map_err(|_| Error::Json)?;
        let paths = super::admitted_payload_paths::admit(&manifest).map_err(Error::Paths)?;
        budget.edge(paths.entries().len())?;
        let m = object(&object(&manifest).unwrap()["members"]).unwrap();
        let authorization_envelope =
            m.get("rootRecoveryAuthorization")
                .and_then(object)
                .map(|auth| {
                    string(&object(&auth["envelope"]).unwrap()["path"])
                        .unwrap()
                        .to_owned()
                });
        let mut listed: Vec<&str> = array(&m["envelopes"])
            .unwrap()
            .iter()
            .map(|r| string(&object(r).unwrap()["path"]).unwrap())
            .collect();
        listed.sort_unstable();
        let mut s = Self {
            paths,
            captured: BTreeMap::new(),
            headers: BTreeMap::new(),
            candidates: BTreeMap::new(),
            authorization_envelope,
        };
        for path in listed {
            let raw = s.load(budget, capture, path)?;
            let digest = opensip_identity::raw_sha256(&raw);
            if let std::collections::btree_map::Entry::Vacant(e) = s.headers.entry(digest) {
                let value = super::super::metadata::parse(&raw).map_err(|_| Error::Json)?;
                let view =
                    super::verified_envelopes::parse_carrier(&value).map_err(Error::Carrier)?;
                if !view.route_matches() {
                    return Err(Error::Route);
                }
                e.insert(Header {
                    kind: view.kind(),
                    domain: view.domain().into(),
                    stored: view.stored_digest(),
                    preimage: view.preimage_digest(),
                });
            }
            let h = &s.headers[&digest];
            // Distinct paths remain distinct candidates, even if their
            // bytes share storage and decoded header. Never first-wins.
            s.candidates
                .entry((h.kind.route().0, h.domain.clone(), h.stored))
                .or_default()
                .push(path.into());
        }
        Ok(s)
    }
    fn select(
        &mut self,
        budget: &mut Budget,
        capture: &mut impl Capture,
        path: &str,
    ) -> Result<Pair, Error> {
        let kind = self
            .paths
            .entries()
            .get(path)
            .and_then(|r| r.kind())
            .ok_or(Error::UnownedBody)?;
        let body = self.load(budget, capture, path)?;
        let value = super::super::metadata::parse(&body).map_err(|_| Error::Json)?;
        let domain = if kind == EnvelopeKind::Root {
            match object(&value)
                .and_then(|o| o.get("rootSchema"))
                .and_then(integer)
            {
                Some(1) => "opensip.metadata.root.1",
                Some(2) => "opensip.metadata.root.2",
                _ => return Err(Error::RootDispatch),
            }
        } else {
            kind.route().1
        };
        let key = (
            kind.route().0,
            domain.into(),
            opensip_identity::raw_sha256(&body),
        );
        let candidates = self.candidates.get(&key).ok_or(Error::Missing)?;
        if candidates.len() != 1 {
            return Err(Error::Ambiguous);
        }
        let envelope_path = &candidates[0];
        if kind == EnvelopeKind::RootRecoveryAuthorization
            && self.authorization_envelope.as_deref() != Some(envelope_path.as_str())
        {
            return Err(Error::AuthorizationEnvelope);
        }
        let envelope = Arc::clone(&self.captured[envelope_path]);
        let header = &self.headers[&opensip_identity::raw_sha256(&envelope)];
        if super::super::metadata_digest_for_domain(domain, &value).map_err(|_| Error::Preimage)?
            != header.preimage
        {
            return Err(Error::Preimage);
        }
        Ok(Pair {
            kind,
            body,
            envelope,
            body_path: path.into(),
            envelope_path: envelope_path.clone(),
        })
    }
}
impl<'op, 'work, 'owner, F: FnMut(&str, usize) -> Result<Vec<u8>, ()>>
    Index<'op, 'work, 'owner, HostCapture<F>>
{
    pub(super) fn new(
        manifest: &[u8],
        budget: &'op mut Budget<'work, 'owner>,
        capture: F,
    ) -> Result<Self, Error> {
        Self::with_context(manifest, budget, HostCapture(capture))
    }
}
impl<'op, 'work, 'owner, F: Capture> Index<'op, 'work, 'owner, F> {
    pub(super) fn with_context(
        manifest: &[u8],
        budget: &'op mut Budget<'work, 'owner>,
        mut capture: F,
    ) -> Result<Self, Error> {
        let data = budget.guard(|b| Data::build(manifest, b, &mut capture))?;
        Ok(Self {
            budget,
            capture,
            data,
        })
    }
    pub(super) fn select(&mut self, path: &str) -> Result<Pair, Error> {
        self.budget
            .guard(|b| self.data.select(b, &mut self.capture, path))
    }
    pub(super) fn authorization_carrier_count(&self) -> usize {
        self.data
            .candidates
            .iter()
            .filter(|(k, _)| k.0 == "root-recovery-authorization")
            .map(|(_, v)| v.len())
            .sum()
    }
}
#[cfg(test)]
mod tests {
    include!("retained_metadata_index_tests.rs");
}
