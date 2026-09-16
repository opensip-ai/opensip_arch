# Author review — repair closed-world selection law

**Standing: AUTHOR_PENDING_REVIEW.** I am a **source coauthor** on this turn, not an
independent acceptor. **No author acceptance and no root agreement is claimed for any byte I
wrote.** This origin supplies no final design, blind or application acceptance. No consumer
output was provided, read or sought. Nothing here qualifies a native producer, a compiler, a
provider or a repository read, and nothing here is a full product repair.

My prior assessment and its probes remain unedited at
`/tmp/opensip-design-corrections/claude-repair-selection-assessment.v1/`. Where that report
overclaimed, the corrections are in `assessment-corrections.md` — all eight root points, plus
two I raised myself.

---

## 1. Input custody, verified before authoring

`repair-selection-successor.v1/input-custody.json` records `copiedFiles: 1353` and parent
manifest `ca713db5…fc95b5`. I did not take that on trust: I hashed **all 1353** author-source
files and compared each to `candidate-subject.v31`.

```
authorFiles 1353 | custodyClaim 1353 | notInFrozen31 0 | differFromFrozen31 0 | exactMatches 1353
```

That baseline (`probes/author-source-baseline.json`) is what every later "changed / unchanged"
statement is measured against. Frozen31 and my old assessment were read-only throughout; the
root mutable combined source was never touched.

## 2. What the law is

`ClosedWorldV2` is a required member of `ViewEntryV3`, so a Run retains **one per Coverage
entry** keyed by `CoverageKeyV2`. The authored law says which entries the unsafe gate reads.

**RS-1 — unsafe set.** Every `delete` and every `replace`, unqualified. Any one activates the
gate. `targets` and `edits` are separate descriptor arrays with **no published
correspondence**, and no target-to-edit pointer is invented: each array is read on its own
terms.

**RS-2 — relevant universes**, the union of two published retained joins:

* every universe reached by **all matching occurrences of every target fingerprint**
  (`finding3.subjectId` → `subject3.universe`). Not a representative: the `finding-key2` frame
  carries no universe, and the projection law that groups occurrences compares `ruleId`,
  subject path, kind, qualified name and detector closure but **not** universe;
* every universe that **owns an unsafe edited path**, from retained subject scopes of the
  `source-path` relations — `file`, `clones`, `vcs-change` — whose `subjects` *are* snapshot
  paths by the registry's `subjectKindLaw`. All three are `universeRule: same-only`, so
  `sourceUniverse` and `targetUniverse` coincide and **no cross-universe join is left
  implicit**. Never a path prefix, display string, sidecar, unreferenced host observation, or
  a `symbol`-kind scope — the same law states symbol-to-path attribution "is NOT re-derivable
  from the retained Run" and that inventing it "would be fabricated evidence". **Multiple
  ownership is preserved**: one path under two Rust targets or editions is two
  `sourceUniverse` values and both must be eligible.

A universe in neither set is **truly unrelated and does not veto**. That scoping is precisely
what stops an unrelated closed finding from justifying a delete in an open universe. An unsafe
path with no owning scope is `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` — typed, not guessed, not
vacuous.

**RS-3 — selected records.** For every relevant universe, **every** retained native
`coverage2` whose scope's **`sourceUniverse`** is that universe. Source-vs-target is stated,
not implied: `ClosedWorldV2` characterises the universe whose subjects were examined, and
`coverageTotality.matchLaw` calls totality "a claim about what THIS universe examined" — the
scope's source side. An entry made in an unrelated universe *about* a relevant one describes
the unrelated universe and is not joined. Selection is **independent of
`evidenceRequirements`**, so a recipe can neither pick a favourable relation/rung nor drop a
conflicting record. Dedupe by retained `coverage2` **identity**, never by relation; order by
the full partition key then that identity.

**RS-4 — the gate.** Non-vacuous conjunction of `deadCodeRepairEligible`. A relevant universe
with no retained native Coverage establishes no closed world — an empty subset is not truth.
`dynamicDispatch` is **not read at all**. Imported observations establish and improve nothing.

**RS-5 — the display summary.** Five fields, unchanged shape. `deadCodeRepairEligible` is the
conjunction; each other member takes the **least-closed** value present, and with nothing
selected the least-closed member of its own enum. It is a **display summary, not a native
producer record**, and never an input to the gate.

**RS-6 — create-only.** No gate, and ineligibility alone adds **no** unmet precondition — but
the summary is still built by the same reduction, so the descriptor and `repairPlanId` stay
deterministic even with zero native Coverage.

**RS-7 — identity.** Shape and recipe unchanged; **values** and Run identity are what move.
No `repairPlanId` equality is claimed across different Runs.

### One enum choice I had to make, and am flagging

`ClosedWorldV2.nonliteralLoading` is `none|present` — it has **no `unknown` member**. Under
one uniform least-closed rule the empty-evidence value is therefore `present`. That is a
display convention, **not** an observation that nonliteral loading was seen; the authoritative
part of that record is `deadCodeRepairEligible: false`. The alternative — widening the native
enum — is a `ClosedWorldV2` field-shape change I do **not** own and did **not** make. If root
prefers a different convention this is the one line to change.

## 3. Changed files

Eight files; before-images of all seven edits are in `before-images/`, each verified equal to
its frozen31 byte-image. Exact digests in `changed-file-handoff.json`.

| path | change | before → after bytes |
|---|---|---|
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | edited | 96452 → 103763 |
| `docs/v2/contracts/product-v1/native-evidence.md` | edited | 276962 → 278061 |
| `…/workflows/schemas/repair.schema.json` | edited | 52576 → 54967 |
| `…/workflows/schemas/evaluator3/repair.schema.json` | edited | 54099 → 56494 |
| `…/workflows/workflows_model.v1.py` | edited | 139660 → 141944 |
| `…/workflows/workflows_model.v3.py` | edited | 3305 → 5453 |
| `…/workflows/check-workflow-projection.v3.py` | edited | 131058 → 157925 |
| `…/workflows/repair_closed_world_selection.v1.py` | **created** | — → 19329 |

`1353 → 1354` files, **0 undeclared changes, 0 missing**.

Both schema edits touch **only**
`$defs/RepairPlanDescriptor/properties/closedWorld/description`. The patch asserts this by
re-parsing both documents, blanking that one annotation in each, and requiring the rest to be
identical — so no field shape, member set, key order or major moved. Per root's point 6 I
state plainly that **annotation bytes did change**; "no schema byte moves" would have been
false.

`workflows_model.v1.py` keeps its historical behaviour exactly: `CLOSED_WORLD_SELECTOR` defaults
to `None` and the old path is byte-equivalent in behaviour. `workflows_model.v3.py`, the
evaluator3 profile, **installs the new owner explicitly** on its own private module instance,
so no other loader of the v1 model is affected.

## 4. Lanes actually executed

All under `/tmp/opensip-architecture-review-env/bin/python -I -B`. Exact commands in
`lane-results.json`.

| lane | outcome |
|---|---|
| `check-workflow-projection.v3.py` (hosts the new section) | **PASS, 432/432**, incl. **43 new `repair-cw`** |
| `check_workflows.v1.py` (historical major-1) | **PASS, 1803/1803** |
| `check-query-projection.v3.py` | PASS |
| `check-comparison-knowledge.v3.py` | PASS |
| `check-integration.py` | PASS, 412/0 |
| `foundation/check-identity.py` | PASS, 1596/0 |
| `foundation/check-atoms.v1.py` | PASS |
| `foundation/check-replay.v3.py` | PASS |
| `native/check_native_evidence.v2.py` | **exit 2 — pin-only** |

The native lane's exit 2 is **entirely** `sha256 mismatch` on exactly my seven edited files —
`distinctFaultKinds == ['sha256 mismatch']`, zero semantic faults, and it exits 0 on frozen31
(`probes/native-lane-detail.json`). Root re-seals pins.

**Pin ledgers my edits invalidate** (I did not edit any of them — root's to seal):
`foundation/evaluator3-source-pins.v1.json` (7), `foundation/source-pins.v1.json` (7),
`workflows/source-pins.v1.json` (7). The new module is in none of them and needs adding.

**One side effect I caused and reverted.** Running `check_native_evidence.v2.py` in-tree made
it rewrite `native/native-evidence-report.v2.json`, a generated report root's ownership list
excludes. I restored it to its exact frozen31 bytes and the final handoff shows 0 undeclared
changes. Disclosing it because it happened, not because it survived.

## 5. Controls, and which are full-Run

Root required that at least one positive and the conflicting negative derive from a **full
admitted Run**. Both do. Each builds a graph, admits it at the native producer boundary inside
the fixture, and closes it through `identity-model.v3.close_run`, which runs the complete
evaluator3 semantic replay — then drives the **evaluator3** `repair_preview` from that closure.

**Full-admitted-Run controls.**

* `repair-cw-all-agreeing-entries-admit-the-unsafe-plan` — positive, over
  `run3:fbc6cee4…`.
* `repair-cw-one-dissenting-entry-defeats-the-unsafe-plan` — the conflicting negative, over
  `run3:a98f2b46…`, dissenting on `package@manifest-declared` in one universe.
* `repair-cw-requirement-omission-does-not-bypass-the-dissent` — the plan's only requirement
  names `imports`; the `package` dissent still defeats it. Root point 8, executed.
* `repair-cw-selection-is-independent-of-evidence-requirements` — a *different* requirement
  list selects the identical records.
* `repair-cw-create-only-is-not-failed-by-ineligibility-alone` — on the **same dissenting
  Run**: applicable, no unmet, and a deterministic summary and id.
* `repair-cw-one-fingerprint-matched-in-two-universes-contributes-both` — multi-universe same
  fingerprint, read off the admitted Run.
* `repair-cw-multi-owner-path-keeps-every-owning-universe` — multi-owner path.
* `repair-cw-dynamicdispatch-present-is-not-a-global-eligibility-veto` — every entry minted
  with `dynamicDispatch: present` by the native owner's own helper; neither gate nor summary
  moves.
* `repair-cw-evaluator3-refuses-a-caller-selected-record`.
* `repair-cw-subject-join-is-guaranteed-by-run-closure` — dropping `subject3` makes
  `close_run` refuse, so the target→universe join rests on guaranteed records.

**UNIT controls** — one published rule over a constructed view, **not** full-Run, and labelled
so in their ids: relevant-universe-without-coverage, unrelated-dissenting-universe-does-not-join,
unrelated-open-universe-does-not-veto, relevance-on-sourceUniverse-only,
missing-subject-record-refuses-typed.

**Why those five are UNIT, stated rather than hidden.** The frozen graph fixture gives both
universes *identical* extents and builds a Coverage for *every* scope. So a relevant universe
with no Coverage, and asymmetric ownership, cannot be produced from it without editing the
fixture — which is outside my ownership. I did not fake a full-Run label for them.

Also covered: create+unsafe activates the gate; the unsafe set is exactly `{delete, replace}`;
zero-coverage summary is the fixed published record; unowned unsafe path is typed and
non-vacuous; order-independence under reversed enumeration; order is the full partition key
then identity; dedupe by identity not relation; the gate reads seven-member records while the
display carries five; both descriptor majors keep their shape; identity recipe unchanged while
values move; **no equal-id claim across Runs**, with the single equality being identical
inputs over the *same* Run; preview is not authorization.

## 6. Unexecuted boundaries and limits

1. **Not executed: real native producer qualification.** Every `ClosedWorldV2` here is a
   synthetic producer observation minted by the native owner's own `closed_world_v2`. No
   compiler, provider, enumerator or repository read was exercised.
2. **Not executed: apply, recover or verify.** Only `repair-preview`, a Query-class step. The
   security authorization path is untouched and unexercised by me.
3. **Not executed: a Rust or TypeScript universe.** Only the fixture's two syntax universes.
   The multi-owner case I exercise is the fixture's shared path, *analogous to* but not an
   instance of Rust editions/targets. `SourceUnitOwnershipV1` is the record that would carry
   the real Rust case and I did not exercise it.
4. **Not executed: a full admitted Run with an uncovered relevant universe, or with
   asymmetric ownership.** UNIT controls only, for the fixture reason in §5.
5. **Not executed: `vcs-change` or `clones` as an actual path owner.** Both are in the
   `source-path` set by registry law and my rule admits them, but every owner in my controls
   came from `file@enumerated`.
6. **Not executed: the imported plane.** I assert imported observations contribute nothing
   because only native `coverage2` records are selected; that is structural, not a test.
7. **Pin ledgers not updated** — deliberately, they are root's. The native lane therefore
   exits 2 on pins alone.
8. **Not done: any native/identity schema field shape, the native model, security, unrelated
   contracts, planning inventories, readiness or application records.** The one place I felt
   ownership pressure is the `nonliteralLoading` enum in §2; I did **not** change it and
   flagged it instead.
9. **No product implementation, no git operation, no edit to frozen31, to my old assessment,
   or to the root mutable source.**

## 7. What I did not broaden into

I did not rewrite native sufficiency, product repair behaviour or any compiler tooling. I did
not carry out the adjacent `sufficiency_v2` relation-keying change my old report flagged, and
I withdrew the adjacent atom-model suggestion entirely (`assessment-corrections.md` §4). The
historical major-1 profile is preserved and labelled rather than corrected — but it is
preserved because root asked for labelled history, **not** to keep an example green: the one
place where a historical behaviour embodied the false presupposition is the seam, and the
current evaluator3 profile now selects the new owner there explicitly.

## 8. Open questions for root

1. The `nonliteralLoading` empty-summary convention (§2). The alternative needs a native enum
   change that is not mine.
2. Whether the five UNIT controls should become full-Run controls, which needs a fixture
   capable of asymmetric extents — a change outside my ownership.
3. Whether the new module belongs in the three pin ledgers root seals, and under which lane's
   `OWNED` list beyond the workflow-projection one I added it to.
