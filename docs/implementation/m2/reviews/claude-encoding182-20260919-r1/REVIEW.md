# Independent review — frozen `ledger-encoding-owners-checkpoint-182`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 182 reference bytes — reconciliation of the attempt-custody companion with the 180 UTF-8-only ledger law, the existing-writer failure disposition, and the unsupported-vs-unobserved diagnostic rule. Policy text only; no mechanism (179/183) and nothing of 181. No cumulative, creator, writer, mapper or authority approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `cf2b75964e958936ed56f0545ec1723c9a6786d9de27d7e37fee714c5439f44e`, 2,073,700 B = request = `archive-pin.json` |
| Members | 1,362, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,289/1,289; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 180 extraction**; 7 changed: `attempt-custody.schema.v1.json`, `identity-and-evidence.md`, five manifests |
| Python | 86/86 byte-identical to 180 |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs (`claude-out/owner/`): all seven lanes exit 0; no bytecode left. As disclosed, no lane exercises these sentences.

## 3. 180 F-1 (attempt-custody companion) — the named file is fixed correctly

`ddlGrammarCorrection.law` now says the CHECK conjunction is encoding-independent, "this property of the grammar does not admit a database encoding", cites the identity section by name, and states that UTF-16 ledgers are refused "even when these CHECK predicates would accept their rows". `standing` changes "lawful rows" to "rows then considered lawful" and records that the later decision now governs. The DDL predicates and the historical probe record are untouched (structured JSON diff: exactly those two string members changed). That is the reconciliation I asked for, and it keeps history honest rather than rewriting it.

## 4. 180 W-1 (writer disposition) — checked against the actual outcome owners, not by analogy

| 182 statement | Actual existing owner | Result |
|---|---|---|
| `operational-failed` / `HOST.IO_FAILURE` / `host-io` | workflows §9 termination contract: operational-failed carries `errorCode` and a non-none `faultCause` from the closed list, which contains `host-io`; security S12 table: "I/O failure → operational-failed / 4 / `HOST.IO_FAILURE`" | consistent; no new vocabulary |
| a **writer-side** ledger that cannot be opened → host-io, no write | `commit-recovery-readonly.v3.md` §4.2 sweep table (the sweep holds the fence and EXCLUSIVE — it *is* a writer): "**inaccessible**: the ledger cannot be opened or read → **no write**; report `operational-failed` / `HOST.IO_FAILURE` / `host-io`" | this is the real precedent and it matches exactly. 182 does not cite it; it should, because it is the one existing writer-side owner |
| not `ledger-corrupt` | `LEDGER.CORRUPT`/`ledger-corrupt` is owned by the quarantine condition (readonly §1 l.67–73) | consistent with 180's "not a claim of corruption" |
| "must not … retry automatically" | workflows §"Retries": "`host-io` and every other fault are never retried"; `mutation`/`import` carry `retryPolicy=none` by schema | consistent; already law, correctly restated |
| "retaining an already allocated ExecutionId and omitting any unestablished Run identity" | the only existing sentence of this shape is readonly §4.2 l.564–565 for `durability-undetermined` ("ExecutionId retained, the `runId` omitted and no automatic retry"); workflows §9: runId appears only when a Run was committed | consistent, and 182 is right to say this refusal is **not** that durability outcome |
| "not a failed commit durability barrier; an earlier uncertain commit keeps its own outcome" | §4.2: the custody row of an uncertain attempt stays `admitted`; only the sweep settles it | consistent. Additional check: the attempt-custody row lives *inside* the ledger, so a refusal at open cannot leave a new `admitted` row behind — there is nothing for the sweep to settle from this refusal. 182 implies this ("before any … mutation"); it is true by construction |
| "An attempt to open an existing ledger never becomes ledger creation" | 179 mechanism: single `open_existing` without create flag | consistent with the mechanism I reviewed |

So the writer disposition is grounded in existing owners. One gap:

### W-1 (low) — `domainDetail` for the writer refusal is unstated
The reader standings table fixes `domainDetail` = *omitted* for `unknown-custody`. 182 says both causes "deliberately share the public host-I/O disposition" and that only **report-only** diagnostics may distinguish them, but does not say the writer's public response omits `domainDetail`. A host author could lawfully put `ledger.encoding-unsupported` vs `ledger.encoding-unobserved` there, which would fork the public route 182 says is shared. One clause ("`domainDetail` omitted, as for `unknown-custody`") closes it.

## 5. 180 W-2 (diagnostic distinction) — adequately decided
"May distinguish using only the captured observation … must not infer a particular encoding after a failed read, or turn either diagnostic into repair/conversion authority." This is the right rule and it is bounded correctly. (183's typed encoding failures will be where it becomes checkable.)

## 6. Finding

### F-1 (medium-low) — a further owner still says no encoding is required of the **ledger**; and my 180 review mis-classified it
`docs/coop/design-corrections/security/carrier-dispatch.v3.json` → `/ddlGrammar/encodingIndependence` ends: "**No carrier or ledger is required to use a particular encoding.**" That `ddlGrammar` block is not carrier-only: it has `attemptCustodyColumns` and `attemptCustodyIntegerColumns` members, i.e. it states grammar law for the project-ledger attempt-custody table. It is unchanged in 182 (and in 180). After 182 the tree therefore still contains one sentence asserting the opposite of "the project ledger MUST use UTF-8".
**Correction of my own 180 report:** there I wrote that the `carrier-dispatch.v3.json` hits "are the security journal and are correctly left alone". I had classified them from grep output truncated at 230 characters and never read this sentence to its end. That was wrong for this member; 180 F-1 should have named two stale sites, not one. The carrier half of the sentence is still correctly untouched (the security journal's encoding tolerance is deliberately out of scope).
Remedy mirrors what 182 did for the companion: split the sentence — no *carrier* is required to use a particular encoding; the project ledger is UTF-8-only under the identity section, and the grammar's encoding-independence does not admit an encoding. `carrier-format.v3.md` l.185/204 speak only of carriers and need no change (`claude-out/io/encoding-statement-scan.txt` lists every ledger/attempt-related encoding statement I found; I read each to its end this time).

## 7. Out of scope, flagged because I found it while tracing owners

`workflows-and-surfaces.md` l.1679 ("Before ordinary project admission, the host inserts a required installation-recovery mutation step if the fenced installation journal requires recovery … host-started recovery invocation") is unchanged since 175 and reads as unconditional host-started recovery. It is not part of 182 and is not counted here; see `NOTES-178-residual-site.md` in this directory, which also corrects a sentence of my 178 report.

## 8. Limits

Text review, re-execution of unchanged lanes, and owner tracing by reading. No executable artefact encodes these sentences. I searched `docs/**/*.md|json` for encoding statements touching the ledger/attempt custody; I did not search Python docstrings or retained historical archives.

## 9. Verdict (bounded)

**180 F-1 is fixed in the file it named, W-1 and W-2 are decided, and the writer disposition agrees with the actual existing owners (termination contract, retry law, sweep "inaccessible" row, durability-undetermined rule). One stale ledger-encoding statement remains in `carrier-dispatch.v3.json` (F-1) — partly my miss in 180 — and the writer's `domainDetail` should be stated (W-1).** No approval of any mechanism, creator, writer, mapper or cumulative readiness.
