Grok review: 458c-c, the doctor report assembler and doctor's installation check, and inventory v80. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-doctor-report458cc-r1.

Law: `docs/implementation/m2/read-premise-458c/PROPOSAL.md` r6 (accepted), items 7, 10 and 12. Also owner.md §5 Diagnostics, the reference `doctor_projection.py` `DoctorSession.assemble`, and `doctor-cases.json`.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-458cc`, based on 417d443. Its diff is product.diff in your output directory.
- **Arch:** v80, `doctor-report-inventory-v80-subject.json`, and `doctor-report-inventory-v80/`.

## What it does

- **Security** (`custody/installation_doctor.rs`):
  - `InstallationFinding { Missing{path}, Pair, Marker, Store, Node, Chain }` and `DoctorInstallation { Complete, Incomplete(Vec) }`.
  - `observe_installation_for_doctor()` uses the same receipt and session (`observe_with`). It returns findings instead of the incomplete row, and every other outcome takes its item 6 row. The fence is released before return.
  - The match is exhaustive. `Missing` of a non-file entry is `Invariant`.
  - Non-doctor `acquire` is unchanged.
- **Host** (`doctor_report.rs`):
  - `DoctorReportSession::assemble(complete, actual, report_producible)` mirrors the reference `DoctorSession`:
    - 255 entries with the note, 256 without;
    - an actual defect with the note's code refuses;
    - any refusal latches.
  - `DoctorReportV1 { result: Invocation5DoctorResult, termination: DoctorTerminationV1 }`:
    - success is exit 0, with `DOCTOR.DEFECTS_FOUND` only when the count is above 0;
    - not producible is operational-failed, 4, `HOST.IO_FAILURE`, `host-io`, `DOCTOR.REPORT_NOT_PRODUCIBLE`.
  - `installation_defect` maps a finding to `CONFIG.CUSTODY_REFUSED` with the r6 item 12 subject.
  - `doctor_installation(session, observed, other) -> Report | Refused(row)`.
- **Remedy texts:** see the `REMEDY_*` constants. Each says the installation is incomplete, names the finding kind, and says "OpenSIP does not repair an incomplete installation."

## Judgment calls: please rule on each

1. The assembler is in host, next to the generated D9 types, and the installation check is in security.
2. `DoctorTerminationV1` is a new host struct, because a success termination has no error code. It adds no envelope member.
3. A finding subject over the `BoundedText` limit makes the report not producible, rather than truncated.
4. The report session is not latched when I is unreachable. The item 6 row ends doctor before assembly.
5. `other` defects are a parameter; no other doctor checks exist yet.
6. `trust doctor` and `store status` have no report producer in the product, so there is no note path to test.
7. The `doctor-cases.json` vectors are restated in Rust with the source sha256 in a comment, because product tests cannot read the arch tree.

## Tests and checks

- **Host, 9 tests:**
  - all 8 vectors;
  - the note placement, text, lack of subject and lack of count;
  - 4-member serialization;
  - the latch;
  - a healthy installation gives 0 with the note, and 1 defect gives 1;
  - 6 findings give 6 entries and no note;
  - 256 and 257, and 255 plus the note and 256 plus the note;
  - over-long subjects;
  - unreachable rows.
- **Security, 6 tests on a real published scratch installation:**
  - complete;
  - two missing members in order;
  - pair, marker, node and a missing node;
  - a missing H goes to `HostIo`;
  - busy through the wait;
  - a 0644 member goes to custody.
- Workspace: 1138/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- `verify_scratch` passes with v80.

## Decide

- Does it implement r6 items 7, 10 and 12 and owner §5 exactly: counts, slots, note, bounds, latch, no truncation, and the per-finding entries?
- Rule on the judgment calls.
- Are v80 and the inheritance right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of doctor-report-inventory-v80-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v80, parent (the v79 pin), successorRecord (the pin of doctor-report-inventory-v80/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
