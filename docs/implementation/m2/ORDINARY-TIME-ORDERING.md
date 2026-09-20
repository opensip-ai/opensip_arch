# Ordinary authentication and clock ordering

Implementation integration finding; actual independent Grok296 source review completed September20 (ORDERING.md; archival pending the report hash-label correction). This does not change frozen289/295 bytes or claim an installed behavior.

The exact215r14 OWNER.md §C.3 requires complete relied-on authentication before using payload times, followed by S4 and its durable write-ahead; shared root/list validity and remaining entry guards apply at the resulting evaluation time. A later refusal does not erase that write-ahead.225r2 TIME-PRODUCER.md likewise derives ordinary newestIssuedAt from manifest/catalog/list, with final-root issue time separate, only after complete authentication.

The existing native verified_root_chains::verify_root_chain combines signature/continuity evidence with evaluation-time guards: ExpiredNoChain, FinalExpired and FinalFuture.289's full root adapter and295's rooted composition retain that full conditional contract.296's source projection over their result can test exact source selection, calendar validation and provenance, but MUST NOT be wired unchanged as the complete pre-S4 producer. Otherwise current root expiry could prevent a clock write-ahead that C.3 requires before a later entry refusal.

Required integration:

1. Keep the full chain helper's existing contract for its existing consumers and tests.
2. Introduce a distinct pre-time root-authentication result. It must retain all root body/schema/calendar, reader, root identity, version/previous/+1, nondecreasing issue, actual old/new signatures, finite-union threshold, first-presented-root and bounded capture checks. It must not accept arbitrary evaluation/wall inputs or silently convert to full current root admission.
3. Compose that result with shared BUNDLE/catalog/list authentication, full inventory-body/catalog joins and derived T1 component authority. Current/BEGIN/history/population qualification remains mandatory independently.
4. Derive the ordinary three-document maximum and separate presented-root issue input. Evaluate S4 under the actual admitted clock context and observation. Persist its complete original-context proof before any corresponding floor publication.
5. Apply root/list validity, minimum versions, same-version identity and every remaining entry guard at the resulting tEval. Run the ordinary completeness owner and preserve the S4 write-ahead if this later stage refuses.

The future-root predicate overlaps S4's payload/root future preflight. Its exact refusal ordering must be checked against the existing owner; do not replace public outcomes or invent a bypass flag. Same-head expired roots and otherwise-authentic future roots need paired tests distinguishing authentication evidence from successful full entry. Invalid ROOT signatures or malformed intrinsic validity intervals must remain pre-time failures.

This is a sequencing gap in connecting previously conditional helpers, not evidence that the installed product has accepted such a payload. No new source selection or implementation readiness is asserted.

## Independent review precision

Actual Grok296 reproduced243 security tests and reviewed frozen215r14/225r2 sources. Its separate ORDERING.md confirms the split. ExpiredNoChain/FinalExpired are the checks that can incorrectly suppress the required write-ahead: apply resulting-time validity after S4 succeeds. FinalFuture moves to S4 preflight after source selection; it legitimately refuses with no clock write. Intrinsic issuedAt < expiresAt and calendar validity remain authentication requirements. The new authentication type must accept no wall/evaluation arguments, even ignored ones, and may not convert into full current admission. Catalog/root expiry projections are evaluation inputs, not floor-write fields. Existing public refusal families stay unchanged.

297 is being tested as this distinct authentication phase. It still depends on externally supplied accepted-head/current-context premises. Neither this note nor the source review certifies current population, OS clock, durable publication, full import or product readiness.
