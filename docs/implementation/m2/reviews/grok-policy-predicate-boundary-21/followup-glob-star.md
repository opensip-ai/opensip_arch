# Follow-up: v1 `glob_match` vs glob-pattern-contract on literal `*`

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Independent probe of actual `workflows_model.v1.glob_match` (1296–1321) against `glob-pattern-contract.v1.md` (19–21). Original advisory21 and other follow-ups **unchanged**. **Not ACCEPT-DESIGN-UNIT. Not silent new semantics.**
**Original pins:** `advisory.md` 12386 / `55f48b2e…e1c6`; `advisory.json` 3342 / `b0c4dffb…7bb5`.
**Preserved trial list:** `/tmp/opensip-implementation/m2-policy-glob-trial-21/initial-literal-star-law-mismatches.json` (4 rows).
**Probe:** `probes/glob_literal_star.py` — actual helper extracted from v1; normative matcher from the contract text (not the helper); proposed one-line patch only in the probe.

## Defect

Contract: in an ordinary segment, pattern `*` matches **zero or more Unicode scalars**, including a literal `*` (U+002A). `?` is one scalar. Other pattern characters match themselves.

Helper `seg_match` (1303–1304):

```
if i < len(p) and (p[i] == '?' or p[i] == s[j]):
    i += 1; j += 1
elif i < len(p) and p[i] == '*':
    star = i; i += 1; mark = j
```

When the pattern position is wildcard `*` **and** the candidate scalar is also `*`, `p[i] == s[j]` is true **before** the star branch. The wildcard is consumed as a **literal** match of that one `*`, and `star` is never recorded. Later scalars cannot be absorbed.

## Probe (actual helper vs independent normative matcher)

All four preserved rows: helper **False**, law **True**. Additional `*?` vs `*` / `*ab`: same. Fullwidth `＊` (U+FF0A) does **not** hit the equality bug (`'*' != '＊'`), so `*a` vs `＊ba` already matches.

| Pattern | Candidate | Helper | Law |
| --- | --- | --- | --- |
| `*a` | `*ba` | false | true |
| `a*b` | `a*xb` | false | true |
| `**a` (ordinary segment, not `**`) | `**ba` | false | true |
| `*?` | `*ab` | false | true |
| `*?` | `*` | false | true |
| `*` | `*` / `a` / `＊` | true | true |
| `*a` | `a` / `xa` / `＊ba` | true | true |
| contract examples `**/*.ts`, `[ab].ts` | (as specified) | true | true |

## Minimal reference correction (successor, not implement now)

In `seg_match`, **exclude `*` from the literal-equality branch** so the star branch always records backtrack:

```
p[i] == '?' or (p[i] == s[j] and p[i] != '*')
```

Probe patch vs law: **0 mismatches** on the rows above. `?` still matches a candidate `*`. Consecutive pattern stars stay equivalent to one star (star branch). This does **not** change `/` splitting or `**` as a whole-segment token (`ps[pi] == '**'` is unchanged).

Contract line 79 currently says the v1 helper implements the predicate. After a successor, that sentence must be re-checked; today it is **false** for literal `*` candidates.

**Do not** patch product `policy.rs` / glob as if this were already selected. Treat as a **candidate reference correction** needing independent review and a successor of `workflows_model.v1.glob_match` (and the contract’s “reference implements” claim).

## Other follow-ups (already finished, bytes preserved)

- Digits: `followup-predicate-digits.md` 3635 / `879f3356…dea7` — `isdigit`+`int` vs shortest decimal; superscripts uncaught `ValueError`.
- First-kind: `followup-subject-kind.md` 4987 / `fe320451…37b7` — first-kind is selected deterministic law; no policy-admit/program-reject pair; do not silently drop the default.
