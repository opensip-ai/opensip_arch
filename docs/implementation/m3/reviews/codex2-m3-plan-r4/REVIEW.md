# CODEX2 review — M3 unit plan r4

**Verdict: ACCEPT.** C2-M3-R3-01 is resolved. The complete diff contains only the requested correction and the r4 response table.

Subject: `docs/implementation/m3/M3-PLAN.md`, 43,947 bytes, SHA-256 `e50f75d3cb7fbbb4d44484585adf2b9899ef6e291a3c4d90fb619fcc9f3663c8`. Preserved r3 SHA-256: `7ef4f0d1147ce8311c49e375c83caf9b5d80895cd77b5e152b9c21799a019c2b`.

## Finding resolution

**C2-M3-R3-01 — resolved.** [M3-PLAN.md:222](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:222) defines `O2_selected` as the latest finish of the O2 parts retained in M3, or zero when none is retained. [M3-PLAN.md:225](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:225) includes it in both X's dependencies and `max(M3-M, R, 23, O2_selected) + 2`. [M3-PLAN.md:231](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:231) adds the requirement that selected O2 work finish by day 24 for the conditional 26-day result. [M3-PLAN.md:237](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:237) qualifies the late-branch discussion.

The prior counterexample is repaired: with K2 finishing at 21 and selected O2 work at 30, M finishes at 24, R at 23, and X at 32. No required finding remains.

## Change scope

The complete r3-to-r4 diff adds the response table and changes only the O2 definition/join, exit maximum, day-24 condition and late-branch qualification. No other bytes changed. This acceptance covers the requested narrow round and approves no successor law or owner decision.

## Nonblocking observation

**C2-M3-R4-N01.** At [M3-PLAN.md:237](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:237), compare the branches' arrivals at X explicitly: `max(21,K2)+3` versus `O2_selected`. For example, K2=25 and O2=26 still leave the K2 branch determining exit because M finishes at 28. The table is correct; 'whichever branch reaches the exit gate later' would make the prose equally precise.

## Verification

Both subject hashes and the r4 byte count matched the request. Only static reads, diff inspection and review artifact writes were performed, with an independent read-only check. No product build, run, test or project script executed. The real runtime home and 413 fixture were not accessed. No commit was made. Outputs are confined to the requested `/tmp/opensip-implementation/reviews/codex2-m3-plan-r4/` directory.
