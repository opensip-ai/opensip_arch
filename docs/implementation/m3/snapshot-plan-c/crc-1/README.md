# CRC-1 — the core role closures (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r4, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs an independent `ACCEPT-DESIGN-UNIT` (Grok reviews r4) and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-C** names successor **CRC-1** (MC:1052): "Item 9: the core detector, adapter and provider closures; the `manifestDigest` text; field restrictions, including r6's two uses of the core provider closure (import producer; syntax-universe producer) and its `semanticClosures` membership exactly when a syntax universe is selected (E1's X-C1); the detector join; a vector". It is the identity owner's successor in EC1's pattern (MC:444-450), and it answers owner question R1 (MC:1210). It also carries the identity-schema `closureKinds` and `closureMembership` text that item 9 needs. CRC-1 and CR-1 must both be accepted before C2a (MC:1076, MC:1086).

**Law standing.** This unit was commissioned against r6 (`PROPOSAL-r6.md`, `8274bca1…`). CODEX2 accepted r7 while it was being drafted (arch `0b19b6886`). r7 changes only item 16's row 8 (SD-6) and R1's wording. Item 7, item 9, the successor rows and the gates are word for word r6's. This README cites r7's lines, which are r6's plus 11 (MC:414-477 is r6:403-466).

**Product.** Main `cd5958b` (I1-P's binding), read only. Its lock has 82 contract successors; B-S2, B-S9 and I1-P were bound after r1's base `9c11c53` (79), and X4-F1 landed with no successor. r2's record is built and checked against `cd5958b`'s lock, read with `git show`.


## r4 changes (lead, after Grok's r3 review)

Grok reviewed r3 (`reviews/grok-crc-1-r3/`) and found r2's RF-1 closed, but raised a new RF-1: this README still carried r2 text at lines 3, 22 and 205. r4 is a README consistency pass. It updates the status line, the r1-members location, the binding steps and the SYN-1F note, and corrects r3's "every candidate byte-identical" (NBO-2). The builder now emits `grok-crc-1-r4`. The nine passage overrides are byte-identical to r2's and r3's.

## r3 changes (lead, after Grok's r2 review)

r2 was reviewed by Grok (`reviews/grok-crc-1-r2/`), after the lead moved the review from GROK2 to Grok. Grok returned REQUIRED-FINDINGS with one finding, RF-1. The lead's rename of the review directory left the builder emitting `grok2-crc-1-r2`, so `--check` failed on the unit draft. r3 changes only:
- the builder's review path and its draft assessment text;
- this README's NBO-2 row, and the SYN-1F digest in cross-law item 1. SYN-1F's copy is now rebuilt on r2's strings: `73645b76…`.

The successor record's nine passage overrides are byte-identical to r2's. Two candidate pins changed: this README's and the builder's.

## r2 changes

r1 (subject `adfa0d97…`) was reviewed by GROK2 (`reviews/grok2-crc-1-r1`): REQUIRED-FINDINGS, with one required finding (RF-1) and two non-blocking observations. r1's changed members are kept in `reviews/grok-crc-1-r2/r1-members/` for diffing (the lead renamed the review directory from `grok2-crc-1-r2`).

| Item | Change |
|---|---|
| **RF-1** (the `selectionLaw` sentence) | Row 5's insertion said that the core provider closure "is never selected otherwise, explicitly included". After the parent's grant that "extra admissible retained closures may be selected explicitly", that reads as the opposite of the rule. It now ends "and is never selected otherwise, not even explicitly; the core adapter closure is never a member", GROK2's replacement verbatim. It agrees with IE:1377 (row 2), with MC:443 and with C2-T13 (MC:470). |
| **The drift check** (the coordinator's instruction) | Every CRC-1 string that states `semanticClosures` membership was checked against IE:1377. There are three: IE:285, IE:1377 and the `selectionLaw` string. IE:285's provider bullet said "and never otherwise". It now says "and is never selected otherwise, not even explicitly", the same clause as rows 2 and 5. The meaning is unchanged, because the bullet already excluded every other case. No other string states membership: the `closureKinds` note, COMP:9, WS:308, WSE:312 and DMS name fields only, and the adapter is "never a … member" in all three statements. `check_crc_1.py` now asserts that all three statements carry the same clause and that no `after` contains "explicitly included", which is the check GROK2 noted was missing. |
| **The base** | The build and check scripts default to `cd5958b`. `PASSAGES.md`'s header, `vector.json`'s `source.product` and the unit draft name it. The parents, the fixture (`2d42bb5d…`) and the selectors are unchanged from `9c11c53`. |
| **`verify_scratch.py`** | Gains `--with-cr-1`, which binds CR-1 first and CRC-1 after it. CR-1's own `--after-crc-1` covers the other order. |
| **NBO-1** (SYN-1F's live draft) | Recorded in cross-law item 1. The live SYN-1F copy has already absorbed r1's three strings, including r1's `selectionLaw` sentence, so it must take r2's. |
| **NBO-2** (the unit draft's review path) | The builder emits the review path of the current round, now `docs/implementation/m3/reviews/grok-crc-1-r4/review.json` (r4), so `--check` covers the unit draft as well. |

Nothing else changes. The nine selectors, the six parents, every other `after`, and the vector's ids are r1's.

## Short names

- **MC** is M3-C r7, accepted by CODEX2: `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` (157,110 bytes, `a1ee9386…`). Its item 9 is MC:414-477.
- **ME** is M3-E1 r3, accepted by Codex: `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`). It contains item 14b (ME:568-593), X-C1 (ME:579-583 and :691) and E3-T14 (ME:593).
- **MH** is M3-H r1: `docs/implementation/m3/fact-admission-h/PROPOSAL-r1.md` (`69f50bb1…`), the bytes Grok reviewed with REQUIRED-FINDINGS (`reviews/grok-fact-admission-h-r1`). It contains item 18 (MH:521-548), its row "C r7 / CRC-1" (MH:685) and X-H3 (MH:734-740). r2 (`PROPOSAL-r2.md`, `4ae48f09…`) appeared during drafting. It carries item 18's producer bullet, the row and X-H3 word for word (r2:624-628, :770, :819), and Grok again returned REQUIRED-FINDINGS, on anchor routing rather than X-H3 (`reviews/grok-fact-admission-h-r2`).
- **EC1** is the bound core evaluator closure successor, `docs/implementation/m2/core-evaluator-closure-ec1/`.
- **X12** is X12 r4, accepted: `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md` (`adc9a88a…`). Its item 2 defines the bundled pack registry, "compiled into the signed core".

The parents, all accepted inputs of the lock at `cd5958b` (and at `9c11c53`):
- **IE** `docs/v2/contracts/product-v1/identity-and-evidence.md` (135,448 bytes, `c82404f3…`).
- **IDS-L** `docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json` (198,725 bytes, `c9214f03…`). This is I1-L's complete successor copy of the identity schema bundle IDS. It carries EC1's two strings in place, so it is the selected IDS.
- **COMP** `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` (51,833 bytes, `30d4d9d2…`).
- **WS** `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (133,335 bytes, `1ee203e3…`).
- **WSE** `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md` (139,497 bytes, `4478ce1a…`), WS's selected effective copy.
- **DMS** `docs/coop/design-corrections/workflows/schemas/evaluator3/detector-manifest.schema.json` (2,043 bytes, `1cbd69c9…`).

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: all nine overrides, each with the exact `before` and the candidate `after` |
| `successor.json` | the contract successor record: six parents, nine passage overrides, no supersession, six candidates |
| `evidence/vector.json` | generated: the five closures of EC1's `baseline-macos` core inventory |
| `evidence/build_crc_1.py` | builds the generated files, the record, the subject manifest and the unit draft deterministically; `--check` compares instead of writing |
| `evidence/check_crc_1.py` | read-only, independent content checks |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, plus a second-override probe |
| `../crc-1-subject.json` | the subject manifest (generated) |
| `../crc-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes

There are nine passage overrides. Every one only inserts text: its `after` keeps its `before` character for character. Each line selector is on a Markdown parent and each JSON Pointer on a JSON parent. `PASSAGES.md` has the full texts.

| # | Parent | Line or pointer | Change |
|---|---|---|---|
| 1 | IE `docs/v2/contracts/product-v1/identity-and-evidence.md` | 285 | After the S1 projection and detector-listing paragraph (IE:279-285), a new paragraph, **Core role closures**. It sets out the three projections; their `manifestDigest`, which also covers EC1's kind-`evaluator` wording at IE:273 and IE:455 for every core role closure; and the rule that a core role closure is never a component-manifest closure. It defines a core role closure of a Plan, gives each closure's admitted fields, states the **detector join**, and records retention and the identity consequence. |
| 2 | IE | 1377 | The `semanticClosures` paragraph (IE:1370-1377) gains the exception. The core provider closure is a direct member exactly when a syntax universe is selected, and is never selected otherwise, not even explicitly. The core adapter closure is never a member. |
| 3 | IDS-L `docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json` | `/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact` | appends "for the core detector, provider and adapter closures, the same TR-CORE-signed core inventory body bytes" |
| 4 | IDS-L | `/x-opensip-digest-domains/closureKinds/note` | appends the three projections and each one's admitted fields; `byField` is unchanged |
| 5 | IDS-L | `/x-opensip-digest-domains/closureMembership/selectionLaw` | appends the same exception as row 2 |
| 6 | COMP `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` | 9 | After "A provider or evaluator closure cannot stand in for it.", inserts the bundled-pack case. `detectorClosure` is the core detector closure: its descriptor equals the seal's evaluator-closure descriptor except for `kind`, and its `contributionId` is in the pack row's `contributions`. It is a distinct closure. Another core's detector closure cannot stand in either. |
| 7 | WS `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | 308 | "`closure.manifestDigest` continues to identify the component manifest body." gains the core role closure case. For a core role closure (a bundled pack's core detector closure, for example), `manifestDigest` is the core inventory body, and the listing is the reserved file of the core platform tree. |
| 8 | WSE `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md` | 312 | the same as 7 (WSE:312 is WS:308's effective copy) |
| 9 | DMS `docs/coop/design-corrections/workflows/schemas/evaluator3/detector-manifest.schema.json` | `/description` | After "never this three-field listing.", the same core role closure case as 7 |

Nothing else changes. `closureKinds.byField`, the closure kind list, every schema shape, H domain and recipe, the enumeration and execution-input schemas, every registry, generated file, product copy and inventory keep their bytes and meaning. The check script shows that the three IDS-L strings are the only change to that document.

## The rule

The texts say the following.
- **Three more projections.** A core release has five closures from one descriptor D, security's selected-platform projection of the authenticated core inventory: the core closure (`kind: core`, security's own, never an identity closure kind), the core evaluator closure (EC1), and now the **core detector**, **core provider** and **core adapter** closures. They differ only by `kind`.
- **`manifestDigest` and `tree`.** For every core role closure, `manifestDigest` is the raw SHA-256 of the TR-CORE-signed inventory body, and `tree` is the platform's regular files.
- **Not component manifests.** No core role closure is ever admitted through a component manifest, a catalog release or CR-1's role table.
- **Recognition.** A closure is a core role closure of a Plan exactly when its descriptor equals, except for `kind`, the descriptor of the core evaluator closure that the Plan selects and the seal names.
- **The admitted fields.** Any other field refuses, `cache-key.producerClosure` included.
  - **Detector:** the `detectorClosure` of each emission row whose rule comes from a pack of the core's bundled pack registry, and so those findings' `finding.ruleClosure`. **The detector join**, checked at Run closure: every bundled-pack emission row names the Plan's core detector closure, and its `contributionId` is in the pack row's `contributions`.
  - **Adapter:** only `import.adapterClosure` of a `dependency` or `prepared` import. Never a `semanticClosures` member.
  - **Provider:** exactly two uses under one identity:
    1. `import.producerClosure` of a `dependency` or `prepared` import;
    2. the producer of syntax-universe work, only where the universe is a `native.semantic-universe.syntax.v2` identity. The fields are `subject-scope.enumeratorClosure`, `view.producerClosure` and so `fact.producerClosure`, `stage-spec.producerClosure`, an enumeration binding's `enumerator.closureId` and `CandidateProducerResultV1.producerClosure`.

    The core provider closure is a `semanticClosures` member exactly when a syntax universe is selected. It never produces a TypeScript or Rust record. Like any stage producer, it registers its syntax stages' output schemas as core platform tree members (IE:1303-1318).
- **Consequences.** Retention is EC1's: the body and tree are stored once per store. Every core release is a new detector, provider and adapter closure, so Plans and Runs that select them get new identities. Historical records keep their bytes.

This is MC item 9 (MC:414-477) and ME item 14b (ME:568-593), clause for clause. The checker asserts that the IE paragraph names every field and condition.

## Why this form: the lock, selector by selector

`build_crc_1.py` reads the lock at `cd5958b` and refuses any selector that a bound successor already overrides.
- **IE:273, IE:278 and IE:455 are taken.** They hold the `manifestDigest` sentence, EC1's paragraph and the `raw-artifact` row, and all three carry EC1's bound overrides. A second override refuses ("conflicting contract passage overrides", `verify_design.py:381-383`), and `verify_scratch.py`'s probe shows the refusal. CRC-1 therefore leaves them untouched. Its new paragraph at the free line 285 says that their kind-`evaluator` wording holds equally for every core role closure (LD-2).
- **The original IDS is taken.** It carries four bound pointer overrides, two of them EC1's on exactly the strings CRC-1 extends. Its selected successor, I1-L's complete copy IDS-L, has those strings in place and no bound override, so CRC-1's three pointers on IDS-L are fresh keys (LD-1).
- **The other six keys are free:** IE:285, IE:1377, COMP:9, WS:308, WSE:312 and DMS `/description`. Nothing overrides them, whether bound at `9c11c53`, bound since then up to `cd5958b`, or drafted and unbound in arch tonight:
  - B-S2, bound at `240a795`, uses IE:542 and :547;
  - SYN-1 uses NE lines;
  - FA-2 uses NE lines and the startup schemas;
  - SYN-1F uses the execution-input contract's line 257 and complete copies, IDS-L's included (cross-law item 1).

## The vector

`evidence/vector.json` takes the product fixture `crates/security/tests/fixtures/core-inventory318.ndjson` at `cd5958b` (2,129,737 bytes, `2d42bb5d…`, unchanged since EC1 and `9c11c53`), case `baseline-macos` (platform `macos-aarch64`). The inventory body is 5,990 bytes, and the core descriptor is held once. The five descriptors differ only by `kind`:

| Kind | `closure2` | Canonical descriptor SHA-256 |
|---|---|---|
| `core` | `closure2:54322a2c18a7ed6d5a2c92ab7e1204884e7095cfc254d40d352f879761fa118d` | `b1158c4b…` |
| `evaluator` | `closure2:7da97b9a4686fe5dc6ff69d83ddde230ac6895afb699717f2ef07a05810b89e2` | `2e777ad0…` |
| `detector` | `closure2:be7bd6cc99990375edfc652b38f48fa5c51677970849b1dca3282245b0503c66` | `b795a299…` |
| `provider` | `closure2:df5e7cbab37c1ebccf867d343eaeb5d2739103492896e87d238a80efa1b8e662` | `5b1ca657…` |
| `adapter` | `closure2:670d260fd9956436fe1ef014d14ca18fb923e223f9a7f514a6fe4043fe36a0bf` | `9c60b40d…` |

The core value is the fixture's own expected closure. The core and evaluator values equal EC1's vector, whose pin is recorded. Across all 53 accepted fixture cases, the five ids of each case are pairwise distinct. The three new descriptors fit IDS-L's closed `closure` shape and kind list. C2a reproduces the vector byte for byte in a Rust test of `core_inventory`, as X3d-3 did for EC1. This is MC's control C2-T9.

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them.

**LD-1. Pointer overrides on the selected IDS copy, and fresh-line overrides elsewhere. No complete copies.** Every IDS change is a string, so JSON Pointer overrides on IDS-L carry it. That is EC1's form, applied to the copy EC1's meaning now lives in.
- **Rejected: overrides on the original IDS.** Two of the three pointers are EC1's and refuse. The original is also no longer the selected text, because I1-L's copy superseded it.
- **Rejected: a new complete IDS copy.** No array or structure changes, so nothing needs a copy. A copy would also be a sibling of the IDS copy SYN-1F must make for its `NativeCause` enum append, and one of the two would have to be rebuilt on the other.
- **Rejected: a complete copy of IE.** That would move the selected IE for every successor in flight (B-S2's IE:542 and :547, VCS-1, NIJ-1's identity citations), for the sake of two parentheticals.

**LD-2. EC1's kind-`evaluator` wording is extended by a later passage, not rewritten.** IE:273 and IE:455 cannot be overridden again. The CRC-1 paragraph states that they hold equally for every core role closure. IDS-L's `manifestDigest` artifact string, which is the authoritative annotation, is extended directly (row 3).
- **Rejected:** leaving the general sentence implicitly false for three new kinds; a complete IE copy (LD-1).

**LD-3. One core per Plan.** A core role closure is recognized as the Plan's core evaluator closure descriptor with another `kind`. MC fixes this for the detector ("from any core other than the seal's evaluator's", MC:464), and its "the same D" (MC:431) fixes it for the provider and adapter.
- **Rejected:** admitting any authenticated core's projections. That needs a signature-level join at Run closure that no contract defines, and it would let an older core's detector stand in, which MC forbids.
- **Disclosed:** a persistent M5 import made under an older core would refuse under this rule. M5's import successor owns that case. At M3 imports are invocation-scoped (MC item 11), so no M3 import is affected.

**LD-4. The admitted fields are a closed list, and any other field refuses, `cache-key.producerClosure` included.** MC's C2-T13a has "refuses in any other field", and C mints no `cache2` at M3 (MC item 16).
- **Rejected:** admitting `cache-key.producerClosure` for syntax stages now. Cache keys belong to L item 3, and a later successor that admits one must name it.

**LD-5. No new refusal code.** A misused core role closure refuses through the field's existing closure-kind and membership refusals at admission and at Run closure. The detector join in replay uses X5's structural row, as MC item 19 wires it.
- **Rejected:** new codes, under the owner's no-new-codes rule.

**LD-6. Consequential passages are included.** WS:308, WSE:312 and DMS `/description` would be false for a core detector closure that carries a compatibility listing. COMP:9 is where the composition contract says what may stand in for a detector, so the detector join belongs there too. All are insert-only (I1-L's LD-L4 and LD-L5 precedent for WS and WSE).
- **Rejected:** leaving them inexact; holding them for a law revision.

**LD-7. Product copies keep their bytes.** The product copies are I1-L's PIDS copy, the product's `schemas/sources/detector-v1.schema.json` and the generated `apps/report/src/generated/report.ts`. This is EC1's rule: annotation prose that no code dispatches on, and no generation-source, registry or drift change. `verify_scratch.py`'s checkout mode confirms that the generation sources still verify.
- **Rejected:** overriding product copies. EC1 chose not to, and I1-L's PIDS copy keeps EC1's text out.

**LD-8 (X-H3, M3-H r1): CRC-1 does not resolve X-H3. It is left to M3-C's next revision (r8) and a follow-on identity successor, CRC-2.** X-H3 (MH:734-740) asks MC's next revision and CRC-1 for a third use of the core provider closure. That use would make it the producer and enumerator of the three inventory relations' records in every universe, a `semanticClosures` member whenever an inventory cell is requested, with one host inventory stage per universe in `exec-plan2` (MH:685). The reasons for leaving it:
1. **The accepted law says the opposite.** CRC-1 carries MC item 9, and MC forbids exactly this: "It is never the producer of any TypeScript or Rust record" (MC:443), the forbidden substitute "the core provider closure on a TypeScript or Rust record" (MC:464), and C2-T13a's refusal leg (MC:474), which is E1's E3-T14 (ME:593). A contract successor carries its law and does not amend it. Enacting X-H3 here would put text in force that its own law forbids, and would ask the reviewer to rule on a law change inside a design unit.
2. **X-H3 is not settled.** M3-H is not accepted: Grok returned REQUIRED-FINDINGS on r1 and again on r2, which repeats X-H3 unchanged. The recommendation also changes C's Plan shape (item 16's `semanticClosures` row and stages) and C's controls (C2-T13 and C2-T13a), which are the law's to decide. Grok's ruling R5 agrees on the order: the third use "is lawful only as a successor" and "H does not apply it before C r7 / CRC-1" (`reviews/grok-fact-admission-h-r1/REVIEW.md:42`).
3. **The timing allows it.** CRC-1 gates C2a, which is on the host chain from day 0. X-H3 gates only H3's TypeScript and Rust leg and C4a's start, on day 16 (MH:715). Bundling an unsettled item would put C2a at risk, and with it C2b, C2c and E2b, for no schedule gain.
4. **r7 was a single-item amendment** (SD-6), and it has now been accepted. Folding X-H3 into it was never open.

**Rejected:**
- (a) enacting the third use in CRC-1 (reason 1);
- (b) folding X-H3 into C r7 (reason 4);
- (c) a conditional clause in CRC-1 ("unless a later successor admits it"), which is not bindable meaning and names no rule;
- (d) attributing TypeScript and Rust inventory records to the language provider's closure, which is false attribution (MC:458; MH item 18);
- (e) a new closure kind for host inventory records: `closureKinds` is closed, the producer fields require `provider`, and MC and EC1 both reject new kinds (MC:460).

**How CRC-1 keeps the follow-on cheap.** CRC-1's closed lists sit at its own selectors (IE:285, IE:1377 and the IDS-L note and `selectionLaw`). `verify_design` refuses a second override of any of them (the probe in `verify_scratch.py`), so CRC-2 cannot rewrite them. CRC-2 should:
1. add its IE text at a fresh line, for example as a paragraph replacing the blank line IE:286 that follows CRC-1's paragraph, and say that it adds a third use to CRC-1's list;
2. carry its IDS text on whichever IDS copy is then selected. If SYN-1F's copy has been bound with CRC-1's strings carried in place, CRC-2's pointers on that copy are fresh. Otherwise it overrides other IDS-L strings or makes the copy itself.

**Recommendation:** draft C r8 once M3-H is accepted, taking X-H3 together with C2-T13, C2-T13a and item 16, and accept CRC-2 before C4a starts (MH:715, day 16).

**LD-9. Binding.** After acceptance the lead appends CRC-1's `contractSuccessors` entry to `design-lock.json` in a binding-only product commit, D3's and I1-L's form, before C2a. Binding changes no product byte and no generation source.
- **Rejected:** binding inside C2a's commit, which would mix review subjects.

## Cross-law items

1. **SYN-1F (E1, drafted separately tonight, unbound).** SYN-1F's `NativeCause` enum append needs a complete IDS copy. Its draft makes one from IDS-L, at `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json`. Both units are pre-day-0, so whichever binds second takes the other in.
   - **If CRC-1 binds first,** SYN-1F's copy must carry CRC-1's three strings in place (I1-L's LD-L2), and its README and copies report should list them.
   - **If SYN-1F binds first,** CRC-1's three IDS overrides are re-pointed to SYN-1F's copy before binding. Their `before` texts must equal the strings in SYN-1F's copy as bound, so they are re-checked against it. This changes only the record, so it needs a short rebase-only re-review.
   - **The live draft (GROK2 NBO-1; resolved).** The SYN-1F copy on disk (200,510 bytes, `73645b76…`) was rebuilt on CRC-1 r2's strings, so its `selectionLaw` sentence is r2's corrected one ("not even explicitly"). r3 and r4 change no string, so SYN-1F's copy stays valid; only its parent pin on this record moves.

   `verify_design` does not enforce selection, so review must hold this (B-S9's residual hazard). The lead should tell SYN-1F's drafter.
2. **E1 and core packaging.** The core provider closure produces each syntax stage, so the syntax stage output schema must be a member of the **core platform tree** at `opensip-interface/stage-output/<operation>.schema.json` (IE:1303-1318). E1 owns the interface (MC:917). E2/E3, and the core inventory builder (463h's successor), must ship it in the signed core tree. Otherwise C4a's stage spec refuses `STAGE_OUTPUT_SCHEMA_UNREGISTERED`.
3. **NIJ-1 (native).** NE's import passages (NE:2650-2732) should name item 13's producer and adapter as CRC-1's core provider and core adapter closures. CRC-1 changes no NE text.
4. **X-H3** (LD-8): M3-C r8 and CRC-2, accepted before C4a starts.
5. **MC r7.** CRC-1 agrees with r7's row 8. The core evaluator and detector closures are core-inventory projections, never component manifests, and R10a never admits them. The same holds for the core provider and adapter closures.
6. **M5.**
   - Cross-release baseline comparison needs the core tree's detector compatibility listing (MC:451). Security S1's receipt field `componentManifestDigest` (SL:60-63) then carries the core inventory body's digest for that closure. That receipt is M5 work, and CRC-1 does not rename it.
   - The rule for older-core imports is LD-3's disclosure.

## Points for the reviewer

- **R1 (MC R1).** Are the three projections and their admitted fields exactly MC item 9 with r6's X-C1, neither wider nor narrower? Is the closed list right, including `cache-key.producerClosure` refusing (LD-4)?
- **R2 (form, LD-1 and LD-2).** Are pointer overrides on IDS-L, plus a later paragraph that extends EC1's taken lines, a sound successor of EC1's meaning? Is the coordination with SYN-1F stated correctly?
- **R3 (recognition, LD-3).** Is "the Plan's core evaluator closure's descriptor with another kind" the right test at admission and at Run closure?
- **R4 (consequential passages, LD-6).** Are WS:308, WSE:312 and DMS `/description` needed, and does any other accepted passage still say that a closure's `manifestDigest` is always a component manifest body? EC1's IE:273 and IE:455 are handled by LD-2.
- **R5 (X-H3, LD-8).** Is leaving X-H3 to C r8 and CRC-2 right, and is the follow-on's binding path sound?
- **R6.** The vector, and well-formedness under `verify_design`'s `contract_successor` and `successor_chain` rules.

## Binding

CRC-1 binds on the `verify_design` at main `cd5958b`, on top of all 82 contract successors, with no prerequisite. r1 also bound at `9c11c53`, on top of 79. After `ACCEPT-DESIGN-UNIT`:
1. copy the accepting round's review into its directory, `docs/implementation/m3/reviews/grok-crc-1-r<N>/review.json`, where the builder's emitted path names N;
2. complete `crc-1-unit.json`: status `ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`;
3. append the four pins to the product lock;
4. run plain `verify_design`.

CR-1 is independent: the two units share no parent, and they bind in either order.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read only. Nothing ran cargo, a test or a product tool other than `verify_design` in the scratch harness. Each run below was made twice.
- **`evidence/build_crc_1.py`**, then `--check`, which reported identical bytes for every generated file, the unit draft included.
- **`evidence/check_crc_1.py`** (default `cd5958b`) passes, and so does `--rev 9c11c53`. It checks:
  - pins, `before`s and inserts, and the IDS-L mask;
  - the paragraph's clauses, and r2's three agreeing membership statements;
  - the vector and all 53 fixture cases;
  - that this README names every passage.
- **`evidence/verify_scratch.py --rev cd5958b`** (design-only) passes:
  - the base lock has 82 successors and passes;
  - with CRC-1 appended there are 83, and the lock passes, with nine overrides and no supersession;
  - the selected inventory is unchanged (`repository-file-inventory.v134.json`), and so is the inheritance projection (55 rows);
  - the second-override probe refuses with "conflicting contract passage overrides".
- **`evidence/verify_scratch.py`** on the checkout at `cd5958b`: 82 to 83, with 40 generation sources and 48 admission sources (15 aliases) verified.
- **Together with CR-1, in both orders:**
  - `evidence/verify_scratch.py --rev cd5958b --with-cr-1` binds CR-1 then CRC-1, 82 to 84;
  - CR-1's `evidence/verify_scratch.py --rev cd5958b --after-crc-1` binds CRC-1 then CR-1, 82 to 84.
- **At r1's base:** `evidence/verify_scratch.py --rev 9c11c53` still binds, 79 to 80.

## Not changed, and noted

- **ENS and EXS keep their bytes.** These are `enumeration-plan.schema.v1.json` (`enumerator.closureId`) and the execution-input schema (`CandidateProducerResultV1.producerClosure`). Their own joins, a Plan-selected provider closure and a producer equal to the binding's enumerator, already admit the selected core provider closure. The universe restriction is the identity rule.
- **NE is unchanged** (NIJ-1's). **SL is unchanged** (CR-1 adds the role table there).
- **No refusal code, class, exit or route is added.**
- **Not claimed:**
  - No product code, test or build was run.
  - The reference checkers (`check-identity.py`, the native checker) were not run.
  - The vector is computed with the same canonical form EC1 used, and validated against the fixture's own expected core closure.

## Owner flag

As with EC1 (MC O-2; ME owner note 4), every core release becomes a new detector, provider and adapter closure. Every Plan that selects one, which means every bundled-pack Plan and every syntax-universe Plan, gets a new identity with each release.
