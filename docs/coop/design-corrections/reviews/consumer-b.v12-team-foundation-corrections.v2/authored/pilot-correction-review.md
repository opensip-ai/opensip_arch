# Pilot correction review — syntax-code Run (consumer-b.v12 team)

**Verdict: `PILOT_READY_FOR_VALIDATOR_RECHECK`**

This is not whole-consumer acceptance, not `ACCEPT-RECONSTRUCTABLE`, and not a claim that the original reconstruction was unaided after this point. Original `blind-review.md` / `blind-review.json` are historical and were not edited. The original 123 requirements remain intact; unexecuted work outside this syntax-code pilot remains visible. Empty peer `newMustIssues` / `newShouldIssues` are not admission.

Bounded work: correct the already-required first syntax-code Run for retained-closure admission, independently recomputed complete proof replay, and a logical-result tamper distinct from a stale-hash control.

## Standing and custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | matches expected |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | matches expected |
| 80 subject files | as listed | previously PASS 80/80; kit bytes not edited |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| peer `review.md` | `308fcc89fb542fbb3c6225533672632cb7795399fa5fdb545aa8356669edace4` | PASS vs `team-inputs.json` |
| peer `review.json` | `a379bd00983d2c007e2a3fdc317c0d568d0112d2f8bb55dacf31b8eb3d581e44` | PASS |
| peer `syntax_code_pilot_corrections.json` | `626175e6dfdc8f0e47fb7c3ab5262bdaea55319958e8e4a352c988374f73fee9` | PASS |
| peer `syntax_code_pilot_corrections.py` | `8dc4fa357e8111d687e795c910a856d3433cac95bbde5611983cb46fda5df7e0` | PASS |
| peer `syntax_code_pilot_probes.json` | `2e238db56c4814c3710d128e2c128765685b5a3422251ca9efa14b022dcfd2fe` | PASS |
| peer `syntax_code_pilot_probes.py` | `4a88784c5ea5a8440c163ceefc4f5f7fd8b11b93723531307adac735fd1de246` | PASS |
| validator snapshot manifest | `824aea890b86ae9d71b914646f1e91bf07e73f590938cf29d8089f65426f27be` | recorded; not re-read as a design oracle |

Builder origin `consumer-b.v12` session `01a083a2-f866-73f2-b41c-8183ebf7bf3e`. Validator origin `consumer-b.v12-kit-validator.v1` session `01a083c2-8945-78a3-92e4-4a28bc9efed7`. Write root is only `consumer-b.v12-team-corrections.v1/output`. The original `/tmp/opensip-design-corrections/consumer-b.v12/output/runs/syntax-code.store.json` still hashes to `8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654` (untouched).

Peer report standing: evidence to assess against the kit, not a design authority. Diagnostic corrections D-CORR-1 (policy `$id` registry) and D-CORR-2 (seven-language host bundle) are validator diagnostics, not required consumer graph repairs. D-CORR-3 independently measured L0 recipe MATCHES the claimed identity; frame retention was the remaining law.

## Mechanical path correction

Copied helper/scripts originally hardcoded `/tmp/opensip-design-corrections/consumer-b.v12/{output,subject}`. Before executing any copied script those literals were redirected into `.../consumer-b.v12-team-corrections.v1/{output,subject}`. A first replace of the longest prefixes followed by a remaining-root replace briefly doubled the suffix (`...v1-team-corrections.v1`); that defect was mechanically repaired to a single team-corrections segment. Record: `output/path-correction-record.json` (SHA `528624d41c28390abcc2519e65f16e1279a2cb6e857bd212f9bad875722e3860`). Historical reviews, kit bytes, team-input bytes, and preserved-failure copies were not rewritten.

## Preserved original failing bytes

Exact original export and builder/replay sources are under `output/preserved-failures/syntax-code-original/`. Store SHA `8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654` (862544 bytes) matches the peer snapshot. Original claimed Run `run3:aa19beddb09888f33cc29eb127574259331922655122840e74293ff0c1704835`, proof `proof3:a646b25f2cbeae24960e7ce754a2bb038f53caadc03cf270c94cc4ff6eefdb6b`. Those bytes were not repaired in place.

## NEW export identities

This is ordinary reconstruction: added/corrected records change identity and dependent claims.

| Record | NEW | OLD (preserved) |
|---|---|---|
| Run | `run3:f2542b3afb9c5042438370893f9932830b4b6b1ac17f16299d35ed55d49db918` | `run3:aa19bedd…` |
| Proof | `proof3:59d3b68084ae4c16c0b09956f24f3923801a82d361d9de8b362659129987e785` | `proof3:a646b25f…` |
| Plan | `plan2:e3965f2fa9c900ed6a8214c12b2dc1f0123bef432113f2781688f8070323326d` | `plan2:c9e95979…` |
| Snapshot | `snapshot2:f50135a27d89a1fa20bd4534f45d0e9f1633379a683b47c70dcec907e46911cd` | unchanged (source inventory/hello.rs bytes unchanged) |
| Store SHA-256 | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` (867956 bytes, 79 blobs) | `8b0f6d82…` (862544, 74 blobs) |
| Meta SHA-256 | `7e9f95652567578ef9e9087386756a00b15e0bf3651411961c96340a4a8d8685` | `524c8200…` |
| Syntax context | `sha256:b1566156d63524debe43d57bb4dee37a0a87aeb092059188f0fbf5b3e4c99655` | `sha256:08d513b0…` |
| Syntax universe | `sha256:4b84311f223aa86de76555f8b03d1a46fe092edf39e0d1b0d73e3b113237d90f` | `sha256:d27d3544…` |
| L0 bodyIdentity | `sha256:72a35a8b39ca25929a4b2f0be6ef1288ebca9192fd04ad7cce37acd372390b36` | same recipe; **now retained under suffix** |
| L1 bodyIdentity | `sha256:874cf4bd66165db89dd7b65b2c8d5caf6bf53edaa3ca5868a9b2d1da55190426` | same recipe; **now retained under suffix** |
| capabilityManifestId | `8bc78baa316d90068394cb4b2f234feca02d5ab53f3aa794032924a395b7e234` | unchanged (manifest bytes unchanged) |

Export path: `/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/runs/syntax-code.store.json`. Full object table and exact blob bytes are in that store.

Helper property changes (not executed vectors): `body_identity` now constructs and can retain the FACT-IDENTITY preimage; `eval_atom` occupancy skips file facts whose `payload.path` ≠ subject `nativeSubjectId` (ADV-EVAL-ATOM-OCCUPANCY-PASS). New helpers `compose_proof.py`, `closure_admit.py`, `proof_replay.py` implement composition §7 reconstruction and recursive retained-closure joins. They are not additional required Runs.

## From-scratch commands and measured outcomes

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/runs/syntax-code.store.json
# measured: exit 0; proofCompareEqual true; closureOk true; firstRefusal null
# expectedProofId == claimedProofId proof3:59d3b680…
# C SHA-256 e9492b0456f58e11a9edebaf43d8c37ce6d2386f9c560cbb9a426eb45f342863
# derivedVerdict pass; derivedAtomValue false; findingCount 0

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/scripts/replay_from_export.py \
  --tamper \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/runs/syntax-code.store.json
# measured: exit 0; citationsPreserved true
# stale-hash control: C(tampered) != C(claimed) true (not treated as semantic replay)
# semantic replay: independently reconstructed expected proof remains verdict=pass / atom=false
# tampered claim verdict=fail; reminted tamperedProofId proof3:b32c360da612191a007b98e0b332101afb36d7cae172ce3a3bf9e9b2d01c9e80
# expected C != tampered C; refused true
```

Replay in a fresh process: reloads the NEW store, admits selected inputs from `executionInputsDigest` (locator only), projects RuleProgramV2 from the Plan policy, derives file subjects from retained inventories (not from claimed `selectedSubjectIds`), walks `emitWhen`, constructs the complete expected proof (predicate node digest/address/value, matchingFactIds, coverageIds, witnesses, findings, waivers, ruleResults, verdict), and compares C with the retained claim. Claimed findings/verdicts are not used to choose subjects or truth.

Measured raw outputs: `runs/syntax-code.replay-measured.json` (SHA `4c79e55d8ef7094a544f8d8c8a50ad59d2a0eeb33ac0ed074af32206a81a2e17`), `runs/syntax-code.tamper-measured.json` (SHA `36af91407dfccbee18be55f563155148b61370422e50567347ae87ef7176d684`).

## Peer finding dispositions

D-CORR-1 and D-CORR-2 are **not consumer repairs**. The rust-only `SyntaxGrammarBundleV1` remains (`grammars` minItems 1; `selectedGrammarIds ⊆ bundle`). PolicyDocumentV2 continues to validate against the workflow `$id` registry already attached in `schema_admit.py`.

| Original probe / refused boundary | Disposition |
|---|---|
| `installed-bundle-seven-languages` | **not-a-consumer-repair** (D-CORR-2). Host-bundled seven languages is a product-host property. Synthetic rust-only grammar remains schema-admissible. |
| `schema-policy` | **not-a-consumer-repair** (D-CORR-1). Validator omitted workflow common/imported-evidence `$id` registry. Not a graph change. |
| `grammar-artifacts-in-closure-tree` | **corrected**. kind=grammar `closure.tree` now contains grammar definition `70b27c78…`, bundleDigest `04e13aeb0de3a28599d7085eab8988a84d70322c39988db1274e7bf0ce1a7a93`, normalizer specificationDigest `8fe22043ebe7e18a9c27b7a288f71b1010b024f040284d0eafab8659f8dd9d91`, plus the existing `bin/grammar` stub. Recursive fetch rehashes every tree member. |
| `schema-payload-declares-73d6f358` | **corrected**. DeclaresPayloadV1 `container=file:hello.rs`, `declared=function:add` (SubjectIdV1). Stock schema check `decl_payload` pass. Declares subject-scope subjects use the same declared id. |
| `clones-bodyIdentity-frame-retained-L0-verbatim-5b8cd31b` | **corrected**. Frame retained under suffix. L0 recipe still equals `sha256:72a35a8b…` (D-CORR-3). Closure fetches, rehashes, parses FACT-IDENTITY, joins L0 span to anchor bytes. |
| `clones-bodyIdentity-frame-retained-L1-lexical-c0ac6ed1` | **corrected**. Frame retained under suffix `874cf4bd…`. |
| `clones-non-L0-requires-retained-frame-L1-lexical-c0ac6ed1` | **corrected**. L1 preimage custody without claiming recomputable tokenisation. |
| `syntax-only-membership-unitOrdinal-null-no-invented-unit` | **corrected**. `UnitMembershipV1.units=[]`; file row `membership=syntax-only`, `unitOrdinal=null`, `reason=grammar-only`. |
| `enumeration-exactly-one-inventory-per-cell-program-kind` | **corrected**. Locators `(0,0,file)`, `(1,0,file)`, `(1,0,package)` complete-empty, `(2,0,symbol)` with examinedPaths=`hello.rs`. |
| `cellOutcome[1]-inventoryDigests-exactly-one-per-kind` | **corrected**. kinds `{file,package}` → two inventory digests. |
| `cellOutcome[2]-inventoryDigests-exactly-one-per-kind` | **corrected**. kinds `{symbol}` → one inventory digest. |
| `fresh-process-replay-script-recomputes-complete-proof` | **corrected**. `replay_from_export.py` reconstructs the complete expected proof from admitted inputs in a fresh process. |
| `complete-proof-bundle-C-compare` | **corrected**. C(expected)==C(claimed); SHA `e9492b04…`. |
| tamper stale-hash vs semantic replay | **corrected**. Same comparison path: expected reconstructed proof versus a logical-result mutation that preserves citation membership and remints enclosing proof identity. Stale-hash control is labelled separately. |

First actual refusal on the **old** export remains `grammar-artifacts-in-closure-tree`. On the **new** export, measured `firstRefusal` is null under the joins this replay executes.

## Four boundaries kept distinct

| Boundary | This correction |
|---|---|
| Stock schema | DeclaresPayloadV1, UnitMembershipV1, four SubjectInventoryV1 records, proof-bundle, ExecutionInputsV1 validate Draft 2020-12 plus independently implemented `x-opensip-order`. Stock is not closure. |
| Helper | C/H/lexical unchanged in law. Occupancy now uses payload.path. Frame constructor/parser added. Shared `compose_expected_proof` is the reconstruction algorithm; replay loads inputs from the exported store in a separate process rather than builder memory. |
| Closure | Grammar tree membership, body-identity frame fetch/parse/join, U-4 membership, per-cell/kind inventories, DeclaresPayloadV1 selector, file inventoried-file joins, RuleProgram projection, complete proof C compare. |
| Host enforcement | Not claimed. Synthetic trusted observations only. |

## Remaining obligations (not completed by this pilot)

- TypeScript, Rust mixed-edition, syntax-data, and rust-partial-clones Runs are **not** re-graded or rebuilt here.
- Original `requirement-status.json` still records those IDs as executed from the historical pass. That over-claim is **not** reaffirmed. The 123 accept-blocking IDs remain the charter; this file does not mark them executed.
- Historical `blind-review` `ACCEPT-RECONSTRUCTABLE` is not a current verdict.
- notReached (peer, still): generic `x-opensip-digest` keyword engine; full delivery.v4 / component-manifest-schemas.v11 security metadata profile of `closure.manifestDigest`; real compiler/OS/crypto/SQLite/host authentication.
- Explanatory dictionaries, relation-rung tables, D9 envelopes, and graph-query fixtures from the original pass are **not** marked as newly executed vectors.
- A later pass must complete other language Runs and remaining scope before any whole-consumer recommendation.

A validator recheck may still refuse on notReached joins this bounded pass did not close. That is why the verdict is `PILOT_READY_FOR_VALIDATOR_RECHECK` and not admission.
