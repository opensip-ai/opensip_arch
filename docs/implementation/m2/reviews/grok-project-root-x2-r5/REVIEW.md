# Review: project root X2 r5

Verdict: ACCEPT.

Subject `docs/implementation/m2/project-root-x2/PROPOSAL.md` is 35787 bytes, sha256 `98d502659a07580066b3a83eea15b6e583ceafa8c484af431a2fb0ba4ffa834f`, matching hashes.txt. `PROPOSAL-r4.md` is the r4 subject: 35239 bytes, sha256 `8c188ad548e1a0896da37e031e501e433274366e340d9ef0e50c5ceb87706574`. Product HEAD is `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. The real OpenSIP support directory is absent. No product cargo. The on-disk X3b text is cited as evidence of the ordering X2 records. This review does not accept X3b.

## r4 findings

RF-1 is closed. Step 6 rechecks the current owners through each retained descriptor and its metadata: the root; the `.opensip`, marker, and namespace owners from steps 3 to 5; registry owner R1; the chain; and the tracking observation. R0 and any replaced capture stay provenance and are not rechecked. The replacement primitive then runs, and its own reconfirm is still R1 before ACTIVE. R0 is never reconfirmed after RESERVED. A reused `.opensip` is the owner step 4 admitted; that step puts the retained handle on the recheck set, and step 6 checks that current owner rather than the absence it replaced when the directory was created. The root sample in item 4 is device, inode, birth, and volume UUID, and the chain recheck remains 468 item 3's identity, name, and custody. Neither compares a parent directory's changed time, so creating `.opensip` does not make the root recheck fail.

RF-2 is closed. Item 7 opens with the ordering note: before this item takes any lease, with the fence held and no project lock, X3b's floor step runs once R is current. R is R0 for an Eligible root and R2 after this admission's registration. S7 writes trust state only under the fence and never under a lease. Item 7a step 3 is only the carrier start, after the transfer and before the fence release. The floor step is not part of 7a. That is the order X3b's current item 1 states, and X2 now records it. The floor step's contents, including its lease probe, stay X3b's law.

## Unchanged and still closed

r3 RF-2 and RF-3 are untouched and stay closed. The fixed Git source list and the index version 2, 3, and 4 decoding are the same text r4 accepted. Item 9's "original-owner rechecks" is the budget name for those pinned owners. It does not restore a recheck of R0. The refusal rows are unchanged.
