# Named performance fleet and workload scope

Author: Codex lead. PROPOSED. Scoped successor to analysis-quality-completion.v2
§3 and its G13 result carrier, responding to WA-7 and WA-17. All behavior,
capability, corpus, authority, numeric ceiling and regression decisions remain.

## Fleet and comparison

G13 runs on all four existing D-102 classes: `macos-15` (macOS arm64),
`macos-15-intel` (macOS x86_64), `ubuntu-24.04` (Linux x86_64), and
`ubuntu-24.04-arm` (Linux arm64). This explicitly replaces the floating
“dedicated four-vCPU/eight-GiB worker for each target” sentence. The published
class has three vCPUs for macos-15 and four for each other class. Actual RAM,
CPU model, image/build, kernel, filesystem and measurement tool are observed
and retained; no eight-GiB machine is invented for these classes.

The trusted qualification wrapper acquires those runner observations separately
from the candidate result. `g13-result-schema.v3.json` adds `runnerClass` and
allows observed positive CPU/RAM values. `check_g13_result_design_v3.py` checks
the exact class/platform/vCPU relation and the report's hardware/image fields
against the separately supplied trusted runner inventory. Absence or disagreement
cannot yield a valid PASS. Synthetic inventory values in the reference tests
are explicitly not measurements. Production acquisition and evidence custody
remain G13 qualification work.

The paired security platform successor distinguishes a development template's
measured build from the release profile acquired on its actual selected class.
A template named 25G83 does not qualify a macos-15 build. G03/G04 retain their
existing class labels and numerical methods; their synthetic core-gate reference
cases therefore need no relabeling to match this choice.

Every platform independently meets cold p95 ≤10,000 ms, warm p95 ≤5,000 ms,
and process-tree peak RSS ≤1,073,741,824 bytes. Five warmups, thirty cold and
thirty warm measurements, nearest-rank p95 (rank 29), concurrency one and the
same signed closure/corpus rules stand. Each class maintains its own baseline;
no faster class can compensate for another failing class, and no cross-class
percentage comparison is meaningful. A >10% latency or RSS regression still
fails even below the absolute ceiling. A changed image/measurement environment
requires paired recapture of the prior qualified release on the current class
before regression scoring, not an automatic baseline reset. The trusted baseline
context names the same class and current measurement environment.

The owners remain Language quality + Product + Release engineering. The reason
for this successor is to make the already decided targets executable on the
adopted fleet, not to lower a threshold or remove a platform. Retained all-class
acceptance, wrong-class/vCPU, mismatched hardware, absent inventory, mismatched
baseline and at/over-threshold cases falsify the result-validation design.
Actual inability to meet a target requires a reviewed D-006 successor; it
cannot be hidden by changing the runner or dropping that platform's budget.

## Workload scope

The absolute latency and RSS targets bind to the exact retained 1,000-module
`linear-chain-0-through-999` benchmark and its declared compiler/graph work.
They do not claim worst-case bounds for every graph or a large cyclic graph.
The small native correctness corpus separately covers multi-module and self
cycles and acyclic graphs, requiring exact SCC outcomes on every platform.
The small corpus remains mandatory correctness work but is not pooled into
the benchmark's thirty latency observations. This states the existing selected
benchmark's scope explicitly; it does not relabel an acyclic input as cyclic.

A later benchmark addition retains separate measurements and a reviewed
threshold decision, rather than quietly changing the denominator behind a
previous baseline. Every original quality cell and native-corpus path remains.

## Scope prerequisite and evidence

For application, analysis-quality-completion.v2 §7's prerequisite naming
scope-rides-completion.v1 is expressly replaced by its independently accepted
v2 successor. The SD-1 AL-3 disposition and all original active negatives are
unchanged. This is a versioned prerequisite repair, not another scope ride.

The reference result tests and schemas here are design evidence only. Actual
platform/profile, native workload and release measurements remain required
before G13 is QUALIFIED. The integrated act still adds G13 to required-now
without changing the 23-row affected set.
