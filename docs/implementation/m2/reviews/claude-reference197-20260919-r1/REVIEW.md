# Independent review — frozen `sqlite-profile-reference-checkpoint-197`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 197 reference bytes — four prose owners (read-only recovery, security/lifecycle, workflows/surfaces, carrier format) stating the WAL-only journal open profile, the reader scope of the SQLite exception, and native contention/retry law. My `SQLITE-RETRY-NOTE.md` was assistance, not acceptance of this text. Owner-text review: nothing here qualifies native or host behaviour, and no cumulative approval is implied.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `91e128132a37e510a07cefb783ff766cb10bacd414e9fba64ebc4fb8de2651e1`, 2,194,956 B = request = `archive-pin.json` |
| Members | 1,376, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Candidate pins | 1,299/1,299; none unpinned; declared changes equal computed |
| Parent | equals **my own verified 195 extraction**; 9 changed = 4 prose owners + 5 source-pin manifests; **91/91 Python identical**, as are all models, SQL, schemas, fixtures |
| Behaviour unchanged | my `sweep`/`binding`/`phasec` probes byte-identical to my 195 (= 192) outputs. First run failed on my own harness (missing argument) — preserved in `io/r1-FAILED-missing-argument/` |

## 2. Owner checks re-run
Reference order, `-I -B`, fresh outputs: all seven lanes exit 0; integration 1,787 passed; carrier 479 / 0 failed. None executes SQLite behaviour, as the README says.

## 3. Closure of my 195 items

| 195 item | 197 | Status |
|---|---|---|
| "F1" in the request = my **N-0** (I withdrew it as a finding; what remained was a missing current citation) | new `carrier-format.v3.md` section: WAL required for inherited 1/2, current 3 and migration-prefix dispatches; observed, never set; non-WAL refused **before dispatch** with no conversion/corruption/quarantine/empty-history inference; unobservable mode keeps its causal outcome; readonly §2 and S7 cite it | **closed**, and stronger than I asked (disposition stated for writer/maintenance opens too). Consistent with the 196 product, where `journal_mode` is observed in the connection function before `admit_connection` |
| W-1 transient exclusive `WAL_WRITE_LOCK` | named in readonly §2 and S7; appender BUSY is "ordinary causal engine contention, not custody loss or evidence corruption"; lease compatibility ≠ contention-free SQLite | **closed** |
| W-2 reader scope / report-only surfaces | exception is the property of every already-admitted SHARED-READ ledger/journal consumer, without importing §2's algorithm; fence-only `doctor`/`trust doctor`/`store status` phases cannot open these databases; "no new phase or lease is inferred" | **closed**. Checked against the unchanged S7 lease map: l.913 lists `doctor`/`trust doctor`/`store status` under *fence only*, l.914 lists "`doctor` project checks" and "`agent serve` reads" under SHARED-READ — 197 names only steps that already hold the lease. **No new authority and no missing existing command** that I could find: every SHARED-READ row (`query`, `recommend`, `baseline show`, `policy show|test`, `candidates`, `inspect`, `review brief`, `repair preview`, agent reads, doctor project checks) is covered by "every admitted SHARED-READ … reader"; command classifications (l.1764–1788) are unchanged |

Retry note incorporation, checked number by number against my evidence: 100 attempts per read-transaction start; attempts 6–9 → 1 µs, 10–100 → 39·(n−9)²; 9,958,498 µs in 95 sleeps; **not** an end-to-end bound; per transaction, not per command; can outlast a lock holder (my case B/M4); valid mapped header need not trigger (M1/M2); first attachment / invalid header / CKPT / read-mark triggers (A, M3, F, H); writers too (A′); 5/261/15 distinct, 15 not a busy code → host-io, never absence/corruption/commit/non-commit; S7's 5 s fence is a different clock. All accurate.

**One place where 197 is more correct than my note** (disclosure): my note listed "no `HAVE_USLEEP`/`HAVE_NANOSLEEP`" among `compile_options` results as if that were evidence. It is not: the pinned `sqlite3CompileOptions` table can report `ENABLE_SETLK_TIMEOUT` (l.23352) but has **no entry** for either sleep macro (only `HAVE_ISNAN`). My real evidence was reading `build.rs` and `unixSleep`. 197's sentence "their absence from compile_options alone is not proof of the sleep implementation" is exactly right; I verified the table after reading it.

## 4. Findings

### F-1 (low-medium) — "No application retry … is authorized" collides with the existing workflow retry owner
Readonly §2 (new): "**No application retry**, project-lock upgrade, checkpoint or writer wait is authorized" — said of the BUSY a writer/reader sees during engine contention — and the README: "No additional application retry is authorized." But unchanged `workflows-and-surfaces.md` l.105–108 already authorizes one: "`retryPolicy=idempotent-retry` is lawful only for `analysis`, `verify`, `query`, `render`, `doctor` and `export-delivery`, only for `faultCause=ledger-busy`, and within the 3-attempt budget". Busy keeps "its existing busy route" (197) = `ledger-busy` = retryable for exactly the SHARED-READ steps 197 has just brought under this paragraph. Read literally the two conflict; read with the README's "additional" they do not. Two consequences worth stating rather than leaving to inference:
1. wording: "no retry **beyond** the workflows idempotent-retry budget and §2's own permitted second capture" (S&L l.2158 "single permitted retry" is a second existing one);
2. arithmetic: the 9,958,498 µs requested-sleep figure is per read-transaction start, so it multiplies by transactions **and by up to 3 workflow attempts**. 197 rightly refuses a deadline; it should say the workflow budget multiplies too, or someone will derive "≈10 s worst case" for `query`.
The PROTOCOL half is already consistent: 15 → `host-io`, and l.108 "`host-io` and every other fault are never retried."

### W-1 (low) — the unchanged executable model still emits the old level-3 cell
S7's lock table level 3 changed from "never for readers" to "no application wait; native WAL retries as specified below", and "Readers never block a writer" became lease-level. `security_lifecycle_model_v1.py` l.1852 `LOCK_ORDER[3]['blocking']` is still `'never for readers'`, returned as `lockOrder` in lease results (l.2080; schema l.2222–2247); `check-security-lifecycle.v1.py` l.400 docstring: "no mode is blocking". The lane passes because vectors assert only `lockOrder.0.name` and `lockOrder.length` (`lease-cases.v1.json` l.45–46) — there is no contract↔model join on that cell. This is the recurring class (prose corrected, executable owner silent). Python was deliberately frozen here, so: either record that the model's column means *application/lease* blocking only, or rebind it in the next Python-touching checkpoint. Not a behavioural defect.

### W-2 (low) — the read-only precedence list does not place the new refusal
Readonly l.98–110 "Precedence of the read-only carrier observations" is unchanged: (1) association naming another binding → `binding-unusable` "before any carrier read"; (2–4) format-3 / inherited / fresh-install rows. The association is a *ledger* row (l.408), so the journal's WAL observation necessarily falls between row 1 and rows 2–4 — consistent with carrier-format's "Before querying carrier definitions or rows". Nothing contradicts, but two outcomes follow that the list should state: a non-WAL **inherited** carrier now yields `unknown-custody`, not row 3's `unknown-carrier-incompatible` (identical public projection — operational-failed / `HOST.IO_FAILURE` / `host-io` / omitted — so no surface changes); and `binding-unusable` still wins without opening the journal at all.

### Notes
- **N-1** "Busy/locked retain their existing busy route": with `PRIVATE_CACHE` connections `SQLITE_LOCKED` (6) is essentially same-connection; harmless to list, just not a cross-process contention outcome.
- **N-2** the qualification list ends "as well as application timeout and lease-release ordering". I found no owner for an *application timeout* around reads (197 itself refuses a total-read deadline). If it means "whatever supervises a stuck read must release the lease in S7 order", say that; otherwise it invites someone to invent a timeout.
- **N-3** "rejects nonempty `LIBSQLITE3_FLAGS`" is the right concrete control; `build.rs` also honours `SQLITE_MAX_VARIABLE_NUMBER`/`SQLITE_MAX_EXPR_DEPTH`/`SQLITE_MAX_COLUMN` from the environment (l.306–319) — visible in `compile_options`, so the comparison already catches them.
- **N-4** carrier-format: "The creator selects and verifies WAL before publishing a new carrier" agrees with the historical `security-completion.v1.md` §5.4 ("opened WAL") that I cited in 195 N-0; the new section does not cite it, which is fine now that it is itself the current owner.

## 5. Limits
Prose review plus source/lane checks; no new engine experiment here (the retry evidence is my separate macOS note — one engine build, simulated invalid-header states). I compared the complete diffs of the four owners and searched the whole tree for surviving absolute statements ("never for readers", "waits on no lock", `busy_timeout`, retry vocabulary); I did not re-read unaffected sections end to end. No model mutation work was repeated: 91/91 Python identical and my probes byte-identical.

## 6. Verdict (bounded)
**197 closes my three 195 items, states the journal WAL profile with a complete refusal disposition, scopes the engine exception to readers that already hold SHARED-READ without creating authority, and reports the native retry behaviour accurately — more carefully than my own note on the sleep macros. One real collision remains (F-1: the absolute "no application retry" against the existing workflows idempotent-retry budget, with its multiplying effect on the sleep figure); W-1 and W-2 are an unjoined model cell and an unplaced precedence step.** No approval of physical custody, native/host qualification, 196's product, or cumulative readiness.
