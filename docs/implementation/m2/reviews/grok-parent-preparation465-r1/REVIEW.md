# Review: parent preparation 465 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/initial-parent-preparation-465/PROPOSAL.md`. No repository edits. No product cargo.

The proposal is 6505 bytes, sha256 `aef6f7cd4c41b88dc6c84623500fbf68702b3dc19d160b5e3c2d748afd7523a8`, matching `hashes.txt`. Items 4 and 5 are the owner's decisions of 2026-09-27. The review is of how they are written. The creator stays disabled.

## Verdict

**ACCEPT.**

## Answers

The effect order matches §3. Nothing is created until the lineages, the actor, `InitialCore` and `InitialPlatform` rechecks, the 460 walk, H's filesystem, the intent target and storage, and the chain's exact names have been rechecked. H's barrier is applied before H is consumed as a parent. Then `Library`, `Application Support` and `OpenSIP` each get create-or-admit, admission, the same filesystem as H, their own barrier, and their containing parent's barrier. That is seven barrier operations: H once as the base, then own and parent for each of the three ancestors. H is flushed again as `Library`'s parent. No directory outside that suffix is created. A barrier error still takes the post-sample, then the attempt latches, which is what `confirm_directory_barrier` already does: it samples after a failed flush and returns no receipt.

The accepted kinds are `FullFlush`, and `Fsync` only when `F_FULLFSYNC` fails with `EINVAL`, `ENOTSUP` or `ENOTTY`. Any other result makes the creator unavailable, with no retry. `DirectoryBarrierReceipt` borrows its directory and `is_for` compares handle identity. The in-memory record keeps the position and the kind beside the owned handle, checked against that handle when taken. It is not serialized and does not enter P0. That is a typed receipt retained for this act. A borrow cannot outlive the handle, and the record does not pretend it can.

Only a raw `EEXIST` from `mkdirat` leads to fresh admission, through a new no-follow open. `create_exclusive_directory` can return a synthetic `AlreadyExists` after `mkdirat` has succeeded, when the new directory is not a fresh empty directory owned by the caller. That result is not admission. Any other failure after the directory call refuses, because a directory the creator made may exist and must not be treated as a pre-existing ancestor. Neither path chmods or rewrites an existing ACL, except item 5.

Item 4 is scoped to the two names in 458 §5. A new 0700 `Library` or `Application Support` omits its ACL, and after a crash that directory is a reused one. Evidence B admits the omission for those names, new or reused, only through the premise's own `fstatfs` on that descriptor. With no premise, both names refuse, as root to H does. The premise is not extended to `OpenSIP` or to `preview-v1`.

Item 5 is not a permission repair. It adds only the zero-rights owner allow that a fresh `OpenSIP` creation would add, and only when that existing directory is owned by the invoking user, mode exactly 0700, ACL omitted, and holds no entry except §2 staging names (`.opensip-stage-install-` plus 32 lowercase hex). The allow grants nothing. Any other `OpenSIP` state refuses as 460 refuses it today. §1b still forbids chmod of an existing ancestor and forbids granting group or other access. §6 still forbids deleting the ancestor. The case is the interrupted creation step, not a repair of a directory that has another mode, owner, ACL, or contents.

Item 6 reserves, before each `mkdirat`, that component's kind check, exact name, ACL capture, the `OpenSIP` append and recapture or the premise `fstatfs`, the filesystem sample, both barriers, and the name recheck. A ledger that cannot cover them stops before the syscall. Later rechecks of core, platform, actor and chain are charged when they run. A failure there latches and leaves the ancestors, which is §6.

Items 7 through 11 hold. The 460 walk's H and `InitialPlatform`'s H must be the same device and inode, and both must pass `qualifies_installation_filesystem`. Storage is rechecked immediately before the first effect and again before the permit: a changed target refuses, and a stronger classification refuses unless the intent carries `--allow-backup-custody`. The preparation is private, not `Clone`, and bound to the attempt and to the intent's lineage and target. The permit is minted only through that preparation, after a positive no-follow absence of `preview-v1`, a fresh recheck, and `consume` of the intent. It holds the preparation's handles, the consumed invocation, the command, the storage admission, the disclosed target, and the absence sample. It holds no fence, stage, or premise. A dangling symlink at `preview-v1` is an entry, so it is `NotPristine`, not absence. That result latches and ends the creator act. Ancestors already created stay. Nothing is deleted. The next invocation re-admits every ancestor and pays every barrier again.

Do not commit.
