# VD1 r1 — explicit supersession of an inventory description

**Law: ACCEPT.** **Tooling: ACCEPT.** Required findings: none.

The rule fits binding v4. A later contract cannot replace a meaning by writing a new `after`. It has to name the current tail, and `before` has to equal that tail's `after`. A stale `before`, a second start from an identical root copy, a skipped link, and a restatement all refuse. The lock's v4 shape, entry fields, and canonical order stay as they are.

## Subjects

Law `docs/implementation/m2/verify-design-vd1/PROPOSAL.md` (r1): 10595 bytes, sha256 `c46828c5b8655b3c1b805af0c18316476f1903dfb0d23835ce5b6d7572dec1da`.

Tooling worktree `/Users/sb/code/opensip-ai/opensip-vd1`, detached at `96ca141895c1e80307dbce72f58e0e2dea6f91cc`. `subject.diff` is 24624 bytes, sha256 `675462b75ff15340d0fd2a65694272fee5550437cd40ba5e466b39ec829c688d`. Two files change: `tools/verify_design.py` (+110) and `tools/tests/test_design_binding.py` (+213). No lock change and no inventory successor.

`~/Library/Application Support/OpenSIP` is absent.

## Why the rule is binding v4's

Binding v4 refuses differing meanings for one physical passage and refuses a conflicting direct override. An inventory successor carries rows by value, so the raw description never moves. The effective sentence is a contract override's `after`, projected by file path into `inventoryPassageInheritance` (16 rows at this head: 468a's eight and 461b's eight).

The four routes that block a refresh are still in force, and the new code leaves their messages alone:

- a direct override whose `before` is the raw bytes conflicts with the projection;
- an override whose `before` is the effective text fails the raw-parent check;
- a second override on the original parent conflicts;
- an inventory successor that rewrites the row fails `inheritedRowsEqualByValue`.

D1's review left `read_premise.rs`, `installation_session.rs`, `store_lineage.rs`, and `initial_installation.rs` on those inherited pointers. X1b's probe shows the same wall for `read_premise.rs`. VD1 adds one reviewed way through that wall. D2 writes the four sentences later.

## Law

Items 1 to 6 are complete. Each supersession has exactly `parent`, `selector`, `before`, `after`, and `supersedes`. `supersedes` has exactly `{record, parent, selector}` and names one override or supersession in a strictly earlier contract record. The parent is an inventory in the chain, the selector is `/files/N/description`, the row matches by value, the parent is not earlier in the chain than the target, and `before` equals the named entry's `after`. Per file path there is one chain: the first link names an ordinary override, and each later link names the previous tail. Once a path has a supersession, an ordinary override of that path refuses, including an identical copy of the root.

On the selected inventory the link is checked against the current effective text and is not projected. On an ancestor it folds into the one inheritance entry: `before` stays the raw bytes, `after` becomes the new text, and the fold requires the entry's current `after` to equal `before`. A stale lock entry still fails "differs from reviewed ancestor meaning". Any other passage keeps binding v4. A v3 record that carries a supersession refuses. v1 and v2 locks have no contract slot, so they cannot bind one.

The standing holds: this changes which reviewed sentence describes a file. It does not change inventory bytes, package edges, roles, ownership, or runtime trust, and verify_design still runs no generator or product code.

### Calls

1. **Accepted.** The target is named. An implicit match of `before` against the effective text would verify, and the record would not say which accepted meaning it ends. A stale pin refuses at the named target.

2. **Accepted.** One inheritance entry per passage. A final link is not projected, so a supersession on the selected inventory leaves the 16 lock rows unchanged. `before` stays the raw bytes that the existing projection helpers already require. One entry per link would change the lock's uniqueness rule and every helper.

3. **Accepted.** Linearity is per file path. Two supersessions that start from identical root copies on different inventories are a double supersession. A restatement refuses even when its text equals the root.

4. **Accepted.** Scope is inventory row descriptions, the one kind binding v4 projects. A line selector or any other passage still follows the existing rule. On a JSON inventory, a line selector already refuses.

5. **Accepted.** An ancestor supersession of a suppressed projection refuses. The identical direct override on the final inventory is what suppressed the inheritance entry. Folding the ancestor link into that direct copy would need a second lock form: an inheritance entry whose `after` had moved, beside an accepted override whose `after` had not. The way to move that meaning is a supersession of the direct copy itself. Fail closed.

6. **Accepted.** D2 is a follow-up, not part of VD1. One review pins one verify_design subject. D2's four texts are checked at D2's head, on the inventory selected then. VD1-a does not close the contract record's field set. The 73 accepted records already carry fields beyond the override list (`standing`, `previousCandidate`, and others). A closed set would refuse this lock. Unknown fields stay a later tooling unit. The binding order is the mitigation for this field: D2 is bound only once VD1-a is in the product, because the tool at 96ca141 ignores a record field it does not know.

7. **Accepted.** No inventory successor. Both paths exist. v119 row 847 (`tools/tests/test_design_binding.py`) still says the tests refuse changed, unreviewed, duplicate, escaping, or cross-subject bindings. Row 896 (`tools/verify_design.py`) still says the tool verifies input bytes and the bound approval chain. Both sentences remain true.

8. **Accepted.** Each contract result gains `passageSupersessions`, and the top-level result gains `inventoryPassageSupersessions`. On this lock every contract list is empty and the count is 0. Scratch verifiers read named keys (`inventoryPassageInheritance`, `contractSuccessors`, and so on). `generate_contracts.py` reads `generationSources` only.

## Tooling

`contract_successor` checks the closed shape, the parent set, a non-empty `after` different from `before`, and that the selector resolves through the existing `selected_passage`. A duplicate parent and selector, shared with an override or another supersession, reuses "duplicate passage override". The `before` is not compared with the raw parent bytes. The named target, the same-row check, the chain, the linearity, and the restatement all run in `successor_chain`, in lock order, against `published`, `earlier_records`, and `tails`. The restatement scan is skipped while `tails` is empty, so this lock's override path decodes nothing new.

The projection loop is unchanged. After it, an ancestor link must match the entry's current `after` and replaces that `after`. A final link must match the effective text, seeded from the inheritance entry or the direct root, and it does not write the entry. `verify` refuses a v3 contract whose supersession list is non-empty ("passage supersessions require a v4 successor chain").

The diff adds that code. The two return statements gain the new fields. `Fx.contract` writes the same record bytes when it is given no supersessions. No existing refusal message is edited.

The 19 `PassageSupersessionTests` hit the guard each refusal names:

- stale `before`, and a rebind to superseded text, fail the chain's `before` comparison;
- a second supersession of one meaning, an identical root copy, and two links for one path in one record fail the tail check;
- a missing record, a wrong sha, a missing entry, and a wrong parent pin fail the named-target checks;
- a reversed chain fails the strictly-earlier check;
- another row, a non-description selector, and a non-inventory passage on either side fail the inventory-row checks;
- a parent earlier in the chain fails the chain-index check;
- a restatement in a later record or the same record fails the post-tail override scan;
- a silent ordinary override still fails the raw-before check or "conflicts with direct override";
- an ancestor link whose lock entry is stale fails the existing inheritance comparison, and a later final link chains from the folded text;
- an ancestor link over a suppressed projection fails "superseded inventory meaning is not inherited";
- the eight malformed shapes, and a duplicate shared with an override, fail inside `contract_successor`;
- a v3 lock fails in `verify`, before any chain check.

## Checks

Private `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/grok-vd1-tmp`, mode 0700. `python3.14`. No product cargo.

- `unittest discover -s tools/tests -p test_design_binding.py`: 83 tests, OK, 0.314s. That is 64 at this head plus the 19 new tests.
- `verify_design.py` with `--implementation .`: passed. 73 contract successors, each with `passageSupersessions` empty, inventory119 selected, 16 inheritance rows, `inventoryPassageSupersessions` 0, 40 generation sources, 48 admission sources, 15 aliases.
- The same command without `--implementation`: passed, with the same successor counts and no generation or admission block.

`probe_real_lock.py` on this worktree, all eight cases matched: a D2-shaped supersession of 461b's `read_premise.rs` meaning passed with 16 rows unchanged and count 1; a second link passed with count 2; a stale raw `before`, a double supersession, a stale rebind, and a chain that names D1's record all refused; the pre-VD1 silent direct override refused with "conflicts with direct override"; the real lock passed with count 0.

The same probe pointed at `/Users/sb/code/opensip-ai/opensip` (current main `adc9081`, which selects inventory v122 and carries 55 inheritance rows) shows the pre-VD1 tool. The four supersession cases the law refuses are accepted there, and the result has no `inventoryPassageSupersessions` field. The silent direct override still refuses. That is why D2 waits until VD1-a is the product tool. The worktree result above is the one for this review: 16 rows at 96ca141.

The other files under `tools/tests` were not run. The lead reports 15 errors there both at 96ca141 and with this diff, from product toolchains and fixtures.

The private temp directory is removed. This directory holds `subject.diff`, `REVIEW.md`, and `review.json`.
