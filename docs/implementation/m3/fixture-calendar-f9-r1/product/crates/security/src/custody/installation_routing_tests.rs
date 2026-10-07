// Law 468 r6 items 1, 3 and 6 with M3-J1 r6 item 3 (unit J3a), on scratch
// account homes only. J1 item 3's durable entry runs over `OnScratch`: the
// production composition's owners on a scratch H, with test attempt slots
// and a test gate flag, 462's signed test trees, the real creator on that H
// and the production gate walk. Controls J-C5 to J-C9 with J-C6b, J-C2's and
// J-C4b's security halves, and every item 6 row the entry can reach. Nothing
// here opens the real account's I; the one live composition (J-C9) refuses
// at InitialCore F0 before any installation path is touched.
use super::super::commit_session::CommitSession;
use super::super::first_registration::{ProjectInputs, Seam as Registration};
use super::super::installation_admission::{DurableWriteGate, GateBarrier, GateSeam, HomeSource};
use super::super::installation_publication::create_at;
use super::super::installation_read_fixture::{churned, private};
use super::super::installation_stage::{I_PARENT, Point, Seam};
use super::super::namespace_lease::{NamespaceSubject, WriterLease};
use super::super::operation_guard::scripted;
use super::super::ordinary_writer::admit_with;
use super::*;
use crate::initial_installation::BackupChoiceRequired;
use crate::trust::{ReadProducers, read_producers, receipts_at};
use opensip_platform::{DirectoryRenameClass, FileLock, LockMode, WorkBudgetError, WorkCost};
use std::cell::{Cell, RefCell};
use std::collections::BTreeSet;
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::sync::atomic::{AtomicBool, Ordering};

const SUFFIX: [&str; 4] = ["Library", "Application Support", "OpenSIP", "preview-v1"];

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
/// A scratch root holding a 0700 `home`, on its canonical path.
fn scratch() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let root = crate::test_scratch::temp_dir().join(format!("opensip-entryj3a-{nonce}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, fs::Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(&root).unwrap();
    let home = root.join("home");
    fs::create_dir(&home).unwrap();
    fs::set_permissions(&home, fs::Permissions::from_mode(0o700)).unwrap();
    (Scratch(root), home)
}
fn installation(home: &Path) -> PathBuf {
    let mut i = home.to_owned();
    for name in SUFFIX {
        i.push(name);
    }
    i
}
fn fence_free(i: &Path) -> bool {
    FileLock::try_acquire(
        fs::File::open(i.join("lifecycle.fence")).unwrap(),
        LockMode::Exclusive,
    )
    .unwrap()
    .is_some()
}
/// Delete I as an outside process would: its owner allows removed first.
fn remove_installation(i: &Path) {
    for args in [["-R", "-N"], ["-R", "u+rwX"]] {
        let _ = std::process::Command::new("/bin/chmod")
            .args(args)
            .arg(i)
            .stderr(std::process::Stdio::null())
            .status();
    }
    fs::remove_dir_all(i).unwrap();
}
/// Every path below `dir`, recursively.
fn tree(dir: &Path) -> BTreeSet<PathBuf> {
    let mut out = BTreeSet::new();
    let mut stack = vec![dir.to_owned()];
    while let Some(at) = stack.pop() {
        let Ok(entries) = fs::read_dir(&at) else {
            continue;
        };
        for entry in entries {
            let path = entry.unwrap().path();
            if fs::symlink_metadata(&path).unwrap().is_dir() {
                stack.push(path.clone());
            }
            out.insert(path);
        }
    }
    out
}
/// Every regular file below `dir` with its bytes.
fn contents(dir: &Path) -> Vec<(PathBuf, Vec<u8>)> {
    tree(dir)
        .into_iter()
        .filter(|path| fs::symlink_metadata(path).unwrap().is_file())
        .map(|path| {
            let bytes = fs::read(&path).unwrap();
            (path, bytes)
        })
        .collect()
}
/// The distinct values of `"<member>":"<prefix>…"` in the files below `dir`.
fn recorded(dir: &Path, member: &str, len: usize) -> BTreeSet<String> {
    let key = format!("\"{member}\":\"");
    let mut out = BTreeSet::new();
    for (_, bytes) in contents(dir) {
        let text = String::from_utf8_lossy(&bytes);
        let mut rest = text.as_ref();
        while let Some(at) = rest.find(&key) {
            rest = &rest[at + key.len()..];
            out.insert(rest[..len.min(rest.len())].to_owned());
        }
    }
    out
}
fn rendered(prefix: &str, bytes: [u8; 16]) -> String {
    bytes
        .iter()
        .fold(prefix.to_owned(), |text, byte| format!("{text}{byte:02x}"))
}

/// Standard error for one entry: what was written, how often it was
/// flushed, and a check that runs at each flush.
struct Notice<'a> {
    bytes: Vec<u8>,
    flushes: usize,
    at_flush: Option<&'a dyn Fn()>,
}
impl Notice<'_> {
    fn new() -> Self {
        Self {
            bytes: Vec::new(),
            flushes: 0,
            at_flush: None,
        }
    }
}
impl std::io::Write for Notice<'_> {
    fn write(&mut self, bytes: &[u8]) -> std::io::Result<usize> {
        self.bytes.extend_from_slice(bytes);
        Ok(bytes.len())
    }
    fn flush(&mut self) -> std::io::Result<()> {
        self.flushes += 1;
        if let Some(check) = self.at_flush {
            check();
        }
        Ok(())
    }
}

/// J1 item 3's owners on a scratch H (`EntryOwners`): attempt A and B on
/// this owner's test slots, both produced over the same signed test tree
/// for H; the real creator on H with `creator`'s seam; X1 item 2's steps 2
/// to 4 with a test gate flag and the production walk on H. The hooks
/// interfere at fixed places, and every attempt's lineage, InitialCore
/// production and gate is counted.
struct OnScratch<'a> {
    home: &'a Path,
    trees: ReadProducers,
    first: AtomicBool,
    second: AtomicBool,
    gate: AtomicBool,
    creator: Seam<'a>,
    gate_seam: GateSeam<'a>,
    /// Attempt B's ledger limits (J-C6b's producer refusal).
    limits_b: Option<WorkCost>,
    /// The gate's ledger limits.
    gate_limits: Option<WorkCost>,
    /// Runs just before the creator act's effects.
    before_create: Option<&'a dyn Fn()>,
    /// Runs just before attempt B is allocated.
    before_b: Option<&'a dyn Fn()>,
    /// Runs just before the gate begins.
    before_gate: Option<&'a dyn Fn()>,
    /// Replaces the receipt's step 4 recheck.
    second_recheck: Option<&'a dyn Fn() -> Result<(), T>>,
    lineages: RefCell<Vec<[u8; 16]>>,
    cores: Cell<usize>,
    gates: Cell<usize>,
    /// What the creator act's effects returned for `Published`: P0's ids.
    published: RefCell<Option<(String, String)>>,
}
fn on_scratch<'a>(tag: &str, home: &'a Path, premise: bool) -> OnScratch<'a> {
    OnScratch {
        home,
        trees: read_producers(tag, premise, Some(home)),
        first: AtomicBool::new(false),
        second: AtomicBool::new(false),
        gate: AtomicBool::new(false),
        creator: Seam::live(),
        gate_seam: GateSeam::live(),
        limits_b: None,
        gate_limits: None,
        before_create: None,
        before_b: None,
        before_gate: None,
        second_recheck: None,
        lineages: RefCell::new(Vec::new()),
        cores: Cell::new(0),
        gates: Cell::new(0),
        published: RefCell::new(None),
    }
}
impl OnScratch<'_> {
    fn produce(
        &self,
        begun: Result<InitialInstallationAttempt, AttemptError>,
    ) -> Result<Producers, T> {
        let producers = produce_unsealed(
            begun,
            InitialInstallationAttempt::observe_actor,
            |attempt| {
                self.cores.set(self.cores.get() + 1);
                self.trees.core(attempt)
            },
            |attempt, actor, core| self.trees.platform(attempt, actor, core),
        )?;
        self.lineages.borrow_mut().push(producers.attempt.lineage());
        Ok(producers)
    }
}
impl EntryOwners for OnScratch<'_> {
    fn first(&self) -> Result<Producers, T> {
        self.produce(InitialInstallationAttempt::for_tests(&self.first, None))
    }
    fn home(&self, _actor: &InitialActor) -> PathBuf {
        self.home.to_owned()
    }
    fn create(
        &self,
        attempt: &mut InitialInstallationAttempt,
        owners: &Owners<'_>,
        intent: CreationIntent,
    ) -> Result<Outcome, Failure> {
        if let Some(hook) = self.before_create {
            hook();
        }
        let outcome = create_at(attempt, owners, intent, self.home, &self.creator);
        if let Ok(Outcome::Published(published)) = &outcome {
            *self.published.borrow_mut() = Some((
                published.request_id().to_owned(),
                published.execution_id().to_owned(),
            ));
        }
        outcome
    }
    fn admit(&self, receipt: WritePlatformReceipt) -> Result<OrdinaryWriteAdmission, T> {
        let rechecks = Cell::new(0);
        admit_with(
            receipt,
            |receipt| {
                rechecks.set(rechecks.get() + 1);
                match (rechecks.get(), self.second_recheck) {
                    (2, Some(script)) => script(),
                    _ => receipt.recheck(),
                }
            },
            || {
                if let Some(hook) = self.before_gate {
                    hook();
                }
                self.gates.set(self.gates.get() + 1);
                DurableWriteGate::for_tests(&self.gate, self.gate_limits)
            },
            |gate, receipt| {
                gate.admit_with(
                    receipt.qualification(),
                    HomeSource::Fixture(self.home),
                    &self.gate_seam,
                )
            },
        )
    }
    fn admit_after(&self, ended: CreatorActEnded) -> Result<OrdinaryWriteAdmission, T> {
        if let Some(hook) = self.before_b {
            hook();
        }
        let producers = self.produce(InitialInstallationAttempt::for_tests_after(
            ended,
            &self.first,
            &self.second,
            self.limits_b,
        ))?;
        self.admit(producers.seal())
    }
}
fn analyze(
    owners: &OnScratch<'_>,
    request: &RequestIdentity,
    notice: &mut Notice<'_>,
) -> Result<DurableEntry, EntryRefusal> {
    enter(owners, CreatorCommand::Analyze, false, request, notice)
}
/// The target every intent here discloses: I under the real account's home.
/// The test creator publishes under the scratch H, but the intent's target
/// is built from the actor, the real account (law 464 item 3), and opens
/// nothing.
fn disclosed() -> PathBuf {
    let flag = AtomicBool::new(false);
    let mut attempt = InitialInstallationAttempt::for_tests(&flag, None).unwrap();
    installation(attempt.observe_actor().unwrap().home())
}
/// The notice the intent writes for I (law 464 item 3).
fn notice_for(i: &Path) -> String {
    format!(
        "opensip: first use creates the installation at {}; retention DEFAULTED \
         durable-unbounded; backup status unknown.\n",
        i.display()
    )
}
/// The creation record of I, as the act discloses it.
fn created_at(i: &Path) -> Option<Created> {
    Some(Created {
        classification: BackupClassification::Unknown,
        target: i.to_owned(),
    })
}

/// Another creator's complete I on `home`, published by the real creator on
/// its own test attempt.
fn publish_other(tag: &str, home: &Path) {
    let mut w = receipts_at(tag, true, Some(home), None);
    let intent = w
        .attempt
        .mint_intent(
            &w.actor,
            CreatorCommand::Analyze,
            false,
            &RequestIdentity::draw().unwrap(),
            &mut Vec::new(),
        )
        .unwrap();
    let owners = Owners {
        actor: &w.actor,
        core: &w.core,
        platform: &w.platform,
    };
    let outcome = create_at(&mut w.attempt, &owners, intent, home, &Seam::live());
    assert!(matches!(outcome, Ok(Outcome::Published(_))), "{outcome:?}");
}
/// X4T-0's signed accepted store for this I's S and K, written as
/// `ReadFixture::accept_trust` writes it, so that a writer's lease-free
/// first read admits a view. Only before attempt B's gate, which reads the
/// trust current record once.
fn accept_trust(i: &Path) {
    use opensip_identity::JsonValue as V;
    let stores: Vec<String> = fs::read_dir(i.join("stores"))
        .unwrap()
        .map(|entry| entry.unwrap().file_name().into_string().unwrap())
        .collect();
    let [store] = stores.as_slice() else {
        panic!("{stores:?}")
    };
    let current = i.join(format!("trust/stores/{store}/state.v1"));
    let V::Object(capsule) = opensip_identity::parse_json(&fs::read(&current).unwrap()).unwrap()
    else {
        panic!("capsule")
    };
    let V::Object(state) = &capsule["store"] else {
        panic!("store")
    };
    let V::Integer(schema) = &state["stateSchema"] else {
        panic!("schema")
    };
    let before = tree(&i.join("trust"));
    crate::trust::write_accepted_trust_issued(i, store, schema.get(), Vec::new(), 1, None, None);
    for path in tree(&i.join("trust")).difference(&before) {
        private(path);
    }
}
const NO_GROUPS: &BTreeSet<u32> = &BTreeSet::new();
fn inputs() -> ProjectInputs<'static> {
    ProjectInputs {
        trust_groups: NO_GROUPS,
        environment: &[],
        system_sources: &[],
    }
}
/// R4 to R12 on an entry's writer, in the order J3d composes them: a
/// first-use project root under H admitted, its tracking observed, its first
/// registration, the handoff (namespace, lease, lease-free first read,
/// floor step), then `CommitSession::open`.
fn open_session(mut writer: OrdinaryWriteAdmission, home: &Path) -> CommitSession {
    let code = home.join("code");
    fs::create_dir(&code).unwrap();
    fs::set_permissions(&code, fs::Permissions::from_mode(0o755)).unwrap();
    let project = code.join("project");
    fs::create_dir(&project).unwrap();
    fs::set_permissions(&project, fs::Permissions::from_mode(0o755)).unwrap();
    let root = writer
        .admit_project_root(&project, None, NO_GROUPS)
        .unwrap();
    let tracking = writer
        .observe_project_tracking_with(&root, &inputs())
        .unwrap();
    let registered = writer
        .register_first_use_with(root, tracking, &inputs(), &Registration::live())
        .unwrap();
    let clock = scripted::Clock::new();
    let operation = writer
        .begin_operation_with(
            NamespaceSubject::Registered(registered),
            WriterLease::AppendWrite,
            &inputs(),
            &scripted::invocation(),
            scripted::seam(&clock, crate::trust::ObservationHook::live()),
        )
        .unwrap();
    CommitSession::open(operation).unwrap()
}

// ------------------------------------------------- J-C5: the steady state

#[test]
fn the_steady_state_takes_one_attempt_and_one_gate_and_writes_nothing() {
    churned(|| {
        let (_scratch, home) = scratch();
        publish_other("entry-steady-other", &home);
        let i = installation(&home);
        let before = contents(&i);
        let owners = on_scratch("entry-steady", &home, true);
        let mut notice = Notice::new();
        let entry = analyze(&owners, &RequestIdentity::draw().unwrap(), &mut notice).unwrap();
        // 3a: attempt A sealed as the write receipt, one gate, no creation.
        assert_eq!(entry.created, None);
        assert_eq!(owners.lineages.borrow().len(), 1);
        assert_eq!((owners.cores.get(), owners.gates.get()), (1, 1));
        assert!(owners.first.load(Ordering::SeqCst));
        assert!(!owners.second.load(Ordering::SeqCst));
        assert!(owners.published.borrow().is_none());
        // No intent, no notice and no change to P0 or any other file of I.
        assert!(notice.bytes.is_empty());
        assert_eq!(notice.flushes, 0);
        assert_eq!(contents(&i), before);
        // The admission holds the fence until it is released.
        assert!(!fence_free(&i));
        entry.admission.release().unwrap();
        assert!(fence_free(&i));
    });
}

// ------------------------------------------------ J-C6: first use, 3b

#[test]
fn first_use_discloses_before_any_effect_and_admits_a_fresh_attempt_b() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let owners = on_scratch("entry-first-use", &home, true);
        let lent = RequestIdentity::draw().unwrap();
        let disclosed_before_effects = Cell::new(false);
        let check = || disclosed_before_effects.set(!home.join(SUFFIX[0]).exists());
        let mut notice = Notice::new();
        notice.at_flush = Some(&check);
        let entry = analyze(&owners, &lent, &mut notice).unwrap();
        // The notice was written and flushed once, before the first creation
        // effect (the fixed ancestor `Library` did not exist yet).
        assert_eq!(
            String::from_utf8(notice.bytes.clone()).unwrap(),
            notice_for(&disclosed())
        );
        assert_eq!(notice.flushes, 1);
        assert!(disclosed_before_effects.get());
        // The act published I, and the record says so with the disclosed
        // target and classification (J1 item 9: `backupStatus: unknown`).
        assert_eq!(entry.created, created_at(&disclosed()));
        let created = entry.created.as_ref().unwrap();
        assert_eq!(
            (created.target(), created.backup_status()),
            (disclosed().as_path(), "unknown")
        );
        // Attempt B is fresh: a second slot, its own lineage, its core and
        // platform produced again on it; one gate, entered by attempt B.
        let lineages = owners.lineages.borrow().clone();
        assert_eq!(lineages.len(), 2);
        assert_ne!(lineages[0], lineages[1]);
        assert_eq!((owners.cores.get(), owners.gates.get()), (2, 1));
        assert!(owners.first.load(Ordering::SeqCst) && owners.second.load(Ordering::SeqCst));
        // J-C2 and J-C4b's prelude half: P0 records the lent RequestId and
        // the prelude's own ExecutionId, which is reserved in this process.
        let (request, execution) = owners.published.borrow().clone().unwrap();
        assert_eq!(request, rendered("req1_", lent.bytes()));
        assert_eq!(recorded(&i, "requestId", 37), BTreeSet::from([request]));
        assert_eq!(
            recorded(&i, "executionId", 38),
            BTreeSet::from([execution.clone()])
        );
        assert!(opensip_platform::execution_id_reserved(&execution));
        // A third allocation is refused: neither slot is free.
        assert_eq!(owners.first().unwrap_err(), T::Invariant);
        assert!(!fence_free(&i));
        entry.admission.release().unwrap();
        assert!(fence_free(&i));
    });
}

#[test]
fn the_two_slot_sequence_refuses_every_other_allocation() {
    // X1 r2 item 7: attempt B needs attempt A and the creator act's token,
    // and there is no third attempt. The token is minted here only because
    // this module is the act's own.
    let ended = || CreatorActEnded { _private: () };
    let (first, second) = (AtomicBool::new(false), AtomicBool::new(false));
    let refused = |begun: Result<InitialInstallationAttempt, AttemptError>| {
        attempt_error(&begun.err().expect("refused"))
    };
    // Attempt B before attempt A.
    assert_eq!(
        refused(InitialInstallationAttempt::for_tests_after(
            ended(),
            &first,
            &second,
            None
        )),
        T::Invariant
    );
    assert!(!second.load(Ordering::SeqCst));
    let a = InitialInstallationAttempt::for_tests(&first, None).unwrap();
    let b = InitialInstallationAttempt::for_tests_after(ended(), &first, &second, None).unwrap();
    assert_ne!(a.lineage(), b.lineage());
    // A third: neither a first slot again, nor a second attempt B.
    assert_eq!(
        refused(InitialInstallationAttempt::for_tests(&first, None)),
        T::Invariant
    );
    assert_eq!(
        refused(InitialInstallationAttempt::for_tests_after(
            ended(),
            &first,
            &second,
            None
        )),
        T::Invariant
    );
}

#[test]
fn the_creator_act_hands_attempt_b_values_only() {
    // J-C6's type-level pin. These patterns name every field and use no
    // `..`, so a field added to the token, the act's result, the record or
    // either entry result fails to compile here. None holds a handle, lock,
    // receipt or observation of attempt A.
    #[allow(dead_code)]
    fn values_only(act: CreatorAct, refusal: EntryRefusal, entry: DurableEntry) {
        let CreatorAct {
            ended: CreatorActEnded { _private: () },
            created,
        } = act;
        let (Some(Created {
            classification: _,
            target: _,
        })
        | None) = created;
        let EntryRefusal {
            termination: _,
            created: _,
        } = refusal;
        let DurableEntry {
            admission: _,
            created: _,
        } = entry;
    }
    // And the act consumes attempt A's producers by value, so they are
    // dropped inside it whatever it returns.
    let source = include_str!("installation_routing.rs");
    // (Spelled in two parts: X11a's J-C1 pin counts the definition's text in
    // every security source, this test file included.)
    let act = &source[source
        .find(concat!("pub(crate) fn ", "run_initial_creator("))
        .unwrap()..];
    let signature = &act[..act.find(") -> Result<CreatorAct, EntryRefusal> {").unwrap()];
    assert!(
        signature.contains("\n    producers: Producers,\n"),
        "{signature}"
    );
    assert!(!signature.contains("&mut Producers") && !signature.contains("&Producers"));
}

// ----------------------------- J-C8: LostRace and NotPristine continue

#[test]
fn not_pristine_ends_the_act_and_attempt_b_admits_the_existing_installation() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        // I appears after the probe and before the act's preparation.
        let other = || publish_other("entry-not-pristine-other", &home);
        let trust = || accept_trust(&i);
        let mut owners = on_scratch("entry-not-pristine", &home, true);
        owners.before_create = Some(&other);
        owners.before_b = Some(&trust);
        let mut notice = Notice::new();
        let entry = analyze(&owners, &RequestIdentity::draw().unwrap(), &mut notice).unwrap();
        // The act minted an intent (its notice is on standard error) but
        // published nothing: no creation record.
        assert_eq!(
            String::from_utf8(notice.bytes).unwrap(),
            notice_for(&disclosed())
        );
        assert_eq!(entry.created, None);
        assert!(owners.published.borrow().is_none());
        assert_eq!(owners.lineages.borrow().len(), 2);
        // Attempt B's writer is an ordinary writer: it reaches R12.
        let session = open_session(entry.admission, &home);
        assert!(opensip_platform::execution_id_reserved(
            session.execution_id()
        ));
        let _ = session.refused().finish();
    });
}

#[test]
fn a_lost_race_ends_the_act_and_attempt_b_admits_the_winner() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        // The winner publishes a complete I just before the loser's rename.
        let winner = RefCell::new(true);
        let hook = |point: Point| {
            if point == Point::Rename && winner.replace(false) {
                publish_other("entry-lost-race-winner", &home);
            }
        };
        let mut owners = on_scratch("entry-lost-race", &home, true);
        owners.creator.at = Some(&hook);
        let trust = || accept_trust(&i);
        owners.before_b = Some(&trust);
        let entry = analyze(
            &owners,
            &RequestIdentity::draw().unwrap(),
            &mut Notice::new(),
        )
        .unwrap();
        assert!(!*winner.borrow());
        assert_eq!(entry.created, None);
        assert!(owners.published.borrow().is_none());
        assert_eq!(owners.lineages.borrow().len(), 2);
        let session = open_session(entry.admission, &home);
        assert!(opensip_platform::execution_id_reserved(
            session.execution_id()
        ));
        let _ = session.refused().finish();
    });
}

#[test]
fn a_lost_race_to_a_foreign_entry_ends_at_attempt_bs_gate_in_the_custody_row() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let hook = |point: Point| {
            if point == Point::Rename {
                fs::create_dir(&i).unwrap();
                fs::set_permissions(&i, fs::Permissions::from_mode(0o700)).unwrap();
            }
        };
        let mut owners = on_scratch("entry-foreign", &home, true);
        owners.creator.at = Some(&hook);
        let refused = analyze(
            &owners,
            &RequestIdentity::draw().unwrap(),
            &mut Notice::new(),
        )
        .unwrap_err();
        // The foreign I has no zero-rights owner allow: the private
        // judgment, at attempt B's gate. Nothing was published.
        assert_eq!(
            refused,
            EntryRefusal {
                termination: T::Custody {
                    subject: "acl-not-returned"
                },
                created: None,
            }
        );
        assert_eq!(owners.lineages.borrow().len(), 2);
    });
}

// ------------------------- J-C6b: refusals after publication disclose it

/// J-C6b: the entry on an empty scratch H publishes I, then attempt B is
/// refused on `row`; the refusal carries the creation record, and the
/// refused writer keeps no fence.
fn refused_after_publication(owners: &OnScratch<'_>, row: T) {
    let refused = analyze(
        owners,
        &RequestIdentity::draw().unwrap(),
        &mut Notice::new(),
    )
    .unwrap_err();
    assert_eq!(
        refused,
        EntryRefusal {
            termination: row,
            created: created_at(&disclosed()),
        }
    );
    assert_eq!(refused.created.as_ref().unwrap().backup_status(), "unknown");
    assert!(owners.published.borrow().is_some());
    // Attempt B was allocated, whatever refused it.
    assert!(owners.second.load(Ordering::SeqCst));
}

#[test]
fn attempt_bs_refused_producers_after_publication_carry_the_creation_record() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let mut owners = on_scratch("entry-after-producers", &home, true);
        owners.limits_b = Some(WorkCost {
            objects: 1,
            edges: 1,
            bytes: 64,
        });
        refused_after_publication(&owners, T::BudgetExhausted);
        assert_eq!(owners.gates.get(), 0);
        assert!(fence_free(&i));
    });
}

#[test]
fn attempt_bs_busy_gate_after_publication_carries_the_creation_record() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let held = RefCell::new(None);
        let hold = || {
            *held.borrow_mut() = FileLock::try_acquire(
                fs::File::open(i.join("lifecycle.fence")).unwrap(),
                LockMode::Exclusive,
            )
            .unwrap();
        };
        let mut owners = on_scratch("entry-after-busy", &home, true);
        owners.before_b = Some(&hold);
        refused_after_publication(&owners, T::Busy);
        assert!(held.borrow().is_some());
        drop(held);
        assert!(fence_free(&i));
    });
}

#[test]
fn attempt_bs_failed_barrier_after_publication_carries_the_creation_record() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let barrier =
            |slot: GateBarrier| -> Option<std::io::Result<opensip_platform::DirectoryBarrier>> {
                (slot == GateBarrier::Installation)
                    .then(|| Err(std::io::Error::from_raw_os_error(5)))
            };
        let mut owners = on_scratch("entry-after-barrier", &home, true);
        owners.gate_seam.barrier = Some(&barrier);
        refused_after_publication(&owners, T::HostIo);
        assert!(fence_free(&i));
    });
}

#[test]
fn attempt_bs_failed_recheck_after_publication_carries_the_creation_record() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let recheck = || Err(T::PlatformUnqualified);
        let mut owners = on_scratch("entry-after-recheck", &home, true);
        owners.second_recheck = Some(&recheck);
        refused_after_publication(&owners, T::PlatformUnqualified);
        // Step 4's refusal released the fence before returning.
        assert!(fence_free(&i));
    });
}

#[test]
fn a_refusal_after_the_rename_carries_the_record_and_one_before_it_does_not() {
    churned(|| {
        // After the rename: the I-parent barrier fails (468 item 6's
        // "any failure after the rename"), and I is visible.
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let script = |slot: usize| -> Option<std::io::Result<opensip_platform::DirectoryBarrier>> {
            (slot == I_PARENT).then(|| Err(std::io::Error::from_raw_os_error(5)))
        };
        let mut owners = on_scratch("entry-after-rename", &home, true);
        owners.creator.barriers = Some(&script);
        let refused = analyze(
            &owners,
            &RequestIdentity::draw().unwrap(),
            &mut Notice::new(),
        )
        .unwrap_err();
        assert_eq!(
            refused,
            EntryRefusal {
                termination: T::HostIo,
                created: created_at(&disclosed()),
            }
        );
        assert!(i.is_dir());
        // No attempt B followed the refused act.
        assert_eq!(owners.lineages.borrow().len(), 1);
        assert!(!owners.second.load(Ordering::SeqCst));

        // Before the rename (not performed, or indeterminate, LD6-1): no
        // record, no I.
        for class in [
            DirectoryRenameClass::NotPerformed,
            DirectoryRenameClass::Indeterminate,
        ] {
            let (_scratch, home) = scratch();
            let rename = || Some(class);
            let mut owners = on_scratch("entry-rename-refused", &home, true);
            owners.creator.rename = Some(&rename);
            let mut notice = Notice::new();
            let refused =
                analyze(&owners, &RequestIdentity::draw().unwrap(), &mut notice).unwrap_err();
            assert_eq!(
                refused,
                EntryRefusal {
                    termination: T::HostIo,
                    created: None,
                },
                "{class:?}"
            );
            assert!(!installation(&home).exists());
            // The notice was still written before the effects.
            assert_eq!(notice.flushes, 1);
        }
    });
}

#[test]
fn a_gate_that_cannot_charge_after_publication_keeps_the_record() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let mut owners = on_scratch("entry-gate-budget", &home, true);
        owners.gate_limits = Some(WorkCost {
            objects: 4,
            edges: 4,
            bytes: 4096,
        });
        let refused = analyze(
            &owners,
            &RequestIdentity::draw().unwrap(),
            &mut Notice::new(),
        )
        .unwrap_err();
        assert_eq!(
            refused,
            EntryRefusal {
                termination: T::BudgetExhausted,
                created: created_at(&disclosed()),
            }
        );
        assert!(fence_free(&i));
    });
}

// --------------------------------------- J-C7: the probe and its race

#[test]
fn the_probe_has_three_outcomes_and_selects_the_route_only() {
    churned(|| {
        let (_scratch, home) = scratch();
        let probe_on = |tag: &str, premise: bool| {
            let owners = on_scratch(tag, &home, premise);
            let mut producers = owners.first().unwrap();
            let used = producers.attempt.used();
            let presence = probe(&mut producers, &home);
            // Charged to attempt A's ledger.
            assert!(producers.attempt.used().edges > used.edges, "{tag}");
            presence
        };
        // Positive absence, at the first missing fixed-suffix component.
        assert_eq!(
            probe_on("probe-empty", true),
            Ok(Presence::PositivelyAbsent(Suffix::Library))
        );
        // A refusal on its row: the omitted ACL at `/` without the premise,
        // and a file where a fixed ancestor belongs, which is not absence.
        assert_eq!(
            probe_on("probe-no-premise", false),
            Err(T::Custody {
                subject: "ancestor-acl-omitted"
            })
        );
        fs::write(home.join(SUFFIX[0]), b"not a directory").unwrap();
        let refused = probe_on("probe-file", true).unwrap_err();
        assert_ne!(refused, T::NotInitialized, "{refused:?}");
        fs::remove_file(home.join(SUFFIX[0])).unwrap();
        // Present; then I's own name absent under a present `OpenSIP`.
        publish_other("probe-present-other", &home);
        assert_eq!(probe_on("probe-present", true), Ok(Presence::Present));
        // The probe holds nothing: the fence is free after it.
        assert!(fence_free(&installation(&home)));
        remove_installation(&installation(&home));
        assert_eq!(
            probe_on("probe-installation-absent", true),
            Ok(Presence::PositivelyAbsent(Suffix::Installation))
        );
    });
}

#[test]
fn present_then_absent_at_the_gate_ends_on_not_initialized() {
    churned(|| {
        let (_scratch, home) = scratch();
        publish_other("entry-race-other", &home);
        let i = installation(&home);
        // I is deleted outside OpenSIP after the probe said `Present`.
        let delete = || remove_installation(&i);
        let mut owners = on_scratch("entry-race", &home, true);
        owners.before_gate = Some(&delete);
        let mut notice = Notice::new();
        let refused = analyze(&owners, &RequestIdentity::draw().unwrap(), &mut notice).unwrap_err();
        assert_eq!(
            refused,
            EntryRefusal {
                termination: T::NotInitialized,
                created: None,
            }
        );
        // The steady-state route: no intent, notice or creation.
        assert!(notice.bytes.is_empty());
        assert!(owners.published.borrow().is_none());
        assert!(!i.exists());
    });
}

#[test]
fn without_the_premise_the_probe_refuses_at_the_root_before_any_intent() {
    churned(|| {
        let (_scratch, home) = scratch();
        let owners = on_scratch("entry-no-premise", &home, false);
        let mut notice = Notice::new();
        let refused = analyze(&owners, &RequestIdentity::draw().unwrap(), &mut notice).unwrap_err();
        assert_eq!(
            refused,
            EntryRefusal {
                termination: T::Custody {
                    subject: "ancestor-acl-omitted"
                },
                created: None,
            }
        );
        assert!(notice.bytes.is_empty());
        assert_eq!(fs::read_dir(&home).unwrap().count(), 0);
    });
}

// ------------------------- J-C4b: three distinct reserved ExecutionIds

#[test]
fn a_first_use_invocation_reserves_three_distinct_execution_ids() {
    churned(|| {
        let (_scratch, home) = scratch();
        let i = installation(&home);
        let mut owners = on_scratch("entry-three-ids", &home, true);
        let trust = || accept_trust(&i);
        owners.before_b = Some(&trust);
        let entry = analyze(
            &owners,
            &RequestIdentity::draw().unwrap(),
            &mut Notice::new(),
        )
        .unwrap();
        // The prelude's: reserved in `mint_intent`, before P0 was staged.
        let (_, prelude) = owners.published.borrow().clone().unwrap();
        assert!(opensip_platform::execution_id_reserved(&prelude));
        // The analysis attempt's: reserved at `CommitSession::open` (R12).
        let session = open_session(entry.admission, &home);
        let attempt = session.execution_id().to_owned();
        assert!(opensip_platform::execution_id_reserved(&attempt));
        // The render attempt's: the host's draw at its start (J3d's call).
        let render = opensip_platform::reserve_execution_id().unwrap();
        let ids = BTreeSet::from([prelude.clone(), attempt.clone(), render.as_str().to_owned()]);
        assert_eq!(ids.len(), 3, "{ids:?}");
        let _ = session.refused().finish();
    });
}

// ----------------------------------- J-C9: a development build at F0

#[test]
fn a_development_build_ends_at_f0_with_no_notice_and_no_installation_path() {
    // The process's one attempt: the actor is the real account, and
    // InitialCore refuses at F0 before the probe, the intent, any notice or
    // any installation path. This is the one test in this binary that
    // allocates the process's production attempt.
    let mut notice = Notice::new();
    let refused = enter_durable_analysis(
        CreatorCommand::Analyze,
        false,
        &RequestIdentity::draw().unwrap(),
        &mut notice,
    )
    .unwrap_err();
    assert_eq!(
        refused,
        EntryRefusal {
            termination: T::NoEmbeddedRelease,
            created: None,
        }
    );
    assert!(notice.bytes.is_empty() && notice.flushes == 0);
    let real = std::env::var_os("HOME").map(PathBuf::from).unwrap();
    assert!(!real.join("Library/Application Support/OpenSIP").exists());
}

#[test]
fn the_entry_probes_first_and_has_exactly_two_routes() {
    // Source pins on the composition (J1 item 3): the producers, then the
    // probe, then either the steady state, which seals attempt A and mints
    // no intent, or first use, which runs the act and then attempt B. The
    // module enters no gate itself and produces no endpoint (468 r6 item 1;
    // X3a r6 item 2): the gate is X1's, reached through `EntryOwners`.
    let source = include_str!("installation_routing.rs");
    let source = source.split("#[cfg(test)]").next().unwrap();
    let enter = &source[source.find("pub(super) fn enter(").unwrap()..];
    let enter = &enter[..enter.find("\n}\n").unwrap()];
    let at = |needle: &str| enter.find(needle).unwrap_or_else(|| panic!("{needle}"));
    assert!(at("owners.first()") < at("probe(&mut producers"));
    assert!(at("probe(&mut producers") < at("Presence::Present =>"));
    assert!(at("Presence::Present =>") < at("producers.seal()"));
    assert!(at("producers.seal()") < at("Presence::PositivelyAbsent(_) =>"));
    assert!(at("Presence::PositivelyAbsent(_) =>") < at("run_initial_creator("));
    assert!(at("run_initial_creator(") < at("owners.admit_after(ended)"));
    assert!(!enter.contains("mint_intent"));
    assert!(!source.contains("DurableWriteGate"));
    assert_eq!(source.matches(".mint_intent(").count(), 1);
}

#[test]
fn the_creator_act_has_no_store_trust_or_registration_entry() {
    // X3a r6 item 2 (S5), X4B r6 (S6) and X2 r10 item 6 (S7) need no code;
    // these pins keep them so. The creator act's module names no endpoint,
    // trust acceptance or registration; first registration has one entry,
    // on the ordinary writer's gate; and no production source keeps 468c's
    // `AdmittedInstallation`, the creator's own admission.
    let routing = include_str!("installation_routing.rs");
    let routing = routing.split("#[cfg(test)]").next().unwrap();
    for name in [
        "store_endpoint",
        "accept_bootstrap",
        "fenced_operation_read",
        "register_",
    ] {
        assert!(!routing.contains(name), "{name}");
    }
    let registration = include_str!("first_registration.rs");
    assert_eq!(registration.matches("fn register_on_gate(").count(), 1);
    let writer = include_str!("ordinary_writer.rs");
    assert_eq!(
        writer
            .matches("first_registration::register_on_gate(")
            .count(),
        1
    );
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    for path in tree(&root) {
        if path.extension().is_some_and(|e| e == "rs")
            && !path.ends_with("installation_routing_tests.rs")
        {
            let text = fs::read_to_string(&path).unwrap();
            assert!(!text.contains("AdmittedInstallation"), "{}", path.display());
            if path.file_name().unwrap() != "first_registration.rs"
                && path.file_name().unwrap() != "ordinary_writer.rs"
                && !path.to_string_lossy().ends_with("_tests.rs")
            {
                assert!(!text.contains("register_on_gate("), "{}", path.display());
            }
        }
    }
}

#[test]
fn representative_refusals_choose_their_rows() {
    use std::io;
    let budget = WorkFailure::<CreationRefusal>::Budget(WorkBudgetError::Edges);
    assert_eq!(work(&budget, creation_refusal), T::BudgetExhausted);
    let cases: Vec<(T, T)> = vec![
        (gate_refusal(&GateRefusal::Busy), T::Busy),
        (gate_refusal(&GateRefusal::Absent), T::NotInitialized),
        (
            gate_refusal(&GateRefusal::Incomplete(IncompleteRefusal::Chain)),
            T::Incomplete,
        ),
        (
            gate_refusal(&GateRefusal::Budget(WorkBudgetError::Objects)),
            T::BudgetExhausted,
        ),
        (gate_refusal(&GateRefusal::Latched), T::Invariant),
        (
            gate_refusal(&GateRefusal::Io(IoFailure::Lock(io::Error::other("x")))),
            T::HostIo,
        ),
        (
            gate_refusal(&GateRefusal::Account(ActorRefusal::AccountChanged)),
            T::AccountRefused,
        ),
        (
            creation_refusal(&CreationRefusal::Rename {
                class: DirectoryRenameClass::Indeterminate,
                failure: None,
            }),
            T::HostIo,
        ),
        (
            creation_refusal(&CreationRefusal::AfterRename(Box::new(
                CreationRefusal::Budget(WorkBudgetError::Edges),
            ))),
            T::BudgetExhausted,
        ),
        (
            creation_refusal(&CreationRefusal::AfterRename(Box::new(
                CreationRefusal::FenceChanged,
            ))),
            T::HostIo,
        ),
        (
            creation_refusal(&CreationRefusal::FenceBusy),
            T::Custody {
                subject: "stage-fence-busy",
            },
        ),
        (
            creation_refusal(&CreationRefusal::Core(
                InitialCoreRefusal::EmbeddedRootAbsent,
            )),
            T::NoEmbeddedRelease,
        ),
        (
            creation_refusal(&CreationRefusal::Core(InitialCoreRefusal::ReleaseRevoked)),
            T::CoreRefused {
                subject: "release-revoked",
            },
        ),
        (
            creation_refusal(&CreationRefusal::Intent(IntentRefusal::Storage(
                BackupChoiceRequired,
            ))),
            T::BackupChoiceRequired,
        ),
        (
            platform_refusal(&InitialPlatformRefusal::Unadmitted(vec![
                "NT-TCB-BOOT:INSTALL_ROOT_FS".into(),
                "NT-TCB-IDENTITY:BUILD_GRAMMAR".into(),
            ])),
            T::PlatformDecision {
                detail: TcbDetail::Boot,
                subject: "INSTALL_ROOT_FS".into(),
            },
        ),
        (
            platform_refusal(&InitialPlatformRefusal::Unadmitted(vec![])),
            T::PlatformUnqualified,
        ),
        (
            platform_refusal(&InitialPlatformRefusal::Translated),
            T::PlatformUnqualified,
        ),
        (
            platform_refusal(&InitialPlatformRefusal::HomeFilesystem),
            T::InstallRootFilesystem,
        ),
        (
            preparation_refusal(&ParentPreparationRefusal::Parent(
                ParentRefusal::AncestorAclOmitted { component: 0 },
            )),
            T::Custody {
                subject: "ancestor-acl-omitted",
            },
        ),
        (
            preparation_refusal(&ParentPreparationRefusal::Unfinishable),
            T::Custody {
                subject: "opensip-unfinishable",
            },
        ),
        (
            actor_refusal(&ActorRefusal::HomeSpelling),
            T::AccountRefused,
        ),
        (attempt_error(&AttemptError::AlreadyAllocated), T::Invariant),
    ];
    for (got, want) in cases {
        assert_eq!(got, want);
    }
}
