# author-03: TypeScript lane boundary checker (candidate B) and bounded comparison

This is the author subject for independent review. Read `comparison.md` first, then `selection-proposal.md`.

| Path | Role |
|---|---|
| `checker/` | Proposed checker: `bin/check-boundary.mjs`, `src/{check,lane,resolve,usages}.mjs`, `test/boundary.test.mjs`, and `node_modules/` (typescript 6.0.3, enhanced-resolve 5.25.1, graceful-fs 4.2.11, tapable 2.3.3) |
| `harness/` | `run-cases.mjs` (both candidates, Node oracles), `regression-cases.mjs`, `expectations.mjs` (revisions), `adapter.mjs` (legacy lane translation), `derive-reviewer-probes.mjs` → `reviewer-probes.generated.mjs`, `cli-invocation.mjs`, `real-lanes/` (records, trial tsconfig, runner), `mutants.mjs`, `summarize-mutants.mjs`, `complexity.mjs`, `freeze-manifest.mjs` |
| `baseline/` | Byte copy of the frozen author02 trial (candidate A, harness, 44-package npm closure), its outer manifest, and its archived test files (including the stale 95-test file) |
| `inputs/` | Byte copies of executed inputs: review-02 (probes script, evidence), the product `design-lock.json`, the pinned architecture inventory chain, the staged control-generation-02 `tools/contracts` and generated bindings, and the pnpm-provision-05 materialization |
| `provenance/` | Archives (5 tarballs), registry records, `verify-archives.mjs` |
| `results/` | `cases.json`, `cases-run.txt`, `cases-run-1.txt` (first run, with failures preserved), `checker-tests.txt`, `cli-invocation.json`, `real-lanes.json`, `mutants.json` plus `mutants/`, `archive-verification.json`, `complexity.json` |
| `freeze-manifest.json` | Every frozen entry (type, mode, bytes, sha256, symlink target), tool closures and the pinned runtime |
| `fullcheck.sh` | Offline reproduction from frozen inputs; regenerates `results/`, so run it in a copy |

## CLI

```sh
/Users/sb/.nvm/versions/node/v24.16.0/bin/node checker/bin/check-boundary.mjs \
  --root REPO --lane-record LANE.json \
  --design-lock inputs/product/design-lock.json --architecture inputs/architecture \
  [--unbound-lane tooling]
```

| Exit code | Meaning |
|---|---|
| 0 | Accepted, JSON report on stdout |
| 1 | Refused, JSON report on stdout |
| 2 | Invalid invocation, lane record or inventory binding (message on stderr) |
| 3 | Internal error |
