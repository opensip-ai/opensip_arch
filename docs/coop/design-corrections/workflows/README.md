# Workflows and surfaces — reference evidence (PROPOSED, NOT SELF-ACCEPTED)

Design evidence for
[`docs/v2/contracts/product-v1/workflows-and-surfaces.md`](../../../v2/contracts/product-v1/workflows-and-surfaces.md).
Authored and corrected by actual Claude, Codex and actual Grok under D-367
delegation. Review standing is governed by the correction record. Claude's
later successor review remains pending credits. Nothing here is product
implementation or qualification.

## Selected evaluator3 profile

`schemas/evaluator3/`, `workflow-projection-contract.v3.md` and
`workflow_projection_model.v3.py` own current output projections.
`command-inventory.v3.json` selects the 45 commands and JSON envelope major3.
`schemas/policy-document.v2.schema.json` owns PolicyDocumentV2 and
`schemas/evaluator3/policy-test.schema.json` owns the current `policy test` input PolicyTestSuiteV2,
evaluated by `policy_test_model.v3.py` and exercised over the authored `policy-test-cases.v3.json`;
unchanged scope, waiver, import and test-execution documents retain their declared schemas. Current Run admission
calls the foundation evaluator3 public replay boundary before projection.
`check-workflow-projection.v3.py` checks current projections over retained
synthetic graphs. The retained workflow1 model/checker below exercises its
historical surface profile and shared unchanged recipes; it does not substitute
for the current projection suite.

## Retained surface profile and shared files

| File | Role |
|---|---|
| `schemas/common.schema.json` | shared closed primitives: product major-two ids, `ExecutionId` (`exec1_`), strict `LogicalPath` vs `UserInputPath`, D9 termination branch contract, domain-detail codes |
| `schemas/invocation-record.schema.json` | invocation → steps (≤64) → attempts (≤3) → derivation binding (≤1024 stages); closed ephemeral/authoritative result union; cancellation |
| `schemas/command-inventory.schema.json`, `command-inventory.v1.json` | the retained profile1 CLI/JSON/SARIF/HTML/agent inventory (45 commands, 5 renderers, 41 outcome goldens) |
| `schemas/command-envelope.schema.json` | `CommandEnvelope` major 2 |
| `schemas/baseline-artifact.schema.json` | portable baseline with pivot closure, embedded context documents and retention pins |
| `schemas/comparison-result.schema.json` | multi-axis comparison with pivot chain B/E0..E4, audit profiles, typed indeterminacy |
| `schemas/imported-evidence.schema.json` | the one `import2` wrapper (foundation `import` mirror), payload bindings, runtime/history payloads, staleness table |
| `schemas/policy-document.schema.json` | closed declarative policy DSL, scope document, waiver set and resolution |
| `schemas/policy-test.schema.json` | retained PolicyTestSuiteV1 authoring test suite (workflow1 input) and the deterministic PolicyTestResultV1, Case and Override definitions the evaluator3 suite reuses |
| `schemas/review.schema.json` | candidate → inspect → review disposition (advisory only) |
| `schemas/repair.schema.json` | repair plan, apply journal, recovery table, mutation receipt |
| `schemas/test-execution.schema.json` | separately authorized test execution step and test payload |
| `schemas/graph-query.schema.json` | bounded read-only query operations |
| `workflows_model.v1.py` | reference model of the contract semantics over synthetic inputs; uses `../foundation/canonical.py` for every hash and exact typed validation |
| `workflow-cases.v1.json` | hand-authored cases and expectations |
| `check_workflows.v1.py` | compiles schemas, validates inventory/cases/outputs, runs the model, writes `workflows-report.v1.json` |
| `source-pins.v1.json`, `run-reference-checks.py` | pinned inputs and launcher |
| `obligation-map.v1.json` | feedback point / AR obligation → sections, schemas, cases |

## Run

```
python -I -B run-reference-checks.py --report workflows-validation-report.json
```

Python 3.12 with jsonschema 4.25.1 (`/tmp/opensip-architecture-review-env`). The
launcher verifies `source-pins.v1.json`, then executes `check_workflows.v1.py`.

## Boundaries

- Pivot presence sets (E0..E4) are supplied by cases; no detector runs.
- Repair journals and trees are in-memory dicts; no OS durability is measured.
- Unit cases use synthetic admitted-grant projections; the separate integration
  checker invokes actual security model admission before creating those projections.
- Expected values were authored by the same author as the model; independent
  review is the oracle. Reference checks are design evidence, not qualification.
