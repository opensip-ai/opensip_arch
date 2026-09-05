# Independent review — section31-supplier-coverage.v4

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**TWO-PART FROZEN SUBJECT:**
- `docs/coop/artifacts/section31-supplier-coverage.v4.json`
- `docs/coop/artifacts/check-section31-supplier-coverage-v4.py`

Measure both sha256 at start and end. Do not edit either. Do not commit.
Expected at dispatch:
- instrument `97727684af2d812d3a677add9b15287db81d6fe36aeaa96d72d5118890a847f6`
- checker `a30928260e9ddd36c680a13925d40353c362151f8729b99b021d400b5c2f96c2`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/section31-supplier-coverage.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/section31-supplier-coverage.v4.review-independent.codex.json`

Do not read the other reviewer's files.

Successor to v3 (both ACCEPT-WITH-ADVISORIES, 0 blockers).
This fold is honesty work. It is not Phase-1A. It is not SATISFIED
evidence. Bound remains 1, unbound remains 7.

Named predecessor repairs to verify by execution, not trust:

| ID | Claimed repair |
|---|---|
| S31V3-01 | BOUND item with no supplier key is a typed FAIL, not KeyError |
| S31V3-02 | `doesNotFailWhen` records that PASS is not semantic completeness of a bound head |
| S31V3-CX-A1 | predecessor Codex verdict token is the exact uppercase `ACCEPT-WITH-ADVISORIES` |

Attack:
- silent SATISFIED or Phase-1A insertion
- treats bound=1 / unbound=7 as complete coverage
- treats item 1 as BOUND
- S31V3-01 still KeyError
- S31V3-02 omitted
- S31V3-CX-A1 still lowercase
- checker PASS used as semantic completeness
- file 08 / freeze / COORD edited

Verdict vocabulary: ACCEPT / ACCEPT-WITH-ADVISORIES / REJECT.
Blockers are MUST-FIX. Advisories are not blockers.
Final chat: short summary plus verdict word.
