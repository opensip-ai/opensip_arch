# Canonical walk law — coauthor review

**Standing.** Actual Grok, bounded read-only coauthor review. Not design ACCEPT. Source hashes below. W files were not edited.

**Verdict: `CLARIFICATION_SOUND_WITH_ONE_SCOPE_AMENDMENT`.**

The proposed FIFO BFS + UTF-8 `fact2`-id hop order is the missing **reach** walk rule. It matches the current reference `directed_hops` / `reach_units` / `VisitBudget` / `finish_operation`. No other selector already owns that exact reach rule. Path already states most of the same walk; do not let “preserve discovered prefix” leak onto path.

## What is already owned vs the gap

| Topic | Owner today |
|---|---|
| Path BFS, `fact2` adjacency order, cap before first entry, `maxDepth` ends expansion, first target hit, zero-hop, **no path if cap before target** | contract §4 `graph.path` |
| Reach **result** order (endpoint tuple) | contract §3 |
| Visited cap before entering an unvisited endpoint | contract §5 |
| `viaFactId` = first reach on “the canonical walk”; omitted on `includeStart` depth-zero | schema `GraphReachRow.viaFactId` |
| Reach **walk** order (FIFO layer, which hop is tried first, which endpoint is entered when the cap bites, first-discovery depth/`viaFactId`) | **unstated** — only the Python |

§3’s endpoint-tuple sort is applied **after** discovery (`reach_units` sorts, then `apply_produced_cap` / paging). It does not choose who is discovered under a visited cap.

## Consistency with the reference model

- `directed_hops`: adjacency lists sorted by `factId.encode("utf-8")`.
- Both `path_unit` and `reach_units`: `deque.popleft()` BFS from admitted start; `if depth >= max_depth: continue` (do not expand at `maxDepth`); `VisitBudget.enter` before first entry; enqueue at parent depth + 1.
- Reach: first time an endpoint is entered, record depth and `viaFactId`; `includeStart` prepends `{depth: 0, endpoint: start}` with no `viaFactId`.
- Reach cap: first failed `enter` sets truncated and **stops**, keeping already-entered rows (canonical discovered prefix).
- Path cap: first failed `enter` **returns no units**. Contract: “If the cap hits before the target is reached, no path is claimed.”
- Path success: first BFS reach of the target returns that path and stops.

The proposal’s shared walk mechanics are correct. “Other backends must reproduce the same result/disclosure” restates existing GX-01 / cache-must-not-change-result; it does not add a new evaluator or bound.

## One amendment (reach prefix vs path)

The sentence “Stop at the first owed unvisited endpoint that cannot enter under the cap, preserving the canonical discovered prefix” is the **reach** law. Applied to path it would contradict §4 and `path_unit` (empty witness, not a prefix path).

The draft already says path keeps its own stopping law; make that bind the prefix sentence.

**Smallest amended paragraph:**

> The canonical bounded walk for `graph.path` and `graph.reach` uses a FIFO breadth-first frontier starting at the admitted start vertex. For each expanded vertex, process eligible directed hops in ascending UTF-8 `fact2`-id order. Enter each endpoint at most once, checking the visited cap before first entry; enqueue a newly reached endpoint with its parent depth plus one. Do not expand endpoints at `maxDepth`. For `graph.reach`, rows retain first-discovery depth and `viaFactId`, then are sorted by the public endpoint tuple before the produced-item prefix and paging. `includeStart` adds the depth-zero row with no `viaFactId`. Reach stops at the first owed unvisited endpoint that cannot enter under the cap, preserving the canonical discovered prefix. `graph.path` keeps its zero-hop law and its first canonical target hit; if the cap hits before the target is entered, no path is claimed and unfinished extra branches are not owed. Other backend strategies must reproduce the same result and disclosure for the declared bounds; physical acceleration stays private.

Hop order is **`fact2` id**, not the public neighbor-row tuple (universe/kind/native id then `fact2`). Those two orders diverge under a cap (witness below).

## “Unique” vs “selected” shortest path

§4 now says the first BFS reach is “the **unique** shortest hop-count path and the lex-least `fact2` sequence among those shortest paths.” Multiple shortest paths can exist. The algorithm **selects** one: a shortest hop-count path, and among those the lex-least `fact2` sequence (which this BFS + `fact2`-sorted hops implements). Root’s **`selected` shortest hop-count path** is the right word. Keep the lex-least tie-break; do not drop it.

## Algorithm-only witness (not a model import)

Start `S`. Two outgoing hops: `fact2:aa… → z-high`, `fact2:bb… → a-low`. `maxVisitedNodes = 2` (start plus one). Independent FIFO BFS:

| Hop processing order | Entered under cap | Reach row |
|---|---|---|
| UTF-8 `fact2` id (proposed / current model) | `S`, `z-high` | `z-high` via `fact2:aa…` |
| Public endpoint-tuple then `fact2` | `S`, `a-low` | `a-low` via `fact2:bb…` |

Same cap, same graph, different bounded membership. That is why reach must name hop order, not only result sort.

Cycle: re-entry of an already entered vertex is skipped (`seen` / enter-at-most-once); no extra bound invented.

## Not invented

No new numeric bounds, no backend data-structure constraint, no change to neighbor public order, no new evaluator.

## Hashes (current `query-successor.v1` workflows)

| File | SHA-256 | bytes |
|---|---|---|
| `query-projection-contract.v3.md` | `2a8f6d44615591df33955dee53d04b25bc8fcf6dab159041f2ad47916f62551b` | 17418 |
| `query_projection_model.v3.py` | `8da16bea35af5f8ecb2518973ce6b668a94fa0d14c860d89c37173a9f99c28e1` | 52898 |
| `schemas/evaluator3/graph-query.schema.json` | `e14ea2f9d4d03ef23182cab6a7279c846ee552ebbdd7fc3082184660cd7354c1` | 35567 |
