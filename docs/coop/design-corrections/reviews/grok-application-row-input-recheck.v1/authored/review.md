# Application row-input integration recheck (read-only; not ACCEPT)

**Standing.** Bounded Grok recheck of root’s integration of the row-map-prep findings. Not independent design acceptance, not application, not qualification, not assembly. Final independent application review remains required.

**Write scope.** `/tmp/opensip-design-corrections/grok-application-row-input-recheck.v1` only (review + probes). No frozen/live/source edits, no blind12 reads, no commit/push.

---

## Verdict

The **required** prep items are integrated:

- Draft v6 preserves v5 except the intended DR-104 JSON / DR-123 prose+JSON / proposal hash / correction record.
- DR-104 JSON matches the corrected markdown (selected input and output identity majors).
- DR-123 one-clause query major3 / concrete run3 / complete query-response parity is in **both** prose and JSON.
- `application_rows.load_rows(--draft)` admits all 28 IDs/order with exact markdown-table equality, `productQualified is False`, `independentGrade == PENDING`, **before** `out.mkdir()`.
- Old absolute `application-assembly.v1/row-map-draft.json` load is **gone**.
- Historical row-map bytes remain `01e37c6f…`.
- Six disposable checker cases PASS; 17 draft before/proposed hashes PASS.

**Portability gap (real, CLI-adaptable).** `check-application-rows.v1.py` hardcodes `/tmp/opensip-design-corrections/application-draft.v6` and has no `--draft`. Copied into final support it still reads the live draft path, so a PASS from that copy does not prove reproduction from support inputs. `load_rows` requires a **draft-shaped** tree (`readiness-row-map.proposed.json` plus the register file). Assembler support stores JSON as `readiness-row-map.input.json` and does not copy the markdown next to it. Root can add CLI `--draft` pointing at a reconstructed draft-shaped tree; that is not a product-qualification demand.

No application ACCEPT.

---

## Read scope

**Read.** draft v6 (row map, register, correction records, documentation-proposal, beforeimage-check.query24.v6); draft v5 for preserve-diff; `application_rows.py`; `check-application-rows.v1.py/json`; `assemble-records.successor.v1.py`; `prepare-validation.py`; `row-map-input-before.v1/*`; `row-map-input-integration.v1.json`; historical `application-assembly.v1/row-map-draft.json`; `coverage_contract.py` IDs; `current-status.json` draft pointer only.

**Not read.** Active blind12; consumer-B; independent-design review body; frozen24 mutation; live source.

**Not done.** Full reference suites, fake binding, actual assemble.

---

## Required findings vs integration

| Prep finding | Integrated? | Evidence |
|---|---|---|
| DR-104 JSON still major2 identity names | **Yes** | v6 JSON+markdown: `the selected input and output identity majors…`. `load_rows(v6)` ADMIT. |
| Assembler L248 absolute historical load retains disposition | **Yes** | Diff vs `row-map-input-before.v1`: load moved to `application_rows.load_rows(draft_base, C.CONDITION2_IDS)` **before** `out.mkdir()`; absolute path removed. |
| Optional DR-123 query-owner3 clause | **Yes** | Both table cell and JSON: `Graph queries use schema major3, resolve to a concrete run3, and preserve complete query-response parity.` |
| Preserve historical JSON `01e37c6f…` | **Yes** | Unchanged in assembly.v1, successor-root `row-map-draft.json`, before.v1, and draft v5 proposed. v6 proposed is new `b98e5126…`. |
| Fail closed on markdown/JSON drift | **Yes** | Helper asserts cell-for-cell equality and ID/order. Checker: stale-disposition REFUSE `Markdown/JSON disposition drift: DR-104`. |

Draft v6 vs v5 file tree: changed only `documentation-proposal.json`, `files/docs/v2/architecture/08-decision-and-readiness-register.md`, `readiness-row-map.proposed.json`. Added `beforeimage-check.query24.v6.json`, `row-map-input-correction.v1.json`. No v5-only files dropped.

---

## Hashes

| Artifact | SHA-256 |
|---|---|
| Historical row-map (unchanged) | `01e37c6f09053ff8885214c7a72a7715ce45b111cad0654ab9f19ee9bde75fcf` |
| draft v6 `readiness-row-map.proposed.json` | `b98e5126d01430b54f29073b68057d08d72604003df6a3533ab15291fc6087ba` |
| v6 register file | `60bf12da7bff0bd500194b2a987bef4a0e3fe69067ecaf43d99bfc30e8e4d4c2` |
| `application_rows.py` | `dfcac2f2b6fddc5d9dc5779f05b936091255e40ab3caffdb41bfc3e557a22b25` |
| `assemble-records.successor.v1.py` | `bdab482b56e36688bdc3f4d8bd4bd32cbe3b225fd1bbc8bcbaa9a3ce0b831981` |
| `prepare-validation.py` | `f063ac8a97d18f0c63cd16a586056ffdd79cf8b4b446cdf7d798dadcd95a83df` |
| `check-application-rows.v1.py` | `706b22c4c01359a36c2b48105812d12dadc0bcdbed488568c1097c6dac41aa09` |
| `check-application-rows.v1.json` | `c797b17329878187e64b1da229ec3e42c03a560844ba8317f9c859fb60eda89f` |
| Frozen subject (status pin only) | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |

17 `documentation-proposal.json` `proposedSha256` values match the v6 `files/` bytes. `beforeimage-check.query24.v6.json` `passed=true`, 17 checks.

---

## Controls

Official six disposable cases (rerun, report hash unchanged): valid-current-draft ADMIT; stale-disposition / missing-row / duplicate-row / qualification-claim / acceptance-claim REFUSE.

Additional probes (`probes/probe-results.json`):

- JSON ID order swap → REFUSE `Condition2 row IDs/order changed`.
- Duplicate disposition header → REFUSE `Expected one current disposition table`.
- Extra row **inside** the current two-column table → REFUSE `Markdown disposition IDs/order changed` (`probes/corrected-table-failures.json`).
- Markdown disposition order swap → REFUSE same.
- Reconstruct draft-shaped tree (JSON name + register path) → ADMIT 28.
- Owner-sentence rewrite (assembler later step) does **not** break table equality.

First extra-row probe ADMITted because it edited the **historical** multi-column `| DR-133 |` row, which `load_rows` does not parse. That is a probe construction error, not a helper miss of the current table.

---

## Portability gap

**Checker default path cannot reproduce from support inputs alone.**

1. `check-application-rows.v1.py` L14: `source = Path('/tmp/opensip-design-corrections/application-draft.v6')`. No argparse.
2. `prepare-validation.py` copies helper, checker, report, `row-map-input-before.v1`, integration record into validation support. It does **not** copy the draft JSON+markdown pair.
3. Assembler copies admitted JSON to `out/support/readiness-row-map.input.json` (different filename) plus the correction record. Markdown lives under `out/files/docs/v2/architecture/08-decision-and-readiness-register.md` after copytree, not beside that JSON.
4. `load_rows` opens `draft/readiness-row-map.proposed.json` and that register path. A support dir with only `readiness-row-map.input.json` raises `FileNotFoundError`.
5. Running the checker from a support copy still hits live draft v6, so exit 0 is not support-input evidence.

**Narrow fix for root (CLI, not product law):** add `--draft` (and maybe `--ids` from coverage_contract). Point it at a reconstructed draft-shaped tree: `readiness-row-map.proposed.json` + `files/docs/v2/architecture/08-decision-and-readiness-register.md`. If support keeps the renamed JSON, either also copy it as `proposed.json` or accept an explicit path. Do not require live `/tmp/.../application-draft.v6` after the draft moves.

This does **not** undo the required integration. It does not demand G-gate qualification.

---

## Limits

- Did not assemble, bind, or run full reference suites.
- Did not grade DR-201–205 or reopen all 28 successor sections.
- Assembler still stamps emitted `independentGrade=ACCEPT-DESIGN` after admitting PENDING draft; that is the existing assembly binding, not a draft self-grade. Final application review still binds the outcome.
- `current-status.json`: `readyForAssembly=false`, `actualApplicationPerformed=false`, `currentDraft` = draft v6.

**acceptanceClaimed:** false.
