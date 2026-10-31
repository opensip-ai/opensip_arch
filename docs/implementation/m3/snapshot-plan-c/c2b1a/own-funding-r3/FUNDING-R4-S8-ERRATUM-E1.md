# FUNDING-DERIVATION-r4 §8, erratum E-1: the census's implementation-work component (R3 author, 2026-10-30)

Status: **PROPOSED.** It needs independent R3 review (the C2b-1a own-funding reviewer, OF-R1-5) and adoption by the
coordinator under OD-AUTO-1's R3-reviewed law calls. It is **additive**:
- the accepted r4 bytes stay frozen
  (`../funding-r3/FUNDING-DERIVATION-r4.md`, sha256 `42c24428e382bdb434fe8fd2b62baa5a41e29bb8b7ff4a0d7ad8b82d1d8feec7`);
- no evaluator term, no §6 column, no §7.1 baseline vector, no cap, nothing in M1a and nothing in BOUND-1 changes.

## E-1.1 Why

FUNDING-r4 §8 defines the census's measured boundary and charges it by its element table. Three of its statements do
not describe the Rust implementation exactly:
- it says that work inside the boundary is counted where it runs;
- it says "no relational operator on key strings runs inside the boundary";
- it publishes the per-record census aggregate as the sum of the census debits.

The Rust census (`typescript_context_price.rs` at d6cc6e4) also does the following inside the boundary, uncounted and
uncharged (own-funding audit AUD-9; REVIEW-r1 OF-R1-5):
- equality tests of member names against static literals: `Tables::arm`'s 9 arm names; `sourceInventory`, `tree`,
  `blobs` and `stages`; `path` and `logicalPath`;
- `p_array`'s growth-step loop, with at most bitlen(n) + 1 iterations;
- `integer_length`'s digit loop, at most 19 iterations over the admitted `JsonInteger` range
  [−2⁶³, 2⁶⁴ − 1];
- a `chars().count()` over static ASCII field names in `order_item`.

The reference model does the equivalent work as dictionary or set operations, which it also does not count.

## E-1.2 The amendment (added after §8's element table)

**The census debit has two components.**

**(B) The baseline component.** It is exactly §8's element table, unchanged: the node, member, item, retained-length
and record charges. Its per-record sum is the model-equal value that §7.1 publishes and F5/F6 hold equal to
`admission_model.py`.

**(I) The implementation component.** It is a set of *implementation events*, each debited inside the boundary before
its work, from sizes available in O(1):

| event | where | debit | covers | bound proof |
| --- | --- | --- | --- | --- |
| I-ARRAY | every array node, before `p_array(n)` | {0, bitlen(n) + 1, 0} | the growth-step loop | capacities 4, 8, …, up to ≥ n: ≤ bitlen(n) + 1 iterations |
| I-NAME | every array node of an `identity` record, before its name classification, which is **computed once per array node** (the arm search, the class `sourceInventory\|tree\|blobs` and `stages`, each used for every item, both `stages` uses included) | {0, 13, 272} | 9 arm-name equalities and 4 class equalities | 9 + 4 = 13 tests; each equality reads ≤ \|literal\| bytes of each operand, plus the length test: 2·(93 + 9) + 2·(16 + 5 + 6 + 7) = 272 |
| I-KEY | every object member, before its key literal tests | {0, 3, 44} | `k == "path"`, `k == "logicalPath"`, and `k == "path"` once more | 2·(5 + 12 + 5) = 44 |
| I-INT | every integer node, before `integer_length` | {0, 20, 0} | the digit loop | ≤ 19 iterations |

- **Static name lengths** are read as `len()`. `order_item`'s `f.chars().count()` becomes `f.len()`, so no event is
  needed for it. Its premise (every `Fields` name is ASCII) is held by a control.
- **The ledger debit** of each record's census is **(B) + (I)**. §7.1's published figures remain (B). The census
  charge in the whole call, per §8's last paragraph, is the sum of the actual debits, now (B) + (I).
- **The sentence "no relational operator on key strings runs inside the boundary"** is replaced, for the census only,
  by this: *no relational operator on key strings runs inside the boundary except the I-NAME and I-KEY literal
  equality tests, each counted and charged as above. The declared-key search remains one counted three-way comparison
  per iteration.* The observer (`observe_keys`) still shows zero relational operations **on the wrapped static
  declared keys**. It is not evidence for the I-NAME and I-KEY tests, which have their own observation (E-1.3).
- **The accepted closed forms are unchanged.** An invocation's own cost (`inv_cost`, `member_cost`, `matched`,
  `order_item`'s closed form, `tuple_key`, `path_check`) is still one counted step. It is bounded by its static table
  entry, as §8 states, and this erratum does not reopen it. The (I) events cover only the implementation work listed
  above.

## E-1.3 Observation and controls (F6, extended)

- **Counting.** Each (I) event opens an element of kind `own:<event>`. F6(b)'s history records it, so the exhaustion
  budgets stay exact. Each literal test, loop iteration and digit step inside it counts a `c.step` with the bytes it
  actually examined, computed as `compare_keys` computes them. Counted ≤ charged holds **per element**, (I) elements
  included, and in total.
- **Reconciliation.** On every F5/F6 record and malformed vector: the actual ledger debit of the census equals
  (B) + (I). (B) equals the model's census charge. (I) equals the sum of the events actually reached:
  - I-ARRAY: Σ over array nodes of (bitlen(n) + 1);
  - I-NAME: 13 per identity array node;
  - I-KEY: 3 per member;
  - I-INT: 20 per integer node.
- **Exhaustion, for each event class.** With a budget of exactly the work charged before the first event of that class,
  the census refuses at that event, and its work has not begun:
  - I-ARRAY: no `p_array` step;
  - I-NAME: the arm-search counter is unchanged;
  - I-KEY: the key-test counter is unchanged;
  - I-INT: the digit counter is unchanged.
- **Mutations:**
  - **M-remove**, for each class: caught by per-element counted > charged;
  - **M-move**, for each class (the debit after the work): caught by the exhaustion probe;
  - **M-extra** (an additional per-item name test that is not hoisted): caught by counted > charged on an identity
    array of ≥ 2 items.
- **The ASCII premise control:** for every `Fields` entry and every static string the census or the terms read with
  `len()`, `chars().count() == len()`.

## E-1.4 Non-effects

- No change to: any evaluator price; FUNDING §3–§7 and §9–§12; SLOT-r4; the §7.1 baseline values; F2's tables;
  `admission_model.py`'s (B) computation; M1a; BOUND-1; or any cap.
- The (I) events are inline event envelopes in code the unit owns and meters (BOUND-1 §2 and §3.1). Each is one
  primitive test or one bounded loop, with no other charge between it and its work.
