"""EDIT 3 (item 1): the owning normative prose states the exact selected law.

The old sentence said the three conditions "each refuse with their own typed reason" without
naming the reasons or saying anything about whether the public carrier could carry them - and it
was, at the time it was written, false in the way that matters: two of those typed reasons named
codes that were in no closed registry, so the carrier refused them. This replaces it with the exact
names, the exact carrier, and the exact meaning of each; and it collapses the third clause, because
a row cited under another schema is NOT a separate reason - the verifier filters rows by schema
digest, so such a row leaves no selected row and meets the same missing-selection refusal.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
DOC = ROOT / 'docs/v2/contracts/product-v1/identity-and-evidence.md'

OLD = """digest. A document that is not selected, a spec that selects no scope parameter,
and a row cited under another schema each refuse with their own typed reason. An
**ambiguous** selection — more than one row citing the registered document — is
refused *before* any payload comparison, on the existing public `CONFIG.INVALID`
carrier and detail: the verifier is existential, so each of two distinct entries
would satisfy it separately, and returning a "verified" digest for one while
another was equally selected would be the false proof this whole section refuses.
No new public detail code is introduced for it.
"""

NEW = """digest.

Each way of failing that proof has its own **named and publicly carriable**
reason, and the two are deliberately not merged. A spec that selects **no**
`ScopeDocumentV1` parameter refuses `REQUEST.PRECONDITION_FAILED` with
`BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`; a row cited under **another** schema is
not a third reason but the same one, because the verifier filters candidate rows
by the registered document digest and such a row leaves none. A spec that selects
**exactly one** row whose `payloadDigest` is not the supplied document's refuses
`REQUEST.PRECONDITION_FAILED` with `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`.
The distinction is what a caller does next: the first says *state a scope
parameter, or stop asking to be bound to a scope policy*, the second says
*supply the document that is already selected*. Both codes are members of the
single closed public detail registry and of the mirrored
`common.schema.json#/$defs/DomainDetailCode`, and therefore of the real carrier
`#/$defs/StepTermination` and of the `errors` array a `kind=failure`
`CommandEnvelope` requires. That is a **registration of two emissions that
already existed**, not a new vocabulary and not a rename: neither refusal's
class, error code, detail spelling, remedy or reachability changes, and before it
the carrier refused both terminations outright, so these two refusals had no
public route at all.

An **ambiguous** selection — more than one row citing the registered document — is
refused *before* any payload comparison, on the existing public `CONFIG.INVALID`
carrier and detail: the verifier is existential, so each of two distinct entries
would satisfy it separately, and returning a "verified" digest for one while
another was equally selected would be the false proof this whole section refuses.
No **new** public detail code is introduced for it, and no third `BASELINE.SCOPE_*`
spelling is created for it.
"""

s = DOC.read_text()
assert s.count(OLD) == 1, s.count(OLD)
DOC.write_text(s.replace(OLD, NEW))
print('prose updated')
