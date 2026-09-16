# Typed metadata successor

Candidate for actual Claude review, not an accepted design replacement. This
folder makes the RF-01 proposal concrete while retaining every accepted parent.
The schemas, command inventory, coverage routing and this contract are selected
as one unit. Product implementation must bind their eventual review/assent before
emitting envelope4. The existing planning source-manifest pointer in the coverage
copy remains the base provenance; successor.json supplies this scoped overlay.

CommandEnvelope4 preserves envelope3 payload constraints on the existing branches,
with its own major changed and `meta` forbidden outside `kind=meta`. Metadata
success accepts only schemaFamily, schemaMajor, kind, requestId,
clientCorrelationId, termination, exitCode and meta. Its termination is exactly
`{"class":"success"}` and exitCode0. Failures keep the existing failure carrier,
D9 legality, registered detail and exit-code derivation. No success metadata may
accompany a failure. A major3 reader rejects4, and a major4 reader rejects3.
The evaluator, Run, finding, query and mutation schema identities stay unchanged.

One additional compatibility correction handles ordinary parser refusals. Envelope3
requires a nonempty errors array of registered domain details, yet the registry has
no general unknown-option/topic detail. Envelope4 permits an empty errors array
only when kind=failure, termination is exactly {class:request-rejected,
errorCode:REQUEST.UNKNOWN_OPTION}, exitCode=2, and diagnostics is nonempty. It
cannot carry a run or a metadata success payload. Other empty-error envelopes
remain invalid. Non-applicable format requests continue to carry their existing
OUTPUT.FORMAT_NOT_APPLICABLE detail. No public detail vocabulary or D9 code is
added; a parser error must not masquerade as a configuration or schema failure.

Metadata schema1 has two closed public variants and a private BuildMetadataV1
definition. All schema integer values use the same exact JSON lexical rules as
the accepted foundation. Host releases use SemVer syntax, at most128 Unicode
scalars. Closure IDs use the existing closure2 grammar, at most256 entries in
strict unique UTF-8 order. Development metadata requires an empty list. Release
shape validity alone does not prove assembly admission or qualification.

The help topic is null or a canonical command name; each command row contains
name, usage and summary. Rows are strictly unique by name and UTF-8 sorted.
Semantic admission compares the entire rows to a trusted, build-selected catalogue:
null topic returns the complete catalogue, otherwise exactly its named row. During
implementation that catalogue lists only implemented commands; full product
completion requires all45 selected inventory commands. A known but unimplemented
topic is refused. Aliases resolve to canonical names before projection. Unknown
options/topics use REQUEST.UNKNOWN_OPTION, exit2, and a bounded diagnostic. The
registry has no general command-argument detail: no new detail is invented. The
additional envelope4 correction below makes that existing D9 error deliverable.

Human output renders the same topic, names, usage and summaries. Version output
renders hostRelease, buildChannel and closureIds from the same compiled record.
The fixed declarative metadata selectors are:

| Parity field | Selector |
|---|---|
| command-names | $.meta.commands[*].name |
| host-release | $.meta.hostRelease |
| build-channel | $.meta.buildChannel |
| closure-ids | $.meta.closureIds |

These are fixed selections in the renderer; no arbitrary JSONPath engine is
required. Existing queryDispatch JSON Pointer behavior is unchanged. Completion
remains human-only and shell-specific; an explicit JSON request is the existing
OUTPUT.FORMAT_NOT_APPLICABLE request rejection. Its error delivery follows the
existing command output policy; it does not gain a success metadata variant.

The private build record excludes the host digest/closure, its own digest,
enclosing archives and signing outputs. The accepted planning phrase
"build-embedded signed release descriptor" is corrected within this scope to
"build-embedded metadata covered by the enclosing signed host/release artifact".
Release tooling admits the non-host component closures first, compiles their
selected identities into the host, then the existing release signing/installation
owners bind the finished host bytes. Version describes the shipped selection,
not installed state, current trust, provider health or a fresh signature check.
This introduces no new signature envelope, signatureVerified field or trust path.

M1 must build development metadata from the exact package version with no closure
IDs. There is no environment flag or caller JSON switch to produce a release
channel in M1. Enabling a release path later requires the owning M6 assembly's
actual prerequisite checks and refusal tests. Trusted build selection is an input
to semantic reference checks, not something established by the reference schema.

Bootstrap metadata paths use arguments and compiled constants only. They do not
inspect the project, configuration, providers, store, installation registry,
network or report assets. Operational request/correlation IDs remain metadata.
The bootstrap and delivery still obey existing outcome and I/O failure rules.

check_metadata.py checks exact source pins, schema shapes, compatibility, metadata
semantics and fixtures. It is architecture reference validation. It does not
satisfy future product startup, renderer parity or release qualification tests.
