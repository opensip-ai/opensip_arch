# B1-A-r2 configuration resolver review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Subject manifest: `db3bf69b3d6b48a28a9c60403b6d30c0f20fe0889961eb2e1c9fd404823f3b50` (8007 bytes; 36 members). Independently rehashed every member; all sizes and hashes match. All 18 authority pins and ten product-reference pins match. The eleven product-map paths exactly cover the candidate's changed/added files and match their staged copies.

## Prior findings resolved

**B1A-R1-RF-01:** Step 7 now checks input.defaults.capabilities and input.defaults.budget_limit as well as the merged leaf. Missing compiled values therefore remain host invariants even when a valid external value wins. The new control covers project/local capability overrides and global/project budget overrides; each identical override remains lawful when defaults are complete. The fix preserves the eleven-step sequence.

**B1A-R1-RF-02:** Pin/hold occurrences now retain their layer and pointer. The conflict path chooses an external occurrence whenever either occurrence is external, the second when both are external, and a host invariant only when both are host-built. The new control covers both default-hold/project-pin and default-pin/project-hold directions, for equal and conflicting versions, and the all-defaults host case. Subjects name the selected contributing occurrence. The scope text records this deterministic policy.

Compared with round 1, only configuration.rs and its resolver tests change among the eleven product files. Reviewed the fixes with the unchanged implementation, registries, vectors, tool sources and accepted authorities in context; no new required issue was found.

## Whole-unit assessment

The resolver remains pure over captured bytes and typed observations: no I/O, environment read, lock, ledger, caller or carrier capture is added. CI does not parse local input. Lexical admission, exact schema admission and per-layer allowlists run for every participating layer before merge. Whole-leaf replacement preserves absent values, followed by the declared logical-path, registry, compiled-default completeness, classification, normalization, semantic-shape and digest steps.

Logical paths match PCM, including the restricted dot sentinel. Profiles use the contract-named default registry. Configured capability membership and existence of a selectable mode are checked without confusing release availability with scope; mode-specific NOT-SELECTED judgment remains with analysis-spec construction (LD-B1A-1). Waivers remain an empty registry. Duplicate requests and pin/hold conflicts follow the component rules with the corrected provenance attribution. Deferred store/path-existence/component-index obligations are expressly outside this pure unit.

The reviewed mapping uses the two DRC classes and the correct layer allowlists. It covers every PCS merge leaf and exactly the semantic leaves of identity-v3. Partition reads the generated table only. Semantic canonical sets are normalized by canonical item bytes; allowedScopes retains its priority order. Identity-v3 semantic-configuration validates the complete five-section record, and resolvedConfigDigest is raw SHA-256 of its canonical bytes. Provenance and operational values do not enter that digest.

Schema-one files use the exact selected preview layer schema, then a labelled 1:1 version-2 projection and re-admission, retaining original-byte hashes and source schema version. No input is rewritten. The X12 wrapper resolves and immediately admits its resolved named pack selection exactly once, with no intervening effect or admission step. The existing pack-admission implementation remains unchanged.

The refusal mapping is exhaustive without a wildcard and adds no public code. External defects retain CONFIG.INVALID; host-built defects and incomplete defaults use the host-invariant route. The mixed-origin conflict correction closes the prior gap. B-S9's unchanged remedy remains the exact 706-byte string with SHA-256 `7ba6e8e50dc3c52f595caf01236019d2cfac6d8f0fd2e40d0dd3644fb0692565`, reused by doctor and pinned by the updated tests.

The seven scoped lead decisions remain within the plan: per-mode capability judgment is deferred to its actual owner; component conflicts are refused with the corrected attribution; allowlists are reviewed generated data; subjects reflect available schema diagnostics and provenance; typed defaults are checked as host-built input; reference cases are re-expressed under the owning layer rules; I/O/store and environment enforcement remain outside B1-a. No S-OP-5 field or release content is selected.

## Verification and evidence

Independently ran both expressly permitted drift checks in the candidate worktree. Both returned exit 0: configuration table generation --check with the requested architecture/pinned formatter, and configuration vector --check against accepted PCM with the pinned package snapshot. The generated registries and all 52 PCM cases are unchanged from round 1. The tool verifies architecture/model inputs and package bytes before loading the model/jsonschema. The Rust vector test compares digest, semantic record and provenance layers or refusal class; its pass is retained in the fresh candidate evidence.

Fresh checks record base host tests at 310 passed/eight failed and candidate at 330 passed/the identical eight failed, across three suites. Configuration tests increase from 11 to 31; both new regression controls are in the passing list. These remain scoped results with pre-existing failures, not an all-host-tests-pass claim.

The fresh evidence records edited-file rustfmt, the two drift checks, nine tool controls, warning-denied all-target host Clippy, operability source census and verify_design passing. Those tests, Clippy and checks were inspected as retained evidence and were not rerun by this review.

All ten mutations compiled and were caught. Independently matched each mutation's failed-test names to its raw log. In particular, completeness-on-winners is caught by the masked-default control, and conflict-blamed-on-second by the mixed-origin conflict control. The recorded restored source hash matches the staged candidate.

The other nine product files are byte-identical to round 1. This preserves the generated mapping/vector tools, S9 test pin, module-comment-only change and single six-call configuration.rs/from mintAudit row. The unchanged row is still exact for five BTreeMap::from calls and one i128::from conversion; no mint or exception-class authority is added.

Product HEAD is the requested `08527ebf732b432d7bfe8fce9c749cbfab51d9c1`, clean; architecture HEAD is `6450467bfc5345cb0727dda571a3de27409b16b2`. Candidate design-lock.json remains byte-identical to base and matches its source pin. Inventory 187 and 162 contract successors remain unchanged; v188 review/binding is still future work. No production caller, product qualification or whole-plan completion is inferred.

## Boundaries

Used permitted read-only reading, hashing, JSON parsing and Git queries, plus the two explicitly permitted drift checks. No Cargo, rustc, tests, builds, other generators or lane were run. No network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, worktree, stage nor control files was edited. Only this directory's REVIEW.md and review.json were written; round-1 artifacts were not modified.
