# Independent review — primary relocation 248 r1 and replay delivery 249 r1

**Standing:** bounded code review of frozen `command-composition-reference-wip-248-r1` and `trust-replay-delivery-wip-249-r1`. **Not** cumulative approval, installed source, native/current-effect authority, durable publication, receipt retention, or product qualification. Archived 247 review/evidence were not edited (`d5a7d732…4984`).

Python 3.12.13 `-I -B`, jsonschema 4.25.1. Sibling names reconstructed from **included** predecessor archives (plus previously verified 241/239 extracts). Frozen variant output directories were not overwritten. Hardcoded `/tmp/opensip-implementation` scripts were redirected onto a review-local work tree.

Public `acknowledge-restore` mapping onto OperationInput `restore-recovery` is owned by `trust-command-restore.v1.md`. Neither 248 nor 249 adds a fifth request leaf or action-string equality.

---

## Verification

| Archive | Bytes | Members | SHA256 |
|---|---|---|---|
| `command-composition-reference-wip-248-r1` | 11723044 | 1455 | `08105445b6c87c728ea33eb0b3087ec4509f218eaaf080d7705180612dcf9396` |
| `trust-replay-delivery-wip-249-r1` | 6220 | 14 | `3298e2b7b2cd5c13e9b94cad87b38635840cf35253dc0fdd36e144d678092c54` |

Pin, tar, member count, and every `subject.json` hash matched before extract; extracts rehashed in full. Standing on both subjects: Incomplete WIP, not approval or source selection.

Included predecessor tars match the already-reviewed pins: 242 r2 `4b649237…6188`, 243 r1 `d207de6c…d18f`, 244 r2 `ce13548b…996a`, 245 r1 `6c7b70fc…3647`, 246 r1 `8421fc04…2614`, 247 r1 `2747c1f5…c38b`.

249 `inputs.json` pins 248 relocated `delivery_reference.py` `8cee55f0…60c8` and workflows-and-surfaces `8d8551c6…3d05`.

---

## Part A — primary relocation 248 r1

Unselected complete snapshot: **1358** candidate files, **25** SHA deltas vs 243 r1 = **20** new subjects under `workflows/current` plus composition note, and **5** established pin inventories (**104** pin updates). Six current modules live in `docs/coop/design-corrections/workflows/current` with local pins (`current-source-pins.v1.json`). Security still loads `trust_operation_reference.py` from `../../security`; no security→workflow import.

Independent AST dump of every `FunctionDef`/`ClassDef`: **32/32** equal to included 242 r2 / 244 r2 / 245 r1 / 246 r1 / 247 r1 bodies (8+5+6+6+2+5). Relocated file SHAs differ only where imports, pin paths, and the 244 base-schema filename (`output-base.schema.json`) change. Class names match. Six relocated modules contain neither `m2-` nor `/tmp/`.

Schema `$id`s on current JSON remain prospective (`urn:opensip:proposal242|244|245|246:…`). No current `$id` overlaps a historical evaluator `$id`. Historical `evaluator3/command-envelope.schema.json` is byte-identical (`37498354…3027f`). 26 historical workflow schema files are byte-identical to 243 r1.

Current inventory **49** rows, first 45 JSON-equal to historical `command-inventory.v3.json`. `agent-serve` stays `steps: [query]`, `authorizationClass: none`. Relocated `current_agent_request` still refuses `mutating-agent-transport-owner-unavailable`. Current `store-gc` `scope_for_command` refuses `mutation-scope-owner-unavailable`. Historical generic evaluator/host are not upgraded by this relocation.

Isolated copy of the candidate tree imports `delivery_reference.py` with **no T siblings** and admits 49 inventory rows; altering local `request_reference.py` after copy fails the pin assertion before admission. That is self-contained candidate import, not an installed-source claim.

### Reproduction (redirected; frozen outputs not overwritten)

| Corpus | Result |
|---|---|
| Relocated 247 delivery cases | **38/38** equal frozen `composition-check-r1.json`, counters 9 / 17 / 6723, source `8cee55f0…60c8` |
| Integration checks | **5/5**: 49⊃45, 26 historical schemas, no temporary imports, isolated import pass, isolated tamper fails |
| Delivery omission controls | **4/4** core-equal frozen `delivery-variants-r1/results.json` (path SHA differs from local `S=Path` rewrite) |

### Root suites (inspected, not rerun)

Source-bound reports on this snapshot: foundation **231/231** PASS; native **477** PASS (PROPOSED, not product measurement); workflows **2193** (PROPOSED-NOT-SELF-ACCEPTED); security **580** cases PASS (synthetic); carrier **479**; integration **1787** (PROPOSED, independent review pending on that suite). Envelope qualification: 168 explicit, 147 composition, 1803 historical, 47 explicit differential, 55 actual replay-crypto, 6000 fuzz. Those receipts do not qualify native effects/custody.

---

## Part B — prepared replay delivery 249 r1

Prepared **replay receipt** binding over 248, not permission to repeat an effect.

Normative join (workflows-and-surfaces §1, pinned): a same-scope **COMPLETED** receipt permits delivery replay with **no second effect**; failure/unknown/incomplete uses recovery law, not blind re-execution. The original receipt is immutable; replay delivery is a **separately identified** receipt with new attempt binding and `replayed=true`. Identity remains `receipt2:` + H(`workflow.mutation-receipt`, object without `receiptId`). `ExecutionId` is outside the idempotency key; each attempt keeps its own. Installation scope follows the 242 owner, not a fabricated ProjectId. Repair-apply’s content-derived `{operation,projectId,repairPlanId,baseSnapshotId}` key is **not** generalized.

249 implementation matches that scope:

1. Same Operation loads original D/outcome; original `effectOutcome` must be `COMPLETED`.
2. Fresh host attempt: same `requestId`/`stepId`, **different** `executionId`.
3. 248 `prepare` runs on the **original** attempt derived from the retained receipt (validates original request/invocation/scope/expansion/context).
4. Supplied replay receipt must be canonical-equal to original except new `executionId`, `replayed=true`, recomputed `receiptId`.
5. Envelope copies original context and substitutes replay `receiptId`/`replayed`. Original D and original receipt bytes are not rewritten.

Standing `prepared-replay-delivery-only` with **nine** pending owners (247’s seven plus `original-publication-durability-and-current-replay-readmission` and `separate-delivery-receipt-retention`).

**COMPLETED + new attempt are grounded and precise here.** FAILED originals refuse `completed-original-required-for-delivery-replay`. INDETERMINATE cannot even be a typed original `TrustCommandOutcomeV1` (`shape`). Same `executionId` refuses `separate-replay-attempt-required`. Do not treat this as a general retry/effect grant or as repair’s cross-request content key.

### Reproduction

| Corpus | Result |
|---|---|
| `check_replay.py` | **41/41** equal frozen `replay-check-r1.json`, counters 9 / **22** / 6723, source `e86cc9a5…862c` |
| Omission controls | **4/4** core-equal: completed / separate-attempt / exact-receipt / shared-budget |

### Independent probes

| Probe | Result |
|---|---|
| Original store dict after prepare | unchanged |
| Original outcome bytes / `replayed: false` | unchanged; replay `receiptId` differs |
| FAILED original | `completed-original-required-for-delivery-replay` |
| Missing `commandOutcome` | `command-outcome-missing` |
| Same ExecutionId | `separate-replay-attempt-required` |
| INDETERMINATE original | `shape:TrustCommandOutcomeV1` |
| `trustContext` vs original 248 prepare | equal; envelope `replayed` flips true |
| COMPLETED + `operational-failed` delivery | `prepared-replay-delivery-only` |
| Fresh requestId borrowing completed D | `replay-same-invocation-required` |
| Repair content-key tokens in 249 source | absent; uses 244 `receipt_id` |
| `current_agent_request` | not called |

No native exploit is claimed by the four omission controls. Asserted signatures/effects in fixtures are not grants.

---

## Remaining (do not count closed)

Native retained-invocation/attempt custody, original publication durability and current replay readmission, separate delivery-receipt retention, metadata authentication/current effects, census, fence/barrier, mutating transport, GC sweep owner, two evidence commands, 51-command integration, M3–M6. 248 is not installed runtime source. 249 does not write a replay receipt into D.

---

## Verdict

- [x] Both archives/pins/members verified. Nested predecessor pins match. 247 report unchanged.
- [x] 248: **38 / 5 / 4** reproduced. 32 function/class ASTs equal; local pins; no temporary imports; no security→workflow import; historical evaluator bytes/URIs unchanged; current `$id`s stay prospective with no historical overlap; inventory 49=45+4; agent-serve read-only; current GC fail-closed; isolated candidate import works and detects local tamper.
- [x] 249: **41 / 4** reproduced. COMPLETED-only + new ExecutionId match the pinned same-scope delivery-replay law. Original D/receipt stay immutable; envelope carries replay identity and original context. Repair content-key is not generalized.
- [ ] **Not** installed source, native/current-effect authority, durable delivery, or command installation.
