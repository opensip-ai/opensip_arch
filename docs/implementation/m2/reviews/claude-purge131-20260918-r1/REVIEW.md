# Independent bounded review — purge admission and complete-output reference 131

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-18.
Request: `purge131-20260918-REQUEST.md`. Scope: the delta of frozen `purge-reference-checkpoint-131` over frozen 127 —
the concrete form of the D3–D6 decisions I adjudicated (r1–r3) and of my output-detail adjudication: pin-budget law,
legacy progress / no-op / import-restore, closed direct and one-step refusal, observed availability and null
receipt, four public details, both schema majors, inventories, model, contracts, mandatory checks. **Pure reference
only**: no pin store, spool, renderer, deletion ordering or host effect exists here and none is inferred from passing
tests. The 127 clock-range defect is unchanged and tracked separately. No frozen/selected edit; scratch copies only
(`-I -B`, `PYTHONDONTWRITEBYTECODE=1`, 0 stray `.pyc`); no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,211,840 bytes, SHA-256 `38750a3033529103f8ccc092d9c5e21483f849ef58b5d1e9093bf8d25e3859e2` = request and `archive-pin.json` |
| Members | 1,598/1,598 regular, length + SHA-256 equal to the manifest, read from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,286/1,286 equal; none unpinned |
| Parent | `parent-inputs.json` (1,284) equals **my own** verified 127 extraction and its `frozen-candidate.json` |
| Changed | **19 changed + 2 new = 21**, as stated: registry, two inventories, six schemas (3 × 2 majors), workflow model + checker, `check-integration.py`, two contracts, five source-pin closures; new `foundation/pin_budget_reference.py`, `workflows/purge_checks.v1.py` |

## 2. Owner checks, fresh scratch, required order
envelope (168 + 145 + 1,803 + 61 + 6,000) → integration 423/0 → security 581 + sweeps → integrated carrier 435/0 →
workflows **2,117/2,117** → foundation 231/231. All exit 0. The retained r1–r3 integration failures are what the
README says they are (examples missing newly required members); I re-ran only the final tree.

## 3. Evidence (all under `claude-out/probes/`)

**3.1 Byte counter = real bytes** (`size_probe.py`). 4,000 random inventories over a 33-symbol adversarial alphabet
(all short escapes, NUL/U+0001/U+001F, DEL, U+0080, U+07FF/U+0800 boundary, U+2028/2029, BOM, U+FFFF, U+10000,
U+10FFFF, combining sequences, `<>&'`): counter = the tree's canonical encoder = an independent stdlib encoding in
**4,000/4,000**; 0 refusals by the encoder of anything the counter admits.

**3.2 Exact ceilings.** An inventory of exactly 2,088,960 bytes (1,361 pins, both majors): counter = canonical =
stdlib = 2,088,960; `within-budget`; admitted. One byte more: `over-limit`, `REFUSE evidence.pin-byte-limit`.
A useful fact I did not expect and the README does not state: **with ASCII names the byte ceiling is unreachable** —
4,096 × (256 + 39) ≈ 1.2 MB — so for ordinary names the *count* ceiling always binds first, and the byte ceiling exists
for escaped/multi-byte names (my first fill needed 7,082 ASCII pins and was refused on count; log kept).

**3.3 Representability closure — confirmed independently, to the byte.** Closed forms at the exact disclosure
ceiling with every optional member maximised:

| Case | direct | one-step |
|---|---|---|
| default remedy, no correlation id | 4,178,951 | 4,179,638 |
| + correlation id 128 × U+0001 (6 bytes each) | 4,179,744 | 4,180,431 |
| caller remedy 1,024 × U+1F600 + correlation 128 × U+1F600 | 4,187,408 | 4,188,095 |
| **caller remedy 1,024 × U+0001 + correlation 128 × U+0001** | **4,191,760** | **4,192,447** (`terminationEmitted:true`; `false` adds the owner's 1 byte → 4,192,448) |

Both maxima equal the owner's figures; overhead 13,840 / 14,528 ≤ 16,384; limit 4,194,304. The answer to "are optional
fields / deep copies / IDs / remedy / correlation fully accounted?" is **yes**, for a structural reason worth
recording: every identifier in the closed forms is fixed-width by pattern (`req1_`, `run2:/run3:`, `prj1-`, `exec1_`),
`mode` is three booleans, the closed validators admit no `projectRoot` (4,096), `invocation`, `diagnostics`,
`agentHints`, `retentionDisclosure` or `cancellation`, and the only free text is `remedy` (×2 copies) and the
correlation id, both bounded in scalars with a 6-byte worst escape. The final `canonical()` size check remains in both
validators, as required.

**3.4 Schema closure in both majors** (`schema_probe.py`, schema only, no host validator): 15 single-change
counterexamples per major — pinned envelope without `purgeRefusal`, with `invocation` / `diagnostics` / `agentHints`,
non-null receipt, RunId of the other major, 4,097 pins, a 257-scalar name, `purgeRefusal` on a pin-limit / fallback /
legacy-projection envelope, rejected pinned StepResult without the projection, projection on a completed step,
wrong record major — **all invalid in legacy (2/1) and in evaluator3 (3/3)**; a 256-scalar non-BMP name (1,024 UTF-8
bytes) is valid in both, i.e. the limit really is scalars.

**3.5 Mutation law** (`law_probe.py`; ceilings shrunk by patching the module constants so random search crosses all
three): 200,000 before/after pairs against an oracle written from the contract paragraph — **0 differences**; row
order never changes a disposition; a pure release is never refused from any state, including legacy long names;
a lawful inventory never leaves the budget; first publication never admits an over-limit set. Totality: 180,000
calls with junk (non-lists, dict subclasses, unhashable ids, surrogates, NaN, non-bool flags): only
`InventoryUnavailable` escapes; **0 foreign exceptions**; malformed structure is refused before any indexing.

**3.6 Workflow compatibility** (`workflow_probe.py`, `workflow_probe2.py`). The closed record refuses every tampering
I tried (retry policy, optional requirement, second attempt, completed outcome, receipt, target, project, added
cancellation / retentionDisclosure, malformed containers — 16/16) and the direct form 12/12 alias-free tamperings,
except the two in F-1/F-3. Overflow fallback: 996 bytes in both majors, closed member set, every tampering refused
(remedy, exit, faultCause, subject, added projection), human/json/agent parity identical with explicit
`purge-disclosure: null`, unknown format refused. Detail ↔ D9 route: `OUTPUT.DOCUMENT_BOUND_EXCEEDED` is
schema-invalid on any other row, `EVALUATION.OUTPUT_BOUND_EXCEEDED` stays valid on the same row (the inverse route),
a pin-limit detail is invalid on the serialization row. Through the **general** runner an explicit render step after a
rejected purge behaves lawfully: gate `terminal` → render runs, aggregate `request-rejected`/2 with the purge detail;
gate `completed` → render skipped, same aggregate; SIGINT before render → `interrupted`/130, phase `before-settle`;
retry on the purge mutation is refused by `validate_dag`.

**3.7 Mutants.** Owner's twelve: script read; in-memory, no pin gate, each names its failing check. Mine,
complementary (28, all compiled; stage 1 the owner's mandatory checker, stage 2 behavioural differential or a targeted
counterexample for every survivor): **19 killed** — 16 by a named failing check, 3 because the mutated model's own
output was refused by a schema or a checker lookup raised (behaviour of the mutant, not a load failure). They cover 13
of 14 budget mutants (name law on untouched names, bytes vs scalars, no-op ignoring kind, duplicates, empty names,
each byte-width rule, commas, runId, status ignoring names, precedence, receipt on no-op, surrogates) plus
errors-equality, relabelling malformed as legacy excess, replay-key join, parity null, legacy exit and the fallback
remedy. **9 survived**: 3 equivalent (the `old <= ceiling` disjunct is implied — `new > ceiling ≥ old ⇒ new ≥ old`,
0/30,000 differences; an attached `invocation` and a two-step record are already refused by the schema), the
false-remedy mutant (F-1), and **five genuinely unpinned joins** — T-1 below.

## 4. Findings

- **F-1 (medium, item 4 — "no false deletion claims") — the closed direct form does not pin its remedy.**
  `pinned_purge_refusal` takes `remedy=` from the caller and `validate_pinned_purge_refusal` accepts any bounded text:
  an envelope whose two detail copies say *"Purged successfully; all pins were deleted."* is **accepted**, and a
  mutant that changes the default text to *"Purge completed and pins deleted…"* passes all 2,117 checks. The other
  three new forms are pinned (the fallback's remedy is a schema constant; tampering is refused). The refusal that
  carries the pin inventory is the one place where a false statement about deletion matters most. Pin it the same way
  (fixed constant, equality in the validator, or a schema `const`); as a side effect the worst case in 3.3 drops by
  ~11 KB and the reserve stops depending on caller text.
- **T-1 (medium as a set) — five joins of the new validators are unpinned** (`survivors.json`; original refuses /
  behaves correctly, mutant does not, mandatory checker silent):
  1. the direct validator's **own budget re-check** — a hand-built envelope one byte over the disclosure ceiling is
     accepted once that check is removed (the schema cannot count bytes, and the envelope still fits 4 MiB);
  2. the **subject = RunId join** of the direct form;
  3. **aggregate termination = step termination** in the one-step record (the aggregate may name other pins);
  4. the **fallback's major for a legacy invocation** — "always 3" survives: only a major-3 overflow is tested, so a
     major-1 record could be answered with a major-3 envelope;
  5. the **per-code pin-limit remedies** — all three codes returning the name remedy survives.
  Each needs one negative case; 1–3 are the cross-field joins a JSON schema cannot express, which is exactly why the
  host validator exists.
- **F-2 (low–medium, item 3) — the general workflow owner cannot produce the pinned refusal at all, so its
  aggregate behaviour is established by hand-built records only.** `run_invocation` on the same one purge step yields
  a record that is **schema-invalid** (its rejected StepResult has neither `purgeDisclosure` nor `purgeRefusal`). I
  checked that this predates 131 (identical on 127), so it is not a regression — but 131 now leans on "explicit
  profile render remains an ordinary aggregate step", and the owner's aggregate is two copied purge steps assembled
  by hand, never passed through `validate_dag`/`run_invocation`. My 3.6 runs show the gate/cancel laws are compatible;
  what is missing is a runner path (a `rejected` observation that carries the projection) so that compound, cancel and
  retry behaviour of a *pinned* step is tested by the owner of those laws rather than beside it.
- **F-3 (low) — declared array order is not enforced on the disclosure.** Both schemas mark `activePins`
  `x-opensip-order: by pinId`, the constructor sorts, but both validators accept an envelope whose two copies are
  identically **unsorted**. Byte size and completeness are unaffected; byte-stable goldens and any consumer relying on
  the declared order are. Either enforce it in the validator or say the annotation is advisory for this array.
- **N-1 (design note, item 3) — purge is now the only one of 19 mutation commands without a `render` step**
  (`agent-serve` is the only other render-less command). I found no workflow law that this violates —
  `TERMINAL_GATE_KINDS`, retry and DAG rules are per-step, `terminationEmitted` is a supplied delivery fact, and the
  inventory still declares formats and parity fields — so it is compatible. But it is an asymmetry introduced to buy
  the closed one-step guarantee; write the reason next to the inventory row, or the next editor will "fix" it.
- **N-2 (policy note, item 1) — the result-based law admits *creating* pins while a ceiling is still exceeded**, as
  long as the batch nets a strict decrease: 9 → 8 → 7 → 6 (ceiling 5), each batch releasing two and creating one, all
  `ADMIT`; likewise release-one-plus-rename-one while over count, although a rename alone is refused. That is
  consistent with "evaluate the complete result" and is monotone, but it sits oddly beside the contract sentence
  "release named pins first, then create or rename under the normal ceiling". Decide which is the rule and say so.
- **N-3 (note)** `first_publication=True` with `before == after` returns `ADMIT` with `receiptRequired: False`,
  while the same no-op otherwise returns `NOOP`. Harmless, but two spellings of one outcome; and what `before` means
  for a first publication (destination inventory? always empty?) is not stated.
- **N-4 (note)** A malformed legacy inventory (duplicate identity, empty name, unknown kind) makes *every* mutation,
  including a release, `unavailable`, and purge cannot disclose it. That is the honest direction and the contract says
  "restoration"; it is the same no-path class as 127 C-3 and deserves the same explicit sentence in the remedy owner.
- **N-5 (note)** `command-inventory.v1.json` was re-serialised with `§` → `§` throughout: ~70 diff lines for a
  one-line semantic change (v3 shows the one line). Semantically equal; it makes the delta harder to audit.
  `pinned_purge_refusal` also returns `errors[0]` and `termination.domainDetail` as the **same object** (my first
  tampering probe was fooled by it; rerun alias-free) — harmless in a pure reference, worth a `deepcopy` before any
  host code imitates it. `pinned_purge_output` with an empty pin list raises `PINNED_PURGE_UNREPRESENTABLE`, which
  mislabels "nothing is pinned".

## 5. Unresolved limits
Everything here is a pure function over supplied observations: same-inventory, lease, caller identity, atomicity of
mixed batches, observed availability, immutability of pin facts, spool creation/cleanup, renderer behaviour, and the
ordering "overflow detected before any deletion" are **assumptions stated in text**, not tested effects. Generated
Rust/TypeScript consumers are not refreshed. The byte law is verified against this tree's canonical encoder; a second
implementation must be checked against the same corpus (mine is reusable: `size_probe.py`).

## 6. Bounded verdict
**131: reviewed, no blocking finding. The byte counter equals real canonical bytes on 4,000 adversarial inventories;
the exact ceiling and one-over behave as specified in both majors; the 4 MiB representability claim reproduces to the
byte (4,191,760 / 4,192,448) with every optional member maximised; the schemas close the forms in both majors
(30/30); the mutation law matches a contract-text oracle on 200,000 cases with no foreign exception; the four details
are bound to their D9 rows and the overflow fallback is closed, constant-size and parity-equal. To correct before
selection: F-1 (remedy of the pinned refusal not pinned — a false deletion claim is accepted) and T-1 (five unpinned
validator joins). F-2, F-3 and the notes are lower.** Not approval of storage, pin mutation, spool, renderers,
deletion ordering, generated consumers, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `diffs/`, `owner/`,
`probes/{size_probe.py,size_probe.SLOW-r1.py,size-probe.json,size-probe.log,size-probe.FAILED-r2.log,size-probe.FAILED-r3-count-exceeded.log,law_probe.py,law-probe.json,law-probe.log,law-probe.r1-swapwalk-meaningless.log,workflow_probe.py,workflow-probe.json,workflow_probe2.py,workflow-probe2.json,schema_probe.py,schema-probe.json,general-runner-127-vs-131.json,mutation.py,mutation.json,mutation.log,survivors.py,survivors.json,survivors.log}`, `hashes.txt`.
