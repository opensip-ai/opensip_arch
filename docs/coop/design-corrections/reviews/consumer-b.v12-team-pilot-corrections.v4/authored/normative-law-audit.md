# Normative law audit — identity-and-evidence.md §3 (entire) after existing-law remint

This inventory covers **every paragraph** of `docs/v2/contracts/product-v1/identity-and-evidence.md` §3 (lines **87–1349**). It is a completeness check, **not** a substitute for execution. Each EXECUTED/KIT row names the checker function and measured operands in `normative-law-audit.json#/positiveLaws` (and `#/tamperLaws`).

Charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` (ORIGINAL TASK REQUIREMENTS). Checker: `helper/s3_closure.py` `execute_s3_laws` / `execute_kit_s3_schema_laws`, invoked from `admit_graph` and `probes/normative_s3_audit.py`.

**Paragraphs:** 115. Unmapped: 0. Applicable-without-assertion: 0.

| disposition | count |
|---|---:|
| EXECUTED | 75 |
| KIT (kit-document law executed on frozen schemas) | 9 |
| N/A (not fields of this syntax-only graph) | 21 |
| META (heading / lead-in) | 9 |
| WITHDRAWN (replaced by payload registry) | 1 |

## Graphs (reminted this pass)

| Graph | Store | Structural §3 | Independent expected proof | Semantic C |
|---|---|---|---|---|
| Positive | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` `run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b` | PASS firstRefusal none | `proof3:8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521` `usedClaimedProofFields=[]` | equal |
| Tamper | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` `run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c` | PASS firstRefusal none | same expected `proof3:8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521` | **unequal** (claimed fail vs derived pass) |

Expected proof is reconstructed from Plan, ExecutionInputs, policy projection, view/facts/coverage/inventories. Claimed proof fields are comparison operands only. Predicate `inputRefs` are a subset of `evaluationInputRefs` (domains coverage+view only). Program bound by `proof.ruleProgramDigest` = `77b07390ddee3917485d15bdde2ab408992ec77236693895e7bc1e681ea66b8e`.

## Existing-law reconstruction (not a new design)

S-origin claimed proofs cited `domain=rule-program` on `predicate.inputRefs` while `evaluationInputRefs` lawfully omitted it (shape B). That violated identity §3 subset MUST. Jointly satisfying shape A omits the citation and binds the program through required digest fields. Checker no longer skips that member. Graph identities **were reminted** because the miss was in the claimed proof record, not merely an unimplemented assertion.

N/A (not invented, not demanded): TS stdlib/rustc LLVM closures, nested rust dependency/cargo/prepared-output identities, ScopeDocumentV1 comparison binding, vcs-change.previousPath, commit-receipt, owner-source-set.

notReached (charter): L1 tokenisation judgment (level-spec freedom; frame/custody executed); component-manifest-schemas.v11 stock schema (prose field contract); ROOT-ADMISSION.

## Paragraph inventory

See `normative-law-audit.json#/paragraphs` for the 115-row table (same map as the S-origin audit; execution now includes `S3-PRED-INPUTREFS-SUBSET-OF-EVALUATIONINPUTREFS` and `S3-EXPECTED-PROOF-PRED-INPUTREFS-SUBSET` with no rule-program skip). S-origin audit bytes preserved at `preserved-failures/syntax-code-s-origin-pilot-v3/normative-law-audit.json`.
