# M3-O1 law r2 review

**Verdict: ACCEPT.** No required findings or new nonblocking observations. M3-O1-RF-01 and M3-O1-NB-01 through NB-03 are resolved.

Subject: `docs/implementation/m3/operability/o1/PROPOSAL.md`, **80,638 bytes**, SHA-256 `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`. Diff base: `PROPOSAL-r1.md`, **73,886 bytes**, SHA-256 `ac3f12fae691e2a9a9fa6c2fff264e3e3a5365fe36652d1bd58951ff1369d37a`. Product basis remains `b7b87b740b4332597ef9d609b1e96d7b420f8885`; the acknowledged move to 43ea32a does not change this review's basis.

## Finding resolution

| Finding | Status | Assessment |
|---|---|---|
| M3-O1-RF-01 | RESOLVED | O1-S owns the operability re-export and already depends on both O1-a and O1-p. O1-p is platform-only, with J3a as its sole prerequisite. |
| M3-O1-NB-01 | RESOLVED | All 31 pins match, including the final r2 REQUEST bytes and the actual r1 request bytes. |
| M3-O1-NB-02 | RESOLVED | Four production assertion macro sites are named correctly. Item 13 and Q1 preserve the optimized profile and add the launch-time re-audit. |
| M3-O1-NB-03 | RESOLVED | The reproduced baseline is 143 production-path lines, including security 73; 129 are in platform/security and 163 are test-only. |

RF-01's fix is consistent across item 2 (line 165), item 20 (495), item 21 (507), O1-C11 (568), the O1-p/O1-S rows (585, 588), the edge bullet (592) and X-O3 (602). O1-S first adds the re-export before migrating the call sites; its control checks that the re-export refers to the platform implementation. The pinned overnight log at arch 99de7516b, lines 876–880, records the same lead decision.

O1-p no longer requires an absent operability target. The existing platform crate, lib.rs and clock.rs are present at the pinned base; disposition.rs and the descriptor mechanism are deliberate additions within that crate. O1-p's row expressly excludes every operability file. O1-b, O1-c and O1-S retain their O1-a prerequisites, and D3a's O1-a edge remains named in the M3P follow-up. The lead's Q2 ruling is preserved: O1-p can land after J3a and before held J4a; the later change rebases.

The rejected alternatives are reasonable. Adding O1-a to O1-p would repair r1 but would serialize an otherwise independent platform unit for a re-export unused before the sweep. Putting the re-export in O1-b is also possible, but that unit does not consume dispose. O1-S already has both prerequisites and owns the first call-site migration, so the chosen location adds no prerequisite and retains a named control owner.

## Count checks

The permitted pinned recount.py ran read-only at nice 19, with Python `-I -B`, against b7b87b7. Its output equals the pinned recount.json:

- `let _ =`: 306 lines in 150 files; 143 production-path lines and 163 test-only lines. Production: platform 56, security 73, storage 10, CLI 3, lifecycle 1. Platform/security total: 129.
- The three installation_read_fixture.rs lines remain included under the stated path rule. No extra exclusion was introduced.
- Assertion macro sites: security/src/trust/floor_publication.rs:702; security/src/trust/trust_bootstrap.rs:956; storage/src/blob_store.rs:81,98. The other five debug_assert text matches are four feature-refusal attributes and one test guard string.

Each operational use of an old figure at r1 lines 56, 331, 449, 477 and 634 is corrected in r2 (73, 348, 466, 494 and 657). Remaining old figures appear in the response/history explanations. Item 19 still requires seeding the exception list at the actual integration base; O1-b still re-audits its measured artifact at launch.

## Answer and diff assessment

The answered-question table at lines 655–664 faithfully records the pinned r1 request and review:

- Q1/Q2 keep the lead rulings and the review's preregistration/rebase qualifications.
- Q3 keeps the concurrency-1 setting, typed negative-unattributed rejection above it, and the S-OP-6 aggregate-parent follow-up.
- Q4/Q5 keep the package-authority boundary and the accepted APP-pinned parent selection followed by recording.
- Q6 keeps owner-held fixed-width mints without an ambient public byte constructor.
- Q7 keeps a defensible coupled ACCEPT-UNIT boundary and an unmeasured planning estimate.
- Q8 keeps the platform-only edge, unsafe-code prohibition, required known-answer/boundary/independent-reference controls and separate code acceptance.

**Only declared changes were made.** The entire supplied unified-diff body exactly matches a fresh diff of the pinned base and subject. The base also equals the bytes committed at arch 99de7516b. Every changed region is the announced ownership/control/dependency fix, count correction, answer record or history/standing/short-name/base-context update. The remaining transport, scope, hashing, sink, finalization, phase, registration and owed-successor mechanism text is unchanged. The two S-OP-2 design-unit acceptances are recorded as context and are not re-reviewed here.

## Verification scope

All 31 supplied pins match, including REQUEST.md: 5,754 bytes / `301e777f07d272ab1f31570af8a024aa29bc4f966a3acf2555dd691bd41a3761`. Evidence is retained in [pin-verification.json](pin-verification.json), [diff-check.json](diff-check.json) and [local-recount.json](local-recount.json).

No Cargo, build, test, lead set, crash-matrix run or verify_design rerun. No repository source edits, commits, pushes or delegation. No OpenSIP real-home or private 413 fixture access. All output is under the requested review directory. This accepts the exact law bytes; implementation units, owed successors and product qualification retain their own gates.

