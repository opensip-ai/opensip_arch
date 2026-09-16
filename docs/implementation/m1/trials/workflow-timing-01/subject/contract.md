# Operational attempt duration owner correction

Root proposal for RP-DO-11; not accepted, not product implementation. This adds
the missing duration owner required by report disposition R03. The successor
invocation:4 is exactly invocation:3 plus required `Attempt.observedDuration`,
its closed definition, and the major/id/title/description change.

## Collection and retention

Only the trusted host observes duration. After it assigns an admitted attempt's
ExecutionId and before beginning that attempt's work, it takes a monotonic clock
sample. It takes the final sample after choosing that attempt's terminal outcome
and before encoding/persisting its terminal Attempt record. It retains the
integer floor of elapsed nanoseconds divided by 1,000,000, in the closed uint64
millisecond domain. Clock origins and wall-clock timestamps are not persisted.
Two samples must come from the same host monotonic clock lifetime. Queueing
before admission, retry backoff between attempts, and writing the final record
are outside this measurement. This is elapsed attempt service time, not CPU
time, benchmark qualification, or an exact end-to-end step duration.

Zero milliseconds is a real measurement of a sub-millisecond or zero interval.
It is never substituted for missing evidence. A missing clock sample yields
`clock-unavailable`, a decreasing pair `clock-regressed`, and an unrepresentable
elapsed millisecond count `duration-overflow`. These observational failures
produce an unavailable duration and do not change the attempt outcome or D9.
Malformed caller types are programming/input-admission errors, not clock states.

Crash recovery assigns an abandoned, previously nonterminal attempt only the
unavailable reason `supervisor-lost`. It cannot subtract its own clock from the
dead supervisor's clock or synthesize a full duration from a heartbeat. Every
abandoned Attempt has this state; no other outcome can use that reason. An
already retained terminal Attempt keeps its recorded duration unchanged.

Every terminal invocation:4 Attempt has the field, including rejected, failed
and cancelled attempts. No field or Attempt is fabricated for a skipped step or
a refusal before an ExecutionId was assigned. Retries retain separate duration
observations under their own ExecutionIds. The existing maximum of three
attempts, retry rules and journal/derivation custody remain unchanged.

These are operational observations attached to RequestId/StepId/ExecutionId.
They never enter a Plan, ExecutionPlan, Run, fact, finding or assessment identity
preimage, and never affect authority, verdict, retry eligibility or dependency
gating. A source-compatible host cannot accept a request/provider/agent supplied
duration as an observation. The pure reference helpers are not custody tokens.

## Historical and report projection

Retained invocation:3 remains under its original schema. Its reader projects
`sourceSchemaMajor:3` and `duration:{state:unavailable,reason:not-retained}`;
this is a disclosed read projection, never a fabricated persisted invocation:4.
The `not-retained` reason is forbidden in newly written invocation:4 Attempts.
For source major4 the report copies the exact admitted observation with source
major4 and the same ExecutionId, joined through the exact selected Invocation
and StepId. It cannot infer duration from another Run or the current clock.
Other source majors are refused until their owner is explicitly selected.

The report shows each attempt's duration independently from its outcome. A step
may additionally show the **sum of retained terminal attempt durations**, clearly
labelled with its attempt count. This sum excludes retry backoff and queueing;
it is not labelled step wall time. If any attempt lacks a measurement, the sum
is unavailable with the missing-attempt count. The individual measured attempts
are still shown. Overflow yields an unavailable sum without truncation. A step
with no attempts says no attempts, never zero duration.

The current report/render step may still be running when its own projection is
built. Such a partial ledger is not a final InvocationRecord. The report marks
that step/attempt in progress and supplies no terminal duration for it; it may
show the immutable terminal observations of earlier attempts. It cannot claim
that the displayed subset is the final step total. Rendering completes before
its final duration is recorded, so the report does not try to contain its own
future final duration. Historical reports can show it from the later retained
terminal record. Cancellation before completion emits no completed document.

## Selection and verification boundary

Admission checks both the schema and the outcome/reason law above. Projection
must join exact source identities and recorded values, not just accept a
self-consistent duration. Durable Attempt custody and actual clock collection
are host implementation work. Report ledger fields, its byte bounds, source
major adapters, browser labels and invocation consumer $refs need a coordinated
reviewed successor before integration. This isolated owner candidate does not
mark RP-DO-11 delivered or waive that work.
