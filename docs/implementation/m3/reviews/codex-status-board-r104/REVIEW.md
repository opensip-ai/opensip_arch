# REQUIRED-FINDINGS — status board r104

Subject manifest: 8,690 bytes, SHA-256 `9a6fe0d79a98c41bef98cc4e8dad42d9fad09e903ae64a1d2d03058e5e38d940`. All 40 members match their byte counts and hashes. Product HEAD is the clean `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `8310f16a0e7fb7e009241bec2e797c2b452c4aee`.

## STATUS-R104-RF-1 — Item 6 contradicts O-1's closure

At `docs/implementation/m3/IMPLEMENTATION-STATUS.md:224`, the current Configuration/discovery item retains this obsolete sentence:

> Open for C2: O-1, the TypeScriptConfigGraphV1 extendsResolved bound of 64 edges, which item 14a does not bound.

Later in the same item it correctly states that O-1 is closed by M3-B r10, S10b and B2-c2b, then says J1 is next. The earlier sentence is false at this cutoff and conflicts with the B row, new accepted-work paragraph and item's own closure sentence. It is part of the current remaining-work summary, rather than a historical accepted-record quotation.

Remove it or explicitly mark it historical and resolved. Preserve the correct closure and remaining composition dependencies, then refresh the board pin and subject manifest. No accepted unit or inherited ledger record needs reopening.

## Verified scope

- All 293 r103 accepted records are inherited by value. Exactly E294–E297 are appended. Their review pins and accepted verdicts, architecture commits and ancestry, product ancestry and available unit-record pins match committed evidence. E294 is law-only with no unit record. The new scopes match their reviews and unit records and add no caller. The six integrated B2-c2b product files match the accepted product-map pins at `29411d18`.
- The 76 inventory and 74 contract bindings from r103 are unchanged by value. Contract bindings 172 and 173 yield 76 contract bindings, with no inventory binding added. Complete binding lists match the current lock tails; new binding pins match committed architecture bytes. The referenced product lock commits contain 172 and then 173 contract successors as stated. Inventory remains 212 with 172 inventory successors.
- `productChangesSinceR103` exactly lists Git's three commits and seven changed files. None intersects the inherited validation maps. All three historical validation-scope records remain equal to r103. `configurationDiscoveryScopes` preserves the inherited 88 entries and appends E294–E297 once, totaling 92.
- The sole moved inherited source authority is live `config-discovery-b/PROPOSAL.md`. The declared old pin matches r103's authority and publication; the new pin matches r10's publication and current committed bytes. All 13 added authority pins verify. No inherited authority was silently removed or otherwise changed.
- The previous-board snapshot is byte-identical to r103's board at `10cb57bce72c6613d77bf0734fe5a0526bdbd0cb`; the historical subject pin also matches. The cutoff and count/range lines correctly state 297 records, inventory bindings v137–212 and contract bindings 98–173.
- Only the B unit-register row changes; its status, evidence and next action appear verbatim in the board. It correctly closes O-1 and retains J1/C1 and C4 obligations. The accepted-work-after-r103 paragraph is accurate. The separate obsolete item-6 sentence is the finding above.
- M3 remains incomplete. J1 composition through C1 custody and J2b, C1 to C4, native owner/worker duties, K1, the SM-11..14 completion round and qualification remain open. No B2/M3-B completion, owner assent or product qualification is inferred.

`recordCorrectionsAccurate: true` concerns inherited accepted records: they remain unchanged, r103's standing corrections remain intact and no new historical record correction is needed. RF-1 concerns the current board narrative.

No non-blocking observations. Review used only read-only hashing, JSON parsing, file reads and Git queries. No compiler, Cargo, tests, lane, network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository, stage nor control file was edited.
