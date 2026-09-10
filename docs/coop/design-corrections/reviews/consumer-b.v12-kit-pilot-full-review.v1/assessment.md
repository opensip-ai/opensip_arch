I'll continue the same origin: copy the independent checker into the new output, verify the two new stores, then run full structural admission plus semantic replay on those exact bytes.Hashes match. Next I’ll copy the predecessor checker with path redirects, then read the evaluator contracts for full replay.Hashes match. I’ll copy the checker with path redirects, keep a predecessor diff, then load the evaluator contracts for full replay.`check.py` still points at the old origin for kit files. I’ll retarget custody hashes, then inspect the two new stores and the policy/evaluator schemas.I'll add the independent evaluator and wire it to run only after structural admission succeeds.`stableId` is an install-registry field, not an S1 Run-closure join. I’ll keep S1’s `platforms[]` tree projection and continue replay.**Verdict: `PILOT_FULL_ADMITS`**

Same origin as the previous export-admission review. These two new stores were not assumed to fail the old six-graph refusals. Replay was derived from Plan-selected inventories and facts, not from claimed proof fields.

| Graph | Structural | Semantic |
|---|---|---|
| syntax-code (`run3:4b58935a…ff7b`) | ADMIT | **REPLAY_MATCH** — derived proof C `eb2a3bd6…ae71` equals the retained proof; evidence/seal/Run IDs match |
| syntax-code.tamper (`run3:8e81be4e…b49c`) | ADMIT first | **REPLAY_REFUSE** — derived `none=false` / verdict `pass` / no findings vs claimed `fail` and `finding3:0c895614…3cdb` |

The tamper graph admitted identities, schema, and citations before the logical disagreement, so the semantic negative counts. Independently: file fact `hello.rs` is a known match, so `none` is false (three-valued law), not true.

Predecessor helper correction (kit-only): Run-closure does not demand install-registry `stableId`; S1 binds `platforms[]` `{os, arch, tree, entrypoint}` plus RJ-3.

This is not whole-consumer ACCEPT and not the other 134 obligations.

Reproduce:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-full-review.v1/output/standalone-checker/check.py
```

Deliverables: `pilot-full-review.md`, `pilot-full-review.json`, `replay/*.replay.json`, `predecessor/` (source + diffs).
