# Typed synthetic snapshot/plan-equivalent sealing over the remaining 21 Rust/TS development read sets

This new preliminary record extends the accepted typed sealing measurement (`docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09`, 13 medium read sets) to the remaining Rust and TypeScript/JavaScript development repositories of the pinned T2 corpus: the union of the Rust and TS/JS `devIds` in the small, large and very-large language buckets (8, 5 and 5 by bucket; by repository `sizeClass`, 8 small, 4 large and 6 very-large, because `poly-very-large-deno` is very-large but selected through its large per-language buckets), and to the three remaining accepted overlay workspaces (aws-lambda/tokio, smithy/powertools, smithy SDK). None is held out. Python overlays and the already-measured serde/json overlay are excluded. The closed probe, control template, set driver and audit are reused at their committed bytes, unchanged (byte-checked against `HEAD` before the run). Read sets are repository-only, as in the closed precedent; dependency-source sets are not invented.

Per workload, three warmups and seven measured fresh children ran under the ordinary lane with a private 0700 Darwin TMPDIR, unchanged HOME, and observed priority 10 on the parent and every child. Every member tree was verified against its corpus digest before reading. 200 children exited zero with empty stderr. One child refused: the first `rs-very-large-aws-sdk-rust` child exited 1 because its registered snapshot shape check (outside the timed span) rejected the inventory under `source-inventory` `maxItems` 100000. The driver retains the refusal and does not run that workload's remaining nine children. The audit derives that workload's exact sorted inventory from the retained refusal evidence (the ValidationError instance) and confirms that `maxItems` is the only schema error. That workload has no timing.

| Workload | Regular rows | Source bytes | Snapshot descriptor bytes | Median ms | Max ms | Within snapshot2 bounds |
|---|---:|---:|---:|---:|---:|---|
| js-large-webpack | 20693 | 57599308 | 3250401 | 850.523333 | 2369.265291 | yes |
| js-small-body-parser | 25 | 183051 | 3303 | 0.931459 | 0.955000 | yes |
| poly-large-rspack | 23980 | 69293473 | 4085164 | 1048.928666 | 1056.229333 | yes |
| poly-small-node-rs | 231 | 16765832 | 30845 | 13.170958 | 13.227667 | yes |
| poly-very-large-deno | 14920 | 93725209 | 2227549 | 591.214167 | 657.035000 | yes |
| rs-large-smithy-rs | 3632 | 51487333 | 647602 | 157.832083 | 174.281083 | yes |
| rs-small-http | 48 | 588072 | 6070 | 1.822042 | 1.875833 | yes |
| rs-small-http-body | 37 | 146468 | 5167 | 1.337375 | 1.359250 | yes |
| rs-small-hyper-util | 60 | 584971 | 7939 | 2.412167 | 2.466875 | yes |
| rs-small-tower | 162 | 567491 | 20926 | 5.770333 | 6.112625 | yes |
| rs-very-large-aws-sdk-rust | 245250 | 2070831625 | 40252878 | refused | refused | NO: rows100000, descriptor4MiB |
| rs-very-large-sui | 19063 | 203261240 | 3509292 | 824.899417 | 832.090417 | yes |
| ts-large-typescript-eslint | 7578 | 24757508 | 1456883 | 321.481167 | 350.261375 | yes |
| ts-small-constructs | 45 | 474408 | 5801 | 1.600083 | 1.636542 | yes |
| ts-small-nextjs-commerce | 78 | 493971 | 10194 | 2.846750 | 2.890250 | yes |
| ts-very-large-aws-cdk | 29360 | 1194848648 | 6519493 | 1618.239084 | 1622.447917 | NO: descriptor4MiB |
| ts-very-large-aws-sdk-js-v3 | 51178 | 615098659 | 8415558 | 2007.434459 | 2029.570667 | NO: descriptor4MiB |
| ts-very-large-vscode | 19945 | 286658620 | 3391452 | 919.520542 | 925.357542 | yes |
| mr-rs-large-aws-lambda-tokio | 2393 | 14006177 | 376607 | 84.004000 | 84.774125 | yes |
| mr-ts-large-smithy-powertools | 3704 | 19360744 | 690966 | 133.502250 | 135.264084 | yes |
| mr-ts-very-large-smithy-sdk | 53493 | 626640522 | 10294441 | 2089.836166 | 2113.830208 | NO: descriptor4MiB |

## Findings against snapshot2's bounds (PROPOSAL-r5 SM-5, MC item 5)

- **Rows (100,000):** rs-very-large-aws-sdk-rust exceeds the row bound on its repository-only read set.
- **Descriptor (4 MiB):** mr-ts-very-large-smithy-sdk, rs-very-large-aws-sdk-rust, ts-very-large-aws-cdk, ts-very-large-aws-sdk-js-v3 exceed the 4 MiB snapshot-equivalent descriptor. The registered schema bounds rows, not descriptor bytes, so the three sealed workloads among them pass the registered shape check while exceeding the SM-5 descriptor bound; the refused aws-sdk-rust inventory misses both.
- **Total bytes (8 GiB):** no workload exceeds it.

17 of 21 read sets fit all three bounds. Every miss is a repository whose `sizeClass` is very-large or the very-large smithy SDK overlay, and adding dependency sources can only enlarge these sets. Per PROPOSAL-r5, a snapshot2 miss is MC's S-R successor question. It is recorded, not worked around: the probe, template and bounds are unchanged, and no sources were trimmed.

Raw children are retained per workload as deterministic USTAR/xz archives under `raw/`. Each member's produced bytes are pinned in `raw-pins.json`. `audit_remaining.py` is new; it follows the closed audit's identity, shape and statistical checks but records the bounds instead of asserting them. It reproduces `checks.json` from either the loose or the packed children. Public control identities match the synthetic host replay fixture, which is not the private 413 fixture. Run on the lead macOS host, not D12; timings are preliminary. Overlay configuration is not captured, and no root manifest is invented.

SM5FigureComplete=false, SM5PlaceholderFilled=false, SMComplete=false, LG1Met=false, snapshotPlanIdentitiesAdmitted=false, dependencySourceSetsIncluded=false, effectiveL=false, productQualification=false. No F or T. Product, law and lock are unchanged.
