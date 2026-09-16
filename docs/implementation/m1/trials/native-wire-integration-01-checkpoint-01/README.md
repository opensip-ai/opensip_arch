# Current native carrier integration01 — pending independent review

This candidate integrates native07 inert carriers with generation02's current
contracts in the same eight generated paths. It does not select the final source
bridge or install product files. Native07 has actual Grok reference acceptance;
renderer05 has historical actual Claude acceptance on its earlier owner input.
The new guard, adapter, rebasing and combined output here still need review.
Historical UNIT.md, original generated/ and test_render.py describe renderer05.
Use this README for the current candidate; do not overwrite that evidence.

The closed_idl.py guard validates the complete carrier against its closed meta
schema, strictly checks names, joins every external schema reference/type name
to the selected generator entry point, and rejects recursive native declarations,
including cycles through implicit frame payload edges. render.py is unchanged
from accepted renderer05. Six guard test groups pass, including distinct
uint64 declarations that lower to the same emitted type. Fourteen renderer
probe groups pass after updating only the two expected counts:18 scalars,
50 records,22 externs. Eight selector mappings exactly match the accepted goldens.

render_checked.py output-c/output-d are identical inert fragments. assemble_eight.py
and assemble_ts.cjs place the native Rust carriers in protocol.rs, all native TS
carriers in report.ts and the TS provider's native/dependency closure in its
protocol.ts. There are30 provider declarations/12 external roots and70 report
native declarations (68 owner names plus two generated payload auxiliaries).
No ninth generated module or report-to-provider dependency is introduced.
Rust is parsed/formatted with syn2.0.119/prettyplease0.2.37; native TS uses the
pinned TS6 printer. The external TS closure uses the unchanged renderTypes
algorithm. Native owner, meta schema, options, eight base outputs, prepared TS
projection, renderer and140 compiler files/Node are pinned or frozen with this
candidate. The formatter's source, dependency lock and observed binary hash are
recorded. This is observed reproduction, not loader confinement or final bootstrap.

Fresh eight-c/eight-d outputs match each other and the exact eight-a bytes compiled
in integrated/. Existing five non-protocol Rust files remain unchanged. The
standalone current/ harness and integrated/ harness both pass nine Rust tests,
two compile-fail doctests and strict exactOptionalPropertyTypes TypeScript.
Integration adds provider-surface positive/negative assignments. Eight selector
docs and variants are checked within their actual Rust payload enums.

Clippy initially reports two infallible TryFrom lints in unchanged generated
invocation.rs. The integrated harness adds clippy::infallible_try_from to its
existing generated-module-only allowances, preserving typify's API. With that
explicit allowance Clippy --all-targets -D warnings passes. The original lib
and failure logs are preserved; the proposed final package lint binding remains
a review item. No lint is disabled for handwritten code.

This is inert representation only. No bounded CBOR parser, semantic admission,
production matchers, sender, prepared-read custody, publication or product
behavior is supplied. Current generation02's default report reader remains
4MiB/depth32 in these base files; the separately staged profile6 report codec
still needs to be combined with this adapter before final output selection.
Source decisions, package inventory, bootstrap, full tool closure and actual
independent integration review remain open. No M1 or release acceptance follows.

Reproduce with the pinned reference Python -I -B: check_closed_idl.py,
test_render_current.py, render_checked.py with fresh output labels, then
assemble_eight.py with fresh labels. Its checked native fragment input remains
output-c. check_integration.py compares the frozen output goldens and compiled
harness bindings. Cargo test --locked --offline in integrated/; use the pinned
Node/TS6 tsc --project integrated/tsconfig.json. Recorded Clippy command is
cargo clippy --locked --offline --all-targets -- -D warnings.
