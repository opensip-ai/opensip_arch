# Complete structural manifest design

Status: PROPOSED, authored by Codex protocol fixture author. This unit completes
machine-readable structural evidence for DR-103 and the metadata half of G15.
It does not change readiness rows, independently approve its own bytes, admit a
component, or qualify a shipping binary. The security, dependency-selection,
canonical-signing and physical packaging units must still join before admission.

## Authority and scope

`component-manifest-schemas.v11.json` is the accepted field/tree/permissions/
typed-absence authority. Its exact bytes, the permission truth tables v9, the
completed version-constraint v2, and Claude's complete security v2 manifest are
pinned in `manifest-cases.completed.v1.json`. The complete schema is
`manifest-schema.completed.v1.json`; the checker is
`check_manifest_completed_v1.py`. The schema uses only local references and
closes every defined object branch. It cannot load a remote schema.

The initial role vocabulary remains exactly `analyzer`. An analyzer with an
empty capabilities array is valid; no auxiliary/build role is invented. Platform
strings remain structurally open as the accepted schema requires. The optional
preview profile separately limits advertised alternatives to the four approved
macOS/Linux arm64/x86_64 pairs. A structurally valid future platform is not a
shipping support claim. Human/JSON/SARIF command advertisements remain structural
vocabulary; applicability and rendering are owned by the host product contracts.

The actual security v2 full manifest passes unchanged, including all five
`typescript.*` capability declarations with closed `{relation,rung}` data:
imports/resolved-target, references/resolved-binding, calls/resolved-callee,
types/checked, and reachability/from-resolved-calls. Reachability requires calls;
capability IDs, permission tokens, and platform alternatives cannot duplicate.
Unknown capability IDs or wrong registered data refuse. Empty capability arrays
remain valid and do not advertise TypeScript analysis support.

## Concrete choices completing prior gaps

The five closed manifest compatibility fields are `manifest`, `hostCore`,
`control`, `providerProtocol`, and `componentState`. `hostCore` uses the completed
v2 exact-SemVer-or-closed-interval language, including its prerelease discipline.
Empty/reversed intervals refuse. The manifest field echoes manifestSchemaVersion.
Other versions remain independent; equality among them is not a schema rule.
The preview profile supports major1 on each active declared surface and host
release0.1.0 in the declared hostCore constraint. Core-state, root, index and lock
metadata dimensions remain in host/lock records; no extra manifest fields are
invented for those records. General schema validity does not negotiate support.

The optional pure-data command option grammar has long flags (`--name`),
description, valueKind string/integer/boolean/path, required repeatable, and an
optional typed default. A repeatable default is an array of the corresponding
scalar type; a nonrepeatable default is that scalar. No parse closures, regex,
short-option bundling or execution hooks are introduced. Positional names are
unique; a variadic argument is last, and a required argument cannot follow an
optional argument. These are explicit concretizations of the previously named
but untyped descriptor members, not claims that older placeholder examples were
already a complete parser contract.

Parent linkage is resolved against command names in this manifest. A referenced
parent name must resolve to exactly one command. Thus an ambiguous parent refuses
instead of choosing an order-dependent parent. Equal child names under distinct
unambiguous parents remain representable. Every chain reaches the sole mounted
root; cycles, unknown parents, duplicate sibling names/aliases and shadowing
refuse. The root must equal manifest.name. Cross-component custody is a supplied
host-context seam: same stableId/provenance coexistence does not collide, while
names belonging to a different pair do. This unit does not implement the
persistent identity ledger or ownership transfer.

ID-DEP-12's previously unowned configuration vocabulary is proposed as two
host-owned tokens: `host.analysis.semantic` and `host.operability.nonsemantic`.
Semantic values enter the existing resolved Plan input semantics. The second
token is allowed only for host-reviewed operability fields. It is not permission
to omit a semantic input, introduce a private precedence layer, derive a new
identity recipe, or activate deferred DR-106. The namespace must equal the
component name; every top-level field is classified, with nested members
inheriting that field's classification. An exact externally supplied host field
map must agree. Manifest bytes cannot approve their own map.

The initial shipped TypeScript field map is EMPTY. Therefore the preview profile
refuses every nonempty component configuration schema, even if a synthetic host
review map would accept it structurally. Nonempty configuration fixtures are
explicitly synthetic, non-shipping design evidence. The closed recursive schema
subset contains object/properties/required/additionalProperties:false,
array/items/minItems/maxItems, string/minLength/maxLength/enum,
integer/minimum/maximum, boolean and null. It has no `$ref`, regex, code or
unsupported extension keywords. Required names must be declared, and reversed
bounds refuse. A future setting requires a host-reviewed mapping change.

The deferred `stateMigration` and `updateData` markers retain their exact accepted
objects and ridesOn arrays. They cannot be replaced by active payloads. No
signature, treeRootDigest, new role or hidden trust field is admitted by the
closed root schema.

## Resource and path rules

The proposed distribution metadata bounds are enforced on real serialized
inputs: 4,194,304 manifest bytes inclusive before parsing, 64 nested JSON
containers including the root, 100,000 entries per array, 100,000 committed tree
entries, 4,096 commands, command depth32 including the mounted root, 64 aliases
per alias array, and 1,024 UTF-8 bytes per path. The byte cap can be the tighter
limit for a large tree; these bounds are simultaneous, not guaranteed attainable
independently. Numeric metadata uses the security profile's signed-64 integer
range, with positive/unsigned field constraints where appropriate; float lexical
forms refuse. This does not change the control channel's independent uint53
sequence limit.

These are admission input constants, not measured latency or performance claims.
Owner: metadata/packaging and host parser. Workload: exact-bound and one-over
serialized fixtures under the four preview platforms, with non-ASCII path pairs,
4MiB padded valid manifests, 4,096/4,097 commands and 64/65-container valid schema
structures. Acceptance: exact-bound parses and passes applicable structural
checks; over-bound refuses before mutation. No shipping platform was run here.
The full tree-count cap also follows from the schema and generic array guard;
no claim of an independently attainable 100,000-entry positive under 4MiB is made.

The parser rejects duplicate keys and retains the duplicated key in the refusal
datum. It checks nesting before invoking the JSON decoder and catches oversized
integer conversion failures. Malformed JSON, surrogate strings, unsupported
numeric forms and closed-schema failures are RJ-6, never Python exceptions or
partial admission. No input is normalized into acceptance.

Every path reference is relative and NFC, with no dot/dot-dot/empty segment,
absolute/drive path, backslash or NUL. Exact and folded path collisions refuse.
Portable reserved basenames and trailing dots/spaces refuse. Each ancestor of a
tree entry must be an explicitly committed directory; symlink targets are
relative to the link's parent, must resolve to a committed entry and may not
escape or cycle. Entrypoints resolve to committed executable files. File, dir,
and symlink branches cannot borrow one another's fields. Declaration and doctor
references use the same path discipline. Path failures are RJ-3.

The reference interpreter reports its Unicode database in the report (15.0.0 in
the retained Python3.12 run). The retained stable-character path corpus is useful
evidence, but is not the production frozen Unicode15.1 table implementation.
That exact-table integration remains a required packaging/security join.

## Typed absence and artifact closure

All six declaration groups are required. Each is exactly a digest reference or
an approved typed-absence object. Typed absence must name an externally approved
exception and match its declared prerequisite's typedAbsenceBehavior. A missing
object or a self-asserted approval is never an exception. Prerequisites retain
ownership, trust, network, expectations, doctor and typed absence/failure fields.
References inside trees and sibling release artifacts are both supported.

The security full manifest is tested for structure and registry consistency;
this checker does not claim its referenced release payloads were supplied. A
separate derived `artifact-closure` base carries retained synthetic bytes for all
file commitments and all six declarations. Blob records are exact hex bytes,
indexed by their measured SHA-256. The checker starts from a retained
path-to-byte custody map, never a supplied digest as an authority to select an
unrelated file. It verifies lengths and hashes, refuses missing artifacts, and
verifies the license artifact's license and notice inventories plus the notice
bytes. Its files are labelled DESIGN-FIXTURE-ONLY and are never executed.

The license inventory lives in the referenced licenses artifact; it is not an
extra unrecognized manifest member. Other declaration payload content and
quality, signatures, trust floors, dependency resolution and OS confinement are
owned by their complete units. A structural/ref-check PASS reports admitted:false.
RJ codes are local refusal families; no D9/exit mapping is invented here.

## Replay and review

```
/tmp/opensip-architecture-review-env/bin/python docs/coop/completion/check_manifest_completed_v1.py --report /tmp/manifest-review.v1.json
```

The retained report is 187/187 PASS: 183 concrete cases plus four exact source
pins. Each case records the exact materialized wire hash/length and its observed
result. Cases include the complete security manifest, empty capabilities,
maximal optional branches, approved exceptions, synthetic artifact closure,
required-member deletions, closed-object mutants, host-map failures,
compatibility disagreement, malformed paths, cycles, reference corruption and
resource bounds. Finite mutation coverage is not exhaustive coverage of all
possible JSON documents. The freeze manifest pins this entire authored unit and
its imported SemVer dependency for independent review; no self-acceptance is
claimed.
