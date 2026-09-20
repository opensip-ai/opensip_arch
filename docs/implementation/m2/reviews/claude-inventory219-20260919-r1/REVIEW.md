# Independent review — frozen `file-inventory-checkpoint-219`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen proposed `repository-file-inventory.v52.json` — an additive file inventory over the **proposed** v51, covering the 356 product files of frozen 218. Membership, ownership, naming, description and package-edge scope only. It installs and selects nothing; **v51 and v52 are both proposals, not selections** (my 212 standing correction applies here from the start), and this is not acceptance of 218, of the unselected chain, of native targets, or cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `fd16a7fcad26e1b6cccaadcac6f681004559c358983c37f0eb924bebe098a090`, 48,200 B = request = `archive-pin.json` |
| Members | 11, all regular/safe, each rehashed against `subject.json` from the tar before extraction; re-verified at the end |
| Parent inventory | `parent-inventory.v51.json` SHA-256 `9c0e1aa9…e504d` — **byte-identical to the v51 frozen in my own verified 212 extraction**, and to the repository working-tree v51. Its own `standing` begins "PROPOSED cumulative private checkpoint211 inventory…" |
| Product basis | `product-inputs218.json` byte-identical to `product-inputs.json` of **my own verified 218 extraction**; `product218/*` and `inventory212/*` pin files byte-identical to those trials' |
| Working tree | an identical `repository-file-inventory.v52.json` sits beside v51 in `docs/implementation/m2/` (byte-equal to the frozen one), as the request states; presence is not selection |

## 2. Independent structural checks (`probes/check219.py` → `io/check219.json`; computed from the JSON and my 218 tree, not from `validation.json`)
| Check | Result |
|---|---|
| v51 rows in v52 | 469/469 equal as objects, **same order**; none changed or dropped |
| Added rows | exactly one: `crates/platform/src/account.rs`; no duplicate among 470 |
| `packages` | 20, array identical to v51 (ids, paths, kinds, purposes, dependency allowances, standing); `schemaVersion` unchanged |
| `pendingDecisions` | v51's retained verbatim as a prefix; one appended: "Review account.rs OS mechanism and this additive inventory, then bind the eventual cumulative runtime/source selection. No OS sample is an admitted actor/home context; no Linux or release qualification is inferred." |
| Membership vs my 218 extraction | 356 product files, **0 unlisted**; the added row exists in 218 |
| Ownership | every row's `package` equals its longest-prefix package — 0 mismatches across all 470 |
| Role / naming | `adapter` — an existing v51 role and the same role as its siblings `platform/src/macos.rs`, `filesystem.rs`, `filesystem/path_binding.rs`, `locks.rs`; file sits directly under the platform crate's `src/` like the other OS mechanisms. No `factory`, no new package, `generated:false` |
| Cargo edges | **17** actual internal edges, **0 outside the unchanged allowances**; my edge set equals `validation.json`'s. `account.rs` needs no new dependency: `libc` was already a target-specific dependency of `opensip-platform` for `cfg(any(macos, linux))`, and `platform/Cargo.toml` and `Cargo.lock` are **byte-identical to 217** |
| Speculative names | none of capsule / trust-state / continuity / slot / selection / fence / lineage added |

## 3. Description against the module
Inventory: "Sample real/effective OS credentials and obtain the real account home through bounded reentrant account-database lookup. No environment-selected identity, group authorization, elevated-execution approval, credential lifetime exclusion or directory custody."
Module (218, reviewed in full there): `getuid`/`geteuid` before and after; `getpwuid_r` of the **real** UID with 1…64 KiB caller buffers; no `HOME`/`USER`/`SUDO_UID` fallback; effective-UID mismatch reported, not endorsed; no group observation; "Samples … do not exclude credential ABA … or establish filesystem custody". **Each clause of the description corresponds to a property of the code, and each exclusion to an explicit disclaimer in it**; "obtain" (not "query") is apt given the provider/cache activity the header discloses. The row claims no consumer, and 218 has none.

## 4. Findings
None. Notes:
- **N-1** the description will stay accurate for successor 220 (native home/ERANGE tests and redacted `Debug` are test/diagnostic changes to the same file, not a change of role or boundary), so v52 need not be re-issued for it; a new file or a changed public surface would.
- **N-2** as in 212: the added row's `standing` string differs from inherited rows' ("proposed; private checkpoint218 account observation, not selected or installed") — honest, and three distinct standing spellings now coexist; harmless unless something compares them for equality.
- **N-3** the row inventories a file that compiles on Linux (`cfg(any(macos, linux))`) while only macOS was exercised; the appended pending decision says so ("no Linux … qualification is inferred"), which is the right place for it.

## 5. Limits
JSON, manifests and the module header only; nothing built or run. The description check relies on my 218 review of `account.rs` rather than a second line-by-line reading. v51's own correctness was reviewed in 212 and is not re-derived.

## 6. Verdict (bounded)
**v52 is a strictly additive successor of the proposed v51: 469 rows and 20 package records unchanged and in order, exactly one new row for the one file 218 added, correct owning package, an existing role consistent with its sibling OS adapters, a description that matches the module clause by clause including its non-authority boundaries, no new dependency (manifests byte-identical to 217) and all 17 Cargo edges within the unchanged allowances. No finding.** Inventory review only — not selection of v51 or v52, not acceptance of 218 or the unselected chain, and not cumulative approval.
