# Package boundaries review 02 — RF-1 delta

**Verdict: ACCEPT-UNIT.** This covers only the scoped internal package boundary developer tool. There are no required findings.

Subject manifest SHA256 `431b0c827b251538f5484d01e65acdb8e024b0422a633c8a607971c3cf55aa5d`. The three file hashes matched before and after. None of the 59 read-only hash entries changed (subject-01/02, candidate-01, review-01, review-01-completion, inventory v3).

## RF-1: closed
- **Tool change:** line 40 now also reads `build_dependencies` and `dev_dependencies`. The loop already covered top-level and `[target.*]` tables. The file is byte-identical to my review-01 fix copy.
- **Tests:** two new groups (four synthetic legacy tables; real Cargo edition 2021 stale-then-fresh). All 14 pass, and the real Cargo test actually ran.
- **UNIT.md:** a descriptive paragraph plus "twelve" changed to "fourteen". No new scope or qualification claim.
- **My original reproducers:**
  - Stale 2021 `[dev_dependencies]`, stale 2021 target `build_dependencies`, and stale no-edition `[dev_dependencies]` are now refused with `forbidden manifest internal edge`.
  - The allowed 2021 `[build_dependencies]` false refusal now passes.
  - The other 34 of my 36 prior probe outcomes are identical to subject-01.

## Conservative edge checks (19/19 as expected, real Cargo 1.95)
- Editions 2015, 2018 and 2021 honor the underscore tables; 2024 rejects them. The stale forbidden edge is refused in all three honoring editions, both top-level and under a triple-target table.
- If both the hyphen and underscore table are present, Cargo keeps only the hyphen table and ignores the other silently. The tool reads both:
  - an identical entry in both tables passes
  - a forbidden entry only in the ignored table is refused
  - differing allowed entries across the pair are refused as "declarations differ"
  
  All of these fail closed.
- Legacy-table variants all refuse: an alias spoof, a pathless internal owner, a workspace-inherited dependency, and a stale 2024 legacy table.

## Mutations
31 mutants in total; the subject tests kill 18.
- **New legacy mutants:** removing the build or dev legacy table is killed, and so is limiting legacy tables to top level. Mapping build to dev kind survives the tests; my probes catch it, and it fails closed.
- **Carried survivors:** the other 12 are unchanged from subject-01.

## Advisories
- **A.** The tool reads underscore tables even where Cargo ignores or rejects them. That's safe, but refusals can be spurious; a clearer refusal for mixed tables or non-2024 editions would help.
- **B.** The legacy kind mapping isn't pinned by a subject test. Add a positive allowed-legacy test.
- **C.** 13 mutants survive the tests, notably dropping the hyphen `build-dependencies` table from the manifest scan (reviewer probes do detect it).
- **D.** The stale-metadata guarantee covers dependency declarations only. A stale `[lib] path` escape and a stale provider added to the host workspace still pass.
- **E.** Still open from review-01:
  - The `cfg( windows )` false refusal remains.
  - Metadata captures and the 14-shared equality need `--filter-platform aarch64-apple-darwin`.
  - The provider lane is hard-coded.
  - New tool paths need additive inventory review.

## Limits
- This is a delta review. The CLI and provider-isolation trial evidence from review-01 was not rerun, since those artifacts and the rest of the tool are unchanged.
- The existing pure build trial is a disposable probe, not a provider implementation.
- Not covered: rustc integration, release, purity, macros/`#[path]`/`include!`, external features, metadata authenticity, inventory amendment, product install, or M1 completion.
- Only Cargo 1.95.0 was probed, and the mutation set is reviewer-chosen.
- No commits or pushes.
