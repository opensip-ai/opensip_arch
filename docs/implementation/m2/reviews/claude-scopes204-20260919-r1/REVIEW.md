# Independent review — frozen `location-scopes-checkpoint-204`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: one private file, `lifecycle/src/locations.rs` — the refactor answering my 200 W-1. Pure syntax helpers: no I/O, admission, custody or lease is claimed and none is reviewed as such. The owner ran no host or mutation pass for 204 and says so; host 126 qualifies 202 only. No selection, installation or cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `e51272afc99f3804a56528e706a413dcd57755a3e4d38cb9975f06fd5a081a6e`, 4,088,032 B = request = `archive-pin.json` |
| Members | 369, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 354/354, none unpinned |
| Parent | equals **my own verified 202 extraction**; exactly one file changed; the shipped `locations-before204.rs` is byte-identical to my 202 copy |

## 2. Owner checks re-run (fresh scratch, offline, locked)
lifecycle 15/15; strict **workspace** Clippy clean.

## 3. What changed (diff read in full)
`LocationNames{namespace, store}` is replaced by three types: `NamespaceNames{namespace}` (namespace dir, both leases, journal + sidecars, witness, trust-domain floor), `StoreNames{store}` (root, marker), and `LedgerNames<'a>{&NamespaceNames, &StoreNames}` obtainable **only** through `namespace.in_store(&store)`; its three ledger methods take no arguments, so there is no way to supply a second namespace. Parsers, literals and `ExecutionComponent::staging_relative` are untouched. The file contains no `pub` at all (0 occurrences) — fields and types are module-private. The doc comment on `LedgerNames` says what the borrow is *not*: "ordinary Rust borrowing, not an operation lease: a future sealed host context must establish admission and retain the required custody and leases". No dummy identifiers appear anywhere; lease paths are now reachable with no store value.

## 4. My checks
- **Paths unchanged — differential, not by inspection.** The same probe body was spliced into a scratch copy of my verified **202** tree (old API) and of **204** (new API) and run over 400 generated `(N, S, G)` triples × 13 roles: **5,200 paths, byte-identical** (`io/paths_202.txt` = `io/paths_204.txt`, same SHA-256). The old probe cannot compile against 204 nor the new against 202, so neither output can have come from the wrong tree. *(First attempt shared one cargo target directory between the two trees and the parent run reused the 204 test binary, producing no parent output; caught because the file was missing, re-run with a separate fresh target — log kept as `build204-parent202.log`, good run `-r2.log`.)*
- **Grammar** is byte-for-byte the 200 code (diff shows no change above the types), so my 24,009-input oracle agreement from the 200 review carries over; the retained grammar and exact-role tests still assert every literal.
- **No scope mixing**: the adapted test shows `n.in_store(&a)` vs `n.in_store(&b)` differ only in the store leg, `other.in_store(&a)` differs in the namespace leg, pairing leaves all namespace roles and both markers unchanged, and the floor stays outside both namespace dir and store. The 200 oddity I cited (`a.marker_relative() == c.marker_relative()` across namespaces) is gone because the marker no longer has a namespace at all.
- **No false capability claim**: nothing is exported; comments disclaim admission on all three types.

## 5. Findings
None. Notes for the first caller:
- **N-1** when visibility is raised (`pub(crate)`), keep the **fields** private and `in_store` the only constructor of `LedgerNames`; a `pub(crate)` struct literal would reopen the mixing this refactor closes.
- **N-2** `NamespaceNames`/`StoreNames` are not `Clone`. Good default: one value per admitted binding; a transition needing two stores borrows the same `NamespaceNames` twice, which is exactly the intended shape.
- **N-3** 202 W-2 still stands: `"store-instance.v1"` is a literal here and again in `storage/store_root.rs`; `StoreNames::marker_relative` is now the natural single owner once the `lifecycle→storage` edge exists.
- **N-4** I ran no mutants: the only behaviour is the path table, which the differential covers completely for the sampled domain, and the type-level property is enforced by the compiler rather than by tests.

## 6. Limits
macOS; scratch copies only (`build204-*`, `target204-*`, created after asserting absence); nothing deleted; build targets excluded from `hashes.txt`. No host-isolation run by me or the owner for these bytes.

## 7. Verdict (bounded)
**204 closes 200 W-1 exactly: namespace roles need no store, store roles need no namespace, ledger roles exist only as a borrowed pairing with no override, and every one of 5,200 sampled role paths is byte-identical to the 202 parent. Nothing is exported and the borrow is explicitly disclaimed as a lease or authority.** No approval of admission, custody, leases, installation or cumulative readiness.
