# Conditional G15 metadata and lock joins

Status: PROPOSED design evidence. Author: Codex protocol fixture author. This
unit supplies concrete inputs for the five conditional schema classes left by
`qualification-design-schema-join.v1.json`: TC-ACCEPT.5, TC-SIG.C-LOCK,
TC-SIG.C-ENVELOPE, TC-BYTE-EXACT.C-CANON and TC-BYTE-EXACT.C-LOCK. Five classes
across four platform labels and three report states produce sixty concrete
conditional slots. The complete overlay retains the other 900 concrete input
assignments, giving eighty keys in each of twelve reports. Input completeness
is not product qualification; native OS executions remain zero.

## Custody and resolver successor

`component-lock-schema.completed.v3.json` retains the reviewed v2 grammar and
adds required `resolutionInputs.registryViewDigest`. `indexDigest` is the domain
preimage digest of exactly one signed catalog (`opensip.metadata.catalog.1`).
`registryViewDigest` is the domain preimage digest of exactly one immutable
scoped registry export (`opensip.metadata.registry-view.1`). The view scopeContext
must equal the lock's, and its sourceStoreDigest must match the externally
pinned host admission-store snapshot. These are custody measurements, never
permission, trust decisions, or authority carried in a lock.

`compatibility-selection-model.v4.py` first validates the complete new input
shape. It verifies actual Ed25519 signatures on the fixed TEST trust-root,
revocation list, catalog and component manifests; checks namespace/routing,
thresholds, timestamp/floor requirements and exact stored/preimage/envelope
custody; validates full manifest structure/registry/path rules; and reconstructs
the scoped registry export from its pinned store. A forged export cannot become
valid by replacing the lock's digest with its own newly measured hash. Project A
shadows the identical global release only inside A; project B retains the global
release. The local store and view are never represented as release-signed files.

The verified candidates feed the unchanged reviewed v3 search/comparison/closure
core through an internal adapter. Its old observation-index digest is private
fixture custody only; it is never published as the external catalog digest. The
external lock replaces that internal input with the full actual catalog/view
inputs, is validated under completed schema v3, and serializes under
`opensip.metadata.lock.1`. There is no silent reinterpretation of the old
synthetic indexes as catalogs. All 149 retained v3 core checks replay unchanged,
including SemVer, closure, sorting, duplicate-input, scope and schema properties;
the retained old report must remain byte-identical. New integrated negative
cases also reject duplicate requests and cross-list duplicate pins/holds.

`permissionPolicyDigest` uses the existing `opensip.metadata.policy.1` domain.
`compatibilityPolicyDigest` is plain SHA-256 of the exact retained compatibility
matrix v4 bytes, as agreed by the lead. It creates no new identity or domain tag.
Both must match the bytes and the external host policy snapshot. The matrix's
independent doctor-report surface does not add a coupled manifest field.

The host context is a fixed fixture input describing the already trusted root,
current store and public-policy snapshots, the evaluation clock and monotonic
floors. A manifest, catalog or lock cannot select those values. This unit checks
consumption of that context; persistent publication, root rotation, host-origin
authority, confinement and full trust-state transition proofs remain owned by
the separate security/lifecycle units.

## Actual retained bytes

The primary bundle contains two complete manifests with distinct UUIDs:
`typescript-analyzer` and the explicitly non-shipping
`fixture-typescript-twin`. Both retain role analyzer. The primary advertises the
five completed TypeScript capabilities and declares a dependency on the twin;
the twin has an empty capability declaration. This is an actual two-component
closure, not two display labels or an inferred hidden edge.

Every committed file and all six declaration references have actual retained
bytes, including the license notice inventory and notice text. The bytes are
copied from the independently reviewed synthetic manifest artifact-closure unit.
They are DESIGN-FIXTURE-ONLY and never executed. Each platform has an actual
profile.1 archive produced by the retained stdlib design encoder and checked by
its independent field decoder against the manifest tree. The catalog's
archiveDigest and sha256 are both plain measurements of those exact archive
bytes; archiveProfileId fixes their interpretation. No tree identity is invented.

Manifest, catalog, revocation and root envelopes contain actual 2-of-3 Ed25519
signatures. The seed material is explicitly PUBLIC TEST ONLY and deterministic
from labelled test strings, so anyone can reproduce these fixtures. It is not a
release key, example pretending to be an authentic release, or key-custody proof.
The root is externally pinned as the fixture trust anchor before its envelope
is inspected; self-signing an arbitrary root cannot create that pin.

Hex encodings in the bundle and variants are exact bytes, not descriptions of
future files. Manifests are deliberately stored in readable JSON while signing
preimages use the adopted canonical encoding. The canonical manifest goldens
retain NFC non-ASCII text. A second serializer independently reproduces those
bytes for this bounded corpus; the security unit owns the wider canonical
Unicode/escaping property suite.

The three report states have concrete environment records. Clean and offline
have no prior selection. Upgrade retains a separately signed 0.9.0 primary
component generation and exact prior lock, verified under its historical
catalog floor8. The new generation is 1.0.0 under current floor9. Replaying the
new selection never mutates the old lock or lowers the current floor. Historical
verification demonstrates prior-byte custody, not permission to dispatch a stale
catalog under current trust. The earlier 900 slots retain their own original
assembly/state inputs and scope; they are not rewritten as these metadata runs.
All fixture assembly records deny network and ambient-path resolution.

## Five conditional properties

| Class | Concrete observation |
|---|---|
| TC-ACCEPT.5 | The verified signed inputs resolve exactly two manifest UUIDs, with project-primary/global-twin scope, and yield a schema-valid canonical lock. |
| TC-SIG.C-LOCK | Every retained selected artifact matches the actual lock; flipping one byte of bin/entry produces RJ-4 DIGEST_MISMATCH. |
| TC-SIG.C-ENVELOPE | Two valid authorized TEST signatures over an envelope carrying the wrong manifest preimage still produce RJ-4 ENVELOPE_MISMATCH. |
| TC-BYTE-EXACT.C-CANON | Stored manifest bytes parse to the retained canonical bytes; an independent serializer and direct domain-prefixed SHA-256 agree with the signed preimage. |
| TC-BYTE-EXACT.C-LOCK | The exact selected lock bytes match an independent serializer and direct domain digest; noncanonical whitespace and a wrong preimage digest refuse. |

Supplementary inputs include a validly signed but below-floor catalog, forged
view with a recomputed claimed digest, wrong project view, valid project-B global
selection, incorrect/missing custody pins, a wrong installation, policy pin
mismatches, missing artifact bytes, a modified manifest, and duplicate input
claims. Refusals produce no partial resolved array. The checker also compares
the complete bundle before and after replay to establish reference-model input
immutability. No product core-survival or physical filesystem durability claim
is made by that comparison.

The matrix overlay replaces the five conditional member assignments and makes
the old implicit AT-definition pointers explicit without changing their meaning. Every
other member retains its previously pinned definition and limitations. Old
placeholder declaration content, selected semantic-rule checks, no-execution
probe specifications and production-adapter obligations are not promoted to
stronger evidence by receiving a concrete input pointer. There are no remaining
conditional requirement-only pointers among the sixty new assignments.

## Review and replay

```
/tmp/opensip-architecture-review-env/bin/python docs/coop/completion/check_g15_conditional_v1.py --report /tmp/g15-conditional-review.v1.json
```

The report retains exact subject/source hashes, the sixty conditional observations,
and the full 960-slot assignment checks. Its freeze manifest is a proposal for
independent review, not self-acceptance. Security dependencies must be their exact
reviewed bytes or an explicitly reviewed successor. No frozen predecessor is
modified by this unit, and no readiness register or product qualification changes.

Retained result: **3,208/3,208 PASS**, including an unchanged byte-identical replay
of the separate 149-check resolver core. All sixty conditional observations are
executed reference checks; all 960 matrix pointers and inherited byte pins resolve.
The fixture clock is explicitly 2026-12-21; it is not a claim about current release
validity or a real ceremony.
