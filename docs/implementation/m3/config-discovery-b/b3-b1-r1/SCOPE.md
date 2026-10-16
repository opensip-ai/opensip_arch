# B3-b1 r1: X2 r9 item 6b, the member observation (M3-B unit B3-b, sub-unit B3-b1)

**Lead scope record, 2026-10-16. Unreviewed candidate.** It implements section 2 of the accepted B3-b plan r2 (`../b3-b/PLAN-r2.md`; Codex `codex-b3b-plan-r2`) under law M3-B r9 item 21 (X2 r9, successor S1; accepted).

**Base.** Product `2b297e6` (167 contract successors, inventory v202). This unit does not depend on B3-b0.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/git_tracking.rs` | **Item 6b,** added as described below. **Item 6a is refactored, not changed** (below). |
| `crates/security/src/custody/git_tracking_member_tests.rs` | **New.** Seven tests over real `git` scratch members under a scratch H, included in the existing test module (no new test `cfg` site). |

**Item 6b's parts:**
- **`NoRepository<'_>`,** constructible only by `TrackingObservation::no_repository()` when item 6a observed W as `NoRepository` (W2). `observe_members` takes it, so 6b cannot run without its precondition (law item 21: "6b without the NoRepository precondition" is forbidden).
- **`MemberPath`,** a canonical relative path of at most 256 segments (M1).
- **`MemberRefusal`,** with its subjects `member-vcs-unsupported:<reason>` and `member-outside-volume` (item 8). **`MemberVerdict`:** `Admitted { gitlinks }` or `Refused`.
- **`observe_members(inputs, NoRepository, members, work)`,** run on the caller's discovery ledger:
  - The environment, the global sources and the system sources are checked **once per pass**. A refusal there refuses every member with its reason.
  - Each member, in the order given, is reached from W's retained descriptor by no-follow opens. On the way it checks the device (M1, `member-outside-volume`), positive lookups of `.git`, `.hg`, `.svn` and `.jj` at every directory strictly between W and M (any is `vcs-other`, and a `.git` there is `evidence-changed`), and at M (`.git` required, any other marker `vcs-other`).
  - Then **item 6a's admitted layout, unchanged:** `M/.git`, `M/.git/config` and `M/.git/index` only, under 6a's custody, volume, linked-worktree, configuration and index rules.
  - The index's gitlinks are returned; they mark nested repositories inside the member, which stay boundaries.
  - Nothing is written. No evidence is retained for a recheck: the member evidence is not in the fenced recheck set (item 21; C1's per-read custody covers it).

**Item 6a, refactored only:**
- **`layout`** is item 6a's repository layout, factored out of `repository` so that 6b uses it unchanged. Every step, charge and evidence sample is in the same order. `repository` is `layout`, then 6a's index decode and marker match, as before.
- **The configuration check is a parameter (`ConfigCheck`).** Item 6a passes its existing `config`, so its behaviour is identical. Item 6b passes `config_decided`, with the same charge, parse and refusals, but the refusal is decided after the charged step returns. Likewise 6b's environment check and index decode are decided outside their charged steps. **Why:** the work ledger closes on any error inside a scope (`work_ledger.rs`). Item 6a ends its pass at its first refusal, but 6b must go on past one member's refusal to the next member on the same discovery ledger. Without this, a refused member closes the ledger and the pass fails `Budget(Closed)`, which the tests first showed.

## Lead decisions

- **LD-B3B1-1. Pass-level refusals refuse every member.** The environment, global and system sources are one union per pass (item 21: "the effective configuration is the union of the fixed system sources, the global sources and `M/.git/config`"). So a refusal in a pass-level source is every member's refusal, with that reason. **Rejected:** failing the whole discovery, which would turn a branch-B disclosure into a refusal.
- **LD-B3B1-2. Host I/O and ledger exhaustion fail the pass;** only 6a's `vcs-unsupported` reasons become per-member refusals. This matches item 8's rows: native I/O is the host I/O row, and exhaustion is `WORK.BUDGET_EXHAUSTED`.
- **LD-B3B1-3. Changed placement is `evidence-changed`.** B3-b2 counts and places a candidate before 6b runs. If a path component is now a symbolic link, absent or not a directory, or if `.git` now sits between W and M, the placement it was counted under no longer holds: `member-vcs-unsupported:evidence-changed`, 6a's reason for changed evidence.
- **LD-B3B1-4. The other-volume control is synthetic.** Law item 21 allows this where the platform cannot mount a volume in a test. The member walk is called with a W device that differs from the member's, which exercises the device comparison and the subject.
- **LD-B3B1-5. A real split index refuses as `index-malformed`.** Real git's split-index main file holds a name-less replacement entry. Item 6a's unchanged decoder refuses it as malformed before it reaches the `link` extension, whose own refusal (`index-split-or-sparse`) 6a's tests cover synthetically. Either way the split index is refused, as the law requires, and the subject is 6a's verdict on real git's bytes. The decoder is not changed here.

## Controls (law item 21)

The tests run over real `git` members in a private 0700 scratch under a synthetic H:
- **A conventional member is admitted,** with its gitlinks: a submodule-style gitlink inside the member is reported and stays a boundary. **Nothing is written:** the member trees are byte-identical before and after, and the pass is charged.
- **Each refusal with its subject:**
  - a `.git` file;
  - `.hg` at M;
  - `.hg` between W and M;
  - `core.worktree`, `include.path` and `extensions.objectformat=sha256`;
  - `commondir` present;
  - a split index;
  - group-writable `.git/index`, and a 0777 `.git` (6a's custody, never waived);
  - a symlinked path component.
- **Another volume** (synthetic, LD-B3B1-4).
- **An environment refusal refuses every member of the pass.**
- **W inside a repository gives no precondition** (`no_repository()` is `None`).
- **64 members are observed in one pass.** The 64/65 cap is B3-b2's count, before 6b.
- **`MemberPath` grammar,** at 256 and 257 segments.

Item 23's owner waiver never reaches Git evidence: `judge_project_object` is called with no waiver, as in 6a.

## Checks

Lane r1, `evidence/checks-r1/`:
- the security suite at base and candidate, with equal failure sets and seven new passing tests;
- Clippy, warnings denied, all targets;
- rustfmt on the new test file (`git_tracking.rs` is not rustfmt-clean at base, so it is not reformatted);
- the `git_tracking` tests, including all of 6a's;
- the environment exceptions;
- the discovery census `--check` (`git_tracking.rs` is outside its cost closure, and the census and the blind receipt stay current);
- the operability source census;
- verify_design.

**Mutations.** Each must make the `git_tracking` tests fail:
- the device check dropped;
- another marker at M allowed;
- a marker between W and M allowed;
- 6b's configuration check latching;
- gitlinks dropped;
- the environment refusal ignored;
- the precondition always granted;
- the linked-worktree check dropped;
- the outside-volume subject altered.

## Inventory

New path for inventory v203: `crates/security/src/custody/git_tracking_member_tests.rs`.

## Not claimed

- No caller: B3-b2 composes 6b with the readers and the walker.
- No member-observation ledger bound: that is B3-b3a.
- No snapshot: that is C1.
- No qualification.
