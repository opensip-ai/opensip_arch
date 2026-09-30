# Review: doctor report 458c-c and inventory v80

Grok is the single reviewer. Claude Opus 5.5 leads. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-458cc` at `417d44362e07b61ca3c34e9bfc1bc5ea76406eba`. The seven uncommitted product files match hashes.txt. `product.diff` is 37824 bytes, sha256 `c1816e65be36a50716833da6f37b0c1f43c676fb5b10599bcdfc5de7ffbf8561`. `~/Library/Application Support/OpenSIP` is absent and is not a symlink. Law is 458c r6 items 7, 10 and 12, with owner §5 Diagnostics, `DoctorSession.assemble`, and `doctor-cases.json`.

## Verdict

**ACCEPT-UNIT.**

Doctor observes I through the same receipt and session as every other read. A reachable incomplete I comes back as one finding per structural defect, and the host assembler turns those findings into the existing doctor report. An unreachable I ends on its item 6 row with no report. Inventory v80 adds four rows and keeps every inherited row equal to v79.

## Items 7, 10 and 12

`observe_installation_for_doctor` mints the read receipt, begins one observation session, and calls `observe_with`. Step 4 still runs after the member reads. An ordinary failure or a failed recheck returns that item 6 row, so doctor produces no report. When the recheck succeeds, every `IncompleteRefusal` is returned and the fence is released. `retain` still calls `complete()`, so every other read command keeps the single incomplete row. The session flag is spent on entry, which is the one session per process. A structural finding stays `Ok`, and the report session stays open.

`findings` maps `Missing(Entry::File)` to `InstallationFinding::Missing { path }`, and Pair, Marker, Store, Node and Chain to those variants. `Missing` of Home, Installation or Parent is `Invariant`. `open_regular` reports a non-regular leaf as `InvalidInput`, and `missing()` treats that as a missing member, so a non-regular required file is the missing finding with its path relative to I.

`DoctorReportSession::assemble` follows the reference. A complete I allows 255 actual defects and then appends `INSTALLATION.DURABILITY_NOT_CHECKED` with owner §5's remedy and no subject. A report without the note allows 256. `defectsFound` counts every entry except that code. A positive count sets `DOCTOR.DEFECTS_FOUND` with the reference remedy `inspect doctor.defects; exit 0 means the report was produced`, on success, exit 0, with no error code. An actual defect that already carries the note's code, a list over the bound, or `report_producible` false sets the latch and projects operational-failed, exit 4, `HOST.IO_FAILURE`, fault `host-io`, detail `DOCTOR.REPORT_NOT_PRODUCIBLE`, remedy `Resolve the report-production failure and run doctor again.` The projected result is `Invocation5DoctorResult`: `kind`, `reportProduced`, `defectsFound`, `defects`.

`installation_defect` uses `CONFIG.CUSTODY_REFUSED` and the item 12 subjects. Each `REMEDY_*` says the installation is incomplete, names the kind, and ends with "OpenSIP does not repair an incomplete installation." `doctor_installation` places installation findings first and appends `other`. A subject or remedy that `BoundedText` refuses (1024 characters) makes the whole report not producible. The defects array stays empty.

The eight `doctor-cases.json` rows are restated in `CASES`. The file is 1625 bytes, sha256 `21668676e87f2e85f9fc7aeb66d1f381fec4e6883fb9515f66f31e541fb33f01`, the hash named in the test. The inherited pair is `DELIVERY.CLOSURE_BYTES_CORRUPT` then `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`.

## Judgments

1. **Crate split: ACCEPT.** The installation check stays in security, on the observation session, and returns findings or an `InstallationTermination`. The assembler stays in host, beside `installation_termination` and the generated D9 types. Host already depends on security and contracts. The diff adds no crate and no dependency. `custody.rs` and the two lib roots only wire the module and the exports.

2. **`DoctorTerminationV1`: ACCEPT.** `InstallationTerminationV1` requires an error code. A produced doctor report is success with no error code, and `DOCTOR.DEFECTS_FOUND` only when the count is positive, matching `terminate()` for `doctor-report`. The struct is host state. The serialized result keeps the schema's four members.

3. **Over-long subject: ACCEPT.** `installation_defect` returns `ReportUnavailable` when the subject exceeds `BoundedText`. `doctor_installation` then assembles with `report_producible` false. The session latches, the result has no defects, and the termination is the not-producible row. A path of 1100 `p`s is that case. Nothing is shortened to fit.

4. **Unreachable I: ACCEPT.** `doctor_installation` returns `Refused(installation_termination(row))` before `assemble`. The report session stays unfailed. The host test covers no embedded release, host I/O, busy, custody and budget. On a published scratch P0, a missing H is `HostIo`, a fence held through the stepping clock is `Busy`, and mode `0644` on `project-registry.v2` is custody. Those are ordinary failures, so they are not findings.

5. **`other` defects: ACCEPT.** They are an already admitted list. No other doctor check exists in the product. On a complete I they count, and the note is appended. On an incomplete I they sit after the findings, and the note is absent. The note's code inside that list is refused, as the reference refuses an actual defect carrying the informational code.

6. **No note on `trust doctor` or `store status`: ACCEPT.** The only assembler is `doctor_installation` / `DoctorReportSession`. Nothing else in the crates calls it. Those two commands have no report producer, so they have no path that emits the note.

7. **Restated vectors: ACCEPT.** Product tests do not read the architecture tree. `CASES` carries each case's id, complete flag, actual count, producible flag, produced flag, count, entry count, exit and notice. The note text, its missing subject, and its exclusion from the count are asserted separately. The human label is a public constant equal to owner §5's sentence and is not a result field.

## Inventory v80

`repository-file-inventory.v80.json` is 313526 bytes, sha256 `838a7f4072b408e8c4011249c89e0974d38616031cda110267c92ab762d0d1e7`. Parent v79 is `docs/implementation/m2/repository-file-inventory.v79.json`, 310321 bytes, sha256 `baf79f6f655bde83a4622d6bd22c37e1294ff4a36646048ceef99f8f5e5a355f`. `successor.json` is 9588 bytes, sha256 `09abb285733f6ae1352c6940fbb409de411ba3798fac888eae7b7f887d769af7`. The subject manifest is 2069 bytes, sha256 `18ba01796139de676b9e962568330b92d35afea727e1bbe8bdbe80c33f983432`. The README is 2453 bytes, sha256 `7577b7b04ed8afe1b9522ec6b32193f234123cf853def40a7dbe3ec58a012774`.

Rows go from 745 to 749. Paths stay sorted and unique. The path set is v79 plus `doctor_report.rs` (adapter, proposed, opensip-host), `doctor_report_tests.rs` (test), `installation_doctor.rs` (service, opensip-security) and `installation_doctor_tests.rs` (test). Every inherited row equals its v79 value. Packages and pending decisions are unchanged. Standing is retitled to the doctor report layout and keeps the same non-qualification sentence. The successor records `inheritedRowsEqualByValue`, `packageDependencyGraphUnchanged` and `pendingDecisionsInheritedUnchanged`, and its parent pin is v79.

The eight path-bound overrides are unchanged: `apps/cli/src/bootstrap.rs`, `apps/report/package.json`, `crates/host/src/installation_lineage.rs`, `crates/identity/src/store_lineage.rs`, `crates/security/src/initial_installation.rs`, `crates/security/src/private_access.rs`, `package.json` and `schemas/sources/imported-v1.schema.json`. Selectors before the host insertion stay put. `installation_lineage.rs` and `store_lineage.rs` move by the two host files. The four security and root selectors move by all four insertions. The five stale descriptions named in v79 stay byte-equal, and the README defers them to a later contract successor. The descriptions of `custody.rs`, `crates/security/src/lib.rs` and `crates/host/src/lib.rs` still describe those roots. The helper is `c890b35f281bef71bc876088caae13886a6057c71717250348ee008e2612dfda`, 2917 bytes. Re-running `verify_projection.py` with `python3 -I -B` against the architecture tree and `/Users/sb/code/opensip-ai/opensip/design-lock.json` printed 8 rows, PASS, 43 corruptions. `verification.stdout` is the 124-byte record, sha256 `dcf19ff444814b39edde13a1ab14b27f92ef670656e4ef42ed1ad70a7b577eea`.

The lead reported the workspace sum 1138/0 on two runs, clippy and fmt clean, `check_package_edges --lane host`, and `verify_scratch` with v80. This review did not replay cargo.

## Required findings

None.
