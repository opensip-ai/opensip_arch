# Independent review — frozen `file-inventory-checkpoint-212`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen proposed `repository-file-inventory.v51.json` — an **additive** file inventory over the selected v50, describing the 355 product files of frozen 211. An inventory records location, owning package, role and purpose. **Additive-inventory review only**: it installs nothing, selects nothing, changes no runtime/design selector, and is not acceptance of the unselected candidate chain (product `fa72e50` remains installed) nor cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `63a19174ccab901c09498533fc67e637788e2718bf172bc79033ffb727058c47`, 47,108 B = request = `archive-pin.json` |
| Members | 10, all regular/safe, each rehashed against `subject.json` from the tar before extraction; re-verified at the end |
| Parent inventory | `parent-inventory.v50.json` SHA-256 `69c54484…d344b` — **byte-identical to the repository's selected `docs/implementation/m2/repository-file-inventory.v50.json`** and to `inputs.json`'s pin |
| Product basis | `product-inputs211.json` byte-identical to `product-inputs.json` of **my own verified 211 extraction**; `product211/archive-pin.json` and `subject.json` byte-identical to the 211 trial's |

## 2. Independent structural checks (`probes/check212.py` → `io/check212.json`; computed from the JSON and from my 211 tree, not from `validation.json`)
| Check | Result |
|---|---|
| v50 rows present unchanged in v51 | 444/444 byte-equal as objects, **in the same order**; none changed, none dropped |
| Added rows | exactly 25; no duplicate path among 469 |
| `packages` | 20, array identical to v50 (ids, paths, kinds, purposes, dependency allowances, standing) |
| `schemaVersion` | unchanged |
| `pendingDecisions` | v50's nine retained verbatim as a prefix; one appended ("Review this additive cumulative private checkpoint211 inventory, including test-only immutable_guards.rs, and bind it to the eventual selected source/runtime manifest. No planned file entry proves implementation, custody or product readiness.") |
| Source membership vs my 211 extraction | 355 product files, **0 not listed**; all 25 added rows exist in 211; 330 of the 444 inherited rows exist in 211 — the other 114 are planned-only rows inherited from v50, untouched |
| Package ownership | for all 469 rows the `package` equals the package whose `path` is the longest prefix of the file — 0 mismatches, inherited and added |
| Role vocabulary | the nine roles used by added rows (`adapter, algorithm, codec, composition, fixture, module, store, test, validator`) are all existing v50 roles; **no `factory`** added or renamed; `generated:false` for all 25 |
| Cargo edges | 11 crates with manifests, **17 actual internal edges** (incl. dev/build sections), **0 outside the unchanged package allowances**; my edge set equals `validation.json`'s. The one edge new since v50's product basis — `opensip-storage → opensip-security` (202) — was already permitted by the unchanged plan |

## 3. Descriptions against the modules (`io/rows_vs_modules.txt`: each added row beside the module's own `//!` header, size and visibility counts)
All 25 descriptions agree with what the files say and do, and consistently carry the owner's limiting clauses rather than capability claims. Points I checked specifically:
- **`ledger_store/immutable_guards.rs`** — role `test`; the module is declared `#[cfg(test)] mod immutable_guards;` (`ledger_store.rs` l.2369–2370), contains only a helper and two `#[test]` functions, header "Schema-level regressions: adversarial SQL, not production mutation APIs". Correctly inventoried as test code living under `src/`.
- **Private boundaries** — 20 of the 20 added Rust files have **zero `pub` items** except `platform/filesystem/path_binding.rs` (5 `pub`: it is the platform mechanism other crates consume; role `adapter`, same as its parent `filesystem.rs`). The security journal readers and storage recovery helpers expose only `pub(crate)/pub(super)`. No description calls any of them an API.
- **Role consistency with parents** — journal readers under `journal_store.rs` (`store`) are `store`/`validator`/`codec`/`composition`/`adapter` by what each does; `trust/role_machine.rs` is `algorithm` like `trust_time.rs`; `store_root.rs` `codec`; `pin_inventory.rs` `algorithm`; `locations.rs` `module` (pure syntax — deliberately not `service` like `leases.rs`). File names follow existing owner submodules (`journal_store/*`, `ledger_store/*`, `filesystem/*`, `trust/*`).
- **Descriptions reflect the latest frozen state**: `locations.rs` — "independent namespace/store scope… borrowing do not establish admitted bindings" (204); `bound_operational.rs` — "retain the exact opened descriptor" (205); `store_root.rs` — "delegate file policy to security" (210); `role_machine.rs` — "joint CORE/INDEX/COMPONENT continuation policy. Guard inputs are asserted" (211).
- **Fixtures** — five data files, each described as reference-derived cases with an explicit non-authority clause.
- **No speculative 203/209 persistence files**: a name scan for capsule / trust-state / continuity / active-slot / selection-pair / source-fence / lineage finds nothing new. The only hits, `lifecycle/src/installation.rs` and `transitions.rs`, are *inherited v50 planned rows*, unchanged.

## 4. Findings
None. Notes:
- **N-1** an identical `repository-file-inventory.v51.json` already sits in the repository working tree beside v50 (byte-equal to the frozen one). That is consistent with "proposal"; selection is a separate act, and nothing I can see treats v51 as selected. Worth keeping that distinction visible wherever "the inventory" is cited.
- **N-2** the added rows' `standing` string ("proposed; private checkpoint211 inventory, not installed or independently accepted") differs from the inherited rows' plain "proposed". Honest and harmless; if any tool ever compares `standing` by equality it will see two values.
- **N-3** the inventory does not (and should not) say which planned-only rows are now obsolete. 114 inherited rows have no file in 211; some (e.g. `lifecycle/src/installation.rs`) are named by other owners as future homes. No action for an additive successor.

## 5. Limits
JSON, manifests and module headers only; nothing built or run (no behaviour is in scope). "Descriptions agree with modules" is my reading of each header plus visibility counts, not a line-by-line re-review of 25 files — most were reviewed in their own frozen checkpoints, which this does not re-open. I did not re-derive v50's own correctness.

## 6. Verdict (bounded)
**v51 is a strictly additive successor of the selected v50: 444 rows and 20 package records unchanged and in order, 25 new rows that exactly cover the 211 files v50 lacked, correct owning packages, existing role vocabulary only, no factory, no speculative persistence names, `immutable_guards.rs` correctly recorded as test code, and all 17 actual Cargo edges inside the unchanged allowances. No finding.** This is review of the additive inventory only — not selection of v51, not acceptance of the candidate chain, and not cumulative approval.
