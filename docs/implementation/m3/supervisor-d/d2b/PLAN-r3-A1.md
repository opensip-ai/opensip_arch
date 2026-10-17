# D2b plan r3, amendment A1 (LD-D2B0-A): D2b-0 admission-only, and D2b-0b owes the generator work

**Lead plan amendment, accepted with D2b-0 r2** (Codex `codex-d2b-0-r2`: ACCEPT-DESIGN-UNIT, `amendmentLDD2B0A` ACCEPT; lead assent `d2b-0-r2-unit.json`). It amends the accepted D2b plan r3 (`PLAN-r3.md`; Codex `codex-d2b-plan-r3`). It is a deferral only: **M3-D item 10 (`PROPOSAL-r5.md`:381) and both accepted materialization maps (FA-2's and RUST3-LIM's `materialization-map.json`) are not amended.** Nothing else in the plan changes.

The accepted text follows verbatim, from `d2b-0-r2/SCOPE.md` (22975 bytes, SHA-256 `300c24ba6ef690319536fbb8d1ba2d743c8f3e0cc181052fd401aa37963d59f8`, a member of the reviewed subject `d2b-0-r2-subject.json`, `3c74788cab3b6b92b03446a3007e082ac7ba52475c64b2a4c13795c48e0edb8d`).

## LD-D2B0-A. The amendment: a deferral, with D2b-0b owing the generator work

**Why.** The generator cannot generate FA-2's census schema without a change to its own reviewed runtime profile:

1. **The pattern profile.** `symbol-census-v1.schema.json`'s `$defs/SubjectIdV1` (line 79) has the pattern `^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])`. It is not in the generator's selected TypeScript pattern table, `tools/contracts/runtime/patterns.ts`, which is generated from a reviewed M1 pattern profile and is unchanged since `436d615`. The pipeline's `validate` step refuses it ("pattern outside selected profile"). The census's request, row and payload types all reach `SubjectIdV1`.
2. **The precedents.** The same pattern is in three schemas that are **admission-only, never generator sources**:
   - `relation-payload-v2.schema.json`:838;
   - `subject-inventory-v1.schema.json`:296;
   - `target-attribution-v2.schema.json`:356.

   Each is in the admission registry and the identity crate's pins, and absent from `schemas/source-map.json`, `schemas/registry.json` and `tools/contracts/options.json`.
3. **The root law annotations.** Each new schema's root carries one law keyword outside the generator runtime's closed annotation set (`tools/contracts/runtime/schema.ts`:17): `x-opensip-symbol-census-law` and `x-opensip-subject-scope-law`. `prepare.py` refuses converting either root.

   Every other keyword in the two schemas is in the selected set. This was checked by walking every schema node.

Generating these schemas therefore needs a reviewed extension of the generator's pattern profile and annotation set: a change to a reviewed generator input, and to the TypeScript runtime text embedded in `apps/report/src/generated/report.ts` and `providers/typescript/src/generated/protocol.ts`. That extension, and the generation it allows, are D2b-0b's, under its own review. They are owed, not waived.

**What it does not amend.** These stay in force exactly as written, and LD-D2B0-A only re-sequences them:
- **M3-D item 10** (`supervisor-d/PROPOSAL-r5.md`:381): "The decoded tree is converted by hand-written, schema-checked code into the generated carrier types. **Serde never deserializes wire bytes** …";
- **FA-2's materialization map** (`native-successors-fa/fa-2/materialization-map.json`, its `standing`): "Those units also add the census schema's source-map and admission rows, re-pin the registries and regenerate carriers …";
- **RUST3-LIM's materialization map** (`rust3-lim/materialization-map.json`, its `standing`): "Those units also add the new schema's source-map and admission rows, re-pin the registries and regenerate carriers …".

D2b-0 does their admission part. D2b-0b does the rest: the source-map rows, the generation-registry re-pin and the regenerated carriers. Neither D2b-3 nor D2b-4 may use a hand-written carrier for a successor payload.

**The D2b plan r3 text it replaces** (`supervisor-d/d2b/PLAN-r3.md`):

- **§1's table, the D2b-0 row** (:81).
  - Current: "| **D2b-0** | The successor schema materialization, FA-2's and RUST3-LIM's schemas, rebased on RCA-1's product handshake; then **a reviewed blind refresh** | the materialization's own checks; the refreshed receipt | — |".
  - Replacement, two rows:
    - "| **D2b-0** | The successor schema materialization, FA-2's and RUST3-LIM's schemas, rebased on RCA-1's product handshake, **admission-only** (LD-D2B0-A): the admission registry and its source map, the identity pins and the host and storage embeddings; no generator input changes, so the blind receipt stays current | the materialization's own checks; the census `--check` against the unchanged receipt | — |"
    - "| **D2b-0b** | The successor schemas' generation: the generator's pattern-profile extension (`SubjectIdV1`'s pattern, with `pattern-profile.json`, a reviewed generator-input change) and the root law annotations; the source-map, generation-registry and options rows; the regenerated carriers (M3-D item 10; both materialization maps); then **a reviewed blind refresh** | the generation checks; the refreshed receipt | D2b-0 |"
- **§1's table, the D2b-3 and D2b-4 rows' dependencies** (:82-83).
  - Current: "D2b-1, D2b-2, D2b-0" (each row's last cell).
  - Replacement: "D2b-1, D2b-2, D2b-0, D2b-0b" (each row's last cell).
- **§1, the order** (:85).
  - Current: "**Order:** D2b-1, then D2b-2, then D2b-0 with its blind refresh, then D2b-3 and D2b-4."
  - Replacement: "**Order:** D2b-1, then D2b-2, then D2b-0, then D2b-0b with its blind refresh, then D2b-3 and D2b-4. D2b-0b is integrated before D2b-3 or D2b-4 consumes either successor payload."
- **§1, the two bullets after the order** (:86-87).
  - Current: "**D2b-0 comes after the two mechanics units.** Its regenerated carriers change `tools/contracts/generator-closure.json`, a file the discovery census binds as reference-loading code. That makes the B2-b4c blind held-out receipt stale, and the census `--check` then fails on main." and "**So D2b-0 is followed at once by the reviewed blind refresh,** before any other lane needs the census: a pre-run Codex review of the blind mode, the lead's mechanical blind run (the owner's standing answer), and a post-run review. This is B2-b4c3's sequence."
  - Replacement: "**D2b-0 and D2b-0b come after the two mechanics units.** D2b-0 changes no generator input (LD-D2B0-A). D2b-0b's regenerated carriers change `tools/contracts/generator-closure.json`, a file the discovery census binds as reference-loading code. That makes the B2-b4c blind held-out receipt stale, and the census `--check` then fails on main." and "**So D2b-0b is followed at once by the reviewed blind refresh,** before any other lane needs the census: a pre-run Codex review of the blind mode, the lead's mechanical blind run (the owner's standing answer), and a post-run review. This is B2-b4c3's sequence. **No hand-written carrier** stands in for a successor payload's generated carrier in D2b-3 or D2b-4 (M3-D item 10)."
- **LD-D2B-13** (:135).
  - Current: "… and its review judges each, with the registry, source-map and admission updates and every regenerated carrier."
  - Replacement: "… and its review judges each, with the admission updates; D2b-0b's review judges the registry and source-map updates and every regenerated carrier."
- **§4, the repository checks** (:211).
  - Current: "For D2b-0, also its generation checks and the census `--check` after the blind refresh."
  - Replacement: "For D2b-0, also the admission-only assertions (no generator input or output changes) and the census `--check` against the unchanged receipt. For D2b-0b, also its generation checks and the census `--check` after the blind refresh."

§0's codec requirement (:54, "each payload decoded by hand-written, schema-checked code into the generated carriers") is **not** replaced, unlike in round 1.

LD-D2B-2's depth bound (computed in D2b-3 and D2b-4 over the complete successor-aware closure, "after D2b-0's materialization") is unchanged. The successor schemas are in the admitted registry from D2b-0 on, and D2b-3 and D2b-4 follow D2b-0b.
