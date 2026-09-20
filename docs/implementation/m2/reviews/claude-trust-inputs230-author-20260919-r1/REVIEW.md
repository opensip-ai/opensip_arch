# Author proposal 230 — the six remaining private trust input nodes

**AUTHOR assistance for root to integrate or adapt. Not independent approval, not selected, no
native authority, no new public command.** No candidate, product, architecture or repository file
was edited; nothing committed or pushed; earlier frozen bytes untouched; output only here.

| file | content |
|---|---|
| `proposed/trust-inputs-230.v1.json` | 61 `$defs`: 50 copied verbatim from root's working 231 bundle (re-asserted equal at build), 11 new. sha256 2e0b38c6…6cec |
| `proposed/INPUT-JOINS.md` | per-input shape rationale and semantic joins, each sentence tagged [source] or [proposal]; integration notes for the 227 r8 inventory |
| `proposed/fixtures-check.json` | 89 conditional cases (10 admit, 75 exact-label refusals, 4 static properties). sha256 7b43b90e…0a1 |
| `proposed/fixtures-check-r3.json` | 1 further case found by re-measuring the survey |
| `proposed/fixtures-check-r2.json` | 21 supplementary cases closing gaps my own guard survey found (below). sha256 27855805…6c43 |
| `claude-out/probes/` | builder+fixtures, supplementary fixtures, self guard survey |
| `claude-out/inputs-as-read/` | byte copies of the root working files I read (they are live drafts, so I pinned what I saw) |

## What is proposed (one line each; detail in INPUT-JOINS.md)

1. **`CreationInputV1`** — platform id, delivering core `closure2`, `{S, G const 0, K}`, store
   marker ref, the creator's private staging name, host observation. No project/run identity, no
   init flag, no invocation copy.
2. **`TargetAbsenceInputV1`** — original host observation INPUT for a forward target: invocation,
   exact intent alias NodeRef, source and target bindings tied to the intent's from/to G/K, foreign
   name count, observation. No `available`/`absent` member; never proof of native absence.
3. **`RestoreDeclarationInputV1`** — exact before image, the ≤ 64 examined orphan publication refs
   of its bucket, transition slot `absent|coherent-terminal`, observation. No `clean` member.
4. **`RestoreProofV1`** — observed image n, proven image N, ordered `PublicationRef` chain of
   length N − n, the ORIGINAL DIRECT terminal witness. A recovery descriptor as witness refuses;
   no own-descriptor/AFTER member is representable; uniqueness is explicitly NOT established.
5. **`RestrictionEvidenceV1`** — revocation (role, OLD `acceptedUnder`, before-history head, list
   node, subject restricted to `namespace|catalogSnapshot`, bound BEGIN iff RECOVERY) or quorum
   (role, closed context, context root, history, bound BEGIN). No count, flag, cause or priority.
6. **`TrustAdmissionInputV1`** — closed purposes `install | continue | restrictive-observation`;
   each purpose owns a closed event set; no image, exemption, skip-time or grant member.

The existing `TransitionIntentInputV1` alias is reused exactly (by NodeRef); no wrapper, no new
hash, no invented request/Execution/Project/Run/receipt recipe anywhere.

## Source conflicts and inconsistencies found (not papered over)

- **K-1 report count.** `transition-input-check-r1.json` has `caseCount: 18`, not 19.
- **K-2 EVENT-JOINS is behind the schema.** Its authored body (l.22) still says the action set is
  "closed (13 values)" and pairs continuity with `continuity-input`; the 231 `OperationInputV1` has
  14 actions (adds `host-trust-admission`) and the kind is `transition-intent-input`. Root's
  numbered corrections at the top override the body, but the body is what a reader cites.
- **K-3 duplicated references in existing shapes.** `CreationEventV1.creationInput` and
  `RestoreEventV1.proof` restate the operation's `input.ref`. I did not remove them (not mine);
  I state the equality joins. Root may prefer deleting the event-side copies.
- **K-4 one evidence slot per observation input.** `RestrictionObservationInputV1` has exactly one
  `restrictionEvidence`, while 215 derives observations for several roles "once … under the
  fence". This composes only if each observed-context role event names its OWN time input; I wrote
  the evidence per (role, purpose) accordingly. If root intended one shared observation input per
  operation, its shape needs a list — a root decision, flagged rather than hidden.
- **K-5 222 wording vs 227 shape.** 222 says the restore event "pins the ordered proving
  descriptors"; in 227 the event holds a NodeRef to the proof, which pins them. Consistent by
  indirection; worth one aligning sentence in 222.
- **K-6 inventory mapping.** 227 r8's `schema_dependency_inventory.py` maps NodeRef targets by
  field NAME and asserts on unknown names. These defs add `intent`, `acceptedUnder`,
  `contextRoot`, `listNode`, `begin`; the assert will (correctly) stop until they are mapped.
- I found **no contradiction** between 224 ("no invented ExecutionId in lineage provenance") and
  the operation shell requiring an `InvocationBinding`: 224 l.7 places creation inside an existing
  admitted invocation, so the ids exist and live on the shell only.
- Root's accepted G-1 amendment (index 0 is chain anchor only; pre-acceptance authority is the
  FINAL root of the complete authenticated embedded chain) needs no field here: quorum evidence
  names an explicit `contextRoot` and cannot select a chain prefix by itself. The live 215
  `OWNER.md` I read is a48e122c… (already differs from frozen r14 d8165f14…).

## Self-check of my own fixtures (done because I found this gap in 229 and 227)

A guard-off survey of my model (disable one refusal reason, re-run all fixtures in memory) showed
**17 of 50 reasons with no dependent case** in the first 89. I added 21 exact-label cases
(`fixtures-check-r2.json`) covering: operation-ref, proof-ref, proof-store, proof-budget,
proof-observed-image, proof-repeated-descriptor, proof-descriptor-join, witness-descriptor-join,
retained-bytes, noncanonical, declaration-store, orphan-order (two forms), operation-action,
evidence-store, quorum-context-root, quorum-history-head, plus a positive current-root quorum case
on a P2-shaped image. Three reasons remain mutation-untestable by label deletion because removing
them raises a `TypeError` first (`unavailable`, `revocation-never-established`,
`quorum-no-accepted-root`); each is hit positively by an exact-label case. The first survey output
is preserved (`claude-out/io/self-guard-survey.json`). I then RE-MEASURED over the supplementary set
(`self-guard-survey-r2.json`): 16 of the 17 are now killed; one (`absence-source-binding`) still
survived, so `fixtures-check-r3.json` adds its negative and shows the case admits with that guard off.
Measured state: every reason is now either killed by an exact-label case or is one of the three
`TypeError` reasons above. A join-level
`operation-action` mismatch of action/kind is unreachable because the 231 shell already closes
that pairing (it refuses `shape:OperationInputV1`); only the event-variant mismatch reaches it.

## Honest native/production boundary

Every join returns a string ending in `-bound-only` / `observation-only`. Not produced or claimed:
signatures, thresholds, envelope admission; native absence, exclusive creation, skeleton,
ancestor reconfirmation, fence, custody; the live complete-bucket census, fork detection,
smallest-digest witness choice and closure admission of N and n for restore; S4/S4.5 evaluation;
v14 transition dispatch; S6. Fixtures use fabricated bytes and toy capsules/descriptors that are
shape-valid under the 231 defs but are not reachable lifecycle states.

## Design choices root should consciously accept or change

- `stagingName` on the creation input (useful for distinguishing competing creators; removable).
- `examinedOrphans` on the declaration (records what the census saw; it is not proof of cleanliness).
- `subjectKind` narrowed to two values from 215 C.1 — if `release` should ever be role-level,
  that is a 215 change, not a schema tweak.
- `roles` on install/continue are host-derived; the derivation rule from closure kind/namespace to
  role set is owed by the v14/215 owner and is NOT in this draft.
- `chain maxItems 16384` is my number (≈ what fits in 4 MiB); the 222 work profile still governs.
- EV-CLOCK is allowed alongside install/continue because their mandatory S4 can surface expiry
  causes; if root holds that CLOCK belongs to a different operation, remove it from `EVENTS`.

## Pins

Frozen / verified: `canonical.py` d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442 ·
primary `revocation.schema.json` (v8) 143027369ccd150449cfe5b45d38645e62931002f47cd73e8cea22d38547fad4 ·
227 r8 archive 9cedf041…8cde (EVENT-JOINS 3a9ff52a…, PENDING-JOINS f2bea10f… — live copies are
byte-equal to frozen r8) · PROOF-NODE-JOINS fd687e4e… · TIME-INPUT-JOINS 912110ff… ·
v14 `machine14.json` from verified 226 r3.
Live working drafts as read (unfrozen): 231 `private-trust-state.schemas.v1.json`
d9ac024357c1645727449bb38f940dbf886244e1d3959998a3e28b64d6857968 · 230 `INPUTS.md` 7f4bf234…,
`trust-context-inputs.v1.json` 278b4102…, `transition-input-check-r1.json` f3cd2b88… ·
215 `OWNER.md` a48e122cc60337a9290a3d3210c9a9d8eb64a31194334d56abc3b141cd072ae9 ·
222 `PERSISTENCE.md` f9963414…, `COMMANDS-AND-RESTORE.md` 3a75d177… · 224 `CREATOR.md`
55a6b0393be505a8cfea36b2b72c9c41afdf81a6278004d03707c11e82a8f035 · 226 `AUDIT-JOINS.md` e66950f9…

Limits of reading: 215, 222 PERSISTENCE and 224 were read by targeted sections (restriction/quorum,
predecessor proof/restore, creation steps), not end to end; 226 AUDIT-JOINS and 203/201 carrier
text were not re-read for this task (no field here touches the carrier). Live drafts may have
moved since I pinned them.
