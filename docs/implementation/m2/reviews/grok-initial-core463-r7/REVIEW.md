# Review: initial core launch 463 r7

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of item 8. No repository edits. No product cargo.

The proposal is 15521 bytes, sha256 `62f36cc2a5419cb6c906848d27dfeeadf8655af2060edaa08934603b0ee7b029`, matching `hashes.txt`. `PROPOSAL-r6.md` is the accepted r6 text: 14264 bytes, sha256 `1db9ca07b3f433b4a876e3e1ba1cc8d6b3419bf588d8ca761eae1794d877b730`. The diff is the header plus item 8.

## Verdict

**ACCEPT.**

## Answer

Item 8 is sound. Items 4 and 5 re-filter quorums, so the revoked key set stays the `keyId` entries. The revocation shape admits exactly four subject kinds, and an unknown kind already fails that shape.

A `release` entry matches this core when its subject equals the inventory's `closure2:` value, the string `core_anchor::capture` binds to `coreClosure`. That string is `closure2:` plus 64 lowercase hex of the canonical closure descriptor (`schemaVersion` 2, kind `core`, the inventory-body digest, the tree, and the platform row). Law 229 defines that id as the core. It is the identity the producer already has, and the list that carries the entry is the release's own embedded revocation, verified under the final root in item 5 step 2. Admitting the release after that list names this id would admit a release that declares itself revoked.

No epoch or counter comparison belongs here. `observe_revocation` matches entries only when the current `revocationVersion` is greater than the operation's start epoch, and it says the verified document is not a current view until admitted time, counters, and root custody exist. Those inputs are an installation's later view of a newer list. Before I exists there is no start epoch. The embedded list is not a later view of this release; it is the release's own statement. A counter comparison would require the store this creator does not have.

`namespace` and `catalogSnapshot` stay with that later predicate. The initial creator executes no namespace member, provider, recipe, or catalog snapshot, so those subjects name nothing this act does. `observe_revocation` already compares them to `closure.namespaces` and `catalogSnapshotVersion` for an ordinary operation after I exists. The revocation observation corpus spells a release subject as a release coordinate (`example/tool@1.0.0`) and compares it to `closure.releases`, which is that operation's set, not the core's `closure2:` id. Item 8 does not move that match. It uses the one identity this core has. The schema leaves `subject` a string of 1 to 256 characters, so both spellings fit; the core's own entry is the closure id.

The item adds no record member and changes no quorum rule. Owner step 3's authentication remains the embedded chain and its revocation, not ordinary namespace or catalog execution.

Do not commit.
