# Complete control body and state design

Status: PROPOSED v3, successor to the frozen v2 package. Author: Codex protocol fixture author. No readiness register
change, permission grant, journal carrier activation, or product qualification is
made by these files. The complete schema is `control-completion.schema.v3.json`;
its version distinguishes this completion from the lead's provisional body
schema, without changing controlProtocolMajor 1.

The accepted authority remains `control-protocol-contract.v2.json`, including
five descriptors, noncanonical UTF-8 JSON control framing, independent direction
sequences, opaque provider bytes, sixteen message types and RF1–RF8. All hello,
helloAck, select and selectAck field names and tuple equality rules remain. This
package supplies the previously incomplete typed body/state details. Security
§7 effect proposals are incorporated conditionally, with the journal repairs in
`security-codex-review.v1.md` SEC-M2/SEC-M5 still required before effect activation.

## Closed carriers

Every frame has exactly `{type,seq,controlMajor,body}`. Sequence starts at 1 in
each direction and cannot wrap. A zero, gap, repeat or over-uint53 sequence is
RF7; numeric lexical forms other than an integer (including `1.0` and `1e0`)
are RF2. Unknown fields anywhere, invalid UTF-8, malformed framing and other
schema violations are RF2. A zero/oversized length refuses from its four-byte
prefix before buffering a body. Pre-helloAck bound is 65,536 bytes; thereafter
the negotiated bound is at least 65,536 and at most 16,777,216 bytes.

| Message | Closed body |
|---|---|
| hello | Existing controlMajor, expectedStableId, admittedManifestDigest, platform, maxControlFrameBytesOffer, subprotocolOffers |
| helloAck | Existing controlMajor, stableId, admittedManifestDigest, maxControlFrameBytes, subprotocolConfirms |
| select / selectAck | Existing role, roleSubprotocol, subprotocolVersion tuple |
| refusal | family; RF1 requires supportedControlMajors; RF6 requires decisionClass PR1–PR9; optional opaque detail |
| ping / pong / health | nonce: nonempty opaque string |
| healthReport | nonce plus ready/busy/stopping status |
| resourceReport | residentBytes, cpuNanoseconds, openHandles: uint53 |
| fault | opaque detail string |
| cancel | reason: user/deadline/supervisor-fault |
| shutdown | reason: normal/cancelled/refused/fault |
| shutdownAck | empty object |
| effectRequest | effectClass HE1/HE2, authorizationRef, operationRef |
| effectResult | requestSeq, decisionSeq, outcomeSeq, commitClass, effectOutcome; optional resultRef |

The table abbreviates wire tokens for readability: the exact schema uses
`RF-1` through `RF-8`, `PR-1` through `PR-9`, and `HE-1` / `HE-2`.
RF1's supported-major array is nonempty, unique and at most sixteen entries.
Other refusal families cannot volunteer it. Only RF6 can carry decisionClass,
and RF6 must carry exactly one allowed decisionClass. A refusal is terminal,
never an effect outcome and never a sixth capability function.

Nonce is deliberately an opaque string, not an arithmetic counter. This choice
preserves the retained protocol fixture bytes; accepted control major1 did not
assign a nonce type. Pong and healthReport must match their outstanding request
nonce exactly. A nonce is not an identity, grant, provider fact, or semantic
sequence. These reports are lawful only in their state/direction windows.

Every string must be representable as UTF-8. Free diagnostic/detail/reference
strings have a 1,024 UTF-8-byte bound; nonce and role/subprotocol labels have a
128 UTF-8-byte bound. JSON Schema `maxLength` is insufficient: the reference
checker separately checks encoded UTF-8 byte length, including non-ASCII exact
and one-over cases. Empty fault/refusal detail is allowed. References and nonce
are nonempty. The bounds are protocol input constants, not latency or workload
claims: owner is Protocol + operability; workload is each retained field at and
one byte over its bound on all four platforms; acceptance is exact acceptance or
RF2 as specified. No normalization, locale comparison or identity from control
bytes is permitted.

## Effect courier join

HE1 names host-staged SC-OPS/SC-CACHE writes; HE2 names brokered project reads.
Unknown classes are RF2. Authorization and operation references are opaque
bounded envelopes here: the permission/journal owner must validate their actual
locator grammar, exact operation/component/generation/platform binding, current
consent and ordered grant records. These strings do not borrow parked DR-006
Run identities, and the checker does not invent a grant-journal schema.

An accepted effectRequest is only a courier event. It does not prove an effect
occurred. External authorization evidence is a reference-checker test seam,
representing the separate host decision. An unauthorized request yields RF6
with the exact PR decision supplied by that owner; the model does not reinterpret
PR classes as exits. The binding-mismatch fixture's PR4 comes from an explicit
external scope decision, not from guessing the meaning of an opaque reference.
The PR6 wire-format case establishes only that the closed vocabulary can carry
it; it does not settle the pending preview confinement-trigger decision.

EffectResult is sent only for an accepted broker request. It names that request's
component-to-host control sequence, the grant journal's RA decision sequence and
RCO/ICO outcome sequence. Both journal sequences are positive uint53; outcomeSeq
must exceed decisionSeq. They are distinct from control seq. Commit class is
REVERSIBLE or IRREVERSIBLE as determined by the journal owner; HE2 cannot claim
IRREVERSIBLE. Outcomes are COMPLETED, FAILED or INDETERMINATE. The doctor-host-act
value DEFINITELY_NOT_PERFORMED and disclosure COMPLETED-BEFORE-REVOCATION are not
wire outcome values. A permission denial is RF6, never an effectResult.

The host supplies a pending-request/outcome record for correlation. Unknown or
mismatched requestSeq, decisionSeq, outcomeSeq, class or outcome is RF7 as a
state/correlation violation. This is not a second permission engine or a claim
that merely matching sequence numbers proves durable execution. Journal proofs,
crash recovery and current authorization must be accepted separately. An outcome
that cannot be delivered after teardown remains the journal owner's durable
record; no channel is reopened or renegotiated to deliver it.

## State and refusal precedence

The complete matrix has every sixteen-message × eight-state × two-direction
cell, 256 cases. The schema closes structure first. Wrong-direction known frames
then receive RF7. On the lawful direction, second hello and steady re-selection
receive the specific RF8 replay class. Other wrong-window/sequence/correlation
violations are RF7. Unauthorized host effects are RF6 with PR detail. Under the completed closed
preview schema, RF5 has no locally generated trigger. The separately frozen
`control-completion.rf5-proof.v2.json` maps all sixteen messages to permitted
functions and both HE classes to broker operations. Unknown semantic fields or
action enums fail RF2, wrong-direction attempts RF7, and operation references
outside the separately authorized broker scope RF6. Opaque prose is never
classified as a semantic act. This explicitly supersedes the earlier reachable
RF5 interpretation for preview while preserving the universal ban and the RF5
refusal vocabulary for future reviewed extensions. No Boolean semantic oracle
is used. A received RF5 refusal remains recognizable and terminal.

There are two source-mandated specific classifications: a string-valued wrong
stableId/digest echo, including digest case or truncation, is RF3 as accepted
CC10 requires; and zero/overflow control seq is RF7 as the accepted sequencing
rule requires. Other simultaneous structural faults still win RF2. The model
preserves this distinction by validating other fields before comparing identity
values; it never accepts an invalid identity value.

| State | Receivable types, on their lawful directions |
|---|---|
| AWAIT-HELLO | hello, refusal |
| AWAIT-HELLO-ACK | helloAck, refusal |
| AWAIT-SELECT | select, shutdown, refusal |
| AWAIT-SELECT-ACK | selectAck, refusal |
| STEADY | ping, pong, health, healthReport, resourceReport, fault, cancel, shutdown, effectRequest, effectResult, refusal |
| TEARDOWN | shutdownAck, refusal |
| CLOSED | none; received frames are RF7 |
| FAULTED | refusal from a still-readable opposite direction only |

FAULTED does not restart the violating direction, which is already stopped.
Receiving refusal from the remaining readable direction records the counterpart's
terminal event and continues the same one-way teardown; it does not create a
new session. Once both directions are closed, every new frame is RF7.

For an unsupported-major hello, the frozen envelope permits direction, sequence, state and replay
checks before selecting RF1, and the receiver never validates its unknown body
schema. The body must still be an object under the frozen envelope; syntactically
invalid JSON cannot be accepted. A future body may contain fields/numeric forms
unknown to major1. RF1 is emitted with controlMajor equal to the offered major,
which is an echo under the frozen refusal core, not a claim that the receiver
implements it. Its supportedControlMajors reports actual support. The awaiting
sender accepts this frozen refusal at the offered major and tears down; it does
not downgrade. A concrete major2/receiver1 vector covers this exchange.

## Existing corpus integration

`control-completion.protocol-join.v3.json` names exact old/new corpus hashes and
212 old case replacements. It replaces the provisional 208-cell thirteen-message
matrix with this complete matrix; corrects the old wrong-direction selectAck
replay witness; and replaces three provisional generic effect/cancel payloads
with the closed HE/enum outcomes. These old files remain frozen review history.
The new schema makes their legacy unknown action tokens RF2, while new denied-authorization cases retain RF6. RF5 local reachability is
explicitly disposed by the closed-preview proof, not fabricated by an oracle.
Activating both contradictory old and new expectations is forbidden.

All other old protocol cases retain their existing scope, including exact
provider framing, data-plane nontranslation, event ordering, atomicity, and the
paired benign-fault/smuggling-fault full semantic snapshot. This joined active
selection contains 9,768 cases. Corpus size is finite evidence, not a universal
proof of all streams or all scheduler behavior.

## Replay and limits

`control-completion.check.v3.py` exercises the actual JSON decoder, closed schema,
UTF-8 byte bounds and reference state/correlation checks. With Python3.12 and
jsonschema4.25.1:

```
python docs/coop/completion/control-completion.check.v3.py --report /tmp/control-review.json
```

The retained report is 448/448 PASS over 444 cases, two accepted source pins,
the complete matrix check and the RF5 reachability check. It captures exact checker/schema/corpus hashes.
All v1/v2 files remain frozen history. Platform aliases remain macOS arm64/x86_64 and Linux arm64/x86_64. No shipping
host was executed and no OS is reported qualified. The external security and
journal proofs remain explicit activation dependencies, especially SEC-M2/M5.

## Resource-safe parser repair and actual preview witness

CTRL-M1 is repaired by parsing JSON with an explicit container stack bounded by
the already bounded frame bytes. Nesting no longer consumes the Python call
stack. Integer lexemes longer than sixteen digits remain lexical tokens; they
are never converted through Python's configurable decimal-digit limit. A
positive oversized envelope seq is RF7; an oversized controlMajor or known
body integer is RF2. Five exact retained probes cover 1,500 nested containers
and 5,000-digit integers, including a future-major deeply nested body that
remains opaque to major1 validation and selects RF1 after frozen envelope checks.
Known-major schemas have fixed shallow bodies; a validator diagnostic recursion
is caught and becomes RF2. This is reference-parser behavior, not evidence of
shipping core survival or OS process isolation.

The generic state matrix's semantic-provider role is a synthetic, non-shipping
control transport tuple. Four additional accepted frames retain an actual
preview handshake using role analyzer, roleSubprotocol typescript and version1.
This package does not add a manifest role token.
