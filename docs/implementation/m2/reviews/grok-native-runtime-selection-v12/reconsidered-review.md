# Native-runtime selection v12 — reconsidered formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. Original `review.md` / `review.json` are **preserved** (`218b5bb6…a9d4` / 3267, `ae89f604…0b94` / 5628). Frozen subject unchanged.

**subjectManifestSha256** `ab5d4ee8f816c20a1c0e182a6e4a92c05062b0aef88db4b9ca470d2d2da80bae`  
`docs/implementation/m2/native-runtime-selection-v12-subject.json` **9904** bytes, 45 members.

## Original finding disposition — **withdrawn**

Original `requiredFindings[0]` `contract-parent-composition-not-in-accepted-set` treated `accepted` as lock `inputs` + inventory candidates + contract records. That is **not** what the live verifier uses.

Independently: unmodified `tools/verify_design.py` `verify()` (515–522) builds `effective` from **both** accepted `sourceManifest` and `applicationManifest`; `successor_chain` (267) starts `accepted = dict(effective)`, then adds selected inventory/contracts. Live `verify(..., design-lock.json, live product)` **passed**. Instrumenting only `contract_successor` to observe that map (14261 entries vs 46 lock inputs): all **three** frozen v12 parents satisfy 223–226 (`bytes`/`sha256` match).

`evaluator_composition_model.v3.py` **16980** / `cceeb42b…cbda` is in accepted `application-subject.v46.json` with `beforeSha256: null`. It is a legitimate parent. It is **not** dropped.

`inLiveLockInputs: false` remains true and is **not** the parent predicate. Not the same class as runtime-v2’s extra parent (that path was absent from **effective**).

## What this unit is

Composes frozen evaluation-budget-25 onto **current live 18/25** as **2 owned product inputs**. Inventory v20 is the selected inventory **candidate** (383 files, 20 packages). New evaluator `budgets.rs` + `lib.rs` export. No host-fixture / identity / policy / Cargo / schema / DAG / TCB change.

Does **not** implement full compose, atom scan, Run, or replay. Stage-meta reference `91cd4c58…9269` is **not** selected.

## Parents (all pass actual 223–226 on live effective map)

| Parent | Live class |
| --- | --- |
| `evaluator_composition_model.v3.py` `cceeb42b…cbda` | accepted application-manifest row (`beforeSha256: null`) |
| `native-runtime-selection-v11/successor.json` `4c70c1e3…d62b` | accepted contract record |
| `repository-file-inventory.v20.json` `321f3da7…f5a7` | accepted **inventory candidate** |

Parents sorted. Disk pins match. Inventory successor **record** is not a parent.

## Composition (unchanged from original independent checks)

Implementation **46924** / `255dcd50…5c3a`. Archive **2307061** / `91c46663…c1c7`. Export 258/258. Materialization **2/2**.

**243** non-lock product files byte-identical to frozen 25; only lock is live 18/25 (`f10fe384…2668` / 55300). Frozen-25 inherited lock remains **9/15** (`515f092c…b523`); not a stale 18/22 label.

Versus live v11: 242 identical, `lib.rs` changed, `budgets.rs` new. Live still lacks `budgets.rs`.

## Law

`estimate_evaluation_work` takes inert census/rule counts. Full input driver must derive them. Cannot mint Run/replay. u128 sentinel limit+1; zero-products stay zero; disabled rules contribute zero; exhaustion **before** 100000 output bound; `BudgetExceeded` has no exact cost.

Archived source-25: 2513 comparisons, 72 AST projections, 6 unit cases; not runtime acceptance.

## Evidence

Host isolation: **125** sources, **18** archives, **113** tests, help/version 0. Six 18/25 base preflights exit 0.

Provider **not rebuilt**: 25 source+`Cargo.lock` pins revalidated against accepted v10 receipt `3aa90b48…9139` (14 archives, 3 unavailable).

Independent: identity-policy 110 passed; 6 budget unit tests ok. Did not re-pipe 2513 rows.

Original substantive pin-checks (composition, isolation, carry-forward, source-25 archive) stand except the withdrawn parent-class claim. Incorporated by pin of original `review.json` `ae89f604…0b94` / 5628.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, full compose, atom scan, replay, or release. Stage-meta remains unselected. Standing is still root assent + private activation, not a live write.
