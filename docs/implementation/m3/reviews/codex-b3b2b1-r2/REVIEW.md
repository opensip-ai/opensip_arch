# B3-B2B1 r2 review

Verdict: **ACCEPT-UNIT**.

Subject manifest: 13,198 bytes, SHA-256 `e6c9d3b45f50c8386d5c79a32267a5cc2512a12ad1f3fab843e315e34a134bdf`. All 55 members match their byte counts and hashes. All product-map parent, candidate and archived pins match. Source-authority, design-lock and identity table-view source pins also match.

Product main is clean at `03876532b54d8327db96091fababb1fd994a83d2`; the detached candidate is at that base with the advertised changes. Architecture HEAD matches `6666ae1abc8f17d01168c715a1d3b4999170ae7f`.

No required findings or non-blocking observations.

## Round-1 findings

**B3B2B1-R1-RF-1 resolved.** TomlTableView::iter now sorts borrowed table entries by the start of their key spans before yielding them, preserving source order for Cargo enumeration instead of key order. The two reference-derived quoted-key collision controls use opposite document orders and select different expected members. This directly exercises the flattened identifier collision that invalidated the old LD-3 argument. The cargo-key-order mutation removes the source-order sort and is caught both by the dedicated collision test and the general vector comparison. No package-key grammar restriction is introduced. LD-3 now states the order requirement rather than claiming order independence.

**B3B2B1-R1-RF-2 resolved.** WorkspaceObservation requests one member_verdict at a time. Branch A performs directory custody and then 6b for each candidate, in ascending path order, returning immediately at its first refusal. It no longer pre-judges later members or retrieves a batch whose later failure could replace an earlier refusal. Branch B uses the same per-candidate interface but continues after excluded candidates.

The new fallible adapter control arms its tripwire only after phase one, so necessary earlier placement observations are allowed. A substituted 6b refusal at a prevents b's directory/verdict observation; without that refusal the b tripwire fires. This verifies the problematic continuation rather than only an output selected from a precomputed verdict vector. The native once-per-decision environment/global-source session remains an explicit B3-b2b2 obligation. The request's later batching wording is superseded by this r2 implementation and LD-5.

**B3B2B1-R1-RF-3 resolved.** Synthetic::children records its directory in listed. Vectors carry a listing allowlist, and the general test checks listing subset and forbidden paths in addition to metadata and content access. The reference recorder obtains that allowlist by wrapping _visible_repositories, taking W and the parents of its observed Cargo.toml probes. In the bound helper those probes occur after pruning, depth and boundary checks, immediately before queueing a directory; consequently this derives the directories the glob walk actually lists without modifying the reference. The boundary-listed mutation performs a discarded listing and is caught by the behavioral access assertion.

**B3B2B1-R1-RF-4 resolved.** Six compact controls add carrier/provider JSON at exactly 4 MiB, over it with true metadata, and over it with understated metadata. The reference expectations distinguish custody rejection from bounded-byte/parser rejection. Exact-limit objects remain usable; true oversized metadata produces custody:TOO_LARGE; an oversized read after understated metadata gives carrier custody:TOO_LARGE and provider parse. The provider TooLarge mapping was corrected accordingly. The 32 JSON controls now include all requested byte, depth, integer, duplicate, numeric and Unicode alignment cases.

## Core and vector fidelity

The two phases preserve branch A's SLM-first trial order: provisional members are supplied to the caller's trial walk, and a failed trial produces TrialRefused before terminal placement/cap/6b decisions. Branch B retains placement-only membership, the distinct-candidate cap before 6b, per-member exclusion, and final-member-only link derivation. Root-in-repository, entry grammar, visible-repository glob classification, candidate depth, owner-waiver reach, unusable manifests, ambiguity and declaration ordering continue to follow the reference in the inspected source and vectors.

WorkspaceObservation remains a suitable pure-core boundary. Carrier/provider bytes are requested only after custody passes, preserving LD-4's justified read-set subset. Uncaptured ACLs do not pass. Literal placement and glob traversal classify anchors before querying protected descendants; links inside inner boundaries/pruned anchors remain suppressed. The access adapter now records all four relevant metadata/marker/listing/content families, with marker observations normalized to the paths _markers consults.

The generator's wrappers record _finish/_refuse decisions without editing their bound bytes. The partition is consistent: 116 baseline cases plus 38 controls yield 154 vectors; 20 rootless cases are listed separately and one inconsistent-side-table case remains input validation. A rootless selection has no W and is not a call to this core; composition must continue to enforce that condition.

The four TOML resource controls still compare the real reference outcome with a separately labelled product parse expectation obtained by substituting unusable TOML and restoring the original carrier digest. Tests separately check RecursionLimit and NodeLimit, making the intentional bounded-parser divergence explicit. Two collision controls and 32 JSON controls complete the 38 controls. The older SCOPE subsection saying 26 JSON controls describes the retained original probes; its r2 table, actual generator and request correctly account for the six added byte controls.

## Closure, identity and evidence

An independent structural comparison confirms both census files change only closure/6's bytes and SHA-256. Every candidate closure pin hashes to its source. custody.rs adds the module declaration block, while census constants/model logic and all census rows/predictions remain unchanged. Held-out standing remains outstanding; no blind store was opened.

The identity views remain read-only. Source-order iteration adds temporary collection/sorting but changes no parser grammar, bounds or existing API behavior. Its actual source bytes match the updated dependency-policy pin. The archived dependency checker still reports the same source-census failure on base and candidate. LD-7 correctly discloses this existing failure rather than claiming a restored dependency gate; its separate policy remediation remains outstanding.

The two permitted checks were rerun successfully: operability source check, 114 rows with no findings, and workspace_member_vectors.py --check against the bound architecture sources. No other executable check was run by this reviewer.

Archived security logs have equal sets of 14 failing tests, with aggregate passes rising from 1,141 to 1,146 across two suites: five new passing tests. Identity has 72 passing tests at both base and candidate. The focused workspace-declaration log reports all five tests passing. These facts support the stated comparison, not an entirely green security/dependency suite.

Archived warning-denied all-target Clippy, formatting, discovery and tracking controls, vector checks, FW-01, storage/census controls, census --check, environment, operability and design verification report success. All thirteen mutation logs show compilation followed by behavioral failures at relevant assertions, including the new Cargo-order and output-preserving listing mutations. No test/build/census command was rerun here.

Acceptance is for the pure decision-core unit. Native observation, the once-per-pass 6b session, retained identity across the handoff, walk composition, complete serialized declarations, T2 controls, joint sweep, later cost bound and qualification remain outside this unit. The prior A2 observation that placement/listing work can exist at zero admitted members remains applicable to B3-b3a.

Review used read-only reading, hashing, JSON parsing, Git queries and the two expressly permitted checks. No Cargo, rustc, tests, builds, lane, census tool or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry/store/overlay was read. No panes or delegation were used. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
