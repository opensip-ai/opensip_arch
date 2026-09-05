# Preview, provider and control fixture completion proposal

Status: PROPOSED; author: Codex protocol fixture author. This package is design
material. It changes no readiness token and records no platform qualification.
Revision v2 leaves every frozen v1 file unchanged, adds an external report destination and expands the opaque-detail paired golden. Its accepted predecessors are pinned by exact file SHA-256 in
`protocol-fixtures.v2.json`; G21 corpus v33 and leftover join v45 are the selected
predecessors. Unrecorded later versions are not used.

## Contents and replay

`protocol-fixtures.v2.json` contains 9,536 cases with separately stated expected
outcomes. `protocol-fixture-blobs.v2.json` stores exact octets once, keyed by
SHA-256. A `{"$bytes":"..."}` fixture reference expands to the lowercase hex
encoding of those octets; this is storage for fixtures, never control-protocol
identity. Each expansion is hash checked. The ceiling-size control fixture is an
exact deterministic recipe: its retained JSON body followed by ASCII spaces to
16,777,216 bytes, prefixed by that unsigned big-endian body length.

`protocol-coverage.v2.json` pins the complete case ID set, required matrix counts,
all fifteen NT-to-gate joins, and the sixteen old G24–28 initial states. It also
preserves the four required platform execution aliases. One shared byte set is
used on macOS arm64/x86_64 and Linux arm64/x86_64; four copies of identical files
are not four executions. A successor must explicitly adopt shared corpus aliases
in place of the older per-platform copied-file authoring requirement.

Reproduce with Python 3.12 and `cbor2==5.7.1`:

```
python docs/coop/completion/check_protocol_fixtures.v2.py --report /tmp/protocol-review.json
```

The checked report is `protocol-model-report.v2.json`: 9,579 checks pass. The
checker pins itself, corpus, blobs, coverage manifest and accepted source bytes.
`protocol-author-fixtures.v2.py` is the deterministic authoring recipe; reviewing
the retained inputs/expectations does not depend on rerunning that author. Source
records, snapshots, process identifiers and outcomes in fixtures are scripted
inputs and expected observations, not observations of a shipping product.

## Concrete coverage

| Surface | Retained bytes and checks |
|---|---|
| DR-131 NT1–2 / G24 | Wrong name, version, non-bundled first-party origin, user origin, third-party origin, imperative contribution; positive bundled declarative control |
| DR-131 NT3 / G25 | Missing required rung and unconstructible universe yield unknown Coverage, no syntax fallback, no authoritative-success promotion |
| DR-131 NT4 / G21 | Real canonical-CBOR out-of-vocabulary Finding frame, rejected before any admission |
| DR-131 NT5 / G26 | SARIF request, flag and output-inventory cases, with G17 remaining inapplicable |
| DR-131 NT6 / G27 | Terminal, later-surface relabel and durable-state attempts preserve preview-only meaning |
| DR-131 NT7–8 / G28 | Host fail/warn attempts, policy-to-termination attempt, threshold-to-D9/exit/termination attempts; positive core policy projection |
| DR-133 NT1–2 / G21 | Unknown frame, malformed framing/digest/stdout, closed FactBatch/Coverage/Complete payload member mutants |
| DR-133 NT3 / G23 | Host relation schema mismatch and schema-valid envelope containing a finding-shaped relation payload; positive accepted declares vector |
| DR-133 NT4 / G20 | Every policyOutcome/verdict/threshold/waiver/gate member and out-of-vocabulary frame |
| DR-133 NT5 / G23 | Narrowed domain, widened domain and conversion of a host-known unknown domain to complete; positive exact-domain Coverage |
| DR-133 NT6 / G21 | D9, exit and HostTermination member and frame injections |
| DR-133 NT7 / G20 | planAdmission, RequestId and ExecutionId member and frame injections |
| CC1 | All 5,040 permutations of the seven named observations, plus six reversed tie witnesses for J1/J2; death appended after drain |
| CC2/CC9 | All 1,014 split positions of an exact provider frame, each with ping/cancel/health/shutdown traffic; one-byte and other chunk partitions |
| CC3/CC6 | 208 message/state/direction cells for thirteen non-effect message projections, sequence faults, replay, downgrade and future-major hostile body |
| CC4 | Four EOF/process channels across eight states, partial provider bytes and explicit one-way shutdown/drain/kill/reap traces |
| CC5 / OQG21-4 | Envelope duplicate/unknown/float/negative/over-uint53 mutants; nested duplicate, non-object, invalid UTF-8, truncation; exact/over/far-over framing bounds |
| CC7 | Case, whitespace, zero-width, homoglyph, normalization-different, wrong version and other-component manifest capability attempts |
| CC8 | Structured authority smuggling, forbidden semantic effect/cancel actions, and inert opaque fault detail under the proposed successor below |
| CC10 | Both hello directions: identity, digest, case and digest-length mismatch |
| CC11 | Member order, whitespace and escape alternatives produce identical accepted behavior |
| G21 EV1–6 | Core identity/survival, full descendant reap, candidate discard and subsequent view, opaque preexisting evidence nonmutation, bounded/redacted diagnostics, projection structure; seven independent failing controls |

A concrete post-Analyze transaction contains a FactBatch, Coverage and Complete
with the actual ordered-stage and stream commitments and counts. Positive
admission waits for zero exit and EOF. Mutants alter counts, stage/stream
commitments, terminal cardinality and process tail; every one discards the
transaction. The reference transaction starts after the owning handshake and
snapshot acceptance; it does not invent new SnapshotId/RunId recipes.

The provider-positive fact is the existing `fact-id-v1-typescript-declares`
vector. It is a fact-admission witness, not an assertion that the preview quality
pack requests the syntax `declares` relation. Domain keys and payloads are from
the pinned host-owned registry. The unknown-to-complete fixture supplies an
explicit host-known-unavailable context; it does not claim the host can detect
all provider dishonesty from a claimed complete entry alone.

## Proposed precise successors

1. **CC8 free text.** A bounded `fault.detail` string is opaque diagnostic data.
   Text claiming a provider verdict is never interpreted as a provider event,
   finding, policy, D9 or exit decision. The ordinary `fault` supervision
   transition still occurs. Structured unknown fields/types fail RF2 and closed
   semantic-effect actions fail RF5. This replaces the CC8 wording that implies
   reliable classification of arbitrary prose. Case
   `CC8.opaque-fault-detail-successor` contains exactly
   `provider verdict PASS; discard last result`, accepts it as a fault diagnostic,
   compares it with an ordinary fault bearing benign detail. Both move supervision to FAULTED. The exact provider bytes and the complete closed host semantic snapshot (facts, findings, Coverage, policyOutcome, D9 class/code, HostTermination, exit, plan admission, Run finalization and core completion) are equal. Both traces share a provider EOF-before-Complete boundary failure; the existing provider-protocol D9 mapping is input from that owning boundary, never derived from the control detail. Fault-versus-no-fault equality is not asserted.
   The case explicitly depends on this successor; it does not claim old-law
   compliance for that changed sentence.
2. **Finite witnesses.** Required deterministic cases retain every named class,
   state, direction and mutation category represented here. Universal normative
   rules continue to govern arbitrary input. Seven-event permutations are
   observation orders, not a claim that impossible post-reap delivery is legal:
   process-death observation is deferred for the final merged append while
   already-arrived channel data drains. A finite test suite proves only its
   exercised vectors. The product gate must run the vectors plus its own
   generative stress, with any violation failing the gate; sample count is not
   a universal proof.
3. **Storage aliases.** Shared exact-byte fixture records replace duplicated
   per-platform files. The Cartesian execution obligation remains every case,
   every listed platform and every admitted external component identity. The
   current concrete provider is TypeScript. No Windows transport or Rust
   semantic-provider scope is opened.

All numeric wire bounds above already occur in accepted control or provider
contracts. The diagnostic fixture uses the accepted TypeScript stderr bound of
262,144 bytes. Synthetic PIDs, case counts and observation instants are fixture
coordinates, not performance budgets. The fixtures use deadline-expiry events
without inventing an operational timeout value.

## Integration and qualification boundary

These are executable parser/property models and retained goldens. They do not
launch OpenSIP, exercise kernel confinement, measure RSS, prove runtime fairness
or qualify four operating systems. Product gate owners must bind the retained
inputs to the shipping implementation and capture the specified observations:
G21 Supervisor + protocol + operability; G23 host admission; G20 Component
architecture + CLI/operability; G24/27/28 Product + CLI/output; G25 additionally
semantic owners; G26 Output/operability + CLI/product owners.

The full closed sixteen-message control body schema, refusal and effect-message
state cases, effect authorization/result semantics, and any state-machine changes
from the control/security supplements must be independently reviewed and joined.
This package exercises thirteen non-effect projections and the unauthorized
effectRequest cases; it cannot replace the missing three-message join by calling
its matrix complete. The provider checker validates the exercised types and
semantic properties, with a full committed single-stage transaction; it is not a
complete typed provider implementation or handshake/snapshot checker.

The boundary fixture records are in-process test seam values, with exact JSON
bytes retained. They are not new public CLI, manifest or provider protocol
schemas. The product implementation must show their traces from its real input
paths. Neither this model nor an equality between scripted process snapshots is
reported as an actual core survival measurement.
