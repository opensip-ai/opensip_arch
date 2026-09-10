# Other-runs independent kit-only review (successor after self-audit)

**Verdict: `OTHER_RUNS_REFUSED`**

Successor of the v2 four-Run recheck after a law/quantifier self-audit against the original charter. Not whole-consumer ACCEPT. Foundation/pilot/workflows/syntax-code remain outside this scoped recheck (pending global integration where the charter's at-least-one set includes them).

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS 80/80 |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | match=True |
| snapshot | `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` | PASS 343/343 |
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | match=True |

Command: `/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/output/independent/selfaudit.py`

## First-refusal map

| Run | Raw | Schema | Structural | Fullsemantic | First refusal |
|---|---|---|---|---|---|
| `ts` | PASS | PASS | REFUSED | NOT_REACHED | `structural:ts.compilerPackageDigest-is-toolchain-tree-member` |
| `rust` | PASS | PASS | REFUSED | NOT_REACHED | `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` |
| `syntax-data` | PASS | PASS | PASS | PASS | none |
| `rust-partial-clones` | PASS | PASS | REFUSED | NOT_REACHED | `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` |

Classification:

- **Existing law, missing implementation of a producing/join recipe:** TypeScript `compilerPackageDigest` is a retained raw blob (`tsc-pkg`) but is not a member of the signed toolchain closure tree named by `toolClosure.closureId` (`native-evidence` §2.4 / schema `retention=closure-tree-member`). Rust (and rust-partial, same context) `toolchain.rustcVersion=1.80.0` is not the admitted tool-closure `semanticVersion=1.0.0` (`native-context-compiler-version-not-from-manifest`, native-evidence §2.3/§11). v2 treated blob rehash / schema inhabitance as those joins.
- **Withdrawn refusal ground:** `R-RUN-CLONES-L0-AND-NORMALIZED` / `R-RUN-CLONES-CUSTODY` as a per-TS-and-Rust demand. Charter/requirements quantifier is at-least-one file-fact Run (TS or Rust or syntax-code). Syntax-code is pending global integration.
- **Absent/contradictory law:** none used as a waiver. Predicate `inputRefs` citing `rule-program` is schema-live (`ProofInputRef.domain`) and excluded from `evaluationInputRefs` by enumeration-contract §7; recorded as a law-interaction, not the first refusal.
- **C equality of shared mistaken derivation:** v2 `compose_proof` C-matched claimed proofs; that does not execute native producing recipes or identity §3 native re-admission.

### `ts`

- Store `ca1b44df3f89bc6d6cc63edfe239ce510a60c7fc47f2d531c5bcb10385b99086`
- Run `run3:9fb05cf2f6ead9bec2ca4f4b773ceb2cba38520582a145f52520b23b51386190` Plan `plan2:9a6654ad5f4e7c976f826f2c7094fc7c14af853bac8afc8bc096fb9e710e21f7` Proof `proof3:6969b09b5f6b0256ff9afb89407a843f3af379a372d206a9eb380e5eb67f8500`
- Layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'} overall **REFUSED**
- First refusal: `structural:ts.compilerPackageDigest-is-toolchain-tree-member` — compilerPackageDigest retention is closure-tree-member of toolClosure.closureId

Reached producing/join failures:
- `ts.compilerPackageDigest-is-toolchain-tree-member` — compilerPackageDigest retention is closure-tree-member of toolClosure.closureId

### `rust`

- Store `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791`
- Run `run3:db63563987becdd0079573e16ba47f09fcb3d4b216904a873c29528bf7ddb23a` Plan `plan2:25d8e4df72f3c2041966cc9bd0b9afe6d83fbbe5e5bdf9c07699082f49068545` Proof `proof3:8c329c54977da78ecdb92e42ae2acb948134fc39e1ca16095166f7ccdf9d8ea2`
- Layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'} overall **REFUSED**
- First refusal: `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion

Reached producing/join failures:
- `rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion

### `syntax-data`

- Store `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099`
- Run `run3:4ec370fb40972db1f8dffa5e2921328e30df8a6348c6191560273fb817f61488` Plan `plan2:09e25c1ec3e3267c252402623391071321a6dc0d2551200dd504c23aabb61cd9` Proof `proof3:d0d5b5f16e5bec05f20b724e2a8a40227c6cdea3efec4ecd9ae316c0b4a3bedc`
- Layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'} overall **ADMIT**
- First refusal: none

### `rust-partial-clones`

- Store `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c`
- Run `run3:4852e398497daf2c361127a6fd82a59e5c82e01b4b6323ee6cb7750458faaca1` Plan `plan2:1539822bf2705d16d3bd57fca3cbd4b3b713622c37f873909e895a0c9c60ea5c` Proof `proof3:9406360530804fa453f5b5a2ce7255c370bd004f19608afd4574fbf7aecd8754`
- Layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'} overall **REFUSED**
- First refusal: `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion

Reached producing/join failures:
- `rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion

## Unexecuted

- ROOT-ADMISSION outside this role
- component-manifest-schemas.v11 inhabitance (CANDIDATE-NOT-APPLIED); stored-bytes tree join still executed in v2
- real host/compiler/crypto/SQLite
- syntax-code / foundation / pilot / workflow / standalone vectors (pending global integration)
- Unicode Default Case Conversion beyond ASCII lib names (current libSelection is ASCII ES2022)
- L1–L3 clone token-stream recomputation (no such facts on these four graphs; at-least-one set pending syntax-code)

