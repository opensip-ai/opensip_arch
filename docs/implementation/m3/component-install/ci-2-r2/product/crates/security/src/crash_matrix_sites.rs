//! Unit X9-1's pin of every source site that names a test-only feature
//! (law X9 r1 item 6: "X9-1 pins the exact list of such sites with a source
//! pin, and no other site may use the feature"; law X8 r3 item 4b: one site
//! list, one joint predicate, extended by name), and the ordinary-lane tests
//! of the shared producers. It runs in every test build of security.
//!
//! The list has four kinds of site:
//! - **Shared fixture gates**, written with the one joint predicate
//!   `any(test, feature = "crash-matrix", feature = "scenario-fixtures")`
//!   (alone, or inside `all(…, target_os = "macos")`). They are X8 r3 item
//!   4b's four named gates, the accessor X3d r8 item 13 adds by name, the
//!   emitter unit CI-1 adds by name (gate 6), the test component and the
//!   fixture store unit CI-2 adds by name (gates 7 and 8), and the closure
//!   each needs to compile and to be reached, nothing else:
//!   1. `Image::Injected` (InitialCore's injected loaded image): the variant
//!      and its ten match arms in `trust/initial_core.rs`, and that file's
//!      `tests` module, which defines the injected image and the signed test
//!      tree; with it, the synthetic V2 profile set: `trust/initial_platform.rs`'s
//!      `tests` module (the signed profile payloads and the receipt
//!      producers) and its re-exports in `trust/root_payload.rs` and
//!      `trust.rs`, the SYNTHETIC-standing admission (`cfg!`) in
//!      `trust/initial_platform.rs`, the signing test keys in
//!      `trust/core_authentication.rs` (its `tests` module and that module's
//!      one import), `InitialInstallationAttempt::for_tests`, and the test
//!      scratch parent in `lib.rs`;
//!   2. `HomeSource::Fixture` and its match arms in `admit_with`'s steps
//!      (`custody/installation_admission.rs`), in the read session's walk
//!      (`custody/installation_session.rs`) and in X6b's recovery admission
//!      (`custody/recovery_admission.rs`); with it, the real creator
//!      path on a scratch H (`create_at` and `prepare_installation_parent_at`),
//!      the write gate's test constructor (`DurableWriteGate::for_tests`),
//!      and the shared installation fixture module (`custody.rs`'s
//!      `installation_read_fixture`, whose read-session helpers stay
//!      `cfg(test)` inside it);
//!   3. X4T-0: `mod accepted_store_fixture` and its one accessor
//!      `accepted_store_files` in `trust/root_payload.rs`, re-exported by
//!      `trust.rs`;
//!   4. the fenced `state.v1` publisher `publish_store_fenced` beside the
//!      trust owner's `publish` (`trust/floor_publication.rs`), re-exported
//!      through `current_trust_admission.rs`, `ordinary_targets.rs`,
//!      `root_payload.rs` and `trust.rs`;
//!   5. (law X3d r8 item 13, unit X3d-3, added by name) the core evaluator
//!      closure's preimage accessor for the synthetic run candidate:
//!      `CommitSession::core_evaluator_closure_preimages`
//!      (`custody/commit_session.rs`), its two hops through
//!      `ProjectOperation` (`custody/operation_handoff.rs`) and the write
//!      receipt (`custody/read_premise.rs`), and the read itself,
//!      `InitialCore::evaluator_closure_preimages`, inside gate 1's
//!      `trust/initial_core.rs` `tests` module (no site of its own);
//!   6. (law CI r5 item 3, component installation plan r3 LD-CIP-3, unit
//!      CI-1, added by name) the profile-1 archive emitter, PKG-AP's byte
//!      algorithm for fixtures only, and its refusal type
//!      (`archive_profile.rs`'s `emit` and `EmitRefusal`);
//!   7. (law CI r5 item 6, component installation plan r3 LD-CIP-3 and
//!      LD-CIP-7, unit CI-2, added by name) C2a-1's `TestComponent`, the
//!      component installer's and retained-tree reader's fixture evidence:
//!      the struct and its impl (`trust_admitted_components.rs`), its
//!      re-export in `trust.rs`, and its public re-export in `lib.rs`;
//!   8. (law CI r5 item 6's fixture path, plan r3 LD-CIP-3, unit CI-2,
//!      added by name) `ComponentStore::fixture` in opensip-lifecycle's
//!      `installation.rs`, the fixture store the same installer fills.
//! - **Crash-matrix-only fixture sites**, `any(test, feature = "crash-matrix")`:
//!   the reserved-slot technique and the inherited carrier fixture in
//!   `journal_store/carrier_operation.rs` (two functions and the format enum)
//!   and their one re-export in `journal_store.rs`. Only the crash matrix
//!   calls them, so they are not on X8's shared list.
//! - **The feature's own declarations**: each crate's compile guard (law X9
//!   r1 item 2, guard 1), each crate's `crash_matrix_support` module, and
//!   unit X9-1's feature-gated census tests (security's `crash_matrix_census`
//!   and storage's X3c-2 census child); and, extended by name by unit X8b
//!   (law X8 r3 items 4a and 4b), security's and storage's `scenario`
//!   modules under `scenario-fixtures` alone. X8b adds no shared fixture
//!   gate: `scenario` reaches the four above, and its production chain is
//!   the shared installation fixture's one composition (gate 2's module).
//! - **X9-0's mechanism** in platform: the barrier module, its macros and the
//!   featureless-expansion pin; and X9 r2 item 3's scripted wall clock in
//!   `observe_clock` (`clock.rs`), which r2 assigns to X9-1.
//!
//! `AppendStep`, `ObjectStep` and the ledger commit hook stay `cfg(test)`
//! (law X8 r3 item 4b), with X9's barrier points beside them.
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

const JOINT: &str = r#"any(test, feature = "crash-matrix", feature = "scenario-fixtures")"#;
const CRASH: &str = r#"any(test, feature = "crash-matrix")"#;

/// Every `(file, predicate)` that names `crash-matrix` or `scenario-fixtures`
/// in a `cfg` attribute or `cfg!` in the workspace's Rust sources, with its
/// count. A predicate is written whitespace-collapsed, as the scanner reads
/// it. Any other site, or a changed count, fails.
fn pinned() -> Vec<(&'static str, String, usize)> {
    let joint = || format!("cfg({JOINT})");
    let joint_macos = || format!(r#"cfg(all({JOINT}, target_os = "macos"))"#);
    let crash = || format!("cfg({CRASH})");
    let crash_macos = || format!(r#"cfg(all({CRASH}, target_os = "macos"))"#);
    let guard = || r#"cfg(all(feature = "crash-matrix", not(debug_assertions)))"#.to_owned();
    let support = || r#"cfg(all(feature = "crash-matrix", target_os = "macos"))"#.to_owned();
    let scenario = || r#"cfg(all(feature = "scenario-fixtures", target_os = "macos"))"#.to_owned();
    vec![
        // Shared gate 1: the injected image and the synthetic V2 profile set.
        ("crates/security/src/trust/initial_core.rs", joint(), 12),
        ("crates/security/src/trust/initial_platform.rs", joint(), 1),
        (
            "crates/security/src/trust/initial_platform.rs",
            format!("cfg!({JOINT})"),
            1,
        ),
        ("crates/security/src/trust/core_authentication.rs", joint(), 2),
        ("crates/security/src/initial_installation.rs", joint(), 1),
        // Shared gate 1's re-export of the receipt producers, gate 3's
        // generator accessor, and the test scratch parent; gate 2's arms,
        // creator path, gate constructor and fixture module.
        ("crates/security/src/trust/root_payload.rs", joint(), 2),
        ("crates/security/src/trust/root_payload.rs", joint_macos(), 2),
        // `trust.rs` and `lib.rs` each hold one more joint site for gate 7.
        ("crates/security/src/trust.rs", joint(), 2),
        ("crates/security/src/trust.rs", joint_macos(), 2),
        ("crates/security/src/lib.rs", joint(), 2),
        (
            "crates/security/src/custody/installation_admission.rs",
            joint(),
            3,
        ),
        ("crates/security/src/custody/installation_session.rs", joint(), 1),
        // X6b's recovery admission walks the same home source.
        ("crates/security/src/custody/recovery_admission.rs", joint(), 1),
        (
            "crates/security/src/custody/installation_publication.rs",
            joint(),
            1,
        ),
        ("crates/security/src/custody/installation_parent.rs", joint(), 1),
        ("crates/security/src/custody.rs", joint_macos(), 1),
        // X4T-0's own pin quotes the predicate its declaration must carry.
        (
            "crates/security/src/trust/accepted_store_fixture_tests.rs",
            joint(),
            1,
        ),
        // Shared gate 5 (law X3d r8 item 13): the preimage accessor and its
        // two hops; the read itself is inside gate 1's `tests` module.
        ("crates/security/src/custody/commit_session.rs", joint(), 1),
        ("crates/security/src/custody/operation_handoff.rs", joint(), 1),
        ("crates/security/src/custody/read_premise.rs", joint(), 1),
        // Shared gate 6 (law CI r5 item 3, unit CI-1): the archive emitter
        // and its refusal type.
        ("crates/security/src/archive_profile.rs", joint(), 2),
        // Shared gate 7 (law CI r5 item 6, unit CI-2): C2a-1's TestComponent.
        (
            "crates/security/src/trust_admitted_components.rs",
            joint(),
            2,
        ),
        // Shared gate 8 (law CI r5 item 6, unit CI-2): the fixture store.
        ("crates/lifecycle/src/installation.rs", joint(), 1),
        // Unit CI-2: lifecycle's forwarded feature carries the guard.
        ("crates/lifecycle/src/lib.rs", guard(), 1),
        // Shared gate 4: the fenced publisher and its re-exports.
        ("crates/security/src/trust/floor_publication.rs", joint(), 1),
        (
            "crates/security/src/trust/current_trust_admission.rs",
            joint_macos(),
            1,
        ),
        ("crates/security/src/trust/ordinary_targets.rs", joint_macos(), 1),
        // Crash-matrix-only fixture sites.
        ("crates/security/src/journal_store/carrier_operation.rs", crash(), 3),
        ("crates/security/src/journal_store.rs", crash_macos(), 1),
        // The feature's own declarations.
        ("crates/security/src/lib.rs", guard(), 1),
        ("crates/security/src/lib.rs", support(), 1),
        (
            "crates/security/src/lib.rs",
            r#"cfg(all(test, feature = "crash-matrix", target_os = "macos"))"#.to_owned(),
            1,
        ),
        ("crates/storage/src/lib.rs", guard(), 1),
        ("crates/storage/src/lib.rs", support(), 1),
        (
            "crates/storage/src/ledger_store/project_commit_tests.rs",
            support(),
            1,
        ),
        // Unit X9-2: storage's matrix target, whole-file under the support
        // predicate (law X9 r1 item 2; its manifest also requires the
        // feature).
        ("crates/storage/tests/commit_tests.rs", support(), 1),
        // Unit X9-5: host's matrix target, whole-file under the support
        // predicate (law X9 r1 item 2 and r10; its manifest also requires the
        // feature).
        ("crates/host/tests/commit_matrix_tests.rs", support(), 1),
        ("crates/host/src/lib.rs", guard(), 1),
        ("crates/host/src/lib.rs", support(), 1),
        // Unit X8b's `scenario` modules (law X8 r3 item 4a).
        ("crates/security/src/lib.rs", scenario(), 1),
        ("crates/storage/src/lib.rs", scenario(), 1),
        // X9 r2 item 3's scripted wall clock (platform), assigned to X9-1.
        (
            "crates/platform/src/clock.rs",
            r#"cfg(all( feature = "crash-matrix", any(target_os = "macos", target_os = "linux") ))"#
                .to_owned(),
            1,
        ),
        (
            "crates/platform/src/clock.rs",
            r#"cfg(not(all( feature = "crash-matrix", any(target_os = "macos", target_os = "linux") )))"#
                .to_owned(),
            1,
        ),
        // X9-0's mechanism (platform).
        ("crates/platform/src/lib.rs", guard(), 1),
        (
            "crates/platform/src/lib.rs",
            r#"cfg(all( feature = "crash-matrix", any(target_os = "macos", target_os = "linux") ))"#
                .to_owned(),
            1,
        ),
        (
            "crates/platform/src/crash_macros.rs",
            r#"cfg(all( feature = "crash-matrix", any(target_os = "macos", target_os = "linux") ))"#
                .to_owned(),
            2,
        ),
        (
            "crates/platform/src/crash_macros.rs",
            r#"cfg(not(all( feature = "crash-matrix", any(target_os = "macos", target_os = "linux") )))"#
                .to_owned(),
            2,
        ),
        (
            "crates/platform/src/crash_matrix_tests.rs",
            r#"cfg(not(feature = "crash-matrix"))"#.to_owned(),
            1,
        ),
    ]
}

fn repository() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .unwrap()
}

/// This pin itself, whose literals spell the predicates it pins.
const SELF: &str = "crates/security/src/crash_matrix_sites.rs";

/// Every `.rs` file under `crates/*/src` and `crates/*/tests`, but this pin.
fn sources(repository: &Path) -> Vec<PathBuf> {
    let mut out = Vec::new();
    let mut stack: Vec<PathBuf> = fs::read_dir(repository.join("crates"))
        .unwrap()
        .map(|e| e.unwrap().path())
        .flat_map(|krate| [krate.join("src"), krate.join("tests")])
        .filter(|p| p.is_dir())
        .collect();
    while let Some(dir) = stack.pop() {
        for entry in fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                stack.push(path);
            } else if path.extension().is_some_and(|e| e == "rs") && path != repository.join(SELF) {
                out.push(path);
            }
        }
    }
    out.sort();
    out
}

/// The `cfg(…)` and `cfg!(…)` expressions of `text` (line comments
/// removed), each with its parentheses balanced and its whitespace
/// collapsed, that name either test-only feature.
fn feature_predicates(text: &str) -> Vec<String> {
    let code: String = text
        .lines()
        .map(|line| match line.find("//") {
            Some(at) if !line[..at].contains('"') => &line[..at],
            _ => line,
        })
        .collect::<Vec<_>>()
        .join("\n");
    let mut out = Vec::new();
    let mut from = 0;
    while let Some(found) = code[from..].find("cfg") {
        let start = from + found;
        from = start + 3;
        let rest = &code[start + 3..];
        let open = if rest.starts_with('(') {
            start + 3
        } else if rest.starts_with("!(") {
            start + 4
        } else {
            continue;
        };
        if start > 0
            && code[..start]
                .chars()
                .next_back()
                .is_some_and(|c| c.is_alphanumeric() || c == '_')
        {
            continue;
        }
        let mut depth = 0usize;
        let mut end = None;
        for (i, c) in code[open..].char_indices() {
            match c {
                '(' => depth += 1,
                ')' => {
                    depth -= 1;
                    if depth == 0 {
                        end = Some(open + i + 1);
                        break;
                    }
                }
                _ => {}
            }
        }
        let Some(end) = end else { continue };
        let expression = code[start..end]
            .split_whitespace()
            .collect::<Vec<_>>()
            .join(" ")
            .replace("( ", "(")
            .replace(" )", ")");
        if expression.contains(r#"feature = "crash-matrix""#)
            || expression.contains(r#"feature = "scenario-fixtures""#)
        {
            out.push(expression);
        }
    }
    out
}

/// Every feature site of the repository, by `(file, predicate)`.
fn scanned(repository: &Path) -> BTreeMap<(String, String), usize> {
    let mut out = BTreeMap::new();
    for path in sources(repository) {
        let text = fs::read_to_string(&path).unwrap();
        let relative = path
            .strip_prefix(repository)
            .unwrap()
            .to_string_lossy()
            .into_owned();
        for predicate in feature_predicates(&text) {
            *out.entry((relative.clone(), predicate)).or_insert(0) += 1;
        }
    }
    out
}

#[test]
fn every_test_feature_site_is_on_the_pinned_list() {
    let mut expected: BTreeMap<(String, String), usize> = BTreeMap::new();
    for (file, predicate, count) in pinned() {
        // The scanner collapses `( ` and ` )`; the pinned text is written
        // as rustfmt leaves it, so it is collapsed the same way.
        let predicate = predicate.replace("( ", "(").replace(" )", ")");
        *expected.entry((file.to_owned(), predicate)).or_insert(0) += count;
    }
    assert_eq!(scanned(&repository()), expected);
}

#[test]
fn the_scanner_finds_every_form_and_skips_comments() {
    let text = r#"
// #[cfg(feature = "crash-matrix")] in a comment is not a site
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
fn a() {}
#[cfg(all(
    any(test, feature = "crash-matrix"),
    target_os = "macos"
))]
fn b() {}
fn c() -> bool { cfg!(feature = "scenario-fixtures") }
#[cfg(test)]
fn d() {}
#[cfg_attr(feature = "crash-matrix", allow(dead_code))]
fn e() {}
"#;
    assert_eq!(
        feature_predicates(text),
        [
            format!("cfg({JOINT})"),
            r#"cfg(all(any(test, feature = "crash-matrix"), target_os = "macos"))"#.to_owned(),
            r#"cfg!(feature = "scenario-fixtures")"#.to_owned(),
        ]
    );
    // `cfg_attr` is not a `cfg`, so a feature there would escape this
    // scanner: no source names a test feature in `cfg_attr`.
    for path in sources(&repository()) {
        let text = fs::read_to_string(&path).unwrap();
        assert!(
            !text.contains(r#"cfg_attr(feature = "crash-matrix""#)
                && !text.contains(r#"cfg_attr(feature = "scenario-fixtures""#)
                && !text.contains(r#"cfg_attr(any(feature = "#),
            "{}",
            path.display()
        );
    }
}

// ------------------------------------------------- the shared producers

use crate::custody::installation_read_fixture::ReadFixture;

#[test]
fn the_shared_producers_install_trust_and_publish_it_under_the_fence() {
    use opensip_platform::{FileLock, LockMode};
    let fixture = ReadFixture::new("x91-producers");
    let at = fixture.at();
    // P0 carries no retained clock record.
    let (schema, version) = at.current_trust_values().unwrap();
    assert_eq!(version, 0);
    assert!(schema == 1 || schema == 2);
    // X4T-0's store for this S, then the fenced publisher twice.
    let closure = at.install_accepted_trust(Vec::new(), 1, None).unwrap();
    assert!(closure.starts_with("closure2:"));
    assert_eq!(at.current_trust_values().unwrap(), (schema, 1));
    assert_eq!(
        at.publish_accepted_trust_fenced(vec![("release", closure.to_owned())], 2),
        Ok((1, 2))
    );
    assert_eq!(at.publish_accepted_trust_fenced(Vec::new(), 3), Ok((2, 3)));
    // The publication takes the fence: with another holder it refuses,
    // and `state.v1` is unchanged.
    let current = fixture
        .installation
        .join(format!("trust/stores/{}/state.v1", fixture.store));
    let before = fs::read(&current).unwrap();
    let held = FileLock::try_acquire(
        fs::File::open(fixture.installation.join("lifecycle.fence")).unwrap(),
        LockMode::Exclusive,
    )
    .unwrap()
    .unwrap();
    let refused = at.publish_accepted_trust_fenced(Vec::new(), 4);
    assert!(
        matches!(&refused, Err(e) if e.starts_with("fence:")),
        "{refused:?}"
    );
    assert_eq!(fs::read(&current).unwrap(), before);
    drop(held);
    // A writer on the same I, by the same gate, still admits.
    let (writer, _trees) = at.writer().unwrap();
    writer.release().unwrap();
}

#[test]
fn the_carrier_fixtures_plant_what_x3b_classifies() {
    use crate::journal_store::{InheritedFormat, plant_inherited_carrier_for_tests};
    for (format, table) in [
        (InheritedFormat::One, "grant_journal"),
        (InheritedFormat::Two, "grant_journal"),
    ] {
        let id: String = opensip_platform::request_entropy()
            .unwrap()
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        let dir = crate::test_scratch::temp_dir().join(format!("opensip-x91-carrier-{id}"));
        fs::create_dir(&dir).unwrap();
        plant_inherited_carrier_for_tests(&dir, format);
        let c = rusqlite::Connection::open(dir.join("grant-journal.sqlite")).unwrap();
        let names: Vec<String> = c
            .prepare("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name")
            .unwrap()
            .query_map([], |r| r.get(0))
            .unwrap()
            .collect::<rusqlite::Result<_>>()
            .unwrap();
        // The inherited schema alone: no format row table, no current
        // journal (X3b item 3a's F46 class, never a migration footprint).
        assert!(names.iter().any(|n| n == table), "{names:?}");
        assert!(
            !names
                .iter()
                .any(|n| n == "carrier_format" || n == "grant_journal_v3")
        );
        let mode: String = c
            .query_row("PRAGMA journal_mode", [], |r| r.get(0))
            .unwrap();
        assert_eq!(mode, "wal");
        drop(c);
        let _ = fs::remove_dir_all(&dir);
    }
}

/// Law X9 r1 item 3's source pin, extended to unit X9-1's sources and unit
/// X9-2's matrix target: the support modules, the census children and the
/// matrix target admit no sleep, polling loop or other timed wait (their
/// only waits are X9-0's blocking record reads).
#[test]
fn the_support_and_census_sources_admit_no_sleep_polling_or_timed_wait() {
    let repository = repository();
    let files = [
        "crates/security/src/crash_matrix_support.rs",
        "crates/security/src/crash_matrix_support/post_state.rs",
        "crates/security/src/crash_matrix_support/run_record.rs",
        "crates/security/src/crash_matrix_census.rs",
        "crates/storage/src/crash_matrix_support.rs",
        "crates/storage/src/crash_matrix_support/run_candidate.rs",
        "crates/storage/src/ledger_store/project_commit_census.rs",
        // Unit X9-2: storage's matrix target (law X9 r1 item 3's pin names
        // both matrix targets).
        "crates/storage/tests/commit_tests.rs",
        "crates/host/src/crash_matrix_support.rs",
        // Unit X9-5: host's matrix target (law X9 r10).
        "crates/host/tests/commit_matrix_tests.rs",
    ];
    let forbidden = [
        ["sl", "eep"].concat(),
        ["park", "_timeout"].concat(),
        ["wait", "_timeout"].concat(),
        ["recv", "_timeout"].concat(),
        ["try", "_wait"].concat(),
        ["try", "_recv"].concat(),
        ["try", "_lock"].concat(),
        ["recv", "_deadline"].concat(),
        ["yield", "_now"].concat(),
        ["spin", "_loop"].concat(),
        ["set_read", "_timeout"].concat(),
        ["set_non", "blocking"].concat(),
        ["O_NON", "BLOCK"].concat(),
        ["Inst", "ant"].concat(),
        ["System", "Time"].concat(),
    ];
    // Law X9 r12 (unit X9-3): item 11's timing guard reads the parent's
    // monotonic clock. The matrix target names it on this one line, which
    // is not a wait; every other line of every file stays pinned.
    let guard_clock = ["type GuardClock = std::time::Inst", "ant;"].concat();
    for file in files {
        let mut guard_lines = 0;
        let text = fs::read_to_string(repository.join(file)).unwrap();
        for (number, raw) in text.lines().enumerate() {
            let code = raw.split("//").next().unwrap_or("");
            // Unit X9-5: host's matrix target names it once too (X9 r12).
            if (file == "crates/storage/tests/commit_tests.rs"
                || file == "crates/host/tests/commit_matrix_tests.rs")
                && code.trim() == guard_clock
            {
                guard_lines += 1;
                continue;
            }
            for token in &forbidden {
                assert!(
                    !code.contains(token.as_str()),
                    "{file}:{}: {token}",
                    number + 1
                );
            }
        }
        assert!(
            guard_lines <= 1,
            "{file}: the timing guard's clock is named once"
        );
    }
}
