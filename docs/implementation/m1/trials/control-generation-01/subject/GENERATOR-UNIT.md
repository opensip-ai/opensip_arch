# Common-control generation candidate

This extends accepted adapter04 with the exact existing control schema3
(SHA2562929de62e9eb3a3dc78959eaf3d50361b8d1f895d086940724c1c743ac46a98c),
whose source45/application46 route is recorded in control-source-route.v1.json.
There are29 raw schema inputs and587 explicit type roots. Control3Root is emitted
in Rust protocol.rs and the TS provider protocol.ts. The current broad report
trial retains all selected roots; final report consumer narrowing remains due.
No transport/state/authorization implementation or native TS2/Rust3 IDL is added.

The control owner uses x-maxUtf8Bytes. The TS runtime now recognizes this one
nonnegative-integer constraint and enforces UTF8 byte length independently of
Unicode scalar maxLength. No regex profile change is needed. Rust remains an
inert carrier: UTF8 bounds, framing, sequence, state, correlation and effects
must be admitted by components/control_protocol.rs and provider counterparts.

The first Rust trial exposed a Typify inline-object naming collision: all16
message variants used the hello body type, rejecting73 of79 positive witnesses.
prepare.py now assigns distinct private titles to conflicting direct object
properties of a named oneOf, using stable variant/property positions. Only
Control3Root has such a collision in the selected587 roots. This changes no
schema ID, wire field, discriminator or authoritative record. Original schema
bytes remain untouched.79 positive frames across all16 variants now roundtrip
exactly in Rust.194 positive/negative schema+UTF8 cases match an independent
Python reference; malformed bounds refuse. Strict TS compilation and all78
existing adapter/build/dependency/binding tests pass. The initial failing trial
is retained honestly. Fresh generation and byte drift are checked separately.

Candidate only. Actual independent review, final native/report source closure,
complete output-consumer selection, reviewed inventory/integration binding,
OS/transport/runtime and release qualification remain. Parent/OS/native runtime
trust and adapter04's confinement/build limitations still apply unchanged.

The current live source preflight refuses the added control path: its existing
accepted route is nested under the historical architecture application, rather
than a direct row in the source45/application46 overlay or a selected contract
candidate. This is an explicit integration obligation. Promote the exact existing
control schema through a reviewed source-selection unit; do not weaken the
verifier or rewrite the historical schema. The other28 schema sources verify.
The nested accepted route and its8 original frozen files remain independently
verifiable through control-source-route.v1.json.
