# Review: native current-trust admission X4T r3

Verdict: ACCEPT.

Subject `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` is 24820 bytes, sha256 `8831dedb2fa59e486ac701b4ac27831d6a4928c4c288c935f0542ab22db84958`, matching hashes.txt. Preserved r2 is 24424 bytes, sha256 `d4c30645b79b2a58577b63f07effbbd93f3996a12fe1abb62f8f5c793ce3437a`. Preserved r1 is 17029 bytes, sha256 `131c59273fd48670c7174f4e33c8e43d8dc6d949fab92f3453c249dcf60baf91`. The live product HEAD is `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. The real OpenSIP support directory is absent. No product cargo.

The diff against r2 is the header, item 10's budget bullet, and item 11's chain sentence. r1 RF-1 through RF-6 stay closed.

## r2 RF-1

A recorded root chain past `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }` refuses on the existing budget row: `WORK.BUDGET_EXHAUSTED`, operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault cause `host-invariant`. That is the row in `diagnostic-routes.json` for an attempt or admission ledger that refused a charge, and the `WORK.BUDGET_EXHAUSTED` registry selector. `ChainError::Limit` has no public detail. The chain is never truncated.

Item 10 names this case on the budget bullet and keeps a link-named chain evaluation on its S5 `ROOT.*` detail. Item 12 requires a 17-link chain to refuse, and item 11 assigns that refusal the budget row. A view over `TRUST_VIEW_COST` stays on that same row.

The two continuation codes, their interim publication under `CONTINUE-CORE-NOT-TRUSTED`, and `TRUST_VIEW_COST` (64 objects, 1024 edges, 120 MiB) are unchanged.
