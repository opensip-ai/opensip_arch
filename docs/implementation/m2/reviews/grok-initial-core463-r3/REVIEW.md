# Review: executing core identity, proposal 463 r3

Grok is the single reviewer. Claude Opus 5.5 leads. Text re-review only. No native job was run. No repository edits.

Subject: `docs/implementation/m2/initial-core-launch-463/PROPOSAL.md`. r1 and r2 are preserved beside it.

## Verdict

**ACCEPT.** RF-1 and RF-2 are closed. Nothing new is wrong.

## RF-1

The image embeds the entrypoint's logical path and the bootstrap directory's logical path, both from the same tree root, beside the root binding. The tree handle is the directory that many already-opened parents above the executable, where the count is the number of components in the embedded entrypoint path, leaf included. For `bin/opensip` that is the second parent of the file: the directory that contains `bin`. The producer does not walk further and does not search. It opens only the bootstrap path, then `payload.json` and `payload.sig.json`, then the manifest's declared root-chain paths. `embeddedBootstrap.directory` must equal the embedded bootstrap path, and the chosen row's entrypoint path must equal the embedded entrypoint path.

## RF-2

The inventory row is the one whose platform id equals the authenticated anchor's `platform` field, the id `core_anchor::capture` already passes to `project`. `InitialCore` does not wait on `InitialPlatform`. Step 4 later observes under that same id and refuses a different running platform. It does not supply or change the id.

## The rest, still holding

The kernel cdhash joined to the opened file is the loaded-image identity. `proc_pidpath` is only the locator. Security.framework stays off the launch path. Core-tree custody is not owner §1b and not premise 458: an omitted ACL refuses, an inherit-only write allow counts as a write, and a symlink has no fallback. K comes from a signed inventory member through a release-record successor, with no default, and a missing member refuses. Each missing embedded value refuses. The qualification row includes a cdhash match whose SHA-256 is not the committed entrypoint.

This is an owner amendment for step 3. It is not code and not creator authority. The implementation unit still owes the image layout, the profile's flag set, the `authenticate` change that takes revocation from the embedded chain, the K successor, and the signed fixtures.
