# Review verdict: changes required (2 findings), subject SHA256 `51d0888012aad92484e34ceb2451cfe2458676945cf32c951790c51befc3a438`

**Scope:** the generic inert Rust/TS renderer for 67 named native types, 23 distinct externs and 2 frame families. I did not approve or re-review the native owner's semantics. This is not a source selection and says nothing about codec, admission, integration or release.

**Standing:** a sound inert renderer, but not yet sufficient as an inert bridge. Two changes are needed; both are narrow.

## Integrity and reproduction
- **File set:** the 24 files, byte sizes and SHA256s match the manifest, both before and after my work. I wrote only inside `m1-native-wire-renderer-review-01/work`.
- **Input pins:** all 11 copies are byte-identical to their origins. I compared the bytes without running any owner helpers.
- **Fresh render:** `render.py` run on a scratch copy produced `wire.rs`, `wire.ts` and `render-result.json` identical to the committed ones.
- **Test gates, all passing:**
  - `cargo test --locked --offline`: 6 tests plus 2 compile-fail doctests.
  - Clippy with `--all-targets -D warnings`: clean.
  - Python `-B test_render.py`: 6 groups.
  - Strict TypeScript 6.0.3: clean.
- **Counts:** 17 scalars, 50 records (45 records, 4 tagged records, 1 alias), 23 externs and 27 private types. Header `frameType` enums match the frame lists exactly: 17 of 17 and 26 of 26. Rust3 `direction` values match. Ts2 has no direction member and none is invented.
- **Mutations the tests catch:**
  - `deserialize_any` changed to `deserialize_byte_buf`
  - `required_value` removed (28 sites)
  - `deny_unknown_fields` removed
  - `skip_serializing_if` removed
  - `Serialize` added to the Rust3 frame (doctest fails)
  - `exactOptionalPropertyTypes` turned off
  - Ts2 payload no longer tied to frame tag
  - `bytes` type widened
  - const `0n` widened to `bigint`

## Required findings

**RF-1: Required null accepts `{}` inside tagged records.** All 18 `()` required-null fields are inside the 4 serde-tagged records. Serde buffers these records before decoding, and that buffer turns an empty map into unit.
- For example, `{"kind":"file",…,"linkTarget":{}}` is accepted and re-serialized as `null`. The same happens for the symlink's `contentSha256: {}`. `[]` is refused, and flat `Option` fields refuse `{}`.
- A CBOR empty map would be read as null the same way. This contradicts the "required null versus absence" representation the unit claims, and no test covers it.
- **Fix:** either render a custom `Deserialize` for tagged records, or refuse non-null for `()` members, e.g. `deserialize_with` using `deserialize_any` so only unit is accepted. Add negative tests for `{}`.

**RF-2: Text and key kind are lost inside tagged records, and a direction probe is vacuous.** Two parts:

(a) I used a hand-written test deserializer that honours type hints the way a schema-directed codec would. Flat records correctly refused bstr for text and bstr or integer-index keys. Inside `Rust3SnapshotEntryV2`, serde's buffering drops the hints, so these were still accepted:
- a bstr where a `String` is expected
- member keys given as a u64 index (`0` read as `path`) or as bstr
- the tag key given as bstr

Tag *values* given as bstr or u64 were refused. `UNIT.md` claims kind preservation "through Serde tagged record buffering", but that holds only for `ByteString`, and even a strict M3 codec cannot repair this path.
- **Fix:** exact text-key/tag/text-kind handling for tagged records, or no derived `Deserialize` on them (as with frames). At minimum, disclose that M3 must hand-decode tagged records, and add negative tests.

(b) `type-probes.ts` `wrongDirection` errors only because its payload `{dependencySourceSetId:'x'}` is incomplete. Widening `direction` in `wire.ts` went undetected by the subject's probes. My probe, which declares a valid `Rust3DependencySourceAcceptedV3` payload, shows the generated TS does correlate direction, but only it catches the mutation.
- **Fix:** give that probe a valid payload so the only error is direction.

## Advisories
1. **Silent acceptance of malformed input:** `render.py` accepts these without complaint. All are outside the current input, but they matter for the pending closed input profile.
   - A header enum lacking a rendered `frameType`.
   - A `frame-payload` member outside an envelope (the TS type is dropped). If nested, Rust compilation fails.
   - A variant body redeclaring the discriminator is silently dropped. The meta schema permits this shape, so this is the highest priority.
   - `const` together with `enum`.
   - Out-of-range uint consts such as `18446744073709551616n` or `-1n`.
   - A record named like a helper, e.g. `ByteString`.
   - The tag member renamed away from `frameType`, which loses TS correlation.
   - Text-enum header members, which emit 20 unused private enums.
2. **Rust keywords:** `if`, `true`, `else`, `while`, `try` and `box` are not escaped. Compilation fails, so this fails closed.
3. **Untested collision checks:** removing the frame-variant or record-variant collision checks from `render.py` still passes the Python tests. Add probes for both.
4. **Rust frame structs are uncorrelated:** `frame_type`, `direction` and `payload` are independent fields, so an inconsistent frame can be constructed. Consider a checked constructor or deriving tag and direction from the payload variant.
5. **Loose deserializers:** for flat records, keeping kind and exact keys also depends on M3's codec honouring hints. State this as a codec duty.
6. **Serialize disclosure:** `ByteString` serializes to a JSON array (`[0,255]`) that its own `Deserialize` refuses. The disclosure in `UNIT.md` is enough, since `Serialize` is not claimed to be wire-qualified.

## Confirmed correct
- **Integers:** u64 and bigint keep `u64::MAX` exact. Floats, negatives, overflow and `1e0` are refused, including inside tagged records.
- **Text escaping:** Rust and TS escaping of `"`, `\` and control characters is correct. Lone surrogates fail closed.
- **Absence, null and empty:**
  - Optional members keep absent, empty and null distinct.
  - Optional-nullable renders as `FieldPresence<Option<T>>` / `?: (T) | null`.
  - A required null reached through a scalar alias still gets `required_value`.
  - Missing required-nullable fields are refused.
- **JSON input edge cases:** duplicate keys and duplicate tags are refused.
- **Bytes:** `ByteString` refuses text, arrays, null and maps. It keeps real bstr and owns its data, including through tagged records.
- **TS types:**
  - Selector alternatives are both allowed statically and don't narrow by tag alone, as disclosed.
  - Readonly is enforced.
  - Unknown tags and extra `direction` members are refused.
  - Bigint has no unsigned bound; that is left to admission.
- **Frames:** no generic serde on frames or payloads, and no invented on-wire discriminator.
- **Constants:** consts are inert in Rust (`analysisOrdinal: 5` is accepted), as disclosed.

The pipeline for validating the source input, its dependencies and the tool closure remains explicitly pending and is not assessed here.
