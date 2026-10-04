# SYN-1 — the native contract successor of law M3-E1 (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code or public code. It needs `ACCEPT-DESIGN-UNIT` from an independent reviewer and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-E1 r3** (`../PROPOSAL-r3.md`, 117,273 bytes, `d71031ff…`, accepted by Codex) names its successors in item 19. This unit is the **SYN-1** row (E1:689), parts (a) to (f):
- (a) the `NativeCause` member `source-parse-error`, lawful only under `input-closure-incomplete`, with the NE §10 row;
- (b) the per-file outcome law, for Coverage (items 10 and 11) and for `clones-near` envelopes (item 14a);
- (c) the data-document "format definition, no parse" sentence (item 8);
- (d) the pre-Plan route row for every `native.syntax-grammar-*` and `native.syntax-normalizer-*` key;
- (e) the `backend-fault` route (item 10);
- (f) no startup-schema change.

SYN-1F (`../syn-1f/`) carries the foundation mirrors and binds with it. SYN-NS (`../syn-ns/`) is the normalizer specification.

**The branch is T-native.** Probe E0 is complete (`../E0-REPORT.md`, 30,730 bytes, `c1011e83…`, arch `c87d311f4`, a record in GROK2's review): P5 failed at a median of 0.818 MiB/s, so under E1 item 3 the manifest's `executionModel` is `native-linked-v1` and item 18's fallback posture applies. **This unit is written for `native-linked-v1`.** Text for `wasm32-fuel-v1` stays only where E1 itself keeps both branches, and it is marked **inactive unless the lead's M4 re-decision selects it**.

**Product.** Main at `cd5958b` (I1-P bound, 82 contract successors), read only. The record is built against it. It also binds on `15c0779` (81), the lock the lead named before I1-P was bound.

## Short names

E1 is M3-E1 r3 (the snapshot above). E0 is the E0 report. NE is `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes, `83b99783…`). NES is `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (277,967 bytes, `2d37b810…`). PNES is its selected product source copy, `docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json` (280,357 bytes, `e5834d37…`), which product main's `schemas/sources/native-v2.schema.json` equals byte for byte. NEM is `native_evidence_model.v2.py` beside NES; B-S9's copies (bound at `8adfe0c`) are the selected native reference. J1 is `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md` (accepted, `c18c0d3c…`). C6 is `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r6.md` (accepted, `8274bca1…`). CRC-1 is M3-C's closure-role successor, `docs/implementation/m3/snapshot-plan-c/crc-1/`, in GROK2's review.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: every override, with its exact `before` and `after` |
| `successor.json` | the record: three parents, five passage overrides, ten candidates |
| `design/native/native-evidence.schemas.v2.json` | NES's successor copy (generated) |
| `product/schemas/sources/native-v2.schema.json` | PNES's successor copy (generated) |
| `materialization-map.json` | generated: the product source E2s copies |
| `evidence/build_syn_1.py` | builds every generated file, the record and the subject; restates verify_design's rules for this record |
| `evidence/check_syn_1.py` | read-only content checks, written independently of the build |
| `evidence/verify_scratch.py` | the real verify_design with a synthetic review and assent (same bytes in all three units) |
| `evidence/copies-report.json` | generated: per copy, the parent, the edits and the changed lines |
| `../PROPOSAL-r3.md` | the law snapshot, the bytes Codex accepted (LD-10) |
| `../syn-1-subject.json` | the subject manifest (generated) |
| `../syn-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes

### Five insert-only line overrides of NE

Each `after` keeps its `before` word for word and only inserts. No accepted successor binds any of these lines; NE's bound lines are 714, 719, 730, 731, 822, 824, 863, 931, 939, 940 and 4135 (all B-S1).

| NE line | E1 source | Change |
|---|---|---|
| 288 | SYN-1 (c), item 8 | The data-document bullet gains: a data-document row is a format definition, never a parser. Its `grammarDigest` names a definition record with `parse: "none"`, no parser for it is pinned, built, linked or run, and no data-document file reaches the parser or gets an outcome. |
| 306 | SYN-1 (b), items 10, 11 and 14a | After the unbundled-language paragraph, a new section, **"Per-file parse outcomes under the syntax universe"**. It has an outcome table (`parsed`, `syntax-error`, `truncated:<bound>`, `backend-fault`) with the facts, bodies and Coverage each one gives, and then: the selected branch's residual risk; the whole-file rule; precedence in one scope; clones; **tree validation with the reserved ERROR symbol 65535**; the byte layout's status; the `clones-near` envelope, case by case; the group retention rule; no envelope after a fault; and the trust limit. |
| 3366 | SYN-1 (a) | The §10 `input-closure-incomplete` row's cause list gains `source-parse-error`, with what it names. |
| 3530 | SYN-1 (d), item 5 | A new route row after the native-context row: **syntax grammar context**. It routes the one new key `native.syntax-grammar-closure-absent` (LD-4), the eleven existing §1.2 keys and E1's admission-chain keys, split by branch, to `request-rejected` / `REQUEST.PRECONDITION_FAILED`, before PlanId. |
| 3541 | SYN-1 (e), item 10 | A new route row after the producer cause-refusal row: **syntax backend fault**, `operational-failed` / `SYSTEM.OUTCOME.ILLEGAL_STATE` (`host-invariant`) / `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>`. |

The route row names 25 keys. `check_syn_1.py` proves that each one is either one of NEM's eleven existing keys, one of the thirteen keys E1 names, or this unit's one new key, and that none is missing.

**The keys by branch** (route row):
- **Both branches:** `-bundle-manifest-mismatch`, `-definition-mismatch`, `-normalization-map-mismatch`, `-execution-model-mismatch`, `-engine-mismatch`, `-bundle-not-the-registry`, and `native.syntax-normalizer-kind-unknown`.
- **`native-linked-v1` (selected):** `-build-mismatch`, item 5's T-native binding of A9 to A11 to the compiled-in table and the linked `Language`.
- **`wasm32-fuel-v1` only (inactive):** `-module-invalid`, `-module-import-forbidden`, `-module-exports-mismatch`, `-abi-mismatch` and `-symbol-table-mismatch`.

### Two complete JSON successor copies

Each copy is its parent's raw bytes with exactly these edits in place. No byte else changes, `$id`s are kept, and no override is bound to either parent, so none is carried. `evidence/copies-report.json` lists every hunk.

| Parent | Copy | Edits |
|---|---|---|
| NES (277,967, `2d37b810…`) | `design/native/native-evidence.schemas.v2.json` (278,348, `bff7c0b7…`) | `"source-parse-error"` at new line 46 (`…/input-closure-incomplete/allowedCauses`) and new line 792 (`#/$defs/NativeCause/enum`); the registry row's `rule` at line 49 |
| PNES (280,357, `e5834d37…`) | `product/schemas/sources/native-v2.schema.json` (280,738, `93a39da8…`) | the same, at new lines 46, 49 and 827 |

- **The position.** The member goes at its code-point position, before `source-replacement-outside-snapshot`. Every copy of the list is in code-point order, so every copy gets it at the same index (LD-8).
- **The `rule` text.** It said "section 10 lists twelve of them", which becomes false. It now says thirteen and names `source-parse-error`'s meaning. Its last sentence ("A null refuses…") is kept.
- **The two copies keep their parents' relation.** The product copy differs from the design copy exactly as PNES differs from NES (the framework-recognition-parameter route key and the new-Plan carrier). `check_syn_1.py` compares the two diffs.

### What does not change: SYN-1 (f) and the rest

- **The startup schema** (`native/provider-startup.schemas.v1.json`) keeps its bytes. Its `:83` and `:610` lists are the TypeScript post-Analyze `Unavailable.reason` vocabulary, and its Coverage entries reference the native owner by URN, so they take the member through the reference (E1 E-R2-03).
- **`UnavailableReasonV3`**, `DeficiencyV2`, `UnresolvedEdgeKindV1`, the public route registry, every D9 class, code and exit, and NCM are unchanged.
- **The `NativeCause` description** is unchanged. Its claims stay true, and IDS's copy of the description stays a copy (LD-7).
- **NEM, and B-S9's selected copies of it, are unchanged** (LD-6).

## The branches

| Matter | `native-linked-v1` (selected) | `wasm32-fuel-v1` (inactive unless M4 re-decides) |
|---|---|---|
| The work bound behind `truncated:fuel` | an operation budget counted in parse-progress callbacks (E1 item 11) | engine fuel |
| `truncated:memory` | does not exist; `maxFileBytes` and `maxNodes` bound the work | `maxMemoryPages` |
| `backend-fault` | a tree that fails validation | that, or a trap other than fuel or memory exhaustion, or a module protocol violation |
| A crash, stack overflow or allocation failure in the parser | **not an outcome**: it ends the host process, a declared residual risk (item 18) | a trap: an ordinary `Err` |
| Admission keys for A9 to A11 | `-build-mismatch` | the five module keys |
| The tree's byte layout | the host's own projection of the linked runtime's tree | the shim ABI (`shimAbi` 1) |

## E0's record items

E0's report (§"E1 record items and observations") and the lead name three items. Each is resolved here or routed.

1. **The ERROR symbol 0xFFFF** — **resolved here** (LD-2). Under both branches the tree carries ERROR as symbol 65535. That is outside `SymbolTableV1`'s contiguous ids (A11) and outside "a symbol in the table" (item 10). NE's new tree-validation bullet makes it the one explicit exception:
   - 65535 is lawful exactly on a node whose `error` flag is set, and the flag is set exactly on such nodes;
   - such a node makes the file `syntax-error`, never `backend-fault`;
   - `SymbolTableV1` lists ids 0 to n−1 contiguously and never lists 65535;
   - ERROR_REPEAT (65534) never appears among visible nodes, and is not lawful there.

   E1's A11 text ("ids contiguous") needs no change under this reading. E1 item 10's "a symbol outside the table" becomes exact in NE, and E1's next revision should cite it (cross-law item E-1).
2. **The wasm headers** (`crates/language/wasm/include`, outside `lib/`) are missing from item 4's closure layout. This matters only under T-wasm, so it is **routed** to E1's next revision and to E2a, marked inactive (E-2). Neither SYN-1 nor SYN-NS states the closure layout.
3. **Eager compilation** (`CompilationMode::Eager`; E0's P4 lazy-translation control showed order-dependent fuel). This is T-wasm only, so it is **routed** to E2b and to E1's `fuelModel` text, marked inactive (E-3).

**`SyntaxTreeV1`'s layout.** E2a fixes the normative layout (LD-3). The probe layout is documented in E0's report under "`SyntaxTreeV1` as E0 encodes it"; NE cites the report and says that layout is not normative. NE states the **decoded validation law** instead, because that law decides `syntax-error` against `backend-fault`, which is a public route.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation, and names the alternatives it rejects. The owner may reverse any of them.

**LD-1. Write for `native-linked-v1`; keep `wasm32-fuel-v1` text only where E1 keeps both, marked inactive.**
- E0 chose T-native inside E1's predeclared branches, so that is the operating branch.
- E1 items 4 to 16 keep both branches, and item 18 reserves an M4 re-decision. So the T-wasm keys and outcomes stay named, so that a re-decision needs no contract successor for them.
- **Rejected:**
  - **Deleting the T-wasm text.** An M4 re-decision would then need another successor.
  - **Leaving it unmarked.** A reader could take an inactive key as live.

**LD-2. ERROR (65535) is the one exception to "a symbol in the table". It is not a table row, and the error flag must agree with it.**
- tree-sitter's builtin ERROR is a runtime constant, the same for every grammar, and not part of a grammar's generated tables. Keeping it out of `SymbolTableV1` keeps that digest a pure function of the grammar.
- Tying the symbol to the flag catches a corrupted tree in either direction.
- **Rejected:**
  - **Listing ERROR as a table row at 65535.** That breaks A11's contiguity, and makes the digest depend on a runtime constant.
  - **Remapping ERROR to id n in the serializer.** E0's P3 equivalence would then compare remapped trees, and the tree would no longer carry tree-sitter's symbol.
  - **Trusting the error flag alone.** A flipped flag on a normal node would go unseen.

**LD-3. State the decoded validation law in NE, not the byte layout.**
- The validation law decides `syntax-error` against `backend-fault`, and so Coverage against an operational failure. That is contract.
- The byte layout appears in no retained record and no public outcome. Under T-native it is the host's own projection.
- **Rejected:**
  - **Stating the layout in NE.** It would make an internal ABI a public contract, so a layout change would need a contract successor while changing no evidence.
  - **Adopting E0's probe layout.** The lead ruled it probe-only.
  - **Leaving validation to E2b.** It decides a public route.

**LD-4. A missing closure refuses with a new key, `native.syntax-grammar-closure-absent`.**
- E1 item 5 says "An installation with no admissible grammar closure cannot mint `native.context.syntax.v2`", and that the request "refuses before PlanId under the native-context route", but it names no key. E3-T1 needs one.
- **Rejected:**
  - **Reusing `native.syntax-grammar-bundle-not-in-closure`.** That presupposes a closure and says a member is missing from it.
  - **Reusing `native.native-context-closure-unretained`.** That is the TypeScript and Rust contexts' stdlib and tool closure key.
  - **No key.** NE:3543 says an unmapped detail is a model error.

**LD-5. The route is a new row immediately after NE:3530, not a widening of NE:3530's cell.**
- E1 says NE:3530's route "gains" the keys. The new row has the same class, code and carrier, so the route is the same. The keys get a readable row of their own, split by branch.
- J1's row 52 cites NE:3530's own keys by name, and those keys keep their row byte for byte.
- **Rejected:** appending about 25 keys to NE:3530's condition cell. It would mix two contexts' keys in one cell, and J1's row 52 would read as covering them when it does not (cross-law item X-J1).

**LD-6. No NEM change, so no copy of B-S9's NEM copies.**
- NEM reads NES's cause registry by data (NEM:45, `DEFICIENCY_CAUSE_REGISTRY = SCHEMAS[…]`) and restates no cause list.
- Its `D9_MAP` (NEM:3591-3618) does not carry the native-context keys of the row SYN-1 extends, so the syntax keys need no `D9_MAP` row either.
- Its §1.2 checks (NEM:2426-2478) are unchanged: steps A3 to A12 are new execution joins with no reference-model counterpart, and they belong to E2b.
- E1's row says "(NE §1.2 and §10, NES, NEM)". This unit finds no NEM byte that is false or incomplete after SYN-1, and records that as a deviation for E1's next revision (E-4).
- **Rejected:**
  - **Copies of B-S9's two NEM copies.** They would differ from their parents in no meaningful byte. A frozen model reads its siblings by fixed path, so a copy under `syn-1/` would not even load the successor NES.
  - **A `D9_MAP` row per syntax key.** It would be inconsistent with how the native-context keys are routed.

**LD-7. Descriptions change only where a statement becomes false.**
- The registry `rule` says "twelve", so it changes. The `NativeCause` description's claims stay true, so it does not.
- IDS's `evaluation-deficiency` carries a copy of that description, and that copy stays a copy.
- **Rejected:** a sentence about `source-parse-error` in the description. It is not needed, and SYN-1F's IDS copy would then have to repeat it.

**LD-8. Code-point position, not appended last.**
- Every `NativeCause` list in the design and the product is in code-point order. EXM:851 and the enumeration model's drift check compare the lists for equality (order included), and E2s-T1 requires "the new member in its owner's order".
- **Rejected:** appending last, I1-L's form (LD-L3). The op enum there is not sorted, and order was part of its proof identity. Here, appending last would break the sorted invariant every copy has.

**LD-9. The product source copy rides in this subject, in I1-L's form.** E2s re-points `schemas/source-map.json` and `schemas/admission-source-map.json` at `product/schemas/sources/native-v2.schema.json`, and copies its bytes. `materialization-map.json` gives the bytes.
- **Rejected:** leaving the product copy to E2s's own record. It would put the one reviewed member in two subjects.

**LD-10. The law snapshot `../PROPOSAL-r3.md` is a candidate,** as F8b's proposal and I1-L's law were (I1-L LD-L7). Later units, E2s's 468a-form record among them, can then name the accepted law as a parent.

**LD-11. SYN-1 and SYN-1F stay two units, but bind together: SYN-1 first, then CRC-1 if it is not yet bound, then SYN-1F, in one binding commit.**
- E1 names them as two rows with two owners: native, and identity plus execution-input.
- EXM:851 holds EXS's `NativeCause` equal to NES's. Binding one without the other would leave the selected design inconsistent, so neither binds alone.
- **Rejected: merging them.** Merging gains nothing that the joint binding rule does not give, and it would mix two owners' review lenses in one subject. The merge question was put to the lead's decision; this is the decision.

**LD-12. The backend-fault row uses only existing members; the D9 owner's assent is recorded and routed.**
- Class `operational-failed`, code `SYSTEM.OUTCOME.ILLEGAL_STATE` with `faultCause: host-invariant` (NES's `hostInvariantSuccessor`), and detail `HOST.INVARIANT_VIOLATED` with a subject. J1's rows 13, 29 and 39 use exactly this shape.
- E1 says "J1/`outcomes.rs` owns the projection". J1's row table needs this row and row 52's widening (X-J1). The lead, as J1's owner, assents here, and the reviewer is asked to rule (R5).

## Deviations from E1 r3 (record items for E1's next revision)

- **E-1.** Item 10's "a symbol outside the table" gains the ERROR exception (LD-2). A11's "ids contiguous" holds as written.
- **E-2.** Item 4's closure layout omits the wasm headers (T-wasm only, inactive).
- **E-3.** Eager compilation is required under T-wasm (inactive). `fuelModel` should name the compilation mode, or E2b should fix `Eager`.
- **E-4.** Item 19's SYN-1 row lists NEM, but no NEM change is needed (LD-6).
- **E-5.** Item 19's SYN-1 (d) key list omits `-normalization-map-mismatch`, which r3 added to A3 and A6. The route row includes it, as item 5's "every `native.syntax-grammar-*` key" requires.
- **E-6.** Item 5 names no key for a missing closure. LD-4 adds `native.syntax-grammar-closure-absent`.
- **E-7.** A12's subject widens. SYN-NS's level specifications carry their own node-kind tables (SYN-NS LD-NS2). `native.syntax-normalizer-kind-unknown` therefore covers every kind, field and anonymous token that `normalizer.v1.json` **or a mapped level specification** names, as the new route row says.
- **E-8.** E0's observations for E2a, carried for the record: tree-sitter 0.25+'s supertype symbol type collapses to `{named: false, visible: false}` in `SymbolTableV1` (E2a may add a type field); and the host crate count under the minimal `wasmi` feature set is 8, not 7 (T-wasm only).

## Cross-law items

- **X-J1 (J1's next revision).** Row 52 gains the `native.syntax-*` keys of the new NE row, which takes the same route, at J-ε before PlanId. A new row, "Syntax backend fault", takes `operational-failed` / 4 / `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant / `HOST.INVARIANT_VIOLATED`, with subject `native.syntax-backend-fault:<grammarId>`, and no runId.
- **E2s.** Copies the two product sources (SYN-1 and SYN-1F), re-points both source maps, carries a 468a-form admission-registry record, regenerates the eight outputs, and updates the evaluator registries E1 lists. SYN-1F's identity copy also carries I1-L's member, so **E2s lands after I1-a**, or carries I1-a's identity source change with it (SYN-1F README).
- **E2b.** Implements `native.syntax-grammar-closure-absent` and the validation law, including the ERROR exception. Under T-native it also implements the dedicated parse thread with a fixed stack (item 18). A12 covers the level specifications (E-7).
- **H and E3.** The outcome table is H's syntax-join input (E1 item 20's second-integrator rule). Nothing here changes H.
- **C and CRC-1.** None for SYN-1. SYN-1F cites CRC-1, and binds after it.

## Points for the reviewer

- **R1 (outcome law).** Is the NE:306 section exactly E1 items 10, 11 and 14a, for `native-linked-v1`, with the T-wasm differences marked? Is anything missing from the envelope table or the retention rule?
- **R2 (ERROR).** Is LD-2's exception right, and is the flag-agreement rule sound on both branches?
- **R3 (keys).** Is the route row complete and correctly split by branch? Is the new key (LD-4) right?
- **R4 (copies).** Is each copy exactly its parent plus the stated edits, at the code-point position? Is (f) right, that no startup, `UnavailableReasonV3` or other reason vocabulary changes?
- **R5 (D9).** Is the backend-fault row (LD-12) right, and is X-J1 the right route for J1?
- **R6 (NEM).** Is LD-6 right that no NEM byte must change?

## Binding

After `ACCEPT-DESIGN-UNIT`, and in the same binding-only product commit as SYN-1F:
1. Copy the review to `docs/implementation/m3/reviews/codex2-syn-1-r1/review.json`.
2. Complete `syn-1-unit.json`: `ACCEPTED-DESIGN-UNIT`, the review pin, and `rootSubstantiveAssent: true`.
3. Append SYN-1's `{record, subjectManifest, review, assent}`.
4. Append CRC-1's entry, unless it is already bound.
5. Append SYN-1F's entry.
6. Run plain verify_design.

The binding changes no product byte and no generation source; E2s does that later.

## Evidence runs

All runs used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read-only. Nothing ran cargo, a product tool or a test.
- **`build_syn_1.py`:** run, then `--check` twice; the bytes were identical.
- **`check_syn_1.py --product …`:** passes, with 25 route keys (11 existing, 13 E1, 1 unit), two copies and five insert-only overrides.
- **`verify_scratch.py`:**
  - `--rev cd5958b`: binds, 82 → 83.
  - `--rev cd5958b --chain`: SYN-1, CRC-1, SYN-1F and SYN-NS bind together, 82 → 86.
  - `--rev 15c0779`: binds, 81 → 82.
  - The checkout at `cd5958b`, with generation and admission sources verified: binds.

  In every run the selected inventory and the inheritance projection are unchanged.

## Not claimed

- No product code, test, build or corpus run was made. Only the three evidence scripts ran.
- NEM and the native checker were not run. On this Mac the native model refuses Python 3.14.6's Unicode data as an environment fault (X12-0 README).
- No law is amended. E1's deviations are record items for its next revision.
- No hostile-input safety, sandbox or confinement claim is made (E1 item 17; AQ:344).
