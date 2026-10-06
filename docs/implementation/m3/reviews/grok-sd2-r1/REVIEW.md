# SD-2 r1

ACCEPT-DESIGN-UNIT. `sd-2-subject.json` is 1392 bytes, sha256 `673d2276fef2f20968e2e9624b1e1f6446b32f3f7d3bc63bb9aa4c4b19c25d7d`. Required findings: none.

This is the independent manifest-owner confirmation record named by accepted M3-D r5 item 9 and item 29, and listed for drafting in M3-PLAN r10 Next item 3. It is a proposed design record. Effect still requires lead assent and a design-lock binding commit. Acceptance here does not bind the lock, put M3-L in effect, authorize D2a integration, or qualify the product.

## Confirmed tuples

CONTRACT.md confirms the two published native selections, with integer majors taken from native-evidence §9.1:

| Selection | role | roleSubprotocol | subprotocolVersion |
|---|---|---|---|
| TypeScript protocol 2 | analyzer | typescript-semantic | 2 |
| Rust protocol 3 | analyzer | rust-semantic | 3 |

The selected role is the admitted `manifest.role`. DR-103 keeps that vocabulary host-owned, and a manifest cannot mint a role. The selected major equals admitted `manifest.compatibility.providerProtocol`. `roleSubprotocol` and `subprotocolVersion` are the opaque tokens of the capability declaration that supports the already pinned selection. The host does not infer a provider from a display name, `stableId`, path, file extension, or the first capability row. `hello.subprotocolOffers` contains exactly that one tuple, and `select` names the same tuple. Hello and select confirm it under existing CCv5 rules. There is no runtime choice and no TypeScript/Rust frame translation.

The retained preview witness stays `analyzer` / `typescript` / `1`. CCv5 lines 199–201 call that handshake synthetic and non-shipping. It is not a TypeScript protocol 2 or Rust protocol 3 token.

A host-built tuple that differs from the admitted selection stays on M3-D r5’s existing `session-spec-inconsistent` route: host-invariant, before spawn or any frame. A provider-spoken mismatch stays on the existing control-refusal or provider-protocol route. The record adds no error, exit, public detail, or wire classification. The checker’s local fates are `MATCH`, `SELECTION`, `MANIFEST`, `CAPABILITY`, `OFFER`, and `SELECT`.

## Preview schema limitation

The completed manifest schema’s capability `oneOf` has five branches, and every branch is `roleSubprotocol` `typescript` with `subprotocolVersion` `1`: `typescript.imports`, `typescript.references`, `typescript.calls`, `typescript.types`, and `typescript.reachability`. The generated component-manifest shape admits that same exclusive set (`node_72` through `node_76`) and does not contain `typescript-semantic` or `rust-semantic`. SD-2 does not admit native declarations against those branches and does not widen the schema. Upstream manifest and role-scoped capability admission remains owed before an actual native session.

The confirmation applies only once a separately admitted pinned native selection exists. It is not an existing full native manifest, session, codec, provider launch, or qualification. An empty `capabilities` array remains a valid general declaration: DR-103 says so, the completed schema’s capabilities array has no `minItems`, and generated `node_11` allows an empty array. An empty list cannot supply one of these native sessions. That projection is the local fate `CAPABILITY`, a session-selection failure, not a new general manifest refusal.

## Successor form

The seven subject members match their pins, and the stage contains no extra file. The successor’s candidates are those members except `successor.json`, with equal pins. `passageOverrides` is `[]`. `passageSupersessions` is omitted, which `verify_design` reads as an empty list. The two parents are DR-103 `component-manifest-schemas.v11.json` (139492 bytes, `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`) and `native-evidence.md` (329013 bytes, `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`). Both are accepted source-manifest rows in `candidate-subject.v45.json`, and the native-evidence row is also a design-lock input. MD5, ML5, CCv5, and the completed manifest schema are evidence pins, not successor parents and not new effective L authorities.

Product base `6b60cfd8db9aea979444c7bb266211fde4d58827` and architecture base `da7a3795bb7191317105f8bea74075235f73f646` are the current HEADs. The product tree is clean. `control-v3.schema.json` and `component_manifest_shape.rs` match the subject pins; hello, confirm, and select type `subprotocolVersion` as an integer of at least 1, and the shape still requires `role` (`node_8`, const `analyzer`) and integer `compatibility.providerProtocol` (`node_30` / `node_1`). Inventory v166 remains the selected tail at 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, and is not a member of this unit. The design lock is schemaVersion 4, with 105 contract successors and no SD-2 record yet. No product code, generated schema, registry, inventory, or contract parent is edited.

## Evidence

Twenty-one unique synthetic projections are pinned: 3 `MATCH`, 6 `SELECTION`, 3 `MANIFEST`, 4 `CAPABILITY`, 3 `OFFER`, and 2 `SELECT`. The three positive cases are the TypeScript confirmation, the Rust confirmation, and a later matching declaration that is not chosen because it is first. Negatives cover the preview tuple, a crossed native major, a minted role, boolean, float, and string majors, manifest role and major disagreement, an empty or wrong capability, an empty offer, two offers, and a select that disagrees or carries an extra member.

The pinned checker was rerun with `nice -n 10`, `python3.14 -I -B`, and the named architecture and product repositories. It exited 0, wrote nothing, and its 1923-byte stdout matched `checks.json`. It checked 8 authority pins. `manifestAdmitted`, `sessionAdmitted`, `codecRan`, `providerLaunched`, and `productQualification` are false. The OpenSIP installation path is absent. These controls are not full manifest admission and not CC frame or state conformance.

X5 and R3’s missing manifest-owner confirmation closes only when this record is accepted and bound. D2a, D2b, D4, and the rest of L’s gate stay open. Full M3 completion and product qualification stay false. Previously accepted units, and the held O1-a, J4a, E2s, and S-OP drafts, stay closed.
