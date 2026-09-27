# Review: initial publication 467 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/initial-publication-467/PROPOSAL.md`. No repository edits. No product cargo.

The proposal is 7327 bytes, sha256 `6d7ef464841852ed693dd718a596e6fb838d39a3b593cb3cb09f7e2f4b7963cb`, matching `hashes.txt`. It covers 466b and 467. No CLI command is wired. The creator stays disabled.

## Verdict

**ACCEPT.**

## Answers

The P0 tree matches owner §2 and the existing `initial_publication::build` locators. The stage holds 14 directories and 11 files. The directories are the ones those files require: `stores/S`, `transitions/lineage/S/0`, `trust/records`, `trust/stores/S/events`, and `trust/publications/initial/S`. The files are the empty `lifecycle.fence`, the empty `project-registry.v2`, `stores/S/store-instance.v1`, `transitions/lineage/S/0/K.node`, `selection.pair`, and the six trust files the builder already emits: three records under `trust/records/<digest>`, the creation event under `trust/stores/S/events/1-<digest>`, the publication descriptor under `trust/publications/initial/S/<digest>`, and `trust/stores/S/state.v1`. S is a fresh 128-bit draw, G is 0, and K is `InitialCore`'s state writer. Each directory is 0700 and each file is 0600, with the zero-rights owner allow. Each new non-trust file must decode with its existing decoder. No schema successor is added.

The effect order is the owner's order. The permit is rechecked and consumed, and storage is rechecked, before the stage exists. S and the clock are taken with no effect. The stage is the existing private-stage primitive: at most eight nonce candidates, no adoption. P0 is built and verified in memory. The 14 directories are created parents first. The fence is created and locked first among the files, and `selection.pair` is last, so dependencies precede the descriptor and the descriptor precedes the current pointer. Validation, the pre-rename barriers, the exclusive rename, the I-parent barrier, the rechecks, the lock release, and the handoff follow. A refusal latches and stops later effects.

Item 2 is sound. `consume` in 465 retires `recheck_intent_storage`. The handoff still carries the admitted storage, the target, and the flag. Rebuilding the target from the actor and re-classifying it before the stage and again before the rename is the same rule as 465 item 8, applied after the intent is gone.

Item 3 keeps the clock as evidence. One `{bootId, mono, wall}` sample is projected by the existing clock projection into `CreationInputV1.observation`. The clock phase stays unevaluated. The sample grants no time admission.

Item 4 is the right reading of §3 and §4. A directory gets its own barrier and its parent's barrier before it receives children. A file gets `F_FULLFSYNC` with no fallback, then its containing directory's barrier. The stage root and its parent are barriered again before the rename. After success, only the I-parent barrier is taken, on the publication parent's handle: §4 says a receipt made on the caller's parent does not `is_for` that duplicate. I's own barrier stays with the §5 durable write gate. Every receipt is checked against the handle it names. Barriers are not batched.

Item 5 is the pre-publication validation §2 and §3 require. Each directory's entries are exactly the manifest's children, the directory passes the private judgment, and its device and inode are the ones retained at creation. Each file is reopened no-follow and must be regular, one link, 0600, owned by the invoking user, privately ACL'd, the same device and inode, and byte-identical under an exact-length cap, then accepted by its decoder. The trust records are verified again from those bytes. The joins are the owner's: marker bytes, stage nonce, `deliveringCore` equal to the pair's closure and the core's, store and generation and state schema across the capsule, pair and node, platform equal to `InitialPlatform`'s, and the invocation with StepId 0.

Item 6 is an acceptable reservation under §2. The post-rename owner rechecks are known work. Paying for them from the rename's reservation, at twice the cost measured by the same rechecks immediately before the rename, is conservative overcount. An overrun fails closed. The barrier is taken before those rechecks, so an overrun loses confirmation and not the barrier. Item 8 then ends the act with durability unconfirmed and no receipt.

Item 7 matches §6. Success continues. `EEXIST` with the stage binding unchanged is `LostRace`: release the lock, leave the stage, no barrier, no winner admission, no retry. Any other error, and any indeterminate visibility including `AlreadyExists` with a failed postcheck, refuses and latches. There is no deletion and no retry. `publish_with` already reports `Unchanged` only for `AlreadyExists` with a successful postcheck, and `Indeterminate` otherwise.

Items 8 through 11 grant nothing beyond the act. `Published` is private, not `Clone`, and holds the target, S, K, the closure, and the invocation ids and command. It holds no handle, fence, lock, or authority. The first ordinary operation takes a fresh fence and the §5 write gate. Creator observations are not promoted. `PROJECT.BUSY` stays the contention result. Nothing is deleted: a loser's stage, a stage that failed before the rename, and a foreign stage all remain. The 465 scan of 64 staging names applies only to an `OpenSIP` with no ACL, which cannot hold a stage. `LostRace` and `NotPristine` go to existing-root admission. Indeterminate, barrier, and recheck failures leave the creator unavailable. Public diagnostics belong to 468.

Do not commit.
