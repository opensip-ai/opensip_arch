The native wire-carrier candidate is written. Its check runs 133 tests and all pass, and each of 16 deliberately planted defects makes at least one test fail. I found no remaining contradiction. Five of my choices need the reviewer's confirmation (end of this message). I only wrote in `/tmp/opensip-implementation/m1-native-wire-owner-author-01`, committed nothing, and this is not an approval.

**What's there**
- **`wire-carriers.v1.json`:** one declarative input for both languages, meant to drive one generator recipe for `protocol.rs` and `protocol.ts`. It holds pinned sources, a separate CBOR profile for TS2 and for Rust3, 17 scalars, 50 record types, both frame tables, 41 hand-written admission rules, the commitment-domain map and a transition overlay. Its closed grammar is `wire-carriers.meta.schema.json`.
- **`successor.json`:** 13 scoped supersession rows, each with exact selectors, justification and the checks that test it. It also lists 8 refuted false gaps. No parent file is changed.
- **`field-coverage.json`:** every TS2 row (182 inherited + 18 new) and every Rust3 row (5 envelope, 205 grammar, 59 external, 76 new, 27 frames) maps to a carrier field, a moved location, a frame or a stated "not carried" reason. Every gap cited in the inventories maps to a resolution.
- **`contract.md`** explains everything; `subject-manifest.json` pins the 18 authored files.

**How the contradictions were resolved**
- **Subject-scope commitment, both languages:** every coverage key carries its own `scope2` value, minted by the host; the worker only echoes it. TS `SubjectScopeV1` and both per-stage domain commitments keep their recipes. The reference model admits the per-key value and refuses both old per-stage values.
- **Anchors:** the provider-wire rule and the shared fact2 rule are stated separately.
  - On the wire, an anchor must be non-empty (fact-plane's rule).
  - The shared fact2 rule (`identity-model.v3.py:1892`) still allows zero-length anchors and is not narrowed.
  - `fact-ref` anchors are refused before any fact2 is minted.
- **Anchor sort order differs by language, which I didn't expect.** TS2 sorts by deterministic-CBOR bytes, while Rust3 inherits fact-plane's CVE1 order. The check shows the same two anchors sorting in opposite orders, so the two carrier records stay separate.
- **TS manifest digest:** plain hex SHA-256 over the CBOR entries, with no domain or prefix.
- **Wrong citation fixed:** the file the earlier proposal called the v2 Rust checker is the v1 checker. The v2 checker computes no manifest digest, and the owner for the recipe is the rust2 text itself.
- **Rust dependency-source digest:** the schema's stated input includes the digest itself, so no value can satisfy it. I replaced it with the same entries-only recipe as the snapshot manifest.
  - Entries are ordered by (packageKey, path).
  - `packageKey` is `name SP version SP sourceId`, joined to each package's file manifest identity.
- **PreparedOutput frames:** field names are unchanged; the values now come from the Plan-bound `PreparedOutputSetV3` rows, with the host joining them to `preparedOutputSetId`. The old V2 payloads point at superseded rust-v1 rows, so this change was unavoidable.
- **Major-3 transition table:** `protocol3-transitions` is the only matching table, and rust2's frame precheck and payload guards run before matching.
  - An Unavailable after any output now faults. rust2 T019 had this guard and P3-25 dropped it. The published table admits that trace, and my overlay faults on it.
  - Eleven other traces behave identically under the reference model and my overlay.
- **Records and types that were missing:** DependencySourceChunk and Accepted, ProviderFault, Cancel, Cancelled, the SnapshotEntryV2 variants and the extra identity-echo substitutions are all typed now. Several earlier "gaps" turned out to be false, for example StageResultV2 is already named by §9.7.

**Carrier representation and naming**
- Byte strings are a Rust `ByteString(Vec<u8>)` and a TS `Uint8Array`. Hex appears only in JSON test vectors.
- TS2 can decode negative integers, which are then refused because no TS2 field accepts them. Rust3 refuses them at decode.
- All type names carry a document/language prefix (`Ts2`, `Rust3`, `Native2`, …), so there is no bare `CoverageKeyV2`.
- No wire tags were added, and none of the private type names is a wire version change.

**Verification limits**
- The checks ran the pinned reference models in the reference env: native-evidence, startup and wire.
- The CBOR codec in `tools/wirecodec.py` is test scaffolding, not a production decoder.
- No generator run, product execution or M2/M3 admission is claimed.

**Choices that need your confirmation**
1. **PreparedOutput entry limits.** I split them as expansion rows ≤ `maxExpansionRows`, generated-file rows ≤ `maxGeneratedFileRows`, and directive rows ≤ `maxPreparedOutputEntries` (256).
2. **Unavailable guard and Cancel before Hello.** I keep the `outputSeen=false` guard on P3-25. The host sends no Cancel before Hello.
3. **Phase values.** ProviderFault `phase` and Cancelled `observedPhase` are the host phase at the moment of the fault or cancel.
4. **Narrower text bounds.** The TS ExecutionId must match `exec1_` plus 32 hex digits, and paths are capped at 4096.
5. **Anchor count.** At most 100000 anchors per candidate, refused at the wire, matching the fact2 limit.

**Future qualification (outside contract completeness):** generator support for the new type kinds, M2 implementation of every hand-written rule, M3 codecs, and measuring real PreparedOutput manifest sizes against the frame limit.
