# Parent preparation and creation permit for the initial creator — proposal 465 r1

2026-09-27. Claude Opus 5.5, implementation lead. Law for unit 465, under owner.md §1a steps 5 and 6, §1b, §2, §3, §4, §5 and §6, and the first-creation storage paragraph, together with laws 458, 460, 462 and 464. Two decisions are the owner's own, made on 2026-09-27 (items 4 and 5). Not code. The creator stays disabled; unit 467 consumes the permit. ACCEPTED by Grok 465 r1 on 2026-09-27.

## Decisions

1. **Order.** Nothing has an effect until every prerequisite is rechecked:
   - the lineage of the actor, core, platform, intent and premise;
   - the actor, `InitialCore` and `InitialPlatform` rechecks;
   - the 460 walk from root to H and the fixed suffix, using the platform's premise if there is one;
   - H's filesystem, which must be the platform's H (item 7);
   - the intent target and storage (item 8);
   - the chain's exact names.

   Then the effects run in this order: H's barrier; then, for `Library`, `Application Support` and `OpenSIP` in turn, create-or-admit, admission, same filesystem as H, the directory's own barrier, and its parent's barrier. That is seven barriers in all: H, then own and parent for each ancestor, with H's barrier counted again as Library's parent (§3). After a barrier error, the post-sample is still taken, and then the attempt latches.
2. **Barrier receipt kinds.** Under the apfs primitive policy (462 item 5), a barrier is accepted if its receipt is `FullFlush`, or `Fsync` taken only as the platform's named-unsupported fallback. Any other result makes the creator unavailable, with no retry. A receipt is checked against its handle when it is taken. A barrier record (its position and kind) is kept in memory next to the owned handle. It is never serialized and never enters P0.
3. **Create or admit.** Admitting an existing ancestor is identical to admitting a new one: exact name, custody, same filesystem as H, its own barrier, and its parent's barrier. A missing ancestor is created exclusively with mode 0700. Only a raw `EEXIST` from `mkdirat` leads to fresh admission, through a new no-follow open. Any other failure after the directory call refuses, because a directory we made but cannot admit may exist. Neither path changes an existing mode or ACL (§1b), except as item 5 allows.
4. **Evidence B covers new and reused external ancestors (owner decision, 2026-09-27).** Law 458 §5 names "the reused `Library` and `Application Support`". That covers those two names whether they already existed or the creator has just made them. A new 0700 directory omits the ACL like a reused one, and after a crash it becomes a reused one anyway. The rule is the same, and it applies only through the premise's own `fstatfs` on that descriptor. When no premise exists, both names refuse on an omitted ACL, as root to H does.
5. **Finishing an interrupted `OpenSIP` (owner decision, 2026-09-27).** A crash between creating `OpenSIP` and adding its zero-rights owner allow leaves a directory with no ACL, and item 458 §5 would refuse it forever. The creator may add exactly that zero-rights owner allow, as a fresh creation does, to an existing `OpenSIP` only when all of these hold:
   - the directory is owned by the invoking user;
   - its mode is exactly 0700;
   - its ACL is omitted;
   - it holds no entry except staging names.

   The allow grants nothing. It completes the interrupted creation step and is not a permission repair. Any other `OpenSIP` state refuses as today.
6. **Budget.** Each directory creation is one effect whose postchecks reserve that component's own work before the syscall:
   - the kind check, exact name and ACL capture;
   - for `OpenSIP`, the append and recapture; otherwise the premise's `fstatfs`;
   - the filesystem sample;
   - both barriers;
   - the name recheck.

   A ledger that cannot reserve them stops before `mkdirat`. The later rechecks of core, platform, actor and chain are charged when they run. If one fails, the attempt latches and the ancestors created so far remain (§6).
7. **Same H.** The 460 walk's H and `InitialPlatform`'s retained H must have the same device and inode, and both must pass `qualifies_installation_filesystem`.
8. **Storage recheck.** Immediately before the first effect, and again before the permit, the intent's target is rechecked (464) and its storage is re-classified. A change of target refuses. A stronger classification than the intent holds (for example `BACKED_UP` where it held `UNKNOWN`) refuses unless the intent carries `--allow-backup-custody`.
9. **The preparation and the permit.**
   - **`InitialParentPreparation`:** private, not Clone, bound to the attempt and to the intent's lineage and target. It holds the H path, the three retained ancestors, `OpenSIP`'s filesystem sample and the seven barrier records.
   - **`InitialCreationPermit`:** minted only through the preparation. It requires:
     - a positive no-follow absence of `preview-v1` through the retained `OpenSIP` handle;
     - the names, intent, storage, core, platform and actor rechecked again;
     - the intent consumed (its single use).

     It holds the preparation's handles, the intent's invocation, command, storage admission and disclosed target, and the absence sample. It holds no fence, stage or premise. It exposes I's parent, a recheck, and a consuming handoff to 467.
10. **`preview-v1` present.** Any entry at `preview-v1`, including a dangling symlink, is not a creation refusal. It is a typed `NotPristine` result that latches and ends the creator act. Routing to existing-root admission belongs to 467 and 468.
11. **Partial creation.** Ancestors already created stay. Nothing is deleted. Any failure after the first effect latches with no later effect. The next invocation re-admits every ancestor and pays every barrier again (§6).

## Forbidden substitutes

Changing an existing ancestor's mode or ACL, except item 5's exact case; treating a synthetic `AlreadyExists` as admission; retrying a failed barrier or accepting an `Fsync` that is not the named fallback; a receipt that is not checked against its handle; the premise outside root to H, `Library` and `Application Support`; a permit without the absence observation or without consuming the intent; deleting created ancestors after a failure.

## Not claimed

No creator is enabled. No stage or publication. No Evidence B on a BASELINE-ATTESTED host: on this macOS 27 development host the real chain refuses at `/`, and tests run on scratch chains.
