# B2-D3-r2 review

**Verdict: ACCEPT-UNIT.** Both round-1 required findings are resolved. No new blocking issue or nonblocking observation found. The mutation-control disposition is sound.

## Verified subject

Rehashed the 14,734-byte subject manifest, SHA-256 `a07a1782438a4ae47a9c3e390db447e439fcd921d78c56b13a704560d249c881`, and all 62 members. Every byte count and hash matches. All five product-map entries match candidate and archive, existing parent pins match HEAD, and the two new paths are absent from HEAD. Source authority pins and the product lock match.

Product main is clean at `b68ddee1a4f915a395ca358b6c7e43203b7e6817`; the candidate is detached at that base with exactly the five mapped changes. Architecture HEAD is `4effe02769ded999749b2e99fadfbb38b30c7b4a`.

## Round-1 findings

**B2D3-R1-RF-1: resolved.** DetectedUnit retains each supplied unit's complete recognition value unchanged, together with ordinal, root and per-result provenance in result order. Assurance, evidence, all effects, unresolved choices, hints and entry state remain available, including for a unit with no recognized result. Detected effects remain unit-relative; project projection applies only to proposals.

The new test keeps distinct partial Next.js route sets visible despite no entry proposal, both with absent configuration and explicit []. It also checks assurance, test globs and vitest-jest provenance. Existing controls assert equality with a complete input recognition. The detected-recognition-dropped mutation is caught.

**B2D3-R1-RF-2: resolved.** The returned base is the actual complete resolve(input) result. Each setting retains a complete resolved_with, including semantic and operational values, winning-leaf provenance and digest. Tests compare those records against actual resolver outputs, rather than only comparing hashes.

The presentation-order correction is necessary and correct. Initial resolution can reorder paths; the project carrier hash in provenance still reflects the initial order. When ordering changes, round_trip now applies the displayed order and resolves again, requiring that order to be stable. in_order presents exactly those paths. Thus resolve(apply_setting(input, presented_paths)) equals the returned resolved_with, including carrier provenance. The effect-not-presented-order mutant is caught by the full-record equality control. Applying none returns the original input's resolution unchanged.

## Attempt-1 mutation disposition

Attempt 1 honestly records a failed mutation aggregate: only round-trip-skipped survived. That version removed the set/cardinality comparison, not application of the proposal or resolver admission. In this function's reachable context, the field was absent, proposal paths were merged uniquely, and the strict resolver admits the submitted path array or refuses it. Its normalization sorts these strings without adding or removing values. The mismatch branch therefore cannot distinguish this mutant under the current resolver contract.

Replacing that mutant with one resolving the unchanged input instead of the proposal meaningfully removes the mechanism being tested. The final mutation is caught by six recommendation tests. The original history and surviving-mutant result remain retained; they are not represented as successful negative evidence.

Keep the set-equality guard as a fail-closed defensive invariant. Removing it is unnecessary, and introducing a fake resolver merely to reach a behavior the actual resolver cannot produce is not required for this unit. If resolver semantics later change to transform this path set, this guard and its coverage should be reconsidered with that change. The final lane's ten caught mutants do not imply that every defensive branch has a distinguishing control.

## Item 18, CH13 and lead decisions

All five planned parts are now present: lossless detected evidence, proposed settings with sources, default rationale, unresolved choices/hints, and actual resolved choice effects. The evidence remains an internal M3 type and no command is wired.

LD-B2D3-1 remains appropriate: no winning entryPoints leaf, including no explicit [], and every unit state all are required before proposing an entry list. This avoids replacing incomplete-unit defaults with a list assembled from complete units alone. Higher-layer empty replacement remains protected.

LD-B2D3-2 remains acceptable as a concrete directory recommendation. Ignore paths are proposed only when absent. A convention d/ is projected to <unit-root>/d, each candidate is checked alone, and the final aggregate is checked again. Nested node_modules directories are not captured by this concrete path; the evidence does not claim recursive or exhaustive coverage. No broader scan or glob inference is introduced.

LD-B2D3-3 through 5 remain correct: proposals use the existing project carrier without dropping other fields, or create an in-memory schemaVersion 2 opensip.json; exact path sets may use resolver order; unit-root projection distinguishes colliding relative names and merges equal project paths with every source. Retained recognition rows are unchanged. Resolver refusals or changed values never become emitted proposals; refused base input is returned unchanged.

The discovery.rs re-export, scoped unused-import allowance and separate implementation module conform to the settled exposure. No public record, writer or caller is added.

## Validation and evidence

Executed the only permitted candidate test command, `python3 -I -B tools/tests/test_discovery_fw01.py`: all eight checks pass, including temporary-copy negative controls. No Cargo, rustc, build, lane or other product test was executed by this reviewer.

Cross-checked the archived raw logs and summaries. The final lane records **370 passes / 8 failures at base**, **377 passes / 8 failures at candidate**, the same eight named failures and equal suite counts. All seven recommendation tests pass. This is baseline parity, not a fully passing host suite.

All ten final mutation logs show actual failed recommendation tests rather than compilation failure. Formatting is clean for both new Rust files and the base-clean edited discovery.rs/lib.rs, with no base-dirty exclusions. Warning-denied all-targets Clippy passes. Archived recognition/YAML vector checks, ten environment checks, the 114-row operability source census and verify_design pass; verify_design reports productQualification false.

The production code remains COVERED and PURE under FW-01, with test code excluded. No filesystem, process, network, environment or publication operation, unsafe block or forbidden authority constructor was found. All carrier changes are in memory. Ordinary strings, collections and exact integers confer no mint authority.

## Boundaries and scope

Neither repository, candidate worktree nor control files were edited. No prohibited private fixture, installation directory, signing key, held tree or T2 store was accessed. No network, other pane or delegation. Only REVIEW.md and review.json were written in the requested directory; permitted FW-01 controls used temporary copies.

Acceptance covers the exact recommendation-library unit and evidence. Inventory binding, any future caller/command, qualification and B2-d completion remain separate; none is claimed complete here.
