# B2-D2-r1 review

**Verdict: REQUIRED-FINDINGS.** Three required corrections remain: complete input-byte validation, actual schema admission and the promised TOML resource controls.

## Subject and live checks

Verified the 8,625-byte manifest, SHA-256 `89c0465f4bdda7a7da4dc29503408d7722e07da61cb1b86808dd0c08193e6899`, and all 37 members. All sizes and hashes match. All six product-map entries match the candidate and archive; existing parent pins match HEAD and the four new paths are absent from HEAD. Ten source authority pins and the product lock pin match.

Product main is clean at `86cf86432b22bf52d8a861d9aedbd71ed211a99a`; the candidate is detached at that base with exactly the six mapped changed/new paths. Architecture HEAD is `f8576e5c82378df3318a05bc0fed6ed4854653d8`.

Executed only the two permitted checks in the candidate worktree: the required Python 3.14 framework vector --check reproduces the committed vector bytes, and `python3 -I -B tools/tests/test_discovery_fw01.py` passes all eight tests. Additional reference probes loaded the bound oracle read-only. No Cargo, rustc, build or lane was run.

## Required findings

### B2D2-R1-RF-1: Validate bytes for every present declared evidence file before recognition

Location: crates/host/src/framework_recognition.rs:159-189 and EVIDENCE_FILES; framework_recognition_tests.rs:a_present_evidence_file_without_bytes_is_refused.

EVIDENCE_FILES is declared but never used to preflight the inputs. MissingEvidenceBytes is raised only if a selected branch calls bytes_of. For paths containing tsconfig.json and jsconfig.json, with bytes only for tsconfig.json, recognition succeeds and never notices the missing jsconfig bytes. A lone jest.config.js without package.json also succeeds without bytes, as does an unselected next/vite config when an earlier config is supplied. This contradicts the stated input/error contract that every present one of the fifteen evidence files has bytes and that a present evidence file without bytes is refused. The sole negative test covers only selected package.json.

Required change: Before any recognizer or explicit-override processing, require bytes for the intersection of paths and EVIDENCE_FILES. Keep non-evidence member content optional. Add coverage for unselected lower-priority configs, both TypeScript config names, configs without a package object, and the explicit-override case; a table over all fifteen evidence names can establish completeness.

### B2D2-R1-RF-2: Perform real schema admission before returning UnitRecognitionV1

Location: crates/host/src/framework_recognition.rs:419-439; crates/contracts/src/generated/identity.rs:6657, 7248, 7337-7358 and 7463.

canonical_bytes followed by serde_json::from_slice into the generated type does not establish the selected schema. Generated schemaVersion/recognizerVersion fields are ExactInteger rather than const-1 validators; recognized/evidence/effect arrays are ordinary Vec values without schema cardinality/uniqueness checks; InternalUnitRootV1 checks length but not its required path pattern. Thus unit_recognition can return Ok for an otherwise valid recognition with schemaVersion 2, empty evidence or duplicate results, or for root_path="..". Canonicalization and a correct recognitionId do not reject these schema violations. The loaded reference validator rejects the first three mutated recognitions. The plan and scope explicitly promise schema-valid rows and Shape on failed admission, so a successful Serde conversion is insufficient.

Required change: Use the existing exact schema-admission machinery, or an equivalently complete check of the selected UnitRecognitionV1/FrameworkRecognitionV1 definitions, before converting to the generated type. Preserve the existing identity computation. Add negative controls for const values, root/entry path patterns, array bounds and uniqueness, as well as positive reference rows. Correct the scope claim that generated deserialization alone is admission.

### B2D2-R1-RF-3: Deliver the promised TOML resource-profile and recursion-divergence controls

Location: tools/host/framework_recognition_vectors.py:UNITS/FACTS; crates/host/src/framework_recognition_tests.rs; accepted PLAN-r3.md:72-75.

The product vectors exercise malformed syntax, BOM, long integers and a large float, but contain no Cargo byte-cap, node-limit or parser-recursion controls. The accepted plan promises exact/past byte/node boundaries with usable tables and specifically labels recursion controls as product-only; the bound reference README defers them to B2-d2. The host lane does not run identity crate unit tests. A reference probe with a usable package table plus x=[ repeated 128 times around 0 returns all/recognized with src/main.rs, while the pinned product parser explicitly tests that nesting as RecursionLimit. No B2-d2 control currently establishes the intended Cargo.toml-not-toml/partial result and unknown workspace fact for that declared divergence.

Required change: Add the promised byte/node at-bound and past-bound controls with usable package/workspace tables and unrelated fields, plus labelled product-only recursion cases with stated expectations. Assert the host recognition disclosure, suppressed Cargo entry effects and cargo_workspace_fact None on resource refusal, retaining normal effects/facts for admitted controls. Keep intentional recursion divergence separate from byte-for-byte oracle equality.

## Other requested decisions

**Recognizer fidelity.** Apart from the input/admission issues above, the inspected decision rules match the reference: package-object triggers; strict-JSON failure disclosure versus admitted non-objects; workspace array/object detection; jest key/config behavior and precedence; all three dependency maps with the eleven-name hint filter; first tsconfig/jsconfig and 64 KiB JSONC check; B2-d1 YAML disposition; Cargo table predicates including inline tables; Next route prefix/suffix selection; Vite index presence; result sorting; and evidence hashes over original bytes. The exact JSON implementations share byte/depth/integer limits, duplicate-key, float, negative-zero and scalar-Unicode restrictions.

Nine constructed reference probes covered null package values, negative zero, out-of-range integers, a lone surrogate, a null jest key, invalid package plus config, competing TypeScript configs, inline Cargo tables and Unicode route order. They support the inspected branch expectations. Rust behavior was assessed statically; it was not executed in this review.

**Bounds and explicit state.** Structural checks directly exercise 32/33 results and 0/64/65 evidence files. Distinct-union entry overflow clears every entry-bearing result and retains the disclosure, including under explicit overrides. The explicit test uses Option presence, so [] wins; automatic state is partial on unresolved choices, otherwise all with entries, otherwise none. The 12 bound vectors include all four at/past split/single combinations with absent, empty and nonempty overrides. The carried B2D0REF-R3-NBO-1/R4-NBO-1 is therefore resolved.

**Identity.** hash_canonical_value with native.framework-recognition.v1 and sha256 text matches closure.rs. The u64-to-i128 ordinal cast is lossless and admitted by the exact integer profile. Identity computation is correct; it does not substitute for schema validation (RF-2).

**Inputs.** Unit-relative member paths and an optional already-resolved carrier-won list are reasonable pure J1 inputs; absence versus explicit empty remains intact. Refusing incomplete evidence is appropriate, but must cover every declared evidence file rather than only files selected on a particular branch (RF-1). Actual resolver provenance extraction remains the caller's duty.

**Vectors and canary.** The 49 unit, 12 bound, seven fact and three provenance cases provide useful agreement evidence; vector generation gates on the exact bound reference and its pinned loading closure. The canary fixture covers postinstall, build.rs, cargo wrapper config, npm/pnpm and evaluation-requiring JS/TS configs. The pure implementation hashes or ignores their bytes without interpreting named paths; the test checks that canary text does not leak into recognition. The current vectors omit malformed-row admission, unselected evidence omissions and the deferred TOML resource controls identified above.

**FW-01 and mint/environment rules.** framework_recognition.rs is included in both COVERED and PURE, with its tests excluded from production. The permitted structural checks and planted negatives pass. Inspection found no filesystem, process, network or environment read, no forbidden authority constructor and no unsafe block. Ordinary JsonInteger/String/collection construction grants no mint authority. The generated-type conversion is a shape-checking problem, not evidence of illicit minting.

## Archived evidence

Read the hashed raw logs and cross-checked their summaries. The base has 361 passes and eight failures; the candidate has 367 passes and the identical eight named failures, with equal suite counts. The six new recognition tests pass. This is baseline parity, not a fully passing host suite.

The archived all-targets Clippy command denies warnings and succeeds. Formatting is clean for both new Rust files and the edited base-clean lib.rs; no base-dirty file is excluded. All ten mutation logs show actual recognition-test failures, not compilation errors, consistent with controls.json. Environment checks pass ten tests; the operability source census passes with 114 rows and no findings. The archived verify_design result reports passed true and productQualification false. These lane successes do not establish the missing contracts described in RF-1 through RF-3.

## Boundaries

Neither repository, candidate worktree nor control files were edited. No prohibited fixture, installation, signing key, held tree or T2 store was accessed. No network, other pane or delegation. Only REVIEW.md and review.json were written in the requested review directory; permitted FW-01 controls used temporary copies. This review grants no implementation acceptance, integration, qualification or B2-d completion.
