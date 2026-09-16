I've made the correction. The current `opensip policy test` now takes a `PolicyTestSuiteV2` with a `PolicyDocumentV2` candidate and evaluates it under the current resolver and atom rules. All work is in my own copy at `R/work/source`; nothing was committed, pinned or planned, and the checks are my own reference evidence, not independent review.

**Source and custody**
- I copied the mutable successor as fresh regular files: 12905 files, no drift in two hash passes, file-list sha `a1c2fd53…a1d7e4`.
- Compared with the assessment's capture, only `workflows_model.v3.py` plus four prose/architecture docs differ.
- The copy differs from the capture in exactly 12 paths. The diff is `output/correction.diff` (1529 lines, sha `beaef533…037088`); full before/after hashes are in `custody/correction-manifest.json`.
- The repair region of `workflows_model.v3.py` (closed-world selector and repair:2 constructor) is byte-identical, as are `repair_closed_world_selection.v1.py`, the legacy V1 model, schema, cases and checker, the atom owner and registry, and the detail registry.

**Your decisions, as built**
1. **Suite:** new schema `workflows/schemas/evaluator3/policy-test.schema.json` defines `PolicyTestSuiteV2` (major 2, candidate `PolicyDocumentV2`; waivers, cases and overrides unchanged). This is a breaking input change, stated as such in the prose.
   - `PolicyTestResultV1`, the `policytest2` prefix and the result carrier are unchanged.
   - `suiteDigest` is now H over the admitted V2 suite; candidate and effective digests are over V2 bytes.
2. **Owner:** `workflows_model.v3.py` now defines its own `run_policy_test` / `run_admitted_policy_test`. They call the v3 resolver and atom owner and a new evaluator, `workflows/policy_test_model.v3.py`. The legacy function stays as `_base.run_policy_test`.
   - The grammar check reads `PolicyDocumentV2`; the f561 positional helper is untouched.
   - Admission order: suite major, then candidate major, then schema/grammar, then fixture and override checks, then resolver details.
   - A wrong major gets `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `EVALUATION.MIXED_OUTPUT_MAJOR` before any grammar check, so it is never called an imperative key.
   - `resolve_policy` refuses non-V2 input the same way; `identity-model.v3` doesn't call it. No new D9 detail.
3. **Semantics:** evaluation reuses the atom owner's registry, rung comparison and comparators, with no new relation table. On the same edge `src/b.ts → src/a.ts`, through the corrected public route, the target-endpoint rule finds `b.ts` and the source-endpoint rule finds `a.ts`.
4. **Unrepresentable inputs:** the endpoint universe domain, `testResult`, `exitStatus`, and test-execution / test-case observations evaluate unknown.
   - A missing imported row never proves absence.
   - Affected finding/no-finding expectations come out `indeterminate`; known hits, Kleene logic and gating are preserved.
   - The rule is published in the new schema, and no result shape changed.
5. **References:** updated the contract's dispatch paragraph ("test" now means the retained `test-execution` documents), §5, §8, §9 and §10, the projection contract table, the envelope and invocation descriptions, and both READMEs. I added exactly one golden, `policy-test-suite-major-unsupported` (goldens 44 → 45). No new sections.
6. **Fixtures and controls:** a new explicitly authored fixture, `workflows/policy-test-cases.v3.json`, plus 24 `pt2-*` checks in the existing workflow-projection checker. They cover every control you listed. The historical V1 route id `policytest2:5ce020d4…ee27` is pinned.

**Results (receipts in `receipts/`)**

| check | before | after |
|---|---|---|
| `check-workflow-projection.v3.py` | 795/795 | 819/819; none removed or flipped, 24 added |
| `check-query-projection.v3.py` | 204/204 | 204/204 |
| historical `check_workflows.v1.py` | 1816/1816 | 1816/1816, stdout byte-identical |
| `check-array-orders.py` | 121 | 123 |
| foundation `check-policy-derivation.v3.py` | — | 6/6 |
| route probe | V1 suite accepted; lawful V2 suite refused | V1 refused on major; V2 → `policytest2:d7fcc42c…5f67` (5 passed / 3 indeterminate / 1 not-executable) |
| focused semantics probe | — | 17/17 |

The historical checker's report file differs only in its internal file-hash table. Two of my own receipts failed and are kept: the first query run lacked `--report`, and the first route probe lacked some constants. Both were rerun successfully.

**For your integration**
- **No new child checker** is needed; the launcher's job list is unchanged.
- **Pins:** update the five pin sets for the 9 modified paths and add the 3 new ones.
- **Planning:** you own the new M5 row for golden `policy-test-suite-major-unsupported`.
- **ce3 merge:** the repair code is untouched here, so expect overlap only in `check-workflow-projection.v3.py` and the contract prose.
- **Full suites:** rerun them under the new pins; I ran only the checks above.

**Limits**
- This is bounded standalone test semantics over finite fact fixtures, not production or full-Run qualification; sources cases stay not-executable.
- Runtime and history rows match by path; the atom owner's ambiguity refusals aren't modelled.
- The result can't say why a rule is indeterminate. The old `CaseResult` wording is narrower than the new §5 law and stays byte-unchanged.
- An unknown override rule or wrong override type is now a typed `CONFIG.INVALID`; the old model crashed with a `KeyError`.
- Expected outcomes are my own; independent review remains the oracle.

No background processes are running.

Files are in `/private/tmp/opensip-design-corrections/claude-policy-test-profile-author.v1`:
- review.md
- review.json
