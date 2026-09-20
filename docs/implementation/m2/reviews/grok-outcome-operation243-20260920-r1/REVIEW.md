# Independent review — primary prepared outcome composition 243 r1

**Standing:** bounded code review of frozen primary 243 r1 over pinned 239 r2, 241 r1, and 238 r2. **Not** cumulative approval, source/runtime selection, native custody, live census, 51-command installation, or authenticated effects. 242 is **not** integrated here. Archived 241/242 reports were not edited.

Python 3.12.13 `-I -B`. Scripts’ hard-coded `/tmp/opensip-implementation` roots were redirected in a **copy**; frozen outputs were not overwritten.

---

## Verification

Frozen `outcome-operation-integration-reference-wip-243-r1`: **9370848 B, 1439 members, SHA256 `d207de6c…d18f`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 1439/1439.

Nested archives inside `inputs/` match the already-reviewed pins:

| Nested | SHA256 | Bytes | Members |
|---|---|---|---|
| 239 r2 | `822e3a9f…48c3` | 7058132 | 1486 |
| 241 r1 | `393a4999…b447` | 30244 | 26 |
| 238 r2 | `04a73688…872e` | 20908 | 52 |

238’s test loader also requires sibling `m2-producer-integration-reference-237` (237 `dca9a702…d050` from the verified 239 nested input). Repro tree used those sibling names.

`frozen-candidate.json`: **1338 files** (239 r2 had 1335). **16** SHA deltas vs 239 r2: three new files (`trust_outcome_reference.py`, `trust-command-actions.v1.json`, `trust-command-outcome-bindings.v1.md`) plus schema, six producer modules, operation module, operation source-pins, and five pin inventories. Base archive SHA is 239 r2.

`pin-changes.json`: **59** explicit pin-row updates across all five inventories (foundation 1304, evaluator3 1308, native 1304, security 1311, workflows 1305). Every `after` hash matches the live candidate file.

`trust-operation-source-pins.v1.json` lists the 125-def schema, command-actions, outcome, record/input/event/graph/restore, and unchanged metadata index `be87c4c3…2f1b7`.

---

## Outcome module vs 241

`trust_outcome_reference.py` `ec30ef59…c189`. Compared to archived 241 `outcome_reference.py` `77a74d3f…b2fb`:

- **Removed:** `workflows_model` import, `current_project_scope`, `INSTALLATION_OPERATIONS`. No security→workflow cycle. No 242 `scope_for_command` / `current_key`.
- **Unchanged bodies:** `installation_scope` / `installation_key` / `bind_params` / `prepare_outcome` / `bind_outcome` / `bind_descriptor`.
- Reader is the relocated 241 `record_reader` as `trust_record_reference.py` (`00ad3a34…e6df`): **125 `$defs`**, **134** registry sites, `TrustCommandOutcomeV1` in `ROOTS`, optional `commandOutcome`.
- Graph algorithm from `class Refusal` is **byte-identical** to 239; only the reader PIN/path prefix changes.

Schema `commandOutcome` is still **not** required. Old descriptors remain structurally legal.

---

## Optional outcome composition (what 243 actually adds)

Shared `Operation` (source `bf92db33…fb3b`) still owns one `Budget`. New behavior:

- **`InputWork._load`:** typed `TrustCommandOutcomeV1` → `parse=False` capture of `operation` then `bind_outcome`. Typed `PublicationDescriptorV1` **with** `commandOutcome` → `bind_descriptor_raw` (outcome then operation, same budget, including repeated reference edges).
- **`parse=False`:** returns raw bytes, not shape admission. Probe: load `OperationInputV1` with `parse=False` yields the original bytes.
- **`Operation.walk`:** full structural `G.walk`, then joins every visited outcome and every D that carries `commandOutcome`. Result standing becomes `structural-dependencies-and-prepared-outcome-bindings-only` with `outcomeBindings`. D without `commandOutcome` is skipped at the join (not treated as completion).
- **`Operation.proof`:** restore/event bridge still uses **this** `input_work`, so every link/terminal descriptor with `commandOutcome` is bound. Nested proof too.
- **`Operation.events`:** if `commandOutcome` is present, charges one extra edge, retains canonical D bytes, binds, **then** `bind_events`. No commandOutcome → join skipped.
- No new budget profile, no counter reset, no collection fallback. Guard failure still latches `operation-budget-closed`.
- Low-level 237 graph/restore `Work()` APIs remain separate structural entry points. Native still must construct **one** `Operation`.

A coherent asserted COMPLETED binding still returns `prepared-bindings-only` and the three pending owners, never a replay permission.

---

## Reproduction

Redirected `check_primary243.py` / `check_variants243.py` (frozen result dirs not overwritten):

| Corpus | Result |
|---|---|
| Predecessor 238 r3 cases via `Q.O =` 243 primary | **46/46** exact |
| New outcome composition cases | **28/28** byte-equal frozen `operation-check-r1/report.json` |
| Binding-omission variants | **4/4** core fields equal frozen `outcome-variants-r1/results.json` |

`sourceSha256` of the primary is `bf92db33…fb3b`. Variant file SHAs differ because the harness rewrites `S = Path(...)` to the local security dir.

New 28 cover: combined walk+bind (2 objects / **3 edges** — the extra edge is the join’s operation reload); shared object/byte/edge budgets; asserted-COMPLETED remains pending; structurally valid graph with bad `receiptId` → `receipt-identity` then fail-stop; typed input/descriptor/events hooks; missing outcome capture; restore (direct and nested) with every link/terminal corrupted separately.

**Syntax typo:** `check_primary243-before-syntax.py` and `check-r1.stderr` retain `else2` (`SyntaxError`). Current `check_primary243.py` is `else 2`. Production modules were not relaxed to pass a test.

Four omission variants each delete one hook (`InputWork` outcome bind, descriptor outcome bind, walk visit loop, events join). Baseline refuses `receipt-identity`; mutant admits. Binding controls, not effect exploits.

---

## Independent probes

| Probe | Result |
|---|---|
| `parse=False` OperationInput load | raw bytes, equal to store |
| `bind_descriptor` on old D (no `commandOutcome`) | `command-outcome-missing` |
| Walk/events of 241 fixture D without event bytes | `operation-capture-cap` (structural missing child; join not claimed) |
| `prepare_outcome('trust-import', challenge-bytes)` | `command-action-binding` |
| Walk after coherent store rewrite + recomputed receipt id | `outcome-store-binding` |
| Walk / typed input with outcome present and operation bytes missing | `operation-capture-cap` |
| Walk counters on good challenge outcome | objects 2, edges 3 |
| 243 operation/outcome import 242 adapter? | no |

Do **not** treat prepared bindings as authenticated effects.

---

## Seven current root receipts (read, not rerun)

| Lane | Frozen r1 receipt |
|---|---|
| foundation | `PASS` 231/231 |
| native | `cases` 477/477 |
| workflows | 2193/2193, `failed: []` |
| security | `counts` 580/580 |
| carrier | 479/479 |
| integration | 1787/1787 |
| envelope | explicit 168, composition/drift 147, recorded differential 1803, actual replay crypto 55, fuzz 6000; `passed: true` |

Envelope `sourceBindings` for the 243 primary, outcome module, 125-def schema, and outcome-bindings prose match candidate bytes. Suites were **not** rerun. Inherited candidate receipts keep historical standing; these owner reports are not cryptographic or native qualification.

---

## Remaining (do not count closed)

- **242** current scope / immutable issuer is not in this snapshot. Host issuers still do not call `bind_step` / `current_key`.
- **store-gc:** 243 does not select a sweep owner. Root’s follow-through (unavailable current GC key pending an explicit owner; partial/pass outcomes, no cross-namespace atomicity; lock class not derived from scope kind) is **outside these frozen bytes** and was not reviewed here.
- Semantic requested-effect proof; original-scope lookup/census/final durability; 51-command transport/inventory/authorization/locks/results; scoped old-T; native one-`Operation` actor; M3–M6.
- Low-level graph/restore defaults remain unintegrated (238 F-2).

---

## Verdict

- [x] Archive/pins/1338-file candidate/16 deltas/59 pin updates/125 defs/134 sites verified.
- [x] 46 predecessor cases exact; 28 new cases and 4 omission variants reproduced. `else2` typo is test-driver only.
- [x] Optional outcome composition matches the stated boundary: typed input/descriptor joins, walk-then-join, proof via same `InputWork`, events bind-before-replay, shared budget, `parse=False` is raw, old D is not completion, pending standing only.
- [x] Independent bad receipt/action/store/missing-ref probes refuse at graph/input/events hooks. 242 not imported.
- [ ] **Not** implementation approval, command installation, native custody, or 242/store-gc closure.
