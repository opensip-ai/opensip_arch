# Independent bounded review — historical mirror policy in the reference, 160 (prose only)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: `history159-mirrors160-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README and
OWNER-DECISION.md read in full. Scope: the delta of frozen `historical-mirrors-reference-checkpoint-160` over frozen
153 — a policy paragraph in `carrier-format.v3.md` §9, one linking clause in the contract's admission table, the
153 W-3/W-4 wording, and five manifest rebindings. No executable behaviour. Scratch only, `-I -B`; no
frozen/selected/product edit, commit, push or delegation; no cumulative approval. No cryptographic corpus repeated.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,081,848 bytes, SHA-256 `e537be68e870a502c06d6a8fe99079ac416a0627bd4d96db27a2f337bd356c64` = `archive-pin.json` (no digest in the request; archive pin and every member verified) |
| Members | 1,360/1,360 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after all runs |
| Candidate pins | 1,287/1,287; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 153 extraction (1,287/1,287) |
| Changed | exactly seven = the declared list: `carrier-format.v3.md`, the contract (`d8022f4b…` → `913916c6…`) and five manifests (every changed manifest line is a SHA-256 value); before-images equal my 153 bytes |
| Python | 84/84 byte-identical to 153 (hence 145) |
| Lanes, fresh scratch | all seven exit 0, counts unchanged (168+145+6,000+1,803 · 423 · 581 · 435 · 2,193 · 231 · 477+66) |
| Binding | one byte appended to either document in a scratch copy: security and native refuse; foundation, workflows and carrier pass (151 N-2, unchanged and disclosed). (My first inline loop reported exit 0 for everything — a shell slip, preserved as `pin-binding-FAILED-r1.txt`; `pin_binding.sh` is the valid run.) |

As the request says, the lanes consume already-admitted projections and **cannot** prove an SQL mirror policy; the
executable boundary is Rust 154/159, which I reviewed separately (159: compatibility cost demonstrated on
DDL-lawful rows; all my 154 mutants killed).

## 2. Assessment of the owner decision
**I agree with the decision, as a decision.** My 154 F-1 asked for exactly this: either cite a frozen source for
NULL-iff-absent or record it as an owner choice with its consequence. The paragraph does the second, and says so in
terms — "an explicit additional typed-reader policy, not a constraint derived from carrierFormat1's DDL or its
'grant-bearing records' comment". The reasoning in OWNER-DECISION.md is sound: a typed population that silently picks
between two persisted representations, or invents a missing binding, is worse than one that declines.

The consequences are all stated and none is hidden:
- refusal is of the **whole requested generation**, hence of a complete migrated population (matches Rust 154/155);
- bytes are preserved; the row is never omitted, mirrored by invention, relabelled schema 3, read as absence or as
  not-committed;
- "this disagreement alone does not prove tampering";
- no repair, restore, writer authorization;
- a separately reviewed diagnostic reader is allowed and may not upgrade what it shows.
It is consistent with the executable reader on every clause (five optional mirrors; equal when present; NULL when
absent), and it rewrites neither the frozen DDL nor history.

## 3. Findings
- **F-1 (low–medium, wording at the one place a host will act on) — "report unavailable custody" is not a standing in
  this document.** §8.1's read-only route table is closed: `binding-unusable`, `unknown-quarantine-condition`,
  `unknown-carrier-incompatible`, `unknown-custody`, `unavailable-busy`. "unavailable custody" is none of them and
  sits lexically between two with **opposite** public meaning: `unknown-custody` (operational-failed / 4 /
  `HOST.IO_FAILURE` / `host-io`, no `domainDetail`) and `unavailable-busy` (`LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY` — a
  *retry* signal). A mirror-policy refusal is permanent for that carrier; routing it to busy would make a caller retry
  forever, and routing it to `unknown-quarantine-condition` (`LEDGER.CORRUPT`) would contradict "does not prove
  tampering". The request and OWNER-DECISION.md both say *unknown custody*; the normative text should too. Since the
  paragraph also promises "no new public error vocabulary", the fix is to name the existing standing and its row —
  e.g. "report `unknown-custody` (§8.1) on the read-only path; never `unavailable-busy`, `unknown-quarantine-condition`
  or not-committed" — and to add the observation ("an inherited generation the typed reader cannot admit") to that
  row of the table so the route is owned where routes are owned. This is the same mapping I asked for in 150 F-2 for
  `MarkerUnavailable`; one sentence can cover both.
- **F-2 (low) — the writer / maintenance-open disposition is not stated.** The paragraph speaks only of the read-only
  path. A writer or maintenance open of a published migrated carrier whose history this reader cannot admit has, in
  §8.1, only `LEDGER.CORRUPT`/`MIGRATION.CORRUPT` rows to fall into — again contradicting "not proof of tampering",
  and "no writer authorization follows" does not say what *does* follow. Either name the row or say explicitly that
  the writer-side disposition is not decided by this profile.
- **N-1 (note)** The policy covers the five *optional* mirrors. The reader also binds the mandatory ones (generation,
  sequence, `record_type`, `operation_ref`, `body_sha256`) to the body, and treats `prev_sha256` as diagnostic only. A
  clause pointing at that ("mandatory mirrors are compared likewise; the previous-digest column is diagnostic") would
  make §9 a complete statement of what 154 does, so the reference and the reader cannot drift on the unmentioned half.
- **W (very low)** 153 W-3/W-4 are folded in accurately ("the deferred DR-113 lifecycle slice"; the cause "is
  unreachable in that preview and remains typed reserved historical input"). "that preview" has no antecedent inside
  the contract paragraph — "in the v8 preview" would read cleanly.

## 4. Closure
| My item | Status |
|---|---|
| history154 **F-1** implicit compatibility decision | **Closed as a decision** — explicit owner choice, cost stated, demonstrated in 159; its public route needs the one-word precision of F-1 above |
| population153 **W-3**, **W-4** | **Closed** (modulo "that preview") |
| population151 N-1/N-2 | unchanged, disclosed |

## 5. Bounded verdict
**160: reviewed, no blocking finding. Exactly two documents and five hash rebindings changed; all executable reference
bytes are identical to 153/145; all seven lanes pass unchanged. The mirror policy is stated as what it is — an owner
choice stricter than frozen DDL1 — with every consequence named and none hidden, and it agrees clause for clause with
the reviewed Rust reader. F-1: the normative sentence says "unavailable custody", which is not one of §8.1's five
standings and lies between `unknown-custody` and the retryable `unavailable-busy`; name `unknown-custody` and give the
observation a row. F-2: the writer/maintenance-open disposition for such a carrier is unstated.** Not approval of any
host mapping (none exists), of the Rust candidates, or of any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (seven), `owner/`
(seven lanes + `exits.txt`), `probes/{pin_binding.sh, pin-binding.txt, pin-binding-FAILED-r1.txt}`, `hashes.txt`.
