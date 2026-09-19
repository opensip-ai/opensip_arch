# Independent review — frozen `store-marker-checkpoint-202`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 202 product bytes — private store-marker codec and three-way observation (`storage/src/store_root.rs`, new), reusing the security crate's bounded retained-path reader through a newly public mechanism function; first `storage→security` edge. Data-only: no admitted store, selection, registry, lease, ACL/owner policy or exclusion is claimed, and none is reviewed as if it were. Unselected, uninstalled; no cumulative approval. My 203 assistance is unrelated to these bytes.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `b640582ee9383a6095e18ab9a366bbc2afe4bbd338df45fdaf26f13e621325ae`, 4,271,444 B = request = `archive-pin.json` |
| Members | 427, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 354/354, none unpinned |
| Parent | equals **my own verified 200 extraction**; 6 modified (`Cargo.lock`, `storage/Cargo.toml`, `storage/lib.rs`, `security/lib.rs`, `security/journal_store.rs`, `…/bound_operational.rs`) + 1 added (`storage/store_root.rs`) |
| Reference pin | `reference201` = the 201 archive I reviewed |
| Host receipt 126 | 234 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh uniquely named scratch, offline, locked)
storage 90/90, security 159/159, strict workspace Clippy clean (`claude-out/owner/`).

## 3. What the bytes do (all read in full)
- **Codec** — precedence: `Bound` (>128) → `Decode` (strict product JSON, duplicate keys refused) → `Shape` (object, exactly two members, `schemaVersion` integer 1, `storeInstanceId` string) → `Instance` (32 lowercase hex) → `NonCanonical` (raw ≠ canonical bytes) → `Binding` (≠ expected). This is 201's order ("admit the closed shape and exact types, then require raw bytes to equal canonical encoding"), with grammar and canonical equality both enforced — the two checks I showed in 199 to be independently necessary (uppercase hex is canonical).
- **Observation** — `Absent` only from the reader's `Absent`; every reader failure and every codec failure is `Unavailable` with its cause kept (`File(Context|Bound|Io)` vs `Marker(..)`). A marker naming another instance is `Unavailable(Binding)`, matching 201 ("Name/marker mismatch is unavailable custody, not an automatic corruption/quarantine"). No creation, minting, retry or repair path exists in the file.
- **Reader (unchanged logic, newly reachable)** — leaf must be one non-empty component without `/`, `\`, NUL, `.`/`..` or the staging prefix; size cap ≤ 4 MiB; chain `recheck()` before open, **after open even when open failed** ("ENOENT under an unlinked retained directory does not establish absence"), and after the read; `open_regular` uses `O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC` and then requires a regular file.
- **Visibility changes** are the minimum for the edge: two enums `pub`, module and function `pub(crate)`, one `pub fn` facade plus two re-exports in `security/lib.rs`. `Cargo.lock` gains only the dependency edge. These are the security crate's **first public items**; the doc comment states the limits accurately.

## 4. My adversarial checks

**Mutants** (13, all compiled; `io/mutation202.json`): **11 killed** — bound check, member count, any-integer schemaVersion, canonical check, expected-instance check, uppercase grammar, length, unreadable→Absent, undecodable→Absent, cap 4096, cap 72. **2 survived**: (a) judging `Binding` before `NonCanonical` — precedence only, both remain refusals, no law fixes their order; (b) **marker file name changed** — see W-2.

**Real file system** (`probes/marker202_probe.rs.txt` → `io/marker202.txt`):

| Case | Result |
|---|---|
| exactly 128 bytes (valid + spaces) | `Unavailable(Marker(NonCanonical))` — reaches the codec |
| 129 bytes | `Unavailable(File(Bound))` — refused by the reader; the two bounds agree at the edge |
| valid + trailing newline | `NonCanonical` |
| mode 0000 | `Unavailable(File(Io(PermissionDenied)))` — not Absent |
| **FIFO at the marker name, no writer** | `Unavailable(File(Io("entry is not a regular file")))` in **0 ms** — no hang |
| valid marker with a second hard link | **`Present`** |
| valid marker, mode 0666 | **`Present`** |
| only `STORE-INSTANCE.V1` exists (default APFS) | **`Present`** — the alias behaviour 201 describes, observed |

The last three are exactly what the README says is *not* checked; they are recorded so the limit is concrete, not as defects.

## 5. Findings

No defect in the codec or the observation mapping; the data-only boundary is expressed honestly in comments, README and types (`observe_marker` and everything in `store_root.rs` is private and `dead_code`-allowed). Two design points and notes.

### W-1 (low-medium; design, before a caller exists) — the exported mechanism cannot later be joined to the operational-file predicate on the *same* descriptor
195 §2 / 201 require S7's operational-file predicates "to each present file", and 198 built that predicate over a **descriptor** (`inspect_operational_file(&File, …)` → `DescriptorObservation`). The function exported here returns **bytes only** (`Present(Vec<u8>)`): the descriptor it read from is closed inside the reader. A future admitting caller therefore cannot apply owner/mode/ACL/link checks to the object whose bytes it holds; it would have to reopen by name — a second object in the general case, which is the very gap the retained-descriptor work exists to close. My probe shows the practical meaning today: a hard-linked or world-writable marker is `Present`. Since this is the first public mechanism of the crate and the shape other owners (witness, floor, slot files) will copy, fix the shape now rather than after callers exist: either return the `DescriptorObservation` taken on the same open file alongside the bytes, or take the policy as a parameter and evaluate it between open and read. Both stay data-only; neither grants authority.

### W-2 (low) — the marker's file name is defined twice with no join
`"store-instance.v1"` is a literal in `lifecycle/src/locations.rs` (200) and again as `MARKER_NAME` in `storage/src/store_root.rs`; the storage tests only ever use the constant, so renaming it survives all 90 tests (mutant (b)), and the two crates would then disagree silently — the lifecycle locator pointing at one name and the reader opening another, which reads as `Absent`. `Absent` is the one observation with a lawful non-refusal meaning (pre-materialisation), so this is the unsafe direction for a drift. Cheapest repair: one literal-pinning assertion in the storage test (as 200's role table does), and when 204 introduces `StoreNames`, make the reader take the leaf from that single owner.

### Notes
- **N-1** on `Binding` the observed instance is dropped. Right for a data-only observer (no foreign identity leaks into a cause); the future host mapper will want it for diagnosis — decide there, not here.
- **N-2** `CapturedMarker` derives `Debug` and carries the raw bytes; harmless (72 private bytes), mentioned only because other operational files reusing this pattern may be larger or sensitive.
- **N-3** `max_bytes` of the public function is caller-chosen up to 4 MiB and `leaf` is any single component: it is a general bounded file reader for the workspace. Accurate doc comment; the inventory successor should classify it as mechanism, as the README says.
- **N-4** the case-alias row above means `Absent` on a case-preserving, case-insensitive volume is "no entry under any case spelling", which is the safe direction; on a case-sensitive volume an uppercase sibling is simply ignored. Both belong to the owed native qualification.

## 6. Limits and disclosure
macOS (default APFS), unprivileged, one run. Mutants/probes only in `build202-*`/`target202-*` scratch copies created after asserting absence and restored from frozen bytes; nothing deleted; no compile failure counted (my first probe draft used an FFI `mkfifo` that the crate's `forbid(unsafe_code)` would have rejected; rewritten to call `/usr/bin/mkfifo` before it was built). I did not re-run host isolation (receipt verified against pins). Concurrency (replacement during the read) was not probed here — the reader's bracket tests from 164 are unchanged and were not re-reviewed.

## 7. Verdict (bounded)
**The marker codec implements 201's exact closed form with the right precedence and both independently necessary checks; absence is reported only from a rechecked directory chain, every other outcome keeps its cause, a FIFO cannot hang it, and 11 of 13 mutants are killed (one survivor is order-only). The data-only boundary is honestly stated. Two things should be settled before the first caller: W-1 — the newly public reader returns bytes without the descriptor observation, so S7's operational-file predicate cannot later be applied to the same object; W-2 — the marker name lives in two crates with nothing joining them, and drift would surface as `Absent`.** No approval of admission, custody, selection, installation or cumulative readiness.
