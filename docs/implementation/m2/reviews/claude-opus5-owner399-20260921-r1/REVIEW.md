# Independent review — corrected initial-root owner 399

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Bounded owner/reference review, document and model only; no native work was needed or done.

**Top verdict: ACCEPT-DESIGN-UNIT**, with **two non-blocking required findings**.

All four of my 397 findings — C-1, C-2, C-3 and C-4 — are closed, and the 398 scope point is
addressed. I checked the closures against the selected schema and model rather than against the
draft's own account, and two of them are now backed by measurements the unit itself does not contain.

C-3 was my error, and 399 corrects it the right way: it **preserves** the selector I would have had
deleted, and fixes the actual defect, which was scope.

---

## 1. Verification

### Pins and members

| Artefact | Declared | Observed | Match |
|---|---|---|---|
| `…/trials/initial-root-binding-proposal-399/subject.tar.xz` | 37 120 B, `7d51ca66a116dbdc9e94f48962b42845edfe8e4f6af4d605a7c79b78773fe07a` | identical | ✓ |
| `…/trials/initial-root-binding-proposal-399/subject.json` | 5 714 B, `7404e7058c31964683496b068981554c96089344d4eae1ad9ccef900f8fa933e` | identical | ✓ |

Both verified **before** extraction; extraction only into this review directory. **37 / 37** members
verified byte-for-byte and by sha256: 0 missing, 0 extra, 0 mismatched, 0 unsafe.

### Source anchors — 40 of 41 live, the 41st historical exactly as declared

**41 anchors; 40 match live. All 16 product anchors match at `cd5af4d`.** The single live mismatch is
the declared one:

| Anchor | Declared (= `cd5af4d`) | Live now |
|---|---|---|
| `crates/platform/src/filesystem.rs` | 73 907 B, `9a02dcbb…` | 81 671 B, `87636b86…` |

That is a historical code anchor, still resolving exactly at `cd5af4d`; the live divergence is the
runtime32 integration. No 399 pin is stale and none was edited.

### Evidence provenance and replay

The carried 392 artefacts are **byte-identical to my own retained 392 copies** — `preinstallation_model.py`,
`publication_model.py`, `check_preinstallation.py`, `check_publication.py`,
`check_digest_compatibility.py`, `lineage_probe.rs`, `run_lineage_probe.py`. `surface_model.py` is the
only model that changed, as expected.

| Check | Result | Frozen output reproduced |
|---|---|---|
| `check_surfaces.py` (**39** cases, new) | PASS | `surface-checks.json` identical |
| `check_preinstallation.py` (historical 392) | PASS 54 | identical |
| `check_publication.py` (historical 392) | PASS 36 | identical |
| `check_digest_compatibility.py` (historical 392) | PASS 7 vectors / 9 refusals | identical |

The seven lineage checks are carried 390 evidence and were **not** rerun; my own 390 rebuild remains
the record. No fresh-native or composed-creator claim is made or implied.

---

## 2. C-1 — closed, and verified against the selected schema

The new Diagnostics text states that `DoctorResult.defectsFound` is a **Uint53 COUNT, not a boolean**,
excludes the single reserved informational code from that count *and* from the condition selecting
`DOCTOR.DEFECTS_FOUND`, and says plainly that this **"explicitly replaces the selected
`workflows_model.v1.py` `doctor_report` `len(defects)` calculation"**.

I checked the three things that decide whether that is implementable.

**(a) Both prior wordings were wrong; 399's is right.** `invocation-v5.schema.json` `$defs/DoctorResult`
has `reportProduced: boolean` and `defectsFound: $ref … Uint53`, and `common-v4.schema.json` defines
`Uint53` as `{integer, minimum 0, maximum 9007199254740991}`. `workflows_model.v1.py:2055` sets
`defectsFound: len(defects)`. So it is a count, and 399 names it as one.

**(b) The amendment is representable without a schema change.** I validated candidate payloads directly
against `$defs/DoctorResult`:

| Payload | Valid? |
|---|---|
| `defectsFound: 0` with one `defects` entry — the 399 healthy shape | **valid** |
| `defectsFound: 1` with one entry — today's shape | valid |
| `defectsFound: 1` with zero entries | valid |
| an entry coded `INSTALLATION.DURABILITY_NOT_CHECKED` | **invalid** |
| 257 `defects` entries | **invalid** |

So the schema does **not** enforce `defectsFound == len(defects)`; that equality lives only in
`doctor_report`, which is exactly what 399 amends. 399's claim of "no new field/severity/parity" holds:
`DomainDetail` is `additionalProperties: false` over `{code, remedy, subject, purgeDisclosure}`, so
a severity field is not merely undesirable, it is unrepresentable.

I chased one candidate finding here and it did not survive. `workflow-cases.v1.json`'s
`envelopeVectors/reject[1]` carries a doctor payload with `defectsFound: 1, defects: []`, which looked
like a selected rule that count must equal length. Validating it shows it is rejected for its
`termination.class` (`policy-failed` is not one of `success`/`operational-failed`/`interrupted` for
this kind), not for the count. I record the dead end because it is the reason I can state the positive
result with confidence.

**(c) The reserved-slot arithmetic is real.** `defects` is `maxItems: 256`, and 257 entries are invalid.
399 reserves one slot, so the actual-defect capacity is 255. Probe Q3 confirms the model: 255 actual →
count 255 with 256 entries; 256 actual → refuses `'cannot produce bounded report'` and **latches**. No
silent truncation.

**My C-1 objection is genuinely answered.** Probe Q1: a healthy complete installation yields
`defectsFound = 0` with the note present, so the selected golden's instruction — *"CI must inspect
`doctor.defectsFound`"* — recovers its signal, and `DOCTOR.DEFECTS_FOUND` no longer fires on every
healthy run. Probe Q2: one actual defect plus the note is 1. Probe Q5: a caller cannot smuggle the
reserved code in as an actual defect to inflate the count — it refuses.

---

## 3. C-2 — closed

*"Only `doctor` carries this informational note. `trust doctor` and `store status` do NOT emit it:
their selected floors/migration/lease fields are not diagnostic-note channels, and this owner adds
none. … omitting this note is not a durability assertion."*

That is option (a) of the three I offered, and the cleanest one. Probe Q4: the model now has distinct
`TRUST_DOCTOR` and `STORE_STATUS` modes returning `existing-diagnostic-fields` with **no note, no count
and no defects list** — the surfaces are no longer indistinguishable, which was the reason my 397
review said the model could not have caught the problem.

---

## 4. C-3 — closed, and it corrects my error rather than deleting the selector

I verified the facts myself for the separate fact addendum: selected identity-and-evidence §5,
"Read-only recovery selectors", line 1685 defines `recover(ExecutionId)` taking the `SHARED-READ` lease,
and line 1702 says of it "…no new execution grant, **no fence acquisition** and no wait on a writer."
My C-3 claim that it had no referent was wrong, and wrong because I inferred absence from a truncated
search.

399 does the right thing with that: the selector is **removed from the fenced SHARED-READ CLI list**
and given its own paragraph — "**Separately owned internal recovery selector — not a CLI command**" —
citing identity §5, naming `architecture/commit-recovery-readonly.v3.md` as its bounded-algorithm owner,
distinguishing it from `repair recover REQUEST-ID`, and stating that this owner introduces no
root/parent barrier, new fence, binding allocation, creator route or alternate result classification
into it. The defect was scope, the fix is scope, and a legitimate selected selector survives.

---

## 5. C-4 and the 398 scope point — closed as disclosure

The fifth model gap is listed in the README and §10. Probe Q7 confirms it is genuinely still open and
honestly labelled: `'backup'` does not appear in the preinstallation model, and no check composes
`initial_storage_choice` with `parents()` or stage allocation. 399 does not claim closure.

The 398 point is scoped rather than waved away: the creator prohibits *application-initiated* network
requests, with an explicit sentence about native OS name services and caches, and no promise of
isolation from them and no environment or local-file shortcut.

---

## 6. Required findings — two, both non-blocking

### RF-1 — the reconciliation list omits the selected v1 checker and its doctor vectors

§9 is otherwise exemplary: it names the D9 mapping, the goldens, registration of **both** new
`DomainDetailCode` values "in the selected closed common schema and its generated bindings", the
`doctor_report` count/termination amendment, `Uint53` rather than boolean, healthy0/mixed1 rendering
goldens, the trust-doctor/store-status no-channel goldens, the no-fence preservation and the
endpoint-only inventory override.

It does not name `check_workflows.v1.py` or `workflow-cases.v1.json`, which are selected and do exercise
this exact join:

- `check_workflows.v1.py:1448-1450` calls `M.doctor(True, [two defects])` and asserts
  `rep['defectsFound'] == 2` **and** `must_valid('doctor.result-schema', …#/$defs/DoctorResult', rep)`.
- `workflow-cases.v1.json` carries doctor vectors with `defectsFound` 2 and 1.

Once `doctor()` appends the reserved note, that call's result gains a third entry whose code is
**invalid until the enum amendment lands** (measured in §2), while its count stays 2. The assertion on
the count still passes; the schema validation does not. Since §9 already names generated bindings, these
belong in the same list.

*Required:* add `check_workflows.v1.py`'s doctor assertions and `workflow-cases.v1.json`'s doctor
vectors to the artefacts the amendment must update, and state their ordering relative to the enum
registration.

### RF-2 — the actual-defect capacity change is implied, not stated

*"Reserve one of its 256 entry slots for the informational note before assembling a complete-root
report."* The consequence, measured in Q3, is that the **actual-defect capacity drops from 256 to 255**:
a complete-root report carrying exactly 256 actual defects was representable before and now refuses.
399 correctly forbids silent truncation, but never says the capacity changed, and the goldens list does
not include the boundary.

*Required:* state the 255 actual maximum for a complete-root report explicitly, and add the boundary
(255 admitted, 256 refused-and-latched) to the rendering goldens §9 already requires.

---

## 7. Observations

- **O-1.** A verified precondition worth surfacing: **neither new code can be emitted today.**
  `INSTALLATION.DURABILITY_NOT_CHECKED` is rejected by the closed 317-value `DomainDetailCode` enum
  (measured). So the enum amendment is not bookkeeping that can trail the behaviour — nothing in this
  design is representable before it lands. 399 requires the registration; this makes its status hard.
- **O-2.** No model in the unit can express that constraint. Probe Q6: the code is a bare string
  constant, and the models carry no schema binding, so the schema check in §2 is *outside* the unit's
  own evidence. Worth a line in §10 beside the five disclosed gaps.
- **O-3.** `defects-found: 0` alongside a non-empty `defects` array is a legitimately odd surface for a
  human reader. 399 handles it with the explicit rendering label "Informational: durability not checked",
  which is the right mitigation; I note it only so the goldens reviewer expects it.
- **O-4.** The exclusion is deliberately scoped to one exact code, with "do not treat unknown codes as
  informational". That is the conservative choice and it should stay that way if a second informational
  code is ever proposed.

---

## 8. Limits

- **Level:** document and model reading, archive/anchor verification, model replay and probing, plus
  direct validation of candidate payloads against the selected `DoctorResult` schema.
- **No native work**, as instructed; none needed. Native source396/runtime33 is reviewed separately and
  neither review depends on the other.
- **Not qualified:** native eligibility producers, actor/custody/profile qualification, P0 construction,
  shared budgets, crash and power-loss behaviour, GC, Linux, release.
- **Not rerun:** the seven supplied-lineage checks (carried 390 evidence).
- **Not re-reviewed:** runtime32/33, inventory59, registry-v2, the 391/396 native work.
- **Unselected references remain unselected:** this owner, S9.3, `store-instance-lineage.v1.json`,
  `host-foundation-completion.v2.md`, 215. 399 is not a formal passage successor; selection requires a
  newly reviewed successor and root assent.
- **Replay caveat:** the four replayed checks run the author's scripts. The independent parts are the
  397→399 diff, the byte-identity of the carried 392 artefacts against my own copies, the exhaustive
  `defectsFound` search across the selected corpus, the direct schema validation, and probes Q1–Q7.

---

## 9. Context HEADs — as of 2026-09-21T16:14:44-07:00

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `7ee1df7020c69172a92baf135fff84537dec8ea1` | "Record accepted publication layout and freeze native runtime review" | 2026-09-21T16:08:50-07:00 |
| product | `4b298dae44e553e8317cf68350f5201cd3fc6771` | "Select directory publication module layout with explicit inherited descriptions" | (clean) |

Stated as of that sample only; the byte pins above, not these labels, are the authority.

---

## 10. Attestation

Read-only against live, frozen, history, product and lock. No byte was edited, no pin was edited, no
select script was run, no native build, no commits, no pushes. All writing went into this review
directory; extraction went only there.

This grants no root assent, no formal selection, no passage reconciliation, no native owner or writer
permission, no current authority, no S9.3 or 215 adoption, no M2 completion and no release
qualification. Every earlier report — including owner397 and its separate fact addendum — is untouched
and keeps its own standing.

Reviewer: Claude Opus 5 (1M context).
