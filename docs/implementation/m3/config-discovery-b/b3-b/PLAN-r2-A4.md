# B3-b plan r2, amendment A4: branch A decides its members before the walk, so index gitlinks bound every descent

**Lead plan amendment, 2026-10-17. Unreviewed, round 2** (round 1: Codex `codex-b3b-plan-a4-r1`, REQUIRED-FINDINGS; see A4-6). It amends the accepted B3-b plan r2 (`PLAN-r2.md`) as amended by A1 to A3. It also changes one accepted reference decision, B3-b0's LD-B3B0-6 (branch A's order). Law M3-B r9 is unchanged.

## A4-1. Why the order must change

**Item 6b's index gitlinks are nested repositories** (law M3-B r9 items 21 and 22). They are known only from the member's index, which item 6b reads.

**B3-b0's branch A is SLM-first** (LD-B3B0-6, r2, after Codex B3B0REF-R1-RF-2). A pass-two walk with the provisional members entered decides the array's grammar, crossings, pruned trees, absence and chain custody. Placement, the cap and item 6b come only after it.

**B3-b0 has no index.** It sees a nested repository only as a VCS marker, so its trial never enters one. The product's trial, run before item 6b, can enter an index-only nested repository, and can list it, judge custody below it, or fail inside it. Those are observations the boundary forbids (Codex B3B2B2B-R2-RF-1). A gitlink-aware walk after the trial cannot undo them, and B3-b2b1's short-circuit rule (Codex B3B2B1-R1-RF-2) forbids observing later members before the trial. **No order consistent with both SLM-first and the index boundary exists.** So the order changes, and B3-b0 is amended to model the index (A4-3).

Codex B3B0REF-R1-RF-2 required that branch A's stated order be the one implemented, and allowed a different public priority if it is settled and documented. This amendment settles one.

## A4-2. The order (branch A, W2, a `workspaceRoots` array or `--workspace-root` present)

1. **The array gate (r2).** This is pure: no observation, no walk and no member decided. It returns SLM's own refusal records, in SLM's own order for these two checks (`_explicit_units`, security_lifecycle_model_v1.py:687-694):
   - **The array's size first.** More than 4,096 roots (`MAX_EXPLICIT_JOINS`, the shared rule's `MAX_WORKSPACE_UNITS`) refuses `PROJECT.EXPLICIT_PATH_INVALID`. Its path is `null`, and its detail is `TOO_MANY_JOINS` for `--workspace-root` or `TOO_MANY_WORKSPACE_ROOTS` for the configuration's array.
   - **Then the first root, in array order, that fails the shared rule's grammar** (`normalize_explicit_root`). It refuses `PROJECT.EXPLICIT_PATH_INVALID` with detail `JOIN_PATH_GRAMMAR`. Its path is the root's raw text, or `null` when that is not a string.

   **Both carry SLM's D9 for that code:** request-rejected, exit 2, `CONFIG.INVALID`. **The chosen provenance** is the provenance of the discovery without members (LD-B3B0-5), which every member-rule refusal carries. The walk without members supplies only that provenance; its own verdict never replaces the gate's.

2. **The member decisions, in path order, each stopping at the first refusal.** These are B3-b0's steps 2 to 4, unchanged in themselves. They now run before any walk:
   - placement failures and other volumes (row 2);
   - the cap (row 5);
   - directory custody, then item 6b, per candidate (row 2).

   No later candidate is observed after a refusal (B3B2B1-R1-RF-2). This holds within the custody-and-6b phase. The placement observations that form and count the candidates precede it, as they do today (Codex B3BA4-R1-NBO-2). **A refusal is a member-rule refusal:** `PROJECT.ROOT_CUSTODY_REFUSED` or `PROJECT.SCOPE_LIMIT`, carrying the provenance of the walk without members (LD-B3B0-5), as today.
3. **The walk, once,** with the admitted members entered and their index gitlinks as nested repositories. It decides absence, crossings (gitlinks included), pruned trees and chain custody, in SLM's array order. **Its refusal is the result,** with no members and the declaration rows as they stand (the shape B3-b0 gives a trial refusal today). Otherwise, its accepted record is the result.

**Precedence, as a public priority:**
- the array's size;
- then grammar, for the whole array;
- then the member rules, in path order;
- then the walk's refusals.

**It differs from LD-B3B0-6 and from SLM's per-root order in two ways:**
- **(r2) Grammar is global.** A malformed root anywhere in the array refuses before an earlier root's crossing, pruning, absence or custody refusal. SLM checks each root completely before the next, so it would give the earlier root's refusal. For example, `["missing", "../bad"]` was `ABSENT` and is now `JOIN_PATH_GRAMMAR`.
- **A member rule comes before a walk refusal** wherever both apply. That covers, for example, a later candidate's layout failure beside an absent root, or beside a crossing in another member. B3-b0 r3's checker pins two such cases, and r4 revises both: `rf2-*-absent-before-layout` and `rf2-*-crossing-before-layout`. The other `rf2-*` cases keep their results: the grammar cases, `member-then-absent` and `member-decisions-in-path-order`.

**Candidates withheld from the provisional set** (a crossing into a nested project, LD-B3B0-7's boundary kind) stay withheld. A root inside one refuses in the walk, as today.

**Branch B is unchanged:** members, item 6b and their gitlinks are decided before its one walk.

## A4-3. The authority: B3-b0 r4, contract successor 169

**A design unit amends B3-b0:**
- **Its `discover`** takes item 6b's index gitlinks as a side table: `memberGitlinks`, giving each admitted candidate's gitlink paths, as `memberObservations` gives its verdict.
- **Pass two** treats each admitted member's gitlink directory as a nested repository: never entered, recorded in `nestedRepositories`, and a crossing for an exact root. The link stage treats an entry at or below a gitlink as inside that nested repository (`entry-not-in-a-member`).
- **Branch A follows A4-2.**
- **Its checker** revises the two `rf2-*` precedence cases to A4-2's priority, keeps the grammar-before-layout and grammar-after-layout cases under both array sources (their records unchanged), and adds controls:
  - (r2) mixed arrays where malformed grammar follows an earlier root that would otherwise refuse: a conventional repository, an absent root and a custody failure, each under both array sources. Each asserts the exact refusal, path and detail, and that no item-6b verdict is consulted;
  - (r2) the array-size boundary: 4,096 roots with a malformed one is the grammar refusal, and 4,097 is the size refusal;
  - a gitlink crossing with a descendant that fails custody;
  - a selected member whose gitlink subtree would fail;
  - the mixed case, a gitlink crossing in one member with another member's refusal, under both array sources;
  - links below a gitlink;
  - a branch-B gitlink.

It is bound as contract successor 169 before the product unit uses it. B2-b0, SLM, the B2-a rule, B-S1 and the schemas are unchanged.

## A4-4. The product (B3-b2b2b round 3)

B3-b2b2b r3 carries the decision core's branch-A restructure (B3-b2b1's code): phase one decides all of branch A, and the trial phase and `TrialRefused` are removed. With it come B3-b2b1's vectors regenerated from r4, the composition's single walk, and the r2 findings B3B2B2B-R2-RF-2 and RF-3. Its controls include, under both array sources:
- the two RF-1 controls, asserting that the walk never enters the gitlink interior;
- the mixed case, bound to r4;
- (r2) the gate's records, asserting that no item-6b request is made;
- the r2 fixes: item 6b's reopened ancestors, `M/.git` and its config and index bound to the shared table, and a provider read repeated within a phase. A3's obligations all remain (Codex B3BA4-R1-NBO-2).

## A4-5. Steps (as amended by A1 to A4)

1. B3-b0, B3-b1, B3-b2a, B3-b2b1 and B3-b2b2a (bound).
2. **B3-b0 r4** (design; contract successor 169), bound.
3. **B3-b2b2b r3**, with its inventory.
4. B3-b2b2c.
5. B3-b3a, B3-b3b and B3-b3c.
6. The status round.

## A4-6. Round 2 (Codex `codex-b3b-plan-a4-r1`)

| Finding | Resolution |
| --- | --- |
| **B3BA4-R1-RF-1:** a no-members walk does not implement the grammar-first refusal | **The gate returns the refusal itself** (A4-2 step 1): the size refusal, then the first malformed root's `JOIN_PATH_GRAMMAR`. The path, D9 and detail are SLM's for that root, and the provenance is that of the discovery without members. The walk supplies only the provenance. **The global grammar-first change, and the size-before-grammar order, are documented** as precedence. **Checker and product controls:** both existing grammar cases kept; mixed arrays (an earlier repository, absence or custody failure, then malformed grammar) asserting exact records and no item-6b consultation; the 4,096/4,097 size boundary. |
| **NBO-1, NBO-2** | Noted. The short circuit is scoped to the custody-and-6b phase (A4-2 step 2). A3's obligations and R2's RF-2 and RF-3 remain, in A4-4. |
