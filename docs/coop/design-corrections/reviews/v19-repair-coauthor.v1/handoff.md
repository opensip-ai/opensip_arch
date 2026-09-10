# v19 repair coauthor — unmet-precondition mapping (bounded source phase)

## Technical assent

**Assent on the merits, with three wording corrections applied.** I checked ownership
before agreeing, not after. `public-detail-registry.v1.json` assigns every `REPAIR.*`
member `owner: "workflows"` with selector `common.schema.json#/$defs/DomainDetailCode`,
and the registry stores **only** code/owner/selector — it publishes no per-code meaning.
The sole live-contract mention of `REPAIR.EVIDENCE_RUN_UNAVAILABLE` is
`workflows-and-surfaces.md:532`. So no exclusive owning meaning is contradicted, no
narrower alternative is required, and the owning contract is the correct place — and the
only place — to say what the code means in this step.

**One honest qualification.** This is a *widening* of the code's published meaning, not a
pure restatement. §6's first paragraph gives one **sufficient** condition; the addition
makes the meaning cover both routes the code already travels. The model does not move;
the contract's stated meaning broadens. That is a legitimate owner action, but it should
be registered as one rather than as pure description.

## Original retraction vs this correction

CB7-SHOULD-1 claimed `unmetPreconditions[].code` must equal the deficiency token, so 11
of 16 outcomes were inexpressible. The blind retracted that in full; nothing here revives
it. This correction has a different subject: not whether the cause is expressible — the
typed `deficiency` field carries it — but **whether the per-requirement entry is emitted
at all**, and **which code it carries and why that code is shared**. Neither was stated.

Root is right to reject both new rationales.

**(a) Schema permissiveness ⇏ optional emission.** Observed: the schema admits an
unsatisfied requirement with an **empty** `unmetPreconditions`, and admits `applicable:
true` with an unsatisfied requirement, because `RepairPlanDescriptor` carries no
`allOf`/`if`/`dependentSchemas` (keywords present: `additionalProperties`, `description`,
`properties`, `required`, `type`). The `applicable` conjunction the clarification cited is
a *description string*, not a constraint. The argument therefore proves too much — the
same reasoning would make the `applicable` law optional. This contract already states the
schema-versus-admission division for the deficiency vocabulary and for `admit_atom`.

**(b) The alternative misnames its condition.** Observed: with the retained fixture's
`deadCodeRepairEligible=true` and a plan containing **both** unsafe actions
(`delete`, `replace`), the model emits only `REPAIR.EVIDENCE_RUN_UNAVAILABLE`;
`REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` fires only when `deadCodeRepairEligible` is false
(remedy names that record's own `reasons`) or the origin is `imported-prepared-declared`.
The clarification's example emits it while eligible is true. Its imported row also borrows
`IMPORT.ABSENT_FOR_PREDICATE`, which this same contract binds at lines 459/482 to an
*optional absent* import that "is not a gating deficiency" — the inverse of a gating
insufficiency. Both rows are shape-valid and both assert a false condition.

The blind's underlying objection still has force on the *name* alone: in this branch the
Run is available. That is precisely why the code's meaning must be stated rather than
left to its name.

**What survives and supports root:** the native `perRequirementConsumerBoundary` standing
says it "adds no D9 class, code, exit or **public detail code**", and its
`whatTheConsumerCarries` says a failing requirement "always has exactly one reported
outcome, so omitting it is never lawful". Sixteen new codes are excluded on the owner's
own terms.

## Changes required (all applied)

1. **CR-1, correctness.** "Retention or replay-assurance failure and per-requirement
   insufficiency share that code" reads as a closed enumeration. It is not closed: the
   model uses the same code at `workflows_model.v1.py:692` (non-retained Run, a Refusal)
   and `:1798` in `repair_verify` ("apply did not complete"), both outside preview.
   Integrated text is scoped: "Preview therefore reaches that one code by two routes."
2. **CR-2, duplicated normative text.** Root's closing sentence and "it must distinguish
   different causes" restate the published sentence they would follow. Dropped; the
   published sentence is preserved byte-for-byte.
3. **CR-3, precision.** The "not a purge claim" is now anchored to in-contract text by
   naming `evidence.purged`/`evidence.missing`, which line 1048 already carries and which
   the registry assigns to owner `identity`. Remedy fields use the backticked `relation`,
   `minResolution`, `deficiency` spellings used elsewhere in §6.

## Controls (16/16 passed) — actual observed values

Labelled **synthetic fixture adapter** over the frozen model and the retained
`repairScenario` fixture; `repair_preview` called directly as the retained checker calls
it.

| control | applicable | entries | code | remedy |
|---|---|---|---|---|
| retained+replayable Run, unsatisfied native req | false | **1** | `REPAIR.EVIDENCE_RUN_UNAVAILABLE` | `…references@resolved-binding (native: resolution-incomplete)` |
| same, different cause | false | 1 | same code | `…(native: external-consumers-unknown)` — differs; different `repairPlanId` |
| imported requirement | false | **1** | same code | `…history-change@observed (imported: import-unmapped-only)` |
| available Run, all satisfied | **true** | **0** | — | — |
| unavailable (purged) Run | false | **1** | same code | `restore or regenerate the Run evidence; assurance must be replayable`; `evidence.purged` **not** emitted |
| both branches at once | false | **2** | same code ×2 | two distinct remedies |

Schema/authority distinction preserved: shape validity and admission behaviour are
reported separately and the first is never treated as evidence of the second.
`evidenceRunId` is unchanged and editing `unmetPreconditions` mints a different
`repairPlanId`.

## Sources

**Unchanged — the correction states existing behaviour.** Model, schemas and cases are
byte-identical; 0 files under `candidate-subject.v18` modified. No new code minted. No new
retained case needed: cases 2, 29, 30, 36 already pin all four behaviours.

## Limits

No host execution, no authorization execution, no product qualification. The local
`.probe-venv` is Python 3.14 / jsonschema 4.26.0 vs the checker's documented 3.12 /
4.25.1 — no parity claimed, checker suite **not** rerun, S1 corroborated independently by
direct schema-keyword inspection. Did not read or edit `v19-native-coauthor.v1`; did not
rerun the six units, refresh pins, edit current cases, or inspect unrelated histories.
Failed attempts retained in `probe-attempts.md`.

## Hashes

| artefact | sha256 |
|---|---|
| `workflow.before.md` (= frozen18 contract) | `a6e34134d73495a5ce32502173daf452bbc7b207c25e83f78c4571ef609bad29` |
| **`workflow.proposed.md`** | **`b3a3bf65ca0cd1bd00654e6dfc0f4f0a9814da96b59aca4e51bf318828721477`** |
| `proposed-paragraph.md` (root's draft) | `339e6d22fb4d7f57ca9ee6765e28d922fe1bf4c6d070a851364e97d745333017` |
| `integrate.py` | `3a646943bcde2bba2e86907e4dac6ab4b6f6b0c15f1add92e366087be245dfa0` |
| `probe_repair_unmet_mapping.v1.py` | `7e543dfec7a136722c96dbb395ef02f081d91ea4bb1c62801411e43331904e87` |
| `probe_repair_unmet_mapping.v1.json` | `29d8711b023fd512abda448f78eb782d31b3ddecfb541ec2c3f845c6ec82d460` |
| `probe_repair_unmet_mapping.v1.log` | `611958ce4746052d85601395444ee36eac2bb7feaa2aac61007da70f9d8c3730` |
| `probe-attempts.md` | `4a8ff2af2e0d98e31c3b92f980eb535c20b89cc787d80953753d4d75bb1351ad` |

Read-only sources observed: `workflows_model.v1.py`
`a268aa4b9e9089a51104365a6c82faf5b01602b84b1dd5adbf0384810e25f7bd`;
`repair.schema.json` `65d5f639fbfe02035924971722afbce183b3f52b48385bf25497eab69057424c`;
`common.schema.json` `16ff6419a12dc3df182ff6031b21ebc686cfb1401bd5a409a68e05a3063f7b81`;
`imported-evidence.schema.json`
`edce21a3c7905f215c019eddc5776e08e6cff59a6ceea4b4e422275ead594b9e`;
`workflow-cases.v1.json` `22b7443048ea5aefff8594ed35ab3ade1fe43594efba31f03e05e76943ae824d`;
`native-evidence.schemas.v2.json`
`9a5f33f49728726cc20fc36c6a26071647578e08d445c29574ebb83c9651944c`;
`public-detail-registry.v1.json`
`e54a395fdf40a33a7db9f94630ae7cc1f79b762014fbef804a9c03a754b53c0f`.

## Exact inserted bytes

Pure insertion at byte offset 45304 (`diff` = `634a635,649`, +1145 bytes, no
pre-existing byte changed), continuing S6's per-requirement projection paragraph:

> That unmet precondition is emitted once per unsatisfied requirement and carries the
> existing `REPAIR.EVIDENCE_RUN_UNAVAILABLE` code, which here says that the evidence Run
> cannot supply what this repair requires and asserts nothing about the Run having been
> purged or lost — `evidence.purged` and `evidence.missing` keep their own distinct
> meaning in query results. Preview therefore reaches that one code by two routes, the
> retained-availability and replayable-assurance failure of the first paragraph above and
> this per-requirement insufficiency, and the two are told apart by the remedy, which
> names that requirement's `relation`, `minResolution`, evidence plane and exact
> `deficiency`. `EvidenceRequirement.deficiency` remains the typed cause carrier: no
> per-deficiency detail code is minted, because the closed public registry is not where a
> per-requirement outcome vocabulary belongs. An unsatisfied requirement with an empty
> `unmetPreconditions` is **not** a conforming projection — the schema alone admits that
> shape, and the emission is decided at admission, the same division of labour already
> stated for the deficiency vocabulary.
