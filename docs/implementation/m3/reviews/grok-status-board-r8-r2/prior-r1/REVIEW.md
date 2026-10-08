# M3 status board r8

REJECT. One standing sentence in the current front door still assigns the bound R3-MR1 membership and raw manifest recipe as unresolved work. The counts, pins, ledger, and lock agree. Finding SB-R8-01 is the required correction.

The subject is `docs/implementation/m3/status/2026-10-08-r8-subject.json`, 3128 bytes, sha256 `3e30576c23e3d6057a5d709d5a9284756f5ae24454576c1c1ad2289de4c9a641`. schemaVersion is 1 and the unit is `IMPLEMENTATION-STATUS-2026-10-08-r8`. It lists 15 sorted unique members under `files`. Every member's length and sha256 matched the stage. The manifest is the extra file on disk and is not one of the 15.

## Bases

Product HEAD is `e14b268a94853e6bce87d1626f342814a45833c5` and the product tree is clean. Architecture HEAD is `7a6f87dc1b5cfd1b7d62332ac50b03a9f6b3be4b`. The only untracked architecture path is `docs/implementation/m3/syntax-e/e2s/`, which is outside this subject. Both requested commits are those HEADs. `7ded60c922dbf019eb70bb68ab5a99bba0c17f62` is an ancestor of the product head, and `370be08a26a3ca05c2c90d6a5703656aaf1ef01b` is an ancestor of the architecture head.

Committed `design-lock.json` at the product head is 592225 bytes, sha256 `4002cc982ae33912a02830d68952240f9bbcf874c259450580e1472bb736c5b2`, schemaVersion 4, with no `SCRATCH`. It has 130 inventory successors and 141 contract successors. The inventory tail is `repository-file-inventory.v170.json`, 639076 bytes, sha256 `6f6b43a8f6f75587864f87705482f7fa5db25e362276fa5fe0cb82e1c0db96ef`. The contract tail is the R3-MR1 successor, subject `6d92876e53c18a4cdf6de87c80cfffbdf83e7453a450bbd6f84e25c6862bafd8`, review `bafaea535d80efecebf3f20dc306c33010bb6f451b29bb1486e4a6f5041db67d`, and assent `beb681d314d3eb3f81566ab03ccbc0b5f0072fc3132322fe781dca3073942e20`. Against the r7 lock at `7ded60c`, the 140 earlier contract successors, all 130 inventory successors, and all 103 passage-inheritance rows are equal by value. The only product diff from `7ded60c` to `e14b268` is `design-lock.json`. Product code is unchanged. Inventory stays 170.

The architecture diff from `370be08` to `7a6f87d` is the R3-MR1 design tree and its archived review. This status stage is not in that commit. The front door says its own architecture commit follows the cutoff. The live `IMPLEMENTATION-STATUS.md` at both `370be08` and `7a6f87d` is still the r7 board.

## Preserved r7 record

`history/previous-board.md` is 16431 bytes, sha256 `97d5bed1c7dafa3fc3beeca33b0058ba4910b3019a795a5f391ae72d96147cd6`, byte-identical to `docs/implementation/m3/IMPLEMENTATION-STATUS.md` at architecture `370be08`. The historical r7 subject is 3128 bytes, sha256 `9776cb61941facf5a71859243e5838058f6f5e72d0dd14bc1e40462b7a073099`.

Accepted-work records E001–E057 equal the r7 ledger by value. E058 is the one added record. Inventory bindings are 34, versions 137 through 170, equal to the r7 bindings and to the lock tail. Contract bindings are 44, successors 98 through 141. The first 43 equal the r7 bindings. The 44th equals the new lock tail. `UPDATE-PROTOCOL.md`, the three C2a advisory files, and the owner-decision packet are byte-identical to r7.

The ten decision cards keep the same ids. O7, D3, and D13 stay `AWAITING_OWNER`. The only card change is NIJ1-R3-CODECS: state `NIJ1_AND_R3_MR1_DESIGN_BOUND; COMPLETE_R3_CODEC_PRODUCER_FAILURE_PUBLICATIONS_OPEN`, with the next action that keeps NIJ-1 and narrow R3-MR1 closed and leaves package/owner witnesses, namespaces, failure composition, and the security library/harness open. The front-door decision table matches those ten cards, including that next action.

The unit register has 23 rows. O1-b stays `ACCEPTED / INTEGRATED / INVENTORY BOUND`. E2s and J4a stay held. The only row change is C1a/b/c; C3a/b/c; C4a/c; X12d. Its evidence and next action record the bound narrow recipe and the open package/owner/failure/library remainder. The front-door family table matches all 23 rows.

Twenty-two authority pins in `source.json` match architecture `7a6f87d`, including the R3-MR1 review, 400 bytes, sha256 `bafaea535d80efecebf3f20dc306c33010bb6f451b29bb1486e4a6f5041db67d`. That review is `ACCEPT-DESIGN-UNIT` with empty findings, subject `6d92876e53c18a4cdf6de87c80cfffbdf83e7453a450bbd6f84e25c6862bafd8`, inventory 170, contract successors after 141, and `R3Resolved`, `productImplemented`, `productQualification`, and `entirePlanComplete` false. The assent unit records lead assent, `ownerAssentInferred` false, and the same open gates. The bound `recipe-controls.json` records four schema copies, two positive digest vectors, and fourteen malformed-row refusals, with `R3Resolved` and `productExecuted` false. This review did not re-run `verify_design.py`. `checks.json` records `productTestsRun` 0.

`source.json`, `checks.json`, the ledger, and the binding file agree at 58 scoped records, 34 inventory bindings, and 44 contract bindings. Twelve current front-door links and twelve previous-board links resolve when the previous board is read from `docs/implementation/m3/`, the directory of the front door it copies. O7, D3, D13, effective L, S-M, product qualification, GT, and the held E2s and J4a gates are unchanged.

## SB-R8-01

`IMPLEMENTATION-STATUS.md` item 1 still says the lead ready action is to resolve the remaining R3 owner membership/manifest recipe and native codec publication duties. The paragraph after item 5 still says R3/native-codec proposals remain ready noncolliding law work. Both sentences are the r7 wording.

The new "What is done" paragraph on that same page says R3-MR1 is accepted and bound as the narrow membership and raw source-specific array selection, and that package/owner witnesses, namespace and failure publication, and the security library/harness remain owed. `source.json` `activeProductUnit`, E058, the NIJ1-R3-CODECS card, and the C1/C3 family row say the same thing. Item 1 and the closing paragraph do not. Revise them so the ready action is that still-open publication, and so they no longer treat the bound membership and raw manifest recipe as unresolved proposal work.

## Scope

`ownerAssentInferred`, `productQualification`, and `entirePlanComplete` are false. Publishing this status record does not change product code, inventory, law, or the lock, and it does not close R3, C3c, effective L, or the execution loop.
