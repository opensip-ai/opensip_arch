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

Candidate02 retains the accepted carrier bodies unchanged and adds four permanent test groups (82 total). A conservative recursive guard now refuses differing sibling inline property schemas that still lack distinct titles, including arrays, enums, constrained strings and nested unions. It also refuses new private titles shadowing existing definition/title names. This is the identified alias class, not a proof of arbitrary Typify name allocation. All current587 roots pass unchanged. The runtime regression executes 44 UTF8-boundary checks plus six exact malformed-bound refusals and three scalar/surrogate checks; it compiles the current runtime template in scratch. Node and the selected TypeScript compiler are required, never silently skipped.

The first full-suite root invocation omitted Python -I and eight execution tests refused at that required guard; the correct -I -B invocation passes all82. An earlier root malformed-bound probe omitted $schema and therefore proved only dialect refusal; independent review01's later ts-direct-probe.json did exercise correct bounds. The new in-tree checks supply the dialect and assert the exact x-maxUtf8Bytes error. Both prior evidence and this correction are retained. Source-preflight-refusal.json now records exit/stderr instead of an empty redirected file. The initial candidate02 compiler link outside its workspace was correctly refused; exact140pinned compiler files were copied into its own tooling workspace, then generation succeeded.
