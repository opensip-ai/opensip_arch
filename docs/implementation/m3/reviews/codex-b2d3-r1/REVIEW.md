# B2-D3-r1 review

**Verdict: REQUIRED-FINDINGS.** Two parts of the returned evidence are narrower than accepted plan section 5: detected results and resolved choice effects. The resolver gate and lead precedence/projection decisions otherwise appear sound.

## Subject and live checks

Rehashed the 7,859-byte subject manifest, SHA-256 `c639b15987529ddd1171e9662c2db4c24dfac09cef49a7e19095957575850c76`, and all 34 members. All sizes and hashes match. All five product-map entries match candidate and archive; existing parents match HEAD and the two new paths are absent from HEAD. Source authority pins and product-lock pin match.

Product main is clean at `b68ddee1a4f915a395ca358b6c7e43203b7e6817`; the candidate is detached at that base with exactly the five mapped changes. Architecture HEAD is `4effe02769ded999749b2e99fadfbb38b30c7b4a`.

Executed only the permitted `python3 -I -B tools/tests/test_discovery_fw01.py` in the candidate: all eight tests pass. No Cargo, rustc, build, lane or other product test was run. Counterexamples below are based on source inspection, not claimed Rust executions.

## Required findings

### B2D3-R1-RF-1: Retain the recognized results in detected evidence

Location: crates/host/src/recommendation.rs:43-50 and 258-274; PLAN-r3.md section 5.

The accepted plan requires detected evidence to contain the recognized results with their evidence. DetectedEvidence retains only Source, provenance and evidence tuples, dropping assurance and all effects. This loses information precisely when a setting is not proposed. For example, two partial Next.js recognitions with identical config bytes/root but pages/a.tsx versus pages/b.tsx produce the same returned evidence: entry proposals are suppressed, config evidence and unresolved choices are identical, and the same ignore directory is proposed. The detected route entries disappear. Test globs also have no representation in the returned payload. The M4 renderer cannot present the detected results from RecommendationEvidenceV1 alone.

Required change: Retain each complete recognized result, or an equivalent lossless internal representation, with its unit and provenance. Keep detected unit-relative effects separate from projected project settings. Add a control showing that differing detected entry effects remain visible when partial recognition or explicit configuration suppresses entry proposals; include assurance and test-glob retention.

### B2D3-R1-RF-2: Return resolved configurations for each choice effect, not only their digests

Location: crates/host/src/recommendation.rs:59-68, 84-95 and round_trip; PLAN-r3.md section 5.

The accepted plan defines the effect of each choice as the resolved configuration with and without each proposed setting. round_trip computes a ResolvedConfigurationV1 but discards it, retaining only its digest and the selected path list. RecommendationEvidenceV1 likewise retains only base_digest. These opaque hashes do not provide the resolved configurations required by the plan or let the future renderer inspect the actual before/after values and provenance. Current tests recompute the resolutions outside the returned evidence and compare digests, so they do not establish this payload requirement.

Required change: Retain the actual base resolved configuration and the resolved configuration for each admitted proposed setting, or equivalent complete resolved-value evidence, while keeping digests as useful identities. Ensure the returned before/after records equal actual resolve outputs, including applying none; preserve carrier fields and the read-only behavior. Update the scope and tests to assert the returned effect records, rather than only recomputing and comparing digests.

## Requested decision assessment

**Item 18 and CH13.** The function is pure, exposed by discovery.rs and uses the actual resolver. Proposed settings, rationale codes, recognizer unresolved choices and per-unit hints are present. Detected evidence and effect evidence are lossy as described in RF-1/RF-2; having five named fields is not sufficient to meet the settled plan payload. Internal types remain appropriate at M3; no public wire schema or command is needed.

**LD-B2D3-1: acceptable.** Winning-leaf provenance distinguishes absence from explicit arrays, including []. A higher-layer empty list is respected. Requiring every supplied unit state to be all before replacing project entryPoints is conservative and prevents a proposal assembled only from complete units from silently overriding incomplete units. The code carries unresolved choices instead of proposing incomplete entry sets.

**LD-B2D3-2: acceptable within its stated scope.** Existing ignorePaths, including an empty list, are protected by the same winning-leaf check. Mapping a directory convention d/ to the concrete unit-root directory <root>/d is consistent with the logical-path field, whose empty final segment is refused. Checking candidates individually preserves usable suggestions when another is refused. This is a concrete directory recommendation, not a recursive glob: nested node_modules below the unit root is not captured, and the type makes no completeness claim for all occurrences. It should not be rendered later as such a claim. No broader scanning or recursive ignore inference is required in this unit.

**LD-B2D3-3: acceptable.** apply_setting clones the resolver input, preserves an existing project carrier's path and other fields, and creates schemaVersion 2 opensip.json only when no project carrier exists. Every result still passes the actual resolver. A supported carrier that cannot admit a new setting produces unresolved evidence rather than a false proposal.

**LD-B2D3-4: acceptable.** The round trip compares both sorted path values and cardinality, then returns the resolver's order. This preserves the exact path set while allowing the resolver's selected canonical ordering.

**LD-B2D3-5: acceptable.** Unit-root projection is applied only to proposed settings. Equal project paths merge while retaining all proposal sources. Recognition paths remain unit-relative. The collision test and two-unit round-trip test establish the intended projection and provenance behavior.

**Resolver and no-write behavior.** Every emitted field passes apply_setting and resolve, followed by exact path-set comparison. Both individual ignore candidates and the final aggregate are checked. Refused proposals are unresolved rather than emitted. Base refusal is returned unchanged; base resolution occurs on the unmodified input. All carrier changes are in memory. Returning the complete resolved base/effects remains required by RF-2.

**Exposure and rules.** The discovery.rs re-export is limited to the internal function/type, with a scoped unused-import allowance because M3 has no caller. The body stays in recommendation.rs. The module is covered and pure under FW-01; tests are excluded from production. Inspection found no filesystem/process/network/environment access, unsafe block or forbidden authority constructor. Ordinary exact-integer/string/collection construction does not grant mint authority.

## Tests and archived evidence

The six tests use the reviewed configuration-vector base defaults and exercise actual resolver round trips, equal-path merging, absent/explicit-empty/higher-empty entry controls, partial recognition, individual ignore refusal, hints, carrier preservation and unchanged base-refusal propagation. They are useful and pass in the archived lane, but do not assert retention of complete detected results or resolved effect records. The existing complete/incomplete and ignore-directory behaviors need not change to fix those omissions.

Cross-checked the hashed raw logs and summaries: base **370 passes / 8 failures**, candidate **376 passes / 8 failures**, identical eight named failures and equal suite counts. All six new recommendation tests pass. This is requested baseline parity, not a failure-free host suite. All eight mutation logs show actual recommendation-test failures rather than compilation failure, matching controls.json.

Formatting is clean for both new Rust files and the edited base-clean discovery.rs/lib.rs; no base-dirty exclusions. Warning-denied all-targets host Clippy passes. Archived recognition/YAML vector checks, FW-01, ten environment checks, the 114-row operability census and verify_design pass. verify_design reports productQualification false. Those results do not supply the missing returned payload content.

## Boundaries

Neither repository, candidate worktree nor control files were edited. No prohibited private fixture, installation directory, signing key, held tree or T2 store was accessed. No network, other pane or delegation. Only REVIEW.md and review.json were written in the requested review directory; permitted FW-01 controls used temporary copies. No acceptance, integration, inventory binding, qualification or B2-d completion is granted here.
