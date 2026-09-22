# Native admission pin correction

The first private admission test run failed22of23 tests with SourceBytes because RegisteredSchemas has its own compiled common4 SourcePin; updating the JSON admission registry alone does not update this trust binding. That refusal is correct. The candidate now explicitly changes only that common4 byte count/digest in crates/identity/src/schema_registry.rs and adds a host regression covering native schema admission and generated Rust enums: new details admitted in common4, refused in common1/common3, and unknown codes still refused. The complete source-set and corrupted-source refusal tests remain unchanged. No runtime self-rehash or fallback is introduced.

The original failing logs are retained. A fresh run is required before freezing. This was found by root native tests, not by the earlier compile-only check or Claude405's consumer audit.
