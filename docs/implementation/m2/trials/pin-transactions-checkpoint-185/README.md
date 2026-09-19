# Pin transactions checkpoint 185

Proposed private storage mechanism; unselected and uninstalled. Base184 has not conferred cumulative acceptance.

Within one BEGIN IMMEDIATE transaction, stage_pin_change reads the actual paired receipt/association Run and complete current pin inventory. It verifies expected contents, operation identity reuse, exact history schema and existing policy including first publication and independent legacy reductions. It stages immutable operational before/after facts and replaces the scoped current projection atomically. Noop adds no history. Every failure poisons the whole transaction, including earlier staged writes. A returned PinStage is staged state, never a committed receipt.

The private pin_change_facts schema is operational history, not semantic Fact/View objects or authority. It carries store/namespace/operation/Run/pin/before-kind/after-kind. History is append-only; renames produce release/create, kind changes one row. The existing reader is shared under the caller-owned transaction, preserving exact schema, unknown-kind and read-budget refusal.

Validation: 73 storage tests, strict workspace Clippy; baseline plus 12 compiled behavioral mutants killed (stale set, different Run, reused operation, first publication, policy, omitted/inverted/misbound history, scope, poisoning, schema and noop). Native host117 verifies 231 source inputs,37 fixtures,51 dependency archives,403 workspace tests and2 doctests, metadata/version/help and unchanged sources. Historical compile r1 failed because a sibling test helper was private; preserved beforeimage and replaced with local SQL assertion.

Host EXCLUSIVE lease/fence, current authorization, physical custody/sidecars, retained closure, semantic pin facts and mutation/publication receipts remain obligations. No production creator, importer or restore publisher is enabled. No claim of full M2, full project or independent acceptance.
