# Independent review — inventory57 layout and composition380 source

Two **separate** verdicts. Neither selects owner379, S9.3, native qualification, or runtime27. Live product `bcd8208` (32/47) was **not** written. Root assent is **not** manufactured. 378 ACCEPT-UNIT and 379 REVIEW/findings remain unchanged (379 ADDENDUM is separate).

---

## 1. Additive inventory v57 — `ACCEPT-UNIT`

Layout packaging only. Parent is **selected inventory56** (live lock last candidate; **32** successors). Adds the two inert platform adapters already accepted as 375/378 **samples**. Does **not** qualify a native profile or grant root authority.

**subjectManifestSha256** `88f00ae7eb15825103a50986346161baa1a6b838e9ab3254f7c5bb915b024a96`  
`docs/implementation/m2/native-directory-inventory-v57-subject.json` **637** B, **3** members, sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `native-directory-inventory-v57/README.md` | 1263 | `684ed02ba357c4340180c18c0e2a51f1719d6bf79c394a31c215b834c6dd9ed0` |
| `native-directory-inventory-v57/successor.json` | 1785 | `e9e9424619258eef87d4b555c7e9f89860a88fd37d4d8499da5185d66e81082d` |
| `repository-file-inventory.v57.json` | 278524 | `f16422c6c4cc2f7dff272e5f25cfbbdf3b74cd01f334103eb57d09789560eb1e` |

`inventory_successor` checks: parent is selected v56 `8935bf9d…786c` / 277494 B; candidate path differs; both preservation flags true and observed; packages/DAG **20** and **9** pending strings identical; sorted unique additions; inherited rows unmutated.

| Claim | Check |
| --- | --- |
| 699 inherited | **0** mutated, **0** removed |
| 2 added | `directory_birth.rs`, `directory_volume.rs` (role adapter; descriptions deny pathname/custody/profile/authority) |
| 701 total | 699+2 |
| platform `lib.rs` / `filesystem.rs` inventory **rows** | unchanged by value (export bytes belong to 380, not this layout) |
| 211/218 obligations | carried UNRESOLVED, texts equal v56 |

Description overrides (lock parent v56) project by stable path: bootstrap **7**, report `package.json` **13**, `package.json` **496→498**, `imported-v1` **563→565**. Stored descriptions equal lock `before`.

`I/project-registry.v2` is **not** a source-inventory row and is not added here.

**requiredFindings:** none. `inventoryCandidateAssessment.verdict`: **ACCEPT**.

---

## 2. Full-source composition 380 — `ACCEPT-UNIT`

Complete 587-file reconstruction of accepted 378 source for staging. **Not** runtime27, **not** owner379, **not** qualification.

Archive `4bdbeb92…74b6` / **6856252 B / 601 members**; subject.json **113163** B `6f09409c83b94968686c6a9164c15ec3c05e5b3808df0c2d651284c33bf1b72a`; **0** pin mismatches. Product **587** files; every pin equals frozen 378 `delta.json` candidate list (**0** mismatches). vs 374: **2** changed (`lib.rs`, `filesystem.rs`) + **2** added (birth+volume) = **4** source changes; Cargo.lock and identity/platform `Cargo.toml` unchanged. Historical `design-lock.json` is in the 587 as provenance and was **not** copied onto live.

Peer 378 REVIEW `fa0ed4be…4d6d` / findings `919eff61…1cf0` and the four serial test logs are **byte-equal** this reviewer’s 378 artifacts. Author workspace `cargo check --locked --offline --workspace --all-targets` exit 0; cargo “Finished … in **20.52s**” (wrapper timer 20.81s). Source bytes match 378, so native filters and provider were **not** rerun.

**requiredFindings:** none.

---

## Scope / limits

Inventory57 + composition380 do not install product or bind runtime27. Runtime27 must receive its **own** formal unit review **after** inventory57 is selected. Owner379 law remains unselected. No commits, push, or live edits.
