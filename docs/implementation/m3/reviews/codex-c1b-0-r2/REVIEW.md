# C1B-0-r2 materialization review

**Verdict: ACCEPT-DESIGN-UNIT.** No required findings or non-blocking observations. C1B0-R1-RF-1 is resolved. This accepts the pinned materialization as a contract-successor design unit with its product changes; binding, production composition and qualification remain separate.

## Subject and review boundaries

The subject manifest is 20,180 bytes, SHA-256 `04258d4e2a9402eccbd8b8953bc0f39b73bd82977d78d498669c5ce53fdd788b`. All 88 members match their declared lengths and hashes. The candidate is detached at main `098527316e7ee76f877b982f20c1493130cbb5ff`, and main is clean. All fourteen product-map candidate and archived copies agree, all parent pins match HEAD, and no mapped path is new. Source.json’s authority, prior-review and current product-lock pins match; successor.json’s parent/candidate pins also match.

Executed only expressly permitted read-only checks, directing helper output files to /dev/null so no additional artifact was created:

- `python3 -I -B evidence/regenerate_c1b0_census.py /dev/null --verify`: passed.
- `python3 -I -B evidence/check_c1b0_preflight.py /dev/null`: passed.
- B-S2’s `python3 -I -B evidence/check_b_s2.py`: passed.
- Candidate `python3 -I -B tools/check_operability.py source --repository .`: passed, 114 rows, no findings.

No Cargo, rustc, builds, generation, ordinary census generation/check command or lane was run during this review. No network, private fixture, installation directory, key, held tree, T2 store/cache, other pane or delegation was accessed. The helper reads public bindings and rendered metadata, not held-out contents. Neither repository, worktree nor control file was edited. Only REVIEW.md and review.json were written.

## C1B0-R1-RF-1: resolved

The package now starts from C1a4’s accepted blind refresh. The live permitted verifier recomputes both receipts’ complete bindings on main and confirms both current, with both records rendering blind-census held-out rows. The archived write record establishes this at lane base 72e07879; the post-lane verifier and live review establish it at the lock-only successor 0985273.

The candidate changes discovery’s binding only at `/reference/1`: generator-closure.json remains 68,832 bytes but changes from `e09d7bfee34fa260c9c040ce351153eb74e2f03eaf7e783ced61047e3455d868` to `325fabbbc91acafad40d0e223f11db0229128dcbae6342023b0b19b40ff130b5`. The companion changes exactly that same pin nested at `/discovery/reference/1`. No other binding changes.

The two census records are now included in the fourteen-path map. The archived ordinary --write regeneration changes only discovery’s entries/heldOutMargin and the companion’s heldOutEntries/heldOutMargin. Direct JSON comparisons confirm exactly ten held-out rows become `outstanding: held-out (blind receipt stale)` in each record and both margins become outstanding. Every lead-readable row, workspace row and other field stays equal. Discovery vectors do not change. Both receipts remain byte-equal to main’s, preserved as historical baseline evidence; neither is refreshed here.

All three ordinary output checks pass in the lane and after the base move: discovery census including vectors, workspace ledger, and snapshot census. The read-only --verify separately establishes the stale state and exact public binding deltas. This properly distinguishes correct regenerated output from receipt freshness. C1b’s stale interval opens on integration, and its one reviewed blind refresh remains after C1b-2. No held-out store was opened and no blind mode was invoked by the reviewed regeneration/verification procedure.

SCOPE now requires ancestry, no overlap with the fourteen reviewed paths, and renewed determinism, operability, output checks and census verification for an admitted base move. The actual move is exactly one descendant commit from 72e07879 to 0985273, changing only design-lock.json. The post-lane record and logs re-prove all named checks at 0985273; the live preflight/verifier also pass there. That is sufficient for this lock-only move without repeating the compiler suites. It does not authorize arbitrary later changes or silent changes to the reviewed product map.

## Schema/code results carried forward

The identity-v3 schema, admission registry, compiled SourcePin, generator options, generated Rust carrier, evaluator code and host controls are byte-identical to round 1’s reviewed candidates. Of the original twelve paths, five differ only through required r2 package-path/hash metadata: source/admission maps select the r2 copies, generator closure re-pins the moved source map, the registry recipe re-pins that closure, and generated report.ts changes only its registry/closure hash comments. The two census records are the substantive package addition resolving RF-1.

The entire candidate schema was independently reconstructed from the current product parent plus exactly B-S2’s four definition assignments. It equals the candidate: vcs-observation is precisely the fragment’s oneOf, v2 is the prior record unchanged, and v3/member definitions are the fragment’s. No unrelated JSON member changes. The file retains its indent-2 ASCII serialization with final newline, applied to I1-L’s anticipated product copy.

The source/admission maps and registryArchitectureSource select the two exact archived copies. The compiled schema pin, three Identity3-prefixed entry points and admission-registry row remain the reviewed ones. All 352 generator-closure file pins match live candidate bytes; the recipe’s closure and options hashes match. The archived selected-pipeline determinism checks reproduce every output with no changed output, both in the lane and post-lane. Their 43 sources and 886 entry points are development-generation evidence, not qualification.

The evaluator still obtains the admitted record, preserves its inventory join, and applies vcs_joins. VCS_KIND_JOIN remains top-level; the member join requires Git with a non-null commit. The direct helper test exercises the redundant join’s otherwise admission-unreachable refusals. The unchanged host controls preserve B-S2’s exact 154/190/365-byte vectors and digests through identity admission and RetainedInputs::identity_record_shape; schema 2 also admits through v2 and schema 3 does not. All twelve merged-schema negatives are checked through both paths. The permitted B-S2 checker independently passes its thirteen checks, including schema 3 under the old definition.

IDS architecture/I1-L design copies and the evaluator scanner pin remain unchanged. Direct snapshot cost sources and tools are unchanged; the nested discovery binding is correctly the companion’s only delta. No new mint call outside generated output, environment read, let-underscore result discard or dependency is introduced. The lexical mint census remains 439 rows. Existing base-dirty generated identity.rs is excluded from rustfmt; all edited base-clean handwritten Rust files are checked.

## Preflight and lane

The live public design preflight refuses exactly `generation source is not selected by accepted design`. In-memory acceptance of exactly the package identity-v3 and admission-registry copies passes, preserving the base’s 43 generation sources, 52 admission sources and 15 verified aliases, with exactly fourteen changed paths. This models the intended contract binding without editing the lock or bypassing production acceptance. The public generator and TypeScript entry points retain the same pre-binding refusal.

The lane of record is c1b0-checks-r2 on 72e07879. Its matched suites have no new failures: contracts 0 to 0 and identity 72 to 72 with zero failures; host 409 to 411 with the same eight failures; storage 137 to 137 with the same 33; evaluator 47 to 48 with zero; security 1187 to 1187 with the same fourteen. No isolated reruns were needed. Focused controls, warning-denied all-targets Clippy, generation determinism, FW-01, environment exceptions, operability and the empty discovery-closure intersection pass.

The allPassed aggregate includes explicit expected-refusal detectors; it does not mean every raw command exited zero. With the two copies accepted in memory, the report TypeScript lane passes. The generator TypeScript lane retains the base-equal loader-policy refusal for tools/contracts/package.json; it is not a successful generator-lane qualification. The unchanged product checker is used by the wrapper. Round-1 void attempts 1 and 2 remain history as SCOPE records: formatting warnings were fixed and pre-binding/base-equal refusals were subsequently classified separately.

All four mutation logs contain actual semantic test failures. Both schema mutations re-pin the compiled identity-v3 SourcePin so their negative controls run rather than merely failing a pin. The other two mutations remove the top-level/member joins and fail the direct evaluator test. Sources are restored after the controls.

## Outcome

The corrected package is acceptable as ACCEPT-DESIGN-UNIT for contract-successor binding of the selected source copies. No new inventory path is required. C1b-1’s Git reads/VCS cost term and cap derivation, C1b-2’s schema-3 sealing and snapshot-level preservation, caller composition and the final reviewed batch refresh remain outstanding. No current held-out margin is claimed for the candidate during the stale interval, and no overall C1b completion or product qualification is implied.
