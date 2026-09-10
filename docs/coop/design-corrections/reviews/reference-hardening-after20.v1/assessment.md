# Bounded reference-hardening source proposal (after v20)

**Standing.** This is a bounded coauthor **source proposal only**. Nothing here is integrated,
committed, pushed or published. The live repository and the frozen v20 subject/history were treated
as read-only throughout. This document expresses **no** independent20 verdict, **no** acceptance,
**no** blind result, **no** readiness grade and **no** implementation authority. The active
independent20 reviewer is unaware of this proposal, reviews its unchanged frozen subject, and its
eventual findings must still be assessed separately and on their own terms.

## 0. Custody and verification

| Item | Value |
| --- | --- |
| Parent source | `/tmp/opensip-design-corrections/candidate-subject.v20` |
| Manifest | `.../reviews/candidate-subject.v20.json` |
| Manifest SHA256 declared | `878e5bebd5a7b144ef7900e774af0e13eb1b3a01d32e7f289b6f483de6832f3c` |
| Manifest SHA256 recomputed | `878e5bebd5a7b144ef7900e774af0e13eb1b3a01d32e7f289b6f483de6832f3c` — **match** |
| Manifest contents | `fileCount` 11932, `reviewPending` true, `applicationPending` true, standing "FROZEN CORRECTED CANDIDATE FOR FRESH INDEPENDENT REVIEW; NO ACCEPTANCE" |
| Root evidence | `.../codex-post-reset.v1/independent20-provisional.v1` |
| Root evidence verification | all **12** files re-hashed against `custody.json`, **0 mismatches** |

Every source file read for this proposal was hashed at read time; the three changed files carry
before/after digests in `proposed-changes.json`. The foundation source ledger
`source-pins.v1.json` (1100 entries) verified with **0 mismatches** against a clean copy of the
parent before any edit.

I read the root's provisional observations critically and **independently re-derived** both of the
two claims I depend on rather than accepting them (§1.1, §2.2). Both reproduced.

## 1. Issue 1 — the wrapper's fixed 120s inner timeout

### 1.1 What actually happened, reproduced here

The root recorded `check-identity.py` exceeding the wrapper's `timeout=120` at **121.34s**, exit 1,
and — the part that matters — `reportChanged: false`. I reproduced this independently on this host
in a clean copy of the frozen parent:

* Direct `check-identity.py`: **exit 0, 1592 passed / 0 failed, 122.30s wall.**
  The suite is not failing; it is finishing, just past the bound.
* Unmodified canonical wrapper on the same copy: **exit 1 at 120.68s**, `subprocess.TimeoutExpired`
  traceback on stderr, and `validation-report.json` **unchanged** at
  `599c84b7af056ac18cc4a231fd529d9338d7a29414eb8e41b70a38e6e6178b6c` — a report that still reads
  `"passed": true` with all five children at `exitCode 0`.

So this is exactly what the brief says it is: **actual marginal timing, not a semantic assertion
failure.** The identity suite passes; the launcher's budget does not fit it.

### 1.2 Root cause, which is not the number

The number is only the trigger. The defect is structural and is visible in the frozen source:

```python
run=subprocess.run([...],capture_output=True,text=True,timeout=120)   # line 20
...
Path(a.report).write_text(...);print(...);sys.exit(...)                # line 23
```

`TimeoutExpired` propagates out of the loop and **past line 23**. The launcher therefore has no
failure path at all: on timeout it never writes a report, so the *previous* run's report survives as
the file on disk, and the only signal that this run failed is the process exit code and a traceback.
Any consumer that reads the report rather than the exit code — and `correction-crosswalk.proposed.json`
and `validation-summary.v1.json` both cite the report as *evidence* — sees a stale success.

Raising the timeout alone would be a band-aid: it moves the cliff without giving the launcher a
failure path, and the next slow host falls off it again with the same stale PASS. I therefore
propose **both** parts, and I regard the report behaviour as the substantive one.

### 1.3 Proposed correction

`docs/coop/design-corrections/foundation/run-reference-checks.py`:

1. **`CHILD_TIMEOUT_SECONDS=600`**, a module constant, per child. Assessment of 600s as the brief
   asked: the slowest child measured **122.3s** here and **121.3s** at root, so 600s is ~5x observed
   cost — wide enough that ordinary host variation no longer decides the outcome, narrow enough that
   a genuine hang is still refused. Suite worst case is bounded at 5 x 600s.
   I deliberately did **not** make it a flag or an environment variable: a caller must not be able to
   widen or narrow the bound that decides whether a run counts.
2. **An explicit failed-report path.** `subprocess.TimeoutExpired` is caught per child. The report is
   still written, with:
   * the **same shape and the same five entries** — the loop continues past a timeout, so counts are
     preserved and the remaining children still report;
   * `timedOut: true` on the entry that ran out of budget (this key is present on **every** entry, so
     the addition is uniform rather than conditional);
   * `exitCode: null`, because none was observed;
   * `reportSha256: null`, because a run that did not finish must not claim a child report it did not
     write (see §1.5 — this is the same stale-artifact defect one level down);
   * the child's partial output plus an explicit `TIMEOUT: no result after 600s` marker on stderr;
   * top-level `passed: false`, `timedOut: [...]`, `childTimeoutSeconds: 600`.
3. **A decode fix that is not cosmetic.** `TimeoutExpired.stdout`/`.stderr` are **bytes even under
   `text=True`** — I verified this empirically rather than assuming it. Writing them raw would raise
   `TypeError` from `json.dumps` and skip the report write *again*, reproducing the original defect
   inside its own fix.

What the change does **not** do, per the brief: it does not mask a timeout as a pass, does not
silently disable or weaken any pin check, and introduces no product lifecycle behaviour
(`productQualification: false` is untouched). The pin sweep still runs to completion **before** any
child starts — pin-before-execution is unchanged, and the `if failures:` branch is byte-identical.

### 1.4 Was a smaller correction sufficient?

I considered three narrower options and rejected each:

* **Raise the timeout only.** Rejected: leaves the launcher with no failure path, so the stale-PASS
  hazard survives untouched and merely becomes rarer — the band-aid.
* **Catch the timeout and abort the loop.** Rejected: produces a truncated `checks` array, which
  violates the "preserve normal report shape/counts" requirement and makes timed-out runs harder to
  diff against passing ones.
* **Add a `reportRewritten` field comparing the child report before/after.** Rejected after testing:
  the child reports are **deterministic** — I confirmed `identity-report.json` is byte-identical
  across runs — so `after == before` on a perfectly successful run, and the field would read `false`
  for a child that did write. It would have been a misleading name for a true fact. `reportSha256:
  null` on timeout says the intended thing exactly and needs no new field.

### 1.5 Evidence, with synthetic injection kept separate from real execution

These are two clearly different things and I am labelling them as such.

**(a) Actual complete suite execution** — corrected wrapper, real 600s budget, disposable corrected
copy, nothing forced:

```
exit 0   real 126.89s  (repeated after mutation revert: exit 0, 123.30s)
{"sourcePinsValid": true, "sourceFileCount": 1100, "checksExecuted": true,
 "passed": true, "timedOut": [], "childTimeoutSeconds": 600, "productQualification": false}
  check-foundation.py            exit 0  timedOut False  231 passed
  check-identity.py              exit 0  timedOut False  1597 passed / 0 failed
  check-product-quality.py       exit 0  timedOut False  24 passed
  check-product-configuration.py exit 0  timedOut False  28 passed
  check-array-orders.py          exit 0  timedOut False  65 passed
```

No child timed out and no timeout path was exercised. **No stale PASS was claimed:** `passed: true`
here is a report this run actually wrote, with `timedOut: []`.

**(b) SYNTHETIC timeout injection** — a *separate, disposable, clearly-named* tree
(`work/SYNTHETIC-timeout-injection`, since deleted; the injected file is retained at
`custody/SYNTHETIC-run-reference-checks.5s.py`) with the budget forced to **5s** purely to exercise
the failure path. This is **not** a suite result and is not part of the proposal:

```
exit 1   real 6.39s
{"sourcePinsValid": true, "sourceFileCount": 1100, "checksExecuted": true,
 "passed": false, "timedOut": ["check-identity.py"], "childTimeoutSeconds": 5, ...}
  check-identity.py  exit None  timedOut True  reportSha256 null  stderr: "TIMEOUT: no result after 5s"
  (the other four still ran and still reported; 5 entries preserved)
report sha BEFORE 7eb3beadafa50aff...  (a PASS report, deliberately seeded)
report sha AFTER  1ccbd60005715d28...  (rewritten, passed=false)
```

The seeded PASS report **was replaced**, which is precisely what the frozen wrapper fails to do. And
`identity-report.json` **existed on disk** (172008 bytes, left by an earlier run) at the moment the
timed-out entry reported `reportSha256: null` — so that null is the wrapper actively declining to
attribute a stale child artifact to a run that did not finish, not an artifact of the file being
absent.

**Root/independent history is unchanged.** I read the provisional evidence and re-verified its
hashes; I wrote nothing into it and edited nothing under `reviews/`.

## 2. Issue 2 — the at-most-one guard's ordering is not held by any control

### 2.1 The gap, stated precisely

`verify_scope_parameter_binding` refuses at-most-one ambiguity **before** the payload match, which is
correct. But both existing ordering controls supply **one of the two candidates**:

* `the-scope-binding-verifier-refuses-an-ambiguous-selection-before-any-digest-match` → `SCOPE_DOCUMENT` (row A)
* `the-ambiguity-refusal-is-not-laundered-by-supplying-either-candidate` → `SCOPE_DOCUMENT` and `SCOPE_DOCUMENT_B`

For a candidate, `any(row.payloadDigest == digest)` **succeeds**, so the mismatch branch does not
raise and the ambiguity is reached and refused **under either ordering**. Both controls hold whichever
position the guard occupies, and therefore neither of them holds the position.

### 2.2 Independently re-derived, not taken on report

I did not accept the root's counterexample on its word. In the disposable corrected copy I applied the
reordering mutation (guard moved below the payload match) against the **frozen, unmodified**
`check-identity.py`:

```
ORIGINAL check-identity.py + MUTATED workflows_model.v1.py  ->  exit 0, 1592 passed / 0 failed
```

Confirmed: the shipped suite does not detect this reordering at all. The three direct-helper scenarios
the root reported also reproduce, and are now the content of the new controls.

### 2.3 Proposed correction

`docs/coop/design-corrections/foundation/check-identity.py`: **five** new named controls, inserted
immediately after the two existing ordering controls, which are **preserved unchanged**. They use the
real existing fixture documents and rows (`SCOPE_DOCUMENT`, `SCOPE_DOCUMENT_B`, `_SCOPE_ROW_A`,
`_SCOPE_ROW_B`, `parameter_row`, `POLICY_DOCUMENT_BYTES`, `_spec`, `_refusal`) plus one distinct third
scope document `SCOPE_DOCUMENT_C`. Every one asserts an **actual** error code / detail pair on a real
`Refusal` object or a real returned digest. There are no bare PASS prints.

| Control | What it decides |
| --- | --- |
| `the-third-scope-document-is-schema-admitted-and-is-neither-of-the-two-candidates` | C is a *real* ScopeDocumentV1 — admitted through the owning unit's own pinned validator (`W.validate_import_record` on `policy-document.schema.json#/$defs/ScopeDocumentV1`), citing the same registered schema digest as A and B, with all three payload digests distinct. Without this the discriminating check could pass for the wrong reason. |
| `an-ambiguous-spec-refuses-as-ambiguous-even-for-a-document-that-is-neither-candidate` | **The discriminator.** Ambiguous spec `[A,B]` + document C must be `('CONFIG.INVALID','CONFIG.INVALID')`. Under the reordering it becomes `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`. |
| `the-same-non-candidate-document-under-one-selected-row-is-an-ordinary-digest-mismatch` | Distinguishes precedence from an ordinary mismatch: the *same* document C under a single row `[A]` is `('REQUEST.PRECONDITION_FAILED','BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH')`. So the check above pins ordering, not some property of C. |
| `the-three-answers-for-one-non-candidate-document-stay-distinct-by-row-multiplicity` | One document, three row multiplicities (none / one / more than one), three distinct answers — missing, mismatch, ambiguity — asserted as an ordered list. |
| `the-third-document-verifies-when-it-is-itself-the-one-selected-parameter` | Valid selection: as the single selected row, C **verifies** and returns its payload digest. Refusal is not all that can happen to it. |

### 2.4 Mutation demonstration

Mutation: the four-line `if len(rows) > 1:` guard block moved verbatim to below the payload-match
block. **481 characters differ, length delta 0** (a pure transposition — no bytes were rewritten).

```
                                        exit  passed  failed
unmutated corrected source               0     1597    0
MUTATED (guard after payload match)      1     1595    2
        FAIL: an-ambiguous-spec-refuses-as-ambiguous-even-for-a-document-that-is-neither-candidate
        FAIL: the-three-answers-for-one-non-candidate-document-stay-distinct-by-row-multiplicity
frozen check-identity.py + same mutation 0     1592    0     <- the gap, re-derived
```

The other three new controls and both pre-existing ordering controls stay green under the mutation,
which is the correct and expected outcome: they are not ordering-sensitive, and only the two that
should discriminate do.

Custody: `mutation/workflows_model.v1.py.ORIGINAL` (sha `f0bf5a6c...`) and
`mutation/workflows_model.v1.py.MUTATED` (sha `832f41dc...`) are retained verbatim, together with the
mutated run's stdout, stderr and exit code. The mutation was **reverted** and the restored file
re-hashed to `f0bf5a6c5c6aa303f1676a30e5d4d7f7416f9f8a5b64824aacf4f40cf268bdf4`, after which the full
canonical suite was re-run and passed again (exit 0).

### 2.5 The false comment

`workflows_model.v1.py` currently says:

> Order is the point: checking the digest first would let a caller who happens to hold one of two
> candidate documents obtain a `verified` digest...

This is **false**, and my mutation runs demonstrate why: with the guard moved after the match, a
caller holding candidate A still gets `CONFIG.INVALID` — the match falls through without returning
and the ambiguity is still reached. Nobody obtains a `verified` digest.

The corrected comment (**comment only**) states the actual consequence: reordering still refuses both
candidates, but changes the answer given to a caller holding **neither** candidate, reporting a defect
that belongs to the **spec alone** as an ordinary statement about the supplied document. It names the
two new controls that hold the order, and notes that the two-candidate controls pass under either
position. The executable ordering and the public routes are untouched.

**Executable behaviour unchanged — evidenced, not asserted.** I compiled both versions and compared
the code objects (`co_code`, consts recursively, names, varnames): **identical**. I also checked the
two brittle count-based identity controls that read this file's text:
`count("'CONFIG.INVALID', 'CONFIG.INVALID'")` stays **1** and `count("CONFIG.INVALID")` stays **38**.

**One thing I deliberately did not change.** The docstring above still says more-than-one is refused
"before any payload comparison, because ... a `verified` digest would prove selection of one document
while another was equally selected." That sentence is about why the guard **exists** — remove the
guard entirely and a candidate holder *would* get a verified digest, which is true — not about where
it sits. It is accurate and outside the brief's "correct only that explanatory comment". I flag it as
marginally easy to misread in the same direction as the comment I did correct, and leave the call to
the integrator.

## 3. Disagreements and limitations

1. **The brief's framing of issue 2's comment is right and I confirm it**; I found no disagreement on
   either issue's substance.
2. **Scope tension I must flag: all three changed files are pinned entries** in
   `foundation/source-pins.v1.json`, which is **not** in the allowed changed-source paths. Integrating
   the proposal without re-pinning makes the launcher refuse with `sourcePinsValid: false` and execute
   nothing. This is a mechanical derivation rather than a design decision, so I have supplied the exact
   replacement digests in `proposed-changes.json`; I re-pinned **only** in the disposable validation
   copy, where I also rewrote the ledger's `standing` string to say so in-band. **I changed no live or
   frozen pin.**
3. **`validation-summary.v1.json` becomes numerically stale** (1940→1945, identity 1592→1597,
   `passingCalls` 1592→1597, `distinctIds` 1580→1585, `duplicateExtraInstances` unchanged at 12 —
   all measured). It is unpinned, so nothing refuses; it would simply be wrong. Outside allowed paths,
   so **not done here**.
4. **`reviews/codex-post-reset.v1/identity-check-counts.v20.json`** carries the same 1592/1580/12
   account and is cited by `validation-summary.v1.json` with a pinned sha256. It is **frozen review
   history**; I did not touch it and I do not think it should be edited. The integrator must decide
   between a successor account file and a recorded delta. **Unresolved and left to the integrator** —
   it is the one item in this proposal I could not close within my bounds.
5. **Host-specific timing.** 122.3s here and 121.3s at root are two data points on similar hardware.
   600s is justified as ~5x observed cost, not as a measured worst case across all hosts.
6. **No product qualification, no readiness claim.** The corrected suite passing 1945 checks is
   evidence that my three edits do not break the reference suite. It is not evidence about the subject
   under independent review, and `productQualification` remains `false` everywhere.
7. **Coverage scope.** I ran the canonical **foundation** suite only, as the brief directed. The
   security, native, workflows, workflow-surface and integration commands were **not** re-run; my
   `workflows_model.v1.py` change is comment-only with identical code objects, which is why I judged
   that acceptable, but it is a stated limitation rather than a demonstrated one.
8. **Failed development attempts:** none were discarded silently. The three narrower designs I
   considered and rejected for issue 1 are recorded in §1.4 with the reason each was rejected; the
   `reportRewritten` option was rejected on the basis of an actual measurement (deterministic child
   reports), not on taste.

## 4. Tests actually run

| # | Run | Result |
| --- | --- | --- |
| 1 | Manifest `candidate-subject.v20.json` re-hash | match |
| 2 | Root evidence custody, 12 files re-hashed | 12/12, 0 mismatches |
| 3 | `source-pins.v1.json` over clean parent copy, 1100 entries | 0 mismatches |
| 4 | Frozen `check-identity.py`, direct | exit 0, **1592/0**, 122.30s |
| 5 | **Frozen wrapper, unmodified** — timeout reproduction | **exit 1**, 120.68s, report **unchanged** at `599c84b7...` still reading `passed: true` |
| 6 | `TimeoutExpired.stdout/.stderr` type probe | **bytes** under `text=True` |
| 7 | Corrected wrapper, full canonical foundation suite | **exit 0**, 126.89s, **1945** = 231+**1597**+24+28+65, `timedOut: []` |
| 8 | SYNTHETIC 5s injection (separate tree, not a suite result) | **exit 1**, `passed: false`, `timedOut: ["check-identity.py"]`, 5 entries, seeded PASS report **replaced** |
| 9 | Frozen `check-identity.py` + reordering mutation | **exit 0, 1592/0** — gap re-derived |
| 10 | Corrected `check-identity.py` + same mutation | **exit 1, 1595/2**, the two named controls fail |
| 11 | Mutation revert + re-hash | restored to `f0bf5a6c...` |
| 12 | Corrected wrapper, full suite after revert | **exit 0**, 123.30s |
| 13 | Compiled-code-object comparison, `workflows_model.v1.py` | **identical** |
| 14 | Literal-count guards in `workflows_model.v1.py` | 1 and 38, both unchanged |

Identity check count: **1592 → 1597** (+5, each new id present exactly once). Foundation total:
**1940 → 1945**. No pre-existing check was modified, removed or renamed, and none regressed.

## 5. Conclusion — bounded source assent

Within the bounds of this session I give my **bounded source assent** to the three proposed changes as
written and hashed in `proposed-changes.json`. They address the two issues at their root — a launcher
with no failure path, and an ordering that no control held — rather than at their symptoms; they
preserve pin-before-execution, report shape and counts, the existing controls, the executable ordering
and the public routes; and each substantive claim above is backed by a run recorded in §4 rather than
by inspection alone.

**One required issue remains unresolved,** and it is not mine to close: the consequential updates in
§3.2–§3.4 lie outside my allowed changed-source paths. The `source-pins.v1.json` re-pin (§3.2) is
mandatory and mechanical — **without it the launcher will refuse to execute** — and the frozen
`identity-check-counts.v20.json` account (§3.4) needs an integrator decision that must not be taken by
editing frozen history.

This is an assent to *source*, and to nothing else. It is not an independent20 verdict, not an
acceptance, not a blind result, not a readiness grade and not implementation authority. The active
independent20 review of the unchanged frozen subject stands entirely apart from this document, and its
findings must still be assessed separately.
