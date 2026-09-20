# Independent scoped review — ROOT corrections in trust-inputs 230 r2 and the 231 r2 assembly

Scope: only what root changed on top of my 230 r2 AUTHOR files, plus the 231 assembly. **This is
not approval of my own unchanged author code, not cumulative protocol approval, and not a verdict
by test count.** No repo/product/candidate edit, commit or push; output only in this directory. My
author fixture directories are untouched.

## Verification and reproduction

- 230 r2 `ee6a4f88…bfb4` (29 members) and 231 r2 `2290dea9…9fa9` (23 members): archive pin and EVERY
  subject member verified from the tar before extraction; both re-verified at the end.
- `claude-author-r2/*` (six files) are byte-equal to my r2 outputs; `check_trust_inputs-before-root.py`
  equals my check; `trust_inputs_model-before-root.py` differs from my model ONLY in four path lines
  (pins relocated to `inputs/` and the sibling reference) — no logic change before root's edits.
- Runs from output-local copies with a sibling symlink to my verified reference-201; Python 3.12
  reference env; scripts write stdout only; **no script edited**.
- 230: 184 cases (20 admit / 158 exact-label refusals / 6 static) — the regenerated report equals
  `input-check-root-r3.json` key for key. Variants: 25/25 source variants killed; guard survey 90
  reasons → 81 killed, 8 ERROR-not-a-kill, 1 direct raise — equals `input-variants-root-r2.json`.
  The AST enumeration of reasons is a real improvement over my regex.
- 231: 11 assembly checks — regenerated report equals `integration-check-r4.json`; schema a3a0b4f4….

## Part 1 — root's 230 corrections

### Confirmed

- **Descriptor projection binding**: `afterProjection.{store, revision, previous}` must equal the
  descriptor header; applied to every chain link AND the witness; source variant killed.
- **Work parameters can only lower** the 222 limits; negative, float, bool and enlarged values refuse
  (adv X5).
- **Host surface**: `surface: "installed-component"` is a required constant on install/continue;
  another value, a missing value, or a surface on restrictive-observation are shape-refused (X6);
  caller roles stay unrepresentable. **EV-CLOCK keeps all six roles** (215 C.2: root expiry is a
  CLOCK cause for every role) while INSTALL/CONTINUE stay on the v14 install-surface triple — the
  variant that re-restricts CLOCK is killed. My r2 restriction of CLOCK to three roles was wrong.
- **Forward/ancestor intent case**: forward requires core-update/store-migrate with schema advance,
  ancestor requires core-rollback/store-rollback with schema retreat, both after the ORIGINAL 201
  `admit_transition_intent`; "same-schema operations do not invent a fresh S" follows from 201.
- **First-link nested recovery — the inference holds.** I checked it against 222's normative text
  and the toy: the toy's `missing-proof-parent` exists because its proof tuple holds descriptor
  identities only and has no capsule object for the parent at index 0; PERSISTENCE says only that a
  recovery descriptor "is NOT an independent prover: its complete retained proof chain, including an
  ORIGINAL terminal descriptor…, must admit". With `observed.image` retained, the nested expectation
  (`nested.proven == observed`, `nested.observed == link.nativeBefore`, same store, direct
  non-recovery witness) is exactly that rule. Root's positive is a coherent history: file at c1 →
  recovery R proves c1…c3 and publishes revision 4 → file rolled back to c3 → chain `[R, d5]`.
  One consequence worth stating in the prose: in this shape the parent ALWAYS has at least two
  children in its bucket (the nested direct witness and R). That is lawful only because 222 counts
  PROVEN children for fork detection; the live census must therefore not treat "two entries" as a fork.

### Findings

#### C-1 (medium) — the target-continuity exception does not bind the target-before to the descriptor's own predecessor

INPUT-JOINS calls the exception "exact": "Ancestor target binds its retained before image".
`descriptor_operation` checks the image's STORE only. Probes on the unmodified model
(`claude-out/io/adv230root.json`):

| probe | result |
|---|---|
| X1 FORWARD continuity (target was ABSENT) on a descriptor with `revision 5` and a non-null `previousCapsule` | **ADMITS** |
| X2 ANCESTOR: `previousCapsule` names a capsule other than `hash(targetBefore.image)` | **ADMITS** |
| X3 ANCESTOR: target-before image revision 3, descriptor revision 9 | **ADMITS** |

A forward target is fresh: its first descriptor is revision 1 with `previousCapsule` and
`nativeBefore` null (224/226; root's own positive fixture is built that way). An ancestor target's
before image IS the descriptor's logical predecessor (root's fixture: `previousCapsule ==
hash(image)`, `revision == image.revision + 1`). Neither is required, so a source-bound shell can ride
on an arbitrary target-store descriptor as long as one well-formed continuity event is listed. In the
restore-proof use it is sharper: every chain link and the witness have revision ≥ 2 and a non-null
predecessor, so a FORWARD continuity link can never be legitimate there, yet it passes
`link-operation-store` / `witness-operation-store`. **Action:** forward ⇒ `revision == 1 and
previousCapsule is None and nativeBefore is None`; ancestor ⇒ `previousCapsule ==
targetBefore.image.sha256 and revision == image.revision + 1`; add the three negatives and a source
variant. (Inside `admit_restore_proof` the caller also knows `cur_ref`; passing it would let the
ancestor join be checked against the chain's actual predecessor.)

#### C-2 (low) — a same-store shell returns before the descriptor's events are looked at

`if o['store'] == d['store']: return o`. A descriptor whose shell is a same-store ordinary import but
whose only event is a target continuity event of ANOTHER operation admits (X4). Event↔operation
equality per descriptor is 226 audit law and INPUT-JOINS lists "event outcomes" as owed, so this is
inside a stated boundary; I note it because the cross-store branch DOES join events and a reader may
assume the same-store branch does too.

#### C-3 (low) — `Work(objects=0)` is accepted

Bounds are `0 <= n <= cap`. A zero budget then refuses every load, so it is harmless, but 229 r3's
equivalent refuses zero (`0 < limit`). Pick one convention.

#### C-4 (low, evidence) — two of root's new reasons are not mutation-killed

`continuity-target-event` and `continuity-target-before` are among the 8 ERROR-not-a-kill rows
(disabling them leads to an exception, not an assertion). Each has an exact-label negative, and root
reports them as not-kills, correctly. Same standing as the six I left; weaker than a kill.

## Part 2 — 231 r2 assembly

Independent audit (not the owner's checker):

- 122 definitions = the previous 110 (`…before-inputs…` is d9ac0243…, byte-equal to the bundle my 230
  model pinned) **unchanged**, plus exactly 12 added; none removed; none of the 110 altered.
- The 12 added equal the `$defs` of root's `trust-inputs-root.v1.json`, and 231's input copy of that
  file is byte-equal to the 230 r2 member.
- All seven source files match `source-pins.json`. Every definition in every source equals the
  assembled one EXCEPT six, each explained by a declared operation: the single rename
  (`LogicalPath` → `CoreLogicalPath` for the core-distribution source; `CorePlatformV2`,
  `EmbeddedBootstrapV1`, `FileRef`, `TreeEntry` are equal after exactly that `$ref` rewrite, and
  `CoreLogicalPath` equals the core source's `LogicalPath`), and the single replacement (the
  `RootAdmissionNodeV1` anchor variant → `$ref CoreAnchorNodeV1`; variants 1 and 2 unchanged).
  `LogicalPath` 1024 / `CoreLogicalPath` 4096 stay distinct. The intent alias is preserved.
- `pendingInputCodecs` is now empty and `pendingAdmission` lists the owed producers; no authority
  claim. 462 local refs resolve; whole-schema meta-validation passes.

Observations (low):
- **A-1 provenance label.** The assembled `core-distribution.v1.json` is the 229 **r1** file
  (57de5b0c…), while 229 is now at r3 (960ecdfd…). I compared them: their `$defs` are identical, so
  nothing is stale in substance; the replacement's `owner` note ("root-corrected229; independently
  reviewing") and the pin would read better against the current frozen revision.
- **A-2** 39 definitions are referenced by no other definition. Most are roots by design (node and
  event types). A few inherited ones are genuinely unused here (`Consent`, `Effects`, `ExpiryStates`,
  `JournalRecord*`, `WalkRecord`, `PrunedTreeRowV2`, `ProjectId`, `SnapshotId`, `RepairPlanId`, …):
  carried verbatim from the primary 201 copy. Harmless, but a private TRUST bundle that can name a
  `ProjectId` invites the identity leakage the 230 inputs were written to exclude; consider an
  explicit "inherited, unused" list.

## Boundaries not treated as findings

Signatures/thresholds/envelopes; native creation, absence, custody; live bucket census, fork
detection, witness choice; closure admission of n and N; S4 durability and dispatch; lineage/current
selection/PhaseB; primary 203 envelope-route integration (outside this review by root's statement).

## Limitations

Probes call root's unmodified functions with fixtures re-typed from root's corpus shapes; ADMITS is
the toy model's verdict on shape-valid, non-reachable values. C-1 was demonstrated at
`descriptor_operation`; I argued, but did not separately run, its consequence inside
`admit_restore_proof`. My own unchanged author logic was NOT re-reviewed here and must not be read as
covered. No harness failure occurred.

## Pins

230 r2: `trust_inputs_model.py` 544a95e1eb7936b4e1795763dc9376d86b3f8b8e2bc1cf95fa61581232dfb375 ·
`check_trust_inputs.py` 2269dc397492cc9b4a312290f21488d53a121b7b2d715f9bd8f59d9abf7f3b08 ·
`check_trust_inputs_variants.py` 44c6acb856f53e3c86d7cbafff57a01ffad7a9eea31a2e346ed4a87feb84d2cc ·
`INPUT-JOINS.md` d2b05b97c0e872c466dd2201b7dbaf0c973dc8142e02c68713333560828d8f4e ·
`trust-inputs-root.v1.json` b2939551042dbfebdf38cce842430ec66e19c98503aac3115592e97d66cfd823
231 r2: `private-trust-state.schemas.v1.json` a3a0b4f468f0a43c2befa0e3157c6796b09128084a9a68c70b4fd04b43bd8520 ·
before-inputs d9ac024357c1645727449bb38f940dbf886244e1d3959998a3e28b64d6857968
Reference: `canonical.py` d47f25db… · kernel df45c9c5… · 222 `successor_model.py` 53cae8d9… (live, as
pinned in my r2) · 222 `PERSISTENCE.md` f9963414… (live)
