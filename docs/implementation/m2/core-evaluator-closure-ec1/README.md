# The core evaluator closure — contract successor EC1

2026-10-02. Claude Opus 5.5, implementation lead. This is the identity contract successor that law X3d r8 item 3 step 1 requires. It is a lead decision under the owner's standing direction of 2026-09-30. It is flagged to the owner, who may override it, because it gives every core release a new evaluator closure and so new PlanIds and RunIds (see "Consequences"). The unit is PROPOSED and needs independent review and root assent before selection. It changes no schema shape, closure kind, domain, hash recipe, registry, generated code, inventory or product file.

## The defect it closes

X3d r7 item 3 step 1 says a Run's "evaluator closure equals the session's selected core closure". At product main a36da7c, `plan` in `crates/storage/src/commit.rs` enforces `run.evaluator_closure() == session.core_closure()`. The two ids come from different descriptors, so they can never be equal, and `prepare_commit` refuses every real `ReplayedRun`. X9-2 found it (EXIT-PLAN, "BLOCKER: commit closure binding").
- **The session side.** `CommitSession::core_closure` is `InitialCore::closure()`, the authenticated core inventory's `closure2:` over `{schemaVersion: 2, kind: "core", manifestDigest, tree, semanticVersion, protocolMajor, platform}` (`crates/security/src/trust/core_inventory.rs`, `bind`).
- **The run side.** Replay requires the seal's `evaluatorClosure` to be a `plan.semanticClosures` member naming a retained closure of `kind: "evaluator"` (`crates/evaluator/src/execution_inputs.rs`, `capture_header`; `execution_reader.rs`).

## What the design said, and why a successor is needed

No accepted text relates the two closures:
- The build plan binds the session to an "admitted producer closure" (line 51), and storage compares "producer selections" (line 67). It never says which closure that is.
- The identity contract makes `evaluation-seal.evaluatorClosure` kind `evaluator` (`closureKinds`) and Plan-selected (`closureMembership`). Its `closure.manifestDigest` is "the admitted component manifest body bytes", for every kind.
- The core inventory (463 item 3; core inventory contract v16) has no evaluator member. Component manifests can't describe one: the admitted shape fixes `kind: "component"` and `role: "analyzer"`. The build plan's component-manifest list (line 703) omits the evaluator.
- The preview contract's policy (D1-plan G28) says `.evaluator` = "pure core".

So no runtime value names an evaluator closure, and none can be derived under the current text. EC1 supplies the missing definition.

## The rule

A core release's evaluator closure is `closure2:` + H("closure", D′). D′ is the authenticated core inventory's selected-platform descriptor, the one security already projects for the core closure, with `kind` set to `"evaluator"` and every other member unchanged:
- `manifestDigest`: raw SHA-256 of the TR-CORE-signed inventory body (`opensip.metadata.inventory.1`), excluding its envelope;
- `tree`: the platform row's regular files as `{path, sha256, bytes}`;
- `semanticVersion`, `protocolMajor` and `platform`: the inventory's.

The core closure and the core evaluator closure of one release therefore differ only by `kind`. Security derives both from the one authenticated inventory it already holds. Nothing is read from a Run, a worker claim or a build-time string, and no new signed data, release format or trust change is needed.

## Overrides

Five text overrides on two accepted inputs. Each `after` keeps every word of its `before` text and only inserts text.

| Parent | Selector | Change |
|---|---|---|
| `foundation/identity-schemas.v3.json` | `/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact` | adds the kind-evaluator artifact: the TR-CORE-signed core inventory body |
| `foundation/identity-schemas.v3.json` | `/x-opensip-digest-domains/closureKinds/note` | adds the rule: the evaluator kind is the pure core, D′ is the core descriptor with kind evaluator, and the two ids differ only by kind |
| `identity-and-evidence.md` | line 273 | the `closure.manifestDigest` sentence names the kind-evaluator artifact |
| `identity-and-evidence.md` | line 278 | appends the "Core evaluator closure" paragraph: the rule, the retention consequence and the identity consequence |
| `identity-and-evidence.md` | line 455 | the `raw-artifact` row names the kind-evaluator artifact |

`closureKinds.byField` and `closureMembership` are unchanged. The evaluator closure is still kind `evaluator`, and it still must be Plan-selected. The kind list gains no `core`: the core descriptor stays security's own projection, outside the identity closure kinds.

No existing successor overrides any of these five selectors. The accepted ones on these parents are lines 45, 48, 51, 52, 58, 1272, 1314, 1635 and 1655, and the pointers `/$defs/program-predicate/description` and `.../outputSchemaDigest/x-opensip-digest/registeredBy/law`.

## Test vector

`evidence/vector.json` takes product fixture `crates/security/tests/fixtures/core-inventory318.ndjson`, case `baseline-macos` (a36da7c). It holds the 5990-byte inventory body, both descriptors, both ids and both descriptors' canonical SHA-256:
- core closure `closure2:54322a2c18a7ed6d5a2c92ab7e1204884e7095cfc254d40d352f879761fa118d`, the fixture's own expected value, recomputed here;
- core evaluator closure `closure2:7da97b9a4686fe5dc6ff69d83ddde230ac6895afb699717f2ef07a05810b89e2`, from the same descriptor with `kind: "evaluator"`.

`check_ec1.py` checks:
- the two descriptors are equal except `kind`, and the two ids differ;
- `manifestDigest` is the body's SHA-256;
- the evaluator descriptor fits the identity closure's closed shape and kind list;
- given the product checkout, all 53 accepted fixture cases recompute their core ids and give different evaluator ids.

X3d-3 reproduces the vector byte for byte in a Rust test of `core_inventory`.

## Consequences (disclosed)

- **Identity.** Every core release is a new evaluator closure. A Plan that a release evaluates selects it, so new PlanIds, RunIds and cache keys follow each release. That fits the identity contract's own rule ("Changing that selection changes the Plan's semantic inputs and identity"). It is the point flagged to the owner.
- **Retention.** Retention is `preimage` by default, and the identity walk retains every `raw-artifact` digest. So a Run that names the core evaluator closure retains the inventory body and every core tree file of that platform. The store keys them by raw SHA-256, so each release is stored once per store, not once per Run. This is the contract's existing rule ("A replayable Run retains them all"), applied to this kind.
- **Historical.** Historical closures, Plans and Runs keep their bytes and are not re-read.

## Rejected alternatives

- **The session exposes an evaluator closure that the core admits, as data.** No authenticated record names one, so there is nothing to expose without this definition.
- **Membership: the core closure contains the evaluator closure, judged by a tree-subset test.** No accepted text states it. It leaves `manifestDigest`, version and platform unbound, and a closure naming one shared data file would pass. It would be a new identity law anyway, and a weaker one.
- **A signed core-inventory member naming an evaluator closure.** It changes the signed release format (a successor to the core inventory contract v16, the inventory shape, 463h's builder and re-signing), and still needs this identity rule for the member's `manifestDigest`.
- **Shipping the evaluator as a TR-COMPONENT component.** It contradicts "evaluator = pure core" (G28) and the build plan's component list, and needs a successor to the analyzer-only component role.
- **Admitting kind `core` as an evaluator closure in replay.** It breaks `closureKinds` and the identity kind list.
- **Dropping X3d's check.** It removes the producer-selection binding that the build plan's line 67 requires.

## Product copies (for X3d-3)

These product files carry the identity closure annotations:
- `schemas/sources/identity-v3.schema.json` (line 287, the `manifestDigest` artifact text; the `closureKinds` note);
- `apps/report/src/generated/report.ts`, generated from it.

Following stage-meta-reference-selection-v1 ("current schema bytes/hash recipes/generated artifacts remain unchanged; explicit passage overrides will describe the new semantic owner"), they keep their bytes. They are annotation prose that no code dispatches on, so there is no generation-source, registry or drift change. `crates/identity/src/closure.rs`'s kind table and `crates/evaluator/src/view-joins-registry.json`'s `closureKinds.byField` are unchanged in meaning and bytes. No golden embeds a closure id that this rule changes. The code change is X3d-3's (law X3d r8 item 13).

## Evidence

- `evidence/build_ec1.py <product>` rebuilds `vector.json`, `successor.json` and the subject manifest deterministically.
- `evidence/check_ec1.py [<product>]` applies the overrides in memory, checks that each only inserts text, and checks the vector, as above.
- `evidence/verify_scratch.py <product>` runs the real verify_design with EC1 appended and a synthetic in-memory review and assent.
