# Law X4T r7

Grok. Law review only. No product cargo. The OpenSIP support directory is absent.

`trust-admission-x4t/PROPOSAL.md` is 35671 bytes, sha256 `7a8283063b4c47fa801cb3954e7ed7dc8e79d6e1fd6f2193bc31e12a7e34a7b1`. `PROPOSAL-r6.md` is the reviewed r6: 35401 bytes, sha256 `a135d5c07753fe7fadd8a0d408d8a7c9fa5b15a8c922fced3978c056b271d968`.

The diff is the title, the r7 provenance sentence, and item 12's budget case. That case now states item 11's r6 pin: the linear charge (one object and its stored bytes per distinct record read), a measured native read within `TRUST_VIEW_COST`, and the closure-check boundary (40 MiB plus a full chain admits; just over 40 MiB with a small chain refuses). It still requires a 33-event descriptor to refuse, a 17-link chain to refuse, a closure over 40 MiB to refuse, and the ceiling refusal.

No remaining sentence requires a measured cost of a closure at its 40 MiB total with 32 events and a 16-link chain. The words "full-size measurement" remain only as the measurement item 11 r6 replaced. Items 1 through 11 are otherwise the r6 text. No new public code.

r6 RF-1 is closed.

## Verdict

ACCEPT.
