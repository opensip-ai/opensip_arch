# Independent review — frozen `physical-locations-checkpoint-200`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 200 product bytes — private syntactic location components (`lifecycle/src/locations.rs`, new), the `Unlinked` refusal (my 198 W-1), and the ledger stage comment (198 T-1 residue). These helpers do no I/O and claim no admission, marker reading, custody or lease; I review them as that. No host rerun is claimed by the owner and none was done here. No selection, installation or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `18b8c64d05e0022cefe79cbd63ee8fd80a54684744e6fbe531c9569297cd6f21`, 4,158,856 B = request = `archive-pin.json` |
| Members | 412, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 353/353, none unpinned |
| Parent | equals **my own verified 198 extraction**; 3 modified (`security/custody.rs`, `storage/ledger_store.rs`, `lifecycle/lib.rs`) + 1 added (`lifecycle/locations.rs`); none removed |
| Reference pin | `reference201/archive-pin.json` = `ebd5b03f…eeeb5` = the 201 archive I verified and reviewed |

## 2. Owner checks re-run (fresh uniquely named scratch, offline, locked)
lifecycle 15/15, security 159/159, storage 87/87, strict **workspace** Clippy clean (`claude-out/owner/`).

## 3. What the source does (read in full)
- Four closed parsers: namespace = 36 bytes, hyphens at 8/13/18/23, `4` at 14, `[89ab]` at 19, otherwise `[0-9a-f]`; store = 32 lowercase hex; execution = `exec1_` + 32 lowercase hex; generation = non-empty, ≤19 digits, no leading zero, ASCII digits, `i64` > 0, re-emitted with `Display` (so the path spelling is canonical by construction, not by trusting the input). The length test precedes the byte indexing, so multi-byte input cannot panic.
- All role paths are built from fixed literals and parsed components; every result is relative with only `Normal` components (asserted). `ledger.sqlite` lives under `stores/S/projects/N/`; leases, journal, sidecars and witness under `host/projects/N/`; floors under `trust/journal-floors/N/G.floor`; marker `stores/S/store-instance.v1`; staging `stores/.staging/E`. **Every row equals the frozen 201 location table.**
- Everything is private; `lib.rs` registers the module under `#[allow(dead_code)]`; no production caller. No `std::fs`, no `Path::exists`, no environment access.
- Custody: `links == 0` in `OperationalFile` scope → `Refusal::Unlinked` (`"UNLINKED"`), checked before the generic `links != 1` → `HardLinked`; configuration scope untouched. The comment states the 195 reason (a last SQLite closer can unlink a sidecar under a retained descriptor) and "Do not retry here". The real-descriptor test now unlinks both names and observes `Unlinked`.
- Ledger control stage now carries the journal stage's sentence "may execute connection-control SQL, never data/schema queries".

## 4. My adversarial checks

**Differential grammar** (`probes/grammar_corpus.py`, `grammar200_probe.rs.txt`): 24,009 generated strings (valid values and single/double mutations: case, deletions, insertions, separators, dot segments, percent forms, non-ASCII digits and letters, doubled values, boundary integers 2⁶³−1/2⁶³) judged by an **independent oracle** written from the 201 grammar text (anchored ASCII regexes; integer bound) and by the product parsers: **byte-identical decisions**, 7,443 accepts (`io/grammar_oracle.tsv` = `io/grammar_product.tsv`). NUL/newline/tab cases are excluded from my TSV corpus; the owner test covers them.

**Mutants** (26, all compiled; `io/mutation200.json`): **24 killed** — version nibble, variant set widened and narrowed, uppercase in UUID and hex, hyphen position, hex length, optional `exec1_`, leading zero, `+` sign; floor back inside the namespace directory (the 199 placement), floor inside the store, floor without namespace, ledger without namespace, ledger outside the store, ledger WAL in the journal directory, leases swapped, journal sidecar suffixes swapped, staging not under `.staging`, marker misplaced; custody 198 behaviour restored, configuration scope changed (killed by the **reference corpus** test — so "historical behaviour unchanged" is differential, not just asserted), `links ≥ 2 → Unlinked`, `links == 0` admitted. **2 survived, both predicted equivalent**: removing `value <= 0` (unreachable: `"0…"` already fails the leading-zero rule, a sign fails the digit rule) and removing the 19-byte cap (20+ digits already fail `i64` parsing). Harmless redundancy; say so in a comment or drop them.

Namespace-restore isolation is pinned three ways by the owner test: floor path does not start with the namespace path, nor the store path, and does start with `trust/journal-floors` — my two placement mutants die on it.

## 5. Findings

No defect. One design point for the next step and notes.

### W-1 (low; design, before these helpers get a caller) — the type couples roles that the law keeps apart
`LocationNames` needs **both** a namespace and a store for every leg. But the lease, journal, witness and floor legs are store-independent *by law* (201: "Store transitions neither move nor replace those carriers"), and the marker leg is namespace-independent (store admission reads it before any namespace is in play; S7 enumerates *all* namespaces for a transition). Consequences once there is a real caller: (a) a reader that needs only `writer.lease` must present some store value — an invitation to pass a placeholder; (b) a store transition holds two stores and one namespace, so it builds two `LocationNames` from two separately supplied namespace values, which is exactly the "independent namespace strings for leases and data" that 201 forbids constructors to accept — nothing in the type stops `a.writer_lease_relative()` being paired with `c.ledger_relative()`. The test `assert_eq!(a.marker_relative(), c.marker_relative())` already shows the marker ignoring half the struct. A shape that matches the law: `NamespaceNames { namespace }` owning the namespace and trust legs; `StoreNames { store }` owning root and marker; and ledger legs only from `namespace.in_store(&store)` borrowing the one namespace value. Purely syntactic still — but then "one N feeds every role" is enforced by construction rather than by the caller's care. Not a defect in 200, which has no caller.

### Notes
- **N-1** `UNLINKED` is a new private code string with no counterpart in the reference discovery vocabulary (`HARD_LINKED` etc. appear in the model and `discovery-cases`; `UNLINKED` does not). Correct while it is reachable only in the operational scope, which no reference corpus covers; if `Refusal::code()` ever feeds a public projection, the operational scope needs its own mapping decision rather than leaking this label. The host mapper is owed anyway.
- **N-2** the staging helper hangs off `ExecutionComponent` alone — right for 201 ("addressed only by the original admitted E"), and correctly there is no ancestor-carrier helper (201's deliberate boundary).
- **N-3** paths are built with `PathBuf::join` of `String`s and compared via `to_str()`; Unix-only by construction, consistent with the rest of the crate.
- **N-4** the inventory-successor note is accurate about what remains (an additive successor to the selected v50 inventory before installation); I did not review inventory bytes because none changed.

## 6. Closure
198 **W-1 closed** (behaviour, label, synthetic and real-descriptor tests; four custody mutants killed). 198 **T-1 residue closed** (comment added; the busy read-back position remains untestable by natural fault, as both of us recorded). 199 F-1 / 201 placement is what the code emits, with regressions.

## 7. Limits and disclosure
macOS, unprivileged. Mutants and probes ran only in `build200-*`/`target200-*` scratch copies created after asserting absence and restored by copying frozen bytes; nothing was deleted; no compile failure occurred. My first probe command was rejected by the tool harness for containing literal non-ASCII characters and was rewritten with escapes before anything ran. Build targets are excluded from `hashes.txt`. No host-isolation run; no file-system behaviour is exercised by these helpers, so none was tested.

## 8. Verdict (bounded)
**The four component grammars agree with an independent oracle on 24,009 inputs, every emitted location equals the frozen 201 table, the floor helper is pinned outside both the namespace directory and every store, and 24 of 26 mutants are killed with the two survivors provably equivalent. The `Unlinked` cause is correct and leaves configuration behaviour differentially unchanged. W-1 is a type-shape recommendation to make "one namespace feeds every role" structural before the first caller exists.** No approval of admission, marker reading, custody, lease integration, installation or cumulative readiness.
