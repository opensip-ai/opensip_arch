# S-M cold-reset series for the TS-row components (U-5a)

This is an outside-product measurement, unit U-5a of the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`, D-7 and U-5). It applies Q0 §9.2's **cold** reset (`harness/DESIGN.md:798-801`) to every F and T component of the six TS rows:
- SM-1 (TS start);
- SM-5 sealing (all 13 read sets, Rust repository-only parts included);
- SM-7 transfer (repository-only sets);
- SM-2 (the configuration cohort, and the express synthesized program under D-4);
- SM-9 at the six TS row sizes under D-1 (141, 193, 678, 936, 1,159, 1,381).

The Rust rows' cold series (U-5b) follow U-1 and U-2, which change Rust SM-4, SM-5 and SM-7. This unit fills no placeholder, computes no F or T and records no outcome.

## The cold reset

`cold_reset.py` runs before **every** run, warmups included, as the first statement of each runner's measured loop and before any timestamp, so no reset work is timed. It does three things:
1. **OpenSIP state.** It deletes the project's OpenSIP state. None is ever created: `Application Support/OpenSIP` is asserted absent.
2. **Disposable caches.** It replaces them with a fresh, empty, private 0700 per-run TMPDIR under the set's TMPDIR, deleting the previous run's first.
3. **Page cache.** It records the OS page-cache state with `vm_stat`: raw output, page size, and file-backed, purgeable and free pages. The page cache is never claimed flushed.

The caller then starts a new process. The label is **"cold OpenSIP state, page cache recorded"**. `cold-reset-records.json` in each component directory holds one record per child, in order.

## The runners

`build_cold_runners.py` copies each accepted runner byte for byte into its own directory, so its outputs never overwrite accepted evidence. It makes only these insertions:
- the `cold_reset` import;
- one `_cr.reset(env,T)` as the first statement of the single measured loop;
- `_cr.write(...)` before the lane is released.

The replay variant also restricts its sizes to the six TS row sizes and redirects its outputs. `ACCEPTED-RUNNER-SOURCE` names each accepted runner. The audit checks every diff (`allDiffsConfined` True).

Recipes are otherwise unchanged: 3 warmups and 7 measured runs, the lane held, priority 10, and the accepted inputs and pins.

**First sealing attempt.** It omitted the probe's sibling `control-template.json`, so its first child exited before any measurement. It is retained as `sealing-attempt0-missing-control-template/` and `run_all-attempt0.log`. The rebuild copies the file; nothing else changed.

## Results (lead macOS, preliminary, not D12; ms)

Accepted warm medians are shown for information only; no ratio or claim is drawn.

| Component | Workload | Cold median | Cold max | Accepted warm median |
|---|---|---:|---:|---:|
| sm1 | SM-1 | 82.938 | 84.772 | 81.849 |
| sealing | js-medium-express | 8.319 | 8.575 | 6.891 |
| sealing | poly-medium-napi-rs | 25.994 | 120.406 | 23.219 |
| sealing | rs-medium-aws-lambda-rust-runtime | 22.132 | 22.518 | 19.476 |
| sealing | rs-medium-axum | 19.931 | 20.125 | 17.446 |
| sealing | rs-medium-hyper | 5.202 | 5.246 | 4.719 |
| sealing | rs-medium-serde | 12.440 | 12.617 | 11.043 |
| sealing | rs-medium-serde-json | 3.322 | 3.452 | 2.948 |
| sealing | rs-medium-tokio | 31.590 | 31.969 | 27.853 |
| sealing | ts-medium-powertools-lambda | 51.730 | 51.973 | 45.720 |
| sealing | ts-medium-smithy-typescript | 90.620 | 91.202 | 80.099 |
| sealing | ts-medium-umami | 74.845 | 75.825 | 66.081 |
| sealing | ts-medium-vite | 116.639 | 117.186 | 102.499 |
| sealing | mr-rs-medium-serde-json | 15.795 | 15.982 | 13.844 |
| transfer | js-medium-express | 6.762 | 6.841 | 4.923 |
| transfer | poly-medium-napi-rs | 20.053 | 20.230 | 15.207 |
| transfer | rs-medium-aws-lambda-rust-runtime | 15.253 | 15.880 | 10.657 |
| transfer | rs-medium-axum | 13.396 | 13.421 | 9.174 |
| transfer | rs-medium-hyper | 5.098 | 5.257 | 3.936 |
| transfer | rs-medium-serde | 9.809 | 9.972 | 6.933 |
| transfer | rs-medium-serde-json | 3.937 | 3.946 | 3.198 |
| transfer | rs-medium-tokio | 22.735 | 22.764 | 15.842 |
| transfer | ts-medium-powertools-lambda | 35.210 | 35.533 | 24.416 |
| transfer | ts-medium-smithy-typescript | 59.740 | 61.106 | 41.624 |
| transfer | ts-medium-umami | 50.206 | 50.372 | 34.211 |
| transfer | ts-medium-vite | 74.518 | 75.247 | 54.558 |
| cohort | js-medium-express | 94.235 | 94.509 | 92.757 |
| cohort | poly-medium-napi-rs | 1032.496 | 1036.900 | 1026.995 |
| cohort | ts-medium-powertools-lambda | 3617.434 | 3638.858 | 3465.558 |
| cohort | ts-medium-smithy-typescript | 16308.127 | 16599.411 | 16295.809 |
| cohort | ts-medium-umami | 2236.398 | 2330.607 | 2302.595 |
| cohort | ts-medium-vite | 7939.892 | 8136.795 | 8059.187 |
| synthesized | js-medium-express | 261.685 | 263.864 | 257.128 |
| replay | replay-141 | 1241.411 | 1246.288 | 1177.007 |
| replay | replay-193 | 1866.231 | 1907.113 | 1844.642 |
| replay | replay-678 | 15657.685 | 16114.688 | 16514.905 |
| replay | replay-936 | 28590.503 | 29540.577 | 28515.224 |
| replay | replay-1159 | 43491.232 | 53588.048 | 44501.860 |
| replay | replay-1381 | 59405.096 | 63440.959 | 62508.590 |

**Evidence.** Bulky raw evidence (the cohort's per-run evidence, and sealing's per-run outputs and inputs) is in `raw-evidence.tar.xz`; `raw-evidence-index.json` pins every member.

## Standing

- **Host and label.** Lead macOS host, preliminary, not D12. The page cache was never flushed, only recorded.
- **Values.** No F, T, outcome or placeholder.
- **Gates.** L-G1 is open, and L is not in effect.
