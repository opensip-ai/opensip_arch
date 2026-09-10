# Exact admission and trustworthy qualification reports

Standing: Codex-authored successor; review and application standing is governed
by the [correction record](../../../coop/design-corrections/README.md) and central
readiness register. Addresses AR-01/02 and the G13 join to full-product native
and platform cells. Reference code is design evidence, not production code.

## 1. Numeric and schema admission

The configuration, policy and metadata carriers apply lexical admission before
JSON decoding can round or normalize a number. An integer field accepts an
ordinary integer token in its declared range. `1.0`, `1e0`, `1E0`,
`1.0000000000000001`, `9007199254740991.1`, booleans and numeric strings do not
satisfy an integer field, even if a JSON Schema implementation treats them as
mathematically equal. `-0`, nonfinite tokens and values outside the canonical
profile range are rejected. Internal configuration layers must also enforce
exact types; an already-decoded `1.0` or `True` cannot satisfy `const:1`.

The [canonical reference](../../../coop/design-corrections/foundation/canonical.py)
provides duplicate-key, Unicode, depth, size and number admission plus an exact
integer/const/enum validator. Existing carrier-specific narrower bounds remain.
The new [foundation reference](../../../coop/design-corrections/foundation/host-foundation-model.v2.py)
replaces only the configuration/policy/parser entry points of
`completion/host-foundation-model.v1.py`. Root discovery belongs to the security
successor; no unsafe historical ancestor search is re-exported as current.

Schema validation follows lexical admission and precedes configuration merge,
identity computation, subprocess disclosure or effects. Invalid external input
is an admission rejection with the existing carrier's D9 code; an invalid
host-generated internal layer is a host invariant fault. Unknown keys and
unsupported schema majors are refused. No parse fallback silently narrows a
user's configuration. UR-1–UR-5 are selected explicitly by the canonical profile
in identity-and-evidence §3, with byte vectors for non-BMP key ordering, integer
boundaries, Unicode normalization distinction, escaping and invalid surrogates.

Closed identifier and digest patterns require the actual end of the string.
The product schemas use the portable ECMAScript assertion `(?![\s\S])` where
an end anchor is intended, because `$` can also match before a final newline.
A newline-suffixed identifier or digest is malformed; stripping whitespace is
not an admission repair. Canonical string encoding itself continues to preserve
legal scalar characters, including escaped newlines in ordinary text fields.

### 1.1 Full-product configuration and zero-config defaults

The historical numeric regression adapter deliberately retains the preview's
compiled profile. Full-product configuration instead uses
`foundation/product-configuration.schema.v2.json` and its resolution reference.
It has closed optional sections: analysis (registered profile/capabilities and
work budget), components (existing request/pins/holds/scope selection), discovery
(entryPoints/workspaceRoots/ignorePaths), policy (registered pack/waiver IDs),
evidence (already-admitted import2 IDs), retention (independent nullable positive
byte/Run/age bounds), and UI color. Every file declares schemaVersion=2. No
configuration field executes code, imports ambient evidence, grants permission,
selects an unregistered capability or rewrites a policy file.

The authenticated release declaration registry supplies the `default` profile and
declares which TS/JS/Rust capabilities this release makes **available**; it is
not the old `preview-typescript` constant, and it does **not** fix the request
scope — that is the matrix's, as the availability paragraph below states. Its *content* is release-specific and remains an
authenticated input, but its schema, membership authority, canonical spelling and
binding to the Plan are normative and published: rows are
`{capabilityId, languageModes[]}` under
`native/native-evidence.schemas.v2.json#/$defs/ReleaseCapabilityRegistryV1`, each
`capabilityId` must be a member of
`native/native-capability-matrix.v2.json#/capabilities[].id` — the single
vocabulary authority, whose law is at `#/capabilityIdLaw` — and each declared
mode must be a registered language mode whose `(capability, mode)` cell is not
`NOT-SELECTED`. That is the same vocabulary this section's
`analysis.capabilities` uses, and its item pattern already excluded the
`relation@rung` spelling; a capability id is a requestable unit of work and is
deliberately not a `relation@rung` fact coordinate, with the matrix publishing
the bridge both ways. "Selects an unregistered capability" is therefore an
enforced refusal rather than a stated intention: it is closed at the
`analysis-spec` boundary and again at Plan/Run closure over the retained record,
not only inside the default-selection helper.

The registry states **availability**, never scope. The `default` profile is the
complete intended product and is fixed by the matrix: for each discovered unit it
requests every capability whose `(capability, mode)` cell is not `NOT-SELECTED`,
including `UNSUPPORTED-TYPED` cells, which are answered by disclosure rather than
omitted. A capability this release does not declare available is still requested
and its absence is **disclosed, not dropped**. Which disclosure depends on the
capability and on what else applies, and native §1.4/§10 own the detail: a
fact-producing capability projects onto its own `relation@rung` Coverage, whose
`(deficiency, nativeCause)` is the owning derivation's under the published
precedence — so a capability the admitted universe cannot serve *at all* keeps
the more specific `language-tier-unsupported`, which outranks
`provider-unavailable`; a **candidate-only** capability has no Coverage entry at
all. Independently of either, the absence is delivered publicly **in the invocation
that selected it**, on `CommandEnvelope.availability`: a
`CapabilityAvailabilityV1` = `{stepCount, totalNoticeCount, steps[]}` whose
per-step `{stepId, noticeCount, notices[]}` entries carry the **complete
ownership tuple in typed fields** — `capabilityId`, `languageMode` and the unit's
own `workspaceRoot` — with the code `native.capability-unavailable`. It is a
declared parity field of **every** `requestClass: analysis` command, so every
applicable renderer carries it, and it is **advisory**: it terminates nothing,
mints no Coverage and grants no Control verdict or repair authority. Earlier
revisions of this paragraph named a singular `StepTermination.domainDetail` or a
`DoctorResult.defects[]` report; neither can deliver this — one is singular where
an invocation has many absences, and a `doctor` report is a **different
invocation**. A staged or development build is an availability fact, not a
narrowed product and not a completed release qualification. Explicit `analysis.capabilities` overrides the
*request* and carries its own provenance; the default's is `DEFAULTED`. Native
§1.4 states the obligation, the disclosure and the host input boundary in full. Discovery populates compiled default values with
recognizer/evidence provenance. Then global, project, interactive local and
explicit flags override in order; arrays replace atomically and records merge
by named field. The environment semantic layer remains empty. CI never probes
the interactive local carrier. Technical recognition is input evidence feeding
default selection, not an authority layer that can override explicit intent.
Winning value, source layer and discovery evidence remain explainable.

Entry/workspace/ignore paths are bounded canonical project-relative paths;
`.` is the sole project-root sentinel for workspaceRoots and ignorePaths;
entryPoints names a concrete source path and cannot use the root sentinel.
Omitting workspaceRoots selects automatic discovery; an explicitly supplied
workspaceRoots array must be nonempty. `[]` is refused rather than silently
interpreted as automatic discovery or as a different native unit selection.
ignorePaths removes that exact path and descendants by whole path segment,
not arbitrary substring. Explicit roots/entries are validated against the
admitted repository boundary and selected language mode; an absent selected
path is CONFIG.INVALID, never silently dropped. An explicit empty entry list
is retained and results in honest incomplete reachability. Native recognizers
own richer discovered test globs and framework semantics; these three override
fields do not execute a glob language. Unknown registry IDs and conflicting
component pins/holds refuse before Plan construction under the deterministic
component resolver. Already-imported evidence IDs must belong to the admitted
project/source/build context under the native/workflow import contract.

Resolved semantic configuration contains analysis, components, discovery,
policy and evidence values: **all five sections are always present** in the
resolved semantic record; a section with no selected fields is exactly `{}`.
An empty section is never omitted. `analysis` always contains `profileId`,
`capabilities` and the complete `{unit,limit}` budget supplied by the authenticated
compiled defaults and then overridden by admitted layers. Missing profile refuses
`CONFIG_PROFILE_MISSING`; missing compiled capabilities/budget is the internal
resolver invariant `CONFIG_DEFAULTS_INCOMPLETE`, never a second zero-config spelling.
Configuration schemaVersion=2 is the **input** carrier. It does not select
evaluator output major. Current evaluator output is identity §4 profile 3.
Explicit version dispatch refuses mixed output-major graphs; unchanged native
and input identities retain their major-two recipes.
For evaluator3, zero-config Plan construction also commits exactly one
`EnumerationPlanV1` and exactly one `EvaluatorEmissionPlanV1` as
`analysis-spec.parameters` (identity-schemas.v3
`requiredForEvaluatorMajors=[3]`). Those parameters are Plan-bound
configuration, not user-file fields of this schema, and they are not an
optional preview. Generic payload-registry cardinality still allows zero
entries for a row a different consumer does not need; an analysis-spec with
`parameters: []` is therefore not a complete default for this evaluator.
The execution-inputs manifest then accounts every selected cell's required
work over the independently retained symbol census. Required cells remain
required when rules are disabled or no subjects match. Native
`default_capability_selection` still requests every non-`NOT-SELECTED`
capability; that request is not a substitute for those two parameters or for
required-cell accounting.
Other section fields are present exactly when selected by default/discovery or an
explicit layer; no implicit empty list is inserted. Thus absent entryPoints means
automatic recognition while explicit `[]` remains deliberate empty intent.
The post-resolution shape is closed by identity-schemas.v3's
`semantic-configuration`, distinct from the optional input-layer schema.
Every array in the input-layer schema explicitly declares `sequence`: layer
admission preserves the user's input until resolution. This is distinct from
the resolved schema's canonical-set annotations; schema admission never performs
the resolver's normalization. All current native, security and workflow schema
arrays likewise declare their owning order using identity §3's enforced keyword.
Sets sort by canonical item bytes; allowedScopes
retains its declared project-before-global priority order. Its digest is SHA256
of canonical semantic configuration bytes. UI, retention bounds, transport
presentation and custody acknowledgements remain operational and cannot alter
that digest; their actual policy/admission still applies. Semantic discovery and
native context digests bind recognizer versions and meaningful effects to Plan.
Configuration-carrier provenance is retained separately from source-code blobs;
a presentation-only CLI change cannot affect Snapshot/Plan/Run.

Schema-one project/global/local files may be read only through the exact legacy
schema and lexical admission, then explicitly projected in memory to the common
version-two fields with sourceSchemaVersion=1 provenance. No file is rewritten
implicitly and no new grant is inferred. Unsupported legacy fields refuse.
Compiled preview defaults are never used as product defaults. A requested
configuration migration is a reviewable data patch through the workflow's
configuration-write authorization, not a side effect of analysis.

`check-product-configuration.py` retains no-config mixed-native selection,
explicit-entry override, exact schema numbers, unknown capability/path refusal,
CI local non-consumption and semantic-versus-operational digest cases. Actual
framework/custody/component resolution has its own native/security/lifecycle
conformance; this narrow resolver does not claim to implement those adapters.

## 2. Separate report custody, semantic correctness and qualification

The release gate has an authenticated invocation context before reading a
candidate report: exact host, provider/data closure, harness, matrix, corpus,
runner public key, runner identity, environment observation and platform profile.
The fresh qualificationRequestId (host RequestId grammar) also binds the
measurement campaign; an older report cannot satisfy a different campaign.
These come from the selected signed release closure and independently admitted
runner inventory. A report cannot supply or alter its own expected subject,
expected answers, trusted runner or performance baseline.

The producer signs the exact report bytes through the qualification signature
frame: ASCII `opensip.qualification.report.2`, NUL, raw 32-byte host digest,
provider-closure digest, harness digest, and SHA256(report bytes), concatenated
in that order. Ed25519 keys are provisioned by the authenticated gate outside
the report. The gate verifies signature before parsing bounded report bytes.
The report's embedded schemaMajor is covered by the signature. Reusing this
signature frame for report schema 3 does not make schema 2 bytes schema 3.

Authentication proves who supplied the observation; it does not prove the
machine executed correctly. The trusted first-party measurement harness,
runner observation path and gate are explicit TCB components. The harness must
execute the selected closure by verified handle, observe exit/EOF and normalized
actual results, and bind the exact measured environment. Product qualification
requires retained real measurements from every required lane; synthetic reports
are tagged reference-only and cannot be promoted. A producer cannot attest its
own unsupported hardware into the allowlist.

The original G13 schema/validator remain frozen historical evidence. The new
`g13-result-schema.v5.json` and `g13-validator.v5.py` close the reproduced defects
for the historical 24-cell shape: independently pinned corpus oracles determine
expected atoms and counters, all subject digests join to trusted context, and
actual observations plus signature are required. Consistently relabeling every
candidate subject digest or zeroing both expected and actual counts now fails.
This adapter does not qualify the added JavaScript/Rust cells.

## 3. Full-product matrix and report schema

The current native matrix is
`native/native-capability-matrix.v2.json`. Expand each declared capability/mode
cell over its four platform families and each selected signed platform profile
from the security contract. A release inventory explicitly selects the
advertised supported cells; unsupported typed cells also receive refusal
conformance cases. No cell disappears because no runner happened to produce a
report. Syntax-only capability is further parameterized by the exact grammar
inventory; one grammar's result does not qualify another grammar.

The full-product report schema is
`foundation/product-quality-report.schema.v3.json`; its gate reference is
`foundation/product-quality-validator.py`. A report covers exactly one trusted
runner/profile/environment and the required cell set for that lane. CellId is
`capability/mode/platform/profile/fixture`; each coordinate comes from the
reviewed matrix and corpus expansion, not from report labels. Every required
fixture names exact source/input bytes, selected capability/rung, expected
normalized observations, expected exit and independently chosen work/stress
bounds. Native reference scenarios supply semantic obligations; executable
native fixtures and their results must be admitted at implementation
qualification before a cell becomes QUALIFIED.

Qualification required cells are `capability/mode/platform/profile/fixture`
measurements of a trusted runner lane. They are not the evaluator's Plan-bound
required analysis cells. Completing a G13 or matrix lane does not mint a Run,
does not commit EnumerationPlanV1 or EvaluatorEmissionPlanV1, and does not
discharge execution-inputs required-cell accounting. Candidate locators and
syntax projections used as corpus answers remain candidate-only; they are not
native fact authority.

The gate's expectedCells is constructed from the verified matrix/corpus and
release selection by the first-party gate. It cannot be supplied as a CLI JSON
argument, copied out of report fields or recomputed from candidate answers.
Expected observation atoms have closed fields `kind`, `subject`, `value` (all
strings); `value` is the schema-defined normalized scalar or canonical JSON
text for structured payloads. The admitted fixture's normalizer and schema
are part of its pinned harness closure. Report atoms sort by canonical bytes,
are unique, and must equal the independent oracle exactly. Counts and
correctness are calculated by the gate; they are absent from the submitted
schema. Duplicate cells/observations, wrong cell sets, wrong exit or substituted
answers cannot be hidden by a reported PASS flag because no such flag is read.

Each benchmark records 3 warmups followed by 7 measured runs in that order,
with positive integer elapsed nanoseconds and peak RSS bytes. The gate calculates median
elapsed time and maximum RSS. For an existing baseline the limits are 1.20×
median time and 1.25× peak RSS, using checked wide-integer cross multiplication (never wrapping), plus the
fixture's independently reviewed absolute bounds. A new supported cell needs
an explicitly reviewed initial baseline and absolute budget; absence is not a
zero or automatic pass. The two baseline measurements must be both present
or both null. A null pair admits an initial-measurement report but never qualifies
a release-selected cell; reviewed initial baseline promotion is a separate gate act. Baseline host/provider/harness, fixture, environment and
platform profile must be compatible by the release gate's signed inventory;
changing the measuring subject cannot silently reuse an unrelated baseline.
Cold-start and retained-evidence workloads are separate fixtures, so warmup
cannot conceal startup or storage regressions. The old reference adapter
retains its historical hardware/performance baseline semantics unchanged.

A well-formed authenticated report may report a failing observation. Report
admission and release qualification are separate: admission verifies custody,
shape and joins; qualification requires every selected cell's correctness and
performance to pass on every required profile lane. Missing, unavailable or
failed lanes block promotion. The release gate also requires lifecycle,
security, output parity and recovery gates; G13 alone never authorizes release.

## 4. Reference evidence and implementation obligations

`foundation/check-foundation.py` retains the original integer and G13
counterexamples, valid controls, exact canonical byte vectors and actual
Ed25519 signature verification with temporary test keys. The reference invokes
the local OpenSSL executable solely to exercise cryptography; production uses
the authenticated first-party implementation, never ambient tool discovery.
`foundation/check-identity.py` independently replays a bounded finite-relation
fixture and exercises identity, proof tampering, retention and crash-state
joins. It is the historical `identity-model.py` harness: it mints `run2`
graphs through hash-only `close_run` and discloses a trusted evaluator
callback and in-memory carrier scope. That is design evidence of unchanged
native and input joins. It is not a general native interpreter, not a
durability proof, and not profile-3 evaluator admission. Current Run minting
and authoritative cache/storage admission are `identity-model.v3.close_run`
complete replay (`check-replay.v3.py`, `check-semantic-replay.v3.py`).
Synthetic graphs admitted by the native owner demonstrate those joins; they
do not qualify a compiler, host or platform. Historical single-atom fixtures
cannot establish profile3 admission.

The full-product report checks exercise a separate TS/JS/Rust-shaped cell set,
forged subject/corpus/answers, missing lanes and false performance claims.

Reports record every scenario, source pins and limits. Independent review reads
semantics and executes adversarial controls; source hashes establish the
reviewed bytes, not correctness. Legacy self-reporting checker claims and their
observability escapes do not enter product evaluation authority. The corrected
product uses explicit admitted data plus trusted pure evaluation; an adversarial
program sharing the verifier's process is not claimed to be contained by Python
introspection. Native measurements, independent implementer reproduction and
supported-platform qualification remain the concrete pre-release gates.

Discovery observations are folded into the trusted `defaults` layer by the host
before the reference Config2 resolver runs; their recognizer identity and path
provenance remain in the discovery record. The reference resolver does not scan
frameworks. A missing profile is `CONFIG_PROFILE_MISSING`; an unknown profile is
`CONFIG_PROFILE_UNREGISTERED`. Both pack and waiver IDs require registry admission.

## 5. Complete product-boundary successor (DR-117)

D-371/D-372 prospectively replace P-1/P-2/G3 only as enumerated here. These are the seven dispositions required by architecture file02, “Current V1 product boundary and required successors”; the historical enumeration and preview acceptance keep their original scope.

1. **Marketplace/catalog and governance depth:** the selected product has one signed first-party component/recipe/schema registry. It has no public marketplace, third-party publisher admission or ecosystem governance promise. Unknown contributions refuse through the closed registry; declaring an id does not establish trust.
2. **External lifecycle parity and discovery:** supported first-party components receive the common installation, update, rollback, offline, doctor and removal contracts. Repository/framework discovery selects applicable admitted capabilities; it is not an external service and cannot install or execute discovered code. Third-party lifecycle parity is outside the selected scope, not a partially specified admission mode.
3. **Contribution roles beyond narrow/data-only:** first-party native providers may produce typed facts/Coverage and prepared input imports. Signed first-party declarative recipes/profiles may select host-owned steps. Only the host constructs findings, evaluates policy/verdict, owns persistence, finalization, rendering and termination. A component cannot acquire those powers by declaring a root command or emitting an output record.
4. **Untrusted native or WASM admission and enforcement:** neither is admitted in this product. No process/WASM boundary is claimed as a sandbox. Separately authorized repository-code preparation/tests are the explicit trusted-code principal of security S10, with the actual platform disclosure/enforcement matrix and revocation/cleanup rules. They do not open an untrusted plugin admission path. G09/G21/G29/G30 must exercise these refusal and authority boundaries; a synthetic fixture is not enforcement evidence.
5. **Imperative contributions, probes, project hooks and root commands:** arbitrary imperative contributions/project hooks/root-parser extensions are not admitted. The closed host command inventory owns every command. Named first-party repair, test, preparation and doctor operations have their exact explicit authorization and effect contracts; a recipe/profile cannot bypass them. Metadata discovery/help/recommend do not run repository hooks or probes. Consent to one executable step never becomes general command or persistence authority.
6. **Network-granted analysis and egress defaults:** ordinary analysis/discovery are offline; there is no implicit index refresh, download, telemetry or required egress. Explicit trust refresh/offline import and explicitly required export delivery have their named host lifecycle/output semantics. Repository-code effects are disclosed/admitted by their actual trusted-code grant; they are never silently reclassified as confined analysis. Required delivery failure can fail the invocation without changing a committed Run's assurance.
7. **G3 physical substrate:** the selected substrate is a signed Rust distribution core/semantic host, pure first-party evaluator, supervised native TS/JS and Rust components, and the signed offline assets and verified storage mechanics required for the selected authoritative profile. This replaces the prototype's lockstep Node/npm train and the preview's narrow command/provider set. The default product profile is authoritative-capable; an explicitly selected management-only installation is not an authoritative closure and refuses analysis until the required signed closure is separately installed through an authorized lifecycle operation. Missing assets never trigger ambient downloads or a weaker analyzer. Every physical dependency, including compiler/runtime/standard-library/LLVM/storage assets actually used, belongs to the admitted closure/TCB inventory and its packaging/offline/quality gates.

The selected exclusions are D-371's credentials, third-party ecosystem, untrusted contributions and TUI exclusions; this section introduces no new scope cut. Product measurements remain required by the named release gates. This is a complete boundary selection now, not a promise that future implementation will choose these policies.
