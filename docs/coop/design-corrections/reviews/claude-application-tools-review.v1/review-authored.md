# Application-tooling review — origin 36063855-9467-40d0-a2fd-7afba09a957f

**Verdict: CHANGES_REQUIRED** (tooling review only — not an application ACCEPT, not design acceptance, not implementation readiness)

Fresh origin, no prior context, no author origin resumed. I authored none of the reviewed bytes and conducted none of the design, blind, or application reviews they orchestrate.

## Custody

- `input-manifest.json` SHA256 = `e25995b7b649f2376e28caae4d5b06cbf8cdbae8e9ddaa6e7b26b7bbf5ecf32a` — **matches**.
- All **19** input files verified byte-exact against the manifest (SHA256 *and* byte length). No extra files in `inputs/`, none missing.
- All 19 read completely.
- Nothing outside `scratch/`, `review.md` and `review.json` was written. Inputs and live repo untouched.
- `check-retain-public.v2.report.json` was read completely and treated as **historical evidence only**, never as an oracle.

## What holds up

The receipt-binding stage is genuinely strong. Against a synthetic root, `bind-review-receipts.v1.py` refused **all 24** boundary cases I put to it, including each of the four excluded Claude author origins in *both* the design and blind roles, all three Grok coauthor sessions, blind reusing the design session, a blind input kit naming another parent, an assent naming another subject or another reviewer session, a missing root design assent, a process session disagreeing with the public envelope, `SHAPE ONLY` receipts, and receipts pre-claiming `readyForAssembly`.

The finalizer is the other strong point. Re-executing the shipped `check-finalizer.py` against the frozen `finalize-application.v1.py` bytes gives 20 passed / 0 failed with `sourceSha256` matching the manifest digest. I added seven cases it does not cover — a live file appearing where `beforeSha256` was null, a live file deleted, a symlinked live target, tampered retained-manifest custody, a missing staged after-image, a manifest claiming `implementationAuthorized` — and all seven refused with **zero writes** and no activation. Activation is written strictly last, `--check` leaves none behind, and an existing activation is never replaced.

Source-pin adaptation is correctly bounded: 8/8: one opening applicability paragraph naming D-372 is admitted with the inherited body byte-preserved, while body edits, a second smuggled paragraph, title changes, appended tails, and an unexpected extra changed pinned path are all refused. Staged grades are properly conditioned — `application_rows.py` refuses any draft asserting `productQualified` or a non-`PENDING` grade, every emitted record carries `effectiveWhen` and `independentApplicationGradeBinding=activation`, all 32 gates keep their three authority flags false, and condition 5 is written and re-asserted as NOT MET. Historical evidence is preserved rather than repinned: the inherited D9 artifact enum is asserted *unchanged*, live guide variants are not overwritten, and the old D369 checker runs unmodified with exact provenance required for every new failure.

## What needs to change

**F1 (MAJOR) — the final application review does not exclude the four Claude author origins.** `retain-application-review.successor.v1.py:87` checks `KNOWN_GROK_COAUTHOR_SESSIONS`, not the `KNOWN_COAUTHOR_SESSIONS` union. Bind and assemble both use the union, so design and blind are protected while the application review is not — and `finalize-application.v1.py` performs no reviewer-origin check at all, which makes line 87 the *only* origin-independence guard on the review that authorizes activation. My probe retained a review for each of the four excluded origins. One-token fix.

**F2 (MAJOR) — coauthor-standing and `--resume` refusal are skipped for vendor `claude`.** Lines 60-61 sit inside `if vendor == 'grok'`. The claude branch does no process check, so a `process.json` declaring coauthor standing, or resuming a known author origin, is retained. The helper already handles `independent-application` correctly; it simply is not called. Hoist one line above the vendor branch.

**F4 (MAJOR) — `verify-applied.py` reimplements the parent-subject digest selector.** Its inline copy (lines 6-11) diverged from `review_envelope.review_subject_digest` in 4 of 8 probed shapes. The consequential one: a design review declaring only `inputKit.parentSubjectSha256` — the layout the shared adapter deliberately admits and the envelope suite explicitly tests — binds and assembles fine, then fails post-activation verification, i.e. *after* the irreversible step. The other three are weakenings (it admits uppercase, wrong-length and non-object forms the adapter fail-closes). Import the shared adapter.

**F5 (MAJOR) — the assembler never re-verifies the Codex root design assent digest.** `bound['codexDesignAssent']['sha256']` appears nowhere in `assemble-records.successor.v1.py`; line 472 loads the file from the live root by path and lines 478/568 propagate its contents into the advisory record and `acceptedContracts`, while line 563 records whatever digest is found *now*. The other four bound artefacts are all compared. Bind does verify the assent, so the receipt carries a correct digest the assembler then ignores — leaving a bind-to-assemble window. Two lines, matching the existing pattern.

Minor items: the finalizer and catalog generator are staged from an unpinned mutable `/tmp` path with no digest assertion (**F6** — orchestration-scoped rather than incorrectly bound authority, since the staged bytes are self-tested, digest-bound at freeze and explicitly put to the reviewer; the path exists here, so this is provenance and portability, not an absent-path failure); launch metadata records a Grok-only exclusion list for both vendors (**F7**); the retain and envelope evidence reports are copied forward with no `sourceSha256` and no re-execution, unlike the finalizer selftest, so they cannot detect drift in the modules they tested (**F8**); the envelope suite writes its report into its own pinned source directory (**F9**, which is why I ran it from a copy). Informational: private-directory classification only inspects the first path component (**F10**), and the DR-011-R10 disposition text is generated boilerplate carrying the *design* reviewer's label on a row about the *blind* consumer — the evidence pointer is correctly the blind review's own verdict, so no author result is substituted, but the attribution is imprecise (**F11**).

F3 (MINOR) is latent: the Claude CLI envelope is copied verbatim because both the sanitizer and the private-source filter are gated on `vendor == 'grok'`, and `public_view`'s claude branch is dead code. A synthetic invented `thinking` key survived into the retained copy. I could not verify whether a real Claude envelope ever carries private content. The Claude *session-log* selector is correct — a synthetic thinking block was properly excluded from `tool-calls.json`.

Notably, the historical retain report's check list contains no case for Claude-vendor session exclusion, Claude-vendor process refusal, or Claude envelope sanitization. F1, F2 and F3 are untested territory, not regressions.

## Scope I did not perform

Six inputs were not executed end-to-end — `assemble-records.successor.v1.py`, `prepare-validation.py`, `freeze-application.py`, `verify-applied.py`, `run-application-reference-suites.py`, `run-applied-reference-checks.py` — because they need the full application-successor root that is not among the inputs. F5-F8 are static/AST-level and labelled as such; no end-to-end reproducer is claimed for F5. The Grok vendor path was exercised only at library level: no Grok CLI, no session directory read. No `.claude` transcript or private reasoning was read anywhere; every sanitizer sentinel was invented. In-process probes ran on host python3 3.14.6, subprocess suites on the reference interpreter 3.12.13.

No application, binding, freeze, launch, retention or activation was performed. **All 32 product gates remain unperformed and condition 5 remains NOT MET**; design acceptance is a separate question this review does not reach. Details, per-finding reproducers and remedies are in `review.json`; probe sources and results are under `scratch/`.
