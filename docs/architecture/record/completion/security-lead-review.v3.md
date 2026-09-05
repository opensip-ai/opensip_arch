# LEAD-CORRECTION-REVIEW 3 — security v8

**ACCEPT: 0 MUST-FIX, 0 SHOULD-FIX.** The frozen subject is `security-freeze.v8.json`, SHA-256 `33dad5ec1692ccbee859ead54d17d9730999a2d61012e2e48cbd1d2ad27e44ca`, with 72 files. I authored none of its bytes. Dispatch `security-lead-review-dispatch.v3.md` is SHA-256 `606602210cbeaf7789c62276235504361927e0e064cc867dbfd67b85c9679494`.

Fresh replay of `check-security-unit.v8.py` passed **864 checks, 0 failures**. The temporary report is `/tmp/security-lead-review-v3-replay.json`, SHA-256 `80dbe3fdb41ece4a22724ca3c01c0fe1330e80df17492ec52f0ed1319baef456`; the frozen report was not modified. The v7→v8 composition is 6 changed paths, 66 unchanged, with no additions or removals.

Review 2’s sole SHOULD-FIX is resolved. Canonical-profile envelope mutations (`2.0`, boolean, and NFD) now return the fixed `RJ-4 UNSIGNED` malformed-envelope result at step 1. Valid integer envelope verification, routing, digest and signature precedence remain intact. The v6 findings remain resolved: project stateClass cannot create global authority, policy refusals yield no grants, and courier context names align. Prior v5 boundary, traversal, broker/courier, witness/recovery, policy duplicate, journal and malformed-record controls remain covered.

The cumulative history is retained exactly: three ordinary exchanges, one UPHOLD, two failed bounded confirmations, lead review 1 OBJECT (2 MUST/1 SHOULD), and lead review 2 OBJECT (0 MUST/1 SHOULD). There is no reset and no additional confirmation. No subject files or register entries were edited. This ACCEPT is a review verdict only; it grants no implementation permission, qualification, or adoption.
