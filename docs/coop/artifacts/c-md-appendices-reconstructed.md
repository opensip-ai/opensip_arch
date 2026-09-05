# Reconstruction — `c.md` Appendices A and B

**Status:** RECONSTRUCTION, not the original. The source file
`docs/internal/coop/c.md` was deleted on 2026-07-29 and is unrecoverable
(`docs/internal/` is gitignored — `.gitignore:91` — so there is no git history,
and no copy exists on disk or in Trash).

**Provenance:** Reconstructed by Agent 3 from having read `c.md` in full earlier
in the same session, immediately after the loss was detected.

**Fidelity, stated honestly:**

| Part | Confidence | Basis |
|------|------------|-------|
| Appendix A SQL blocks | **High** | Structured, distinctive content |
| Appendix A query-mapping table | **High** | Structured, distinctive content |
| Appendix A "three things to get right" | **High** (substance), medium (exact wording) | Distinctive argument, paraphrase risk on phrasing |
| Appendix B mapping table | **High** | Structured table; one cell independently re-verified below |
| Prose framing / status notes | **Medium** — substance preserved, wording approximate | Recalled, not quoted |

**Independent verification of the one checkable claim inside Appendix B:**
`packages/contracts/src/index.ts` is **exactly 423 lines** on `main`, matching
c.md's "423 lines of re-exports" verbatim. That is a distinctive number and is
good evidence the recall of this file is sound.

**A note on the LOC figures c.md cited elsewhere** (not part of these
appendices, but relevant if they are quoted from this file): c.md's per-package
LOC counted **src + test**. Src-only counts on `main` are roughly half
(`core` ~39.7k src, `graph/engine` ~37.3k src, `cli` ~78.0k src). ADR count is
181 today vs c.md's 183. Do not mix the two accounting bases.

---

## Appendix A — Fact schema sketch

> **Status (c.md's own framing): sketch, not a design.** Included so the claims
> in section 2 ("one fact store, many queries") could be pressure-tested rather
> than taken on faith. The real schema needs the answer to product call #3
> (how much cross-language rule portability matters), plus a pass against the
> checks that would strain it hardest.

```sql
-- Content-addressed. content_hash is the invalidation key for everything
-- derived from this file.
file(
  id, path, lang, content_hash, size, is_generated, is_test
)

-- One row per declaration. body_hash powers clone detection;
-- signature_hash powers API-change detection.
symbol(
  id, file_id, kind,            -- function | class | method | type | const | module
  name, qualified_name,
  span_start, span_end,
  visibility,                   -- exported | public | private | local
  signature_hash, body_hash,
  parent_symbol_id              -- nesting: methods within classes, closures
)

-- One row per use. resolved_symbol_id null = unresolved (dynamic, external,
-- or extractor limitation) — the null rate is a quality metric worth tracking.
reference(
  id, from_symbol_id, from_file_id,
  to_name, resolved_symbol_id,
  kind,                         -- call | import | type_ref | inherit | instantiate
  span_start, span_end
)

import(
  id, file_id, module_spec, resolved_file_id, imported_names, is_type_only
)

-- Escape hatch for text/regex rules and for surfacing evidence excerpts.
-- NOT a general filesystem handle — rules request spans, they do not read files.
span_text(file_id, span_start, span_end) -> text
```

### Query mappings for section 2's table

```text
call graph          reference WHERE kind='call'
                      JOIN symbol ON resolved_symbol_id

dead code / yagni   symbol WHERE visibility='exported'
                      AND id NOT IN (SELECT resolved_symbol_id FROM reference)
                      AND file.is_test = false

duplicate bodies    symbol GROUP BY body_hash HAVING count(*) > 1
                      (exact); minhash bucket for near-duplicate

blast radius        recursive CTE over reference, seeded at symbol X,
                      direction = inbound

impact (--changed)  files with changed content_hash
                      → symbols in them
                      → inbound transitive closure

select_tests        impact closure ∩ symbol WHERE file.is_test = true

package cycles      SCC over import edges, grouped by owning package
```

### The three things this schema must get right

1. **`resolved_symbol_id` nullability.** Unresolved references are the honest
   representation of dynamic dispatch and external calls. The *rate* of nulls
   per language is the single best quality signal for an extractor and should be
   surfaced, not hidden.
2. **`body_hash` normalization policy.** Whitespace? Comments? Identifier
   renaming? This determines whether clone detection finds real duplication or
   noise, and it is the one decision hardest to change later because baselines
   depend on it.
3. **The escape hatch's shape.** `span_text` as a *pull* API (rules request
   spans) rather than a filesystem handle is what keeps rules capability-free.
   If a rule can ask for arbitrary file content, the sandbox is theatre.

---

## Appendix B — Mapping: current concept → proposed home

| Current | Proposed |
| --- | --- |
| `core` (72k, "kernel") | `kernel` (fact + run model, errors, IDs, wire types) — genuinely small |
| `contracts` (423-line re-export facade) | *deleted* — no cross-package cycles to break |
| `Tool` interface | split: `Extractor` / `Rule` / `Projection` |
| `ToolCliContext` seams | *deleted* — host owns I/O; rules are pure |
| `RunScope` + ALS + `globalThis` pin | explicit context in-process; wire protocol out-of-process |
| `SCOPE_ABI_VERSION` | protocol version on the wire |
| `graph/engine` (73k) | fact store + traversal queries |
| `yagni` engine | a query |
| `clone-detection` | a fact (`body_hash`) + a grouping query |
| `shared-analysis/impact` | a query |
| baseline plane (2 tables, 4 seams, per-tool strategies) | queries over run history + host-side fingerprint functions |
| `StoredSession` + `StoredSessionHostMetrics` + catalogs | one `Run` record |
| freshness facets, `g1:` generations, cursors | content-hash freshness |
| `targeting`, `codebase`, `config`, `output`, `format`, `session-store`, `cli-live`, `cli-ui` | internal modules of `apps/cli` |
| external scanner adapters | **kept as-is** — correct shape |
| check packs | tier-1 declarative rules + tier-2 narrow-API imperative |
| `mcp` | kept as a package (separate process) — but a thin projection over runs |

---

## Amendments by later three-agent consensus

These are **not** part of the reconstruction. They are recorded here so the
appendices are usable without being misleading: several c.md positions were
amended or superseded during the deliberation. Cited by agreement-item number
in `agents-log.md`.

| c.md position | Consensus disposition |
|---------------|----------------------|
| Content-hash freshness replaces coverage machinery | **Partially rejected.** Coverage survives as a multi-axis, typed concern; it is a content-addressed artifact with its own digest and a set commitment for exact membership (items 19, 34). Content hashing is necessary but insufficient — negative queries and cross-file semantic universes must enter derivation keys. |
| `reference` schema as drawn | **Amended.** Facts must carry `resolution` and `confidence` provenance, because the TS semantic guest is an **extractor-tier** producer of resolved references, not a rule capability (item 23). |
| Type-aware checks are the fact store's main limit | **Measured and largely dissolved.** The checker-dependent floor is 1 of 141 check files (~0.7%) — `null-safety`. The escape hatch is for imperative complexity, not type fidelity (items 23, 32). |
| All rules out-of-process | **Amended to tiered execution.** ~64% of checks are pure text/pattern, so the in-process declarative matcher is the main path, not a concession. |
| `span_text` pull API keeps rules capability-free | **Directionally right, but a signature is not a boundary.** Ambient module resolution defeats in-language confinement; enforcement requires trusted TCB, an opaque capability in a restricted module graph, or out-of-process (items 32, 36). |
| ~6–8 packages | **Superseded.** The governing count is **public versioned contracts** (initial target ≤5); crate count is build engineering (item 29). |
| `contracts` deleted; `mcp` kept | Consistent with the target; sequencing is governed by the D19 strangler slices, and package deletion must never lead the replacement capability. |
| Rules classified by "needs an AST" | **Superseded by predicate-based classification** — reachability/authority/capability predicates must run over resolved-reference facts regardless of how simple their surface pattern looks (item 33). |

## Why this file exists

The durability risk was flagged in the log two turns before it materialised:
sealed decisions and source material living only in a gitignored tree that
CLAUDE.md explicitly says may be deleted at any time. Appendix A is the natural
seed for a future fact-schema artifact and Appendix B feeds D19 strangler
mapping, so these two were worth recovering; the rest of `c.md` is substantially
absorbed into `agents-log.md`.

Anything that graduates from here into `docs/internal/coop/architecture/` or
`docs/decisions/` should be re-derived and re-verified against source, not
inherited from this reconstruction on trust.
