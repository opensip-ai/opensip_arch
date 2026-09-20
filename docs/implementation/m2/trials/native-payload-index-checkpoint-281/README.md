# Payload-v1 declaration and metadata index support 281

Private, unselected native candidate based on frozen 280. Installed product `fa72e50` remains unchanged. This extends the existing metadata index from payload-v2 recovery inputs to the existing payload-v1 format. It does not authenticate metadata or grant operational authority. No dependency or public API changes.

The dedicated recovery bundle verifier still accepts only schema 2, kind `recovery`, with its closed root-recovery authorization pair. Its existing `payload_shape` entry point retains that restriction. A separate index shape dispatcher accepts strict integer schema 1 or 2 and applies the exact corresponding primary schema. Schema 1 permits both `ordinary` and the legacy `recovery` label structurally, has eight closed member fields and no authorization pair. A legacy label does not create recovery authority. Schema 2 remains recovery-only with nine member fields and the authorization pair.

Declaration preflight shares the existing Unicode 15 normalization/casefold, path alias, reserved frame-name, file-parent and declared-edge checks. The authorization body and its exact once-listed envelope are required only for schema 2. Index data stores an optional authorization-envelope path; it does not synthesize a path for schema 1. Slot-owned body kinds, actual retained bytes, exact envelope pairing, root schema/domain dispatch, preimage checks, every-listed-path presence, known-length caps, shared budget and failure latching remain the same.

This is an index over a trusted capture callback; it does not prove filesystem custody or bounded native capture. Synthetic index fixture envelopes intentionally have invalid cryptographic signatures. A successful pair binds bytes and a declaration; it is not a signature result, root-chain admission, current revocation decision or ordinary import authorization. Artifact bytes remain unselected here.

## Evidence

Authoring reverified every frozen 280 product pin and every frozen 265 archive member, including all current candidate bytes. The exact primary payload-v1 schema is SHA256 `bb9ab011b8b8d3f819552a7aa8924a1df9e6e00abf447f0a5e99330060b43da0`. The original 265 `trust_metadata_index_reference.py` and `trust_operation_reference.py` supply the oracle; these files are not edited.

537 full-shape/dispatch comparison rows (37 positive) cover closed fields, required fields, all source node types, strict schema versions, both legacy kinds, forbidden authorization fields, root count bounds, lexical timestamps and exact member-path schema behavior. Every row also checks that the dedicated recovery shape remains schema2-only. Existing recovery shape, signature and index fixtures are byte-identical and rerun.

28 declaration-preflight cases (7 positive) convert the earlier path corpus to schema1. Their oracle uses the unchanged original Index constructor, with a private subclass that stops at the first byte load; the test claim is only preflight completion before capture. Removing a schema2-only authorization constraint legitimately changes some expected outcomes.

54 actual same-Operation index cases (25 constructed, 10 completely selected) cover the schema1 versions of 263 faults plus explicit version/kind and authorization cases, normalization/alias/parent checks before capture, missing listed files, cached-content new paths, ambiguous envelopes, root domains and budget caps. Exact returned pairs, ordered captures/caps, counters and failure state are compared to the original reference. Selected pairs remain usable after the index, input byte map and Budget are dropped. Prior 263 schema2 cases and subsequent recovery consumers also run unchanged.

227 security tests pass (`security-initial-r1`), with final strict workspace Clippy and formatting checks. No full workspace or isolated host rerun is claimed; 277's 515+2 remains predecessor evidence. Compiled controls and exact patches are retained in `mutation-check-r1`; a failure that first catches a different mismatch or panic is not an exploit proof. The fixture generator initially had a Python keyword-spacing syntax error before producing any fixtures; its beforeimage is preserved. No production correction was required by the initial comparison corpus.

422 product pins: 418 inherited unchanged from 280, changed `trust.rs`, and three new fixture files. The new versioned shape helper is shared internally while recovery verification retains its explicit wrapper. `trust_policy.rs` and all 280 policy fixtures are unchanged. All member hashes and source pins are rechecked when freezing.

Remaining ordinary metadata authentication/retained closure composition, physical capsule/reference admission, time/accepted-role effects/current and historical population, artifact/repair/full command composition, native source custody/adoption, fences/census/durable writers/runtime selection and M3–M6 remain open. There is no cumulative approval or installed feature claim.
