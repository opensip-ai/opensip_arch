# Independent review: report projection author-04 (`m1-report-projection-subject-04`)

**Verdict: CHANGES REQUIRED** for the carrier unit: one blocking finding and two required.

**What this verdict does not cover.**
- The report design remains **blocked** (RP-DO-01, 03–12).
- AUDIT-G10 and RP-OBL-C01 remain **open**.
- The design-obligation register is not a set of completed features, and nothing here accepts the report design.
- No browser, runtime performance, generator or release qualification is claimed.

**Subject identity.**
- Outer manifest SHA-256: `5e43e1a1034d5c8af308a0360cbdc3499b933d6f0062f58ca2712ed9e317b20e`
- Inner `subject-files.json`: `c66c1e34…a39a37`
- 18 files, 79 external pins, 2 listings.

## Verification and strict check

**Before review:** the outer SHA matched, all 18 files matched by hash and length, and the file set was exact. The inner SHA matched, and the 79 pins and 2 listings were present.

**Strict run.** I copied exactly the 18 declared files to `work/closure` before any import, then ran:

`TMPDIR=work/tmp python -I -B -X pycache_prefix=work/pyc-prefix check.py --architecture ARCH --subject-strict --out work/strict-check-result.json`

It exited **0** and reproduced every root count:

| Item | Count |
|---|---|
| Report cases (accepts) | 146 (25) |
| Envelope cases | 22 |
| Metadata cases | 43 |
| Aggregate cases | 14 |
| Delivery goldens | 28 |
| Coverage rows | 323 |
| Pins / listings | 79 / 2 |
| Source compiles | 20 |
| Rehashed opens | 1421 |
| Child processes | 0 |
| `documentMaxBytes` | 27,827,964 |
| Audit ledger bound | 19,435,937 |

**After review:** see `work/after-verification.json` and the end of this file.

## Closure of review-03 findings

| Finding | Status | Independent basis |
|---|---|---|
| RPR3-1 graph count | Partly closed | G1/G2/G3 and my G7 are refused; the public-cap positive (G8) is accepted. **G4–G6 are accepted** (RPR4-1). |
| RPR3-2 bounds | Closed | See "Bounds" below. |
| RPR3-3 D9 / cancellation | Closed under the root correction | See "D9 and cancellation" below. Residual: RPR4-2. |
| RPR3-4 closure | Closed | See "Closure" below. Residual advisories: A1, A2. |
| RPR3-5 coverage | Closed | See "Coverage" below. |
| RPR3-6 obligations | Addressed as a register, not completion | 12 obligations with unit, gate, closure criterion and successor; design declared blocked. Residuals: RPR4-3, A5, A7. |
| A1 / A2 / A3 / A5 / A6 / A8 | Closed | Contradiction join; host-asserted count; P5; J-HISTORY-BASELINE; P8; P1. |
| A4 | Partly closed | The produced-items label is falsified by RPR4-1. |
| A7 / A9 | Open | RP-DO-12; generator not run. |

**Bounds.** My hand-built maximal owner-valid StepTermination is **6,471,125 B** (4096 pins, 6-byte escapes, schema- and typed-valid). That is within the structural bound of 6,476,835 B.

My maximal kind=run audit document is **accepted at 25,524,326 B**:

| Component | Bytes | Limit |
|---|---|---|
| Envelope | 4,193,751 | 4 MiB boundary |
| Ledger | 17,133,229 | 19,435,937 |
| Panels | 4,194,060 | effective budget 4,194,304 |

The remaining budget before the `min` is 6,497,565 B, and one more evidence entry is refused `J-BUDGET-BYTES`. Author B1 (the 10 MB class) is accepted in the strict run.

**D9 and cancellation.** My D9/cancellation implementation, written from workflows §1, matches:
- all 14 aggregate cases;
- all 28 delivery goldens. In each, prior terminations are retained, the aggregate is separate, and results are identical across human, JSON, agent and HTML.

The before-settle `runId` choice (last committed Run) equals the owner reference model (`workflows_model.v1.py:379-381`). K1 and K2 (cancellation inside a delivered report) are refused `J-LEDGER-CANCELLATION`.

**Closure.** My whole-process trace shows:
- 79/79 pins read, 0 unpinned governed reads;
- 0 child-process events, 0 architecture pyc opens;
- `--out` written and never read.

My PoCs, in `work/probes/closure_poc.out`:

| PoC | Result |
|---|---|
| P1: forged header-valid pyc for the real pinned `canonical.py` | Stock loader runs it; enforced loader runs the verified source |
| P2: unpinned copy | `UNPINNED-LOAD` |
| P3: bytecode-only module | Refused |
| P4: undeclared write | `UNDECLARED-WRITE` |
| P5: out read | `DECLARED-OUT-READ` |
| P6: subprocess and `os.system` | `CHILD-PROCESS-REFUSED` |
| P7/P8: simulated pin and listing drift | Refused at use |

**Coverage.** I applied the overlay with my own code:
- Unscoped, base and overlay stop at the same pre-existing condition.
- The only missing key is `crates/reporting/src/assets.rs` (the version row, M1). With that scoped fix, both are **valid**.
- Reverting the `fit` parity fields gives **"Command metadata drift"**; an untracked review issue and a removed row are also refused.
- The historical coverage bytes equal the accepted subject.

## Required findings

### RPR4-1 (blocking): the page law never joins `producedItems` to `totalItems` or rows

**The gap.** `report_model.py:96-123` uses `producedItems` only in `items ≤ produced` and the cap test. Its no-cursor truncated-bound rule checks `total == items`, not `produced == items`.

**The owner laws say otherwise** (`query-projection-contract.v3.md`):
- `:136`: the produced prefix is `producedItems`, and the remaining units are owed (lower-bound);
- `:140`: completeness means complete **and** exact;
- `:146`: `totalItems` is qualified by `countBasis`.

So an exact complete answer produced exactly `totalItems` units, and a lower-bound `totalItems` is the produced prefix.

**Probes** (`work/probes/probe_rpr4.json`):

| Probe | Mutation | Result |
|---|---|---|
| G4 | Slot 0 cut to 1 row; truncated-bound/lower-bound; `producedItems` = 100000 cap; `totalItems` forged to 1; no cursor | **accept** |
| G5 | Visited cap reached; produced 50, total 1, 1 row, no cursor | **accept** |
| G6 | complete/exact/total 1, 1 row, `producedItems` 1000 | **accept**, labelled `complete-page-set` |
| G7 (control) | Total 107 but 1 row | `J-GRAPH-COUNT` |
| G8 (positive) | Capped full page with cursor | accept |

**Correction:**
- Require `totalItems == producedItems` for every graph page.
- Hence no-cursor truncated-bound ⇒ `items == producedItems`, and complete ⇒ `producedItems == items`.
- Add G4–G6 as refusal cases.

### RPR4-2 (required): the D9 aggregate counts skipped required steps, unlike the owner model

**The divergence.**
- `invocation_aggregate` aggregates every recorded required termination, including skipped steps.
- The pinned owner reference model filters `outcome != 'skipped'` (`workflows_model.v1.py:385-388`). It records skipped steps as `request-rejected REQUEST.PRECONDITION_FAILED` (`:306`), and an all-skipped invocation aggregates to success.

**Probe** (`skipped_probe.json`): with [analysis success, query skipped request-rejected], the subject gives `request-rejected` while the owner rule gives `success`. The indeterminate variant diverges the same way.

No case or golden covers skipped steps, and the root direction requires the owned aggregate unchanged.

**Correction:** exclude skipped steps as the owner model does, and add aggregate, report and golden cases.

### RPR4-3 (required): RP-OBL-C01 is confirmed but not tracked where it can block integration

**Confirmed independently** (`d9_independent.json`):
- An interrupted `kind=failure` envelope with `errors` empty or omitted is refused by **both envelope4 (accepted) and envelope5**.
- The same envelope becomes valid in both only if it carries an unrelated DomainDetail such as `evidence.purged`.
- No DomainDetailCode mentions interruption, cancellation or signals.

**Pre-existing.** Envelope major 3 already had `errors` minItems 1, and envelope4/5 allow empty `errors` only for `REQUEST.UNKNOWN_OPTION`. Author-04 neither introduced the gap nor invented a code.

**Material impact:**
- Every command interrupted before a committed Run or a query result has no conformant output in any of the four renderers.
- The `cancel-before-settle-no-commit` aggregate case has no delivery golden.
- An emitter can only conform by inventing false detail.

**Not tracked.** RP-OBL-C01 appears only in `contract.md` and `fixtures.json#/obligations`. It is absent from the design register, the coverage `reviewIssueAdditions`, and every command, renderer or workflowGolden row, so M1 integration could pass coverage without it.

**Correction:**
- Record it as an open review issue on the affected rows, requiring an envelope/workflow owner correction before M1 final integration.
- Add a negative golden forbidding invented interruption detail.
- Invent no code here.

## Advisories

- **A1: closure alias bypass.** `governed()` compares strings. PoC P9 read the unpinned `docs/implementation/README.md` via a case-variant path (`…/OPENSIP_ARCH/…`) under the hook, while the exact path is refused. The checker never uses aliases, but enforcement should compare realpath plus `(st_dev, st_ino)`.
- **A2: pre-hook write and counter.** `tempfile.gettempdir()` writes a probe file into `TMPDIR` before the hook is installed. Also, `closure.declaredOutWrites` reports 0 even though `--out` was written.
- **A3: owner codec.** The maximal termination is refused by the owner canonical codec (4 MiB). If invocation:3 records are admitted through that codec, the structural ledger bound is far above what is reachable. The owner should state the record bound, and M01 should measure the 27.8 MB document.
- **A4: disclosure label.** The static disclosure `graphUnresolvedSubjects` lacks a host-assertion marker, unlike the history count. Browser admission (B01) checks shape, codec and internal joins only, and must not present verified labels as semantic proof of host retention.
- **A5: R05 row.** The R05 coverage row treats conditional RP-DO-02 as keeping the row open.
- **A6: workaround value.** M1 is justified by the version row, but M0 also validates; the rationale is recorded.
- **A7: register standing.** Register entries are proposals to other owners. RP-DO-11 implies invocation and ledger successors after M1.
- **A8 / A9:** RP-DO-12 is still open; generator integration was not run.

## Untested limits

- No browser, renderer, generator, performance or release work was done; all sizes are constructions.
- The probes use the subject's mock graph owner, not a product engine or ledger store.
- The owner model was compared by its rules, not by executing its scripts.
- Only case-variance aliases were tested; no symlink or hard-link aliases, since writes were restricted to this directory.
- Fork refusal was not attempted.
- Concurrent-writer TOCTOU was not exercised; it is an acknowledged trusted-host limit.
- The owner absences behind RP-DO were not re-searched.
- Author responses and session logs were not read.

## After-verification

I recomputed the following after writing this review. The results are in `work/after-verification.json`:
- the outer SHA, 18/18 files and exact set, and the inner SHA;
- all 79 pins and 2 listings against current bytes;
- that the closure copy is unchanged and neither the subject nor the copy has a `__pycache__`.

All outputs are under `m1-report-projection-review-04/`. No commit or push was made.
