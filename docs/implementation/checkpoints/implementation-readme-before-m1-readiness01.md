# OpenSIP implementation

Product code lives in the sibling `opensip` repository. This repository retains the accepted design, reference models and review evidence. The user authorizes continuous implementation with actual Grok reviewing and Codex leading. Historical Claude reviews remain valid within their recorded scopes. No new implementation commit or push is authorized.

The [active work guide](ACTIVE-WORK.md) gives the current task, exact review subjects and resume instructions. The [accepted baseline](../coop/design-corrections/reviews/root-application46-delivery.v1/README.md) and [build plan](../v2/architecture/implementation-boundaries-and-build-plan.md) remain authoritative; reviewed successors preserve their history.

## Implemented in the product

- Canonical identity and generated contracts, with 44 owned schema/source files and eight generated files. [Source selection v3](m1/source-selection-unit.v3.json) is bound in the actual design lock.
- Metadata CLI: help, version and shell completion. [CLI integration](m1/trials/cli-materialization-03/) passed 22 tests, strict Clippy and formatting. Repository analysis is still being implemented.
- Reviewed development contract generator, explicit offline provisioning inputs and exact generation/drift checks. [Generator05 integration](m1/trials/generator-materialization-05/) verifies the live product; [public activation tests](m1/trials/generator-activation-02/) cover changed/missing outputs, repair, clean generation, unexpected-file preservation and wrong-interpreter refusal. Its bound tooling policy explicitly retains the compiler's unresolved dynamic-loader limitation.
- Reviewed TypeScript and Cargo boundary tools, independent npm locks, and the selected public TypeScript check command. [Bootstrap integration](m1/trials/bootstrap-materialization-01/) passes all three live lanes, the current Rust graph and an unchanged generator drift check. [Private activation](m1/trials/bootstrap-activation-01/) passed18commands, including exact refusal controls and compile/check cycles. Checker10 has234regression tests; its unverified-output parsing issue is closed.
- [Platform entropy backend guard](m1/trials/platform-backend-materialization-01/) refuses effective compiler/config backend overrides. Five real Cargo controls, the22workspace tests, strict Clippy and formatting pass; live platform build and TypeScript/design checks pass. This closes the override gap, not complete native build/release qualification.
- [Contracts dependency/source guard](m1/trials/contracts-dependency-materialization-01/) checks eight exact local files and eleven dependency checksum/feature selections. Actual Grok accepted it; seven real Cargo controls and private/live activation passed. An unexpected implicit build script also refuses. Unreferenced files outside `src` and test-target contents are outside this production-source census.
- [Foundation primitives](m2/trials/foundation-primitives-materialization-02/) add exact hash-frame decoding and retained-directory regular-file reads. Actual Grok accepted the corrected sources; a clean host build from35selected files passed30tests, strict Clippy and boundary checks. These primitives do not establish semantic admission or storage authority.
- [Independent Rust provider workspace](m1/trials/rust-provider-workspace-materialization-01/) has its own manifest, lock and development toolchain. The updated17file source export builds offline from12verified archives. Its development entry point deliberately refuses analysis; compiler/protocol implementation remains M3.
- Initial report help and styles. The complete offline report application and host delivery are not integrated.

The live design lock selects eight inventory and ten contract successors. The latest inventory has333file responsibilities across the unchanged20package structure. This is a plan and ownership guide, not a claim that all333files are implemented.

## Milestones

| Milestone | Status |
|---|---|
| M0 design baseline | Accepted; implementation corrections are reviewed separately |
| M1 isolated builds/contracts | In progress; remaining work includes isolated-build qualification, asset/build duties and fresh blind consumer B |
| M2 admission/publication | Foundation primitives integrated; full replay, security and durable publication not implemented |
| M3 TS/JS/Rust analysis | Not implemented |
| M4 report/historical queries | Reader and presentation views reviewed in staged units; full app, retained source locations and host delivery incomplete |
| M5 workflows/lifecycle | Not implemented |
| M6 release qualification | Not implemented;32release gates and54recovery cases remain unperformed |

Staged and reference tests do not complete milestones or establish release qualification. The scoped review records under `m1/reviews/` distinguish actual Claude/Grok reviews, root reproductions, failed attempts and remaining duties.

## Current work

The live product remains at eight inventory and ten contract successors. The fresh Grok consumer completed an independent review of the frozen M1 development snapshot. Its follow-up identified a missing build-time asset-pin/channel check, so final M1 acceptance remains withheld.

Logical paths, array ordering, host output delivery, and the checker executable-mode/documentation correction now have independent acceptance and root assent, but await combined installation. The asset-channel correction passes 32 workspace tests, including real compile-success and compile-failure cases, and is undergoing actual Grok review. Full descriptor admission, replay, native analysis, report delivery and release qualification remain separate work.

The [active work guide](ACTIVE-WORK.md) records exact subjects, review state and resume steps. Prior bootstrap and checker status text is preserved in [the preceding checkpoint](checkpoints/implementation-readme-before-bootstrap01.md).

[Earlier implementation status and unit tables](checkpoints/implementation-readme-before-generator05.md) are preserved as historical checkpoints with an adjacent hash/length receipt. Their old pending/accepted statements should not replace the current scoped records.
