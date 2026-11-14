# Adoption receipt: C2A-ORDER-E1 r10 (the order of reservation, endpoint join and classification on the durable-analysis entry)

**Written by the lead coordinator (OD-LEAD-1, OD-DECIDE-1).** The record's own text says no amendment applies until its open points O1 to O5 are decided and adopted. This receipt records those decisions. The accepted bytes are NOT edited.

**Adopted:** the exact bytes `docs/implementation/m3/host-pipeline-j/c2a-order-e1-r1/README.md` (38740 bytes), sha256 `58ebe0ee4841ca77cb3f8e9d6e8729ebf35a13d855e2aebaf3f6a8b5d91c27f0`, the bytes both reviewers accepted at head `0286a5c62728a0af72d3ba3d41b42e9fb2638ad0`.

**The open points, each decided as the record proposes:**

- **O1 (E1c):** option (a) with A-1 to A-12 is adopted. The project owner agreed to it on 2026-11-12 (recorded in `docs/implementation/OD-DECIDE-1.md`); the cross-vendor reviewer found it supportable with A-1 to A-12 adopted.
- **O2 (A-7's reading, IE and WS unamended):** stands. The cross-vendor reviewer found the reading defensible and found no further necessary identity-contract amendment. No contract successor to IE or WS follows from this record.
- **O3 (E3, the fresh classification at R7):** adopted with the named successor clause MJ-R7S, which supersedes MJ:398's last sentence for R7 and keeps the creator's own rechecks. Both reviewers accepted it.
- **O4 (E2, the MJ:391-392 erratum):** adopted as an explicit prospective erratum. A registration that survives a later endpoint refusal stays valid, consumes registry capacity and is not rolled back.
- **O5 (the two storage choices):** adopted as MJ-R7S states it: the 464 choice at R7, the grants choice at the first source-derived write, with its input producers owed.
- **O6:** closed in the record: the later grants choice retains R7's classification and the same invocation's flag; MJ:959 is unchanged.

**Basis, bound by value:** Codex gpt-6.1-sol/high (`reviews/codex-c2a-order-e1-r1/review.json`): ACCEPT at `0286a5c62`. Claude claude-opus-5-5/medium (`reviews/claude-c2a-order-e1-r1/review.json`): ACCEPT at `0286a5c62`, including its check of MJ-R7S (iv) against the product code.

**Reported to the project owner** (who may overrule): O1 and O4 are the points the record marks "project owner told".

**Not done by this receipt:** no code is accepted; the controls E1-C1 to E3-C5 are owed by the units that implement the entry; the grants choice's input producers are owed; no design-lock entry is made.
