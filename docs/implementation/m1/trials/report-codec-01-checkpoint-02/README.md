# Report codec candidate01 — unaccepted

This adds a fixed report JSON profile in TypeScript and Rust:27,829,365 bytes and
39 container levels, derived from the exact current joint report schema. The
existing4MiB/depth32 codec and canonical identity hash functions retain their
limits. One parsing/encoding algorithm per language serves both fixed profiles;
callers cannot supply arbitrary profile limits through the proposed public API.

TypeScript exports `parseReportExact` and `canonicalReport`. The generated report
wrapper chooses this codec only for the exact selected ReportProjection1 root;
other roots retain the default codec. Generation refuses a different report root
before emitting files. Runtime ordering and uniqueness checks use the selected
codec within the report. Schema documents still use the default codec.

Rust proposes `parse_report_json`, `report_canonical_bytes`, `REPORT_MAX_BYTES`
and `REPORT_MAX_DEPTH` exports from the identity primitive crate, reusing its
private parser/encoder. This API placement needs actual independent review;
reporting already has the approved dependency on identity. The digest module is
unchanged and still calls the default canonicalizer. No product file was changed.

Verification:

- 102 TS codec checks cover inclusive byte limits, depths, exact integers, Unicode,
  duplicate keys, getters, shared bytes and immutable enforcement despite CJS
  informational-export mutation.
- 13 Rust tests pass, including all10 unchanged baseline groups and3 new profile/
  hash-boundary groups. Clippy with warnings denied passes.
- A 4,202,744-byte dense report is captured from the unchanged full joint reference
  admission; only that test's final evidence write is redirected. It passes the
  generated runtime and exact Rust/TS canonical round-trip, while the default
  codec refuses it. This is a synthetic reference fixture, not an actual Run,
  delivery or release/performance qualification.
- 62 current report/envelope cases plus6 generated wrapper controls pass, including rejection of the stale inventory5 provenance.
- 3,014 deterministic Rust/TS comparisons agree:3,000 accepted canonical values and
  14 lexical refusals. The dense report bytes also agree exactly across languages.
- Repeated TS generation matches. Six Rust carrier files and the provider's type
  body are unchanged from joint-generation checkpoint02.

The current generated interfaces are in `output02/`, reproduced at `output03/`. Rust codec changes are under
`rust/`; `probe/` is a separate conformance harness, not a proposed product crate.
`profile-source.json`, `tool-closure.json`, `rust-source-selection.json` and result
files identify inputs and scope. The initial Rust edit script hit its duplicate
text guard before emitting modified source; that failed attempt is preserved.

Remaining work includes actual Claude review, final source/API/inventory/recipe
selection, Rust host/report consumer integration, embedded owner byte/depth and
semantic admission, browser/runtime and release qualification. The InvocationRecord
codec question L01 and required-output policy L02 remain separate and unresolved.
This candidate implements codecs; it does not implement complete report admission
or delivery. Maximum permitted document performance is not qualified.

The provenance defect in `follow-up-findings.json` is corrected in joint checkpoint06
and this current source rebase. The report schema and fresh fixtures name inventory6;
the generated consumer refuses the old marker. All Rust codec/probe sources and
TS codec/template algorithms remain byte-identical to checkpoint01. Earlier
102 TS boundary checks,13 Rust tests and Clippy evidence are inherited for those
unchanged algorithms; current tests rerun62 reports plus6 controls, dense full
reference/generated admission, and3014 Rust/TS comparisons. The dense fixture
changes only its provenance marker and remains4,202,744 bytes.

`generate_rebase02.py` performs two fresh TS generations with the current source
and codec closure, copies the six exact pinned Rust carriers, and compares all
eight resulting files. It does not claim to run the Rust generator again.
`rebase-result02.json` verifies that unchanged-source claim and distinguishes
current runs from inherited evidence. Earlier checkpoint01 is preserved.
