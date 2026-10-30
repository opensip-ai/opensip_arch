VERDICT: ACCEPT-UNIT

Unit C2B-M5-INVENTORY-v241-r1. Required findings: none.

Independent Codex review, round 1, 2026-10-29, R1-BALANCED, gpt-6.1-sol/medium. Product main and claude/c2b-m5 are f61b0cbfdb2ff9f6e6606993daa59e00a0e8111e, parent cd40e1df0dd53437c59ef262ceaea3038ecaa6e7; product worktree clean. Architecture remains 6f28e1067242a53d4ffe5522b06e7bd69ebe8a52. Current M5 plan/handoff and routing selection were rechecked; older control progress/checkpoint pins remain historical.

After reading REQUEST.md, ran its route preflight before substantive work:

```text
python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/tools/agent_model_route.py check --provider codex --plan /Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b-m5/review-binding/REQUEST.md
ROUTE-OK R1-BALANCED codex gpt-6.1-sol/medium
```

Only read-only inspection, hashing, Git comparisons, build_v241.py --check, and the unmodified design verifier on the existing lead dry-run candidate were used. No product/architecture/lock edit, commit, push, root assent, build/test, refresh, census or store access occurred. All new scratch is under review-binding/scratch/; only the requested four review artifacts are written under binding/reviews/.

Fifteen request pins match in full. LEAD-LOG.md alone grew from 13046 to 13290 bytes: its first 13046 bytes still hash to the exact requested 893e4e9d09439f2fd9037abb98e377b4fc6a7a5df1dd173ba9628f31b182eb24. The 244-byte appended status entry reports dispatch of this review and coordination; no subject byte changed. The pinned prefix is preserved in scratch/LEAD-LOG-requested-prefix.md. Live log SHA-256 is c6ed52235144651de139248944f55c0611d819811c15703f77c7c2e32799ee41.

## Findings

### B-NBO-1 — The additive inventory and exact subjects are correct

Independently derived git diff --diff-filter=A 17c9cf6 f61b0cb: exactly the 17 candidate additions. The 1439 v240 rows survive byte-independent JSON value comparison without any edit or removal, yielding 1456 sorted unique rows. All 20 package objects, package policy, pending decisions and every non-file field except the expressly permitted standing text remain equal by value. Planned absent rows are retained without converting them into implemented files.

Reviewed every addition against its actual source/header or generated fixture at f61b0cb. Package ownership is opensip-host, opensip-platform or opensip-security as appropriate. Roles match algorithm/service, test or fixture. Only node_modules_layout_vectors.json is generated; the shared admission cases are a handwritten fixture. Descriptions preserve the distinction between library, measurement harness, generated predictions, allocator controls and qualification. The L8b2 row preserves specified production contract versus measurement expectation; neither the ignored M3 population nor a measurement profile claims a new production run.

The candidate and successor in stage/ equal the builder's checked outputs. The successor pins the exact unchanged v240 parent, exact v241 candidate and complete sorted added-file list. The inventory subject contains exactly the candidate and successor pins. review.json binds c9834ab6e168eb2cdadd5b82e83903c260edcb4c558c1157b612d1c613fff871, the subject manifest SHA-256, rather than confusing it with the inventory file's digest.

Read-only builder invocation passed:

```text
python3 -I -B c2b-m5/binding/build_v241.py --main 17c9cf6d447dcfde4b6e12f2de9f820606046019 --head f61b0cbfdb2ff9f6e6606993daa59e00a0e8111e --check
checked
```

### B-NBO-2 — Inventory acceptance does not clear the companion description unit

The companion C2B-M5-DESCRIPTIONS-r1 review has required findings B-RF-1 and B-RF-2 at v241 /files/770/description and /files/818/description. An additive inventory is required to preserve those inherited raw rows; their current meanings must be repaired by the description successor. This inventory may be accepted independently, but the requested two-unit binding is not cleared.

The existing lock's 169 inherited meanings project into 180 at v241. This carries the S4 v240 record's eleven direct overrides and its two supersession tails, accounting for overlap with earlier inherited rows; it does not drop or revive the superseded meanings. The lead dry-run verifier succeeds (201 inventory successors, 189 contract successors), with productQualification=false. Its placeholder review/assent population and earlier cd40e1d staging are structural evidence only. Real root assent, exact final review copies, lock verification and integration remain separate.

### B-NBO-3 — Binding joins are exact and fail closed on the rejected description review

make_assents.py requires accepting verdicts, empty requiredFindings and the exact staged subject-manifest hashes. Its inventory gate also requires the exact accepted candidate pin. bind_lock.py appends the exact parent/candidate/record/review/assent pins for inventory and the exact record/subject/review/assent pins for descriptions; it derives inherited meanings with the product verifier, then runs the unmodified verifier on the resulting candidate. The verifier checks inventory candidate/parent/record joins and the accepting review/root-assent requirements; its description path checks the reviewed manifest membership and exact passage selectors/bytes.

The description REQUIRED-FINDINGS verdict cannot satisfy those gates. make_assents.py writes its inventory assent before checking descriptions, so it may leave only an inventory assent on rejection; that does not authorize the second unit or a combined lock. No real or reviewer-authored root assent was created here.

## Reviewed bytes

L = lead-2026-10-25; A = opensip_arch; P = product main. All paths below are qualified accordingly. The scratch audit also retains every modified-file source pin and effective description used by the companion review.

| Subject | Bytes | SHA-256 |
|---|---:|---|
| L/c2b-m5/binding/stage/docs/implementation/m2/repository-file-inventory.v241.json | 822071 | `77f298a1181f8250f576192e37e587ed2041e3d9c22f0392170acd45be818197` |
| L/c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/inventory-v241-r1/successor.json | 1512 | `3eaf4021babef3e6b927470155c8343d558049f0c5dab25f23e458340d63219e` |
| L/c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/inventory-v241-r1-subject.json | 488 | `c9834ab6e168eb2cdadd5b82e83903c260edcb4c558c1157b612d1c613fff871` |
| A/docs/implementation/m2/repository-file-inventory.v240.json | 813563 | `e5f5489955314ed530998a873496b2385941ccd817db140f6b5a7471ac213ddc` |
| L/c2b-m5/binding/build_v241.py | 10626 | `04b0b04d0d4b5d4c23cad0a6d6f70833d6e68aec18e9519d6f97f2ecc1731e49` |
| L/c2b-m5/binding/stage_binding.py | 5441 | `b3bfb2d08d81b3c11e6c37472bb8e88b0abc27865b1973a11abfccc825712ec8` |
| P/crates/host/src/node_modules_layout.rs | 56678 | `660a46add48aa423533a7eaa8f2cad03471ad59fc002852dccd6380b7c127310` |
| P/crates/host/src/node_modules_layout_tests.rs | 102620 | `b1b37664daf64d222f623320af7dbdf594462b50f0064228133d6714d63ac8f4` |
| P/crates/host/src/node_modules_layout_vectors.json | 24464 | `1befb82ab64586ebc4d67ca9f42a4cdef7984255e1ef724a46d1287ff6c3fff7` |
| P/crates/host/src/snapshot_admission.rs | 22448 | `59febe43c4d2dca3129560deecaee9c7d491629aa25be2c0a569ac1b02799bb5` |
| P/crates/host/src/snapshot_admission_tests.rs | 9349 | `1c664eea532ce040f083a70bb812deb12e32bcdcd35b826fd880ab91436c238e` |
| P/crates/host/src/snapshot_harness_tests.rs | 24541 | `4971032380ff54062c3485cf0379fd6620dfc8a266f3100258c95d38639dc350` |
| P/crates/host/src/snapshot_m3_tests.rs | 67336 | `a998d3661868894eb1624a38eb62b71748f341ceef9eaed5cae453c75a47506c` |
| P/crates/host/tests/admission_allocations.rs | 2953 | `f819d290870ab041861ed9ba619a5827f257ef7bb63166a7cffdc42967c60f14` |
| P/crates/host/tests/metered_parse.rs | 7902 | `9bbecb9256f0903138a84c003ebd6826688957c77cdb2f937e673140c1b06943` |
| P/crates/host/tests/support/admission_cases.rs | 4802 | `bb1708a3ce5bd911627a8dba1639b1d719654006b8a704a2cb3e68f2cf02ee6c` |
| P/crates/host/tests/terminal_allocations.rs | 5499 | `cda84a3475fa50f41295949d0126e1a1c60a45070540520f86965b0c577e2159` |
| P/crates/platform/src/link_target.rs | 5307 | `249a4c0d897fb15d982b02cdac688f73df409b6fd7adc2b201c550f013bcadf4` |
| P/crates/platform/src/link_target_tests.rs | 5588 | `39ca0a1cefea0405b71c2521ab0628fb6682cce86be6eafe7fffd42ab2dddc10` |
| P/crates/security/src/snapshot_sort.rs | 5727 | `b66fae47223b7d5873eb6ff042d995c18f887abcb48ad4f2c5411d4479d1027c` |
| P/crates/security/src/snapshot_sort_tests.rs | 7392 | `ed4a895ded618ebf4029e0387117041a37685c4b5ac59dc7b6c13cb911d61187` |
| P/crates/security/src/snapshot_terminal.rs | 5191 | `87ceafa7756be0dcfd6c9f1b07fa6cc509fcd39266024e391844864e639935a6` |
| P/crates/security/src/snapshot_terminal_tests.rs | 9187 | `42b0664b8cb1fc9b14f8c2c2bdf2f870cd6a87287e78bb82f6286a7357e1b31b` |
| L/c2b-m5/review-binding/scratch/audit.json | 39744 | `739a41af97ffe0f5faa0677c14d970a7d0b65210a4602b586f9367bbe37e11c4` |
