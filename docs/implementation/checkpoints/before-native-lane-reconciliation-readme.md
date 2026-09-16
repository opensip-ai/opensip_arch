# OpenSIP implementation

Product code lives in the sibling `opensip` repository. This repository retains the accepted design, reference models and review evidence. The user authorizes continuous implementation with actual Grok reviewing and Codex leading. Historical Claude reviews remain valid within their recorded scopes. No new implementation commit or push is authorized.

The [active work guide](ACTIVE-WORK.md) gives the current task, exact review subjects and resume instructions. The [accepted baseline](../coop/design-corrections/reviews/root-application46-delivery.v1/README.md) and [build plan](../v2/architecture/implementation-boundaries-and-build-plan.md) remain authoritative; reviewed successors preserve their history.

## Implemented in the product

- Canonical identity and generated contracts, with 44 owned schema/source files and eight generated files. [Source selection v3](m1/source-selection-unit.v3.json) is bound in the actual design lock.
- Metadata CLI: help, version and shell completion. [CLI integration](m1/trials/cli-materialization-03/) passed 22 tests, strict Clippy and formatting. Repository analysis is still being implemented.
- Reviewed development contract generator, explicit offline provisioning inputs and exact generation/drift checks. [Generator05 integration](m1/trials/generator-materialization-05/) verifies the live product; [public activation tests](m1/trials/generator-activation-02/) cover changed/missing outputs, repair, clean generation, unexpected-file preservation and wrong-interpreter refusal. Its bound tooling policy explicitly retains the compiler's unresolved dynamic-loader limitation.
- Reviewed TypeScript and Cargo boundary tools, independent npm locks, and the selected public TypeScript check command. [Bootstrap integration](m1/trials/bootstrap-materialization-01/) passes all three live lanes, the current Rust graph and an unchanged generator drift check. [Private activation](m1/trials/bootstrap-activation-01/) passed18commands, including exact refusal controls and compile/check cycles. Checker10 has234regression tests; its unverified-output parsing issue is closed.
- [Platform entropy backend guard](m1/trials/platform-backend-materialization-01/) refuses effective compiler/config backend overrides. Five real Cargo controls, the22workspace tests, strict Clippy and formatting pass; live platform build and TypeScript/design checks pass. This closes the override gap, not complete native build/release qualification.
- Initial report help and styles. The complete offline report application and host delivery are not integrated.

The live design lock selects seven inventory and seven contract successors. The latest inventory has330file responsibilities across the unchanged20package structure. This is a plan and ownership guide, not a claim that all330files are implemented.

## Milestones

| Milestone | Status |
|---|---|
| M0 design baseline | Accepted; implementation corrections are reviewed separately |
| M1 isolated builds/contracts | In progress; remaining work includes isolated-build qualification, asset/build duties and fresh blind consumer B |
| M2 admission/publication | Not implemented |
| M3 TS/JS/Rust analysis | Not implemented |
| M4 report/historical queries | Reader and presentation views reviewed in staged units; full app, retained source locations and host delivery incomplete |
| M5 workflows/lifecycle | Not implemented |
| M6 release qualification | Not implemented;32release gates and54recovery cases remain unperformed |

Staged and reference tests do not complete milestones or establish release qualification. The scoped review records under `m1/reviews/` distinguish actual Claude/Grok reviews, root reproductions, failed attempts and remaining duties.

## Current work

The entropy backend guard and tooling integration above are installed and verified. Current work adds exact contracts-source verification to the dependency-feature check. A private actual-Cargo control refuses feature expansion enabled by another workspace member. The new dependency checker is not reviewed or installed yet; isolated build/source and remaining asset duties still gate M1.

The [active work guide](ACTIVE-WORK.md) records exact subjects, review state and resume steps. Prior bootstrap and checker status text is preserved in [the preceding checkpoint](checkpoints/implementation-readme-before-bootstrap01.md).

[Earlier implementation status and unit tables](checkpoints/implementation-readme-before-generator05.md) are preserved as historical checkpoints with an adjacent hash/length receipt. Their old pending/accepted statements should not replace the current scoped records.
