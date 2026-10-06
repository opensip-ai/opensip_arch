# FX-CAP-1 coordinated request capacity

Status: proposed exact contract successor; owner direction selected, independent acceptance pending.

## Selected change

The current closed request and Plan shapes remain. `analysis-spec.requestedCapabilities.maxItems` becomes **11264**, and `plan.nativeContextDigests.maxItems` becomes **1024**. The per-step `CapabilityAvailabilityStepV1.notices.maxItems` becomes **11264** in both workflow common schema versions, preserving one notice per selected row without truncation. No other schema maximum changes. The matrix at this successor's parent has at most eleven selected capabilities per language program unit; 1024 × 11 = 11264. A TypeScript and a Rust unit in the same marker directory count as two language program units for this sizing target, while the scope descriptor still deduplicates roots as before.

This supplies cardinality expressibility for complete defaults over up to 1024 selected units. It does not add an upper bound of 1024 units where no such bound existed, promise all inputs with that many units fit, raise file/path/byte/work limits, qualify performance, or admit previously unregistered capabilities. The original 1024-root bound, 4096 discovery-unit bound, 128 semantic-closure bound, 256 Plan-import bound, all producer and protocol bounds, and canonical record 4 MiB bound remain. A later matrix extension must reassess the full-default target and change this bound by an explicit successor if needed.

Unit and context counts are independent: identical admitted context identities deduplicate; up to 1024 distinct contexts become expressible. Context identities, retention and compiler/source admission rules do not change. More than 1024 contexts refuses at the existing native producer boundary; the prospective Plan repeats the check. No allocation based on an unadmitted count is authorized.

## Refusal and algorithm

At externally supplied or defaulted analysis-spec admission, check actual-array cardinality against 11264 first, then complete schema shape, then the closed capability vocabulary and ownership tuples. A non-array, absent member or wrong type goes to shape validation unchanged. At context production check the distinct admitted context set against 1024. At prospective Plan admission keep declaration-order tie breaking: semanticClosures, nativeContextDigests, importIds. A crossing keeps the original `REQUEST.UNSATISFIABLE`, exit 2, public detail `PROJECT.SCOPE_LIMIT` and `field:count>limit` subject. Neither boundary truncates, silently drops a capability or root, shards the invocation, or creates a Plan or Run for a refused step.

The context limit is a count of admitted, deduplicated identities, not inferred compiler processes. Requests that fit cardinality still undergo every byte, dependency, stage, frame, work and storage check. Their existing origin-dependent refusal and fault rules remain. In particular a malformed over-bound externally retained record follows its schema/retention route, not the caller-remedy route for a prospective request. Earlier committed invocation steps and operational attribution are preserved on later refusal.

## Identity and retained compatibility

This is a narrowly scoped reviewed exception to the identity major rule: four numeric maxima increase (two identity fields and the notice array in two common-schema versions), under the existing majors, without changing any field, identifier domain, canonicalization, uniqueness, ordering, digest preimage, authority requirement, capability or predicate meaning. All previously admitted records remain within the widened sets and replay with their exact original bytes and identities. No document named directly by a payload-registry row is changed; identity schema bundles and these common-schema dependencies acquire no historical payload reader row. Retained schema-reference closures keep exact dependency bytes, and historical producer closures stay intact. The selected HSR law remains intact.

New readers admit the widened sets after full unchanged semantic checks. Old readers may refuse larger arrays; they never truncate or reinterpret them. No downgraded or narrowed substitute Run is manufactured for an old reader. Changed release implementation uses a new authenticated core/detector closure under existing release identity rules. Compatibility is explicitly forward-readable only where the older reader's original limits already admit the record.

The exact full schema copy supplied with this subject is the effective identity bundle for these two limits. Its remaining HSR-governed major-law annotation carries the same exception. The three complete copies select the four numeric maxima; passage overrides remain text-only. Both per-step availability descriptions explicitly state the new bound and exact noticeCount. The historical invocation description is retained; existing output-byte failure never truncates notices. It is an implementation input for a later materialization unit, not a claim that product schema sources or generated code have changed merely by binding this design subject.

## Implementation and qualification obligations

The lead must update C2-T16's 129-context test to 1025 contexts, retaining the 128/129 cases as successful cardinality controls. The published requested-capability cardinality one-over becomes11265; retain1024/1025 as accepted-cardinality controls. C4-T9 remains the1025-character malformed-string schema refusal. Existing duplicate-tuple, malformed-string, undeclared-mode/capability and retained-origin tests remain. C4-T7's closure/import crossings remain129 and257 respectively; only its context crossing changes. Host internal errors retain their existing illegal-state route.

Add exact-bound and one-over independent fixtures for requested rows and distinct contexts; prove equivalent-context deduplication. Include all-TS, all-Rust and colocated mixed units, cross-unit imports/consumers and one aggregate Coverage population. Cases that cross unchanged canonical bytes, producer stage/key limits or snapshot bounds must keep their original refusal, not claim this successor guarantees success.

Resource qualification measures full cold/warm source snapshots, requests, Plan, codec, context creation, provider stages, fact/Coverage admission, retained replay, cancellation and aggregate process-tree memory. The synthetic request-size spike is sizing evidence only; it qualifies nothing. The implementation lead records the exact workload axes and selected runner limits before claiming a supported 1024-unit performance envelope.

No automatic sharding, new reference-form snapshot, S-R selection, scheduling strategy, plugin execution or interpreter is selected by this successor. Existing S-R/S-B work retains its own review and dependencies. Implementation consumers are host discovery/default admission, context and Plan construction, producer/reference admission, evaluator retained closure, schemas/generator registries and the qualification harness.

## Revision r2

R1 remains frozen and unselected. Grok2 findings FX-CAP-1-RF-01 and RF-02 are addressed: four numeric JSON Pointer overrides are removed; complete copies select those maxima under the major-law and native text authority; both common-schema step descriptions receive exact text overrides. Historical invocation descriptions remain unchanged. NB-03 is addressed by naming C2-T16 and preserving C4-T9. NB-02 is queued for a later historical-reader-aware description revision.
