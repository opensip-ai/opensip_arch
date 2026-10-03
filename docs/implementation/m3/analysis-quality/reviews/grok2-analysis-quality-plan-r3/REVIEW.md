# GROK2 fact review — M3 analysis-quality plan r3

Verdict: **REQUIRED-FINDINGS**.

Subject: `docs/implementation/m3/analysis-quality/PLAN.md`, 62339 bytes, sha256 `8f5b3547322940f2ad3003ddda95a9245591644330fee98e70fc07648c14c2b9`. That matches the request pin. The previous subject is `PLAN-r2.md`, sha256 `dd351ffe79b59f920b91da6372c7f132c1e9e69ea20bf1fd280b942f1d1936ed`. Read-only. No product code was run. `~/Library/Application Support/OpenSIP` was absent.

The diff against `PLAN-r2.md` is the title, the new r3 response table, and four body edits: the §4.3 confidence rule, the §5.1 RSS sentence, and INC-1, INC-4, INC-6 and INC-8. Nothing else in the body changed.

## r2 findings

All three are resolved.

| ID | Resolved | Where |
|---|---|---|
| RF-1 | yes | PLAN:326. The run records the concurrent summed high-water and the sum of per-process high-water counters, and the budget uses the larger. LQM:925 is that method. AQC:142-145 is the high-water resident sum for the same preview workload. The plan no longer says a sum of peaks is excluded. |
| RF-2 | yes | PLAN:367 and PLAN:379. `scope2` and `fact2` bind the snapshot (IE:183-184). `coverage2` binds the scope (IE:185). `view2` binds the Plan (IE:186). New source creates a new Plan and Run (IE:1605-1606). IE:1586-1592 is now cited only for complete replay on cache admission, which is what those lines say. INC-4 compares semantic payloads and correspondence on one new snapshot, and it does not compare snapshot- or Plan-bound identities across different Plans. |
| RF-3 | yes | PLAN:383. The single writer is the lifecycle lease (IE:1657-1660). The grant is named `RepoExecutionGrantV2`. NE:1273 and NE:1311 say the operational reference stays outside the Plan. |

## New finding

### RF-1 — The r3 table says §2 Q2 changed, and §2 still states the rule §4.3 withdrew

PLAN:50 says C2-AQ-R2-01 changed §2 Q2 and §4.3: the exact Clopper–Pearson bound applies only to established independent samples, 299 and 29 are examples, and a clustered stratum uses a preregistered cluster-aware bound or is INSUFFICIENT-EVIDENCE.

The diff does not touch §2. PLAN:137 still says the Q2 target is the one-sided 95% exact lower bound per rule × language × mode. PLAN:145 still says 0.99 needs about 299 independent error-free gating findings per stratum, and it points that sentence at §4.3. PLAN:230-234 now says the opposite about when that exact bound governs and what 299 and 29 are.

Those two sections are both acceptance text. A reader of the definition table still implements the unqualified exact bound.

**Fix.** Make PLAN:137 and PLAN:145 say the same primary rule as PLAN:230-234. The exact bound is for a stratum whose findings are established independent samples. 299 and 29 stay examples for that case. A correlated stratum uses the preregistered cluster-aware bound, or it is INSUFFICIENT-EVIDENCE.

## Citations checked

| Citation | What r3 uses it for | Result |
|---|---|---|
| IE:183-186 | scope and fact bind the snapshot, Coverage binds the scope, view binds the Plan | Matches the domain table. |
| IE:1605-1606 | new source creates a new Plan and Run | The sentence is there. It does not itself mention a snapshot. The following "so" clause is the plan's inference from a new Run, not a second claim in those lines. |
| IE:1586-1592 | cache admission against an authoritative Run requires complete replay | Matches. |
| IE:467 | `RepoExecutionGrantV2` lives outside the Plan | Does not say that. It is the `owner-retained` row for the grant's owner file-manifest admission. |
| IE:1387 | same | Does not say that. It is the semantic-grant digest of the grant's owner projection. `plan2` includes the semantic grant (IE:182). |
| NE:1273, NE:1311 | the operational grant reference is outside the Plan | Both say that. These carry RF-3. |
| NE:2014 | `CoverageResultV3` has no reuse field | The section starts there. The record at NE:2020-2033 has no reuse field. |
| LQM:925 | budget value is the larger of the two RSS quantities | Matches, including the missing-child NON-PASS rule, which the plan does not restate. |
| operability plan §4.1 | reuse provenance is an operational timing record | That section records phase spans, cache hits and misses, and changed-scope reuse, and it says timing does not touch evidence or identity. |

## Beyond the table

r3 does not change any section the response table does not name. The missing edit is the other way: the table names a §2 Q2 change, and that section is byte-for-byte the r2 text.

## Non-blocking

1. **PLAN:383.** IE:467 and IE:1387 name `RepoExecutionGrantV2` but do not place the operational reference outside the Plan. NE:1273 and NE:1311 do. Dropping the two identity-file citations would leave the claim intact.
2. **PLAN:367.** "So no old Run's replay is evidence for the new snapshot" is not the text of IE:1605-1606. Those lines stop at a new Plan and Run. The inference is consistent with a Run binding its snapshot, and the citation is attached to the Plan/Run clause.
