# B2-D2-r2 review

**Verdict: ACCEPT-UNIT.** All three round-1 required findings are resolved. No new blocking issue or nonblocking observation found.

## Subject verification

Verified the 16,009-byte manifest, SHA-256 `34aaf0b29b3f4ddfe293843d6ddf84db6fdaa36fd5f1c93e8fdb4b4ca30b3e16`, and rehashed all 67 members. All pins match. Product-map entries match candidate and archived bytes, parent pins match HEAD, and new paths are absent from HEAD. Source authority pins and the product lock pin match.

Product main is clean at `86cf86432b22bf52d8a861d9aedbd71ed211a99a`; the candidate is detached at that base with exactly the six mapped changes. Architecture HEAD is `f8576e5c82378df3318a05bc0fed6ed4854653d8`.

## Prior-finding disposition

**B2D2-R1-RF-1: resolved.** Evidence preflight is the first operation in recognize, before any parser, recognizer selection or explicit override. It checks every EVIDENCE_FILES name present in paths and returns MissingEvidenceBytes for the first missing name in the declared order. Non-evidence member content remains optional. Tests exercise all fifteen names with absent/empty overrides, lower-priority unselected configs, a jest config without package.json and optional ordinary member bytes. The new preflight-removal mutant is caught.

**B2D2-R1-RF-2: resolved.** unit_recognition now admits the whole canonical row using RegisteredSchemas at `opensip.product.framework-recognition-plan.1#/$defs/UnitRecognitionV1` before generated deserialization. SchemaHandle::admit_json converts a completed mismatch to an error; registry, validation and budget errors all map to Shape. The 64 * 1024 * 1024 budget is finite metered admission work, not a larger JSON byte allowance. Existing canonical byte/depth bounds still apply. Archived reference and maximum-entry cases admit under this budget; no bypass or budget-related regression was found.

Generated Serde conversion alone still does not prove schema validity, but it is no longer used as that proof. The actual schema check enforces constants, paths, bounds and uniqueness. Negative cases cover version constants, empty evidence, duplicate results, absolute entry paths, unresolved-choice cardinality, unknown state and invalid roots. The admission-removal mutant is caught. Identity computation remains unchanged and matches closure.rs.

**B2D2-R1-RF-3: resolved.** Seven new TOML profile cases cover exactly 4 MiB and one past, exactly 1,000,000 below-root nodes and one past, two labelled product-only recursion refusals, and an admitted shallower control. Both workspace and package tables precede the unrelated fields. The node count correctly includes workspace, members, package, name and x before array elements.

The reference-equal cases check summaries, recognitionId and Cargo-workspace fact. The 128-array and 100-dotted-key cases independently state the product expectation: Cargo.toml-not-toml, zero Cargo entries, partial state and unknown workspace fact. Their differing reference summaries are recorded as comparison evidence, not used as product expectations. The generator requires that the labelled divergence actually differs. Rust tests reconstruct the documents and check their lengths, results and facts. This correctly separates intentional recursion divergence from reference equality.

## Fidelity, inputs and evidence coverage

The production diff from r1 adds preflight and schema admission without changing the nine recognizer rules. Package JSON admission, admitted non-objects, config priority, JSONC/YAML/TOML dispositions, inline table detection, hints, route selection, sorting, byte-based evidence hashing, structural bounds, per-unit distinct-union overflow and explicit-empty precedence remain consistent with the bound reference. Every retained result stays bounded under an override. Unit-relative paths and the empty semantic discovery fold remain unchanged; FR-6 through FR-8 are not introduced.

Additional read-only reference probes covered non-object package JSON, negative zero, duplicate keys, a null jest key, competing TypeScript configs, inline Cargo tables, explicit empty override over unresolved discovery, non-UTF-8 config bytes and shallow/deep Cargo nesting. These support the inspected rule expectations. Rust was not executed by this reviewer.

The vector set has 49 unit, 12 entry-bound, seven TOML profile, seven fact and three provenance cases. The full entry-bound matrix includes explicit-nonempty single-result overflow, so the carried B2D0REF-R3-NBO-1/R4-NBO-1 remains resolved. Direct structural/union tests and the canary fixture remain appropriate. The input contract is suitable for J1: admitted member paths, complete declared evidence bytes and an already-resolved optional carrier-won entry list. C4's Plan commitment and explicit list retention remain separate.

## Live and archived validation

Executed only the permitted candidate commands:

- Python 3.14 framework vector --check: passed, reproducing committed bytes from the pinned oracle and loading closure.
- `python3 -I -B tools/tests/test_discovery_fw01.py`: eight tests passed, including temporary-copy negative controls.

Cross-checked the hashed lane logs and summaries. Final host totals are **361 passed / 8 failed at base** and **370 passed / 8 failed at candidate**, with the identical eight named baseline failures and equal suite counts. All nine recognition tests pass. This is the requested failure-set parity, not a claim that the host suite has no failures.

Final formatting classifications are clean for the edited/new Rust files, with no base-dirty exclusions. Warning-denied all-targets host Clippy passes. All twelve mutation logs show actual failed recognition tests, not compilation failure. Environment checks, the 114-row operability source census and verify_design pass; verify_design reports productQualification false.

Attempt 1 is retained and marked failed solely for Clippy collapsible_if in the schema negative test. The current let-chain addresses that diagnostic; the final lane passes. Attempt 1's other checks and twelve mutations are preserved as history rather than substituted for final validation.

## FW-01 and scope

The recognizer remains COVERED and PURE, with its tests excluded from production. Inspection and permitted structural checks show no environment, filesystem, process, socket or publication access, forbidden authority constructor or unsafe block. The ordinal cast is lossless; ordinary exact-integer construction is not mint authority. Added schema admission is pure, using the supplied registered schema set. Canary config bytes are hashed or ignored, never evaluated.

This acceptance covers the exact B2-d2 library unit and its evidence. No caller, Plan commitment, recommendation evidence, inventory binding, qualification or B2-d/B2/M3-B completion is claimed.

Neither repository, candidate worktree nor control files were edited. No Cargo, rustc, build or lane was run. No network, other pane or delegation; no prohibited fixture, installation, signing key, held tree or T2 store was accessed. Only REVIEW.md and review.json were written in this review directory; permitted FW-01 controls used their own temporary copies.
