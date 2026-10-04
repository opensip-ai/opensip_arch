# FA-1 — clean non-Complete terminals discard their candidates (native contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route, public code, schema, frame or protocol. It needs Grok's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** The accepted fact-admission law **M3-H r3** (`docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, Grok ACCEPT, `7a562720…`) routes cross-law item **X-H2** to the native owner as successor **FA-1** (H3:809, H3:859):
- **X-H2.** NE:3849-3850 admits "facts before the terminal" on a clean `BudgetExhausted` or `Unavailable`. The retained `delivery.v2` and `rust-provider-protocol.v2` selectors discard every candidate on those terminals, and NE §0 does not supersede them (H3:123, H3:859).
- **H's decision.** On a clean `Unavailable` or `BudgetExhausted`, every candidate is discarded and only the terminal's exhaustive Coverage is admitted (H3 decisions-at-a-glance row 4, H3:133; item 4, H3:242-263). It rests on H's boundary law: only D3's clean settlement reaches H, and admission is atomic per Analyze (row 3, H3:132; item 3, H3:206-240).
- **The rest of the FA-1 row.** "It also adds `native.coverage-closed-world-mismatch` to NE:3529's producer-boundary row (item 13)" (H3:809; item 13, H3:445-455). H2's closed-world wiring waits on it (H3:832).

FA-1 makes NE agree with the retained selectors and with H. It also answers M3-D's finding **F7** (MD:623, MD:1107), which handed this choice to H.

**Product.** Main at `cd5958b` (I1-P's binding, 82 contract successors), read only. The record is built and checked against it. No bound successor overrides any line FA-1 uses.

## Short names

Each sha256 prefix is the first 8 hex of the exact bytes pinned in the review request (`reviews/grok-fa-1-r1/hashes.txt`).

| Name | Document | sha256 |
|---|---|---|
| **H3** | `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, M3-H r3, the accepted snapshot (Grok, `reviews/grok-fact-admission-h-r3`) | `7a562720…` |
| **MD** | `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, M3-D r3, the accepted snapshot (GROK2) | `9679dbc4…` |
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md`, M3-J1 r4, the accepted snapshot (GROK2) | `c18c0d3c…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md`, the parent (329,013 bytes) | `83b99783…` |
| **DLV** | `docs/coop/artifacts/delivery.v2.json`, TS2's inherited base | `47b6cfd1…` |
| **RPP** | `docs/coop/artifacts/rust-provider-protocol.v2.json`, Rust3's inherited base | `6308a98c…` |
| **NES** | `docs/coop/design-corrections/native/native-evidence.schemas.v2.json`, the registered native bundle | `2d37b810…` |
| **NEM** | the native reference model: the selected copy `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py` (`a7e40715…`) and the frozen `docs/coop/design-corrections/native/native_evidence_model.v2.py` (`7d1c0acf…`) | |
| **NC** | `docs/coop/design-corrections/native/native-cases.v2.json`, the native reference cases | `a08b8cc3…` |
| **FA-2** | `docs/implementation/m3/native-successors-fa/fa-2/`, r2, in review with Codex (`reviews/codex-fa-2-r2`); not accepted | `f6b105f4…` (record) |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: every override with its exact `before` and candidate `after`, and the effective fault-law paragraph NE:3837-3855 after FA-1 |
| `successor.json` | the contract successor record: one parent (NE), three line overrides, no supersession |
| `evidence/build_fa1.py` | builds `PASSAGES.md`, the record, the subject manifest and the draft unit record deterministically; `--check` compares instead of writing |
| `evidence/check_fa1.py` | read-only content checks |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, the binding-order probes and one conflict probe |
| `../fa-1-subject.json` | the subject manifest (generated) |
| `../fa-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes: every changed passage

Each `before` is the parent line exactly, as `verify_design` reads it (`splitlines`). The full texts are in `PASSAGES.md` and `successor.json`.

| # | Parent | Line | Form | Change |
|---|---|---|---|---|
| 1 | NE | 3529 | insert-only | The §10 admission and event route row for producer-boundary faults (`operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION`, operational record) gains one condition and its internal key, after the `view2` clause and before "**worker fault**": a Coverage entry whose `closedWorld` contradicts a §4.5 record law, `native.coverage-closed-world-mismatch` |
| 2 | NE | 3849 | replace | "`BudgetExhausted` and `Unavailable` are clean typed terminals: facts before the" becomes "… are clean typed terminals (contract successor FA-1). On a" |
| 3 | NE | 3850 | replace | "terminal are admitted and the Run is authoritative with the stage `partial`." becomes the discard rule, the clean-settlement condition, the pre-Analyze case, the unchanged `partial` / authoritative sentence, the retained selectors by exact path, the reason (only `Complete` carries `factStreamCommitment`), and `StageAuthorityV1.factsAdmitted` = `none` |

No other NE line changes. The other lines of the fault-law paragraph, NE:3837-3848 and NE:3851-3855, keep their bytes: the fault rule, the incomplete-inputs rule for a clean `Complete`, and the primary-deficiency route of the stage.

### 1. The terminal rule (NE:3849-3850)

After FA-1 the two lines read:

> `BudgetExhausted` and `Unavailable` are clean typed terminals (contract successor FA-1). On a `BudgetExhausted` or a post-Analyze `Unavailable`, every fact candidate of that Analyze, and every occupancy companion it carried, is discarded, and only the terminal's exhaustive Coverage is admitted, at the producer boundary after a clean settlement (the valid terminal with its exhaustive Coverage and matching `coverageCommitment`, zero exit, EOF); a pre-Analyze `Unavailable` has no candidates, and its Coverage is the host conversion of §9.7. The Run is authoritative with the stage `partial`. The retained candidate dispositions govern, and §0 supersedes none of them: […the six selectors…]. Only `Complete` carries `factStreamCommitment` (`CompleteV1`, `CompleteV2`); these two terminals commit their Coverage alone, so nothing verifies a candidate streamed before them. For these two terminals `StageAuthorityV1.factsAdmitted` is `none`; where the reference `stage_authority` returns `before-terminal`, this text governs and the reference is the defect.

The six retained selectors, each named by exact path in the text and checked by `check_fa1.py` to resolve to the quoted value:

| Base | Selector | Value |
|---|---|---|
| DLV | `$.typescriptSemanticSubstrate.supervision.factBatchAtomicity.onUnavailable` (DLV:1140) | `DISCARD_ALL_CANDIDATES` |
| DLV | `$.typescriptSemanticSubstrate.supervision.factBatchAtomicity.onBudgetExhausted` (DLV:1141) | `DISCARD_ALL_CANDIDATES` |
| DLV | `$.typescriptSemanticSubstrate.supervision.cleanUnavailable.candidateDisposition` (DLV:1152) | `DISCARD_ALL_CANDIDATES` |
| DLV | `$.typescriptSemanticSubstrate.supervision.deterministicBudget.candidateDisposition` (DLV:1164) | `DISCARD_ALL_CANDIDATES` |
| RPP | `$.candidateAtomicity.discardAllOn` (RPP:597) | "every other terminal, cancellation, process/protocol fault or safety bound" |
| RPP | `$.candidateAtomicity.unavailableAndBudgetCoverage` (RPP:598) | "Only a valid terminal plus exhaustive unknown Coverage plus zero exit/EOF may admit terminal Coverage; candidates remain discarded." |

What stays exactly as it was:
- **The terminal is clean, not a fault.** The stage is `partial` and the Run is authoritative. The stage's native termination is still the route of its primary deficiency, `COVERAGE.BUDGET_EXHAUSTED` or `COVERAGE.PROVIDER_UNAVAILABLE` unless an entry declares a more specific one (NE:3851-3855). That is MJ row 31, indeterminate 3 (MJ:677). DLV:1156's "never operational-failed solely for clean Unavailable" holds.
- **The terminal's Coverage is admitted** at item 10's producer boundary (H3 item 11), one entry per requested key in stage-major/key order (NE:3288-3292, unchanged).
- **Fault and cancellation** keep "no facts, no Coverage entries and no Run" (NE:3837-3843).

### 2. The closed-world key (NE:3529)

H's item 13 checks two §4.5 record laws over a stage's facts and refuses a contradiction on NE §10's producer row, but "is wired only after FA-1 adds that key to NE:3529's producer-boundary row" (H3:451). The row gains, word for word:

> ; **a Coverage entry whose `closedWorld` contradicts a §4.5 record law at the producer boundary** (`native.coverage-closed-world-mismatch`, contract successor FA-1): `deadCodeRepairEligible` true while `exportsClosed` is not `closed`, `entryPointsRecognized` is not `all` or `nonliteralLoading` is not `none`; or `nonliteralLoading=none` beside an `unresolved-edge` fact of class `require-nonliteral`, `dynamic-import-nonliteral`, `reflective-access` or `indirect-eval` admitted from the entry's own stage

The two laws are NE:2237-2239 ("`deadCodeRepairEligible` is true only with `exportsClosed=closed`, `entryPointsRecognized=all` and no nonliteral loading") and NE:2221-2222 (ingredient 3, the four nonliteral classes). The row's class, code and carrier do not change: `operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION`, operational record. That is MJ row 30 (MJ:676), the route H item 22 already gives the closed-world refusal "once FA-1 is accepted".

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects. The owner may reverse any of them.

**LD-A1. FA-1 carries both halves of H's FA-1 row.**
- The lead's assignment names the X-H2 fix. H3's successor table defines FA-1 as that fix **and** the NE:3529 key, and H2's closed-world wiring waits on it (H3:809, H3:832). Splitting would leave that leg with no successor.
- **Rejected:**
  - **X-H2 only.** H3's FA-1 row would be half done, and H-C13 would stay test-only with no unit to wire it.
  - **A separate FA-1b for the key.** A second review round for one insertion on a disjoint line of the same document.

**LD-A2. The fix is NE prose. The reference triple is not overridden, and the text says it governs.**
- NE:3837 names `stage_authority`, `run_termination` and `StageAuthorityV1` as the reference of this paragraph. Both model files return `factsAdmitted: "before-terminal"` for `budget-exhausted` and `unavailable` (the B-S9 copy at lines 3729 and 3733, NEM v2 at lines 3720 and 3724), and NC asserts it (case with `"$b.factsAdmitted": "before-terminal"`, NC:13342). The passage therefore states the record value, `none`, and that where the reference disagrees "this text governs and the reference is the defect". That is NE's own rule for its other reference implementation (NE:708-710).
- `none` is a member of the registered enum (`NES#/$defs/StageAuthorityV1/properties/factsAdmitted`: `all`, `before-terminal`, `none`), so the stated value is schema-valid. `before-terminal` stays a registered member that no terminal produces.
- The reference refresh is owed (finding FA1-F1).
- **Rejected:**
  - **Line overrides of the two model copies plus a JSON Pointer override of the case.** A model and case change needs the native checker rerun, a machine job this docs-only unit does not do. On this Mac the native model also refuses Python 3.14.6's Unicode data as an environment fault (B-S9 README, "Not claimed"). It would also tie FA-1 to B-S9's copy selection.
  - **Removing `before-terminal` from the enum.** NES is registered bytes (its raw SHA-256 is a `payloadSchemaDigest`, NE §10), and the product's generated `Native2StageAuthorityV1FactsAdmitted` (`crates/contracts/src/generated/evidence.rs`) would change.
  - **Silence about the reference.** NE's own paragraph heading would cite a function that contradicts it.

**LD-A3. The discard covers the occupancy companions, and the pre-Analyze case is stated.**
- H item 4 discards "every fact candidate and every occupancy companion of that Analyze" (H3:247). A companion is captured only after "minting fact2 from this batch's candidates" (NE:3099-3101), so with no candidate admitted none can bind. Saying so avoids a reader looking for a companion rule.
- A pre-Analyze `Unavailable` has no Analyze and no candidates; its Coverage is §9.7's host conversion (NE:3227-3268), which H mints (H3 item 11). The text says so rather than calling that Coverage "the terminal's".
- **Rejected:** a bare "candidates are discarded", which leaves both cases to inference.

**LD-A4. Form: three line overrides of NE, two of them replacements.**
- NE:3849-3850 must withdraw a clause, so those two `after`s replace their lines. NE:3529 is insert-only.
- The paragraph's other lines are untouched, so the incomplete-inputs rule (NE:3843-3848) and the primary-deficiency route (NE:3851-3855) keep their bytes.
- **Rejected:**
  - **A §0 row** recording the dispositions as retained. §0 lists superseded selectors (NE:108), and nothing is superseded here. NE:138, §0's last row, is also overridden by FA-2, which would force a binding order.
  - **An override of NE:3837 or NE:3851.** Neither line is false.

**LD-A5. The closed-world key's reach.**
- It is checked at the producer boundary only, over the facts of the entry's own stage, which is exactly H item 13's scope (H3:448-450). It is not added to Run closure: the retained-record inspector recomputes "only the bijection and the RC-2 preconditions" (NE:3005-3007), and H calls it an H extension (H3:452).
- It is an internal key on an existing row, like the §4.1a keys beside it. It is not a `DomainDetailCode` and not a key of `NES#/x-opensip-public-route-registry`, whose scope is the capability and Coverage-cause guards; none of the §4.1a keys is in either. No public code is added.
- §9.5 (NE:3005-3007) is not changed: it says what the host recomputes, and a cross-check of a producer claim recomputes nothing.
- The two halves meet on a clean non-Complete terminal: no fact is admitted there (half 1), so only the first law can refuse a terminal entry.
- **Rejected:** a universe-wide check (NE:2221-2222 says "in the universe"). H's admission sees one stage's facts in its provisional view; a contract wider than its only checker would be unmet.

## FA-2 and the other drafts on NE

**FA-2 touches none of FA-1's lines.** FA-2 r2's NE overrides are lines 93, 138, 1913, 1927, 2791, 2814, 2884, 2990, 3235, 3279, 3292, 3313 and 4195. FA-1's are 3529, 3849 and 3850. So no binding order needs coordinating: FA-1 used other selectors by construction, and it kept off NE:138 (LD-A4). `verify_scratch.py` binds FA-2 then FA-1 and FA-1 then FA-2 on top of the 82; both pass with 84.

**They agree in substance.** FA-2's §9.8 already says a clean `BudgetExhausted` or post-Analyze `Unavailable` "carries none" of the census, and that "a fault, a cancellation or a missing `Complete` admits no census (§10)" (`fa-2/section-9-8.md:75-80`). FA-1's §10 text is the rule that sentence leans on. Neither depends on the other being bound.

**The other unbound drafts are disjoint too.** `rust3-lim` overrides NE 123, 2790, 2883, 2942, 3028 and 3070; SYN-1 overrides NE 288, 306, 3366, 3530 and 3541; SD-5 (`supervisor-d/sd-5/`, drafted beside this unit) overrides NE 3540. The bound overrides on NE are B-S1's eleven (714, 719, 730, 731, 822, 824, 863, 931, 939, 940, 4135). `build_fa1.py` asserts all of this.

## Not changed, and why

- **NE §0** (NE:108-145). It supersedes no candidate disposition (H3:859; `check_fa1.py` shows NE never names one), and nothing is superseded now.
- **§9.7's terminal coverage** (NE:3288-3292). It is true as written; FA-2 overrides NE:3292.
- **The startup law and its product copy** (`provider-startup.schemas.v1.json` and `startup.v1.schema.json`, `/x-opensip-startup-law/coverageFrames/terminals`). It states the terminals' Coverage and says nothing about candidates; FA-2 overrides that pointer for the census only.
- **ENC's owed symbol inventories** on these terminals (`partial` / `budget-exhausted`, `unavailable` / `provider-unavailable`; H3 item 4). They are the enumeration contract's rule (ENC:120-121), unchanged.
- **The reference triple** (LD-A2; finding FA1-F1).

## Cross-law items and findings

| ID | For | Item |
|---|---|---|
| **X-FA1-H** | M3-H's next revision | Item 4's "Only one clause of NE:3849-3850 is not applied" becomes "NE:3849-3850 as FA-1 states it". Item 13's wiring and H-C13 open once FA-1 is bound (H2's gate, H3:832). No rule changes. |
| **X-FA1-D** | M3-D's next revision | F7 (MD:623, MD:1107) is answered: item 20 cites NE:3849-3850 as FA-1 states it. |
| **X-FA1-J1** | M3-J1's next revision | Record only: row 31's basis NE:3844-3855 now reads as FA-1 states it. The route is unchanged. |
| **FA1-F1** | the native reference owner | `stage_authority` in both model files (the B-S9 copy at lines 3729 and 3733, NEM v2 at lines 3720 and 3724) returns `factsAdmitted: "before-terminal"`, and NC:13342 asserts it. Both should become `none`, by B-S9-copy line overrides and a case override, in a unit that reruns the native checker on a host whose Python the model admits. Until then NE:3850 governs. |
| **FA-2** | Codex's FA-2 review | None. No shared line and no conflicting meaning. |

No owner question is raised.

## Binding

FA-1 has passage overrides only, so it binds on the `verify_design` at main `cd5958b` with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok-fa-1-r1/review.json`;
- complete `fa-1-unit.json` (`ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`);
- append to the product lock `{record, subjectManifest, review, assent}` pinning `fa-1/successor.json`, `fa-1-subject.json`, the review and `fa-1-unit.json`, in a binding-only product commit;
- run plain `verify_design`.

Selecting FA-1 changes no product byte and no generation source. Nothing is staged tonight: the product is read-only for this run.

**Evidence runs** (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read-only):
- `build_fa1.py`, then `build_fa1.py --check`: identical bytes.
- `check_fa1.py`: pass.
- `verify_scratch.py --rev cd5958b` and on the main checkout at `cd5958b`: FA-1 binds, 82 to 83 contract successors, with three overrides and no supersession. The selected inventory and inheritance are unchanged. FA-2 in both orders and SD-5 in both orders bind, 84 each. A later override of NE:3849 refuses with "conflicting contract passage overrides". On the checkout, 40 generation sources are verified.

## Controls owed by the implementing units

They are H's, unchanged; FA-1 makes them lawful against NE:
- **H-C3** (H2, H5): a clean `BudgetExhausted`, and a clean post-Analyze `Unavailable`, after `FactBatch` frames: zero `fact2`, every terminal entry admitted, the stage `partial`, MJ row 31's route.
- **H-C13** (H2): `deadCodeRepairEligible: true` beside a `require-nonliteral` edge refuses `native.coverage-closed-world-mismatch` on MJ row 30. It is wired once FA-1 is bound.
- **D3-T22** (D3): a fault after some `FactBatch` frames discards every candidate (MD item 20). Unchanged.

## Not claimed

- No product code, test, build or checker run was made. Only the three evidence scripts ran, read-only.
- The native reference checker was not run, and neither model file was imported: `check_fa1.py` parses them with `ast`.
- No law is amended. No public code, class, exit, frame, protocol member, limit or schema member is added or removed.
- No Linux claim.
