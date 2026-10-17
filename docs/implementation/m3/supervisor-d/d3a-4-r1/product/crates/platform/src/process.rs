// M3-D r5 items 1 to 8 (unit D1a, D1a plan r1): the only production spawner.
// It provides process launch, exit observation, group signalling, reaping
// and per-child scratch for already authorized operations (CH14:392), and
// holds no policy (CH14:285): no deadline, ceiling, ladder or outcome.
// Supervision is `components/supervisor.rs` (D3); construction from an
// admitted selection is `components/session_factory.rs` (D4), whose closure
// recheck is the only production path to a `VerifiedLaunch`.
//
// macOS only at D1a (LD-D1A-1). On every other target the same API exists
// and refuses with `PlatformUnsupported`; the Linux half (pidfd, pipe2,
// closefrom, the subreaper, /var/tmp) is D1a-L, landed on a Linux lane.
use std::ffi::{CString, OsStr};
use std::fmt;
use std::io;
use std::os::unix::ffi::OsStrExt;
use std::path::{Path, PathBuf};

// ------------------------------------------------------------------ launch specs

/// The closed launch classes (item 1). There is no `RepositoryCode` class at
/// M3 (F-6). `TestFixture` exists only in test builds and runs first-party
/// test binaries, never repository bytes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LaunchClass {
    /// A TS2 or Rust3 provider: fds 0 to 4 (item 5).
    Provider,
    /// A first-party closure tool before PlanId: fds 0 to 2, fd0 at EOF.
    Tool,
    /// Tests only: this crate's own, or a dependent's dev-dependency
    /// through the `test-fixture` feature (D3a-0, LD-D3A-9), which
    /// `lib.rs` refuses in any build without debug assertions.
    #[cfg(any(test, feature = "test-fixture"))]
    TestFixture,
}

/// Which descriptor set a child receives (item 5).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DescriptorSet {
    /// 0 data in, 1 data out, 2 stderr, 3 control in, 4 control out.
    Provider,
    /// 0 at EOF, 1 output, 2 stderr.
    Tool,
}
impl DescriptorSet {
    pub fn count(self) -> usize {
        match self {
            Self::Provider => 5,
            Self::Tool => 3,
        }
    }
}

/// Why a spec is refused at construction (items 2 and 3).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SpecError {
    /// The executable, or another path argument, is not absolute.
    RelativePath(String),
    /// A path, argv element, key or value holds a NUL byte.
    Nul,
    /// `argv[0]` is not the executable's absolute path.
    ArgvZero,
    /// An argv element beyond the class's exact shape.
    ExtraArgument,
    EmptyKey,
    /// A key containing `=`.
    KeyEquals(String),
    DuplicateKey(String),
    /// A key outside the class's closed allowlist.
    KeyNotAllowed(String),
    /// A key D1 always refuses (item 3: PATH, CARGO_*, RUSTFLAGS, ...).
    KeyDenied(String),
}
impl fmt::Display for SpecError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

/// The keys D1 refuses for any class, whatever an allowlist says
/// (item 3; NE:1734-1736).
fn denied(key: &str) -> bool {
    matches!(key, "PATH" | "RUSTFLAGS" | "CC" | "CXX" | "LD" | "AR")
        || ["CARGO_", "RUSTC", "RUSTDOC", "RUSTUP_", "TARGET_"]
            .iter()
            .any(|prefix| key.starts_with(prefix))
}

/// A child environment built from empty (item 3). The host reads no
/// environment variable to build it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChildEnvironment {
    /// `KEY=VALUE`, in the class's fixed order.
    entries: Vec<(String, String)>,
}
impl ChildEnvironment {
    /// TS2: exactly `LC_ALL=C`, `LANG=C`, `TZ=UTC`, `UV_THREADPOOL_SIZE=4` and
    /// `OPENSIP_BROKER_CONTEXT` (BBC:119-131).
    pub fn typescript(broker_context: &str) -> Result<Self, SpecError> {
        Self::checked(
            &[
                ("LC_ALL", "C"),
                ("LANG", "C"),
                ("TZ", "UTC"),
                ("UV_THREADPOOL_SIZE", "4"),
                ("OPENSIP_BROKER_CONTEXT", broker_context),
            ],
            &[
                "LC_ALL",
                "LANG",
                "TZ",
                "UV_THREADPOOL_SIZE",
                "OPENSIP_BROKER_CONTEXT",
            ],
        )
    }
    /// Rust3: exactly `LANG=C`, `LC_ALL=C`, `TZ=UTC` (DRJ2:102-108).
    pub fn rust() -> Self {
        Self {
            entries: [("LANG", "C"), ("LC_ALL", "C"), ("TZ", "UTC")]
                .iter()
                .map(|(k, v)| ((*k).to_owned(), (*v).to_owned()))
                .collect(),
        }
    }
    /// A tool: only the keys C3b's adapter law names (NE:1728-1741). That
    /// allowlist is C3b's; until it lands it is empty, so only the empty
    /// environment is admitted.
    pub fn tool(entries: &[(&str, &str)]) -> Result<Self, SpecError> {
        Self::checked(entries, TOOL_ALLOWLIST)
    }
    #[cfg(test)]
    pub(crate) fn fixture(entries: &[(&str, &str)]) -> Result<Self, SpecError> {
        let keys: Vec<&str> = entries.iter().map(|(k, _)| *k).collect();
        Self::checked(entries, &keys)
    }
    fn checked(entries: &[(&str, &str)], allowed: &[&str]) -> Result<Self, SpecError> {
        let mut out: Vec<(String, String)> = Vec::new();
        for (key, value) in entries {
            if key.is_empty() {
                return Err(SpecError::EmptyKey);
            }
            if key.contains('\0') || value.contains('\0') {
                return Err(SpecError::Nul);
            }
            if key.contains('=') {
                return Err(SpecError::KeyEquals((*key).to_owned()));
            }
            if denied(key) {
                return Err(SpecError::KeyDenied((*key).to_owned()));
            }
            if !allowed.contains(key) {
                return Err(SpecError::KeyNotAllowed((*key).to_owned()));
            }
            if out.iter().any(|(k, _)| k == key) {
                return Err(SpecError::DuplicateKey((*key).to_owned()));
            }
            out.push(((*key).to_owned(), (*value).to_owned()));
        }
        Ok(Self { entries: out })
    }
    pub fn entries(&self) -> &[(String, String)] {
        &self.entries
    }
}

/// C3b's tool environment allowlist: empty until C3b names its keys.
const TOOL_ALLOWLIST: &[&str] = &[];

/// One argument of a spec: a fixed value, or the child's scratch path,
/// which exists only at spawn (Rust3's `--scratch-root`, DRJ2:94).
#[derive(Debug, Clone, PartialEq, Eq)]
enum Arg {
    Fixed(CString),
    Scratch,
}

/// A validated launch (items 1 to 3): absolute executable, exact argv,
/// environment from empty, and the class's descriptor set.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaunchSpec {
    class: LaunchClass,
    descriptors: DescriptorSet,
    executable: PathBuf,
    argv: Vec<Arg>,
    environment: ChildEnvironment,
}

fn absolute(path: &Path) -> Result<CString, SpecError> {
    if !path.is_absolute() {
        return Err(SpecError::RelativePath(path.display().to_string()));
    }
    c_bytes(path.as_os_str())
}
fn c_bytes(value: &OsStr) -> Result<CString, SpecError> {
    CString::new(value.as_bytes()).map_err(|_| SpecError::Nul)
}
fn c_text(value: &str) -> Result<CString, SpecError> {
    CString::new(value.as_bytes()).map_err(|_| SpecError::Nul)
}

impl LaunchSpec {
    /// TS2 (BBC:102-107): `[absBundledNode, --no-addons,
    /// --no-global-search-paths, --openssl-config=absVerifiedEmptyConfig,
    /// absBundledProviderEntry]`.
    pub fn typescript(
        node: &Path,
        openssl_config: &Path,
        entry: &Path,
        broker_context: &str,
    ) -> Result<Self, SpecError> {
        // D1a plan r2 (RF-3): the environment is BBC's, built here; no caller
        // can supply another.
        let environment = ChildEnvironment::typescript(broker_context)?;
        let mut config = b"--openssl-config=".to_vec();
        config.extend_from_slice(absolute(openssl_config)?.as_bytes());
        let config = CString::new(config).map_err(|_| SpecError::Nul)?;
        Ok(Self {
            class: LaunchClass::Provider,
            descriptors: DescriptorSet::Provider,
            executable: node.to_path_buf(),
            argv: vec![
                Arg::Fixed(absolute(node)?),
                Arg::Fixed(c_text("--no-addons")?),
                Arg::Fixed(c_text("--no-global-search-paths")?),
                Arg::Fixed(config),
                Arg::Fixed(absolute(entry)?),
            ],
            environment,
        })
    }
    /// Rust3 (DRJ2:92-96): exactly six ordered elements, the scratch root
    /// being the child's own fresh scratch.
    pub fn rust(provider: &Path, toolchain_root: &Path) -> Result<Self, SpecError> {
        Ok(Self {
            class: LaunchClass::Provider,
            descriptors: DescriptorSet::Provider,
            executable: provider.to_path_buf(),
            argv: vec![
                Arg::Fixed(absolute(provider)?),
                Arg::Fixed(c_text("--protocol-stdio-v2")?),
                Arg::Fixed(c_text("--toolchain-root")?),
                Arg::Fixed(absolute(toolchain_root)?),
                Arg::Fixed(c_text("--scratch-root")?),
                Arg::Scratch,
            ],
            environment: ChildEnvironment::rust(),
        })
    }
    /// A tool (item 2): its exact argv is C3b's, under MC item 12, with
    /// `argv[0]` the executable's absolute path. Crate-internal until C3b's
    /// adapter law supplies the argv and the environment allowlist (D1a plan
    /// r2, RF-3).
    #[allow(dead_code)]
    pub(crate) fn tool(
        executable: &Path,
        argv: &[&OsStr],
        environment: ChildEnvironment,
    ) -> Result<Self, SpecError> {
        Self::exact(
            LaunchClass::Tool,
            DescriptorSet::Tool,
            executable,
            argv,
            environment,
        )
    }
    /// A first-party test binary with an exact argv (item 1), for tests
    /// only: the one item the `test-fixture` feature exposes (D3a-0).
    #[cfg(any(test, feature = "test-fixture"))]
    pub fn fixture(
        descriptors: DescriptorSet,
        executable: &Path,
        argv: &[&OsStr],
        environment: ChildEnvironment,
    ) -> Result<Self, SpecError> {
        Self::exact(
            LaunchClass::TestFixture,
            descriptors,
            executable,
            argv,
            environment,
        )
    }
    fn exact(
        class: LaunchClass,
        descriptors: DescriptorSet,
        executable: &Path,
        argv: &[&OsStr],
        environment: ChildEnvironment,
    ) -> Result<Self, SpecError> {
        let exe = absolute(executable)?;
        let first = argv.first().ok_or(SpecError::ArgvZero)?;
        if c_bytes(first)? != exe {
            return Err(SpecError::ArgvZero);
        }
        let mut args = Vec::with_capacity(argv.len());
        for a in argv {
            args.push(Arg::Fixed(c_bytes(a)?));
        }
        Ok(Self {
            class,
            descriptors,
            executable: executable.to_path_buf(),
            argv: args,
            environment,
        })
    }
    pub fn class(&self) -> LaunchClass {
        self.class
    }
    pub fn descriptors(&self) -> DescriptorSet {
        self.descriptors
    }
    pub fn executable(&self) -> &Path {
        &self.executable
    }
    pub fn environment(&self) -> &ChildEnvironment {
        &self.environment
    }
    /// The argv with `scratch` in place of the scratch argument.
    pub(crate) fn resolved_argv(&self, scratch: &Path) -> Result<Vec<CString>, SpecError> {
        self.argv
            .iter()
            .map(|a| match a {
                Arg::Fixed(c) => Ok(c.clone()),
                Arg::Scratch => absolute(scratch),
            })
            .collect()
    }
}

/// What the closure owner's recheck observed immediately before the launch
/// (item 2; CPC:251): the member, its descriptor identity and its digest.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClosureRecheck {
    pub member: String,
    pub device: u64,
    pub inode: u64,
    pub sha256: String,
}

/// The only value the spawner accepts. D4's session factory is its only
/// production constructor (LD-D1A-3, pinned by D5-S1's structural check);
/// D1 performs no digest check of its own.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VerifiedLaunch {
    spec: LaunchSpec,
    recheck: ClosureRecheck,
}
impl VerifiedLaunch {
    pub fn from_recheck(spec: LaunchSpec, recheck: ClosureRecheck) -> Self {
        Self { spec, recheck }
    }
    pub fn spec(&self) -> &LaunchSpec {
        &self.spec
    }
    pub fn recheck(&self) -> &ClosureRecheck {
        &self.recheck
    }
}

// ------------------------------------------------------------------ errors

#[derive(Debug)]
pub enum LaunchError {
    /// D1a implements this host's macOS family only (LD-D1A-1).
    PlatformUnsupported,
    Spec(SpecError),
    /// A system call failed; the call is named.
    Io {
        call: &'static str,
        error: io::Error,
    },
    /// The scratch root or a child scratch is not a private directory.
    ScratchCustody(&'static str),
    /// `killpg` after the root was reaped (the reap-last rule, item 4).
    GroupAfterReap,
    AlreadyReaped,
    /// A setup step failed after the spawn, and killing and reaping the
    /// child then failed too; both errors are kept.
    SetupAbandoned {
        setup: Box<LaunchError>,
        reap: io::Error,
    },
}
impl fmt::Display for LaunchError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

/// How a child ended, from the exit source or the reap (`wait4`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ExitStatus {
    /// The raw wait status.
    pub raw: i32,
}
impl ExitStatus {
    pub fn code(self) -> Option<i32> {
        let s = self.raw;
        ((s & 0x7f) == 0).then_some((s >> 8) & 0xff)
    }
    pub fn signal(self) -> Option<i32> {
        let s = self.raw;
        let sig = s & 0x7f;
        (sig != 0 && sig != 0x7f).then_some(sig)
    }
}

/// The POSIX.1-2017 signals whose default action terminates a process (T or
/// A), less `SIGPOLL`, by this target's pinned `libc` constants (S-OP-2c item
/// 23a's `ChildSignal`; unit D3a-4). A raw termination-signal number maps to
/// a member only by equality with that member's constant; there is no number
/// table here. Mechanism only: which signals a record names is S-OP-2c's.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TerminatingSignal {
    Abrt,
    Alrm,
    Bus,
    Fpe,
    Hup,
    Ill,
    Int,
    Kill,
    Pipe,
    Prof,
    Quit,
    Segv,
    Sys,
    Term,
    Trap,
    Usr1,
    Usr2,
    Vtalrm,
    Xcpu,
    Xfsz,
}
impl TerminatingSignal {
    /// The member whose constant equals `raw` on this target, if any.
    #[cfg(any(target_os = "macos", target_os = "linux"))]
    pub fn of(raw: i32) -> Option<Self> {
        [
            (libc::SIGABRT, Self::Abrt),
            (libc::SIGALRM, Self::Alrm),
            (libc::SIGBUS, Self::Bus),
            (libc::SIGFPE, Self::Fpe),
            (libc::SIGHUP, Self::Hup),
            (libc::SIGILL, Self::Ill),
            (libc::SIGINT, Self::Int),
            (libc::SIGKILL, Self::Kill),
            (libc::SIGPIPE, Self::Pipe),
            (libc::SIGPROF, Self::Prof),
            (libc::SIGQUIT, Self::Quit),
            (libc::SIGSEGV, Self::Segv),
            (libc::SIGSYS, Self::Sys),
            (libc::SIGTERM, Self::Term),
            (libc::SIGTRAP, Self::Trap),
            (libc::SIGUSR1, Self::Usr1),
            (libc::SIGUSR2, Self::Usr2),
            (libc::SIGVTALRM, Self::Vtalrm),
            (libc::SIGXCPU, Self::Xcpu),
            (libc::SIGXFSZ, Self::Xfsz),
        ]
        .into_iter()
        .find(|(number, _)| *number == raw)
        .map(|(_, member)| member)
    }
    /// No pinned constants on an unsupported target: nothing maps.
    #[cfg(not(any(target_os = "macos", target_os = "linux")))]
    pub fn of(_raw: i32) -> Option<Self> {
        None
    }
}

/// What `wait4` returns at the final reap: the status and the rusage
/// fields S-OP-2's `provider.process.reaped` records (SOP2:910).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Reaped {
    pub status: ExitStatus,
    pub user_micros: u64,
    pub system_micros: u64,
    pub max_resident_bytes: u64,
}

/// One descriptor of a readiness wait (unit D3a-1; item 12's "one readiness
/// loop per child", :449): what the caller waits for, and what `wait_ready`
/// observed. Mechanism only: which descriptors, and what readiness means
/// for each, are the supervisor's.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Readiness {
    pub fd: std::os::fd::RawFd,
    pub read: bool,
    pub write: bool,
    /// Set by `wait_ready`: readable, or at end of file, hang-up or error,
    /// so that the next read reports which.
    pub readable: bool,
    /// Set by `wait_ready`: writable, or the reader is gone, so that the
    /// next write reports which.
    pub writable: bool,
}
impl Readiness {
    pub fn new(fd: std::os::fd::RawFd, read: bool, write: bool) -> Self {
        Self {
            fd,
            read,
            write,
            readable: false,
            writable: false,
        }
    }
}

#[cfg(target_os = "macos")]
pub use macos::{
    Child, ChildScratch, ScratchRoot, Unreaped, group_members, resident_bytes, spawn, wait_ready,
};
#[cfg(all(test, target_os = "macos"))]
pub(crate) use macos::{
    FAIL_EXIT_SOURCE, FAIL_REAP, FORCE_NP, INJECT_EINTR, LAST_CHDIR, POLL_EINTR, SCRATCH_HOOK,
    SYSCALLS, ScratchPoint, WALK_LOG, WalkCall, scratch_cost,
};

#[cfg(not(target_os = "macos"))]
pub use unsupported::{
    Child, ChildScratch, ScratchRoot, Unreaped, group_members, resident_bytes, spawn, wait_ready,
};

// ------------------------------------------------------------------ macOS

#[cfg(target_os = "macos")]
mod macos {
    use super::{DescriptorSet, ExitStatus, LaunchError, Readiness, Reaped, VerifiedLaunch};
    use crate::{WorkCost, WorkFailure, WorkScope};
    use std::ffi::{CStr, CString};
    use std::fs::File;
    use std::io;
    use std::os::fd::{AsRawFd, FromRawFd, IntoRawFd, OwnedFd, RawFd};
    use std::os::unix::ffi::OsStrExt;
    use std::path::{Path, PathBuf};
    use std::sync::{Arc, Once};
    use std::time::Duration;

    // SDK 27 declarations the pinned libc 0.2.189 lacks (LD-D1A-2).
    /// `usr/include/sys/spawn.h:61`.
    const POSIX_SPAWN_SETSID: libc::c_short = 0x0400;
    /// `usr/include/sys/fcntl.h:293`.
    const F_SETNOSIGPIPE: libc::c_int = 73;
    /// `usr/include/sys/proc_info.h:52`.
    const PROC_PGRP_ONLY: u32 = 2;

    #[cfg(test)]
    thread_local! {
        /// The fallback control (D1a plan r2, RF-1): skip the macOS 26 symbol.
        pub(crate) static FORCE_NP: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
        /// The setup-failure control (D1a r1 RF-4): fail `exit_source` after
        /// the given delay.
        pub(crate) static FAIL_EXIT_SOURCE: std::cell::Cell<Option<Duration>> = const { std::cell::Cell::new(None) };
        /// The interrupted-reap control (D1a r1 RF-3): this many `waitpid`
        /// calls report `EINTR` before the real one.
        pub(crate) static INJECT_EINTR: std::cell::Cell<u32> = const { std::cell::Cell::new(0) };
        /// The fallback control's witness: which symbol the last spawn used.
        pub(crate) static LAST_CHDIR: std::cell::Cell<&'static str> = const { std::cell::Cell::new("") };
        /// The abandoned-setup control (D1a r3 RF-1): `kill_and_reap`
        /// reaps for real, then reports failure.
        pub(crate) static FAIL_REAP: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
        /// The contested-sweep and creation controls (D1a r2 NBO-2): run at
        /// a sweep's or a creation's named point on this thread.
        pub(crate) static SCRATCH_HOOK: std::cell::RefCell<ScratchHook> =
            const { std::cell::RefCell::new(None) };
        /// The signal and reap calls this thread made on a child, in order
        /// (D3a-0: an abandoned root's `Drop` makes none).
        pub(crate) static SYSCALLS: std::cell::RefCell<Vec<&'static str>> =
            const { std::cell::RefCell::new(Vec::new()) };
        /// The readiness wait's interrupted-call control (unit D3a-1 r2): every
        /// `poll` on this thread reports `EINTR`.
        pub(crate) static POLL_EINTR: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
        /// The bounded scratch walks' calls on this thread, recorded where
        /// each is made, so a test prices them independently of the charges
        /// (D3a-0).
        pub(crate) static WALK_LOG: std::cell::RefCell<Vec<WalkCall>> =
            const { std::cell::RefCell::new(Vec::new()) };
    }
    #[cfg(test)]
    fn record(call: &'static str) {
        SYSCALLS.with_borrow_mut(|c| c.push(call));
    }
    #[cfg(test)]
    fn walk_log(call: WalkCall) {
        WALK_LOG.with_borrow_mut(|c| c.push(call));
    }
    /// One call of a bounded scratch walk, as `WALK_LOG` records it.
    #[cfg(test)]
    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub(crate) enum WalkCall {
        /// A `readdir`, or a `rewinddir` before another removal pass.
        Read,
        /// An entry's no-follow `fstatat`.
        Status,
        /// A directory entered, with its name's length (0 for the root).
        Descend(usize),
        /// An `unlinkat` of an entry or an emptied directory.
        Unlink,
        /// The child scratch's own `unlinkat`, with its leaf's length.
        Leaf(usize),
        /// A descent's directory descriptor made (the root's duplicate or an
        /// entry's open), recorded once it exists; its charge is the
        /// `Descend` that must precede it.
        Open,
    }
    /// The work each recorded walk call is charged.
    #[cfg(test)]
    pub(crate) fn scratch_cost(call: WalkCall) -> WorkCost {
        match call {
            WalkCall::Read => READ_COST,
            WalkCall::Status => STATUS_COST,
            WalkCall::Descend(name) => descend_cost(name),
            WalkCall::Unlink => UNLINK_COST,
            WalkCall::Leaf(leaf) => leaf_cost(leaf),
            WalkCall::Open => WorkCost::default(),
        }
    }
    /// A test thread's `SCRATCH_HOOK`.
    #[cfg(test)]
    pub(crate) type ScratchHook = Option<Box<dyn FnMut(ScratchPoint)>>;
    /// Where `SCRATCH_HOOK` runs.
    #[cfg(test)]
    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub(crate) enum ScratchPoint {
        /// A creation has its staged root and holds its lock, unpublished.
        Staged,
        /// A sweep has opened a sibling's lock file, before trying it.
        LockOpened,
        /// A sweep holds a sibling's lock, before re-verifying it.
        LockTaken,
    }
    #[cfg(test)]
    fn scratch_hook(point: ScratchPoint) {
        SCRATCH_HOOK.with_borrow_mut(|h| {
            if let Some(h) = h {
                h(point);
            }
        });
    }

    type AddChdir = unsafe extern "C" fn(
        *mut libc::posix_spawn_file_actions_t,
        *const libc::c_char,
    ) -> libc::c_int;

    /// `posix_spawn_file_actions_addchdir` from macOS 26 (`spawn.h:72`), or
    /// the `_np` form before it (`spawn.h:184-185`), resolved at run time so
    /// the binary loads on either.
    fn add_chdir() -> Result<AddChdir, LaunchError> {
        for name in [
            c"posix_spawn_file_actions_addchdir",
            c"posix_spawn_file_actions_addchdir_np",
        ] {
            #[cfg(test)]
            if name == c"posix_spawn_file_actions_addchdir" && FORCE_NP.with(|f| f.get()) {
                continue;
            }
            // SAFETY: dlsym with the default handle and a NUL-terminated name.
            let symbol = unsafe { libc::dlsym(libc::RTLD_DEFAULT, name.as_ptr()) };
            if !symbol.is_null() {
                #[cfg(test)]
                LAST_CHDIR.with(|l| {
                    l.set(if name == c"posix_spawn_file_actions_addchdir" {
                        "addchdir"
                    } else {
                        "addchdir_np"
                    })
                });
                // SAFETY: both symbols have exactly this C signature.
                return Ok(unsafe { std::mem::transmute::<*mut libc::c_void, AddChdir>(symbol) });
            }
        }
        Err(LaunchError::Io {
            call: "dlsym(posix_spawn_file_actions_addchdir)",
            error: io::Error::new(io::ErrorKind::Unsupported, "no addchdir"),
        })
    }

    fn last(call: &'static str) -> LaunchError {
        LaunchError::Io {
            call,
            error: io::Error::last_os_error(),
        }
    }
    fn check(call: &'static str, rc: libc::c_int) -> Result<(), LaunchError> {
        if rc == -1 { Err(last(call)) } else { Ok(()) }
    }
    /// The posix_spawn family returns the error number instead of -1.
    fn check_spawn(call: &'static str, rc: libc::c_int) -> Result<(), LaunchError> {
        if rc == 0 {
            Ok(())
        } else {
            Err(LaunchError::Io {
                call,
                error: io::Error::from_raw_os_error(rc),
            })
        }
    }

    /// Item 7: before the first spawn the host lowers its own soft
    /// `RLIMIT_CORE` to 0, so every child inherits it.
    fn lower_core_limit() -> Result<(), LaunchError> {
        static ONCE: Once = Once::new();
        let mut result = Ok(());
        ONCE.call_once(|| {
            let mut limit = libc::rlimit {
                rlim_cur: 0,
                rlim_max: 0,
            };
            // SAFETY: valid out-pointer.
            if unsafe { libc::getrlimit(libc::RLIMIT_CORE, &mut limit) } == -1 {
                result = Err(last("getrlimit(RLIMIT_CORE)"));
                return;
            }
            limit.rlim_cur = 0;
            // SAFETY: valid pointer to an initialized rlimit.
            if unsafe { libc::setrlimit(libc::RLIMIT_CORE, &limit) } == -1 {
                result = Err(last("setrlimit(RLIMIT_CORE)"));
            }
        });
        result?;
        let mut now = libc::rlimit {
            rlim_cur: 1,
            rlim_max: 0,
        };
        // SAFETY: valid out-pointer.
        check("getrlimit(RLIMIT_CORE)", unsafe {
            libc::getrlimit(libc::RLIMIT_CORE, &mut now)
        })?;
        if now.rlim_cur != 0 {
            return Err(LaunchError::Io {
                call: "setrlimit(RLIMIT_CORE)",
                error: io::Error::other("soft RLIMIT_CORE is not 0"),
            });
        }
        Ok(())
    }

    fn set_flag(
        fd: RawFd,
        get: libc::c_int,
        set: libc::c_int,
        flag: libc::c_int,
    ) -> Result<(), LaunchError> {
        // SAFETY: fcntl on a descriptor this module owns.
        let current = unsafe { libc::fcntl(fd, get) };
        check("fcntl(get)", current)?;
        // SAFETY: as above.
        check("fcntl(set)", unsafe {
            libc::fcntl(fd, set, current | flag)
        })
    }

    /// A fresh pipe (item 5): both ends close-on-exec; the host end
    /// non-blocking, and `F_SETNOSIGPIPE` when the host writes. The child
    /// end is moved to a descriptor at or above 10, so no `dup2` source can
    /// collide with a target in 0 to 4.
    fn pipe(host_writes: bool) -> Result<(OwnedFd, OwnedFd), LaunchError> {
        let mut fds = [0 as RawFd; 2];
        // SAFETY: valid two-element out-array.
        check("pipe", unsafe { libc::pipe(fds.as_mut_ptr()) })?;
        // SAFETY: pipe returned two fresh descriptors this function now owns.
        let (read, write) = unsafe { (OwnedFd::from_raw_fd(fds[0]), OwnedFd::from_raw_fd(fds[1])) };
        for fd in [&read, &write] {
            set_flag(
                fd.as_raw_fd(),
                libc::F_GETFD,
                libc::F_SETFD,
                libc::FD_CLOEXEC,
            )?;
        }
        let (host, child) = if host_writes {
            (write, read)
        } else {
            (read, write)
        };
        set_flag(
            host.as_raw_fd(),
            libc::F_GETFL,
            libc::F_SETFL,
            libc::O_NONBLOCK,
        )?;
        if host_writes {
            // SAFETY: fcntl on the host's write end.
            check("fcntl(F_SETNOSIGPIPE)", unsafe {
                libc::fcntl(host.as_raw_fd(), F_SETNOSIGPIPE, 1)
            })?;
        }
        // SAFETY: duplicate the child end at or above 10, close-on-exec.
        let high = unsafe { libc::fcntl(child.as_raw_fd(), libc::F_DUPFD_CLOEXEC, 10) };
        check("fcntl(F_DUPFD_CLOEXEC)", high)?;
        // SAFETY: `high` is a fresh descriptor; `child` is dropped (closed).
        let child = unsafe { OwnedFd::from_raw_fd(high) };
        Ok((host, child))
    }

    fn file(fd: OwnedFd) -> File {
        // SAFETY: ownership of the descriptor moves into the File.
        unsafe { File::from_raw_fd(fd.into_raw_fd()) }
    }

    fn random_hex() -> Result<String, LaunchError> {
        let mut bytes = [0u8; 16];
        getrandom::fill(&mut bytes).map_err(|_| LaunchError::Io {
            call: "getrandom",
            error: io::Error::other("no randomness"),
        })?;
        Ok(bytes.iter().map(|b| format!("{b:02x}")).collect())
    }

    fn name(text: &str) -> Result<CString, LaunchError> {
        CString::new(text).map_err(|_| LaunchError::ScratchCustody("name"))
    }

    /// `mkdirat` mode 0700 under `parent`, then a no-follow open, verified
    /// to be a directory owned by this user with mode 0700.
    fn private_directory(parent: RawFd, leaf: &str) -> Result<OwnedFd, LaunchError> {
        let c = name(leaf)?;
        // SAFETY: valid descriptor and NUL-terminated name.
        check("mkdirat", unsafe {
            libc::mkdirat(parent, c.as_ptr(), 0o700)
        })?;
        // SAFETY: no-follow directory open of the entry just created.
        let fd = unsafe {
            libc::openat(
                parent,
                c.as_ptr(),
                libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            )
        };
        check("openat(directory)", fd)?;
        // SAFETY: fresh descriptor; the mode is set exactly, whatever the umask.
        let dir = unsafe { OwnedFd::from_raw_fd(fd) };
        check("fchmod", unsafe { libc::fchmod(dir.as_raw_fd(), 0o700) })?;
        drop(dir);
        open_directory(parent, &c)
    }
    fn open_directory(parent: RawFd, c: &CStr) -> Result<OwnedFd, LaunchError> {
        // SAFETY: valid descriptor and name; no-follow directory open.
        let fd = unsafe {
            libc::openat(
                parent,
                c.as_ptr(),
                libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            )
        };
        check("openat(directory)", fd)?;
        // SAFETY: fresh descriptor.
        let dir = unsafe { OwnedFd::from_raw_fd(fd) };
        let st = fstat(dir.as_raw_fd())?;
        // SAFETY: getuid has no failure mode.
        let uid = unsafe { libc::getuid() };
        if (st.st_mode & libc::S_IFMT) != libc::S_IFDIR
            || st.st_uid != uid
            || (st.st_mode & 0o7777) != 0o700
        {
            return Err(LaunchError::ScratchCustody("not a private 0700 directory"));
        }
        Ok(dir)
    }
    fn fstat(fd: RawFd) -> Result<libc::stat, LaunchError> {
        // SAFETY: zeroed stat is a valid out-buffer.
        let mut st: libc::stat = unsafe { std::mem::zeroed() };
        // SAFETY: valid descriptor and out-pointer.
        check("fstat", unsafe { libc::fstat(fd, &mut st) })?;
        Ok(st)
    }
    fn fd_path(fd: RawFd) -> Result<PathBuf, LaunchError> {
        let mut buf = vec![0u8; libc::PATH_MAX as usize];
        // SAFETY: F_GETPATH writes at most PATH_MAX bytes into `buf`.
        check("fcntl(F_GETPATH)", unsafe {
            libc::fcntl(fd, libc::F_GETPATH, buf.as_mut_ptr())
        })?;
        let end = buf.iter().position(|b| *b == 0).unwrap_or(buf.len());
        Ok(Path::new(std::ffi::OsStr::from_bytes(&buf[..end])).to_path_buf())
    }

    /// The published name prefix of a scratch root, and the staging prefix it
    /// is built under first (D1a r1 RF-2): a root is visible to a sweeper only
    /// once its lock file exists and is held.
    const ROOT_PREFIX: &[u8] = b"opensip-scratch-";
    /// A root under construction (D1a r1 RF-2), published by exclusive
    /// rename once its lock is held. A crash before publication leaves a
    /// staging directory that no child ever ran in. The sweep never matches
    /// it, since sweeping staging names would race a creator, so it stays
    /// until a separately coordinated cleanup exists (D1a r2 NBO-1).
    const STAGING_PREFIX: &str = ".opensip-scratch-staging-";

    /// What a scratch root holds for as long as any of its children lives
    /// (D1a r1 RF-1): its parent and its own descriptors, and the invocation's
    /// lock, held by `flock` until the last owner drops.
    #[derive(Debug)]
    struct RootState {
        parent: OwnedFd,
        root: OwnedFd,
        _lock: OwnedFd,
        leaf: String,
        path: PathBuf,
    }

    /// The scratch root (item 6): `opensip-scratch-<128-bit hex>`, 0700,
    /// under the per-user temporary root, with a lock file held by `flock`
    /// for the invocation's life. Each child's scratch is a fresh
    /// subdirectory, and keeps the root's state alive.
    #[derive(Debug)]
    pub struct ScratchRoot {
        state: Arc<RootState>,
        children: u64,
    }
    impl ScratchRoot {
        /// Production: under `confstr(_CS_DARWIN_USER_TEMP_DIR)`, read
        /// without the environment; `TMPDIR` is never consulted.
        pub fn create() -> Result<Self, LaunchError> {
            let mut buf = vec![0u8; libc::PATH_MAX as usize];
            // SAFETY: confstr writes at most `buf.len()` bytes.
            let n = unsafe {
                libc::confstr(
                    libc::_CS_DARWIN_USER_TEMP_DIR,
                    buf.as_mut_ptr().cast(),
                    buf.len(),
                )
            };
            if n == 0 || n > buf.len() {
                return Err(last("confstr(_CS_DARWIN_USER_TEMP_DIR)"));
            }
            let path = CString::new(&buf[..n - 1])
                .map_err(|_| LaunchError::ScratchCustody("temp root"))?;
            // SAFETY: absolute path, no-follow directory open.
            let fd = unsafe {
                libc::open(
                    path.as_ptr(),
                    libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
                )
            };
            check("open(temp root)", fd)?;
            // SAFETY: fresh descriptor.
            Self::create_in(unsafe { OwnedFd::from_raw_fd(fd) })
        }
        /// The test seam: an explicit parent directory descriptor. The root
        /// is built under a staging name, its lock created and held, and only
        /// then published under its final name with `RENAME_EXCL`, so a
        /// sweeper never sees an unlocked root (D1a r1 RF-2).
        pub fn create_in(parent: OwnedFd) -> Result<Self, LaunchError> {
            let hex = random_hex()?;
            let staging = format!("{STAGING_PREFIX}{hex}");
            let leaf = format!("opensip-scratch-{hex}");
            let root = private_directory(parent.as_raw_fd(), &staging)?;
            let lock_name = name("lock")?;
            // SAFETY: create-exclusive, no-follow, under the new root.
            let lock = unsafe {
                libc::openat(
                    root.as_raw_fd(),
                    lock_name.as_ptr(),
                    libc::O_RDWR
                        | libc::O_CREAT
                        | libc::O_EXCL
                        | libc::O_NOFOLLOW
                        | libc::O_CLOEXEC,
                    0o600,
                )
            };
            check("openat(lock)", lock)?;
            // SAFETY: fresh descriptor.
            let lock = unsafe { OwnedFd::from_raw_fd(lock) };
            // SAFETY: flock on the lock file just created.
            check("flock", unsafe {
                libc::flock(lock.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB)
            })?;
            #[cfg(test)]
            scratch_hook(ScratchPoint::Staged);
            let from = name(&staging)?;
            let to = name(&leaf)?;
            // SAFETY: both names are under the held parent; RENAME_EXCL never
            // replaces an existing entry.
            check("renameatx_np(RENAME_EXCL)", unsafe {
                libc::renameatx_np(
                    parent.as_raw_fd(),
                    from.as_ptr(),
                    parent.as_raw_fd(),
                    to.as_ptr(),
                    libc::RENAME_EXCL,
                )
            })?;
            let path = fd_path(root.as_raw_fd())?;
            Ok(Self {
                state: Arc::new(RootState {
                    parent,
                    root,
                    _lock: lock,
                    leaf,
                    path,
                }),
                children: 0,
            })
        }
        pub fn path(&self) -> &Path {
            &self.state.path
        }
        pub fn leaf(&self) -> &str {
            &self.state.leaf
        }
        /// A fresh, empty child scratch, created immediately before a spawn
        /// and never reused (item 6, r2). It keeps the root's state alive.
        fn child(&mut self) -> Result<ChildScratch, LaunchError> {
            self.children += 1;
            let leaf = format!("child-{}-{}", self.children, random_hex()?);
            let dir = private_directory(self.state.root.as_raw_fd(), &leaf)?;
            let path = fd_path(dir.as_raw_fd())?;
            Ok(ChildScratch {
                root: Arc::clone(&self.state),
                leaf,
                dir,
                path,
            })
        }
        /// The stale sweep (item 6; D1a r1 RF-2): a sibling `opensip-scratch-*`
        /// is removed only when this process opens its lock file and takes
        /// the lock without waiting, and the lock is held until the root is
        /// gone. A lock that cannot be opened, or is held, proves nothing and
        /// the sibling is kept. Returns the names removed.
        pub fn sweep(&self) -> Result<Vec<String>, LaunchError> {
            let mut removed = Vec::new();
            let parent = self.state.parent.as_raw_fd();
            for entry in list(parent)? {
                let bytes = entry.as_bytes();
                if !bytes.starts_with(ROOT_PREFIX) || bytes == self.state.leaf.as_bytes() {
                    continue;
                }
                let Ok(dir) = open_directory(parent, &entry) else {
                    continue;
                };
                let lock = name("lock")?;
                // SAFETY: no-follow open of the sibling's lock file.
                let fd = unsafe {
                    libc::openat(
                        dir.as_raw_fd(),
                        lock.as_ptr(),
                        libc::O_RDWR | libc::O_NOFOLLOW | libc::O_CLOEXEC,
                    )
                };
                if fd == -1 {
                    continue;
                }
                // SAFETY: fresh descriptor, held until the root is removed.
                let held = unsafe { OwnedFd::from_raw_fd(fd) };
                #[cfg(test)]
                scratch_hook(ScratchPoint::LockOpened);
                // SAFETY: non-blocking flock probe.
                if unsafe { libc::flock(held.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } == -1 {
                    continue;
                }
                #[cfg(test)]
                scratch_hook(ScratchPoint::LockTaken);
                // The lock proves death only if it is still this root's lock
                // and the root is still at its name: a concurrent sweeper
                // that won unlinks the lock before releasing it (D1a r1 RF-2).
                if !same_entry(dir.as_raw_fd(), &lock, held.as_raw_fd())
                    || !same_entry(parent, &entry, dir.as_raw_fd())
                {
                    continue;
                }
                remove_tree(dir.as_raw_fd())?;
                drop(dir);
                // SAFETY: remove the now-empty sibling directory itself.
                check("unlinkat(scratch root)", unsafe {
                    libc::unlinkat(parent, entry.as_ptr(), libc::AT_REMOVEDIR)
                })?;
                drop(held);
                removed.push(String::from_utf8_lossy(bytes).into_owned());
            }
            Ok(removed)
        }
    }

    /// A child's scratch: fresh, 0700, the child's cwd (item 6). It holds
    /// the root's state, so the root's descriptors and lock outlive it.
    #[derive(Debug)]
    pub struct ChildScratch {
        root: Arc<RootState>,
        leaf: String,
        dir: OwnedFd,
        path: PathBuf,
    }
    impl ChildScratch {
        pub fn path(&self) -> &Path {
            &self.path
        }
        pub fn inode(&self) -> Result<u64, LaunchError> {
            Ok(fstat(self.dir.as_raw_fd())?.st_ino)
        }
        /// The bounded measuring walk (D3a-0, LD-D3A-12; item 16): the sum
        /// of every non-directory entry's own size (`st_size`, a link's own
        /// length, never its target's). Each read, status read and descent
        /// is charged to `work` before it is made; no listing is collected
        /// whole; no link is followed. It stops as soon as the sum passes
        /// `byte_limit`: a result at most `byte_limit` is the exact total,
        /// and a greater one is where the walk stopped. The limit and what a
        /// breach means are D3's.
        pub fn measure(
            &self,
            byte_limit: u64,
            work: &mut WorkScope<'_>,
        ) -> Result<u64, WorkFailure<LaunchError>> {
            let mut stack = Vec::new();
            enter(&mut stack, || dup(self.dir.as_raw_fd()), None, work)?;
            let mut total = 0u64;
            let mut buf = [0u8; NAME_BYTES];
            while let Some(at) = stack.len().checked_sub(1) {
                let Some(len) = stack[at].next(&mut buf, work)? else {
                    stack.pop();
                    continue;
                };
                let dir = stack[at].dir.as_raw_fd();
                let entry = entry_name(&buf, len)?;
                let st = status(dir, entry, work)?;
                if (st.st_mode & libc::S_IFMT) == libc::S_IFDIR {
                    enter(&mut stack, || open_entry(dir, entry), Some(entry), work)?;
                } else {
                    total = total.saturating_add(st.st_size as u64);
                    if total > byte_limit {
                        return Ok(total);
                    }
                }
            }
            Ok(total)
        }
        /// The bounded removal walk (D3a-0, LD-D3A-12; item 20): everything
        /// below the scratch, then the scratch itself, under the no-follow
        /// discipline (a link is unlinked as a link, its target untouched:
        /// D1-T8). Each read, status read, descent and unlink is charged to
        /// `work` before it is made, and no listing is collected whole: a
        /// directory is read again after a pass that removed anything, until
        /// a pass finds it empty. Exhaustion is the ledger's `Budget`
        /// failure, with no errno; an I/O failure carries its call and
        /// errno. Either leaves the rest of the scratch in place. What each
        /// means is D3's (item 20; LD-D3A-17).
        pub fn remove_bounded(
            self,
            work: &mut WorkScope<'_>,
        ) -> Result<(), WorkFailure<LaunchError>> {
            let mut stack = Vec::new();
            enter(&mut stack, || dup(self.dir.as_raw_fd()), None, work)?;
            let mut buf = [0u8; NAME_BYTES];
            while let Some(at) = stack.len().checked_sub(1) {
                match stack[at].next(&mut buf, work)? {
                    Some(len) => {
                        let dir = stack[at].dir.as_raw_fd();
                        let entry = entry_name(&buf, len)?;
                        let st = status(dir, entry, work)?;
                        if (st.st_mode & libc::S_IFMT) == libc::S_IFDIR {
                            enter(&mut stack, || open_entry(dir, entry), Some(entry), work)?;
                        } else {
                            unlink(dir, entry, 0, work)?;
                            stack[at].changed = true;
                        }
                    }
                    None if stack[at].changed => stack[at].rewind(work)?,
                    None => {
                        let Some(done) = stack.pop() else { break };
                        let Some(parent) = stack.last_mut() else {
                            break;
                        };
                        let removed = done.name.as_deref().ok_or(WorkFailure::Operation(
                            LaunchError::ScratchCustody("an entered directory has no name"),
                        ))?;
                        unlink(parent.dir.as_raw_fd(), removed, libc::AT_REMOVEDIR, work)?;
                        parent.changed = true;
                    }
                }
            }
            work.charge::<LaunchError>(leaf_cost(self.leaf.len()))?;
            #[cfg(test)]
            walk_log(WalkCall::Leaf(self.leaf.len()));
            let c = name(&self.leaf).map_err(WorkFailure::Operation)?;
            // SAFETY: the root's descriptor is held by `self.root`.
            check("unlinkat(child scratch)", unsafe {
                libc::unlinkat(self.root.root.as_raw_fd(), c.as_ptr(), libc::AT_REMOVEDIR)
            })
            .map_err(WorkFailure::Operation)
        }
    }

    /// The longest name `readdir` returns, with its NUL (`d_name`'s size).
    const NAME_BYTES: usize = 1024;
    /// One `readdir`, or one `rewinddir` before another removal pass.
    const READ_COST: WorkCost = WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    };
    /// One entry's no-follow `fstatat`, on the name in the walk's stack
    /// buffer (no allocation).
    const STATUS_COST: WorkCost = WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    };
    /// One `unlinkat` of a listed name or an emptied directory.
    const UNLINK_COST: WorkCost = WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    };
    /// Entering a directory named with `name` bytes (0 for the walk's root):
    /// its name's NUL-terminated copy, the no-follow open (for the root, the
    /// duplicate of its held descriptor), the stream's duplicate and the
    /// stream (libSystem's opaque buffer counted as an object), and the
    /// stack's slot at its amortized growth (at most four slots per level).
    fn descend_cost(name: usize) -> WorkCost {
        WorkCost {
            objects: 3,
            edges: 3,
            bytes: name
                .saturating_add(1)
                .saturating_add(4 * std::mem::size_of::<Level>()),
        }
    }
    /// The child scratch's own removal: its leaf's NUL-terminated copy and
    /// the `unlinkat`.
    fn leaf_cost(leaf: usize) -> WorkCost {
        WorkCost {
            objects: 1,
            edges: 1,
            bytes: leaf.saturating_add(1),
        }
    }

    /// One open directory of a bounded walk: its descriptor, a stream over a
    /// duplicate of it, its name in its parent (none for the walk's root),
    /// and whether this removal pass changed it.
    struct Level {
        dir: OwnedFd,
        stream: *mut libc::DIR,
        name: Option<CString>,
        changed: bool,
    }
    impl Drop for Level {
        fn drop(&mut self) {
            // SAFETY: the stream was opened once and owns its duplicate.
            unsafe { libc::closedir(self.stream) };
        }
    }
    impl Level {
        /// The next name other than `.` and `..`, copied with its NUL into
        /// `buf`, its length returned; `None` at the end of this pass. Each
        /// `readdir` is charged first.
        fn next(
            &mut self,
            buf: &mut [u8; NAME_BYTES],
            work: &mut WorkScope<'_>,
        ) -> Result<Option<usize>, WorkFailure<LaunchError>> {
            loop {
                work.charge::<LaunchError>(READ_COST)?;
                #[cfg(test)]
                walk_log(WalkCall::Read);
                // SAFETY: libSystem returns this thread's errno cell.
                unsafe { *libc::__error() = 0 };
                // SAFETY: a live stream; readdir returns null at the end.
                let entry = unsafe { libc::readdir(self.stream) };
                if entry.is_null() {
                    // SAFETY: as above.
                    let errno = unsafe { *libc::__error() };
                    if errno != 0 {
                        return Err(WorkFailure::Operation(LaunchError::Io {
                            call: "readdir",
                            error: io::Error::from_raw_os_error(errno),
                        }));
                    }
                    return Ok(None);
                }
                // SAFETY: d_name is NUL-terminated within the entry.
                let n = unsafe { CStr::from_ptr((*entry).d_name.as_ptr()) };
                let bytes = n.to_bytes_with_nul();
                if bytes == b".\0" || bytes == b"..\0" {
                    continue;
                }
                buf[..bytes.len()].copy_from_slice(bytes);
                return Ok(Some(bytes.len() - 1));
            }
        }
        /// Read this directory again from its start (a removal pass),
        /// charged as a read.
        fn rewind(&mut self, work: &mut WorkScope<'_>) -> Result<(), WorkFailure<LaunchError>> {
            work.charge::<LaunchError>(READ_COST)?;
            #[cfg(test)]
            walk_log(WalkCall::Read);
            // SAFETY: a live stream.
            unsafe { libc::rewinddir(self.stream) };
            self.changed = false;
            Ok(())
        }
    }
    /// The name `Level::next` copied into `buf`.
    fn entry_name(buf: &[u8; NAME_BYTES], len: usize) -> Result<&CStr, WorkFailure<LaunchError>> {
        CStr::from_bytes_with_nul(&buf[..=len])
            .map_err(|_| WorkFailure::Operation(LaunchError::ScratchCustody("entry name")))
    }
    /// A close-on-exec duplicate of `fd`.
    fn dup(fd: RawFd) -> Result<OwnedFd, WorkFailure<LaunchError>> {
        // SAFETY: duplicate a descriptor this module holds.
        let dup = unsafe { libc::fcntl(fd, libc::F_DUPFD_CLOEXEC, 0) };
        check("fcntl(F_DUPFD_CLOEXEC)", dup).map_err(WorkFailure::Operation)?;
        // SAFETY: fresh descriptor.
        Ok(unsafe { OwnedFd::from_raw_fd(dup) })
    }
    /// Enter a directory, charged before anything of it is made (r2, Codex
    /// D3A0-R1-RF-1): the charge, then `open` (the root's duplicate or the
    /// entry's no-follow open), its name's copy, and a stream over its own
    /// duplicate, read from the start.
    fn enter(
        stack: &mut Vec<Level>,
        open: impl FnOnce() -> Result<OwnedFd, WorkFailure<LaunchError>>,
        name: Option<&CStr>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), WorkFailure<LaunchError>> {
        let len = name.map_or(0, |n| n.to_bytes().len());
        work.charge::<LaunchError>(descend_cost(len))?;
        #[cfg(test)]
        walk_log(WalkCall::Descend(len));
        let dir = open()?;
        #[cfg(test)]
        walk_log(WalkCall::Open);
        let name = name.map(CStr::to_owned);
        let scan = dup(dir.as_raw_fd())?;
        // SAFETY: rewind the duplicate's shared offset to the start.
        unsafe { libc::lseek(scan.as_raw_fd(), 0, libc::SEEK_SET) };
        let raw = scan.into_raw_fd();
        // SAFETY: fdopendir takes ownership of `raw` on success.
        let stream = unsafe { libc::fdopendir(raw) };
        if stream.is_null() {
            let error = last("fdopendir");
            // SAFETY: fdopendir failed, so `raw` is still ours to close.
            unsafe { libc::close(raw) };
            return Err(WorkFailure::Operation(error));
        }
        stack.push(Level {
            dir,
            stream,
            name,
            changed: false,
        });
        Ok(())
    }
    /// `entry`'s no-follow status, charged first.
    fn status(
        dir: RawFd,
        entry: &CStr,
        work: &mut WorkScope<'_>,
    ) -> Result<libc::stat, WorkFailure<LaunchError>> {
        work.charge::<LaunchError>(STATUS_COST)?;
        #[cfg(test)]
        walk_log(WalkCall::Status);
        // SAFETY: zeroed stat is a valid out-buffer.
        let mut st: libc::stat = unsafe { std::mem::zeroed() };
        // SAFETY: valid descriptor, name and out-pointer; never following.
        check("fstatat", unsafe {
            libc::fstatat(dir, entry.as_ptr(), &mut st, libc::AT_SYMLINK_NOFOLLOW)
        })
        .map_err(WorkFailure::Operation)?;
        Ok(st)
    }
    /// A no-follow directory open of `entry` (its charge is the descent's).
    fn open_entry(dir: RawFd, entry: &CStr) -> Result<OwnedFd, WorkFailure<LaunchError>> {
        // SAFETY: valid descriptor and name; a link is refused, not followed.
        let fd = unsafe {
            libc::openat(
                dir,
                entry.as_ptr(),
                libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            )
        };
        check("openat(scratch)", fd).map_err(WorkFailure::Operation)?;
        // SAFETY: fresh descriptor.
        Ok(unsafe { OwnedFd::from_raw_fd(fd) })
    }
    /// `unlinkat(dir, entry, flags)`, charged first; a link is unlinked as
    /// itself.
    fn unlink(
        dir: RawFd,
        entry: &CStr,
        flags: libc::c_int,
        work: &mut WorkScope<'_>,
    ) -> Result<(), WorkFailure<LaunchError>> {
        work.charge::<LaunchError>(UNLINK_COST)?;
        #[cfg(test)]
        walk_log(WalkCall::Unlink);
        // SAFETY: valid descriptor and name.
        check("unlinkat(scratch)", unsafe {
            libc::unlinkat(dir, entry.as_ptr(), flags)
        })
        .map_err(WorkFailure::Operation)
    }

    /// Whether `name` under `dir` is, without following a link, the very
    /// object `fd` holds (device and inode).
    fn same_entry(dir: RawFd, name: &CStr, fd: RawFd) -> bool {
        // SAFETY: zeroed stat is a valid out-buffer.
        let mut at: libc::stat = unsafe { std::mem::zeroed() };
        // SAFETY: valid descriptor, name and out-pointer.
        if unsafe { libc::fstatat(dir, name.as_ptr(), &mut at, libc::AT_SYMLINK_NOFOLLOW) } == -1 {
            return false;
        }
        match fstat(fd) {
            Ok(held) => held.st_dev == at.st_dev && held.st_ino == at.st_ino,
            Err(_) => false,
        }
    }

    /// The names in a directory, byte for byte, without `.` and `..`
    /// (D1a r1 NBO-2: never converted lossily).
    fn list(dir: RawFd) -> Result<Vec<CString>, LaunchError> {
        // SAFETY: duplicate so fdopendir/closedir own their own descriptor.
        let dup = unsafe { libc::fcntl(dir, libc::F_DUPFD_CLOEXEC, 0) };
        check("fcntl(F_DUPFD_CLOEXEC)", dup)?;
        // SAFETY: rewind the duplicate's shared offset to the start.
        unsafe { libc::lseek(dup, 0, libc::SEEK_SET) };
        // SAFETY: fdopendir takes ownership of `dup`.
        let stream = unsafe { libc::fdopendir(dup) };
        if stream.is_null() {
            // SAFETY: fdopendir failed, so `dup` is still ours to close.
            unsafe { libc::close(dup) };
            return Err(last("fdopendir"));
        }
        let mut names = Vec::new();
        loop {
            // SAFETY: valid stream; readdir returns null at the end.
            let entry = unsafe { libc::readdir(stream) };
            if entry.is_null() {
                break;
            }
            // SAFETY: d_name is NUL-terminated within the entry.
            let n = unsafe { CStr::from_ptr((*entry).d_name.as_ptr()) };
            let bytes = n.to_bytes();
            if bytes != b"." && bytes != b".." {
                names.push(n.to_owned());
            }
        }
        // SAFETY: closes the stream and its descriptor.
        unsafe { libc::closedir(stream) };
        Ok(names)
    }

    /// Remove everything below `dir`, never following a link: each entry is
    /// examined with `fstatat(AT_SYMLINK_NOFOLLOW)`, a directory is opened
    /// `O_NOFOLLOW` and emptied first, and everything else is unlinked as
    /// itself. Names are the exact bytes listed.
    fn remove_tree(dir: RawFd) -> Result<(), LaunchError> {
        for c in list(dir)? {
            // SAFETY: zeroed stat is a valid out-buffer.
            let mut st: libc::stat = unsafe { std::mem::zeroed() };
            // SAFETY: valid descriptor, name and out-pointer.
            check("fstatat", unsafe {
                libc::fstatat(dir, c.as_ptr(), &mut st, libc::AT_SYMLINK_NOFOLLOW)
            })?;
            if (st.st_mode & libc::S_IFMT) == libc::S_IFDIR {
                // SAFETY: no-follow directory open.
                let fd = unsafe {
                    libc::openat(
                        dir,
                        c.as_ptr(),
                        libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
                    )
                };
                check("openat(remove)", fd)?;
                // SAFETY: fresh descriptor.
                let child = unsafe { OwnedFd::from_raw_fd(fd) };
                remove_tree(child.as_raw_fd())?;
                drop(child);
                // SAFETY: valid descriptor and name.
                check("unlinkat(dir)", unsafe {
                    libc::unlinkat(dir, c.as_ptr(), libc::AT_REMOVEDIR)
                })?;
            } else {
                // SAFETY: valid descriptor and name; unlinks a link as a link.
                check("unlinkat", unsafe { libc::unlinkat(dir, c.as_ptr(), 0) })?;
            }
        }
        Ok(())
    }

    /// The exact-pid reap (D1a r1 RF-3): `waitpid(pid)` for this one child,
    /// retried on `EINTR`, never a wildcard. `Some` is the reaped status;
    /// `None` is `ECHILD` (nothing of ours to reap); any other error is
    /// returned, and nothing is assumed reaped.
    fn reap_exact(process_id: libc::pid_t) -> Result<Option<i32>, io::Error> {
        loop {
            #[cfg(test)]
            let injected = INJECT_EINTR.with(|c| {
                let n = c.get();
                c.set(n.saturating_sub(1));
                n > 0
            });
            #[cfg(not(test))]
            let injected = false;
            let mut status = 0;
            let (rc, error) = if injected {
                (-1, io::Error::from_raw_os_error(libc::EINTR))
            } else {
                #[cfg(test)]
                record("waitpid");
                // SAFETY: waitpid on exactly this child.
                let rc = unsafe { libc::waitpid(process_id, &mut status, 0) };
                (rc, io::Error::last_os_error())
            };
            if rc == process_id {
                return Ok(Some(status));
            }
            match error.raw_os_error() {
                Some(libc::EINTR) => continue,
                Some(libc::ECHILD) => return Ok(None),
                _ => return Err(error),
            }
        }
    }

    /// The primitive's own error cleanup after a successful `posix_spawn`
    /// (D1a r1 RF-4), and `Drop`'s last resort: the reserved group first,
    /// then the root itself, then the exact reap.
    fn kill_and_reap(process_id: libc::pid_t) -> Result<Option<i32>, io::Error> {
        #[cfg(test)]
        record("killpg+kill");
        // SAFETY: the root is unreaped, so its pid and group id are reserved.
        unsafe {
            libc::killpg(process_id, libc::SIGKILL);
            libc::kill(process_id, libc::SIGKILL);
        }
        let reaped = reap_exact(process_id);
        #[cfg(test)]
        if FAIL_REAP.with(|f| f.get()) {
            return reaped.and(Err(io::Error::other("injected reap failure")));
        }
        reaped
    }

    /// A spawned child (items 4 and 5): its pid (also its session and group
    /// id), the host ends of its descriptors, its exit source and scratch.
    #[derive(Debug)]
    pub struct Child {
        process_id: libc::pid_t,
        /// `kqueue` with `EVFILT_PROC` / `NOTE_EXIT | NOTE_EXITSTATUS`.
        exit_queue: OwnedFd,
        /// By slot; `None` once taken, and for a tool's closed fd0.
        host_ends: Vec<Option<File>>,
        scratch: Option<ChildScratch>,
        /// The child's own hold on its scratch root's state (the root's
        /// descriptors and the invocation lock), independent of the
        /// detachable scratch, until the child is reaped (D1a r2 RF-1).
        root_guard: Option<Arc<RootState>>,
        reaped: bool,
        /// Set by `abandon` alone: `Drop` then neither signals nor reaps.
        abandoned: bool,
    }

    /// Spawn one verified launch (items 1 to 7) under `root`.
    pub fn spawn(launch: VerifiedLaunch, root: &mut ScratchRoot) -> Result<Child, LaunchError> {
        let spec = launch.spec();
        lower_core_limit()?;
        let scratch = root.child()?;
        let argv = spec
            .resolved_argv(scratch.path())
            .map_err(LaunchError::Spec)?;
        let exe = CString::new(spec.executable().as_os_str().as_bytes())
            .map_err(|_| LaunchError::Spec(super::SpecError::Nul))?;
        let env: Vec<CString> = spec
            .environment()
            .entries()
            .iter()
            .map(|(k, v)| CString::new(format!("{k}={v}")))
            .collect::<Result<_, _>>()
            .map_err(|_| LaunchError::Spec(super::SpecError::Nul))?;

        // Item 5: fresh pipes; the host writes fd 0 and fd 3, reads 1, 2, 4.
        let count = spec.descriptors().count();
        let mut host_ends = Vec::with_capacity(count);
        let mut child_ends = Vec::with_capacity(count);
        for slot in 0..count {
            let host_writes = slot == 0 || slot == 3;
            let (host, child) = pipe(host_writes)?;
            // A tool's fd0 reads EOF at once: the host closes its write end.
            let closed = slot == 0 && spec.descriptors() == DescriptorSet::Tool;
            host_ends.push((!closed).then(|| file(host)));
            child_ends.push(child);
        }

        let add_chdir = add_chdir()?;
        let cwd = CString::new(scratch.path().as_os_str().as_bytes())
            .map_err(|_| LaunchError::ScratchCustody("scratch path"))?;
        let mut argv_ptrs: Vec<*mut libc::c_char> =
            argv.iter().map(|a| a.as_ptr().cast_mut()).collect();
        argv_ptrs.push(std::ptr::null_mut());
        let mut env_ptrs: Vec<*mut libc::c_char> =
            env.iter().map(|e| e.as_ptr().cast_mut()).collect();
        env_ptrs.push(std::ptr::null_mut());
        let mut attr = SpawnAttributes::new()?;
        let mut actions = FileActions::new()?;
        let flags = POSIX_SPAWN_SETSID
            | libc::POSIX_SPAWN_CLOEXEC_DEFAULT as libc::c_short
            | libc::POSIX_SPAWN_SETSIGDEF as libc::c_short
            | libc::POSIX_SPAWN_SETSIGMASK as libc::c_short;
        // SAFETY: initialized attribute object.
        check_spawn("posix_spawnattr_setflags", unsafe {
            libc::posix_spawnattr_setflags(&mut attr.0, flags)
        })?;
        // SAFETY: zeroed sigset_t values, filled and emptied before use.
        let (mut all, mut none): (libc::sigset_t, libc::sigset_t) =
            unsafe { (std::mem::zeroed(), std::mem::zeroed()) };
        // SAFETY: valid sigset pointers.
        unsafe {
            libc::sigfillset(&mut all);
            libc::sigemptyset(&mut none);
        }
        // SAFETY: initialized attribute object and sigsets.
        check_spawn("posix_spawnattr_setsigdefault", unsafe {
            libc::posix_spawnattr_setsigdefault(&mut attr.0, &all)
        })?;
        // SAFETY: as above.
        check_spawn("posix_spawnattr_setsigmask", unsafe {
            libc::posix_spawnattr_setsigmask(&mut attr.0, &none)
        })?;
        for (slot, child) in child_ends.iter().enumerate() {
            // SAFETY: initialized file actions; every source is at or above
            // 10, so no target in 0 to 4 is a later source.
            check_spawn("posix_spawn_file_actions_adddup2", unsafe {
                libc::posix_spawn_file_actions_adddup2(
                    &mut actions.0,
                    child.as_raw_fd(),
                    slot as libc::c_int,
                )
            })?;
        }
        // SAFETY: resolved addchdir with initialized actions and a C path.
        check_spawn("posix_spawn_file_actions_addchdir", unsafe {
            add_chdir(&mut actions.0, cwd.as_ptr())
        })?;
        let mut process_id: libc::pid_t = 0;
        // SAFETY: by path, never posix_spawnp, with initialized attributes
        // and actions and NUL-terminated argv and envp arrays.
        let result = check_spawn("posix_spawn", unsafe {
            libc::posix_spawn(
                &mut process_id,
                exe.as_ptr(),
                &actions.0,
                &attr.0,
                argv_ptrs.as_ptr(),
                env_ptrs.as_ptr(),
            )
        })
        .map(|()| process_id);
        let process_id = result?;
        drop(child_ends);
        let exit_queue = match exit_source(process_id) {
            Ok(q) => q,
            Err(e) => {
                // The child we could not observe: its group, then itself,
                // then the exact reap (D1a r1 RF-4). The setup error is the
                // one returned, unless the reap fails as well.
                return Err(match kill_and_reap(process_id) {
                    Ok(_) => e,
                    Err(reap) => {
                        // Not exactly reaped, so it may still run in its
                        // scratch: the scratch and its hold on the root are
                        // kept for this process's life, as `Drop` keeps an
                        // unreapable child's (D1a r3 RF-1).
                        std::mem::forget(scratch);
                        LaunchError::SetupAbandoned {
                            setup: Box::new(e),
                            reap,
                        }
                    }
                });
            }
        };
        Ok(Child {
            process_id,
            exit_queue,
            host_ends,
            root_guard: Some(Arc::clone(&scratch.root)),
            scratch: Some(scratch),
            reaped: false,
            abandoned: false,
        })
    }

    /// `posix_spawnattr_t`, destroyed on drop.
    struct SpawnAttributes(libc::posix_spawnattr_t);
    impl SpawnAttributes {
        fn new() -> Result<Self, LaunchError> {
            let mut a: libc::posix_spawnattr_t = std::ptr::null_mut();
            // SAFETY: valid out-pointer.
            check_spawn("posix_spawnattr_init", unsafe {
                libc::posix_spawnattr_init(&mut a)
            })?;
            Ok(Self(a))
        }
    }
    impl Drop for SpawnAttributes {
        fn drop(&mut self) {
            // SAFETY: initialized in `new`.
            unsafe { libc::posix_spawnattr_destroy(&mut self.0) };
        }
    }
    /// `posix_spawn_file_actions_t`, destroyed on drop.
    struct FileActions(libc::posix_spawn_file_actions_t);
    impl FileActions {
        fn new() -> Result<Self, LaunchError> {
            let mut a: libc::posix_spawn_file_actions_t = std::ptr::null_mut();
            // SAFETY: valid out-pointer.
            check_spawn("posix_spawn_file_actions_init", unsafe {
                libc::posix_spawn_file_actions_init(&mut a)
            })?;
            Ok(Self(a))
        }
    }
    impl Drop for FileActions {
        fn drop(&mut self) {
            // SAFETY: initialized in `new`.
            unsafe { libc::posix_spawn_file_actions_destroy(&mut self.0) };
        }
    }

    /// Item 4: `kqueue` `EVFILT_PROC` with `NOTE_EXIT | NOTE_EXITSTATUS`,
    /// registered on the unreaped child (CF-P MX-7).
    fn exit_source(process_id: libc::pid_t) -> Result<OwnedFd, LaunchError> {
        #[cfg(test)]
        if let Some(delay) = FAIL_EXIT_SOURCE.with(|f| f.get()) {
            // The setup-failure control (D1a r1 RF-4): give the child time to
            // fork a descendant, then fail as kqueue exhaustion would.
            std::thread::sleep(delay);
            return Err(LaunchError::Io {
                call: "kqueue",
                error: io::Error::from_raw_os_error(libc::EMFILE),
            });
        }
        // SAFETY: kqueue has no inputs.
        let kq = unsafe { libc::kqueue() };
        check("kqueue", kq)?;
        // SAFETY: fresh descriptor.
        let kq = unsafe { OwnedFd::from_raw_fd(kq) };
        set_flag(
            kq.as_raw_fd(),
            libc::F_GETFD,
            libc::F_SETFD,
            libc::FD_CLOEXEC,
        )?;
        let change = libc::kevent {
            ident: process_id as libc::uintptr_t,
            filter: libc::EVFILT_PROC,
            flags: libc::EV_ADD | libc::EV_ONESHOT,
            fflags: libc::NOTE_EXIT | libc::NOTE_EXITSTATUS,
            data: 0,
            udata: std::ptr::null_mut(),
        };
        // SAFETY: one change, no events requested.
        check("kevent(register)", unsafe {
            libc::kevent(
                kq.as_raw_fd(),
                &change,
                1,
                std::ptr::null_mut(),
                0,
                std::ptr::null(),
            )
        })?;
        Ok(kq)
    }

    impl Child {
        /// The child's pid, which is also its session and process group id.
        pub fn process_id(&self) -> i32 {
            self.process_id
        }
        /// Take the host end of one slot (for a supervisor's I/O loop).
        /// A tool's fd0 has none: its write end was closed at spawn.
        pub fn take_host_end(&mut self, slot: usize) -> Option<File> {
            self.host_ends.get_mut(slot)?.take()
        }
        pub fn scratch(&self) -> Option<&ChildScratch> {
            self.scratch.as_ref()
        }
        pub fn take_scratch(&mut self) -> Option<ChildScratch> {
            self.scratch.take()
        }
        /// The exit source's descriptor, for a supervisor's event loop.
        pub fn exit_source(&self) -> RawFd {
            self.exit_queue.as_raw_fd()
        }
        /// Wait up to `timeout` for the exit event; the child stays
        /// unreaped, so its pid and group id stay reserved (item 4).
        pub fn wait_exit(&self, timeout: Duration) -> Result<Option<ExitStatus>, LaunchError> {
            let ts = libc::timespec {
                tv_sec: timeout.as_secs() as libc::time_t,
                tv_nsec: timeout.subsec_nanos() as libc::c_long,
            };
            // SAFETY: zeroed kevent is a valid out-buffer.
            let mut event: libc::kevent = unsafe { std::mem::zeroed() };
            // SAFETY: wait for at most one event with a timeout.
            let n = unsafe {
                libc::kevent(
                    self.exit_queue.as_raw_fd(),
                    std::ptr::null(),
                    0,
                    &mut event,
                    1,
                    &ts,
                )
            };
            check("kevent(wait)", n)?;
            if n == 0 {
                return Ok(None);
            }
            Ok(Some(ExitStatus {
                raw: event.data as i32,
            }))
        }
        /// `waitid(P_PID, pid, WEXITED | WNOWAIT | WNOHANG)`: whether the
        /// child has exited, leaving it waitable.
        pub fn has_exited(&self) -> Result<bool, LaunchError> {
            // SAFETY: zeroed siginfo is a valid out-buffer.
            let mut info: libc::siginfo_t = unsafe { std::mem::zeroed() };
            // SAFETY: waitid on our own child without reaping it.
            check("waitid", unsafe {
                libc::waitid(
                    libc::P_PID,
                    self.process_id as libc::id_t,
                    &mut info,
                    libc::WEXITED | libc::WNOWAIT | libc::WNOHANG,
                )
            })?;
            Ok(info.si_pid != 0)
        }
        /// Signal the child's process group, only while the root is unreaped
        /// (the reap-last rule, item 4).
        pub fn signal_group(&self, signal: i32) -> Result<(), LaunchError> {
            if self.reaped {
                return Err(LaunchError::GroupAfterReap);
            }
            #[cfg(test)]
            record("killpg");
            // SAFETY: killpg on the child's own group id.
            check("killpg", unsafe { libc::killpg(self.process_id, signal) })
        }
        /// The final reap, `wait4(pid)`, with rusage (item 4).
        pub fn reap(&mut self) -> Result<Reaped, LaunchError> {
            if self.reaped {
                return Err(LaunchError::AlreadyReaped);
            }
            let mut status = 0;
            // SAFETY: zeroed rusage is a valid out-buffer.
            let mut usage: libc::rusage = unsafe { std::mem::zeroed() };
            // SAFETY: wait4 on exactly this child, never a wildcard.
            #[cfg(test)]
            record("wait4");
            let rc = loop {
                // SAFETY: wait4 on exactly this child, retried on EINTR.
                let rc = unsafe { libc::wait4(self.process_id, &mut status, 0, &mut usage) };
                if rc == -1 && io::Error::last_os_error().raw_os_error() == Some(libc::EINTR) {
                    continue;
                }
                break rc;
            };
            check("wait4", rc)?;
            Ok(self.settle_reap(status, usage))
        }
        /// The non-blocking reap (D3a-0, LD-D3A-14): `wait4(pid, WNOHANG)`,
        /// which D3 calls after the exit source reports the exit. `None`
        /// leaves the child unreaped, its pid and group id still reserved.
        /// It never blocks; the reap ceiling and its outcome are D3's.
        pub fn try_reap(&mut self) -> Result<Option<Reaped>, LaunchError> {
            if self.reaped {
                return Err(LaunchError::AlreadyReaped);
            }
            let mut status = 0;
            // SAFETY: zeroed rusage is a valid out-buffer.
            let mut usage: libc::rusage = unsafe { std::mem::zeroed() };
            #[cfg(test)]
            record("wait4(WNOHANG)");
            let rc = loop {
                // SAFETY: wait4 on exactly this child, never blocking, retried
                // on EINTR.
                let rc =
                    unsafe { libc::wait4(self.process_id, &mut status, libc::WNOHANG, &mut usage) };
                if rc == -1 && io::Error::last_os_error().raw_os_error() == Some(libc::EINTR) {
                    continue;
                }
                break rc;
            };
            check("wait4", rc)?;
            if rc == 0 {
                return Ok(None);
            }
            Ok(Some(self.settle_reap(status, usage)))
        }
        /// Give up on reaping the root (D3a-0, LD-D3A-14; item 18's reap
        /// ceiling): the host never signals or reaps it again. The returned
        /// [`Unreaped`] keeps the scratch-root hold, any attached scratch and
        /// the pid for the record, for this process's life.
        pub fn abandon(mut self) -> Unreaped {
            self.abandoned = true;
            Unreaped {
                process_id: self.process_id,
                root_guard: self.root_guard.take(),
                scratch: self.scratch.take(),
            }
        }
        /// A reap's settlement: the child no longer runs.
        fn settle_reap(&mut self, status: i32, usage: libc::rusage) -> Reaped {
            self.reaped = true;
            // Reaped: the child no longer runs, so its own hold on the root
            // ends; an attached scratch still holds it.
            self.root_guard = None;
            let micros = |t: libc::timeval| t.tv_sec as u64 * 1_000_000 + t.tv_usec as u64;
            Reaped {
                status: ExitStatus { raw: status },
                user_micros: micros(usage.ru_utime),
                system_micros: micros(usage.ru_stime),
                // macOS reports ru_maxrss in bytes.
                max_resident_bytes: usage.ru_maxrss as u64,
            }
        }
        pub fn is_reaped(&self) -> bool {
            self.reaped
        }
    }
    impl Drop for Child {
        /// Dropping an unreaped child is a supervisor defect; the group is
        /// killed and the root reaped so no zombie or orphan escapes.
        fn drop(&mut self) {
            // An abandoned root is never signalled or reaped again; its hold
            // moved into the `Unreaped` (D3a-0).
            if self.abandoned {
                return;
            }
            // Reaped only when the exact reap says so (D1a r1 RF-3).
            if !self.reaped && kill_and_reap(self.process_id).is_ok() {
                self.reaped = true;
            }
            // A child that could not be reaped may still be running in its
            // scratch, so its hold on the root is never released: the lock
            // stays held for this process's life (D1a r2 RF-1).
            if !self.reaped {
                std::mem::forget(self.root_guard.take());
            }
        }
    }

    /// A root the host gave up reaping at the ceiling (D3a-0, LD-D3A-14):
    /// it is never signalled or reaped again, and its scratch-root hold and
    /// any attached scratch are kept for this process's life, as an
    /// unreapable child's are (D1a r2 RF-1). Its `Drop` neither signals nor
    /// blocks.
    #[derive(Debug)]
    pub struct Unreaped {
        process_id: libc::pid_t,
        root_guard: Option<Arc<RootState>>,
        scratch: Option<ChildScratch>,
    }
    impl Unreaped {
        /// The pid, for the operational record.
        pub fn process_id(&self) -> i32 {
            self.process_id
        }
    }
    impl Drop for Unreaped {
        fn drop(&mut self) {
            // The root may still run in its scratch: neither is released.
            std::mem::forget(self.root_guard.take());
            std::mem::forget(self.scratch.take());
        }
    }

    /// One process's resident bytes (D3a-0, LD-D3A-8; item 16's input):
    /// `proc_pid_rusage(RUSAGE_INFO_V0)`'s `ri_resident_size`. A primitive
    /// with no policy, for the supervised root and its group's members.
    pub fn resident_bytes(process_id: i32) -> Result<u64, LaunchError> {
        // SAFETY: zeroed rusage_info_v0 is a valid out-buffer.
        let mut info: libc::rusage_info_v0 = unsafe { std::mem::zeroed() };
        // SAFETY: a buffer of the V0 flavour's exact type.
        check("proc_pid_rusage", unsafe {
            libc::proc_pid_rusage(
                process_id,
                libc::RUSAGE_INFO_V0,
                (&mut info as *mut libc::rusage_info_v0).cast::<libc::rusage_info_t>(),
            )
        })?;
        Ok(info.ri_resident_size)
    }

    /// Wait until one of `entries` is ready or `timeout` passes (unit D3a-1;
    /// item 12, :449: the supervisor's one readiness loop over the child's
    /// host ends and its exit source): one `poll(2)`, retried only on
    /// `EINTR` within the same deadline. Returns how many are ready, each
    /// entry's `readable` and `writable` set from what `poll` reported. A
    /// timeout of zero only samples. It holds no policy: which descriptors
    /// are waited on, and for what, are the caller's.
    pub fn wait_ready(entries: &mut [Readiness], timeout: Duration) -> Result<usize, LaunchError> {
        let mut fds: Vec<libc::pollfd> = entries
            .iter()
            .map(|e| libc::pollfd {
                fd: e.fd,
                events: if e.read { libc::POLLIN } else { 0 }
                    | if e.write { libc::POLLOUT } else { 0 },
                revents: 0,
            })
            .collect();
        let deadline = std::time::Instant::now() + timeout;
        let ready = loop {
            let left = deadline.saturating_duration_since(std::time::Instant::now());
            // Rounded up, so a sub-millisecond remainder still waits.
            let millis = left.as_micros().div_ceil(1000).min(i32::MAX as u128) as libc::c_int;
            #[cfg(test)]
            let interrupted = POLL_EINTR.with(|c| c.get());
            #[cfg(not(test))]
            let interrupted = false;
            let rc = if interrupted {
                -1
            } else {
                // SAFETY: `fds` is a live array of `fds.len()` pollfd records.
                unsafe { libc::poll(fds.as_mut_ptr(), fds.len() as libc::nfds_t, millis) }
            };
            if rc == -1
                && (interrupted || io::Error::last_os_error().raw_os_error() == Some(libc::EINTR))
            {
                // Retried only within the original deadline (r2, Codex
                // D3A1-R1-RF-3): past it, an interrupted wait is a timeout,
                // with nothing ready. A zero timeout still samples once.
                if std::time::Instant::now() >= deadline {
                    for entry in entries.iter_mut() {
                        entry.readable = false;
                        entry.writable = false;
                    }
                    return Ok(0);
                }
                continue;
            }
            check("poll", rc)?;
            break rc as usize;
        };
        for (entry, fd) in entries.iter_mut().zip(&fds) {
            let gone = fd.revents & (libc::POLLHUP | libc::POLLERR | libc::POLLNVAL) != 0;
            entry.readable = entry.read && (fd.revents & libc::POLLIN != 0 || gone);
            entry.writable = entry.write && (fd.revents & libc::POLLOUT != 0 || gone);
        }
        Ok(ready)
    }

    /// Group membership by enumeration (item 18's input; item 8):
    /// `proc_listpids(PROC_PGRP_ONLY, pgid)`, which returns bytes. Never a
    /// `killpg` error.
    pub fn group_members(group: i32) -> Result<Vec<i32>, LaunchError> {
        let mut capacity = 64usize;
        loop {
            let mut buf = vec![0 as libc::pid_t; capacity];
            let size = (capacity * std::mem::size_of::<libc::pid_t>()) as libc::c_int;
            // SAFETY: buffer of `size` bytes.
            let bytes = unsafe {
                libc::proc_listpids(PROC_PGRP_ONLY, group as u32, buf.as_mut_ptr().cast(), size)
            };
            if bytes < 0 {
                return Err(last("proc_listpids"));
            }
            let n = bytes as usize / std::mem::size_of::<libc::pid_t>();
            if n < capacity {
                buf.truncate(n);
                buf.retain(|p| *p != 0);
                buf.sort_unstable();
                return Ok(buf);
            }
            capacity *= 2;
        }
    }
}

// ------------------------------------------------------------------ other targets

#[cfg(not(target_os = "macos"))]
mod unsupported {
    use super::{ExitStatus, LaunchError, Reaped, VerifiedLaunch};
    use crate::{WorkFailure, WorkScope};
    use std::fs::File;
    use std::path::Path;
    use std::time::Duration;

    #[derive(Debug)]
    pub struct ScratchRoot(());
    impl ScratchRoot {
        pub fn create() -> Result<Self, LaunchError> {
            Err(LaunchError::PlatformUnsupported)
        }
        pub fn path(&self) -> &Path {
            Path::new("/")
        }
        pub fn sweep(&self) -> Result<Vec<String>, LaunchError> {
            Err(LaunchError::PlatformUnsupported)
        }
    }
    #[derive(Debug)]
    pub struct ChildScratch(());
    impl ChildScratch {
        pub fn measure(
            &self,
            _: u64,
            _: &mut WorkScope<'_>,
        ) -> Result<u64, WorkFailure<LaunchError>> {
            Err(WorkFailure::Operation(LaunchError::PlatformUnsupported))
        }
        pub fn remove_bounded(self, _: &mut WorkScope<'_>) -> Result<(), WorkFailure<LaunchError>> {
            Err(WorkFailure::Operation(LaunchError::PlatformUnsupported))
        }
    }
    #[derive(Debug)]
    pub struct Unreaped(());
    impl Unreaped {
        pub fn process_id(&self) -> i32 {
            0
        }
    }
    #[derive(Debug)]
    pub struct Child(());
    impl Child {
        pub fn process_id(&self) -> i32 {
            0
        }
        pub fn take_host_end(&mut self, _: usize) -> Option<File> {
            None
        }
        pub fn wait_exit(&self, _: Duration) -> Result<Option<ExitStatus>, LaunchError> {
            Err(LaunchError::PlatformUnsupported)
        }
        pub fn signal_group(&self, _: i32) -> Result<(), LaunchError> {
            Err(LaunchError::PlatformUnsupported)
        }
        pub fn reap(&mut self) -> Result<Reaped, LaunchError> {
            Err(LaunchError::PlatformUnsupported)
        }
        pub fn try_reap(&mut self) -> Result<Option<Reaped>, LaunchError> {
            Err(LaunchError::PlatformUnsupported)
        }
        pub fn abandon(self) -> Unreaped {
            Unreaped(())
        }
    }
    pub fn resident_bytes(_: i32) -> Result<u64, LaunchError> {
        Err(LaunchError::PlatformUnsupported)
    }
    pub fn wait_ready(_: &mut [super::Readiness], _: Duration) -> Result<usize, LaunchError> {
        Err(LaunchError::PlatformUnsupported)
    }
    pub fn spawn(_: VerifiedLaunch, _: &mut ScratchRoot) -> Result<Child, LaunchError> {
        Err(LaunchError::PlatformUnsupported)
    }
    pub fn group_members(_: i32) -> Result<Vec<i32>, LaunchError> {
        Err(LaunchError::PlatformUnsupported)
    }
}
