# Independent design/reference review — OpenSIP candidate-subject.v13

**Verdict: ACCEPT.** Zero unresolved MUST. Zero unresolved SHOULD. Two advisories,
recorded separately and deliberately not promoted to blockers.

`subjectManifestSha256 = 8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023`

**Reviewer standing.** Fresh independent session. I authored none of these bytes.
I am not coauthor `6f624b3a-aade-4530-addc-03c02405732a`, not prior independent
`864c56f8-181e-47fc-9681-690374211d0d`, and not blind consumer
`4dcdbac0-6004-49dc-8a37-70dad208639d`. I used no subagents, wrote no product
code, made no commit, push or source edit, and wrote only inside
`/tmp/opensip-design-corrections/post-reset-review.v13`. This is a design and
reference review. It is **not** blind reconstructability, **not** application
acceptance, **not** product qualification and **not** implementation
authorization.

---

## 1. Custody

The manifest hashes to the required value exactly. All **4379** declared files
match their declared SHA-256 **and** byte length; nothing is missing; there are
**zero undeclared files** anywhere under the snapshot root and **zero symlinks**;
`fileCount` and `totalBytes` agree with recomputation. Verified **before** the
review and again **after** — identical, clean both times
(`evidence/integrity-before.json`, `evidence/integrity-after.json`).

I recomputed the predecessor link myself rather than repeating the claim: the v12
manifest hashes to `fc124cc7…1678beb`, which is what v13 declares.

All work ran in a **disposable full copy** of the subject, verified byte-identical
to the frozen tree before use. The frozen subject was never written to.

---

## 2. The exact v12 → v13 delta

Recomputed from the two manifests, not read from a changelog: **1398 added, 0
removed, 36 modified**. 1396 of the additions are review records under
`reviews/`. Across the eight key normative files the change is strongly additive
— **1223 lines added, 65 removed**.

I inspected **every one of the 65 removals**. Each maps to a named correction,
and the most important ones are the defects themselves:

| Removed | Why it matters |
|---|---|
| `identity-model.py`: `… not in row['rungs'] and row['rungs']` | the exact CB3-MUST-1 empty-table bypass |
| `workflows_model.v1.py`: `RES_ORDER` | the global cross-relation rank table — CB3-MUST-2 |
| `policy-document.schema.json`: `Resolution` enum | the withdrawn abstract tier vocabulary |
| `imported-evidence.schema.json`: `sequence`, `minItems: 1` | CB3-SHOULD-1 and SHOULD-2 |
| `native_evidence_model.v2.py`: the `LADDERS` literal | replaced by derivation from the authority |

Nothing was silently dropped. Three of the five product contracts were modified
(`identity-and-evidence.md`, `native-evidence.md`, `workflows-and-surfaces.md`);
`README.md`, `admission-and-qualification.md` and `security-and-lifecycle.md` are
carried unchanged.

---

## 3. Reference command reproduction

All **six** recorded commands reproduced in the disposable copy. Before running
anything I independently verified **all 1308 transitive pins across four ledgers**
(1128 distinct targets): zero mismatched, zero missing. The v11 two-stale-pin
failure did not recur. **I did not re-pin anything.**

| Command | Exit | Result |
|---|---|---|
| foundation | 0 | 1325 = 231 + 977 + 24 + 28 + 65 |
| security | 0 | 456/456 cases, 10 invariant sweeps |
| native | 0 | 346/346 cases, 66 matrix cells |
| workflows | 0 | pins valid, 65 sources |
| workflow-surface | 0 | 1598/1598 checks |
| integration | 0 | 363 passed, 0 failed |

Every generated report and every log is **byte-identical** to the retained
candidate results. All eight reports were freshly written (mtimes confirm it), so
byte-identity is a determinism result rather than a skipped write. **I found no
intended nondeterministic operational field**, and therefore normalized nothing.

**Counts versus unique cases.** The identity account is honest and I recomputed
it: 977 passing *calls* but **965 distinct ids**, 12 duplicate extra instances,
from exactly two repeated ids (`closed-closure` ×7, `exact-version-closure` ×7).
The record states this rather than reporting 977 unique cases.

**Failed first attempt.** `final-reference.v13-attempt1` is retained with
`passed: false` and integration at exit 1, along with the stale prior report. The
failure is preserved, not overwritten. Record and crosswalk changes preceded the
final pin refresh, and the final seal of the same 1308 pins passed — consistent
with my own pre-run verification. A working-tree PASS is not proof of frozen
bytes; my verdict rests on the frozen manifest.

---

## 4. The five actual Bv3 MUST findings

I read the **full** `blind-review.json` and its companion Markdown, not a
summary, and confirmed the in-subject copy is byte-identical to the repository
copy. Earlier acceptance and positive reference counts discharge nothing. I
treated every root and coauthor assertion as a claim to test, and ran **286
independently authored probe cases** against **actual Run admission** wherever
possible — not schema enums.

### CB3-MUST-1 — the rung ladder — **RESOLVED**

All thirteen relations now publish an explicit weakest-first `ladder`, alongside
`ladderAuthority`, `rungsAreFieldRulesNotTheLadder`, `membershipRule` and
`subjectKindLaw`. Eight relations still carry `rungs: {}` — correctly, because
that is the per-rung *field-rule* table and single-rung relations have no field
variance.

**One authority, verified.** The foundation registry is the single source. The
native model and the workflow model **derive** their ladders by reading that file
at import time — they are not copies at all, which is stronger than the declared
"drift-checked mirror". The only genuine second copy is the capability-manifest
JSON registry, and I verified it matches **exactly and in order** for all 13
relations. All 12 inherited ladders match `fact-plane.v1` verbatim;
`unresolved-edge@[observed]` is the declared native-only addition.

**The decisive test was at Run admission.** My first attempt was insufficient and
I say so: swapping only `relation` left the `references` payload in place, so
those cases died at `PAYLOAD_RECORD` **before the ladder guard ever ran**. A
refusal that never reaches the guard under test is not evidence about that guard.
Supplying valid per-relation payloads for the four constructible symbol relations
(`declares`, `literal`, `control-flow`, `reachability`) gave:

- **4/4 positive controls admit a complete Run** at the relation's own rung, and
- **56/56 foreign-rung cases refuse specifically at `RELATION_RUNG_NOT_IN_LADDER`.**

Under the removed guard, all 56 would have admitted. Also confirmed:
`declares@resolved-callee` refuses; `references@syntactic` refuses (so the flat
15-rung vocabulary is necessary but never sufficient — `syntactic` is shared by
three relations); per-rung required/forbidden field rules still fire; and
unregistered universes refuse.

*Limit:* `file`, `package`, `vcs-change` and `clones` refuse earlier for
unrelated join reasons, so for those four the ladder is covered at the registry
and authority layer only.

### CB3-MUST-2 — `minResolution` — **RESOLVED**

The abstract tier enum is withdrawn; the atom names the rung directly, with
satisfaction defined as ladder-index comparison **within one relation**, and "a
rung of another relation is not a weaker or stronger value, it is a refusal". I
verified the three flat vocabularies now coincide exactly — workflow policy
`Rung` (15), native `RequirementV2` `Rung` (15), and the union of the 13 authority
ladders (15) are one set. `RES_ORDER` is gone from live code; the only surviving
mention is a withdrawal note that quotes it and independently flags that its
`external`/`resolved` tie was itself an arbitrary collision.

**CX-BV3-EVIDENCE-USE-1 reproduced at both boundaries.** This took four
corrections to my own harness — three upstream joins (a stale stage-spec blob, a
stale seal `policyDigest`, a stale compiled program) each masked the guard under
test and made all three arms share one cause. Once isolated, varying **only** the
declaration:

| Arm | Policy admission | Retained Run admission |
|---|---|---|
| matching declaration | admits | passes the gate, stops at a *different* later join |
| omitted declaration | refuses `IMPORT.ABSENT_FOR_PREDICATE` | **refuses `POLICY_RULE_NOT_ADMISSIBLE:…:IMPORT.ABSENT_FOR_PREDICATE`** |
| mismatched kind | refuses | **refuses `POLICY_RULE_NOT_ADMISSIBLE`** |

Distinct causes in both differentials. `close_run` now calls the **complete**
per-rule admission, not `admit_atom` alone — so merely validating individual atoms
could not produce this refusal. The earlier one-document-two-answers divergence is
closed. The declaration must *match*, not merely exist.

*Limit:* my declared arm then stops at `PROGRAM_PREDICATE_PROGRAM_JOIN` because I
did not rebuild the predicate witness. That is my harness, not a design result.

### CB3-MUST-3 (with ADV-3) — `syntax-only` — **RESOLVED**

A third closed context/universe pair is registered. Universe fields stay
**required and non-nullable** — nullability was explicitly rejected so every fact
still states what produced it — and the syntax universe carries a retained,
closure-joined **grammar bundle** and normalizer, with no toolchain, stdlib,
lockfile or config graph.

**The compiler-free claim is real, and I checked the snapshot rather than the
flag.** The pure-syntax inventory contains no `Cargo.toml`, `Cargo.lock`,
`.cargo/config.toml`, `tsconfig*.json`, `package.json` or `package-lock.json`,
and the Plan names **exactly one** native context. The fixture itself warns that
renaming a file to `.md` would only demonstrate a file-inventory Run inside a
*mixed* repository — and that warning is correct.

All three released-v2 root counterexamples now refuse **at actual Run admission**:

- pure Markdown `declares` fact → `SYNTAX_CAPABILITY_UNSUPPORTED_FACT`
- complete empty `declares`/`clones` Coverage → producer discloses
  `unknown` + `language-tier-unsupported`/`capability-missing`; an **injected**
  false complete refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`
- code-grammar `references@resolved-binding` (and imports/calls/types/
  reachability) → `SYNTAX_CAPABILITY_UNSUPPORTED_FACT`

I injected false complete, null cause, wrong cause and wrong deficiency into
**actual empty Runs** rather than trusting producer normalization; each refuses
with its own distinct typed cause. The healthy syntax clone control is a **real**
complete (`complete`/null/null) and carries **no Rust ownership cause** — the v2
defect that conflated a missing ownership *axis* with a missing ownership *record*
is fixed.

**Code versus data capability — substantively assessed, and sound.** `syntaxClass`
is **not caller-selected**: it is read from a closed published registry, the
declared value must equal the registered value, and the coupling to the
clone-preimage language enum is enforced in **both** directions. Declared suffixes
must match the host's bundled routing, and one suffix may own only one grammar. So
a caller cannot promote Markdown into the clone identity domain nor demote Rust out
of it, and no fabricated data-language tokenisation is claimed anywhere. All four
bundled data grammars (json, toml, yaml, markdown) close real **inventory** Runs
and refuse code-construct facts. Inventory-only scope stays representable: a
non-parseable path and a foreign-language `.py` path both still inventory.

**Selected-row suffix control.** A TypeScript row owning only `.ts` supports
`a.ts` and does **not** support `a.tsx`; a row owning both does. I confirmed this
is the exact function the Run path calls, with the universe's selected rows and
the fact's own anchor paths. *Limit:* I did not build a Run with a `.tsx` anchor
under a `.ts`-only selection; the row-level control is verified at the helper.

**The subjectKind law is unambiguous where it is executable,** and I probed both
halves. Source-path relations are judged on the scope's **own** subjects with
`require_all=True`: a README-only clone scope is unsupported, a code-only scope is
supported, and a **mixed** code+data clone scope is unsupported in **both orders**
— a mixed scope cannot hide its unsupported member.

**On the coarser symbol limit, which I was asked to assess independently: I judge
it sound and correctly disclosed.** It is coarse but not vacuous — a data-only
inventory still refuses and an empty extent still refuses. Crucially it cannot
launder an unsupported *fact*, because facts are judged `require_all=True` on
their own anchors: I confirmed at Run admission that a Markdown-anchored
`declares` fact refuses in the *same* snapshot where a code-anchored one admits.
The residual is confined to empty symbol-relation scopes in mixed repositories,
which is inherent to an opaque `SubjectIdV1`. Inventing symbol-to-path parsing
would be fabricated evidence, and the registry states the limit rather than
working around it. Some general comments retain earlier extent shorthand, but the
executable law governs and does not create a second reading.

Existing behaviour is preserved: **16/16** complete Runs close across
{typescript, rust} × eight relations.

### CB3-MUST-4 — `ScopeDocumentV1` — **RESOLVED**

The parameter class carries a second row keyed by the **exact** document and
selector. I treated the row as insufficient on its own and tested the joins: a
legal parameter **closes a real retained Run**; malformed and unknown-field
payloads refuse at `PAYLOAD_RECORD:#/$defs/ScopeDocumentV1`; an unregistered
schema refuses at `PAYLOAD_PARAMETER_UNREGISTERED`, so the class is still closed.

The two scope records stay **distinct**: the repository scope-descriptor offered
as the operator glob document refuses, and the glob document offered under the
import-source-context schema refuses. Repository discovery extent and operator
policy selection do not substitute for each other.

The comparison join itself works: a selected parameter verifies; no selected
parameter refuses `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`; a digest mismatch
refuses `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`. A comparison in which **only**
the operator glob policy changes moves `scopeDigest`. And the design is honest
about the unverified path: `adopt_baseline` with no analysis spec states in its
own docstring that the binding is then a *caller assertion* — pure digest
projection grants no selection proof.

### CB3-MUST-5 — partial-ownership disclosure — **RESOLVED**

Three registered `NativeCause` members are paired in one table; all three
deficiencies are `input-closure-incomplete`, all three causes are registered,
distinct and non-null. The source itself records that adding the enum members was
necessary and **not sufficient** — a vocabulary nothing derives and nothing
enforces leaves the disclosure optional, which is exactly what the old
counterexamples showed. The pairing is now **derived** by the owning producer from
committed ownership and *this* scope's subjects, and never read from the claim
being judged.

I probed the derivation exhaustively with **19** ownership records I constructed
myself. Missing, partial and ambiguous each yield their own cause; `partial` is
checked *before any row is read*, so incomplete discovery cannot act as an
implicit edition selection; a dangling unit record and a crate absent from the
edition map are ambiguous; two selected owners that agree owe nothing.

The subtle half — **explicit selection is not unfinished enumeration** — holds. A
path compiled by no selected target owes nothing. Owners lying entirely outside
the selection who disagree with each other create **no false ambiguity**. A
selected owner plus a conflicting unselected one is unambiguous. Ambiguity on a
path outside this scope's subjects does not taint it, while the same record *is*
ambiguous for its own subject. At Run admission three *separate* refusals fire
(false complete, undisclosed, deficiency mismatch) because three different things
can be wrong with one claim; the old check stopped after two.

---

## 5. The three SHOULD findings

I compared **logical shape** — order annotation, type, required membership,
`minItems`, `maxItems`, `uniqueItems` — not JSON text.

- **SHOULD-1 — RESOLVED.** `import.omissions` is `canonical-set` in both units;
  all three scope arrays are `canonical-set` in both; required sets and property
  sets agree. Sweeping **every** mirrored wrapper field, **zero** disagree on
  owning order.
- **SHOULD-2 — RESOLVED.** `minItems 0` and `maxItems 4096` in **both** units. I
  checked both bounds deliberately: testing only the maximum would have missed the
  `minItems` half, which was the actual divergence. I agree with the selected law
  — `minItems 1` was **not** justified merely because `payloadDigest` exists,
  because mandatory payload retention is a separate obligation from the *optional*
  asset inventory, and the maximum adopts the already-published 4096/256 MiB bound
  rather than inventing one. The root "6 mismatches / 13 cases" figures are
  counterexample probes and I did not treat them as product qualification.
- **SHOULD-3 — RESOLVED.** `contentSha256` is now asserted "as RETAINED, joined by
  digest", the rows are "deliberately NOT snapshot inventory rows", and the
  machine-readable join is still a `blobJoin`. Conventional pruning by path
  segment and bare-specifier resolution are unchanged. My first check flagged this
  by naive substring match; the old phrase survives exactly once, inside the
  sentence that quotes and disclaims it.

---

## 6. The four Bv3 advisories

Accounted individually, original severities and limits preserved. None erased,
none promoted to a blocker.

- **ADV-1 — valid limitation, carried.** Pin-ledger completeness is a *host*
  obligation under the exclusive purge lease; a closed schema cannot express "this
  set is all of them". The contract says so itself.
- **ADV-2 — valid limitation, carried.** The confinement truth-table join is a
  host act; schema validity must not be read as an enforcement claim.
- **ADV-3 — addressed.** The matrix now publishes an explicit `inventory`
  capability naming exactly `(file, enumerated)`, `(package, manifest-declared)`
  and `(vcs-change, vcs-reported)`. This advisory related to MUST-3 and moved with
  it: the matrix grew from 60 to 66 cells.
- **ADV-4 — open, carried, and refined below.** The 723-byte illustration is
  still stated as a flat constant.

---

## 7. New findings

**New MUST issues: none. New SHOULD issues: none.**

Two new advisories, neither a blocker:

### CLAUDE-V13-ADV-1 — a stale count in `validation-summary.v1.json`

`native.matrixCells` records **60**; the matrix actually carries **66** cells
(57 + 6 + 3), and the generated native report and reference log both say 66. This
is genuine staleness *introduced by this delta*, not a value that was never right:
in v12 the summary claimed 60 against an actual 60 and agreed. MUST-3 added the
syntax-only mode, and although `validation-summary.v1.json` is itself one of the
36 modified files, this field was not updated. The root cause is that **nothing
joins the summary to the artifacts it summarises**, so the stale value survives a
full six-command PASS. Every other count in the file agrees exactly.

I classify this as an advisory rather than a SHOULD because it changes no
admission decision and no public output — two conforming implementations would
build identically — and the file's own standing is "REFERENCE EVIDENCE ONLY". I
record it prominently because it understates demonstrated native coverage in a
record cited as evidence for this review.

### CLAUDE-V13-ADV-2 — the 21-crate illustration can fall *under* its own limit

The contract states "twenty-one crates already produces 723 bytes of raw map,
against a maximum of 255." I measured it myself rather than adopting either
published number, and the advisory is stronger than recorded: with short crate
names (`c0..c20`) a 21-crate edition map canonicalises to **222 bytes — below the
255 maximum**. Medium names give 400; long names 946. So the number is not merely
name-dependent, and the crate count is not a threshold.

The **design conclusion is untouched and correct**: a map-valued component is not
representable under a `u8` length for ordinary valid inputs, which is exactly why
`languageVersion` is the raw 32 bytes of a SHA-256. This is motivational prose,
so it stays an advisory.

---

## 8. Preserved safeguards

Verified by exact diff plus **40** targeted probe cases aimed where the removals
could plausibly regress something. All 40 agree.

Confirmed independently: typed canonical equality including bool/int aliases
(`true≠1`, `false≠0`, nested `[true]≠[1]`, with positive controls); all thirteen
closed relation selectors resolve to distinct payload schemas; all three digest-law
limbs (raw payload where a frame is required refuses; an unregistered H domain
refuses; `SHA256(C(X))` is never `H(D,X)`; one descriptor under two domains gives
two identities); **no global ordering of unrelated relation rungs** survives; JS
body language through a TS universe closes and mints a different Run; raw-32
`derived` dialect encoding on all three universes with the clone-preimage language
enum still closed to three; and monotonic missingness under RC-2 — not-attempted,
non-exhaustive, partial and absent stage terminals are never `complete`, an
admitted unresolved edge *inside* the examined partition blocks `complete` while
one outside it does not, and an unresolved rung is `not-applicable`.

Registered-schema mutations were treated as tests of the schema/reference law, not
as attacks on unmodified closed payloads.

*Evidence limit, stated rather than glossed:* a number of listed safeguards —
TS `node_modules`/config/layout/ordered repeats/jsconfig, L0 versus L1–L3 custody,
Rust edition override and `#` paths and same-physical-file selections, cache
validated-hit boundary, mutation versus repair replay, purge disclosure,
required-output failure after commit, leased pin ledger versus pure projection,
reference cycles and annotation traversal — are exercised by the six suites I
reproduced byte-identically (3740+ checks) rather than by probes I authored
myself.

---

## 9. Scope dispositions

- **16 AR** — all `CARRIED-UNCHANGED`. Field-level diff shows all 16 rows differ
  **only** in review-provenance pointers; obligation, selector, contract, unit,
  ownerRows and evidence are byte-identical. AR-15 additionally advanced its
  `status`. No AR obligation was discharged by this delta, and this review
  discharges none.
- **15 FW** — all `CARRIED-UNCHANGED`. All 15 live in
  `current-source-map.proposed.md`, which is **byte-identical** v12→v13 and absent
  from the modified set.
- **27 inherited residuals** (DR-001…DR-011 and DR-011-R01…R16) — each
  individually keyed, all `CARRIED-UNCHANGED`, basis: the three source files are
  byte-identical and absent from the modified set. Preservation is **not** a new
  discharge and none is closed.
- **30 evaluation subresiduals** — `CARRIED-UNCHANGED`; the file is byte-identical
  and its own standing is that it closes nothing before review/application.
- **5 scoped DR-201…DR-205** — `ROUTING-ASSESSED-ONLY-NOT-APPLIED`. They are
  carried on AR-15, whose only substantive change is its status string. **These
  five routing assessments do not alone grant their final application outcomes;**
  the separate full application review must grade them.
- **32 product qualification gates** — independently enumerated: 32 items, all
  three booleans false on **every** one. `ALL-32-REMAIN-UNDEMONSTRATED`. This
  review demonstrates none.

Application and readiness records intentionally remain unapplied. D371/D372's one
complete product in stages, supported TS/JS/Rust on the four named macOS/Linux
machine families, is unchanged; I invented no implicit tool execution, untrusted
ecosystem, full Map application or bundled semantic model.

---

## 10. My own harness errors

Ten, all corrected and retained rather than hidden, because several of them are
the reason the probes are trustworthy. The most instructive:

- I read the inherited ladders from the wrong registry path, and parsed `LADDERS`
  as a literal when it is a **dict comprehension** — i.e. derived from the
  authority, which is stronger than the mirror the prose claims. Failed attempt 1
  retained at `evidence/p1-ladder-authority.FAILED-ATTEMPT-1.json`.
- I expected a weak-rung control to admit while leaving a forbidden field present.
  The design correctly refused; **my expectation was wrong**.
- My first cross-relation cases died at `PAYLOAD_RECORD` before reaching the
  ladder guard — a pass I had not earned, fixed by supplying valid payloads.
- In the evidenceUse probe, three successive upstream joins masked the guard under
  test until isolated.
- Twice — SHOULD-3 and `RES_ORDER` — naive substring matching flagged text that
  turned out to be a sentence *quoting and disclaiming* the defect it fixed.

None of these is a defect of the subject.

---

## 11. Limitations

Every native, compiler, OS, cryptographic and storage observation in this kit
remains a **synthetic assumption**, never measured enforcement. I exercised the
subject's own models as the system under test, so passing my probes shows the
design behaves as specified under *my* reading of the contracts. A constructor
refusing to build a graph (`FIXTURE_NO_ADMISSIBLE_PAYLOAD` for data-grammar clone
facts) is **not** evidence that admission would reject it — the subject records
that limit itself and I preserve it. I did not re-derive the inherited
`fact-plane.v1`, `delivery.v4` or security truth-table artifacts; I verified their
pinned digests and read the cited sections. The per-finding evidence limits are
stated in §4 and in `review.json`.

---

## 12. What this ACCEPT is not

It grants **no** readiness change, **no** application acceptance, **no** product
qualification and **no** implementation authorization. It closes no inherited
residual and elevates none. It does not grant the five scoped owner decisions
their final application outcomes. It does **not** substitute for the NEW blind
consumer review on these newly accepted normative bytes, nor for the separate
full application review — both remain distinct gates, and neither is a reason to
reject otherwise coherent pending design records.

**Required next acts:** a new blind consumer review; the complete independently
reviewed application and readiness reconciliation; substantive Codex agreement
with this assessment before any implementation. Optionally, and not blocking:
correct `native.matrixCells` to 66 and qualify the 21-crate illustration.

---

## 13. Substantive assessment

This revision does what the blind reviewer predicted it would need to do, and it
does it in the right way. Four of the five MUST findings were *closure* failures
at seams between documents that each got their own side right, and the fix in
every case was to make one document the authority and have the others **derive**
from it rather than restate it. The ladder is the clearest instance: two of the
three former copies are now computed by reading the authority at import time, so
they cannot drift at all, and the single remaining copy is checked exactly and in
order. That is a better answer than a stricter drift test.

The parts I probed hardest held. The empty-table bypass is genuinely closed at Run
admission with positive controls on both sides. The evidenceUse obligation now
fires at the retained Run boundary and not only at policy admission, which is what
made the old defect a real one-document-two-answers divergence. The `syntax-only`
universe is the most substantial addition and it resists the obvious attacks: it
does not widen semantic capability, it refuses to fabricate a tokenisation law it
has not published, its `syntaxClass` is registry-decided rather than
caller-selected, and its clone identity binds to the grammar that actually read
the body rather than to an invented compiler.

What I find most persuasive is not any single guard but the pattern in the
removals. Each deleted line is replaced by prose naming the defect it was — the
`and row['rungs']` conflation, the `RES_ORDER` tie between `external` and
`resolved`, the ownership cause that nothing derived and nothing compared. A
revision that documents its own former errors that precisely is one whose
remaining claims are easier to trust, and it is why my two advisories are about a
stale summary count and an over-confident illustration rather than about anything
load-bearing.

The design is coherent, the corrections are real and verified at the boundaries
that matter, and nothing I could construct broke them. Zero unresolved MUST, zero
unresolved SHOULD: **ACCEPT**, with the two advisories recorded above and every
downstream gate still open.

---

## 14. Artifacts

| Path | Contents |
|---|---|
| `review.md` | this review |
| `review.json` | structured verdict, dispositions, `newMustIssues` (empty), `newShouldIssues` (empty), `newAdvisories` |
| `evidence/integrity-before.json`, `integrity-after.json` | frozen-subject custody, both phases |
| `evidence/integrity-copy-prerun.json`, `integrity-copy-postrun.json` | disposable copy delta custody |
| `evidence/delta-v12-v13.json` | recomputed exact delta |
| `evidence/p0-pins-prerun.json` | 1308 transitive pins verified before running |
| `evidence/p1…p8*.json` | 286 probe cases, including the retained failed first attempt |
| `probes/*.py` | 14 independently authored probes |
| `logs/*.log` | my six reference command logs (byte-identical to retained) |
| `work/subject-copy` | disposable full copy, verified clean before and after |
