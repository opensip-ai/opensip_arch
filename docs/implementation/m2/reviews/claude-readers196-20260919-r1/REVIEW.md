# Independent review — frozen `reader-effects-checkpoint-196`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 196 product bytes — reader engine controls in both SQLite readers, their physical-effect regressions, and the empty-chain refusal (my 193 N-1). Not the complete 195 contract (custody, location relationships, admitted SHARED-READ, exclusion, consumption, Linux, local filesystems, host pipeline are declared owed), not 197, no timing claim, no cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `61628785a171e8ec97793cd62069583e39cb28c77e00f495cdc96dcee6ba508d`, 4,296,952 B = request = `archive-pin.json` |
| Members | 440, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 352/352, none unpinned |
| Parent | equals **my own verified 194 extraction**; exactly three changed: `storage/ledger_store.rs`, `security/journal_store.rs`, `security/custody.rs`; nothing added/removed |
| Host receipt 124 | 232 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch copy, offline, locked, dedicated target)

storage 85/85, security 154/154, strict Clippy clean (`claude-out/owner/`). The preserved failed r1 journal fixture is explained correctly: a merely opened holder has no read lock, so an appender could be last closer and delete the WAL — consistent with what I measured for 195.

## 3. What is right

- Both readers: `READ_ONLY` open → `is_readonly(main)` refusal → `busy_timeout(0)` API → `NO_CKPT_ON_CLOSE` set **and** effective read-back, all before any SQL. Writer gate and writer close behaviour unchanged (diff).
- **Journal reader order fully conforms to 195**: `query_only` set and `query_only`/`busy_timeout` read back before its first database-touching statement (`PRAGMA journal_mode`).
- Ledger: `query_only` set + read back now precede the encoding observation; busy-first (184) and encoding-before-domain-text (180) are preserved. The new `SQLITE_LIMIT_LENGTH=1` fault is a better fixture than the old SQL-length one: integer control pragmas still work, so it reaches the encoding query.
- Refusal after the database has been touched, over a **non-empty WAL** (my probe, `io/refusal196.txt`): UTF-16 ledger → `Encoding(Unsupported)`, main and WAL byte-identical before/after refusal and after drop; UTF-8 control likewise.
- Empty chain refuses with its own variant; mutant killed by the new test.

## 4. Findings

### F-1 (low-medium) — ledger reader verifies the effective busy timeout **after** its first database-touching query
(Also raised in the owner's self-audit message during this review; independently visible in the bytes.) 195 §2: "It then sets and verifies query_only=ON… before any data/schema query. **The effective zero busy timeout is also verified before those queries.**" In `configure()` the `("busy_timeout", 0)` read-back sits in the later verification loop, after `PRAGMA main.encoding` — the statement that attaches WAL/SHM (measured in my 195 review). The journal reader does this correctly, so the two readers differ. Practical exposure is small (the API call returns `Result`, and my probe reads 0 at that moment), but the read-back exists precisely because a successful configuration call is not the effective value, and 179 F-1 was a 5.4 s wait at exactly this statement. Fix: read `busy_timeout` back beside `query_only`; keep the later loop.

### T-1 (medium as a test gap) — nothing pins the control **order**, and "a control failure … cannot reach a database query" is untested
Order mutants, scratch copy, all compiled, judged by test results (`io/mutation196.json`):

| Mutant | Result |
|---|---|
| ledger: `query_only` moved back after the encoding query (the 194 order) | **survived** 85/85 |
| ledger: NO_CKPT control moved to the very end (after `journal_mode`) | **survived** |
| journal: NO_CKPT control moved after `journal_mode` | **survived** |

So the central 196 claim is carried by reading the code only. It *is* observable: with the owner's own `LIMIT_LENGTH=1` fault, the connection state at the moment of failure reveals what had run — frozen code: `query_only=1 no_ckpt=true`; first mutant: `query_only=0`; second: `no_ckpt=false` (`io/order-q/`, `io/order-ckpt/`). The owner's fault test asserts `query_only==0` *before* `configure` but nothing *after*; two assertions there kill both ledger mutants. A stronger, fault-free form: split the pre-SQL controls into one function and assert **no sidecar exists** after it returns on a clean ledger — the file system is the order spy, and it would cover F-1 too.

### T-2 (medium as a test gap) — the physical-effect tests cannot see the control they accompany
| Mutant | Result |
|---|---|
| NO_CKPT omitted (ledger / journal) | killed — but **only by `assert_reader_controls`' flag assertion** (panic is `db_config(NO_CKPT_ON_CLOSE)`), not by an effect |
| NO_CKPT omitted **and** that flag assertion removed | **survived**, both readers: every main/WAL/SHM effect assertion still passes (`io/mutation196b.json`) |
| reader opened `READ_WRITE`, access check removed, NO_CKPT kept | **whole suite passes** once the helper's `is_readonly` assertion is removed — NO_CKPT alone preserves the WAL |
| same, NO_CKPT also omitted | killed by the effect assertions (WAL checkpointed/deleted at last close) (`io/mutation196c.json`) |

This is the engine fact I recorded for 194/195: a read-only descriptor cannot checkpoint or delete at close, so with READ_ONLY intact NO_CKPT has no observable effect; it is a second layer that matters only if read-only access is lost. That is a sound design and the README's claim ("enabling/omitting close control" mutants pass) is true — but the kills come from configuration assertions (and, for the `false` mutant, from the product's own refusal), not from "physical effect regressions". Say so, and add the one test where the layer is load-bearing: the fourth row above as a permanent negative (a test-only read-write open through the same configure path, showing WAL preserved with the control and destroyed without).
Also surviving, and I judge these **not practically testable** without a fault-injecting engine: reader access check removed (ledger, journal), NO_CKPT read-back removed, `query_only` read-back weakened. They are defensive checks on values the engine does not misreport; listed for honesty, no test demanded.

### N-1 — refusal vocabulary
Ledger gives `Configuration("reader_access_mode")` / `("no_checkpoint_on_close")`; the journal collapses every control failure into the unit `CarrierReadError::Configuration`. Fine for now; when the host mapper arrives the journal side cannot say which control failed.

### N-2 — unwritable-directory test
Typed `ReadOnly`, main unchanged, no sidecars: correct and causal. It restores the mode before asserting, good. It is macOS/unprivileged-only by its own guard; Linux owed as stated.

### N-3 — for 197, not a 196 defect
My `SQLITE-RETRY-NOTE.md` applies to both readers unchanged: `busy_timeout=0` verified here does not bound native WAL retries; `SQLITE_PROTOCOL` would surface as `Sql(..)`/`CarrierReadError::Sql` — causal, not rewritten. Grep of the three changed files (run after drafting this sentence, result as expected): `DatabaseBusy` appears only in test assertions and one doc comment; no production classifier folds codes, so 15 stays distinct from 5/261.

## 5. Closure of earlier items
193 N-1 (empty chain) **closed**. 195 N-1 (query_only before encoding) **closed for query_only; open for the busy read-back (F-1)**. 194 writer gate unchanged and its tests pass.

## 6. Limits and disclosure
macOS, one engine build. Mutants and probes ran only in fresh scratch copies (`build196-*`, `target196-*`), restored by copy from the frozen bytes; compile failures would not have been counted (none occurred). **Disclosure:** before starting I removed regenerable `target*` build directories from my *194* review's scratch to free space; its `hashes.txt` (which never covered them) still verifies 100 %. A second such command was cancelled by the user; since then nothing has been deleted and all scratch is uniquely named. Build targets are excluded from `hashes.txt`.

## 7. Verdict (bounded)
**The reader controls are correctly implemented and, for the journal reader, correctly ordered; the ledger reader has one ordering nonconformance with 195 (F-1, busy read-back after the first database-touching query). The larger point is evidential: no test pins the order (T-1), and the effect tests are insensitive to the NO_CKPT control because READ_ONLY already guarantees those effects (T-2). Both gaps have cheap, deterministic tests, shown above.** No approval of physical custody, lease integration, timing, 197, or cumulative readiness.
