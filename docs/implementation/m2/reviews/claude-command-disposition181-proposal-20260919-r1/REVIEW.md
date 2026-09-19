# Proposal assistance — 181 command classification: companion artifact vs. required inventory field

Reviewer: Claude. 2026-09-19. **Assistance only** — not a frozen-byte review, not acceptance, not implementation approval, no cumulative approval; the owner-authored frozen 181 needs its own review and nothing here binds it. No source, frozen, selected or repository file was edited; the draft companion exists only in memory inside my probe.
Trees used (both verified in my own reviews): reference = `claude-encoding180-20260919-r1/…/candidate` (inventory and schemas unchanged since 178); product = `claude-limits179-20260919-r1/…/product`.
Evidence: `claude-out/companion_probe.py` → `companion_probe.txt`. **r1 is preserved** (`companion_probe-r1.py`, `companion_probe-r1-THREE-UNDETECTED.txt`): three drift cases went undetected — two were defects in my own probe (substring flag match; digest taken from the file on disk instead of the mutated copy), one was a real design gap (§4, R11). A later edit of mine also broke the script's syntax once; fixed, no output was taken from the broken state.

## 0. Recommendation

**Yes — use the companion. It is the better architecture here, not merely the cheaper one**, and this reverses the field-in-inventory shape I sketched in my phases-181 assessment §5 (which I had already had to correct once for consumer impact). Reasons, all measured:

1. **The closed command set has five schema owners, not one.** `CommandName` (45 names) and a closed 14-field `Command` (`additionalProperties:false`) appear in: reference `schemas/command-inventory.schema.json` (`$id …:command-inventory`, schemaMajor 1), reference `schemas/evaluator3/…` (`…:evaluator3:command-inventory:3`), and product `inventory-v3`, `inventory-v4`, `command-inventory-v6` (ids `:3`, `:4`, `:6`). There are two live reference **instances** (`command-inventory.v1.json`, read by `check_workflows.v1.py`; `command-inventory.v3.json`, read by the v3 projection checkers and `foundation/check-current-profile.v3.py`), and the product `design-lock.json` pins the v3 instance by path. A required field means a new major in each lineage, 45-row edits in two instances, regenerated product contracts, registry/source-map/design-lock rebinding — for a fact that none of those consumers (renderers, goldens, parity) uses.
2. **All five schemas agree on the 45 names, and the two instances agree on everything classification depends on.** v1 and v3 differ only in `cli`, `parityFields`, `queryDispatch`; my *classification projection* — `(name, requestClass, authorizationClass, writesTrackedIntent, flag tokens of cli)` — has the **same digest for v1 and v3** (`4dc9d09cd8f0…`). One companion can therefore be bound to both reference instances (and later to the product's) without forking.
3. **Ownership is cleaner.** Active-slot disposition is a security S9.2 decision about an installation slot; the inventory is a workflows artifact about surfaces, renderers and goldens. 178 already had to say "S9.2 owns the closed table" in the workflows document. A security-owned companion keyed by the workflows-owned name set puts the fact with its owner and leaves the join explicit and checked.

What you give up, stated plainly: a second artifact can drift from the first, and schema `required` no longer gives totality for free. §3–§4 are the controls that buy that back; with them the companion's totality is *stronger* than a required field's, because a field can be present and wrong, whereas R3–R11 cross-check it against the inventory's own columns.

## 1. Precise shape I would choose

`docs/coop/design-corrections/security/active-slot-dispositions.v1.json` (security-owned; its schema in the security bundle), closed at every level:

- `schemaVersion: 1`; `owner: "security S9.2"`; `boundCommandNames`: the 45 names, **sorted, unique** (so the artifact is self-describing and R1 is checkable without the inventory);
- `boundClassificationProjection`: `{ "fields": ["name","requestClass","authorizationClass","writesTrackedIntent","cliFlagTokens"], "sha256": … }` — the projection recipe is part of the artifact, canonical JSON (foundation canonicaliser), so the digest is reproducible by any lane;
- `dispositions`: object keyed by command name, value `oneOf`
  - a string from the closed enum `executor | trust-only-reader-barrier | nonexecuting-mutator | reader | report-only | outside`, or
  - `{ "byMode": [ { "when": "default" | "--flag", "disposition": <enum **without** `executor`> } … ] }` — ≥2 entries, unique `when`, exactly one `default`. Making `executor` unrepresentable inside `byMode` encodes "no mode can select executor status" in the schema rather than in prose;
  - or, for a server entry, `{ "perRequest": <enum without executor>, "processStart": "outside" }` (§5);
- `observerSelector`: a closed map disposition → `observe` | `observe_for_nonexecuting_mutation` | `executor-phases` | `none`. This is the join that does not exist anywhere today; it lets the security lane assert that every disposition has exactly one selector and that the 173/175 observer's two functions are the only reader/mutator selectors.

Deliberately **not** in the artifact: authority, consent, lease sets, or any per-command prose. It classifies; it grants nothing (say so in its `standing`).

## 2. What changes in existing owners (validation-compatible)

- `authorizationClass` **description strings** in both reference schema copies (the two copies differ only in `$id`/title/description/`const` — they are not byte-identical, so edit each) — this is the D5 correction from my phases assessment: journaled intent's frozen set for recovery, newly admitted intent's set afterwards. Description-only edits keep every instance valid. **Caution:** they still change the schema files' bytes, so their pins move in the manifests, and the product's embedded `inventory-v3.schema.json` (sha `34e4b2c0…`) is already a *different file* from the reference evaluator3 schema (sha `6cd2302f…`) under the same `$id …:3`. I did not diff those two; the owner should know whether product-side copies are meant to track description text. If they are, this "description-only" edit has a product tail; if not, say so.
- S9.2 table and workflows §"Interrupted installation transitions": reduce to "the companion is authoritative; this table is its rendering", and have a checker render-and-compare so prose cannot drift (same pattern as `sync-public-details`).
- No inventory instance, golden, renderer or product schema changes.

## 3. Totality and consistency rules (run in my probe against the real inventory; baseline clean once `agent-serve` is decided)

| Rule | Statement |
|---|---|
| R1 | companion key set == closed `CommandName` enum (checked against **every** schema copy that carries the enum) |
| R2 | companion key set == each bound inventory instance's command names |
| R3 | `executor` ⇔ `authorizationClass == core-transition-leases` |
| R4 | `executor` never appears under `byMode`/`perRequest` (also schema-enforced) |
| R5 | `outside` ⇔ `requestClass == meta` (plus a server's `processStart`) |
| R6 | `trust-only-reader-barrier` ⇒ `requestClass == trust` |
| R7 | `report-only` ⇒ `authorizationClass == none` ∧ ¬`writesTrackedIntent` |
| R8 | `reader` ⇒ `requestClass ∈ {query, serve}` |
| R9 | every non-default `when` is a **tokenised** flag of that command's `cli` (my r1 used substring matching and accepted `--apply` inside `--apply-recovery` — write the rule on tokens) |
| R10 | `boundClassificationProjection.sha256` equals the recomputed projection of each bound instance |
| R11 | the closed policy sets — five executors, four trust-only, three report-only — equal an expectation **held by the security lane**, not derived from the artifact |

Distribution on today's inventory: 5 executor, 4 trust-only, 19 nonexecuting-mutator, 10 reader (incl. `agent-serve` per §5), 3 report-only, 3 outside, 1 byMode.

## 4. Drift behaviour (probe §C — each case mutates a copy)

| Drift | Caught by |
|---|---|
| inventory gains a command, companion not updated | R2, R10 |
| schema enum gains a name, no instance updated | R1 |
| inventory turns `purge` into a `core-transition-leases` command | R3, R10 |
| companion promotes `import` to `executor` | R3, R11 |
| companion lets a `repair-recover` mode select `executor` | R4 |
| companion names a flag the grammar lacks | R9 (only once tokenised) |
| companion demotes `trust-refresh` to ordinary mutator | **R11 only** |
| companion calls `analyze` a reader | R8 |
| inventory gains an unrelated optional flag | R10 (deliberately noisy: a new flag can be a new mode) |
| inventory changes a parity field | nothing (deliberately quiet) |

Two design points this exposed:
- **R11 is necessary.** Structural rules cannot tell the 178 trust-only choice from its more conservative alternative, because both are self-consistent. A policy choice needs a closed expectation in its owner's lane; otherwise a well-formed edit silently undoes it. The same is true of a required inventory field — the companion does not create this need, it just makes it visible.
- **Bind to a projection, not to whole-file digests.** A whole-file pin would need one entry per instance (v1, v3, later product v6), would churn on every parity/golden edit, and would say nothing about *why* a rebinding is needed. The projection digest is identical across v1/v3 today and moves exactly when a classification-relevant column moves. Whole-file custody is already provided by the source-pin manifests; do not duplicate it here.

Residual risk I cannot remove: a *new* inventory column that becomes classification-relevant later (say, a future `leaseMode`) is outside the projection until someone adds it. Mitigation: the projection's field list is in the artifact and R1/R2 fire on any new command, which is when such a column would arrive.

## 5. `agent serve`: process start vs. each brokered request

What the owners actually say (I found no other text; absence is reported as absence):
- inventory row: `requestClass: serve`, `steps: ["query"]`, `authorizationClass: none`, `formats: ["agent"]`, `writesTrackedIntent: false`, `repositoryExecution: never`, no flags;
- S7 modes: "`SHARED-READ` (any number; queries, rendering, doctor, **read-only agents**)"; S7 lease map: "`agent serve` **reads**" under SHARED-READ;
- build plan: `agent-serve` → M5, `crates/host/src/agent_server.rs`. No protocol text, no statement of lease lifetime, no mutating agent request anywhere.

Decision I recommend: **classify each brokered request, as `reader`; classify process start as `outside`.** Reasoning from existing law rather than preference:
1. 178's table "classifies every invocation that acquires a fence or project lease". A server that held a SHARED-READ lease for its lifetime would make every EXCLUSIVE core transition `PROJECT.BUSY` indefinitely, so leases must be per request; hence the lease-acquiring "invocation" *is* the request, and process start acquires nothing → `outside`, exactly like `help`.
2. A slot observation made at start would be stale by the first request: a transition can be journaled at any time after. The reader barrier is only sound if observed under the fence immediately before the lease it protects. So the server **must not cache a permit** across requests; each request re-observes; a busy/unknown-custody result is returned to that request and the server stays up.
3. "Underlying command" classification is unnecessary **today** because the only step is `query`. State the forward rule now: a future agent request that is not a read is classified as its underlying inventoried command and is a new inventory fact (`steps` changes → R10 trips → companion must be re-decided). It never inherits `reader` from the server entry, and never `executor` (R4 shape).
The owner should add one sentence to S7 or workflows §8 saying leases and slot observation are per brokered request; that sentence does not exist yet and the companion entry would otherwise be the only place the rule lives.

## 6. Consumer / versioning impact of the companion

- New: one security-owned JSON + its schema; security-lane checks R1–R11 + selector totality; pins in the security manifest (and wherever the security bundle is mirrored); workflows lane gains a read-only join (R1/R2) or, better, the security lane reads the inventory — it already reads other workflows files in the integration lane, so put the cross-owner join in **integration**, which exists for exactly this.
- Unchanged: both inventory instances, all five inventory schemas' validation behaviour, 45 goldens, renderers, product registry/design-lock (unless description text is mirrored — §2 caution).
- Versioning: `v1` of the companion; a new command or a changed policy choice is a new companion version with the old one retained, mirroring how the inventory lineages are kept. Product adoption later is one new registered schema id and a host classifier that reads it — additive, no closed schema reopened.
- Host classification remains owed; it would then have a machine source with a selector map instead of a markdown table.

## 7. Limits

I did not diff product `inventory-v3.schema.json` against the reference evaluator3 schema, read `check-workflow-projection.v3.py` beyond its inventory loads, or look for agent-protocol text outside `docs/v2/contracts/product-v1`, `docs/v2/architecture` and the inventory. The probe's rule set is a sketch to test the idea, not a proposed checker; R3–R8 encode correlations that hold on today's 45 rows and each needs an owner's sentence before it is law. No approval of any kind is implied.
