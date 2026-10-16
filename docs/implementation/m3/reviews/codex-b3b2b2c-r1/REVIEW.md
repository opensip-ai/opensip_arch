# B3-B2B2C-r1 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Subject manifest: `docs/implementation/m3/config-discovery-b/b3-b2b2c-r1-subject.json`, 19277 bytes, SHA-256 `3f92df4f77cd2f417100f7e3d370f92fe36cc7318254942cec4118d8fbf403bf`. I independently rehashed all 79 members successfully, verified the source authority and product-lock pins, and checked every product-map parent, candidate and archived file. Product main is clean at `c0a976187d8efd06280aa98a5e1762a7b44e8c60`; architecture is at `51d916212d4ace3844fdd02ad734925ec6246b3d`; the detached candidate is at the product base. Its changes are exactly the five mapped files.

## Tool and corpus controls

The reconstruction tool first checks the T2 manifest against the bound census pin. Each selected workspace is explicitly lead-readable and Cargo or npm. Every member passes through the census's `store_path` held-out guard before its store is inspected, then through `verified_tree`, which recomputes Git-tree and QD-22 digests with no-follow traversal. `verified_workspace` verifies the canonical overlay, digest, archived acquisition copy, mount set and store targets. Held-out workspaces are skipped; a held-out member cannot reach its store through the reconstruction path.

Provider manifests are copied only from regular-file nodes in those verified trees, at the overlay's exact link directories. The tool renders sorted Cargo patch entries and cross-checks the complete bytes against the cache rendering. LD-4's quoted TOML keys preserve the specified table semantics. npm uses item 20's private package with sorted literal workspace directories. Python is correctly excluded because no M3 reader exists.

The CLI resolves the output location, rejects either checkout and its descendants, requires a new output directory, and creates it privately. The lane supplies an external 0700 temporary directory and removes the reconstruction. I independently checked the four lead-readable canonical overlay records against their digests, cache and acquisition copies, member-store link targets, provider-manifest inputs and Cargo renderings. No held-out store or overlay was opened. No provider manifest is embedded in any subject member; the package contains source, metadata and execution evidence, not copied corpus fixtures.

## Controls (a) and (b), and lead decisions

Control (a)'s `Supplied` wrapper is confined to the test module. It supplies conventional-repository placement markers only for the overlay's providing mounts and admission only for those candidates. Entry observations, children, custody capture and file reads remain native. This is the accepted plan's link-stage seam, including NBO-1's supplied placement, with no production bypass. Its expected link map comes from an overlay string checked against a hardcoded reviewed digest, independently of the carrier under test. Assertions check declared providers, unresolved entries, ecosystem, provider containment and exact link-map equality.

Control (b) initializes every overlay mount as a conventional Git repository with an empty valid index and calls the unchanged discovery through the shared `discover_at` helper. It checks acceptance, reader declarations, admitted providers, exact links, absence of unresolved entries, and the serialized V3 member and declaration fields. Extracting the helper preserves the prior composition and race controls.

**LD-1 is acceptable for these controls.** `temp_dir()` locates lane-owned test input outside repositories; it adds no configuration or discovery semantic input and no new exception to item 9's enumerated environment methods. Both controls are explicitly ignored during ordinary suites and explicitly selected by the lane. The lane checks the two-passed result, and its log identifies both test names as passed. This evidence is sufficient for the requested controls; ordinary suite counts alone would not be.

**LD-2 follows item 20.** The generated carriers declare providing mounts, rather than automatically admitting every overlay mount. Consumer-only mounts remain undeclared nested repositories, which control (b) checks as an exact set. Independent overlay inspection gives mount/provider/link counts of 2/1/3 for serde-json, 8/7/16 for aws-lambda-tokio, 2/1/5 for smithy-powertools and 2/2/20 for smithy-sdk. This distinction is honestly exercised, with no claim that every overlay mount is admitted.

## Joint sweep

**LD-3 is a valid transfer of the P3 control to the product instruments.** The host test extends the fixture with two declared real Git members, a nested repository and nested project inside a member, and an installed dependency tree. It passes security's admitted inventory to the native instrument over the fixture's marker inventory. The test checks equal unit sets, exactly W and both members; exact nested-boundary records; and the native instrument's exact excluded-unit paths and reasons. Security does not enumerate units inside boundaries its walker never enters, so equality of those unobserved exclusion rows would be inappropriate.

Removing `repos/b` from the admitted member set retains its VCS anchor and must refuse `native.boundary-inventory-mismatch` with anchor `repos/b/.git`. That is B-S1 U-8's missing-member check. The two sweep mutations independently demonstrate that admitted-member propagation and the host check matter.

## Evidence assessment

I inspected the final `b3b2b2c-checks-r1` logs and runner, separately from the retained first attempt. Independently parsed full-suite logs have equal named failure sets: security 14 at base and candidate, with 1165 passes each; host 8 at both, with 357 versus 358 passes. These suites retain base failures and are not wholly passing suites. Candidate security has two additional ignored controls, both separately passed in the T2 run; the host gains the passing joint-sweep test.

The final evidence records all-targets warning-denied Clippy for security, security with scenario fixtures, and host; clean edited-file formatting; eight host scenario discovery tests; all seven discovery/member/rule vector checks; FW-01, storage and census controls; census verification; environment exceptions; operability; and successful `verify_design` with product qualification false. I also independently compared the candidate census record and vectors byte for byte with main and ran the expressly permitted operability source check: passed, 114 rows, no findings.

| Mutation | Observed failing gate |
| --- | --- |
| `carrier-drops-a-link` | Tool rejects Cargo carrier/cache mismatch before either control runs. |
| `cargo-carrier-written-short` | Both T2 controls reject unequal overlay link maps after the tool's cross-check. |
| `npm-carrier-drops-a-link` | Both T2 controls reject unequal overlay link maps. |
| `provider-manifest-swapped` | Both T2 controls reject unresolved declarations. |
| `npm-links-not-npm` | Both T2 controls reject the link ecosystem. |
| `inventory-members-dropped` | Joint sweep rejects the missing admitted-member set. |
| `host-member-check-dropped` | Joint sweep fails because the required missing-member refusal disappears. |

The mutation logs show assertion/refusal failures rather than compilation failures. The added post-cross-check Cargo mutation closes the evidentiary limitation identified in the first attempt.

This acceptance is for the bounded controls unit, not qualification, S8 assembly, CLI composition, member-observation bounds, workspace margins or completion of B3-b. I did not rerun Cargo, rustc, builds, tests, the lane, census, reconstruction tool or verify_design. Apart from the permitted operability source command, this review used read-only reading, hashing, parsing and Git queries. Neither repository, worktree nor control files were edited; only the requested review artifacts are written. No network, prohibited fixtures or installation data, held trees, other panes or delegated agents were used.
