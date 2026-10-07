//! Named crash barrier points for the X9 crash, lock and revocation matrix
//! (law X9 r1 items 1 to 5). This module exists only under the test-only
//! `crash-matrix` feature, which no manifest enables and which refuses every
//! build without debug assertions (item 2).
//!
//! A point is reached through `crash_barrier!` and named by the thread's
//! `crash_scope!` stack: `<scope>.<step>` at a protocol site, and
//! `<scope>/<primitive-step>.<before|after>` inside a platform primitive.
//! Occurrence `#k` (1-based) counts per full name within one process.
//!
//! Without `OPENSIP_X9_ARMS` in the environment, every point is one read of
//! a process-wide `OnceLock` followed by a return: no record, no wait and no
//! change to the primitive. With it (a matrix child, `OPENSIP_X9_CHILD` set),
//! every reached point writes one tagged stderr record
//! `X9|<pid>|<thread>|<n>|<full name>#<k>|<event>|<payload>` in a single
//! `write(2)` of at most 512 bytes, and an armed point acts:
//! - `hold`: write `held`, then block on stdin until the parent writes
//!   `resume` (only when exactly one thread holds) or `resume <name>#<k>`,
//!   or kills the process. No product code runs between the two;
//! - `fail-before` / `fail-after` (fallible points): return the step's
//!   native failure without, or after, performing the effect;
//! - `torn` (write points): write the first half of the bytes, then hold;
//! - `inject-id:<id>` (`x3d.session.execution-draw` only): return that id.
//!
//! An action the point's kind does not admit, a primitive reached outside
//! any scope, an unknown scope or a malformed arming is a `harness-error`
//! record followed by exit status 86. This module never sleeps, polls or
//! waits on a timer; its only waits are a blocking stdin read and a condvar
//! wait for a resume another holder read.
use std::cell::{Cell, RefCell};
use std::collections::{BTreeMap, HashMap};
use std::io::{self, BufRead, Write};
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Condvar, Mutex, MutexGuard, OnceLock, PoisonError};

pub mod driver;
#[cfg(test)]
mod self_tests;

/// COMMON4's signal names, admitted on the test-only X9 control channel.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SignalInput {
    Sigint,
    Sigterm,
    Sighup,
}
impl SignalInput {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Sigint => "SIGINT",
            Self::Sigterm => "SIGTERM",
            Self::Sighup => "SIGHUP",
        }
    }
}
/// One runner-owned registration. Its thread alone delivers control signals;
/// held product threads only route input. Drop closes and joins that input.
pub struct SignalRegistration {
    active: Option<&'static Active>,
    thread: Option<std::thread::JoinHandle<()>>,
}
impl Drop for SignalRegistration {
    fn drop(&mut self) {
        if let Some(active) = self.active {
            lock(&active.signal_input).take();
        }
        if let Some(thread) = self.thread.take()
            && thread.join().is_err()
            && let Some(active) = self.active
        {
            active.harness_exit("signal input thread failed");
        }
    }
}
pub fn register_signal_input(input: impl Fn(SignalInput) + Send + 'static) -> SignalRegistration {
    let Some(active) = state() else {
        return SignalRegistration {
            active: None,
            thread: None,
        };
    };
    let (sender, receiver) = std::sync::mpsc::channel();
    {
        let mut registered = lock(&active.signal_input);
        if registered.is_some() {
            drop(registered);
            active.harness_exit("signal input already registered");
        }
        *registered = Some(sender);
    }
    let thread = std::thread::spawn(move || {
        while let Ok(signal) = receiver.recv() {
            if std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| input(signal))).is_err() {
                active.harness_exit("signal input callback failed");
            }
            active.record("-", "signalled", signal.as_str());
        }
    });
    SignalRegistration {
        active: Some(active),
        thread: Some(thread),
    }
}

/// The arming list; its presence (even empty) turns tracing on.
pub const ARMS_VAR: &str = "OPENSIP_X9_ARMS";
/// The driver name of a matrix child.
pub const CHILD_VAR: &str = "OPENSIP_X9_CHILD";
/// The path of the child driver's input file under the run's scratch root.
pub const INPUT_VAR: &str = "OPENSIP_X9_INPUT";
/// Law X9 r2 item 3: the scripted wall clock, `<E>:<k>`.
pub const CLOCK_VAR: &str = "OPENSIP_X9_CLOCK";
/// The script's name in a run record (`clock.script`).
pub const CLOCK_SCRIPT: &str = "x9-ordinal-3600";
/// Wall readings per process ordinal: the 3600th reading is a harness error.
pub const CLOCK_READINGS: u64 = 3600;
/// The exit status of a child that reports a `harness-error`.
pub const HARNESS_EXIT_CODE: i32 = 86;
/// One record is one `write(2)` of at most `PIPE_BUF` bytes on macOS.
pub const RECORD_LIMIT: usize = 512;
/// The one point of kind `draw` (item 4).
pub const DRAW_POINT: &str = "x3d.session.execution-draw";
/// The platform primitives' own steps (item 1).
pub const PRIMITIVE_STEPS: &[&str] = &[
    "create",
    "write",
    "file-barrier",
    "rename",
    "link",
    "directory-barrier",
    "reopen-confirm",
    "lock",
    "unlock",
];

/// Whether a scope's protocol points can change durable state. A kill set
/// holds only durability points; a thread other than the killed one may
/// report only read-only points after the kill point (item 3).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Access {
    Durable,
    ReadOnly,
}

// The scope names fixed by law X9 r1 item 5. tools/check_crash_matrix.py
// reads this block for the release-absence scan; keep one entry per line.
// BEGIN X9 SCOPE REGISTRY
pub const SCOPES: &[(&str, Access)] = &[
    ("x4t.floor-publication", Access::Durable),
    ("x3b.floor", Access::Durable),
    ("x3b.end.floor", Access::Durable),
    ("x3b.init", Access::Durable),
    ("x3b.start.witness", Access::Durable),
    ("x3b.append.seal", Access::Durable),
    ("x3b.append.rev", Access::Durable),
    ("x3b.append.cln", Access::Durable),
    ("x3b.append.terminal", Access::Durable),
    ("x3b.rollover", Access::Durable),
    ("x3c.ledger-create", Access::Durable),
    ("x3c.attempt", Access::Durable),
    ("x3c.object", Access::Durable),
    ("x3c.evidence", Access::Durable),
    ("x3d.session", Access::Durable),
    ("x3d.publish", Access::Durable),
    ("x3d.finish", Access::Durable),
    ("x4.checkpoint", Access::Durable),
    ("x4.gate", Access::Durable),
    ("x4.observer", Access::ReadOnly),
    ("x2.fence", Access::Durable),
    ("x2.lease", Access::Durable),
    ("x6.recover", Access::ReadOnly),
    ("x6.sweep", Access::Durable),
    ("x7.delivery", Access::Durable),
];
// END X9 SCOPE REGISTRY

// The self-tests' own scopes exist only in this crate's test build.
#[cfg(test)]
pub(crate) const SELF_TEST_SCOPES: &[(&str, Access)] = &[
    ("x9.selftest", Access::Durable),
    ("x9.selftest-observer", Access::ReadOnly),
];
#[cfg(not(test))]
const SELF_TEST_SCOPES: &[(&str, Access)] = &[];

/// The kind every point declares in its macro (item 4).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    /// Admits only `hold`.
    Step,
    /// Admits `hold`, `fail-before` at `.before` and `fail-after` at `.after`.
    Fallible,
    /// Admits `hold`, and `torn` at `.before`.
    Write,
    /// Admits `hold`; an armed rendezvous replaces the product's timed wait.
    Gate,
    /// Admits `hold` and `inject-id`; only `x3d.session.execution-draw`.
    Draw,
}

/// The injected failure a fallible point's caller turns into its own error.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Fault {
    /// The effect was not performed.
    Before,
    /// The effect was performed and reports failure.
    After,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Action {
    Hold,
    FailBefore,
    FailAfter,
    Torn,
    InjectId(String),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Occurrence {
    Nth(u32),
    Every,
}

/// One `<full name>#<k|*>=<action>` entry of `OPENSIP_X9_ARMS`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Arm {
    pub point: String,
    pub occurrence: Occurrence,
    pub action: Action,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Phase {
    Before,
    After,
}

fn registered(scope: &str) -> Option<Access> {
    SCOPES
        .iter()
        .chain(SELF_TEST_SCOPES)
        .find(|(name, _)| *name == scope)
        .map(|(_, access)| *access)
}

/// The longest registered scope that `path` equals or extends at a `.`.
fn registered_prefix(path: &str) -> Option<(&str, Access)> {
    let mut found = None;
    for (index, _) in path.match_indices('.').chain([(path.len(), "")]) {
        if let Some(access) = registered(&path[..index]) {
            found = Some((&path[..index], access));
        }
    }
    found
}

fn segments_valid(path: &str) -> bool {
    !path.is_empty()
        && path.split('.').all(|segment| {
            !segment.is_empty()
                && segment
                    .bytes()
                    .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-' || b == b'_')
        })
}

/// Check a full point name against the grammar: a registered scope, any
/// further scope or step segments, and for a primitive point exactly one
/// `/<primitive-step>.<before|after>`. A protocol point has at least one
/// segment after its registered scope.
pub fn validate_point(name: &str) -> Result<(), String> {
    let (path, primitive) = match name.split_once('/') {
        Some((path, primitive)) => (path, Some(primitive)),
        None => (name, None),
    };
    if !segments_valid(path) {
        return Err(format!("invalid point name {name:?}"));
    }
    let Some((scope, _)) = registered_prefix(path) else {
        return Err(format!("unregistered scope in {name:?}"));
    };
    match primitive {
        Some(primitive) => {
            let Some((step, phase)) = primitive.rsplit_once('.') else {
                return Err(format!("primitive point without a phase: {name:?}"));
            };
            if !PRIMITIVE_STEPS.contains(&step) || !matches!(phase, "before" | "after") {
                return Err(format!("unknown primitive point {name:?}"));
            }
        }
        None if scope.len() == path.len() => {
            return Err(format!("protocol point without a step: {name:?}"));
        }
        None => {}
    }
    Ok(())
}

/// A primitive point is always a durability point; a protocol point is one
/// unless its scope is registered read-only (item 5's kill set).
pub fn is_durability_point(name: &str) -> bool {
    if name.contains('/') {
        return true;
    }
    registered_prefix(name).is_none_or(|(_, access)| access == Access::Durable)
}

fn parse_action(text: &str) -> Result<Action, String> {
    Ok(match text {
        "hold" => Action::Hold,
        "fail-before" => Action::FailBefore,
        "fail-after" => Action::FailAfter,
        "torn" => Action::Torn,
        _ => {
            let Some(id) = text.strip_prefix("inject-id:") else {
                return Err(format!("unknown action {text:?}"));
            };
            let valid = id.len() > "exec1_".len()
                && id.len() <= 128
                && id.starts_with("exec1_")
                && id
                    .bytes()
                    .all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-');
            if !valid {
                return Err(format!("invalid injected ExecutionId {id:?}"));
            }
            Action::InjectId(id.to_owned())
        }
    })
}

/// Parse `OPENSIP_X9_ARMS`: a comma-separated list of
/// `<full name>#<k|*>=<action>`; the empty string arms nothing (a census).
/// Whether a point's kind admits its action is checked where it is reached.
pub fn parse_arms(text: &str) -> Result<Vec<Arm>, String> {
    let mut arms: Vec<Arm> = Vec::new();
    if text.is_empty() {
        return Ok(arms);
    }
    for entry in text.split(',') {
        let Some((target, action)) = entry.split_once('=') else {
            return Err(format!("arm without an action: {entry:?}"));
        };
        let Some((point, occurrence)) = target.rsplit_once('#') else {
            return Err(format!("arm without an occurrence: {entry:?}"));
        };
        validate_point(point)?;
        let occurrence = match occurrence {
            "*" => Occurrence::Every,
            digits if !digits.starts_with('0') && digits.bytes().all(|b| b.is_ascii_digit()) => {
                Occurrence::Nth(
                    digits
                        .parse()
                        .map_err(|_| format!("invalid occurrence in {entry:?}"))?,
                )
            }
            _ => return Err(format!("invalid occurrence in {entry:?}")),
        };
        let action = parse_action(action)?;
        if matches!(action, Action::InjectId(_)) && point != DRAW_POINT {
            return Err(format!("inject-id outside {DRAW_POINT}: {entry:?}"));
        }
        if arms.iter().any(|arm| {
            arm.point == point
                && (arm.occurrence == occurrence
                    || arm.occurrence == Occurrence::Every
                    || occurrence == Occurrence::Every)
        }) {
            return Err(format!("overlapping arms for {point:?}"));
        }
        arms.push(Arm {
            point: point.to_owned(),
            occurrence,
            action,
        });
    }
    Ok(arms)
}

fn admitted(kind: Kind, phase: Option<Phase>, action: &Action) -> bool {
    match action {
        Action::Hold => true,
        Action::FailBefore => kind == Kind::Fallible && phase == Some(Phase::Before),
        Action::FailAfter => kind == Kind::Fallible && phase == Some(Phase::After),
        Action::Torn => kind == Kind::Write && phase == Some(Phase::Before),
        Action::InjectId(_) => kind == Kind::Draw,
    }
}

fn primitive_kind(step: &str) -> Option<Kind> {
    match step {
        "write" => Some(Kind::Write),
        "file-barrier" | "rename" | "directory-barrier" => Some(Kind::Fallible),
        step if PRIMITIVE_STEPS.contains(&step) => Some(Kind::Step),
        _ => None,
    }
}

#[derive(Default)]
struct Control {
    // A held thread is reading stdin for every holder.
    reader: bool,
    // stdin reached end of file: the parent is gone.
    closed: bool,
    // Held points by `<name>#<k>`, and whether a resume has named them.
    held: BTreeMap<String, bool>,
}

struct Active {
    arms: Vec<Arm>,
    occurrences: Mutex<HashMap<String, u32>>,
    // Numbers records and serializes their writes, so `n` is stderr order.
    sequence: Mutex<u64>,
    control: Mutex<Control>,
    resumed: Condvar,
    signal_input: Mutex<Option<std::sync::mpsc::Sender<SignalInput>>>,
}

enum Reached {
    Passed,
    Resumed,
    // An admitted action for the caller, at `<name>#<k>`.
    Act(String),
}

static STATE: OnceLock<Option<Active>> = OnceLock::new();
static NEXT_THREAD: AtomicU64 = AtomicU64::new(1);

thread_local! {
    static THREAD: Cell<u64> = const { Cell::new(0) };
    static SCOPE: RefCell<Vec<String>> = const { RefCell::new(Vec::new()) };
}

fn lock<T>(mutex: &Mutex<T>) -> MutexGuard<'_, T> {
    mutex.lock().unwrap_or_else(PoisonError::into_inner)
}

fn thread_index() -> u64 {
    THREAD.with(|cell| {
        if cell.get() == 0 {
            cell.set(NEXT_THREAD.fetch_add(1, Ordering::Relaxed));
        }
        cell.get()
    })
}

fn state() -> Option<&'static Active> {
    STATE.get_or_init(initialize).as_ref()
}

fn initialize() -> Option<Active> {
    let arms = std::env::var_os(ARMS_VAR)?;
    if std::env::var_os(CHILD_VAR).is_none() {
        early_exit("OPENSIP_X9_ARMS outside a matrix child");
    }
    let Some(arms) = arms.to_str() else {
        early_exit("OPENSIP_X9_ARMS is not UTF-8");
    };
    let arms = parse_arms(arms).unwrap_or_else(|reason| early_exit(&reason));
    Some(Active {
        arms,
        occurrences: Mutex::new(HashMap::new()),
        sequence: Mutex::new(0),
        control: Mutex::new(Control::default()),
        resumed: Condvar::new(),
        signal_input: Mutex::new(None),
    })
}

// Before the state exists: one record numbered 0, then exit.
fn early_exit(reason: &str) -> ! {
    let mut line = format!("X9|{}|0|0|-|harness-error|", std::process::id());
    line.extend(
        reason
            .chars()
            .filter(|c| *c != '\n' && *c != '\r')
            .take(256),
    );
    line.push('\n');
    let _ = io::stderr().write(line.as_bytes());
    std::process::exit(HARNESS_EXIT_CODE)
}

impl Active {
    fn record(&self, point: &str, event: &str, payload: &str) {
        let mut sequence = lock(&self.sequence);
        *sequence += 1;
        let mut line = format!(
            "X9|{}|{}|{}|{point}|{event}|{payload}\n",
            std::process::id(),
            thread_index(),
            *sequence
        );
        let fatal = line.len() > RECORD_LIMIT || payload.contains(['\n', '\r']);
        if fatal {
            line = format!(
                "X9|{}|{}|{}|-|harness-error|record over {RECORD_LIMIT} bytes or multiline at {point}\n",
                std::process::id(),
                thread_index(),
                *sequence
            );
        }
        let written = matches!(io::stderr().write(line.as_bytes()), Ok(n) if n == line.len());
        drop(sequence);
        if fatal || !written {
            std::process::exit(HARNESS_EXIT_CODE);
        }
    }

    fn harness_exit(&self, reason: &str) -> ! {
        let reason: String = reason
            .chars()
            .filter(|c| *c != '\n' && *c != '\r')
            .take(256)
            .collect();
        self.record("-", "harness-error", &reason);
        std::process::exit(HARNESS_EXIT_CODE)
    }

    fn next_occurrence(&self, name: &str) -> u32 {
        let mut occurrences = lock(&self.occurrences);
        let count = occurrences.entry(name.to_owned()).or_insert(0);
        *count += 1;
        *count
    }

    fn armed(&self, name: &str, occurrence: u32) -> Option<&Action> {
        self.arms
            .iter()
            .find(|arm| {
                arm.point == name
                    && match arm.occurrence {
                        Occurrence::Every => true,
                        Occurrence::Nth(k) => k == occurrence,
                    }
            })
            .map(|arm| &arm.action)
    }

    // One reached point: `pass`, a completed `hold`, or an admitted action
    // for the caller to perform (whose event it records here).
    fn reach(&self, name: &str, kind: Kind, phase: Option<Phase>) -> Reached {
        let occurrence = self.next_occurrence(name);
        let key = format!("{name}#{occurrence}");
        let Some(action) = self.armed(name, occurrence) else {
            self.record(&key, "pass", "");
            return Reached::Passed;
        };
        if !admitted(kind, phase, action) {
            self.harness_exit(&format!("{action:?} is not admitted at {key} ({kind:?})"));
        }
        match action {
            Action::Hold => {
                self.hold(&key, "");
                Reached::Resumed
            }
            Action::FailBefore => {
                self.record(&key, "fail-before", "");
                Reached::Act(key)
            }
            Action::FailAfter => {
                self.record(&key, "fail-after", "");
                Reached::Act(key)
            }
            // The caller writes the half, then holds; or records the id.
            Action::Torn | Action::InjectId(_) => Reached::Act(key),
        }
    }

    // Write `held`, then block until a resume names this point. Exactly one
    // held thread at a time reads stdin; it hands each line to its target.
    fn hold(&self, key: &str, payload: &str) {
        // Registered before `held` is written, so a resume the parent sends
        // on reading it always finds this point, whichever thread reads it.
        lock(&self.control).held.insert(key.to_owned(), false);
        self.record(key, "held", payload);
        let mut control = lock(&self.control);
        loop {
            if control.held.get(key) == Some(&true) {
                control.held.remove(key);
                break;
            }
            if control.closed {
                drop(control);
                self.harness_exit(&format!("stdin closed while {key} was held"));
            }
            if control.reader {
                control = self
                    .resumed
                    .wait(control)
                    .unwrap_or_else(PoisonError::into_inner);
                continue;
            }
            control.reader = true;
            drop(control);
            let mut line = String::new();
            let read = io::stdin().lock().read_line(&mut line);
            control = lock(&self.control);
            control.reader = false;
            match read {
                Ok(0) => control.closed = true,
                Ok(_) => {
                    let text = line.strip_suffix('\n').unwrap_or(&line);
                    if let Some(name) = text.strip_prefix("signal ") {
                        let signal = match name {
                            "SIGINT" => SignalInput::Sigint,
                            "SIGTERM" => SignalInput::Sigterm,
                            "SIGHUP" => SignalInput::Sighup,
                            _ => {
                                drop(control);
                                self.harness_exit("unknown signal input name");
                            }
                        };
                        drop(control);
                        let sender = lock(&self.signal_input)
                            .clone()
                            .unwrap_or_else(|| self.harness_exit("signal input not registered"));
                        if sender.send(signal).is_err() {
                            self.harness_exit("signal input closed");
                        }
                        self.resumed.notify_all();
                        control = lock(&self.control);
                        continue;
                    }
                    let target = match line.strip_suffix('\n').unwrap_or(&line) {
                        "resume" => {
                            let mut waiting = control.held.iter().filter(|(_, resumed)| !**resumed);
                            match (waiting.next(), waiting.next()) {
                                (Some((point, _)), None) => Some(point.clone()),
                                _ => None,
                            }
                        }
                        text => text
                            .strip_prefix("resume ")
                            .filter(|point| control.held.get(*point) == Some(&false))
                            .map(str::to_owned),
                    };
                    let Some(target) = target else {
                        drop(control);
                        self.harness_exit(&format!("control line {line:?} names no held point"));
                    };
                    control.held.insert(target, true);
                }
                Err(_) => control.closed = true,
            }
            self.resumed.notify_all();
        }
        drop(control);
        self.record(key, "resumed", payload);
    }

    fn primitive_base(&self, step: &str, kind: Kind) -> String {
        if primitive_kind(step) != Some(kind) {
            self.harness_exit(&format!("primitive step {step:?} declared as {kind:?}"));
        }
        match current_scope() {
            Some(scope) => format!("{scope}/{step}"),
            None => self.harness_exit(&format!("durability primitive {step} outside any scope")),
        }
    }

    fn protocol_name(&self, scope: Option<&str>, step: &str) -> String {
        let scope = match scope {
            Some(name) => resolve_scope(name),
            None => current_scope().ok_or_else(|| "protocol point outside any scope".to_owned()),
        }
        .unwrap_or_else(|reason| self.harness_exit(&reason));
        let name = format!("{scope}.{step}");
        if let Err(reason) = validate_point(&name) {
            self.harness_exit(&reason);
        }
        name
    }
}

fn current_scope() -> Option<String> {
    SCOPE.with(|stack| stack.borrow().last().cloned())
}

// A registered scope, or one that extends a registered scope, is absolute;
// any other name is a relative segment under the thread's current scope.
fn resolve_scope(name: &str) -> Result<String, String> {
    if !segments_valid(name) {
        return Err(format!("invalid scope name {name:?}"));
    }
    if registered_prefix(name).is_some() {
        return Ok(name.to_owned());
    }
    match current_scope() {
        Some(current) => Ok(format!("{current}.{name}")),
        None => Err(format!("unregistered scope {name:?} outside any scope")),
    }
}

fn eio() -> io::Error {
    io::Error::from_raw_os_error(libc::EIO)
}

/// Leaves the scope `crash_scope!` entered when it is dropped.
pub struct ScopeGuard {
    entered: bool,
}
impl Drop for ScopeGuard {
    fn drop(&mut self) {
        if self.entered {
            SCOPE.with(|stack| stack.borrow_mut().pop());
        }
    }
}

/// `crash_scope!`'s entry: push the resolved scope on this thread's stack.
pub fn enter_scope(name: &str) -> ScopeGuard {
    let Some(active) = state() else {
        return ScopeGuard { entered: false };
    };
    let scope = resolve_scope(name).unwrap_or_else(|reason| active.harness_exit(&reason));
    SCOPE.with(|stack| stack.borrow_mut().push(scope));
    ScopeGuard { entered: true }
}

/// A platform primitive's `.before` and `.after` points around its effect.
/// `.after` is reached only when the effect succeeded. A fallible step's
/// injected failure is `EIO`, the native I/O error class of these steps.
pub fn primitive<T>(
    step: &'static str,
    kind: Kind,
    effect: impl FnOnce() -> io::Result<T>,
) -> io::Result<T> {
    let Some(active) = state() else {
        return effect();
    };
    let base = active.primitive_base(step, kind);
    if let Reached::Act(_) = active.reach(&format!("{base}.before"), kind, Some(Phase::Before)) {
        return Err(eio());
    }
    let value = effect()?;
    if let Reached::Act(_) = active.reach(&format!("{base}.after"), kind, Some(Phase::After)) {
        return Err(eio());
    }
    Ok(value)
}

/// A platform write's points. `torn` writes the first half of `bytes` with
/// the same effect, then holds; a resumed torn write returns `EIO`.
pub fn primitive_write<T>(
    step: &'static str,
    bytes: &[u8],
    effect: impl FnOnce(&[u8]) -> io::Result<T>,
) -> io::Result<T> {
    let Some(active) = state() else {
        return effect(bytes);
    };
    let base = active.primitive_base(step, Kind::Write);
    if let Reached::Act(key) =
        active.reach(&format!("{base}.before"), Kind::Write, Some(Phase::Before))
    {
        effect(&bytes[..bytes.len() / 2])?;
        active.hold(&key, "torn");
        return Err(eio());
    }
    let value = effect(bytes)?;
    active.reach(&format!("{base}.after"), Kind::Write, Some(Phase::After));
    Ok(value)
}

/// One protocol point `<scope>.<step>` of kind `step`.
pub fn point(scope: Option<&str>, step: &str) {
    let Some(active) = state() else {
        return;
    };
    let name = active.protocol_name(scope, step);
    active.reach(&name, Kind::Step, None);
}

/// A protocol site's fallible step: `<scope>.<step>.before` and `.after`
/// around `effect`; an injected failure becomes the site's own error.
pub fn fallible<T, E>(
    scope: Option<&str>,
    step: &str,
    effect: impl FnOnce() -> Result<T, E>,
    fault: impl FnOnce(Fault) -> E,
) -> Result<T, E> {
    let Some(active) = state() else {
        return effect();
    };
    let base = active.protocol_name(scope, step);
    if let Reached::Act(_) = active.reach(
        &format!("{base}.before"),
        Kind::Fallible,
        Some(Phase::Before),
    ) {
        return Err(fault(Fault::Before));
    }
    let value = effect()?;
    if let Reached::Act(_) =
        active.reach(&format!("{base}.after"), Kind::Fallible, Some(Phase::After))
    {
        return Err(fault(Fault::After));
    }
    Ok(value)
}

/// A gate point: true when an armed rendezvous replaced the timed wait.
pub fn gate(scope: Option<&str>, step: &str) -> bool {
    let Some(active) = state() else {
        return false;
    };
    let name = active.protocol_name(scope, step);
    matches!(active.reach(&name, Kind::Gate, None), Reached::Resumed)
}

/// The draw point. Unarmed, its `pass` record follows the draw and carries
/// `payload(&value)`; armed `inject-id`, the id replaces the draw.
pub fn draw<T>(
    scope: Option<&str>,
    step: &str,
    draw: impl FnOnce() -> T,
    inject: impl FnOnce(&str) -> T,
    payload: impl FnOnce(&T) -> String,
) -> T {
    let Some(active) = state() else {
        return draw();
    };
    let name = active.protocol_name(scope, step);
    if name != DRAW_POINT {
        active.harness_exit(&format!("draw point {name} is not {DRAW_POINT}"));
    }
    let occurrence = active.next_occurrence(&name);
    let key = format!("{name}#{occurrence}");
    match active.armed(&name, occurrence) {
        Some(Action::InjectId(id)) => {
            active.record(&key, "inject-id", id);
            inject(id)
        }
        Some(Action::Hold) => {
            active.hold(&key, "");
            let value = draw();
            active.record(&key, "pass", &payload(&value));
            value
        }
        Some(action) => active.harness_exit(&format!("{action:?} is not admitted at {key} (Draw)")),
        None => {
            let value = draw();
            active.record(&key, "pass", &payload(&value));
            value
        }
    }
}

/// Why an `inject-id` value was not reserved.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InjectedExecutionId {
    /// Not identity §2's `exec1_` and 32 lowercase hex.
    Grammar,
    /// Already reserved in this process. An injected id is never redrawn.
    Reserved,
}

/// Law M3-J1 r6 item 2 with X3d r9 S10.1 (unit J3a): the draw point's
/// `inject-id` value, reserved in this process's `ExecutionIdReservations`
/// exactly as a draw is, so that the session holds a `ReservedExecutionId`
/// on every path. An earlier run's id is not in this process's registry, so
/// F34's injected id still reaches the attempt row's trigger. Only the draw
/// point's `inject` closure calls it, and it exists only under this
/// test-only feature: a release build has no constructor from text.
pub fn reserve_injected_execution_id(
    id: &str,
) -> Result<crate::ReservedExecutionId, InjectedExecutionId> {
    let bytes = crate::parse_execution_id(id).ok_or(InjectedExecutionId::Grammar)?;
    if crate::ExecutionIdReservations::process()
        .reserved
        .insert(bytes)
    {
        Ok(crate::ReservedExecutionId {
            bytes,
            rendered: crate::render_id("exec1_", &bytes),
        })
    } else {
        Err(InjectedExecutionId::Reserved)
    }
}

/// Report a matrix child's returned outcome as an `outcome` record.
pub fn report_outcome(payload: &str) {
    if let Some(active) = state() {
        active.record("-", "outcome", payload);
    }
}

// ------------------------------------------------- the scripted wall clock

/// `OPENSIP_X9_CLOCK=<E>:<k>`, parsed once: E a whole Unix second (the run
/// set's `clockEpoch`), k the process's ordinal in its run.
static CLOCK: OnceLock<Option<(i64, u32)>> = OnceLock::new();
static CLOCK_READ: AtomicU64 = AtomicU64::new(0);

/// Parse a clock script: `<E>:<k>`, E a non-negative whole second, k an
/// ordinal, with no sign, space or leading zero.
pub fn parse_clock(text: &str) -> Result<(i64, u32), String> {
    let plain = |s: &str| {
        !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit()) && (s == "0" || !s.starts_with('0'))
    };
    let Some((epoch, ordinal)) = text.split_once(':') else {
        return Err(format!("clock script without an ordinal: {text:?}"));
    };
    if !plain(epoch) || !plain(ordinal) {
        return Err(format!("invalid clock script {text:?}"));
    }
    let epoch: i64 = epoch
        .parse()
        .map_err(|_| format!("invalid clock epoch {text:?}"))?;
    let ordinal: u32 = ordinal
        .parse()
        .map_err(|_| format!("invalid clock ordinal {text:?}"))?;
    epoch
        .checked_add(i64::from(ordinal) * CLOCK_READINGS as i64 + CLOCK_READINGS as i64)
        .ok_or_else(|| format!("clock script out of range {text:?}"))?;
    Ok((epoch, ordinal))
}

fn clock_script() -> Option<(i64, u32)> {
    *CLOCK.get_or_init(|| {
        let text = std::env::var_os(CLOCK_VAR)?;
        if std::env::var_os(CHILD_VAR).is_none() {
            early_exit("OPENSIP_X9_CLOCK outside a matrix child");
        }
        let Some(text) = text.to_str() else {
            early_exit("OPENSIP_X9_CLOCK is not UTF-8");
        };
        Some(parse_clock(text).unwrap_or_else(|reason| early_exit(&reason)))
    })
}

/// Law X9 r2 item 3: in a matrix child with `OPENSIP_X9_CLOCK=<E>:<k>`, the
/// n-th wall reading of the process (n from 0) is `E + 3600·k + n` seconds
/// with zero nanoseconds, in place of the OS's; `None` in any other
/// process, which reads the OS's. Only `observe_clock`'s wall reading calls
/// it; the monotonic readings and the boot identity stay native. A 3600th
/// reading is a harness error.
pub fn scripted_wall() -> Option<(i64, u32)> {
    let (epoch, ordinal) = clock_script()?;
    let n = CLOCK_READ.fetch_add(1, Ordering::SeqCst);
    if n >= CLOCK_READINGS {
        let reason = format!("wall reading {n} past the script of ordinal {ordinal}");
        match state() {
            Some(active) => active.harness_exit(&reason),
            None => early_exit(&reason),
        }
    }
    Some((
        epoch + i64::from(ordinal) * CLOCK_READINGS as i64 + n as i64,
        0,
    ))
}

/// In a matrix child, its driver name and input path; `None` in any other
/// process. It reads the arming first, so a malformed one stops the child.
pub fn child_role() -> Option<(String, PathBuf)> {
    let role = std::env::var(CHILD_VAR).ok()?;
    let active = state();
    match std::env::var_os(INPUT_VAR) {
        Some(input) => Some((role, PathBuf::from(input))),
        None => match active {
            Some(active) => active.harness_exit("matrix child without OPENSIP_X9_INPUT"),
            None => early_exit("matrix child without OPENSIP_X9_INPUT"),
        },
    }
}
