# Review: executing core identity, proposal 463 r2

Grok is the single reviewer. Claude Opus 5.5 leads. Text re-review only. No native job was run. No repository edits.

Subject: `docs/implementation/m2/initial-core-launch-463/PROPOSAL.md`. r1 is preserved as `PROPOSAL-r1.md`.

## Verdict

**REQUIRED-FINDINGS.** The inventory no longer names the directory that is searched for it. Two facts are still missing before an implementation can open that directory and choose its platform row.

## What r2 closes

The image embeds the bootstrap logical path beside the root binding. Opens are only that directory's `payload.json` and `payload.sig.json`, then only paths the authenticated manifest's root chain declares. There is no directory listing and no "latest" name. `embeddedBootstrap.directory` must equal the embedded path. The entrypoint's relative path, SHA-256, and length must equal the chosen row. Core-tree custody is separate from owner §1b and premise 458: omission refuses, and a symlink on the kernel path has no fallback. K comes from a signed inventory member through a release-record successor, with no default. The qualification row includes a cdhash match whose SHA-256 is not the committed entrypoint. Security.framework stays off the launch path.

## Required findings

### RF-1: The tree root is still unnamed, so the embedded bootstrap path has nothing to be relative to

The path is "relative to the tree root that contains the entrypoint", and the producer opens it from "the retained tree handle". The image does not embed the entrypoint's own logical path. Before the inventory exists, the only handles are the no-follow components of `proc_pidpath` and the executable descriptor. Nothing in those values says how many components above the file the tree root is.

Failure: the release entrypoint is `bin/opensip` and the bootstrap path is `bootstrap`. The producer treats the executable's parent as the tree root and misses the real `payload.json`. A producer that walks ancestors until a `payload.json` verifies, because the text says the root is the one that "contains the entrypoint", accepts the first signed tree it finds. The kernel CodeDirectory join still passes.

Embed the entrypoint's logical path from the same root. The tree handle is exactly that many already-opened parents above the file. Do not walk further and do not search. The inventory's entrypoint path must equal that embedded path, and `embeddedBootstrap.directory` must equal the embedded bootstrap path.

### RF-2: The platform row is chosen by `InitialPlatform`, which needs this core first

Owner step 3 produces `InitialCore`. Step 4 produces `InitialPlatform` through the core's embedded authentication context. r2 selects the inventory row by "the authenticated profile's platform id for this boot (`InitialPlatform`)".

Failure: step 3 waits for the step 4 receipt, and step 4 waits for the step 3 receipt. Or step 3 runs first by scanning `platforms` for a row whose entrypoint bytes match, which r2 forbids, and a different platform id than the anchor's is admitted.

`core_anchor::capture` already projects the inventory with the anchor's own `platform` field. The row is that single id. `InitialPlatform` later observes under the same id. It does not supply the id.

## Observations

- An ACL allow that is inherit-only is still a write grant on this path, as it is for an external ancestor of I.
- A missing embedded bootstrap path refuses, the same as a missing root binding or an unsigned tree. The development-build sentence should say each of those absences refuses.
