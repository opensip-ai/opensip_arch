# Independent review: combined reference101 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: adjudicate closure of my reference60 findings B1/B2/M1/M2 and L2–L5 and Unicode64 U-M1
in the frozen reference101 bytes; assess the checker and integration-fixture corrections; state interaction
with inherited 69/73 and with envelope66. **Bounded to the root / integration / UCD corrections.** It is not
approval of reference69, reference73, envelope66, any Rust draft, or the product, and it is not formal
selection.

## Bounded verdict

**Reviewed — the reference60 blocking findings are closed; three narrow follow-ups are required before
formal selection, none of which is a defect in the corrected gate logic.**

| Finding | Adjudication |
|---|---|
| **B1** generated `DomainDetail` enum drift | **Closed.** Follow-up F1: the new generator's drift check is not executed by any checker. |
| **B2** cross-unit pins | **Closed.** All five inventories verify; rebinding is confined to the changed files. |
| **M1** unpinned regressions | **Substantially closed — 11 of 16 reverted-correction mutants are now killed by the retained checker.** Follow-up F2: three behavioural mutants still survive (cheap to pin). |
| **M2** uncomposed chain / profile-set admission | **Closed for the case router and both composed boundaries.** Residuals R1–R3 below. |
| **L2** three statements of one rule | **Partly closed.** Threshold helper is shared; the reduced `_admit_root_semantic` duplicate remains (now unreachable through the public route). |
| **L3** detail string / nested codes / unbounded | **Closed.** |
| **L4** retained rules outside an exception boundary | **Closed as scoped.** Residual R2: the new composed boundaries themselves raise on malformed presented data. |
| **L5** sticky malformed continuity | **Closed — and my original wording was overstated;** the owner's clarification is the correct statement of behaviour. |
| **U-M1** interpreter-dependent reference | **Closed for the normative successor.** |
| Checker no longer overwrites input-schema failures | **Substantive and correct** (demonstrated old-vs-new). |
| Integration positive chain constructs a real successor | **Substantive and correct** — and it exposes something my reference60 review missed (see "Correction to my own reference60 review"). |

**Selection blocker outside the corrected logic (F3):** the 101 contract file carries the full envelope66
contract text by inheritance from 73, while envelope66 is changes-required and its schema/reference are not
in the 101 tree. Selecting this contract file would select that text.

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/reference-integration-checkpoint-101/subject.tar.xz` (1,847,184 B) | `a53e24c337b8960e8b4b031aa5910165d8e87d9e39c5f04222abd205ff5a424f` | = `archive-pin.json` |
| `subject.json` (1,318 members) | `685df346d18fc96f5e22384e431e6fd7c6fcd7e02e4a85a8dd78ceaebcb32c49` | every member re-hashed from the tar **before** extraction |
| `README.md` / `archive-pin.json` | `c0fba83e…4297c3` / `aa663a96…01d377` | |
| `frozen-candidate.json` (1,266 entries) | in manifest | all 1,266 candidate files hash-match; 0 unlisted files under `candidate/` |
| candidate model `security_lifecycle_model_v1.py` | `9a70bb5372dc63cc35959ab1fd2e26bac4da8f1f36f933f2715da3d1fd5195ae` | before-image `082f8681…537662` = parent73 |
| parent73 manifest (from `parent-inputs.json`) | `a3a6dde8…661301` | 14 files changed, 2 added, 0 removed vs parent73 |

Extraction refused nothing: 0 symlinks / non-regular members / absolute or `..` paths. Re-verified
byte-identical after all checks and probes. Every mutation or scratch run used a temporary copy under
`claude-out/` that was deleted afterwards; no `__pycache__` written into the subject. `git status` shows only
an untracked `m2/reviews/claude-storage-questions-…` directory, not mine.

**Changed vs parent73 (computed from the two manifests):** `check-integration.py`; the four existing pin
inventories; `security/check-security-lifecycle.v1.py`; `public-detail-cases`, `root-chain-cases`,
`root-schema-cases`, `trust-clock-cases`; the model; both workflow `common.schema.json`; the contract.
**Added:** `workflows/source-pins.v1.json`, `workflows/sync-public-details.v1.py`.

## Owner checks, re-run independently into fresh output (`claude-out/checks/`)

| Check | Result |
|---|---|
| `security/check-security-lifecycle.v1.py` | exit 0 — 490/490 cases, 12/12 sweeps, pins valid |
| `check-integration.py` (the correct owner path) | exit 0 — **412 passed, 0 failed** |
| `foundation/check-foundation.py` | exit 0 — 231/231 |
| `workflows/check_workflows.v1.py` | exit 0 — 1,816/1,816 |
| `native/check_native_evidence.v2.py` (report path redirected — it otherwise writes into the tree) | exit 0 — 477/477, 66 matrix cells |
| `workflows/sync-public-details.v1.py` (read-only mode) | exit 0 — `{"drift": []}` |
| model import under Python 3.14 / UCD 16 | `RuntimeError: metadata reference requires Unicode 15.0.0` |

These reproduce the reported counts. They are same-author tests; the adjudications below rest on my own
probes.

## Adjudication detail

### B1 — closed
Structural comparison of both `common.schema.json` files against parent73: identical outside
`DomainDetailCode.enum`; the enum equals the registry code set, sorted and unique; the **text diff is exactly
one added line** per file (`ROOT.RETAINED_SEMANTIC_POLICY`). So the generator's whole-file re-serialisation
did not disturb formatting, and "enum-only" is true. Integration (which aborted on reference60) now passes.

**F1 (follow-up, required before selection).** `sync-public-details.v1.py` is referenced by nothing except
the workflow pin inventory — no checker runs its drift mode. `check-integration.py:405-413` proves
*registry ⊆ enum* only; a stale or extra enum member, or a hand edit to one copy, is caught by nobody. B1
was precisely "a generated copy nobody re-checks", so the generator's read-only mode should be a checked
step (integration or workflows), with a retained negative.

### B2 — closed
For each of the five inventories (`security`, `foundation`, `foundation/evaluator3`, `native`, `workflows`):
every pinned path exists and hash-matches the candidate (1,252–1,256 pins each, 0 unverifiable, 0 duplicate
paths). Against the before-images: **re-hashed paths are exactly the changed files that inventory pins, no
additions or removals, and no non-pin member changed**; r2 re-binds only `check-integration.py` (plus, in
evaluator3, the four sibling inventories it pins). The r1 before-images of the four existing inventories
equal parent73. The reconstructed workflow inventory's pre-101 bytes are `6e75029f…` — byte-identical to the
foundation inventory's selected bytes, consistent with the stated retained45 reconstruction; I did not
re-derive that reconstruction from the 44 base + 45 delta myself (assumption 2).
Cosmetic: `security/source-pins.v1.json` still carries `status: UNACCEPTED-ROOT-POLICY-CORRECTION-60`.

### M1 — substantially closed (mutation evidence, `claude-out/probes/mutation.json`)
I reverted each correction one at a time in a scratch copy of the tree (re-pinning only the mutated model so
the checker would run) and ran the **retained** 490-case checker.

| Mutant (one correction reverted) | Retained checker |
|---|---|
| schema-2 extension tail removed | **killed** — 10 cases |
| schema-2 typed-absence rule removed | **killed** — 6 cases |
| retained v8 call removed | **killed** — 10 cases + sweep |
| malformed-continuity anchor fix reverted | **killed** — the fixture now asserts the writes |
| timestamp ASCII-digit grammar reverted | **killed** |
| calendar typed-refusal removed | **killed** — 3 cases |
| chain routing reverted to the primitive | **killed** — 5 cases |
| profile-set routing reverted to the primitive | **killed** — 1 case |
| threshold helper weakened to ≥ 1 | **killed** — 2 cases |
| retained-policy exception becomes admission | **killed** — sweep |
| detail bound removed | **killed** — sweep |
| **composition skips the accepted (stored) root** | **SURVIVES** |
| **composition checks only the first link** | **SURVIVES** |
| **threshold helper ignores `namespaces`** | **SURVIVES** |
| revocation authority string reverted to TR-INDEX | survives (prose constant; low) |
| UCD guard removed | survives (cannot fail under the 3.12 interpreter the checker requires; low) |

**F2 (follow-up, required before selection).** The three behavioural survivors are not equivalent mutants —
the unmutated model refuses each input (`survivors-inputschema.json`): a defective *stored* root with a good
successor → `ROOT.RETAINED_SEMANTIC_POLICY`; a good first link with a defective second link → same; an
active `TR-PROFILE` / `TR-REPAIR` with `namespaces: []` → `ROOT.TR_*_THRESHOLD_POLICY`. No retained case
covers any of them (no schema-2 case has an active extension role with empty namespaces; no chain case has a
bad stored root or a bad later link). Three fixtures close this. The UCD guard can be pinned without a
second interpreter by a sweep that reloads the model source with `unicodedata.unidata_version` patched.

### M2 — closed for the public route; residuals
- `run_case('root-chain')` and `run_case('profile-set-envelope')` now refuse my reference60 counterexamples:
  defective successor, defective **stored** root, defective second link, and profile-set over an unadmitted
  root; a schema-2 link under a `{1}` reader is `ROOT.SCHEMA_UNSUPPORTED`; state is reported unchanged.
- **Migrated fixtures are real.** After resolving the fixtures' templates through the checker's own
  resolver, every chain-rule negative (`CHAIN_GAP`, `CHAIN_BACKDATED`, both thresholds, `EXPIRED_NO_CHAIN`,
  `FINAL_EXPIRED`, `FINAL_FUTURE`: 8 cases) and all 4 positives run over roots that **pass the document
  boundary**; 6 cases are decided at the document boundary; and 2 cases
  (`composed-chain-refuses-R2badCoreStanding`, `…R2duplicatePublic`) are ones the primitive alone would
  **ACCEPT** — i.e. they genuinely test composition. All profile-set cases but the one deliberate negative
  run over an admitted root. (A raw scan of the fixture file reports the templates as `ROOT.SCHEMA_SHAPE`;
  that is an artefact of unresolved templates, not a defect — recorded because my first probe did exactly
  that.)
- **R1.** `verify_root_chain` and `admit_profile_set_envelope` remain importable and still ACCEPT the
  defective inputs when called directly. The contract now says so ("internal projected-rule primitives"),
  and the only in-model callers are the two composed boundaries, so this is a naming/visibility residual, not
  a hole in the routed path. An underscore prefix would make the statement enforceable by inspection.
- **R2 (medium, not a regression).** The composed boundaries are declared public but are not total on
  malformed presented data. 12,000 junk-typed mutations through `run_case` produced uncaught
  `TypeError`/`KeyError` in all three routes — e.g. a chain link without `root` (`KeyError` in
  `admit_root_chain`), `chain` not a list, an unhashable `signers` member, `state` without
  `acceptedVersion`. Chain links and signer lists are presented data. v8's law was "any exception inside the
  boundary is a refusal"; L4 restored it for the retained-rule call only. Same class as envelope66 E-B1;
  fix both with one rule.
- **R3 (low).** `admit_profile_set` hard-codes reader `(1, 2)` while `admit_root_chain` takes the reader
  set; and a composed chain refusal moves the descriptive text into `remedy`, so its public detail has
  `subject: null` where the document route has the bounded `ruleFailures=` subject. Neither is wrong;
  both are asymmetries worth a sentence in the contract. R3's reader point is the same gap as envelope66 E-M1.

### L2 — partly closed
`_extension_role_threshold_ok` is now the single threshold owner for the early gate and the chain primitive,
and the unreachable duplicate in `_preserved_root_policy` was removed (confirmed killed-mutant sensitivity).
The reduced `_admit_root_semantic` remains, with its own codes (`ROOT.TR_REPAIR_STANDING`,
`ROOT.KEY_REUSED_ACROSS_ROLES`, `ROOT.KERNEL_ATTESTATION_KEYS_POLICY`). Through the routed path those
branches are now dead: three chain cases that it used to decide are decided at the document boundary with
different codes (`ROOT.KEY_REUSE`, `ROOT.TR_REPAIR_THRESHOLD_POLICY`, `ROOT.TR_REPAIR_ACTIVE_UNDER_SCHEMA_1`).
Nonblocking; the honest end state is to delete the reduced function's root-shape branches or state that they
exist only for direct primitive use.

### L3 — closed
Through the real gate with 64 unbound keys: subject is **1,023 scalars** (reference60 produced 1,932),
ends `;omitted=24`, contains **no registered public code** and no `ROOT.` token, and the projected public
detail **validates against the workflow `DomainDetail` schema**. Arithmetic checked (200 reasons → 40 kept +
160 omitted = 200; length exactly 1,024); a single over-long reason degrades to `ruleFailures=;omitted=1`
rather than overflowing. Deterministic. Contract wording now matches the emitted grammar and states that
truncation affects explanation only, never evaluation.

### L4 — closed as scoped
`_RV8.admit_root` is wrapped; an injected exception refuses with the registered code (sweep, and my mutant
"exception becomes admission" is killed). The contract now also states that importing the v8 helper does not
verify its provenance and that it is TCB — the right disposition for the import-time coupling. See R2 for
the wider boundary.

### L5 — closed; my finding was overstated
I wrote that malformed continuity is sticky "until reboot". The code and the new contract paragraph are
right and I was not: the finding repeats only while same-boot `mono` is below the anchor; once it reaches
the anchor, ordinary continuity resumes. The retained fixture now pins the write set (mutant killed).

### U-M1 — closed for the normative successor
The model refuses to load unless `unidata_version == "15.0.0"` (verified under the 3.14 interpreter; the
owner's preserved `wrong-interpreter.stderr` shows the same). Differential against the reference60 model
over 12,000 mutated roots: **0 result differences, 0 detail-code differences, 0 exceptions** — the
corrections changed no admission outcome. Historical v8 stays directly importable without a guard, which is
the stated design ("consumed through the guarded successor"); `native/*_model`, `foundation/identity-model*`
and `artifacts/check-fact-plane.py` also import `unicodedata` for their own profiles — I did not assess
whether any of them implements the *metadata* profile (assumption 3).

### The two process corrections
- **Input-schema failure preservation — substantive.** I forced `inputValid: true` on
  `codex-profile-malformed-body` in a scratch tree and ran both checkers: the **old checker reports PASS and
  an overall pass; the new checker reports FAIL on `inputSchemas.envelope`**. The one-line change
  (`=` → `.extend`) is exactly the defect, and the fixture's corrected `inputValid: false` is right: the body
  is schema-invalid by construction. Other units' checkers were not audited for the same overwrite pattern.
- **Integration positive chain — substantive.** `root1`/`root2` in the schema fixtures are two schema
  variants of the *same* `rootVersion`, so they were never a lawful chain; the control now derives an
  explicit successor in memory. The retained r2 report (411/1) is the honest record of that.

## Correction to my own reference60 review
Reference60's migrated `root1`/`root2` already had identical versions, so its
`complete-root-chain-admitted` control would have failed with `ROOT.CHAIN_GAP`. I did not see it: on
reference60 `check-integration.py` aborted at line 413 (B1) **before writing a report**, and its `check()`
records failures without raising, so the earlier failure was masked. My statement there that the candidate's
only integration problem was the enum drift was therefore incomplete. Reference101's handling is correct.

## F3 — dependency-order finding: the contract carries envelope66
`diff reference60-contract → parent73-contract` shows 73's contract already contains the complete
envelope66 section, and 101 keeps it: the eight-kind carrier table, "`RECOVERY` is a proposed explicit
signed role token", "Reader support for added kinds and root2 must be declared explicitly", "callers cannot
invent signers or a bodyDigest", and a normative reference to `signature-envelope.schema.json`
(contract l.903–950). But envelope66 is **changes-required** (E-B1, E-M1, E-M2, E-L1, E-L2), its successor
is not frozen, and **neither `signature-envelope.schema.json` nor `envelope_reference.py` exists anywhere in
the 101 tree**. So the contract, as frozen, (a) cites an owner file that is absent, (b) asserts the
reader-support rule that no reference implements, and (c) states a projection-binding guarantee that 101's
own README correctly says is not provided ("still consumes explicit asserted signer TCB"). The root /
integration / UCD paragraphs are sound; the *file* is not selectable independently of the envelope
successor. Disposition options: split the envelope section out of this contract revision until its successor
is reviewed, or order formal selection so the envelope successor lands first. Either way this is a
sequencing decision, not a defect in 101's corrections.

## Inherited 69 / 73 — interaction only, not approved
The reference60 → parent73 model delta is small (41 changed lines) and I read it without reviewing it:
recovery — full-string hex grammar (`fullmatch`), a monotonic-expiry overflow refusal, calendar-valid epoch
and pending timestamps, pending-shape checked before authority comparisons, bounded `bootId`; platform —
ASCII-digit, full-string macOS build and Linux release grammars, `is True` / exact-integer observation
predicates. Interaction with the reviewed corrections: none found — they share only `ts()` and `HEX64`, both
of which moved in the stricter direction, and the differential above shows root admission unchanged. They
are **not** covered by this verdict: the recovery reordering (shape before quorum/counter) changes refusal
precedence and needs its own adjudication against S4.5; the platform predicates need review against S8/§8.4.
My mutation set did not target them.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction, and after every stage) | 1,318/1,318 from tar; 0 unsafe members; extraction unchanged |
| five unit checkers + generator drift mode (`checks/`) | all exit 0 with the reported counts |
| `probes/static_pins_enums.py` **r1** | **Failed — reviewer bug** (assumed every inventory uses `pins`; three use `files`). Preserved as `.failed-r1.py` + note |
| `probes/static_pins_enums.py` r2 | five inventories verify; whitelist-only rebinding; one-line enum diffs |
| `probes/dynamic.py` | composition attacks refused; bounded detail; 12,000-root differential clean; exception fuzz → R2 |
| `probes/chain_cases.py` | where every chain / profile case is decided, after template resolution |
| `probes/mutation.py` | 16 mutants: 11 killed, 5 survive |
| `probes/survivors_and_inputschema.py` | survivors are real gaps; old checker PASS vs new checker FAIL |

Interpreter: `/tmp/opensip-implementation/native-case15-reference-env/bin/python` (3.12.13 / UCD 15);
`metadata-reference-env` (3.14 / UCD 16) only for the load-refusal test. No cryptography was exercised; the
root checks involve none.

## Unresolved assumptions and limits
1. Verdict is bounded to the root / integration / UCD corrections. Reference69, reference73, envelope66 and
   all Rust drafts remain separately reviewable; nothing here transfers to them.
2. I verified the reconstructed workflow inventory's bytes and its consistency with the foundation
   inventory, not the 44 + 45-delta reconstruction procedure itself.
3. Whether any non-security Python owner implements the metadata NFC profile unguarded was not assessed.
4. Mutation testing covered the corrections in scope (16 mutants), not the whole model; a killed mutant
   shows a correction is pinned, not that the rule is complete.
5. Signer sets remain asserted TCB; composition proves document admission precedes projection, not that any
   signature was verified.
6. The four non-security unit checkers were re-run, not reviewed.
