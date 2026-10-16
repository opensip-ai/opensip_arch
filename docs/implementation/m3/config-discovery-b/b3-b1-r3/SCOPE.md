# B3-b1 r3: X2 r9 item 6b, the member observation (M3-B unit B3-b, sub-unit B3-b1)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 3.** It implements section 2 of the accepted B3-b plan r2 (`../b3-b/PLAN-r2.md`; Codex `codex-b3b-plan-r2`) under law M3-B r9 item 21 (X2 r9, successor S1; accepted).

**Base.** Product `25972e1`: 168 contract successors (B3-b0 bound), inventory v202. Round 1's base was `2b297e6`; the two differ only in `design-lock.json`. This unit does not depend on B3-b0.

## r3 changes (Codex `codex-b3b1-r2`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B1-R2-RF-1:** `NoRepository::covers` bound pathname labels, not the retained root | **The proof holds the retained chain item 6a walked, and item 6b takes W from it.** A new `RootObservation<'a>` pairs item 6a's `TrackingObservation` with the `&'a ProjectChain` of the inputs it observed. Only `observe_root(inputs, work)` constructs it: `observe_tracking` unchanged, then `inputs.chain`. `NoRepository<'a>` is now that chain (`NoRepository(&'a ProjectChain)`), constructed only by `RootObservation::no_repository()` when the observation is `NoRepository`. `MemberInputs` no longer has a `chain`: `observe_members` destructures the proof and derives W, its retained descriptor and its device from the proof's chain. There is no second chain to substitute, so the binding is the borrow itself and no label, spelling or birth comparison stands in for it. `covers`, `TrackingObservation::no_repository` and the `precondition-root-mismatch` refusal are removed. Item 6a's `observe_tracking` and `recheck_tracking`, and every existing caller of them, are unchanged; `TrackingObservation` is unchanged. **Controls:** the cross-spelling control is kept, now as a substitution that cannot reach W_B. W_A's proof drives the pass over W_A: its member `a` is admitted, W_B's `m` is `evidence-changed` (not under W_A), and W_B's own observation gives no proof. **The new same-spelling control:** W_A is retained and observed in no repository, then moved aside, and a repository with a nested repository `m` takes its spelling as W_B. Under W_A's proof, `a` (still under the moved W_A) is admitted, `m` is not reached (`evidence-changed`), and W_B gives no proof. The ancestor-subset case Codex noted is gone with `covers`: a proof names one chain. **Mutation:** r2's `root-binding-skipped` retires with `covers`; `precondition-always` is retargeted at `RootObservation::no_repository`. |
| **B3B1-R2-NBO-1:** the custody mutation bypassed the fault injector | **A new mutation, `capture-refusal-latches`,** keeps `judge_decided` and its test-only fault queue, but decides the injected native capture refusal inside a charged step, as the accounted capture does. The same injected `Changed` and `Unsupported` faults then latch the ledger, and both not-latched controls fail on `expect`. `member-custody-latches` is kept as the guard against replacing the member judge. The injection point stays after the native capture: the platform crate is not changed for a test seam. |

**Evidence.** Lane r3 is at `evidence/b3b1-checks-r3/`. **Erratum:** r1's and r2's SCOPE and requests named their lanes `evidence/checks-r1/` and `evidence/checks-r2/`. The archived directories are `b3b1-checks-r1/` and `b3b1-checks-r2/`, as Codex found them.

## r2 changes (Codex `codex-b3b1-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B1-R1-RF-1:** native ACL-capture refusals still latched the shared discovery ledger | **The shared steps take a pass (`Pass`).** `Pass::Tracking` is item 6a: its existing `config` and `judge_project_object`, unchanged. `Pass::Members` is item 6b: `config_decided`, and a new **`judge_decided`**. That is `judge_project_object`'s custody judgment with the same charge (`capture_descriptor_acl_observed` charges `descriptor_acl_capture_cost()`, as the accounted capture does), the same pure check (`check_project_object_ordered`, shared order) and the same premise. A native capture refusal (`Changed`, `Malformed` or `Unsupported`) returns as a value and is decided after the charged step: it is the object's reason (`git-custody`, `config-custody`, `index-custody`, `global-custody`), as in 6a, and the ledger stays usable. Capture I/O and the premise's own filesystem sample fail the pass (LD-B3B1-2). **The custody facts are explicit:** `MemberInputs` carries the trusted groups and the premise (`MemberCustody`), and 6b builds its `ProjectChainPolicy` from them, so there is one source. `project_chain.rs`, which the census pins, is unchanged. **New controls,** through a test-only capture-fault queue in the member pass: a refused first member (`Changed` on its `.git` capture) followed by a valid member; a lone refused member (`Malformed` on its config capture); and a pass-level refusal (`Unsupported` on the global `~/.gitconfig` capture), which refuses every member. Each shows that the enclosing ledger scope still returns its value. **Mutation:** `member-custody-latches`. |
| **B3B1-R1-RF-2:** the `NoRepository` proof was not bound to the root used | **(Superseded in r3: see above.)** **`NoRepository::covers(chain)`.** The proof's evidence must hold the positive absence of every VCS marker at every directory of the given chain, from W up to `/`, under the chain's own spelling (the labels item 6a records). `observe_members` checks it before any member work, so a proof for another root refuses the pass (`precondition-root-mismatch`). **New control:** W_A outside any repository and W_B inside one. W_A's proof with W_B's chain refuses, with no member observed, and the ledger is not latched. **Mutation:** `root-binding-skipped`. |
| **B3B1-R1-NBO-1:** a mutation log was missing from the pinned evidence | The package builder excluded every path containing `-work`, which caught `mutation-linked-worktree-dropped.log`. It now excludes only work directories, and lane r2's archive holds every mutation log. |

Lane r2 is kept in `../b3-b1-r2/` and lane r1 in `../b3-b1-r1/`.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/git_tracking.rs` | **Item 6b,** added as described below. **Item 6a is refactored, not changed** (below). |
| `crates/security/src/custody/git_tracking_member_tests.rs` | **New.** Eleven tests (r3) over real `git` scratch members under a scratch H, included in the existing test module (no new test `cfg` site). |

**Item 6b's parts:**
- **`RootObservation<'a>` and `observe_root`** (r3): item 6a's observation bound to the retained chain it walked.
- **`NoRepository<'a>`,** W's retained chain, constructible only by `RootObservation::no_repository()` when item 6a observed W as `NoRepository` (W2). `observe_members` takes it and derives W from it, so 6b cannot run without its precondition (law item 21: "6b without the NoRepository precondition" is forbidden), nor over another root (r3).
- **`MemberPath`,** a canonical relative path of at most 256 segments (M1).
- **`MemberRefusal`,** with its subjects `member-vcs-unsupported:<reason>` and `member-outside-volume` (item 8). **`MemberVerdict`:** `Admitted { gitlinks }` or `Refused`.
- **`observe_members(MemberInputs, NoRepository, members, work)`,** run on the caller's discovery ledger:
  - The environment, the global sources and the system sources are checked **once per pass**. A refusal there refuses every member with its reason.
  - Each member, in the order given, is reached from W's retained descriptor by no-follow opens. On the way it checks the device (M1, `member-outside-volume`), positive lookups of `.git`, `.hg`, `.svn` and `.jj` at every directory strictly between W and M (any is `vcs-other`, and a `.git` there is `evidence-changed`), and at M (`.git` required, any other marker `vcs-other`).
  - Then **item 6a's admitted layout, unchanged:** `M/.git`, `M/.git/config` and `M/.git/index` only, under 6a's custody, volume, linked-worktree, configuration and index rules.
  - The index's gitlinks are returned; they mark nested repositories inside the member, which stay boundaries.
  - Nothing is written. No evidence is retained for a recheck: the member evidence is not in the fenced recheck set (item 21; C1's per-read custody covers it).

**Item 6a, refactored only:**
- **`layout`** is item 6a's repository layout, factored out of `repository` so that 6b uses it unchanged. Every step, charge and evidence sample is in the same order. `repository` is `layout`, then 6a's index decode and marker match, as before.
- **(r2) The pass is a parameter (`Pass`).** It replaces r1's `ConfigCheck`, and covers the configuration check and the custody judgment. Item 6a passes `Pass::Tracking`, its existing `config` and `judge_project_object`, so its behaviour is identical. Item 6b passes `Pass::Members`: `config_decided` and `judge_decided`, with the same charges and refusals, but decided after the charged step returns. Likewise 6b's environment check and index decode are decided outside their charged steps. **Why:** the work ledger closes on any error inside a scope (`work_ledger.rs`). Item 6a ends its pass at its first refusal, but 6b must go on past one member's refusal to the next member on the same discovery ledger. Without this, a refused member closes the ledger and the pass fails `Budget(Closed)`, which the tests first showed.

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
- (r2) **Capture refusals do not latch:** a refused first member followed by a valid one, a lone refused member, and a pass-level refusal.
- (r3) **A proof never authorizes another root,** at another spelling or at the same spelling.
- **64 members are observed in one pass.** The 64/65 cap is B3-b2's count, before 6b.
- **`MemberPath` grammar,** at 256 and 257 segments.

Item 23's owner waiver never reaches Git evidence: `judge_project_object` is called with no waiver, as in 6a.

## Checks

Lane r3, `evidence/b3b1-checks-r3/`:
- the security suite at base and candidate, with equal failure sets and eleven new passing tests (r3);
- Clippy, warnings denied, all targets;
- rustfmt on the new test file (`git_tracking.rs` is not rustfmt-clean at base, so it is not reformatted);
- the `git_tracking` tests, including all of 6a's;
- the environment exceptions;
- the discovery census `--check` (`git_tracking.rs` is outside its cost closure, and the census and the blind receipt stay current);
- the operability source census;
- verify_design.

**Mutations.** Each must make the `git_tracking` tests fail (r2 added `member-custody-latches` and retargeted `member-config-latches` at `Pass::config`; r3 adds `capture-refusal-latches`, retires `root-binding-skipped` and retargets `precondition-always`):
- the device check dropped;
- another marker at M allowed;
- a marker between W and M allowed;
- 6b's configuration check latching;
- gitlinks dropped;
- the environment refusal ignored;
- the precondition always granted;
- the linked-worktree check dropped;
- the outside-volume subject altered;
- (r2) the member pass judging custody with the latching capture;
- (r3) an injected capture refusal decided inside a charged step.

## Inventory

New path for inventory v203: `crates/security/src/custody/git_tracking_member_tests.rs`.

## Not claimed

- No caller: B3-b2 composes 6b with the readers and the walker.
- No member-observation ledger bound: that is B3-b3a.
- No snapshot: that is C1.
- No qualification.
