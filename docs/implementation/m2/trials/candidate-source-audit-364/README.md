# Candidate source and generator audit 364

The three schema-generated Rust files in frozen candidate363 reproduce byte for byte from the exact268/313 generators and inputs after Rust1.95 formatting. All574/1008/587 archive members were verified before use. The manifest generator received one explicit input-path adapter; both313 generators are unchanged. The generated files also match the historical313 product bytes.

The Unicode15 unassigned table matches all707 reconstructed ranges from pinned UnicodeData.txt. The full default case-fold table matches1530 mappings from all1112064 valid scalars under Python3.12/UCD15; unmapped scalars remain identity. This is a data-table audit, not a new qualification of normalization wrappers or the Unicode16 bridge.

Selected inventory32 has409 rows; candidate363 has508 files. There are213 unlisted candidate files:79 Rust source files and134 fixtures. Conversely114 inventory rows are not yet candidate files. `unlisted-files.json` accounts for every path and pin. This does not accept those paths, descriptions, APIs, fixtures, dependencies or source semantics into the product. `LAYOUT.md` proposes the next bounded source change.

Failed tooling runs are preserved. r1 resolved the interpreter symlink and could not import jsonschema; r2 retained the original interpreter path but the old temporary environment still lacked importable package files. r3 copied those incomplete directories and failed importing attrs. A fresh Python3.12 environment installed the same six pinned dependency versions offline from the local cache. r4 completed regeneration and Unicode audits, but its `/tests/fixtures/` classification missed storage/fixtures/pin-budget174.json. r5 corrects only that classification and completes all checks. Earlier80/133 counts are superseded by79/134. No failed run is counted as passing.

The successful replay retains its actual generator dependency files and hashes, Python executable hash, generator commands, source-path adapter, expected/generated output bytes, and full source manifests. These are development audit dependencies, not additions to the product dependency graph. Replay scripts still contain explicit audit paths; a portable product generator is separate work.

Actual Claude retry at06:41 received its Fable quota refusal. Grok remains the independent reviewer; no Claude agreement is claimed. This audit does not close the five-member binding/source-standing question, current authority, writers, release qualification or M2–M6. Candidate363 and both repositories were unmodified by the audit.
