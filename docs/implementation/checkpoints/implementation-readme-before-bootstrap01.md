# OpenSIP implementation

Product code lives in the sibling `opensip` repository. This repository retains the accepted design, reference models and review evidence. The user authorizes continuous implementation with actual Grok reviewing and Codex leading. Historical Claude reviews remain valid within their recorded scopes. No new implementation commit or push is authorized.

The [active work guide](ACTIVE-WORK.md) gives the current task, exact review subjects and resume instructions. The [accepted baseline](../coop/design-corrections/reviews/root-application46-delivery.v1/README.md) and [build plan](../v2/architecture/implementation-boundaries-and-build-plan.md) remain authoritative; reviewed successors preserve their history.

## Implemented in the product

- Canonical identity and generated contracts, with 44 owned schema/source files and eight generated files. [Source selection v3](m1/source-selection-unit.v3.json) is bound in the actual design lock.
- Metadata CLI: help, version and shell completion. [CLI integration](m1/trials/cli-materialization-03/) passed 22 tests, strict Clippy and formatting. Repository analysis is still being implemented.
- Reviewed development contract generator, explicit offline provisioning inputs and exact generation/drift checks. [Generator05 integration](m1/trials/generator-materialization-05/) verifies the live product; [public activation tests](m1/trials/generator-activation-02/) cover changed/missing outputs, repair, clean generation, unexpected-file preservation and wrong-interpreter refusal. Its bound tooling policy explicitly retains the compiler's unresolved dynamic-loader limitation.
- Initial report help and styles. The complete offline report application and host delivery are not integrated.

The live design lock selects four inventory and five contract successors. The latest inventory has324file responsibilities across the unchanged20package structure. This is a plan and ownership guide, not a claim that all324files are implemented.

## Milestones

| Milestone | Status |
|---|---|
| M0 design baseline | Accepted; implementation corrections are reviewed separately |
| M1 isolated builds/contracts | In progress; remaining work includes boundary/bootstrap integration, asset/build duties and fresh blind consumer B |
| M2 admission/publication | Not implemented |
| M3 TS/JS/Rust analysis | Not implemented |
| M4 report/historical queries | Reader and presentation views reviewed in staged units; full app, retained source locations and host delivery incomplete |
| M5 workflows/lifecycle | Not implemented |
| M6 release qualification | Not implemented;32release gates and54recovery cases remain unperformed |

Staged and reference tests do not complete milestones or establish release qualification. The scoped review records under `m1/reviews/` distinguish actual Claude/Grok reviews, root reproductions, failed attempts and remaining duties.

## Current review and next integration

Grok is reviewing the checker09 correction for normal compile/check cycles. All233root tests pass, including nine new tests for exact, changed, extra, linked, stale and partially present compiler outputs. The earlier checker08mistakes existing compiled JavaScript for undeclared source; its history is preserved. Checker09is not yet approved or installed.

The generic TypeScript bootstrap/orchestration proposal remains unfrozen in `m1/bootstrap-selection-v1/`. It must absorb the accepted checker result, bind exact files and scoped package-manager/bundler decisions, and pass actual activation before installation. The active work guide records the concrete next steps and paths.

[Earlier implementation status and unit tables](checkpoints/implementation-readme-before-generator05.md) are preserved as historical checkpoints with an adjacent hash/length receipt. Their old pending/accepted statements should not replace the current scoped records.
