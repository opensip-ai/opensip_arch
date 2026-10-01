# Review: grant journal X3b r4

Verdict: ACCEPT.

Subject `docs/implementation/m2/journal-x3b/PROPOSAL.md` is 24340 bytes, sha256 `296c05673cb535aec3d363f6ff908ef3d7011b2351d6322b67c47fa492c4a156`, matching hashes.txt. Preserved r3 is 24070 bytes, sha256 `4404777dcddd392b50df71955f25a07e3f4e1da7b3fa4d73b46db51ebdc42148`. Live product HEAD is `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. The real OpenSIP support directory is absent. No product cargo.

The diff against r3 is the header and one floor-table cell. r3 RF-1 is closed.

## Floor table

Format dispatch is unchanged and still runs before the table. A present floor that reaches the table has already decoded as a whole `CarrierFloor` whose `projectKeyDigest` is the hex of `SHA-256(N)`. A decoded floor at `lastSeq` 0 has `tailSha256` null, and `grantGeneration` may be any integer above 0.

No-carrier rows, in order:

- Floor absent, no carrier, no witness: write the whole INIT floor.
- Floor absent, complete format 3, any witness: `floorLost`.
- Floor absent, no carrier, witness present: `floorLost`.
- Floor present, no carrier, witness absent, and the floor is `grantGeneration` 1 at `lastSeq` 0: INIT resumes under the lease. Nothing is written.
- Floor present, no carrier, and any other witness or floor state: `uncertainTailLoss`. The cell names the r3 case, generation 2 at `lastSeq` 0.

That fifth cell is the complement of the fourth. A witness with the INIT floor matches it. A witnessless floor at generation 1 and `lastSeq` 0 does not, because the witness is absent and the floor is that INIT floor. A present format-3 carrier still takes the reconcile row. Format 1, format 2, and an unlawful format-3 footprint still refuse in the dispatch and write nothing.

Item 3a remains the creation procedure the INIT-resume row names. Its guard is a present floor at `lastSeq` 0 with no carrier and no witness. Generation 2 at `lastSeq` 0 is `uncertainTailLoss` in the table, so that row does not resume creation. The crash list's `floor 0` bullets stay the INIT floor from r3: generation 1, `lastSeq` 0, `tailSha256` null.

## What holds

The floor step stays under the fence before any lease, and the carrier start stays inside the handoff. The probe, the digest preimage, the writer storing no quarantine marker, and the closed floor shape are unchanged. Item 8 is unchanged and still matches S12: quarantine and binding mismatch are operational-failed, exit 4, `LEDGER.CORRUPT`, with `domainDetail` omitted; a format-3 footprint is `MIGRATION.CORRUPT` on that same code; F46 is `HOST.IO_FAILURE`, `host-io`; a busy journal transaction is `LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY`. Reconcile stays read-only in the floor step. The floor is copied forward only after OK, REVERT, or ADVANCE, and only when the committed tail is higher.
