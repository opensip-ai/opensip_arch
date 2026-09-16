# Independent Grok review: reviewer-neutral binding01

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-reviewer-neutral-binding-subject-01`
**Manifest SHA-256:** `6b0e228bd68e25b725e233eafcc9e411379a2d4ec8c9870ea2b808d38efd553f`
**Members:** 15
**Verdict:** **ACCEPT WITHIN STATED TOOL DELTA SCOPE**

This is tool syntax/attribution only. It does **not** approve upcoming source or inventory records, product readiness, or any Grok/Claude review as evidence. Synthetic test fixtures are not actual reviewer approvals. Historical Claude/base application fields stay named as Claude.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not written.

| Check | Result |
| --- | --- |
| Manifest | `6b0e228b…553f` matches declared and adjacent copy |
| Files | 15 listed = 15 walk |
| Parent pins | product `tools/verify_design.py` `1dce4b8a…8948` (28077 B); `test_design_binding.py` and `design-lock.json` byte-identical to product |
| After | frozen hash unchanged |

Delta vs parent verifier: new `reviewer_reference()` and **two** successor-assent call sites (inventory `root review`, contract `contract root review`). Application/completion still uses `actualClaudeApplicationReview` / `independentApplicationReview` (activation) unchanged.

## Reproduction

- Inherited `test_design_binding.py`: **56/56**
- New `test_reviewer_reference.py`: **7/7** methods (21 subcases)
- Live lock with this verifier + frozen/product `design-lock.json` against architecture: **passed**, 46 inputs, 1 inventory successor, 2 contract successors, `productQualification: false`

## Exactly-one-field law

`reviewer_reference` requires exactly one of `actualClaudeReview` or `independentReview` (`key in assent`). Duplicates refuse even when pins are identical. The chosen pin is still joined with `same_reference` to the lock’s reviewed bytes. A field named `grokReview` is not a review pin.

Inventory review join still omits `size=True` (bytes ignored). Contract review join still requires bytes. Independently confirmed; no new pin semantics.

## Independent whole-verifier probes (12/12)

`review/probes/independent_binding.py`:

| Probe | Result |
| --- | --- |
| v4 baseline with legacy Claude successor fields | pass |
| Mixed v4: inventory `independentReview`, contract `actualClaudeReview` | same joins |
| Dual names even when identical | refuse |
| Missing field / unknown `grokReview` | refuse |
| Neutral stale sha256 / cross-subject application review | refuse “different subject” |
| Neutral name + CHANGES-REQUIRED review | refuse “independent inventory acceptance” |
| Inventory `bytes=0` on independentReview | still accepted (unchanged) |
| Contract `bytes=0` | still refused |
| Rename completion `actualClaudeApplicationReview` | still refused |

A model/field name is not an authenticator. The lock pin and reviewed-byte join are.

## Must-fix / should-fix

None in this tool-delta scope.

## Remaining duties

Adopt this verifier only after this review and root assent. New Grok source/inventory assents may then use `independentReview` **once those records exist and are independently reviewed**. This freeze does not create or accept those records.
