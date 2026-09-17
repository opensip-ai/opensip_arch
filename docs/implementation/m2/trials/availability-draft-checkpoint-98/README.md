# Private evidence availability draft 98

Copies the exact 329-file draft 97 parent. The frozen candidate has 330 files: 328 unchanged, the storage module list updated, and the already planned availability.rs added. No inventory, dependency, schema or fixture-path changes.

AvailabilityRecord uses the existing pinned RegisteredSchemas selector for the closed availability record, including exact product JSON, u64 generation, typed references and canonical-set ordering. It additionally refuses retained with missing references. Initial generation is zero; a proposed successor must name the same Run and increment generation by exactly one with checked overflow. Exact supplied record bytes are retained. No sealed Run, historical assurance or disposable index is rewritten or accepted as an input to this helper.

364 actual reference schema/order/extra-rule cases and 360 actual EvidenceStore.set_availability transitions cover all states, missing evidence and the u64 boundary. Tests additionally reject stale/skipped/cross-Run transitions, work exhaustion and nonzero initial generations. 25 storage tests and strict workspace Clippy passed. Fresh host 60 COMPLETE: 210 sources, 51 archives, 256 total Rust tests and build/tests/doctests/metadata/help/version passed.

Parsing and successor checks are inert. The eventual transaction owner must establish Run existence, read and compare the actual current generation atomically, and obtain the required security authority. A retained successor needs verified closure/restoration independently; this helper does not perform it. Pin-aware purge, shared-blob GC, persistence and command-specific error projection remain separate. No independent review, Linux/power-loss or release qualification is claimed.

Preparation initially stopped before source edits because architecture and bundled schema bytes differ in payload-registry paths. All definitions and all other top-level fields match. The failure, unchanged-parent verification and explicit resume script are retained; schema bytes were not modified.
