# Review: implementation status r120

**Verdict: ACCEPT**

The frozen subject manifest has SHA-256 `1555cb3e50af69f724859ddbcd24d203b93866f59ccc19b1808b56351c3aee07`. All 223 declared members match their recorded sizes and digests, the manifest has no duplicate path, and the stage contains no missing or undeclared subject file.

## Required findings

None.

## Verified evidence

- The live product and architecture heads are exactly `0f5bbe492a40ff03c18262536f58c86e5af64be0` and `5cfac374ac9e3f853f978726a4f66e1c7da335f7`. The current `design-lock.json` is 762,295 bytes with SHA-256 `bde5e7720e8ef8f1b57d23143caccff1315d1aa96e43304a3732b05a295a9d92`. All 986 architecture-authority pins and all 857 binding-tail artifact pins rehash against the current repositories.
- The accepted-work ledger contains contiguous unique IDs E001-E398. Its E001-E396 prefix equals accepted r119 by JSON value. Exactly E397 and E398 follow: E397 is the jointly reviewed full D2b-4b code plus inventory237 unit, and E398 is description contract185. There is no fabricated independent inventory-review record.
- The product history after accepted r119 is exactly three commits in order: `348d70152b30d69787970f74bbf3c67806301955`, `c12e63063e09ce25e07028b60414d8d2a5b5dae3`, and `0f5bbe492a40ff03c18262536f58c86e5af64be0`. The first changes the exact 24 accepted D2b-4b paths; the latter two change only `design-lock.json`. The architecture history after accepted r119 is exactly `cc95944033afb016921fd455a6543b8ec3be99df` and `5cfac374ac9e3f853f978726a4f66e1c7da335f7`, matching E397 and E398. All cited commits are ancestors of the live heads.
- E397 resolves to an `ACCEPTED-UNIT` record with substantive root assent and an `ACCEPT-UNIT` independent review. That same review explicitly accepts inventory237; its review JSON contains the inventory assessment and exact parent, candidate, and successor pins. E398 resolves to an `ACCEPTED-DESIGN-UNIT` record with substantive root assent and an `ACCEPT-DESIGN-UNIT` review. Both records have empty required findings and retain `productQualification:false`.
- The binding ledger is exactly the current lock's inventory tail v137-v237 and contract tail 98-185. It contains 101 inventory bindings and 88 contract bindings. The current lock has 197 inventory successors, 185 contract successors, and 145 inventory-passage inheritance entries.
- Inventory237 contains 1,410 unique file rows. Its 1,392 parent rows are equal by path and value to inventory236, with no removal or changed existing row; exactly the 18 Rust3 send paths are added. The 20 packages and nine pending decisions remain equal. The accepted unit preserves the 91 planned absences.
- Contract185 has exactly five raw inventory237 overrides and one explicit supersession of contract184's provider-dispatch passage. The supersession names the exact prior record, inventory236 parent, and `/files/48/description` selector. The 145 inherited meanings remain unchanged, the five new direct meanings bring the current effective population to 150, and the next inventory is explicitly required to fold the supersession so the stale dispatch meaning cannot survive.
- The archived D2b-4b evidence and accepted unit agree on the scoped implementation: 24 changed paths and 18 new paths; 55 carrier duties with 23 builder/sender locations; the 32 source-derived limits and signed tokens; complete manifest, native-H, and raw-wire commitments; all prepared rows including failed rows; per-key C4 scope-2 joins; complete envelope accounting with one maximal Cancel reserve; independent Plan-derived sender realization; and the actual table-gated participant with one-I/O turns, pending-Cancel ordering, frame preallocation, and once-only original-buffer transfer after DONE.
- The current 24 product source pins match the accepted integration bytes. The focused evidence records 87 Rust3 tests, 362 component tests, 86 identity tests, equal empty candidate/base failure sets, component all-target warning-denied Clippy, 21 freshly compiled runtime mutation kills, and exact restoration of all 23 mutated Rust sources. The lexical-census path is separately pinned and audited. No retained past mutant executable is claimed.
- The status boundary is correct in both visible and machine-readable forms. Rust3 4a base receive and 4b host send/base participant are accepted and integrated; reference host V3 construction is supported at every count under the selected token. The current receiver and participant still refuse census/reference worker sessions pending 4c, and `Rust3CodecAccepted` remains false. The 23 visible unit-family rows equal the machine register field-for-field.
- The full default-workspace tests and Clippy at `abb39a09d4dbb20c01e9d61d3ed1c70831ea84ba` are correctly retained as historical after the 4b source changes. Current full-workspace test and Clippy flags are false, the current tested-workspace product is null, and current evidence is limited to the accepted components/identity/Clippy scope. Prior red and ignored histories remain disclosed without waiver.
- Both public binding objects equal their current receipt bindings. Their 80 referenced product/architecture pins rehash, all four public receipt/census files match their recorded bytes, and the record claims zero blind invocations and no private-content inspection.
- The previous-board snapshot is byte-exact to accepted r119. The 11 owner decisions are unchanged, all 13 front-door/update-protocol relative links resolve, lead and reviewer roles are current, and no product test or lane is attributed to this status review.

The board leaves D2b-4c FA-2/reference worker admission and replay, H/C4, production and source39 composition, D4-4, CI4, D5, C/J/S6/CF, Linux/platform, owner/privacy/clock/T2, and full-project qualification open. It does not promote scoped 4b evidence to production or product qualification.

## Non-blocking observations

None.
