# Independent review — frozen `ledger-encoding-reference-checkpoint-180`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 180 reference bytes — the owner decision that the project ledger is UTF-8-only, stated in two owner documents. It is a policy text review; the mechanism is 179 and is reviewed separately. My 177 F-1 having prompted this decision is not acceptance of these bytes. 178 F-1/F-2 are expressly out of scope (181). No cumulative, host, creator, migration or authority approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `35b32b5668babd72da44c70b3f634a51dbd2226efcac20109e09147e465842c9`, 2,081,620 B = request = `archive-pin.json` |
| Members | 1,362, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,289/1,289; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 178 extraction**; 7 changed: `identity-and-evidence.md`, `commit-recovery-readonly.v3.md`, five manifests |
| Python | 86/86 byte-identical to 178 (model and 43 vectors included) |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs (`claude-out/owner/`): envelope → integration → security → carrier → workflows → foundation → native, **all exit 0**, no bytecode left. As the README says, this shows binding/regression stability only; no lane exercises the new rule.

## 3. The decision, assessed

**Sound and correctly motivated.** The stated reason is the one I measured in 177 (malformed UTF-16 keys transcoded into a *different valid* name), and the text draws the right conclusion: validating the returned UTF-8 cannot bind stored identity, so the boundary has to be the database encoding, checked once at the shared opener, not per column. It refuses rather than converts, keeps JSON BLOB law untouched, and explicitly declines to touch the security journal's separately owned, deliberately encoding-tolerant historical admission.

**Projection is the existing one.** `commit-recovery-readonly.v3.md` §1 l.66 already has `unknown-custody → operational-failed / HOST.IO_FAILURE / host-io`; 180 adds no vocabulary. Placing the rule beside "Ledger unreadable → unknown-custody (F24). Never absence" is the right neighbourhood, and "never absence / corruption / quarantine / recreate" closes the dangerous alternatives.

**Facts the rule leans on, checked (`claude-out/probes/encoding_probe.py` → `io/encoding_probe.txt`, SQLite 3.51.0):**
- `PRAGMA main.encoding` reports `UTF-16le`/`UTF-16be` for such ledgers on a read-only connection (header bytes 56–59 = 2 / 3), so the observation discriminates.
- A **zero-byte file reports `UTF-8` with zero tables.** The text already guards this ("observing `UTF-8` proves none of them"; "an empty fallback database is never absence") — good, because otherwise the check would read as a positive.
- I tried to flip the encoding of an existing ledger through SQL alone under a connection that had already observed UTF-8 (drop all, checkpoint, VACUUM, reopen, `PRAGMA encoding='UTF-16le'`, recreate): SQLite kept the header at UTF-8. So "check on the retained connection, then read" has no SQL-only time-of-check gap; changing it needs in-place file rewriting, which is the separately owned filesystem-custody problem. I therefore do **not** raise the check-vs-snapshot ordering as a finding.

## 4. Findings

### F-1 (medium-low) — a third owner of project-ledger physical law still says the opposite
`docs/v2/architecture/attempt-custody.schema.v1.json` → `ddlGrammarCorrection.law`: "The conjunction does not depend on the database text encoding (exercised under UTF-8, UTF-16le and UTF-16be); **no encoding is required.**" Its `standing` records that an earlier byte-length predicate was withdrawn precisely because it "refused **lawful** rows in UTF-16 databases". Attempt custody is one of the tables 180 names as UTF-8-only, and this file is a *selected companion* of the very document 180 edits (`commit-recovery-readonly.v3.md` l.13, l.603). It is unchanged in 180 (not among the 7), so after 180 the tree says both "a UTF-16 project ledger is unsupported even if otherwise valid" and "no encoding is required … lawful rows in UTF-16 databases".
The two are reconcilable — encoding-independent CHECK grammar is still worthwhile defence in depth — but the file has to say so: the grammar does not depend on encoding; the **ledger** nevertheless requires UTF-8 under identity §"Project ledger text encoding (180)"; UTF-16 rows are no longer "lawful", merely not mis-refused by the DDL. This is the same class as 175 F-1 (a rule corrected at the sites one was looking at, with a further owner left stale); the request's "two owner docs" undercounts by one. The carrier-side statements (`carrier-format.v3.md` l.184–205, `carrier-dispatch.v3.json`) are the security journal and are correctly left alone.

### W-1 (low) — the writer's public disposition is named only by analogy
180 binds "both the reader and existing-writer openers", but the only projection it states is "the existing **recovery** outcome is `unknown-custody` …", and the row it cites lives in the read-only recovery standings table. For a commit-path writer that meets a UTF-16 ledger the text gives no outcome of its own. `HOST.IO_FAILURE` is very likely what the writer owner wants too, but that owner should say it; writer disposition of reader-defined refusals has been open since my 160 F-2 / 165 and this adds one more instance.

### W-2 (low) — "cannot be observed" is not distinguished from "observed and wrong", and that is fine — but say it is deliberate
Both map to `unknown-custody`. A host mapper or `doctor` will want to tell the user "this ledger is UTF-16; it is unsupported" rather than a generic I/O failure, since the remedy differs (restore/migrate vs retry). The contract forbids neither, but report-only diagnostics are where that distinction should be owned; one sentence would prevent a future "generic failure only" reading.

### N-1 (note) — creator rule is unexercisable today
"New-ledger creation must select and verify UTF-8 before publishing its schema" has no creator to bind to (disclosed). When one exists, note that `PRAGMA encoding` is silently ignored once any content exists (my probe), so "verify" must be a read-back, exactly as written — keep that word.

## 5. Closure of earlier findings

**177 F-1: decided at the policy level by these bytes** (UTF-8-only, refuse, no conversion); mechanism closure is a 179 question. Nothing else is addressed or claimed.

## 6. Limits

Text review plus re-execution of unchanged lanes plus a scratch SQLite fact probe (system SQLite 3.51.0, not the product's bundled 3.53.2). I did not search every historical/retained document for encoding statements beyond a tree-wide grep for `utf-16|encoding` in `docs/**/*.md|json`; hits outside the project ledger were read only far enough to classify them as security-journal or unrelated.

## 7. Verdict (bounded)

**The decision is coherent, correctly scoped and uses only existing public vocabulary; all lanes pass. F-1 should be fixed before this text is relied on as the single statement of project-ledger encoding law, because a selected companion owner still says no encoding is required.** No approval of the 179 mechanism, of any creator/migration, or cumulative readiness.
