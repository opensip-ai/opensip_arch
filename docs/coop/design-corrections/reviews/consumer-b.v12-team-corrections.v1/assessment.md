I’ll continue the same origin in the team-corrections workspace: verify team-input hashes, read the peer review in full, then correct only the syntax-code pilot.I’ll verify the team-input hashes, then read the peer review and diagnostic corrections in full before touching probes or the pilot.Hashes match. Next I’ll read the remaining peer review details and the kit laws for the seven refused boundaries, then path-correct scripts before changing the pilot.I'll continue the bounded syntax-code pilot in the team-corrections workspace: verify hashes, read the remaining peer review and kit laws, then path-correct scripts and preserve the original failing artifacts before any semantic edits.I'll verify the kit and team-input hashes, then read the remaining peer review and the kit laws for the refused boundaries.Hashes and peer review are in view. Next I’ll independently rehash the team-inputs and read the builder, replay, and kit-law files for the refused boundaries.Peer hashes match. I’ll read the builder, replay, and kit-law files next, then apply path corrections only in the team-corrections workspace.I’ll read the remaining kit laws and helper modules that govern inventories, membership, payloads, and proof reconstruction.Peer hashes and kit laws are confirmed. I’ll preserve the original failing artifacts, then path-correct only the scripts that will run.The path rewrite doubled the team-corrections suffix. I’ll restore the live scripts to a single correct root before any further edits.Path correction is in place. Next I’ll add the identity, occupancy, closure, and proof-reconstruction helpers, then update the builder.I’ll update the syntax-code builder next: grammar-tree retention, SubjectIdV1 payloads, body-identity frames, U-4 membership, and per-cell inventories.Replay and tamper both passed. I’ll derive remaining proof locators from admitted inputs, then collect NEW IDs and hashes for the review.Replay still matches after deriving locators from admitted inputs. I’ll write the pilot-correction review with every peer finding disposition and the NEW identities.**Verdict: `PILOT_READY_FOR_VALIDATOR_RECHECK`** — not whole-consumer acceptance, and not a reaffirmation of the historical `ACCEPT-RECONSTRUCTABLE`.

The original syntax-code export is preserved. A **new** Run was rebuilt against existing kit law, then replayed in a fresh process with a logical-result tamper distinct from a stale-hash control. D-CORR-1 (policy `$id` registry) and D-CORR-2 (seven-language host bundle) were **not** treated as consumer graph repairs. Empty peer `newMust`/`newShould` lists were not treated as admission.

## NEW identities

| Record | ID |
|---|---|
| Run | `run3:f2542b3afb9c5042438370893f9932830b4b6b1ac17f16299d35ed55d49db918` |
| Proof | `proof3:59d3b68084ae4c16c0b09956f24f3923801a82d361d9de8b362659129987e785` |
| Plan | `plan2:e3965f2fa9c900ed6a8214c12b2dc1f0123bef432113f2781688f8070323326d` |
| Snapshot | `snapshot2:f50135a27d89a1fa20bd4534f45d0e9f1633379a683b47c70dcec907e46911cd` (source bytes unchanged) |
| Store | SHA-256 `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` (867956 bytes, 79 blobs) |

Old failing store `8b0f6d826ed04f…` / Run `run3:aa19bedd…` is under `output/preserved-failures/syntax-code-original/`. Kit, team-inputs, and original `blind-review` bytes were not edited.

## Peer refusals addressed

- Grammar closure tree now contains bundleDigest `04e13aeb…` and normalizer specificationDigest `8fe22043…` (plus the rust grammar definition).
- DeclaresPayloadV1 is SubjectIdV1: `file:hello.rs` / `function:add`.
- L0 and L1 FACT-IDENTITY frames are retained; L0 identity is still `sha256:72a35a8b…` (recipe match plus frame custody).
- Syntax-only membership is `units=[]`, `unitOrdinal: null`, reason `grammar-only`.
- Inventories exist for `(0,0,file)`, `(1,0,file)`, `(1,0,package)` complete-empty, `(2,0,symbol)`.
- Fresh-process replay reconstructs the complete expected proof from admitted inputs and compares C (`e9492b04…`, equal).
- Tamper preserves citations, changes claimed verdict/value, remints proof identity `proof3:b32c360d…`, and refuses because independently derived verdict remains `pass`.

## From-scratch commands (measured exit 0)

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/runs/syntax-code.store.json

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/scripts/replay_from_export.py \
  --tamper \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v1/output/runs/syntax-code.store.json
```

## Still not done

TypeScript, Rust, syntax-data, and rust-partial Runs were not rebuilt. The original 123 requirements still stand; historical `requirement-status.json` over-claims are not reaffirmed. Component-manifest security profile, a generic digest-keyword engine, and real host/compiler enforcement remain notReached. A validator recheck can still refuse those.

Reviews: `output/pilot-correction-review.md` and `output/pilot-correction-review.json`.
