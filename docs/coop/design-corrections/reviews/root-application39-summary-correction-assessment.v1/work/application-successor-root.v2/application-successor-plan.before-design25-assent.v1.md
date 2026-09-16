# Current prospective application — candidate25

Use application-completion-runbook.target-proof.v2.md and current-status.json for current task state. Candidate25 is frozen and byte-verified; passing reference suites do not grant acceptance. Fresh actual Grok whole-design review, NEW blind consumer and root assessments must complete before any receipt binding or assembly. Old source21/source24, consumer9/11/12 and draftv3/v6 references below are preserved preparation history, not current acceptance inputs. Future application tools are this reviewed-later v2 copy; v1 originals remain unchanged. No product implementation, commit or push.

## Preserved preparation history

# Evaluator3 application successor — preparation only

Standing: **not ready to assemble, freeze, launch, or activate.** No source acceptance of evaluator3 exists. This directory is coauthor preparation. Historical Claude source21 ACCEPT (`360c2758…`, `post-reset-review.v21`) does not accept successor bytes. Historical `consumer-b.v9` has no `blind-review.json`; Codex `blind-assessment.v9.json` has `rootBlindAssent: false`. Live activation file does not exist.

Root runs these tools only after: W/security listing join freeze of one evaluator3 subject, fresh actual Grok independent review of all five contracts, NEW blind with actual native TS/Rust full replay, and Codex design-assent + blind-assessment in the assembler shape.

## What to run later (not now)

1. Fill `input-review-receipt.schema.v1.json` against actual frozen + independent + NEW-blind bytes. Example is shape-only.
2. `bind-review-receipts.v1.py --receipt <filled> --out bound-review-receipt.v1.json`  
   Refuses historical source21 subject (unless explicitly v21), coauthor standing, known coauthor sessions, cross-vendor envelopes, missing findings lists, hash mismatch, same design/blind session.
3. `assemble-records.successor.v1.py --root … --out … --bound-receipt … --design-version --consumer-version --application-version`
4. `apply-advisory-records.successor.v1.py --root … --stage … --bound-receipt …`
5. Reuse unchanged from `application-assembly.v1`: `prepare-validation.py`, `freeze-application.py`, `check-finalizer.py`, `finalize-application.v1.py`, `verify-applied.py`. When copying support, also copy this directory’s successor adapters. Do not edit the assembly originals.
6. `launch-application-review.successor.v1.py` then `retain-application-review.successor.v1.py`.
7. Finalizer writes `docs/coop/design-corrections/application-activation.v1.json` **last**.

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.

## Input review receipt shape

See `input-review-receipt.schema.v1.json`. Decoder: `review_envelope.py`.

| Gate | Grok (authorized interim) | Claude (later credits; do not fabricate) |
|---|---|---|
| Public file | receipt-named `response.public.json` preferred; else `response.raw.json` | `response.json` |
| Success | `stopReason` **is** `end_turn` (not `stop_reason`) | `is_error` **is** `False` (key present) |
| Session | `sessionId` | `session_id` |
| Public body | nonempty `text` | Claude `result` / existing envelope |
| Thought | not a gate; strip for public view | not retained |
| Tool history | named `chat_history.jsonl`: `assistant.tool_calls` + `tool_result` | `~/.claude/projects/*/session.jsonl` `tool_use`/`tool_result` |

Review JSON (design and application ACCEPT; blind `ACCEPT-RECONSTRUCTABLE`):

- `verdict` or `overallVerdict`
- `subjectManifestSha256` exact frozen manifest SHA
- `newMustIssues` and `newShouldIssues` present as **empty lists**
- Design also: `arDispositions` AR-01..16, `fwDispositions` FW-01..15, `inheritedResidualDispositions` DR-001..011 + DR-011-R01..R16, `scopedReviewOwnerDispositions` DR-201..205 with accounted routing (`ROUTED-ONLY` or `ROUTING-ASSESSED-ONLY-NOT-APPLIED`, both authority flags false, nonempty scope/basis)

Codex blind assessment **required** fields (historical v9 does not satisfy): `rootBlindAssent true`, `fullRead true`, `actualSessionId` = decoded public session, `parentSubjectSha256`, `review.path/sha256`, empty `unresolvedRootMustIssues`/`unresolvedRootShouldIssues`, `newAdvisoryApplicationAccount` id-set equal to the blind advisories.

Do not bind this coauthor session `0d7f2cda-0e54-45e1-9a68-a8782587a8a0` (empty `response.raw.json` here; process standing is coauthor / no source acceptance).

## Exact evaluator3 record path / field updates

Staged under the future application package `files/`, effective only after independent application ACCEPT + activation. Not written live by this preparation.

| Path | Fields / action |
|---|---|
| `docs/coop/design-corrections/application.v1.json` | `designSubject`, `independentDesignReview`, `independentDesignReviewVendor`, `independentReviewerPublicLabel`, `freshBlindConsumerReview`, Codex assent/assessment, `conditions` 1–4 `MET-DESIGN`, **5 `NOT MET`**, `implementationAuthorized false`, `qualificationClaimed false`, `d9CarriedImplementationUnitObligation true`, `productGatesUnperformed true` |
| `docs/coop/design-corrections/readiness-row-map.v1.json` | 28 rows `DR-101..107,109..115,117..127,130,131,133`; excluded 108/116/128/129; `independentGrade ACCEPT-DESIGN` bound to activation; `condition5 NOT MET` |
| `docs/v2/architecture/08-decision-and-readiness-register.md` | Draft.v3 body copied first (must rebase `beforeSha256`). Assembler replaces exactly five `This is a new subject-specific design review.` sentences with the activation-binding sentence. Live register today remains NOT MET; do not treat draft SATISFIED-DESIGN as live. |
| `docs/coop/design-corrections/review-owner-dispositions.v1.json` | DR-201..205 preserved literal rows; `applicationDisposition ACCEPT-DESIGN`; not a grade |
| `docs/coop/design-corrections/correction-crosswalk.applied.v1.json` | 16 AR + 15 FW from the **actual** successor review dispositions |
| `docs/coop/design-corrections/inherited-residuals.applied.v1.json` | 11 parents + 16 residuals; **`carriedCrossUnitObligation` only on DR-007 and DR-011-R08** |
| `docs/coop/design-corrections/evaluation-residual-dispositions.applied.v1.json` | 30 items |
| `docs/coop/design-corrections/qualification-gates.applied.v1.json` | DR-G01..G32; `qualified`/`demonstrated`/`implementationHarnessAuthored` all **false** |
| `docs/coop/design-corrections/accepted-review-advisories.v1.json` | Successor advisories + historical **CLAUDE-V13-ADV-1/2** ids preserved (not renamed) |
| `docs/coop/design-corrections/validation-summary.applied.v1.json` | Measured `native.matrixCells` from accepted snapshot; historical v13 SHA `8e6670f7…` / 60 cells retained; **do not** put a Grok review path in `claudeFinalReview` |
| `docs/coop/COORDINATOR-DECISIONS.md` | Append adopted D-372 body naming actual independent reviewer label from the bound receipt |
| `docs/coop/design-corrections/README.md` | Prepend applied account; historical chronology follows |
| `docs/coop/design-corrections/application-activation.v1.json` | **Finalizer only, last.** Not present now. |
| `docs/coop/design-corrections/current-source-map.proposed.md` | Cited as source map; isolated map is still proposed |

D9: carried implementation-unit obligation, not a design-level blocker (actual Claude v20). 32 product gates unperformed, separate from design acceptance.

## Adaptation vs name-swap

Old assembly hardcodes `candidate-subject.v21.json`, Claude `response.json` / `is_error` / `session_id`, Claude CLI, `~/.claude/projects` JSONL, and README “actual Claude”. Successor adapters:

- take `--bound-receipt` + versions; subject path is the frozen evaluator3 manifest
- decode Grok `stopReason=end_turn` / `sessionId` or Claude `is_error`/`session_id` — cross-decode refuses
- refuse coauthor process standing and known coauthor session ids
- keep CLAUDE-V13-ADV-1/2, historical v13 SHA, D9 evidence bundle under `support/d9-obligation-evidence/actual-claude/` as historical
- measure current matrix cells; do not hardcode 66 as law (isolated/source21 matrix is 66 today)
- launch prompt still requires all 16 AR / 15 FW / 27 inherited / 30 eval / 28 condition-2 / 5 owners / 32 gates

Reuse without rewrite: freeze, prepare-validation, check-finalizer, finalizer, verify-applied (already gate on review.json verdict + empty findings + exact subject hash).

## Live vs isolated

- LIVE resume: `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/NEXT-REVIEW.md` (evaluator3 listing-join; freeze + Grok independent + NEW blind + application reconciliation).
- Isolated copy `evaluator-successor.v1/.../reviews/NEXT-REVIEW.md` is still the source21 freeze text (same bytes as frozen v21). Isolated `README.md` current section is the successor standing.
- Isolated source: `/tmp/opensip-design-corrections/evaluator-successor.v1`. LIVE accepted normative source not yet applied.
- Draft.v3 `documentation-proposal.json` `beforeSha256` must be **rebased** after freeze/doc motion or assemble refuses.

## Specific blockers (do not paper over)

1. No frozen evaluator3 candidate yet (W v11/v12 listing/trust join still active per LIVE NEXT-REVIEW).
2. No actual Grok independent review of a frozen evaluator3 subject; no NEW blind; no successor `design-assent.{dv}` / assembler-shaped `blind-assessment.{bv}`.
3. Required freeze sidecars for assemble: `candidate-source.{dv}.tar.gz`, `identity-check-counts.{dv}.json`, `final-reference.{dv}/reference-checks.json`.
4. Draft.v3 rebase after live doc hashes change.
5. `prepare-validation.py` currently asserts native pin intersections are only `03-configuration-and-security.md` and `10-mvp-and-future-scope.md`. Re-verify after freeze; if evaluator3 docs add pin intersections, that guard must be updated by a reviewed assembly change — not here.
6. Grok independent-review `--permission-mode`: coauthor used `acceptEdits`. Launch default is `dontAsk` via receipt override; confirm the actual Grok flag that confines writes to the application-review directory. Do not resume coauthor sessions.
7. Retain for Grok requires `applicationSessionTranscriptPath` on the bound receipt after launch; there is no Claude-log fallback.
8. Historical source21 Claude v21 ACCEPT and incomplete v9 blind are **not** inputs.
9. This preparation session is not independent review evidence.

`check-review-envelope.v1.py` is the only script intended to run now.
