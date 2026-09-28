# Review: existing-root admission 468 r3

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of law 468 after r2. No repository edits and no product cargo.

Subject `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md`, 8361 bytes, sha256 `f366fdd9ee6dd32738603b6e4214f98ebb33273bc50fa195d3c207a43d7578fb`. `PROPOSAL-r2.md` preserves the r2 bytes (`2e348f9ac590ddefc13289d14c37b54d486523240f8af43af78526c9268878c0`, 8138 bytes). The diff is the header, item 3 step 1, and two table cells.

## Verdict

**ACCEPT.**

r2 RF-1 and RF-2 are closed. Nothing new is wrong.

## Busy fence

Item 3 step 1 stops on a busy fence with the item 6 busy termination and does not treat `PROJECT.BUSY` as the error code. No recheck, barrier or later effect follows. The row is operational-failed, exit 4, error code `LEDGER.BUSY_TIMEOUT`, domain detail `PROJECT.BUSY`, fault cause `ledger-busy`. That is the S12 row, and the schema pairs `ledger-busy` with `LEDGER.BUSY_TIMEOUT`.

## Budget

The ledger row is operational-failed, exit 4, error code `SYSTEM.OUTCOME.ILLEGAL_STATE`, new domain detail `WORK.BUDGET_EXHAUSTED`, fault cause `host-invariant`. The schema pairs `host-invariant` only with `SYSTEM.OUTCOME.ILLEGAL_STATE`. The detail remains one of the three new codes.

The other rows are unchanged from the r2 review and still match S12 and `diagnostic-routes.json`. The gate recheck set from r2 is unchanged.
