# FX-COMP-1 round 2 independent review

Reviewer: GROK2. Verdict: ACCEPT-DESIGN-UNIT. Reviewed at 2026-10-06T04:08:49Z.

Subject `docs/implementation/fallow-expansion/components-r2/subject.json` is 1644 bytes, SHA-256 `0afd515a2c19f9a466a6f409d0b815942b50f59e3b25d3c5835463f05e2a3aa4`. All eight members match the manifest. This accepts the frozen design unit. It does not bind the unit, and it does not qualify an adapter, grammar, or repair rule.

Components r1 was frozen and was not dispatched. This is the first independent review of the programme's component subject. The r2 author correction is the fixture `malformed-source-no-text-span`.

## What is accepted

`ComponentSourceModelV1` is an extraction intermediate. Schema validity, a complete extraction state, and an exact original span give no fact, Coverage, Run, repair grant, or new capability. `validate` returns `semanticCompleteness: not-established` and `repairAuthority: false` on every admissible record.

The closed formats are `vue`, `svelte`, `astro`, `css`, `typescript`, `javascript`, and `rust`. Ordinary files use one `whole` region whose language equals the format. Vue, Svelte, and Astro use `container`, `script`, `template`, `style`, and `unmapped`. Template languages stay format-specific. CSS uses `whole` with language `css`. Regions of a nonempty file partition `[0, byteLength)` in order. An empty file has zero regions and is extraction-complete.

Derived segments partition the derived blob. `exact` requires identical byte slices and UTF-8 boundaries. `anchor` may cite original bytes and yields no exact span. `generated` has null source endpoints and yields no exact span. A span translates only when every intersecting segment is `exact` and the source pieces abut in order. A discontiguous copy returns no bounding box.

A malformed UTF-8 original is admissible only as one whole-file `unmapped` region with language `unknown`, state `malformed`, blocker `malformed-source`, and `derived: null`. `exact_original_span` then raises `span-source-utf8`. The 25th fixture is admissible and expects that error. The same refusal holds for a truncated sequence, an overlong encoding, and a UTF-8 surrogate sequence. Hiding those bytes as a complete `whole` region fails `malformed-source-account`.

The single passage override selects `docs/v2/contracts/product-v1/native-evidence.md` line 2777. The parent is the accepted lock input, 329013 bytes, SHA-256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. The parent does not parse as JSON, so the line selector is the v4 form for this document. `before` is the closed-world sentence on that line. `after` keeps that sentence and appends the shared-source section. No selected successor owns line 2777. The record has no passage supersession. Candidates are the seven subject members other than `successor.json`, sorted, and each pin equals the manifest.

Admission order in the reference is canonical JSON constraints, the 4 MiB bound, schema shape, snapshot and closure joins, original partition, format and language compatibility, derived rehash, map checks, and derived model state. Schema bounds are 65536 regions and 65536 segments. Snapshot and closure identifiers use the current `snapshot2:` and `closure2:` grammars. Source bytes and derived blobs are rehashed. The producer closure join is membership in the admitted closure-id set.

Staged adapter work stays outside this record: no grammar binary, recognizer id, public fault code, or matrix widening. The native insertion is the authority for the model. The schema, reference, and fixtures are the candidate members.

## Author correction

Fixture `malformed-source-no-text-span` uses source byte `ff`, the required malformed account, and span `[0, 1)` with error `span-source-utf8`. `check.py` against the pinned jsonschema packages passed all 25 fixtures, including this one. A direct call on that region also raises `span-source-utf8` before any offset is returned.

## Non-blocking observations

`fixtures.json` has no two-region partition, no `preprocessor-unavailable` region, and no script-plus-template pair. Independent probes of `reference.py` admitted a four-region Vue partition carrying `preprocessor-unavailable`, refused a gap and an overlap, refused a map that cites another region's bytes, and kept `repairAuthority` false when a script region and a template region are both extraction-complete. Adding those fixtures on a later revision would lock the probes. Their absence does not change this acceptance.

`exact_json` applies `depth < 32` to every value. `tools/quality/canonical.py` `typed` applies the depth limit only to containers at depth 32 or greater, matching identity-and-evidence §3: the root counts as 1, and keys and scalars add no container depth. A 32-container value is refused by the reference and admitted by `typed`. A 33-container value is refused by both. No schema-valid `ComponentSourceModelV1` reaches that depth. Canonical bytes of a valid sample record match `canonical.canonical`.

A region may carry blocker `invalid-source-map` together with a structurally valid exact map. The map still translates, and `repairAuthority` remains false. A map that fails structural validation is refused before any span is read. A later revision can refuse the mixed label.

`source.path` is a bounded string joined to the admitted snapshot. The reference does not reapply the `LogicalPath` grammar. A snapshot that already contains a non-canonical key will satisfy the join. That matches the stated premise that snapshot admission has already happened.

Components r1 also selects native-evidence.md line 2777 and is a different frozen subject. Binding it beside this record would be a conflicting override. This acceptance covers r2 only.

## Methods and limitations

Member, parent, and candidate pins were hashed independently. The passage `before` was compared with line 2777 of the parent. The lock's 102 contract successors were scanned for that selector. `check.py --deps /tmp/opensip-fx-python/python-packages` passed 25 fixtures. `build.py --check` against the frozen product lock matched the frozen bytes and was not used to write. Adversarial calls covered malformed UTF-8, split characters, multi-region partitions, cross-region map ownership, ordinary-format kind rules, anchor and generated spans, empty derived blobs, and the depth predicate. Product worktree `/Users/sb/code/opensip-ai/opensip-fx-design` remains `f5f5b4d20eca34ab2312b3ffc141c378da326afe` on `design/fallow-expansion`, tree clean. Design lock is 526786 bytes, SHA-256 `205eee0fcecb7076107db695b351c430cbc6866d10441857719f5bdeee235c83`, 102 contract successors and 103 inventory successors. Checker `tools/verify_design.py` is SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`. A full baseline `verify_design` was not re-run. Architecture HEAD is `a9f6557eeb924d3163d7494e83adbd69106e41fb`; the parent byte pin still matches the lock input. No repository file was edited. No product cargo, test lane, or lane lock was used. No adapter or product qualification is claimed.
