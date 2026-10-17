// M3-D r5 items 1 to 8 (unit D1a): the macOS rows of D1-T1 to T9 and T7b.
// The `TestFixture` child is this test binary (LD-D1A-4), spawned through
// `process.rs` with an exact argv that selects `fixture_child`; it reports
// what the controls observe over fd1, one `D1FIX key=value` line each.
// Linux rows (D1-T9b and every Linux half) are not run on this host.
use crate::process::{
    ChildEnvironment, ClosureRecheck, DescriptorSet, FAIL_EXIT_SOURCE, FORCE_NP, INJECT_EINTR,
    LAST_CHDIR, LaunchError, LaunchSpec, ScratchRoot, SpecError, VerifiedLaunch, group_members,
    spawn,
};
use std::collections::BTreeMap;
use std::ffi::OsStr;
use std::fs::File;
use std::io::Read;
use std::os::fd::{AsRawFd, FromRawFd, IntoRawFd, OwnedFd};
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::time::Duration;

const SENTINEL: &str = "opensip-d1-fixture";
const FIXTURE: &str = "process_tests::fixture_child";

// ------------------------------------------------------------------ the fixture child

/// In an ordinary test run this does nothing. Spawned with the sentinel it
/// is the `TestFixture` child: it reports and exits without returning to the
/// test harness.
#[test]
fn fixture_child() {
    let args: Vec<String> = std::env::args().collect();
    if !args.iter().any(|a| a == SENTINEL) {
        return;
    }
    let mode = args
        .iter()
        .find_map(|a| a.strip_prefix("mode="))
        .unwrap_or("report")
        .to_owned();
    if mode == "descendant" {
        // A grandchild in the child's group, which writes its own pid to
        // `grandchild.pid` in the cwd (the scratch) with async-signal-safe
        // calls only, then waits to be killed; the child waits too.
        let forked = unsafe { libc::fork() };
        if forked == 0 {
            let me = unsafe { libc::getpid() };
            let mut digits = [0u8; 16];
            let mut n = me as u32;
            let mut at = digits.len();
            loop {
                at -= 1;
                digits[at] = b'0' + (n % 10) as u8;
                n /= 10;
                if n == 0 {
                    break;
                }
            }
            let fd = unsafe {
                libc::open(
                    c"grandchild.pid.tmp".as_ptr(),
                    libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL,
                    0o600,
                )
            };
            unsafe {
                libc::write(fd, digits[at..].as_ptr().cast(), digits.len() - at);
                libc::close(fd);
                libc::rename(c"grandchild.pid.tmp".as_ptr(), c"grandchild.pid".as_ptr());
            }
            loop {
                unsafe { libc::pause() };
            }
        }
        loop {
            unsafe { libc::pause() };
        }
    }
    let mut lines = Vec::new();
    // The environment, exactly.
    for (k, v) in std::env::vars_os() {
        lines.push(format!(
            "env={}={}",
            k.to_string_lossy(),
            v.to_string_lossy()
        ));
    }
    // Open descriptors over the table range.
    let open: Vec<String> = (0..1024)
        .filter(|fd| unsafe { libc::fcntl(*fd, libc::F_GETFD) } != -1)
        .map(|fd| fd.to_string())
        .collect();
    lines.push(format!("fds={}", open.join(",")));
    // Session, group and pid.
    let (me, sid, pgid) = unsafe { (libc::getpid(), libc::getsid(0), libc::getpgid(0)) };
    lines.push(format!("self={me} sid={sid} pgid={pgid}"));
    // A controlling terminal cannot be opened.
    let tty = unsafe { libc::open(c"/dev/tty".as_ptr(), libc::O_RDWR | libc::O_NOCTTY) };
    lines.push(format!(
        "tty={}",
        if tty == -1 { "none" } else { "present" }
    ));
    // Signal dispositions and the mask.
    let mut caught = Vec::new();
    for sig in 1..32 {
        let mut old: libc::sigaction = unsafe { std::mem::zeroed() };
        if unsafe { libc::sigaction(sig, std::ptr::null(), &mut old) } == 0
            && old.sa_sigaction != libc::SIG_DFL
        {
            caught.push(sig.to_string());
        }
    }
    lines.push(format!("nondefault={}", caught.join(",")));
    let mut mask: libc::sigset_t = unsafe { std::mem::zeroed() };
    unsafe { libc::pthread_sigmask(libc::SIG_SETMASK, std::ptr::null(), &mut mask) };
    let blocked: Vec<String> = (1..32)
        .filter(|s| unsafe { libc::sigismember(&mask, *s) } == 1)
        .map(|s| s.to_string())
        .collect();
    lines.push(format!("blocked={}", blocked.join(",")));
    // RLIMIT_CORE.
    let mut core = libc::rlimit {
        rlim_cur: 1,
        rlim_max: 0,
    };
    unsafe { libc::getrlimit(libc::RLIMIT_CORE, &mut core) };
    lines.push(format!("core={}", core.rlim_cur));
    // The cwd: inode, mode, owner and emptiness.
    let cwd = std::fs::metadata(".").unwrap();
    let entries = std::fs::read_dir(".").unwrap().count();
    lines.push(format!(
        "cwd_ino={} cwd_mode={:o} cwd_uid={} cwd_entries={}",
        cwd.ino(),
        cwd.mode() & 0o7777,
        cwd.uid(),
        entries
    ));
    // fd0: does it read EOF at once?
    if mode == "stdin-eof" || mode == "hold" {
        let mut buf = [0u8; 16];
        let mut total = 0usize;
        loop {
            let n = unsafe { libc::read(0, buf.as_mut_ptr().cast(), buf.len()) };
            if n <= 0 {
                break;
            }
            total += n as usize;
        }
        lines.push(format!("stdin_bytes={total}"));
    }
    let mut out = String::new();
    for l in &lines {
        out.push_str("D1FIX ");
        out.push_str(l);
        out.push('\n');
    }
    unsafe { libc::write(1, out.as_ptr().cast(), out.len()) };
    let code = if mode == "exit7" { 7 } else { 0 };
    unsafe { libc::_exit(code) };
}

// ------------------------------------------------------------------ helpers

struct TestDir(PathBuf);
impl Drop for TestDir {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn test_dir() -> TestDir {
    let mut bytes = [0u8; 8];
    getrandom::fill(&mut bytes).unwrap();
    let hex: String = bytes.iter().map(|b| format!("{b:02x}")).collect();
    let dir = std::env::temp_dir().join(format!("opensip-d1a-test-{hex}"));
    std::fs::create_dir(&dir).unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    TestDir(dir.canonicalize().unwrap())
}
fn open_dir(path: &Path) -> OwnedFd {
    let file = File::open(path).unwrap();
    // SAFETY: ownership of the descriptor moves from the File (D1a r1 RF-5).
    unsafe { OwnedFd::from_raw_fd(file.into_raw_fd()) }
}
fn root_in(dir: &TestDir) -> ScratchRoot {
    ScratchRoot::create_in(open_dir(&dir.0)).unwrap()
}
fn recheck() -> ClosureRecheck {
    ClosureRecheck {
        member: "test-fixture".to_owned(),
        device: 0,
        inode: 0,
        sha256: "0".repeat(64),
    }
}
fn fixture_spec(set: DescriptorSet, env: ChildEnvironment, mode: &str) -> LaunchSpec {
    let exe = std::env::current_exe().unwrap();
    let mode = format!("mode={mode}");
    let argv: Vec<&OsStr> = vec![
        exe.as_os_str(),
        OsStr::new(FIXTURE),
        OsStr::new("--exact"),
        OsStr::new("--nocapture"),
        OsStr::new("--test-threads=1"),
        OsStr::new(SENTINEL),
        OsStr::new(&mode),
    ];
    LaunchSpec::fixture(set, &exe, &argv, env).unwrap()
}
fn blocking(file: &File) {
    let fd = file.as_raw_fd();
    let flags = unsafe { libc::fcntl(fd, libc::F_GETFL) };
    unsafe { libc::fcntl(fd, libc::F_SETFL, flags & !libc::O_NONBLOCK) };
}
/// Run a fixture to completion and return its report and exit code.
fn run(set: DescriptorSet, env: ChildEnvironment, mode: &str, root: &mut ScratchRoot) -> Report {
    let mut child = spawn(
        VerifiedLaunch::from_recheck(fixture_spec(set, env, mode), recheck()),
        root,
    )
    .unwrap();
    // Close the host's fd0 write end (a provider set), so a reader sees EOF.
    drop(child.take_host_end(0));
    let mut out = child.take_host_end(1).unwrap();
    blocking(&out);
    let mut text = String::new();
    out.read_to_string(&mut text).unwrap();
    let status = child
        .wait_exit(Duration::from_secs(30))
        .unwrap()
        .expect("exit");
    let reaped = child.reap().unwrap();
    assert_eq!(reaped.status, status);
    let scratch_ino = child.scratch().map(|s| s.inode().unwrap());
    let mut report = Report {
        lines: BTreeMap::new(),
        env: Vec::new(),
        code: status.code(),
        process_id: child.process_id(),
        scratch_ino,
    };
    // libtest prints `test … ` without a newline before the fixture writes,
    // so a marker may follow other text on its line.
    for line in text
        .lines()
        .filter_map(|l| l.split_once("D1FIX ").map(|(_, r)| r))
    {
        if let Some(e) = line.strip_prefix("env=") {
            report.env.push(e.to_owned());
        } else {
            for field in line.split(' ') {
                if let Some((k, v)) = field.split_once('=') {
                    report.lines.insert(k.to_owned(), v.to_owned());
                }
            }
        }
    }
    report.env.sort();
    report
}
struct Report {
    lines: BTreeMap<String, String>,
    env: Vec<String>,
    code: Option<i32>,
    process_id: i32,
    scratch_ino: Option<u64>,
}
impl Report {
    fn get(&self, k: &str) -> &str {
        self.lines
            .get(k)
            .map(String::as_str)
            .unwrap_or_else(|| panic!("missing {k}"))
    }
}

// ------------------------------------------------------------------ D1-T2, T3: specs

#[test]
fn d1_t2_specs_refuse_relative_paths_extra_arguments_and_bad_argv_zero() {
    let env = ChildEnvironment::rust();
    assert!(matches!(
        LaunchSpec::rust(Path::new("provider"), Path::new("/toolchain")),
        Err(SpecError::RelativePath(_))
    ));
    assert!(matches!(
        LaunchSpec::rust(Path::new("/provider"), Path::new("toolchain")),
        Err(SpecError::RelativePath(_))
    ));
    let rust = LaunchSpec::rust(Path::new("/p/provider"), Path::new("/p/toolchain")).unwrap();
    assert_eq!(rust.environment(), &env);
    // D1a plan r2 (RF-3): each provider profile's argv and environment are
    // exact, element by element; no caller can supply another.
    let ts = LaunchSpec::typescript(
        Path::new("/r/node"),
        Path::new("/r/share/openssl-empty.cnf"),
        Path::new("/r/provider/index.js"),
        "ctx",
    )
    .unwrap();
    assert_eq!(ts.descriptors(), DescriptorSet::Provider);
    let argv = |spec: &LaunchSpec| -> Vec<String> {
        spec.resolved_argv(Path::new("/s/scratch"))
            .unwrap()
            .iter()
            .map(|c| c.to_string_lossy().into_owned())
            .collect()
    };
    assert_eq!(
        argv(&ts),
        [
            "/r/node",
            "--no-addons",
            "--no-global-search-paths",
            "--openssl-config=/r/share/openssl-empty.cnf",
            "/r/provider/index.js",
        ]
    );
    let env = |spec: &LaunchSpec| -> Vec<String> {
        spec.environment()
            .entries()
            .iter()
            .map(|(k, v)| format!("{k}={v}"))
            .collect()
    };
    assert_eq!(
        env(&ts),
        [
            "LC_ALL=C",
            "LANG=C",
            "TZ=UTC",
            "UV_THREADPOOL_SIZE=4",
            "OPENSIP_BROKER_CONTEXT=ctx",
        ]
    );
    assert_eq!(
        argv(&rust),
        [
            "/p/provider",
            "--protocol-stdio-v2",
            "--toolchain-root",
            "/p/toolchain",
            "--scratch-root",
            "/s/scratch",
        ]
    );
    assert_eq!(env(&rust), ["LANG=C", "LC_ALL=C", "TZ=UTC"]);
    for bad in [
        ("share/openssl-empty.cnf", "/r/provider/index.js"),
        ("/r/share/openssl-empty.cnf", "provider/index.js"),
    ] {
        assert!(matches!(
            LaunchSpec::typescript(
                Path::new("/r/node"),
                Path::new(bad.0),
                Path::new(bad.1),
                "ctx"
            ),
            Err(SpecError::RelativePath(_))
        ));
    }
    assert!(matches!(
        LaunchSpec::typescript(Path::new("node"), Path::new("/c"), Path::new("/e"), "ctx"),
        Err(SpecError::RelativePath(_))
    ));
    assert_eq!(
        LaunchSpec::typescript(
            Path::new("/r/node"),
            Path::new("/c"),
            Path::new("/e"),
            "a\0b"
        )
        .unwrap_err(),
        SpecError::Nul
    );
    // A tool's argv[0] must be the executable's absolute path.
    let tool = |argv: &[&str]| {
        let argv: Vec<&OsStr> = argv.iter().map(OsStr::new).collect();
        LaunchSpec::tool(
            Path::new("/b/cargo"),
            &argv,
            ChildEnvironment::tool(&[]).unwrap(),
        )
    };
    assert!(tool(&["/b/cargo", "metadata"]).is_ok());
    assert_eq!(
        tool(&["cargo", "metadata"]).unwrap_err(),
        SpecError::ArgvZero
    );
    assert_eq!(tool(&[]).unwrap_err(), SpecError::ArgvZero);
    assert!(matches!(
        LaunchSpec::tool(
            Path::new("cargo"),
            &[OsStr::new("cargo")],
            ChildEnvironment::tool(&[]).unwrap()
        ),
        Err(SpecError::RelativePath(_))
    ));
}

#[test]
fn d1_t3_environments_are_built_from_empty_and_validated() {
    let ts = ChildEnvironment::typescript("ctx").unwrap();
    let keys: Vec<&str> = ts.entries().iter().map(|(k, _)| k.as_str()).collect();
    assert_eq!(
        keys,
        [
            "LC_ALL",
            "LANG",
            "TZ",
            "UV_THREADPOOL_SIZE",
            "OPENSIP_BROKER_CONTEXT"
        ]
    );
    let rust: Vec<String> = ChildEnvironment::rust()
        .entries()
        .iter()
        .map(|(k, v)| format!("{k}={v}"))
        .collect();
    assert_eq!(rust, ["LANG=C", "LC_ALL=C", "TZ=UTC"]);
    assert_eq!(
        ChildEnvironment::typescript("a\0b").unwrap_err(),
        SpecError::Nul
    );
    // C3b's tool allowlist is empty until C3b names its keys.
    assert_eq!(
        ChildEnvironment::tool(&[("HOME", "/x")]).unwrap_err(),
        SpecError::KeyNotAllowed("HOME".to_owned())
    );
    for denied in [
        "PATH",
        "CARGO_HOME",
        "RUSTFLAGS",
        "RUSTC_WRAPPER",
        "RUSTUP_HOME",
        "CC",
        "TARGET_CC",
    ] {
        assert_eq!(
            ChildEnvironment::tool(&[(denied, "x")]).unwrap_err(),
            SpecError::KeyDenied(denied.to_owned()),
            "{denied}"
        );
    }
    assert_eq!(
        ChildEnvironment::fixture(&[("", "x")]).unwrap_err(),
        SpecError::EmptyKey
    );
    assert_eq!(
        ChildEnvironment::fixture(&[("A=B", "x")]).unwrap_err(),
        SpecError::KeyEquals("A=B".to_owned())
    );
    assert_eq!(
        ChildEnvironment::fixture(&[("A", "1"), ("A", "2")]).unwrap_err(),
        SpecError::DuplicateKey("A".to_owned())
    );
}

#[test]
fn d1_t3_the_child_sees_exactly_its_class_environment() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let ts = ChildEnvironment::typescript("bootstrap").unwrap();
    let report = run(DescriptorSet::Provider, ts, "report", &mut root);
    assert_eq!(
        report.env,
        [
            "LANG=C",
            "LC_ALL=C",
            "OPENSIP_BROKER_CONTEXT=bootstrap",
            "TZ=UTC",
            "UV_THREADPOOL_SIZE=4",
        ]
    );
    let report = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    assert_eq!(report.env, ["LANG=C", "LC_ALL=C", "TZ=UTC"]);
    let report = run(
        DescriptorSet::Tool,
        ChildEnvironment::tool(&[]).unwrap(),
        "report",
        &mut root,
    );
    assert!(report.env.is_empty(), "{:?}", report.env);
}

// ------------------------------------------------------------------ D1-T1, T4, T5, T6, T9

#[test]
fn d1_t1_t5_each_class_receives_exactly_its_descriptor_set() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let provider = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    assert_eq!(provider.get("fds"), "0,1,2,3,4");
    let tool = run(
        DescriptorSet::Tool,
        ChildEnvironment::tool(&[]).unwrap(),
        "stdin-eof",
        &mut root,
    );
    assert_eq!(tool.get("fds"), "0,1,2");
    // A tool's fd0 reads EOF at once.
    assert_eq!(tool.get("stdin_bytes"), "0");
}

#[test]
fn d1_t4_the_child_leads_a_new_session_with_no_controlling_terminal() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let r = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    let me = r.get("self");
    assert_eq!(r.get("sid"), me);
    assert_eq!(r.get("pgid"), me);
    assert_eq!(me, r.process_id.to_string());
    assert_eq!(r.get("tty"), "none");
}

#[test]
fn d1_t6_a_descriptor_opened_without_cloexec_during_spawn_does_not_reach_the_child() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let stop = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
    let flag = stop.clone();
    let opener = std::thread::spawn(move || {
        let mut held = Vec::new();
        while !flag.load(std::sync::atomic::Ordering::Relaxed) {
            // Deliberately inheritable: no O_CLOEXEC.
            let fd = unsafe { libc::open(c"/dev/null".as_ptr(), libc::O_RDONLY) };
            if fd >= 0 {
                held.push(fd);
            }
            if held.len() > 64 {
                for fd in held.drain(..) {
                    unsafe { libc::close(fd) };
                }
            }
        }
        for fd in held {
            unsafe { libc::close(fd) };
        }
    });
    for _ in 0..8 {
        let r = run(
            DescriptorSet::Provider,
            ChildEnvironment::rust(),
            "report",
            &mut root,
        );
        assert_eq!(r.get("fds"), "0,1,2,3,4");
    }
    stop.store(true, std::sync::atomic::Ordering::Relaxed);
    opener.join().unwrap();
}

#[test]
fn d1_t9_default_dispositions_empty_mask_and_no_core_files() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    // The host ignores SIGUSR1 and blocks SIGUSR2 in the spawning thread;
    // neither may carry into the child (item 7).
    let mut ignore: libc::sigaction = unsafe { std::mem::zeroed() };
    ignore.sa_sigaction = libc::SIG_IGN;
    let mut previous: libc::sigaction = unsafe { std::mem::zeroed() };
    unsafe { libc::sigaction(libc::SIGUSR1, &ignore, &mut previous) };
    let mut block: libc::sigset_t = unsafe { std::mem::zeroed() };
    let mut old_mask: libc::sigset_t = unsafe { std::mem::zeroed() };
    unsafe {
        libc::sigemptyset(&mut block);
        libc::sigaddset(&mut block, libc::SIGUSR2);
        libc::pthread_sigmask(libc::SIG_BLOCK, &block, &mut old_mask);
    }
    let r = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    unsafe {
        libc::pthread_sigmask(libc::SIG_SETMASK, &old_mask, std::ptr::null_mut());
        libc::sigaction(libc::SIGUSR1, &previous, std::ptr::null_mut());
    }
    // The child's own Rust runtime installs SIGBUS (10) and SIGSEGV (11)
    // handlers and ignores SIGPIPE (13) after exec; every other signal,
    // SIGUSR1 (30) included, is at its default.
    assert_eq!(r.get("nondefault"), "10,11,13");
    assert_eq!(r.get("blocked"), "");
    assert_eq!(r.get("core"), "0");
    // The host's own soft limit was lowered before the first spawn (item 7).
    let mut core = libc::rlimit {
        rlim_cur: 1,
        rlim_max: 0,
    };
    unsafe { libc::getrlimit(libc::RLIMIT_CORE, &mut core) };
    assert_eq!(core.rlim_cur, 0);
}

// ------------------------------------------------------------------ D1-T7, T7b, T8

#[test]
fn d1_t7_scratch_is_a_fresh_private_cwd_never_shared() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let a = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    let b = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    let uid = unsafe { libc::getuid() }.to_string();
    for r in [&a, &b] {
        assert_eq!(r.get("cwd_mode"), "700");
        assert_eq!(r.get("cwd_uid"), uid);
        // D1-T7b: empty at spawn.
        assert_eq!(r.get("cwd_entries"), "0");
        assert_eq!(
            Some(r.get("cwd_ino").parse::<u64>().unwrap()),
            r.scratch_ino
        );
    }
    assert_ne!(a.get("cwd_ino"), b.get("cwd_ino"));
    // The root itself is private and named as item 6 says.
    assert!(root.leaf().starts_with("opensip-scratch-"));
    assert_eq!(root.leaf().len(), "opensip-scratch-".len() + 32);
    let meta = std::fs::metadata(root.path()).unwrap();
    assert_eq!(meta.mode() & 0o7777, 0o700);
}

#[test]
fn d1_t8_the_sweep_removes_a_dead_owner_and_never_follows_a_link() {
    let dir = test_dir();
    let outside = dir.0.join("outside-target");
    std::fs::write(&outside, b"keep").unwrap();
    // A dead owner: a scratch root whose lock is released (dropped), left on disk.
    let dead_path = {
        let mut dead = root_in(&dir);
        let r = run(
            DescriptorSet::Provider,
            ChildEnvironment::rust(),
            "report",
            &mut dead,
        );
        assert_eq!(r.code, Some(0));
        let p = dead.path().to_path_buf();
        std::os::unix::fs::symlink(&outside, p.join("planted-link")).unwrap();
        std::fs::create_dir(p.join("nested")).unwrap();
        std::os::unix::fs::symlink(&dir.0, p.join("nested").join("dir-link")).unwrap();
        p
    };
    // A live owner, holding its lock.
    let live = root_in(&dir);
    let sweeper = root_in(&dir);
    let removed = sweeper.sweep().unwrap();
    assert_eq!(
        removed,
        [dead_path
            .file_name()
            .unwrap()
            .to_string_lossy()
            .into_owned()]
    );
    assert!(!dead_path.exists());
    assert!(live.path().exists());
    assert_eq!(std::fs::read(&outside).unwrap(), b"keep");
    assert!(dir.0.exists());
}

// ------------------------------------------------------------------ item 4: exit, reap, group

#[test]
fn the_exit_source_fires_on_the_unreaped_child_which_stays_waitable() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let mut child = spawn(
        VerifiedLaunch::from_recheck(
            fixture_spec(DescriptorSet::Provider, ChildEnvironment::rust(), "exit7"),
            recheck(),
        ),
        &mut root,
    )
    .unwrap();
    let status = child
        .wait_exit(Duration::from_secs(30))
        .unwrap()
        .expect("exit");
    assert_eq!(status.code(), Some(7));
    assert!(child.has_exited().unwrap());
    // Still unreaped: the group can be signalled (its id is reserved).
    assert!(child.signal_group(0).is_ok() || child.has_exited().unwrap());
    let reaped = child.reap().unwrap();
    assert_eq!(reaped.status.code(), Some(7));
    // The reap-last rule.
    assert!(matches!(
        child.signal_group(libc::SIGTERM),
        Err(LaunchError::GroupAfterReap)
    ));
    assert!(matches!(child.reap(), Err(LaunchError::AlreadyReaped)));
}

#[test]
fn group_membership_comes_from_enumeration() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let mut child = spawn(
        VerifiedLaunch::from_recheck(
            fixture_spec(DescriptorSet::Provider, ChildEnvironment::rust(), "hold"),
            recheck(),
        ),
        &mut root,
    )
    .unwrap();
    let pid = child.process_id();
    assert_eq!(group_members(pid).unwrap(), [pid]);
    // Release the child: close its stdin.
    drop(child.take_host_end(0));
    child
        .wait_exit(Duration::from_secs(30))
        .unwrap()
        .expect("exit");
    child.reap().unwrap();
}

// ------------------------------------------------------------------ structural

#[test]
fn process_rs_spawns_by_path_only() {
    let source = include_str!("process.rs");
    let code: String = source
        .lines()
        .filter(|l| !l.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n");
    for banned in [
        "posix_spawnp(",
        "Command::new(",
        "execvp(",
        "execlp(",
        "execvpe(",
    ] {
        assert!(!code.contains(banned), "{banned}");
    }
    assert!(code.contains("libc::posix_spawn("));
    assert!(code.contains("POSIX_SPAWN_SETSID"));
    assert!(code.contains("POSIX_SPAWN_CLOEXEC_DEFAULT"));
}

// ------------------------------------------------------------------ D1a plan r2

#[test]
fn the_host_write_ends_carry_no_sigpipe_and_the_read_ends_are_untouched() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let mut child = spawn(
        VerifiedLaunch::from_recheck(
            fixture_spec(DescriptorSet::Provider, ChildEnvironment::rust(), "hold"),
            recheck(),
        ),
        &mut root,
    )
    .unwrap();
    // F_GETNOSIGPIPE, `sys/fcntl.h:294`.
    const F_GETNOSIGPIPE: libc::c_int = 74;
    let mut ends = Vec::new();
    for slot in 0..5 {
        ends.push(child.take_host_end(slot).unwrap());
    }
    for (slot, end) in ends.iter().enumerate() {
        let nosigpipe = unsafe { libc::fcntl(end.as_raw_fd(), F_GETNOSIGPIPE) };
        let expected = if slot == 0 || slot == 3 { 1 } else { 0 };
        assert_eq!(nosigpipe, expected, "slot {slot}");
    }
    drop(ends);
    child
        .wait_exit(Duration::from_secs(30))
        .unwrap()
        .expect("exit");
    child.reap().unwrap();
}

#[test]
fn addchdir_falls_back_to_the_np_form_when_the_new_symbol_is_absent() {
    let dir = test_dir();
    let mut root = root_in(&dir);
    let r = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    assert_eq!(LAST_CHDIR.with(|l| l.get()), "addchdir");
    assert_eq!(
        Some(r.get("cwd_ino").parse::<u64>().unwrap()),
        r.scratch_ino
    );
    FORCE_NP.with(|f| f.set(true));
    let r = run(
        DescriptorSet::Provider,
        ChildEnvironment::rust(),
        "report",
        &mut root,
    );
    FORCE_NP.with(|f| f.set(false));
    assert_eq!(LAST_CHDIR.with(|l| l.get()), "addchdir_np");
    assert_eq!(
        Some(r.get("cwd_ino").parse::<u64>().unwrap()),
        r.scratch_ino
    );
}

// ------------------------------------------------------------------ D1a r1 findings

fn alive(pid: i32) -> bool {
    unsafe { libc::kill(pid, 0) == 0 }
}
fn eventually_gone(pid: i32) -> bool {
    for _ in 0..200 {
        if !alive(pid) {
            return true;
        }
        std::thread::sleep(Duration::from_millis(25));
    }
    false
}

#[test]
fn a_child_keeps_its_scratch_root_and_lock_after_the_root_is_dropped() {
    // RF-1: dropping `ScratchRoot` while a child or a taken scratch lives
    // keeps the root's descriptors and lock, so a sibling sweep keeps it.
    let dir = test_dir();
    let mut root = root_in(&dir);
    let root_path = root.path().to_path_buf();
    let mut child = spawn(
        VerifiedLaunch::from_recheck(
            fixture_spec(DescriptorSet::Provider, ChildEnvironment::rust(), "hold"),
            recheck(),
        ),
        &mut root,
    )
    .unwrap();
    drop(root);
    // Descriptor churn, so a closed root descriptor would have been reused.
    let churn: Vec<File> = (0..32).map(|_| File::open("/dev/null").unwrap()).collect();
    let sweeper = root_in(&dir);
    assert_eq!(sweeper.sweep().unwrap(), Vec::<String>::new());
    assert!(root_path.exists());
    drop(child.take_host_end(0));
    child
        .wait_exit(Duration::from_secs(30))
        .unwrap()
        .expect("exit");
    child.reap().unwrap();
    let scratch = child.take_scratch().unwrap();
    let scratch_path = scratch.path().to_path_buf();
    drop(child);
    assert!(
        sweeper.sweep().unwrap().is_empty(),
        "the taken scratch still holds the lock"
    );
    scratch.remove().unwrap();
    assert!(!scratch_path.exists());
    assert!(root_path.exists());
    drop(churn);
    // The last owner is gone: the root's lock is free, and a sweep removes it.
    // The lock file is now free. Another test's fork may briefly share the
    // open file description between its fork and its exec, which only makes
    // a sweeper keep the root a little longer, so both are retried.
    let mut free = false;
    for _ in 0..200 {
        let probe = File::open(root_path.join("lock")).unwrap();
        free = unsafe { libc::flock(probe.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } == 0;
        drop(probe);
        if free {
            break;
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    assert!(free, "the dropped root's lock is still held");
    let mut removed = Vec::new();
    for _ in 0..200 {
        removed = sweeper.sweep().unwrap();
        if !removed.is_empty() {
            break;
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    assert_eq!(removed.len(), 1);
    assert!(!root_path.exists());
}

#[test]
fn the_sweep_never_removes_a_root_it_could_not_lock() {
    // RF-2: an unlocked-looking sibling without a lock file, and one whose
    // lock cannot be opened, are kept; only a lock this sweep takes proves
    // death.
    let dir = test_dir();
    let no_lock = dir.0.join("opensip-scratch-nolock");
    std::fs::create_dir(&no_lock).unwrap();
    std::fs::set_permissions(&no_lock, std::fs::Permissions::from_mode(0o700)).unwrap();
    let unreadable = dir.0.join("opensip-scratch-unreadable");
    std::fs::create_dir(&unreadable).unwrap();
    std::fs::set_permissions(&unreadable, std::fs::Permissions::from_mode(0o700)).unwrap();
    std::fs::write(unreadable.join("lock"), b"").unwrap();
    std::fs::set_permissions(
        unreadable.join("lock"),
        std::fs::Permissions::from_mode(0o000),
    )
    .unwrap();
    let sweeper = root_in(&dir);
    assert!(sweeper.sweep().unwrap().is_empty());
    assert!(no_lock.exists() && unreadable.exists());
    std::fs::set_permissions(
        unreadable.join("lock"),
        std::fs::Permissions::from_mode(0o600),
    )
    .unwrap();
}

#[test]
fn two_concurrent_sweepers_remove_a_dead_root_once_and_creation_is_never_swept() {
    // RF-2: a dead root (its owner dropped) is removed exactly once by two
    // concurrent sweepers; roots created during the sweeps are never removed
    // while their owners live.
    let dir = test_dir();
    let dead_path = {
        let dead = root_in(&dir);
        dead.path().to_path_buf()
    };
    let parent = dir.0.clone();
    let sweepers: Vec<_> = (0..2)
        .map(|_| {
            let parent = parent.clone();
            std::thread::spawn(move || {
                let me = ScratchRoot::create_in(open_dir(&parent)).unwrap();
                let mut removed = Vec::new();
                for _ in 0..20 {
                    removed.extend(me.sweep().unwrap());
                }
                (me, removed)
            })
        })
        .collect();
    let creators: Vec<ScratchRoot> = (0..20).map(|_| root_in(&dir)).collect();
    let results: Vec<_> = sweepers.into_iter().map(|h| h.join().unwrap()).collect();
    let removed: Vec<&String> = results.iter().flat_map(|(_, r)| r).collect();
    assert_eq!(removed.len(), 1, "{removed:?}");
    assert!(!dead_path.exists());
    for live in &creators {
        assert!(live.path().exists());
    }
    for (me, _) in &results {
        assert!(me.path().exists());
    }
}

#[test]
fn dropping_a_live_child_reaps_it_through_interrupted_waits() {
    // RF-3: three injected EINTRs before the real wait; the child is reaped
    // exactly, and nothing is left to wait for.
    let dir = test_dir();
    let mut root = root_in(&dir);
    let mut child = spawn(
        VerifiedLaunch::from_recheck(
            fixture_spec(DescriptorSet::Provider, ChildEnvironment::rust(), "hold"),
            recheck(),
        ),
        &mut root,
    )
    .unwrap();
    let pid = child.process_id();
    let ends: Vec<File> = (0..5)
        .filter_map(|slot| child.take_host_end(slot))
        .collect();
    INJECT_EINTR.with(|c| c.set(3));
    drop(child);
    assert_eq!(INJECT_EINTR.with(|c| c.get()), 0);
    drop(ends);
    let mut status = 0;
    let rc = unsafe { libc::waitpid(pid, &mut status, libc::WNOHANG) };
    assert_eq!(rc, -1);
    assert_eq!(
        std::io::Error::last_os_error().raw_os_error(),
        Some(libc::ECHILD)
    );
}

#[test]
fn a_setup_failure_after_the_spawn_kills_the_childs_whole_group() {
    // RF-4: the exit source fails after the child has forked a descendant;
    // the spawn returns the error, and the descendant is killed with its
    // group.
    let dir = test_dir();
    let mut root = root_in(&dir);
    FAIL_EXIT_SOURCE.with(|f| f.set(Some(Duration::from_millis(500))));
    let result = spawn(
        VerifiedLaunch::from_recheck(
            fixture_spec(
                DescriptorSet::Provider,
                ChildEnvironment::rust(),
                "descendant",
            ),
            recheck(),
        ),
        &mut root,
    );
    FAIL_EXIT_SOURCE.with(|f| f.set(None));
    assert!(
        matches!(result, Err(LaunchError::Io { call: "kqueue", .. })),
        "{result:?}"
    );
    let scratch = std::fs::read_dir(root.path())
        .unwrap()
        .filter_map(Result::ok)
        .map(|e| e.path())
        .find(|p| {
            p.file_name()
                .is_some_and(|n| n.to_string_lossy().starts_with("child-"))
        })
        .expect("the child's scratch");
    let grandchild: i32 = std::fs::read_to_string(scratch.join("grandchild.pid"))
        .expect("the descendant wrote its pid")
        .trim()
        .parse()
        .unwrap();
    assert!(
        eventually_gone(grandchild),
        "descendant {grandchild} survived"
    );
}
