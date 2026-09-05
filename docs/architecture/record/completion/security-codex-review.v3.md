# Security turn 3 — independent review

OBJECT: six MUST-FIX, zero SHOULD-FIX. The unit is CONTESTED after its third exchange under D-368. All65 subject hashes match;230/230 checks replay identically except run time. No register edit.

## SEC3-M1 — Root admission boundary

A shape-valid root with kernelAttestationKeys containing one known root key is semantically admitted and its manifest envelope returns VERIFIED. The preview explicitly requires that list empty. In addition, direct verify_envelope admits a root whose five recoveryAuthority entries repeat one key: the schema rejects that shape, but verify_envelope never invokes root-schema validation and admit_root omits recovery-list duplication checks.

Repair: Require preview kernelAttestationKeys=[] at admission (and preferably schema). Make the root admission boundary enforce both closed shape and all semantic list/key rules before signature use, or expose an explicit validated-root type with an enforced precondition; do not let verify_envelope independently label an unvalidated root admitted. Retain exact negatives.

## SEC3-M2 — Policy narrowing

Both raw policies are schema-valid, but global prefix src plus project src/../private or src/../../outside produces effective grants with no refusals. Lexical startswith admits traversal that leaves the globally allowed subtree. This contradicts the project-only-narrows rule. A later effect/path boundary may still refuse the target; this finding does not assert demonstrated product access.

Repair: Validate canonical policy path syntax at source admission and compare normalized, component-delimited paths. Refuse dot/dotdot, absolute/drive/backslash/empty-segment or other forbidden path forms as applicable to the inherited scope grammar; a policy source must not earn a narrowing proof solely from a lexical prefix. Retain both exact traversal negatives and legal descendant/prefix-sibling controls.

## SEC3-M3 — Witness reconciliation

The recovery helper returns OK for COMMITTED seq:true at tail1, REVERT for PENDING2 with no bodySha256 at tail1, and ADVANCE for PENDING0 with empty journal. These malformed state records bypass the promised quarantine branch. Recognizing only the literal MALFORMED sentinel does not validate a supplied witness dictionary.

Repair: Define and validate the closed witness shape before comparing it with a verified tail: strict integer generation/sequence ranges, no bool, legal state, required carrier identity/hash and state-specific genesis/PENDING constraints. Invalid witness bytes/fields must map to quarantine; only a valid witness can authorize REVERT/ADVANCE. Preserve legal INIT/OK/REVERT/ADVANCE and lost-tail controls.

## SEC3-M4 — Broker and courier admission require their context

The executable guards skip mandatory checks when context is absent. HE2 accepts missing snapshot membership and missing scope.snapshotDigest. An empty broker grant scope still admits. resolve_result(ref, callback) returns bytes without a carrying successful response, request correlation, scratch custody or file stat; a trailing-newline rr spelling also returns OK. The normative contract promises these checks before delivery. This is a design-model counterexample, not a claim of exploited production code.

Repair: Make the guard boundary require admitted request/grant/snapshot/courier context; absent or malformed context refuses. Check both broker and underlying scope against the exact prebound operation/target/parameters. Require canonical full-match refs. Retain absent-context and foreign/empty/narrowed-scope negatives, response association and actual byte courier joins. Pure lower-level helpers may remain only if explicitly separated from the enforcing boundary and not scored as admission.

## SEC3-M5 — HE1 durable effect ordering

The concrete HE1 narrative commits the staged host-state bytes and unlinks the stage before saying it appends RA/RCI/RCO. That contradicts durable authorization before effect. The same paragraph has no ICI/ICO path although the paired SDK permits IRREVERSIBLE HE1. The earlier generic inheritance cannot leave two incompatible implementable orders.

Repair: State an explicit ordered HE1 algorithm: validate/admit and durable RA; acquire/check the applicable reversible or irreversible intent boundary before any committed effect; apply from immutable bounded buffer; append matching RCO or ICO after the actual outcome; cleanup and receipt only at the lawful point. Tie the receipt commit id to the correct outcome record for both classes and retain crash/REV cases before/after each actual boundary. Preserve FAILED/INDETERMINATE semantics and do not infer not-performed solely from missing outcome.

## SEC3-M6 — Linux release profile versus preserved qualification fleet

Both Linux templates hard-code kernelSeries 6.8.0-generic and linux-image-6.8.0-*-generic rather than a release-measured field, while the preserved ubuntu-24.04 fleet currently publishes kernel6.17.0-1022-azure (image20260823.283.1). Release measurement currently fills keys/boot form/version but cannot replace these fixed identity members under the stated scheme. Thus WA7 is not fully resolved: the required runner cannot match that fixed profile.

Repair: Specify how the supported Ubuntu publisher/flavor/series baseline is acquired and qualified per actual D102 class. Make example6.8generic explicitly illustrative where appropriate and bind measured release profiles to actual class kernel package/series/flavor without weakening publisher/OS/identity checks. Include a non-6.8 Azure-class example and wrong-series negative. Do not change the four-class fleet merely to fit an illustrative profile.

The fleet observation is from the [official Ubuntu24.04 runner inventory](https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md), observed2026-09-04. Exact helper counterexamples and source custody are retained in the JSON review and its pinned assist/probe reports. Production execution is not claimed.
