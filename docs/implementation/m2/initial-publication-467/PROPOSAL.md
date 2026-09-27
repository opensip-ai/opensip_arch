# Stage, validate and publish the initial installation — proposal 467 r1

2026-09-27. Claude Opus 5.5, implementation lead. Law for units 466b (the remaining P0 producers) and 467 (stage, validate, publish, routes, handoff), under owner.md §1a step 6, §2 to §6, and laws 463, 464 and 465. Not code. Library only: no CLI command is wired (464 item 7), and development builds refuse at F0 (463). ACCEPTED by Grok 467 r1 on 2026-09-27.

## The P0 tree

The stage `OpenSIP/.opensip-stage-install-<nonce>` becomes `preview-v1` on publication. It holds exactly 14 directories and 11 files:
- **Directories:**
  - `stores`, `stores/S`
  - `transitions`, `transitions/lineage`, `transitions/lineage/S`, `transitions/lineage/S/0`
  - `trust`, `trust/records`, `trust/stores`, `trust/stores/S`, `trust/stores/S/events`
  - `trust/publications`, `trust/publications/initial`, `trust/publications/initial/S`
- **Files:**
  - `lifecycle.fence`: empty;
  - `project-registry.v2`: no entries;
  - `stores/S/store-instance.v1`;
  - `transitions/lineage/S/0/K.node`;
  - `selection.pair`;
  - the six trust files of 466 r1: three records, the creation event, the publication descriptor, and `trust/stores/S/state.v1`.

S is a fresh 128-bit CSPRNG draw, G is 0, and K is from `InitialCore`'s state writer. Every directory is 0700 and every file 0600, each with the zero-rights owner allow of a fresh private creation. Each new non-trust file is encoded canonically and must decode with its existing decoder. No schema successor is needed.

## Decisions

1. **Order.** The effects run in this order:
   1. Recheck and consume the permit (465 item 9), then recheck storage (item 2).
   2. Draw S and take the clock (item 3). No effect.
   3. Create the private stage.
   4. Build P0 in memory and verify it with the existing verifiers.
   5. Create the 14 directories, parents first.
   6. Create and write the 11 files. The fence goes first and is locked exclusively for the rest of the act. Then the registry, marker, node, trust records, event, descriptor and `state.v1`. `selection.pair` goes last: dependencies precede the descriptor, and the descriptor precedes the current pointer.
   7. Validate the whole stage (item 5).
   8. Re-barrier the stage and its parent, and recheck the owners.
   9. Exclusively rename the stage to `preview-v1`.
   10. Take the I-parent barrier.
   11. Run the post-publication rechecks.
   12. Release the fence lock.
   13. Hand off.

   Any refusal latches, and no later effect runs.
2. **Storage after the intent is consumed.** Consuming the intent in 465 retires `recheck_intent_storage`. The handoff carries the admitted storage, the target and the flag. Before the stage is created and again before the rename, the target is rebuilt from the actor and the storage is re-classified. A change refuses as in 465 item 8.
3. **Clock.** `CreationInputV1.observation` is one clock sample `{bootId, mono, wall}`, taken once before the stage and projected by the existing clock projection. It is recorded evidence only. P0's clock phase stays unevaluated, and it grants no time admission.
4. **Barriers.** Every directory receives its own barrier and its parent's barrier before it receives children. Every file receives `F_FULLFSYNC` (no fallback) and then its containing directory's barrier. The stage root and its parent are barriered again before the rename. After the rename, only the I-parent barrier is taken (§4). I's own barrier belongs to the §5 write gate. Every receipt is checked against the handle it is for. Batching barriers would be a law change and is not made.
5. **Validation before publication.** For every retained directory:
   - its entries must be exactly the manifest's children;
   - it must pass the private judgment;
   - it must have the device and inode retained at creation.

   Every file is reopened no-follow by name and must be:
   - regular, one link, 0600, owned by the invoking user, with a private ACL;
   - the same device and inode as at creation;
   - bytes equal to the written bytes, read with an exact-length cap;
   - accepted by its decoder.

   The trust records are verified again from the reread bytes. The cross-joins hold:
   - the physical marker equals the marker record;
   - the staging name equals the stage nonce;
   - `deliveringCore` equals the pair's closure, which equals the core's;
   - store, generation and state schema agree across the capsule, the pair and the node;
   - `platform` equals `InitialPlatform`'s;
   - the invocation is the handoff's, with StepId 0.
6. **Budget.** One ledger: the attempt's. Every effect reserves its own postchecks before its syscall. The owner rechecks after the rename (core, platform, actor) run inside the rename's own reservation. It is sized at twice their cost as measured by the same rechecks just before the rename, and an overrun fails closed. After the rename the order is barrier first, then rechecks, so an overrun can only lose confirmation, never the barrier.
7. **Rename outcome classification.**
   - Success continues.
   - `EEXIST` with the stage binding unchanged is the **loser route**. Release the fence lock, leave the stage, end the act, and return the typed `LostRace`. No barrier, no admission of the winner, no retry.
   - Any other error with the binding unchanged means no rename was performed. It refuses and latches.
   - Any indeterminate visibility is the **indeterminate route**. Latch, release the lock, and refuse. No barrier, no receipt, no winner admission, no retry and no deletion.
8. **After the rename.** If the I-parent barrier or a recheck fails, I is visible and complete but its durability is unconfirmed. There is no receipt, and the act ends without a retry (§6).
9. **Handoff.** On success the act returns `Published`: a private, non-Clone value holding the target, S, K, the closure, and the invocation ids and command. It holds no handle, fence, lock or authority. The creator releases its fence lock after its rechecks. The installation's first ordinary operation enters through the ordinary installation fence and the §5 durable write gate: fresh fence, its own barriers, id reservation. Creator observations are never promoted. Normal contention (`PROJECT.BUSY`) applies.
10. **Leftovers.** The act deletes nothing:
    - a loser's stage, a stage that failed before the rename, and any foreign stage all remain;
    - removing one's own leftover stage is a separate, later mechanism, per §6, with the live owner, retained handles and the same budget;
    - 465's 64-entry staging scan applies only to an `OpenSIP` with no ACL, which cannot hold stages.
11. **Routing.** `LostRace` and `NotPristine` go to existing-root admission (468 and M2). Indeterminate, barrier and recheck failures leave the creator unavailable. The public diagnostic mapping belongs to 468.

## Forbidden substitutes

Deleting or adopting any stage; retrying a rename or barrier; admitting the winner after `EEXIST`; publishing without full validation; promoting creator observations into ordinary authority; a barrier on a handle other than the one its receipt names; a clock sample used as time admission; wiring a CLI command.

## Not claimed

No creator is enabled. On this BASELINE-ATTESTED host the real chain refuses at `/`, so every test uses a scratch chain. No cleanup mechanism. No public diagnostics.
