# Independent review — frozen `retry-layout-reference-checkpoint-199`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 199 reference bytes — closure of my 197 F-1/W-1/W-2/N-2 and the new current owner `physical-store-layout.v1.md` with its joins. **My layout199 note was assistance; this reviews the exact choices, including one I proposed and now think is wrong (F-1).** Old `PROPOSED` headers are not treated as permission blocks, per the request. No OS qualification, custody, implementation or cumulative approval is implied.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `5e370268edb355226adc73f38fe3955af0a4d196904af34022e8967b459fa51b`, 2,251,300 B = request = `archive-pin.json` |
| Members | 1,385, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Candidate pins | 1,300/1,300; none unpinned; declared changes equal computed |
| Parent | equals **my own verified 197 extraction**; 12 changed + 1 added = 13: new layout owner; four prose owners (readonly, S&L, carrier-format, build plan); model cell + checker; six pin manifests (incl. envelope); **89/91 Python identical**, the two changed are a one-string model cell and the checker join (diffs read in full); `transition-journal-cases.v1.json` identical |

## 2. Owner checks re-run
All seven lanes exit 0 (`claude-out/owner/`); none executes file-system behaviour.

**The new contract↔model join is genuine** (scratch copies of the tree; first run refused on **source pins — not counted**; pins then rebound in scratch, `io/joinmut-*-rebound.*`): model cell reverted → `sweep_lease_modes` false; contract cell reverted → false; **both changed consistently to the same stale text → still false** (the constant assertion). 580/580 other checks still pass in each, so the failure is the join and nothing else.

## 3. Closure of 197

| 197 | 199 | Status |
|---|---|---|
| F-1 absolute "no application retry" vs workflows retry owner | readonly §2: "authorizes no **additional** application retry"; names workflows §1 (enumerated step kinds, `ledger-busy` only, ≤3 attempts) and §2's second capture as the two existing owners; `host-io` incl. `SQLITE_PROTOCOL` never workflow-retried; "Transaction counts and workflow attempts therefore both affect total elapsed time; none establishes a total-read deadline" | **closed** — workflows text itself correctly untouched |
| W-1 stale model cell | cell rebound + join (§2) | **closed** |
| W-2 unplaced non-WAL refusal | readonly: between step 1 and any carrier observation; `binding-unusable` wins without opening the journal; later rows "do not relabel this earlier unsupported-mode outcome" | **closed** |
| N-2 "application timeout" | replaced by "effective zero busy-handler setting and S7 lease-release ordering"; "does not introduce an application read timeout or cancellation capability" | **closed** |

## 4. The layout owner — what I checked and found right
- **Adoption, not restatement**: the JSON locator is adopted with `I/host` named as project-state-root and S7's `<namespace>` equated to `I/host/projects/N`; "does not revive the historical registry's superseded identity or lease protocol". S7, readonly, carrier-format and the build plan each *cite* the owner; none restates paths. One owner.
- **Leases, journal, single witness outside every store**, with the reasons (same inode for source and target; one carrier per namespace; `journalCarrierDigest` stays the security-owned `projectKeyDigest`, "No hash of N, S or a pathname replaces it"). Witness correctly singular.
- **S7.1's collection-copy sentence is replaced in S7.1 itself**, not only in the new file; no other site still requires a collection copy (`io/floor_copy_sites.txt`: readonly l.264/558 speak of the fence-boundary *tail copy*, which is unchanged; the model's "floors copied forward" at l.2248 is the six-counter law). The six `FLOOR_KEYS` image/copy/max/freshness protocol is explicitly untouched; "no claimed atomicity spans the journal, high-water files, lifecycle or evidence ledger". This removes my layout gap 6 (no crash window exists to specify).
- **Marker bytes**: computed with the tree's `foundation/canonical.py` — `{"schemaVersion":1,"storeInstanceId":"<hex32>"}` is exactly **72 bytes** (≤128 cap), key order input-independent; trailing newline, leading space, BOM and `1.0` all fail raw==canonical. **Uppercase hex passes raw==canonical**, so the hex32-lowercase grammar is separately load-bearing — the owner requires both ("S satisfying the hex32 grammar" *and* canonical equality); an implementation doing only one is wrong (`io/marker_bytes.txt`). Product profile is the right one (S2: documents carrying `schemaVersion`), unlike witness/floor which stay on the metadata codec.
- **Name is a locator**: "never … infer its identity from the directory name"; mismatch is unavailable custody, not corruption. `.staging` cannot collide with a hex32 name. Staging keyed by the *original* E matches the 186 attribution law, and makes abort's deletion target non-nominatable.
- Component grammars match their owners (UUIDv4 lowercase; hex32; `grantGeneration` 1..2⁶³−1 shortest decimal; `exec1_`+hex32). Provenance/full binding/retained handles/local-FS qualification all stated as still required.

## 5. Findings

### F-1 (medium) — floors *inside the namespace directory* narrow a detection property that current owners still claim
Placement: `I/host/projects/N/floors/G.floor`, beside `grant-journal.sqlite` and `grant-journal.witness`. Current claims: S&L l.718–723 "Confirming a retained carrier therefore establishes presence, contiguity and **non-rollback below the last observed operation boundary**"; v8 §5.4 l.297 "the SC-TRUST high-water detects a **project-namespace rollback** below the last observed operation boundary"; §5.5 "Detected: … a project rollback below an observed floor". v1's stated design reason for a separate trust file was "precisely so lifecycle restore cannot carry trust state".
With the high-water in the same directory as the carrier it guards, the most ordinary rollback of a project's state — restoring or syncing back the directory `host/projects/N/` (backup tool, snapshot, file sync; no adversary needed) — restores journal, witness **and floors coherently**. Every comparison then agrees and the rollback is undetected. Only a rollback of the journal/witness *files alone* remains detected. 199 says the collection is "absent from lifecycle/store backups and restores", which binds the product's own backup code but not the directory's physical fate, and the owner does not mention the detection bound at all.
**This is my own proposal's defect**: my layout note offered `host/projects/<N>/floors/` for reading A and did not weigh this. The property option A needs is only "outside every store and never touched by a store transition". That is equally met by an install-level trust-owned subtree, e.g. `I/trust/journal-floors/N/G.floor`, which keeps the high-water out of the namespace directory's blast radius (whole-install-root rollback stays the stated undetected class, unchanged). If the in-namespace placement is kept, then S&L l.718–723 and the detection-bound wording must be narrowed honestly to "rollback of the carrier/witness that does not also restore `floors/`". I recommend moving it; either way the owner has to say which.

### W-1 (low-medium) — the owner is complete for read-only recovery, not for S9.2/186 transitions
The heading scopes it to "S7 retained custody and read-only recovery", which it covers. The request calls it the complete layout owner; for transitions these 186-protocol objects have **no location**: the **ancestor stage carrier** ("ancestor, a separate small staging carrier" — the table has only "Forward store staging"); the **carrier state/binding record** (staged-empty…COMMITTED/published, bound to original E + intentDigest — after `stores/.staging/E` is renamed to `stores/S` the path no longer carries E, so the binding must be a file inside the root, and the marker holds only S); the **prepared floor image**; the **source-fence record**; the **installation selection pair** carrier; the **active-slot/transition-journal** carrier; the **lineage table**. Nothing is contradicted — but say in the owner that these are deliberately not yet placed, and whether `.staging/E` is also the ancestor carrier's home (same key, so it could be) or forbidden for it.

### W-2 (low) — case-insensitive file systems vs "no case variant"
The grammar emits lowercase only, but on default APFS `stores/<S>` resolves a directory whose *stored* name differs in case. Marker==S still holds, so identity is safe; "no case variant" is then true of the constructor, not of the object found. The before/after **name observations** the owner already demands are what close this — say that they compare the stored name bytes, and list case-folding/normalizing file systems under the local-filesystem qualification. Same-UID actor only, so inside the existing threat bound.

### Notes
- **N-1** marker "prospective": S2.1 said explicitly that no product witness/floor writer had shipped, so no migration exemption exists. The marker section says "prospective file encoding" but not whether any store root already exists under the S9.3 "persisted in that store's own root" rule with different bytes. If none does (I believe so; not checked in product here), say it, as S2.1 did — that is the whole legacy-bridge cost, zero.
- **N-2** `floors/` creation: readers never create it and S7.1 already makes a missing floor `unknown-custody (floor-absent)`. Absent *directory* and absent *file* therefore coincide — fine, but the fenced writer that first creates `floors/` should be named with the namespace-directory creation rule (exclusive, no-follow, 0700, fsync dir+parent) so it inherits the same discipline.
- **N-3** the historical `namespaceCrashCleanup` lists "no retained journal/witness/root" as the condition for cleaning an unregistered directory; floors are not in that list. Harmless (an unregistered namespace cannot have reached a fenced boundary) and 199 already says the layout "grants no deletion of retained trust files".
- **N-4** README/request say "closed 128byte marker": the file is 72 bytes; 128 is the read cap. The owner text is right.

## 6. Limits
Prose/owner review plus lane, join-mutation and canonical-bytes checks. No file-system experiment (nothing here is implemented). I compared all diffs in full and searched the tree for copy-forward and location statements; I did not re-read unaffected sections. Unchanged transition algorithms were not re-mutated (Python delta is one string and one join).

## 7. Verdict (bounded)
**199 closes all four 197 items, with a checker join I confirmed kills in both directions after pin rebinding. The layout owner is single-sourced, consistent across the five citing owners, and its lease/journal/witness/ledger/marker/staging choices follow from existing law; removing the collection copy from S7.1 eliminates a crash window rather than specifying one. One choice should be reconsidered before implementation: F-1 — keeping the per-generation high-water files in the same directory as the journal they guard lets an ordinary namespace-directory restore roll both back together, narrowing a non-rollback property that S&L and v8 still claim; an install-level trust subtree satisfies option A without that cost. W-1 asks the owner to state that transition objects are not yet placed.** No approval of implementation, OS qualification or cumulative readiness.
