# SYN-1F — the foundation mirrors of SYN-1 (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, state, field, refusal code or public code. It needs `ACCEPT-DESIGN-UNIT` from an independent reviewer and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-E1 r3** (`../PROPOSAL-r3.md`, `d71031ff…`) names successor **SYN-1F** in item 19 (E1:690), "joined with SYN-1 (E-R1)". `source-parse-error` enters exactly the five foundation `NativeCause` copies, by selector. The unit also states that execution-inputs §6 and EXM's candidate derivation apply unchanged to item 14a's syntax-only envelope, with item 14b's producer. No new state, field or refusal code is added.

It binds with **SYN-1** (`../syn-1/`), which adds the member to the native owner, NES. EXM:851 holds the execution-input copy equal to NES, so neither unit binds alone (SYN-1 LD-11).

**It binds after CRC-1, which is now bound.** CRC-1 is M3-C's closure-role successor (`docs/implementation/m3/snapshot-plan-c/crc-1/`). It was **accepted at r4 by Grok and bound at product main `392499e`**: `successor.json` `29df5f5e…`, subject `ec896801…`. It puts three JSON Pointer overrides on **I1-L's selected identity-schema copy**, which is this unit's IDS parent:
- `/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact`;
- `/x-opensip-digest-domains/closureKinds/note`;
- `/x-opensip-digest-domains/closureMembership/selectionLaw`.

This unit's IDS copy **carries those three overrides, as CRC-1 r2 states them, and as r3 and the bound r4 keep them byte for byte** (r3 and r4 changed only the record's candidate pins). r2 changed one of them after GROK2's r1 finding: the `closureMembership` selection law now ends "…and is never selected otherwise, not even explicitly; the core adapter closure is never a member." That replaces r1's wrong "explicitly included". (r2's other change, IE:285, is a text override this unit does not carry.) Earlier builds of this unit were made on CRC-1 r1, r2 and r3; only the r3 build was assigned, and none was reviewed. CRC-1's bound record is one of this unit's parents, so verify_design itself enforces the order (LD-F3). Against the `392499e` lock, where CRC-1 is bound, SYN-1F binds on its own.

**The branch.** Nothing here depends on the execution model. E0 chose `native-linked-v1` (`../E0-REPORT.md`, `c1011e83…`), and the member, the mirrors and the envelope are the same on both branches.

**Product.** Main at `392499e` (CRC-1 bound, 83 contract successors), read only. The record is built against `design-lock.json@392499e`, where CRC-1's three overrides are ordinary bound entries of the identity parent.

## Short names

E1, E0, NES and CRC-1 are as in SYN-1's README. The other names:
- **EXC:** `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` (35,845 bytes, `22ee2507…`).
- **EXS:** `docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json`.
- **EXM:** `execution_inputs_model.v1.py` beside EXS.
- **ENS:** `enumeration-plan.schema.v1.json`.
- **SIS:** `subject-inventory.schema.v1.json`.
- **EPR:** `evaluator-projection-registry.v1.json`.
- **I1L-IDS and I1L-PIDS:** I1-L's selected copies, `docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json` (198,725 bytes, `c9214f03…`) and `…/i1-l/product/schemas/sources/identity-v3.schema.json` (198,423 bytes, `eb6ec957…`).
- **ARS:** `docs/implementation/m2/admission-runtime-selection-v1/schemas/sources/`, the selected product sources of EXS, SIS and ENS. Each is byte-identical to its foundation file.
- **C6:** M3-C r6 (`snapshot-plan-c/PROPOSAL-r6.md`, `8274bca1…`).

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the one override, with its exact `before` and `after` |
| `successor.json` | the record: eleven parents, one passage override, sixteen candidates |
| `design/foundation/*.json` | the five foundation successor copies (generated) |
| `product/schemas/sources/*.json` | the four product source successor copies (generated) |
| `materialization-map.json` | generated: the four product sources E2s copies |
| `evidence/build_syn_1f.py` | builds every generated file, the record and the subject; restates verify_design's rules for this record; `--without-crc-1` builds the other order |
| `evidence/check_syn_1f.py` | read-only content checks, written independently of the build |
| `evidence/verify_scratch.py` | the real verify_design with synthetic review and assent; it appends CRC-1 first unless it is bound |
| `evidence/copies-report.json` | generated: per copy, the parent, the overrides carried, the new member line and the hunks |
| `../syn-1f-subject.json` | the subject manifest (generated) |
| `../syn-1f-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes

### Nine complete JSON successor copies, one member each

Each copy is its parent's effective text with `"source-parse-error"` inserted at its code-point position, before `"source-replacement-outside-snapshot"`, in the one `NativeCause` copy the parent holds. The effective text is the raw bytes, with every override bound to that parent applied, plus CRC-1's, which binds first. Before the edit, every parent's list equals NES's `#/$defs/NativeCause/enum`; after it, every copy's list equals SYN-1's NES copy.

| Copy | Parent | Selector | New line | Carried |
|---|---|---|---|---|
| `design/foundation/execution-inputs.schema.v1.json` (39,940, `0c196cba…`) | EXS (39,910, `604bd941…`) | `#/$defs/NativeCause/enum` | 217 | — |
| `design/foundation/identity-schemas.v3.json` (200,510, `73645b76…`) | I1L-IDS | `#/$defs/evaluation-deficiency/properties/nativeCause/oneOf/0/enum` | 3494 | CRC-1's three bound overrides (r4, the same strings as r2 and r3; lines 287, 4748 and 4820) |
| `design/foundation/subject-inventory.schema.v1.json` (16,891, `34e49cd1…`) | SIS (16,861, `6ab46925…`) | `#/$defs/NativeCause/enum` | 462 | — |
| `design/foundation/enumeration-plan.schema.v1.json` (20,005, `cc29483f…`) | ENS (19,975, `10627cb6…`) | `#/$defs/NativeCause/enum` | 261 | — |
| `design/foundation/evaluator-projection-registry.v1.json` (60,035, `c5a0aa82…`) | EPR (60,005, `65f163cc…`) | `#/$defs/NativeCause/enum` | 1161 | — |
| `product/schemas/sources/execution-inputs-v1.schema.json` | ARS execution-inputs-v1 | `#/$defs/NativeCause/enum` | 217 | — |
| `product/schemas/sources/identity-v3.schema.json` (198,461, `080a8522…`) | I1L-PIDS | as IDS | 3494 | — (CRC-1, like EC1, leaves product copies alone) |
| `product/schemas/sources/subject-inventory-v1.schema.json` | ARS subject-inventory-v1 | `#/$defs/NativeCause/enum` | 462 | — |
| `product/schemas/sources/enumeration-plan-v1.schema.json` | ARS enumeration-plan-v1 | `#/$defs/NativeCause/enum` | 261 | — |

- **The pairs keep their relations.** Each byte-equal design and product pair is still byte-equal. The identity design copy differs from the identity product copy exactly as their effective parents do: the framework-recognition-plan row, EC1's two strings, and now CRC-1's three. `build_syn_1f.py` asserts both.
- **The descriptions stay true.** SIS and ENS say "Copied closed membership of …NativeCause", and EPR says "Copied exact native owner enum". IDS's description copy is unchanged because NES's is (SYN-1 LD-7).
- **I1-L's member is kept.** The identity copies keep I1-L's `cycle-representative` member and the overrides I1-L carried, because their parents are I1-L's copies.
- **B-S2's IDS fragment still applies.** B-S2's `identity-schemas.v3.b-s2-additions.json` is a merge rule over `vcs-observation`, which no copy touches, so it applies on top as before.

### One insert-only line override of EXC (§6)

EXC:257 is §6's census paragraph ("Complete `examinedPaths` equals the Plan `candidateSourcePaths`…"). After it comes a new paragraph, "The syntax-only `clones-near` envelope". It says:
- the envelope is exactly one retained `CandidateProducerResultV1`, admitted by §6 and `derive_outcome` **unchanged**;
- its `producerClosure` is the binding's `enumerator.closureId`, which is the core provider closure (C6 item 9 and X-C1, as CRC-1 records it; this unit adds **no closure-role text**);
- its `stageOrdinal` is the binding row's syntax stage, and its census is C4a's `candidateSourcePaths` (X-C2);
- its pair, `examinedPaths`, groups and `sourceBodies` follow NE §1.2's outcome and retention law (SYN-1);
- `nativeCause` may be `source-parse-error`, under `input-closure-incomplete` only;
- the enumeration-local `source-syntax-invalid` stays distinct.

No accepted successor overrides any EXC line.

## Lead decisions

**LD-F1. Complete successor copies (I1-L's LD-L1 form), five design and four product.**
- A JSON Pointer override replaces one string and cannot add an enum member. A line selector on a JSON parent refuses ("v4 JSON parent passages require JSON Pointer selectors").
- **Rejected:** a verify_design profile for array appends, which would be a tooling unit and a re-pin, for one enum member.

**LD-F2. The product copies ride in this subject, one per selected product source, even where design and product are byte-equal.**
- Each copy succeeds exactly one parent, as the selection layout already pairs them, and E2s re-points each source map row at its copy. `materialization-map.json` gives each before and after.
- **Rejected:**
  - **One copy serving both a design file and its byte-equal product source.** One successor of two parents blurs which selection moved.
  - **Leaving the product copies to E2s.** That puts the member in two subjects.

**LD-F3. The IDS copy descends from I1-L's selected copy, carries CRC-1's three overrides, and names CRC-1's record as a parent.**
- A copy is its parent's effective text (I1-L LD-L2; B-S9 LD-1).
- A copy of the frozen IDS would fork the selected identity text, losing I1-L's member and its four carried meanings.
- CRC-1 binds three meanings on I1-L's design copy. A copy that ignored them would silently revert them.
- With CRC-1's record as a parent, verify_design refuses SYN-1F until CRC-1 is bound. A scratch probe confirmed it before CRC-1 was bound: SYN-1F alone on the `cd5958b` lock refused, "contract parent is not an accepted base or selected inventory". On `392499e`, where CRC-1 r4 is bound, it binds.
- **CRC-1 is bound,** so the order cannot flip. `build_syn_1f.py --without-crc-1` remains only for a lock without CRC-1. If the lock ever binds another CRC-1 record, the build stops: `CRC1_SHA256` must match the bound record.
- **Rejected:**
  - **Overriding CRC-1's selectors again** (verify_design refuses it).
  - **A copy without CRC-1's text,** which would leave CRC-1's later binding pointing at a superseded copy: B-S9's residual hazard, which only review catches.

**LD-F4. Code-point position** (SYN-1 LD-8). EXM:851 and the enumeration model's drift check (`enumeration_model.v1.py:220`) compare lists for equality, and every copy gets the member at the same index as NES's copy.

**LD-F5. The EXC paragraph restates no closure-role law. It cites CRC-1 and C6 for the producer.** CRC-1 owns the identity schema's closure-role text (M3-C r6's X-C1). This unit only says that EXC's existing envelope rules apply to the syntax producer unchanged.
- **Rejected:** editing IDS's `closureKinds` or `closureMembership` here, which would duplicate CRC-1's text.

**LD-F6. No model or checker changes.**
- EXM, the enumeration model and `check-identity.py` read the frozen parents by fixed path, so they are historical references. Their drift checks compare list equality, which the copies keep.
- `check_syn_1f.py` restates that comparison over the copies.
- **Rejected:** model copies, which would read the frozen siblings anyway (SYN-1 LD-6).

**LD-F7. The evaluator projection registry gets its copy, though it is design-only.**
- E1 lists it among the five. Its `NativeCause` is "Copied exact native owner enum", which would otherwise become false.
- Nothing in the product reads it, so E2s has no materialization for it.

## Consequences for E2s, and cross-law items

- **E2s after I1-a.** SYN-1F's identity product copy descends from I1-L's product copy, so it also holds I1-L's `cycle-representative`. E2s therefore lands after I1-a, or it carries I1-a's identity source change, together with its regenerated outputs and its `atom-registry.json` pins (I1-L README, "For I1-a").
  - **Rejected:** a copy of the frozen PIDS without I1-L's member, which would fork the selected product identity source.
- **E2s's other duties.** It copies the four sources and re-points both source maps, carries a 468a-form record for its new `schemas/admission-registry.json`, regenerates the eight outputs, and updates the evaluator registries. The `#/causes`, `#/nativeCauses`, `#/scanner/nativeCauseCodes`, `#/causeRegistry`, `#/ownerNativeCause` and `#/schemaNativeCause` selectors are listed in E1 item 20's E2s row, and their order is code-point order.
- **CRC-1.** Binds first (LD-F3). If CRC-1 changes, SYN-1F is rebuilt.
- **M3-C r6 and C4a.** The census (X-C2) and the producer (X-C1) are C's. Nothing here changes them.
- **None for H, B or J1.** SYN-1's README carries X-J1.

## Points for the reviewer

- **R1 (selectors).** Are these exactly the five foundation `NativeCause` copies and the four product sources E2s needs, with no other cause or reason list touched? Are the startup schema and `UnavailableReasonV3` untouched (SYN-1's (f))?
- **R2 (copies).** Is each copy its effective parent plus one member, at the code-point position? Do the identity copies carry I1-L's and CRC-1's meanings correctly, and is the product copy right to carry neither EC1's nor CRC-1's text?
- **R3 (order).** Is binding after CRC-1, enforced through the parent pin, right (LD-F3)? (CRC-1 r4 is now bound at `392499e`.)
- **R4 (EXC).** Is the §6 paragraph true and minimal, and does it stay off CRC-1's ground?

## Binding

This unit binds in SYN-1's binding commit, after SYN-1; CRC-1 is already bound (SYN-1 README, "Binding"). After `ACCEPT-DESIGN-UNIT`:
1. Copy the review to `docs/implementation/m3/reviews/codex2-syn-1f-r1/review.json`.
2. Complete `syn-1f-unit.json`.
3. Append the entry after SYN-1's.
4. Run plain verify_design.

The binding changes no product byte.

## Evidence runs

All runs used `python3.14 -I -B` at `nice -n 19`, read-only.
- **`build_syn_1f.py`:** run, then `--check` twice; the bytes were identical.
- **`check_syn_1f.py`:** passes, with nine copies, CRC-1's three overrides carried in the IDS design copy only, and the mirror invariant met.
- **`verify_scratch.py`:**
  - `--rev 392499e`: SYN-1F alone, 83 → 84 (CRC-1 r4 is bound).
  - `--rev 392499e --chain`: SYN-1, SYN-1F and SYN-NS, 83 → 86.
  - The checkout at `392499e`, with generation and admission sources verified: binds, 83 → 86.

  In every run the selected inventory and the inheritance projection are unchanged.
- **The order probe:** SYN-1F alone on `cd5958b`, where CRC-1 is not bound, refuses, as LD-F3 intends.

## Not claimed

- EXM, the enumeration model and `check-identity.py` were not run.
- No product, registry, generated-code or inventory file is touched.
- No closure-role, Plan or census law is stated: those are CRC-1's and C's.
