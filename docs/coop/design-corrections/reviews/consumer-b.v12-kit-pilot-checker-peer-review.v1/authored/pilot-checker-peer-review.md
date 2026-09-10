# Pilot checker peer review

Same P4 original kit-only reviewer origin. Bounded peer review of P5 PILOT_FULL_ADMITS and producing-law checker. Not a new origin, not design coauthoring, not whole-consumer ACCEPT. Target-gap finding preserved.

**Verdict: `PILOT_FULL_ADMITS`**

Fresh isolated execution plus independent operand reconstruction: producing joins run before semantic replay; selectedRefs/file totality/accounts/outcomes reconstructed then C-equal claimed inputs; complete derived proof C (all required fields) equals the positive retained proof; tamper structurally admits then REPLAY_PROOF_MISMATCH on full proof C and enclosing H. No earlier prerequisite failure on the positive.

Not whole-consumer ACCEPT. Not product qualification. Prior target-representability FILE/PACKAGE import-target gap remains preserved and is not in this syntax-only `file@enumerated` source-endpoint pilot.

## Custody

- peer-snapshot manifest `8c3667bb36f2f7efa84eb21abaa7b93bb29c09d06fcd4a506c27f1b3d5e50639` match=True filesAllMatch=True
- export-manifest `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f` match=True
- `exports/syntax-code.store.json` `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` bytes=889218 match=True claimedRunId=`run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`
- `exports/syntax-code.tamper.store.json` `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` bytes=893046 match=True claimedRunId=`run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c`
- kit `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` match=True
- charter `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` match=True
- requirements `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` match=True
- preserved target-gap md `580e5879243a089163f239ab4984d1ab30eb7ee94e32b7a743d8bd99ebeaa168` match=True
- isolated exact-source match snapshot checker: True

Command: `/tmp/opensip-architecture-review-env/bin/python -I -B output/independent/peer_review.py`

## Isolated execution

Peer code ran only from `/private/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/checker`. Exact source at `/private/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/exact-source`. Path-only diff `/private/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/path-only.diff` sha256 `f7f02ccef5b9e45f1630452593f36769a28f9d558c8d1cfcbaab428eaf835964`. Exact standalone-checker bytes preserved. Redirected copy changes only Path/cd constants to authorized kit, this origin's exports, and this output dir.

Exports were not reminted. Claimed P5 output was not used as expected values.

## Call graph (actual, not function-name coverage)

- `Admit.run_admission`: structural phases then `_phase_replay` (joins before replay=True).
- `Replay.run` call order includes `ProducingLaw.execute` before `_evaluate` (True). execute methods: `['_load_aux', '_enum_plan_identity_and_joins', '_membership_cover_and_extents', '_expected_inventories_and_totality', '_stage_receipts', '_derive_selected_refs', '_derive_native_accounts', '_derive_cell_outcomes', '_evaluation_input_refs', '_atom_and_composition_branches', 'mark_pass']`.
- Native context admission: `_admit_native_context` at frame retain (True); `_phase_native` is a mark_pass after that retain (True).
- Complete proof C compared (True); enclosing H reconstructed from derived proof (True).
- Inventory locators harvested from claimed selectedRefs then cardinality-checked against enum-plan keys (True). Extra keys are not refused by a dedicated `if extra` (True).
- Derived `evaluationInputRefs` assigned from claimed selectedRefs after producing C-equality (True).

## Independent graph measurements

| Graph | Structural | Producing-before-replay | selectedRefs C | file totality | extra inv | Semantic | First refusal |
|---|---|---|---|---|---|---|---|
| syntax-code | ADMIT | True | True | True | [] | REPLAY_MATCH | None |
| syntax-code.tamper | ADMIT | True | True | True | [] | REPLAY_REFUSE | REPLAY_PROOF_MISMATCH |

### syntax-code

- store `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` claimed `run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`
- snapshot paths `['hello.rs']`; membership cover True
- independently derived extents `{"0-0": {"file": ["hello.rs"], "package": [], "symbol": ["hello.rs"]}, "1-0": {"file": ["hello.rs"], "package": [], "symbol": ["hello.rs"]}, "2-0": {"file": ["hello.rs"], "package": [], "symbol": ["hello.rs"]}}`
- file totality `[{"digest": "2840804605aa902abf05d88cd2d61929c341b8e2b32d794a593e5724a933a6e6", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}, {"digest": "d8bd5295d4ec09d8226001b9be6ab1293ee9db6f4493f8c2597be1b66773a317", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}, {"digest": "2840804605aa902abf05d88cd2d61929c341b8e2b32d794a593e5724a933a6e6", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}, {"digest": "d8bd5295d4ec09d8226001b9be6ab1293ee9db6f4493f8c2597be1b66773a317", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}]`
- selectedRefs reconstructed C-equal claimed: **True**
- evaluationInputRefs equals reconstructed selectedRefs ∪ execution-inputs: **True** (uses claimed selected after join: True)
- matching file facts `['fact2:852404c12751162c8a75c1c9e67465d2be7b356602fa2f663e03fa838849a717']`; atom none=false **True**
- derived subjects `['subject3:8bf8bec7e09259f035cb9fb392a27ffa0cf7e579b164c20c0181198704b6a3ab']`
- proof required fields missing `[]`; keysEqual True
- predicate required missing `[]`; value=false op=none
- proof C equal **True** derived `eb2a3bd6a2da159fd68c24436b47cdd0eaa064f0276bf83878ee4565f5fdae71` claimed `eb2a3bd6a2da159fd68c24436b47cdd0eaa064f0276bf83878ee4565f5fdae71`
- derived enclosing `{'evidenceId': 'evidence3:4746de6ff54a67c062c1d23bca7ebdb6d280f598585500b0b3821ee21a57925b', 'sealId': 'seal3:df983e7b0fe612a6fd8859db7b528bf9a47ecb38f9b01436dd6163533e18c713', 'runId': 'run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b'}` claimed `{'evidenceId': 'evidence3:4746de6ff54a67c062c1d23bca7ebdb6d280f598585500b0b3821ee21a57925b', 'sealId': 'seal3:df983e7b0fe612a6fd8859db7b528bf9a47ecb38f9b01436dd6163533e18c713', 'runId': 'run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b'}`
- extra finding frames not in proof `[]`
- witness blob present `{'111728e6d423b403382d074dbd6928b91165ee34649878169fd260046124cf8b': True}`
- policy `{'ruleId': 'file-present', 'enabled': True, 'subjectKind': 'file', 'universe': 'syntax', 'op': 'none', 'relation': 'file', 'endpoint': 'source'}`; importIds `[]`; native contexts `{'2eb761b2b1ec979d5fd90feaf671171931b589d2969d193ee96c845f0b9c329f': 'native.context.syntax.v2'}`
- producing `{'assertionCount': 80, 'executedPass': 60, 'executedFail': 0, 'notReached': 20, 'applicableCount': 60, 'inapplicableCount': 20}`

### syntax-code.tamper

- store `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` claimed `run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c`
- snapshot paths `['hello.rs']`; membership cover True
- independently derived extents `{"0-0": {"file": ["hello.rs"], "package": [], "symbol": ["hello.rs"]}, "1-0": {"file": ["hello.rs"], "package": [], "symbol": ["hello.rs"]}, "2-0": {"file": ["hello.rs"], "package": [], "symbol": ["hello.rs"]}}`
- file totality `[{"digest": "2840804605aa902abf05d88cd2d61929c341b8e2b32d794a593e5724a933a6e6", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}, {"digest": "d8bd5295d4ec09d8226001b9be6ab1293ee9db6f4493f8c2597be1b66773a317", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}, {"digest": "2840804605aa902abf05d88cd2d61929c341b8e2b32d794a593e5724a933a6e6", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}, {"digest": "d8bd5295d4ec09d8226001b9be6ab1293ee9db6f4493f8c2597be1b66773a317", "rowPaths": ["hello.rs"], "derivedExtent": ["hello.rs"], "equal": true}]`
- selectedRefs reconstructed C-equal claimed: **True**
- evaluationInputRefs equals reconstructed selectedRefs ∪ execution-inputs: **True** (uses claimed selected after join: True)
- matching file facts `['fact2:852404c12751162c8a75c1c9e67465d2be7b356602fa2f663e03fa838849a717']`; atom none=false **True**
- derived subjects `['subject3:8bf8bec7e09259f035cb9fb392a27ffa0cf7e579b164c20c0181198704b6a3ab']`
- proof required fields missing `[]`; keysEqual True
- predicate required missing `[]`; value=false op=none
- proof C equal **False** derived `eb2a3bd6a2da159fd68c24436b47cdd0eaa064f0276bf83878ee4565f5fdae71` claimed `2d2df6df77cd23dd6053d69a83e7339f4889ac206a6829f3c5bd5ad178efc9da`
- derived enclosing `{'evidenceId': 'evidence3:4746de6ff54a67c062c1d23bca7ebdb6d280f598585500b0b3821ee21a57925b', 'sealId': 'seal3:df983e7b0fe612a6fd8859db7b528bf9a47ecb38f9b01436dd6163533e18c713', 'runId': 'run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b'}` claimed `{'evidenceId': 'evidence3:a0bdd4e099cb6d53f4b6dddb98e6ca39a1787e03152abfd3adb03c8df1017b89', 'sealId': 'seal3:8e015cc38955c08d9ab78efc26130b8651e300e0503900536929dd9cda146e14', 'runId': 'run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c'}`
- extra finding frames not in proof `[]`
- witness blob present `{'111728e6d423b403382d074dbd6928b91165ee34649878169fd260046124cf8b': True}`
- policy `{'ruleId': 'file-present', 'enabled': True, 'subjectKind': 'file', 'universe': 'syntax', 'op': 'none', 'relation': 'file', 'endpoint': 'source'}`; importIds `[]`; native contexts `{'2eb761b2b1ec979d5fd90feaf671171931b589d2969d193ee96c845f0b9c329f': 'native.context.syntax.v2'}`
- producing `{'assertionCount': 80, 'executedPass': 60, 'executedFail': 0, 'notReached': 20, 'applicableCount': 60, 'inapplicableCount': 20}`

## Owner / field assertions

- **identityCompleteReplay**: evaluator-composition-contract.v3.md §7 Compare C of the COMPLETE recomputed proof and enclosing H. Checker encodes full derived_proof and compares C plus reconstructed evidence/seal/run identities.
- **enumerationFileTotality**: enumeration-contract.v1.md complete file rows[].path set equality with independently derived KindExtentV1.paths — field-specific, not schema state enum.
- **executionInputsSelectedRefs**: execution-inputs-contract.v1.md selectedRefs exact totality reconstructed from complete receipt outputRefs ∪ captured view coverageIds ∪ expected inventories ∪ Plan importIds.
- **atomNoneKnownHit**: atom-evaluation-contract.v1.md Kleene none with known match is false; occupancy file path vs nativeSubjectId.
- **compositionNoFinding**: emitWhen false ⇒ no finding3; gating complete population ⇒ verdict pass.
- **nativeContext**: native-evidence.md syntax grammar closure kind and parserVersion=semanticVersion executed at frame retain.

Field-specific file totality was executed as `rows[].path` set equality to the independently derived extent `{hello.rs}`, not as `state ∈ {complete,partial,unavailable}`. Outcome `state=complete` is derived in producing-law cell outcomes then joined, not accepted because the schema permits the token.

## Prior-claim disposition

- P5 claim: `PILOT_FULL_ADMITS` (earlier grade withdrawn by P5: True)
- Fresh measurement agrees on graph verdicts: True
- Disposition: prior claim confirmed by fresh measurement and independent operand reconstruction for original pilot scope
- peer-snapshot admission-results.json / replay JSON were not expected-value oracles

## Limitations

- Not whole-134 consumer ACCEPT, not product qualification, not graph-query reconstruction. Target-representability FILE/PACKAGE import-target gap from this origin remains preserved and is outside this syntax-only file@enumerated source-endpoint pilot.
- python -I isolates away venv site-packages because architecture-review-env/bin/python is a uv base symlink; execution restored only that env's site-packages. Peer logic was not edited.
- ENUM-INV-CARDINALITY records extra locators but the checker does not refuse extra (cell,program,kind) inventories. On these two stores extra was empty, so the omitted refuse did not hide a store defect.
- Replay._evaluate builds evaluationInputRefs from claimed selectedRefs after producing-law C equality. Equivalent on these stores because reconstructed selectedRefs C-equal claimed.
- discover_units re-execution is notReached because discovery-defaults.py is absent from the 80-file kit. Extents were still independently derived from retained membership+snapshot+scope. Satisfiable kit-bounded interpretation, not a silent skip of rows[].path totality.
- Symbol declaration rows are not recomputed (enumeration-contract host does not recompute native symbol rows). examinedPaths vs derived symbol extent is still joined.
- none=true sufficiency_v2 branch is unimplemented; Kleene none with known match is false on both graphs so the branch is not taken.
- _waived_ids always returns []. Plan waiverDigest is present as a locator; producing COMP-WAIVER-EMPTY is the executed empty-membership join. Not a live defect on these stores.
- L-NATIVE-ADMIT phase is a mark_pass; _admit_native_context actually runs at native-context frame retain. Syntax grammar closure/version joins therefore execute before replay.
- Witness/finding extra CAS objects are not scanned as a reachable-output set. Composition law: additional retained unreachable objects do not become authoritative findings. Derived findingIds empty on the positive; tamper claimed finding is not in derived proof.
- P5 snapshot admission-results.json was not used as an expected value. Fresh isolated execution is the measurement; P5 PILOT_FULL_ADMITS is a prior claim under disposition.
- No author reference code, goldens, root checkers, other origins, or network. Provenance paths in peer reports were not followed.
- No normative kit or export bytes were edited or reminted.

No normative design edit. No export remint.
