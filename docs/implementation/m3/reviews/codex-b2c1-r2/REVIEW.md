# B2-C1-r2 review

Verdict: **REQUIRED-FINDINGS**

All three round-1 required findings and its metadata observation are resolved. One remaining exact-reference refusal mismatch blocks acceptance of this subject.

## Subject and bases

Rehashed the 10216-byte subject manifest, SHA-256 `4a2544ae65e08c697bee8a01222091d3c01d4903b44f5ffbc016e31976c31690`, and all 46 members; every size and hash matches. Confirmed clean product main `b0154f08f9193bbf3ca368420c2dae2006c11661` and architecture HEAD `b6e42226f103642306e8c0cd1ac2ddc1b633587a`. Source authority/product-lock pins and all product-map candidate, archive and existing-parent pins match. The changed/untracked candidate paths exactly equal the product map.

## Round-1 resolutions

**RF-1 resolved.** Production discovery, membership and scope entries require &AdmittedBoundaries. Their Option-taking implementations are private; the standalone wrappers exist only under cfg(test). The explicit gate returns native.admitted-boundaries-required on absence. The new recorded source control checks the gate, test-only module and signatures; the corresponding mutation is caught. The security-owned private fields and crate-private constructor remain intact, with record admission in the existing scenario seam.

**RF-2 resolved.** Root, scope and scenario schema-equivalent bounds now count Unicode characters. The new vectors cover the 2049-character/4098-byte admitted root, a 4096-character prefix, 4097-character prefix rejection and oversized unit/member roots with the reference's length-refusal strings. Independently replayed these new calls against the bound reference; outcomes and recorded keys match. The remaining finding below concerns grammar-error formatting, not these corrected length decisions.

**RF-3 resolved.** After cardinality admission, the generated request rows are checked against capability/mode vocabulary and NOT-SELECTED cells in canonical order. The unknown-mode vector now carries the reference refusal. Independently replayed that vector. Its new mutation is caught.

**NBO-1 resolved.** source.json omits the stale contractSuccessorsUnchanged value and records publicApiAdded=true for the explicit Rust surface.

## B2C1-R2-RF-1 — Complete the new Python repr reproduction

`discovery.rs:323–351` adds python_repr to reproduce the reference's exact malformed-root keys. It escapes backslash, quotes, ASCII controls and DEL. Its final branch emits every remaining character literally. Python repr also escapes non-printable Unicode characters, so this is not the same representation.

Read-only reference probes, starting from a valid discovered unit and replacing only rootPath, produce:

| Malformed root code points | Reference value fragment in the refusal string |
| --- | --- |
| U+002F U+0085 | `'/\x85'` |
| U+002F U+2028 | `'/\u2028'` |

The table's backslashes are literal characters in the returned string. The complete prefix is `NATIVE_UNIT_ROOT_REPRESENTATION:units[0].rootPath:#/$defs/InternalUnitRootV1:`. Candidate source instead appends the actual U+0085 or U+2028 after the slash. Consequently its returned key differs byte for byte from the selected oracle. Both roots still refuse: this is a bounded diagnostic/refusal-reproduction issue, not an admission bypass. No Rust execution was performed; the reference result was executed through the permitted import, and the candidate behavior follows directly from its formatter branches.

Implement the reference's non-printable Unicode representation or select an alternative through the appropriate design route. Add reference-generated grammar-refusal vectors for these cases, preserving the accepted-root behavior and exact key comparison. Existing multibyte positive/length-negative vectors do not exercise this branch.

## Other implementation and evidence conclusions

The r2 diff preserves the previously reviewed discovery algorithm and its LD-B2C0-1/member/subset/folding/cap/mode/fallback/order behavior. Security export functions continue to call the shared rule rather than restate it. The rule and custody.rs are byte-unchanged, and every modeled cost-closure pin in the existing public receipt still matches the candidate. No corpus store was opened. The closed alias map, matrix-derived defaults, scope digest/disclosure and FW-01 coverage remain sound within the reviewed scope.

Independently reran only the permitted checks: source census passed with 114 rows and no findings; FW-01 passed 7 tests; the discovery-unit-vector check verified the generated record. Independently replayed all seven newly recorded reference calls.

Recorded evidence shows identical security failure sets (14 failures, 1128 passes at both base and candidate) and identical host failure sets (8 failures, passes 343 to 348). All eleven mutation logs contain actual test failures and no Rust compilation errors. Recorded Clippy covers host and security with --all-targets and -D warnings and passes. These Rust/lane results were inspected, not rerun. They do not cover RF-1 above.

Cargo workspace status as a supplied observation and membershipDigest binding at the later Plan stage remain justified scope decisions. No production caller, environment read or law change is added. Inventory v201 still follows for the six new paths; B2-c/B2-b and qualification remain incomplete.

## Boundaries

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, worktree, stage nor control files were edited. No Cargo, rustc, builds, lane, network, other panes or delegation were used. Execution was limited to the expressly permitted Python checks and read-only bound-reference probes. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.
