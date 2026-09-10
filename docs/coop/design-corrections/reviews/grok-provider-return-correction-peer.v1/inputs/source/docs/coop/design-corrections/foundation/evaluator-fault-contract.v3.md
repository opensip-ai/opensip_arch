# Evaluator3 fault boundaries

An internal refusal is not itself a public D9 code. The host retains the originating boundary and applies the public route for that boundary. It does not infer origin from a filename, a retained-versus-live flag or a prefix in the error text. The closed condition/origin routes are in evaluator-fault-observation.schema.v3.json. The reference evaluator_fault_model.v3.py validates actual StepTermination and command-envelope3 owners; check-evaluator-faults.v3.py exercises all routes and envelope parity.

The same reference admission can be invoked over newly returned producer data or retained data. Re-admitting retained producer data preserves the producer-contract meaning of a structural violation. A known external configuration remains external configuration. A host bug constructing its own internal layer is a host invariant fault, as in the inherited native public-route law.

| Condition | Public meaning |
| --- | --- |
| Malformed external policy, emission selection or configuration | request-rejected, CONFIG.INVALID, existing CONFIG.INVALID detail |
| Well-formed prospective selection above a published limit | request-rejected, REQUEST.UNSATISFIABLE; exact field/count/limit and narrowing remedy, before any Plan is minted |
| Invalid host-generated internal layer | operational-failed, SYSTEM.OUTCOME.ILLEGAL_STATE, host-invariant, existing HOST.INVARIANT_VIOLATED envelope detail |
| Provider omits a required inventory/result pointer, supplies a malformed outcome, or violates its Plan/stage/subject joins | operational-failed, PROVIDER.PROTOCOL_VIOLATION, provider-protocol; structural producer violation, including re-derivation over retained producer inputs |
| Referenced promised retained bytes are lost | the existing EvidenceUnavailable carrier: operational-failed, HOST.IO_FAILURE, host-io, evidence.missing plus the missing reference |
| Supplied bytes fail schema/identity admission | admission refusal under their actual external or producer boundary; never silently converted into a missing-byte observation |
| Complete semantic replay disagrees with an otherwise admitted sealed result | evidence.regeneration-mismatch under the retained regeneration boundary; a live first-party evaluator contradicting its own reconstruction is a host invariant fault |
| A complete output cannot fit the published array or canonical-byte bound | operational-failed, OUTPUT.SERIALIZATION_FAILED, output-serialization, EVALUATION.OUTPUT_BOUND_EXCEEDED; no truncated or empty substitute Run |

A valid partial/unavailable inventory, missing optional evidence, unknown native sufficiency or bounded execution exhaustion is semantic evidence. It is retained as typed deficiencies and participates in the specified rule/execution aggregation. It is not malformed producer output merely because its value is indeterminate. A source manifest that fails parsing uses the enumeration-local source-syntax-invalid deficiency; it does not extend NativeCause or pretend the provider crashed.

Pointer omission, promised-byte loss and supplied-byte invalidity are separate observations with different remedies. The adapter must preserve the typed upstream decision list and relevant reference, rather than flattening every refusal to HOST.IO_FAILURE or accepting an arbitrary public-detail string. Existing D9 class/error/exit mappings remain in force. The mandatory LIVE D9 successor-artifact obligation is not discharged by this design reference or by a passing route-control suite.

## Typed observation, custody and public projection

A host boundary records exactly one closed condition and its actual origin. The
record names the raw SHA-256 of the unmodified owner diagnostic artifact and a
relevant reference (required for pointer omission, promised loss and replay mismatch). The adapter checks the artifact bytes and retains
the entire observation. It does not parse exception text to establish origin,
discard nested owner decisions, or rename NativeCause as a public error code.
Re-admission preserves the original producer or external origin. An arbitrary
caller cannot turn a provider failure into a host I/O failure by supplying a
different origin; capture of that origin belongs to the host TCB.

The 24 allowed condition/origin pairs are explicit in the schema registry.
Unsupported pairs refuse JSON Schema admission as well as routing. Valid semantic partial outcomes, ordinary unknown
predicates and exhausted logical analysis budgets are not members of this fault
condition enum. A prospective selection limit and an output serialization bound include the exact field,
observed count and maximum; observed must exceed maximum. The cross-field numeric
comparison is a reference admission rule; standard JSON Schema cannot express
arbitrary sibling integer inequality without a nonstandard extension. The prospective selection refusal precedes Plan construction. Output
serialization failure can follow a Plan but must not mint a substitute Run. Missing promised bytes and omitted required output pointers
require a nonempty reference and have different allowed origins. Both replay
mismatch origins require the affected Run reference; no anonymous regeneration
mismatch is admitted.

EVALUATION.REQUIRED_OUTPUT_OMITTED identifies a missing required provider or host
output pointer on the public surface, retaining its exact reference.
Provider-return TargetAttributionV2 / `ProviderTargetAttributionReturnV2`
refusals use this existing boundary: malformed provider envelope or V2 record
is `input-schema-invalid:provider-return`; join, occupancy-conflict and
ephemeral-identity-conflict refusals are `input-join-invalid:provider-return`.
Both keep public detail `EVALUATION.INPUT_REFUSED`. Host-constructed mapping is
`host-internal` and `HOST.INVARIANT_VIOLATED`. Internal `TARGET_ATTRIBUTION_*`
and `PROVIDER_RETURN_*` keys stay in diagnostic bytes; they are not
DomainDetailCode members and invent no D9 code. Missing envelope is lawful
occupancy-unknown, not `required-output-pointer-omitted`. LIVE D9
successor-artifact remains a future obligation.

EVALUATION.INPUT_REFUSED preserves a structural evaluator input failure with
the exact diagnostic retained separately. EVALUATION.SELECTION_LIMIT names a
well-formed prospective request above the published bound.
EVALUATION.OUTPUT_BOUND_EXCEEDED names serialization failure. These are closed
DomainDetail codes registered in the common public registry; they create no
new D9 error code or exit code. The whole failure envelope carries the same
detail as StepTermination, and its exit code derives from termination.class.
Changing either side or reporting a different class's exit code refuses parity
admission. The earlier native owner may lawfully omit a domain detail; this
evaluator boundary supplies its own specifically registered detail.

The retained-regeneration route agrees with identity's existing
RegenerationMismatch carrier (HOST.IO_FAILURE, host-io,
evidence.regeneration-mismatch). A live host evaluator contradiction is instead
host-invariant. A source failure does not make an admitted Run authoritative:
no failure envelope may replace a missing complete Run with an empty success.

These bounded route controls are reference design evidence. The mandatory
LIVE D9 successor-artifact obligation and platform/host execution checks remain
separate implementation conformance requirements.

## Native origin mapping and owner carriers

The evaluator boundary uses its own closed origin vocabulary. Its schema's
`x-opensip-native-origin-map` explicitly maps the overlapping native boundaries:
external-configuration → external-configuration; external-specification →
externally-supplied-spec; host-internal → host-generated-internal-layer;
release-declaration → authenticated-release-declaration; provider-return →
producer-boundary. The evaluator-only retention, pre-Plan and serialization
origins have no native producer equivalent. Passing evaluator spellings directly
to the native public-route helper is not supported. This mapping preserves
boundary meaning, not equality of evaluator and native diagnostic detail codes.

`owner_observation` accepts a typed retained owner carrier, retains opaque
diagnostic bytes and verifies the entire resulting termination, including
remedy and subject, against that carrier. It neither parses an exception
message nor substitutes a partially matching DomainDetail. The loss and
retained-regeneration routes use the existing identity remedies verbatim.
