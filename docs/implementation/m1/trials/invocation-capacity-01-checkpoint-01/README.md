# Invocation capacity investigation01 — unaccepted

L01 needs an explicit rule for the complete operational InvocationRecord. The
existing descriptor profile is4MiB/depth32; the report's separate profile does
not select an invocation profile. The identity contract's descriptor wording
and the logical workflow record must be joined explicitly by their owners.

A concrete reference counterexample now narrows the decision. A2,954-byte plan
with16 synthetic doctor steps completes the pinned workflow replay. The largest
StepResult is276,171 bytes and every child passes the exact default codec. The
complete invocation5 record is4,421,772 bytes: its schema passes, while the
selected exact codec refuses BYTE_LIMIT. The generated TypeScript report consumer
also rejects it as a report. Parsing JSON with a larger codec grants no record
admission. These observations do not demonstrate an admitted workflow profile,
an authentic doctor observation, retention, a public command, or a product bug.

The pinned structural estimator cannot establish a finite whole-record bound.
That is a limitation of this estimator, not proof that the schema permits
unbounded records: for example it cannot count escaped literal dots in the
fixed InstallationTransitionJournalRef pattern. Recursive query/policy material
also needs its actual owner codec boundaries. Do not convert that result into
an invented universal maximum.

The proposed direction for review is to separate the logical invocation view
from its retention representation and from each public materialization. Preserve
exact immutable planned-step, attempt and terminal-result records with explicit
source bindings; stream a complete aggregate where selected. Keep identity and
embedded owner codec profiles unchanged. Introduce no persistent evidence-ledger
writes for read-only or ephemeral invocations. This direction is not an adopted
storage schema, public API or product implementation.

A conditional calculation shows the cost of simply composing child caps: if each
complete StepSpec, StepResult and root termination is independently bounded by
4MiB/depth32,64 steps give a conservative aggregate bound of541,093,629 bytes and
34 container levels. This is over516MiB, not a sensible default whole-memory
allocation. It is also not a proved reachable maximum or selected profile. The
complete child-boundary premise is itself an owner decision and must address
post-effect recording failures. This calculation supports evaluating streaming
and separately bounded views; it does not silently raise a public limit.

The owner decision must state:

1. Whether complete invocations are serialized/admitted as descriptors or as a
   distinct bounded operational format, and which exact versions it covers.
2. Which private records are retained in durable, read-only and ephemeral modes;
   how they are bound to RequestId/StepId/ExecutionId and restored after failure.
3. Where every byte/depth limit is enforced, including nested owners and the
   whole aggregate; how capacity is secured before effects and earlier committed
   outcomes survive any later record/output failure.
4. Whether a full-record view is required, its streaming/materialization policy,
   and its interaction with L02's required-output precedence.
5. What this implies for the report-at-render ledger bound, including a renewed
   derivation and eventual maximum-document measurement. A finalized invocation
   is not the same object as the report's in-progress-render ledger.

Current report bounds remain conservative and unchanged. L01 remains open;
this investigation provides evidence and a review proposal, not an owner verdict.
Actual Claude must assess the proposed retention direction, the child-boundary
premise and any source changes before the final implementation binding.

Run inspect_bounds.py, check_record_composition.py, check_current_boundary.cjs
and derive_segmented_envelope.py with the pinned current joint/generator/codec
inputs. The first check attempted a nonexistent helper; its source and failure
are preserved. The corrected check uses the actual exact canonicalizer and
requires the specific BYTE_LIMIT refusal. The large JSON fixture is a synthetic
reference output, never an admitted retained invocation.
