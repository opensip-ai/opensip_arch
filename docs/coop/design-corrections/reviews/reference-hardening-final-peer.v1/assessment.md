# Bounded final-source peer assessment — reference hardening after v20

**Standing.** This is a bounded **source proposal only**, written as a peer/coauthor to the completed
first coauthor proposal. Nothing here is integrated, committed, pushed, published, or applied to the
live repository or to the frozen v20 subject. It expresses **no** independent20 verdict, **no**
acceptance, **no** blind result, **no** readiness grade, **no** product architecture acceptance and
**no** implementation authority. The first coauthor proposal is preserved untouched and re-verified at
its recorded digests. All root integration, ledger, count-record, readiness, independent, blind and
application work remains **pending** and nothing here anticipates its outcome.

---

## 0. Custody

| Item | Value |
| --- | --- |
| Parent source | `/tmp/opensip-design-corrections/candidate-subject.v20` (11932 files) |
| Manifest declared | `878e5bebd5a7b144ef7900e774af0e13eb1b3a01d32e7f289b6f483de6832f3c` |
| Manifest recomputed | `878e5beb…` — **match** |
| Frozen `run-reference-checks.py` | `9f12c7d4…` 1958 B — **match**, unchanged at end of session |
| Frozen `check-identity.py` | `d60afe7a…` 575389 B — **match**, unchanged at end of session |
| Frozen `workflows_model.v1.py` | `24aa11cf…` 137623 B — **match**, unchanged at end of session |
| Foundation pin ledger over a clean copy | 1100 entries, **0 mismatches** |
| First coauthor proposal | all 9 recorded deliverables re-hashed, **0 mismatches**, untouched |
| independent20 `review.json` | `fd7b6a85…` — **match** with the declared SHA, read only |

Every source file was hashed at read time. The three changed files carry before/after digests and byte
lengths in `proposed-changes.json`, together with the first coauthor proposal's digests as a third
column so the two proposals can be told apart mechanically.

### 0.1 One custody defect in the first coauthor proposal

`custody/proposed-hashes.json` in the first proposal labels the **after** byte counts as
`beforeBytes` (3927 / 578677 / 138477 are the *after* sizes; the frozen sizes are 1958 / 575389 /
137623). Its own `proposed-changes.json` is correct, so nothing downstream of that file is wrong, but
a reader taking `proposed-hashes.json` at face value gets the wrong before-sizes. Flagged for the
successor record; not a defect in any changed source path.

---

## 1. Assent to the three refinements

I agree with all three, with one place where I go **further** than the brief and one where I disagree
with the first proposal's stated reasoning rather than with root. Each is verified against actual
source below, not accepted on report.

### 1.1 `foundation/run-reference-checks.py` — **agree, all five qualifications**

The executable correction is carried over **exactly**: AST modulo docstrings and compiled code objects
are both identical to the first proposal (`evidence/ast-code-comparison.txt`, block A). Only the
docstring and two comments changed.

**(a) "the SAME shape" is not true and is now not claimed.** Read against the two result dicts: every
entry gains `timedOut`, and the result gains `timedOut` and `childTimeoutSeconds`. That is a
**superset**, not an identical shape. The docstring now says so, and adds the property that actually
matters to a consumer — every previously present key is still present.

**(b) 5 × 600 s = 3000 s is a child-budget aggregate, not a wall-time bound.** Verified structurally:
the pin sweep hashes all 1100 ledger entries *before* any child starts, each child costs a process
creation and teardown, and the final report write follows the loop. None of that is inside any
`timeout=`. The first proposal's "Suite worst case is bounded at 5 x 600s" is therefore wrong as a
wall-clock statement. The comment now states the aggregate, states what it excludes, and explicitly
says **this file states no whole-run wall-time bound and no caller may derive one from it**.

This is not pedantry — it is exactly the failure that already happened one level up. An outer
orchestration bound of 600 s preempts a single child's *inner* 600 s budget and destroys the very
timeout report the change exists to produce. Root's final runner at outer **3600 s** is consistent
with an inner aggregate of 3000 s plus sweep, spawn and write overhead, and I propose **no**
orchestration change.

**(c) `reportSha256: null` is not proof that nothing was written.** Verified from the code: on the
timeout branch `sha` is set to `None` **without consulting the filesystem at all**. It is a refusal to
attribute, not an observation about disk. The first proposal's own synthetic evidence says this
plainly — `identity-report.json` **existed on disk at 172008 bytes** at the moment `null` was
reported — so its docstring wording ("cannot claim the child report it did not write") contradicts its
own measurement. The docstring now says: **no completed result is attributed**, and explicitly notes
that a child can be killed after writing, and that an earlier run's report can be sitting there under
the same name.

**(d) "no failure path at all" is too broad.** Verified against the frozen file: a nonzero child exit
was already reported (`exitCode` on the entry, `passed` false), and a changed or missing pin was
already reported (`sourcePinsValid` false, `changedOrMissing` named, no child run). Only a **timeout**
escaped past the write. The first proposal's §1.2 prose overstates this; its docstring was already
narrower. The docstring now names the missing path as exactly that one, and only that one.

**(e) 600 s is a bounded reference-run budget, not a law.** Agreed and stated: not a product timeout,
not a service level, not an authorization law, and not citable as one outside this file.

### 1.2 `workflows/workflows_model.v1.py` — **agree, and measured rather than argued**

Executable behaviour is identical to **frozen v20** and to the first proposal — AST modulo docstrings
and compiled code objects both identical (blocks C and D). Exactly **one** docstring differs,
`verify_scope_parameter_binding`, enumerated separately.

**The precedence claim was too broad, and this is measurable.** The first proposal's comment said
*"Ambiguity is decidable without reading `scope` at all, so it is decided first and every caller of an
ambiguous spec is told the same one thing."* The first clause is true in principle; the conclusion is
false about this code, because `digest = doc_digest(scope)` runs **above the row filter**, before the
rows are even counted. `evidence/probe-ambiguity-precedence.py`, run against the unmodified frozen
model, puts **one ambiguous spec** to five callers:

```
candidate A            -> Refusal CONFIG.INVALID / CONFIG.INVALID
non-candidate C        -> Refusal CONFIG.INVALID / CONFIG.INVALID
float member           -> AdmissionError EXACT_JSON_TYPE_REQUIRED
negative zero          -> AdmissionError EXACT_JSON_TYPE_REQUIRED
non-string key         -> AdmissionError STRING_KEY_REQUIRED

DISTINCT ANSWERS FOR ONE AMBIGUOUS SPEC: 3
CLAIM "every caller ... is told the same one thing" HOLDS: False
```

So the comment is narrowed to the one precedence the code establishes: **ambiguity outranks the
payload-digest match, for a scope document this function has already digested.** It is not precedence
over canonicalisation, and `adopt_baseline`'s authority and availability checks still precede the
function entirely. All three are now said explicitly.

**Existence versus position, kept apart.** The comment now separates them: *existence* is the whole of
the soundness argument (with no guard, either candidate holder obtains a `verified` digest, because
the existential match succeeds for each separately); *position* decides only which true reason a
caller holding **neither** candidate is given. independent20 NEW-SHOULD-1 reaches the same
distinction independently ("the harm the prose names IS covered, because deleting the guard outright
was detected") — I record that as corroboration I did **not** re-derive here.

**Where I disagree with the first proposal.** It examined the docstring and chose to leave it,
reasoning that the sentence "is about why the guard **exists** … It is accurate." Clause by clause
that is right. As composed it is not: the `because` binds the existential rationale to the phrase
*"refused before any payload comparison"*, so a reader takes the **ordering** to be what prevents the
verified digest — the exact misreading the new inline comment twelve lines below now denies. Leaving
it would have left one function documenting two incompatible rationales. I made the minimal edit that
attaches the rationale to the refusal *existing* and states the placement separately for what it
decides. No new law is introduced; the CARDINALITY registry citation and both preserved refusals are
untouched.

That edit has a methodological consequence the first proposal did not have to face: **a docstring is a
code-object constant**, so its "identical compiled code objects" test would now fail for an
intentional documentation change. `work/compare-executable.py` therefore normalises docstrings to a
sentinel, compares AST and code objects, and then reports the differing docstrings **by qualified
name** as a separate result — intended documentation change made visible rather than hidden.

### 1.3 `foundation/check-identity.py` — **agree with the removal**

All five new third-document controls are carried over **byte-identically**: the diff against the first
proposal contains no addition at all, only a four-line deletion. Every substantive carrier, registry
and enum-membership control is preserved. Static control inventory against frozen v20: **+5 / −1**,
with the order of every shared id preserved (`evidence/control-inventory.txt`).

Five reasons the removed control should go, the third and fifth of them measured here:

1. **It asserts over source text, not behaviour.** `count("'CONFIG.INVALID', 'CONFIG.INVALID'")==1`
   and `count("CONFIG.INVALID")>2` over another file's bytes. Reformatting the call across lines, or
   any future refusal legitimately using that legal pair, breaks it while behaviour is unchanged.
2. **Its name outruns what the counts witness.** independent20 ADV-3 states this precisely:
   `CONFIG.INVALID` is already published elsewhere as an *error_code*, and as a **detail** only at
   this site. "A code this model already published" is witnessed only in the weak string sense.
3. **Measured coupling, not hypothetical.** My own comment-and-docstring edit — proven
   executable-inert — moves its input from **38 to 39** (`evidence/brittle-count-coupling.txt`). It
   still passes, but a control whose inputs move when a comment is edited is measuring the wrong
   thing. This is the concrete case for removal rather than repair.
4. **What it was meant to prove is already proven, behaviourally and next door**: closed-registry
   membership in both `D9ErrorCode` and the public `DomainDetailCode` enum; admission of the *actual*
   termination through the owning unit's own pinned `StepTermination` validator; and a live negative
   control showing that validator refuses an unregistered detail.
5. **Measured: it never held the ordering.** Under the reordering mutation both counts are unchanged
   (1 and 39 on each side), so it passed under mutation. Its removal cannot weaken the ordering
   discrimination — confirmed by the mutated run below failing exactly the same two controls.

Nothing replaces it. No duplicate assertion, no new product requirement.

---

## 2. Runs — what was measured here

All runs used a disposable copy of the frozen parent with the three overlay files installed and the
ledger re-pinned **in the copy only**. Interpreter: CPython **3.12.13**, Unicode **15.0.0**,
`jsonschema` 4.26.0, `referencing` 0.37.0.

### 2.1 The final identity checker — MEASURED, once

```
work/refenv/bin/python -I -B .../foundation/check-identity.py --report .../identity-report.json
exit 0    {"passed": 1596, "failed": 0, "productQualification": false}    118.36 s wall
```

Count account derived from the report itself, not from arithmetic:

| | passing calls | distinct ids | historical duplicate extras |
| --- | --- | --- | --- |
| frozen v20 | 1592 | 1580 | 12 |
| **this proposal, measured** | **1596** | **1584** | **12** |

`1592 + 5 new − 1 removed = 1596`; `1580 + 5 − 1 = 1584`. The two historical duplicate ids
(`closed-closure` ×7, `exact-version-closure` ×7, 12 extra instances) are untouched. This **matches**
the figures root expected, and it is measured rather than assumed.

### 2.2 Foundation total — MEASURED, all five components

The other four children were run directly (they are unchanged sources, and this is not a repeat of the
five-child wrapper):

```
check-foundation.py             exit 0   231
check-identity.py               exit 0   1596
check-product-quality.py        exit 0   24
check-product-configuration.py  exit 0   28
check-array-orders.py           exit 0   65
                                       ----
                                        1944
```

Foundation **1944**, measured componentwise, matching root's expectation.

### 2.3 Reordering mutation — MEASURED here, deliberately not reused

Root permitted reuse. I re-ran it anyway, for one named reason: **the control I removed reads the
source text of the very file the mutation edits**, so reusing mutation evidence about that file while
deleting a text-count check over it deserved a measurement rather than an argument.

The same transposition the first session used, applied to *this* proposal's file — the at-most-one
guard moved verbatim below the payload match, **481 characters differing, length delta 0**, a pure
transposition (asserted by the mutation script, not assumed):

```
exit 1    {"passed": 1594, "failed": 2}    120.80 s wall
  FAIL an-ambiguous-spec-refuses-as-ambiguous-even-for-a-document-that-is-neither-candidate
  FAIL the-three-answers-for-one-non-candidate-document-stay-distinct-by-row-multiplicity
```

Exactly the two discriminating controls, and only those. `1596 − 2 = 1594`. The mutation copy is
separate; the primary copy was never mutated and needed no revert.

### 2.4 What is REUSED and not re-run — stated as reuse

**The wrapper timeout evidence**, including the synthetic 5 s injection, is **reused from the first
coauthor proposal and was not re-executed here.** The basis is proof, not assertion:
`run-reference-checks.py` is executable-identical to that proposal — AST modulo docstrings and
compiled code objects both identical — and docstring/comment text cannot alter `subprocess` behaviour.
The five-child wrapper itself was **not** re-run here either; that its report shape and timeout path
behave as the first proposal measured is **stated on that equivalence, not demonstrated in this
session**.

---

## 3. Remaining issues and limits

1. **`source-pins.v1.json` still requires a consequential update outside the allowed paths.** All
   three files are pinned entries the launcher verifies before executing anything; without re-pinning
   it refuses with `sourcePinsValid: false` and runs nothing. Exact replacement digests are in
   `proposed-changes.json`. Mechanical, but the proposal is not executable as-integrated without it.
   Unchanged from the first proposal — not resolved by this session.
2. **`validation-summary.v1.json` goes stale**: `checksPassed` 1940 → 1944, `components.identity`
   1592 → 1596, `identityCountAccount.passingCalls` 1592 → 1596, `distinctIds` 1580 → 1584,
   `duplicateExtraInstances` unchanged at 12. Not pinned, so nothing refuses; it would simply be wrong.
3. **`identity-check-counts.v20.json` is frozen review history and was not touched.** Whether to add a
   successor account is an integrator decision I deliberately did not take. Old count records are
   never rewritten.
4. **Advisory, new here, and not a proposed fourth path.** The reference suite is bound to Unicode case
   data **15.0.0** and refuses as an explicit *environment fault* on any other. My first run, on
   CPython 3.14 (Unicode 16.0.0), faulted with `UNICODE_CASE_DATA_VERSION:declared=15.0.0:running=16.0.0`
   (`dev-attempts/ATTEMPT1-py314-unicode16-environment-fault.stderr`). This is **fail-closed and
   correct** — it refuses rather than folding differently — but the launcher pins 1100 source files and
   does not record the interpreter precondition that makes its counts reproducible. Raised as an
   observation for the successor record; I am **not** proposing a change to any path for it.
5. **Not re-derived by me**: independent20's claim that deleting the guard outright is already
   detected. I treat it as an observation, not as verified here.
6. **Scope actually exercised**: the foundation suite only. Security, native, workflows and
   integration suites were not run. Stated, not demonstrated.
7. **The first proposal's `custody/proposed-hashes.json` byte-label defect** (§0.1) should be corrected
   in the successor record.

## 4. Verdict of this peer session

**Bounded final-source assent** to the three changed paths as hashed in `proposed-changes.json`, with
the consequential-update issue (§3.1) open and outside these paths.

This is assent to **source** only. It is not an acceptance, not an independent verdict, not a blind
result, not a readiness grade, and not authority to implement. Root integration, the four final
source-pin ledgers, the final reports/counts and readiness records, the successor freeze including the
21-of-31 unchanged protected files, a fresh independent review, a new blind pass and application work
all remain **pending**, and no acceptance is inferred from any of them.
