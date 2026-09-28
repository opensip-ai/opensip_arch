# Review: existing-root admission 468 r5

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review after r4. No repository edits and no product cargo.

Subject `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md`, 11373 bytes, sha256 `0959e3083f95841783d39d3d299960000b556d95ebbea18b8f237cefc8d5ccf7`. `PROPOSAL-r4.md` preserves the r4 bytes (`bbd48bad7c04e509b4e9d54b19e586f546f129d11fbd18615a36eb5660404e0a`, 10395 bytes). The diff is item 4.

## Verdict

**ACCEPT.**

r4 RF-1 is closed.

The observation path reaches the fence only through item 3 steps 0 and 1: the charged retained walk, then the no-follow attempt on the retained I handle. It does not call `NativeInstallationFence::try_acquire`. It has its own ledger, takes no barrier, charges its member reads before they run, and rechecks under the held fence.

A read command has no `InitialPlatform`, so that walk's premise can only be the 458c receipt. Until 458c is accepted, 468 builds no observation path. 468c ships the write path and the public routing. The doctor note and the 256-slot rule stay stated in item 5 and are implemented with 458c/461. Item 4 records the open scope for 458c: item 9 says root to H, while step 0 also reaches `Library` and `Application Support`, so 458c covers those two with 465 item 4's scope or they refuse on an omitted ACL.
