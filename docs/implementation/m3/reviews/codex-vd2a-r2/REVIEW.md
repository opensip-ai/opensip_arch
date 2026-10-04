**ACCEPT-UNIT: VD2-a r2 plus F8c. ACCEPT-DESIGN-UNIT: F8c's refreshed record. No required findings remain. VD2A-RF-01 is CLOSED.**

Reviewed the worktree `/Users/sb/code/opensip-ai/opensip-vd2a`, detached at `cca4fe48d3cf44c6c73c0e625bd4de769cd34899`, against the accepted VD2 r1 snapshot and the pinned r1 review. All 73 requested pins matched initially and at the final check. The product diff remains the seven declared modified files, +441/-13, with no added path or commit.

| Accepted subject | Bytes | SHA-256 |
|---|---:|---|
| Product diff from `cca4fe4` | 35,350 | `8d2fa33ad4f022fcd38fa59a1c788e3a8fdcc199f5130c77f0837c820ab67f82` |
| F8c subject manifest | 3,808 | `280120c78e364f7bca0b428f6b26d1e445e50c2616fe025826b2ff52312daffc` |
| F8c successor record | 5,231 | `cd6ba04352794c58a497837b836eec787bf2d8987f976901b1aae6dbc51a79e1` |
| Product and reference verifier | 43,946 | `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326` |

**VD2A-RF-01 disposition.** The new comparison at `tools/verify_design.py:423` canonicalizes both entire lists with `json.dumps(..., sort_keys=True)`. It now distinguishes booleans, integers and floating-point values, retains list order, ignores object key order, and keeps the original refusal message. The accepted VD1 target-pin equality and the already canonical target lookup are unchanged. The r1-to-r2 interdiff applies to both retained r1 product files and reproduces the current files exactly; no other verifier behavior was introduced by this round.

N20's four subcases now refuse: a review listing `true` for line 1; `1.0` for line 1; a float byte count for the record's integer count; and the reverse byte-count mismatch. All four fail against both the r1 verifier and the law prototype. N21 preserves the named-boolean selector refusal at target lookup. P11 writes genuinely unsorted review keys, rejoins the exact review and assent pins and still binds. P12 binds the float target-pin form only when the review lists that same record value. The retained r1 reproducer now produces REFUSED, REFUSED, REFUSED and PASSED, with the requested messages and final count 1. The two new comparison mutants are killed respectively by N20 and P11.

VD2-NB-01 remains CLOSED: all six prior additions and the rewritten VD1 test remain, and all 46 extension controls pass. The law's 40 controls also pass. The base lock's plain and implementation outputs equal the base verifier outputs apart from `contractPassageSupersessions: 0`; contract-history, inventory projection and source checks retain their existing results.

**Judgment calls.**

1. Agree: no separate listed-selector validity branch is needed. For a contract passage, the review selector must be canonically identical to `supersedes.selector`, which rule 2.3 already matches to the entry selector resolved under rule 2.1. For an inventory passage, the unchanged VD1 lookup matches the named canonical selector to a published, resolving target entry. Thus a listed selector cannot independently be invalid while the record passes. The comparison itself supplies this requirement.
2. Accept whole-list encoding. It canonicalizes each nested object and preserves array position; it is equivalent to ordered per-entry comparison, and also rejects a non-list, extra entries, missing entries or reordered entries.
3. Accept P12 as a passing compatibility control. Exact path and digest with a numerically equal byte count still identify the same target under VD1. The new review requirement compares the record's own values, so N20c/d correctly refuse differently typed review values in both directions. Tightening target-pin types would be a separate deliberate change.
4. Accept the rebase to `cca4fe4`. The verifier, tests and four F8c base materializations are byte-identical between `4c761e8` and `cca4fe4`. All five F8c parents remain accepted exact pins. The staged lock extends the new base and package-edge checks correctly use selected inventory v136.

The earlier decisions about v4-only coverage, numbered per-record checking order, retaining the unreachable root-kind invariant, optional fixture review lists, the tool-only provenance diff and the separate contract review remain applicable. The fix does not change the contract or inventory chain mechanism, lock schema, output shape beyond the law's count, or first-refusal precedence.

**F8c's refreshed record.** Checked as a contract successor: the manifest covers all 17 candidates plus the record, every member has its exact pin, all five parents are accepted bases, and no candidate reuses an accepted path. There are no overrides or supersessions. Parent pins and candidate paths equal r1's. Exactly 12 candidate files moved, plus the record, manifest and outside-subject unit draft, matching the 15 retained r1 members. The five unchanged evidence scripts remain byte-identical. The changed pinning-script docstring and freeze-script base/review-path updates agree with the request.

The four materialization-map rows match the base bytes, current worktree bytes and architecture product copies. The 5,901-byte tool-only diff equals the actual verifier portion of the product diff and applies to F8b's accepted parent to produce the candidate exactly. The closure and lane registry each change only the verifier row; the other 348 closure rows, 159 lane rows and toolchain data stay unchanged. The schema registry changes only its closure digest. The report changes only header lines 2 and 3. Neither the base nor r1 digests remain in tracked worktree consumers.

No rebuild is needed: the Rust sources/manifests, builder, receipt and selected rebuild-02 executable remain unchanged. The required public drift replay validates the re-pinned closure and build receipt, uses the selected executable, and passes with 40 sources, eight outputs and `changed: []`. No Rust source reads the changed tooling or re-pin files. Every modified path remains covered by v136 with a true description, so no inventory successor is required.

The staged lock is the canonical `cca4fe4` lock plus exactly F8c's row. With the two synthetic review/assent placeholders served in memory, it selects each changed closure, registry, report, lane-registry and verifier copy exactly once through F8c. It advances contract successors 95 to 96 while retaining 96 inventory successors, v136, 100 inheritance rows, 21 VD1 links and zero contract links. Plain verifier, public generator and TypeScript checker all refuse the staged placeholders at `SCRATCH-F8C/review.json`. Actual review/assent pin replacement, root assent and plain post-binding checks remain the lead's stated integration steps.

**Independent checks.**

| Check | Result |
|---|---|
| Initial and final requested pins | 73/73 match |
| Design binding tests | 121 pass |
| Current tests against base / r1 / prototype | Expected 41 failed/error assertions / exactly N20's four failures / exactly N20's four failures |
| Retained r1 equality probes | Three requested refusals, then float-target success with count 1 |
| Law fixture / extension / real-lock probes | 40/40 / 46/46 / 17/17 expected outcomes |
| Mutation run | 19/20 killed; only the accepted unreachable root-kind guard survives; expected exit 1 |
| Base/new verifier, plain and implementation | Equal except added zero contract count; 95 contracts, 96 inventory successors |
| Scratch staged verification | Pass; 96 contracts, 96 inventory successors, v136; 40 generation sources, 48 admission sources and 15 aliases |
| Real public generator drift | Pass; 40 sources, eight outputs, `changed: []` |
| TypeScript scratch preflight | Selected registry, 12 tracked rows and both trusted entry points match; expected missing node_modules refusal before any child |
| Plain staged verifier / generator / TypeScript checker | Each exits 1 at the expected review placeholder |
| TypeScript tool / crash-matrix tool unit tests | 3 / 26 pass; no crash-matrix set |
| Cargo fmt / host and provider metadata | Pass |
| Optional host `schema_sources` tests | 25 pass |
| Host/provider package-edge checks, v136 | Pass: host 12 packages, 22 declared/20 resolved edges; provider one workspace package, two/two edges |
| Package-edge tests | 14 pass |
| Security-crypto / identity dependency checks | Pass: 11 dependencies/eight local sources; eight dependencies/305 sources |
| Dependency-policy / identity-dependency tests | 9 / 5 pass |

The real-lock runner redirects only the two moved, unbound SD7-r1 reference reads to the tracked retained copies, checking their exact law pins first. The verifier, bound architecture inputs and all 17 cases are unchanged. This is the same bounded substitution documented in r1, now provisioned by the request.

**SD7 compatibility and limits.** The GROK2 review list is canonically equal to SD7-r2's record list. Independently reran its scratch proof with only the documented staged-count constant changed from 95 to 96 in scratch: SD7 binds with one contract link, all five refusal messages remain exact, VD1 fails closed, and the effective NE equals NE7 (380,848 bytes, `0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3`). See `sd7-replay-context.json` and `sd7-r2-replay.json`. The separate SD7 subject's stale count and r1 tool/record citations remain untouched, as disclosed by the lead; this review does not amend that subject.

Full TypeScript children remain unrun because the existing offline esbuild 0.28.2 boundary is unprovisioned. The scratch TypeScript success denotes valid preflight plus the expected refusal, not a passing TypeScript lane. The optional full materialization replay was not run; exact map, delta, interdiff and tool-diff application checks plus the real public drift replay passed. Acceptance covers these exact development-tooling bytes, not release or runtime qualification.

All commands ran at nice 19 with the recorded private 0700 Darwin-user TMPDIR. Cargo used the review-local target and cloned offline registry; Cargo commands and Cargo-invoking policy drivers were preceded by process guards, which found no X9 run. The generator guard found no competing generator before the public drift replay. Git was read-only and used only the named product worktree. No repository edit, commit, push, delegation, crash-matrix set, real OpenSIP application-home access or private 413 fixture read occurred. Review and retained evidence files are under this review directory.
