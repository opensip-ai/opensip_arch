# Independent review — frozen `carrier-guard-checkpoint-189`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 189 product bytes — adoption of reference 188's `cf_no_replace` guard in the current carrier DDL and the eight-object dispatch. My 188 T-1/W-1/W-2/W-3/N-1 are **not** claimed closed here (owner: reference 190) and are not assessed. No creator, upgrade, custody, full-host, formal-selection or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `d6ec27766ee65de6fd2d3facb7dce7e602dc28f731774043f41805dc3a7e62e7`, 4,260,048 B = request = `archive-pin.json` |
| Members | 411, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 352/352; none unpinned |
| Parent | equals **my own verified 187 extraction**; 349 unchanged; changed `journal_store.rs` (`f9f6c25571e2e8c3…`), `carrier_dispatch.rs` (`af7af363c68f790e…`), `bracketed_capture.rs` (`f7cd46c84bc5da52…`); fixtures unchanged |
| Production-part delta (everything before `#[cfg(test)]`) | `journal_store.rs`: the three guard lines only. `carrier_dispatch.rs`: comment, the eight-name list, `len() != 8`; the query keeps `COLLATE NOCASE` and is `LIMIT 9`. `bracketed_capture.rs`: **0** production lines (one test count) |
| Host receipt 119 | 232 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **141 security tests pass; strict workspace Clippy exit 0**.

## 3. Reference ↔ product DDL (`claude-out/io/ddl_equality.txt`)

`CURRENT_CARRIER_DDL` extracted from the Rust source is **byte-equal** to `grant-journal.carrier.v3.sql` in my verified 188 reference tree (12,149 bytes, `sha d6bca750567ce169…` both); the instantiated `sqlite_schema` rows are equal. `inherited_schema.rs` (format-1 and format-2 DDL) is byte-identical to my 187 product. So my 188 N-1 (one-object divergence between reference and product) ends with these bytes.

## 4. My probe (`claude-out/probes/dispatch_probe.rs.txt` → `io/dispatch.txt`)

Every case runs the real `capture()` on a real file; the main database bytes are compared around each read (all unchanged — reading never repairs).

| # | Case | Result |
|---|---|---|
| 0 | exact eight objects, unpublished / published | `Ok(objects=8, current=false)` / `Ok(objects=8, current=true)` |
| 1 | **each of the eight objects missing in turn**, unpublished and (where the table survives) published — 14 cases | all `PartialFootprint` |
| 2 | the seven-object draft (current DDL minus the guard), unpublished and **published** | `PartialFootprint` both — a carrier built from the 186/187 DDL is refused, not upgraded |
| 3 | guard present by name but wrong: `AFTER INSERT`; `RAISE(IGNORE)`; different message; `WHEN … AND 0`; one extra space; **upper-case name with the exact body**; attached to the other table; a VIEW named `cf_no_replace`; a TABLE named `cf_no_replace` | all `Read(Definition)` — name presence never admits a definition |
| 4 | a genuine **ninth** matching row: triggers have their own namespace, so `CREATE TABLE CF_NO_UPDATE(x)` coexists with the trigger (9 rows under `COLLATE NOCASE`), unpublished and published | `PartialFootprint` — the `LIMIT 9` overflow bound does its job; an unrelated extra index on the journal table → `Read(Definition)` |
| 5 | guard semantics on the product DDL, **UTF-8 / UTF-16le / UTF-16be** (encoding asserted after creation), `recursive_triggers=OFF`: `INSERT`, `REPLACE`, `INSERT OR REPLACE`, `INSERT OR IGNORE` of the singleton | all four refused in all three encodings, `ConstraintViolation` / extended **1811**, message "carrier format binding cannot be replaced"; row preserved; dispatch afterwards `Ok(objects=8, current=true)` |

Probe r1 is preserved (`dispatch-r1-ENCODING-NOT-SET.txt`, `dispatch_probe-r1.rs.txt`): my encoding setup left the fixture's sidecars beside the re-created file, so all three "encodings" were UTF-8 — it proved nothing about UTF-16. r2 removes the sidecars and asserts the encoding; r2 also adds the real ninth-row case after I realised a case-variant *trigger* cannot exist but a same-named *table* can.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`)

Baseline green; none failed to compile. **7/7 killed by the owner's tests**: guard removed from the DDL while dispatch expects eight; guard predicate never true; guard keyed on the wrong column; dispatch accepting seven; dispatch accepting eight-or-more; case-sensitive name lookup; guard name omitted from the names query. Two of these (the DDL/dispatch mismatches) are killed by broad adapter tests rather than a dedicated one, which is fine: a DDL/dispatch disagreement breaks everything, loudly.

## 6. Findings

None against the change. Notes:

### N-1 — refusal class for a guard-less carrier is `PartialFootprint`, for a wrong guard `Read(Definition)`
Both are refusals and neither repairs. They differ in public route only if a future mapper distinguishes "partial migration footprint" from "definition mismatch"; reference 188's checker expects `migration-footprint-corrupt` for the dropped-guard carrier in both open phases, and the product's two error kinds both have to land there or on the corresponding read-only standing. That mapping is owed host work, not part of 189; I note it so the seven-object draft does not quietly acquire a different public meaning from the other partial prefixes.

### N-2 — no deployed carrier can be stranded, because no creator exists
"Older seven-object drafts are refused, never upgraded" is safe today only because nothing in production creates a format-3 carrier (re-checked in this tree: production still executes `CURRENT_CARRIER_DDL` solely into an in-memory expectation connection). The README says so. When a creator lands, the eight-object definition is what it must write; there is no migration path from a seven-object carrier and none should be inferred.

### N-3 — scope
Format 1, format 2, `carrier_quarantine` and `carrier_capacity_pause` are byte-identical and remain unguardable by trigger, as inventoried. Disclosed; not a gap in this checkpoint.

## 7. Closure of earlier findings

| Finding | Status |
|---|---|
| 185 F-1 for `carrier_format` | **Closed in the product** (was closed at reference level in 188): schema-level, any connection, three encodings |
| 188 N-1 (reference/product DDL differ by one object) | **Closed by these bytes** — byte-equal |
| 188 T-1, W-1, W-2, W-3 | not addressed here, by the owner's statement; still open against the reference |
| 187 six storage guards | unchanged (storage crate byte-identical) |

## 8. Limits

Synthetic carriers on a local filesystem; bundled SQLite. I did not rebuild the owner's five compiled mutants or host receipt 119, did not exercise read-only recovery routes beyond `capture()`, and did not test big-endian hosts, WAL sidecar custody or concurrent writers.

## 9. Verdict (bounded)

**The product DDL is byte-equal to the reviewed 188 reference; the singleton guard refuses all four duplicate verbs in three encodings with recursive triggers off and preserves the row; dispatch admits exactly the eight exact definitions and refuses every partial prefix, the seven-object draft (published or not), every wrong-definition/case/kind variant and a genuine ninth name, without altering a byte. No finding.** No approval of a creator, upgrade, host mapping or cumulative readiness.
