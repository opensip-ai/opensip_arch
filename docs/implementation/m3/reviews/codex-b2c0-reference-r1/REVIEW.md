# B2-C0-REFERENCE-r1 review

Verdict: **REQUIRED-FINDINGS**

One required finding blocks acceptance. No non-blocking observations.

## Exact subject and checks

Rehashed the 1131-byte manifest, SHA-256 `e60e6c811f21a99c9a40f2b27bd4a61efd22a96433ebee7ca8b15bf30b36aed1`, and all five members. Every byte count and digest matches. The successor record is 4831 bytes, SHA-256 `7f2e1202410a848809a2c79566b60c06f707eccbfb78ac43cec4dda880f18f13`.

Confirmed clean product main `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5` and architecture HEAD `7c55cdab1bd1c24144e2222496296e10a54dde34`. Read the wrapper, checker, record, support script and scratch-verification summary, and the relevant selected model/shared-rule/B-S1/NE behavior.

Ran the expressly permitted staged checker, directing its result to this directory's review.json before replacing it with the final review. Its parsed result equals the staged checks.json exactly: 26 historical and 26 current cases pass; seven explained differences; all four member-control rows and the current P3 join pass; all five mutations are caught. Imported the reference read-only for additional synthetic probes. No actual repository tree or held-out entry was used as a fixture.

## B2C0REF-R1-RF-1 — Honor every admitted boundary in the new checks

`native_unit_reference.py:167–199` implements both new boundary decisions with `rule.classify_boundary`, passing only nestedRepositories and nestedProjects. The selected native model's `_boundary_hit` also invokes `classify_custody_exclusion`. Its directory-custody and DEPTH rows exclude a directory and everything below it; marker-custody rows exclude exactly one marker. These distinctions are already part of the selected law.

Consequently the wrapper applies its new member check and LD-B2C0-1 filter inconsistently with B-S1's “not at or below an admitted boundary” condition and its own proposed “outside every admitted boundary” passage.

Two synthetic probes reproduce the problem. Each inventory first passes current V3 admission, uses selectedRoot `/h/w`, has empty members/repository/project lists and has `custodyExcludedUnits = [{path: "blocked", reason: "DIRECTORY_CUSTODY:ACL_UNREADABLE"}]`:

1. With a root package.json marker, a `blocked/node_modules/x/package.json` marker and no admitted pruned rows, discovery incorrectly returns `native.boundary-inventory-mismatch` with `missingAnchors = [{path: "blocked/node_modules", reason: "dependency-tree"}]`. Under the proposed passage that anchor is below an admitted directory boundary and must not be compared.
2. With only the root package marker and an admitted `blocked/.git` vcs-tree row, discovery incorrectly returns `native.boundary-inventory-mismatch`, `reason: "member-not-admitted"`. B-S1 requires no member for a vcs-tree parent already below an admitted boundary.

The selected model confirms `_boundary_hit("blocked", inventory) == ("blocked", "custody-excluded")`. These refusals are therefore not merely different labels for the same accepted boundary behavior. A product implemented against this oracle would inherit false refusals of excluded content. The supplied cases exercise nested repository/project boundaries but do not expose this combination.

**Required correction:** apply the full selected boundary predicate in both new checks, including directory custody and DEPTH, while preserving marker-only exclusions. For the anchor-derivation filter, classify the derived pruned anchor's location as the passage specifies. Add regressions for both directory-custody and depth exclusions, carried and derived anchors, and a marker-only exclusion that must not exempt unrelated anchors. Keep controls proving a missing or re-reasoned anchor outside all boundaries still refuses.

## Other conclusions

The loading strategy preserves the selected model bytes and pins its model/import closure. Relocating __file__ supplies the historical sibling layout; separate historical/current module objects and the documented rule, V3-admission, output-validation and member-field substitutions are appropriate in principle. The merged bundle adds B-S1 definitions without replacing base definitions. The current successful output is validated as UnitDiscoveryV3 and retains memberRepositories. RF-1 concerns the new semantics around those substitutions, not their basic need.

The P3 conflict is real: the current walker never enters nested repositories/projects, while native marker-derived anchors could demand observations inside them. A narrow passage override exempting anchors below admitted boundaries is a reasonable design resolution. The changed case's original inside-boundary anchor now admits, while its current outside-boundary variant preserves the foreign-inventory refusal; its invalid caller-ignores step remains checked. The six other expectation differences are SX-1 scope-prefix additions. The current two-sided P3 sweep is useful and passes, but the boundary coverage is insufficient until RF-1 is resolved. Thus ld1ConflictRealAndResolutionSound is false for this frozen implementation even though the conflict and proposed principle are sound.

All 13 parent byte pins match and are sorted. Candidate pins exactly cover the four subject members other than the record itself. The sole override's before text equals NE line 838 exactly, names a declared parent and has no earlier exact-selector restatement in the 165-contract chain. Read-only comparison with contract_successor's rules supports the proposed record shape. The supplied scratch evidence reports base and synthetic-successor-166 verification passing; it uses synthetic acceptance/assent and is not actual independent acceptance. No verifier was executed by this reviewer. The record can be reconsidered for ordinal 166 after the finding is fixed and reviewed; this subject cannot be bound with this REQUIRED-FINDINGS verdict.

## Boundaries

Final outputs are only REVIEW.md and review.json in the requested directory. No repository, stage or control files were edited. No Cargo, tests outside the expressly allowed checker, builds, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was read. No product change or qualification is granted.
