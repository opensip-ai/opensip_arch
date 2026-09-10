I’ll start from this v5 copy’s kit, requirements, team-inputs, and current four-Run artifacts, then assess both peer reports against original kit law before any producer runs.I’ll authenticate the two peer reports, freeze the byte-identical scopes, and read the findings against original kit law.I’ll read the original Run requirements and the kit owners for the peer findings so corrections follow published law, not the reviewers’ expected digests.I’ll freeze the other scopes, redirect write paths into this v5 output, and preserve the four peer-refused Run graphs before correcting them.Builders succeeded with the expected cell outcomes. Next I’ll run from-scratch admission, replay, and whole-graph tamper on all four stores.**Verdict: `OTHER_RUNS_READY_FOR_INDEPENDENT_RECHECK`**

This is not whole-consumer acceptance and not root admission. Both peer reports (`OTHER_RUNS_REFUSED`) were checked against original kit law. Their expected proof digests on unadmitted graphs were not copied.

Syntax-code, all `foundation/` artifacts, and workflow/scope outputs stayed byte-identical (0 mismatches). The four peer-refused stores were preserved under `preserved-failures/v4-peer-refused-four-runs/` before replacement.

Existing-law corrections actually executed:

- **TS** RuntimePayloadV1 now uses `istanbul-json` and an object `observationWindow` (`import2:98fee8f9…`).
- **Rust** `crateRootPaths` is inventoried `#/a/Cargo.toml`; `proc-macro-srv` length is 14; clones mint under **one** selection (`bin.tool@2021`). Same file at 2018 vs 2021 is two selections, not one ambiguous `selectedUnitIds`. Lib vs lib+test at 2018 keeps L0 stable.
- **syntax-data** matrix cell `clones-fact × syntax-only` is `SUPPORTED-DESIGN` → account `supported-available`; Coverage stays unknown + `language-tier-unsupported`/`capability-missing`; required cell **partial**; seal **indeterminate**.
- **rust-partial** required partial cell now carries `executionDeficiencies` and sealed **indeterminate** (composition §5).
- **evaluationInputRefs** = selectedRefs + execution-inputs only.
- **Tamper** remints proof, evidence, seal, and run; admits the replacement; then semantically refuses. Stale-hash is separate.

From-scratch admission/replay on all four: `closureOk=true`, claimed proof C equals independently reconstructed expected proof C, `firstRefusal=null`.

| Run | Store SHA-256 | Verdict |
|---|---|---|
| ts | `ca1b44df3f89bc6d6cc63edfe239ce510a60c7fc47f2d531c5bcb10385b99086` | pass |
| rust | `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791` | pass |
| syntax-data | `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099` | indeterminate |
| rust-partial | `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c` | indeterminate |

Shared helper `evaluationInputRefs` change would move syntax-code proof C if that store were rebuilt; it was not overwritten.

Remaining: ROOT-ADMISSION, v11 inhabitance, real host/compiler/crypto, L1 tokenisation, unrequested default-profile cells. All 123 original accept-blocking obligations remain.

Reviews: `other-runs-completion-review.json` SHA `8356dacd7b3d0a72e67a0cf6f8d25e0053d77db64c607578e10e20a16539afb9`; `.md` SHA `d76fd558d15deaf2f5f556f25cb2c5cba2a0a9de2587569e12ea907b761ee73d`.
