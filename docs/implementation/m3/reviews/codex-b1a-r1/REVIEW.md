# B1-A-r1 configuration resolver review

Verdict: **REQUIRED-FINDINGS**

Required findings: two. Non-blocking observations: none.

Subject manifest: `a8037278b4849d2d888325eeebd54054bab0a5f15091fe88331c2cc944b64532` (7545 bytes; 34 members). Rehashed every member; all sizes and hashes match. All 18 architecture authority pins and ten product-reference pins match. The eleven mapped candidate paths exactly cover the worktree delta and match their staged copies. Product remains clean at `08527ebf732b432d7bfe8fce9c749cbfab51d9c1`; architecture is at `6450467bfc5345cb0727dda571a3de27409b16b2`.

## Required findings

### B1A-R1-RF-01 — External overrides can conceal incomplete compiled defaults

Location: configuration.rs, step 7, around line 546.

The completeness loop asks whether the merged winner map contains capabilities and budget. It never checks whether those required values were supplied by CompiledDefaultsV1. Consequently these statically traced cases reach successful resolution:

- defaults.capabilities is None, while a valid project layer supplies analysis.capabilities.
- defaults.budget_limit is None, while a valid global/project layer supplies analysis.budget.

AQ:132–137 explicitly requires missing **compiled** capabilities/budget to be CONFIG_DEFAULTS_INCOMPLETE, a host invariant, rather than a second zero-config spelling. The accepted plan retains that obligation. Checking only resolved completeness lets an external carrier repair a malformed host default input.

At step 7, check the original compiled-defaults input independently of the winner map. Keep lawful higher-layer overrides when the compiled defaults are complete. Add negative controls where a valid external override masks each missing internal field. The existing tests only remove each default when no later layer supplies a replacement, and PCM's merged-record checks do not independently establish this internal-input obligation.

### B1A-R1-RF-02 — An external pin can be reported as a host fault

Location: configuration.rs, cross-field pins/holds loop, around lines 526–542.

The loop visits pins, then holds, retaining only stable IDs. A duplicate always calls refuse with the current field winner's layer. Consider otherwise valid defaults containing holds=[A@1] and a project layer containing pins=[A@2]. Both layers are individually well formed. The new external pin creates the conflict, but the second visited occurrence is the trusted default hold, so the result is HostInvariant, SYSTEM.OUTCOME_ILLEGAL_STATE, exit 4.

Reversing the fields gives an external CONFIG.INVALID refusal. Field traversal order therefore determines whether equivalent caller-introduced conflicts become a request rejection or a host failure. The same issue affects equal-version duplicate pin/hold pairs. This is not a defect in the valid defaults by themselves. AQ §1 and the plan's external/internal distinction require the external defect to retain its request-rejected row.

Track both occurrences' provenance and specify a deterministic external-conflict subject policy. Route conflicts introduced by external layers to CONFIG.INVALID; reserve host invariants for inconsistent host-built values. Add both defaults-holds/project-pins and defaults-pins/project-holds cases, for duplicate and conflicting versions. Existing cross-layer coverage uses project/local only and cannot detect this misclassification.

These are source-traced counterexamples; no prohibited Rust execution or new test was run for this review.

## Implementation and authority checks

The resolver is pure over captured bytes and typed observations: no carrier I/O, environment access, locks, ledgers or caller is added. Local bytes are not parsed in CI. Steps 1–3 admit every participating layer before merge, and the subsequent logical-path, registry, completeness, partition, normalization, semantic-shape and digest steps appear in the required order. The step-7 predicate, rather than the position of that step, is the RF-01 defect.

Whole-leaf replacement and absence preservation match the reference. Paths follow PCM's project-relative rules, with dot accepted only for workspaceRoots and ignorePaths. The per-layer mapping uses the two DRC classes, includes every PCS merge leaf and matches the semantic leaves of identity-v3. Partition uses only the generated table. Canonical-set normalization preserves allowedScopes order, and the digest is raw SHA-256 of canonical normalized semantic bytes. Provenance is retained separately with original carrier hashes/schema versions and never enters the digest.

LD-B1A-1 appropriately separates matrix membership from mode-specific NOT-SELECTED judgment: the resolver has no mode and the exported cells remain for analysis-spec construction. LD-B1A-2's duplicate/conflict rule agrees with the component reference, subject to RF-02's attribution correction. The reviewed defaults allowlist, typed-default explanation, schema-engine whole-document subjects, re-expressed reference fixtures and deferred I/O/store obligations retain their stated scope. No release content or S-OP-5 field is selected.

Schema-one carriers select the exact preview layer schema, project in memory and are re-admitted as version 2 with sourceSchemaVersion 1 provenance. Input bytes are not rewritten. resolve_analysis_configuration resolves, constructs its resolved named pack selection and calls admit_policy_selection once, with no intervening admission/effect. Existing policy admission remains unchanged.

The termination match is exhaustive and uses existing codes. External CONFIG.INVALID and internal host-invariant shapes are correct apart from RF-02's choice of origin. B-S9's remedy is exactly 706 ASCII bytes with SHA-256 `7ba6e8e50dc3c52f595caf01236019d2cfac6d8f0fd2e40d0dd3644fb0692565`; doctor reuse and test re-pinning remain intact.

## Vectors, drift and retained checks

Ran only the two explicitly permitted checks in the candidate worktree. Both returned exit 0:

- generate_configuration_tables.py --check, with the requested architecture and pinned rustfmt.
- configuration_vectors.py --check, with the requested architecture and product packages root.

Source inspection confirms architecture pins precede model loading, and all provisioned Python package pins are checked before adding their snapshot to the import path. The 52 cases re-express the accepted checker's properties under MB's layer allowlists; schema-one PCM expectations use the labelled version-2 projection. The Rust vector loop checks digest, semantic record and provenance layers on success, or the corresponding refusal class. The retained candidate test evidence records its pass. These vectors do not cover the two counterexamples above.

The pinned host comparison records the same eight pre-existing failures in base and candidate, with 18 additional passing configuration tests (11→29). Candidate evidence records warning-denied all-target host Clippy, edited-file formatting, operability source check, verify_design and tools controls passing. Those retained tests and checks were not rerun here.

All eight mutation logs contain the failed test names recorded in mutations.json; all compiled and were caught, and the restored source hash matches the subject. Passing mutations support the tested properties without establishing the missing masked-default and mixed-trust conflict cases.

The operability change adds only the audited configuration.rs/from/call count of six; all prior mintAudit rows and exception-class rows are retained. The six additions are the five BTreeMap::from calls and i128::from conversion, not mint authority. The design lock is byte-identical to base and matches its source pin, retaining inventory 187 and 162 contract successors. No v188 bind, production caller, new public code, product qualification or overall completion is claimed.

## Boundaries

Used permitted read-only reading, hashing, JSON parsing and Git queries, plus the two expressly permitted drift checks. No Cargo, rustc, tests, builds, other generators or lane were run. No network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, worktree, stage nor control files was edited. Only this directory's REVIEW.md and review.json were written.
