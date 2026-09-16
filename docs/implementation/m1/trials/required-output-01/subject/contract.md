# Required finite-command output, candidate01

Root proposal for L02; not selected, independently reviewed or product code.
The inherited report/interruption owners remain unchanged in `owner/`. This
candidate specifies the final required machine-output operation after those
owners have produced their aggregate. It does not change their step ordering,
cancellation choices, availability rows, recorded errors or committed Runs.

## Complete output or explicit operational failure

The selected CommandEnvelope codec remains 4 MiB. A command is not guaranteed
to produce a normal envelope for every otherwise admissible repository or
invocation. If its complete required envelope cannot be represented by the
selected codec, the final required output operation fails with the existing
OUTPUT.SERIALIZATION_FAILED / operational-failed / exit4 law. No selection,
availability notice, error, Run reference or other required member may be
removed to manufacture a smaller successful envelope. No current-checkout
query, reanalysis or newer Run may substitute for unavailable historical data.

The host admits the complete envelope against its selected schema and all
semantic joins, encodes it with the selected exact-number codec and enforces
that codec's byte/depth/value bounds before writing any of its bytes to the
required output channel. The codec must enforce its resource bounds during
encoding; an unbounded allocation followed by a length check is not a product
implementation of this rule. This reference delegates admission and bounded
encoding to a trusted callback, then independently checks returned bytes and
the cap. It does not implement that codec or prove full native Run admission.

This is an explicit capacity-failure policy, rather than a larger profile or a
selection preflight policy. Actual independent review must decide whether this
policy satisfies the intended product experience and L02 obligation. The
original capacity audit's stronger prevention/representation alternatives are
not claimed to have been implemented. Large lawful invocations can fail output
after committing useful work under this proposal. L01 retained InvocationRecord
capacity is a different obligation and remains open.

## Two terminations with different owners

The invocation aggregate records completed/cancelled steps. The process finalizer
also owns required output. On complete admitted output and successful required
write/flush, process termination is exactly the aggregate. This includes an
interrupted aggregate with exit130 and its optional earlier committed Run.

If the required envelope operation fails, the finalizer applies the existing
D9 v1.14 `machine-output-serialization-failed` axes to that failing operation
alone. The axis `interruption=none` describes the output failure, not a denial
of a recorded earlier signal. The resulting process class is operational-failed
and its code OUTPUT.SERIALIZATION_FAILED, even if the preserved invocation
aggregate was interrupted. The earlier cancellation, all step terminations and
every committed Run remain unchanged. This ordering is a proposed explicit
composition rule; the old D9 golden alone did not test interrupted composition.

Failure to serialize, enforce the selected envelope codec, or write/flush the
normal machine envelope all use this existing output-serialization golden.
Required renderer failures remain owned by the report's render step and existing
DELIVERY.REQUIRED_FAILED law. They are aggregated before this operation; this
candidate does not relabel them or alter optional-render behavior. If delivery
of their resulting failure envelope also fails, that later output failure owns
the process termination. No new D9 class, map entry or public detail is added.

The finalizer has one commit and one process-exit write site. Required output
completion or its fault must be known before that commit. Signals and optional
delivery faults after that point remain metadata and cannot cause a second
commit or reclassification. Live signal observation and arbitration before the
commit remain implementation duties; this reference starts with the aggregate
already admitted by its owner. It is not a live signal-race qualification.

## Stream and file behavior

Before-emission admission/encoding/capacity failure emits no normal stdout
envelope. A best-effort fixed ASCII diagnostic on stderr names the existing
error code. It contains no caller string, path, exception text or uncommitted
candidate identity. Failure to write that diagnostic neither retries the
normal document nor changes the process class. stderr may itself contain only
a prefix if it fails.

A stream write or flush may fail after exposing a prefix or even all envelope
bytes. A host cannot retract those bytes or claim atomic stdout. It must not
append a second fallback envelope to the same stream. The process still exits4;
consumers must require successful delivery termination as well as an admitted
complete document before claiming delivery success. A partial stream is not an
alternate valid CommandEnvelope. A complete document followed by flush failure
can name the earlier aggregate while the process reports the output fault.

For a file destination the required delivery adapter must stage the complete
document, perform its required durability operations and publish according to
the selected platform contract. This reference does not implement file atomicity,
fsync, rename, old-target preservation or crash recovery. A failure after visible
publication must not be falsely described as if no bytes became visible.

## Prospective owner integration

Apply the following clarification to D9 `invariant-envelope-parity` in an
explicit successor, with exact parent binding and actual review: for finite CLI
commands, the normal CommandEnvelope termination equals process termination
when its admission/serialization and required delivery complete successfully.
If required output fails, D9's failing-output operation governs process exit;
the host may have exposed partial or complete earlier envelope bytes and must
not fabricate an atomicity guarantee. Preserve all class maps and existing
goldens. Rebase the checker’s successor-equality expectation explicitly; never
edit accepted v1.14 in place or assert its old checker accepts changed prose.

Bind this rule into report/interruption delivery and the CLI host finalizer,
including interruption07's sentence that recording/delivery retains its own
operational fault law. Envelope availability remains an exact invocation-owned
account when an envelope is delivered; this proposal grants no truncation
exception. Report document and HTML limits remain distinct from the envelope
codec; each complete required artifact must pass its own owner before emission.
Integrate the real private RequestContext, admitted aggregate, codec, renderer,
I/O adapters and exit site. Regenerate and review the final source closure.

## Evidence boundary

The checker imports the unchanged 27-file D9 authority closure under Python
`-I -B`, reproduces its full base check, and derives the output fault from its
real class/code functions. It uses the unchanged report08 aggregation and
renderer functions for synthetic step records. Fake writer/codec faults test
composition and disclosure; they are not native selection or live-process
proof. Its byte-boundary fixtures are bytes supplied by a trusted stand-in,
not full admitted maximum-size Runs. Actual codec, process, file/pipe failures,
signals and platform recovery remain required integration tests.
