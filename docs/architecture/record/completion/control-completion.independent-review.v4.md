# Independent control repair review v4

**OBJECT — CCR-1 is repaired, but the repair introduces one narrow identity-validation regression.** External replay passes **457/457**; all eight subject pins remain unchanged. Exact hashes and three v3/v4 comparison probes are in [the review JSON](control-completion.independent-review.v4.json).

## CCR4-1

validation_value is also the copy whose string stableId/digest fields were replaced with trusted context identities for specific RF3 comparison. Passing that copy to utf8_bounds now skips UTF8 representability and byte-cap validation of the original identity strings. A hello with escaped lone-surrogate expectedStableId, or 1025-byte stableId/digest, changed from RF2 under v3 to RF3 under v4.

**Required repair:** Run UTF8 checks over a copy of the original parsed frame with only seq replaced by the valid sentinel when needed. Keep original identity/digest strings for the byte/encoding validation walk; continue using context substitution only for the intended schema comparison exception. Add hello and helloAck surrogate/overlong identity cases including a combined sequence-fault variant.

Narrow refusal-family regression; both families remain terminal. No accepted malformed frame or permission escalation is claimed.

The stateful stopped-direction trace addresses the earlier SHOULD. Final security/journal activation and qualification remain separate. No subject/register change or automatic acceptance/SATISFIED is asserted.
