# Other-runs independent kit-only review (successor after law-interaction disposition)

**Verdict: `OTHER_RUNS_REFUSED`**

Successor four-Run grades after resolving the predicate.inputRefs / evaluationInputRefs law-interaction. Same exact stores. Not whole-consumer ACCEPT.

## Custody

- charter `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` match=True
- kit `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` match=True
- snapshot `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` match=True

## Withdrawn

- **selfaudit.v3 syntax-data structural/fullsemantic PASS and overall ADMIT** — Rested on treating identity §3 subset MUST as diagnostic because ProofInputRef.domain permits rule-program. Schema permit of a shared type is not an exception to the subset MUST.
- **selfaudit.v3 diagnostic/notUsedAsFirstRefusal on predicate-inputRefs-subset for all four graphs** — For ts/rust/rust-partial the native producing-rule first refusals remain first (earlier in closure). The subset failure is additional reached structural law on the claimed proof but does not replace those first refusals. For syntax-data it is the first refusal.

## First-refusal map (same exact four stores)

| Run | Raw | Schema | Structural | Fullsemantic | First refusal |
|---|---|---|---|---|---|
| `ts` | PASS | PASS | REFUSED | NOT_REACHED | `structural:ts.compilerPackageDigest-is-toolchain-tree-member` |
| `rust` | PASS | PASS | REFUSED | NOT_REACHED | `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` |
| `syntax-data` | PASS | PASS | REFUSED | NOT_REACHED | `structural:predicate-inputRefs-subset-of-evaluationInputRefs` |
| `rust-partial-clones` | PASS | PASS | REFUSED | NOT_REACHED | `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` |

ts / rust / rust-partial keep the self-audit native producing-rule first refusals (`compilerPackageDigest` tree membership; `rustcVersion` ≠ closure `semanticVersion`). Those precede proof-record subset in closure. The subset MUST also fails on those claimed proofs and is notReached for acceptance as a *first* refusal. syntax-data native producing rules remain passed; its first refusal is now the subset MUST. fullsemantic is NOT_REACHED on every structurally refused graph.

### `ts`

- Store `ca1b44df3f89bc6d6cc63edfe239ce510a60c7fc47f2d531c5bcb10385b99086`
- Run `run3:9fb05cf2f6ead9bec2ca4f4b773ceb2cba38520582a145f52520b23b51386190` Proof `proof3:6969b09b5f6b0256ff9afb89407a843f3af379a372d206a9eb380e5eb67f8500`
- Overall **REFUSED** layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'}
- First refusal: `structural:ts.compilerPackageDigest-is-toolchain-tree-member` — compilerPackageDigest retention is closure-tree-member of toolClosure.closureId
- notReached: ['complete-semantic-replay']

### `rust`

- Store `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791`
- Run `run3:db63563987becdd0079573e16ba47f09fcb3d4b216904a873c29528bf7ddb23a` Proof `proof3:8c329c54977da78ecdb92e42ae2acb948134fc39e1ca16095166f7ccdf9d8ea2`
- Overall **REFUSED** layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'}
- First refusal: `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion
- notReached: ['complete-semantic-replay']

### `syntax-data`

- Store `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099`
- Run `run3:4ec370fb40972db1f8dffa5e2921328e30df8a6348c6191560273fb817f61488` Proof `proof3:d0d5b5f16e5bec05f20b724e2a8a40227c6cdea3efec4ecd9ae316c0b4a3bedc`
- Overall **REFUSED** layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'}
- First refusal: `structural:predicate-inputRefs-subset-of-evaluationInputRefs` — identity-and-evidence.md §3 MUST: Predicate input refs are a subset of evaluationInputRefs. claimed extras=[{'predicateId': 'p', 'ref': {'digest': '71aaef89749857b54552f394b368a64df5a3c70df079daf7109ee1bcc9381b40', 'domain': 'rule-program'}}]
- notReached: ['complete-semantic-replay']

### `rust-partial-clones`

- Store `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c`
- Run `run3:4852e398497daf2c361127a6fd82a59e5c82e01b4b6323ee6cb7750458faaca1` Proof `proof3:9406360530804fa453f5b5a2ce7255c370bd004f19608afd4574fbf7aecd8754`
- Overall **REFUSED** layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'}
- First refusal: `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion
- notReached: ['complete-semantic-replay']

No whole-consumer ACCEPT. No remint.

