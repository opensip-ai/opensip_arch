# Status board r106 review

Verdict: **ACCEPT**. No required findings or non-blocking observations.

## Exact subject and inheritance

Independently verified the 8,690-byte subject manifest SHA-256 `a50fd06c09f90ef9600728d31e78190c02f5677e27d07b43e12de914fb271f75` and all 40 members, then rehashed them before writing. Product main is clean at `e937dac74c8e529fee3efb6f84439d05280e48ea`; architecture HEAD is `3f930927dc288f6bdbd9fe9ec826564ad2f74081`, matching the cut-off.

Compared the inherited data against r105's committed bytes at `2894884ef33b0434a7c09029d2f727cf5f7a2524`, without re-reviewing the closed units:

- All 305 accepted-work records are equal by value; exactly E306–E310 are appended, giving 310.
- All 78 inventory bindings and 76 contract bindings are inherited by value. Only v215 and v216 are appended: 80 inventory bindings, still 76 contract bindings.
- Earlier `productChangesSince*` entries, inherited validation scopes and scope lists are unchanged. The snapshot/supervisor list preserves its prefix and contains each E298–E310 exactly once.
- The authority list preserves its inherited prefix exactly; the 13 appended pins match their archived bytes. `authorityRepins` remains empty, as does the inherited global `recordCorrections` list.
- The previous-board snapshot is byte-identical to r105's committed 274,201-byte front door, SHA-256 `76ecd774afc5a1288997e26fa86575277558fbc52bb82a38d9f06ee89113a5c3`. Its original, snapshot and historical-subject pins verify.

## Appended accepted scopes

| Record | Scope | Architecture commit | Product commit |
| --- | --- | --- | --- |
| E306 | C1a2 code/model unit | `0272078e` | `41f6cae7` |
| E307 | Corrected inventory v215 | `43eeba89` | `34a3cd89` |
| E308 | D2a common control codec | `3a662678` | `a9a84a6f` |
| E309 | D2b plan r3 only | `1649a041` | none |
| E310 | Inventory v216 | `3f930927` | `e937dac7` |

For each, verified its review pin and accepting verdict against committed architecture bytes, architecture ancestry, product ancestry and the unit-record pin where present. E309 correctly has no unit record; its plan and explicit lead assent are pinned separately. All 14 integrated C1a2 product-map files and all seven D2a files match the accepted candidate pins at their respective product commits. This verifies integration identity, not their implementations anew.

The scopes retain the accepted limitations: C1a2 is preparatory capture/custody and model work with no caller, sealing or ledger profile; D2a is a codec with no stream acquisition, supervisor caller or provider protocol; D2b is plan acceptance rather than subunit completion.

E307 correctly carries both inventory review rounds and the preparation-path defect, with round 2's accepted v215 destination authoritative. E308 preserves D2A-R2-NBO-1 as a unit-record correction: the recorded mutation demonstrates context reassembly only; the lead's separate policy-field check is attributed to the lead and not represented as lane evidence. This appends a corrected unit scope without rewriting an inherited record or the accepted subject.

## Bindings and validation scope

The v215 and v216 binding objects exactly match the product lock. Their parent, candidate, successor, review and assent pins verify. Both product binding commits change only `design-lock.json`. The cut-off lock pin matches; it contains 176 inventory successors and 173 contract successors, ending at inventory v216. No contract successor was added in this update.

`productChangesSinceR105` exactly matches Git: four commits in reverse ancestry order and 22 changed paths. Its intersection with inherited mapped validation files is exactly `crates/host/src/lib.rs`. That diff adds 10 lines and removes none: comments and the macOS-gated candidate_custody/snapshot module declarations. Other inherited mapped validation files are unchanged across this interval.

The host validation scope remains at `76d30ee0e65e3e01042b30ae08c856bf0df2fc2e`, with `notRerunOnMain: true`. Independently verified its product-map candidates at that historical commit. Its 300-test result is not claimed as a current-main pass; the source record explicitly distinguishes C1a2's own equal-failure-set validation. This follows the historical-scope treatment of earlier status rounds and does not transplant validation to changed code. Root-observation and slot-execution scopes remain untouched.

## Board and open work

All 23 board table rows agree with the machine-readable register's status, evidence and next action. Only the C and D family rows change. The C row closes C1a2/v215 alongside C1a1 and leads with C1a3, the r9 cap record and C1a4. The D row closes D2a/v216 alongside D1a and records D2b plan r3 while keeping its five implementation subunits and D3a–D5 open. D1a remains macOS-scoped.

The cut-off line, 310-record explanation, v137–216 / contract98–173 ranges and accepted-work-after-r105 paragraph agree with the ledgers. No whole C1, D2, M3-C, M3-D or M3 completion is inferred. C1a3/C1a4 with r9, C1b/C1c, D1a-L/D1b, D2b implementation, D3a–D5, J1 composition, C2–C4, native owner/worker, K1, SM-11..14 completion and qualification retain their gates. Later draft-review developments are not accepted work at this pinned cut-off.

Owner assent is not inferred. Explicit existing assents are distinguished from the lead's forthcoming status assent. Fresh design verification and architecture-only publication remain subsequent steps; no qualification or push is claimed.

## Boundaries

Only read-only hashing, JSON parsing, inspection and Git queries were used. No compiler, Cargo, tests or lane was run. No network, other pane, delegation, private 413 fixture, installation, signing key, held tree or T2 held-out entry was accessed. Neither repository, the stage nor control files were edited. Only the requested REVIEW.md and review.json were written.
