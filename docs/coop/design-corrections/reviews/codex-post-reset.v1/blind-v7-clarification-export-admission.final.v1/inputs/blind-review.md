# OpenSIP DR-011-R10 — blind consumer-B reconstruction (CORRECTED, clarification v1)

**Verdict: CHANGES_REQUIRED** — one MUST and one SHOULD remain; one original
SHOULD is retracted in full.

**Standing.** This supersedes my original blind report *as a corrected
statement of the same pass*. The original is immutable historical evidence at
`consumer-b.v7/output/blind-review.json` (SHA-256 `520b7ddf…d466d4`) and
`blind-review.md` (SHA-256 `ecd765f8…7a02e25`); both hashes re-verified. This
pass is a **post-review clarification after root feedback**, not a new fresh
blind and not a design-correction authoring pass. No contract, schema or kit
byte was edited. Design was read only from `consumer-b.v7/subject`; all 45 kit
files re-verified byte-identical at finish. No product qualification,
implementation authorization or readiness grade is claimed.

The correction record — what root raised, what I reproduced, what I changed, and
where I disagree — is `clarification.md` / `clarification.json`.

---

## 1. What changed from the original report, and why

Root audited my exported bytes, rehashed every blob and recomputed every object
identity (all correct), and raised two defects **in my own validator and
builders**. I reproduced both against the original exported bytes with the
original helpers *before changing anything*, and both are real.

### 1.1 My closure did not admit three record families

The original `Closure` walked `run`, `snapshot`, `plan`, `evidence`, `seal`,
`proof`, `closure`, `fact`, `subject-scope`, `coverage` and `view` — and never
walked `finding`, `finding-fingerprint` or `execution-plan` at all. Those three
domains were **exported and never admitted against any schema or order
annotation**. Consequently
`identity-schemas.v2#/$defs/finding/properties/evidenceRefs`, annotated
`x-opensip-order: canonical-set`, was never enforced, and my builder emitted
`[fact, coverage]` in construction order. Because `C` sorts object keys the sort
key is `{"digest":…,"domain":…}` — the **digest** decides — so the array was
ascending only by luck of which hex was lower.

**My original sentence "every record is validated against its owning normative
schema" was false as stated.** It is withdrawn.

### 1.2 My grammar-bundle check tested retention, not membership

Native §1.2 requires "every grammar definition, the bundle manifest and the
normalizer specification **present in the retained tree**". My original
`vec_syntax` put unrelated placeholder bytes in the `kind=grammar` closure tree
and retained the declared `bundleDigest`/`grammarDigest` bytes as loose CAS
blobs; my checker only tested `in cas`. Root's phrasing is exactly right:
**merely retaining a blob elsewhere in CAS does not satisfy membership.** The
normalizer specification passed only because I had coincidentally used identical
bytes in both places.

### 1.3 Where my measurement differs from root's

Root stated the unordered `evidenceRefs` are in RUN-TS, RUN-RS-A/A2 and
RUN-SYN-DATA, that five originals are refused, and that "both incomplete Rust
disclosure graphs admit". I measure **six** distinct graphs refused, because
**RUN-RS-NO-OWNERSHIP-DISCLOSED** also carries unordered `evidenceRefs` (fact
digest `9369…` before coverage digest `2d5a…`). Only **one** of the two
disclosure graphs — PARTIAL-ENUMERATION — admits. I accept root's substance in
full and record the different set, because the corrected report has to state
measured scope.

| graph | evidenceRefs ascending | grammar members in tree | corrected checker |
|---|---|---|---|
| RUN-TS | no | n/a | REFUSED |
| RUN-RS-A | no | n/a | REFUSED |
| RUN-RS-A2 | no | n/a | REFUSED |
| RUN-RS-NO-OWNERSHIP-DISCLOSED | **no** | n/a | **REFUSED** |
| RUN-RS-PARTIAL-ENUMERATION-DISCLOSED | yes | n/a | ADMITTED |
| RUN-RS-B | yes | n/a | ADMITTED |
| RUN-SYN-CODE | yes | no (3) | REFUSED |
| RUN-SYN-DATA | no | no (5) | REFUSED |

### 1.4 The corrections

Rather than hand-patch the three missing joins, I closed the *class*:
`admit_every_retained_object()` now runs schema **and** declared-order admission
over **every** retained typed object, dispatching through a closed
`FOUNDATION_SELECTOR` map plus the kit's own
`x-opensip-digest-domains.domainSets` for native domains. **A domain with no row
is itself a refusal.** I added the finding and execution-plan joins that were
missing, and replaced the grammar CAS test with a closure-**tree membership**
test carrying three distinct refusals.

Builders: `evidenceRefs` is now sorted by `C(item)`; the grammar closure tree is
**built from** the exact bytes the bundle declares.

---

## 2. Corrected measured scope

### Record admission — stated, not asserted

**Every retained typed object of all 16 domains is admitted against its owning
schema and its declared `x-opensip-order`, with zero uncovered domains**, plus
the named canonical-record preimages the closure fetches. Measured on RUN-TS:

`closure` 5, `coverage` 4, `evaluation-seal` 1, `execution-plan` 1, `fact` 17,
`finding` 1, `finding-fingerprint` 1, `native.context.typescript.v2` 3,
`native.semantic-universe.typescript.v2` 3, `plan` 1, `proof-bundle` 1, `run` 1,
`semantic-evidence` 1, `snapshot` 1, `subject-scope` 4, `view` 1 — **uncovered: none**.

### Graphs

| graph | objects | blobs | checks | result |
|---|---|---|---|---|
| RUN-TS | 46 | 120 | 379 | ADMITTED |
| RUN-RS-A | 41 | 114 | 328 | ADMITTED |
| RUN-RS-A2 | 41 | 114 | 328 | ADMITTED |
| RUN-RS-B | 40 | 110 | 319 | ADMITTED |
| RUN-RS-PARTIAL-ENUMERATION-DISCLOSED | 37 | 99 | 292 | ADMITTED |
| RUN-RS-NO-OWNERSHIP-DISCLOSED | 37 | 99 | 290 | ADMITTED |
| RUN-SYN-CODE | 31 | 77 | 207 | ADMITTED |
| RUN-SYN-DATA | 28 | 73 | 188 | ADMITTED |
| **RUN-TS-MUST1-PROBE** | 48 | 123 | 394 | ADMITTED |

**9 graphs, 2725 closure checks, 0 failures** on a from-scratch reload
(original: 8 graphs, 1974 checks). **36 negatives, all refused** (original: 29),
including six new discriminating negatives for exactly the two laws my original
checker did not enforce — in each grammar negative the bytes **remain** in the
CAS, so each is precisely a membership test.

---

## 3. Findings

### CB7-MUST-1 — **STANDS**

*A TypeScript/JavaScript clone body-dialect refusal has no published Coverage
classification, and the ambiguity reaches `run2`.*

Selectors, statement and reasoning are unchanged from the original report.
Re-measured on the corrected validator and **exported as a complete inspectable
graph**, `RUN-TS-MUST1-PROBE` (48 objects, 123 blobs, **394 checks, 0
refusals**, reloaded from scratch):

* scope: `clones@normalized-body-hash` over the inventoried path
  `package.json`, under the TypeScript universe;
* Coverage: `complete`, `deficiency: null`, `nativeCause: null`;
* clones facts anchored on that path: **0**;
* the body-dialect selector for that path refuses
  `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN`, which is named in **no** prose
  contract in the kit.

Correcting the two helper defects changed neither the probe's Coverage, its zero
clones facts, nor the selector's refusal — the finding is not an artifact of
them. Scope unchanged and precise: TypeScript/JavaScript universes only; the
syntax universe is closed by the grammar-capability guard and Rust by the
ownership selection law, both measured.

### CB7-SHOULD-2 — **STANDS**, with two corrections to my own wording

*Reachable Plan cardinality boundaries with no published typed refusal.*

**Correction (a): reachability is now measured, not argued.** The original
vector built a Plan-shaped object from 129 **synthetic** hex strings. The
corrected vector mints **129 real, distinct `TypeScriptNativeContextV2`
records** — one per real unit, each with its own inventoried `tsconfig.json` and
its own retained config graph, every H frame retained and every identity
recomputing:

| | 128 units | 129 units |
|---|---|---|
| distinct real contexts minted | 128 | 129 |
| analysis-spec rows (bound 1024) | admitted | 129, **admitted** |
| scope-descriptor roots (bound 1024) | admitted | 129, **admitted** |
| `plan.nativeContextDigests` (bound 128) | admitted | **refused** |
| Plan mints | **yes** | **no** |

**Correction (b): "names no field" was overbroad — root is right.** The refusal
*does* prefix the field name (`nativeContextDigests: [...]`). Re-measured: 8806
characters, restates the whole 129-element array, ends `"… is too long"`, and
carries **no standalone count, no limit and no remedy** (an earlier heuristic of
mine matched `128`/`129` inside 64-hex digests and gave a false positive; it is
corrected and disclosed). Same for `plan.importIds` at 257 (19555 characters).

The corrected claim: **no typed `PROJECT.SCOPE_LIMIT`-style refusal with a
bounded subject `field:count>limit` and a remedy is published for the `plan`
record family**, while native §14 publishes exactly that for four fields across
two other record families and explicitly rejects the generic projection.

**Correction (c): bounds re-measured** — `plan.nativeContextDigests` **128**,
`plan.semanticClosures` **128**, `plan.importIds` **256**, against
`semantic-configuration.evidence.importIds` **1024**. The original already
stated 128 for `semanticClosures`; confirmed, not changed.

### CB7-SHOULD-1 — **RETRACTED IN FULL**

*"The mandated per-requirement cause carrier cannot express 11 of 16 producible
outcomes."*

Root's challenge is correct. **My finding imposed an equation the kit never
states**: `unmetPreconditions[].code == the deficiency token`. Workflows §6 says
the exact cause is carried into the requirement's unmet precondition **so that
two different causes are two different REMEDIES**, and `DomainDetail` carries a
required `remedy`.

Three things in the kit I failed to weigh:

1. `x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary` names
   the carrier explicitly — record `repair.schema.json#/$defs/EvidenceRequirement`,
   field `deficiency`, "REQUIRED exactly when satisfied is false" — and states
   that the boundary "adds no D9 class, code, exit or **public detail code**".
2. `x-opensip-imported-requirement-law` distinguishes two outcomes in exactly
   root's terms: *"Named separately … **because the remedies differ**: import the
   evidence versus widen the capture."*
3. `RepairPlanDescriptor.applicable`'s own description is a conjunction, so
   `applicable:false` with an **empty** `unmetPreconditions` is consistent —
   measured schema-admitted.

**Measured: 16 of 16** outcomes are expressible in the field the law names. My
"5 of 16" counted membership of a different vocabulary in a different field.

**`REPAIR.EVIDENCE_RUN_UNAVAILABLE`, assessed as root asked:** registered, but
**not applicable** — §6 binds it to an evidence Run whose availability is
retained and whose sealed assurance is replayable, whereas an unsatisfied
requirement means the Run *is* available and its evidence is insufficient.
Borrowing it would misname the condition. It is also **not needed**.

**Demonstration** — two complete `RepairPlanV1` records, both schema- and
order-admitted, **zero new codes**:

| | native cause | imported cause |
|---|---|---|
| requirement | `references@resolved-binding` | `history-change@observed` |
| retained `deficiency` | `required-relation-missing` | `history-range-insufficient` |
| registered `code` | `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` | `IMPORT.ABSENT_FOR_PREDICATE` |
| `remedy` | carries plane + relation + rung + deficiency, "…re-analyse with the references capability requested for this unit" | carries plane + relation + rung + deficiency, "…widen the collected revision range and re-import" |
| `applicable` | false | false |

**Discriminating control:** collapsing both onto one remedy string makes the
remedies identical — which is what the purpose clause forbids, and is what makes
the positive meaningful.

**Expressible ≠ authorized.** Such a descriptor is a *disclosure*. Apply
additionally requires `applicable == true`, a `RepairApplyAuthorizationV1` bound
to the **exact** `repairPlanId`, base snapshot and project, and re-checked live
recipe trust. Measured: the authorization naming one plan does not name the
other.

**No residue requiring source clarification.** What remains is implementation
latitude the purpose clause leaves open — whether a host *also* emits an
`unmetPreconditions` entry, and which registered condition code it uses. That is
a choice among lawful renderings of a disclosure whose mandated carrier is
named, closed and total. The original finding text stands verbatim in the
immutable original report as evidence of the error.

### Advisories — all five STAND

`CB7-ADV-1` count corrected: the original compared **10 inherited fault-map
entries** against **12 successor enum members** (which include the `none`
sentinel). The like-for-like enum comparison is **11 → 12**; the delta is the
same single member (`host-invariant`) either way. `CB7-ADV-2`…`CB7-ADV-5`
unchanged.

---

## 4. Reporting-scope limits, corrected by measurement

Root's eight points are confirmed and now recorded as measurements, not
assertions:

1. **Failure envelopes** (7) are literal composed `CommandEnvelope` objects
   validated against the envelope schema and the termination branch contract —
   **not** raised-and-caught internal failures.
2. **Authorization vectors** measure schema validity, effect-value equality
   against the pinned truth table in the `child-process` mode, the canonical
   empty owner-array digest, and the display-alias enum refusal. The CI-consent
   refusal, the over-claimed `ENFORCED-PLATFORM` refusal and the repair-plan edit
   boundary are **literal assertions**, not outputs of an executed security
   admission engine.
3. **Comparison cases** are schema-valid descriptors with conceptual
   classifications — **not** a comparison engine; no pivot evaluated, no finding
   set diffed. The two ScopeDocument Plans **are** real Plans with distinct
   PlanIds, but are **not** two fully compared Runs.
4. **`minResolutionPredicates`** are ladder-index helpers plus cross-relation
   refusal — **not** full `sufficiency_v2` over every Coverage/evidence boundary.
5. **Relation digest-law traversal** covers **7 top-level occurrences**, not
   arbitrary schema inheritance (nested members, array elements, map values,
   `$defs` aliases, inline equal patterns and combinator branches are outside
   what I walked).
6. **"Single-field mutation" was not generally accurate.** Measured: **4 of 33**
   distinct mutations change strictly one field. The rest change a whole record,
   a retained blob, a closure tree or a selection, and most recompute downstream
   identities. What holds for all: each **isolates one law**.
7. **`nativeHPreimages.canonicalPayloadBytes`** are 400-character truncated
   heads for **4 of 6** records; full bytes are in the per-run blob exports.
8. **ADV-1 counts** corrected as above.

---

## 5. Limitations (added to the original set)

* This pass corrected **two real defects in my own validator** that my original
  pass did not catch. The corrected checker is still my own code written from
  prose; the same class of omission may remain elsewhere.
* My measured affected set **differs from root's stated count**: six original
  graphs are refused by the corrected checker, not five.
* Root's diagnostic copies were neither supplied to me nor used as an oracle;
  every conclusion here is my own measurement over the unchanged kit.
* Everything remains schema validation, helper predicates and retained closure —
  never host enforcement. Every OS, compiler, cryptographic, storage and
  confinement observation is a synthetic TCB assumption.

---

## 6. Verdict

**CHANGES_REQUIRED**, unchanged in class.

The reconstruction is stronger than the original claimed in one respect and
weaker in another, and both are now stated honestly. Stronger: nine complete
graphs close under a validator that admits every retained object domain against
its owning schema *and* its declared order, with 36 negatives all refused and
the MUST-1 probe itself exported as an inspectable graph. Weaker: my original
totality claim about record admission was false, and two laws went unenforced
until root found them.

The verdict is unchanged because **CB7-MUST-1** survives re-measurement on the
corrected build and is untouched by the helper defects, and **CB7-SHOULD-2**
survives with its reachability upgraded from argument to measurement.
**CB7-SHOULD-1 is withdrawn** — it was my error, not the design's. No new
findings were raised in this pass.

Any source fix would require a newly frozen candidate and another fresh
independent blind; this clarification accepts no future change and grades
nothing.

### Reproducing

```
cd /tmp/opensip-design-corrections/consumer-b.v7-clarification.v1/output
python -I -B work/run_all.py     # build, measure, export 9 graphs + 36 negatives
python -I -B work/verify.py      # from-scratch reload and closure
python -I -B probes/probe_root_claims.py                       # pre-fix reproduction
python -I -B probes/verify_originals_with_corrected_checker.py # corrected checker vs originals
```
