# B2-A inventory v191 review

**Verdict: ACCEPT-UNIT.** Inventory candidate assessment: **ACCEPT**. No required findings or nonblocking observations.

Rehashed the 695-byte subject manifest, SHA-256 `28d57df6015562eef3f16ae9122b7f2e9334d8cec8b122b315e57cb6df594f6e`, and all three members. All sizes and digests match. Independently verified the parent, candidate, successor record, integration census, accepted code review and accepted code subject pins. The code review is ACCEPT-UNIT with no findings and names the exact accepted subject digest.

Product HEAD is the requested clean `6c5b8e8ba1086426ffe719198192a4c4bc530b55`; architecture HEAD is `370424e58eaaa9da26959bfed81390dced511da2`. The pre-existing untracked architecture E2s directory was left uninspected and untouched. Hash comparison confirms that the integrated product files match the accepted code product map; this was an integration-byte check, not a code re-review.

## Inventory assessment

Exactly four rows are added, matching the accepted code's new paths:

| Path | Package | Role | Generated |
|---|---|---|---|
| `crates/security/src/custody/discovery_rule.rs` | opensip-security | algorithm | false |
| `crates/security/src/custody/discovery_rule_tests.rs` | opensip-security | test | false |
| `crates/security/src/custody/discovery_rule_vectors.json` | opensip-security | fixture | true |
| `tools/security/discovery_rule_vectors.py` | tooling | builder | false |

Their descriptions accurately cover the accepted pure rule, its controls, generated reference results and developer generator. They make no walker, record-production, public-export, membership or qualification claim. The rule path had no planned row in v190.

The candidate is sorted, unique and a strict superset: 1,230 → 1,234 file rows. All 1,230 inherited rows are equal by value, including `custody.rs` and the planned host discovery rows. Every other top-level value is unchanged, including all 20 packages and nine pending decisions. All 99 inherited still-absent paths remain unchanged and exactly equal the record's `inheritedPlannedFilesRetained` list. All 1,135 tracked product paths are covered. The successor's `addedFiles` list is exact.

## Census and binding

Ran only the permitted source census on integrated product main: **passed, 114 rows, no findings**, matching the staged integration census. Verified the checker and exception-file pins; both files are byte-identical to the accepted code's product base. The mint-audit list has **439 rows**, unchanged. Its lexical audit does not grant mint authority.

The 675,253-byte candidate has SHA-256 `0a6f2a00f0fab397dac2ac45e41e0550cf6f2576bb1ccbe7071f004c21dbac6b`. Its 672,997-byte parent remains at SHA-256 `1c6f17df0eeebc747defcd8b89d08a13b9fafa8965e8609d62139b4a04bd583e`. The 5,620-byte successor record has SHA-256 `bd1a68ba8665c0733ccd5727bbb37aa741fbff393d48f4d5daf7eaf8753d87df`. No product qualification is claimed.

Lead assent, architecture publication and a separate product-lock binding with fresh design verification remain subsequent actions; this review makes no binding.

## Boundaries

Inventory-only review. Used read-only inspection, hashing, JSON parsing, Git queries and the explicitly permitted source census. Ran no compiler, Cargo, tests or lane; used no network, other panes or delegation; accessed no private fixture, installation directory, signing keys or held trees. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this review directory.
