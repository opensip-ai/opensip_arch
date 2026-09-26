# Review: initial core launch 463 r4

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of the r4 amendment to accepted 463 r3. No repository edits. No product cargo.

The proposal is 12846 bytes, sha256 `1c66458d24d36cffd43d6d7263fe3dd2690dd01f78b7046ae8cb6f0bac38d3f7`, matching `hashes.txt`. `PROPOSAL-r3.md` is 8802 bytes, sha256 `999e238dbc84ca0fd8ee11299a5ca56ca3daa602a565973fb4a87e94b839b222`. The diff is the header note plus the section "r4 amendment".

## Verdict

**REQUIRED-FINDINGS.**

## Answers

Items 1, 3, 4, 6, and 7 are sound completions of r3.

The inventory names are law 229's reserved top-level pair. `core_inventory` refuses `inventory.json` and `inventory.sig.json` inside the tree (`inventory-self-reference`). Opening those two names, no-follow, under the tree-root handle, under the same custody rule, with no listing and no "latest", is the missing locator. r3 already opens the bootstrap directory, `payload.json`, `payload.sig.json`, and the root-chain paths the manifest declares.

The compiled-target platform id is acceptable. `CoreAnchorNodeV1.platform` is a `PlatformId`, and `core_anchor::capture` selects the inventory row with `project(&body, platform)`. Before installation the producer is the one writing that field, so reading it back from the anchor it just built is circular. `macos-aarch64` and `macos-x86_64` are the two macOS machine ids. A target with no platform id has no `InitialCore`, which keeps Linux unavailable. `InitialPlatform` still observes the machine and refuses a different platform, so a cross-compiled or translated image does not keep a mismatched id.

Verifying TR-CORE and TR-BUNDLE does not conflict with law 229. `metadata_pair` checks the carrier subject (kind, domain, route, stored digest, preimage) and does not check a quorum. `authenticate` checks the root-chain quorums only. Law 229's "TR-CORE's signature is never an input" is about anchor recomputation: the node proves which bytes are index 0, and the signature is not one of those bytes. r4 checks the quorum in a separate pre-installation authentication step, after the chain and the revocation pass, and still does not feed the signature into the recomputation. Inventory kind is TR-CORE; the bootstrap manifest is a payload envelope, and payload envelopes use TR-BUNDLE. Without that check, `stateWriter` and `requiredCodeSigningFlags` would be carried by an unsigned inventory. This is also the open-then-verify §3.3 requires for an executed member: the inventory those bytes are checked against has to be the signed release manifest.

Putting K and the flags on the inventory is the right home, and the owner amendment is acceptable. Law 229 makes the inventory the signed core release manifest. `stateWriter` 1 or 2 is the release's writer capability, which is where owner step 3 already derives K, and a missing or other value still refuses with no default. `requiredCodeSigningFlags` is a property of that core image, per platform row, not of the machine population. The profile set stays the population document. D-367 is the delegated design authority under which these owner amendments are reviewed; accepted r3 already amends §1a step 3. The superseded sentence forbids a new installation-record member and forbids `selection.pair` or a future C from choosing K. r4 keeps both restraints: the member is `stateWriter` on the release inventory, and the caller does not choose it. The r3 sentences that say the flags come from "the admitted release profile" are governed by this amendment: the flags are the inventory member, not a profile-set field.

The custody predicate matches r3's bullet and is the right split from `check_external_ancestor`. The core tree is not an external ancestor of I, so premise 458 does not apply. Any owner or root, no group or other write, no ACL write to anyone else, inherit-only allows counted, omission and the NOACL sentinel refused until a signed core-path qualification exists. That is §3.3's open-then-verify custody on the descriptors the launch actually opens.

## Required findings

**RF-1.** The revocation document's own quorum is not re-filtered. Step 1 authenticates the chain with an empty set. Step 2 verifies the embedded revocation under the final root with that same empty `previously_revoked_keys` (`verify_revocation` filters only by the set it is given). Step 3 re-filters chain links, TR-CORE, and TR-BUNDLE, and does not re-filter the revocation quorum with the set the document just established. A key named in that set can be the signature that makes the set effective, and it still counts after step 3. The same second pass `filtered_again` already provides for the other quorums has to include this one before any fact is admitted.

**RF-2.** The in-memory store is short of what `capture` loads. The anchor node has three `DocRef`s: `coreInventory`, `bootstrapManifest`, and `root`. r4's list is those three, and the 322 review calls them the three initial raw pairs. `capture` also loads the anchor record itself from the records collection, and `EmbeddedCapture` loads every later root-chain member by the tree digest. A store that holds only the three pairs cannot serve that walk. The chain files r3 already opens have to be charged into the same attempt-owned store, with the constructed anchor record, and nothing else.

Do not commit.
