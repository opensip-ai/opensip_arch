# M3-E1 r3 review

**Verdict: ACCEPT.** E-R2-01, E-R2-02 and E-R2-03 are resolved. No required finding remains. Three non-blocking observations concern control wording and citation/checklist metadata.

Subject: `docs/implementation/m3/syntax-e/PROPOSAL.md`, 117,273 bytes, sha256 `d71031ff1aee01ba20b471e9db1891f4a0e976751741ffa10a783585eedd7c46`. All 35 requested pins match live bytes. The product is clean at `3e64266aa8729160cd22509dcfff95a3bb09fcea`. Line references use these exact r3 bytes.

## Resolution and assessment

| Finding | Resolution | Evidence |
|---|---|---|
| E-R2-01 | Resolved | Items 11/14a at 429–430 and 524–551; E3-T9 at 560–563; EXS sourceBodies cap and EXC §6; retention models in static-analysis.json. |
| E-R2-02 | Resolved | Item 4 at 189–215; A3/A6 at 245/248; retained Run-closure joins at 261–263; E2-T33–T36 at 283–286; SYN-NS at 693; IE:1068–1089 and IDS normalizationSpecificationLaw. |
| E-R2-03 | Resolved | SYN-1/SYN-1F at 689–690; E2s and its two controls at 709; complete selector census and generation registry comparison in static-analysis.json. |

**Body-union bound.** The retained carrier now stays within 100,000 source-body rows. Oversized groups are withheld first. Remaining groups are ordered by their raw canonical group digest, and one longest prefix is retained within both limits. No component is cut, no retained member loses custody, and any withholding makes the envelope partial. Budget exhaustion yields budget-exhausted/null unless unsupported language or input-closure-incomplete has higher precedence. No withholding can produce an empty complete result.

The union model retains all 25 groups and 100,000 ids at the exact boundary. Growing the smaller group to 1,697 ids gives 100,001 proposed ids, of which the digest-ordered prefix retains 24 groups and 98,304 custody rows, with partial/budget-exhausted/null. A reduced arithmetic example proves that once a valid group breaks the union bound, later groups are withheld even if they would fit individually. Twenty-four production-order permutations give the same retained prefix. Existing whole-file snapshot custody and the Plan census, universe, producer, stage, and required-cell joins remain unchanged. Other table rows retain the r2 behavior: syntax-error and truncation withhold files, unsupported census paths stay disclosed, backend faults/cancellation retain no envelope, and a successful empty result retains the exact census.

**Normalization closure.** The fixed canonical IE map is now a second root alongside the manifest. A3 bounds and admits it. A6 joins normalizerId, exactly four ascending level rows, their fixed paths, tree digest/length and retained-byte hashes. The native normalizer stays a distinct manifest member with its native admission meaning. Every member must be reachable from either root, so unrelated members still refuse. Both T-wasm and T-native carry the same normalization retention law. IE's Run-closure checks are preserved; the new pre-Plan checks complement them. The positive complete-closure control and missing map, missing/wrong/mismatched level and extra-file controls cover both branches.

**Cause selectors.** The live census exactly matches SYN-1F's five foundation enum selectors and E2s's 13 product selectors: five schema enum copies, the native input-closure-incomplete allowedCauses row, and seven evaluator-registry lists. No additional matching list appeared in the scanned product schema sources or evaluator registries. The eight declared output paths equal the closed generation registry's outputs. Regeneration and byte verification remain future E2s work.

The startup schema contains no NativeCause copy. Its TypeScript post-Analyze lists remain the existing reason vocabulary; Coverage references the native owner. Native UnavailableReasonV3 remains separate and unchanged. E2s-T1 checks the exact mirror changes and unchanged reason lists. E2s-T2 requires source-parse-error to be admitted on its lawful input-closure-incomplete Coverage/candidate pair and refused under other deficiencies and as a TypeScript Unavailable reason.

**Regression and schedule.** The diff preserves the ordered A1–A12 chain, SymbolTableV1, static pre-Plan refusals versus execution faults, whole-registry selection, both backend branches, X-C1/X-C2 and the producer/census ownership assessed in r2. E3 waits for the accepted H interface rather than integrated H. The arithmetic model retains E2b/E2c/E3 at days 5/8/14, H at 22, J2 at 25 and 14 days of E3 slack. E2s by day 12, K2 by 28, selected O2 by 31 and the lead set by 22 preserve the conditional day-33 host chain. Second-integrator acceptance continues to own final wiring and end-to-end controls. E-N1 to E-N5 remain resolved or preserved.

## Non-blocking observations

**E-R3-NB-01 — E3-T9, lines 560–563.** Change “add one member to any group” to growing the 1,696-member group to 1,697. The other 24 groups are already at 4,096; growing one of them first hits the per-group bound and does not isolate the new body-union limit. Also document that the million-group bound is dominated by 100,000 body ids for disjoint components. Separate reduced-cap arithmetic/fixture branch coverage can be labelled as such. The operative retention rule is sound.

**E-R3-NB-02 — SYN-1(d), line 689.** Add -normalization-map-mismatch to the explicit new-key list. A3/A6 already define it, and item 5 line 239 plus SYN-1's universal prefix rule already give its pre-Plan route; the explicit successor checklist simply omitted the new name.

**E-R3-NB-03 — C citation basis, line 37, line 49 and item 14b at 577–585.** Some C: references still use later-file coordinates despite the new fixed-r3 short name. The pinned C r3 import-role restrictions are at 353–355 and C2-T13 at 379; current r5 has them at 411–413 and 437. The short-name live r5 digest prefix 7f76052d also differs from the actual request/live pin 431a498c. Align the references and distinguish accepted subject bytes from any later wrapper changes. The actual provisions are unchanged, and X-C1/X-C2 remain explicitly gated on C's next revision, so this does not alter the assessment.

## Scope and evidence

This is acceptance of the pinned M3-E1 successor law only. It does not accept product code, inventory bytes, confinement, performance or a verify_design recording unit. SYN-1, SYN-1F and SYN-NS require their own ACCEPT-DESIGN-UNIT reviews; X-C1/X-C2 require C's next revision; E2a/E2s/E2b/E2c/E3 require their own ACCEPT-UNIT inventory reviews. This review has no inventoryCandidateAssessment.

Evidence consists of exact pins, the retained subject and diff, the prior findings, and read-only JSON/selector/digest/reachability/cardinality/schedule models over 91 supplemental inputs. The models do not execute product or owner code and do not constitute implementation tests. No new upstream source was fetched or built; actual immutable upstream selection remains E2a/SYN-DEP work.

All new files were written only under this r3 review directory. No repository edit, commit, push, delegation, product build, Cargo command, test run, real OpenSIP-home access, or 413-fixture access occurred. Scratch scripts used Python 3.14.6 with -I -B, nice -n 19, and a private 0700 TMPDIR under the review directory.
