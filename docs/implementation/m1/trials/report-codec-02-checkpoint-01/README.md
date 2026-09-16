# Report codec02 — coverage source rebase

Current output04 is reproduced exactly at output05 using joint-generation02 checkpoint01 and joint10 checkpoint01. The selected development profile6 retains the same fixed report codec limits:27,829,365 bytes and39 container levels. Default canonical identity/envelope limits remain4MiB/depth32.

The TS and Rust codec algorithms/templates are byte-identical to codec01. The report source schema and generated report carriers now include individual coverage descriptor/payload rows, retained Run or ephemeral Plan sources, and the current native schema provenance. Six freshly generated Rust carriers from generation02 are copied exactly; TS generation executes twice here. This is not another Rust generator invocation.

71 generated-wrapper checks pass, including64 current complete report/envelope cases, a4,202,613-byte dense report, canonical round trip, default envelope refusal, unknown-root refusal, stale inventory marker and stale profile refusal. The dense fixture passes full joint reference admission and current generated validation. It is synthetic reference evidence, not a native-admitted maximum-width Run or delivery qualification.3,014 deterministic Rust/TS comparisons pass (3,000 canonical accepts,14 lexical refusals); the dense bytes agree exactly. All1,558 joint10 checkpoint members remain unchanged after the capture.

Earlier102 TS boundary checks,13 Rust tests and Clippy apply to unchanged algorithm bytes. The current Rust conformance probe was rebuilt; generated consumer, dense-report and cross-language checks were rerun. A test-harness log-name collision preserved the older log and was resumed under an unused name; see run03-continuation-note.json.

The historical rust-source-selection.json retains its earlier profile-source hash. Current profile-source.json and rebase-result03.json bind the same Rust codec bytes to profile6. No earlier receipt is rewritten or promoted into a new acceptance.

Remaining: actual independent review, final source/API/inventory/bootstrap selection, current browser reader and views, host/source custody, report delivery and release qualification. L01 whole InvocationRecord codec and L02 required-output capacity policy remain separate. No product files were installed.
