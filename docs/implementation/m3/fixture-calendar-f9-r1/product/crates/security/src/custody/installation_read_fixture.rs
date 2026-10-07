// Test support for law 458c r5 item 8 (unit 458c-b2), on scratch account
// homes only. A real P0 is published by the 467 composition under a scratch
// H and that act ends; each read fence then produces the read receipt
// (458c-a) over 462's signed test trees for the same H, with the premise,
// and runs the observation session on it (458c-b1) with the real account's
// credentials and the scratch H. Nothing here opens the real account's I.
use super::installation_admission::{GateRefusal, HomeSource, IoFailure};
use super::installation_parent::ParentPreparationRefusal;
use super::installation_publication::{Outcome, create_at};
use super::installation_read::ReadSession;
use super::installation_session::{ObservationSession, OsClock, SessionRefusal, SessionSeam};
use super::installation_root::ParentRefusal;
use super::installation_stage::{CreationRefusal, Failure, Owners, Seam};
use super::read_premise::produce_on;
use crate::initial_installation::{CreatorCommand, InitialInstallationAttempt};
use crate::installation_observation::InstallationReadFence;
use crate::trust::{ReadProducers, read_producers, receipts_at};
use opensip_platform::{DescriptorAclCaptureError, WorkCost};
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};

const SUFFIX: [&str; 4] = ["Library", "Application Support", "OpenSIP", "preview-v1"];
static TAGS: AtomicUsize = AtomicUsize::new(0);

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "-N"])
            .arg(&self.0)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "u+rwX"])
            .arg(&self.0)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = fs::remove_dir_all(&self.0);
    }
}

/// A published P0 under a scratch H, and the signed test trees of every
/// read receipt produced for it, which live as long as the fixture.
pub(crate) struct ReadFixture {
    pub(crate) home: PathBuf,
    pub(crate) installation: PathBuf,
    /// The store S the creator drew.
    pub(crate) store: String,
    tag: String,
    producers: std::cell::RefCell<Vec<ReadProducers>>,
    _scratch: Scratch,
}
impl ReadFixture {
    pub(crate) fn new(tag: &str) -> Self {
        Self::new_in(tag, None)
    }
    /// `new`, with the scratch root under `parent` instead of the test
    /// scratch parent (law X8 r3 item 4c: a scenario home under the caller's
    /// scratch parent).
    pub(crate) fn new_in(tag: &str, parent: Option<&Path>) -> Self {
        // F4: a creation that refused only for churn in a shared ancestor
        // starts over in a fresh scratch root (see `shared_churn`).
        for attempt in 1.. {
            match Self::create(tag, parent) {
                Ok(fixture) => return fixture,
                Err(Failure::Operation(CreationRefusal::Parent(ParentPreparationRefusal::Parent(
                    refusal,
                )))) if settle(&refusal, attempt) => {}
                Err(other) => panic!("{other:?}"),
            }
        }
        unreachable!()
    }
    fn create(tag: &str, parent: Option<&Path>) -> Result<Self, Failure> {
        let nonce: String = opensip_platform::request_entropy()
            .unwrap()
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        let scratch = crate::test_scratch::temp_dir();
        let root = parent
            .unwrap_or(&scratch)
            .join(format!("opensip-read458c-{nonce}"));
        fs::create_dir(&root).unwrap();
        fs::set_permissions(&root, fs::Permissions::from_mode(0o700)).unwrap();
        let root = fs::canonicalize(&root).unwrap();
        let scratch = Scratch(root.clone());
        let home = root.join("home");
        fs::create_dir(&home).unwrap();
        fs::set_permissions(&home, fs::Permissions::from_mode(0o700)).unwrap();
        let tag = format!("{tag}-{}", TAGS.fetch_add(1, Ordering::SeqCst));
        let mut r = receipts_at(&format!("{tag}-create"), true, Some(&home), None);
        let intent = r
            .attempt
            .mint_intent(
                &r.actor,
                CreatorCommand::Analyze,
                false,
                &opensip_platform::RequestIdentity::draw().unwrap(),
                &mut Vec::new(),
            )
            .unwrap();
        let owners = Owners {
            actor: &r.actor,
            core: &r.core,
            platform: &r.platform,
        };
        let store = match create_at(&mut r.attempt, &owners, intent, &home, &Seam::live())? {
            Outcome::Published(published) => published.store().to_owned(),
            other => panic!("{other:?}"),
        };
        let installation = SUFFIX.iter().fold(home.clone(), |path, name| path.join(name));
        Ok(Self {
            home,
            installation,
            store,
            tag,
            producers: std::cell::RefCell::new(Vec::new()),
            _scratch: scratch,
        })
    }
    /// Unit X4a: replace this I's P0 trust store with X4T-0's signed
    /// accepted store for the same S and K (revocation list version 1, no
    /// entries), so a writer's fenced first read admits a view. `state.v1`
    /// is rewritten in place; its custody sample changes, which the next
    /// gate reads afresh.
    #[cfg(test)]
    pub(crate) fn accept_trust(&self) {
        self.write_trust(Vec::new(), 1);
    }
    /// The accepted store with these revocation entries and list version.
    #[cfg(test)]
    pub(crate) fn write_trust(&self, revocations: Vec<(&'static str, String)>, version: i128) {
        self.write_trust_issued(revocations, version, None);
    }
    /// Unit X4-F2: the accepted store with its bootstrap manifest issued at
    /// `issued` (X4T-0's knob), which raises its L above the list's issue
    /// time, so a first read's tEval can pass the list's staleness.
    #[cfg(test)]
    pub(crate) fn accept_trust_issued(&self, issued: &'static str) {
        self.write_trust_issued(Vec::new(), 1, Some(issued));
    }
    #[cfg(test)]
    fn write_trust_issued(
        &self,
        revocations: Vec<(&'static str, String)>,
        version: i128,
        issued: Option<&'static str>,
    ) {
        let current = self
            .installation
            .join(format!("trust/stores/{}/state.v1", self.store));
        let capsule = opensip_identity::parse_json(&fs::read(&current).unwrap()).unwrap();
        let opensip_identity::JsonValue::Object(capsule) = capsule else {
            panic!("capsule")
        };
        let opensip_identity::JsonValue::Object(store) = &capsule["store"] else {
            panic!("store")
        };
        let opensip_identity::JsonValue::Integer(schema) = &store["stateSchema"] else {
            panic!("schema")
        };
        let before = trust_paths(&self.installation);
        crate::trust::write_accepted_trust_issued(
            &self.installation,
            &self.store,
            schema.get(),
            revocations,
            version,
            issued,
            None,
        );
        // Every new directory and file gets the creator's zero-rights owner
        // allow, as a private creation would.
        for path in trust_paths(&self.installation).difference(&before) {
            private(path);
        }
    }
    /// Unit X4a: publish the accepted store with these revocation entries and
    /// list version as another writer would, by atomic replacement: every
    /// immutable file first (new names beside the existing ones), then the
    /// new `state.v1` renamed over the old one. Returns the old `state.v1`'s
    /// bytes.
    #[cfg(test)]
    pub(crate) fn swap_trust(
        &self,
        revocations: Vec<(&'static str, String)>,
        version: i128,
    ) -> Vec<u8> {
        let current = self
            .installation
            .join(format!("trust/stores/{}/state.v1", self.store));
        let old = fs::read(&current).unwrap();
        let before = trust_paths(&self.installation);
        let staging = self
            .installation
            .parent()
            .unwrap()
            .join(format!("x4a-swap-{}", TAGS.fetch_add(1, Ordering::SeqCst)));
        fs::create_dir(&staging).unwrap();
        fs::set_permissions(&staging, fs::Permissions::from_mode(0o700)).unwrap();
        fs::create_dir_all(staging.join(format!("trust/stores/{}", self.store))).unwrap();
        fs::copy(
            &current,
            staging.join(format!("trust/stores/{}/state.v1", self.store)),
        )
        .unwrap();
        let fixture = ReadFixture {
            home: self.home.clone(),
            installation: staging.clone(),
            store: self.store.clone(),
            tag: self.tag.clone(),
            producers: std::cell::RefCell::new(Vec::new()),
            _scratch: Scratch(staging.join("never")),
        };
        fixture.write_trust(revocations, version);
        let mut stack = vec![staging.join("trust")];
        while let Some(dir) = stack.pop() {
            for entry in fs::read_dir(&dir).unwrap() {
                let path = entry.unwrap().path();
                let relative = path.strip_prefix(&staging).unwrap().to_path_buf();
                let target = self.installation.join(&relative);
                if path.is_dir() {
                    if !target.exists() {
                        fs::create_dir(&target).unwrap();
                        fs::set_permissions(&target, fs::Permissions::from_mode(0o700)).unwrap();
                    }
                    stack.push(path);
                } else if relative.file_name().unwrap() != "state.v1" && !target.exists() {
                    fs::copy(&path, &target).unwrap();
                    fs::set_permissions(&target, fs::Permissions::from_mode(0o600)).unwrap();
                }
            }
        }
        let after = trust_paths(&self.installation);
        for path in after.difference(&before) {
            private(path);
        }
        private(&staging.join(format!("trust/stores/{}/state.v1", self.store)));
        fs::rename(
            staging.join(format!("trust/stores/{}/state.v1", self.store)),
            &current,
        )
        .unwrap();
        fs::remove_dir_all(&staging).unwrap();
        old
    }
    /// A read session on this I, on its own test attempt and session flag,
    /// with the owner's caps unless `limits` is given.
    #[cfg(test)]
    pub(crate) fn session(&self, limits: Option<WorkCost>) -> Result<ReadSession, SessionRefusal> {
        let mut producers = self.producers.borrow_mut();
        let tag = format!("{}-read{}", self.tag, producers.len());
        let (session, kept) = session_at(&tag, &self.home, limits);
        producers.push(kept);
        session
    }
    /// A read fence on this I at the owner's caps. A session that refused only for churn in a shared ancestor is
    /// opened again (F4, see `shared_churn`).
    #[cfg(test)]
    pub(crate) fn fence(&self) -> InstallationReadFence {
        for attempt in 1.. {
            match self.session(None) {
                Err(refusal) if session_churn(&refusal, attempt) => {}
                session => return InstallationReadFence::from_session(session.unwrap()),
            }
        }
        unreachable!()
    }
    /// Write a file below I as its readers expect: every missing directory
    /// 0700 and the file 0600, each given the zero-rights owner allow of a
    /// private creation.
    pub(crate) fn write(&self, relative: &str, bytes: &[u8]) -> PathBuf {
        let mut path = self.installation.clone();
        for part in Path::new(relative).parent().unwrap().components() {
            path.push(part);
            if !path.exists() {
                fs::create_dir(&path).unwrap();
                fs::set_permissions(&path, fs::Permissions::from_mode(0o700)).unwrap();
                private(&path);
            }
        }
        let path = self.installation.join(relative);
        let fresh = !path.exists();
        fs::write(&path, bytes).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o600)).unwrap();
        if fresh {
            private(&path);
        }
        path
    }
}
/// F4: whether a walk from `/` refused only because the descriptor capture
/// of `component` saw that directory change while it was sampled, where
/// `component` is above this process's private scratch parent: `/` through
/// the shared system temp directory and `opensip-test`. Other processes
/// change those directories (any entry another process creates or removes in
/// the temp directory changes it), and no fixture or mutation under test
/// touches them. F3's per-process parent keeps every fixture below them but
/// cannot take them out of a walk that starts at `/`.
pub(crate) fn shared_churn(refusal: &ParentRefusal) -> bool {
    matches!(
        refusal,
        ParentRefusal::Capture {
            component,
            error: DescriptorAclCaptureError::Changed,
        } if *component < private_component()
    )
}
/// The walk index of this process's private scratch parent. Component 0 is
/// `/`, so it is the canonical parent's component count less one.
fn private_component() -> usize {
    let parent = fs::canonicalize(crate::test_scratch::temp_dir()).unwrap();
    parent.components().count() - 1
}
/// F5: run a whole test again, on fresh fixtures, only when it panicked in
/// an attempt during which this thread's ancestor walks refused one or more
/// descriptor captures as `Changed` (`installation_root::CHANGED_CAPTURES`),
/// every one of them above the private parent: `/` through `opensip-test`,
/// which other processes change and no fixture or mutation under test
/// touches (`shared_churn`). Such a refusal reaches a test as many rows, some
/// without the component (`ancestor-acl`, `acl-unreadable`, a guard's stop
/// cause), so the witness is the walk's own record, not the panic text. At
/// most eight attempts with F3's backoff; every assertion stays strict, any
/// other failure is final, and the last attempt's failure is reported.
#[cfg(test)]
pub(crate) fn churned(test: impl Fn() + std::panic::RefUnwindSafe) {
    use super::installation_root::CHANGED_CAPTURES;
    const ATTEMPTS: u32 = 8;
    for attempt in 1..=ATTEMPTS {
        CHANGED_CAPTURES.take();
        let Err(panic) = std::panic::catch_unwind(&test) else {
            return;
        };
        let changed = CHANGED_CAPTURES.take();
        let private = private_component();
        let churn = !changed.is_empty() && changed.iter().all(|&component| component < private);
        if attempt == ATTEMPTS || !churn {
            std::panic::resume_unwind(panic);
        }
        std::thread::sleep(std::time::Duration::from_millis(25 * u64::from(attempt)));
    }
}
/// `shared_churn` for a session's refusal (the walk's I/O row).
#[cfg(test)]
pub(crate) fn session_churn(refusal: &SessionRefusal, attempt: u32) -> bool {
    match refusal {
        SessionRefusal::Gate(GateRefusal::Io(IoFailure::Chain(refusal))) => settle(refusal, attempt),
        _ => false,
    }
}
/// Whether to start over after `refusal` on `attempt`: only for shared
/// churn, at most eight attempts, with F3's backoff. Churn that never
/// settles fails the test.
fn settle(refusal: &ParentRefusal, attempt: u32) -> bool {
    const ATTEMPTS: u32 = 8;
    if !shared_churn(refusal) {
        return false;
    }
    assert!(attempt < ATTEMPTS, "a shared ancestor kept changing: {refusal:?}");
    std::thread::sleep(std::time::Duration::from_millis(25 * u64::from(attempt)));
    true
}
/// A read session on the I under `home`: the read receipt over a signed
/// test tree with the premise, on its own test attempt, and the observation
/// session on its own flag. The tree must outlive the session's use.
#[cfg(test)]
pub(crate) fn session_at(
    tag: &str,
    home: &Path,
    limits: Option<WorkCost>,
) -> (Result<ReadSession, SessionRefusal>, ReadProducers) {
    let producers = read_producers(tag, true, Some(home));
    let receipt = produce_on(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
        InitialInstallationAttempt::observe_actor,
        |attempt| producers.core(attempt),
        |attempt, actor, core| producers.platform(attempt, actor, core),
    )
    .unwrap();
    let session = ObservationSession::for_tests(&AtomicBool::new(false), limits).and_then(
        |session| {
            session.retain_with(
                receipt,
                HomeSource::Fixture(home),
                &mut OsClock,
                &SessionSeam::live(),
            )
        },
    );
    (session, producers)
}
/// A read fence on the I under `home`, and the tree it depends on.
#[cfg(test)]
pub(crate) fn fence_at(tag: &str, home: &Path) -> (InstallationReadFence, ReadProducers) {
    let (session, producers) = session_at(tag, home, None);
    (InstallationReadFence::from_session(session.unwrap()), producers)
}
/// Every directory and file under `I/trust`.
fn trust_paths(installation: &Path) -> std::collections::BTreeSet<PathBuf> {
    let mut out = std::collections::BTreeSet::new();
    let mut stack = vec![installation.join("trust")];
    while let Some(dir) = stack.pop() {
        for entry in fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                stack.push(path.clone());
            }
            out.insert(path);
        }
    }
    out
}
/// The zero-rights owner allow of a private creation.
pub(crate) fn private(path: &Path) {
    let file = fs::File::open(path).unwrap();
    opensip_platform::WorkLedger::new()
        .scope(|work| opensip_platform::append_owner_zero_allow_accounted(&file, work))
        .unwrap();
}

/// Law X3a item 3's chains: extend the node chain of the published store S
/// under `installation` so its newest node is at `generation`, each node
/// naming the one before it, and reselect the pair at that generation. Every
/// new directory is 0700 and every new file 0600, each with the zero-rights
/// owner allow. The trust current record is left naming generation 0.
pub(crate) fn select_generation(installation: &Path, store: &str, generation: i64) {
    use opensip_identity::{DecodedLineageNodeV1, DecodedSelectionV1};
    let pair = DecodedSelectionV1::decode(&fs::read(installation.join("selection.pair")).unwrap())
        .unwrap();
    let k = pair.state_schema();
    let lineage = installation.join(format!("transitions/lineage/{store}"));
    for g in 1..=generation {
        let dir = lineage.join(g.to_string());
        if !dir.exists() {
            fs::create_dir(&dir).unwrap();
            fs::set_permissions(&dir, fs::Permissions::from_mode(0o700)).unwrap();
            private(&dir);
        }
        let node = format!(
            concat!(
                "{{\"predecessor\":{{\"stateSchema\":{k},\"storeGeneration\":{p},",
                "\"storeInstanceId\":\"{s}\"}},\"schemaVersion\":1,",
                "\"selectedByIntentDigest\":\"{d}\",\"stateSchema\":{k},",
                "\"storeGeneration\":{g},\"storeInstanceId\":\"{s}\"}}"
            ),
            k = k,
            p = g - 1,
            s = store,
            d = "a".repeat(64),
            g = g,
        );
        DecodedLineageNodeV1::decode(node.as_bytes()).expect("a canonical node");
        let path = dir.join(format!("{k}.node"));
        let fresh = !path.exists();
        fs::write(&path, node.as_bytes()).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o600)).unwrap();
        if fresh {
            private(&path);
        }
    }
    let selected = format!(
        concat!(
            "{{\"coreClosure\":\"{c}\",\"selectionSchema\":1,\"stateSchema\":{k},",
            "\"storeGeneration\":{g},\"storeInstanceId\":\"{s}\"}}"
        ),
        c = pair.core_closure(),
        k = k,
        g = generation,
        s = store,
    );
    DecodedSelectionV1::decode(selected.as_bytes()).expect("a canonical pair");
    fs::write(installation.join("selection.pair"), selected.as_bytes()).unwrap();
}

/// Law X3a item 3's unended chain: rewrite the published root node at G 0,
/// in place, so it names a predecessor at G 100 that is never read. A walk
/// that reaches it after 64 nodes stops at the session limit.
pub(crate) fn unroot(installation: &Path, store: &str) {
    use opensip_identity::DecodedLineageNodeV1;
    let dir = installation.join(format!("transitions/lineage/{store}/0"));
    let leaf = fs::read_dir(&dir).unwrap().next().unwrap().unwrap().path();
    let root = DecodedLineageNodeV1::decode(&fs::read(&leaf).unwrap()).unwrap();
    let k = root.key().state_schema();
    let node = format!(
        concat!(
            "{{\"predecessor\":{{\"stateSchema\":{k},\"storeGeneration\":100,",
            "\"storeInstanceId\":\"{s}\"}},\"schemaVersion\":1,",
            "\"selectedByIntentDigest\":\"{d}\",\"stateSchema\":{k},",
            "\"storeGeneration\":0,\"storeInstanceId\":\"{s}\"}}"
        ),
        k = k,
        s = store,
        d = "b".repeat(64),
    );
    DecodedLineageNodeV1::decode(node.as_bytes()).expect("a canonical node");
    fs::write(&leaf, node.as_bytes()).unwrap();
}

/// Law X9 r1 item 6 and law X8 r3 items 4b, 4c and 5a (unit X9-1): a
/// published synthetic installation named by its paths, for a process that
/// did not create it (a matrix child or a helper process). It owns nothing
/// and removes nothing. Its producers are on the shared fixture-gate site
/// list, and both support surfaces call them.
#[derive(Debug, Clone)]
pub(crate) struct InstallationAt {
    pub(crate) home: PathBuf,
    pub(crate) installation: PathBuf,
    pub(crate) store: String,
}
impl ReadFixture {
    /// This fixture's installation, by its paths.
    pub(crate) fn at(&self) -> InstallationAt {
        InstallationAt {
            home: self.home.clone(),
            installation: self.installation.clone(),
            store: self.store.clone(),
        }
    }
}
impl InstallationAt {
    fn tag(&self, what: &str) -> String {
        format!("x9-{what}{}", TAGS.fetch_add(1, Ordering::SeqCst))
    }
    /// An ordinary writer on this I (law X1 item 2's composition over its
    /// seams): the write receipt over a signed test tree with the premise, on
    /// its own test attempt, then the write gate on its own test flag over
    /// the scratch H, by the production walk. The tree outlives the writer.
    pub(crate) fn writer(
        &self,
    ) -> Result<(super::ordinary_writer::OrdinaryWriteAdmission, ReadProducers), String> {
        self.admitted_writer()
            .map_err(|(stage, row)| format!("{stage}: {row:?}"))
    }
    /// `writer`, with the refusal's stage and its 468 item 6 row.
    pub(crate) fn admitted_writer(
        &self,
    ) -> Result<
        (super::ordinary_writer::OrdinaryWriteAdmission, ReadProducers),
        (&'static str, crate::InstallationTermination),
    > {
        use super::installation_admission::{DurableWriteGate, GateSeam};
        use super::read_premise::{Write, WritePlatformReceipt, produce_for};
        let producers = read_producers(&self.tag("writer"), true, Some(&self.home));
        let receipt = produce_for::<Write>(
            InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
            InitialInstallationAttempt::observe_actor,
            |attempt| producers.core(attempt),
            |attempt, actor, core| producers.platform(attempt, actor, core),
        )
        .map_err(|row| ("write receipt", row))?;
        let admission = super::ordinary_writer::admit_with(
            receipt,
            WritePlatformReceipt::recheck,
            || DurableWriteGate::for_tests(&AtomicBool::new(false), None),
            |gate, receipt| {
                gate.admit_with(
                    receipt.qualification(),
                    HomeSource::Fixture(&self.home),
                    &GateSeam::live(),
                )
            },
        )
        .map_err(|row| ("writer", row))?;
        Ok((admission, producers))
    }
    /// Law X8 r3 item 4c's production chain to a `ProjectOperation`, the one
    /// composition both support surfaces' operation entries call (unit
    /// X8b): X1's ordinary writer on this I, X2b's root admission and
    /// tracking, X2c's first registration when the root classifies as a
    /// first-use candidate (otherwise the admitted root as it classified),
    /// then `begin_operation`: X2d's namespace and lease, X3a's endpoint,
    /// X4's lease-free first read and monitor, X3b's floor step and carrier
    /// start, and X2e's handoff. The invocation's RequestId and ExecutionId
    /// are drawn from the host CSPRNG. Every refusal is its own row through
    /// 468c's vocabulary (X3d r6 item 9's maps); the writer, and with it the
    /// fence, is released on every refusal. The signed test tree is
    /// returned beside the operation and must outlive it.
    pub(crate) fn operation(
        &self,
        root: &Path,
        lease: super::namespace_lease::WriterLease,
    ) -> Result<(super::operation_handoff::ProjectOperation, ReadProducers), crate::InstallationTermination>
    {
        use super::commit_session::{operation_termination, project_termination};
        use super::first_registration::{ProjectInputs, ProjectWriteRefusal, Seam};
        use super::namespace_lease::NamespaceSubject;
        use super::project_admission::Classification;
        use crate::InstallationTermination as T;
        static NO_GROUPS: std::collections::BTreeSet<u32> = std::collections::BTreeSet::new();
        let inputs = ProjectInputs {
            trust_groups: &NO_GROUPS,
            environment: &[],
            system_sources: &[],
        };
        let project = |refusal: ProjectWriteRefusal| project_termination(&refusal.row());
        let (mut writer, trees) = self.admitted_writer().map_err(|(_, row)| row)?;
        let admission = writer
            .admit_project_root(root, None, inputs.trust_groups)
            .map_err(project)?;
        let tracking = writer
            .observe_project_tracking_with(&admission, &inputs)
            .map_err(project)?;
        let subject = if matches!(admission.classification(), Classification::FirstUseCandidate) {
            NamespaceSubject::Registered(
                writer
                    .register_first_use_with(admission, tracking, &inputs, &Seam::live())
                    .map_err(project)?,
            )
        } else {
            NamespaceSubject::Eligible {
                admission,
                tracking,
            }
        };
        let drawn = |prefix: &str| -> Result<String, T> {
            let bytes = opensip_platform::request_entropy().map_err(|_| T::HostIo)?;
            Ok(bytes
                .iter()
                .fold(prefix.to_owned(), |id, b| format!("{id}{b:02x}")))
        };
        let invocation =
            crate::trust::TrustInvocation::new(&drawn("req1_")?, &drawn("exec1_")?, 0)
                .ok_or(T::Invariant)?;
        let operation = writer
            .begin_operation(subject, lease, &inputs, &invocation)
            .map_err(|refusal| operation_termination(&refusal.row()))?;
        Ok((operation, trees))
    }
    /// The stored-capsule values of this I's `trust/stores/S/state.v1`,
    /// read by name: its state schema K and its revocation version (0 while
    /// the capsule carries no retained clock record, as P0's does not).
    /// Read-only: no fence, no write, no admission.
    pub(crate) fn current_trust_values(&self) -> Result<(i128, i128), String> {
        use opensip_identity::JsonValue as V;
        let path = self
            .installation
            .join(format!("trust/stores/{}/state.v1", self.store));
        let raw = fs::read(&path).map_err(|e| format!("state.v1: {e}"))?;
        let capsule = opensip_identity::parse_json(&raw).map_err(|e| format!("{e:?}"))?;
        let member = |v: &V, key: &str| match v {
            V::Object(o) => o.get(key).cloned(),
            _ => None,
        };
        let integer = |v: Option<V>| match v {
            Some(V::Integer(n)) => Some(n.get()),
            _ => None,
        };
        let schema = member(&capsule, "store")
            .and_then(|store| integer(member(&store, "stateSchema")))
            .ok_or("state.v1 store.stateSchema")?;
        let version = member(&capsule, "clock")
            .and_then(|clock| member(&clock, "record"))
            .and_then(|record| integer(member(&record, "revocationVersion")))
            .unwrap_or(0);
        Ok((schema, version))
    }
    /// X4T-0's signed accepted store for this I's S and K, with these
    /// revocation entries and list version, written in place as a fixture
    /// writes it, with no fence: every file, `state.v1` last; each fresh
    /// directory 0700 and each fresh file 0600 with the zero-rights owner
    /// allow. The accepted trust a synthetic installation starts from.
    /// Returns the core closure the store's P0 names.
    pub(crate) fn install_accepted_trust(
        &self,
        revocations: Vec<(&'static str, String)>,
        revocation_version: i128,
        accepted_seconds: Option<i64>,
    ) -> Result<&'static str, String> {
        let (schema, _) = self.current_trust_values()?;
        let (files, closure) = crate::trust::accepted_store_files(
            &self.store,
            schema,
            revocations,
            revocation_version,
            accepted_seconds,
        );
        for (relative, bytes) in &files {
            let mut path = self.installation.clone();
            for part in Path::new(relative).parent().unwrap().components() {
                path.push(part);
                if !path.exists() {
                    fs::create_dir(&path).map_err(|e| format!("{relative}: {e}"))?;
                    fs::set_permissions(&path, fs::Permissions::from_mode(0o700))
                        .map_err(|e| format!("{relative}: {e}"))?;
                    private(&path);
                }
            }
            let path = self.installation.join(relative);
            let fresh = !path.exists();
            fs::write(&path, bytes).map_err(|e| format!("{relative}: {e}"))?;
            fs::set_permissions(&path, fs::Permissions::from_mode(0o600))
                .map_err(|e| format!("{relative}: {e}"))?;
            if fresh {
                private(&path);
            }
        }
        Ok(closure)
    }
    /// The shared fenced publisher (X8 r3 item 4c's `publish_revocation_fenced`
    /// and X9 r1 item 6's publication helper are thin callers): a write gate
    /// takes this I's fence by its production walk over the scratch H, on its
    /// own test attempt and gate; X4T-0's store for S and K with these
    /// revocation entries and list version is published under that fence by
    /// the trust owner's protocol (`state.v1` replaced last); the gate's
    /// retained owner advances to the confirmed `state.v1`; then the fence is
    /// released. A store file that no locator addresses (S's marker) must
    /// already be here with exactly its bytes. Returns the revocation version
    /// before and after.
    pub(crate) fn publish_accepted_trust_fenced(
        &self,
        revocations: Vec<(&'static str, String)>,
        revocation_version: i128,
    ) -> Result<(i128, i128), String> {
        self.publish_trust_fenced(revocations, revocation_version, None)
            .map_err(|refusal| refusal.text())
    }
    /// `publish_accepted_trust_fenced`, with the refusal kept by stage
    /// (unit X8b: X8 r3 item 4c's `publish_revocation_fenced` names its row).
    pub(crate) fn publish_trust_fenced(
        &self,
        revocations: Vec<(&'static str, String)>,
        revocation_version: i128,
        accepted_seconds: Option<i64>,
    ) -> Result<(i128, i128), FencedRefusal> {
        use super::installation_admission::{DurableWriteGate, GateSeam};
        use super::read_premise::{Write, produce_for};
        let (schema, before) = self.current_trust_values().map_err(FencedRefusal::Fixture)?;
        let (generated, _) = crate::trust::accepted_store_files(
            &self.store,
            schema,
            revocations,
            revocation_version,
            accepted_seconds,
        );
        let mut files = Vec::new();
        for (path, bytes) in generated {
            let parts: Vec<&str> = path.split('/').collect();
            let addressed = matches!(
                parts.as_slice(),
                ["trust", "records" | "objects", _]
                    | ["trust", "stores", _, "events" | "state.v1", ..]
                    | ["trust", "publications", ..]
            );
            if addressed {
                files.push((path, bytes));
            } else if fs::read(self.installation.join(&path)).ok().as_deref() != Some(&bytes[..]) {
                return Err(FencedRefusal::Fixture(format!(
                    "{path}: not already present with its bytes"
                )));
            }
        }
        let producers = read_producers(&self.tag("publish"), true, Some(&self.home));
        let receipt = produce_for::<Write>(
            InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
            InitialInstallationAttempt::observe_actor,
            |attempt| producers.core(attempt),
            |attempt, actor, core| producers.platform(attempt, actor, core),
        )
        .map_err(FencedRefusal::Receipt)?;
        let mut gate = DurableWriteGate::for_tests(&AtomicBool::new(false), None)
            .map_err(FencedRefusal::Gate)?;
        let mut installation = gate
            .admit_with(
                receipt.qualification(),
                HomeSource::Fixture(&self.home),
                &GateSeam::live(),
            )
            .map_err(FencedRefusal::Fence)?;
        let published = {
            let read = installation.current_trust();
            let fence = installation.held_fence();
            opensip_platform::WorkLedger::new().scope(|work| {
                crate::trust::publish_store_fenced(&fence, &read, &files, work)
                    .map_err(opensip_platform::WorkFailure::Operation)
            })
        };
        let advanced = match published {
            Ok(confirmed) => installation
                .advance_current(&confirmed)
                .map_err(FencedRefusal::Advance),
            Err(failure) => Err(FencedRefusal::Publication(failure)),
        };
        let released = installation.release().map_err(FencedRefusal::Release);
        advanced.and(released)?;
        let (_, after) = self.current_trust_values().map_err(FencedRefusal::Fixture)?;
        Ok((before, after))
    }
}

/// Why the shared fenced publisher refused, by stage. Values only.
#[derive(Debug)]
pub(crate) enum FencedRefusal {
    /// The scratch installation is not one this fixture can publish for: its
    /// `state.v1` unreadable by name, or a store file that no locator
    /// addresses absent or different. Nothing was written.
    Fixture(String),
    /// The write receipt over the signed test tree refused.
    Receipt(crate::InstallationTermination),
    /// The write gate could not begin.
    Gate(GateRefusal),
    /// The gate's production walk refused to take I's fence (another holder
    /// has it, or custody refused). Nothing was written.
    Fence(GateRefusal),
    /// The trust owner's protocol refused under the fence.
    Publication(opensip_platform::WorkFailure<crate::trust::TrustRefusal>),
    /// The gate's retained owner could not advance to the confirmed file.
    Advance(GateRefusal),
    /// Releasing the fence failed.
    Release(std::io::Error),
}
impl FencedRefusal {
    /// The text `publish_accepted_trust_fenced` has always returned.
    fn text(&self) -> String {
        use opensip_platform::WorkFailure;
        match self {
            Self::Fixture(text) => text.clone(),
            Self::Receipt(row) => format!("write receipt: {row:?}"),
            Self::Gate(e) => format!("gate: {e:?}"),
            Self::Fence(e) => format!("fence: {e:?}"),
            Self::Publication(WorkFailure::Operation(e)) => {
                format!("publication: Operation({:?})", format!("{e:?}"))
            }
            Self::Publication(WorkFailure::Budget(b)) => format!("publication: Budget({b:?})"),
            Self::Advance(e) => format!("advance: {e:?}"),
            Self::Release(e) => format!("release: {e}"),
        }
    }
    /// The refusal's 468 item 6 row: the gate's rows through 468c's map, the
    /// trust owner's through X4T r9 item 10's, the budget row, the host I/O
    /// row for a failed release, and the invariant row for a scratch
    /// installation this fixture cannot serve (a broken caller).
    pub(crate) fn termination(&self) -> crate::InstallationTermination {
        use super::installation_routing::gate_refusal;
        use crate::InstallationTermination as T;
        use opensip_platform::WorkFailure;
        match self {
            Self::Fixture(_) => T::Invariant,
            Self::Receipt(row) => row.clone(),
            Self::Gate(e) | Self::Fence(e) | Self::Advance(e) => gate_refusal(e),
            Self::Publication(WorkFailure::Budget(_)) => T::BudgetExhausted,
            Self::Publication(WorkFailure::Operation(refusal)) => {
                super::operation_guard::trust_termination(&refusal.row)
            }
            Self::Release(_) => T::HostIo,
        }
    }
}
