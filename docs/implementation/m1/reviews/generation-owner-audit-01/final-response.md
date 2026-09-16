I've written `audit.md` and `audit.json` to `/tmp/opensip-implementation/m1-generation-owner-audit-01/`, and `audit.json` parses. Nothing else was changed and I made no commits. No generator, drift trial or schema validation was run: the checks were hashes, `$ref` resolution, name collisions, if/then/else counts and manifest membership. Every cited owner's current bytes are in the source45 manifest, except the three `metadata-v1` paths.

**Problems with the current trial**
- **It produced nothing.** Exit code was 101 and output was 0 bytes: typify 0.8.0 panics on `if/then/else`, which 19 of the 28 schemas use, including envelope4 and identity v3. Getting a generator that handles this comes before any protocol work.
- **Wrong metadata paths.** The trial registers the `metadata-v1/*` paths. The bytes are identical to `metadata-v2`, but the registry must name the accepted `metadata-v2` paths.
- **The old schemas can't be dropped.** Following `$ref` by schema `$id` from envelope4, inventory4 and metadata1 reaches 19 documents, including envelope3, inventory3, policy-document v1, policy-test v1 and workflows common. There are 100 same-named definitions across the 28, so generated names need a namespace per schema `$id`, not a dedupe by name.
- **Duplicate current definitions.** `native-evidence.schemas.v2#/$defs/HelloV3`, `HelloAckV3` and `ProtocolLimitsV3` are superseded by the same-named definitions in `provider-handshake.schemas.v1` (native-evidence.md §0). Nothing outside that group references them, so excluding all three is safe. `AtomSuccessorV1` has the only dangling ref and nothing references it, so starting generation from listed entry points leaves it out without a special exclusion.

**Missing source owners for the eight files**
- **Already covered by schemas:** `identity.rs`, `evidence.rs`, `invocation.rs`, `mod.rs`, and the envelope part of `output.rs`.
- **TypeScript protocol major 2** (`protocol.rs` and `protocol.ts`): the source is `delivery.v2.json` (`47b6cfd1…`) under `$.typescriptSemanticSubstrate.providerProtocol.wireSchema`. The envelope, frame table, Snapshot*/Analyze/Complete/Cancel*/FactBatchV1 payloads and 14 definitions are retained and must be translated. Everything else maps to existing handshake/startup schemas; the audit lists each selector.
- **Rust protocol major 3** (`protocol.rs`): the source is `rust-provider-protocol.v2.json` (`6308a98c…`). Its file status says "candidate, not applied", but native-evidence.md §9.1 pins these exact bytes as the inherited base; the v3/v4 artifacts are not owners. The envelope (major 2→3), the frames added in §9.2 and the retained payloads need translation. Exact gaps where the source isn't precise enough:
  - no name for the major-3 envelope;
  - `DependencySourceChunk` has a member list but no types or bounds;
  - the PreparedOutput* frames say "inert rows only" without saying which entry record they carry;
  - `CoverageKeyV2` and `FactCandidateV1` are defined by more than one owner.
- **Common control frames:** I found no schema or field grammar. `02-distribution-and-components.md` says "Concrete schemas remain DR-103". An owner has to name a source or explicitly limit `protocol.rs` to provider frames.
- **Report projection** (`report.ts`, part of `output.rs`): no document is identified as the report projection schema. This needs an explicit reviewed owner mapping.
- **Security/private schemas** (security-lifecycle, attempt-custody, carrier-highwater, journal-record): nothing in the 28 references them, and they aren't inputs to the eight public generated files. They belong to handwritten security/storage code (M2).

**Recommended strategy**
- **Three recipes:** all six Rust files in one (forced by the `mod.rs` sibling rule), the TypeScript provider protocol in one, and the report in one.
- **Options file:** explicit entry points per output, a list of superseded definitions that refuse if reached, and a table mapping each schema `$id` to its module name.
- **Protocol translations:** new derived JSON Schema documents with distinct `$id`s. Every definition records its source path, hash, selector and disposition, and names are namespaced by language (`typescript2` / `rust3`). These need separate review; I haven't approved them.

**Staged partial:** yes, but only as a labelled checkpoint that is never called M1-complete. The build plan (lines 748 and 757–765) requires the first recipe and its drift trial to cover all eight files. So the consistent staged form generates all eight, with the protocol files holding only the schema-based subset and the open gaps recorded so the M1 completeness check fails. M1's help/version and identity checks don't need provider frames. Whether a partial protocol file satisfies line 765 is for the root reviewer to decide.

**Required work:** the two protocol translations, owner decisions for the report projection and control frames, the `metadata-v2` path fix, and the options file. Not needed as generator inputs: commitment/state-machine law, the transition tables, other historical protocol versions, and the private schemas.

**Limits:** I sampled the retained field grammars rather than tabulating every field. The "not found" results for control frames and the report projection cover only the sources listed in the audit.
