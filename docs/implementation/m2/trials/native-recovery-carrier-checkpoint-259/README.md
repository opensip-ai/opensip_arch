# Native recovery carrier 259 — private candidate

Exact223 snapshot:359 product files,355 unchanged,one Rust source changed,three new fixtures. Full parent archive/member verification precedes clone. No product installation or source selection.

Ports reviewed233 carrier behavior: ninth `root-recovery-authorization` kind/domain `opensip.metadata.root-recovery.1` uses RECOVERY keys; payload discriminator must be exact integer1/2 and match domain; caller capability explicit/default payload1. Empty reader declarations refuse. Existing Ed25519/strict-key/quorum implementation reused. Carrier verification does not validate the complete authorization body or grant current authority.

175 security tests PASS; workspace 472 tests plus2doctests PASS; strict workspace Clippy PASS.52 reference assertions generate44 real-signed native cases, whose outcomes/quorum members/message/body/preimage digests match. Reader capability tests and historical exact-byte delta binding included. Four compiled omission controls (dispatch/capability/domain/recovery-key source) are caught; baseline passes. TESTONLY signing keys.

Historical fixture bytes preserved. Complete carrier1805 corpus includes reviewed233 exact47 delta rows (all raw-line hashes and before results match); older1284 corpus has14 declared rows, with root placeholders still handled by inherited successor test. Only32/12 outcome strings change respectively; other listed rows retain mismatch outcome. Initial broad inventory included five unchanged parse failures per corpus; r2 narrows it to the reviewed strict-parser phase boundary, production unchanged. Beforeimages/reports preserved.

Initial recording driver stopped at missing233 editable source-pin dependency before crypto. r2 uses the full258 candidate and proves the checker/verifier are byte-identical to233; all normal source pins checked before/after. No bypass. Fixture generation is a recording-only adaptation of the reference driver. Full authorization/bundle/metadata/current revocation/held-root/S4/role/batch/native custody/census/durability/writer owners remain. Workspace build is a local development check, not an isolated-host or release qualification rerun.
