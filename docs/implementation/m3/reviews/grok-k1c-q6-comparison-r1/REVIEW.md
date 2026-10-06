# K1c Q6 core budget arithmetic r1

Verdict: ACCEPT-UNIT.

`compare_core` is a local arithmetic helper. It calls the accepted `summarize_slots` for the seven-position median, the maximum charged peak, and the incomplete flag, then applies the published ratios to caller-supplied baseline numbers and a six-coordinate basis projection. It does not read a baseline record, discover a baseline, or emit an envelope row.

## Arithmetic

The projection is `[measurement, reset, cache policy, kernel release, runner class, cgroup entry method]`. `canonical` compares the whole list, so nested cache and charge-ownership objects keep CAN types. Compatibility also requires the current measurement to be the string `cgroupMemoryPeak` and the current reset to equal this call's reset. An RSS measurement, a different reset, a missing number, or a missing projection yields `no-baseline` on a complete sample. Any slot reason yields `incomplete` first, and the known median and maximum stay in the result.

`within` requires all three inclusive integer checks: `5 * elapsed <= 6 * baselineElapsed` (1.20), `4 * chargedPeak <= 5 * baselineChargedPeak` (1.25), and the selected absolute elapsed bound. Those bounds are small 5 s / 2 s, medium 30 s / 8 s, and large 120 s / 30 s, in nanoseconds, for cold and warm. The 1 / 2 / 4 GiB figures are reported as `absoluteChargeComparison` and never change status. `very-large`, `first-use`, `edit`, and any other class raise `UNSELECTED_CORE_ABSOLUTE_BOUND`. Root-reaped time stays inside `summarize_slots` and is not an elapsed input.

The worktree is detached at `fd8eaff8f781552b4e5b6b830be2f74ca5a9a1e7` with only `tools/quality/q6_comparison.py` and `tools/quality/test_q6_comparison.py` untracked. The evidence diff is 12183 bytes, sha256 `0c0155d509af943cb86f4f3e4bccebebde0f2ef0e5995b352a18b0b44dc62cd7`, and its two new-file bodies match those sources. Accepted `canonical.py` and `measurement.py` match the review pins. Q0 r13, AQP r5, and the r13 envelope schema match their pins. The author logs record 14 new tests and 12 accepted sample-accounting tests, both OK, under `python3.14 -I -B` and `nice -n 10`. This review did not rerun them and did not run Cargo, a compiler, a producer, or a measurement.

## Inventory

Subject manifest sha256 `4cecf5afcee4a5c9a8846e700f38193400a4ebbee4ab99ece930973eabcf8755` (1458 bytes). Its seven files match: the v161 README, successor, candidate inventory, checks.json, checks.py, and the two test logs.

Candidate `repository-file-inventory.v161.json` is 608759 bytes, sha256 `e2ebb6cb8ac26dc97872d55190bd9cbd8c68f8e8c6f1acd2f5c424952f2b9c76`. Parent v160 is 607562 bytes, sha256 `6193d61e9de637dc8322327f3c3261bb7132b50ffcfd0bf4f8a09823f89b3fff`. Successor `docs/implementation/m2/k1c-q6-comparison-inventory-v161/successor.json` is 307508 bytes, sha256 `50baf7778a83fd93c1b55426eddec35337f036f68f5ad2132e02692d8d01920a`.

v161 has 1057 sorted unique paths. The only additions are `tools/quality/q6_comparison.py` at index 978 (package tooling, role validator) and `tools/quality/test_q6_comparison.py` at index 992 (package tooling, role test). All 1055 parent rows are unchanged. Packages stay 20 and pending decisions stay 9. The candidate standing sentence remains the v160 I1-b2 sentence. The successor standing names the K1c Q6 core budget arithmetic inventory. All 103 description projections keep the v160 before and effective text, keyed by stable path. `tools/tests/test_check_crash_matrix.py` moves from 1002 to 1004. `schemas/sources/imported-v1.schema.json` stays at 864 and `tools/check_crash_matrix.py` stays at 897.

No Fact2, D12 eligibility, D13 equivalence, full K1c, or product qualification is claimed. Whole-lane QD26 remains outstanding.
