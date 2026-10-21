# Review: native-owner boundary repair source preflight r1

**Verdict: PREFLIGHT-CLEAR**

No required findings.

This verdict is limited to the frozen two-file source repair identified by subject-manifest SHA-256 `a9af430609cdb686a7e2b11e5fc2ef3f3cb065569d72abf91f3ad8bdd2fd9571`. It resolves the source defect described by `OWNPAT-UNIT-R1-RF-1`. It does not accept the repaired unit, its pending complete owning R5 evidence, integration, blind refresh, or product qualification.

## Independent checks

- Rehashed all 21 declared manifest members and confirmed that the subject manifest itself is the only staged file outside its membership. Rejoined `source.json` to the exact rejected R1 subject manifest and 42-row product map. All 27 parent paths match the pinned product base, all 15 new paths remain absent from that base, and the live product and architecture heads match the declared bases.
- Confirmed exactly two product paths change from rejected R1: `crates/identity/src/schema_patterns.rs` and `crates/identity/src/schema_tests.rs`. The other 40 candidate tuples are byte-exact. No schema, source map, registry, generator, fixture, runtime metadata, dependency, entrypoint, alias, or provenance path changes.
- Compared the repaired matcher with the accepted product-base predecessor. `Kind`, the shared `TABLE`, generic `matches()`, and every inherited helper are byte-exact to that predecessor apart from the separator newline before the native helper. The shared table therefore contains exactly the predecessor's ordered 72 forms; both corrected complete-relative-path literals and `Kind::CompleteRelativePath` are absent from it.
- Confirmed the two corrected literals remain inside the unchanged closed 26-form native-owner gate. Their complete-input predicate is now evaluated directly only after that gate, preserving the intended empty/nonempty distinction, absolute-path refusal, NUL/backslash refusal, and exact `.` / `..` segment refusal. All other native forms continue through their previously reviewed special cases or the unchanged inherited dispatcher.
- Confirmed `schema.rs` is byte-exact to rejected R1. Its owner-aware `pattern` dispatch still selects native semantics only for the three closed resolved document identities, restores inherited semantics after a native-to-foreign reference, and routes all `patternProperties` keys through the shared inherited matcher.
- Reviewed the new controls. Each corrected literal is exercised under all three selected native owners, including empty and nonempty behavior plus full-input line-terminator and path refusals. The same literals must fail generic admission even under native-looking IDs, fail direct foreign admission, fail through native-to-foreign references, and fail as `patternProperties` keys for native and foreign owners. A separate test compares the entire ordered shared form list with all 72 predecessor literals.
- Confirmed the focused evidence pins both repaired source files exactly and records 78 identity tests, two registered-host controls, and one provider-path control passing. These focused results are evidence for this preflight only.
- Reviewed the strengthened finite differential. Its control first requires the candidate shared form list to equal the predecessor's exact 72-form list, then requires every native-only form absent from that list to be refused by the inherited matcher for all 119,250 inputs. The archived report records 3,100,500 native and 8,586,000 inherited comparisons, exact inherited-set equality, zero shared-form additions, native-only inherited refusal, and zero mismatches.
- Confirmed all 13 core mutation records and all four companion mutation records are compiled runtime failures with nonempty failed-test lists and exact restoration. The new controls independently catch reinsertion of each corrected literal into the shared table and routing `patternProperties` through the native profile. Restored positive controls are recorded as passing, and the mutation source pins join the repaired matcher and unchanged companion paths.
- Confirmed the rejected R1 review and subject are preserved by exact hash. Nothing in this package reclassifies that round or claims complete repaired-unit acceptance.

## Remaining boundary

Complete owning R5 is still pending. A separately frozen complete repaired unit, with exact final source and owning-evidence joins, requires independent code-unit review before acceptance. Blind refresh remains incomplete and product qualification remains false.
