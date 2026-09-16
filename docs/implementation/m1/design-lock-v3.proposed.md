# Developer design lock v3

Candidate implementation profile; actual code review pending. Version3 carries
forward the base approval/input pins and the accepted v2 inventory binding, then
adds one `contractSuccessor` with exactly four {path,sha256,bytes} pins: record,
subjectManifest, review, assent. Older lock1/2 remain supported and reject unknown
fields. This is still developer provenance consistency, not runtime authority or
cryptographic reviewer identity.

The exact independent review must ACCEPT-DESIGN-UNIT on the selected subject
manifest with no required findings. Root ACCEPTED-DESIGN-UNIT, substantive assent
and empty required unit findings must bind that review, manifest and successor
record. The record must be a member of the reviewed subject; its candidates must
cover exactly every other subject member with identical pins. All actual bytes
are verified without executing any candidate reference script.

Each sorted unique parent pin must be selected by the accepted source/application
overlay or be the separately accepted inventory candidate. A candidate cannot
overwrite a parent path. Optional previousCandidate is verified as historical
bytes, not as an approval. Exact passage overrides select one string from a
pinned parent by positive line number or JSON Pointer and supply its distinct
replacement. Duplicate selectors, stale before-text, invalid pointers and parents
outside the record refuse. The checker reports the selected candidate pins and
these overrides; it does not rewrite historical files or run implementation tests.

This profile selects the accepted metadata-v2 unit in full, including its semantic
contract, sources, fixtures, reference checker and coverage. Consumers must read
these selected inputs and apply the declared passage overrides when interpreting
the corresponding accepted parents. Base acceptance and product qualification
remain separate. A later contract unit must be newly reviewed and bound; this
single profile does not silently chain unreviewed successors.
