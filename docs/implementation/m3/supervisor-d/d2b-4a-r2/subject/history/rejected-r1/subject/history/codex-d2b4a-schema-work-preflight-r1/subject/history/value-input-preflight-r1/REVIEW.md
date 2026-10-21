# CODEX2 Review — D2b-4a decoded-value schema mechanism preflight r1

## Verdict

**PREFLIGHT-CLEAR**

## Required findings

None.

## Source assessment

The frozen subject descriptor has the requested SHA-256 (`d16d26a9f83b3cf21e4d1b4c1418004b7f13513d6aad63ea73b8575a77b071cd`). All 51 declared members match their byte counts and SHA-256 values, with no missing or extra frozen member. The three parent identity files are exact bytes from product commit `ca6f5be9ded80c50a143b2f219258c95c80db2e6`; all three candidate files and all nine unaccepted context paths equal the named worktree bytes. The seven architecture authorities equal commit `278d1a27b4cea095b37eed09e7109d8a98be7696`.

The three-file candidate is coherent:

- `Program::admit_value` checks the same selected entry, resolves the same document owner and `$ref` closure, and calls the existing evaluator. It does not introduce a source, alias, selector fallback, owner profile, schema, or dependency.
- The complete value is structurally charged before NFC/model validation or schema evaluation. Checked subtraction prevents budget wraparound; the model walk rejects non-NFC strings and keys, retains exact private-range integers, forbids unrepresentable scalar kinds by type, and matches the existing 32-container model boundary. Its recursion is therefore bounded independently of the evaluator's existing reference-depth guard.
- `SchemaHandle::admit_value` returns the existing opaque `ShapeValue` only after the complete check and then owns a copy of the already validated inert value. The handle retains the selected schema ID, complete-document digest, and selector. It supplies no CAN bytes, digest, provenance, descriptor meaning, execution permission, or publication authority.
- Errors from references, limits, malformed schema operations, patterns, and nested branches continue to propagate through `$ref`, `allOf`, `anyOf`, `oneOf`, `not`, and `if`. Treating `ArrayOrderError::Canonical` as `Error::Json` is the correct conservative behavior: a failed canonical operation cannot become a mismatch that `not`, `if`, or `anyOf` turns into admission. Other order/type failures remain completed mismatches.
- The existing `Program::admit_json` and `SchemaHandle::admit_json` bodies and their 4 MiB profile are unchanged. The shared canonical-order correction does not alter a successfully parsed old JSON input: a child canonical representation cannot exceed the complete admitted JSON bytes, and the existing parse already enforces the same depth and scalar model.

The accepted D2b PLAN-r3/A2 duties authorize this representation mechanism. They require a strict deterministic-CBOR decode bounded at the transport, followed by the selected closed-schema check and hand conversion; they do not require re-rendering the decoded value through CAN's separate 4 MiB JSON profile. Applying the existing registered evaluator directly to its inert exact value model is an implementation of that duty, not a new schema or protocol choice. No further design selection is required for this helper boundary.

## Frozen evidence and limits

The preserved red demonstrates the concrete mismatch: the small original-schema control passed while the permitted wide strict-CBOR value failed only at the intermediate JSON byte cap. The final archived report records 86 identity tests, 15 Rust3 mechanism tests, and Clippy passing. The positive wide value passes; its wrong digest and unknown root member still refuse.

All four mutation cases compiled successfully, failed at their intended runtime witnesses, restored all 12 source/fixture pins, and passed a fresh restored positive. No compilation failure is counted as a kill. The public binding computation equals both current binding objects; all referenced public pins rehash, both held receipt bindings match, and no blind run occurred.

This verdict is limited to the three identity source files. The nine Rust3/carrier/fixture paths remain unaccepted context. The complete D2b-4a receiver, transport nesting closure, caller budget and allocation justification, context/provenance/counters, typed conversion, complete owning controls and mutations, final unit review, integration, inventory binding, and qualification remain owed.

## Non-blocking observations

None.
