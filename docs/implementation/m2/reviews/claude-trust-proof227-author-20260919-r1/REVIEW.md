# Author assistance: acyclic metadata / root / image proof nodes (227 follow-through)

**Status: AUTHOR DRAFT for root review. Not independent approval, not a review verdict, nothing
selected.** I wrote these fragments, so I cannot approve them. No candidate, product or
architecture file was edited; nothing was committed or pushed; all output is under this directory.

## Deliverables

| file | what |
|---|---|
| `proposed/trust-proof-nodes.v1.json` | 41 `$defs`: 32 copied verbatim from frozen 227 r5 (re-asserted equal at build), 2 copied verbatim from primary `opensip-payload.1`, 7 new. sha256 `14ffc8ca…ed79` |
| `proposed/JOIN-NOTES.md` | layering rule, per-node joins, scoped image admission; every rule tagged existing/proposed |
| `proposed/shape-check.json` | 88 cases: 52 refusals, 15 admits, 17 DAG-edge rows, 4 static schema properties |
| `claude-out/probes/{build,check}_proof_nodes.py` | builder and checks (frozen `canonical.py` d47f25db… exact-integer validator) |
| `source-hashes.json`, `source-hashes-215r14.json` | every cited source, with hashes and what was / was not verified |

## Inputs and verification

- 227 r5: archive pin and all 66 members verified from the tar before extraction; re-verified
  at the end (`claude-out/pin-verification.json`, mode `re-verified`).
- 215 r14: archive pin and all 1445 members verified by exact path, read from the tar, not
  extracted. `OWNER.md` = d8165f14… = the `logical215.md` cited here.
- 222 r6: `PERSISTENCE.md` f8ddaecc… from my earlier verified extraction, byte-equal to the copy
  pinned in 225 r2.
- 225 r2 / 226 r3: archives verified in my 227 event-shell task; cited files re-hashed here.
  226 r3 was not re-read for this draft (no claim below depends on it beyond what 227 r5 restates).
- Reference-201: my verified extraction; seven cited files re-hashed.

## Decisions taken (each answers a question in the request)

1. **Ownership: root's candidate direction is right, with one subtraction.** Raw closure with no
   root backreference (layer 1) → root-edge authentication nodes (layer 3) → metadata admissions
   and 222 history nodes (layer 4). I do NOT add a separate "admitted payload closure/context"
   node: every consumer that needs the (closure, root edge) pair already names both, and a node
   restating the pair is precisely where the back-edge returns. JOIN-NOTES §0/§2.
2. **The closure restates nothing signed.** The signed logical-member map IS the retained
   manifest body. The closure adds only what the manifest lacks: byte lengths and envelope
   pairing for retained members (`BlobRef`/`DocRef`), and inert artifact observations. `path` is
   the primary entry schema verbatim and is never opened — no PATH dependency.
3. **Artifact observations cannot be dereferenced.** `{path, sha256, observedBytes}` is
   deliberately not a `BlobRef`: no retained object, no 4 MiB cap, no platform/entrypoint member.
4. **Ordinary vs recovery is a closed two-variant union.** `authorization` required in one and
   absent (not null) in the other; recovery members must EQUAL the full signed scope, ordinary
   may be a relied-on subset. The scope token discriminates; it grants nothing.
5. **Authentication ≠ acceptance is structural.** No boolean exists in any new def (static
   check). Acceptance is only `heads.root.admission == NodeRef` in a 222-proven capsule plus its
   role event.
6. **Current vs historical has no flag.** A node records the context it was evaluated in;
   COMMIT re-admission yields a different node (same documents, different context). Old nodes
   are replayed against their own context and never cited as current standing.
7. **`CapsuleImageV1` is a pure alias.** Same bytes, same raw hash that 222 already uses as the
   predecessor key. Standing needs the native-before join or the 222 proof; the T-traversal table
   in JOIN-NOTES §3 separates S4.5/restrictive consumers from ordinary/continuity/restore.

## Remaining owners — not completed here, deliberately

- **U-1 (blocks the `anchor` variant's exactness). Identity `closure.kind` has no core kind.**
  `identity-schemas.v3.json` enumerates `provider, evaluator, detector, toolchain, stdlib,
  rust-dev-llvm, grammar, adapter`, while security-and-lifecycle l.1495 types
  `fromCoreClosure`/`toCoreClosure` as `closure2:`. I used `ClosureId` because that is the
  existing identifier, but I could not find which `kind` a core closure hashes under, nor the
  path of the embedded root body/envelope inside its `tree`. Owner: identity §3 /
  distribution-core inventory. I did not invent a kind or a path.
- **U-2. One-node closure vs primary cardinalities.** Primary allows 3 × 100000 entries; at
  ≥ ~100 bytes per retained entry a 4 MiB node holds roughly 40k. 222 r6 already says such a
  closure is refused, not truncated — so this is an availability bound root has stated, not a
  new one. If root later wants large payloads, the owner is a paged closure with its own
  completeness proof; I did not draft one (speculative).
- **U-3. Staged verification order** (JOIN-NOTES §2): time-free authentication, then S4, then
  expiry. Needs to be stated by the 225/227 time owner; `S4EvaluationInputV1` must never gain a
  same-operation root reference. Today it has none (checked).
- **U-4. `MetadataAdmissionNodeV1(kind=revocation)` overlaps the 222 history `list` node.**
  Both carry `{list DocRef, admittingRoot}`. Smaller alternative: `heads.revocation.admission`
  names the history node and this node exists for `catalog` only. Root's call; I kept both
  because `AcceptedMetadataHead.admission` is one field for two kinds.
- **U-5. Manifest-envelope custody.** The payload manifest's own envelope cannot be a member of
  the manifest it signs. Where the importer finds it (and whether `envelopes[]` pairs bodies by
  `subject.storedSha256` only) is owned by the payload/custody contract; I state the join, not
  the discovery rule.
- **U-6. `ordinary` edge omits the old root document** in favour of `parent`. 222 r6 prose lists
  both documents; this is a knowing deviation, explained in JOIN-NOTES §2.
- Not attempted: canonical byte encodings beyond reuse of `canonical.py`, DDL, native producers,
  signature/threshold adapters, 222 proof integration, event-union joins (root's 226/227 work).

## Limits of the checks

Shape cases use the frozen validator and single-change mutations of admitted baselines; only
`AdmissionError`/`ValidationError` count as refusal. The join and DAG functions are toy sketches
over fabricated bytes: no signature, threshold, custody, 222 publication proof or S4 evaluation
runs. The DAG table encodes the rule rather than discovering it. `maxItems 65536` was chosen to
mirror the 222 object ceiling and is unmeasured.

Disclosures: my boolean detector first mis-fired because `1 in (True, False)` is true in Python
(fixed with identity comparison before any result was recorded); a first 215 r14 member pass used
suffix matching and reported 15 false mismatches, redone by exact path with 0; one re-verify run
without its pin argument wrote an empty `pin-verification.json`, immediately re-run correctly.
