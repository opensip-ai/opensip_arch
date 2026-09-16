# Independent Grok review: logical-path-selection v1

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m2/logical-path-selection-v1-subject.json`
**Manifest SHA-256:** `81b43104e418925acaaa44f8e27eb6826b4bb49c2a9db5a816c7a6a105a27632`
**Members:** 23
**Verdict:** **ACCEPT-DESIGN-UNIT**

Bounded identity `LogicalPath` inert text for the selected `#/$defs/LogicalPath` profile used by direct `Blob.path` / `import-blob.path`. Not filesystem custody, whole-descriptor admission, schema ordering, snapshot join, or replay. Frozen 8/8 baseline does not approve these two files. Parent foundation v2 is live **8 inventory / 9 contract**; this unit is not installed. Neither M1 nor M2 is complete.

## Custody and inheritance

23/23 selection members match. Frozen implementation subject `docs/implementation/m2/trials/logical-path-01/subject.json` SHA `81aa152b…651c` — **197/197**. Adjacent archive matches `archive-pin.json`. Candidates are exactly the subject minus `successor.json` (22). Parents pin-match live: foundation-primitives-selection-v2 successor `1bf114cf…fd7b` / 6853 and inventory v10 `6608fabd…8bc9` / 121810 (20 packages). Both map rows match frozen product, candidate product, and inventory v10 (`descriptors.rs` already planned as identity validator). Private copy only.

Only `crates/identity/src/lib.rs` and new `descriptors.rs` differ from live foundation v2. `Cargo.toml`, `canonical.rs`, `canonical_tests.rs`, and `digests.rs` are byte-identical to live. Live still has no `descriptors.rs`. Schema owner `identity.v3.schema.json` SHA `311c1feb…b68f` / 197480 equals the frozen product copy. Selector `#/$defs/LogicalPath`. Generated carriers were not re-reviewed. Probe harness is evidence only (not an installed product binary). Recorded preparation-failure01 is a pre-copy helper path error, not a product test failure.

## Semantics and encapsulation

`LogicalPath(String)` is a private tuple field. Public construction is `parse` / `FromStr` only. No `Default`, `Deserialize`, or unchecked constructor. `as_str` / `into_string` return the original text. `#![no_std]` + `forbid(unsafe_code)`; no filesystem APIs.

Checks, in order: nonempty; Unicode **scalar** count ≤ 4096 (not UTF-8 bytes or UTF-16 units); no `\` or NUL; split `/` refuses empty / `.` / `..`; each component ≤ 255 scalars; then the selected Python-`re` `$` edge: a final LF after a last segment that is `.` or `..` is refused (`.\n`, `a/..\n`), while `a\n`, `.\n\n`, `a/.\r\n`, `.\u{2028}` remain admitted. NFC/NFD and case are not rewritten. This is the selected jsonschema + `not.pattern` profile, not a stricter invented path policy.

Application scope matches the schema description: this grammar is the **direct** `$ref` on Blob/import-blob path, including the 255-per-segment bound. It must not be applied to fingerprint `subjectKey.logicalPath` (plain `minLength`/`maxLength` 4096; `ordered()` without the 255 bound) or scope-descriptor path arrays (`Text`, where `.` is admitted project root). This unit does not dispatch descriptor fields.

## Tests and independent oracle

Private copy, Cargo/rustc 1.95, Node off PATH:

| Check | Result |
| --- | --- |
| `cargo test --locked --offline -p opensip-identity --all-targets` | **19/19** |
| `cargo clippy ... -p opensip-identity --all-targets -- -D warnings` | pass |
| `Cargo.lock` | unchanged |

Independent Python **jsonschema 4.25.1** Draft 2020-12 validator on `#/$defs/LogicalPath` plus an imperative Unicode-scalar/segment/`$` reference versus the actual Rust public API (`LogicalPath::parse` through the evidence probe): **4697/4697 agree**, 0 mismatches. Targeted counterexamples (empty, `.` scope root, `..`, absolute, `//`, backslash, NUL, final-LF dots, emoji 255/256, NFC vs NFD, colon/space/newline filenames) all agree across Rust, jsonschema, and imperative. Probe is not installed.

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

## Limits

- Inert lexical profile only. No descriptor assembly, ordering, snapshot join, storage, or replay.
- Finite 4697-case corpus plus 19 tests; not a proof of all Unicode or all schema combinators.
- Does not change generated Rust carriers, which still do not check this pattern.
- After genuine assent, foundation source-export proof must be refreshed to include the sixth identity file.
- Not M1/M2 complete, not release, sandbox, or fresh blind consumer.
