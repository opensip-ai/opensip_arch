# Joint authoring interfaces — proposed, not yet accepted

User instruction: Codex and actual Claude address all AR-01–16 issues now.
D-367 delegates product/design decisions; D-371 selects one full-product design.
No existing frozen source or audit record is edited. A prospective D-372 act
will name exact replacement selectors, reviewed subjects and applicability.
Product implementation is not part of this task. Authors cannot accept their
own bytes. Codex reviews Claude-authored units; actual Claude reviews Codex's
units; a fresh Claude session reviews mixed integration. Working-tree delivery,
without a commit/push, is proposed in the act, as in D-370/371.

## Shared choices for drafts

These are concrete coordinating proposals, subject to reciprocal review.
If a choice is technically unsound, identify the exact alternative in your
handoff; do not silently invent a conflicting interface.

- One current product contract set: `docs/v2/contracts/product-v1/`.
- New product envelope/identity/command versions are explicit successors;
  historical V1 and D-369 preview bytes retain their original scope. Existing
  immutable fact payload/FACT-ID recipes can be referenced, never reinterpreted.
- Host-owned ProjectId retains PROJECT-ID-V1 marker+registry rules. Private
  operational namespace UUID is a locator bound one-to-one to that ProjectId;
  neither is a path-derived semantic identity. Explicit adoption/fork handles
  cross-machine identity. Ordinary clone creates a new tenant.
- Invocation uses existing host RequestId as its operational identity, with
  StepId = unsigned integer position in a bounded acyclic ordered step list;
  each admitted attempt has its own ExecutionId. No new ambiguous InvocationId.
- Run identity is content-derived (`run2:<sha256>`), excludes attempts/clocks/
  receipts; Run is an immutable source+plan+semantic-evidence+evaluation seal.
  Fresh attempt on identical admitted inputs may link the same Run. Query,
  rendering, import custody and mutation are operational steps, not fake Runs.
- New content identities use H(domain, typed descriptor): SHA-256 over ASCII
  `opensip.product.v1` + NUL + ASCII domain + NUL + uint64 big-endian byte length
  + exact canonical UTF-8 JSON descriptor. Canonical JSON: closed schemas;
  UTF-8-byte key order; preserve scalar Unicode (no normalization), reject
  surrogates/duplicates; minimal JSON escaping; integers -2^63..2^64-1 only,
  no float/exponent or negative-zero admission; booleans separate; no whitespace.
  All legacy floating confidence stays in its original fact identity or is
  explicitly mapped to declared rational/integer evidence fields in a successor.
  Codex owns exact descriptor/schema recipes; authors refer to these named
  domains without inventing another serializer.
- Product Plan descriptor binds source SnapshotId, selected semantic closure,
  workflow analysis specification, resolved configuration, native context,
  imported evidence descriptors, policy/waivers, scope/budgets and semantic
  grant projection. Operational credential/nonce/expiry/receipt data stay out.
- Import descriptor domains distinguish runtime, test, history, dependency and
  prepared evidence. Required common fields: kind, schemaVersion, source/build
  correspondence, producer/version, adapter/version, blob inventory+digests,
  scope/observation semantics, completeness/omissions. Exact records are authored
  by native/workflow owners, then joined to the common identity schema.
- Full-product `opensip` defaults to discovery then durable authoritative analyze;
  no-policy retention is the binding durable-unbounded CD-RT-5 default, with
  DEFAULTED provenance and visible first-use/storage disclosure. No implicit
  policy write. An explicit `--ephemeral` analysis is non-authoritative and
  cannot supply authoritative baseline/repair prerequisites.
- D9 stays host-owned: completed analysis fail=1, admission rejection=2,
  indeterminate evidence=3, operational/delivery/persistence failure=4,
  cancellation follows existing D9. New typed domain detail must explicitly
  map to a lawful existing cause or a reviewed successor, never silently use 0.
- Repository execution is disabled by default. If explicit native/test execution
  is selected, it needs an admitted trusted repository-code principal and narrow
  user authorization. No enforcement claim for network/process confinement where
  the host only discloses it. Imported independently prepared artifacts are a
  supported alternative, not ambient reads or implicit execution.
- Authoritative proof/retention/replay/repair must join one host writer and current
  trust. Content identity does not prove custody, permission, or authenticity.

## Ownership

| Author | Files owned | Audit scope |
|---|---|---|
| Codex | identity-and-evidence.md; admission-and-qualification.md; foundation/ evidence; integration/act/navigation | AR-01/02/09/15, integration |
| Claude security | security-and-lifecycle.md; security/ evidence | AR-03/04/05/06/14, AR-16 offline/doctor guidance |
| Claude native | native-evidence.md; native/ evidence | AR-07/12/13 native cells; input evidence schemas |
| Claude workflow | workflows-and-surfaces.md; workflows/ evidence | AR-08/10/11/13 surfaces/16; policy/review/repair |

Each unit includes exact closed schemas/decision tables, refusal/partial/recovery
behavior, source-pinned adversarial reference checks, selected numeric bounds,
and explicit superseded-source selectors. A prose promise or new owner label
does not close a gap. Reference checks are design evidence, not OS/product
qualification. Never label an invented cryptographic proof as measured evidence.

## Concrete identity join authored during parallel work

`foundation/identity-schemas.v2.json` now names exact product major-two descriptors.
Product source identity is snapshot2; product FactRecord2 is fact2 and wraps the
existing relation-payload schema/digest with snapshot2, source/target universes,
producer closure, verified anchors and integer confidence millionths. This is an
explicit FACT-ID-V2 successor, not new bytes under FACT-ID-V1. Existing V1 native
payload grammars may be reused unchanged; legacy fact IDs remain historical and
are not relabeled. New native role protocol negotiates these source/fact/coverage
versions before source disclosure; no raw snapshot2 is sent to a V1-only worker.
This resolves the existing source-ID grammar mismatch rather than treating raw
old fact IDs as if they were bound to the new product source identity. Native
unit must join this explicit successor during integration.

## Storage custody join found during inherited residual reconciliation

Identity-and-evidence §5 retains TM V17: detected backup-managed storage requires
an explicit first source-write choice, distinct from no-policy CD-RT-5 durable
default. `--allow-backup-custody` acknowledges external-copy limits for this
invocation, or a pre-existing admitted storage-policy record covers it; no
implicit policy-file write. CI without choice refuses REQUEST.PRECONDITION_FAILED
with `storage.backup-choice-required`. UNKNOWN is not "not backed up". This is
operational custody metadata and does not alter Run semantic identity. Sync/
upload/shared storage classifications remain distinct. Workflow command schema
and security storage admission need this explicit join in final integration.

## Full-product configuration join

Foundation now owns product-configuration.schema.v2.json (not the old
preview-typescript compiled constant). Default profile/capabilities come from
admitted release declarations plus native applicability; explicit bounded
entryPoints/workspaceRoots/ignorePaths override discovered defaults. Common
schema2 sections bind registered policy packs and already-admitted import2 IDs.
See admission-and-qualification §1.1 for exact merge/CI/legacy projection and
semantic-versus-operational digest rules. Security's safe discovery admits this
carrier; workflows recommend produces a schema2 candidate and validates it
without granting effects or writing config. Frozen foundation subject v4 includes the reviewed corrections; earlier
subjects v1/v2 were unreviewed and v3 received CHANGES_REQUIRED. Final integration
selects exact accepted unit bytes, never an unreviewed intermediate snapshot.

## Final digest and principal joins

All foundation fields documented as raw digests use raw SHA256 of retained
canonical payload bytes, not a domain-framed hash under another owner's name.
In particular Plan scopeDigest hashes foundation scope-descriptor; a workflow
glob policy is a separate scope-policy input. A schema digest hashes exact FULL
schema document bytes; registry kind/domain/selector chooses one closed $def.
Runtime/test/history admit workflow canonical payloads only; native input adapter
shapes normalize first. Dependency/prepared admit native.import-payload domains.
VCS commit equality or a declared build string alone cannot establish correspondence.

P-TRUSTED-REPO is the display/authorization principal mapped to semantic-grant
kind trusted-repository-code. Runtime authorization binds the exact operation,
project, snapshot, argv/closure or repair plan, current trust and operation lifetime.
Repair apply is a host-brokered source mutation, not repository-code execution.
Immutable mutation receipts acquire verification links through separate append-only
records, never by editing their content-derived preimages.
