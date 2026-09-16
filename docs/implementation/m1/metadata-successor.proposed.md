# M1 metadata correction — proposal for review

Standing: author proposal responding to plan-review RF-01. Not accepted, not a
replacement for the accepted design, and not implemented. The original envelope3,
command inventory and coverage bytes remain unchanged.

## Problem and selected direction

Help/version require a shared human/JSON projection, but the closed envelope3 has
neither metadata payloads nor parity pointers. Adding fields or a union branch to
that major would change what existing closed consumers accept. Select a new
CommandEnvelope major4, retaining the evaluator3 semantic payload owners. This
is an envelope compatibility change, not an evaluator/Run/finding identity change.

The successor carries forward existing envelope3 payload constraints,
change its own ID and schemaMajor to4, and add exactly one `kind=meta` branch with
one closed `meta` union discriminated by `command` (`help` or `version`). `meta` is
required only on that branch and forbidden on all other branches. Metadata
success forbids project/store/Run/query/mutation/doctor/invocation payloads and
has termination `{class: success}` and exitCode0. Request/correlation IDs retain
their existing types and remain operational metadata. Error delivery uses the
existing failure branch and D9 error/exit rules, without a success metadata payload.

A major3 reader must reject major4; no implicit conversion, discarded fields or
major3 output containing undocumented fields. The new implementation emits the
selected major4 on all JSON commands, and inventory/coverage/renderer selectors
must move together. Old major3 reference evidence retains its historical meaning.
Before acceptance, author the complete closed schema, scoped inventory/coverage
successors, positive and negative fixtures, and a check that the only schema
changes from3 are the reviewed compatibility/meta additions. Pin all exact bytes
and obtain actual Claude review; prose alone does not close RF-01.

## Typed payloads and parity

`HelpMetadataV1` contains exactly `command: help`, `topic` (null for top-level,
otherwise a declared command name), and `commands` (ordered closed rows containing
name, usage and summary). Names come from the build-selected command catalogue,
unique in UTF-8 lexical order; a topic narrows to that declared command. During
partial implementation the catalogue contains only implemented commands; listing
a command does not manufacture its implementation or qualification. At complete
implementation it covers the entire selected public command inventory. Human help
renders these same rows. The `command-names` selector is `meta.commands[*].name`.
Any separately declared command aliases resolve to the same canonical name.

`VersionMetadataV1` contains exactly `command: version`, `hostRelease`,
`buildChannel` (`development` or `release`), and `closureIds` (unique UTF-8 lexical
order). `host-release` selects `meta.hostRelease`, `closure-ids` selects
`meta.closureIds`; buildChannel is a required additional parity field at
`meta.buildChannel`. Human output visibly prints the channel even when a semver
suffix also says development. A development build has an empty closureIds array;
it never emits invented closure2-shaped placeholders. A release build's IDs are
only the non-host component closures explicitly selected by the reviewed release
assembly. These report shipped build selection, not current installed state,
current trust, provider availability or successful execution.

Completion stays human-only. `--format=json` for completion follows the registered
not-applicable refusal. It does not gain a metadata variant implicitly.

## Build metadata, signing and the self-hash cycle

Use a closed private `BuildMetadataV1` record with `schemaVersion:1`, hostRelease,
buildChannel, and closureIds. Field bounds and release-semver grammar must be
specified in its schema before implementation. Build tooling validates the
record and compiles its exact values into the host. The metadata record excludes
its own digest, the host executable's digest/closure ID, enclosing release archive
identity and signing outputs. Those can only be computed after building the host;
embedding them would require an unsatisfiable self-hash cycle.

Correct the planning phrase "build-embedded signed release descriptor" to
"build-embedded metadata covered by the enclosing signed host/release artifact".
This follows the accepted report-asset host-pin trust direction. The release
assembly supplies admitted non-host closure IDs, builds the host containing them,
then binds the completed host bytes through the existing signing/installation
owners. It introduces no new signing scheme, signature-envelope kind or runtime
signature checker. The ordinary host/installation trust boundary remains in force.

M1 emits only `buildChannel=development`, using the exact package version and no
release closure claims. Release assembly must refuse channel release until its
existing manifest/signature and qualification prerequisites actually pass. A
release-channel build cannot be obtained just by setting an ambient environment
flag or by trusting a caller-authored JSON boolean. Implementation must define
that build admission path and test its refusal before enabling release-channel
output; M6 still owns actual qualification. Version never performs a fresh trust
check and carries no `signatureVerified` assertion.

## Startup boundary and required verification

CLI bootstrap supplies arguments and the operational request/correlation IDs to
a pure metadata projection. Help/version read only compiled constants; completion
renders its selected shell script. No repository inspection, configuration load,
provider start, store acquisition, catalog access, network request or report asset
load occurs. Writing requested output remains an ordinary CLI delivery effect.

Review must challenge schema exclusivity, failure/exit parity, channel disclosure,
release assembly provenance, the self-hash exclusion and all parity selectors.
Tests must include forbidden payload mixing, unknown fields/majors, invented
release IDs in development, topic/name ordering, human/JSON parity and startup
with unavailable project/provider/store resources. This proposal does not count
as those tests or as a completed metadata deliverable.

## Concrete candidate

The complete current candidate is [metadata-v1](metadata-v1/README.md). Its schemas,
inventory4, coverage successor and executable reference fixtures supersede this
initial prose where more specific. One additional envelope4 correction is explicit:
generic parser refusals with REQUEST.UNKNOWN_OPTION may carry errors=[] only with
exact request-rejected termination, exit2 and a nonempty diagnostic list. The
registry has no generic CLI detail, and this avoids inventing one. Other empty-error
cases remain refused. Actual acceptance and product implementation are pending.
