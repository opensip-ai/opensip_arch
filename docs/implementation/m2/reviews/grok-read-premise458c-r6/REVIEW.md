# Review: read premise 458c r6

Grok is the single reviewer. Claude Opus 5.5 leads. Law review. No repository edits and no product cargo.

Subject `docs/implementation/m2/read-premise-458c/PROPOSAL.md` is 18468 bytes, sha256 `e49dc83739ef24e40963a16b7cf4727eeadf1e8087ca4fe1f858d44264ea9b53`. Product HEAD is `417d44362e07b61ca3c34e9bfc1bc5ea76406eba`. The diff against preserved `PROPOSAL-r5.md` is the header, item 10, and the structural-finding bullet of item 12. The preserved r5 file is the accepted text with the acceptance stamp in its header.

## Verdict

**ACCEPT.**

Each structural finding is one `DomainDetail` whose code is the existing `CONFIG.CUSTODY_REFUSED` and whose subject names the finding. 458c-c is the unit that builds the first doctor report assembler.

## Classification

468 item 6 publishes an incomplete installation as request-rejected, exit 2, error `CONFIG.INVALID`, detail `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`. `CONFIG.CUSTODY_REFUSED` is an existing `DomainDetailCode`. A doctor defect is a `DomainDetail`: required `code` and `remedy`, optional `subject`. `subject` is `BoundedText` (maximum 1024). The product type `Common4DomainDetail` has that shape. No new enum member, registry row, or envelope field is required.

Item 12 puts `CONFIG.CUSTODY_REFUSED` on each finding and keeps the `installation-incomplete` subject family:

- `installation-incomplete:missing:<path relative to I>` for `IncompleteRefusal::Missing` (absent or non-regular);
- `installation-incomplete:pair`, `:marker`, `:store`, `:node`, and `:chain` for the other five variants.

The session records those six variants and no other structural finding. Independent members can each be missing, and the path keeps those entries distinct. Pair, marker, and store are one finding each. The node walk records one node finding and stops, or one chain finding when the walk fails without a node finding. A decoded store id is 32 lowercase hex characters, so a marker path `stores/<id>/store-instance.v1` and a lineage path `transitions/lineage/<id>/<generation>/<schema>.node` stay inside `BoundedText` with the prefix.

A produced report still follows owner §5. A positive actual-defect count selects `DOCTOR.DEFECTS_FOUND` and exit 0. These entries count, because the code is an existing classification and is not `INSTALLATION.DURABILITY_NOT_CHECKED`. A custody refusal, a busy fence, a budget refusal, or any other item 6 refusal still produces no report. Every other read command still ends on the single incomplete row, subject `installation-incomplete`.

The remedy is one fixed text per kind. It says the installation is incomplete and that OpenSIP does not repair it, which is owner §6. 458c-c reviews the text.

`doctor-cases.json` still drives count, notice, capacity, overflow, and the unproducible report. Its synthetic actual defects stay `DELIVERY.CLOSURE_BYTES_CORRUPT`, and the inherited pair stays the two existing delivery and component codes. Those cases do not classify an installation finding. Item 12 names that classification. The case file's bounds stay the report law.

## Assembler

The product has generated `Invocation5DoctorResult` and no report assembler. Owner §5 already assigns doctor the defects channel, the 255+1 complete-root rule, the 256 partial-root bound, `DOCTOR.DEFECTS_FOUND`, `DOCTOR.REPORT_NOT_PRODUCIBLE`, and the latch. r5 already gave that note to 458c-c. Item 10 has 458c-c build the library assembler on that existing shape, following `DoctorSession.assemble`: admit the actual details, reserve the note only for a complete I, refuse and latch when the report cannot be produced, and return the existing `DoctorResult` fields. Item 12's entries are the actual details for structural findings. The human label "Informational: durability not checked" stays with the CLI renderer. The reference appends it in the human projection. The cases' label expectation belongs to that renderer.

## Required findings

None.
