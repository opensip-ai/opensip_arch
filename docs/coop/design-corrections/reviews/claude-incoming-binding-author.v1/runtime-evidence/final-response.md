I fixed both issues and the checks pass. MUST-34-01 was a real design defect: incoming answered a certain negative even though the subject's own program had never been searched. A-12's wording is corrected. While checking A-12 I also found and fixed a gap the review missed.

## MUST-34-01 — accepted and fixed

**Cause.** The incoming loop only visits programs that have an available binding. If the subject's own universe *U* has none, *U→U* is never checked. On frozen34 that gave `none`/`count-at-most 0`/`all-covered` = `true` and `exists` = `false` in four cases: *U* unbound with a same-family *U2* fully evidenced, and three foreign-family-only cases (available only, unavailable only, both).

**New rule (contract §4, incoming step I1).**
- **When:** the endpoint is `target`, P2 did not return, and no available owed binding has `universe = U`. This is the same test as outgoing step 1.
- **What it emits:** `selector-unbound` with a null universe, the same record outgoing already uses. No new cause token, field or schema.
- **Effect:** completeness becomes unknown, but evaluation does not stop. Every other program is still accounted and keeps its causes.
- **Known facts are kept:** `exists`, `none` and an exceeded `count-at-most` keep their results. Only answers that need completeness become unknown.
- **Other cases:** an unavailable binding never satisfies the rule, so its cause is kept alongside. Foreign-family-only inputs are unknown, with both cross-family disclosures kept. A narrowed request narrows the work done, not what a negative must have searched.

**Old versus new (atom API, synthetic inputs):**
- 24 incoming cells changed: 16 went from negative to unknown, and 8 were already unknown and just gained the cause. No outgoing cell changed.
- P2 and every case where *U* is bound are unchanged.
- With two known facts: `none`, `exists` and `count≤1` are unchanged; `count≤2` and `all-covered` go from `true` to unknown.
- The multi-provider cases give one result across all insertion orders.

**Reachability.** I found no admission rule that makes this impossible, but I haven't shown it's reachable either. The request and the enumeration cell check work per unit, and nothing I read requires every unit to be requested for every capability. I did not run enumeration admission or build a retained Run. For the default profile I read the reviewer's q11 and did not rerun it.

## A-12 — accepted, plus one finding

1. **Provider group with no scopes.** The wording now matches what's admitted. An attestation for such a group is always a global `INCOMING_SEARCH_SCHEMA` refusal. The only lawful way to close an empty program is an explicit scope with no subjects, plus complete Coverage or an attestation. No code change; both models behave the same.
2. **Scope without `enumeratorClosure`.** The reviewer is right that the native carrier refuses both a missing and a null key. At the atom API, though, frozen34 only refused null. A scope with the key missing skipped validation and could produce `none=true`, including through an attestation that names it. `_scope_descriptor` now passes fields through so a missing key is refused like null, both during evaluation and during global attestation admission. This tightens admission to match the owning schema; nothing was loosened.

## Changed files, checks and handoff

| File | frozen34 → successor | Lines |
|---|---|---|
| `atom-evaluation-contract.v1.md` | `d7ef1336…` → `7ee61c18…` | +61/−4 |
| `atom_model.v1.py` | `a5e082a5…` → `c1243ca9…` | +21/−19 |
| `check-atoms.v1.py` | `c5de4a84…` → `258099be…` | +312/−1 |

- **Checks:** 89/89 pass. The original 81 are kept and passed before the new cases existed, and no old expected result changed.
- **Old fixture edit:** I changed one fixture value: `dynamic-import` → `dynamic-import-nonliteral`, because the old value isn't a valid enum member. The expected result is unchanged.
- **New checks:** 6 of the 8 fail on frozen34 and pass on the successor. The other 2 pin behaviour that shouldn't change.
- **Downstream checkers:** the 7 checkers that import the atom model exit 0 on both trees with identical output. That shows nothing regressed; it doesn't show they reach the new rule.
- **Not run:** closed enumeration admission, retained Runs, the six broad groups, and pin validation.
- **Custody:** frozen34 has no drift, and exactly these three files differ in the successor tree.

**Still open:**
- **Reachability:** MUST-34-01 is still undemonstrated beyond synthetic inputs and schema checks.
- **Unknown-family cases:** only tested with an input shape the plan schema itself refuses.
- **Unvalidated scopes:** a scope missing `enumeratorClosure` that nothing names or uses still isn't validated, though it can't affect any result.

**For root:**
- **Pins:** 15 pin rows are stale. No file was added, so no new pin is needed.
- **Schema wording:** `incoming-search.schema.v1.json` still says "untagged scopes fall back to all S scopes". That describes no admitted input and should be dropped by its owner; it isn't one of my files.
- **Your preparation runtime:** three files in `root-source35-preparation.v1` changed after I started. Nothing here touched or read them.

Two probe bugs of mine are kept in the receipts. One made a false "order-dependent" result, which I reran. I had also expected global admission not to validate named scopes; the P6 probe showed it does, so I dropped that claim. Nothing here is acceptance or qualification of any kind.

Files are in `/tmp/opensip-design-corrections/claude-incoming-binding-author.v1/`:
- review.md
- review.json
