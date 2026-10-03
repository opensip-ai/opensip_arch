# CODEX2 review: M3 analysis-quality plan r3

**Verdict: ACCEPT.**

Both CODEX2 r2 required findings are resolved at plan level. The changed text introduces no blocking error, and the complete r2-to-r3 diff contains only the declared review fixes, the response table and the revision-title update. Acceptance is of this plan revision, not of any future contract successor, measurement or qualification claim.

Subject: [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:1), 62339 bytes; SHA-256 `8f5b3547322940f2ad3003ddda95a9245591644330fee98e70fc07648c14c2b9`. The preserved r2 snapshot also matches its requested digest.

## Resolution of r2 required findings

### C2-AQ-R2-01: RESOLVED

**Location:** docs/implementation/m3/analysis-quality/PLAN.md:230-235 (§4.3).

One primary obligation now governs precision acceptance. Exact Clopper-Pearson applies only after independence is established; otherwise a preregistered cluster-aware method must meet minimum independent-repository requirements and handle the zero-error boundary without a degenerate pass. Unsupported or insufficient inference cannot pass. The 299/29 counts are explicitly independent-sample examples. A qualified advisory rule must meet 0.90; an interim experiment remains declared unqualified, gains no Q2 pass or automatic waiver, and is recorded under D13 and the selected inventory. This satisfies the requested plan-level correction; fixing the actual clustered method remains an owned pre-measurement harness task.

### C2-AQ-R2-02: RESOLVED

**Location:** docs/implementation/m3/analysis-quality/PLAN.md:367-387 (INC-1/2/4/8).

INC-4 compares current semantic payloads and correspondence for the same new snapshot and semantic input closure, with identity comparisons confined to the appropriate pair and no cross-Plan identity assertion. INC-8 places recomputation/reuse history in an operational record, explicitly excludes it from canonical Coverage, and preserves typed incomplete results where current obligations are not re-established. Fully re-admitted reused work can support complete Coverage. The cited operability §4.1 records reuse in timing/diagnostics without changing evidence or identity. The corrected binding and current-grant citations agree with the replay/cache contracts.

## Required findings

None.

## New citation checks

| Citation | Result | Assessment |
|---|---|---|
| [IE:183-186](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:183) | SUPPORTED | scope2 and fact2 bind the snapshot; coverage2 binds scope/payload/schema; view2 binds Plan. |
| [IE:1605-1606](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1605) | SUPPORTED | New source or policy creates a new Plan/Run; the preceding text forbids replacing the sealed Run. |
| [IE:467](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:467) | SUPPORTED-IN-COMBINATION | Identifies security's RepoExecutionGrantV2 owner admission and owner-retained manifests. Outside-Plan placement is established directly by the accompanying NE citations. |
| [IE:1387](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1387) | SUPPORTED-IN-COMBINATION | Identifies the grant's owner-source projection retained through semantic-grant principals; it does not place the live operational grant inside Plan. |
| [NE:1273](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:1273) | SUPPORTED | executionCapableResolution is a semantic statement, never a host execution grant; operational RepoExecutionGrantV2 is outside Plan. |
| [NE:1311](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:1311) | SUPPORTED | Explicitly keeps the operational grant reference outside Plan. |
| [NE:2014](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2014) | SUPPORTED | The §4.3 ViewEntryV3/CoverageResultV3 definition has semantic examination/resolution fields and no reuse-history member. |
| [LQM:925](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/language-quality-matrix.completed.v2.json:925) | SUPPORTED | Records the maximum observed concurrent RSS sum and the sum of individual high-water counters, with the larger used as the conservative budget value. |
| [operability plan §4.1](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:110) | SUPPORTED | Records cache hits/misses and changed-scope reuse; timing never touches evidence or identity. This is a compatible future operational-record route, not an accepted contract successor. |

The lifecycle single-writer reference at IE:1657-1660 and the unchanged current-closure cache checks at IE:1610-1626 were also read. The updated grant language keeps operational permission separate from semantic input identity.

## Diff scope

All substantive edits map to the five declared r2 findings. The only change outside those fixes and the response table is the mechanical revision-title update. Owner decisions, targets, catalog, corpus selection, Python/platform scope and milestone rows are unchanged.

The six unified-diff hunks contain:

- Revision heading r2 to r3.
- Added r3 changes and review responses table and introductory bookkeeping.
- Section 4.3 confidence, insufficient-evidence/advisory standing and repository-correlation text: C2-AQ-R2-01.
- Section 5.1 RSS budget methodology: GROK2 r2 RF-1.
- INC-1 snapshot/scope/Plan binding citations: GROK2 r2 RF-2.
- INC-4 same-input semantic equivalence and identity comparisons: GROK2 r2 RF-2 and C2-AQ-R2-02.
- INC-6 lifecycle writer versus operational execution grant: GROK2 r2 RF-3.
- INC-8 operational reuse provenance outside semantic Coverage: C2-AQ-R2-02.

## Non-blocking observation

**C2-AQ-R3-N01 — docs/implementation/m3/analysis-quality/PLAN.md:137 (§2 Q2 summary).**

The unchanged summary row still calls the lower bound exact for every stratum, whereas the revised detailed rule conditionally uses exact Clopper-Pearson for independent findings and a preregistered defensible method for correlated findings. The explicit single primary obligation in §4.3 now resolves the operational ambiguity; this remaining summary wording is an editorial synchronization issue.

**Follow-up:** Have the Q2 row say one-sided 95% lower bound under §4.3's confidence rule, reserving exact Clopper-Pearson for the independent case. No new target, owner decision or broad review round is needed.

## Review boundary

Narrow review only. Previously closed r1 findings and owner decisions were not reopened.

Read-only source/diff/hash inspection; no product code, tests, benchmarks, delegation or commits. No access to the runtime OpenSIP home or private 413 UUID fixture. Only REVIEW.md and review.json were written under the requested /tmp directory.

ACCEPT does not approve a contract/schema/gate successor or establish a measurement, implemented capability or qualified release.
