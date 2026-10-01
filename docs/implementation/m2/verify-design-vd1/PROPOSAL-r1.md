# Explicit supersession of an inventory description meaning — proposal VD1 r1

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit VD1 of EXIT-PLAN.md ("Deferred tooling follow-up (lead decision, 2026-09-30)"). It amends how `tools/verify_design.py` judges a v4 design lock, so it amends design binding v4 (`m1/trials/binding4-01/subject/UNIT.md`, accepted by review binding4-01). Items 1, 4 and 6 contain lead decisions, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation and record it. Not runtime law: verify_design stays a developer provenance check and grants no product trust.

## Problem

Binding v4 fixed two rules for passage meanings:
- "Differing meanings for the same physical passage refuse; no implicit last-writer-wins rule."
- "A direct identical final override makes propagation unnecessary; a conflict refuses."

An inventory successor carries every row by value, so an inventory's raw description bytes never change. A row's effective description is the `after` of a contract successor's passage override. When a later inventory is selected, verify_design projects that override by stable file path onto the selected inventory, and the lock pins the projection in `inventoryPassageInheritance` (16 rows at product 96ca141: 468a's eight and 461b's eight).

So nothing lawful can change a description once it has been given a meaning:
- **A direct override on the selected inventory** has `before` equal to the raw bytes. It differs from the projection, so it refuses ("inherited inventory meaning conflicts with direct override").
- **An override with `before` equal to the effective text** refuses earlier, because an override's `before` must equal its parent's raw passage.
- **A second override on the original parent** refuses ("conflicting contract passage overrides").
- **An inventory successor that rewrites the row** refuses ("changed or removed an inherited row").

The same holds for a direct override that is not yet projected, such as D1's 39 rows on inventory119. The four rows D1 deferred are `read_premise.rs`, `installation_session.rs`, `store_lineage.rs` and `initial_installation.rs`. Their meanings come from 461b (on inventory80) and 468a (on inventory74), and they are stale. They cannot be refreshed. `stale-descriptions-x1b/probe.py` shows each route refusing.

## Rule

1. **An explicit supersession (lead decision).** A contract successor record may carry `passageSupersessions`, a list. When it is absent, the list is empty. Each entry has exactly these fields:
   - `parent`, `selector`, `before`, `after`, with the same meaning as a passage override;
   - `supersedes`, which has exactly `record`, `parent` and `selector`. `record` is the exact pin of an earlier contract successor's record. `parent` and `selector` name one entry in that record, either a passage override or a passage supersession.

   A supersession replaces exactly the meaning it names, and nothing else. It is reviewed and assented to as part of its contract successor. It needs the same `ACCEPT-DESIGN-UNIT` review and root assent as any other content of that successor.
2. **Checks.** verify_design refuses a supersession unless every one of these holds:
   1. **Shape.** Its fields are closed. Its `parent` is one of its record's accepted parents, and that parent is an inventory in the lock's inventory chain (the base input inventory or any inventory successor candidate). Its selector is `/files/N/description`, and the selector resolves. `after` is a non-empty string different from `before`. No two overrides or supersessions in one record share a parent and selector.
   2. **Named target.** `supersedes.record` equals the record pin of a contract successor that comes strictly earlier in `contractSuccessors`. That record contains an entry with exactly `supersedes.parent` and `supersedes.selector`. That entry is itself an inventory row description passage on an inventory in the chain.
   3. **Same row.** The supersession and its target select the same file path, and the row is equal by value in both parents. The supersession's parent is not earlier in the inventory chain than the target's parent.
   4. **Chain.** `before` equals the target's `after`, byte for byte. A supersession never matches against raw inventory bytes.
   5. **Linear.** For each file path, the supersessions in lock order form one chain. The first names an ordinary passage override, which is the row's root. Each later one names the supersession immediately before it for that path. Anything else refuses as a double supersession. That covers a second supersession of the same meaning, a supersession of a meaning that has already been superseded, a supersession through an identical copy of the root, and two supersessions of one row in one record.
   6. **No restatement.** Once a row has a supersession, an ordinary passage override of that row in the same or a later record refuses. That is true even if the override is identical to the root.
3. **Effective meaning.** A row's effective description is its root's `after`, superseded in chain order.
   - **On the selected inventory.** A supersession whose parent is the selected inventory is not projected, just as a direct override is not. Its `before` must equal the row's current effective text: the inheritance entry's `after` (or the direct root's `after`), carried through any earlier supersessions.
   - **On an ancestor.** A supersession whose parent is an ancestor inventory is projected by stable file path. It folds into the row's single `inventoryPassageInheritance` entry. The entry's `before` stays the selected inventory's raw passage, and its `after` becomes the supersession's `after`. The fold requires the entry's current `after` to equal the supersession's `before`. If the row's root projection was suppressed by an identical direct override on the selected inventory, so that the row has no inheritance entry, an ancestor supersession refuses.
   - **The lock's shape.** The lock's schema version, entry fields and canonical order are unchanged. A stale lock entry, one that still shows the superseded `after`, refuses ("differs from reviewed ancestor meaning").
4. **Everything else unchanged (lead decision).**
   - Every existing refusal stands and is not weakened. These still refuse: an ordinary override whose `before` is not the parent's raw passage; a conflicting direct override of an inherited row; a conflicting override on the original parent; differing ancestor meanings for one file; an inventory successor that changes a row; an omitted, stale, extra or misordered inheritance entry.
   - Supersession is limited to inventory row descriptions, which is the only kind binding v4 projects. Any other passage, base contract text included, keeps binding v4's rule unchanged: a different meaning refuses.
   - A version 1 to 3 lock has no contract chain. A record in it that carries a supersession refuses.
5. **Standing.** A supersession changes which reviewed sentence describes a file. It never changes inventory bytes, package edges, roles or ownership, and it never grants runtime trust. verify_design still executes no generator or product code.
6. **Units after the law (lead decision).**
   - **VD1-a.** The `tools/verify_design.py` change and its tests in `tools/tests/test_design_binding.py`. No other product file changes, and no inventory successor is needed: both paths exist, and their v119 descriptions stay true. The real lock verifies unchanged, with 16 inheritance rows and no supersession.
   - **D2.** This is a named follow-up, not part of VD1. It is a description-only contract successor with four supersessions:
     - `read_premise.rs` and `installation_session.rs`, naming 461b's overrides;
     - `store_lineage.rs` and `initial_installation.rs`, naming 468a's overrides.

     Each `before` is the current inheritance `after`. Each new text is written against the product at D2's head. It is built on whatever inventory the lock selects at that time. Inventory122 is in review now and would carry D1's projection to 55 rows. D2 is reviewed as its own subject, because the review shape allows one `subjectManifestSha256` per unit.
     - **Binding order.** D2 may be bound only after VD1-a is in the product. The verify_design at 96ca141 ignores a record field it does not know. A supersession bound before VD1-a would therefore pass without being checked at all; the probe shows a stale `before` passing there. D2's scratch check asserts `inventoryPassageSupersessions` equals 4, and that result field exists only from VD1-a on.
   - **The next inventory successor after D2.** Its projection helper folds D2's supersessions, as rule 3 says. When the helper carries the supersession onto its new candidate, its `effectiveDescription` is the chain's last `after`.

## Rejected alternatives

- **Last writer wins.** A later contract's override would silently replace an earlier meaning. Binding v4 forbids this, and it lets a stale `before` rebind unseen.
- **An override whose `before` may match either the raw bytes or the effective text.** Which meaning it replaces would be ambiguous. A stale effective text would still attach to the row, and a raw-text match would silently start a second root.
- **An implicit chain, matching `before` against the effective text without naming the target.** It is workable, but the reviewed record would not say which accepted meaning it ends. A stale pin should refuse at the named target, not be inferred. The explicit `supersedes` makes double supersession a structural check.
- **Rewriting the row in an inventory successor.** This breaks the additive, equal-by-value profile. It also makes every historical override's `before` mismatch its projected row.
- **Editing or withdrawing the accepted overrides.** Accepted records are immutable reviewed bytes.
- **A supersession list in the lock.** The lock pins reviewed content; it does not author it. A meaning change belongs in a reviewed contract successor.
- **Keeping one inheritance entry per chain link.** This needs several entries per selector. That changes the lock's uniqueness rule and every projection helper. Folding keeps one entry per passage, and `before` stays the raw bytes that the existing helpers already assert.
- **Doing D2 inside VD1.** One review cannot pin two verify_design subjects. D2's text must also be checked against current code, on the inventory selected after inventory122.

## Not claimed

No product behavior, release gate or runtime trust changes. The descriptions themselves are D2's.
