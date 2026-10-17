// Unit C1a3's sealing controls (C1a plan r4 as amended by r6, section C1a3):
// each walks a scratch project under security's scenario home, through the
// durable route's snapshot root, then seals it.
use super::*;
use crate::snapshot::tests::{
    custodied, custody_dir, insert_reached, no_boundaries, session, sha, write,
};
use crate::snapshot::{ReadError, ReadFailure};
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes, digest_hex};
use opensip_platform::WorkLedger;
use opensip_security::scenario::ScenarioHome;
use opensip_security::snapshot_source::{SnapshotCustody, SnapshotTracking};
use opensip_security::snapshot_walk::SnapshotExtent;
use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;

fn project_id() -> String {
    format!("prj1-{}", "a".repeat(64))
}
const CONFIG: &str = "1111111111111111111111111111111111111111111111111111111111111111";
const SCOPE: &str = "2222222222222222222222222222222222222222222222222222222222222222";

/// One sealing attempt's outcome, and the inventory the session held.
struct Outcome {
    sealed: Result<SealedSnapshot, String>,
    rows: Vec<(String, [u8; 32], u64)>,
    tracking: SnapshotTracking,
    inventory_blob: Option<Vec<u8>>,
}

/// Walk `root` (no boundaries, the given `ignorePaths`) into a fresh session,
/// running `before` on it first (pre-walk captures, synthetic rows), then
/// seal it with `carrier` and `members`.
fn seal_tree(
    home: &ScenarioHome,
    root: &Path,
    ignore: &[&str],
    carrier: ProjectCarrierObservation,
    members: &[String],
    before: impl FnOnce(&mut CaptureSession, &SnapshotRoot<'_>, SnapshotCustody<'_>, &mut WorkScope<'_>),
) -> Outcome {
    let (_custody, dir) = custody_dir();
    let bounds = no_boundaries();
    let member_roots = BTreeSet::new();
    let ignore: Vec<String> = ignore.iter().map(|s| (*s).to_owned()).collect();
    let extent = WorkLedger::discovery_profile()
        .scope(|work| SnapshotExtent::new(&bounds, &member_roots, &ignore, work))
        .unwrap();
    let registry = crate::embedded_schema_registry().unwrap();
    let project = project_id();
    home.with_snapshot_root(root, |snapshot, judge| {
        WorkLedger::discovery_profile()
            .scope(|work| {
                let mut session = session(&dir, work);
                before(&mut session, snapshot, judge, work);
                let report = session.walk(snapshot, judge, &extent, work)?;
                let inputs = SealInputs {
                    project_id: &project,
                    resolved_config_digest: CONFIG,
                    scope_digest: SCOPE,
                    carrier,
                    members,
                };
                let sealed = seal(&mut session, snapshot, &report, &inputs, &registry, work);
                let rows = session
                    .inventory()
                    .map(|(p, c)| (p.to_owned(), c.sha256, c.bytes))
                    .collect();
                let inventory_blob = sealed
                    .as_ref()
                    .ok()
                    .map(|s| s.source_inventory_digest)
                    .map(|digest| custodied(&mut session, &digest, work));
                Ok::<_, ReadFailure>(Outcome {
                    sealed: sealed.map_err(|f| format!("{f:?}")),
                    rows,
                    tracking: snapshot.tracking(),
                    inventory_blob,
                })
            })
            .unwrap()
    })
    .unwrap()
}

fn row_value(path: &str, sha256: &[u8; 32], bytes: u64) -> V {
    V::Object(BTreeMap::from_iter([
        (
            "bytes".to_owned(),
            V::Integer(JsonInteger::new(i128::from(bytes)).unwrap()),
        ),
        ("path".to_owned(), V::String(path.to_owned())),
        ("sha256".to_owned(), V::String(digest_hex(sha256))),
    ]))
}

/// C1-T17 and the record (item 1): the sealed descriptor is the canonical
/// encoding of `{schemaVersion: 2, projectId, sourceInventory,
/// resolvedConfigDigest, scopeDigest, vcsDigest}`, built here independently
/// with the identity crate's encoder; `sourceInventoryDigest` is the
/// inventory's canonical SHA-256 and its custody blob is those bytes; and
/// `snapshot2` is identity-v3's snapshot id of that descriptor. The project
/// carrier stays in the inventory.
#[test]
fn a_sealed_snapshot_is_its_canonical_descriptor_and_snapshot2() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a3-record");
    write(&root, "a.txt", b"alpha");
    write(&root, "src/lib.rs", b"pub fn f() {}\n");
    write(&root, "opensip.json", b"{}\n");
    let carrier = ProjectCarrierObservation::Present {
        sha256: raw_sha256(b"{}\n"),
    };
    let out = seal_tree(&home, &root, &[], carrier, &[], |_, _, _, _| {});
    assert_eq!(out.tracking, SnapshotTracking::NoRepository);
    let sealed = out.sealed.unwrap();
    let paths: Vec<&str> = out.rows.iter().map(|(p, _, _)| p.as_str()).collect();
    assert_eq!(paths, ["a.txt", "opensip.json", "src/lib.rs"]);
    let inventory = V::Array(
        out.rows
            .iter()
            .map(|(p, s, b)| row_value(p, s, *b))
            .collect(),
    );
    let inventory_bytes = canonical_bytes(&inventory).unwrap();
    assert_eq!(sealed.source_inventory_digest, raw_sha256(&inventory_bytes));
    assert_eq!(out.inventory_blob.unwrap(), inventory_bytes);
    let vcs = V::Object(BTreeMap::from_iter([
        (
            "schemaVersion".to_owned(),
            V::Integer(JsonInteger::new(2).unwrap()),
        ),
        ("kind".to_owned(), V::String("none".to_owned())),
        ("commitId".to_owned(), V::Null),
        ("dirty".to_owned(), V::Bool(false)),
        (
            "sourceInventoryDigest".to_owned(),
            V::String(digest_hex(&raw_sha256(&inventory_bytes))),
        ),
    ]));
    let registry = crate::embedded_schema_registry().unwrap();
    // The VCS record admits as identity-v3's `vcs-observation`.
    registry
        .schema(
            "urn:opensip:product-v1:identity:v3",
            "/$defs/vcs-observation",
        )
        .unwrap()
        .admit_json(&canonical_bytes(&vcs).unwrap(), 100_000)
        .unwrap();
    let descriptor = V::Object(BTreeMap::from_iter([
        (
            "schemaVersion".to_owned(),
            V::Integer(JsonInteger::new(2).unwrap()),
        ),
        ("projectId".to_owned(), V::String(project_id())),
        ("sourceInventory".to_owned(), inventory),
        (
            "resolvedConfigDigest".to_owned(),
            V::String(CONFIG.to_owned()),
        ),
        ("scopeDigest".to_owned(), V::String(SCOPE.to_owned())),
        (
            "vcsDigest".to_owned(),
            V::String(digest_hex(&raw_sha256(&canonical_bytes(&vcs).unwrap()))),
        ),
    ]));
    let expected = canonical_bytes(&descriptor).unwrap();
    assert_eq!(sealed.descriptor, expected);
    let id =
        IdentityCandidate::from_json(&registry, IdentityDomain::Snapshot, &expected, 10_000_000)
            .unwrap()
            .identifier()
            .to_owned();
    assert_eq!(sealed.snapshot2, id);
    assert!(sealed.snapshot2.starts_with("snapshot2:"));
    assert_eq!((sealed.rows, sealed.total_bytes), (3, 5 + 14 + 3));
}

/// The hand encoders write exactly the identity crate's canonical bytes, so
/// the counted lengths are the encoded ones.
#[test]
fn the_encoders_write_the_canonical_encoders_bytes() {
    for text in [
        "",
        "a",
        "a\"b",
        "c\\d",
        "\u{1}\u{8}\u{c}\n\r\t\u{1f}",
        "\u{e9}t\u{e9}",
        "\u{65e5}\u{672c}",
        "\u{1f600}",
        "src/a b/c.rs",
    ] {
        let canonical = canonical_bytes(&V::String(text.to_owned())).unwrap();
        let mut ours = Vec::new();
        push_string(&mut ours, text);
        assert_eq!(ours, canonical, "{text:?}");
        assert_eq!(string_len(text), canonical.len(), "{text:?}");
    }
    for n in [0u64, 9, 10, 99, 100, 1 << 32, u64::MAX] {
        let mut ours = Vec::new();
        push_decimal(&mut ours, n);
        assert_eq!(ours, n.to_string().as_bytes());
        assert_eq!(decimal_len(n), ours.len());
        let sha256 = raw_sha256(&n.to_be_bytes());
        let canonical = canonical_bytes(&row_value("p\"\n", &sha256, n)).unwrap();
        let mut row = Vec::new();
        push_row(&mut row, "p\"\n", &sha256, n);
        assert_eq!(row, canonical);
        assert_eq!(row_len("p\"\n", n), canonical.len());
    }
}

fn refusal(out: &Outcome) -> &str {
    out.sealed
        .as_ref()
        .err()
        .map(String::as_str)
        .unwrap_or("sealed")
}

/// C1-T26 (item 1 rule 2): the carrier join, one case per table row. X2
/// captures the carrier when the root is admitted; each change happens
/// after that capture and before the walk. None retries, and no refusal
/// mints a snapshot.
#[test]
fn the_carrier_join_has_one_outcome_per_row() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let bytes: &[u8] = b"{\"x\":1}\n";
    let present = ProjectCarrierObservation::Present {
        sha256: raw_sha256(bytes),
    };
    let absent = ProjectCarrierObservation::Absent;
    // `admitted`: whether the carrier exists when X2 admits the root;
    // `change`: what happens to it after X2's capture, before the walk.
    let case = |name: &str, admitted: bool, change: &dyn Fn(&Path), ignore: &[&str], carrier| {
        let root = home.project(name);
        write(&root, "a.txt", b"a");
        if admitted {
            write(&root, "opensip.json", bytes);
        }
        let at = root.clone();
        seal_tree(&home, &root, ignore, carrier, &[], move |_, _, _, _| {
            change(&at)
        })
    };
    let stable = |_: &Path| {};
    assert!(
        case("c1a3-present", true, &stable, &[], present)
            .sealed
            .is_ok()
    );
    assert!(
        case("c1a3-absent", false, &stable, &[], absent)
            .sealed
            .is_ok()
    );
    let changed = case(
        "c1a3-digest",
        true,
        &|r| write(r, "opensip.json", b"{}\n"),
        &[],
        present,
    );
    assert!(
        refusal(&changed).contains("CarrierChanged(Digest)"),
        "{}",
        refusal(&changed)
    );
    let removed = case(
        "c1a3-present-absent",
        true,
        &|r| std::fs::remove_file(r.join("opensip.json")).unwrap(),
        &[],
        present,
    );
    assert!(refusal(&removed).contains("CarrierChanged(PresentAbsent)"));
    let created = case(
        "c1a3-absent-present",
        false,
        &|r| write(r, "opensip.json", bytes),
        &[],
        absent,
    );
    assert!(refusal(&created).contains("CarrierChanged(AbsentPresent)"));
    let directory = case(
        "c1a3-type-directory",
        true,
        &|r| {
            std::fs::remove_file(r.join("opensip.json")).unwrap();
            write(r, "opensip.json/inner.txt", b"i");
        },
        &[],
        present,
    );
    assert!(
        refusal(&directory).contains("CarrierChanged(Type)"),
        "{}",
        refusal(&directory)
    );
    let link = case(
        "c1a3-type-symlink",
        true,
        &|r| {
            std::fs::remove_file(r.join("opensip.json")).unwrap();
            std::os::unix::fs::symlink("a.txt", r.join("opensip.json")).unwrap();
        },
        &[],
        present,
    );
    assert!(
        refusal(&link).contains("CarrierChanged(Type)"),
        "{}",
        refusal(&link)
    );
    let special = case(
        "c1a3-type-fifo",
        true,
        &|r| {
            std::fs::remove_file(r.join("opensip.json")).unwrap();
            let made = std::process::Command::new("/usr/bin/mkfifo")
                .arg(r.join("opensip.json"))
                .status()
                .unwrap();
            assert!(made.success());
        },
        &[],
        present,
    );
    assert!(
        refusal(&special).contains("CarrierChanged(Type)"),
        "{}",
        refusal(&special)
    );
    let excluded = case("c1a3-excluded", true, &stable, &["opensip.json"], present);
    assert!(
        refusal(&excluded).contains("CarrierChanged(Excluded)"),
        "{}",
        refusal(&excluded)
    );
    // An excluded carrier is never inventoried.
    assert!(excluded.rows.iter().all(|(p, _, _)| p != "opensip.json"));
}

/// Item 1: a capture the walk never reaches (here under `ignorePaths`)
/// refuses at sealing, rather than binding an uninventoried byte.
#[test]
fn a_leftover_capture_refuses_at_sealing() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a3-leftover");
    write(&root, "a.txt", b"a");
    write(&root, "ignored/package.json", b"{}");
    let out = seal_tree(
        &home,
        &root,
        &["ignored"],
        ProjectCarrierObservation::Absent,
        &[],
        |session, snapshot, judge, work| {
            session
                .capture(snapshot, "ignored/package.json", judge, work)
                .unwrap();
        },
    );
    assert!(
        refusal(&out).contains("LeftoverCapture(\"ignored/package.json\")"),
        "{}",
        refusal(&out)
    );
}

/// C1A-T4 (LD-C1A-5): a NoRepository root with one admitted Git member is
/// C1b's, so sealing refuses `SnapshotVcsPending`.
#[test]
fn a_root_with_an_admitted_member_is_vcs_pending() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("c1a3-member");
    write(&root, "a.txt", b"a");
    let out = seal_tree(
        &home,
        &root,
        &[],
        ProjectCarrierObservation::Absent,
        &["member".to_owned()],
        |_, _, _, _| {},
    );
    assert_eq!(out.tracking, SnapshotTracking::NoRepository);
    assert_eq!(refusal(&out), "Operation(VcsPending)");
}

/// The rows of `count` synthetic captures `p<index>`, padded so they sort.
fn synthetic(session: &mut CaptureSession, count: usize, bytes: u64) {
    for index in 0..count {
        insert_reached(session, &format!("p{index:06}"), sha(b"x"), bytes);
    }
}

/// C1-T18 to C1-T21 (item 5), each at step 5: 100,001 rows refuse `rows`
/// (and 100,000 rows pass the row bound, to be refused by the descriptor);
/// a descriptor of exactly 4 MiB admits and one byte more refuses
/// `descriptor`, though its inventory alone fits; exactly 8 GiB admits and
/// one byte more refuses `totalBytes`. Each refusal carries its field,
/// observed value and limit, and mints nothing: no snapshot and no
/// inventory blob.
#[test]
fn the_bounds_refuse_one_past_each_and_admit_at_each() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let rows = |count: usize| {
        let root = home.project(&format!("c1a3-rows-{count}"));
        seal_tree(
            &home,
            &root,
            &[],
            ProjectCarrierObservation::Absent,
            &[],
            |s, _, _, _| synthetic(s, count, 1),
        )
    };
    let over = rows(100_001);
    assert_eq!(
        refusal(&over),
        "Operation(Bound { field: Rows, observed: 100001, limit: 100000 })"
    );
    assert!(refusal(&rows(100_000)).contains("Bound { field: Descriptor"));

    // A descriptor of exactly `target` bytes: rows of a fixed path length,
    // then one row whose path makes up the rest.
    let project = project_id();
    let inputs = SealInputs {
        project_id: &project,
        resolved_config_digest: CONFIG,
        scope_digest: SCOPE,
        carrier: ProjectCarrierObservation::Absent,
        members: &[],
    };
    let exact = |target: usize| {
        let root = home.project(&format!("c1a3-descriptor-{target}"));
        seal_tree(
            &home,
            &root,
            &[],
            ProjectCarrierObservation::Absent,
            &[],
            |s, _, _, _| {
                let mut inventory = 2usize;
                let mut index = 0usize;
                let name = |index: usize, extra: usize| format!("d{index:06}{}", "x".repeat(extra));
                loop {
                    let full = row_len(&name(index, 180), 1) + usize::from(index > 0);
                    if descriptor_len(&inputs, inventory + full)
                        + row_len(&name(index + 1, 0), 1)
                        + 1
                        > target
                    {
                        break;
                    }
                    insert_reached(s, &name(index, 180), sha(b"x"), 1);
                    inventory += full;
                    index += 1;
                }
                let rest =
                    target - descriptor_len(&inputs, inventory) - 1 - row_len(&name(index, 0), 1);
                let last = name(index, rest);
                insert_reached(s, &last, sha(b"x"), 1);
                assert_eq!(
                    descriptor_len(&inputs, inventory + 1 + row_len(&last, 1)),
                    target
                );
            },
        )
    };
    let at = exact(MAX_BYTES);
    let sealed = at.sealed.unwrap();
    assert_eq!(sealed.descriptor.len(), MAX_BYTES);
    let past = exact(MAX_BYTES + 1);
    assert_eq!(
        refusal(&past),
        format!(
            "Operation(Bound {{ field: Descriptor, observed: {}, limit: {MAX_BYTES} }})",
            MAX_BYTES + 1
        )
    );

    let total = |bytes: u64| {
        let root = home.project(&format!("c1a3-total-{bytes}"));
        seal_tree(
            &home,
            &root,
            &[],
            ProjectCarrierObservation::Absent,
            &[],
            |s, _, _, _| synthetic(s, 1, bytes),
        )
    };
    assert!(total(MAX_TOTAL_BYTES).sealed.is_ok());
    let past = total(MAX_TOTAL_BYTES + 1);
    assert_eq!(
        refusal(&past),
        format!(
            "Operation(Bound {{ field: TotalBytes, observed: {}, limit: {MAX_TOTAL_BYTES} }})",
            MAX_TOTAL_BYTES + 1
        )
    );
    // Nothing is minted on a refusal, not even the inventory blob.
    assert!(past.inventory_blob.is_none());
}

/// C1A-T6's composition: an over-8-GiB inventory is preloaded into the
/// session, then the walk runs, and sealing is reached only through the
/// walk's own `Ok` report. `install` sets the case's injection, given
/// `z.txt`'s path. Returns the walk's refusal, if any, and the sealing
/// outcome, if sealing ran.
fn over_bound_then_walk(
    home: &ScenarioHome,
    case: &str,
    z: &[u8],
    install: impl FnOnce(std::path::PathBuf),
) -> (Option<ReadFailure>, Option<Result<SealedSnapshot, String>>) {
    let root = home.project(&format!("c1a3-order-{case}"));
    write(&root, "a.txt", b"a");
    write(&root, "z.txt", z);
    install(root.join("z.txt"));
    let (_custody, dir) = custody_dir();
    let bounds = no_boundaries();
    let members = BTreeSet::new();
    let extent = WorkLedger::discovery_profile()
        .scope(|work| SnapshotExtent::new(&bounds, &members, &[], work))
        .unwrap();
    let registry = crate::embedded_schema_registry().unwrap();
    let project = project_id();
    home.with_snapshot_root(&root, |snapshot, judge| {
        WorkLedger::discovery_profile()
            .scope(|work| {
                let mut session = session(&dir, work);
                synthetic(&mut session, 1, MAX_TOTAL_BYTES + 1);
                let report = match session.walk(snapshot, judge, &extent, work) {
                    Ok(report) => report,
                    Err(refused) => return Ok::<_, ReadFailure>((Some(refused), None)),
                };
                let inputs = SealInputs {
                    project_id: &project,
                    resolved_config_digest: CONFIG,
                    scope_digest: SCOPE,
                    carrier: ProjectCarrierObservation::Absent,
                    members: &[],
                };
                let sealed = seal(&mut session, snapshot, &report, &inputs, &registry, work);
                Ok((None, Some(sealed.map_err(|f| format!("{f:?}")))))
            })
            .unwrap()
    })
    .unwrap()
}

/// C1A-T6 and item 6's order: the walk is step 1, and sealing takes the
/// walk's report only on its `Ok`, so with an over-8-GiB inventory already
/// held, a later read failure, a change during a read and a custody write
/// failure each refuse with their own refusal, and sealing never runs. The
/// control (no injection) reaches sealing and refuses `totalBytes`. The walk
/// itself judges no total: nothing in the session or the walk names the
/// bound. That the report is this session's walk is the composition's
/// precondition (NBO-1 binds it when J2 composes the production path); the
/// report's type does not prove it.
#[test]
fn walk_refusals_come_before_the_bounds() {
    use crate::candidate_custody::{WRITE_HOOK, WriteInjection};
    use crate::snapshot::{READ_HOOK, ReadPoint};
    let home = ScenarioHome::create(&std::env::temp_dir());

    let (walked, sealed) = over_bound_then_walk(&home, "control", b"zz", drop);
    assert!(walked.is_none());
    assert!(
        sealed.unwrap().unwrap_err().contains("field: TotalBytes"),
        "the control reaches step 5"
    );

    let (walked, sealed) = over_bound_then_walk(&home, "read", b"zz", |_| {
        READ_HOOK.with_borrow_mut(|h| {
            *h = Some(Box::new(|path: &str, point| match point {
                ReadPoint::BeforeCall(1) if path == "z.txt" => {
                    Some(std::io::Error::other("injected"))
                }
                _ => None,
            }))
        })
    });
    READ_HOOK.with_borrow_mut(|h| *h = None);
    assert!(
        matches!(walked, Some(WorkFailure::Operation(ReadError::Read { ref path, .. })) if path == "z.txt"),
        "{walked:?}"
    );
    assert!(sealed.is_none());

    let big = vec![b'z'; 2 * READ_CHUNK];
    let (walked, sealed) = over_bound_then_walk(&home, "changed", &big, |target| {
        READ_HOOK.with_borrow_mut(|h| {
            *h = Some(Box::new(move |path: &str, point| {
                if path == "z.txt" && matches!(point, ReadPoint::BeforeCall(2)) {
                    use std::io::Write;
                    let mut f = std::fs::OpenOptions::new()
                        .append(true)
                        .open(&target)
                        .unwrap();
                    f.write_all(b"more").unwrap();
                }
                None
            }))
        })
    });
    READ_HOOK.with_borrow_mut(|h| *h = None);
    assert!(
        matches!(walked, Some(WorkFailure::Operation(ReadError::ChangedDuringRead(ref path))) if path == "z.txt"),
        "{walked:?}"
    );
    assert!(sealed.is_none());

    // z.txt's one chunk is its 2 bytes; a.txt's is 1.
    let (walked, sealed) = over_bound_then_walk(&home, "custody", b"zz", |_| {
        WRITE_HOOK.with_borrow_mut(|h| {
            *h = Some(Box::new(|chunk| {
                (chunk == 2).then(|| WriteInjection::Fail(std::io::Error::other("injected")))
            }))
        })
    });
    WRITE_HOOK.with_borrow_mut(|h| *h = None);
    assert!(
        matches!(walked, Some(WorkFailure::Operation(ReadError::Custody(_)))),
        "{walked:?}"
    );
    assert!(sealed.is_none());

    for module in [
        include_str!("snapshot.rs"),
        include_str!("../../security/src/snapshot_walk.rs"),
    ] {
        assert!(!module.contains("MAX_TOTAL_BYTES") && !module.contains("8_589_934_592"));
    }
}

/// r2 (Codex C1A3-R1-RF-1): sealing's every heap allocation is charged
/// before it happens. The digest hex is written from a stack array, equal to
/// the identity crate's hex; the production source names no other
/// allocating conversion; and each allocation site's nearest preceding
/// charge is its own exact length.
#[test]
fn sealing_allocates_only_what_it_charges() {
    for digest in [[0u8; 32], [0xff; 32], sha(b"x")] {
        assert_eq!(
            hex_digits(&digest).as_slice(),
            digest_hex(&digest).as_bytes()
        );
    }
    let source = include_str!("snapshot_seal.rs");
    let production = &source[..source.find("#[cfg(test)]").unwrap()];
    for conversion in [
        "digest_hex",
        "format!",
        "to_string",
        "String::",
        "vec!",
        "collect",
        "Box::",
        "clone()",
        "concat",
        "join(",
        "to_vec",
    ] {
        assert!(!production.contains(conversion), "{conversion}");
    }
    let lines: Vec<&str> = production.lines().collect();
    let sites: Vec<usize> = (0..lines.len())
        .filter(|&at| lines[at].contains("with_capacity(") || lines[at].contains("to_owned()"))
        .collect();
    assert_eq!(sites.len(), 5, "{sites:?}");
    assert_eq!(production.matches("Vec::with_capacity(160)").count(), 1);
    for (allocation, charge) in [
        ("leftover.to_owned()", "owned_record(leftover.len())"),
        (
            "Vec::with_capacity(inventory_len)",
            "owned_record(inventory_len)",
        ),
        // none_observation's own Vec::with_capacity(160).
        ("none_observation(&inventory_digest)", "owned_record(160)"),
        (
            "Vec::with_capacity(descriptor_bytes)",
            "owned_record(descriptor_bytes)",
        ),
        (
            "candidate.identifier().to_owned()",
            "owned_record(\"snapshot2:\".len() + 64)",
        ),
    ] {
        let at = lines.iter().position(|l| l.contains(allocation)).unwrap();
        let charged = lines[..at]
            .iter()
            .rev()
            .find(|l| l.contains("work.charge"))
            .unwrap();
        assert!(charged.contains(charge), "{allocation}: {charged}");
    }
}

/// C1-T11 (with C1a1): two copies of one tree, differing only in a pruned
/// `target/` beside `Cargo.toml` and in unread `node_modules` files, seal to
/// the same `snapshot2`.
#[test]
fn pruned_contents_do_not_move_snapshot2() {
    let home = ScenarioHome::create(&std::env::temp_dir());
    let ids: Vec<String> = ["one", "two"]
        .into_iter()
        .map(|variant| {
            let root = home.project(&format!("c1a3-pruned-{variant}"));
            write(&root, "Cargo.toml", b"[package]\nname = \"p\"\n");
            write(&root, "src/lib.rs", b"pub fn f() {}\n");
            write(&root, &format!("target/{variant}.o"), variant.as_bytes());
            write(
                &root,
                &format!("node_modules/{variant}/index.js"),
                variant.as_bytes(),
            );
            seal_tree(
                &home,
                &root,
                &[],
                ProjectCarrierObservation::Absent,
                &[],
                |_, _, _, _| {},
            )
            .sealed
            .unwrap()
            .snapshot2
        })
        .collect();
    assert_eq!(ids[0], ids[1]);
}

/// C1-T23's source pin: the descriptor builder takes no operational value,
/// no request or execution id, process id, clock or host path.
#[test]
fn no_operational_value_reaches_the_descriptor() {
    let code = include_str!("snapshot_seal.rs");
    let production = code.split("#[cfg(test)]\n#[path").next().unwrap();
    for word in [
        "RequestId",
        "request_id",
        "ExecutionId",
        "execution_id",
        "process::id",
        "SystemTime",
        "Instant",
        "spelling",
        "env::",
    ] {
        assert!(!production.contains(word), "{word}");
    }
    // The descriptor's fields are exactly the record's six.
    let descriptor = include_str!("snapshot_seal.rs");
    for field in [
        "projectId",
        "resolvedConfigDigest",
        "schemaVersion",
        "scopeDigest",
        "sourceInventory",
        "vcsDigest",
    ] {
        assert!(descriptor.contains(field), "{field}");
    }
}
