# Status board r107 review

**Verdict: REQUIRED-FINDINGS.** One required finding; no non-blocking observations. The factual ledger and binding changes pass review, but the D-family row does not render its intended next action.

Subject manifest SHA-256: `02119f5fa52f0bf6766817295168a57116ae823cbd1b82694276d4efd108e388` (8,690 bytes). All 40 subject members match their recorded lengths and hashes. Product cut-off: `23b3871269c6553c96097084dd412b3aa95dec68`; architecture cut-off: `ae83833d05d956a0562e188f0ad04fc37a63944b`.

## Required finding

### STATUS-R107-RF-1 — Escape the new pipe in the D-family table row

**Location:** `docs/implementation/m3/IMPLEMENTATION-STATUS.md:252`.

The new D3a evidence contains `{reason: io-failure with its errno (K2 Errno) | work-exhausted with no errno}` inside the four-column Markdown table. Its unescaped `|` creates a fifth cell: the Evidence cell ends early, the remainder beginning `work-exhausted with no errno}` becomes Next action, and the intended Next action beginning `D1a (macOS), D2a and D2b-1 are accepted and bound` is an extra cell discarded by GFM table rendering. The predecessor D row had five delimiter pipes; this row has six.

This hides the intended remaining-work sequence and breaks the visible board's agreement with the machine-readable register. The prose paragraph outside the table and the JSON string may use this separator normally.

**Required correction:** escape the table's literal pipe as `\|`, or write the alternatives using “or.” Confirm the row has four cells and the D1a-L/D2b/D3a/D3b/D4/D5 next action occupies the final cell. Refresh the changed subject pins.

## Verified records and bindings

- All 310 predecessor records are inherited by value from accepted r106 at `24fbf182c3d3144d8a159bee7d9d2a0e6418996c`; exactly E311–E316 are appended, totaling 316. Inherited records were compared, not re-reviewed.
- E311's D3a plan r4 review and explicit lead assent support plan acceptance with LD-D3A-17 and carry NBO-1 to D3a-1. No implementation completion is inferred.
- E312's C1a3 review, unit record and product commit `a68be52f` agree. All ten committed paths match the archived product-map candidates. Its scope remains preparatory sealing without a caller, read set, Git implementation or snapshot profile.
- E313's v217 review and unit record match the binding at product `3e70bbf2`.
- E314's M3-C r9 review and explicit lead assent support a law record only. Caps remain conditional on C1a4's remedies (a) and (b-prime); the downstream documentation observation is carried to C1a4. No profile or binding is claimed.
- E315's D2b-1 review, unit record and product `d70af811` agree. All eight committed paths match the archived product-map candidates. This closes wire mechanics only, without a caller or either complete codec.
- E316's v218 review and unit record agree with the binding at product `23b38712`.

For each new record, checked review lengths/hashes and verdicts at its architecture commit, unit-record pins where present, recorded prior review rounds, architecture ancestry to the cut-off and product ancestry to the cut-off. E311 and E314 correctly have no unit record; their explicit lead assents are authorities.

The 80 inherited inventory bindings and all 76 contract bindings are equal by value. Only v217 and v218 are appended, totaling 82 inventory bindings. Both equal bindings in the cut-off design lock. The pinned lock verifies and contains 178 inventory successors and 173 contract successors.

## Validation history and authorities

`productChangesSinceR106` matches Git's four commits, in order, and its complete 19-file change list. Exactly one of the seven inherited validation-map paths changes: host `lib.rs`. Its diff adds the sealing module declaration and comment (four lines, no removals). Identity `lib.rs` gains eleven lines for the NFC helper/version and is absent from those scope maps.

Verified all mapped candidate pins against each scope's own product commit. Keeping the 300-test host validation historical at `76d30ee` is correct; it is explicitly not claimed on main. Root-observation and slot-execution scopes remain untouched. All inherited scope lists and earlier `productChangesSince*` entries are equal by value. `snapshotAndSupervisorScopes` enumerates E298–E316 once each.

Inherited authority rows are unchanged, and all 16 appended authorities hash correctly against committed bytes at the architecture cut-off. These include the two plans/law records and their lead assents, new reviews/unit records, and r106's review/assent. Empty `authorityRepins` and `recordCorrections` are accurate. The previous-board snapshot is byte-identical to the accepted r106 board at its publication commit.

## Board scope and remaining work

Apart from the table rendering defect, the changed C and D status/evidence/action text agrees with the register and accepted scopes. The cut-off line correctly states inventory 218 / 178 successors and contracts 173; the evidence-count line correctly states 316 records, v137–218 and contracts 98–173. The new “accepted work after r106” paragraph stays within the six accepted scopes. C1a4 leads the C next action with its required blind refresh. D2b-0 and D2b-2 through D2b-4 remain open; the accepted D3a plan does not close D3a-0 through D3a-3.

C1a4, C1b/C1c; D1a-L/D1b, the remaining D2b units, D3a/D3b/D4/D5; J1 composition, C2–C4, native owner/worker and K1; and SM-11–14 completion/qualification remain owed. Neither parent-family completion nor whole-plan completion is inferred from these child records. No owner assent, product qualification, push or fresh validation is inferred.

Only read-only hashing, JSON inspection and Git queries were performed. No compiler, Cargo, tests or lanes ran. Neither repository nor the stage/control files was edited. Only the two requested review artifacts were written.
