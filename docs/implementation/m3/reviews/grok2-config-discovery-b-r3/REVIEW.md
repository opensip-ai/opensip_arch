# M3-B r3 — REQUIRED-FINDINGS

Subject: `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, 106199 bytes, sha256 `06ac4d915c1fcdcdb22e342b33f8b90b2ae738a1fd3b838d5861c14bfbd8109f`. Diff base: `PROPOSAL-r2.md`, 94762 bytes, sha256 `92e6582534d3f59443bade8e1dd7c32f9a3fed9249b979ae2ed56cfcc15becaa`. Read-only. No cargo. `~/Library/Application Support/OpenSIP` was absent. Product main is `218465fb71fd62ca01856d40d26ec822f45233be`. The pins in `hashes.txt` match except the overnight log, which the pin says may grow; the cited entries are present by title.

r3 is a record revision. The diff is 17 hunks: the r3 table, removal of r2's acceptance note, the marked passages, and the re-pins that table names. One unchanged cell changes meaning because the cell above it was rewritten. That is RF-1.

## RF-1

Item 24's directory-custody row (`PROPOSAL.md:776`) still has `as above` in the code column.

In r2 that chain is closed. The layout row (`PROPOSAL-r2.md:752`) states `PROJECT.ROOT_CUSTODY_REFUSED` / `CONFIG.INVALID`. The in-repository row (`:753`) says `as above`. The directory-custody row (`:754`) says `as above`, so it states the same pair, with the existing custody subjects.

r3 rewrites only the in-repository row (`PROPOSAL.md:775`). Its code cell is now row 1's `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` with `JOIN_CROSSES_NESTED_REPOSITORY`. The directory-custody row is byte-identical to r2, so `as above` now names that pair.

RBS1 R2 moves the in-repository crossing onto row 1 and leaves directory custody where it was. B-S1's S3 passage says a member directory's custody failure refuses with its existing custody subject, and a crossing into a repository that cannot become a member refuses `JOIN_CROSSES_NESTED_REPOSITORY`. X2 r9 item 8 pairs those custody subjects with `PROJECT.ROOT_CUSTODY_REFUSED` (`PROPOSAL-r9.md:363`). The r3 changes table does not name this row.

The fix is to write `PROJECT.ROOT_CUSTODY_REFUSED` / `CONFIG.INVALID` (X2:250-270) in that code cell, and to leave the subject as the existing custody subjects.

## What the record holds

**Row 3.** `PROPOSAL.md:775` agrees with item 22 (`:692`) and with row 1. An explicit or config member when W fails W2 is a crossing into a repository that cannot become a member, and it keeps `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` with `JOIN_CROSSES_NESTED_REPOSITORY`. `workspace-root-inside-repository` is stated as row 6's disclosure subject for a reader entry. That is RBS1 R2 and B-S1 LD-6. Item 21 (`:640`) still lists the subjects X2 r9 lists, and it points at item 24 for when each applies. X2 r9 defers that question at `PROPOSAL-r9.md:87`, `:325` and `:374`.

**Rows 5 and 6.** n counts distinct repositories the active branch's declarations name after placement (M1 to M3), before X2 r9 item 6b reads any Git configuration or index. n > 64 refuses `PROJECT.SCOPE_LIMIT` / `REQUEST.UNSATISFIABLE` with subject `members:<n>>64` in both branches, and nothing is dropped to fit. The remedy citation is B-S1 LD-17, and the sentence at SL:1323 in `b-s1/PASSAGES.md` is the sentence LD-17 quotes, including that X2's registry-capacity remedy stays with its three subjects. Row 6 excludes the cap. When W fails W2, readers declare nothing and derive no link; a literal entry inside a nested repository is `member-excluded` with subject `workspace-root-inside-repository`, and no other entry is recorded. That matches RBS1 R4 and R5, LD-7, LD-10 and LD-17, and the reader registry's `memberCap` and `rootInRepository`.

**Bound units.** B-S1 (with SX-1) is the commit `9c11c53e96971df38e29bb142692bcad77094225`, B-S2 is `240a795898c87423b1d2fb9463fb800302f1a5d3`, and B-S9 is `8adfe0cf99e97da98edb78826cee43a9fcf708df`. Each review is `ACCEPT-DESIGN-UNIT` with no required findings (B-S2's observation stays with C1b; r3 does not call it settled). S9 is B-S9. B-S1's row drops S9. B1-a depends on B-S9. The product still carries the X12-0 string: `configuration.rs:24` is `REMEDY_CONFIG_INVALID`, `doctor_ingress.rs:216` reuses it, and `configuration_tests.rs:338-343` pins length 367 and the SHA-256. Those three files are byte-identical at `30c5db1` and `218465f`. B1-a embeds B-S9's string there and repins the test, which is what B-S9's README and review say. B2-a implements SX-1's anchor and owes the `discovery-defaults.py` refresh (LD-14, BS1-F3). The controls paragraph points at B-S1's list for B2-a, B2-b and B3-b. F10 matches B-S1 §1: `.opensip` at the selected root and at each admitted member root is an exact anchor, never entered, never source and never inventoried. F9's sentence matches the SL:286 and NE:4135 overrides, which name `AdmittedBoundaryInventoryV3`. S1 and S2 are the accepted X2 r9 and X12 r4 laws. The quoted S2 passage keeps X12 r4's own I1 citations.

**Re-pins.** All 18 M3P citations move by −2, and each cited line of `M3-PLAN-r4.md` equals the live r4 file at arch `6f85fe717`. The operative I1 citations move by −2 onto `preview-pack-i1/PROPOSAL-r2.md`; r2's I1:379–388 equal that snapshot at −2 against arch `b412bce73`. The r2 history table and item 10's quoted S2 passage keep the reviewed live numbers. X2 and X12 citation multisets are unchanged. Cited lines of `PROPOSAL-r8.md` and `PROPOSAL-r3.md` equal the live files at arch `bf3007f0f` and `0f69f15fc`; each acceptance sentence sits inside one existing line (X2 line 3, X12 line 12). X4's live bytes are `8eb4223e…`, equal to arch `22c969a0f`. ML item 17 is r1's item at lines 494–509 and r5's item at line 898, "Launch rules are the D law's, under O7."

**Cited product files.** Against `30c5db1`, the cited host, custody, platform, identity and schema files are byte-identical at `218465f`. `schemas/registry.json` differs only at line 328, a `generatorClosureSha256`. Lines 60–66 and 132–138 are unchanged. `5214350..218465f` is the three binding commits CR-1, SYN-1 and SYN-1F, and that range touches `design-lock.json` only.

## Non-blocking

NBO-1. Item 13 (`PROPOSAL.md:396`) still says `boundary_inventory` produces `AdmittedBoundaryInventoryV2`, or V3 under D15. F9's added sentence correctly reports the two V3 overrides. B-S1 LD-4 makes version 3 the current discovery record for every project. The next record can point that row at LD-4.
