# Distribution qualification design evidence, version 1

Status: **PROPOSED. Design evidence only. No product gate is QUALIFIED.**
Author: Codex distribution fixture contributor. The completion lead and Claude
must independently review and apply the final integrated contract before any
register change. These files do not amend the old contracts by themselves.

Run from the repository root:

```sh
python3 docs/coop/completion/check_qualification_design.py
```

The checker uses only Python's standard library. It validates committed fixture
bytes and expected observations, then writes `qualification-design-report.v1.json`
with the input and checker digests. Use `--report /tmp/qualification-replay.json`
to replay without writing the review-frozen report. Archive parsing, local SQLite process-death
checks, and selector evaluation actually execute. Product adapters, language
providers, signing ceremonies and four-platform qualification do not execute.

## Source authority and count reconciliation

The inputs pin `component-packaging-contract.v14` (D-108),
`harness.DR-G15.packaging-adapter-conformance.v7` and its recorded occupancy
remeasurement v9 (D-214), `component-manifest-schemas.v11` (D-104),
`component-manifest-fixture-corpus.v6` (D-106), `monorepo-ci-contract.v16`
(D-124), and `lifecycle-generation-contract.v2` (D-107). They pin frozen artifacts,
not the mutable coordinator log or the lead's still-changing completion draft.
The integrated adoption must additionally pin the final reference choices.

The historical phrase “324 AT fixture cells” means **27 AT member keys × four
platforms × three states**, not “AT-3, 24 cells.” There are twelve report units,
each with eighty member keys: 960 slots altogether. The 53 non-AT schema keys
account for the other 636 slots. The old corpus contains **51 authored inputs**;
input count and member-key count describe different domains.

## Packaging and inherited schema coverage

`qualification-design-packaging.v1.json` supplies seventeen AT-ARCHIVE member
vectors, seven supplementary exact-byte negatives, thirteen path vectors and
positive/negative observations for the ten remaining AT halves. The archive
files live in `qualification-design-bytes.v1/` and each has its own SHA-256 pin.
A field-by-field strict decoder checks profile.1; stdlib `tarfile` independently
decodes the fixed vector and constructs an identical archive using a second
header implementation. This is concrete design evidence of the chosen format.
Two actual runs of the eventual Rust adapter remain a G15 execution obligation.

| Old obligation | Concrete design evidence | Product execution still required |
| --- | --- | --- |
| AT-1 clean assembly | Complete and missing-artifact observation pairs, clean environment record | Offline adapter emission and trusted installation under applied trust contract |
| AT-2 no ambient dependencies | Empty PATH/runtime/package state, attempted implicit-download rejection | Actual network-denied adapter process and environment controls |
| AT-3 hostile paths | All thirteen TC-PATH members, including actual escaping symlink and dual normalization diagnostics | Actual production admission and fixture-generator isolation |
| AT-4 health and opaque role/version tokens | Closed health record presence/reference predicates; incompatible confirmation negative | G21 framing, negotiation and actual health invocation |
| AT-5 offline assembly/install | Complete, missing closure and denied-network observation pairs | G08/G15 offline installation; no authoritative sealed closure claim |
| AT-6 update/rollback | Immutable prior tuple/current-trust/monotonic-state observation predicates | Preview generation rollback under G18; core self-update/repair stays DR-110 deferred |
| AT-7 owner-defined gates | Complete passing observation map and digest-bound failing G13 result | Actual G01–G05/G13 results and custody verification |
| AT-8 exact archive | All seventeen member keys, capacity endpoints and hostile byte mutations | Actual adapter conformance per report unit and platform |

Every matrix slot points to a fixture definition. `clean`, `offline`, and
`upgrade` have explicit environment records; upgrade names an immutable prior
selection, while clean/offline have no prior selection. All assembly work is
network-denied. Reusing format vectors across platforms is deliberate: profile.1
is platform-independent. These assignments are not twelve fabricated runs.

The maximum-size archive vector is expressly metadata-only: it tests the
8,589,934,591-byte octal-field endpoint without storing or claiming an 8 GiB
archive. The high mode endpoint tests archive field capacity; it does not override
manifest or executable permission policy. The 100-byte link target case tests
archive representation, not whether the target is an admitted executable tree.

`qualification-design-schema-join.v1.json` maps all 53 schema member keys to exact
input paths/selectors. The checker validates every D-106 authored/supporting byte
pin and independently interprets selected identity, naming, parent/alias cycle,
path, reserved-field, digest, scope, deprecation and closure rules. It deliberately
does not read a packet's `expected` field to derive its result. These are selected
semantic-rule checks, not a claim to have implemented every v11 schema property.

Forty-seven keys map to inherited authored inputs, TC-PATH.11 maps to the new
normalization diagnostics fixture, and five keys explicitly await final
integration with the lead's lock and Claude's security supplements:

- `TC-ACCEPT.5`: actual multi-component lock input; the old optional fixture is single-component.
- `TC-SIG.C-LOCK`: artifact bytes against the adopted lock digest.
- `TC-SIG.C-ENVELOPE`: wrong signing preimage under the adopted detached envelope.
- `TC-BYTE-EXACT.C-CANON`: adopted metadata serialization preimage vectors.
- `TC-BYTE-EXACT.C-LOCK`: adopted lock serialization/digest recomputation.

Those five keys cover sixty report slots. Their current pointers are explicitly
marked integration requirements, never manufactured fixture bytes or success.
The integrated successor must replace each with concrete final input pins before
claiming all fixture authoring complete.

Two inherited limitations are now exposed rather than silently counted as proof:

1. The old `TC-PATH.symlink-escape` uses `bin/entry -> ../outside`, which resolves
   inside the root at `outside`. It can be refused for traversal/absence but does
   not isolate root escape. The new `TC-PATH.8` uses `../../outside` and the checker
   verifies root escape. Supplemental boundary cases separately record containment
   and full admission: `../outside` with a declared root target is contained but
   still RJ-3 under the inherited no-parent-segment grammar; `../../outside` is
   outside; `bin/entry -> target` with declared `bin/target` is admitted.
2. The old no-execution packet supplies a recorder and an empty initial log; it
   never ran product admission. Its checker result is `PROBE-SPEC-VALID`, **not**
   “zero product executions observed.” Likewise `dummy.empty` declarations prove
   schema/reference presence only, not SBOM, licensing or quality evidence.

The new normalization pair requests both `non-NFC` and `normalization-duplicate`
diagnostics. That is a proposed diagnostics successor, not an invented RJ-3
subcode. If the integrated contract instead rejects immediately on non-NFC, this
fixture cannot discriminate pairwise normalization checking and must remain
unscored as the D-106 corpus correctly records.

## CI and independent releases

`qualification-design-ci.v1.json` names the shipping TypeScript provider as
`opensip.typescript`, shared distribution core as SL-1, and a **not-shipped trusted
qualification-only TypeScript twin** `fixture.typescript.twin`. These are fixture
identities, not an application of manifest stableId UUIDs. The twin provides a
second component for dependency/independent-release attacks without introducing a
second preview language or a requirement to ship an additional component. The
integrated ownership encoding must bind these fixture labels to actual manifest
identity tuples; it must never use a display label as a production stableId.

The closed pre-mutation domain is two identities × one role × four platforms ×
fifteen old change classes = 120 cells, plus the separate DEF-WIN deferred slot.
The twin's cases apply an identity permutation so the changed component really
changes. DEF-ROLE-NON-TS remains a documentation sentinel, not a fictitious result
cell. ROLELESS-NA is separately checked. Twenty-six selector scenarios cover
all fifteen change classes and supplementary attacks. The independent unit
inventory prevents deleting an untouched ownership declaration from silently
shrinking the input universe.

| G16 class | Checker evidence |
| --- | --- |
| 1 | C-A-ONLY, including symmetric twin case |
| 2 | C-B-VIA-DEP, SUP-DEPENDENCY-OMITTED |
| 3 | All seven missing/invalid classes, complete conflict, conflict+missing dominance |
| 4 | Selected lane signature-verifier observations and refusal of required blocked/invalid inputs |
| 5 | Two-component fixed point and individual PROTOCOL/SEMANTIC/LOCK seeds |
| 6–9 | Exact closed lane map; missing shared-core or skipped proof rejected; SL-5/SL-6 retained |
| 10 | 120-cell pre-mutation matrix, explicit DEF-WIN and ROLELESS-NA |
| 11 | Aggregate selection bound to the selector decision digest |
| 12 | IR-1 component-new, IR-2 core-new, IR-3 rollback/coexistence, IR-4 individual route; lockstep and bundle-only refusals |
| 13 | Owner/dependency/change-set/FDB digest join, wrong decision/input/aggregate attacks |
| 14 | Pinned pre-mutation basis, exact uniqueness/count checks and omission attack |

`signatureVerified` is deliberately an input observation from the future trust
verifier. These tests prove that the result consumer refuses false/missing
verification and wrong joins. They do not constitute a release signature. The
production metadata digest encoding is owned by the security supplement;
`canon()` here is explicitly only fixture custody encoding. Selector outputs
are platform-neutral; executing them for four platform labels does not qualify
four native platforms.

## Lifecycle and crash recovery

`qualification-design-lifecycle.v1.json` supplies before/after crashes around all
thirteen reference publication events, including PREPARING, writes, file/directory
sync, VERIFIED, rename, parent sync, READY, transaction writes, durable commit and
acknowledgement. Twenty-two additional inputs cover all eight old properties:
immutable selections, exact closure, operation pinning, conflicting projects,
lease death, every named preview reachability root, old-or-new publication,
current trust and monotonic floors. Migration prepare/abort/commit have explicit
inputs, and attempted no-return/mixed migrations refuse in the preview.

The checker additionally runs two real local SQLite subprocesses which exit
without connection cleanup before and after commit. It verifies selection and
transition move together, an already-running operation retains its old
generation, and another project's conflicting generation remains unchanged.
This exercises local SQLite process-death semantics. It does not simulate power
failure or establish filesystem durability on Linux/macOS targets.

G18 must inject death before/after **every actual implementation** write, fsync,
rename and transaction durability boundary, including all child operations of
these abstract phases. The rule is not “only the thirteen listed calls.” Any
new unmapped boundary fails qualification until mapped and exercised. The
lifecycle/grant journal must use the integrated security design's shared writer,
lock and durability discipline. Trust floor rollback remains forbidden. Core
self-update and repair-media execution remain the existing DR-110 deferral.
