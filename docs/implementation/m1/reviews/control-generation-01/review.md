# Review: common-control generation extension (subject 01)

- **Verdict:** ACCEPT-UNIT, carriers and shape only
- **Subject manifest SHA-256:** `c4d3c10dde2fdf2eeb1eb5f396796ebcc6cfe7a57e65cffdb3bb96fe02e1679c`
- **Required findings:** none

This unit adds the exact existing control schema3 to accepted adapter04 as the 29th source. That gives 587 roots and 14 provider roots, with `Control3Root` emitted in the protocol module. The TS runtime now enforces `x-maxUtf8Bytes`. The Rust projection gets private unique titles for conflicting direct object properties of named `oneOf` branches. All three changes are correct within that scope.

This is not integration. It is not source-selection promotion, not control-protocol semantic admission, and not M1, product or release qualification.

## What I verified independently

- **Exact set:** 88/88 files matched before and after the review.
  - During the review my read-only import created a `__pycache__` in the frozen subject. I removed only that file and re-verified the exact set (see Limits).
- **Scope of the change:** compared with parent adapter04, only the claimed files changed.
  - The Rust modules for the other roots differ only in their two header hash lines.
  - `report.ts` keeps all 28 previous embedded schemas byte-for-byte and adds the control schema bytes exactly.
- **Source and metadata:**
  - `control.v3` is byte-identical to the architecture schema (`2929de62…`).
  - All 29 rows agree across options, registry, recipe and source-map. There are no duplicate type names or namespaces.
  - No other source uses the new keyword.
- **Naming transform:**
  - Across all 587 definitions, the transform changes only `Control3Root`. It adds 16 unique titles that collide with no definition name or existing title.
  - A scan for remaining name collisions finds 1 without the transform and 0 with it.
- **Fresh generation:** 8 outputs, nothing changed, registry hash `a2155988…`.
- **Tests and compilers:**
  - All 78 unit tests pass.
  - Clippy passes with `-D warnings`.
  - Strict `tsc` passes on the report and provider outputs.
- **Corpus:** rerunning `corpus.py` from the pinned 480-case source reproduced 194 cases (79 positive, 115 negative) byte-identically.
- **TS probes:** 0 mismatches against my Python reference over the 194 corpus cases plus 858 new probe cases:
  - all 21 UTF-8 sites, at 1 to 4 bytes per character, at and past each limit;
  - integer min, max and just outside, for all 16 variants;
  - all 240 cross-variant body swaps;
  - 14 lexical frames.
  - Other direct checks: a bound of 0 behaves correctly, a lone surrogate is refused, and every malformed bound is refused.
- **Rust probes:**
  - All 79 positive frames, covering all 16 variants, roundtrip exactly.
  - No schema-valid case is rejected, and no accepted case fails roundtrip.
  - All 232 invalid body swaps are rejected, so bodies are no longer conflated.
  - Integer and presence mapping is lossless.
- **Old witnesses:** 1338 of 1343 pass on the new TS runtime. The other 5 are the three denied refs, which are correctly refused. This matches review 04.
- **Live source preflight:** I reproduced the refusal ("generation source is not selected by accepted design"). With only the control row removed, the copy passes, and parent adapter04 passes.

## Advisories

1. **CA1 – Preflight receipt was empty.** The validation `source-preflight.json` is 0 bytes.
   - I reproduced the refusal myself.
   - The subject's own `tools/verify_design.py` has no source preflight and passes, so integration must bind the binding4 preflight.
   - Integration must also promote the exact raw schema through a reviewed source-selection unit. Don't weaken the verifier or rewrite history.
2. **CA2 – The naming fix is narrow.** It covers only `type: object` properties directly inside a top-level `oneOf`. Enums, constrained strings, arrays and nested unions could alias the same way in a future schema.
   - Add a check in `prepare.py` that refuses any remaining collision, so it fails closed.
   - Titles are based on property position, so adding a property renames private Rust types. Wire names are unaffected.
3. **CA3 – No in-tree tests for the new behaviour.** The body-collision fix and the `x-maxUtf8Bytes` rules (enforcement and malformed-bound refusal) have no tests in the tree. Add them before integration.
4. **CA4 – The Rust carrier is inert and looser than the schema.** It accepts 29 of 115 corpus negatives, plus most UTF-8 and range negatives in my probes.
   - This is by design, but `Control3Root` must never be treated as admission.
   - `crates/components/src/control_protocol.rs`, the declared semantic owner, does not exist yet.
5. **CA5 – Stale metadata and untracked route.**
   - `openObligations` still lists common control owner selection.
   - `control-source-route.v1.json` is untracked in the architecture checkout.

## Limits

- Not reviewed: framing, state, sequence, correlation, permission and effect semantics.
- Adapter04's confinement, dependency and build algorithms were not re-audited, because this change doesn't touch them.
- My reference validator uses the same jsonschema library as the author's. I wrote the UTF-8 extension separately.
- The collision scan is a heuristic, not a proof.
- The architecture checkout is dirty, so pins were verified by hash only.
- No native IDL, no final report owner, and no integration or qualification of any kind.
- Self-disclosure: my naming scan imported the frozen `prepare.py` without `-B`, which briefly created `tools/contracts/__pycache__/prepare.cpython-314.pyc` in the subject. I removed only that file and re-verified the exact set.

All probe scripts, inputs and results are under `work/`, with hashes listed in `review.json`.
