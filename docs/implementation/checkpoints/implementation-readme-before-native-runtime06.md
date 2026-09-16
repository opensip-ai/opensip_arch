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
- [Registered schema and identity runtime](m2/trials/admission-runtime-materialization-01/) provides immutable48source schema admission,15current aliases and private candidate identities, separate from40generation sources. Shape/hash admission does not establish a retained Run or replay.
- [Retained evidence and native-context runtime](m2/trials/native-runtime-materialization-03/) installs35 reviewed inputs: retained objects/frames/records/payload/relation diagnostics, exact CVE1 capability admission, the Plan capability-byte join, and Rust/TypeScript/syntax context checks. Actual Grok and root accepted the exact dependency source policy and documented bounded Hangul unsafe dependency code. Unicode16 NFC and owned Unicode15 full lowercase remain separate.94workspace tests and isolated108host/25provider source exports support this bounded unit; live source/design/dependency/build checks pass.
- [Native universe, retained bytes and Plan checks](m2/trials/native-runtime-materialization-04/) installs10 reviewed inputs. Syntax/TypeScript/Rust binders, native frame and closure member retention, and Plan selection/capability/prepared-grant/read-set checks now compose over explicit retained inputs.383Plan comparisons and304retention outputs match the reference;99Rust tests and isolated112host/25provider exports pass. Explicit census diagnostics do not prove complete Run admission or replay.
- [Retained clone body identity](m2/trials/native-runtime-materialization-05/) installs seven reviewed inputs: interpreter normalization maps, compiler/grammar dialect projection, integer Rust editions and retained body framing. L0 source recomputation and L1–L3 token custody pass965reference cases;100Rust tests and isolated114host/25provider exports pass. This does not qualify normalizers or establish full anchor, capability, Coverage, Plan or Run admission.
- Initial report help and styles. The complete offline report application and host delivery are not integrated.

The live design lock selects 14 inventory and 18 contract successors. [Inventory 16](m2/capability-support-inventory-v16-unit.json) describes 377 file responsibilities across the unchanged 20-package structure. This is a plan and ownership guide, not a claim that all 377 files are implemented.

## Milestones

| Milestone | Status |
|---|---|
| M0 design baseline | Accepted; implementation corrections are reviewed separately |
| M1 isolated builds/contracts | Accepted development checkpoint; [root readiness](m1/READINESS.md) records actual fresh/scoped reviews and verified integration |
| M2 admission/publication | Registered schema/identity, native context/universe/retention and explicit-census Plan checks integrated; full graph joins, replay/security/durable publication remain |
| M3 TS/JS/Rust analysis | Not implemented |
| M4 report/historical queries | Reader and presentation views reviewed in staged units; full app, retained source locations and host delivery incomplete |
| M5 workflows/lifecycle | Not implemented |
| M6 release qualification | Not implemented;32release gates and54recovery cases remain unperformed |

Staged and reference tests do not complete milestones or establish release qualification. The scoped review records under `m1/reviews/` distinguish actual Claude/Grok reviews, root reproductions, failed attempts and remaining duties.

## Current work

M1 remains an accepted development checkpoint. M2 now includes the selected schema/identity runtime and retained/native-context unit described above. A packaging error in native-runtime selectionv2 was caught during private activation before live changes; [selectionv3](m2/native-runtime-selection-v3-unit.json) corrects the parent list while preserving all reviewed source bytes and failed-attempt evidence.

The native universe, retention and Plan unit is now installed after actual Grok formal review, root assent, private activation and live source/design/dependency verification. Clone body-identity work is a separate private candidate checking interpreter-owned normalization maps, source dialect, verbatim body spans and normalized-token framing. Full graph/native capability/coverage/import joins, complete Run reconstruction, evaluator replay and storage/security publication remain required.

The [active work guide](ACTIVE-WORK.md) records exact subjects, review state and resume steps. The [previous status](checkpoints/implementation-readme-before-native-runtime03.md) and earlier checkpoints preserve historical claims. M2 completion, native compiler providers, the full report and workflows, and M6 qualification remain required.
