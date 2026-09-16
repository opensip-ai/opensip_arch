**Disposition: REAL-GAP.** The current `opensip policy test SUITE` route cannot test a lawful PolicyDocumentV2 policy. It only admits V1 candidates and resolves and evaluates them with the old workflow1 code. The contract says the current policy is V2. I found no published conversion or dispatch bridge. This is a read-only coauthor assessment of the fixed capture, not acceptance or the final independent review.

I checked all 1360 source files against root's `capture.json`: they match, and each probe run re-checked them before and after with no change. There were three probe runs. The first failed on a bug in my probe; I kept its receipt. The other two passed.

**Proven by probes on the actual code:**
- **The command runs the old code.** `run_admitted_policy_test` calls the v1 `run_policy_test` object. That function uses the v1 resolver and evaluator, not the v3 overrides; v3 defines no evaluator, and the v1 one never reads `endpoint`.
- **Admission is V1.** The suite schema requires a `PolicyDocumentV1` candidate, and the grammar check reads the V1 policy schema.
- **Lawful current policies are refused.** Three V2 policies pass the V2 schema, the v3 resolver and the `policy show` record, yet all three are refused before evaluation. Two get `CONFIG.INVALID`; the one using `endpoint: target` gets `POLICY.IMPERATIVE_KEY_REFUSED`.
- **`schemaMajor` alone decides it.** The checker's own V2 policy is admitted once only `schemaMajor` is set to 1. I ran that as a diagnostic only, not as a lawful conversion.
- **V1 still works.** The owner's V1 suite is admitted, and its result fits the current result record.
- **`policy show` and `policy test` never overlap.** `policy show` accepts the V2 policies and rejects the owner's V1 fixture policy.
- **The old resolver disagrees with current rules.**
  - The command accepts the owner fixture policy, which the v3 resolver refuses (`ATOM_FILTER_FIELD_FORBIDDEN: history-change.confidenceMillionths`).
  - It accepts a target endpoint on `file`, which v3 refuses.
  - It refuses a V2 `test-execution` rule that v3 admits.
- **Different meaning, not just a different schema.** Called directly (a diagnostic, not the product route), the old evaluator gives the same finding with or without `endpoint: target`. It lands on `src/b.ts`, and the expectation on `src/a.ts` fails.

**Inferred, not executed:**
- **Not intentional.** The dispatch sentence "test records keep their selected owners" doesn't mean V1 candidates. The same paragraph, §5 and §10 all put the policy on V2, and "test" most plausibly means `test-execution`.
- **A passing V1 candidate is useless here.** It can't be enforced in this profile: Plan admission, `policy show` and every evaluator3 projection require V2, and relabelling is forbidden.
- **Target semantics.** Under the V2 atom rules, a target-endpoint rule would be decided for `src/a.ts`. I read this from the atom owner and registry but didn't run it on suite fixtures.
- **Test filters.** The facts fixture can't express V2 test-result filters.

**Not counted:** the known string-expression grammar failure (`oc2-owner-string-expression-case-is-policy-imperative-key-refused`) and the repair join defects. The `endpoint` misclassification above is a different route that comes from the V1 grammar choice; you may want to de-duplicate it if the separate grammar fix also retargets the schema.

**Suggested fix for your review (nothing applied):**
1. Add a `PolicyTestSuiteV2` whose candidate is `PolicyDocumentV2`. Keep `PolicyTestSuiteV1` for the old workflow1 profile.
2. Keep `PolicyTestResultV1` and its identity. §10 already defines its digests over V2 bytes, so no major bump; only description text changes.
3. In v3, refuse V1 candidates with a typed refusal (no coercion) and point the grammar check at the V2 schema.
4. Define a v3 authoring-test function that uses the v3 resolver and V2 atom rules, including `endpoint`. It must not call the imported v1 function, whose globals bind the old code. Decide how test filters behave in a facts fixture.
5. Fix the contract §5 and dispatch-paragraph wording and add a golden for a refused V1 candidate.
6. Add checks for V2 positives, V1 refusal, endpoint discrimination and a policy only the old resolver accepts.

**Limits:**
- I didn't rerun the full projection checker or review the whole source.
- The bridge search was a bounded text search of this capture.
- Sources-kind cases, host execution and grades are out of scope.

No subprocesses are still running.

Files are in `/private/tmp/opensip-design-corrections/claude-policy-test-profile-assessment.v1`:
- `review.md`
- `review.json` — rebuilt from the probe output, and the build refuses if any proven fact fails
- `probes/output/policy-test-profile-probe.json`
- `custody/`
- `receipts/`
