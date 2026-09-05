# Core gate design evidence v1

Author: Codex security_behavior_review. Proposed for independent parent review.
This unit supplies synthetic scorer inputs and expected outputs for the active
G01–G05 occupancy predicates. It changes no threshold, fleet, waiver or gate
standing. All86 historical initial-state identifiers receive exact result links.
The old files are unchanged; historical `UNDECIDED` names are not current rules.

The contract pins active occupancies G01v11/G02v6/G03v5/G04v5/G05v4, the five
naming catalogs and their detailed inherited timing/delta rules. It pins the
parent's proposed core/accounting and doctor sections separately, so parent
edits outside those sections do not invalidate unrelated evidence. Parent
normative approval remains separate from this unit's independent review.

There are114 compact cases over six shared bases. Each patch produces a concrete
input; expected results are retained independently of the evaluator. The checker
also replays exactly the six existing G02 accounting cases and25 doctor RSS
cases, without rerunning their wider suites. All four fleet labels and both
help/version commands have executed synthetic timing, no-load and RSS cases.
G05 has a synthetic case for each of the four platform labels. These labels
parameterize design records; no OS measurement run is claimed.

G01 checks all six offered platform/container slots, inclusive25,000,000 bytes,
publication custody, required signature/SBOM references and every default-install
exclusion. Size quantities and the publication map are independently acquired
trusted observations at production integration. The model does not authenticate
release signatures or claim that a25MB byte array is a signed pkg/tar.zst.
G02 adds exact path/digest inventory uniqueness, declared dependency closure,
acyclic roots and layer/shared-executable checks to the existing accounting cases.

G03 uses N21 and nearest ranks11/20/21, with the five100/150/250/50/100ms bounds.
Warm p50 is reported as telemetry. Sorting, every bound, malformed records, wrong
fleets, universal projections, translated execution and timing instrumentation
have explicit cases. Preflight and capture observations are trusted inputs;
this model does not implement D-102 capture or prove their real acquisition.

The two FC-G03 fixture trees contain actual retained inert hostile input files.
Their local digest is SHA256 of a compact lexical list of[path,fileDigest]. This
is fixture custody, not a new product TreeCommitment identity. The checker reads
and hashes every file. No fixture script is executed. Dedicated no-load records
bind both trees, distinct launch IDs, an empty external workdir and absence of
environment/PATH pointers. Open/read/exec/mmap events on either tree fail;
an inventory name alone does not. Missing capture, wrong fixture pin, launch
reuse and missing reap fail. Real OS capture completeness remains qualification.

G04 scores all42 help/version launches (21 cold/warm pairs), each peak and
steady quantity, with40/50 decimal MB bounds. Linux VmRSS kB is multiplied by1024;
macOS resident_size is already bytes. Cadence, process target and source API are
checked. The inherited25-case doctor scorer retains60/100 MB, one launch per
sample, and the explicit read-only modes. Analyze and consented probes are
outside the applicable G04 scoring domain, as the inherited rule specifies.

G05 requires matched21-pair observations, the same thin P, empty coreOnly
component membership, one synthetic TypeScript identity on the enabled side,
and the status/inventory endpoints. It computes median(enabled)-median(core),
with a distinguishing case against median(pair differences). Missing publication,
wrong derivation and negative start/RSS deltas refuse or fail. Download/install
quantities are exact trusted observations; installation uses adopted G02
accounting. A1GB publication passes this measurement-mandatory predicate because
G05 has no numeric cap. This does not admit a component or waive another gate.

Every state map entry has a nonempty executed result list and a separate
execution remainder. `EXECUTION-OUTPUT` is limited to G01 actual signed-container,
signature-set and SBOM release outputs; their synthetic custody checks remain
mapped. All other scoring/input requirements are `DESIGN-MAPPED`, including the
two actual FC-G03 fixture inputs. This classification does not disguise active
input/golden authoring as performance measurement.

Replay with:

```
PYTHONDONTWRITEBYTECODE=1 /tmp/opensip-architecture-review-env/bin/python -B docs/coop/completion/core-gate-design-check.v1.py --report /tmp/core-gate-replay.json
```

No product process, signature ceremony, native fleet, release waiver or real
startup/RSS result is certified. Second-qualified-release regression comparison
and waiver decisions remain their already specified qualification process; this
unit exercises the fixed absolute/measurement-mandatory predicates. No register
mutation, SATISFIED status or automatic acceptance is made.
