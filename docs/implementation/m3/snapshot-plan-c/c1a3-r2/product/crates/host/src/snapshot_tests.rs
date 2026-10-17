// Unit C1a2's capture-session controls (C1a plan r4, C1a2): each walks a
// scratch project under security's scenario home, through the durable route's
// snapshot root, into a private 0700 custody directory.
use super::*;
use crate::candidate_custody::{CustodyFailure, digest_hex};
use opensip_identity::{RawSha256, parse_json};
use opensip_platform::{RetainedDirectory, WorkLedger};
use opensip_security::discovery_export::AdmittedBoundaries;
use opensip_security::scenario::ScenarioHome;
use std::collections::BTreeSet;
use std::fs::File;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};

pub(crate) struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        // The removal is checked unless the test is already failing.
        let removed = std::fs::remove_dir_all(&self.0);
        if !std::thread::panicking() {
            removed.unwrap();
        }
    }
}
/// A private custody directory (0700, with the zero-rights owner ACL),
/// outside the project.
pub(crate) fn custody_dir() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let base = std::env::temp_dir().join(format!("opensip-c1a2-session-{nonce}"));
    std::fs::create_dir(&base).unwrap();
    std::fs::set_permissions(&base, std::fs::Permissions::from_mode(0o700)).unwrap();
    let base = std::fs::canonicalize(&base).unwrap();
    let dir = base.join("custody");
    std::fs::create_dir(&dir).unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    crate::candidate_custody::tests::make_private(&dir);
    (Scratch(base), dir)
}
pub(crate) fn write(root: &Path, rel: &str, bytes: &[u8]) {
    let path = root.join(rel);
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent).unwrap();
    }
    std::fs::write(&path, bytes).unwrap();
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o644)).unwrap();
}
pub(crate) fn no_boundaries() -> AdmittedBoundaries {
    let raw = r#"{"schemaVersion":3,"source":"security.discovery","selectedRoot":"/h/w","nestedRepositories":[],"nestedProjects":[],"custodyExcludedUnits":[],"prunedTrees":[],"memberRepositories":[]}"#;
    opensip_security::scenario::admitted_boundaries(&parse_json(raw.as_bytes()).unwrap()).unwrap()
}
pub(crate) fn sha(bytes: &[u8]) -> [u8; 32] {
    RawSha256::new().update(bytes).unwrap().finish()
}
pub(crate) fn session(dir: &Path, work: &mut WorkScope<'_>) -> CaptureSession {
    let handle = RetainedDirectory::from_retained_handle(File::open(dir).unwrap()).unwrap();
    let uid = std::fs::metadata(dir).unwrap().uid();
    let custody = CandidateCustody::new(handle, uid, work)
        .map_err(|f: CustodyFailure| format!("{f:?}"))
        .unwrap();
    CaptureSession::open(custody, work).unwrap()
}
/// A synthetic reached capture, for sealing's bound controls (100,001 rows,
/// over 8 GiB) without that many real files (unit C1a3).
pub(crate) fn insert_reached(
    session: &mut CaptureSession,
    path: &str,
    sha256: [u8; 32],
    bytes: u64,
) {
    let stamp = Stamp {
        device: 0,
        inode: 0,
        size: bytes,
        modified: (0, 0),
        changed: (0, 0),
    };
    session.captures.insert(
        path.to_owned(),
        Capture {
            sha256,
            bytes,
            stamp,
            origin: Some(CaptureOrigin::Walk),
        },
    );
}
/// A custody blob's bytes, through `open`'s verification.
pub(crate) fn custodied(
    session: &mut CaptureSession,
    sha256: &[u8; 32],
    work: &mut WorkScope<'_>,
) -> Vec<u8> {
    let (custody, buffer) = session.custody_and_buffer();
    let mut file = custody.open(sha256, buffer, work).unwrap();
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).unwrap();
    bytes
}
pub(crate) fn reset_spies() {
    READ_PASSES.with_borrow_mut(BTreeMap::clear);
    READ_HOOK.with_borrow_mut(|h| *h = None);
}

/// Walk `root` (no boundaries, the given `ignorePaths`) into a fresh session,
/// running `before` on it first (the pre-walk captures) and `after` on the
/// result, all under one ledger.
pub(crate) fn with_walk<T>(
    root: &Path,
    ignore: &[&str],
    before: impl FnOnce(&mut CaptureSession, &SnapshotRoot<'_>, SnapshotCustody<'_>, &mut WorkScope<'_>),
    after: impl FnOnce(
        Result<SnapshotWalkReport, ReadFailure>,
        &mut CaptureSession,
        &mut WorkScope<'_>,
    ) -> T,
    home: &ScenarioHome,
) -> T {
    let (_custody, dir) = custody_dir();
    let bounds = no_boundaries();
    let members = BTreeSet::new();
    let ignore: Vec<String> = ignore.iter().map(|s| (*s).to_owned()).collect();
    let extent = WorkLedger::discovery_profile()
        .scope(|work| SnapshotExtent::new(&bounds, &members, &ignore, work))
        .unwrap();
    home.with_snapshot_root(root, |snapshot, judge| {
        WorkLedger::discovery_profile()
            .scope(|work| {
                let mut session = session(&dir, work);
                before(&mut session, snapshot, judge, work);
                let walked = session.walk(snapshot, judge, &extent, work);
                Ok::<_, ReadFailure>(after(walked, &mut session, work))
            })
            .unwrap()
    })
    .unwrap()
}

// ------------------------------------------------------------------ C1-T1 and C1-T3

#[test]
fn the_bytes_retained_and_delivered_are_the_bytes_hashed_and_a_later_rewrite_changes_nothing() {
    reset_spies();
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a2-t1");
    write(&root, "a.txt", b"alpha");
    write(&root, "src/main.rs", b"fn main() {}\n");
    write(&root, "big.bin", &vec![7u8; 3 * READ_CHUNK + 5]);
    write(&root, "copy.txt", b"alpha");
    write(&root, "empty", b"");
    let originals: BTreeMap<&str, Vec<u8>> =
        ["a.txt", "big.bin", "copy.txt", "empty", "src/main.rs"]
            .into_iter()
            .map(|p| (p, std::fs::read(root.join(p)).unwrap()))
            .collect();
    let rows = with_walk(
        &root,
        &[],
        |_, _, _, _| {},
        |walked, session, work| {
            walked.unwrap();
            let rows: Vec<(String, [u8; 32], u64)> = session
                .inventory()
                .map(|(p, c)| (p.to_owned(), c.sha256, c.bytes))
                .collect();
            // C1-T1: a recording sink reads each row from custody; it is the
            // bytes hashed, row by row.
            for (path, sha256, bytes) in &rows {
                let delivered = custodied(session, sha256, work);
                assert_eq!(delivered, originals[path.as_str()], "{path}");
                assert_eq!(*sha256, sha(&delivered), "{path}");
                assert_eq!(*bytes, delivered.len() as u64, "{path}");
            }
            // Equal bytes share one blob.
            assert_eq!(session.custody().blob_count(), 4);
            // C1-T25's side record: every row came from the walk.
            assert!(
                session
                    .inventory()
                    .all(|(_, c)| c.origin == Some(CaptureOrigin::Walk))
            );
            // C1-T3: a rewrite after the session changes nothing it holds.
            std::fs::write(root.join("a.txt"), b"ALPHA, rewritten").unwrap();
            let again = custodied(session, &rows[0].1, work);
            assert_eq!(again, b"alpha");
            rows
        },
        &home,
    );
    let paths: Vec<&str> = rows.iter().map(|(p, _, _)| p.as_str()).collect();
    assert_eq!(
        paths,
        ["a.txt", "big.bin", "copy.txt", "empty", "src/main.rs"]
    );
    // Each file was read exactly once.
    READ_PASSES.with_borrow(|passes| {
        assert!(passes.values().all(|n| *n == 1), "{passes:?}");
        assert_eq!(passes.len(), 5);
    });
}

// ------------------------------------------------------------------ C1A-T1 and C1-T24

#[test]
fn a_path_captured_before_the_walk_is_read_once_and_reused_by_the_walk() {
    reset_spies();
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a2-reuse");
    write(&root, "package.json", b"{\"name\":\"p\"}");
    write(&root, "index.ts", b"export {}\n");
    let (captured, rows) = with_walk(
        &root,
        &[],
        |session, snapshot, judge, work| {
            session
                .capture(snapshot, "package.json", judge, work)
                .unwrap();
            // A second request returns the kept capture, with no read.
            session
                .capture(snapshot, "package.json", judge, work)
                .unwrap();
        },
        |walked, session, _| {
            walked.unwrap();
            assert_eq!(session.leftovers().count(), 0);
            let rows: Vec<(String, Option<CaptureOrigin>)> = session
                .inventory()
                .map(|(p, c)| (p.to_owned(), c.origin))
                .collect();
            (session.custody().blob_count(), rows)
        },
        &home,
    );
    assert_eq!(captured, 2);
    assert_eq!(
        rows,
        [
            ("index.ts".to_owned(), Some(CaptureOrigin::Walk)),
            ("package.json".to_owned(), Some(CaptureOrigin::Walk)),
        ]
    );
    // The read-count spy: one pass for the captured path, though both the
    // capture and the walk reached it.
    READ_PASSES.with_borrow(|passes| {
        assert_eq!(passes.get("package.json"), Some(&1), "{passes:?}");
        assert_eq!(passes.get("index.ts"), Some(&1), "{passes:?}");
    });
}

#[test]
fn a_captured_file_rewritten_before_the_walk_reaches_it_refuses_with_no_reread() {
    reset_spies();
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a2-t24");
    write(&root, "package.json", b"{\"name\":\"p\"}");
    let refused = with_walk(
        &root,
        &[],
        |session, snapshot, judge, work| {
            session
                .capture(snapshot, "package.json", judge, work)
                .unwrap();
            // C1-T24: rewritten after the capture, before the walk.
            std::fs::write(root.join("package.json"), b"{\"name\":\"q\"}").unwrap();
        },
        |walked, _, _| format!("{:?}", walked.unwrap_err()),
        &home,
    );
    assert!(
        refused.contains("ChangedSinceCapture(\"package.json\")"),
        "{refused}"
    );
    READ_PASSES.with_borrow(|passes| assert_eq!(passes.get("package.json"), Some(&1)));
}

#[test]
fn a_capture_the_walk_never_reaches_is_a_leftover_and_never_inventoried() {
    reset_spies();
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a2-leftover");
    write(&root, "ignored/package.json", b"{}");
    write(&root, "kept.txt", b"k");
    let (leftovers, rows) = with_walk(
        &root,
        &["ignored"],
        |session, snapshot, judge, work| {
            session
                .capture(snapshot, "ignored/package.json", judge, work)
                .unwrap();
        },
        |walked, session, _| {
            walked.unwrap();
            let leftovers: Vec<String> = session.leftovers().map(str::to_owned).collect();
            let rows: Vec<String> = session.inventory().map(|(p, _)| p.to_owned()).collect();
            (leftovers, rows)
        },
        &home,
    );
    assert_eq!(leftovers, ["ignored/package.json"]);
    assert_eq!(rows, ["kept.txt"]);
}

// ------------------------------------------------------------------ the read's own refusals

#[test]
fn a_file_changed_before_or_during_its_read_refuses_with_no_retry() {
    for (case, expected) in [
        ("before", "ChangedBeforeRead(\"f.txt\")"),
        ("grows", "ChangedDuringRead(\"f.txt\")"),
        ("rewritten", "ChangedDuringRead(\"f.txt\")"),
    ] {
        reset_spies();
        let home = ScenarioHome::create(&std::env::temp_dir());
        let root = home.project(&format!("c1a2-change-{case}"));
        write(&root, "f.txt", &vec![b'x'; 2 * READ_CHUNK]);
        let target = root.join("f.txt");
        READ_HOOK.with_borrow_mut(|h| {
            *h = Some(Box::new(move |path, point| {
                if path != "f.txt" {
                    return None;
                }
                match (case, point) {
                    ("before", ReadPoint::BeforeSample) => {
                        std::fs::write(&target, vec![b'y'; 2 * READ_CHUNK + 1]).unwrap();
                    }
                    ("grows", ReadPoint::BeforeCall(2)) => {
                        use std::io::Write;
                        let mut f = std::fs::OpenOptions::new()
                            .append(true)
                            .open(&target)
                            .unwrap();
                        f.write_all(b"more").unwrap();
                    }
                    ("rewritten", ReadPoint::BeforeCall(2)) => {
                        use std::os::unix::fs::FileExt;
                        let f = std::fs::OpenOptions::new()
                            .write(true)
                            .open(&target)
                            .unwrap();
                        f.write_all_at(b"Z", 0).unwrap();
                    }
                    _ => {}
                }
                None
            }));
        });
        let refused = with_walk(
            &root,
            &[],
            |_, _, _, _| {},
            |walked, _, _| format!("{:?}", walked.unwrap_err()),
            &home,
        );
        reset_spies();
        assert!(refused.contains(expected), "{case}: {refused}");
    }
}

#[test]
fn the_attempt_envelope_bounds_interrupted_reads_and_a_read_error_refuses() {
    for (case, expected) in [
        ("interrupted", "ReadAttemptsExhausted(\"f.txt\")"),
        ("error", "Read { path: \"f.txt\""),
    ] {
        reset_spies();
        let home = ScenarioHome::create(&std::env::temp_dir());
        let root = home.project(&format!("c1a2-attempts-{case}"));
        write(&root, "f.txt", b"twelve bytes");
        let calls = std::rc::Rc::new(std::cell::Cell::new(0u64));
        let counted = calls.clone();
        READ_HOOK.with_borrow_mut(|h| {
            *h = Some(Box::new(move |path, point| match (path, point) {
                ("f.txt", ReadPoint::BeforeCall(n)) if case == "interrupted" => {
                    counted.set(n);
                    Some(io::Error::new(io::ErrorKind::Interrupted, "injected"))
                }
                ("f.txt", ReadPoint::BeforeCall(1)) => Some(io::Error::other("injected")),
                _ => None,
            }));
        });
        let refused = with_walk(
            &root,
            &[],
            |_, _, _, _| {},
            |walked, _, _| format!("{:?}", walked.unwrap_err()),
            &home,
        );
        reset_spies();
        assert!(refused.contains(expected), "{case}: {refused}");
        if case == "interrupted" {
            // Exactly the envelope's attempts were made, each one charged.
            assert_eq!(calls.get(), attempt_envelope(12));
        }
    }
    // The envelope: 2·⌈size / 64 KiB⌉ + 2.
    assert_eq!(attempt_envelope(0), 2);
    assert_eq!(attempt_envelope(12), 4);
    assert_eq!(attempt_envelope(READ_CHUNK as u64), 4);
    assert_eq!(attempt_envelope(READ_CHUNK as u64 + 1), 6);
}

// ------------------------------------------------------------------ pricing

#[test]
fn the_buffer_is_charged_once_by_the_readers_growth_rule() {
    // 4 KiB, then doubling, to 64 KiB: every growth requested, never refunded.
    assert_eq!(
        buffer_cost(),
        WorkCost {
            objects: 1,
            edges: 0,
            bytes: 4096 + 8192 + 16_384 + 32_768 + 65_536,
        }
    );
}

/// A payload of `len` bytes in one file: the session's charge, beyond the
/// walk's own, for that file.
fn payload_charge(len: u64, name: &str) -> WorkCost {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project(name);
    let f = File::create(root.join("payload.bin")).unwrap();
    f.set_len(len).unwrap();
    drop(f);
    std::fs::set_permissions(
        root.join("payload.bin"),
        std::fs::Permissions::from_mode(0o644),
    )
    .unwrap();
    let (_custody, dir) = custody_dir();
    let bounds = no_boundaries();
    let members = BTreeSet::new();
    let extent = WorkLedger::discovery_profile()
        .scope(|work| SnapshotExtent::new(&bounds, &members, &[], work))
        .unwrap();
    home.with_snapshot_root(&root, |snapshot, judge| {
        let mut walk_only = WorkLedger::discovery_profile();
        walk_only
            .scope(|work| {
                let mut visit = |_: SourceFile, _: &mut WorkScope<'_>| Ok::<_, ReadFailure>(());
                walk_snapshot(snapshot, judge, &extent, &mut visit, work).map(drop)
            })
            .map_err(|f| format!("{f:?}"))
            .unwrap();
        let mut full = WorkLedger::discovery_profile();
        full.scope(|work| {
            let mut session = session(&dir, work);
            session.walk(snapshot, judge, &extent, work).map(drop)
        })
        .map_err(|f| format!("{f:?}"))
        .unwrap();
        let (a, b) = (walk_only.used(), full.used());
        WorkCost {
            objects: b.objects - a.objects,
            edges: b.edges - a.edges,
            bytes: b.bytes - a.bytes,
        }
    })
    .unwrap()
}

#[test]
fn a_stream_is_charged_its_buffer_and_attempts_and_no_byte_grows_with_its_size() {
    let small = payload_charge(1, "c1a2-payload-small");
    let large = payload_charge(64 * READ_CHUNK as u64, "c1a2-payload-large");
    // Equal objects and bytes; edges differ by exactly the extra read attempts
    // and chunk writes (64 + 1 against 1 + 1 attempts; 64 against 1 write).
    assert_eq!((large.objects, large.bytes), (small.objects, small.bytes));
    assert_eq!(large.edges - small.edges, (65 - 2) + (64 - 1));
}

/// C1a plan r4's 4 GiB control: a sparse 4 GiB file, read once into custody,
/// is charged as the small one plus its attempts and writes only. A lane
/// probe (it writes 4 GiB into custody), run explicitly.
#[test]
#[ignore]
fn a_four_gibibyte_stream_is_charged_only_its_buffer_and_its_read_attempts() {
    let gib4 = 4u64 << 30;
    let small = payload_charge(1, "c1a2-payload-1");
    let large = payload_charge(gib4, "c1a2-payload-4gib");
    let chunks = gib4 / READ_CHUNK as u64;
    assert_eq!((large.objects, large.bytes), (small.objects, small.bytes));
    assert_eq!(
        large.edges - small.edges,
        ((chunks + 1 - 2) + (chunks - 1)) as usize
    );
}

// ------------------------------------------------------------------ C1-T2's source pin

#[test]
fn the_session_is_the_only_source_read_site() {
    // `snapshot.rs` holds the one read of a source descriptor; the security
    // walk and opener read no content; custody reads only its own files.
    let snapshot = include_str!("snapshot.rs");
    let production = snapshot.split("#[cfg(test)]\n#[path").next().unwrap();
    assert_eq!(production.matches("source.file().read(").count(), 1);
    for module in [
        include_str!("../../security/src/snapshot_source.rs"),
        include_str!("../../security/src/snapshot_walk.rs"),
    ] {
        let code = module.split("#[cfg(test)]\n#[path").next().unwrap();
        for read in [
            ".read(",
            "read_to_end",
            "read_exact",
            "read_to_string",
            "io::Read",
            "Read}",
        ] {
            assert!(!code.contains(read), "{read}");
        }
    }
    let custody = include_str!("candidate_custody.rs");
    let code = custody.split("#[cfg(test)]\n#[path").next().unwrap();
    // Its one read is `open`'s verification of its own custody file.
    assert_eq!(code.matches(".read(").count(), 1);
    assert!(code.contains("let mut file = work.run(RetainedDirectory::open_regular_cost(&name)"));
    assert!(!code.contains("SourceFile"));
    // The digest name matches the custody's own spelling.
    assert_eq!(digest_hex(&sha(b"")).len(), 64);
}

/// r2 (Codex C1A2-R1-RF-3): every heap allocation in the session's and
/// custody's production code is at a charged site. Each refusal moves the
/// source's own path, charged when the source was made, and never copies
/// one; custody's errors carry native errors, never a formatted string.
#[test]
fn every_session_and_custody_allocation_is_at_a_charged_site() {
    let production = |module: &'static str| module.split("#[cfg(test)]\n#[path").next().unwrap();
    let snapshot = production(include_str!("snapshot.rs"));
    let custody = production(include_str!("candidate_custody.rs"));
    for (code, spelling, sites) in [
        // The one copy is the test-only read-pass spy's.
        (snapshot, "to_owned()", 1),
        (snapshot, "vec![", 1),
        (snapshot, "source.into_parts().0", 7),
        (custody, "format!(", 1),
        (custody, "String::with_capacity(", 1),
        (custody, "digest_hex(", 3),
    ] {
        assert_eq!(code.matches(spelling).count(), sites, "{spelling}");
    }
    for code in [snapshot, custody] {
        for spelling in [
            "to_string()",
            "to_vec()",
            "String::from",
            ".clone()",
            "Box::new",
            ".collect",
        ] {
            assert!(!code.contains(spelling), "{spelling}");
        }
    }
    assert!(snapshot.contains(
        "    #[cfg(test)]\n    READ_PASSES.with_borrow_mut(|passes| *passes.entry(source.path().to_owned())"
    ));
    assert!(snapshot.contains(
        "work.charge::<ReadError>(buffer_cost())?;\n        Ok(Self {\n            custody,\n            buffer: vec![0; READ_CHUNK],"
    ));
    assert!(custody.contains(
        "work.charge::<CustodyError>(owned_record(name_bytes))?;\n        let name = format!(\"pending-{}\", self.next);"
    ));
    for call in [
        "let name = digest_hex(sha256);",
        "let hex = digest_hex(&sha256);",
    ] {
        assert!(
            custody.contains(&format!(
                "work.charge::<CustodyError>(owned_record(64))?;\n        {call}"
            )),
            "{call}"
        );
    }
}

// ------------------------------------------------------------------ the session's charge model

/// The trees of security's `snapshot_ledger_vectors.json`, materialized
/// under `root` (hard links into `links`), as C1a1's oracle does.
fn materialize(root: &Path, links: &Path, tree: &[opensip_identity::JsonValue]) {
    use opensip_identity::JsonValue as V;
    let text = |v: &V, k: &str| match v {
        V::Object(m) => match m.get(k) {
            Some(V::String(s)) => s.clone(),
            _ => panic!("{k}"),
        },
        _ => panic!("entry"),
    };
    let get = |v: &V, k: &str| match v {
        V::Object(m) => m.get(k).cloned(),
        _ => None,
    };
    for (index, entry) in tree.iter().enumerate() {
        let path = root.join(text(entry, "path"));
        let mode = || u32::from_str_radix(&text(entry, "mode"), 8).unwrap();
        let kind = text(entry, "kind");
        match kind.as_str() {
            "dir" => {
                std::fs::create_dir(&path).unwrap();
                std::fs::set_permissions(&path, std::fs::Permissions::from_mode(mode())).unwrap();
            }
            "file" => {
                std::fs::write(&path, text(entry, "text").as_bytes()).unwrap();
                std::fs::set_permissions(&path, std::fs::Permissions::from_mode(mode())).unwrap();
                if matches!(get(entry, "hardlink"), Some(V::Bool(true))) {
                    std::fs::hard_link(&path, links.join(format!("h{index}"))).unwrap();
                }
            }
            "symlink" => std::os::unix::fs::symlink(text(entry, "target"), &path).unwrap(),
            "fifo" => assert!(
                std::process::Command::new("/usr/bin/mkfifo")
                    .arg("-m")
                    .arg(text(entry, "mode"))
                    .arg(&path)
                    .status()
                    .unwrap()
                    .success()
            ),
            "socket" => {
                let nonce: String = opensip_platform::request_entropy().unwrap()[..6]
                    .iter()
                    .map(|b| format!("{b:02x}"))
                    .collect();
                let short = std::env::temp_dir().join(format!("s{nonce}"));
                drop(std::os::unix::net::UnixListener::bind(&short).unwrap());
                std::fs::rename(&short, &path).unwrap();
            }
            other => panic!("{other}"),
        }
        if let Some(V::String(who)) = get(entry, "acl") {
            let principal = if who == "user" {
                "user:nobody"
            } else {
                "group:everyone"
            };
            let right = if kind == "dir" { "add_file" } else { "write" };
            assert!(
                std::process::Command::new("/bin/chmod")
                    .arg("+a")
                    .arg(format!("{principal} allow {right}"))
                    .arg(&path)
                    .status()
                    .unwrap()
                    .success()
            );
        }
    }
}

#[test]
fn the_session_charges_exactly_the_models_read_and_custody_terms() {
    use opensip_identity::JsonValue as V;
    // The two record sizes and the custody admission's ACL capture price
    // (r2, C1A2-R1-RF-1), which the model reads from these lines.
    assert_eq!(std::mem::size_of::<Capture>(), 104);
    assert_eq!(std::mem::size_of::<([u8; 32], u64)>(), 40);
    assert_eq!(
        opensip_platform::descriptor_acl_capture_cost(),
        WorkCost {
            objects: 1,
            edges: 131,
            bytes: 7940,
        }
    );
    const TREES: &[u8] = include_bytes!("../../security/src/snapshot_ledger_vectors.json");
    const SESSIONS: &[u8] = include_bytes!("snapshot_session_vectors.json");
    let field = |v: &V, k: &str| -> V {
        match v {
            V::Object(m) => m.get(k).cloned().unwrap_or(V::Null),
            _ => V::Null,
        }
    };
    let items = |v: V| match v {
        V::Array(a) => a,
        _ => Vec::new(),
    };
    let text = |v: V| match v {
        V::String(s) => s,
        _ => panic!("not a string"),
    };
    let count = |v: V| match v {
        V::Integer(i) => usize::try_from(i.get()).unwrap(),
        _ => panic!("not an integer"),
    };
    let trees = items(field(&parse_json(TREES).unwrap(), "cases"));
    let sessions = items(field(&parse_json(SESSIONS).unwrap(), "cases"));
    assert_eq!(trees.len(), sessions.len());
    let home = ScenarioHome::create(&std::env::temp_dir());
    let (mut checked, mut unrouted) = (0, Vec::new());
    for (index, (case, session_case)) in trees.iter().zip(&sessions).enumerate() {
        let id = text(field(case, "id"));
        assert_eq!(text(field(session_case, "id")), id);
        let root = home.project(&format!("c1a2-model-{index}"));
        let (_links_scratch, links) = custody_dir();
        materialize(&root, &links, &items(field(case, "tree")));
        let inventory = field(case, "inventory");
        let strings = |k: &str| -> Vec<V> { items(field(&inventory, k)) };
        let record = V::Object(
            [
                (
                    "schemaVersion",
                    V::Integer(opensip_identity::JsonInteger::new(3).unwrap()),
                ),
                ("source", V::String("security.discovery".to_owned())),
                ("selectedRoot", V::String("/h/w".to_owned())),
                (
                    "nestedRepositories",
                    V::Array(strings("nestedRepositories")),
                ),
                ("nestedProjects", V::Array(strings("nestedProjects"))),
                (
                    "custodyExcludedUnits",
                    V::Array(strings("custodyExcludedUnits")),
                ),
                ("prunedTrees", V::Array(Vec::new())),
                ("memberRepositories", V::Array(Vec::new())),
            ]
            .into_iter()
            .map(|(k, v)| (k.to_owned(), v))
            .collect(),
        );
        let bounds = opensip_security::scenario::admitted_boundaries(&record)
            .unwrap_or_else(|e| panic!("{id}: {e:?}"));
        let members: BTreeSet<String> = items(field(case, "members"))
            .into_iter()
            .map(text)
            .collect();
        let extent = WorkLedger::discovery_profile()
            .scope(|work| SnapshotExtent::new(&bounds, &members, &[], work))
            .unwrap();
        let own = std::fs::metadata(&root).unwrap().gid();
        let gids: Vec<u32> = match field(case, "groups") {
            V::String(g) if g == "own" => vec![own],
            V::String(g) if g == "other" => vec![4243],
            _ => Vec::new(),
        };
        let waive = matches!(field(case, "waive"), V::Bool(true));
        let foreign = matches!(field(case, "foreign"), V::Bool(true)).then_some(4242);
        let (_custody, dir) = custody_dir();
        let routed = home.with_snapshot_root_as(&root, &gids, waive, foreign, |snapshot, judge| {
            let mut walk_only = WorkLedger::discovery_profile();
            walk_only
                .scope(|work| {
                    let mut visit = |_: SourceFile, _: &mut WorkScope<'_>| Ok::<_, ReadFailure>(());
                    walk_snapshot(snapshot, judge, &extent, &mut visit, work).map(drop)
                })
                .unwrap_or_else(|f| panic!("{id}: walk {f:?}"));
            let mut full = WorkLedger::discovery_profile();
            let handed = full
                .scope(|work| {
                    let mut session = session(&dir, work);
                    session.walk(snapshot, judge, &extent, work)?;
                    Ok::<_, ReadFailure>(session.inventory().count())
                })
                .unwrap_or_else(|f| panic!("{id}: session {f:?}"));
            let (a, b) = (walk_only.used(), full.used());
            (
                (b.objects - a.objects, b.edges - a.edges, b.bytes - a.bytes),
                handed,
            )
        });
        // X2 admits no project root holding VCS evidence it cannot observe
        // (a root-level `.git` or `.hg` directory or file), so those trees
        // have no durable route; their walk terms are C1a1's control.
        let (diff, handed) = match routed {
            Ok(result) => result,
            Err(termination) => {
                eprintln!("session {id}: no route ({termination:?})");
                unrouted.push((id, format!("{termination:?}")));
                continue;
            }
        };
        let predicted = field(session_case, "predicted");
        let expected = (
            count(field(&predicted, "objects")),
            count(field(&predicted, "edges")),
            count(field(&predicted, "bytes")),
        );
        eprintln!("session {id}: native {diff:?} predicted {expected:?}");
        assert_eq!(handed, count(field(session_case, "handed")), "{id}");
        assert_eq!(diff, expected, "{id}");
        checked += 1;
    }
    eprintln!("session: {checked} exact, unrouted {unrouted:?}");
    assert_eq!(checked + unrouted.len(), 35);
    // Exactly these trees have no durable route, each for X2's own reason:
    // a root `.git` with no tracking observation, a root `.opensip` that is
    // a file, and a root `.opensip/project-id.v1` that is not the marker.
    let expected = [
        ("pruned-anchors-all-four", "vcs-unsupported"),
        ("opensip-file-at-the-root", "identity-contradiction"),
        ("opensip-anchors-root-and-member", "marker-custody"),
    ];
    assert_eq!(unrouted.len(), expected.len(), "{unrouted:?}");
    for ((id, why), (want_id, want_why)) in unrouted.iter().zip(expected) {
        assert_eq!(id, want_id);
        assert!(why.contains(want_why), "{id}: {why}");
    }
}
