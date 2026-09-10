# Independent review — frozen candidate subject v21

**Subject manifest SHA256:** `360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`
**Verdict: ACCEPT** — no unresolved MUST, no unresolved SHOULD, one new advisory.

This is a fresh independent review by actual Claude. I authored none of this subject.
Nothing here applies a correction, activates readiness, grants an application outcome or
qualifies a product. Machine-readable form and the full ID-keyed disposition maps are in
`review.json`; probes, logs, mutated bytes and copy deltas are retained beside it.

## 1. Custody verified before and after

The declared manifest hash matched the file on disk. I then verified every declared hash
and length rather than sampling: 12,212 of 12,212 files, exact `totalBytes` of 716,986,273,
zero missing, zero extra on disk, zero mismatches — and I re-ran the identical sweep after
all execution and mutation work, with the same result. The frozen subject was never written to.

The protected-history custody block declares 31 files. All 31 are in the subject with
manifest-, snapshot- and live-source-equal hashes; exactly 10 carry
`presentInPredecessor: true` and 21 do not, which is precisely the "20 contained 10; 21
outside, verified live then" account, and live drift is zero for all 31. The custody
`sourceRecord` is itself in the manifest and hash-equal.

There are four source-pin ledgers, not five, and I verified all 1,312 pins (foundation
1100, native 72, security 74, workflows 66) against both the snapshot and the live tree,
before and after. All clean, twice.

## 2. Reading the design first

Before touching any author finding I read all five product contracts and their index in
full, in bounded consecutive ranges with no skipped or truncated range: 7,729 lines across
six files. `contract-read-coverage.json` records each exact path, its hash (agreeing with
the manifest), its total line count and the observed read ranges, and asserts contiguity
from line 1 to end for every file. I did not substitute searches, hashes or a manifest for
reading the design. That record is the discharge of ROOT-V20-REVIEW-SCOPE's first half.

## 3. What source 21 actually changes

I recomputed the v20→v21 delta from the two manifests rather than reading the assessment's
account: 280 files added, 0 removed, 15 changed. Of the 15, exactly **three** are
executable — `foundation/run-reference-checks.py`, `foundation/check-identity.py`,
`workflows/workflows_model.v1.py`. **Zero** schema documents changed. **Zero** product
contract bytes changed; I hashed all six contract files under v20 and v21 and every one is
identical. The remaining twelve are consequential: the four ledgers repinned to exactly
those three files (the security and workflows ledgers additionally repin
`correction-crosswalk.proposed.json`), five regenerated reports, and three governance prose
files. So the "only three reference files" claim is accurate for executables, and my
substantive scope is correctly the whole source-20 design, which these bytes carry unchanged.

## 4. The six canonical commands, reproduced

I made a disposable **full** copy of the frozen subject — 12,212 files, verified byte-exact
against the manifest, with the ledgers left **unrepinned** — and executed all six canonical
commands from `final-reference.v21/reference-checks.json` there, with the foundation outer
timeout at 3600s (inner 600s per child, owned by the launcher) and 600s for the rest.

All six exited 0. Every declared `sourceSha256` matched the file actually executed. No
orchestration timeout occurred, so no partial-failure record was needed, though the
orchestrator was written to preserve one and flushes after every command.

The result worth stating is the **copy delta: zero files changed, added or removed.** Every
regenerated report — foundation validation, identity, product quality, product
configuration, array order, security, native, workflows, workflow surface, integration — is
byte-identical to the frozen one. That is a real reproducibility property, not a passing
flag, and it is the strongest thing an executed check can honestly contribute here. It
remains evidence about a reference model over synthetic trusted inputs. A Python exit 0 is
not an assertion, and none of this qualifies a platform.

## 5. NEW-SHOULD-1, tested by mutating one law

The independent-20 SHOULD was that the old candidate-holder controls could not detect a
guard-order regression. I did not take the correction on trust and I did not copy the
algorithm. I called the **real owning entrypoint**,
`workflows_model.v1.verify_scope_parameter_binding`, with admitted positive data first.

On the frozen bytes, two positives verify and return the expected payload digest, and one
supplied non-candidate document gets three distinct answers by row multiplicity: zero rows
→ `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`, one row →
`BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`, two rows → `CONFIG.INVALID`.

I then mutated **exactly one law** in a disposable copy — moving the at-most-one ambiguity
guard below the payload-digest match — and re-called the same real entrypoint. Of seven
scenarios, exactly **one** changed: two rows plus a non-candidate document regressed from
`CONFIG.INVALID` to `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`. Both candidate-holder
scenarios were **unchanged**. That is the direct demonstration, on these bytes, that the
v20 controls could not have held the order, and that the position decides which true reason
a non-candidate caller is given rather than soundness — exactly as the model's own comment
now says.

Running `check-identity.py` against the mutated tree gave exit 1 and **1594 passed / 2
failed**, against a frozen baseline of **1596 / 0**. The two failures were precisely
`an-ambiguous-spec-refuses-as-ambiguous-even-for-a-document-that-is-neither-candidate` and
`the-three-answers-for-one-non-candidate-document-stay-distinct-by-row-multiplicity` — the
two the model names as order-holding. This independently reproduces the root-recorded
1594/2. The mutation copy delta was exactly one file. Mutated bytes, diff, log and report
are retained.

The removed control, `the-scope-ambiguity-detail-is-a-code-this-model-already-published`,
counted string occurrences in another file. It established nothing semantic and would have
broken on innocuous edits. Removing it while retaining the behavioural carrier and registry
controls is the right call.

I also tested the "workflow code unchanged apart from documentation" claim rather than
accepting it: the v20 and v21 ASTs are equal modulo docstrings, the docstring-stripped
compiled code objects are identical, exactly one function docstring changed
(`verify_scope_parameter_binding`), and the module docstring did not. Full code objects
*including* docstrings are not identical — which is expected, and which the root's own
qualification already states rather than overclaims.

The launcher change is correct as written: `CHILD_TIMEOUT_SECONDS = 600` is a fixed
constant rather than a flag or environment variable, `TimeoutExpired` is caught, the timed
out entry carries `exitCode: null` and `reportSha256: null`, `passed` is false, and the
report is a strict superset of the previous shape.

## 6. The cumulative source-20 laws

I inspected each changed law against the actual bytes and control flow, not against the
author's account of them. Full per-ID bases are in `review.json`; the load-bearing findings:

**One selected parameter per registered row** is enforced at three places, and the two that
must not drift genuinely share one function: `identity-model.admit_parameter_selection` is
called by `native_evidence_model.admit_analysis_spec` (the pre-Plan boundary, step 4) and by
`identity-model.open_run_closure` over the retained analysis spec. The third is the
independent workflow verifier. Zero stays legal, distinct registered rows coexist,
byte-identical duplicates refuse earlier on `uniqueItems` plus the canonical-set order law,
and unregistered or two-row-per-digest cases keep their own named refusals
(`PAYLOAD_PARAMETER_UNREGISTERED`, `PAYLOAD_PARAMETER_AMBIGUOUS_ROW`). The pre-Plan helper
is honest about its own history: it states that an earlier placement inside the vocabulary
helper made the analysis-spec-wide claim an overclaim.

**RC-6.** I counted the ladder authority myself: 13 relations, **17** registered
`(relation, rung)` pairs, 5 resolved and 12 not — the exact partition the contract asserts,
and the same 17 a control independently asserts. RC-6 is coded as an implication, not an
equality, so an honest `unknown` beside an exhaustive examination stays lawful in both
directions. It is decided in `coverage_bijection`, which the producer boundary calls and
which retained Run closure re-runs over the retained payload. Enumeration completeness and
resolution completeness stay distinct; RC-0 still outranks; RC-3's `complete` with
`incomplete` resolution remains lawful.

**Stage output domains.** Both arrays `$ref` a flat `#/$defs/Domain` whose 32 members equal
the `Ref.domain` enum and the `byDomain` key set exactly, so existing walkers resolve it.
Equality between the two arrays is separately enforced at closure by `equal_typed` →
`STAGE_SPEC_OUTPUT_DOMAIN_JOIN`. Empty is permitted and its own description denies
completeness, evidence and producer authority. `stage-spec.operation` stays a
provider-interface token with no platform-wide enum, in deliberate contrast to the closed
seven evaluator predicates.

**Closure membership** publishes exactly 6 direct, 2 equal-to-direct and 7
selected-through-other-input bindings, matching the claimed 6/2/7, with a `selectionLaw`
that explicitly refuses an exact-minimal-set reading and permits deliberate extra selections.

**Registered schema documents** carry the artifact class at *both* selectors — the
annotation on `view.schemaDigests` items and the `schema` proof-input-ref row in `byDomain`
— and the closed set is derived from the one payload registry with no second list to drift.
The view set stays a declaration, never a derived union and never admission authority.

**Baseline scope public details.** The closed registry and the mirrored `DomainDetailCode`
enum both hold 289 members and are set-equal; both `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`
and `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH` are registered, and they are the only two
`BASELINE.SCOPE_*` spellings — no third was invented for ambiguity, which correctly reuses
`CONFIG.INVALID`. I ran `adopt_baseline` for real: both refusals propagate with class, code
and detail intact and admit against the real `StepTermination` carrier and failure envelope.

The sentinel correction is substantively right and I confirmed its premise is reachable
rather than hypothetical: `adopt_baseline` really does raise
`Refusal('CONFIG.INVALID', None, 'duplicate fingerprint in baseline entries')`, so a
`.detail`-only projection genuinely could not distinguish refusal from return. The positive
uses a unique module-level object with an identity comparison, which distinguishes *any*
refusal. I additionally checked the adjacent risk — that a `detail=None` refusal might emit
an explicitly null `domainDetail`, which workflows §0 forbids — and it does not: the
optional field is omitted and the termination admits against the real schema.

**Import IDs.** The equality is code, not prose: any difference in either direction raises
`IMPORT_JOIN`, with the evaluated subset and citability kept separate by
`UNSELECTED_EVALUATION_IMPORT` and `HIDDEN_FINDING_EVIDENCE`.

## 7. The preserved complete design, read as a whole

Source 21 changes no contract byte, so my substantive scope is the whole source-20 design.
Reading it end to end rather than by selector, these are the axes I judged and what I found.

**Zero-config capabilities, discovery and configuration.** The default profile is fixed by
the matrix, not by a release: for each discovered unit it requests every capability whose
`(capability, mode)` cell is not `NOT-SELECTED`, including `UNSUPPORTED-TYPED` cells, which
are answered by disclosure rather than omitted. The corpus corrects its own earlier
subset-permission wording explicitly, and the absence route is delivered in the invocation
that selected it, on `CommandEnvelope.availability`, composed per step because 1024 is the
analysis-spec bound and not an invocation-wide one — two admitted selections of 1023 compose
2046 notices and none is dropped. The ownership tuple travels in typed fields rather than a
concatenated subject, with a stated reason: `workspaceRoot` is bounded at 4096 while
`BoundedText` is 1024, so concatenation could silently collapse two units. Configuration
resolution keeps all five sections always present, distinguishes an absent `entryPoints`
from an explicit `[]`, and separates semantic from operational digests. Discovery is one
shared rule consumed by both the security and native instruments rather than restated, with
pruning by exact path segment and a pruned tree recorded once with its hidden marker count.

**Native ownership and the clone progression.** The body-identity chain is the part I
scrutinised hardest because it is where a false equivalence would be most costly, and it
holds. `bodyIdentity` is a fully framed, domain-separated preimage; the double length prefix
at `L0-verbatim` is stated with a worked byte example and an explicit statement of which of
two grammatically available readings is admitted. Dialect is per language, closed and always
selected, with no null branch and no single-edition fast path — Cargo lets a target override
its package edition, so the ownership relation is required for every Rust clones fact and a
universe committing none admits no clone. `unitId` is `H` over a published four-field
preimage rather than a delimiter join, and the reason given is correct: the delimiter form
was injective only by forbidding `#` in a directory the path contract admits. Selected scope
and partial enumeration are held apart rather than collapsed, with partial refusing before
any row is read so incomplete discovery cannot act as an implicit edition selection. The
split between what a host recomputes at L0 and what is only retained custody at L1–L3 is
stated as custody-and-framing evidence, qualifying no parser and grading no tokenisation.

**Static, runtime, test, history and import evidence.** The two evidence planes are kept
genuinely disjoint: native fact relations carry `DeficiencyV2`, the two imported-evidence
relations carry their own vocabulary, the plane is decided at admission from registry
membership rather than from the value, and a cross-plane value is refused. The
fingerprint-to-subject projection for imported requirements publishes its granularity limit
— a runtime row without a symbol and every history row give file granularity, distinct
findings can project to one observation, and more than one matching subject refuses rather
than picking. "No hits is not non-use" is carried through: `observable-unhit` is bounded
negative evidence, `unobservable` and `unmapped` never become unhit signals, and one window
never establishes a universal negative. Imported evidence can be an additional required
condition but never by itself the closed-world basis for an unsafe `delete` or `replace`.

**Deterministic typed identities and closure.** The closing digest law admits no default —
an unannotated 64-hex field is inadmissible — which is stronger than the array law and is
what prevents a new field from silently inheriting a plausible rule. The four terminal
representations are closed, `by-domain` is correctly a selector rather than a fifth
terminal, and the H-frame admission is exact in both directions so a raw payload cannot be
offered where a frame is required or the reverse. Run closure re-runs the owning contract's
own admission over retained bytes rather than trusting a frame or an ADMIT flag, and it
re-executes nothing: no compiler, provider, repository or filesystem operation. Coverage
scope disjointness is decided at retained closure on the full owning tuple, with the
explicit acknowledgement that per-Coverage admission sees one scope and therefore cannot
decide a property holding between two.

**Changed code and baseline.** The comparison chain attributes each fingerprint to the first
axis at which it changes, requires the actual prior detector closure under current trust
rather than substituting B for E0, and makes a removed detector indeterminate rather than
silently clean. Fingerprint dual emission is stated to migrate identity only and never to
supply the prior algorithm. Audit profiles select gate semantics explicitly instead of
letting enum precedence decide a gate.

**Invocation, repair, replay and errors.** The step DAG and the derivation DAG are separated
so neither references the other. Repair preview, apply, verify and recover are separately
authorized, with the closed-world gate decided against the evidence Run's own record before
any descriptor is built, and the descriptor's five-field projection explicitly granting no
authority of its own. The recovery table is closed over journal state, and a target that is
neither preimage nor postimage blocks rather than guessing. Cache key construction and cache
hit admission are correctly two different acts, only the second being an admission.

**Authorization and availability.** Grant admission is operational and precedes any Plan; a
test-runner grant contributes no Plan principal, and prepared availability never implies
that this host held a grant. Confinement is never claimed anywhere, effect values are copied
from the pinned truth table per execution mode, and the one token whose value would
over-claim is deliberately unprojected. Sealed assurance and current availability are kept
as separate records so a retention decision never rewrites a verdict.

Across all of these the pattern I kept meeting is the one that matters for a design of this
kind: where the corpus cannot establish something, it says so and names the boundary,
rather than narrowing the claim quietly. I looked for the opposite pattern and did not find
an instance I could turn into a counterexample.

## 8. One new advisory

**V21-CL-ADV-1 — a timed-out reference child leaves the previous run's per-script report on
disk under the same name.** `run-reference-checks.py` never clears the target report before
spawning. If `check-identity.py` exceeded its budget, the launcher would correctly record
`timedOut: true`, `exitCode: null`, `reportSha256: null` and `passed: false` — but
`foundation/identity-report.json` from an earlier successful run would still be sitting
there carrying its own `passed: 1596, failed: 0`, indistinguishable by inspection of that
file alone.

I am deliberately filing this as advisory rather than SHOULD. The launcher's own report is
honest, its docstring states this exact hazard verbatim, and I searched every `.py` in the
corpus outside `reviews/`: the only consumer of those five report filenames is the launcher
itself, so nothing inside the reviewed corpus can be misled. The exposure is to an external
or human reader, or to a future application step reading a per-script report directly. The
remedy is cheap — unlink the target with `missing_ok` before each spawn, or write each run
into a fresh report directory — and it would make "no completed result is attributed" and
"no stale bytes are present" coincide instead of depending on the reader consulting the
launcher report.

## 9. Prior findings, governance, and what this review does not do

All 13 source-20 finding IDs are disposed individually in `review.json` by ID — CB-GAP-1
through CB-GAP-5, CX-V20-SCHEMA-REGISTRATION, CX-V20-STAGE-REF-COMPATIBILITY, V20-ROOT-3,
V20-ROOT-4, V20-ROOT-5, CX-V20-SENTINEL-SUCCESS, CX-V20-FINAL-FIXTURE and
CX-V20-REVIEW-PRECISION — together with NEW-SHOULD-1, ROOT-V20-REVIEW-SCOPE, CB-ADV-1
through CB-ADV-4, and the five current advisory accounts (V20-ADV-1/2/3 and
V21-FINAL-PEER-ADVISORY-NEW-1/2). CB-ADV-4 is carried as a live open cross-unit obligation,
not closed: the selected composition adds `faultCause: host-invariant` under the existing
`SYSTEM.OUTCOME.ILLEGAL_STATE` while `d9-exit-contract.v1.14.json` keeps its bytes, so a
checker reading the inherited artifact alone would refuse a lawful termination. Publishing
the successor artifact rather than repinning history is the right choice; application must
reconcile it.

Governance counts were recomputed from the frozen bytes rather than taken from a label:
16 AR rows (AR-01..16), 15 FW rows (FW-01..15), 27 inherited residuals (DR-001..011 plus
DR-011-R01..R16), 30 evaluation residuals (RES-EP13-01..30), 5 scoped review owners
(DR-201..205) and 32 unperformed gates (DR-G01..G32). Each set is disposed by ID in
`review.json`. Carry-forward and routing are not a fresh readiness grade, and I have not
treated them as one: DR-201..205 carry `appliedByThisReview: false` and
`finalApplicationOutcomeGranted: false`, because the register itself records the 28 affected
V2 rows and DR-201–205 as OPEN for full-product integration against the newly selected
capability set, whatever their historical architecture-preview acceptance. No residual is
CLOSED by this review; DR-011-R10 in particular cannot be closed by a proposed table and
needs the fresh blind reconstruction.

Every qualification flag is false. D-372 is unapplied. Readiness condition 5 is NOT MET —
the register measures it as such and nothing here changes it. A new blind 9 complete
semantic proof reconstruction and a separately, independently reviewed complete application
follow source acceptance; this review performs neither and claims neither.

The limits of what I established should be read as strictly as the corpus states its own.
I read design bytes and executed design-reference checks over synthetic trusted inputs. I
established no product qualification, no compiler or OS enforcement, no confinement and no
complete semantic proof replay. Closure admission is not proof replay. The 17-pair RC-6
sweep is helper-level by construction; sealed-Run RC-6 coverage is the narrower named
`file@enumerated` vectors in both minting universes, exactly as those controls label
themselves, and I have not counted twelve helper cells as twelve sealed-Run tests. Where I
report a schema or literal observation I say so, and I do not equate it with execution
security. My environment was `/tmp/opensip-architecture-review-env`, which is its own
measured environment and not the documented root one.

**ACCEPT** is my substantive judgement on these exact bytes, not deference to the coauthor
assent, which is explicitly bounded and not independent acceptance. The one SHOULD returned
by independent 20 is closed by evidence I produced by mutating the real admission, and the
three advisories are addressed and verified. I found no counterexample, owning selector and
first failing boundary that would support a new MUST or SHOULD, and I have not manufactured
one to appear rigorous.
