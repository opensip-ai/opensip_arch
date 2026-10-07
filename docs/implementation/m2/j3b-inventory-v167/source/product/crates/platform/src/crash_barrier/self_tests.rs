//! Law X9 r1 item 12's X9-0 self-tests. Each test re-executes this test
//! binary as a matrix child running `matrix_child` (which returns at once in
//! the parent's own run), drives it through its stderr records and stdin,
//! and checks the state a real process death or an injected failure leaves.
use super::driver::{Census, CensusPoint, ChildSpec, Exit, HarnessError, MatrixChild, Record};
use super::{
    Action, Arm, Fault, HARNESS_EXIT_CODE, Occurrence, child_role, is_durability_point, parse_arms,
    report_outcome, validate_point,
};
use crate::crash_matrix_tests::{
    ACCOUNTED, EXPECTED_OUTCOME, REPLACED, Scratch, expected_listing, listing, workload,
};
use crate::{FileLock, LockMode, RetainedDirectory};
use std::fs::{self, File};
use std::os::unix::process::ExitStatusExt;
use std::path::{Path, PathBuf};
use std::time::Duration;

const ENTRY: &str = "crash_barrier::self_tests::matrix_child";

fn field(input: &str, key: &str) -> String {
    input
        .lines()
        .find_map(|line| line.strip_prefix(&format!("{key}=")))
        .unwrap_or_default()
        .to_owned()
}

// Two threads: main holds at `x9.selftest.main-hold`; the side thread holds
// at a read-only tick, then reports a read-only or a durability point.
fn observer(durable: bool) -> String {
    let side = std::thread::spawn(move || {
        crate::crash_barrier!("x9.selftest-observer", "tick", step);
        if durable {
            crate::crash_barrier!("x9.selftest", "side-durable", step);
        } else {
            crate::crash_barrier!("x9.selftest-observer", "after-tick", step);
        }
        crate::crash_barrier!("x9.selftest-observer", "side-done", step);
    });
    crate::crash_barrier!("x9.selftest", "main-hold", step);
    side.join().unwrap();
    "observer=ok".to_owned()
}

// The protocol-site kinds: a gate, a fallible step and the draw.
fn kinds() -> String {
    let (gate, commit) = crate::crash_scope!("x9.selftest", {
        let mut waited = false;
        crate::crash_barrier!(_, "tick", gate, waited = true);
        let commit: Result<u8, String> =
            crate::crash_barrier!(_, "commit", fallible, Ok(7), |fault: Fault| format!(
                "{fault:?}"
            ));
        (if waited { "waited" } else { "rendezvous" }, commit)
    });
    let id = crate::crash_scope!("x3d.session", {
        crate::crash_barrier!(
            _,
            "execution-draw",
            draw,
            String::from("exec1_drawn"),
            |id: &str| id.to_owned(),
            |value: &String| value.clone()
        )
    });
    format!("gate={gate};commit={commit:?};draw={id}")
}

// Law X9 r2 item 3: `count` wall readings through `observe_clock`, each
// as `<seconds>.<nanos>`, and whether the monotonic readings moved forward.
fn clock_readings(count: usize) -> String {
    let mut walls = Vec::new();
    let mut monotonic = Vec::new();
    for _ in 0..count {
        let observed = crate::observe_clock().unwrap();
        walls.push(format!(
            "{}.{}",
            observed.wall_unix_seconds(),
            observed.wall_nanoseconds()
        ));
        monotonic.push(observed.monotonic_before());
    }
    let forward = monotonic.windows(2).all(|w| w[0] <= w[1]);
    format!("clock={};monotonic-forward={forward}", walls.join(","))
}

/// The matrix child entry. In the parent's own run it returns at once.
#[test]
fn matrix_child() {
    let Some((role, input)) = child_role() else {
        return;
    };
    let input = fs::read_to_string(input).unwrap();
    let root = PathBuf::from(field(&input, "root"));
    let outcome = match role.as_str() {
        "workload" => workload(&root),
        "unscoped" => {
            let dir = RetainedDirectory::from_retained_handle(File::open(&root).unwrap()).unwrap();
            match dir.replace_regular("unscoped", REPLACED) {
                Ok(_) => "unscoped=ok".to_owned(),
                Err(e) => format!("unscoped=err:{:?}", e.stage()),
            }
        }
        "observer" => observer(field(&input, "variant") == "durable"),
        "signal-input" => {
            let main = std::thread::current().id();
            let delivered = std::sync::Arc::new(std::sync::Mutex::new(Vec::new()));
            let captured = delivered.clone();
            let registration = super::register_signal_input(move |signal| {
                assert_ne!(std::thread::current().id(), main);
                captured.lock().unwrap().push(signal.as_str());
            });
            crate::crash_barrier!("x9.selftest", "main-hold", step);
            drop(registration);
            let values = delivered.lock().unwrap();
            format!("signals={}", values.join(","))
        }
        "signal-unregistered" => {
            crate::crash_barrier!("x9.selftest", "main-hold", step);
            "unexpected-resume".into()
        }
        "kinds" => kinds(),
        "clock" => clock_readings(field(&input, "variant").parse().unwrap()),
        other => panic!("unknown matrix child role {other}"),
    };
    report_outcome(&outcome);
    println!("\nOUTCOME {outcome}");
}

struct Run {
    scratch: Scratch,
    child: MatrixChild,
}

fn start(role: &str, arms: Option<&str>, variant: &str) -> Run {
    start_watched(role, arms, variant, None)
}

fn start_watched(role: &str, arms: Option<&str>, variant: &str, watchdog: Option<Duration>) -> Run {
    let scratch = Scratch::new("selftest");
    let input = scratch.parent.join("input");
    fs::write(
        &input,
        format!("root={}\nvariant={variant}\n", scratch.root().display()),
    )
    .unwrap();
    let spec = ChildSpec {
        entry: ENTRY,
        role,
        input: &input,
        arms,
        clock: None,
        scratch_parent: &scratch.parent,
    };
    let child = match watchdog {
        Some(limit) => MatrixChild::spawn_with_watchdog(&spec, limit),
        None => MatrixChild::spawn(&spec),
    }
    .unwrap();
    Run { scratch, child }
}

fn staging(root: &Path) -> Vec<(String, Option<Vec<u8>>)> {
    listing(root)
        .into_iter()
        .filter(|(name, _)| name.starts_with(".opensip-stage-"))
        .collect()
}

fn events(exit: &Exit, point: &str) -> Vec<String> {
    exit.records
        .iter()
        .filter(|r| r.point == point)
        .map(|r| r.event.clone())
        .collect()
}

#[test]
fn a_kill_at_a_platform_point_is_a_verified_process_death() {
    // After the rename and before the directory barrier: the new bytes are
    // visible, then the process dies.
    let point = "x9.selftest.replace/rename.after#1";
    let mut run = start("workload", Some(&format!("{point}=hold")), "");
    let held = run.child.await_held(point).unwrap();
    assert_eq!(held.payload, "");
    assert_eq!(
        listing(&run.scratch.root()),
        vec![("replaced".to_owned(), Some(REPLACED.to_vec()))]
    );
    let exit = run.child.kill().unwrap();
    exit.verify_death_at(point).unwrap();
    assert_eq!(exit.status.signal(), Some(9));
    assert!(exit.outcome().is_none());
    assert_eq!(
        exit.verify_death_at("x9.selftest.replace/rename.before#1"),
        Err(HarnessError::NotReached(
            "x9.selftest.replace/rename.before#1".to_owned()
        ))
    );
    assert!(matches!(exit.verify_finished(), Err(HarnessError::Exit(_))));

    // Before the staging write: the empty staging file stays, because a
    // killed process runs no destructor; the target never appears.
    let point = "x9.selftest.replace/write.before#1";
    let mut run = start("workload", Some(&format!("{point}=hold")), "");
    run.child.await_held(point).unwrap();
    let exit = run.child.kill().unwrap();
    exit.verify_death_at(point).unwrap();
    let left = listing(&run.scratch.root());
    assert_eq!(left.len(), 1);
    assert!(left[0].0.starts_with(".opensip-stage-"));
    assert_eq!(left[0].1, Some(Vec::new()));

    // A held flock is the kernel's until the process dies.
    let point = "x9.selftest.lock/lock.after#1";
    let mut run = start("workload", Some(&format!("{point}=hold")), "");
    run.child.await_held(point).unwrap();
    let lease = run.scratch.root().join("lease");
    assert!(
        FileLock::try_acquire(File::open(&lease).unwrap(), LockMode::Exclusive)
            .unwrap()
            .is_none()
    );
    let exit = run.child.kill().unwrap();
    exit.verify_death_at(point).unwrap();
    assert!(
        FileLock::try_acquire(File::open(&lease).unwrap(), LockMode::Exclusive)
            .unwrap()
            .is_some()
    );
}

#[test]
fn hold_then_resume_completes_the_lawful_run() {
    let first = "x9.selftest.publish/link.before#1";
    let second = "x9.selftest.accounted/write.after#1";
    let mut run = start("workload", Some(&format!("{first}=hold,{second}=hold")), "");
    run.child.await_held(first).unwrap();
    assert!(!run.scratch.root().join("published").exists());
    run.child.resume(first).unwrap();
    run.child.await_held(second).unwrap();
    assert_eq!(
        fs::read(run.scratch.root().join("accounted.tmp")).unwrap(),
        ACCOUNTED
    );
    assert!(run.child.resume(first).is_err());
    run.child.resume(second).unwrap();
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some(EXPECTED_OUTCOME));
    assert_eq!(listing(&run.scratch.root()), expected_listing());
    assert_eq!(events(&exit, first), ["held", "resumed"]);
    assert_eq!(events(&exit, second), ["held", "resumed"]);

    // The law's bare `resume` reaches the one held thread.
    let point = "x9.selftest.confirm/reopen-confirm.after#1";
    let mut run = start("workload", Some(&format!("{point}=hold")), "");
    run.child.await_held(point).unwrap();
    run.child.control_line("resume").unwrap();
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some(EXPECTED_OUTCOME));
}

#[test]
fn fail_before_and_fail_after_return_the_native_failure() {
    let present = |root: &Path, name: &str| root.join(name).exists();
    for (arm, outcome, replaced) in [
        (
            "x9.selftest.replace/rename.before#1=fail-before",
            "replace=err:Rename:Indeterminate:5",
            false,
        ),
        (
            "x9.selftest.replace/rename.after#1=fail-after",
            "replace=err:Rename:Indeterminate:5",
            true,
        ),
        (
            "x9.selftest.replace/file-barrier.before#1=fail-before",
            "replace=err:SyncTemporary:Unchanged:5",
            false,
        ),
        (
            "x9.selftest.replace/file-barrier.after#1=fail-after",
            "replace=err:SyncTemporary:Unchanged:5",
            false,
        ),
        (
            "x9.selftest.replace/directory-barrier.before#1=fail-before",
            "replace=err:SyncDirectory:Indeterminate:5",
            true,
        ),
    ] {
        let Run { scratch, child } = start("workload", Some(arm), "");
        let exit = child.finish().unwrap();
        exit.verify_finished().unwrap();
        let reported = exit.outcome().unwrap();
        assert!(
            reported.starts_with(&format!("{outcome};")),
            "{arm}: {reported}"
        );
        assert!(reported.ends_with(";publish=ok;confirm=ok;accounted=ok;lock=ok"));
        assert_eq!(present(&scratch.root(), "replaced"), replaced, "{arm}");
        // The process survived, so the primitive's own cleanup ran.
        assert!(staging(&scratch.root()).is_empty(), "{arm}");
        let (point, action) = arm.split_once('=').unwrap();
        assert_eq!(events(&exit, point), [action], "{arm}");
    }
    // The accounted forms fail the same way and leave their effect.
    let arm = "x9.selftest.accounted/directory-barrier.after#1=fail-after";
    let run = start("workload", Some(arm), "");
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    let reported = exit.outcome().unwrap();
    assert!(
        reported.contains(";accounted=err:barrier:Os { code: 5,"),
        "{reported}"
    );
    assert!(run.scratch.root().join("accounted").exists());
    assert!(!run.scratch.root().join("made").exists());
}

#[test]
fn a_torn_write_leaves_half_the_bytes_then_holds() {
    let point = "x9.selftest.replace/write.before#1";
    let mut run = start("workload", Some(&format!("{point}=torn")), "");
    let held = run.child.await_held(point).unwrap();
    assert_eq!(held.payload, "torn");
    let left = staging(&run.scratch.root());
    assert_eq!(left.len(), 1);
    assert_eq!(left[0].1.as_deref(), Some(&REPLACED[..REPLACED.len() / 2]));
    let exit = run.child.kill().unwrap();
    exit.verify_death_at(point).unwrap();
    assert!(!run.scratch.root().join("replaced").exists());

    // Resumed, the torn write is a failed write and the process cleans up.
    let mut run = start("workload", Some(&format!("{point}=torn")), "");
    run.child.await_held(point).unwrap();
    run.child.resume(point).unwrap();
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert!(
        exit.outcome()
            .unwrap()
            .starts_with("replace=err:WriteTemporary:Unchanged:5;")
    );
    assert!(staging(&run.scratch.root()).is_empty());
    assert!(!run.scratch.root().join("replaced").exists());

    // The accounted write tears its new file the same way.
    let point = "x9.selftest.accounted/write.before#1";
    let mut run = start("workload", Some(&format!("{point}=torn")), "");
    run.child.await_held(point).unwrap();
    assert_eq!(
        fs::read(run.scratch.root().join("accounted.tmp")).unwrap(),
        &ACCOUNTED[..ACCOUNTED.len() / 2]
    );
    run.child.kill().unwrap().verify_death_at(point).unwrap();
}

fn census_point(name: &str, occurrences: u32) -> CensusPoint {
    CensusPoint {
        name: name.to_owned(),
        occurrences,
        durability: true,
    }
}

// The platform points the workload reaches, each `.before` and `.after`.
fn expected_census() -> Vec<CensusPoint> {
    let mut points = Vec::new();
    for (scope, steps) in [
        (
            "accounted",
            &[
                "create",
                "write",
                "file-barrier",
                "rename",
                "directory-barrier",
            ][..],
        ),
        (
            "confirm",
            &["file-barrier", "directory-barrier", "reopen-confirm"][..],
        ),
        ("lock", &["create", "lock", "unlock"][..]),
        (
            "publish",
            &[
                "create",
                "write",
                "file-barrier",
                "link",
                "directory-barrier",
            ][..],
        ),
        (
            "replace",
            &[
                "create",
                "write",
                "file-barrier",
                "rename",
                "directory-barrier",
            ][..],
        ),
    ] {
        for step in steps {
            // The accounted scope creates a file and then a directory.
            let n = if scope == "accounted" && *step == "create" {
                2
            } else {
                1
            };
            for phase in ["after", "before"] {
                points.push(census_point(
                    &format!("x9.selftest.{scope}/{step}.{phase}"),
                    n,
                ));
            }
        }
    }
    points.sort_by(|a, b| a.name.cmp(&b.name));
    points
}

#[test]
fn an_unarmed_child_matches_the_featureless_run_and_records_the_census() {
    // No OPENSIP_X9_ARMS: every point is a OnceLock read and a return, so
    // the child writes no record and leaves the featureless outcome and tree.
    let run = start("workload", None, "");
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert!(exit.records.is_empty(), "{:?}", exit.records);
    assert!(
        exit.stdout
            .contains(&format!("OUTCOME {EXPECTED_OUTCOME}\n"))
    );
    assert_eq!(listing(&run.scratch.root()), expected_listing());

    // Traced with nothing armed: the same outcome and tree, and the census.
    let run = start("workload", Some(""), "");
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some(EXPECTED_OUTCOME));
    assert_eq!(listing(&run.scratch.root()), expected_listing());
    assert!(exit.records.iter().all(|r| r.pid == exit.records[0].pid));
    let census = Census::from_exit(&exit).unwrap();
    assert_eq!(census.points, expected_census());
    let kills = census.kill_set();
    // 42 points at #1, and the accounted creates' second occurrence.
    assert_eq!(kills.len(), 44);
    assert!(kills.contains(&"x9.selftest.accounted/create.before#2".to_owned()));
    assert!(kills.contains(&"x9.selftest.replace/rename.after#1".to_owned()));
    // The trace is reproducible apart from the process id.
    let again = start("workload", Some(""), "").child.finish().unwrap();
    assert_eq!(again.trace(), exit.trace());

    // A census needs a traced child with nothing armed.
    let armed = start("workload", Some("x9.selftest.lock/unlock.after#1=hold"), "");
    let mut child = armed.child;
    child.await_held("x9.selftest.lock/unlock.after#1").unwrap();
    child.resume("x9.selftest.lock/unlock.after#1").unwrap();
    let exit = child.finish().unwrap();
    assert!(matches!(
        Census::from_exit(&exit),
        Err(HarnessError::Arms(_))
    ));
}

#[test]
fn an_armed_point_never_reached_is_a_harness_error() {
    let point = "x9.selftest.replace/rename.after";
    let run = start("workload", Some(&format!("{point}#2=hold")), "");
    let exit = run.child.finish().unwrap();
    assert_eq!(
        exit.verify_finished(),
        Err(HarnessError::NotReached(point.to_owned()))
    );
    let run = start("workload", Some("x9.selftest.never.reached#1=hold"), "");
    let mut child = run.child;
    assert_eq!(
        child.await_held("x9.selftest.never.reached#1"),
        Err(HarnessError::NotReached(
            "x9.selftest.never.reached#1".to_owned()
        ))
    );
}

#[test]
fn an_action_the_point_kind_does_not_admit_is_a_harness_error_in_the_child() {
    for arm in [
        "x9.selftest.replace/create.before#1=fail-before",
        "x9.selftest.replace/rename.before#1=torn",
        "x9.selftest.replace/rename.before#1=fail-after",
        "x9.selftest.replace/rename.after#1=fail-before",
        "x9.selftest.replace/write.after#1=torn",
        "x9.selftest.lock/lock.before#1=fail-before",
    ] {
        let run = start("workload", Some(arm), "");
        let exit = run.child.finish().unwrap();
        assert_eq!(exit.status.code(), Some(HARNESS_EXIT_CODE), "{arm}");
        match exit.verify_finished() {
            Err(HarnessError::Child(reason)) => {
                assert!(reason.contains("not admitted"), "{reason}")
            }
            other => panic!("{arm}: {other:?}"),
        }
    }
    // A malformed arming never starts a child.
    assert!(matches!(
        MatrixChild::spawn(&ChildSpec {
            entry: ENTRY,
            role: "workload",
            input: Path::new("/nonexistent"),
            arms: Some("x9.selftest.replace/fsync.before#1=hold"),
            clock: None,
            scratch_parent: Path::new("/nonexistent"),
        }),
        Err(HarnessError::Arms(_))
    ));
}

#[test]
fn a_primitive_outside_any_scope_is_a_harness_error() {
    let run = start("unscoped", Some(""), "");
    let exit = run.child.finish().unwrap();
    match exit.verify_finished() {
        Err(HarnessError::Child(reason)) => {
            assert!(reason.contains("create outside any scope"), "{reason}")
        }
        other => panic!("{other:?}"),
    }
    // Untraced, the same child is unaffected.
    let run = start("unscoped", None, "");
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert!(exit.stdout.contains("OUTCOME unscoped=ok\n"));
}

const MAIN: &str = "x9.selftest.main-hold#1";
const TICK: &str = "x9.selftest-observer.tick#1";
const DONE: &str = "x9.selftest-observer.side-done#1";

fn two_holds(variant: &str) -> Run {
    let mut run = start(
        "observer",
        Some(&format!("{MAIN}=hold,{TICK}=hold")),
        variant,
    );
    run.child.await_held(MAIN).unwrap();
    run.child.await_held(TICK).unwrap();
    run
}

#[test]
fn resumes_are_addressed_and_only_read_only_points_may_follow_a_kill_point() {
    // Two held threads: the parent resumes the side thread, then main.
    let mut run = two_holds("read-only");
    run.child.resume(TICK).unwrap();
    run.child.await_event(DONE, "pass").unwrap();
    run.child.resume(MAIN).unwrap();
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some("observer=ok"));
    let resumed: Vec<&Record> = exit
        .records
        .iter()
        .filter(|r| r.event == "resumed")
        .collect();
    assert_eq!(resumed[0].point, TICK);
    assert_eq!(resumed[1].point, MAIN);
    assert_ne!(resumed[0].thread, resumed[1].thread);

    // Killed at main's hold after the side thread ran read-only points.
    let mut run = two_holds("read-only");
    run.child.resume(TICK).unwrap();
    run.child.await_event(DONE, "pass").unwrap();
    run.child.kill().unwrap().verify_death_at(MAIN).unwrap();

    // A durability point after the kill point fails the death check.
    let mut run = two_holds("durable");
    run.child.resume(TICK).unwrap();
    run.child.await_event(DONE, "pass").unwrap();
    match run.child.kill().unwrap().verify_death_at(MAIN) {
        Err(HarnessError::AfterKillPoint(record)) => {
            assert_eq!(record, "x9.selftest.side-durable#1 pass")
        }
        other => panic!("{other:?}"),
    }

    // A bare `resume` with two threads held names no single point.
    let mut run = two_holds("read-only");
    run.child.control_line("resume").unwrap();
    let exit = run.child.finish().unwrap();
    match exit.verify_finished() {
        Err(HarnessError::Child(reason)) => assert!(reason.contains("names no held point")),
        other => panic!("{other:?}"),
    }
}

#[test]
fn the_watchdog_kills_a_stuck_child_as_a_harness_error() {
    let point = "x9.selftest.replace/rename.before#1";
    let mut run = start_watched(
        "workload",
        Some(&format!("{point}=hold")),
        "",
        Some(Duration::from_secs(1)),
    );
    run.child.await_held(point).unwrap();
    // Never resumed: only the watchdog ends the run.
    let exit = run.child.finish().unwrap();
    assert!(exit.watchdog_fired);
    assert_eq!(exit.verify_finished(), Err(HarnessError::Watchdog));
    assert_eq!(exit.verify_death_at(point), Err(HarnessError::Watchdog));
}

#[test]
fn gate_fallible_and_draw_points_at_protocol_sites() {
    let run = start("kinds", Some(""), "");
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(
        exit.outcome(),
        Some("gate=waited;commit=Ok(7);draw=exec1_drawn")
    );
    let draw = exit
        .records
        .iter()
        .find(|r| r.point == "x3d.session.execution-draw#1")
        .unwrap();
    assert_eq!(
        (draw.event.as_str(), draw.payload.as_str()),
        ("pass", "exec1_drawn")
    );
    assert_eq!(events(&exit, "x9.selftest.commit.before#1"), ["pass"]);

    let arms = "x9.selftest.tick#1=hold,x9.selftest.commit.after#1=fail-after,\
                x3d.session.execution-draw#1=inject-id:exec1_injected";
    let mut run = start("kinds", Some(arms), "");
    run.child.await_held("x9.selftest.tick#1").unwrap();
    run.child.resume("x9.selftest.tick#1").unwrap();
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(
        exit.outcome(),
        Some("gate=rendezvous;commit=Err(\"After\");draw=exec1_injected")
    );

    let run = start("kinds", Some("x9.selftest.commit.before#1=fail-before"), "");
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(
        exit.outcome(),
        Some("gate=waited;commit=Err(\"Before\");draw=exec1_drawn")
    );

    // `inject-id` is admitted at the draw point only, and only kind `draw`
    // admits it.
    let run = start("kinds", Some("x3d.session.execution-draw#1=torn"), "");
    let exit = run.child.finish().unwrap();
    assert!(matches!(
        exit.verify_finished(),
        Err(HarnessError::Child(_))
    ));
}

#[test]
fn the_arming_grammar_and_point_names() {
    assert_eq!(parse_arms("").unwrap(), []);
    assert_eq!(
        parse_arms(
            "x3b.append.seal.witness-pending/rename.after#1=hold,x3c.object/write.before#*=torn,\
             x3d.session.execution-draw#2=inject-id:exec1_ab-C_9"
        )
        .unwrap(),
        [
            Arm {
                point: "x3b.append.seal.witness-pending/rename.after".to_owned(),
                occurrence: Occurrence::Nth(1),
                action: Action::Hold
            },
            Arm {
                point: "x3c.object/write.before".to_owned(),
                occurrence: Occurrence::Every,
                action: Action::Torn
            },
            Arm {
                point: "x3d.session.execution-draw".to_owned(),
                occurrence: Occurrence::Nth(2),
                action: Action::InjectId("exec1_ab-C_9".to_owned())
            },
        ]
    );
    for refused in [
        "x3c.attempt.commit.after",
        "x3c.attempt.commit.after#0=hold",
        "x3c.attempt.commit.after#01=hold",
        "x3c.attempt.commit.after#1",
        "x3c.attempt.commit.after#1=crash",
        "x3c.attempt.commit.after#1=hold,",
        "x3c.attempt.commit.after#1=hold,x3c.attempt.commit.after#*=hold",
        "x3c.attempt.commit.after#2=hold,x3c.attempt.commit.after#2=fail-after",
        "x3c.attempt.commit.after#1=inject-id:exec1_a",
        "x3d.session.execution-draw#1=inject-id:exec2_a",
        "x3d.session.execution-draw#1=inject-id:exec1_",
        "x3d.session.execution-draw#1=inject-id:exec1_a,b",
        "x9.unknown.step#1=hold",
        "x3c.attempt#1=hold",
        "x3c.object/fsync.before#1=hold",
        "x3c.object/write#1=hold",
        "x3c.object/write.during#1=hold",
        "x3c.object/write.before/x#1=hold",
        "X3c.attempt.commit#1=hold",
        "x3c.attempt..commit#1=hold",
    ] {
        assert!(parse_arms(refused).is_err(), "accepted {refused:?}");
    }
    validate_point("x3b.end.floor/directory-barrier.before").unwrap();
    validate_point("x3c.evidence.stage-run_records").unwrap();
    assert!(is_durability_point("x6.recover/lock.after"));
    assert!(is_durability_point("x3d.publish.commit-returned"));
    assert!(!is_durability_point("x6.recover.after-lease"));
    assert!(!is_durability_point("x4.observer.tick"));
    assert!(!is_durability_point("x9.selftest-observer.tick"));
    let census = super::driver::Census {
        points: vec![
            census_point("x3c.object/write.before", 7),
            census_point("x3c.object/link.after", 2),
            census_point("x3c.object/create.after", 1),
            CensusPoint {
                name: "x6.recover.after-lease".to_owned(),
                occurrences: 1,
                durability: false,
            },
        ],
    };
    assert_eq!(
        census.kill_set(),
        [
            "x3c.object/write.before#1",
            "x3c.object/write.before#4",
            "x3c.object/write.before#7",
            "x3c.object/link.after#1",
            "x3c.object/link.after#2",
            "x3c.object/create.after#1",
        ]
    );
}

// ------------------------------------------- the scripted wall clock (r2)

fn clock_child(clock: Option<super::driver::ScriptedClock>, count: usize) -> (Scratch, Exit) {
    let scratch = Scratch::new("clock");
    let input = scratch.parent.join("input");
    fs::write(
        &input,
        format!("root={}\nvariant={count}\n", scratch.root().display()),
    )
    .unwrap();
    let exit = MatrixChild::spawn(&ChildSpec {
        entry: ENTRY,
        role: "clock",
        input: &input,
        arms: None,
        clock,
        scratch_parent: &scratch.parent,
    })
    .unwrap()
    .finish()
    .unwrap();
    (scratch, exit)
}

#[test]
fn a_scripted_clock_gives_each_ordinal_its_own_increasing_wall_seconds() {
    use super::driver::ScriptedClock;
    const E: i64 = 1_790_985_600;
    for ordinal in [0u32, 1, 2] {
        let (_scratch, exit) = clock_child(Some(ScriptedClock { epoch: E, ordinal }), 3);
        exit.verify_finished().unwrap();
        // Untraced: no record, and the outcome on stdout.
        assert!(exit.records.is_empty());
        let base = E + 3600 * i64::from(ordinal);
        assert!(
            exit.stdout.contains(&format!(
                "OUTCOME clock={}.0,{}.0,{}.0;monotonic-forward=true",
                base,
                base + 1,
                base + 2
            )),
            "{}",
            exit.stdout
        );
    }
    // Without a script the wall reading is the OS's: it lies between the
    // OS readings `date +%s` gives around the child, with a margin for a
    // small clock step. The bracket holds on any date, E's hours included,
    // and reads the clock outside this pinned file's own code.
    let os_seconds = || -> i64 {
        let out = std::process::Command::new("/bin/date")
            .arg("+%s")
            .output()
            .unwrap();
        assert!(out.status.success());
        String::from_utf8(out.stdout)
            .unwrap()
            .trim()
            .parse()
            .unwrap()
    };
    let margin = 60;
    let before = os_seconds();
    let (_scratch, exit) = clock_child(None, 1);
    let after = os_seconds();
    exit.verify_finished().unwrap();
    let line = exit
        .stdout
        .lines()
        .find(|l| l.starts_with("OUTCOME "))
        .unwrap();
    let seconds: i64 = line["OUTCOME clock=".len()..]
        .split('.')
        .next()
        .unwrap()
        .parse()
        .unwrap();
    assert!(
        (before - margin..=after + margin).contains(&seconds),
        "{seconds} outside the OS readings {before}..={after}"
    );
}

#[test]
fn a_3600th_wall_reading_is_a_harness_error() {
    use super::driver::ScriptedClock;
    let script = Some(ScriptedClock {
        epoch: 1_790_985_600,
        ordinal: 1,
    });
    let (_scratch, exit) = clock_child(script, 3600);
    exit.verify_finished().unwrap();
    let (_scratch, exit) = clock_child(script, 3601);
    assert_eq!(exit.status.code(), Some(HARNESS_EXIT_CODE));
    assert!(
        matches!(exit.verify_finished(), Err(HarnessError::Child(reason)) if reason.contains("wall reading 3600"))
    );
}

#[test]
fn the_clock_script_grammar() {
    use super::parse_clock;
    assert_eq!(parse_clock("1790985600:0"), Ok((1_790_985_600, 0)));
    assert_eq!(parse_clock("0:12"), Ok((0, 12)));
    for bad in [
        "",
        "1790985600",
        ":1",
        "1:",
        "-1:0",
        "1: 0",
        "01:0",
        "1:01",
        "1:x",
        "1.5:0",
        "9223372036854775807:0",
    ] {
        assert!(parse_clock(bad).is_err(), "accepted {bad:?}");
    }
}

#[test]
fn signal_input_acknowledges_completed_delivery_on_its_own_thread() {
    let point = "x9.selftest.main-hold#1";
    let mut run = start("signal-input", Some(&format!("{point}=hold")), "");
    let held = run.child.await_held(point).unwrap();
    for signal in [
        super::SignalInput::Sigint,
        super::SignalInput::Sigterm,
        super::SignalInput::Sighup,
    ] {
        run.child.signal(signal).unwrap();
    }
    run.child.resume(point).unwrap();
    let exit = run.child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some("signals=SIGINT,SIGTERM,SIGHUP"));
    let acknowledgements: Vec<_> = exit
        .records
        .iter()
        .filter(|r| r.event == "signalled")
        .collect();
    assert_eq!(acknowledgements.len(), 3);
    for record in acknowledgements {
        assert_eq!(record.point, "-");
        assert_ne!(record.thread, held.thread);
    }
}
#[test]
fn signal_input_rejects_unknown_names_and_missing_registration() {
    let point = "x9.selftest.main-hold#1";
    for (role, line, expected) in [
        ("signal-input", "signal SIGKILL", "unknown signal"),
        ("signal-unregistered", "signal SIGINT", "not registered"),
    ] {
        let mut run = start(role, Some(&format!("{point}=hold")), "");
        run.child.await_held(point).unwrap();
        run.child.control_line(line).unwrap();
        let exit = run.child.finish().unwrap();
        assert!(
            matches!(exit.verify_finished(), Err(HarnessError::Child(reason)) if reason.contains(expected))
        );
        assert!(!exit.records.iter().any(|r| r.event == "signalled"));
    }
}
