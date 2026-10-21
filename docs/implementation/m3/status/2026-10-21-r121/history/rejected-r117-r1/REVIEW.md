# Review: implementation status r117

**Verdict: REQUIRED-FINDINGS**

The frozen subject manifest has the requested SHA-256 (`0b034199e7ab16b10996842bba1e5dfcf6e25ce95b3e330441a96595cda6c1b5`). All 88 declared members match their recorded sizes and digests, all 947 architecture-authority pins rehash, and all 830 binding artifact pins rehash. One current front-door statement does not agree with that evidence.

## Required findings

### STATUS-R117-RF-1 — Correct the binding-ledger ranges in the current front door

`docs/implementation/m3/IMPLEMENTATION-STATUS.md:11` says the r117 binding ledger covers inventory bindings v137–233 and contract bindings 98–178. The frozen ledger, current design lock, checks, and source record establish 98 inventory bindings through v234 and 85 contract bindings through successor 182. The same front door correctly reports inventory 234 and contract successor 182 at line 3, so line 11 is internally inconsistent and understates the current ledger.

Update line 11 to state the actual complete ranges, inventory v137–234 and contracts 98–182. Regenerate the subject manifest and preserve this rejected review in the correction history.

## Verified evidence

- The first 376 accepted-work records are preserved by JSON value from r116. Exactly E377–E387 are appended, with contiguous IDs, eleven distinct scoped records, and exact accepted unit/review pins.
- The product ancestry from `21306d28b4c0508d9219d53b428dd84163c7567d` to `f8dec47906e44bc3d35f7f0c18e23669b595cbae` is exactly the declared eight commits. The architecture ancestry from the accepted r116 publication to `b8b5517acd2cd570ee7ac081fc43f91913f18451` is exactly the declared eleven commits. Source contracts 179–181, inventory 234, and description contract 182 are recorded as design-lock bindings rather than product-code commits.
- Inventory 234 has 194 successors and retains packages 20, pending 9, and planned 91. Its 117 inherited descriptions preserve 113 prior meanings plus four accepted CI-3L meanings. Contract 182 adds 15 direct current-inventory descriptions without changing those 117 inherited entries, and the status record carries the requirement that a future inventory successor project the 15 direct meanings as well.
- The binding ledger is the exact current-lock tail: 98 inventory bindings and 85 contract bindings, with all 830 artifact pins matching the live architecture bytes.
- E377–E382 keep source selection, generator profile, loader policy, complete 42-path materialization, additive inventory, and description qualification distinct. The code evidence remains scoped to 21 owning checks, 17 caught/restored compiled mutants, 72 legacy Rust forms, 26 native forms, 352 generator inputs, eight outputs, and 15 new synthetic companions. No semantic source-39 registration, production caller, source/profile admission, or qualification is claimed.
- E383–E385 are procedure records only. The original postcheck failures and the first supplement's custody failure remain explicit. Only the separately reviewed and freshly root-assented second procedure supplies the successful 9 Rust, 21 companion, 25 discovery, and design checks used by E386's post-run acceptance. The two real blind modes remain once each, with five ordinary checks and the exact five-unit binding union; no retry is hidden.
- E386 integrates exactly two existing receipts and two existing census files at product `91f422b11bedac820d27c52289c2a499cf4c757f`. E387 separately records the one-file, one-additive-line product fixture repair at product `f8dec47906e44bc3d35f7f0c18e23669b595cbae` and architecture `b8b5517acd2cd570ee7ac081fc43f91913f18451`, closes `OWNPAT-CBRUN-R1-NBO-1`, and leaves all four receipt/census data hashes unchanged. The front door explicitly records the resulting status-only closure of `OWNPAT-CFIX-R1-NBO-1`.
- Historical host validation remains scoped to its unchanged mapped files; no current whole-host run is inferred. Relative links resolve, register/table roles agree, owner assent is not inferred, and D2b-3c, the Rust triple, D4, CI4, D5, C/J/S6/CF, Linux, owner, privacy, platform, clock, and whole-project qualification gates remain open.

## Non-blocking observations

None.
