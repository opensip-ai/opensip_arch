# Review: grant journal X3b r3

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/journal-x3b/PROPOSAL.md` is 24070 bytes, sha256 `4404777dcddd392b50df71955f25a07e3f4e1da7b3fa4d73b46db51ebdc42148`, matching hashes.txt. Preserved r2 is 21949 bytes, sha256 `cb14fe66734aa913fe207543cdf3ad890255ed130b7feb9b85d2557fd5e1e78c`. Live product HEAD is `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. The real OpenSIP support directory is absent. No product cargo.

r2 RF-1 is closed. Format dispatch runs before the floor table, with or without a floor. A complete format-1 or format-2 carrier is the F46 row. A format-3 footprint that is not a lawful durable prefix is `MIGRATION.CORRUPT`. A complete format-3 carrier whose `project_key_digest` is not the lowercase hex of `SHA-256(N)` is the binding row. `floorLost` is only a complete format-3 carrier, or a witness, whose floor is absent. Each of those refusals writes nothing.

r2 RF-2 is closed for the states it named. The absent-carrier quarantine is a present floor and no carrier, with a witness or with `lastSeq` above 0. A present format-3 carrier is reconciled read-only. `witnesslessRestore`, `witnessMalformed`, `uncertainTailLoss`, a protocol violation, and a carrier mismatch leave the floor untouched. The floor is copied forward only after OK, REVERT, or ADVANCE, and only when the committed tail is higher. The INIT floor is the whole `CarrierFloor`: `highWaterSchema` 1, `projectKeyDigest` the hex of `SHA-256(N)`, `grantGeneration` 1, `lastSeq` 0, `tailSha256` null. The crash list now has the format-1/2 row and the qualified `floorLost`. A tail behind the floor is floor regression, so a higher tail still copies forward.

## Required finding

### RF-1 — A non-INIT floor at lastSeq 0 with no carrier matches no row

Row 4 resumes INIT only when the floor is `grantGeneration` 1 and `lastSeq` 0, with no carrier and no witness. Row 5 quarantines `uncertainTailLoss` when the witness is present or `lastSeq` is above 0. A decoded floor may have `grantGeneration` above 1 with `lastSeq` 0: `CarrierFloor` accepts any generation above 0, and `tailSha256` is null at sequence 0. That state matches neither row.

Failure scenario: the floor decodes as generation 2, `lastSeq` 0, `tailSha256` null, and the namespace has no carrier and no witness. The open has no action. The floor is not the INIT floor, and it is not quarantined.

Required: a present floor with no carrier and no witness is `uncertainTailLoss` unless it is the INIT floor, `grantGeneration` 1 and `lastSeq` 0. That INIT floor still resumes creation and writes nothing.

## What holds

The floor step stays under the fence before any lease, and the carrier start stays inside the handoff. That is X2 r5 item 7's ordering. The probe, the digest preimage, the writer storing no quarantine marker, and the closed floor shape are unchanged. Item 8's rows match S12: F46 is operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, with no domain detail; the format-3 footprint is `MIGRATION.CORRUPT` on `LEDGER.CORRUPT`; binding mismatch and the quarantine reasons omit `domainDetail`. The witness write for REVERT, ADVANCE, and INIT belongs to the carrier start. Item 3a still creates the carrier only when none exists.
