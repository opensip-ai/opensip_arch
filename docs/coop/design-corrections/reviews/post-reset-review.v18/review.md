# Independent review — OpenSIP design corrections, candidate v18

**Subject manifest SHA256:** `cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44`
**Verdict: ACCEPT** — of the frozen v18 *source bytes only*.
**New MUST issues: none. New SHOULD issues: none. New advisories: three.**

This is not a blind review, not an application, not a readiness reconciliation and not product
qualification. A fresh blind consumer review and a complete independent application remain
required after this source ACCEPT. I claim no blind agreement, no application agreement and no
readiness agreement.

I authored none of the subject. I am not the v17 independent reviewer, not the blind reviewer,
and not the v18 source coauthor. I treated source, reviews and history as read-only; every byte I
wrote is under `/tmp/opensip-design-corrections/post-reset-review.v18`. No live repository byte
and no frozen snapshot byte was written at any point in this session.

## 1. Custody

The frozen manifest hashes to the declared value at 1,907,291 bytes. I verified **all 7,864
declared files** in the snapshot: zero hash mismatches, zero length mismatches, zero missing
files, zero undeclared extras, and the summed actual bytes equal the declared 544,831,302
exactly. I repeated the identical verification after all probes and controls had run; the result
is unchanged and the live manifest re-hashes to the same digest.

I verified the transitive pins directly rather than accepting a count. Across the four pin
documents there are **1,308 pin entries** (foundation 1,099, native 71, security 73, workflows
65). All 1,308 resolve to a file present in the snapshot whose actual bytes hash to the pinned
digest — zero mismatched, zero unresolved. Recovering the v17 pin documents from the v17 tarball
and diffing entry-by-entry, the only pinned digests that moved are `check_workflows.v1.py` (in
all four pin files) and `correction-crosswalk.proposed.json` (in security and workflows). I
performed no repinning, and none was needed to make anything pass.

## 2. The six canonical commands

I reproduced all six reference commands in a **disposable FULL exact copy** of all 7,864 files —
not a partial extract. All six matched their declared source SHA256, all six exited 0 as
declared, every regenerated report was **byte-identical to the frozen report**, and every
captured stdout was byte-identical to the corresponding frozen log. I then re-inventoried the
copy against the frozen snapshot: **0 added, 0 removed, 0 changed**.

One scoping point matters here. The source coauthor invoked `check_workflows.v1.py` directly and
states plainly that the source-pin gate was therefore *not* exercised, and that its 1,219-file
working copies intentionally omit review files. I confirmed those numbers independently: v17
carries 1,216 non-review files and 6,455 review files, so a copy of the non-review tree plus the
three review files the pin manifests name is 1,219, omitting 6,452. Because I ran the full six
through the `run-reference-checks.py` wrappers over a complete copy, the pin gate **was**
exercised in my reproduction. That gap in the coauthor's evidence is closed.

## 3. The executable delta, verified independently

The declared delta is ten membership guards in `workflows/check_workflows.v1.py`. I did not take
that on trust from either the root exact-AST claim or the coauthor's compare-inventory.

Comparing the two manifests, exactly **11 paths changed** and 193 were added, with none removed.
Of the 11: one executable checker, four source-pin files, three generated reports, one narrative
README, one review-routing record, and the correction crosswalk. Line counts are identical at
1,423 before and after; the unified diff is ten hunks, each a single line.

My proof is an AST rollback. I rewrote every boolean conjunction of the shape `(K in D and RHS)`
back to `RHS`, restricted to sites where `RHS` actually reads key `K` — precisely the "guard the
key you are about to compare" shape — and compared full AST dumps. The result: **10 guard sites
in v18, 0 in v17, and the rolled-back v18 AST is exactly equal to the v17 AST.** Because each
guard is added as the *first* conjunct of an AND whose second conjunct is the unchanged v17
expression, the new condition implies the old one. The delta is therefore not merely small, it is
**monotonically stricter**: a guard can turn a passing check into a failing one, never the
reverse.

A first, looser version of that transformer over-matched an unrelated pre-existing conjunct
(`'sarif' in c['formats'] and ...` at line 1340), reported 11 sites and failed the equality. That
attempt is preserved rather than discarded; the restricted transformer is the proof.

I inspected all ten contexts individually, and they are the ones named: invocation (171), import
with its optional `errorCode` conjunct (384), the reversed source-mapping comparison (407),
repair preview (1112), `recoverRefusal` (1158), repair apply (1171), repair verify (1203),
test execution (1226), render (1320) and review (1360). Two keys are guarded: `refusal` at nine
sites, `recoverRefusal` at one.

**No equivalent was missed inside the checker.** I censused all 23 `except` handlers and
classified every equality comparison between an expectation and the caught exception:
10 unguarded defaulting comparisons in v17, **0 in v18**. Thirteen handlers carry no
expected-refusal comparison at all — they compare against string literals, or return the detail —
and one comparison (`case['expect']['errorCode']`) is subscript-indexed, which raises loudly
rather than passing silently.

## 4. My own discriminating controls

Root's 100 synthetic handler-body executions and the coauthor's single corpus injection are
supporting evidence. They are not my oracle. I authored my own.

**Ten-context control.** For each context I injected a detail-`None` refusal into the model entry
point called inside that try, then ran the v17 and v18 checkers over the *identical* tree. Rows
that pass under v17 and fail under v18 are actual false passes the guard removes. Result:
**a real false pass demonstrated in 10 of 10 contexts, 69 false-pass rows removed in total, and
zero regressions** — no check anywhere failed under v17 and passed under v18. Render needed a
call-index sweep because `M.render` is also called outside any try; calls #1–#3 escaped uncaught
and are preserved as failed attempts, and call #4 lands inside the guarded loop.

**Null-semantics truth table.** The stronger control uses no model patching at all. The model
itself raises a detail-free refusal at `workflows_model.v1.py:1539` in `repair_preview`
("target fingerprint not in the evidence Run"), reachable from a case that empties
`run['findings']` via `runOverride`. Varying only the corpus:

| variant | v17 checker | v18 checker | meaning |
|---|---|---|---|
| A — no `refusal` key | **PASS, suite exit 0** | FAIL, exit 1 | actual false pass, removed |
| B — `"refusal": null` | PASS | PASS | deliberate null remains legal |
| C — wrong named refusal | FAIL | FAIL | named negative preserved |
| D — untouched corpus | PASS | PASS | no regression |

All four match the intended semantics. Variant A is the substantive one: under the old checker a
completely refused repair preview left the entire reference suite green at exit 0.

**Reachability, honestly scoped.** My first measurement of the model was wrong and I corrected
it: counting a positional `None` as "has a detail" gave 0 detail-free raise sites and would have
framed the defect as merely theoretical. Re-measured, **10 of the 83 `raise Refusal` sites pass
`detail=None`**. The defect was live-reachable in the current model. It was not currently
*triggered*, because the frozen corpus does not reach one of those sites with a
success-expecting case — which is exactly why the unchanged suite passes identically under both
checkers.

Note also what the guard *adds*. Under the old code `"refusal": null` and an absent key were
indistinguishable, so an explicit null was not expressible. Under the new code it is meaningful.
The corpus today has 21 named refusal expectations and zero explicit nulls, so this is a
preserved capability rather than an exercised one.

## 5. Claims I checked and found wanting

Three findings of my own, all non-blocking, all raised as advisories rather than required
changes.

**V18-ADV-1.** The coauthor justifies the guard as "the checker's own law" on the grounds that
each of the ten handlers is already paired with a post-try `if 'refusal' in exp:` check. I
checked all ten: **that pairing exists at only 4 of 10 sites** (171, 384, 1112, 1226). At the
other six — 407, 1158, 1171, 1203, 1320, 1360 — there is no such check; line 1203, for instance,
is followed by a `must_valid` on the verify result schema. The rationale is overbroad. The
correction is still right on its own merits, and at those six sites the guard is if anything more
valuable, because nothing else there detected an unexpected detail-free refusal. My controls
demonstrate the effect at all ten sites, including the six unpaired ones.

**V18-ADV-2.** One same-class conflation survives, inside a corrected handler. Line 384 retains
`(case['expect'].get('errorCode') is None or case['expect']['errorCode'] == x.error_code)`, in
which a deliberate `errorCode: null` is indistinguishable from an absent one. I scoped it before
raising it: `Refusal.__init__` takes `error_code` as a required positional and all 83 raise sites
supply a non-null code, so "expect no error code" is not a satisfiable expectation; and none of
the six corpus cases carrying `errorCode` declares null. The expression is dead rather than a
live vector, and unlike the ten it cannot pass on its own, since the guarded refusal-detail
conjunct must still match. Fixing it is outside the bounded v18 scope and would change no current
verdict.

**V18-ADV-3.** The coauthor's first completeness heuristic contains a dead term: `is_get` requires
`len(args) == 1`, so the later `defaulted = any(len(n.args) > 1 ...)` can never be true, and
two-argument `.get(key, default)` calls are invisible to that scan entirely rather than merely
un-excluded. The scan cannot support a completeness claim over them. The conclusion is
nonetheless sound — I counted 39 two-argument `.get` calls in the checker and **zero** of them
participate in an equality comparison inside an except handler — and my own census, which does
not use that heuristic, independently reaches the same set of exactly ten.

I also record that the coauthor's later compare-inventory is not a full AST proof and the
first heuristic is not sound; my rollback equality is what establishes that the delta is exactly
ten new guards.

## 6. Prior findings, and a disagreement kept in the record

The 26 findings resolved at v17 (7 CB6 rows and 19 additional source rows) are preserved by
exact prior reference into `post-reset-review.v17-clarification.v1/review.json`
(`7acde294…`), together with my own byte-identity and monotonicity proof. I did not re-derive
each original finding, and I did not infer preservation from the v17 ACCEPT headline or from
counts.

On **CX-V17-REFUSAL-EXPECTATION**: the independent v17 reviewer graded this advisory
(nonblocking), as V17-ADV-3. Root graded it SHOULD, explicitly withheld promotion for the checker
false pass, and the source coauthor independently agreed a SHOULD correction was warranted. That
disagreement stands in the record. The v17 reviewer did not regrade its own advisory and nothing
here should be read as claiming it did. My own grade, formed independently, agrees with SHOULD —
a harness that returns exit 0 green while a repair preview was refused is a real assurance
weakness — and it is my judgement, not a restatement of anyone else's.

**V17-ADV-1** is accounted at original severity. I read the consumers rather than the prose: both
call sites index `perKindApplicability[req['relation']]` by a validated relation key
(`workflows_model.v1.py:1012`, `:1148`), and `requirement_plane` resolves the plane from
`EVIDENCE_RELATIONS` registry membership, never from a naming convention, with `admit_atom`
refusing an unregistered relation first. The embedded `rule` key is unreachable as a relation and
is inert metadata. No silent relocation occurred — the schema still carries `rule` and the file is
byte-identical to v17.

**V17-ADV-2** is resolved. I swept all 107 declared `{path, sha256}` joins in the v18 governance
records against actual frozen bytes: 102 resolve exactly, one is a subject-manifest digest, and
the four that do not match file bytes are each explicitly labelled historical as-of pins carrying
a separate `currentSource` that *does* resolve. Item 44 (V14-ADV-2) labels its `ef0c244e`
correction as historical as-of-v16 and binds `currentSource` `53380a2455490e07` for
`foundation/relation-payload-schemas.v2.json`, which I confirmed equals the actual v18 bytes. The
frozen v17 advisory account is not in the changed-path set, so the original is untouched. I keep
review-file digests, subject-manifest digests and historical as-of references distinct throughout.

**V17-ADV-3** carries its original advisory severity, and the root-required correction is
implemented at all ten sites. **V18-OBS-1** I reproduced and agree is non-blocking: when the guard
fires the row reads `detail: null`, but the check id names the failing control and the verdict is
correct. It is a reference-test diagnostic convenience touching no public contract.

## 7. Preserved design laws

The thirteen unchanged v17 correction areas — zero-config discovery and installed capability
availability; typed config and TS logical node kinds; language-specific native evidence and
provider/body/dialect ownership; clone progression and confidence; import/runtime/history/test
evidence authority; per-requirement native-9 / imported-7 causes with lossless
producer/consumer vocabulary; coverage partition within the full owning tuple and conditional
file totality; stable identity and typed canonical closure; baseline changed-code audit;
command/operation/generic-vs-repair replay; immutable Run and current availability; public
failure composition; and authorization and output failure after a committed Run — are preserved,
and I establish that structurally rather than by headline.

**Zero law-bearing files changed.** All 42 product contracts, schemas, models and case-corpus
files in v18 are byte-identical to their v17 entries. The five product contracts and their index
are unchanged. The one executable change is confined to a reference harness and is monotonically
stricter, so no law enforced in v17 is unenforced in v18. I found **no new required gap**, and I
have manufactured no product host measurement in place of one.

## 8. Governance

Sixteen AR rows, fifteen FW rows, twenty-seven inherited residuals (DR-001..011 plus the DR-011
subledger R01..R16; DR-012 is header prose, explicitly excluded, not a row), thirty evaluation
sub-residuals, five scoped review owners and thirty-two qualification gates. Each is given an
ID-keyed disposition with its own basis, scope and authority, and none is a new grade.

All AR, FW and residual owning documents are byte-identical v17→v18. The one owner document that
changed is `correction-crosswalk.proposed.json`, and I diffed it leaf-by-leaf: **64 changed
leaves are all `latestCompletedReview` pointers, 96 added leaves are appended `historicalReviews`
entries, and nothing was removed.** Review routing moved; no obligation, selector, owner, unit,
contract or status field did, and no history was lost.

The five DR-201..205 owner rows are routing-assessed only, and each literally sets
`appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`. I read
`qualification-gates.proposed.json` in the snapshot directly: 32 rows, DR-G01..DR-G32, and **zero
rows carry a non-false value** for `demonstrated`, `qualified` or `implementationHarnessAuthored`.
D-372 is unapplied, its condition 5 is NOT MET, and the central readiness register is unchanged
and byte-identical. The four selected macOS/Linux machine IDs and the TS/JS/Rust/bounded-grammar
paths are retained in byte-identical files; carried, not regraded by me.

## 9. Evidence boundaries

Reference counts are calls and cases, not product qualification. The 46 handler line hits in the
coauthor's coverage trace show reachability only, not coverage of all null edge cases; my
controls supply the discriminating behaviour that trace does not establish. I distinguish
measured schema/helper checks, full closure, case injection, source inspection and host
qualification — of which **none was performed**, and I invented none. Partial helper inputs are
not admitted native or full Runs. I did not repeat the v17 full probe suite, because no new
concern requires it; I note for the record that the earlier v17 CL3 figure mixed denominators
(177 of 240 cross-product controls plus 14 presence/carryability equals 191, where a full sweep
would be 254), that 7 p06 controls actually exercised full closure, and that other
authorization/config/key claims remain static or helper-level as originally qualified.

Five failed attempts are preserved with their sources and raw outputs, including the report-field
misparse that initially reported zero deltas in every context, the regex monotonicity restatement
that matched nothing, the ancestor predicate that called all ten guarded sites unguarded, the
three render injections that escaped uncaught, and the raise-site miscount that would have framed
a live defect as latent.

## 10. Verdict

**ACCEPT** the frozen v18 source bytes. The correction is bounded, complete for this checker,
minimal, monotonically safe, and independently verified rather than accepted on report. No
required finding is unresolved, so no required finding forces CHANGES_REQUIRED.

Still required, and not supplied here: a fresh blind consumer review of these exact bytes — no
blind pass has accepted v17 or v18, the prior v16 ACCEPT did not survive blind 6, and all blind-6
and earlier corrections remain in view — and a complete, independently reviewed application and
readiness reconciliation. No implementation, commit, push, publication or readiness change is
authorized by this review.
