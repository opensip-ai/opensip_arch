# Blind review — consumer-b.v24, source39 closure-discipline self-audit (runtime source39.v3)

**Verdict: CHANGES_REQUIRED**

**Standing**
- **Origin.** This continues the same original blind origin `9d3dfb70-b2d3-498c-a3c1-f8de9e488514`. Fresh-origin independence is **not** claimed anew.
- **Scope.** It is an additional self-audit of this origin's existing reconstruction against the **unchanged** normative source39 kit. It is not a new design kit, not an acceptance, and not a replacement for the source39.v1 finding s39-M1.
- **Where it ran.** The audit began in runtime `consumer-b.v24-source39.v2`, which stopped before its final chain, checkpoints and review. This runtime completed it from an exact copy of that output.
- **Copied results.** A copied result is prior measured work. It is reused only where `notes/12-v3-completion.md` records why reuse is exact; every closure-dependent result was re-executed here.
- **History.** The original `consumer-b.v24` and `source39.v1` results are preserved as immutable own history.
- This review makes **no product qualification claim** and grants no implementation authorization.
- **Root admission.** External root admission of the exported bytes is a separate gate. Its outcome is unobserved here.
- **Future qualification.** Real OS/compiler/crypto/SQLite measurement, native provider execution as enforcement, host authentication and synthetic TCB enforcement are future qualification. They were explicitly not performed and are not counted as design omissions.

**Why CHANGES_REQUIRED.** It rests on the kit, not on this runtime's own work:
- **s39-M1 remains open** (U-4b assigns no tsjs `unitKind` while `UnitMembershipV1` enters PlanId).
- **No new normative owner** was supplied, and this review invents no mapping.
- **Every other stop condition now holds:**
  - all 123 requirements and 8 standing rules are executed with none failed;
  - all 27 claimed complete positives pass owning-schema admission, owner graph admission, the independent retained closure, replay and exact export;
  - all retention negatives pass;
  - custody passes.

---

## 1. Input custody

- **Manifest.** `subject/consumer-input-manifest.json` SHA-256 is `c2f2f88d2e3bebfa8fa1b521cb76d2584483eb922973d6e555fe05a15da4ad80`, parent `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`.
  - All 104 members are hash- and length-exact, with no unlisted files.
  - Verified at phase 0 (`vectors/phase0-custody.json`, `logs/v3-p0.0`) and again at the end (`runs/final-custody.json`, PASS, rows identical to phase 0).
  - The rows are identical to the source39.v1 and v2 custody rows.
- **Charter and requirements.** `charter.md` (SHA-256 `dc442d85…`) and `requirements.json` (`eb91643f…`) differ from v2's only in runtime paths. Counts are 123 requirements, 8 standing rules and 3 future items.
- **Read:**
  - the charter, requirements and kit;
  - own v2 `final-response.md` and runtime logs;
  - own `consumer-b.v24`, source39.v1 and v2 outputs (read-only);
  - the installed Python standard library and jsonschema.
- **Not used:** LIVE, author sources/models/fixtures, root artifacts, other agents' work, private logs, the web, subagents.
- **Custody gap.** None.

## 2. What the self-audit set out to test, and what it found

**The question.** Is output construction really separated from closure validation?
- Does closure derive the complete retained graph required by the owning schemas and registries, independently of what the emitter retained?
- Is replay used only after that closure admits?

**Method**
1. **Preserve and self-check own prior bytes first** (v2, `selfcheck/pre-summary.json`).
   - The source39.v1 output (636 files) was copied byte-exact to `preserved/source39-v1/`.
   - The unchanged ported code was run in fresh processes over all 63 exported stores.
   - It reproduced v1's recorded closure/replay result for all 62 stores that have a v1 record.
2. **Take the reference vocabulary from the kit** (`vectors/reference-census.json`):
   - 231 typed-prefix positions;
   - 232 `x-opensip-digest` annotations in 14 representation/retention pairs;
   - the `x-opensip-digest-domains` registry joins;
   - closureMembership and closureKinds.
3. **Build an independent retained-closure validator**, `ref/retained_graph.py`. It is kept separate from the emitter:
   - it reads only the exported content-addressed blobs (re-hashing each fetch) and the kit;
   - it imports no builder, evaluator, closure, digestlaw or native helper, and never reads the export `objectTable`.

   Starting from `run3`, it resolves:
   - every typed-prefix field in its prefix-selected identity domain (identity s3 table and composition s9.7);
   - every annotation per its representation and retention;
   - `byDomain`;
   - `domainSets` joins (`closureJoins`, `nestedIdentities`, `nestedRecords.blobJoins`, `blobJoins`, `snapshotJoins`, `contextAgreementFields`);
   - closure membership and kinds;
   - selected-import membership;
   - the payload registry;
   - Plan and snapshot joins.

   Faults are reported by obligation: LEXICAL, SCHEMA, IDENTITY, RETENTION or JOIN.
4. **Measure every v1 store with the validator before correcting anything.**

**Findings: actual helper defects, each corrected from the kit** (`tools/hc_v2.py`; `checkpoints/phase-5.json`, `phase-9.json`)

| HC | Where | Defect | Kit selector | Original failure retained |
|---|---|---|---|---|
| HC-33 | closure pipeline | Typed-prefix **output** references were never resolved and admitted before replay: proof `findingIds`, predicate `subjectId`s, rule enumerations, finding subject/fingerprint/ruleClosure and evidence arrays. Replay compared only the evaluator's own emitted object subset. | evaluator-composition-contract.v3 s7 line 74; identity s3 lines 435-439, 616-617 | v1 code ADMITs all 27 positives; the validator refuses all 63 stores (`selfcheck/pre/*.walk.json`) |
| HC-34 | replay | No exact reachable output-set equality | s7 lines 76, 328 | — |
| HC-35 | evaluator | `subject3` descriptors emitted only for subjects that produced a finding | s7 line 72 | every v1 store lacks those frames |
| HC-36 | validator (made in v2) | Typed values in workflow-owned Plan inputs treated as retention references | s7 line 74, s5 line 54; identity s3 lines 597-600, 627-631 | `logs/v2-build.4.from_scratch.log` (cmp-empty, cmp-budget) |
| HC-37 | validator (made in v3) | Plan-selection membership applied only to typed-prefix `import2` refs, not by-domain import refs | identity-schemas.v3 `closureMembership.selectedThroughOtherInput` | `preserved/v3-pre-hc37/`: the validator admitted `ts-pass~hidden-import` |
| HC-38 | validator (made in v3) | SourceUnitOwnershipV1 `unitId` derivation delegated although published | native-evidence.schemas.v2 `x-opensip-digest-law.retention.derived`, `$defs/UnitIdentityV1` | same: the validator admitted `rust-mixed~unit-id-not-derived` |

HC-14..HC-32 (source39.v1) remain in the ported code as prior corrections (`preserved/source39-v1/tools/hc_source39.py`).

**Failed attempts in my own new tools**, kept and not counted as helper corrections:
- the first remint of `retention_negatives.py` did not re-order generic canonical records (`logs/v2-negatives.0`);
- the rebind tool rewrote its own constants (restored; `notes/12`);
- the first checkpoint-9 write failed R-NEGATIVE-FIRST-REFUSAL and R-VALID-VS-INVALID-VS-EXPLANATORY, because the new negatives and census files lacked top-level `firstRefusal`/`masksLater` and classification labels. They were re-emitted (`preserved/v3-pre-labels/`, `logs/v3-record.3` → `logs/v3-record2.0`).

**Pre/post matrix** (`selfcheck/prepost-matrix.json`, v3; every cell is a fresh-process closure over exact bytes)

| Code \ bytes | source39.v1 stores | final stores |
|---|---|---|
| pre-correction helpers (`preserved/pre-hc33`) | 27/27 positives ADMIT | 27/27 ADMIT |
| corrected helpers | 26/27 REFUSE at retained closure (`PREIMAGE_MISSING typed-prefix:evaluation-subject`); `cmp-empty` references no subject, so its bytes are unchanged | 27/27 ADMIT |

Run, proof, evidence and seal identities are unchanged for every positive. The only byte delta is the added `evaluation-subject` frames.

**Consequence.** The source39.v1 exports were incomplete under composition s7, and source39.v1 closure admitted them. That was this reconstruction's defect, not the kit's. The exports below replace them.

## 3. Closure stage order and the claimed complete positives

`ref/closure.py close_run` runs:
1. owner graph admission;
2. the independent retained closure (stages 1 and 2 always both run and are reported separately);
3. semantic replay, only if 1 and 2 both admit;
4. exact reachable output-set equality.

First refusal, masked stages and stage-ordered faults are recorded.

**Exact final export claims.** Each `runs/<run>.store.json` holds the complete object table and every blob/frame keyed by raw SHA-256 (base64 JSON).

| Run | runId | store SHA-256 | bytes | blobs | objects | sealed verdict |
|---|---|---|---|---|---|---|
| cmp-base | `run3:5d35fcf55e5241861493e0965d065222abeae07c0a49d08ddc4501ab62ea2f0f` | `440d6f2369127f704de168c4034d796f05ce76a362e2a46f700289346da7ae45` | 1112861 | 202 | 75 | fail |
| cmp-budget | `run3:1d98ac938f6659668801420f8c79698e3db60440482209116634cad792aec181` | `e9f7c0bd8fa4f1013cb72b46dbb152a0a8c2190178bd988a452a7b55cc8efdf5` | 1022388 | 177 | 69 | indeterminate |
| cmp-code | `run3:9326c8c8a6357bed3529fee00eeccebf018f6c19de3587bf64382b8b375acca1` | `917c9988aa409ca060a32918dc3b70b4e1f8ec6fa22b16ba04beb70d053d938a` | 1121510 | 211 | 79 | fail |
| cmp-code-det2 | `run3:670a5bc5d8ff5c1eac682de20ae734da605189af48c827506ff2bd6729610d34` | `f2ba26fb136e0580911391855d494e9a74722d192fdb4af93b064f3440db6d0c` | 1121535 | 211 | 79 | fail |
| cmp-code-detc | `run3:90cdd3ab2ce0b4dd53bbf8a87b158f9be29f75a3c1f830bc36cc0b5736d3d1b0` | `4bdb8ed3d2e509da6345bcf2c24bd518394e7417d42c09f81f1c3b889a7a0ae5` | 1122245 | 212 | 79 | fail |
| cmp-empty | `run3:3526a8eca6e72fb608a597c328c950988b027faa4de247a0b2e6c7f503e3f1c4` | `7703a49ac29eae236fb53b14d8b8c075fb596e6dd3531e52d69922982fe2cb9a` | 1010767 | 170 | 62 | pass |
| cmp-evidence | `run3:52e8122c27fca56bf57c53afce0bd92de7cdce647ff950651ab7ed3d78ae39a8` | `bb0fd7d8c0fe4dcdb708f12bc6f1ce0fecdae2c6c9567a3a9bf2911bfc5675f9` | 1108933 | 198 | 73 | fail |
| cmp-gbase | `run3:c58194c522c8d73d193ddf2005f687ee7737bca7b87b600a3f00df43b26dbde2` | `3a30f92566b78a3dff82c0a7b731b90a4839cd3beabf8688af063d09553eaacb` | 1112858 | 202 | 75 | fail |
| cmp-gevidence | `run3:9145eb6b54534ab910316e4c1b2b1a2538bbf2ae1a07592c96a4efdb0ca4b3f4` | `39613c1af2df16905a706e88a5845ea61834ae273e779c19a1da8eba7da57ee2` | 1108930 | 198 | 73 | fail |
| cmp-gmissing | `run3:954c7b96b4056e815dfa61eb68c1b8dcd521b676bb0bef47370c7e29f0450c59` | `186a287f21721b35eaadcaba170d5faf7f8874ee99393b65b3989fba1517c583` | 1127952 | 199 | 73 | fail |
| cmp-hidden | `run3:8c9aff3547853a5cdbfbe9ae8cb7be38c178eaec818b0ce63b3e2aa6f7f3e857` | `aaf4a839530f9fe942f3140856ba5ac517da10cd3e58fedb8754cf3bb5ba3bd9` | 1095618 | 201 | 75 | pass |
| cmp-policy | `run3:e14fef7e8c4b7f1e7f074533f16005c792ee36707ecd0f6658c6c752bfa36078` | `03b5afe28add1a9caed563448d514c00f9f61fd22ef1ccbc0dbad8bcdedc2e0b` | 1128333 | 211 | 79 | fail |
| cmp-scope | `run3:8d062185f99711c8a519d3b4103ad5a21e747a323e638c37e1cc3a6a37bfe2e9` | `b0af49598b77332541eaa05a385213c1bfbe38234105ebc9fcbf9775650a3df5` | 1062626 | 194 | 69 | fail |
| cmp-waiver | `run3:a8a8137d3dc5a7c7c15511b9b41c0bdae1a47263c40aa5cf5d9c0e88bc129715` | `13ada3997c58efb4f449a7a073458b044f0c74e193713bc9e900cc5a83b5fbdd` | 1112503 | 202 | 75 | fail |
| rust-ambiguous | `run3:4725bc8dbefc4ee676f7fce51d21a41935571699dd193330f1a7c022bb9f5bdc` | `7552bce9e2a366e1ab896f10bd4af6c9417e62c0bc6aaf3ec5501465c1deb88d` | 980191 | 179 | 73 | pass |
| rust-extra-unit | `run3:faca3160c1897eed3b3c53160c6cef84fc2d638023b4b147007b0ca657e53aa1` | `8107cca3dd24b9bef332f03517f14ada301f15239754786b4353ef6642dd3691` | 969566 | 182 | 74 | pass |
| rust-mixed | `run3:c17dab38e1c1878869dd01651123e2372448fcf821994f54e1555d031cad4fbe` | `69f735463a76e2facf3b043b70aab180465dade3927de50a59598d58c079bce1` | 969145 | 182 | 74 | pass |
| rust-mixed-clones-required | `run3:085f12935f50bfc361ca2910c756239560ca72835e3208de684055655222ca1d` | `927f899f04cfe9f9115df11f3209f6b7617b76b8d2f0084cc353cf34db1572ec` | 969153 | 182 | 74 | pass |
| rust-partial | `run3:1d9d244284d91cd05b47f8d3ac430549e76a10fe55addbf2a153f5fa4f6bafa2` | `13f5c38ae9f174ef268ea4800269c5a35be702f99f7996f246ffe6c667d8b2fa` | 986094 | 158 | 62 | pass |
| rust-same-file-2021 | `run3:f5bfe8ca229d8d7d1e7173a0bd1b945834d55d2212aeaa5779a7a39a6f439b1d` | `725ffb57a9a95451b8642d1c12189b4b5f87c93e0ee07159c86ec5b1eb60c7a3` | 955189 | 171 | 68 | pass |
| syntax-code | `run3:8cc6895466e2a56c1439d8825567613d5f2e42bb3fe7d5de039f11432c4956e2` | `bf786b7c362bc64c9e28ebfd1149b743075c30c1edddc14a25c4ba93070afe49` | 945139 | 156 | 57 | pass |
| syntax-data | `run3:52a969b07ae1e4d329ca0f63324878ac59560081886d4a3552201fa04d737a85` | `3ae809acf93aa026b49249dcda08a5b8b8d1a444aeae359ad39655034f4d2bce` | 971923 | 114 | 34 | pass |
| syntax-mixed-disclosed | `run3:8c87d4306ad8e483fc7cf46c0fb15e7ee39bf9c58614c942f44f5787de6c7f85` | `8c8e19c261443ffc511934d0321dce4e6c1fb74a42f48f647f2e45168859d0a0` | 1059345 | 180 | 65 | indeterminate |
| syntax-mixed-omitted | `run3:c8a1c906ae787219dc5d10411315a3dfa1f407bb99a760edfe400d59a4559086` | `ef4a023143c168fdfecc97b6a4bf110d0762f42a1c8c02f73686a77523e36d1b` | 1013430 | 177 | 63 | pass |
| ts-clones-required | `run3:47122c4202855ab6c4557e90052272ea378ac22604ed98a29a801d98c9d424d6` | `3d16c4757a93002fdf12b3d41bf19220ac493b1a8517e0f1e0dbac4ca5a1f962` | 1112859 | 202 | 75 | pass |
| ts-fail | `run3:3809aba8571fd58014824c7331099d680536e47b1b9d60bf67cbe73c0ed8fa22` | `c6a3f764a83c4ce2bf30d99c0802882ef3607fbb87e666c78250c581949b9c3c` | 1112860 | 202 | 75 | fail |
| ts-pass | `run3:8e61b64f43fe2c36291c219e95704c5473cfbc8a741c49d57fffa42b9822b220` | `c423e7c98b468594ac5f1c5992667408896779fb1d58b1817b824c43850a25c5` | 1112852 | 202 | 75 | pass |

**Designed negative.** `syntax-mixed-falsecomplete` (`run3:2ae6cc37…`, store `10f9afaa…`) refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.

**Measured on these bytes in runtime source39.v3**
- **Owning schema** (`runs/<run>.records.json`, `logs/v3-closure.6`): every admitted record is re-validated against its owning schema, including typed scalars, stock Draft 2020-12, the `x-opensip-order` walk and the `x-opensip-digest` law. 27 positives, 0 failures.
- **From-scratch** (`runs/from-scratch.summary.json`, `logs/v3-closure.1`): one fresh process per Run. All 27 ADMIT through owner admission, retained closure, replay and reachable-set equality; the designed negative refuses.
- **Retained closure per positive:**
  - required preimages: 109–210;
  - reachable semantic outputs: 4–28, equal to the recomputed set;
  - exemptions: only the 32 workflow owner-scoped keys (HC-36);
  - unreachable, non-authoritative frames: `policy-derivation3`, and in some variants unselected closures or imports.
- **Replay export** (`runs/replay-export.summary.json`, `logs/v3-closure.5`): 27/27, each gated on a fresh `close_run` ADMIT.
  - The exported inputs, derived enumeration, 520 predicate proofs with witnesses, findings and verdict are recomputed from the retained program and evidence only.
  - C(recomputed proof) is byte-equal to the retained proof frame, and evidence/seal/Run identities are equal.
  - Every witness is byte-equal.
- **Tamper controls** (`runs/{syntax-code,ts-pass,rust-mixed}.tamper-outputs.json`, `logs/v3-closure.2-4`).
  - Controls: parameter value, citation, severity, waiver membership, enumeration, finding removed, witness, verdict, predicate value, and imported address (ts-pass only).
  - Each keeps identities and citations valid with enclosing identities reminted. Owner admission and the retained closure admit it, and replay refuses (`SEMANTIC_REPLAY_PROOF_MISMATCH`).
  - The stale-hash, missing-input and missing-output identity controls refuse before replay.
- **Replay-all** (`runs/replay-all.summary.json`, `logs/v3-closure.0`): 62 stores.
  - 29 ADMIT: the 27 positives plus the lawful controls `syntax-code~budget-exhausted` and `~explicit-endpoint-source`.
  - 33 REFUSE, first at owner graph admission with owner-named causes.
  - The independent closure also refuses 10 of those 33. The other 23 are owner-semantic laws it explicitly delegates (§8).
- **Three-valued law.** `vectors/replay-three-valued.json`.

## 4. Retention/reference-class negatives (`vectors/retention-negatives.json`, `logs/v3-neg2.1`)

**Construction.**
- One negative per applicable class of the census vocabulary, constructed from a corrected positive by an exact mutation plus an independent remint: every enclosing record is rewritten, re-ordered under its own registered selector and re-hashed, so no stale hash remains.
- Each is closed by the corrected code and by the pre-correction code (`preserved/pre-hc33`).
- Every row carries `firstRefusal`, `masksLater` and `classification`.
- **32/32 constructed and passing.** No refusal code was asserted in advance.

**First refused by the independent retained closure** (owner admission admits; replay masked)

| Class | Validator first refusal | Pre-correction code |
|---|---|---|
| subject3 descriptor missing | RETENTION PREIMAGE_MISSING | **ADMIT** |
| finding3 missing / finding-key2 missing | RETENTION PREIMAGE_MISSING | replay OUTPUT_OBJECT_MISSING |
| finding3 prefix carries a subject frame | IDENTITY FRAME_DOMAIN_NOT_ALLOWED | replay PROOF_MISMATCH |
| finding3 frame outside `$defs/finding` | SCHEMA FRAME_RECORD_REFUSED | replay PROOF_MISMATCH |
| canonical record where an H frame is required | LEXICAL FRAME_PREFIX | replay PROOF_MISMATCH |
| h-identity domainSet (subject universe names a context) | IDENTITY FRAME_DOMAIN_NOT_ALLOWED | replay PROOF_MISMATCH |
| canonical-record preimage (finding-parameters) missing | RETENTION PREIMAGE_MISSING | replay OUTPUT_PREIMAGE_MISSING |
| by-domain FindingEvidenceRef names a wrong-domain frame | IDENTITY FRAME_DOMAIN_NOT_ALLOWED | replay PROOF_MISMATCH |
| closureMembership.direct (finding.ruleClosure unselected) | JOIN CLOSURE_MEMBERSHIP_DIRECT | replay PROOF_MISMATCH |
| closureKinds (finding.ruleClosure names the evaluator closure) | JOIN CLOSURE_KIND_MISMATCH | replay PROOF_MISMATCH |

**First refused by owner graph admission** (the validator also refuses; its refusal is masked). The validator's own refusal by class:
- historical `finding2` major: SCHEMA;
- scope2 input missing: RETENTION;
- native-nested preimage-frame: RETENTION;
- non-canonical witness: LEXICAL;
- witness selector: SCHEMA;
- payload-class schema-digest join: JOIN;
- program-predicate fragment: JOIN FRAGMENT_MISMATCH;
- closure tree bytes missing: RETENTION;
- Blob length: RETENTION ARTIFACT_LENGTH_MISMATCH;
- unregistered schema document: JOIN;
- closure-tree-member: JOIN;
- capability-manifest-id derived: JOIN DERIVED_MISMATCH;
- snapshot-path: JOIN;
- clones framed body identity: RETENTION;
- nestedRecords.blobJoins: RETENTION, via the shared snapshot row;
- snapshotJoins path-and-digest: RETENTION first;
- closureJoins kind: JOIN;
- contextAgreementFields: JOIN UNIVERSE_CONTEXT_AGREEMENT;
- equalToDirect: JOIN FACT_PRODUCER_VIEW_JOIN.

**Controls**
- An extra unreferenced `finding3` frame ADMITs and is listed unreachable, non-authoritative.
- A reachable but unrecomputed `finding3` (enclosing identities reminted) is admitted by both closures and refused by replay.

**Builder input mutations**, for classes that live in native owner inputs:
- `ts-pass~hidden-import`: validator JOIN UNSELECTED_EVALUATION_IMPORT;
- `rust-mixed~unit-id-not-derived`: JOIN DERIVED_UNBOUND;
- `ts-pass~config-graph-path-outside-snapshot`: RETENTION;
- `rust-mixed~config-projection-mismatch`: refused only by owner binding, because that join is not a `domainSets` registry join.

**Not reached.** `canonical-record/owner-retained`, `raw-artifact/owner-retained` and `snapshot-path/not-joined` occur in no constructed positive. They have no negative and are not claimed.

## 5. Standalone, schema-envelope, config and query vectors

All assert their controls and exit nonzero on failure. Where each result was measured is stated; `selfcheck/v1-v2-provenance.json` records that 56 re-executed report documents equal their source39.v1 counterparts after removing process fields.

- **Phases 1–3** (measured in v2, `logs/v2-p0to3.*`): canonical/H/lexical, raw-vs-parsed, semantic-vs-operational, acyclic joins; CVE1 eight types; capability-manifest admission with four named gates, first refusal and masking (5 positives, 19 negatives); protocol3 traces (34 rows exercised, pairwise disjoint).
- **Phase 4** (v2): relation/rung table (17 rows, 6 modes); count/class/attempt rules on retained scopes and Coverage; code-vs-data matrix; enumeration vs resolution; advertised mode paths, including rust-cargo-prepared.
- **Phase 5 vectors** (v3, `logs/v3-closure.9`): Rust body-identity pairs; unsupported grammar; hidden or mismatched input per language, with first refusal and masking.
- **Phase 6** (v2): synthesized, custom multi-base and JS shared-base config; JS clone body through the TS universe; clones negatives; repair descriptor and authority; min-resolution at three levels with repair evidence; imported-observation boundary; mutation replay scope and repair-apply key; pinned purge.
- **Phase 7:**
  - v3 (`logs/v3-closure.10`, `.13`): zero-config chain to receipt; multi-unit availability with candidate-only clones; invocation, single- and multi-step; public-from-internal and four failure envelopes; D9 extension precedence; receipts and availability; run termination (28 Runs, 9 candidate checks, 30 compositions).
  - v2: discovery/membership (16 vectors).
- **Phase 8:**
  - v3 envelopes (`logs/v3-closure.11`): purge/replay/output failure; public termination goldens 45/45.
  - v2 compare: baseline audit; missing, evidence-changed, empty and scope-policy-only comparisons; E0 vs E1..E3; pivot-only fingerprints; test/preparation/repair authorization; host-captured vs candidate; empty/partial/unavailable/missing; detector compatibility file.
- **Graph query** (v3, `logs/v3-closure.12`): 53 executed vectors over Runs admitted by the complete `close_run`, 0 failures. Carrier is CommandEnvelope major 3 `querySurface=graph-query-response` with `queryResponse`; parity is read at `command-inventory.v3` `queryDispatch.parityPaths`.

## 6. Issues

### newMustIssues

**s39-M1 — U-4b assigns no `unitKind` to a tsjs unit although UnitMembershipV1 is identity** (carried from source39.v1, unresolved)
- **Selectors**
  - native-evidence.md lines 730-732: "`UnitMembershipV1` enters `PlanId` through `membershipDigest`, so every choice below is identity and none is left to an implementation".
  - native-evidence.md lines 744-748 (U-4b.2) give the tsjs unit's marker, mode, `recognizerId` and `recognizerVersion`, but no `unitKind`. Rust and fallback kinds are assigned at lines 739-740 and 854-855.
  - native-evidence.md line 622 and `native-evidence.schemas.v2.json#/$defs/WorkspaceUnitV2/properties/unitKind` give the enum `ts-program|js-program` with no mapping.
  - `enumeration-plan.schema.v1.json` `membershipDigest` feeds the analysis-spec parameter, then PlanId.
- **Measured** (`vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned`, equal to v1). One `js-allowjs` unit spelled `js-program` and `ts-program`:
  - both are schema-valid;
  - both pass `ENUMERATION_MEMBERSHIP_ORDER` / `_ROW_DERIVATION`;
  - `membershipDigest` values differ: `34d0e48f…` vs `52a0e505…`.
- **Gap.** Two conforming hosts mint different PlanIds for one repository.
- **Invention it forced.** This reconstruction chose `ts-tsconfig`→`ts-program` and `js-allowjs`/`js-synthesized`→`js-program`, measured beside the alternative. The remedy is one kit mapping row.

### newShouldIssues

None.

### Advisories (nonblocking)

**Carried from source39.v1** (kit unchanged, measurements re-executed)
- **A-c1.** Unpublished internal refusal names still carried as `cb24`: syntax grammar-capability scope variants, E0 pivot joins, detector listing, test consent relabel, native-preparation grant joins.
- **A-c2.** `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination (native s10 lines 3285-3299).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change, so gating evidence rules report INDETERMINATE `evidence-content-changed` (workflows s3 lines 440-449).
- **A-n1.** IndeterminateReason (3), the detector disposition, is unreachable for entries (workflows s3 lines 402-411).
- **A-n2.** Run-termination s6 member order: UNKNOWN_FIELD vs NOT_DERIVED; both refuse.
- **A-n3.** Run-termination non-object candidate has no published key; the indeterminate key is a wildcard.
- **A-n4.** Run-termination s7.3 commit-inventory member set is fixed by a reference path. Operational only.
- **A-n5.** U-4b.2 "deepest workspace" is self-referential for nested workspaces. Unmeasured; Cargo rejects them.
- **A-n6.** U-4b does not restate a rust unit's languageMode; it is derivable.

**New in this self-audit**
- **A-v2-1. Typed-prefix closure boundary for workflow-owned Plan input documents.**
  - Composition s7 line 74 closes the reference fields of *outputs*.
  - Whether schema-declared typed values inside workflow-owned Plan inputs are closure references is unstated. Examples: WaiverSetV1 `target.fingerprint`, PolicyDocumentV2 import addresses.
  - A literal all-schemas reading makes the lawful `cmp-empty`/`cmp-budget` unclosable (`logs/v2-build.4.from_scratch.log`).
  - The deterministic reading comes from s7 "these outputs", s5 waiver equality and identity s3 lines 597-600/627-631. One scoping sentence would settle it.
- **A-v2-2. `policy-derivation3` is outside the reachable output set.**
  - It is constructed (s7 line 70, s9.7) but referenced by no run3/seal3/evidence3/proof3 field, so reachable-set equality cannot include it.
  - Exports retain it as an unreachable, non-authoritative frame.
- **A-v2-3. Identity s3 "closed" wording.**
  - Identity s3 lines 441-467 call the representations and retention modes closed and close `derived`/`owner-retained` to single identity fields.
  - The native and relation digest laws publish further modes and representations (census counts).
  - Each bundle's law is the deterministic owner, but a literal cross-bundle reading would refuse lawful fields.

**What required invention.** Only s39-M1 (the `unitKind` mapping). The HC-33..HC-38 corrections each followed a precise kit sentence and were helper defects, not design gaps.

## 7. Requirement dispositions

`requirement-status.json` holds one row per ID; checkpoints are `checkpoints/phase-0.json` … `phase-11.json`, each carrying the unioned ID set.

| Phase | IDs | Disposition and principal evidence |
|---|---|---|
| 0 custody | S-FRESH-ORIGIN, S-NOT-PRODUCT, S-KIT-ONLY, S-MANIFEST-VERIFY, S-NO-ORACLE, S-MISSING-DEP-IS-CUSTODY, S-PROFILE-CURRENT, S-CONTINUATION, R-FIVE-CONTRACTS-INDEX, R-SOURCE-MAP-SCOPE, R-CVE1-TYPES-AVAILABLE | executed in v3 (`vectors/phase0-custody.json`); continuation, independence not claimed anew |
| 1 | R-H-HELPER, R-CVE1-EIGHT-TYPES, R-LEXICAL-ADMISSION, R-SEMANTIC-VS-OPERATIONAL, R-RAW-VS-PARSED, R-ACYCLIC-JOINS | executed (v2 measurement, reused) |
| 2 | R-CAP-ADMISSION, R-CAP-NAMED-GATES | executed (v2) |
| 3 | R-TRACE-COMPLETE, -UNAVAILABLE, -CANCEL, -FAULT, -IDENTITY-BEFORE-SOURCE, -TERMINAL, -EXECUTED-VS-HOST | executed (v2) |
| 4 | R-RELATION-RUNG-TABLE, R-COUNT-CLASS-ATTEMPT, R-CODE-VS-DATA-MATRIX, R-ENUM-VS-RESOLUTION, R-ADVERTISED-MODE-PATHS | executed (v2 tables; gate re-read from v3 phase-5 log) |
| 5 complete Runs | R-RUN-TS, -TS-NODE-MODULES, -TS-CONFIG-DEPS, -RUST, -RUST-MIXED-EDITION, -RUST-TARGET-EDITION, -RUST-BODY-DIALECT, -RUST-SAME-FILE-TWO-EDITIONS, -RUST-PARTIAL-EMPTY-CLONES, -RUST-HASH-MARKER, -RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE, -RUST-LARGE-EDITION-MAP, -RUST-VERSION-COMPONENT, -FILE-FACT-INVENTORY, -CLONES-L0-AND-NORMALIZED, -CLONES-CUSTODY, -SYNTAX-CODE, -SYNTAX-DATA, -NO-COMPILER-UNIT, -UNAVAILABLE-SEMANTIC, -UNSUPPORTED-GRAMMAR, -NONCEMPTY-CONTEXT, R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC, R-IMPORTED-PAYLOAD-IN-GRAPH, R-CLONE-DEFICIENCY-PAIRING, R-HIDDEN-MISMATCH-PER-LANGUAGE, R-NATIVE-PREIMAGE-JOINS | executed: stores built in v2 after HC-35, every store closed again in v3 with the four-stage pipeline |
| 6 | R-CONFIG-SYNTHESIZED, -CUSTOM-MULTI-BASE, -JS-SHARED-BASE, R-JS-CLONE-BODY-THROUGH-TS, R-CLONES-NEGATIVE-VECTORS, R-REPAIR-DESCRIPTOR, R-REPAIR-AUTHORITY-PER-TARGET, R-MIN-RESOLUTION-THREE-LEVELS, R-MIN-RESOLUTION-REPAIR-EVIDENCE, R-IMPORTED-OBSERVATION-BOUNDARY, R-MUTATION-REPLAY-SCOPE, R-REPAIR-APPLY-KEY, R-PINNED-PURGE | executed (v2 vectors, no closure stage) |
| 7 | R-CHAIN-ZERO-CONFIG-TO-RECEIPT, R-SEMANTIC-VS-OPERATIONAL-AUTHORITY, R-MUTATION-VS-ANALYSIS-STEPS, R-MULTI-UNIT-MISSING-CAPS, R-CANDIDATE-ONLY-CLONES, R-INVOCATION-DISCLOSURE, R-SINGLE-STEP, R-MULTI-STEP-DIFFERENT-SELECTIONS, R-PROMISE-VS-AVAILABILITY, R-PUBLIC-FROM-INTERNAL-REFUSAL, R-ENVELOPE-CONFIG-INPUT, -EXTERNAL-INPUT, -HOST-INVALID, -PRODUCER-BOUNDARY, R-FAILURE-ENVELOPES-D9, R-D9-EXTENSION-PRECEDENCE, R-DURABLE-RECEIPT-AVAILABILITY | executed (phase-7 and run-termination vectors in v3; discovery in v2) |
| 8 | R-BASELINE-AUDIT, R-CMP-MISSING, R-CMP-EVIDENCE-CHANGED, R-CMP-EMPTY-RESULT, R-TEST-PREP-REPAIR-AUTH, R-PURGE-REPLAY-OUTPUT-FAILURE, R-SCOPE-POLICY-ONLY-COMPARISON, R-PUBLIC-TERMINATION-EXAMPLES, R-SUBSYSTEM-OWNERS, R-E0-VS-E1-E3, R-PIVOT-ONLY-FINGERPRINTS, R-HOST-CAPTURED-VS-CANDIDATE, R-EMPTY-PARTIAL-UNAVAILABLE-MISSING, R-DETECTOR-COMPAT-FILE | executed (envelopes in v3; compare in v2) |
| 9 | R-VALIDATE-OWNING-SCHEMA, R-INDEPENDENT-CLOSURE-JOINS, R-OBJECT-TABLE-FRAMES, R-FROM-SCRATCH-COMMAND, R-RETAINED-ARTIFACTS-IN-CLOSURE, R-SELECTED-PROVIDER-CONTEXT, R-VALID-VS-INVALID-VS-EXPLANATORY, R-MEASURED-NOT-COUNTS, R-NEGATIVE-FIRST-REFUSAL, R-DISTINGUISH-FOUR-BOUNDARIES, R-HELPER-KIT-ONLY, R-REPLAY-AFTER-ADMISSION, R-REPLAY-ENUM-AND-IDS, R-REPLAY-PREDICATE-WITNESS-VERDICT, R-REPLAY-NO-CALLER-TRUTH, R-REPLAY-COMPARE-BUNDLE, R-REPLAY-EXPORT, R-REPLAY-THREE-VALUED, R-REPLAY-TAMPER, R-ROOT-ADMISSION-EXPORT, R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR | executed in v3 (checkpoint 9 rewritten after the artifact-shape fix; root outcome unobserved) |
| 10 | R-IDENTIFY-GAPS, R-FREEDOM-VS-MISSING, R-BLOCKER-NOT-ADJUST | executed (`notes/10-gaps.md`) |
| 11 | R-DELIVER-MD-JSON, R-VERDICT-ENUM, R-MUST-SHOULD-ADVISORY, R-NO-ACCEPT-IF-INCOMPLETE, R-NO-QUALIFICATION-CLAIM | executed by the phase-11 check of these two files (`checkpoints/phase-11.json`, `logs/v3-phase11.*`) |

Final counts (`blind-review.json#/counts`):
- 123 requirements plus 8 standing rules, 131 in total: 131 executed, 0 unexecuted, 0 failed.
- 3 future-qualification items: not claimed.
- 27 claimed complete positives.
| future | F-OS-COMPILER-CRYPTO-SQLITE, F-SYNTHETIC-TCB, F-AUTH-HOST | futureQualification: not demanded, not claimed |

## 8. Limitations

- **Walker scope** (`ref/retained_graph.py`).
  - Executed: retention, identity, schema and registry joins, closure membership/kinds, selected imports and SourceUnitOwnershipV1 `unitId` derivation.
  - Delegated to owner graph admission, which runs as its own stage in every closure:
    - `languageVersionBinding` derivation;
    - clones body-identity parse joins;
    - native context/universe admission and binding (including the rust `configProjectionSha256` join);
    - enumeration and execution-input derivation;
    - import grant and staleness;
    - parameter cardinality;
    - pruned-read and scope-capability laws.

    23 refused mutation stores are refused by owner admission alone for these reasons.
- **Census classes with no constructed positive** have no negative (§4).
- **Run-termination.** s7.5 row 2 and s5 stage-terminal carriers are not constructed from built Runs.
- **Result reuse.** Some results that don't involve the retained-closure stage were measured in v2 and reused with mtime evidence (`notes/12-v3-completion.md`). Every closure-dependent result was re-executed in v3.
- **Negatives execution.** Negatives are closed in-process by the corrected code and in fresh processes by the pre-correction code.
- **Root admission** of these exports is unobserved.
- **Future qualification** was not performed.

## 9. From-scratch commands

Run from `/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3/output`:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py          # four-stage close_run per positive, fresh process each
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py         # admission-gated replay export of inputs, derivation and complete proof
/tmp/opensip-architecture-review-env/bin/python -I -B tools/walk_run.py runs/<run>.store.json <dst>   # independent retained closure alone
/tmp/opensip-architecture-review-env/bin/python -I -B tools/retention_negatives.py   # class negatives (post and pre-correction code)
```

The full set is in `notes/09-reconstruction.md`. The self-audit narrative is in `notes/11-v2-self-audit.md`, and the completion ledger in `notes/12-v3-completion.md`.
