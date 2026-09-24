# Review: executing core identity, proposal 463 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Text review only. No native job was run. No repository edits.

Architecture `403d97309` is clean. Product `cd48f87` is clean. Subject: `docs/implementation/m2/initial-core-launch-463/PROPOSAL.md`.

## Verdict

**REQUIRED-FINDINGS.** One finding. The kernel join, the refusal of Security.framework, the custody split, and the owner of K can stand once the bootstrap is located without the inventory.

## Answers

1. **The kernel CodeDirectory hash joined to the opened file and the inventory commitment is an honest loaded-image owner for the entrypoint.** `csops(CS_OPS_CDHASH)` and `csops(CS_OPS_STATUS)` are libSystem observations of the image the kernel validated. The in-core parser already refuses a CodeDirectory whose hash type is not SHA-256 (`cd[37] != 2`) and returns the first 20 bytes of `CC_SHA256` over that directory, which is the kernel cdhash for that hash type. `proc_pidpath` is a locator. No-follow opens, then the file's parsed cdhash must equal the kernel hash and the file's SHA-256 and length must equal that platform row's committed entrypoint. A substituted file fails one of those equalities. This uses neither argv, PATH, `current_exe` as identity, a caller descriptor, nor a record inside I. The dyld measurement stays the loader observation named in security-completion v8 §8.3; it is not the core's identity.

2. **Embedding the root binding avoids the digest cycle. The sentence that locates the records does not.** `RootBinding` is `rootSchema`, `rootVersion`, and `rootDigest`. The anchor commits to the inventory, the inventory commits to the tree, and the tree contains the image, so the image must not embed the anchor digest. That part is sound. The records are then "read from the core tree's embedded bootstrap directory, which the inventory names (`embeddedBootstrap`)". The inventory is one of those records. `core_anchor::capture` already starts from a supplied anchor `NodeRef`, and `CoreInventoryV2` only then names `embeddedBootstrap.directory`, with `payload.json` and `payload.sig.json` fixed under that directory. Using the inventory to find the directory, or listing the tree for a binding that matches the embedded digest, is the circularity and the enumeration the proposal forbids. See RF-1.

3. **The three open questions.**

   **Launch owner under §8.3.** The kernel hash and the in-core parser stay inside libSystem. Security.framework remains the qualification-only helper and is not a launch-closure member. A notarized release's extra flags (hardened runtime, kill-on-invalid) are whatever the admitted profile requires on top of `CS_VALID`. The implementation names those kernel flags; it does not call `SecCode*`.

   **Custody of the core tree.** This tree is the executing core, not an external ancestor of I. Owner §1b and premise 458 stay on the root-to-H chain and the reused `Library` and `Application Support` directories. They do not admit the core tree, and `installAclOmission` is not reused. The core path gets its own rule: no-follow, no group or other write, and no ACL write grant to any other principal, on every directory the open traverses. An omitted ACL on that path refuses until a separate signed qualification exists. The cdhash join still refuses a file swapped between `proc_pidpath` and the read.

   **Owner of K.** A signed core-inventory member, or a record that member commits, naming the writer schema. `stateSchema` on a store binding or a transition intent does not declare it. A decoder capability does not declare it. There is no default. `InitialCore` derives K only after that release-record successor is selected: K=2 when the admitted member names the stage-2 writer, K=1 only when it names the stage-1 writer, and any other or missing member refuses.

4. **What an implementation unit still needs, besides RF-1.** The Mach-O layout of the embedded blob, the exact profile flag set, and the `authenticate` change that takes the revocation set from the embedded chain instead of a caller argument, including a refusal of an empty caller set. Those are named. The bootstrap discovery fact is not.

## Required findings

### RF-1: The bootstrap directory is identified by the inventory that lives inside it

Failure: the image embeds a root binding and no path. The producer asks the inventory for `embeddedBootstrap.directory` in order to open the inventory, which does not exist yet. It lists the core tree and takes a file whose root binding equals the embedded digest. A second file with that binding, or a name that sorts last, becomes the anchor. The kernel CodeDirectory check still passes, because it never sees which record was chosen. The same hole admits "one platform entry" by scanning `platforms` for an entrypoint whose bytes match, rather than the single row for the authenticated profile's platform id.

The image carries the bootstrap directory's logical path beside the root binding. A path is not an anchor digest; the digest cycle stays closed. From the retained entrypoint tree, open only that relative directory's `payload.json` and `payload.sig.json`, then only paths the authenticated manifest's `rootChain` declares. Require `embeddedBootstrap.directory` to equal the path that was embedded. Select the platform row by the authenticated profile's platform id, and require the opened file's relative path, SHA-256, and length to be that row's entrypoint. No directory listing and no "latest" name.

## Observations

- The qualification row should include an inventory SHA-256 mismatch, alongside the substituted file and the flag check. A file can match the kernel cdhash and still be the wrong committed entrypoint.
- A symlink component on the kernel path refuses under no-follow. That is a refusal, not a reason to fall back to `current_exe` or to follow the link.
- Development builds with no embedded binding and no signed tree have no `InitialCore`. Test-signed fixtures stay under `#[cfg(test)]`.
