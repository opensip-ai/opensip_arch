# Author review v2 — repair closed-world selection: ownership census and display law

**Standing: AUTHOR_PENDING_REVIEW.** Source coauthor, not an acceptor. **No author acceptance
and no root agreement is claimed for any byte written this turn.** No final design, blind or
application acceptance comes from this origin. No consumer output was supplied or read. No
product implementation, no commit, no push. My v1 source/runtime/handoff and the independent
review are preserved unedited.

Corrections to my earlier claims, and the scope correction to the independent report, are in
`assessment-corrections.md`.

---

## 1. Input custody, verified before authoring

`repair-selection-successor.v2/input-custody.json` declares 1354 files copied from my completed
v1 handoff source. Verified independently (`probes/v2-source-baseline.json`):

```
custody declares 1354 | v2 tree 1354 | mismatches 0 | extra 0 | missing 0
v2 vs v1 source: 1354 files, 0 differ, 0 only-in-v1
all 8 v1 changed files carry their v1 AFTER hashes into v2: True
```

## 2. What changed, and why

### RRS-A1 — ownership is the retained selected-program census

The previous law read only source-path Coverage scopes. It now reads the **retained
`EnumerationPlanV1`**, reached through guaranteed retained joins:
`run3 → plan2 → analysisSpecDigest → parameters`, selecting the entry whose `schemaDigest`
resolves through the identity owner's **own** `parameter_row_of` to
`foundation/enumeration-plan.schema.v1.json`. That parameter is **required** for evaluator3 and
re-admitted by full replay, so this is guaranteed retained evidence — not a caller-selected map,
not an optional unsigned sidecar, not filename parsing.

| binding | treatment |
|---|---|
| `selected`, universe non-null, census contains the path | contributes that **universe** |
| `selected`, universe **null**, retained extent contains the path | **typed unresolved ownership**; does not vanish behind a closed owner |
| `unselected` | **never inferred** as an owner |

A binding's **applicable path census** is its own `extents[]` per kind plus
`candidateSourcePaths`. Each kind is read as itself — `file`/`package` are host membership
extents, `symbol` is the selected program's **code** scope — so all snapshot files are not
treated as every compiler's `programRootFiles`, and a selected program whose census lacks the
edit **stays unrelated**. Multiple ownership is preserved. Source-path scopes remain as an
**additional witness** whose redundancy is now **measured** (`witnessOnlyUniverses`).

### RRS-A2 — display and remedy

Sentinel stated exactly as `{false, unknown, none, present, unknown}` and called a **display
sentinel**, never "all-unknown"; **no member authoritative**, boolean included; **absence folded
into the reduction** so the display cannot read closed while eligibility is refused; ordering
published as **UTF-8 bytes** over the **six** members; remedies name **all six unabbreviated**
including the `coverage2` identity. `dynamicDispatch` stays out of the gate and keeps its
target-relative role; recipe trust, policy consent, current-snapshot equality and the
authorization bound to the exact `repairPlanId` remain separately required; preview authorizes
nothing.

## 3. The decisive evidence

**Reachability, at the enumeration owner's own admission** (`probes/symbol-only-admission.json`;
enumeration-owner admission, **not** a full Run): symbol-only selected available universe →
**ADMIT**; unavailable selected binding retaining the path → **ADMIT**; candidate-only
`candidateSourcePaths` → **ADMIT**.

**A full admitted asymmetric Run**, which root had not claimed and told me not to claim without
executing:

```
run3:896bef61cbe9969d20ccd93d7948ffbee2cedb747eb0ebf633584f96aaf1e63d  (close_run ADMIT)
  17ce4077e6  inventory cell only, file extent, file@enumerated scope, eligible true
  03bbcc3284  syntax cell only, symbol extent ['src/index.ts'],
              scopes: declares / literal / control-flow — NO source-path scope,
              declares Coverage eligible FALSE
  source-path-only owners : ['17ce4077e6']   -> old law admits the delete
  census owners           : both             -> refused, naming the declares record
```

Also verified on that same Run: an unrelated path is typed unresolved; `README.md` (in the file
extent, not in the symbol program's extent) leaves the symbol program **unrelated** and the plan
eligible — so the file extent is not being read as the symbol program's extent.

## 4. Changed files

Nine files. Before-images for all nine are in `before-images/`; exact digests in
`changed-file-handoff.json`. **1354 → 1354 files, 0 undeclared changes, 0 unexpected new files,
0 missing.**

| path | before → after |
|---|---|
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | 103763 → 107738 |
| `docs/v2/contracts/product-v1/native-evidence.md` | 278061 → 278434 |
| `…/workflows/schemas/repair.schema.json` | 54967 → 57156 |
| `…/workflows/schemas/evaluator3/repair.schema.json` | 56494 → 58683 |
| `…/workflows/workflows_model.v1.py` | 141944 → 142287 |
| `…/workflows/workflows_model.v3.py` | 5453 → 5765 |
| `…/workflows/repair_closed_world_selection.v1.py` | 19329 → 32990 |
| `…/workflows/check-workflow-projection.v3.py` | 157925 → 174272 |
| **`…/foundation/evaluator_graph_fixture.v3.py`** *(separate entry)* | 23665 → 25847 |

**The fixture is the authorized bounded extension, tracked as its own handoff category.** It
adds one **default-off** keyword, `symbol_only_second_program`, plus the required-native pair
split that keyword needs. No default changed: with it unset the baseline Run is still
`run3:fbc6cee4…`, bit-identical. I did **not** change identity or native admission to make
anything pass, and altered no unrelated fixture default.

Both schema edits touch **only**
`$defs/RepairPlanDescriptor/properties/closedWorld/description`, proven by re-parsing each
document, blanking that one annotation, and requiring the remainder byte-identical. Annotation
**bytes do change**; no field shape, member set, key order or major does.

## 5. Lanes executed

Once, after changes settled. Full `stdout`/`stderr`/exit receipts in `probes/receipts/`;
summary in `lane-results.json`.

| lane | outcome |
|---|---|
| `check-workflow-projection.v3.py` *(changed)* | **PASS 458/458**, incl. **69 `repair-cw`** |
| `check_workflows.v1.py` *(changed seam)* | PASS |
| `check-replay.v3.py` *(fixture regression)* | PASS |
| `check-semantic-replay.v3.py` | PASS |
| `check-execution-replay.v3.py` | PASS |
| `check-enumeration.v1.py` *(enumeration owner untouched)* | PASS |
| `check-identity.py` | PASS |
| `check-integration.py` | PASS |
| `native/check_native_evidence.v2.py` | **exit 2 — see below** |

**Native lane, stated precisely.** It **stopped at pin admission**. It reported `sha256`
**pin mismatches** on exactly the nine changed files and **did not execute its subsequent
semantic checks**. **The absence of reported semantic faults is not evidence that those checks
passed.** Root assesses the sealed integrated run.

**Pin ledgers** (I edited none; root seals them). Five exist; three carry entries:

| ledger | pinned | broken by me | new module not yet pinned |
|---|---|---|---|
| `foundation/evaluator3-source-pins.v1.json` | 1242 | 8 | yes |
| `foundation/source-pins.v1.json` | 1238 | 8 | yes |
| `workflows/source-pins.v1.json` | 1238 | 8 | yes |
| `native/source-pins.v2.json` | 0 | — | — |
| `security/source-pins.v1.json` | 0 | — | — |

One generated source report, `native/native-evidence-report.v2.json`, was rewritten by running
that lane in-tree. It is **preserved** at `probes/preserved-source-reports/` and its original
bytes restored, which is why the handoff shows 0 undeclared changes.

## 6. Controls — which are full-Run, which are UNIT

**Full admitted Run** (built by the fixture, admitted at `admit_coverage_result_v3`, closed by
`close_run`'s complete semantic replay, and — for the asymmetric one — also driven through the
current evaluator3 preview): the positive; the conflicting negative; the **asymmetric
selected-program** control and its four companions; requirement-omission-does-not-bypass;
selection-independent-of-requirements; create-only; multi-universe same fingerprint; multi-owner
path; `dynamicDispatch` present is not a veto; evaluator3 refuses a caller-selected record;
witness redundancy measured.

**UNIT**, labelled in their ids, over constructed views or plans: relevant-universe-without-
Coverage; unrelated-universe-does-not-join; unrelated-open-universe-does-not-veto; relevance-on-
`sourceUniverse`-only; missing-subject-record-refuses-typed; **unavailable-binding-does-not-
vanish**; **unselected-binding-never-inferred**; **candidateSourcePaths-are-a-census**;
**multiple-owners-all-must-be-eligible**.

The last four are UNIT because the frozen fixture builds no unavailable, unselected or
candidate-only binding. Their **admissibility** was confirmed separately against the enumeration
owner's own `admit_enumeration`; that is an enumeration-owner admission, **not** a full Run, and
neither the module nor the controls claim otherwise.

## 7. Unexecuted boundaries and limits

1. **No native producer qualification.** Every `ClosedWorldV2` is a synthetic observation minted
   by the native owner's own `closed_world_v2`. No compiler, provider, enumerator or repository
   read was exercised.
2. **No apply, recover or verify**, and no exercise of the security authorization path. Preview
   only.
3. **No Rust or TypeScript universe.** Only the fixture's two syntax universes. Rust
   `sourceUnitOwnership` multi-target ownership is covered **by rule, not by execution**.
4. **Unavailable / unselected / candidate-only bindings were not built into a full Run** — UNIT
   controls plus a separate enumeration-owner admission probe.
5. **`vcs-change` and `clones` were never exercised as actual witnesses**; every witness in the
   controls came from `file@enumerated`.
6. **The imported plane is excluded structurally, not by test** — only native `coverage2`
   records are selected.
7. **Pin ledgers not updated**, deliberately; hence the native lane's pin stop.
8. **The native lane's semantic checks did not run** (§5). No claim is made about them.
9. **No identity or native admission change was made to make anything pass**, and no
   identity/native schema field shape, native model, security, unrelated contract, planning
   inventory, readiness or application record was touched.
10. **Root's separate glob source was not read or overwritten.**

## 8. Open questions for root

1. Whether the fixture extension should live in the fixture at all, or whether the asymmetric
   graph belongs in a workflows-local fixture. I put it in the fixture because that is where
   `build_file_inputs` composes the enumeration plan, inventories and scopes together; splitting
   it would have duplicated all three.
2. Whether the four UNIT binding controls should become full-Run controls, which needs fixture
   support for unavailable/candidate-only bindings that does not exist today.
3. Pin sealing for the nine changed files plus adding `repair_closed_world_selection.v1.py` to
   the three populated ledgers.
