# Design delta DRAFT — graph lanes: exact accelerators vs. semantic producers

**Status: DRAFT FOR REVIEW AFTER SIGNATURE. IT CHANGES NOTHING AND BINDS NOTHING.**

This file is a proposal written under
[`IMPLEMENTATION-FREEZE.md`](../IMPLEMENTATION-FREEZE.md) §10. It is not a delta
that has been taken up. It amends no law, no binding artifact, no claim status, no
product disposition, and no seal. It applies no edit to any other file in this
tree. `CD-RT-5` remains `BLOCKED_ON_PHASE_1A`; the §11 signature block remains
`[NOT FROZEN]`; every §7.1 parked recipe remains parked and open.

Nothing below may be cited as authority. If any sentence here conflicts with the
live authority set — binding artifacts and the claim register, then accepted
product scope/dispositions, then the freeze and implementer blueprint, then
narrative architecture — this file loses.

**Drafted:** 2026-08-04 · **Verification basis:** live bytes read on 2026-08-04,
recorded in §11.

---

## 0. What this draft found before it proposed anything

This delta was commissioned to establish one distinction:

> **Exact accelerators** are rebuildable, non-authoritative caches — host-owned,
> excluded from Run and Evidence identity, usable only when bound to the exact
> Project, Snapshot and fact-partition set. **Algorithms that can change findings**
> are semantic producers, not caches; their algorithm identity, version,
> parameters, inputs and Coverage enter the normal semantic identity chain.

**Re-verification against live bytes says that distinction is already normative,
in six places, and has been since before this draft was commissioned.** It is
freeze §6 **law 8** in the law text itself, a freeze §8 **litmus question**,
blueprint **§2.1** rules 1–8, blueprint **§5.A** and **§7.4**, architecture **04**
and **06**, and traceability row `GX-01` in **11**. §1.1 below quotes each.

Proposing it again would be the exact failure this corpus names a paper seal: a
document that reads as a change while changing nothing, and which then makes the
property *look* twice-decided while leaving it exactly as enforced as it was.

So the spine of this draft is still that distinction, but what the draft *proposes
about it* is different, and narrower:

| | The distinction is… | Proposal |
|---|---|---|
| **as a rule** | already law (§6 law 8) | **nothing.** Do not restate it. |
| **as an identity exclusion** | stated only in narrative architecture (04, 06) — the weakest authority tier — while the recipes it constrains (`RunId`, `EvidenceDigest`, cache keys) are **parked and unwritten** | `D-1` — one clause at law level, §3.1 |
| **as a mechanical property** | enforced by **zero** binding artifacts and **zero** checkers; the only gates are blueprint prose and are conditional | `D-3` — an instrument, options unadjudicated, §3.3 |
| **as a citation** | `GX-05`/`GX-09` name a plan section that does not contain the cited content, and the plan cannot be edited | `D-2` — repoint or re-pin, §3.2 |

`D-1` is the only proposed change to normative text. `D-2` is a citation repair.
`D-3` is a choice this draft deliberately does not make for the reviewer.

---

## 1. Reason and new evidence — §10 item 1

### 1.1 The three review items that are already law — re-verified, not taken on trust

The commissioning note listed three review items as already binding. All three
confirm, one with a correction to the citation and one with a precise limit on
what "mechanically enforced" covers.

**(a) "typed QueryService; adapters cannot query storage."** Freeze §6 **law 16**,
verbatim (`IMPLEMENTATION-FREEZE.md:874-875`):

> 16. No renderer, agent surface, or report performs policy or reads physical
>     storage tables directly.

Corroborated at blueprint §4 by the forbidden edges
`query -> physical storage tables|host orchestration|provider adapters` and
`any renderer or query projection -> physical storage tables`, and by
`architecture/08-surfaces-and-topology.md:50-56`:

> The host resolves storage and supplies typed sealed values. Query logic never
> reads physical tables, invokes a provider, starts analysis, allocates an attempt,
> seals a Run, derives policy, or chooses process termination.

**Established. Nothing to add.**

**(b) "project-scoped persisted keys."** Freeze §6 **law 8**, first two sentences,
verbatim (`IMPLEMENTATION-FREEZE.md:846-848`):

> 8. The host is sole Run-sealing and durable-state authority. Each canonical
>    ProjectId owns `projects/<ProjectId>/ledger.sqlite` and its own physical CAS;
>    cross-project physical deduplication is forbidden.

Corroborated at blueprint §4 (`crates/store` must not own `cross-project physical
dedup`) and `architecture/06-evidence-and-persistence.md:165-166`:

> No component or generation is shared physically across ProjectIds, and a
> project-local dense node number has meaning only under its generation.

**Established. Nothing to add.**

**(c) "global origin/fact ranking — never adopt."** Freeze §6 **law 3**, opening,
verbatim (`IMPLEMENTATION-FREEZE.md:796`):

> 3. C-1 is predicate-relative. There is no global fact or layer ordering.

Mechanically enforced by `artifacts/fact-plane.v1.json` `$.c1Boundary`
(`fact-plane.v1.json:657-660`):

> `"forbiddenGlobalFields": ["quality", "tier", "degraded", "rank"]`

`python3 -I -B artifacts/check-fact-plane.py --selftest` was executed on
2026-08-04 and reports *"all 30 semantic mutations and 4 root-shape cases rejected
— the proof path is load-bearing"*, including
`("add a 'quality' field to the envelope (F1 / C-1)", _m_envelope_quality)` and
`("declare a global layer ordering (F7 / C-1)", _m_global_ladder)`.

**Established.** Two limits worth recording precisely, neither of which this delta
proposes to repair:

1. The enforcement is real but is a **parallel constant**, not a read of the
   contract: `check-fact-plane.py:39` declares
   `FORBIDDEN_ENVELOPE = {"quality", "tier", "degraded", "rank"}` and applies it at
   line 864 (`for bad in FORBIDDEN_ENVELOPE & set(env)`). The checker never reads
   `$.c1Boundary` — `grep -n "c1Boundary" artifacts/check-fact-plane.py` returns
   nothing. The two lists agree today. An edit to the contract's declared list
   would not change what the instrument enforces. That is a silent-drift shape of
   the class §7.2 exists to catch, it is **outside this delta's subject**, and it
   is named here only so a reviewer sees it was looked at.
2. `F7` guards `rank`/`order` on a relation and `layerOrder`/`tierOrder`/
   `globalLadder` at contract root; the forbidden-envelope set guards the fact
   envelope. Together they cover the law-3 surface this delta touches.

### 1.2 The distinction itself is already law — the quotes that make this draft narrow

Freeze §6 **law 8**, third sentence onward, verbatim
(`IMPLEMENTATION-FREEZE.md:848-855`):

> Warm/provider state is acceleration only. The same rule governs graph indexes: an
> **exact accelerator** is project-scoped, rebuildable, optional, and must be
> parity-equivalent to canonical traversal. Any graph computation whose
> algorithm/version/parameters/inputs can change an edge, finding, ordering,
> omission, or Coverage is a **semantic producer**, not a cache, and must follow
> normal Plan/fact/provenance/Coverage/evidence custody. Neither cache absence nor
> cache corruption may become a false empty or clean result.

Freeze §8 implementer litmus, verbatim (`IMPLEMENTATION-FREEZE.md:1452-1453`):

> - how an exact graph accelerator differs from a semantic graph producer, and what
>   happens when the accelerator is absent, corrupt, partial, or stale;

Blueprint §2.1 rule 6, verbatim (`IMPLEMENTER-BLUEPRINT.md:792-795`):

> 6. Any graph algorithm whose version, parameters, threshold, approximation, or
>    inputs can change semantic output is a fact producer. Route it through normal
>    Plan/provider identity, fact admission, provenance, Coverage, and evidence;
>    never hide it in `crates/index`.

`architecture/04-fact-plane.md:259-262`, the classification table, verbatim:

> | Kind | Test | Identity and custody consequence |
> |---|---|---|
> | **Exact accelerator** | Removing it or changing its physical implementation may change latency or memory, but the canonical answer remains byte-equivalent | Private, rebuildable cache. It is never evidence authority and does not enter Run semantics. |
> | **Semantic producer** | Its algorithm, version, parameters, threshold, approximation, or input set can change an edge, finding, rank, omission, or Coverage | Normal admitted analysis. The relevant producer/algorithm inputs are bound through the Plan/fact path; outputs carry provenance and Coverage and follow ordinary evidence custody. |

The distinction is derivable from law 2 — *"Only declared analysis inputs may
affect `PlanId`"* — and law 4 — *"Every required predicate receives exact Coverage;
unmet requiredness cannot become pass or a false no-match"* — and it is also
**stated**. The commissioning premise that it is "nowhere stated" does not survive
contact with the bytes. That finding is the single most important thing in this
draft and it *subtracts* from the delta rather than adding to it.

### 1.3 The new evidence that does justify a delta

Three findings, each verified on 2026-08-04.

**E-1 — the identity-exclusion half of the distinction sits one authority tier
below the rest of it, and the recipes it constrains are unwritten.**

Law 8 binds an accelerator's *custody* (project-scoped, rebuildable, optional,
parity-equivalent) and its *failure behavior* (no false empty, no false clean). It
does **not** say that a generation, manifest, active pointer, or cache key is
excluded from identity. The exclusion exists only as narrative architecture — the
authority tier the borrow register itself ranks last:

- `04-fact-plane.md:261` — *"It is never evidence authority and does not enter Run semantics."*
- `06-evidence-and-persistence.md:157-159` — *"The generation manifest and active pointer live only in the rebuildable cache partition. They are not a Run, evidence object, proof of Coverage, or source of a semantic identity."*

This matters now, and not later, because of what freeze §7.1 says is still open.
`RunId` derivation, sealed-Run manifest identity, `EvidenceDigest`, `FactViewId`,
and **cache and regeneration key recipes** are all parked rows, and §7.1 closes:

> Every row above must be closed by a binding artifact before signature. None may
> be closed by this record, by the blueprint, by a checker, or by an implementer.

So the authors of those recipes have not written them yet, and at law level nothing
currently tells them that a cache generation digest is not an admissible input. The
blueprint's §4 forbidden edge
`index -> policy|evidence authority|Run seal|semantic producer ownership`
constrains *dependency direction* — `crates/index` may not reach into evidence. It
does not constrain *identity composition*, and the party that composes `RunId` is
the host, which sits on the permitted side of that edge. A host that mixes an
accelerator's generation digest into a Run or evidence identity violates no live
law, breaks no forbidden edge, and produces exactly the outcome the distinction
exists to prevent: a rebuildable cache becomes load-bearing for a sealed identity,
and rebuilding the cache changes the identity of a Run that did not change.

**E-2 — `GX-05`/`GX-09` cite a plan section that does not contain the cited
content, and the plan is not editable.**

`architecture/11-traceability.md:106`, verbatim:

> | `GX-05`, `GX-09` | Sharding, CSR, side indexes, bounded reach materialisation, and their performance remain measured implementation choices | [implementation plan](../ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) Phase 5; blueprint §8.4 |

`GORTEX-BORROW-REGISTER.md:44` and `:48` carry the same citation in their "OpenSIP
home" column: `[plan Phase 5](ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md)`.

`ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` §"Phase 5 — Implementation kickoff"
(lines 279–297) contains a six-row build-order table and an
"Architecture-was-good-enough criterion". It contains no graph row, no index row,
no query row, no measurement gate, and the strings *graph*, *index*, *accelerator*
and *QueryService* do not appear in it. The section exists; the content it is cited
for does not. The blueprint half of both citations resolves correctly — §8.4
*"Phase-5 graph/query measurements"* is real and complete.

The content that would satisfy the plan half exists, and is verifiably a reverted
edit. `/private/tmp/.../scratchpad/gortex-preserved/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.gortex-edit.md`
(sha256 `2edce752e7d669e82224dc57c63e2872219b13660f979f75033cc4e363b769b8`)
carries a `#### Gortex-derived implementation profile` block and a five-row
Phase-5 gate table; `diff` against the live file shows those blocks present in the
preserved copy and absent from the live one. That copy is scratch, is not in the
tree, and binds nothing.

The plan **cannot** simply be edited to close this. Its SHA-256
`47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e` is pinned in
seven retained checkers — `check-retention-custody-v16.py` through `-v22.py` —
each as a hash-verified closure member (`check-retention-custody-v22.py:142`). An
edit breaks all seven and invalidates every verdict standing on them, which freeze
§7.2 addresses directly:

> A change to reviewed bytes requires a version bump and a new verdict; it may
> never be made in place.

This is therefore a real §10 decision and not a typo fix. §3.2 states the options.

**E-3 — the distinction has no instrument, and its gates are conditional prose.**

Searched on 2026-08-04 across `docs/coop/artifacts/`:

- no file matches `GX-0` — the borrow IDs appear in no binding artifact;
- no `.py` checker matches `accelerat`, `GraphView`, `DerivedIndex`, `derived_index`, or `graph_index`;
- no binding artifact defines a graph-lane conformance obligation.

The only conformance surface is blueprint §7.4, whose own header states its
conditionality, verbatim (`IMPLEMENTER-BLUEPRINT.md:1552-1555`):

> The pure reference graph and `QueryService` participate in the v1 inspect/query
> path. A persisted accelerator does **not**: these gates become required only when
> an exact derived index is introduced, and they determine whether that index may
> serve answers. Failing them means bypass the index, not weaken the query.

That conditionality is defensible for the seven gates that describe an index. It is
questionable for the two that are law 4 restated — parity and absence — and for the
one that guards the boundary itself — semantic-producer classification. Those three
constrain behavior that exists in v1 *with no index at all*: a reference traversal
that cannot meet a declared bound must still yield Coverage rather than an empty
set, and a semantic algorithm must be classified correctly whether or not anyone
has built a cache to hide it in. See §8, T1, T8 and T9.

The corpus's own standard on this point, from `GORTEX-BORROW-REGISTER.md:83-84`:

> When a `GX-*` row is implemented, replace its disposition only after linking the
> exact tests or retained measurement report; prose completion is not enough.

---

## 2. Affected claims, artifacts, modules, fixtures, product behavior — §10 item 2

**Claims.** None change status. `C-1` is untouched: this delta does not modify the
predicate-relative model, introduces no ordering, and adds no field to any relation
ladder or fact envelope. `CD-RT-5` stays `BLOCKED_ON_PHASE_1A`. `V10`, `G19`,
`R-1`, `D9`, `C-2`, `P-4` are untouched. `claim-register.v1.json` needs no edit for
`D-1` or `D-2`; whether `D-3` would require a register row depends on which option
§3.3 is adjudicated to, and this draft does not decide that.

**Binding artifacts.** `D-1` and `D-2` require no artifact edit. `D-3` under option
`I-b` or `I-c` would introduce one new artifact plus its retained checker, which
would then need a §3 disposition row, an independent review at exactly its bytes,
and a §7.2-conformant digest record. That cost is the reason §3.3 does not choose.

**Documents in the change surface** — *if the delta is taken up; this draft edits
none of them*:

| Document | Touched by | Nature |
|---|---|---|
| `IMPLEMENTATION-FREEZE.md` §6 law 8 | `D-1` | one added clause |
| `IMPLEMENTATION-FREEZE.md` §7.1 | `D-1` | one added obligation on recipe authors |
| `architecture/11-traceability.md` row `GX-05`,`GX-09` | `D-2` | citation |
| `GORTEX-BORROW-REGISTER.md` rows `GX-05`, `GX-09` | `D-2` | citation |
| `IMPLEMENTER-BLUEPRINT.md` §7.4 | `D-3` | gate conditionality; possible tenth row |
| `architecture/04-fact-plane.md`, `06-evidence-and-persistence.md` | none | already correct; `D-1` promotes their statement, it does not contradict it |
| `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` | `D-2` option `C-b` only | **pinned in seven checkers; see §3.2** |

**Modules.** No crate boundary moves. The surfaces named by the obligations in §8
are the existing blueprint §4 packages: `opensip-graph` (`GraphView`, canonical
reference traversal), `opensip-index` (generation manifests/state machine, exact
accelerator build/read validation), `opensip-query` (`QueryService` over a
host-supplied sealed `QueryView`), `opensip-store` (project-keyed cache API),
`opensip-host` (cache adapter, identity minting), and the ordinary fact/provider
owners for semantic producers. No forbidden dependency edge is added, removed, or
weakened. `D-1` constrains the host's identity composition, which no existing edge
covers (§1.3, E-1).

**Fixtures.** §8 names ten obligations. Nine correspond to existing blueprint §7.4
gates; **T7 has no current gate row** and exists today only as narrative prose at
`04-fact-plane.md:266-269`. No fixture is retired.

**Product behavior.** None. No v1 capability is added, removed, enabled, or
flagged. §4.1's required set does not grow; §4.2's exclusions stand. A conforming
v1 with no persisted accelerator at all is unaffected by every clause in §3.

---

## 3. Old and new normative text — §10 item 3

### 3.1 `D-1` — the identity-exclusion clause *(the only proposed normative change)*

**Where:** `IMPLEMENTATION-FREEZE.md` §6, law 8.

**Old text, verbatim, live at 2026-08-04 (`IMPLEMENTATION-FREEZE.md:846-855`):**

> 8. The host is sole Run-sealing and durable-state authority. Each canonical
>    ProjectId owns `projects/<ProjectId>/ledger.sqlite` and its own physical CAS;
>    cross-project physical deduplication is forbidden. Warm/provider state
>    is acceleration only. The same rule governs graph indexes: an **exact
>    accelerator** is project-scoped, rebuildable, optional, and must be
>    parity-equivalent to canonical traversal. Any graph computation whose
>    algorithm/version/parameters/inputs can change an edge, finding, ordering,
>    omission, or Coverage is a **semantic producer**, not a cache, and must follow
>    normal Plan/fact/provenance/Coverage/evidence custody. Neither cache absence nor
>    cache corruption may become a false empty or clean result.

**New text — proposed. The whole change is the final two sentences; every word
above them is carried byte-identically:**

> 8. The host is sole Run-sealing and durable-state authority. Each canonical
>    ProjectId owns `projects/<ProjectId>/ledger.sqlite` and its own physical CAS;
>    cross-project physical deduplication is forbidden. Warm/provider state
>    is acceleration only. The same rule governs graph indexes: an **exact
>    accelerator** is project-scoped, rebuildable, optional, and must be
>    parity-equivalent to canonical traversal. Any graph computation whose
>    algorithm/version/parameters/inputs can change an edge, finding, ordering,
>    omission, or Coverage is a **semantic producer**, not a cache, and must follow
>    normal Plan/fact/provenance/Coverage/evidence custody. Neither cache absence nor
>    cache corruption may become a false empty or clean result.
>    **No accelerator state is an identity input.** No derived-index generation,
>    component, manifest, active-pointer state, lease, local dense ID, or cache
>    lookup key may be an input to `SNAPSHOT-ID-V1`, `PLAN-ID-V1`, `RunId`, sealed-Run
>    manifest identity, `EvidenceDigest`, a finding fingerprint, or any Coverage
>    value — whether composed inside `crates/index` or by the host that mints the
>    identity. **An accelerator is usable only where bound**: it may serve a query
>    only while bound to the same canonical `ProjectId`, sealed Snapshot, and exact
>    fact view/partition set as that query, and a binding that cannot be verified is
>    a bypass, never a weaker answer.

**Companion clause, `IMPLEMENTATION-FREEZE.md` §7.1.** The parked rows are the
place this exclusion will either be honored or quietly lost. Proposed addition
after the table's closing paragraph — *"Every row above must be closed by a binding
artifact before signature."*:

> A binding artifact closing the `RunId`, sealed-Run manifest identity,
> `EvidenceDigest`, finding-fingerprint, `FactViewId`, or cache/regeneration-key
> row MUST state law 8's accelerator-exclusion explicitly for the identity it
> defines, and MUST be checkable against it. A recipe that is silent on the
> exclusion does not satisfy this section.

**Why this is a change and not a restatement.** Law 8 binds custody, parity, and
failure behavior. It does not mention identity. The exclusion exists only at
`04:261` and `06:157-159`, which are narrative architecture and rank below the
freeze in the authority order the borrow register states. The blueprint §4 edge
`index -> policy|evidence authority|Run seal|semantic producer ownership` bars
`crates/index` from reaching evidence; it does not bar the host from reaching into
`crates/index` for an input, and the host is the identity minter. Meanwhile the six
identities named above are all §7.1 parks — not yet written. This clause is
addressed to the people who will write them.

**Derivation, so the clause is not a new idea.** Law 2: *"Only declared analysis
inputs may affect `PlanId`"* — an accelerator is by law 8's own words *optional*
and *rebuildable*, so it is not a declared analysis input, and the same reasoning
extends to identities whose recipes are still open. Law 4: *"Every required
predicate receives exact Coverage; unmet requiredness cannot become pass or a false
no-match"* — an unverifiable accelerator binding is unmet requiredness, and the
sanctioned outcome is bypass or Coverage, never a shorter answer. `D-1` writes down
the consequence; it does not introduce a new principle. **A reviewer should test
exactly that**: if `D-1` says anything not entailed by laws 2, 4 and 8, it is
overreach and should be cut back to what is.

### 3.2 `D-2` — the `GX-05`/`GX-09` citation

**Old text, verbatim (`architecture/11-traceability.md:106`):**

> | `GX-05`, `GX-09` | Sharding, CSR, side indexes, bounded reach materialisation, and their performance remain measured implementation choices | [implementation plan](../ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) Phase 5; blueprint §8.4 |

**Old text, verbatim (`GORTEX-BORROW-REGISTER.md:44`, "OpenSIP home" cell):**

> [plan Phase 5](ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md), [blueprint](IMPLEMENTER-BLUEPRINT.md)

Three candidate closures. **This draft recommends `C-a` and does not adjudicate.**

| | Option | New text / action | Cost |
|---|---|---|---|
| `C-a` | **Repoint the citation to the document that holds the content.** | 11 row becomes *"…measured implementation choices \| blueprint §8.4 (measurements) and §7.4 (parity gates)"*; register cells drop the plan link and cite blueprint §8.4. | None to the pinned plan, none to the seven checkers. Honest: §8.4 is complete and is where the obligation actually lives. |
| `C-b` | **Restore the reverted Phase-5 content in the plan.** | Re-apply the `#### Gortex-derived implementation profile` and Phase-5 gate blocks preserved at sha256 `2edce752…`. | Changes `47df412d…`. Requires re-pinning **seven** retained checkers `check-retention-custody-v16..v22.py`, each of which currently carries a standing verdict over that closure. §7.2 forbids the in-place edit; every affected verdict needs a version bump and a new verdict. Disproportionate to a citation. |
| `C-c` | **Record the citation as knowingly aspirational.** | Annotate both rows: the plan does not carry this content and is byte-pinned. | Cheapest, but leaves a citation that does not resolve. This corpus has a specific history with citations that point at bytes not carrying what they claim. |

**The general point a reviewer should weigh above the three options.** Seven
checkers pin a *narrative planning document* as a hash-verified closure member.
That pin makes the plan effectively immutable while it remains the cited home for
anything. Whether a plan should be pinned that way at all is a question larger than
this delta and is flagged, not answered, here.

### 3.3 `D-3` — an instrument for the distinction *(deliberately unadjudicated)*

`D-1` and `D-2` are prose. E-3 established that the distinction has no mechanical
enforcement anywhere in the corpus. Three options; **this draft states the costs
and does not choose.**

| | Option | Shape | Honest cost |
|---|---|---|---|
| `I-a` | **Leave it to §7.4, promote three gates.** | Amend §7.4's header so that `T1`, `T8`, `T9` are unconditional and the remaining seven stay index-conditional; add `T7` as the missing tenth row. | Cheapest. Leaves the property enforced by prose in the blueprint, which is precisely what E-3 identifies as the gap. |
| `I-b` | **A binding conformance artifact plus a retained checker.** | `graph-lane-conformance.v1.json` + `check-graph-lane-conformance.py` with a `--selftest` mutation suite over the ten obligations of §8, entering the §3 disposition ledger. | A new §3 row, an independent review at exactly its bytes, a §7.2-conformant digest record, and a `SELFTEST-NOT-RUN`/exit-3 discipline matching `check-evidence-v9.py`. Adds a pre-signature surface. |
| `I-c` | **Extend an existing instrument.** | Add the classification and identity-exclusion checks to `check-fact-plane.py`. | Cheapest instrument-wise, but the graph lane is not the fact plane's subject; it would bury the property in an unrelated contract and enlarge an artifact that currently passes cleanly. |

**Hard constraint on any option.** Freeze §7.1 parks *"cache and regeneration key
recipes"* and `FactViewId`, and states that none may be closed *"by this record, by
the blueprint, by a checker, or by an implementer."* An instrument for this delta
must therefore test **binding dimensions and behavior** — that a query and the
accelerator it uses agree on ProjectId, Snapshot, and fact view/partition set, and
that a mismatch bypasses — and must **not** test or imply a key byte recipe. A
`D-3` instrument that accidentally fixes a cache key would close a park it has no
authority to close. `04-fact-plane.md:274-276` says the same thing about the same
dimension list: *"Those are required **binding dimensions**, not a new byte grammar
… an implementer may not invent them from this paragraph."*

---

## 4. Checker and mutation changes — §10 item 4

**Under `D-1` alone:** none. Law 8 has no retained checker; no existing checker
reads §6, and no artifact digest changes. `check-fact-plane.py`,
`check-retention-custody-v16..v22.py`, and every other retained instrument are
unaffected, and `47df412d…` is unchanged.

**Under `D-2` option `C-a` or `C-c`:** none. `11-traceability.md` and
`GORTEX-BORROW-REGISTER.md` are not pinned by any checker — verified by searching
the corpus for their names in `.py` files on 2026-08-04.

**Under `D-2` option `C-b`:** seven. `check-retention-custody-v16.py` through
`-v22.py` each carry `ARCHITECTURE_PLAN: "47df412dba…"` in a hash-verified closure
map. Every one requires a new version and a new independent verdict under §7.2;
none may be re-pinned in place.

**Under `D-3` option `I-b`, the mutation suite the instrument would have to
reject** — listed so a reviewer can price it, not as a specification:

| # | Mutation | Must be rejected because |
|---|---|---|
| M1 | declare a graph computation with a version/parameter field as an exact accelerator | it is a semantic producer (law 8) |
| M2 | feed a generation digest into a Run/evidence identity preimage | `D-1` |
| M3 | serve a query from a generation bound to a different Snapshot | `D-1` binding clause; §7.4 stale key |
| M4 | return an empty edge set where the accelerator is absent | law 4; law 8 final sentence |
| M5 | return an empty edge set where the reference path exceeds its bound | law 4; `T7` |
| M6 | activate a generation with one component's digest unverified | §7.4 incomplete construction |
| M7 | let a query observe components from two generations | §7.4 query pinning |
| M8 | share a physical cache object across two ProjectIds | law 8; §7.4 project isolation |
| M9 | let a dense local ID escape its generation as a `FactId` or subject identity | blueprint §2.1 rule 8 |
| M10 | route a CLI query around `QueryService` to a physical table | law 16 |
| M11 | present a bound-truncated reach set as exhaustive | `04:266-269`; `T7` |
| M12 | admit a semantic producer's output without provenance/Coverage | law 8; law 4 |

Following `check-evidence-v9.py`, a `D-3` instrument must make *"the suite did not
run"* a distinct observable — `SELFTEST-REFUSED`/`SELFTEST-NOT-RUN` and exit `3`,
separate from green `0`, findings `1`, bad invocation `2`. Freeze §7.2 records why
that shape is mandatory: a dead `--selftest` produced a clean pair while verifying
nothing.

---

## 5. Independent review and adjudication — §10 item 5

**OPEN. This has not happened and this draft does not claim it.**

No review of this file exists. No adjudication of `D-2`'s three options or `D-3`'s
three options exists. The author of this draft is not independent of it.

What a review must do, stated so the obligation is falsifiable:

1. **Re-run the paper-seal test independently.** §0 and §1.1–1.2 assert that the
   distinction is already law and that the commissioning premise was wrong. A
   reviewer who cannot reproduce that from the live bytes should reject this draft
   rather than accept its narrowing.
2. **Test `D-1` for overreach.** §3.1 claims every clause is entailed by laws 2, 4
   and 8. Any clause that is not entailed is new law arriving through a delta that
   describes itself as a consequence, and must be cut or escalated as its own
   decision.
3. **Test `D-1` for redundancy.** If a reviewer finds the identity exclusion
   already binding somewhere this draft did not search — a binding artifact rather
   than 04/06 narrative — then `D-1` is itself a paper seal and must be withdrawn.
   This draft searched `artifacts/` for accelerator and index terms and found
   nothing; it did not exhaustively read all 300+ artifacts.
4. **Adjudicate `D-2` and `D-3` explicitly**, including the option of doing
   nothing. §7.2's subject-freezing rule applies: whatever bytes are dispatched for
   review must not move while the review runs.

Under §7.2.1 the reviewed subject must be frozen before dispatch. If this file is
dispatched, its SHA-256 at dispatch time must be recorded by the reviewer, and any
later edit requires a `v2` and a new verdict.

---

## 6. Compatibility and migration impact — §10 item 6

**Product behavior:** none. No v1 capability changes. §4.1 does not grow, §4.2
holds.

**Implementations:** none exist. Freeze §11 reads `[NOT FROZEN]` and §9 records
that this file *"carries no permission to start Phase-5 product implementation."*
There is nothing built against law 8 to migrate.

**Stored data:** none. `D-1` constrains what may enter an identity; it defines no
identity, so no stored value changes shape, and no ledger, CAS, or cache partition
requires migration. Because every identity it names is a §7.1 **park**, `D-1`
cannot invalidate an existing derivation — there are none.

**Forward compatibility, which is the actual point:** `D-1` is cheap now and
expensive later. Once a `RunId` or `EvidenceDigest` recipe is bound, discovering
that it admits a cache input is not a clause edit — it is a new recipe version, a
new independent verdict, and re-derivation of everything pinned to it. The whole
migration argument for `D-1` is that it lands before the recipes, not after.

**If `D-2` `C-b` is chosen:** seven retained checkers and their standing verdicts
require version bumps. That is the migration cost of a citation repair, and it is
why `C-a` is recommended.

---

## 7. New freeze version, payload manifest, snapshot reference — §10 item 7

**CANNOT BE FILLED, AND IS NOT INVENTED HERE.**

There is no freeze version to increment. `IMPLEMENTATION-FREEZE.md` §11 reads, live
at 2026-08-04:

```text
Disposition: [NOT FROZEN]
Freeze version: [UNSET]
Date: [UNSET]
Payload hash: [UNSET]
Snapshot/tag: [UNSET]
```

and §9.2 reads:

```text
Manifest artifact: [UNSET]
Manifest SHA-256: [UNSET]
Snapshot/tag/commit: [UNSET]
Freeze date/timezone: [UNSET]
```

Item 7 is therefore vacuous at the time of drafting and stays open until v1 is
signed and this delta is taken up. Two things a reviewer should note rather than
have restated as fields:

1. §9.2's manifest covers *"the complete `docs/coop/` snapshot"*. **This file is
   inside that payload.** Its existence changes the payload manifest and therefore
   the payload hash, before any delta is adopted. If the manifest has been
   generated, `python3 -I -B artifacts/make-freeze-manifest.py --verify` will now
   report `deltas/gortex-graph-lanes.delta-draft.v1.md` as an added path. That is
   correct behavior, not a defect, and is stated here so it is not mistaken for one.
2. If this delta is taken up post-signature, the version increment, regenerated
   manifest, and snapshot reference are produced then, by the signer, from the tree
   as it exists then. Writing plausible values here would be a fabricated field of
   the class §4.4 exists to record.

---

## 8. The conformance suite — ten acceptance obligations

Written as testable obligations against named blueprint §4 surfaces. **`T1` and
`T8` lead: they are law 4 restated executably.** The right-hand column records
where each obligation lives today, which is the honest measure of what `D-3` would
add.

Each obligation's oracle is the pure reference traversal in `opensip-graph`, never
fixtures emitted by the builder under test (`IMPLEMENTER-BLUEPRINT.md:1569-1572`).

| # | Obligation | Surfaces | Falsified by | Lives today in |
|---|---|---|---|---|
| **T1** | **Enabled/disabled equivalence.** For every fixture in the declared set — positive, empty, cyclic, disconnected, multi-edge, bounded-depth, budget-limited — a `QueryService` request executed with the accelerator active and with it absent returns **byte-equivalent** canonical results, ordering, Coverage, truncation state, and cursors. | `opensip-query`, `opensip-graph`, `opensip-index` | any byte difference in the canonical result between the two runs | §7.4 *reference parity*, **conditional** |
| T2 | **Physical determinism.** Shard count, insertion order, worker schedule, and cache process restart do not alter any canonical result. Local dense IDs never appear in a canonical result. | `opensip-index`, `opensip-query` | a canonical result varying with a physical parameter; a dense ID escaping | §7.4 *physical determinism* |
| **T3** | **Partial generations are never query-visible.** Crash-inject after every component write and before and after activation. No query observes a `building` generation, a partial component set, or a mix of two generations. Recovery reaches either the prior complete generation or a newly verified complete one — never a third state. | `opensip-index`, `opensip-store` cache API, `opensip-host` cache adapter | any query result derived from an unactivated or mixed generation | §7.4 *incomplete construction* |
| T4 | **Corrupt or mis-bound generations are refused before use.** Damage each of manifest, component digest, count, schema, kind, version, parameter, and each binding input in turn; each is detected **before** the generation serves an answer. A generation bound to a different ProjectId, Snapshot, or fact view/partition set cannot be selected. | `opensip-index`, `opensip-host` | a damaged or mis-bound generation serving one answer | §7.4 *corruption and stale key*; binding half proposed for law level by `D-1` |
| T5 | **Query pinning.** A query concurrent with an activation observes exactly its pinned generation, old or new, never a splice. Collection of a stale generation waits for its pin to drain. | `opensip-index`, `opensip-query` | a spliced result; collection of a pinned generation | §7.4 *query pinning* |
| T6 | **Project isolation.** Identical source and object content under two ProjectIds shares no generation path, active pointer, dense-ID namespace, lease, or physical cache object. | `opensip-store`, `opensip-index` | any shared physical object or namespace across ProjectIds | §7.4 *project isolation*; law 8 |
| T7 | **Bounded results are never presented as exhaustive.** A response that stops at a declared depth or budget reports that through its bounded-result/Coverage shape. A truncated reach set is never returned as a complete one, with or without an accelerator. | `opensip-query`, `opensip-graph` | a truncated set returned without its bound/Coverage disclosure | **no §7.4 gate row.** Narrative only, `04-fact-plane.md:266-269`. Proposed as the missing tenth gate under `D-3` |
| **T8** | **Absence never becomes a false negative.** Delete the entire cache partition: second-process inspection and canonical answers are preserved. Where the reference computation cannot satisfy a declared bound, the result is explicit Coverage/indeterminate. No path returns an empty edge set, a no-match, or a clean verdict because an index was missing, corrupt, stale, or refused. | `opensip-query`, `opensip-graph`, `opensip-host` | any empty, no-match, or clean result attributable to accelerator state | §7.4 *absence*, **conditional** — law 4 is not conditional |
| **T9** | **Semantic graph algorithms enter the identity chain.** A graph computation whose algorithm, version, parameter, threshold, approximation, or input corpus can change an edge, finding, ordering, omission, or Coverage is admitted as a producer: its identity and inputs bind through the Plan/fact path, its outputs carry provenance and Coverage, and it follows ordinary evidence custody. Mutating such a version or parameter must not be expressible through the exact-index API. | ordinary fact/provider owners, `opensip-plan`, `opensip-facts`, `opensip-index` (as the surface that must **refuse**) | a semantics-changing algorithm reachable behind the cache API, or admitted without provenance/Coverage | §7.4 *semantic-producer guard*, **conditional**; law 8 is not conditional |
| T10 | **Adapter convergence.** The v1 CLI query/inspect adapter invokes `QueryService`. Any later adapter replays the same request/result goldens rather than a transport- or storage-specific handler, and creates no second analysis engine. | `opensip-cli`, `opensip-query` | an adapter reading a physical table or reproducing query logic | §7.4 *adapter convergence*; law 16 |

**What the right-hand column shows.** Nine of ten exist as blueprint gates and one
(`T7`) does not exist as a gate at all. Three (`T1`, `T8`, `T9`) restate
unconditional laws through a gate table that declares itself conditional on an
accelerator existing. That mismatch — not the absence of the distinction — is the
conformance gap this delta is for.

---

## 9. Scope discipline — what this draft does not do

Stated explicitly because each is a way this delta could be wrong.

- **It does not reopen the v1 slice.** §4.1's required set does not grow; §4.2's
  exclusions stand. No persisted accelerator becomes required. Blueprint §2.1
  already says an implementation *"can complete the first vertical slice with no
  derived index"*, and nothing here changes that.
- **It introduces no Gortex-specific public contract.** No GCX1 syntax, no wire
  format, no shard layout, no compact projection encoding, no upstream type. Only
  the *distinction* is borrowed, and it was already borrowed and already law.
- **It does not modify the predicate-relative C-1 model.** No ordering, rank, tier,
  or quality field is added anywhere. `D-1` adds an exclusion, which removes
  admissible inputs rather than adding an ordering.
- **It closes no parked recipe.** `FactViewId`, cache/regeneration keys, `RunId`,
  sealed-manifest identity, `EvidenceDigest`, and finding fingerprints stay parked
  and open. `D-1` constrains what those recipes may admit; it does not write one,
  and §3.3 forbids a `D-3` instrument from writing one either.
- **It changes no status.** Nothing is signed, sealed, frozen, applied, or
  discharged. `CD-RT-5` remains `BLOCKED_ON_PHASE_1A`.

**Phase-5, post-v1 and never — named and left where they are.** None of these
appears in the normative text of §3, and a reviewer should check that claim
directly:

| Item | Borrow ID | Stays where |
|---|---|---|
| Sharding, adjacency CSR, O(1) side indexes, precomputed bounded reach | `GX-05` | **Phase 5** measurement, blueprint §8.4. Candidates, not architecture. |
| Graph/query instrumentation and retained measurement reports | `GX-09` | **Phase 5**, blueprint §8.4 |
| Compact lossless agent projection | `GX-06` | **post-v1 parked**, product scope change required |
| Session-scoped editor/speculative overlays | `GX-07` | **post-v1 parked**, product scope change required |
| Resident provider pools, lazy startup, idle reaping, watcher debouncing | `GX-08` | **post-v1 parked** behind R-1 and product scope |
| Cross-project analysis, edges, and plans | `GX-04` | **post-v1**; v1 admits one canonical ProjectId |
| Global provenance/origin/fact-quality/fallback rank | `GX-N01` | **never.** Law 3; `forbiddenGlobalFields` |
| `PATH`/system-selected provider authority | `GX-N02` | **never** |
| Silent substitution on unavailable provider/relation/index | `GX-N03` | **never.** Laws 3 and 4 |
| Live daemon/overlay/cache state as evidence authority | `GX-N04` | **never.** Law 8; `D-1` sharpens this one at law level |
| VCS commit as snapshot identity | `GX-N05` | **never** |
| Model-generated ranking on the analysis path | `GX-N06` | **never.** Law 1 |

---

## 10. Where this draft is unsure — named, not smoothed over

1. **Whether `D-1` is a real gap or a reading failure.** The strongest counterclaim
   is that `04:261` and `06:157-159` already say it, and that promoting narrative
   to law adds ceremony. The counter-counter is the authority ordering plus the
   fact that every constrained recipe is unwritten. **This draft is confident about
   the facts and less confident that the remedy is proportionate.** A reviewer may
   reasonably reduce `D-1` to its §7.1 companion clause alone.
2. **Whether the §7.4 conditionality is actually wrong.** §7.4 is coherent as
   written: gates about an index need an index. The claim that `T1`, `T8` and `T9`
   should be unconditional rests on those three constraining behavior that exists
   without one. That reading may be wrong, and the fix might be one sentence in
   §7.4 rather than a new instrument.
3. **Whether `D-3` is worth its cost before signature.** A new binding artifact
   adds a §3 row, an independent review, and a §7.2 digest record to a pre-freeze
   surface that is already carrying `EVIDENCE` and `TM` at `UNSET — BLOCKS FREEZE`.
   `I-a` may be the right answer purely on sequencing. **This draft does not know.**
4. **`D-2` `C-a` versus `C-c`.** `C-a` is recommended, but repointing a citation
   away from the plan quietly concedes that the plan is not the owner of Phase-5
   graph obligations, which slightly contradicts the plan's own role. That may be
   fine; it was not adjudicated here.
5. **Search completeness for `D-1`.** The claim that no binding artifact carries the
   identity exclusion rests on targeted searches of `artifacts/` for accelerator,
   index, graph and `QueryService` terms and for `GX-0`. It is **not** an
   exhaustive read of every artifact. A reviewer should treat E-1 as falsifiable
   and try to falsify it. *(§5 item 3.)*
6. **`T7`'s status.** It is a real obligation from `04:266-269` with no gate row.
   Whether that is an oversight or a deliberate judgment that bound honesty is
   covered by the ordinary Coverage machinery, this draft could not determine from
   the bytes.
7. **Where `D-1` belongs.** It is drafted as an addition to law 8 because that is
   where the distinction lives. It touches identities owned by law 6. Splitting it
   across two laws, or placing it wholly in §7.1, are both defensible and this
   draft did not resolve which is correct.
8. **The `check-fact-plane.py` parallel-constant observation (§1.1).** It is
   verified and it is real, but it is adjacent to this delta's subject rather than
   part of it. Whether it warrants its own delta, a non-blocking residual, or
   nothing at all is not this draft's call.

---

## 11. Verification record

Every quotation above was read from the live file on 2026-08-04; nothing is quoted
from memory or from a summary.

**Pinned-plan integrity, re-confirmed after this draft was written:**

```text
47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e  docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md
```

unchanged, and still matching the value pinned by `check-retention-custody-v16.py`
through `-v22.py`.

**Files read for this draft** (read-only; none modified):
`IMPLEMENTATION-FREEZE.md` §§3–4, 6, 7.1, 7.2, 8, 9.2, 9.3, 10, 11 ·
`IMPLEMENTER-BLUEPRINT.md` §§2.1, 4, 5.A, 5.1, 7.4, 8.4 ·
`ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` §§4 (Phase 5), 5 ·
`GORTEX-BORROW-REGISTER.md` (all) ·
`architecture/04-fact-plane.md`, `06-evidence-and-persistence.md`,
`08-surfaces-and-topology.md`, `11-traceability.md` ·
`v1-slice.md` · `artifacts/fact-plane.v1.json` ·
`artifacts/check-fact-plane.py` · `artifacts/check-retention-custody-v22.py` ·
`artifacts/claim-register.v1.json`.

**Command executed:** `python3 -I -B artifacts/check-fact-plane.py --selftest` —
green, *"all 30 semantic mutations and 4 root-shape cases rejected"*.

**Files this draft modified:** none. **Files created:** this one.
