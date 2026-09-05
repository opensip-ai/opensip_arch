# Independent lifecycle carrier review v1

**OBJECT — two concrete SQL defects require correction.** External replay passed **88/88**, byte-identical to the retained report, on SQLite 3.53.3. The independent probes below keep the normal writer fence and callbacks.

All six subject pins matched before and after review. Freeze SHA-256: `3cef22bea874f73fb085328062433b4c07fcd2f283b543fc0d2fd4badefc37cb`. Exact hashes, probe observations and full reproducer source are in [the independent review JSON](lifecycle-carrier.independent-review.v1.json). No subject or register changes.

## LCR-1 — REPLACE statements bypass immutable rows, lease release, retention, and tombstone guards

The tested connection has PRAGMA recursive_triggers=0, which is not constrained in requiredPragmas. INSERT OR REPLACE removes a conflicting row without invoking its DELETE triggers under this setting; it does not run UPDATE immutability guards. Valid INSERT guards then allow the replacement. A live acquired lease with unchanged UUID/boot/token can switch from G1 to G2 after selection advances, without any release authorization. A retained transition and retired registry key can also be replaced; an unreferenced READY generation can be reset with different digests/platform without a GC ticket. All probes keep the writer lock, foreign_keys=ON, and the supplied callbacks; no schema tampering or forged OS liveness facts are needed for the lease example.

**Required repair:** Close REPLACE/conflict-replacement paths explicitly. Prefer BEFORE INSERT collision guards for immutable primary and unique identities so replacement cannot silently delete an existing row, and/or require and verify recursive_triggers=ON on every connection with guarded deletes sufficient to reject the attempted replacement. Check collisions through UNIQUE indexes as well as primary keys. Retain negative INSERT OR REPLACE / REPLACE and relevant UPDATE OR REPLACE cases for lease lifetime, tombstones, generation identity, transition retention, and quarantine. Verify legitimate publication and cleanup still pass.

## LCR-2 — Canonical UUID and digest checks accept embedded NUL suffixes

SQLite text length and GLOB checks stop at NUL in these expressions. The DDL accepts a 43-byte id consisting of a valid 36-character UUID followed by NUL and suffix, and a 71-byte digest consisting of 64 lowercase hex characters followed by NUL and suffix. STRICT TEXT does not enforce the intended byte grammar. Different consumers can disagree on identity/digest bytes even though SQL declares the row canonical.

**Required repair:** Explicitly reject NUL in every constrained textual carrier, and enforce exact ASCII byte lengths for UUID/digest domains using BLOB length as appropriate. Audit repeated namespace/lease/boot/transition UUIDs, root hex, decimal identities and all digest fields for the same truncation behavior. Add NUL-prefix/middle/suffix and malformed-byte boundary cases through real SQL; do not rely on a later verifier callback to repair scalar DDL grammar.

## Review boundary

The actual SQLite transaction/crash witnesses and nonblocking flock probe are useful design evidence. The four-field epoch, safe opaque-key registry mapping, and host callback contracts remain explicit. Paired adoption by the parent distribution and security successors is pending integration, not an additional defect. No requirement is made for SQL to prove OS or cryptographic facts.

SHOULD: add the synthetic global-context/project-tuple contradiction described in LCR-S1. Keep actual platform and power-loss qualification at their existing gates.

Replay: `python3 -B docs/coop/completion/lifecycle-carrier.check.v1.py --report /tmp/lifecycle-carrier-independent-replay.v1.json`.

No automatic acceptance, SATISFIED status, or register disposition is asserted.
