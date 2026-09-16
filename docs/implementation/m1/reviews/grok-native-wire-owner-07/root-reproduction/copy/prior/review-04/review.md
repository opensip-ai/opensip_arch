# Review 04: resumed independent delta review of native wire owner, author candidate 04

**Verdict: changes-required.** Four new required findings and five advisories follow.

**Standing.** This is a resumed review from my review-03 context, not a fresh session. No subagents, background jobs, commits, push or private-session inspection were used. It is a review only: it is not approval, source promotion, provider admission, codec, runtime, sender or generator qualification, and it claims no platform, M2, M3 or release qualification. The owner pattern successor is a reference owner correction applied in memory. The production Rust/TS matchers, the M3 sender, the generator, the accepted source bridge and the renderer rebase are still required.

## Custody

**Subject:** `m1-native-wire-owner-subject-04`, outer manifest `fdd640ff…fbb266`.

**Before the review: PASS.**
- **File set:** 80/80 files, with none extra, missing or mismatched. The directories are `inputs`, `prior/*` and `tools` only.
- **Inner manifest:** `subject-files.json` (`a2293654…44ee`) lists 39 inputs, 4 outputs and 36 evidence files; with itself it makes the outer 80.
- **Pins:** all 36 architecture pins match, with no change from candidate 03 (HEAD `c3856824`). The Node pin matches.
- **`prior/` copies:** the review-03 files are byte-equal to my review-03 scratch, and the subject-03 manifest and files are byte-equal to the frozen subject-03. The preserved failures, the vacuous-control disclosure, the length-cache bug and the corrected counts therefore stay intact as evidence.
- **Method:** custody checks used `python3 -B`, and the pins were parsed as text. Nothing was imported from the frozen subject; all execution ran from my copy.

## Reproduction (from only the 39 inputs, in `scratch/copy`)

Runs used `env -i`, the reference Python with `-I -B`, and a private pycache and TMPDIR under the copy's `tmp/`. No `__pycache__` appeared outside `tmp/`.

- **check.py: 478 checks, 0 failed.** Ids, outcomes and details are identical to the frozen output. The closure shows 36 architecture reads, 0 unpinned, 0 bytecode, 27 subject reads with 0 unlisted, and 11 executions, all of the pinned Node.
- **selftest.py: 108/108 caught**, with a clean baseline (14 reviewer-01, 13 reviewer-02 and 8 reviewer-03 mutants adapted).
- **Root:** the validation directory's `stdout.txt` shows only the check at 478/0. No root selftest or isolation result was present, so no root pass is claimed.

## Review-03 dispositions

| Finding | Disposition |
|---|---|
| RF-1 path sites | **Resolved for the `$ref` closure.** There are 10 sites and the 34 rows are corrected. My `x<LF>/../../escape.rs` and `x<LF>/../y.rs` counterexamples are now refused, and `a/..<LF>` is admitted. Residue: relation payload paths (new RF-3) |
| RF-2 final owner | **Resolved for the wrapped owner functions:** each input ends as admitted or routed, never an untyped exception. Residue: how far the evaluator reaches (new RF-2) |
| RF-3 prepared modes | **Resolved for all-fresh sets:** explicit mode refuses, defaulted mode falls back with a disclosure, and 256 rows are admitted. Residue: a stale plus over-limit set in defaulted mode bypasses the limit (new RF-1) |
| RF-4 sender binding | **Resolved for schedule binding:** the refusal is qualified, the non-byte-minimal witness is kept and alternate chunking is refused. Residue: the Cancel law is not enforced (new RF-4) |
| A-1 codes | **Resolved:** bound keys use UNSATISFIABLE (the `PROJECT.SCOPE_LIMIT` family); representability keys use PRECONDITION_FAILED |
| A-2 route mutants | **Resolved:** all `r3_*` controls are caught. Residue: remedy phrase (A-1 below) |
| A-3 `plan2` fate | **Resolved** |
| A-4 TS2 boundary | **Resolved, independently reproduced:** exactly 67,108,864 bytes (64 MiB) with 180,399 entries, and 67,108,865 one over |
| A-5 seal counts | **Resolved:** the review-03 control and my seal-count mutant are both caught |
| A-6 newline set admission | **Resolved** |
| A-7 Cancel meaning | **Resolved:** P3-29 is the only Cancel row, `*PRE_COMPLETE` is WAIT_HELLO_ACK…READY_COMPLETE, and removing the reserve from the totals is caught |
| A-8 pins/trust | **Retained** |
| A-9 callee closures | **Resolved** |

## Required findings

### RF-1: a stale row in a defaulted prepared set bypasses the wire limit

**Evidence** (successor installed). A set of 300 inert rows with `rows[0]` stale, in defaulted mode:
- **The owner falls back but keeps rows.** It returns `fallback-non-prepared` with **299 usable rows**.
- **The successor passes that through.** It applies the limit only when the owner outcome is `admitted`, so it returns 299 usable rows with no disclosure. The same 300 rows, all fresh, fall back correctly with 0 usable rows.
- **The planner accepts it.** A 299-entry prepared plan is not refused, because the planner checks only frame bytes and totals.
- **The carrier refuses it.** The `PreparedOutputManifest` with 299 entries is refused as `ARRAY_BOUND`.

**Fix.**
- Apply the limit to the rows actually selected under every non-rejected owner outcome, and publish the defaulted outcome.
- Make the planner refuse entry counts over `maxPreparedOutputEntries`, `maxSnapshotEntries` and `maxDependencySourceEntries`.
- Add vectors for both.

### RF-2: the evaluator successor reaches beyond its declared parents, and "unchanged" is false

**Evidence.**
- **Which validators are patched.** `install()` patches every canonical copy loaded by the models: `identity_canonical` (including IM.C), `wire_canonical` and `startup_canonical`.
- **What the parents cover.** The declared parents are only `evidence`, `startup`, `handshake`, `occupancy`, `factBatch3` and the three models plus `canonical`.
- **Executed change.** identity v3 `#/$defs/LogicalPath` validated through `NE.IM.C` refuses `a/..<LF>` pinned and admits it with the successor installed. That pattern has no lookahead, so the "unchanged" list is false.
- **Corpus-level changes in non-parent documents:**
  - c2v3: 4 patterns (a trailing LF on identifier, version and digest values);
  - rust2: DigestHex and Sha256Text;
  - identity v2/v3 and workflows common: `LogicalPath/not`;
  - relation registry: `CanonicalPath`.
- **The scope is unpinned.** Mutant `m_patch_native_C_only_not_IM` fails 0 of 478 checks.

**Fix.**
- Publish a closed normative scope as (document, consumer) pairs.
- Either restrict installation to that scope, or add parents and consumer-impact rows for every affected document.
- Correct the "unchanged" list.
- Add controls in both directions.

### RF-3: the relation-payload CanonicalPath is still defective, contradicting "every occurrence"

**Evidence.**
- **The pattern.** `relation-payload-schemas.v2.json#/$defs/CanonicalPath` keeps `(?!.*(^|/)\.\.?(/|$))`.
- **Its users.** It backs `FilePayloadV1.path`, `PackagePayloadV1.manifestPath`, and `VcsChangePayloadV1.path` and `previousPath`.
- **No correction row.** The successor has none for this document.
- **Result.** Under the installed ECMA evaluator it admits `x<LF>/../y.rs`, which the corrected evidence pattern refuses.
- **Why the closure misses it.** These are worker fact payload paths, opaque to the carrier `$ref` closure, but the successor claims every occurrence.

**Fix.**
- Either add a scoped row and parent with payload vectors,
- or narrow the claim and record the correction as an owning duty of the fact-plane unit.

### RF-4: the reference sender does not enforce its Cancel law

**Evidence.**
- **The rule.** `HOST-SEND-SCHEDULE` allows a Cancel "at any point after Hello". P3 `*PRE_COMPLETE` excludes START (`hostMaySendInStart=false`).
- **Before Hello.** `sender_ref.consume` accepts a Cancel as the **first frame** (sequence 0).
- **Wrong echo.** It also accepts a Cancel with a different same-length `executionId`, or with `analysisOrdinal` 7; only the size is compared with the reserve. A wrong `reason` is caught only by the carrier CONST check.
- **Payload bytes.** Mutant `m_sender_no_payload_bytes_check` fails 0 checks, so the payload-byte divergence refusal has no control.

**Fix.**
- Refuse a Cancel before the Hello slot has been consumed.
- Require the exact echo payload.
- Add vectors for cancel-before-hello, wrong execution, wrong ordinal, and a same-coordinates payload-bytes divergence.

## Advisories

- **A-1.** Removing "generated-file logical path" from the `native.provider-input-not-representable` remedy fails 0 checks. Bind every (key, fault) phrase.
- **A-2.** The sender's per-frame request-limit re-check is unreachable for accepted plans (mutant fails 0). Add a control or state that it is defensive.
- **A-3.** State that the phase A prepared path refusal outranks owner non-inert and stale refusals. That order is consistent with the owner validating the schema first: a dylib row plus `x<LF>/../y` yields the path key.
- **A-4. Remaining integration duties:**
  - source-bridge promotion of the in-memory pattern rows;
  - production Rust/TS matchers (ECMA `[\s\S]*` inside a lookahead);
  - an M3 sender implementing `HOST-SEND-SCHEDULE`;
  - generator work and the renderer rebase;
  - the D9 exit-contract successor;
  - the fact-plane relation payload path law.
- **A-5.** Root binding must retain the 36 exact pin bytes and the Node pin. The system libraries are trusted and unpinned, and the open/Popen audit is not confinement.

## Independent assessments accepted

- **Dot-segment law:** the complete-string law with a legitimate `..<LF>` segment is accepted.
- **ECMA differential:** 28 owner patterns and 87 strings, 0 disagreements, reproduced in my run.
- **Route split:** representability keys use PRECONDITION_FAILED and bound keys UNSATISFIABLE; the origin is external input and maps to request-rejected.
- **Canonical send schedule:**
  - Slots carry exact bytes and coordinates; seal slots carry the counts.
  - The Cancel reserve is counted in the totals (149 bytes in my small plan: 6685 bytes without it, 6834 with it).
  - The 40-byte prefix is excluded, as owner law.
  - TS2 has no totals.
  - A refusal means only "does not fit the selected schedule".

## Reviewer mutants (`scratch/mutants.out.json`)

**Caught:**

| Mutant | Checks failed |
|---|---|
| correction token reverted to a no-op | 4 |
| Cancel reserve check removed | 2 |
| seal count check removed | 2 |
| fallback keeps partial rows | 4 |
| phase A in explicit mode only | 2 |
| Cancel reserve counted as zero bytes | 8 |

**Uncaught (0 checks fail):**
- patch only the native `C`, not the other canonical copies
- sender payload-bytes check removed
- sender request-limit re-check removed
- generated-file phrase dropped from the remedy

## Untested limits

- **Not assessed:** no production admission, codec, runtime, sender, generator or platform run.
- **Reproduced but not re-derived** with separate code: the e12 realizations, the 17 remedy pairs, the ECMA differential and the regex inventory; I relied on the author's checks in my copy.
- **Rust regex:** lowering was not executed (the crate is unavailable offline).
- **Relation payload paths:** reachability was not exercised through a real fact-plane admission.
- **Out-of-parent consumer changes:** executed only for identity `LogicalPath` via IM.C; the rest are corpus-level.
- **Root's run:** selftest and isolation were not observed complete.

## Custody after the review

**PASS.**
- **Subject 04:** the outer manifest is still `fdd640ff…fbb266`, and the walk finds 80 files with none extra, missing or mismatched. The directories are unchanged.
- **Pins:** all 36 match, with HEAD `c3856824` showing 12 modified and 11 untracked. The Node pin is unchanged.
- **No stray bytecode:** neither frozen subject 03 nor 04 contains `__pycache__` or `.pyc`, and subject 03 still walks to 64 files.
- **Method:** the checks used `python3 -B` with no imports from any frozen subject (`scratch/custody-after.json`). This review wrote only under `m1-native-wire-owner-review-04`.
