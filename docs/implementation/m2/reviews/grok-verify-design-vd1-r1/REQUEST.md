Grok review: VD1, explicit supersession of an inventory description meaning in `tools/verify_design.py`. The review covers law VD1 r1 and its tooling (VD1-a) together, with **separate verdicts**. Claude Opus 5.5 leads. You are the single reviewer.

Do not edit any repository, commit, push or delegate. Write only under `/tmp/opensip-implementation/reviews/grok-verify-design-vd1-r1`. Run no product cargo: no Rust changes. You may run the Python commands under "Checks" and read-only git.

## Subjects

The pins are in hashes.txt.

- **Law.** `docs/implementation/m2/verify-design-vd1/PROPOSAL.md` (r1), untracked in arch.
- **Tooling.** The worktree `/Users/sb/code/opensip-ai/opensip-vd1` is detached at product main 96ca141. Two existing files change: `tools/verify_design.py` and `tools/tests/test_design_binding.py`. Save `git -C /Users/sb/code/opensip-ai/opensip-vd1 diff` as `subject.diff` and check its sha256 against hashes.txt.
- **Evidence (not a subject).** `docs/implementation/m2/verify-design-vd1/evidence/probe_real_lock.py`.

There is no lock change, inventory change or new path. The v119 descriptions of both files stay true (rows 847 and 896).

## Context

Read these first:
- EXIT-PLAN.md, "Deferred tooling follow-up (lead decision, 2026-09-30)".
- `description-batch-d1/README.md` ("Deferred to VD1"), and judgment call 1 in `reviews/grok-description-batch-d1-r1/REVIEW.md`.
- `stale-descriptions-x1b/` (README and probe.py).
- The precedent that created `inventoryPassageInheritance`, design binding v4: `docs/implementation/m1/trials/binding4-01/subject/UNIT.md`, and review `m1/reviews/binding4-01/review.md`. Its rule: "Differing meanings for the same physical passage refuse; no implicit last-writer-wins rule. … A direct identical final override makes propagation unnecessary; a conflict refuses."
- The 16 rows in the lock come from 468a (on inventory74) and 461b (on inventory80), carried by `ordinary-writer-inventory-v81` and later inventories.

## Why nothing can change an inherited meaning at 96ca141

- **Inventory rows are carried by value.** Raw descriptions never change. The effective text is the projection's `after`.
- **Overrides match raw bytes.** `contract_successor` requires an override's `before` to equal the parent's raw passage, so it can never name the effective text.
- **A direct override on the selected inventory conflicts.** Its `before` is the raw text, its `after` is new, and it differs from the projection: "inherited inventory meaning conflicts with direct override".
- **A second override on the original parent conflicts:** "conflicting contract passage overrides".
- **An inventory successor rewriting the row refuses:** `inheritedRowsEqualByValue` and "inherited inventory passage row changed".

## Design (law items 1 to 4)

**The new field.** A contract successor record may carry `passageSupersessions`. Each entry has exactly `parent`, `selector`, `before`, `after` and `supersedes`. `supersedes` has exactly `{record, parent, selector}` and names one entry, an override or a supersession, in a strictly earlier contract successor's record.

**What verify_design checks:**
- **Shape.** The parent is an inventory in the lock's chain, and the selector is `/files/N/description`.
- **Same row.** The supersession and its target select the same row by value. The supersession's parent is not earlier in the chain than the target's.
- **Chain.** `before` equals the target's `after`.
- **Linear.** For each file path, supersessions form one chain: the first names a root override, and each later one names the previous tail.
- **No restatement.** A row with a supersession cannot be given an ordinary override in the same or a later record.

**How it projects:**
- A link on the selected inventory is checked against the current effective text and is not projected.
- An ancestor link folds into the row's single inheritance entry: `before` stays the raw bytes and `after` becomes the new text.

## Tooling (VD1-a)

**`contract_successor`:**
- Validates the closed shape of each supersession. A parent and selector that duplicate any override or supersession in the same record is refused.
- Checks the parent is in the record's parent set, the text change is non-empty and different, and the selector resolves.
- Returns the supersessions as `passageSupersessions` in each unit's result. A v3 lock whose single contract carries a supersession refuses.

**`successor_chain`:**
- `inventory_row` resolves a passage to `(chain index, row)` only for a `/files/N/description` pointer on an exact inventory pin in the chain.
- **The contract loop**, in lock order:
  - checks each supersession against `published` (every entry of earlier records), `earlier_records` (exact record pins) and `tails` (the chain tail for each file path);
  - then refuses any ordinary override of a row that is now in `tails`. This check is skipped while `tails` is empty, so the real lock's path decodes nothing new.
- **After the existing projection** (unchanged), the fold:
  - an ancestor link must match the entry's current `after`, and replaces it;
  - a final link must match `current`, seeded from the inheritance entry or the direct root.
- The result gains a top-level `inventoryPassageSupersessions` count.

**Unchanged.** Every existing statement and refusal message is unchanged. The diff only adds code, apart from two return statements and the test fixture's `Fx.contract`, which writes the same record bytes when it is given no supersessions.

## Checks run by the lead

All runs used `PATH=/opt/homebrew/bin:/usr/bin:/bin` and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`.

**`python3.14 -B -m unittest discover -s tools/tests -p 'test_design_binding.py'`, in the worktree.** 83 tests OK, up from 64 at 96ca141. The 19 new tests are in `PassageSupersessionTests`:

Accepted cases:
- a supersession of an inherited row on the final inventory, with the lock unchanged;
- a chain of two;
- a supersession of a direct (plain) final override;
- an ancestor link folding into one inheritance entry. A stale lock entry refuses, and a later final link chains from the folded text.

Refusal cases:
- a stale `before` (raw bytes);
- a stale rebind to superseded text;
- a double supersession of one meaning;
- a double supersession through an identical root copy;
- two supersessions of one row in one record;
- a missing chain:
  - the named record is not in the lock;
  - the named record has a wrong sha;
  - the named entry is not in the record;
  - the named entry's parent pin is wrong;
- a named record that is not strictly earlier;
- a different row, or a non-description selector;
- a non-inventory passage, on either side;
- a parent that precedes its target;
- a restatement, in a later record or in the same record;
- a silent change, which still refuses through both pre-VD1 routes;
- an ancestor supersession of a suppressed projection;
- malformed entries (eight shapes, plus a duplicate with an override);
- a v3 lock.

The other files in `tools/tests` have 15 errors both at 96ca141 and with the change: they need product toolchains or fixtures. They are unrelated.

**`python3.14 -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .`, in the worktree.** Passed: 73 contract successors, inventory119 selected, 16 inheritance rows, `inventoryPassageSupersessions` 0, 40 generation sources, 48 admission sources and 15 aliases. Without `--implementation` it also passes.

**`python3.14 -I -B docs/implementation/m2/verify-design-vd1/evidence/probe_real_lock.py`.** This is the real lock plus in-memory D2-shaped successors that supersede the inherited `read_premise.rs` meaning (461b's override). All 8 cases matched their expectations:

| Case | Result |
|---|---|
| D2-shaped supersession | PASSED, 16 rows unchanged |
| Second link | PASSED |
| Stale raw `before` | REFUSED |
| Double supersession of 461b | REFUSED |
| Stale rebind | REFUSED |
| Missing chain (D1's record named) | REFUSED |
| Pre-VD1 silent direct override | REFUSED, "conflicts with direct override" |
| Real lock | PASSED |

The same probe with `/Users/sb/code/opensip-ai/opensip` (main) as its argument **passes all four refusal cases**. The pre-VD1 verify_design ignores an unknown record field. This is why law item 6 fixes D2's binding order.

## Judgment calls: rule on each

1. **The target is named explicitly (lead decision).** Rejected: an implicit chain that matches `before` against the effective text. It works, but the reviewed record would not say which meaning it ends.
2. **Fold into one inheritance entry; a final link is not projected (lead decision).** The lock's v4 shape, entry fields and canonical order are unchanged. `before` stays the raw bytes, which the existing projection helpers (for example inventory122's `verify_projection.py`) already assert. Rejected: one entry per link.
3. **Linearity is per file path, not per target identity.** Two supersessions that start from identical root copies on different inventories are still a double supersession. Restating a row once it is superseded refuses, even when the restatement is identical to the root.
4. **Scope.** Only inventory row descriptions, the one kind binding v4 projects. Every other passage keeps binding v4's rule.
5. **An ancestor supersession of a suppressed projection refuses** (the root has an identical direct copy on the final inventory). This fails closed rather than defining a second lock form. Is that the right call, or should it fold into the direct copy?
6. **D2 is a named follow-up, not part of VD1 (lead decision).** One review cannot pin two verify_design subjects. D2's four texts must be checked against code at D2's head and built on the inventory selected after inventory122, which is in review. D2 must be bound only once VD1-a is in the product, because the old tool silently ignores `passageSupersessions`. Should VD1-a also close the record's field set? The lead's view is no: the 73 accepted records carry varied fields (`standing`, `previousCandidate` and others), and closing them is a separate change.
7. **No inventory successor.** Both paths exist, and their descriptions stay true.
8. **The output gains fields:** each contract result's `passageSupersessions`, and the top-level `inventoryPassageSupersessions`. Callers such as `verify_scratch.py` read named keys only.

## Decide

**For the law:**
- Is the rule sound under binding v4? Does it reintroduce any last-writer-wins path?
- Are items 1 to 6 complete and unambiguous?
- Are the rejected alternatives right?

**For the tooling:**
- Does the code implement the law exactly?
- Can any stale `before`, missing chain, fork, restatement or silent change pass?
- Is any existing check weakened?
- Do the tests cover each refusal at its intended guard?

Is anything else wrong?

## review.json

review.json must contain:
- `"law"`: `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "requiredFindings": [...], "subjectSha256": "<sha256 of PROPOSAL.md>"}`;
- `"tooling"`: `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "requiredFindings": [...], "subjectSha256": "<sha256 of subject.diff>"}`;
- `"productHead"`: the full hash of 96ca141.

VD1 is not a verify_design-selected unit: no lock binding is added. So it carries no `subjectManifestSha256` and no `inventoryCandidateAssessment`.

Write REVIEW.md and review.json. Do not commit.
