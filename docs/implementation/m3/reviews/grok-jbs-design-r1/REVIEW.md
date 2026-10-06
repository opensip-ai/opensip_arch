# J-BS/S13 design r1

ACCEPT-DESIGN-UNIT. `j-bs-r1-subject.json` is 1448 bytes, sha256 `238093ec4bb5f266f2ecc32f8af12453e120ec43b276da630cb6fcf9d4a365c5`. Required findings: none.

This is the independent backup-status contract successor named by accepted M3-J1 r6 item 9 and item 13. It is lawful ahead of J3d. J3d remains the first emitter and still owns J-C18 and J-C19. This acceptance does not integrate J3d, run its end-to-end controls, or qualify the product.

## Schema copy

The candidate is a complete copy of the selected invocation5 schema. Removing `backupStatus` and the new `allOf` restores the parent JSON value for value. `$id` stays `urn:opensip:product-v1:workflows:evaluator3:invocation:5`, `schemaMajor` stays 5, and `RetentionDisclosure.required` stays `policy`, `provenance`, `firstUse`, and `storageRoot`. No `$ref` is added or retargeted.

`backupStatus` is an optional string whose enum is exactly `backed-up`, `not-backed-up`, and `unknown`. The `if`/`then`/`else` requires that member when `firstUse` is true and forbids it when `firstUse` is false. A missing `firstUse` still fails the existing required list. Null, boolean, numeric, and other string values are not a status. The schema does not infer presence from a detector, a minted intent, a storage scan, or a successful response.

Envelope7’s `retentionDisclosure` reference already names invocation5’s `RetentionDisclosure`. This successor does not copy or amend envelope7. The empty-errors `interrupted` branch still forbids `retentionDisclosure` at command-envelope v7 line 790. Product and architecture envelope bytes remain `42632` / `2cb6c8adaeeed4fc1b52573a291c1de5da512c0cf9ec1b1e0faa68313c4d436f`.

## Carrier law

CONTRACT.md matches J1 r6 item 9. `firstUse` is true exactly when this invocation’s creator performed the publication rename and `created` is `Some`, including every refusal after rename. `LostRace` and `NotPristine` create nothing, so `firstUse` stays false. The value is the classification retained on this invocation’s `CreationIntent`. Accepted 464 item 2 keeps the classifier constant: `classify_backup` returns `Unknown`, and `disclosed()` spells the three enum values. A missing detector does not become `not-backed-up`. The notice is still written and flushed before effects. The field adds a carrier and leaves 464 item 4’s acknowledgement unadded.

Once `created` is `Some`, every durable success or failure envelope carries `retentionDisclosure` as `durable-unbounded`, `DEFAULTED`, `firstUse` true, the intent’s disclosed `storageRoot`, and `backupStatus`, including attempt B’s post-rename refusals. The empty-errors interrupted branch is the exception and never carries that member; on a first-use interrupt the notice is the carrier. Otherwise durable disclosure starts only after R3, with `firstUse` false, the admitted account-derived root, and no `backupStatus`. Before R3 it is absent. Ephemeral disclosure starts after capture opens, with policy `ephemeral`, provenance `EXPLICIT-FLAG`, `firstUse` false, the temporary custody root, and no `backupStatus`. M3 adds no bounded retention, purge, or GC.

The generic shape permits all three spellings with any existing policy and provenance, provided the presence rule holds. Actual M3 emission remains `unknown`, and J3d enforces the policy, timing, and creation forms. These controls do not publish, create an installation, or emit an envelope.

## Successor form

Seven stage members match the subject pins, with no extra file. Candidates are those members except `successor.json`, with equal pins. `passageOverrides` is `[]`. `passageSupersessions` is omitted, which `verify_design` reads as an empty list. The sole parent is `docs/implementation/m1/source-selection-v2/schemas/sources/invocation.v5.schema.json`, 71161 bytes, sha256 `28aa0c42b05fa3ad13ae4d9aed1bac17983453577306b8e15678dc74af63f4fb`. That pin is the architecture source in the product source map and the registry’s invocation5 `sourceSha256`. The same pin is a candidate of the bound successor `docs/implementation/m2/initial-root-binding-owner-selection-v1/successor.json` (43921 bytes, `3a713c5c39a3feca2db3a05924103d49c10f11bef3c32f93d8c286fecd813e54`). The product schema file is still those parent bytes. The design lock is schemaVersion 4, with 106 contract successors, and this record is not yet among them. Inventory v166 remains the selected tail at 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. No new inventory path is in this unit.

The current product tree at `2146910cca62e2dce492e7b637e4c2d11390c419` is clean. The registry still names the existing eight generated outputs: `apps/report/src/generated/report.ts`, `crates/contracts/src/generated/evidence.rs`, `identity.rs`, `invocation.rs`, `mod.rs`, `output.rs`, `protocol.rs`, and `providers/typescript/src/generated/protocol.ts`. F8b’s generator-closure successor is already bound. The amended carrier binds only after a separate Grok review of the regeneration code leg, which re-pins changed schema, registry, and generator-closure bytes, with code and design-lock commits kept separate. This review does not accept that leg.

## Evidence

The pinned checker was rerun with `nice -n 10` and `python3.14 -I -B -S` against the named repositories. It exited 0, wrote nothing, and its 15750-byte stdout matched `checks.json`. It restored the parent by removing exactly the new field and rule, pinned the 128-file contracts snapshot `bd1ebac8f2efec1a5a88e35f8628c12ba67764c1e601e5aca773fecdf3178a82`, and did not call a generator, creator, or emitter. The run covered 72 presence combinations, 22 malformed or member controls, 3 empty-errors interrupted envelopes that validate without disclosure, and 6 interrupted envelopes that refuse disclosure. `noticeExecuted`, `emitterRan`, `generatorRan`, and `productQualification` are false. The OpenSIP installation path is absent.

Previously accepted units, and the held O1-a, J4a, E2s, and S-OP drafts, stay closed.
