# Successor corrections — RRS-A1, RRS-A2, and the independent report's scope

**Standing: AUTHOR_PENDING_REVIEW.** Source coauthor, not an acceptor. **No final design,
blind or application acceptance comes from this origin.** My v1 source, runtime and handoff are
preserved unedited, as is the independent review at
`claude-glob-repair-bounded-review.v1/`. No consumer output was supplied or read.

---

## 1. RRS-A1 — my ownership law was wrong, and the omission is reachable

**What I wrote in v1.** Path ownership came from retained `source-path` subject scopes
(`file`, `clones`, `vcs-change`) alone. I argued from `subjectKindLaw` that those scopes name
paths, and from the same law's statement that a symbol's path "is NOT re-derivable from the
retained Run" that a symbol-kind scope could never contribute an owner.

**Why that was wrong.** Root's diagnosis is exact, and the independent review confirms it at
static normative scope. The `subjectKindLaw` proves those scopes **name** paths. It does not
prove they **enumerate every selected program that owns** one. And the opaque-symbol-ID
observation answers a **different question**: I do not need to reconstruct a path from a symbol
ID, because `enumeration-contract.v1.md` publishes the program's path **extent** directly —
available bindings carry `extents[]` with a non-null universe (§1), candidate-only bindings
carry `candidateSourcePaths` (§1), unavailable bindings keep `extents` "populated from host
membership so expected file/package paths are not lost" (§1), and the symbol extent is the
selected program's code scope (§5, §8). I reached for an argument that sounded rigorous and
used it to answer a question it did not address.

**I did not assume the omission was reachable — I tested it.** Driving the enumeration owner's
own `admit_enumeration` through the frozen `check-enumeration.v1.py` helpers
(`probes/symbol-only-admission.json`):

| shape | result |
|---|---|
| universe bound **only** to a symbol-kind cell, owning a path via its symbol extent, no file inventory | **ADMIT** |
| **unavailable** selected binding retaining a host symbol extent containing the path | **ADMIT** |
| candidate-only cell carrying `candidateSourcePaths` | **ADMIT** |

Admission does **not** prevent it. Root asked me to refute the hypothesised case honestly if it
did; it does not, so I corrected the law.

**And then I built it as a full admitted Run.** Root stated no full-Run counterexample had been
constructed and told me not to claim one without executing it. I executed one:

```
run3:896bef61cbe9969d20ccd93d7948ffbee2cedb747eb0ebf633584f96aaf1e63d   close_run ADMIT
  universe 17ce4077e6 : inventory cell only; file extent + file@enumerated scope; eligible true
  universe 03bbcc3284 : syntax cell only; symbol extent ['src/index.ts'];
                        scopes are declares/literal/control-flow ONLY — no source-path scope;
                        declares Coverage eligible FALSE
  source-path-scope-only owners : ['17ce4077e6']          -> would ADMIT the delete
  selected-program census owners: both                    -> REFUSES, naming the declares record
```

That is the discriminating control, through full Run admission **and** the current preview.

**The corrected law.** Ownership is the **retained selected-program census** of this Run's
`EnumerationPlanV1` — a **required** evaluator3 parameter (`EVALUATOR_REQUIRED_PARAMETER_MISSING`
when absent, re-admitted by full replay), reached through `run3 → plan2 → analysisSpecDigest →
parameters` using the identity owner's **own** `parameter_row_of`. No caller-selected map, no
optional unsigned sidecar, no filename parsing. Per selected binding: `extents[]` per kind plus
`candidateSourcePaths`. Available → contributes its universe. **Selected but unavailable** →
typed unresolved ownership that does **not** vanish behind a closed owner. **Unselected** →
never inferred. Each extent kind is read as itself, so file/package host extents stay distinct
from the semantic symbol program extent, all snapshot files are not every compiler's
`programRootFiles`, and a selected program whose own census lacks the edit **stays unrelated**.

**Source-path scopes are retained as an additional witness**, and their redundancy is now
*measured* rather than assumed: `witnessOnlyUniverses` is reported, and in the symmetric Run it
is empty while in the asymmetric Run the witness set is a strict subset of the census.

## 2. RRS-A2 — all five points, and what each now says

1. **Sentinel wording.** "the fixed all-unknown value" was wrong and is gone. The value is the
   **five-field least-closed display sentinel**
   `{false, unknown, none, present, unknown}`, described identically in the module, §6 and both
   schema annotations, including in the create-only paragraph.
2. **"Authoritative" boolean.** Removed. The module now says **no member of the record is
   authoritative, the boolean included**, and a control asserts the old phrase is absent.
3. **Summary versus eligibility.** Now defined rather than left open: when a relevant universe
   retains no Coverage, or an ownership is unresolved, the reduction **folds the sentinel in**,
   so the display cannot read as closed while eligibility is refused. It remains a display, not
   a native record.
4. **Ordering.** Prose, module and both annotations now name **UTF-8 encoded bytes** and the
   **six**-member sequence — the five `CoverageKeyV2` coordinates then the `coverage2` identity,
   which makes the order total between records agreeing on all five.
5. **Remedies.** Dissent remedies now name **all six members unabbreviated**, including the
   exact retained `coverage2` identity.

## 3. Correcting the independent report's scope, as root qualified it

The independent review (origin `ce3dec3b-…`) is preserved unchanged; this corrects scope, not
its findings, and both of its dispositions stand.

* **Its RRS-A2 point 5 demonstration is not two lawfully admitted native records.** It built two
  `file@enumerated` records differing in `targetUniverse`. `file` is `universeRule: same-only`,
  so `sourceUniverse != targetUniverse` is not an admissible `file` key, and abbreviated
  pseudo-IDs are not retained identities. **I do not repeat that claim.** The *structural* fact
  it reports — that the old remedy omitted `coverageId`, `targetUniverse` and the scope
  commitment — is real and is what I fixed. My discriminating controls are conforming: one keeps
  `file` source == target and separates the records by `subjectScopeCommitment` and `coverage2`
  identity; the other uses `imports`, which the registry gives `universeRule: admitted-target`,
  for the cross-universe key. A control asserts that relation-rule split explicitly.
* **No full-Run remedy counterexample is claimed** by root, by the reviewer, or by me.
* **The sentinel has three non-unknown members, not two.** Counting only
  `entryPointsRecognized` and `nonliteralLoading` as "wrong on 2 of the 5 fields" understates
  it: the boolean `false` is also not `unknown`. A control asserts exactly two members are
  `unknown` and three are not.
* Its RRS-A1 evidence is **static normative plus a unit-scoped probe**, with no full-Run
  counterexample — its own words. I have now executed one; that is mine to report, not a
  restatement of theirs.

## 4. Two further corrections I am making on my own initiative

**My v1 claim that the source-path join "leaves no cross-universe question open."** True of
those three relations, and I used it as though it settled the ownership question generally. It
settled only the *witness* join. The cross-universe question for **Coverage selection** is
separate and is answered on `sourceUniverse` alone; the ownership question needed the census.

**My v1 native-lane reporting was imprecise.** I wrote that the lane showed "zero semantic
faults". It showed **no reported** semantic faults because it **stopped at pin admission and
never executed them**. Absence of reported faults is not evidence that those checks passed.
This turn's record states that explicitly (`probes/native-lane-detail.json`,
`semanticChecksExecuted: false`), and root assesses the sealed integrated run.

---

**Nothing here is accepted.** These bytes are AUTHOR_PENDING_REVIEW; the limits and unexecuted
boundaries are in `author-review.md` and are part of this correction.
