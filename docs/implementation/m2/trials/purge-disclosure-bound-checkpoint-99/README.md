# Purge disclosure representation finding 99

Standing: reproduced contract/reference boundary gap; proposed correction, awaiting actual independent review. No selected design or product source was changed.

The workflow contract allows 4,096 active pins per Run, with names of up to 256 Unicode scalar characters, and says these limits keep the complete refusal representable. The required failure envelope repeats the full disclosure in termination.domainDetail and errors[0]. Product canonical JSON has a 4,194,304-byte limit.

The current evaluator3 disclosure and command-envelope schemas accept every following complete inventory (unique sorted names, each four ASCII hex characters plus 252 repeated characters):

| Repeated character | Complete disclosure bytes | Complete required envelope bytes | Product encoding |
| --- | ---: | ---: | --- |
| ASCII x | 1,175,752 | 2,352,308 | Admitted |
| é (two UTF-8 bytes) | 2,207,944 | 4,416,692 | BYTE_LIMIT |
| 😀 (four UTF-8 bytes) | 4,272,328 | 8,545,460 | BYTE_LIMIT |
| U+0001 (six-byte JSON escape) | 6,336,712 | 12,674,228 | BYTE_LIMIT |

The important failure already occurs with ordinary non-ASCII text; it does not depend on control characters. Name scalar limits and pin count alone cannot guarantee a complete representable refusal. Truncating pins or silently changing the requested refusal into a generic serialization failure would violate the complete-inventory obligation.

`observations-r2.json` records actual selected schema validation and actual product canonicalizer results. Source bytes are pinned and were compared with current architecture owners. The current-major envelope was constructed explicitly from the required owner shape; this is not a claim that the inherited historical helper executes evaluator3. The initial `observations.json` used that inherited helper with a run3 ID and got CONFIG.INVALID before reaching size validation. That unsuccessful probe and its script are preserved and excluded from the finding's evidence.

## Proposed correction for review

Add an aggregate serialized-size admission condition before durable creation or modification of a retention pin, in the same protected operation that observes the complete resulting pin set. Preserve the existing name/count maxima and all pins. Calculate the complete required public refusal representation, including BOTH copies of the disclosure, JSON escaping, exact metadata and bounded context overhead. Reject admission before creating an inventory that cannot be disclosed; do not truncate or revoke existing pins as a fallback.

The proposed preflight script demonstrates the boundary for the fixed minimal required current failure envelope and exact existing remedy. At 256 scalars/name, the largest admitted counts in that representation are 4,096 ASCII, 3,889 two-byte, 2,010 four-byte and 1,355 escaped-control names. Each following count within the existing 4,096 maximum exceeds the cap. These observed thresholds are NOT proposed replacement count limits.

Actual reviewers must settle the single owning byte budget, optional/wrapper context accounting, all JSON/human/agent projections, and the precondition/error projection for attempted pin admission. They must also review how a pre-existing over-budget inventory is represented without destructive changes or false completeness. A fixed minimal envelope preflight alone is not claimed to resolve those integration questions. No policy narrowing, wire-schema revision or released defect assertion is made here.

This finding does not invalidate draft 98's separate availability record checks. Pin persistence and purge authorization are still unimplemented, so the defect can be corrected before those product paths are installed.
