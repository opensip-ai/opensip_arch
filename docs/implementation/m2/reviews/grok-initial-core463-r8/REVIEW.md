# Review: initial core launch 463 r8

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of items 9 to 12. No repository edits. No product cargo.

The proposal is 17910 bytes, sha256 `a5bc3b60337b25aa36d2eb8a77b938f32efa934ec67a3f04719915bca4d6dbcf`, matching `hashes.txt`. `PROPOSAL-r7.md` is the accepted r7 text: 15563 bytes, sha256 `1955c94fdcc5511581b61ca1bd77cd0c4f47599bec8979167be7baa44f866385`. The diff is the header plus items 9 to 12.

## Verdict

**ACCEPT.**

## Answers

Item 9 is the closed store applied to the index. `Data::build` loads every path in `members.envelopes` before `select`. Item 2 stores the chain bodies' envelopes and the revocation envelope, and nothing else. A listed envelope outside that set cannot be loaded, so the producer requires the list to be exactly one envelope per root-chain body plus the revocation body, paired one-to-one by the carrier's stored digest. Any other listed envelope refuses the release. The catalog body remains a payload member and is not loaded. This does not widen the store.

Item 10 is an acceptable stated limit, and r3 does not require the stronger reading. r3's tree-root handle is as many already-opened parents above the executable as the entrypoint has components, and the producer never walks further. The opens, and therefore "every directory the opens traverse," start at that handle: the tree root, the directories down to the entrypoint and the bootstrap directory, the executable, and every opened file. Those are what item 7 judges. The directories above the handle are the kernel path's locator. 463a already keeps that path retained, rechecked by exact name, and free of symlinks, and r3 still refuses a symlink component on the kernel path. `/` carries no ACL, so running the core-tree predicate on those ancestors would refuse every installation. r3's separate signed qualification for an omitted ACL is the same kind of later qualification item 10 names for the install location above the tree root. The limit does not admit those ancestors.

Item 11 does not weaken production. The attempt ledger's byte cap is 268435456. The current security test binary `opensip_security-14ad03b34222b156` is 620155232 bytes, so it cannot be the image whose bytes the producer reads. The platform test copies a small binary, executes that copy, and checks the kernel CodeDirectory hash, the file bytes, and the tree ACL, which is the live join. The producer end-to-end test uses a signed on-disk tree and a test-only injected observation so custody, release, entrypoint, flags, and K still run. Production has only the live observation, so the injection is not a production input.

Item 12 is right to keep item 8. The revocation file is a tree row, and the `closure2:` id commits to that row's digest. A list whose subject is that id would have to contain a digest of bytes that include the id. That is a hash fixed point, so the check does not fire on a normally constructed release. It remains the defensive comparison, tested on synthetic entries that are not that fixed point.

Do not commit.
