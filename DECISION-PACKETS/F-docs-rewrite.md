# F — Documentation rewrite after sealing: decision packet

> **Decision-support only.** Nothing here is decided, moved, or edited. Every item in §6 is the owner's. Written 2026-08-27 by the Claude orchestrator's synthesis subagent at HEAD `4abb961aad98525ca8b992a24609a6286964a451` (last COORD heading `## D-292 — Record g21 leftover-join.v13 as G21 leftover remasurement`, COORD L16035). Nothing under `docs/` was read for mutation; the only output is this file.

**Sources of truth.** `docs/v2/architecture/08-decision-and-readiness-register.md` (file 08; sha256 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`, 429 lines); `docs/coop/COORDINATOR-DECISIONS.md` (COORD; sha256 `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466`, 16165 lines, 277 `## D-NNN —` headings, 10 containing `(CONTESTED)`); `docs/coop/artifacts/` (frozen). Line references are `08:L<n>` and `COORD:L<n>`.

**Inputs synthesised** (each read in full; the verifier findings quoted in the dispatch were applied as corrections — see §0.2):

| Inventory | Path | Verifier verdict | Findings applied here |
|---|---|---|---|
| Contracts / register rows | `DECISION-PACKETS/F-inventory-contracts.md` | REJECT | 3 |
| Gates G01–G32 | `DECISION-PACKETS/F-inventory-gates.md` | REJECT | 2 |
| COORD entries D-000…D-292 | `DECISION-PACKETS/F-inventory-decisions.md` | REJECT | 3 |
| Other material under `docs/` | `DECISION-PACKETS/F-inventory-other-docs.md` | REJECT | 8 |

Packet contents: §1 content inventory summary; §2 proposed tree; §3 per-doc-type templates; §4 derivation and review process; §5 sizing; §6 owner options; §7 risks; §8 open questions; §9 citations.

---

## 0. Rules applied and corrections carried

### 0.1 Rules

- **Currency rule (per task).** "Current/final" of an artifact lineage = the highest version recorded by a non-CONTESTED COORD heading of the form `## D-NNN — Record <artifact> …` (the **COORD rule**); for design contracts, alternatively the version the file 08 row cell names (the **cell rule**). Every row of the §1.5 table states which rule produced its version; divergent rows show both.
- **CONTESTED headings are parked, not adopted** (COORD D-000 clause 2, COORD:L32–L35: "the decision is recorded `CONTESTED` with both positions, parked"). The ten CONTESTED headings (`D-017 / D-019–D-024` L1490, `D-059` L2469, `D-051 / D-052 / D-053` L2640, `D-067` L2733, `D-094` L3738, `D-095` L3772, `D-098` L3870, `D-099` L3901, `D-101` L3932, `D-272` L13963) never supply a current version.
- **Status tokens** are the leading label of a file 08 status cell (08:L401–L404). Tokens and version numbers are quoted verbatim; an absent value is written "not in the record".
- **"Final version" is not "accepted".** Every harness occupancy, corpus, contract candidate and leftover-join listed below carries `status` `CANDIDATE-NOT-APPLIED` in its own bytes and "binds NOTHING" in its recording entry (e.g. D-292 COORD:L16076–L16077 "The candidate binds NOTHING"; gates inventory Summary: "28 × `CANDIDATE-NOT-APPLIED`, 0 × `QUALIFIED`"). "Final" here means only "the version the sealed record leaves current"; standing is stated separately in every table.
- **Classification vocabulary used in this packet** (reconciling the four inventories, which used four different schemes):
  - `DESIGN-FINAL` — row lead label `SATISFIED` and the design content is an independently accepted contract or an adopted D-000 decision (contracts inventory §0).
  - `DESIGN-CANDIDATE` — a non-CONTESTED Record heading records an accepted candidate artifact (design contract, harness occupancy, corpus) for a row that is not `SATISFIED` (contracts inventory §0). The gates inventory's label "DESIGN-FINAL" for current occupancies and named corpora is **renamed `DESIGN-CANDIDATE (final occupancy version)`** in this packet, because those artifacts are `CANDIDATE-NOT-APPLIED` and their gate rows are `OPEN`/`HARD-BLOCKED` (gates inventory Rule 7 says its label "is this packet's proposal … not a status in the record").
  - `PROCESS-ONLY` — neither of the above: V1 prerequisite tracking, re-review gates, release qualification, deferrals, predecessor versions, reviews, drafts, dispatch texts, logs, prompts.
  - For prose under `docs/` (other-docs inventory §0): `DESIGN-SOURCE`, `REFERENCE`, `PROCESS-ONLY`, `STALE`, `UNKNOWN`.
  - For COORD entries (decisions inventory §1): `BINDING-DESIGN`, `CUSTODY`, `PROCESS`, `PARKED`.

### 0.2 Verifier corrections applied (do not re-import the original error)

| Inventory · location | Original claim | Correction used in this packet | Verified against bytes here |
|---|---|---|---|
| contracts §2 DR-117 Standing; §4c; §5 Q3 | Quote "Gate 1 Class A remains false under D-137's express reservation" attributed to D-137 | The sentence is in D-168 (COORD:L7092–L7093) and D-207 (COORD:L9096–L9097), both describing D-137's reservation; D-137's own words are "D-056 Class A is not opened" (COORD:L5812–L5813) | yes — all three ranges re-read |
| contracts §0 `CANDIDATE-NOT-APPLIED` test as applied to DR-111 (D-103), DR-103 (D-104/D-106), DR-112 (D-105), DR-107 (D-107), DR-120 (D-108), DR-105 (D-109) | Test required the entry to say "binds NOTHING" | Widened test: "a non-CONTESTED Record heading records an accepted candidate and the entry states no `SATISFIED` / row stays `OPEN` (or its own token) / `D-056 Class A is not opened` / does not edit file 08". Actual wording: D-103 "DR-111 stays OPEN. No SATISFIED. … D-056 Class A is not opened. Does not edit file 08" (L4064–L4067); D-104 "DR-103 stays OPEN. No SATISFIED. … D-056 Class A is not opened" (L4108–L4110); D-105 "DR-112 stays OPEN. No SATISFIED. … D-056 Class A is not opened" (L4153–L4158); D-106 "DR-103 stays OPEN. No SATISFIED. … D-056 Class A is not opened" (L4206–L4211); D-107 "DR-107 stays PROPOSED-CLOSED-FOR-REVIEW / OPEN. No SATISFIED. … D-056 Class A is not opened" (L4254–L4259); D-108 "DR-120 stays OPEN. No SATISFIED. … D-056 Class A is not opened" (L4301–L4304); D-109 "DR-105 stays OPEN. No SATISFIED. … D-056 Class A is not opened" (L4347–L4350). The literal token `binds NOTHING` first appears in this series at D-110 (L4396) | yes — all seven ranges re-read |
| contracts §4b "Standing counts" | "none 21" | **none 23** (the Standing column: DR-002–DR-012 = 11, DR-128/129/130 = 3, DR-201–205 = 5, DR-G06/G11/G13/G17 = 4; 11+3+5+4 = 23) | recount from the inventory's own column |
| gates L313 (DR-G16) | "the occupancy also references g16-input-corpus.v1.json" | Dropped; `g16-input-corpus.v1.json` is pinned only by `g16-input-corpus.v2.json`'s own bytes (gates Appendix A last paragraph lists it under "superseded predecessors … pinned as `basedOn`") | inventory text |
| gates L29 and L658 | "file 08 line 421" for the condition-4 snapshot cell | **08:L417** (condition 4 row: "**32 of 32 owners named** … 29 `OPEN`, 3 `HARD-BLOCKED`") | yes — 08:L417 re-read |
| decisions §5 preamble (L379) | "no BINDING-DESIGN entry has a later non-CONTESTED Record heading for the same artifact except D-038" | Three do: D-038 `host-effect-authorization.v8` → v25 at D-126 (L5197); D-086 `gate-harness-naming.v3` → v6 at D-145 (L6066); D-013 `component-manifest-schemas.v2` → v11 at D-104 (L4076). Current under the COORD rule: v25 / v6 / v11. Cell rule: the DR-103 cell (08:L285) names `component-manifest-schemas.v2`; DR-105/DR-114 cells (08:L287, L296) name `host-effect-authorization.v8`; the gate-naming parent is not named in a cell | inventory §5b and contracts §4c |
| decisions §4 D-017 row (L362) and §6.2 (L555) | "no entry cites D-019…D-024 individually" | D-018 cites D-019 and D-020 by number: "Route selection is D-019 and D-020, if adopted" (COORD:L1455); the route selections landed as D-028/D-029/D-030. Only D-021–D-024 have no per-number citation outside the D-017 entry | yes — COORD:L1453–L1457 re-read |
| decisions §7 D-096 row (L599) | Status "name only" for `deferral.DR-106-109-113.preview.v2` | D-096 does not name that file; its Decision says "the five preview-deferral v2 artifacts" (L3818). The five on-disk files and their digests are listed in §1.5 row "deferral.*" of this packet (measured with `shasum -a 256`) | yes — `ls`/`shasum` here |
| other-docs §2.2 rows 36, 40 | sha256 prefixes `f813693cc9105815`, `5949bb3c6c945811` | `f813693cc910581d` (cleansheet-a/decisions.json), `5949bb3c6c944581` (cleansheet-c/decisions.json) | yes — remeasured |
| other-docs §2.4 row 59 | "`check-versioning` v1–v14" | On disk: `check-versioning.py` plus `check-versioning-v5.py` … `check-versioning-v14.py` (11 files) | yes — `ls` |
| other-docs §1 D10, §2.3 row 43, §3.2, §5 | README L83-85 for the reservation sentence | **`docs/v2/architecture/README.md` L94**: "`docs/v2/implementation/` remains reserved and absent until the central register explicitly reaches blueprint-ready and product/architecture authorities approve." | yes — `grep -n` |
| other-docs §2.1 rows 1, 8 | `docs/README.md` L9 | A→I plan is linked at `docs/README.md` **L10**; the claim-register pointer is **L13** | yes — `cat -n` |
| other-docs §2.1 row 11 | "L5 upstream `zzet/gortex@4d2f4972…`" | **L4** | yes |
| other-docs §2.1 row 18 | D-005 records both review outcomes | D-005 (`## D-005 — Apply r1-lifetime-neutrality.conformance.v1.9`, L596) records the v1.9 outcome only; the v7 review's outcome is not in the record under COORD (that lineage was later applied at v12 by `## D-003 — Apply evidence-identity-recipes.v12`, L514) | inventory text + COORD headings |
| other-docs §2.2 rows 35–40 | STALE reason cites `11-traceability.md` L7-8 as absorption evidence | The traceability source list names `agents-log.md`, not the cleansheet files — inventory inference; the cited superseder is the `agents-log.md` adjudication (B-ADJ-01..07) | inventory text |
| other-docs §2.1 row 14 (`agents-log.md`) | PROCESS-ONLY | **REFERENCE** (declared provenance source per `11-traceability.md` L7-8, L175). §4 counts become REFERENCE **38** / PROCESS-ONLY **10** | recount |

### 0.3 Corrections from the recommendation exchange (Codex rounds 1–3; independent re-verifications)

`DECISION-PACKETS/F-docs-rewrite.codex-recommendation.json` (round 1, verdict `DISAGREE`) found nine structural defects in this packet's drafts and recommendation lines, and `DECISION-PACKETS/F-docs-rewrite.codex-recommendation.r2.json` (round 2, verdict `AGREE-WITH-AMENDMENT`) found six more, carried as its three amendments; the reconciled position is `DECISION-PACKETS/F-docs-rewrite.claude-recommendation.r3.md`. After round 1 and before those round-2 repairs, an independent re-verification of the 15 verifier fixes (`DECISION-PACKETS/.verify/F-docs-rewrite.md.reverify1.json`) produced three wording corrections (its `newErrors` 1–3; its fourth item is recorded there as nits) that were applied to this file before the Codex-driven repairs below — that intermediate state is not retained and was never a reviewed subject. A second independent re-verification (`DECISION-PACKETS/.verify/F-docs-rewrite.md.reverify2.json`, verdict `REJECT`) then found eight further defects plus the clause-1/clause-4 inconsistency recorded in its own row below, all repaired. Each defect is repaired in place above and recorded below so the original error is not re-imported. Refutations 1–6, 9 and 16 of the round-1 review, and refutations 1–3 and 10 of the round-2 review, found no defect in the packet's bytes. `DECISION-PACKETS/F-docs-rewrite.codex-recommendation.r3.json` (round 3, verdict `AGREE-WITH-AMENDMENT`, confidence high) then found five consistency defects in this packet — its refutations 5–9, carried as its amendments 1–5 — and one in the round-3 reply (refutation 10, amendment 6); the protocol allows no fourth exchange, so all six were applied without a further Codex reply, and each is a row at the end of this table and an item of `DECISION-PACKETS/F-docs-rewrite.claude-postnote.md`. Refutations 1–4, 11 and 12 of the round-3 review found no defect in the packet's bytes. A third independent re-verification (`DECISION-PACKETS/.verify/F-docs-rewrite.md.reverify3.json`, verdict `REJECT`) ran against the state of this file before those round-3 amendments were applied — a state that is not retained and was never a reviewed subject — and found two further defects and six nits; each is a row at the end of this table, and the one whose subject the round-3 amendments had already repaired is recorded there as needing no byte change.

| Finding | Original claim in this packet | Correction now in this packet | Verified against bytes here |
|---|---|---|---|
| Codex r1 · refutation 7 | §4.5 5-B: D-SEAL may map condition 5's words "by the same mechanism D-010 used to amend condition 2's wording" | D-010's C-D010 amended file 08 **itself** — "Per D-001's new-row rule, C-D010 amends file 08's condition-2 wording" (COORD:L1003–L1004, within D-010 L1003–L1012; the historical range in D-001's blockquote is handled by the pin-note at COORD:L119–L122) — which is 5-C's form, not a later heading that maps words file 08 still carries. The 5-B row no longer cites D-010 as its mechanism; §4.5 and §6.5 recommendation lines updated | yes — COORD:L1003–L1012 and L116–L122 re-read |
| Codex r1 · refutation 8 | §6.2 recommendation: "the record's own convention is path + digest (D-033 property pins, COORD L1820)" | D-033's Subject is "DR-001 citation form only" (COORD:L1815) and its form is `(path, named section or selector, segment hash)` (COORD:L1823) — a DR-001 citation-form rule, not a record-wide full-file path + sha256 convention. The (a) recommendation now stands on the single-byte-home and drift grounds only | yes — COORD:L1812–L1826 re-read |
| Codex r1 · refutation 10 | §4.2 Subject: an in-tree manifest `docs/coop/artifacts/seal-manifest.v1.json`, "one path + sha256 per tracked file under docs/" | Unexecutable as prescribed: once tracked the manifest must hash itself, and it must hash `docs/coop/COORDINATOR-DECISIONS.md` while that file's D-SEAL bytes carry the manifest's digest. The Subject now cites the reviewed measurement artifact of `<P>` recorded as the penultimate heading; the all-files manifest is external (`docs/archive-manifest.v1.json`, §4.3–§4.4), produced after the move, and hashes every archived file including the terminal COORD bytes. §4.8 item 2 and §8 Q16 follow the new name | yes — the round-1 reviewed packet, sha256 `29d7a11c9a9ecd59ec9507d484a89eb1bfd4f2f48c86e415f5242efa4ec0d202`, L478–L483 as quoted in `F-docs-rewrite.codex-recommendation.json` refutation 10 |
| Codex r1 · refutation 11 | §4.2/§4.4: "Seal the design record at HEAD `<X>`", `<X>` identified in §4.4 as the seal's own commit | A commit id depends on the tree containing COORD, so an entry cannot carry the id of the commit that will contain it. D-SEAL now cites the already-known measured commit `<P>` throughout, and cites `<R>`, the commit that recorded the measurement heading preceding it — both known when the entry is written. The seal commit `<S>` and the rename commit `<M>` are described inside the sealed bytes ("the commit carrying this entry"; "the rename commit that immediately follows this entry's commit") and named nowhere in them; they are recorded only in `docs/ARCHIVE.md` (§4.4), which is written after both exist (Codex r2 amendment 1 and re-verification 2 `newErrors` 2, below) | yes — the round-1 reviewed packet, sha256 `29d7a11c9a9ecd59ec9507d484a89eb1bfd4f2f48c86e415f5242efa4ec0d202`, L465–L483 and L559 as quoted in `F-docs-rewrite.codex-recommendation.json` refutation 11; and the §4.2 / §4.4 drafts as they now stand |
| Codex r1 · refutation 12 | §4.3/§4.4: one commit that renames `docs/`, adds a new `docs/README.md`, and writes a new `<ARCHIVE>/README.md` | `docs/README.md` is tracked (`git ls-files docs/README.md`), so the rename already produces `<ARCHIVE>/README.md` from those bytes; adding a front door and rewriting that archive path in the same commit cannot be renames-only. `<M>` is now `git mv docs <ARCHIVE>` and nothing else; the front door, `docs/ARCHIVE.md` and the manifest are later commits; the archive gains no new file, and the §4.4 draft is retitled `docs/ARCHIVE.md` | yes — `git ls-files docs/README.md` run here |
| Codex r1 · refutation 13 | §4.1 precondition 3, §6.8(b), §7 R6: "`git mv` does not move untracked files, so they would be orphaned at the old path" | Codex's controlled test reproduced here in a throwaway repository: `git mv docs archive` reported `R  docs/tracked.txt -> archive/tracked.txt` and `?? archive/untracked.txt`, and `docs/` was gone — untracked files travel with the directory. The stated reason is now the untracked overlay: a byte-identical archive must not carry files the measurement never covered | yes — test rerun here under the session scratchpad |
| Codex r1 · refutation 14 | §6.8 recommendation: "move `DECISION-PACKETS/` into `<ARCHIVE>/packets/` in the same rename commit" | That adds bytes that were never members of the moved tree, breaking both the renames-only property of `<M>` and the byte-identity of the archive; `git ls-files DECISION-PACKETS` returns no files at HEAD `4abb961`, so the directory is untracked today. The recommendation is now to commit `DECISION-PACKETS/` at the repository root before the measurement | yes — `git ls-files DECISION-PACKETS` run here (0 files) |
| Codex r1 · refutation 15 | §4.2 clause 6: "Does not amend D-000 or D-056 except as clause 1 closes this register", while §6.10's recommendation moved authority to the ADR set | D-000 requires every decision made under the delegation protocol to be recorded in this register (COORD:L3–L4), in its stated entry format (COORD:L9–L12), with clause-3 fields and clause-4 commits per decision (COORD:L36–L42); closing it and seating new authoritative decisions elsewhere is substantive. Clause 1 now states the amendment explicitly, clause 6 says D-000 is amended exactly as clauses 1 and 4 state and in no other respect, and §6.10's (a) row records what that option would additionally amend | yes — COORD:L3–L12 and L36–L42 re-read |
| Codex r1 · refutation 20 | §6.6 recommendation: "list the 26 on **both** the gate page and the row page" | §4.8 item 4 requires every artifact to be reachable from exactly one page with no duplicate home. The canonical catalog is now on the row pages DR-105/DR-114 — whose joins name the corpora (`permission-leftover-join.v12`, D-283; `doctor-actor-leftover-join.v12`, D-285) — and G09/G12 cross-reference it | yes — the round-1 reviewed packet, sha256 `29d7a11c9a9ecd59ec9507d484a89eb1bfd4f2f48c86e415f5242efa4ec0d202`, L620 and L722 as quoted in `F-docs-rewrite.codex-recommendation.json` refutation 20 |
| Codex r2 · amendment 1 (refutations 4, 5, 6) | `<P>` was described both as the already-known input to the measurement and as the parent of the seal commit; `<ARCHIVE>/` was described as the `docs/` tree at `<P>`; the clause-2 mapping predicate was keyed to paths present at `<P>` | Four states, four placeholders, defined in the §2 legend and used throughout: `<P>` (the already-known measured commit), `<R>` (the D-000 measurement-record commit, which adds the measurement artifact, appends the penultimate COORD heading — both pinned to `<P>` — and carries that cycle's own draft, review-prompt and reviewer-verdict artifacts, as the re-verification 3 row below records), `<S>` (the user-seal commit, parent `<R>`, which appends D-SEAL and changes no other file) and `<M>` (the pure move). The archive is the `docs/` tree at `<S>` (§4.3–§4.4); the mapping predicate is the tracked paths present in the sealed tree at `<S>` immediately before the move, with `docs/v2/implementation/` the stated literal exception (§4.2 clauses 2–3, §4.5, §7 R4); the archive rule reads "nothing changes after the authorized pure move" (§4.4) | yes — `F-docs-rewrite.codex-recommendation.r2.json` refutations 4–6, and D-000 clause 4 re-read at COORD:L39–L42 |
| Codex r2 · amendment 2 (refutations 8, 9) | D-000 clause 4 was paraphrased as a commit-per-decision rule and the sequence omitted the pushes; D-SEAL's Reversibility claimed a total overturn by two reverts | D-000 clause 4 is "**Commit and push per decision** (user amendment 2026-08-12)" (COORD:L39–L42): `<R>` is committed and pushed before the seal, `<S>` is committed and pushed before the move (§4.1 preconditions 4–5, §4.3). D-SEAL's Reversibility now states the order — front-door/metadata commits, then the rename, then this entry — and is qualified as total only while no dependent post-move work exists (§4.2) | yes — COORD:L39–L42 re-read here ("**Commit and push per decision** (user amendment 2026-08-12), so the user can roll back or cherry-pick at decision granularity") |
| Codex r2 · amendment 3 (refutation 7) | the `Codex r1 · refutation` 10, 11 and 20 rows of this table cited a pre-correction packet by a sha256 prefix for which no artifact is retained and which was never a reviewed subject | Those three rows cite the round-1 reviewed subject, sha256 `29d7a11c9a9ecd59ec9507d484a89eb1bfd4f2f48c86e415f5242efa4ec0d202`, whose line ranges the round-1 Codex JSON quotes; the unretained intermediate state is described in the preamble above instead of being cited as a subject | yes — `F-docs-rewrite.codex-recommendation.json` refutation 1 (independent recomputation of `29d7a11c…`) and its refutations 10, 11, 20 |
| Re-verification 2 · `newErrors` 1 | §4.4: "`<ARCHIVE>/` is the byte-identical archive of the repository's `docs/` tree as it stood at the measured pre-seal commit `<P>`" | The archive is the `docs/` tree at `<S>` — the tree measured at `<P>`, plus what `<R>` adds (the measurement artifact, the penultimate COORD heading, and that D-000 cycle's own draft, review-prompt and reviewer-verdict artifacts under `docs/coop/artifacts/` — the enumeration corrected by re-verification 3, below), plus the single D-SEAL heading appended to COORD — moved unchanged by `<M>` (§4.4); §4.3 adds the `git diff --name-only <P> <R>` and `git diff --name-only <R> <S>` checks and anchors the commit-message example to `<S>` | yes — `.verify/F-docs-rewrite.md.reverify2.json` `newErrors` 1 and its `integrity` item on byte-identity |
| Re-verification 2 · `newErrors` 2 | The D-SEAL draft named `<S>` in its Commit field and `<M>` in clause 5 and Reversibility, and its trailing paragraph required every `<…>` token, `<S>` and `<M>` included, to be "measured at sealing time" | Neither placeholder appears in the sealed bytes: the Commit field, clause 5 and Reversibility describe those commits, and the trailing paragraph states that `<S>` and `<M>` are recorded only in `docs/ARCHIVE.md`, written after both exist (§4.2). Row `Codex r1 · refutation 11` above is restated to match | yes — `.verify/F-docs-rewrite.md.reverify2.json` `newErrors` 2 and its `integrity` item "Everything D-SEAL cites is knowable when the entry is written" |
| Re-verification 2 · `newErrors` 3 | The untracked-overlay guard was `git status --porcelain` (§4.1 precondition 3, §4.3, §7 R6) | `.gitignore` L4–L5 list `__pycache__/` and `*.pyc`, so those paths are ignored, not untracked, and plain porcelain never lists them: measured here, `git status --porcelain -- docs \| grep -c pycache` = 0 while `git status --porcelain --ignored -- docs` returns `!! docs/coop/artifacts/__pycache__/` (29 `.pyc` files at HEAD `4abb961`), and `git mv` carries that directory into the archive. The guard is now `git status --porcelain --ignored -- docs` before the measurement and `git status --porcelain --ignored -- <ARCHIVE>` after `<M>` (§4.1, §4.3, §7 R6) | yes — `.gitignore` L4–L5, both `git status` forms, and `find docs -name '*.pyc' \| wc -l` = 29, run here |
| Re-verification 2 · `newErrors` 4 | §2's legend defined a single stale sealing-commit placeholder (the `SEAL` token) and §2/§3 used it nine times, including §3.4's "Measured at" column header, over a column copied from a D-SEAL field headed "Measured at `<P>`" | The legend defines `<ARCHIVE>`, `<P>`, `<R>`, `<S>`, `<M>` and no longer defines the `SEAL` placeholder; every §2/§3 use is `<P>` where the measured state is meant (status/token columns, "Measured at") or `<S>` where the archived snapshot or derivation source is meant (§3.0 rule 5's front-matter line and the front-matter block, the `register/` row of §2.1) | yes — `.verify/F-docs-rewrite.md.reverify2.json` `newErrors` 4; no `SEAL` placeholder remains in this file, only the entry id `D-SEAL` |
| Re-verification 2 · `newErrors` 5 | §2's tree, §2.1's root row and §5.1's count omitted `docs/ARCHIVE.md` and `docs/archive-manifest.v1.json`, which §4.3–§4.4 and §4.8 item 6 require in the new tree, so the page carrying the path mapping sat outside the review regime | Both appear in §2's tree and §2.1's root row; `docs/ARCHIVE.md` is the fifth root page and is dual-reviewed like any other page (root pages **5**, total **128**, 149 with candidate ADRs — §5.1, §5.2); `docs/archive-manifest.v1.json` is validated by the pre-check script rather than dual-reviewed and is not a page in the §5 count (§4.8 item 2) | yes — `.verify/F-docs-rewrite.md.reverify2.json` `newErrors` 5; the §5.1 sum recomputed here (5 + 7 + 26 + 32 + 6 + 49 + 3 = 128) |
| Re-verification 2 · `newErrors` 6 | D-SEAL's Reversibility: "Total by `git revert` of the rename commit `<M>` and of this entry's commit `<S>` (the two commits are separate so each reverts cleanly)" | Reverting the rename while the new front door occupies `docs/README.md` conflicts, so the order is stated — front-door/metadata commits, then the rename, then this entry — and the claim is qualified: once derived pages or successor-register decisions exist, those are reversed or superseded first (§4.2) | yes — `.verify/F-docs-rewrite.md.reverify2.json` `newErrors` 6, against the post-move commits of §4.3 |
| Re-verification 2 · `newErrors` 7 | The D-001 pin-note was cited as `COORD:L119–L121` in §0.3 row 7, §4.5's 5-B row and §9 | The parenthetical runs COORD:L119–L122 (L122 is "operative.)*"); all three places cite L119–L122 | yes — COORD:L119–L122 re-read here |
| Re-verification 2 · `newErrors` 8 | §9 cited "D-033 L1801 (L1820 property-pin form)" while §0.3 row 8 and §6.2 pin the tuple | COORD:L1820 is the first line of D-033 clause 1 ("**Citation form.** Whole-document freeze and blueprint pins used"); the tuple `(path, named section or selector, segment hash)` is at L1823, which §9 now cites | yes — COORD:L1818–L1826 re-read here |
| Re-verification 2 · `integrity` (D-SEAL clause 6 vs clauses 1 and 4) | Clause 4 carried the §6.10 bracket but clause 1 did not, so under §6.10 option (a) clause 1's unbracketed text and clause 6's "in no other respect" would be falsified | Clause 1 gained a bracket, but its default assertions ("amends D-000 in one respect"; the successor "keeps D-000 clause 3's entry fields") stood outside it, so under option (a) they were not retracted — the residual defect re-verification 3 records below. Clause 1 now takes clause 4's form: the whole amendment sentence is bracketed and both option texts are supplied, and clause 6's appositive gloss is bracketed the same way (§4.2, §6.10) | yes — `.verify/F-docs-rewrite.md.reverify2.json` `integrity` item "D-SEAL clause 6's negation vs clauses 1 and 4", and `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 2 for the residual, repaired in the row below |
| Codex r3 · amendment 1 (refutation 5) | D-SEAL clause 2 mapped only paths cited "in this register, in file 08, or in any frozen artifact", while `docs/ARCHIVE.md`'s mapping paragraph also mapped citations in `DECISION-PACKETS/` and §6.8 said the five named root working-file classes acquire mapped citations "by the D-SEAL mapping clause" — later sections claiming more than the operative clause granted | One rule, stated in the same terms in all four places: a `docs/<p>` citation **written in or before the sealing entry, in any tracked repository file present at `<S>`** (inside the sealed entry: in the tree of the commit carrying it) resolves to `<ARCHIVE>/<p>` **when `docs/<p>` is itself a tracked path in that tree, immediately before the move**; a path absent from the tree is not remapped (clause 3 carries the one such path the record names), and a citation written after the seal is not mapped and names its target directly (§4.2 clause 2, §4.4 "Path mapping", §6.8 root working-files row, §7 R4) | yes — `F-docs-rewrite.codex-recommendation.r3.json` refutation 5, and the four passages (packet L547–L556, L673–L682, L857, L888 as they stood) re-read here |
| Codex r3 · amendment 2 (refutation 6) | D-SEAL clause 3's default text, §4.5's 5-A-as-amended row and §6.5's recommendation line called `docs/v2/implementation/` "reserved" at the seal, carrying 08:L395's pre-authorization wording forward as current standing | Condition 5 MET is a §4.1 precondition, so at `<P>` the authorization 08:L392–L393 names has been given: an absent `docs/v2/implementation/` is **authorized but not yet created**, preserved literally as the prospective live path, and nothing is created for it. 08:L395 ("Until then, `docs/v2/implementation/` remains reserved and absent") is quoted as the position before that authorization — history, not this entry's statement of current standing (§4.2 clause 3, §4.4 mapping example, §4.5, §6.5) | yes — 08:L388–L395 re-read here: L390–L391 condition 4, L392–L393 condition 5 ("Product and architecture authorities explicitly authorize creation of / `docs/v2/implementation/` against a refreshed exact authority baseline."), L394 blank, L395 "Until then, `docs/v2/implementation/` remains reserved and absent." |
| Codex r3 · amendment 3 (refutation 7) | §2's tree, §2.1's root row and §4.3's post-`<M>` steps omitted the successor register that §6.10 (b) names and §4.8 item 9 requires; and item 9 made the owner's sign-off that register's first entry although item 1 records a CONTESTED page's disposition there, which can come first | `docs/DECISIONS.md` — the successor decision register D-SEAL clause 4 names, in §6.10 (b)'s COORD form (under §6.10 (a) the same content is ADRs in `decisions/` instead) — is in §2's tree, in §2.1's root row and in §4.3's commits after `<M>`, and is stated in both places to be **not** one of the 128 derived review pages, so §5.1's counts are unchanged. Whichever entry that register records first cites D-SEAL and `<P>` (clause 4); the owner's sign-off is that first entry only if no post-seal decision and no CONTESTED-page disposition was recorded earlier, and otherwise follows them (§4.8 items 1, 6 and 9) | yes — `F-docs-rewrite.codex-recommendation.r3.json` refutation 7; §6.10 (b), §4.3, §4.8 items 1/6/9 and D-SEAL clause 4 re-read here |
| Codex r3 · amendment 4 (refutation 8) | §4.4 rule 3: the manifest "is regenerated only if the archive is shown to have changed — which is itself the defect of rule 1", which would let the detector be re-minted to agree with the defect rule 1 forbids | `docs/archive-manifest.v1.json` is **pinned to the archive as it stood at `<M>`** and is never regenerated from changed bytes: a mismatch is repaired by restoring the archived bytes, or the original manifest if the manifest was what changed. An intentional new archive state is a separate act needing an explicit authorization recorded in the successor register and a new manifest version (`archive-manifest.v2.json`, …), which leaves the `v1` manifest as the pin on `<M>` (§4.4 rule 3; §4.8 item 2 validates without rewriting, item 8's CI reports a mismatch and never regenerates) | yes — `F-docs-rewrite.codex-recommendation.r3.json` refutation 8; §4.4 rules 1–4 and §4.8 items 2 and 8 re-read here |
| Codex r3 · amendment 5 (refutation 9) | §2's `decisions/` line and §5.1 said "70 if candidates are included", §2.1's decisions row and §1.2 tied the 21 candidate groups to "§6.3/§6.4", and §6.4's recommendation includes candidates — so §6.4 (b) read as if it also selected the 21 extra ADRs and the 149-page scenario | Two separate choices, said so in every place the trigger appears: §6.4 (b) governs whether candidates appear, labelled, on the contract, gate and design pages and adds no ADRs; §6.3 (b) keeps exactly **49** ADR groups and the **128**-page baseline; the 21 candidate-ADR groups of §1.2/§5b are a separate expansion of §6.3 that §6.4 (b) does not select, and the total is 149 only if the owner selects it (§1.2, §2, §2.1, §5.1, §5.2, §6.3, §6.4). The arithmetic is unchanged | yes — the §5.1 sum recomputed here (5 + 7 + 26 + 32 + 6 + 49 + 3 = 128; + 21 = 149); `F-docs-rewrite.codex-recommendation.r3.json` refutation 9 |
| Codex r3 · amendment 6 (refutation 10) — in the reply file, not in this packet | Claude's round-3 reply (`DECISION-PACKETS/F-docs-rewrite.claude-recommendation.r3.md`) said the ignored artifact cache holds "30+" `.pyc` files | The measured count at HEAD `4abb961` is **29**, and the reply now says 29. No packet byte changed for this row: §0.3 (re-verification 2 `newErrors` 3), §4.1 precondition 3 and §7 R6 already said 29 | yes — `find docs/coop/artifacts/__pycache__ -type f -name '*.pyc' \| wc -l` = 29 run here, and no `30+` remains in the reply file (`grep -n '30+'` returns nothing) |
| Re-verification 3 · `newErrors` 1 (defect) | §4.3: "`git diff --name-only <P> <R>` returns exactly two paths, the measurement artifact `<MEASUREMENT-PATH>` and `docs/coop/COORDINATOR-DECISIONS.md`" — and with it the §2 legend's, §4.1 precondition 4's, §4.4's and R10's account of the `<P>`→`<S>` delta as the measurement artifact plus the two appended headings | A D-000 cycle commit is never two files. Measured here: `git show --name-only --format= 4abb961` (D-292) lists **13** files — COORD, the D-292 draft and its turn-2 draft, the two matching review prompts, four `review-adversarial.{claude2,codex}[.turn2].json` verdicts, `g21-leftover-join.v13.json`, its two `review-independent` verdicts and its review prompt — and `cb8bd16` (D-291), `20e6d2d` (D-290) and `8d0cf09` (D-288) list **9** files each on the same pattern, everything but COORD under `docs/coop/artifacts/`. The check now returns COORD, `<MEASUREMENT-PATH>` and that cycle's own draft, review-prompt and reviewer-verdict artifacts, each enumerated by path in the measurement entry's Status field so the check is exact, and nothing else; the `<R>` additions are stated in full in §2's legend, §4.1 precondition 4, §4.3, §4.4's opening paragraph and Measurement-commit row, and R10; R6 records those tracked artifacts as the one measured-tree addition the archive is designed to carry; and the `<R>`→`<S>` one-file check is stated to assume the user-made seal form of §6.7 (a), since under §6.7's bracketed (b) ALTERNATIVE `<S>` carries review artifacts of its own | yes — `git show --stat --format=` and `git show --name-only --format=` run here on 4abb961 / cb8bd16 / 20e6d2d / 8d0cf09 (13 / 9 / 9 / 9 files changed); D-292's Status field COORD:L16038–L16050 and Subject COORD:L16072–L16073 re-read, and that entry (COORD:L16035–L16165) carries no `review-independent` citation; `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 1 |
| Re-verification 3 · `newErrors` 2 (defect) | D-SEAL clause 1 asserted "amends D-000 in one respect" and that the successor "keeps D-000 clause 3's entry fields" outside its §6.10 bracket, so under option (a) — which §6.10(a) itself describes as amending D-000 "in three respects beyond location", the entry form included — the bracket added amendments without retracting those assertions; clause 6's appositive gloss enumerated only the (b) content | Clause 1 now takes clause 4's form: the whole amendment sentence is bracketed and both texts are supplied — option (b) "amends D-000 in one respect: the register's location …", keeping clause 3's entry fields and clause 4's commit-and-push rule; option (a) "amends D-000 in four respects: the register's location; the end of the D-NNN series; the entry form; and the authority of the ADR set (§6.10(a))", with clause 4's "**Commit and push per decision**" (COORD:L39–L42) unchanged either way. Clause 6's appositive is bracketed the same way, so it enumerates the chosen option's content. The fenced draft still names neither `<S>` nor `<M>` | yes — `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 2 and its `integrity` item "Clauses 1, 4 and 6 stay consistent under BOTH §6.10 options"; §6.10 rows (a) and (b) and COORD:L3–L12 / L36–L42 re-read here; `grep -c` for `<S>` and `<M>` between the §4.2 fence markers = 0 |
| Re-verification 3 · `newErrors` 3 (nit) — already repaired, no byte changed | `docs/ARCHIVE.md`'s path-mapping paragraph and §6.8 mapped citations written in `DECISION-PACKETS/`, while D-SEAL clause 2 scoped the rule to "this register, in file 08, or in any frozen artifact" | Repaired before this pass by Codex r3 amendment 1 above, which the re-verification pre-dates: clause 2 maps a citation written before the entry "in any tracked repository file present in the tree of the commit carrying this entry — this register, file 08, a frozen artifact, or a tracked file outside `docs/`", which is the rule `docs/ARCHIVE.md`, §6.8 and R4 state. Nothing further was needed and no byte changed for this row | yes — §4.2 clause 2, §4.4 "Path mapping", §6.8's root working-files row and §7 R4 re-read here; `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 3 |
| Re-verification 3 · `newErrors` 4 (nit) | §4.4's opening paragraph asserted the `<R>` addition unconditionally while its own mapping example said "`<MEASUREMENT-PATH>`, if it is under `docs/`" | `<MEASUREMENT-PATH>` is required to be a path under `docs/coop/artifacts/` — the record's uniform home for cycle artifacts — in §4.2's Subject and in §4.4, and the conditional is dropped from the §4.4 mapping example | yes — `ls docs/coop/artifacts` run here (5566 entries; every artifact of the four decision commits measured above sits there); `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 4 |
| Re-verification 3 · `newErrors` 5 (nit) | §4.2's Subject pinned "the sha256 of `docs/coop/COORDINATOR-DECISIONS.md` taken up to and including the last heading of that register before the measurement heading", which admits a heading-line-only reading, and §4.3 prescribed no way to recompute a prefix digest | The Subject defines the prefix exactly — from the first byte of the file through the last byte preceding the measurement heading's `## ` line, with that prefix's length in bytes recorded beside the digest, so entry bodies are covered — and §4.3 states the recomputation: extract that byte range from the archived register and hash it, never the whole file. §4.3's `<R>`→`<S>` check adds `git diff --numstat <R> <S>`, whose zero deleted lines show the seal appends and removes nothing | yes — `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 5; the §4.2 Subject and §4.3 checks as they now stand |
| Re-verification 3 · `newErrors` 6 (nit) | R6 put the overlay risk at "anything left untracked or ignored under `docs/` at `<P>`" | New ignored files can appear after `<P>`: `.gitignore` L1–L3 records that any `.pyc` present "is the residue of an invocation that omitted -B", so a checker run at `<R>` or `<S>` creates them. R6 now reads "at any point up to `<M>`", matching the guard it cites — `git status --porcelain --ignored` runs before the measurement and again immediately before the move (§4.1 precondition 3, §4.3) | yes — `.gitignore` L1–L5 re-read here; `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 6 |
| Re-verification 3 · `newErrors` 7 (nit) | §9 cited D-000 "clauses 1–5 L26–L46" | COORD:L26 is the Decision lead-in ("- **Decision:** The assistant completes the coop design end-to-end, making"), clauses 1–5 run L29–L45 (L45 "procedure is written to cost less than the decision did."), and L46 opens "- **Sequencing note (standing):**"; §9 now cites "Decision L26–L45 (clauses 1–5 L29–L45)" | yes — COORD:L26, L29, L45 and L46 re-read here |
| Re-verification 3 · `newErrors` 8 (nit) | D-SEAL clause 2's tracked-path qualifier trailed the sentence ("… **when `docs/<p>` is itself a tracked path in that tree**"), so it could be read as attaching to the citing file rather than to the cited path | Clause 2 now opens with the qualifier attached to the path — "Every path of the form `docs/<p>` that is itself a tracked path in the tree of the commit carrying this entry, immediately before that rename** resolves to `<ARCHIVE>/<p>` from the rename on, wherever it is cited by a citation written in or before this entry in a tracked repository file present in that tree" — with the rule's substance exactly as Codex r3 amendment 1 left it; `docs/ARCHIVE.md`, §6.8 and R4 continue to state that same rule | yes — `.verify/F-docs-rewrite.md.reverify3.json` `newErrors` 8; §4.2 clause 2, §4.4, §6.8 and §7 R4 re-read here |
| Re-verification 4 · residual 1 (defect) | D-SEAL clause 2 mapped a path only where cited "by a citation written before this entry", which excluded the sealing entry's own citations of file 08 and of this register — while its closing sentence promised every sha256 in this register remains verifiable at the mapped path | Clause 2 now reads "written in or before this entry" and the later-citation sentence reads "first written after this entry"; `docs/ARCHIVE.md`, §6.8 and R4 read "in or before the sealing entry"; the row above for Codex r3 · amendment 1 says "stated in the same terms" rather than "identically" | yes — `.verify/F-docs-rewrite.md.reverify4.json` residual 1; clause 2 re-read after the edit; applied by the orchestrator by hand and byte-checked, not independently re-verified |
| Re-verification 4 · residuals 2–6 (nits) | §0.3 quoted clause 2 with a comma the bytes lack; §4.3 read `--numstat` zero deletions as proof that the seal *appends*; `<R>`'s parent was never stated; §2.1 called `DECISIONS.md` a "non-page file"; §4.1 precondition 2 still said "F1 NOT STARTED" | Quote made byte-exact; `--numstat` now proves only that nothing was removed (append position rests on D-SEAL being the last heading and on the prefix digest); §2 legend and §4.1 precondition 4 state `<R>`'s parent is `<P>`, `<S>`'s is `<R>`, `<M>`'s is `<S>`; §2.1 reads "neither of them one of the 128 review pages"; precondition 2 reads "F1 included" | yes — `.verify/F-docs-rewrite.md.reverify4.json` residuals 2–6; same hand pass as the row above |

---

## 1. Content inventory summary

### 1.1 Register rows (file 08) — 81 rows

Source: contracts inventory §1–§4b (corrected per §0.2).

| Class | Count | Rows |
|---|---|---|
| DESIGN-FINAL | **5** | DR-102 (`SATISFIED 2026-08-14 (D-085 / D-056 Class A)`, 08:L284), DR-104 (`SATISFIED 2026-08-23 (D-236 / D-056 Class B)`, L286), DR-115 (`SATISFIED 2026-08-14 (D-089 / D-056 Class B)`, L297), DR-119 (`SATISFIED 2026-08-14 (D-091 / D-056 Class B)`, L301), DR-123 (`SATISFIED 2026-08-14 (D-092 / D-056 Class B)`, L305). DR-001 also leads `SATISFIED` (08:L34) but is a V1 provenance check, classified PROCESS-ONLY. |
| DESIGN-CANDIDATE | **52** | 24 V2 rows: DR-101, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 120, 121, 122, 124, 125, 126, 127, 131, 133; 28 gate rows with a recorded occupancy: G01–G05, G07–G10, G12, G14–G16, G18–G32. |
| PROCESS-ONLY | **24** | DR-001–DR-012 (12), DR-128/129/130 (3), DR-201–DR-205 (5), DR-G06, G11, G13, G17 (4). |

Standing counts (corrected): `ACCEPTED (SATISFIED-grade)` 6 (DR-001, 102, 104, 115, 119, 123); `CANDIDATE-NOT-APPLIED` 52; `DECIDED-V1-NOT-INTEGRATED` 1 (DR-118, 08:L300, which also carries candidate v13); `PROPOSED-CLOSED-FOR-REVIEW` 2 (DR-107 08:L289, DR-122 08:L304 — both also carry a COORD candidate); `none` 23.

Register snapshot at HEAD (08:L397–L418): condition 1 **MET** (preview scope, 08:L414), condition 2 **NOT MET** ("**5 of 32 `SATISFIED`** — 24 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`", 08:L415), condition 3 **MET** (08:L416), condition 4 **MET** ("32 of 32 owners named … 28 of 28 required gates name a recorded identifier … 29 `OPEN`, 3 `HARD-BLOCKED`", 08:L417), condition 5 **NOT MET** ("Not started; structurally last, and gated on 1, 2 and 4", 08:L418). The rewrite is gated on all five (owner's agreement, `DECISIONS-NEEDED.md` F1).

Items that are PROCESS-ONLY as rows but carry **scope constraints the new design docs must honour by reference** (contracts inventory §5 Q4): riders RB-DR005-V2-A1 (08:L38), RB-DR009-V2-A1 (08:L42), RB-DR011-V3-A1/A2/A3 (08:L44), and `product-boundary-preview.v2`'s exclusions PB-1..PB-6 EXCLUDED / PB-7 NOT REPLACED (D-068, COORD:L2713); the D-002/D-010 deferral dispositions for DR-106/109/113 (deferred wholly), DR-108/110/116/128/129 (deferred), DR-130 (no upgrade continuity) (decisions inventory §2 rows D-002, D-010, D-018).

### 1.2 COORD entries — 277 headings

Source: decisions inventory §3 (literal CUSTODY reading).

| Class | Count | Notes |
|---|---|---|
| BINDING-DESIGN | **72** | 49 distinct ADR groups (decisions inventory §5). Sub-tags: gate-naming 14, route 10, disposition 10, owner-record 10, product 8, satisfied 5, rule 4, register-row 4, contract-accepted 4, v1-apply 3. |
| CUSTODY | **170** | leftover-remasurement 88, contract-candidate 33 (§5b), occupancy-remasurement 28, leftover-measurement 10, fixture-corpus 6, instrument 2, leftover-grouping 2, deferral-candidates 1. |
| PROCESS | **25** | mf6-transcription 7, hygiene 5, citation-convention 3, delegation 2, sequencing 2, mechanics 2, pin-correction 2, authority 1, grant-withdrawal 1. |
| PARKED | **10** | every CONTESTED heading has a later ADOPTED heading on the same subject (decisions inventory §4). |

Alternative reading (decisions inventory §6.1): if the 33 contract-candidate recordings are treated as design content, counts become BINDING-DESIGN 105 / CUSTODY 137 / PROCESS 25 / PARKED 10 and the ADR group count rises from 49 to 70 (49 + 21 new row groups: ADR-DR101, DR105, DR106, DR107, DR108, DR109, DR110, DR111, DR112, DR113, DR116, DR117, DR120, DR121, DR122, DR124, DR125, DR126, DR127, DR131, DR133; the remaining 12 candidate entries fold into existing groups ADR-DR103, ADR-DR114, ADR-HOSTEFFECT, ADR-IDENT, ADR-LQ). Adding these 21 groups to the ADR set is an expansion of owner option §6.3; §6.4 governs a different question — whether candidates appear, labelled, on the contract, gate and design pages at all — and selecting §6.4 (b) does not select this expansion.

### 1.3 Gate artifacts (G01–G32)

Source: gates inventory Summary, Table 1, Appendix A/B (corrected per §0.2).

- 28 gates have a current occupancy recorded by D-208…D-235 (all `ADOPTED 2026-08-22`, decisions inventory §2 rows 193–220); 4 have none (G06, G11 `HARD-BLOCKED` with no `named:` prefix; G13 "reserved, not named"; G17 "dropped / inapplicable (D-077 SARIF drop; D-086)").
- Occupancy `status` field: 28 × `CANDIDATE-NOT-APPLIED`, 0 × `QUALIFIED`; `reviewStatus` `AWAITING-INDEPENDENT-REVIEW` in every occupancy's own bytes (dual ACCEPT lives in the COORD entry and review siblings).
- Named corpora/catalogs/coverage-domain/fixture-corpus files reachable from a current occupancy or current gate join: **43 distinct files** (list in §1.5c). All carry `status` `CANDIDATE-NOT-APPLIED`; most have only a `claude2` review sibling and no COORD heading of their own (gates inventory open question 2).
- 21 gates have a current GATE leftover-join; G01–G05 are carried by `distribution-core-leftover-join.v9` (D-287), G31 by `identity-namespace-leftover-join.v6` (D-175), G32 by `doctor-actor-leftover-join.v12` (D-285).
- leftoverDesign `true` remaining: one `*-FX-AUTHORING` obligation per gate join except G23 (none `true`); plus G07 `OBL-FILESYSTEM-COVERAGE`, G10 `OBL-SELECTOR-REFRESH`.
- PROCESS-ONLY volume in this family: 78 predecessor occupancy files, 123 gate leftover-join files (current + predecessors), plus every `*.review-*`, `*.review-prompt.md`, `coordinator-decisions.D-*.draft.md`, `_dispatch.*.txt` sibling.

### 1.4 Other material under `docs/` — 82 inventory rows

Source: other-docs inventory §4 (corrected per §0.2: `agents-log.md` → REFERENCE).

| Class | Count | What it is |
|---|---|---|
| DESIGN-SOURCE | **24** | `docs/v2/architecture/00,01,02,03,04,05,10,12-*.md` (8); `docs/coop/architecture/00–09` (10); `IMPLEMENTATION-FREEZE.md`, `IMPLEMENTER-BLUEPRINT.md`, `v1-slice.md`, `product-dispositions.md`, `COORDINATOR-DECISIONS.md`, transition brief (6). |
| REFERENCE | **38** | glossary/conventions/evidence pins/indexes (`docs/v2/architecture/README.md` "Stable terms" L76–L88 and "Claim labels" L63–L74; `09-v1-to-v2-claim-matrix.md`; `v1-authority-baseline.json` — all 49 pinned digests MATCH live bytes; `v1-status-evidence.json`; `prototype-evidence-reference.md`; `docs/MAP-VS-CONTROL.md` (L3 `**Status:** product boundary (guidance)`; other-docs row 2; 0 matches in file 08/COORD); `TREE-ENDSTATE.md`; `GORTEX-BORROW-REGISTER.md`; `coop/architecture/10-method.md`, `11-traceability.md`; `steering/*` (4); `agents-log.md`; 124 `check-*.py`; `make-freeze-manifest.py`; 17 fixture directories (230 files)). |
| PROCESS-ONLY | **10** | `p.md`, `agentlog3.md`, `agentlog4.md`, `REVIEW-PROMPT-final.md`, `REVIEW-PROMPTS-2026-08-13.md`, 760 `_dispatch.*.txt` (31 untracked), `coordinator-decisions.D-057.turn2.FROZEN`, `_handoff.d000-orchestrator-live.txt`, `_recording-checklist.g31-after-dual-00.txt`, 29 `.pyc`. |
| STALE | **8** | `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` (superseded as checklist by 08:L370–L373 and D-001), 6 cleansheet files, `freeze-payload-manifest.txt` (D-014 COORD:L1377–L1381: "619 recorded paths against 694 live … 75 absent"). |
| UNKNOWN | **2** | `docs/coop/deltas/*.delta-draft.v1.md` — both self-declare non-binding, in different words, each at its own L3: `gortex-borrow-triage.delta-draft.v1.md` L3 "DRAFT. NOT ADOPTED. BINDS NOTHING. CHANGES NO STATUS."; `gortex-graph-lanes.delta-draft.v1.md` L3 "Status: DRAFT FOR REVIEW AFTER SIGNATURE. IT CHANGES NOTHING AND BINDS NOTHING.". 0 citations in file 08/COORD. Disposition is an owner call (§8). |

Whole-tree volume (other-docs §0): 5881 files under `docs/`; 5823 under `docs/coop/artifacts/` (3411 `.json`, 1470 `.md`, 763 `.txt`, 125 `.py`, 29 `.pyc`, 18 `.bin`, 2 `.onebyte`, 2 `.empty`, 1 `.sh`, 1 `.log`, 1 `.FROZEN`). Measured here in addition: 1338 files matching `review-independent`, 1093 matching `review-prompt`, 368 matching `coordinator-decisions.D-*draft`, 353 `harness.DR-G*` files, 262 non-review `*leftover-join*` files. `docs/v2/implementation/` does not exist and has no history at any ref (other-docs §3.2).

### 1.5 Final version per contract / harness / corpus / leftover-join lineage

Legend for the **Rule** column: `COORD` = highest non-CONTESTED Record heading; `cell` = version the file 08 row cell names; `cell = COORD` = both agree (single recorded version); `DIVERGENT` = cell names an older version than COORD (both shown; COORD version is final under the task rule, cell version is history — contracts inventory §4c, §5 Q2). Every digest is a full sha256 recomputed on disk by the inventories at HEAD `4abb961` (and, for the deferral files, by this packet).

#### 1.5a Design contracts and row-level candidates (26 rows; 32 artifact rows = 31 contract/corpus artifacts + 1 condition-4 naming candidate)

**The 31/32 rule (what "31" means wherever this packet writes it).** The table below has **32** artifact rows; rows DR-115, DR-119 and DR-123 carry a decision and no artifact and are not among them. The 32nd row is `dr117-ee-gate-naming` **v3** (row DR-117), whose Standing cell reads "condition-4 naming candidate" — not a contract or corpus. Excluding it gives the **31** used in §2 (`contracts/json/`), §2.1, §5.1 and §6.2(b). Two of those 31 — `component-manifest-fixture-corpus.v6` (DR-103) and `identity-namespace-negative-test-corpus.v1` (DR-104) — are also among the 43 named corpora of §1.5c, so the 31 of §1.5a ∪ the 43 of §1.5c = **72 distinct files, not 74**; in the proposed tree their single home is `gates/corpora/` (§4.8 item 4; §8 Q22).

| Row (08 line) | Lineage `docs/coop/artifacts/<name>` | Final version · sha256 | Recording heading (COORD line) | Rule | Cell names | Standing at HEAD |
|---|---|---|---|---|---|---|
| DR-101 (L283) | `distribution-core-inventory-contract` | **v16** `429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b` | D-114 (L4563) | COORD (cell names none) | none | CANDIDATE-NOT-APPLIED; row `OPEN` |
| DR-102 (L284) | `control-protocol-contract` | **v2** `c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca` | D-015 (L1201); SATISFIED at D-085 (L3508) | cell = COORD | v2 | ACCEPTED (SATISFIED-grade); remainder CC-1..CC-11 at DR-G21 |
| DR-103 (L285) | `component-manifest-schemas` | **v11** `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005` (cell: v2 `73114ddec12d3ec6dfbcb51b7002d983ff9dbfa1fa39189bb025008f1f501381`, D-013 L1150) | D-104 (L4076; the quoted sentence is at L4103: "D-013 remains the historical recording of schemas.v2") | DIVERGENT → v11 | v2 | CANDIDATE-NOT-APPLIED; row `OPEN — design contract ACCEPTED 2026-08-13 (D-013)…` |
| DR-103 | `component-manifest-fixture-corpus` | **v6** `8dfa9346ada4fefce0aabca96062208e4fea7371a6aab68eaee75cdc908a21a5` | D-106 (L4169) | COORD | none | CANDIDATE-NOT-APPLIED |
| DR-104 (L286) | policy at D-012 (L1050) — decision, no artifact; `identity-namespace-integration-contract` | **v4** `cd7ff948d95cf595ed1b7654c7ea2a458540f417cf13922373fcf8af8b280e62` | D-131 (L5493; v3 recorded at D-123 L5042; the sentence "remains the D-123 subject" is D-131's own, COORD L5526–L5527) | cell (D-012) + COORD (v4) | D-012 only | row ACCEPTED (SATISFIED-grade, D-236 L11125); contract v4 CANDIDATE-NOT-APPLIED |
| DR-104 | `identity-namespace-negative-test-corpus` | **v1** `2c0795cd58e95e56afad46899b3c5d546d4fb520e38e1a8c3f7c132aa69583dd` | D-130 (L5431) | COORD | none | CANDIDATE-NOT-APPLIED (fixtures for DR-G31) |
| DR-105 (L287) | `permission-truth-tables` | **v9** `05d559647d103a47c18ed5177b71900a1d9dfcdea6b9a1255aefcec5f09eaccb` (cell: v2 `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a` D-042 L1954; v6 `ad1bb75d7f029f64979d3c4e6fe5dd3446cd30465b36d4a7b3f9471f06a6dd34` D-109 L4317) | D-128 (L5312) | DIVERGENT → v9 | v2 | CANDIDATE-NOT-APPLIED; row `OPEN` |
| DR-105 / DR-114 | `host-effect-authorization` | **v25** `b91b9f739b10b1bd30eb56b9d68feac81c483ad86f50e11ed33b95e98ae2d9b9` (cell: v8 `2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc` D-038 L1744 / D-093 L3692) | D-126 (L5197: "Recorded v8 … is not retargeted") | DIVERGENT → v25 | v8 | CANDIDATE-NOT-APPLIED |
| DR-106 (L288) | `offline-analysis-closure-contract` | **v3** `f3b094bfabcaa20c0e8c8b5af64f7d9d9a14dda76fbc9606805e6b3f489bec11` | D-118 (L4824) | COORD | none | CANDIDATE-NOT-APPLIED; row `OPEN / inherits hard blockers`; deferred wholly (D-002) |
| DR-107 (L289) | `lifecycle-generation-contract` | **v2** `a5f9d6a35f83d64687cdd2a00ec3106251ae407e54a5538727c086dd8f9ab77b` | D-107 (L4224) | COORD | none | CANDIDATE-NOT-APPLIED; row `PROPOSED-CLOSED-FOR-REVIEW` |
| DR-108 (L290) | `secret-storage-contract` | **v3** `2919b5cd77782cdb3785650390de6b25725c850bd5b359bf7fccd62265651923` | D-112 (L4459) | COORD | none | CANDIDATE-NOT-APPLIED; row `OPEN` |
| DR-109 (L291) | `storage-mechanics-contract` | **v5** `8a43c5b53367a85615648129915d8b19e5b12b2bb32c972f2147093233bd20fb` | D-120 (L4886) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN / inherits hard blockers` |
| DR-110 (L292) | `self-update-repair-contract` | **v3** `73a44c2b07a2b8e8db48497a04557d99d65f91497a717eaf2fdf07fc8008690a` | D-121 (L4940) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-111 (L293) | `compatibility-matrices-contract` | **v5** `d0386cee26d8aafd3d07b46f21352cc3d9d03cdc8f406de0adf571f8c81f7f41` | D-103 (L4036) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-112 (L294) | `signed-index-trust-contract` | **v8** `fc171321e969c74464dbc9ff67edd9b874aac1d1c7375c7dc8e431469442efe0` | D-105 (L4122) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-113 (L295) | `replay-purge-contract` | **v2** `48cb28a5ea3a5609b2b74474a7599a386daeb7c373ec662241d35cd92b6a82e2` | D-119 (L4771) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN / inherits hard blockers` |
| DR-114 (L296) | `doctor-contract` | **v4** `df2e717555616db096e61548458f23b442f7f0e37b2d2461eabc2c33201e94b3` | D-035 (L1603) | cell = COORD | v4 | accepted design contract (D-035); row `OPEN — design contract ACCEPTED 2026-08-13 (D-035)…` |
| DR-114 | `doctor-actor-join-integration-contract` | **v8** `c830f954605a4a1d47c5643230439340994a0c42c4a487359541c578d00bc662` (v6 `f63554d534d249dfdb674be3c78b61bbd1a4a4bdeb56cb06247b24c647ab38d1` D-127 L5253) | D-129 (L5370) | COORD | none | CANDIDATE-NOT-APPLIED |
| DR-115 (L297) | thresholds at D-006 (L698) — decision, no artifact; fleet-class successor D-102 (L3963) | — | D-089 SATISFIED (L3545) | cell | D-006 | ACCEPTED (SATISFIED-grade); remainder measurement at DR-G01..G05 |
| DR-116 (L298) | `third-party-policy-contract` | **v1** `78386c7a386376508d9f44d8a3fbe1388b7c1b78798bceb74ab83002ab3ef442` | D-122 (L4991) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-117 (L299) | (a) `product-boundary-successor-contract` | **v8** `52c70f7715fb869bae70bc588043dc5b4d731b73408d2d451e868b8de963f362` | D-116 (L4669) | COORD | none | CANDIDATE-NOT-APPLIED ("leftover T2-02 candidate"); D-137 L5815–L5816: "v8 remains the D-116 leftover T2-02 candidate" |
| DR-117 | (b) `preview-product-boundary-successor` | **v8** `f2e788e51c347e1033073f0718e701d164affe51e7f667da9bcd49a08837144c` (v7 D-168 L7061; v5 `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` D-137 L5779) | D-207 (L9062, "leftover remasurement") | COORD | none | CANDIDATE-NOT-APPLIED; "D-056 Class A is not opened" (D-137 L5812–L5813); "Gate 1 Class A remains false under D-137's express reservation" (D-207 L9096–L9097). Two parallel lineages — owner question (§8) |
| DR-117 | `dr117-ee-gate-naming` | **v3** `fb5e928415098c7726bcd91f455327472b6ae7cfe34f65b288ba99cba3ef82c2` | D-159 (L6682) | COORD | none | condition-4 naming candidate |
| DR-118 (L300) | decisions D-002 (L342), D-007 (L820); `language-quality-matrix-contract` | **v13** `9efffdb3f7ec806bc967db5eff5868aea0a7d11524b1e026993a46505d35c2ae` | D-113 (L4510) | cell (decisions) + COORD (v13) | D-002/D-007 | row `DECIDED-V1-NOT-INTEGRATED`; v13 CANDIDATE-NOT-APPLIED |
| DR-119 (L301) | rule at D-008 (L923) — no artifact | — | D-091 SATISFIED (L3611) | cell | D-008 | ACCEPTED (SATISFIED-grade); remainder closure evidence at DR-G14 |
| DR-120 (L302) | `component-packaging-contract` | **v14** `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c` | D-108 (L4271) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-121 (L303) | `monorepo-ci-contract` | **v16** `67ca501660a2ba515ce37adc799c5418e4ffd156308189662245e5a5e45a2ddb` | D-124 (L5095) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-122 (L304) | `sarif-projection-contract` | **v15** `8996a92d00ddd47d212dbeecaf51f25b77b90d87aaa618cda9ad00749fd1d589` | D-115 (L4612) | COORD (cell names V1 `operability.v10.json` only) | `operability.v10` | CANDIDATE-NOT-APPLIED; row `PROPOSED-CLOSED-FOR-REVIEW`; G17 inapplicable (D-077) |
| DR-123 (L305) | baseline at D-009 (L960) — no artifact | — | D-092 SATISFIED (L3650) | cell | D-009 | ACCEPTED (SATISFIED-grade) |
| DR-124 (L306) | `state-class-contract` | **v11** `b5456c63e865b53738b1f11f46a898438afca7890a6069a8653aad6ea78d86bb` | D-117 (L4723) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-125 (L307) | `component-sdk-contract` | **v4** `c53d541f12258eb96e86f0f5dbd3924a5f2e189d19c8f8672bae9037532461c3` | D-110 (L4362) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-126 (L308) | `platform-tcb-contract` | **v45** `da87bdb4d100c90e9450fb82744b7d327ae6b7332db550ea808bdbdb0444a7e5` | D-125 (L5146) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-127 (L309) | `anti-lockstep-contract` | **v7** `8c41bddd7c351abc3a0b4b721f9302df29ba7d053352cb950ec8b23e4afdd671` | D-111 (L4411) | COORD | none | CANDIDATE-NOT-APPLIED; `OPEN` |
| DR-131 (L313) | `preview-analyze-contract` | **v2** `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` | D-138 (L5836) | cell = COORD | v2 | CANDIDATE-NOT-APPLIED, "binds NOTHING"; `OPEN` |
| DR-133 (L314) | `provider-only-output-contract` | **v3** `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` | D-136 (L5748) | cell = COORD | v3 | CANDIDATE-NOT-APPLIED, "binds NOTHING"; `OPEN` |

Naming parents and three-limb acts (gate registry, preamble 08:L328–L333, table header 08:L335, per contracts inventory §4a): `gate-harness-naming` **v6** `b74e30092cf1f5aad55434d2f12465fa31111923c1b2c0c5ddc8a78445b5ffba` (D-145 L6066; v3 `b5236612394a3d24259f3b11b99e9928b530a4be3d147d2007d00c3ee96c3ccd` D-086 L3428; v7 and v8 exist on disk with zero COORD mentions — contracts §5 Q1); `g31-three-limb-act` **v1** `7d5848439b3cca947f1a9c8be730ca21c716559321306778ab7b24876cf28dd7` (D-167 L7001); `g32-three-limb-act` **v2** `8a64123830a95bd7774f171531f7872a34e35aeaf865383311c29dbb7ed5fc31` (D-169 L7113).

Preview dispositions (condition 1; owner-recorded; PROCESS-ONLY rows but scope-binding by reference): `route-b.DR-002.preview-disposition.v2` `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06` (D-058); `route-b.DR-003.preview-tm.v2` `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52` (D-065); `route-b.DR-004.preview-disposition.v2` `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76` (D-064); `route-b.DR-005.preview-disposition.v2` `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809` + RB-DR005-V2-A1 (D-060); `route-b.DR-006.preview-disposition.v2` `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161` (D-077); `route-b.DR-007.preview-disposition.v2` `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7` (D-078); `route-b.DR-008.preview-disposition.v2` `8b2d21392bde0906ea75a6c29b1083e3b441205fd3eafb66a13135734a9ca41c` (D-061); `route-b.DR-009.preview-disposition.v2` `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782` + RB-DR009-V2-A1 (D-079); `route-b.DR-011.preview-disposition.v3` `f1c7f6b7f6a827b34e0aac1533bab581198181d7a35236eceb9de64ca41be1b1` + RB-DR011-V3-A1..A3 (D-083); `product-boundary-preview.v2` `ff7a09130a2b5b409b02725a839f9d7b5fb88e945d7f9bbb63c0d0154c627b85` (D-068, Route C). All only recorded versions (rule: COORD = cell).

Deferral candidates (D-096, L3802; `CANDIDATE-NOT-RECORDED`, owner-recording blocked pending a grant per D-100 L3998): `deferral.DR-106-109-113.preview.v2.json` `194b01fc6bd9201e…`, `deferral.DR-108.preview.v2.json` `225be4f985889b42…`, `deferral.DR-110.preview.v2.json` `b6b678dc18dc0ff5…`, `deferral.DR-116.preview.v2.json` `ac8d2d4d414a66ef…`, `deferral.windows-platform.preview.v2.json` `e7dd2b718fc6af5e…` (16-hex prefixes measured here; full digests for the first four are in contracts inventory §2; the Windows artifact "is not a file-08 row" per D-100). D-096 does not name these files individually (it says "the five preview-deferral v2 artifacts", L3818).

V1 applied heads referenced by cells (V1-authoritative; not V2 design): `evidence.v15` `28dc3c1aaa97f723afa8c079682a43999ca5c79686e7cde0f11e38421a179b29` (D-014 L1296); `retention-tiers.v28` `e622b3cc19ba6a550348d849eedf5867e27a0302800b5b705a57e3bb611f9de2` (DR-008 cell); `r1-lifetime-neutrality.conformance.v1.9` `37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab` (D-005 L596); `evidence-identity-recipes.v12` `f0bfaebd7a66cd04b1f8642605e22df67e202a065c10bab5dd8ac818a4429998` (D-003 L514); `section31-supplier-coverage.v4` `97727684af2d812d3a677add9b15287db81d6fe36aeaa96d72d5118890a847f6` (D-045 L2123).

#### 1.5b Harness occupancies (28) and gate leftover-joins (21) — final versions

All occupancies recorded by one non-CONTESTED heading each (COORD rule; the file 08 cell names only the harness identifier "not authored; not QUALIFIED" — gates open question 1). Digest = gates inventory Appendix B (28/28 MATCH the `Frozen occupancy` line of the recording entry).

| Gate (08 line) | Occupancy final version · sha256 · D (line) | Gate leftover-join final · sha256 · D (line) | leftoverDesign `true` |
|---|---|---|---|
| G01 (L337) | `harness.DR-G01.core-download.v9.json` `f28b0d97723550c8690eec2a6ac7803efba93fd797f266600b038b14e269277b` D-231 (L10711) | none — carried by `distribution-core-leftover-join.v9` `e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7` D-287 (L15495) | OBL-2, OBL-D1, OBL-D2 (on DR-101 join) |
| G02 (L338) | `harness.DR-G02.core-installed.v4.json` `1bc247f779fa980ecde7d7a244effa6116f02a79be4a0ee74e0cedb168ccf360` D-232 (L10792) | as G01 | as G01 |
| G03 (L339) | `harness.DR-G03.core-startup.v5.json` `398ec6474eacbc4b873488dd07bce0e6295c2149d9d2794a177d13a96ebb8324` D-233 (L10876) | as G01 | as G01 |
| G04 (L340) | `harness.DR-G04.core-memory.v4.json` `f664f7fd7a428dc9fd05a3142f5a50a242704659d72f66fb509c66106e4e7845` D-234 (L10958) | as G01 | as G01 |
| G05 (L341) | `harness.DR-G05.component-delta.v4.json` `fb1b2158f16d07814a6c5f67166faadb12d122353f26d23e804060f7687b7875` D-235 (L11041) | as G01 | as G01 |
| G06 (L342) | not in the record | not in the record | — |
| G07 (L343) | `harness.DR-G07.exact-bytes.v4.json` `99be421cd11a7524c87ee56b31b1c3b8335d8156bdb0d27a3a94ddddae7a56ed` D-210 (L9247) | `exact-bytes-leftover-join.v7.json` `2f73148e1fe6e1b0a734ba92978e876bb0594f5770f5ac23d1ab1fe3dd1d0df7` D-286 (L15387) | OBL-G07-FX-AUTHORING, OBL-FILESYSTEM-COVERAGE |
| G08 (L344) | `harness.DR-G08.trust-recovery.install-surfaces.v3.json` `13076be20e4eef0dfe352786b705de09304a69f583529502388e5086f6f098c0` D-211 (L9307) | `g08-leftover-join.v5.json` `ba1c19d7f5e6ec4b67fc5b7589e0b5ef3c946d186166660ccdf63ea916d9a60f` D-281 (L14774) | OBL-G08-FX-AUTHORING |
| G09 (L345) | `harness.DR-G09.permissions.preview-scoped.v4.json` `603f96ebfd63466ca669ec97701462dd93f0997c398ea87b9f9a41ed495d6646` D-220 (L9902) | `g09-leftover-join.v12.json` `fc96ba91080ccef81259c6eb5ac004303a2b919e922d4bb54a448e26d149727c` D-288 (L15624) | OBL-FX-AUTHORING |
| G10 (L346) | `harness.DR-G10.provider-conformance.ts-major-1.v2.json` `b0cbce06487b96bbe7f6af1dae62ba3b3ca55aaa41305cb96f531099e86bf7c9` D-212 (L9368) | `provider-leftover-join.v4.json` `0e31f5b558e77b55a5aa42b711e5f5927062f67ed9f150d78c875326b79f16d4` D-279 (L14592) | OBL-G10-FX-AUTHORING, OBL-SELECTOR-REFRESH |
| G11 (L347) | not in the record | not in the record | — |
| G12 (L348) | `harness.DR-G12.doctor-purge.preview.v6.json` `e6b72a9e0cc7053c991c51c510531c6ecd263bb895c70a3e9ab84bd6b6256735` D-221 (L9972) | `g12-leftover-join.v5.json` `5770cc9cb993ba5ac467df4648820167addff7b5f7a10d4442fa7e57913779d4` D-289 (L15746) | OBL-DOCTOR-FX-AUTHORING |
| G13 (L349) | not in the record ("reserved, not named") | leftover on `language-quality-leftover-join.v5` (DR-118, D-273) | — |
| G14 (L350) | `harness.DR-G14.language-runtime-ux.typescript.v4.json` `0b4c25f4c2e5ae7fbf0a9a2762ccce813a6174401d9c51d123ecb2f8b1ddb647` D-213 (L9431) | `language-runtime-leftover-join.v7.json` `90e29696f0b3ed2b23c3a5f1d7c089d54aef6887e6f3a8d9d9dfe988282fb4e3` D-274 (L14132) | OBL-G14-FX-AUTHORING |
| G15 (L351) | `harness.DR-G15.packaging-adapter-conformance.v9.json` `d82fac570f952cbc234be682b658cf94d5f7571bf4297e777e4e2c4280f98479` D-214 (L9495) | `g15-leftover-join.v6.json` `4b2ac34c6f8c16422c1afa3f7c45ca92864953cae94c8154e508cdcfd0c8b2d2` D-290 (L15841) | OBL-AT-FX-AUTHORING |
| G16 (L352) | `harness.DR-G16.ci-isolation-integration.v5.json` `3e3107499ffb576c11b3d4c290470921062066f518cbd80b6a563b446ebc918e` D-215 (L9557) | `g16-leftover-join.v5.json` `7ce75ea514322a6e17546ec8e9b91c4fb2f66128271d6c6d757e3f627e05ab78` D-278 (L14502) | OBL-G16-FX-AUTHORING |
| G17 (L353) | not in the record ("dropped / inapplicable (D-077 SARIF drop; D-086)") | not in the record | — |
| G18 (L354) | `harness.DR-G18.lifecycle-generation-recovery.v4.json` `2ce9aa522bf014af27b088d3bd50885a271e5e321ba6c372af527552cb6660cc` D-216 (L9629) | `g18-leftover-join.v6.json` `f531ba6a952c8c55733454c19e46ac388f0eec4d31f3b5d29bfe04fbdeaac66e` D-276 (L14322) | OBL-G18-FX-AUTHORING |
| G19 (L355) | `harness.DR-G19.state-class-authority.preview-classes.v2.json` `57f392b2cc30302e3c354781c56c37a30a9241e16e067fda6a281b27ed8691ac` D-222 (L10044) | `g19-leftover-join.v5.json` `d7bce01edb64e25ac70df8feb9119e2e87aadd40c6259ffd50d797e9bfb6d126` D-291 (L15938) | OBL-G19-FX-AUTHORING |
| G20 (L356) | `harness.DR-G20.component-operability.v2.json` `2c4823b7c5feb04afb739602397f81dc34333617c284bff21e82657fa289bb37` D-217 (L9696) | `g20-leftover-join.v6.json` `d666a4492ef3c598b53606fff453cb14a968822b9c29b25b0b535ebde01b2d97` D-269 (L13708) | OBL-G20-FX-AUTHORING |
| G21 (L357) | `harness.DR-G21.component-failure-containment.v4.json` `13addb3cc70611efe22876f84dbe9e15d9a27529446d7e03841d2b2a3f552e0b` D-218 (L9768) | `g21-leftover-join.v13.json` `058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e` D-292 (L16035) | OBL-G21-FX-AUTHORING |
| G22 (L358) | `harness.DR-G22.platform-abi-loader.v2.json` `2973cda2adac1b612c084b64606e4fc5b5ed5b78317fc64780a7311172ff1307` D-219 (L9836) | `g22-leftover-join.v5.json` `70e0efd68e9003d7828c93e2d7d26dad81664adebfcb1c8d38b006c80e620d3f` D-271 (L13881) | OBL-G22-FX-AUTHORING |
| G23 (L359) | `harness.DR-G23.provider-well-formed-admission.preview.v2.json` `f48ba637bdf193785c05906a1686ce268b27b6ce7355de07fa5effefdd84fb0b` D-223 (L10114) | `g23-leftover-join.v8.json` `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` D-240 (L11391) | none |
| G24 (L360) | `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json` `ee41d14c7896ce97ebbf6611054991688ef1755499fbdc9d7f274498ebf9fdd4` D-224 (L10185) | `g24-leftover-join.v4.json` `c451f7ce20e93442172322ff2fd29a029a9a0ca209538ece7c590d32c72e43d7` D-250 (L12208) | OBL-G24-FX-AUTHORING |
| G25 (L361) | `harness.DR-G25.preview-analyze-missing-rung.preview.v3.json` `4f124cd763974b603fb307e13830cc7f79bc559c3b05ab7d39c59194d2f5dfde` D-225 (L10262) | `g25-leftover-join.v5.json` `9f2b137fe0b01830b4113ef26c8283214a75982f588f164391d61c5510f67aa3` D-249 (L12127) | OBL-G25-FX-AUTHORING |
| G26 (L362) | `harness.DR-G26.preview-analyze-sarif-not-advertised.preview.v2.json` `3a6f13799ef960170370a2a74930d62778a9671b2065ac3e83ca485c21721ffb` D-226 (L10336) | `g26-leftover-join.v4.json` `aba91c5a43f77ccb9244977c746ca8238b54a4e3af5f431b37b74ce6e5e68591` D-251 (L12295) | OBL-G26-FX-AUTHORING |
| G27 (L363) | `harness.DR-G27.preview-analyze-not-sealed-run.preview.v2.json` `436a60117e50d8716e52b7700195dd9fd053151abb0130148efab99f28a65794` D-227 (L10406) | `g27-leftover-join.v4.json` `630b226a852e2d6479513559cb0773fad67f80271d4814e726fc69c3aa943a5f` D-252 (L12364) | OBL-G27-FX-AUTHORING |
| G28 (L364) | `harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.json` `e540ea53b8cfd4e75c05eabfb4c321dca566161b135dc630c2bd1fec5d31ff4d` D-228 (L10481) | `g28-leftover-join.v4.json` `604dc98dfc4fd6ec2df1c22f2169b5ec921f2f43ab43ef7e0c98b48750dee085` D-253 (L12432) | OBL-G28-FX-AUTHORING |
| G29 (L365) | `harness.DR-G29.preview-boundary-excluded-form-admission.preview.v3.json` `94a40de95097afbf51e50461bac54f5fc95326215cf94e89a2f3655c731be96d` D-229 (L10556) | `g29-leftover-join.v4.json` `9e1af4ba3b21e483154825fa2c6d275f7ee805d1fb455f01c9d35e48411c3f64` D-254 (L12500) | OBL-G29-FX-AUTHORING |
| G30 (L366) | `harness.DR-G30.preview-boundary-install-shape.preview.v2.json` `371695b8fc7b5cf61e016508da69436fbe6146683979f0c2468f52757a16cfda` D-230 (L10634) | `g30-leftover-join.v4.json` `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` D-255 (L12585) | OBL-G30-FX-AUTHORING |
| G31 (L367) | `harness.DR-G31.identity-namespace-negative-test.preview.v5.json` `4cc42b86cf74b95c88c8efc9b85e48b894759712d30fbc1aaee079f301ca00a4` D-208 (L9125) | none — row join `identity-namespace-leftover-join.v6` `ab31c6075723d34503958a838ad1a3c4da37b3644390b6df8117ae34758099cc` D-175 (L7432) (cites G31 occupancy v2; A3 agreed recommendation: remasure to v7 last) | none on that join |
| G32 (L368) | `harness.DR-G32.actor-join-fixture-execution.preview.v3.json` `9c782a50fecd45bcec3b8eaa3fa6b8ea09b240d9cda5d530564b9e84fa48df49` D-209 (L9188) | none — row join `doctor-actor-leftover-join.v12` `0c0b894ffb5f80981282455a99153975e3fac30ade076d2596efb2b4fcf1a9e9` D-285 (L15261) | OBL-JOIN-FX-AUTHORING (on DR-114 join) |

Row leftover-joins, final versions (contracts inventory §4c; every predecessor is expressly "not current" in its successor entry): distribution-core v9 (D-287); component-manifest v9 `e71dca64c78a8feea9e72df5ae846eb2843be50fb10d01d54d5b65714ed1d2c4` (D-282); identity-namespace v6 (D-175); permission v12 `496b75c60c6540c3272c2c57d86c43ca71a77a1ed2eceaa6e3a1c49251374fb3` (D-283); doctor-actor v12 (D-285); language-quality v5 `e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53` (D-273; D-272 CONTESTED; v4 dual REJECT); lifecycle v4 `bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb` (D-275); compatibility v2 `33e4299d7f65bf37c2f5d54193e004c69d542d3f5da99417e1360efc2f8b7259` (D-177); signed-index v4 `ae5176e2a420be75b8aade77e7f265bc411968a75a35647ae01bfc708835a174` (D-280); packaging v4 `03251cc80cc774c12335ad038eedbb38ce73431623306f11fa1e75e40db61d07` (D-266); monorepo v4 `03d4478c3ce6ea843f8a4ee3ea1dcc6d8c06bd661f71970fe836ce107b611481` (D-277); sarif v4 `a2ab59d79051337906ae610b4c34f8203dcac0d9038f2826b32f68630bd07640` (D-182); state-class v4 `16b00ce69fea9e5fe83f44892ffee0a69f5b41a4ad18a6aca1ce7e77e830c902` (D-284); sdk v6 `e91d6e926830833d563bb89f3693d65328173af6f0d42275ad5339ef73880341` (D-267); platform-tcb v9 `1774427e9500940d24f75fbaee622142a8be72547d68a026e18d6e957369e26a` (D-268); anti-lockstep v3 `820d724a10a1e11a2188a323a3425cd13f4c483892bb487fb93f6542103c85e1` (D-186). Rows with no leftover-join lineage: DR-106, 108, 109, 110, 113, 116, 131, 133 (DR-131/133 carry `*-nt-gate-join` / `*-admission-leftover` measurements D-144/146/148/149; DR-117 carries `preview-product-boundary-ee-gate-join.v1` D-155 and `preview-product-boundary-admission-leftover.v1` D-156) — contracts §5 Q6.

**Note on standing of leftover-joins in the new docs.** Leftover-joins are measurements ("Record … as … leftover remasurement … binds NOTHING") — the form of every non-CONTESTED `Record … leftover remasurement` heading in D-160…D-292. Four headings in that range do not carry the token `binds NOTHING`: D-166 (L6977, "Remove the duplicate D-165 heading" — hygiene), D-167 (L7001) and D-169 (L7113) (three-limb acts adding a required-now gate), and D-272 (L13963, CONTESTED). They are PROCESS-ONLY for the rewrite (gates inventory Rule 7). What survives from them into a design doc is the *fact* each records — which obligations remain leftover-design at sealing — cited to the sealed join's bytes (§3.5 gate template, "Remainder" section). If A4 is adopted (`PROPOSAL.cross-citation-convention.md`, draft D-293), the reading convention it states must be quoted in the new register's "How to read" section; otherwise the record's version-number reading applies. Not decided at HEAD.

#### 1.5c Named corpora reachable from a current occupancy or current gate join (43 files; gates inventory)

`at-named-corpus-catalog.v1`, `component-manifest-fixture-corpus.v6`, `doctor-fc-join-input-corpus.v2`, `g07-coverage-domain.v1`, `g07-input-corpus.v1`, `g07-named-corpus-catalog.v1`, `g08-input-corpus.v1`, `g08-named-corpus-catalog.v1`, `g09-named-corpus-catalog.v1`, `g10-input-corpus.v1`, `g10-named-corpus-catalog.v1`, `g12-named-corpus-catalog.v1`, `g14-input-corpus.v1`, `g14-named-corpus-catalog.v1`, `g15-input-corpus.v1`, `g16-input-corpus.v2`, `g16-named-corpus-catalog.v1`, `g18-input-corpus.v2`, `g18-named-corpus-catalog.v1`, `g19-input-corpus.v2`, `g19-named-corpus-catalog.v1`, `g20-input-corpus.v1`, `g20-named-corpus-catalog.v2`, `g21-fixture-corpus.v1`, `g21-fixture-corpus.v2`, `g21-fixture-corpus.v7`, `g21-fixture-corpus.v8`, `g21-input-corpus.v1`, `g21-named-corpus-catalog.v1`, `g22-input-corpus.v2`, `g22-named-corpus-catalog.v1`, `g23-fixture-corpus.v3`, `g23-fixture-corpus.v4`, `g23-input-corpus.v1`, `g24-input-corpus.v1`, `g25-input-corpus.v1`, `g26-input-corpus.v1`, `g27-input-corpus.v1`, `g28-input-corpus.v1`, `g29-input-corpus.v1`, `g30-input-corpus.v1`, `identity-namespace-negative-test-corpus.v1`, `permission-r6-r10-input-corpus.v2` (all `.json`; digests in gates inventory Table 2). Plus, named only by the DR-105 / DR-114 joins (gates Appendix A): 14 `permission-fx*-input-corpus` files named by `permission-leftover-join.v12.json` (G09), and for G12 **13** `doctor-fc-*-input-corpus` files named by `doctor-actor-leftover-join.v12.json`, **12** of them not already among the 43 (the 13th is `doctor-fc-join-input-corpus.v2`, already in the 43) — so 14 + 12 = 26 files additional to the 43. Home not decided (gates open question 3). On disk but named by nothing recorded: `g01..g05-input-corpus.*`, `g21-fixture-corpus.v3..v6`, `g23-fixture-corpus.v1..v2`, `g16/g18/g19/g22-input-corpus.v1`, `g20-named-corpus-catalog.v1` (gates Appendix A) — archive only. Fixture bytes: 17 directories under `docs/coop/artifacts/fixtures/` (230 files; other-docs §2.4 rows 65–81), of which `dr-103/`, `dr-105.v1/`, `dr-105.v2/`, `g21.v3–v6/`, `g23.v1–v2/` have no COORD heading of their own (other-docs Q5).

---

## 2. Proposed directory tree

Placeholders: `<ARCHIVE>` = the archive directory name (owner option §6.1; the owner's working name is `docs-old`); `<P>` = the already-known **measured commit** — the commit at which file 08 shows all five conditions MET and which the measurement artifact measures (§4.1, §4.2); `<R>` = the **D-000 measurement-record commit**, whose parent is `<P>` and which adds that measurement artifact, the penultimate COORD heading — both pinned to `<P>` — and that cycle's own draft, review-prompt and reviewer-verdict artifacts under `docs/coop/artifacts/` (a D-000 cycle commit is never two files; §4.3 measures the record's own), and is committed and pushed per D-000 clause 4 ("**Commit and push per decision**", COORD:L39–L42); `<S>` = the **user-seal commit**, whose parent is `<R>`, which appends `D-SEAL` as the last COORD heading and changes no other file, and is committed and pushed before the move; `<M>` = the **pure move** `git mv docs <ARCHIVE>` (renames only), which moves the `docs/` tree as it stands at `<S>`; `D-SEAL` = the sealing entry's number (the next free number at sealing time — **not assigned here**). The four commits and the acts that produce them are §4.1–§4.4; the archived tree is `docs/` as it stood at `<S>`, and the register/gate/contract pages quote the state measured at `<P>`. Numbers of docs are the baseline of §5 (options in §6 change them).

```
docs/
├── README.md                          front door: what this tree is, authority order, how to cite, link to <ARCHIVE>/README.md
├── ARCHIVE.md                         seal metadata (§4.4): the D-SEAL heading, <P>, <R>, <S>, <M>, the path-mapping table over the <S> snapshot, the read-only rules; a page, dual-reviewed like any other
├── archive-manifest.v1.json           external digest list (§4.3): one path + sha256 per file under <ARCHIVE>/; validated by script, not a review page (§4.8 item 2)
├── AUTHORITY.md                       authority order + citation rule + status/standing vocabulary (verbatim from 08:L19–L28 and D-056/D-133)
├── GLOSSARY.md                        one entry per term (template §3.6)
├── DECISIONS.md                       successor decision register named in D-SEAL clause 4 — §6.10 (b) COORD form, continuing the D-series after D-SEAL (under §6.10 (a) post-seal decisions are ADRs in decisions/ instead); written after <M> (§4.3); not a derived review page and not one of the 128 counted in §5.1 (§4.8)
├── design/                            subsystem design docs (template §3.1)
│   ├── 00-overview.md                 architecture at a glance (from v2 README L44–L61 "Architecture at a glance"; 00-status-and-authority.md)
│   ├── 01-semantic-model-and-host-authority.md
│   ├── 02-distribution-and-components.md
│   ├── 03-configuration-and-security.md
│   ├── 04-lifecycle-delivery-and-operations.md
│   ├── 05-v1-to-v2-relationship.md
│   └── 06-scope-preview-and-deferrals.md   D-002 slice, D-018 naming, preview dispositions + riders, D-096 deferrals, DR-128/129/130, file 10 scope map, file 12 goal
├── contracts/                         one companion page per row that carries a contract (template §3.2) + the final contract bytes (copied or linked — §6.2)
│   ├── README.md                      index table: row → lineage → final version → sha256 → standing → recording D
│   ├── DR-101.distribution-core-inventory-contract.md
│   ├── DR-102.control-protocol-contract.md
│   ├── DR-103.component-manifest-schemas.md          (schemas v11 + fixture-corpus v6; D-013 v2 as history)
│   ├── DR-104.identity-namespace.md                  (D-012 policy; integration contract v4; negative-test corpus v1)
│   ├── DR-105.permission-truth-tables.md             (truth tables v9; host-effect v25; v2/v6/v8 as history)
│   ├── DR-106.offline-analysis-closure-contract.md
│   ├── DR-107.lifecycle-generation-contract.md
│   ├── DR-108.secret-storage-contract.md
│   ├── DR-109.storage-mechanics-contract.md
│   ├── DR-110.self-update-repair-contract.md
│   ├── DR-111.compatibility-matrices-contract.md
│   ├── DR-112.signed-index-trust-contract.md
│   ├── DR-113.replay-purge-contract.md
│   ├── DR-114.doctor-contract.md                     (doctor v4; actor-join v8)
│   ├── DR-116.third-party-policy-contract.md
│   ├── DR-117.product-boundary-successor.md          (both lineages until §8 Q3 is answered)
│   ├── DR-118.language-quality-matrix-contract.md
│   ├── DR-120.component-packaging-contract.md
│   ├── DR-121.monorepo-ci-contract.md
│   ├── DR-122.sarif-projection-contract.md
│   ├── DR-124.state-class-contract.md
│   ├── DR-125.component-sdk-contract.md
│   ├── DR-126.platform-tcb-contract.md
│   ├── DR-127.anti-lockstep-contract.md
│   ├── DR-131.preview-analyze-contract.md
│   ├── DR-133.provider-only-output-contract.md
│   └── json/                          ONLY if §6.2 = copy: 29 of the 31 §1.5a artifacts (§1.5a 31/32 rule), byte-identical, same file names as in the archive; `component-manifest-fixture-corpus.v6` and `identity-namespace-negative-test-corpus.v1` live once under gates/corpora/ (§8 Q22)
├── gates/                             one page per gate row (template §3.5), 32 pages incl. the four unnamed gates
│   ├── README.md                      gate registry index: id, claim, owner, harness id, occupancy final version, corpus files, status token at <P>
│   ├── DR-G01.core-download.md … DR-G32.actor-join-fixture-execution.md
│   ├── occupancy/                     ONLY if §6.2 = copy: the 28 final occupancy JSON files
│   ├── corpora/                       ONLY if §6.2 = copy: the 43 named corpus/catalog/coverage files (incl. the two also listed in §1.5a) (+26 DR-join-named files — 14 permission-fx* + the 12 doctor-fc-* not already among the 43 — if §8 Q-gates-3 says so)
│   └── fixtures/                      ONLY if §6.2 = copy and §6.6 = copy fixtures: the fixture directories enumerated in the gates/ row of §2.1
├── register/
│   ├── README.md                      how to read (08:L12–L28 verbatim; D-056/D-133 SATISFIED rule; token counting rule 08:L401–L404; A4 convention if adopted)
│   ├── inherited-v1-prerequisites.md  DR-001–DR-012 + DR-011 residual subledger (08:L30–L91), status at <P>
│   ├── v2-decisions.md                DR-101–DR-133 (08:L207–L314), status at <P>
│   ├── review-findings.md             DR-201–DR-205 (08:L316–L324)
│   ├── release-gates.md               DR-G01–DR-G32 (08:L326–L368)
│   └── readiness.md                   five conditions verbatim (08:L370–L395), sealed snapshot (08:L397–L418 form), the condition-5 path clause (§4.4), the seal pointer
├── decisions/                         ADR-style condensed decisions (template §3.3)
│   ├── README.md                      index: ADR id → title → D-ids → rows → status; and the reverse map D-NNN → ADR
│   └── ADR-0001-definition-of-done.md … ADR-0049-dr104-satisfied.md   (49 groups under §6.3 (b) — the §5.1 baseline; the 21 candidate-ADR groups of §1.2/§5b are a separate expansion of §6.3 that would make it 70, and §6.4 (b), which labels candidates on the contract/gate/design pages, does not select it)
└── v1/                                POINTERS ONLY (no copies): where V1 authority lives in <ARCHIVE> (freeze, blueprint, v1-slice, product-dispositions, claim-register, checkers, applied heads)
    └── README.md
```

### 2.1 Per directory: what goes in, what is excluded

| Directory | Goes in (with archival source class) | Excluded (stays in `<ARCHIVE>` only) |
|---|---|---|
| `docs/` root (`README.md`, `ARCHIVE.md`, `AUTHORITY.md`, `GLOSSARY.md`, plus `archive-manifest.v1.json` and `DECISIONS.md`, neither of them one of the 128 review pages) | Front door (TREE-ENDSTATE §6 "Front-door README (required content)" L234–L263 as the pattern); the seal metadata `ARCHIVE.md` (§4.4: the D-SEAL heading, `<P>`, `<R>`, `<S>`, `<M>`, the path mapping over the `<S>` snapshot, the read-only rules) and the external `archive-manifest.v1.json` (§4.3), both written in commits after `<M>` and neither of them inside `<ARCHIVE>/`; the successor decision register `DECISIONS.md` that D-SEAL clause 4 names (§6.10 (b): COORD form, continuing the D-series; under §6.10 (a) the same content is ADRs in `decisions/` instead), also written after `<M>` (§4.3) and also outside `<ARCHIVE>/` — like the manifest it is not a derived review page and is not one of the 128 counted in §5.1 (§4.8 items 1, 6 and 9); authority order; citation rule (§3.0); glossary entries derived from v2 README "Stable terms" (L76–L88), "Claim labels" (L63–L74), file 08 status vocabulary (L19–L28), COORD standing tokens (`CANDIDATE-NOT-APPLIED`, `CANDIDATE-NOT-RECORDED`, `binds NOTHING`, `PREFERENCE-LADEN`, `RULE-GOVERNED`, `CONTESTED`), gate vocabulary (`named:`, `not authored; not QUALIFIED`, leftoverDesign, remasurement, occupancy, three-limb act) | `docs/README.md` (old, points at a STALE plan at L10); `p.md`; handoff/session prompts; `docs/MAP-VS-CONTROL.md` (REFERENCE, 20200 bytes, other-docs row 2; not cited by file 08 or COORD) — archive-only unless the owner carries it as a REFERENCE pointer (§8 Q23) |
| `design/` | DESIGN-SOURCE prose from `docs/v2/architecture/00–05, 10, 12` (8 files) condensed and re-cited; the "Architecture at a glance" diagram (v2 README L46–L57); scope constraints from preview dispositions/riders and D-002/D-010/D-018/D-096 by reference | `docs/coop/architecture/00–11` (V1 greenfield narrative; DESIGN-SOURCE for V1, referenced from `v1/README.md`, not rewritten); the transition brief (`OPENSIP-DISTRIBUTION-AND-COMPONENT-TRANSITION-BRIEF.md`, "**Authority:** NONE." L5 — other-docs Q2); `07-review-record.md`, `09-v1-to-v2-claim-matrix.md`, `11-three-reviewer-direction-synthesis.md` (REFERENCE / review commentary); `steering/`, `cleansheet/`, `deltas/` |
| `contracts/` | 26 companion pages; the 31 final artifacts of §1.5a (§1.5a 31/32 rule; copy or link per §6.2, and if copied then 29 of them under `contracts/json/` because `component-manifest-fixture-corpus.v6` and `identity-namespace-negative-test-corpus.v1` are homed once under `gates/corpora/` — §8 Q22); the two naming parents and two three-limb acts referenced from `gates/` | Every predecessor version (e.g. `platform-tcb-contract.v1–v44`, `permission-truth-tables.v1/v3–v5/v7–v8`); every `*.review-*`, `*.review-prompt.md`, `coordinator-decisions.D-*.draft.md`; unrecorded higher versions (`gate-harness-naming.v7/v8`, `core-gate-harness-specifications.v1–v4`, `identity-nt11-gate-naming.*`, `join-fx-gate-naming.*`, `doctor-leftover-join.v1` — contracts §5 Q1); deferral candidates (`CANDIDATE-NOT-RECORDED`) unless §6.4 says otherwise; V1 applied heads (pointers only from `v1/`) |
| `gates/` | 32 gate pages; 28 final occupancies; 43 named corpora (+ the 26 DR-join-named corpora if the owner assigns them here); the fixture directories COORD names by path (`fixtures/dr-103.v2/` and `fixtures/dr-103.v4/` — COORD:L4211–L4212 in D-106 and COORD:L5474 in D-130; `fixtures/g21.v7/` — COORD:L11999 in D-247, and named by `g21-fixture-corpus.v7`, D-245 L11761) plus exactly these five further directories, each named by a current fixture-corpus artifact of the §1.5c list whose Record heading is cited (`g21.v1/` from `g21-fixture-corpus.v1`, D-241 L11465; `g21.v2/` from `g21-fixture-corpus.v2`, D-243 L11614; `g21.v8/` from `g21-fixture-corpus.v8`, D-247 L11944; `g23.v3/` from `g23-fixture-corpus.v3`, D-237 L11190; `g23.v4/` from `g23-fixture-corpus.v4`, D-239 L11325), if §6.6 = copy | 78 predecessor occupancies; all 123 gate leftover-join files (facts extracted into the gate page's "Remainder" section, cited to the final join); unrecorded corpora (`g01..g05-input-corpus.*`, `g21-fixture-corpus.v3–v6`, `g23-fixture-corpus.v1–v2`, superseded `*-input-corpus.v1`); the fixture directories with no COORD heading of their own (`fixtures/dr-103/`, `dr-105.v1/`, `dr-105.v2/`, `g21.v3–v6/`, `g23.v1–v2/` — §1.5c. Note: `g21.v3–v6/` are also named inside `g21-fixture-corpus.v7` (D-245 L11761) and `g21-fixture-corpus.v8` (D-247 L11944), and `g23.v1–v2/` inside `g23-fixture-corpus.v3/v4` (D-237 L11190 / D-239 L11325), so their exclusion is an owner choice (§8 Q11), not a consequence of a rule; `dr-105.v1/` and `dr-105.v2/` are named by five of the 14 `permission-fx*-input-corpus` files that `permission-leftover-join.v12` names (fx1.v2, fx2a.v1, fx2b.v1, fx3.v1, fx9.v1), and `dr-105.v2/` also by the unrecorded `g23-fixture-corpus.v1/v2`); review siblings; dispatch texts |
| `register/` | The final register content of file 08 as archived at `<S>` (its bytes unchanged since `<P>`), re-cited row by row; the sealed snapshot in the 08:L397 form; the readiness decision verbatim; the condition-5 clause; the pointer to `D-SEAL` | The cell prose history that the archive already holds (each row cites `<ARCHIVE>/v2/architecture/08-…#<row>` for the long-form cell); DR-011 residual reconciliation detail beyond the token table (08:L69–L91) unless the owner wants it live |
| `decisions/` | One ADR per ADR group of the 72 BINDING-DESIGN entries (49 groups, decisions inventory §5), each linking every D-NNN it condenses by `<ARCHIVE>/coop/COORDINATOR-DECISIONS.md#d-nnn` and COORD line; the 21 candidate groups of §5b are a separate expansion the owner may select under §6.3; §6.4 (b)'s labelled candidates on the contract, gate and design pages do not select it | The 170 CUSTODY entries (their facts surface in `contracts/` and `gates/` pages, not as ADRs); the 25 PROCESS entries (D-000 protocol, D-054/D-132 grants, MF-6 transcriptions, hygiene, pin corrections) — summarised once in `AUTHORITY.md` "How the record was made", not as ADRs; the 10 PARKED entries (listed in the ADR index as "CONTESTED — parked; resolved by D-xxx", decisions inventory §4, not condensed) |
| `v1/` | `README.md` pointer table only: V1 authority files (`IMPLEMENTATION-FREEZE.md` `e809d439…`, `IMPLEMENTER-BLUEPRINT.md` `909394c5…`, `v1-slice.md`, `product-dispositions.md` + `product-dispositions.v1.json`, `claim-register.v1.json` `767dc210d4fa8b6d…`, `v1-authority-baseline.json` with 49 MATCHing pins, `v1-status-evidence.json`, the 124 `check-*.py`, the five applied heads of §1.5a) | Everything else V1 (`coop/architecture/*`, `steering/*`, `GORTEX-BORROW-REGISTER.md`, `programming-language.md`, `agents-log.md`, `agentlog3/4.md`, review prompts) |

Excluded from the new tree entirely and never copied: 760 `_dispatch.*.txt`; 1338 `review-independent` files; 1093 `review-prompt` files; 368 COORD drafts; `coordinator-decisions.D-057.turn2.FROZEN`; `_handoff.*`, `_recording-checklist.*`; `__pycache__/`; `freeze-payload-manifest.txt` (STALE); `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` (STALE); cleansheet (STALE); `deltas/` (UNKNOWN; §8).

Relationship to `TREE-ENDSTATE.md` (REFERENCE): that plan chose `docs/coop/` → `docs/architecture/` (§2.2 L54) with `freeze/ implementer/ guide/ contracts/ instruments/ history/` (§7.2), forbade mass moves "during multi-agent contract churn" (§7.1), and said "Graduate **conclusions**, not the deliberation corpus" (§5.5, L230) and "Do **not** delete the deliberation corpus" (§1.1, L32). The owner's F1 plan (`git mv docs <ARCHIVE>` + new `docs/`) satisfies the anti-goals and the "after Phase 4 signed" timing but is a *different layout* from TREE-ENDSTATE §3; TREE-ENDSTATE has no file 08 or COORD citation (other-docs row 9), so nothing in the record requires its layout. §6.1 lists it as an option.

---

## 3. Per-doc-type templates

### 3.0 Citation rule (applies to every template)

1. **Every sentence that asserts anything ends with a citation** in one of three forms:
   - prose: `[<ARCHIVE>/<path>#<heading>` or `L<n>–L<m>]` — e.g. `[<ARCHIVE>/v2/architecture/08-decision-and-readiness-register.md L415]`;
   - COORD: `[COORD D-NNN L<n>]` (heading line, or the line of the quoted sentence);
   - artifact: `[<ARCHIVE>/coop/artifacts/<file> sha256:<full 64 hex>]` — the digest is mandatory for JSON artifacts; a 16-hex prefix is not accepted.
   A sentence with no citation must carry the marker `[editorial]` and may contain no token, number, version, owner, verdict, or claim about the design; reviewers REJECT any `[editorial]` sentence that does.
2. **Tokens, versions, digests, owners, dates are verbatim** from the cited bytes; paraphrase is allowed for prose, never for those.
3. **No deictic version references**: never "this vK", "the current join", "latest"; always the named file with version (successor-audit checklist: deictic "This vK", bare version tokens, claims contradicted by bytes are REJECT grounds).
4. **Absence is stated, not filled**: "not in the record" plus what was searched (e.g. "no COORD heading names `g01-input-corpus.v1`").
5. **Archive wins**: every page carries the front-matter line `Derived from the sealed record at <S>; on conflict the archive governs.`
6. **Standing is never upgraded by derivation**: a `CANDIDATE-NOT-APPLIED` artifact is described as such on every page that names it; a `SATISFIED` row cites its D-056/D-133 class and its named remainder.
7. **Front matter (all templates):**
   ```
   ---
   doc-type: <design|contract|adr|register|gate|glossary>
   derived-from: <ARCHIVE> @ <S sha>
   seal-entry: D-SEAL
   sources: [<list of every archival path/digest cited below>]
   review: <ARCHIVE-independent dual review id — filled at ACCEPT>
   ---
   ```

### 3.1 Subsystem design doc (`design/NN-*.md`)

```markdown
---  (front matter §3.0.7)
# <Title — verbatim H1 of the archival source, e.g. "Distribution and Component Architecture">

> Source of this page: <ARCHIVE>/v2/architecture/02-distribution-and-components.md (sha256 <…>) [status line quoted verbatim: "> **Status:** DRAFT — proposed V2 product/distribution delta" L3].
> Register rows this page is bound by: <verbatim "Readiness:" line, e.g. "DR-010, DR-101 through DR-107, DR-116 through DR-128, DR-205" L5>.

## 1. Purpose and boundary          (what the subsystem is; what it is not — each sentence cited)
## 2. Preserved V1 laws             (claim label "Preserved V1 structural law" — cite the V1 source via v1/README.md pointers)
## 3. Binding product decisions     (D-NNN decisions with ADR links: e.g. D-002, D-006, D-008, D-009, D-012)
## 4. Accepted design contracts     (only rows whose contract is ACCEPTED (SATISFIED-grade) or an accepted design contract D-013/D-015/D-035/D-038; link contracts/DR-xxx page; state remainder)
## 5. Candidate design (not applied) (only if §6.4 allows; every item labelled `CANDIDATE-NOT-APPLIED` with its recording D and "binds NOTHING")
## 6. Scope constraints             (preview dispositions and riders; deferrals; exclusions PB-1..PB-7 — by reference to design/06)
## 7. Open decisions at sealing     (reserved numbers/lists/owners exactly as the sealed join/contract names them; "not in the record" where absent)
## 8. Gates that measure this subsystem (DR-G ids → gates/ pages)
## 9. Sources                       (every archival path + sha256 cited above, one per line)
```
Required: sections 1, 2 or 3, 6, 9. Forbidden: any sentence that introduces a mechanism, threshold, name, or route absent from the cited source.

### 3.2 Contract companion page (`contracts/DR-xxx.<lineage>.md`)

```markdown
---  (front matter)
# DR-xxx — <verbatim Decision cell text from file 08 row>

| Field | Value (verbatim) |
|---|---|
| Register row | DR-xxx (<ARCHIVE>/v2/architecture/08-… L<n>) |
| Owner / decision authority | <cell> |
| Status token at <P> | `<leading label>` (cell continues: "<first clause>") |
| Final artifact | `<ARCHIVE>/coop/artifacts/<name>.v<N>.json` sha256 `<64 hex>` |
| Recording entry | `## D-NNN — <heading verbatim>` (COORD L<n>) |
| Rule applied | COORD / cell / DIVERGENT (cell names v<k>: "<cell clause>") |
| Standing | `CANDIDATE-NOT-APPLIED` — "<recording entry's own words, e.g. 'The candidate binds NOTHING. DR-xxx stays OPEN.'>" (COORD L<n>) — or ACCEPTED (SATISFIED-grade) under D-056 Class A/B with remainder "<verbatim>" |
| Verdicts | Claude `<review file>` sha256 …; Codex `<review file>` sha256 … (digests as quoted in the recording entry) |
| Lineage history | v1 … v<N-1>: <disposition each, from the recording entries; "not in the record" where none> |

## 1. What the contract binds (if applied)     (summary of the artifact's own top-level sections, each sentence citing a JSON path, e.g. `$.namedOpenDecisions[0].id` = `OD-112-1`)
## 2. Named open decisions / reserved values    (verbatim ids and the "RESERVED"/"UNDECIDED" words from the artifact)
## 3. Leftover-design at sealing               (from the final row leftover-join: obligation id → leftoverDesign → existingGate → executionObligationOwnerToday, each cited to the join's `$.obligations[i]`)
## 4. Related rows and gates                   (DR-G ids that execute it; sibling rows named by the recording entry)
## 5. Sources
```
Rule: the page never restates the JSON in prose beyond §1; the JSON is the contract; the page is the map.

### 3.3 ADR (`decisions/ADR-NNNN-<slug>.md`)

```markdown
---  (front matter; plus `condenses: [D-NNN, D-MMM, …]`, `adr-group: <group id from decisions inventory §5>`)
# ADR-NNNN — <Proposed ADR title from decisions inventory §5, ≤12 words>

- **Status:** ADOPTED <date verbatim from the COORD Status line of the last member> — or "CONTESTED, parked; resolved by <D-id>" for a PARKED pointer (not an ADR body)
- **Archival entries:** `## D-NNN — <heading verbatim>` (<ARCHIVE>/coop/COORDINATOR-DECISIONS.md L<n>) [one line per member]
- **Decision type (verbatim):** RULE-GOVERNED / PREFERENCE-LADEN / user-made (D-000 / D-054 / D-132 form)
- **Register rows touched:** <verbatim list from the entries>

## Context        (why the decision was needed — only from the entry's own text and the rows it names)
## Decision       (the Decision text, quoted or tightly condensed; every clause cited to its COORD line; riders quoted verbatim, e.g. RB-DR005-V2-A1)
## Does not       (the entry's own "Does not …" negations, verbatim — they are load-bearing in this record)
## Readiness effect (verbatim)
## Reversibility / overturn (verbatim: class, overturn token e.g. `C-D056`)
## Consequences seen later (only later ADOPTED entries that cite this one by number — no inference)
## Sources
```
Granularity is §6.3. A merged ADR (e.g. ADR for `ADR-RB-DR005` = D-028 select, D-039 record, D-060 owner-record) keeps three "Archival entries" lines and three dated Status tokens.

### 3.4 Register page (`register/*.md`)

```markdown
---  (front matter; plus `file08-sha256-at-seal: <64 hex>`)
# <Section title verbatim from file 08, e.g. "V2 architecture and product decisions">

> This table is the sealed register section re-cited row by row. Cell prose is abridged to its leading label plus the first clause; the full cell is at <ARCHIVE>/v2/architecture/08-… L<n>. Status-token counting rule: the leading label of each status cell (08:L401–L404).

| ID | Decision (verbatim) | Owner (verbatim) | Status token at <P> | Recording D-ids | Design page | Contract / occupancy (final version · sha256) | Blueprint impact (verbatim lead) |
|---|---|---|---|---|---|---|---|
| DR-xxx (08:L<n>) | … | … | `<lead>` | D-… | design/NN | contracts/DR-xxx | … |

## Sealed snapshot (form of 08:L397–L418)
| Condition | Required (verbatim) | Measured at <P> (verbatim from the sealing entry's **Measured at <P>** field) | Standing |
## Readiness decision (08:L370–L395, verbatim)
## Condition-5 path clause   (the option chosen in §6.5, quoted from D-SEAL)
## Sources
```
Rule: no row is dropped (condition 4 counts 32 of 32 owners, 08:L417; G06/G11/G13/G17 stay as rows — gates open question 7). No token is regenerated by the rewrite; every token is copied from the sealed file 08 and cross-checked against D-SEAL's snapshot.

### 3.5 Gate page (`gates/DR-Gxx.<name>.md`)

```markdown
---  (front matter)
# DR-Gxx <GATE-NAME> — <Claim cell verbatim>

| Field | Value (verbatim) |
|---|---|
| Register row | 08:L<n> |
| Owner | <cell> |
| Harness identifier | `<named: … text>` or "reserved, not named" / "dropped / inapplicable" / "(no `named:` prefix)" |
| Status token at <P> | `<lead>`; Assurance stage now: `<cell>` |
| Threshold / waiver | <cell verbatim; D-006 numbers by reference> |
| Final occupancy | `harness.DR-Gxx.<name>.v<N>.json` sha256 `<64 hex>`; `$.status` `CANDIDATE-NOT-APPLIED`; recorded by `## D-NNN — Record … as Gxx occupancy remasurement` (COORD L<n>) — or "not in the record" |
| Named corpora / catalogs / coverage-domain / fixture corpora | one line each: file · version · sha256 · named by (occupancy / gate join / DR join) |
| Fixture directories | `<ARCHIVE>/coop/artifacts/fixtures/<dir>/` (recording D or "no COORD heading; referenced by <corpus file>") |
| Final gate leftover-join | `<file>` sha256 … D-NNN — or "none of its own; carried by <row join>" |

## 1. What the gate proves            (from the occupancy's own claim/scope fields, cited by JSON path)
## 2. Remainder at sealing            (obligation → leftoverDesign true/false → existingGate → owner, from the final join `$.obligations[]`; `$.leftoverDesignOpenStanding` quoted verbatim)
## 3. Predecessor occupancies         (versions + the recording entry's disposition sentence verbatim; "not characterized — not in the record" where the entry is silent)
## 4. Rows this gate executes for     (DR ids; D-056 remainder links)
## 5. Sources
```

### 3.6 Glossary entry (`GLOSSARY.md`, one block per term)

```markdown
### <Term (verbatim spelling as used in the record)>
- **Meaning:** <one sentence, verbatim or near-verbatim from the defining source> [citation]
- **Defining source:** <ARCHIVE>/… L<n> (e.g. v2 README "Stable terms" L80 for "Signed distribution core"; 08:L21 for `HARD-BLOCKED`; COORD D-056 L3363 for the SATISFIED-evidence rule)
- **Used in:** <pages of this tree>
- **Not to be confused with:** <only if the record itself draws the distinction, e.g. "Management-only core" vs "Authoritative offline analysis closure" (README L82–L83)>
```
Seed list (all from the record): the nine "Stable terms" (v2 README L80–L88); the six "Claim labels" (L65–L71); the five status tokens (08:L21–L28); `ACCEPTED` (DR-201–205 gate token, 08:L320–L324); `CANDIDATE-NOT-APPLIED`; `CANDIDATE-NOT-RECORDED` (D-096); `binds NOTHING`; `RULE-GOVERNED` / `PREFERENCE-LADEN` (D-000 clause 5); `CONTESTED` (D-000 clause 2); `Class A` / `Class B` (D-056); `SATISFIED-GRADE`; `MF-6`; `T2-02`; `Route A/B/C`; `architecture preview` (D-018); `required-now`; `named:` / `not authored; not QUALIFIED`; `occupancy remasurement`; `leftover-join` / `leftoverDesign`; `three-limb act`; `remainder`; `rider`; `owner-record`; `property pin` (D-033).

---

## 4. Derivation and review process

### 4.1 Preconditions (all must hold before any step below)

1. File 08 snapshot shows **all five conditions MET** (at HEAD: 1, 3, 4 MET; 2 and 5 NOT MET — 08:L414–L418). Condition 5 requires "Product and architecture authorities explicitly authorize creation of `docs/v2/implementation/` against a refreshed exact authority baseline" (08:L392–L393; D-001 §1 blockquote, condition 5 at COORD L116–L117).
2. The owner's pending decisions A–E (`DECISIONS-NEEDED.md`; recommendations in `DECISIONS-RECOMMENDED.md`, all AGREED, F1 included) are recorded, because several change what the new docs must say (A4 citation convention; B1–B3 Class A openings; C1–C9 reserved values; D1 fixture authoring; A3 identity-namespace v7).
3. Nothing untracked **and nothing ignored** remains under `docs/` at the measured commit `<P>`: the 31 untracked `_dispatch.*.txt` files (other-docs Q6) are committed or deliberately deleted, the repo-root working files are committed, and `git status --porcelain --ignored -- docs` reports nothing, **before** the measurement (§6.8). The `--ignored` flag is load-bearing: the repository `.gitignore` lists `__pycache__/` (L4) and `*.pyc` (L5), so `docs/coop/artifacts/__pycache__/` — 29 `.pyc` files at HEAD `4abb961` — is ignored rather than untracked and plain `git status --porcelain` never lists it (measured here: `git status --porcelain -- docs | grep -c pycache` = 0; `git status --porcelain --ignored -- docs` returns `!! docs/coop/artifacts/__pycache__/`). The reason for the check is not orphaning — a controlled test in a throwaway repository (one tracked and one untracked file under `docs/`) shows that `git mv docs archive` reports `R  docs/tracked.txt -> archive/tracked.txt` and `?? archive/untracked.txt` and leaves no `docs/` behind, i.e. `git mv` of a directory carries untracked files, and ignored files, with it — the reason is that a sealed, byte-identical archive must not carry an overlay that the measurement of `<P>` never covered (§7 R6).
4. The four repository states of §4.2–§4.3 are reached in this order (`<R>`'s parent is `<P>`, `<S>`'s parent is `<R>`, `<M>`'s parent is `<S>`), each of the three commits after `<P>` committed **and pushed** before the next act begins, per D-000 clause 4 ("**Commit and push per decision** (user amendment 2026-08-12)", COORD:L39–L42): `<P>`, the already-known measured commit of precondition 1; `<R>`, the D-000 measurement-record commit, which adds the measurement artifact and the penultimate COORD heading, both pinned to `<P>` (§4.2 Subject), together with that cycle's own draft, review-prompt and reviewer-verdict artifacts under `docs/coop/artifacts/` (§4.3); `<S>`, the user-seal commit, whose parent is `<R>`, which appends `D-SEAL` as the **last heading** of COORD and changes no other file (§4.2); `<M>`, the pure move, which renames only (§4.3). The archived tree is `docs/` as it stands at `<S>`.
5. Each of those commits is pushed (E2 agreed: push only after the owner approves the exact HEAD; fetch, fast-forward check, non-force push), so `origin/main` carries `<R>` before the seal is written and `<S>` before the move is made.

### 4.2 Sealing entry text — DRAFT (form of a user-made entry, D-054/D-132 class, COORD:L2361 / L5554; number and digests are placeholders)

```
## D-SEAL — Seal the design record at the measured commit <P>

- **Date:** <YYYY-MM-DD>
- **Status:** **ADOPTED <YYYY-MM-DD>.** Made directly by the user in
  conversation. Same class as D-000 / D-054 / D-132: the seal is the
  user's decision, recorded verbatim rather than made on their behalf.
  [ALTERNATIVE (§6.7): D-000 cycle — Turn n of 3: CONSENT from both
  independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX; Claude 2 <review file>
  <sha256>; Codex <review file> <sha256>; subject
  coordinator-decisions.D-SEAL.turn<n>.draft.md <sha256>.]
- **Decision type:** RULE-GOVERNED. Records that D-001's five conditions
  are MET at the measured commit <P> — the commit the measurement heading
  immediately preceding this one measures, which is not the parent of this
  entry's own commit — and closes this register to further headings. Not a
  remasurement. Not SATISFIED-GRADE. Marks no row SATISFIED.
- **Subject:** the measurement artifact <MEASUREMENT-PATH> — a path
  under `docs/coop/artifacts/`, this record's uniform home for cycle
  artifacts — sha256 `<64 hex>`, recorded by a D-000 cycle as the heading
  immediately preceding this one (the penultimate heading of this
  register) and committed and pushed as <R> before this entry is written,
  which states for the commit <P>: the sha256 of
  `docs/v2/architecture/08-decision-and-readiness-register.md` (file 08);
  the sha256 of the prefix of `docs/coop/COORDINATOR-DECISIONS.md` that
  runs from the first byte of that file through the last byte preceding
  the measurement heading's `## ` line, that prefix's length in bytes
  recorded beside the digest, so the digest covers every heading of this
  register before the measurement heading, entry bodies included; the
  five-condition table verbatim; the required-now count; the
  last gate row; and that last heading's id. No manifest of all files
  under the sealed tree lives inside that tree: such a manifest would
  have to hash itself, and would have to hash
  `docs/coop/COORDINATOR-DECISIONS.md` while this register embeds the
  manifest's own digest. The all-files manifest of the archive is
  produced outside the archive, after the move (§4.3, §4.4).
- **Measured at <P> (quoted from the measurement artifact, which takes
  them from the file 08 snapshot's leading labels):**
  Condition 1 <verbatim>; Condition 2 <n> of <m> `SATISFIED` <verbatim
  remainder of the cell>; Condition 3 <verbatim>; Condition 4 <verbatim>;
  Condition 5 <verbatim, naming the authorizing entry D-AUTH>.
  Required-now <n>. Last gate row DR-G<nn>. Last live heading before the
  measurement heading: D-<NNN>.
- **Decision:**
  1. The design record (file 08, this register, and `docs/coop/artifacts/`)
     is SEALED at the measured commit <P>, as it stands in the tree of the
     commit carrying this entry. No heading is appended to this register
     after D-SEAL. [Insert the amendment sentence for the option chosen
     in §6.10 verbatim. Option (b): "This heading amends D-000 in one
     respect: the register D-000 names as the place where every decision
     made under the delegation protocol is recorded ('Every decision made
     on the user's behalf under the delegation protocol is recorded
     here', COORD:L3–L4; entry format COORD:L9–L12) is closed at this
     heading, and the recording obligation continues in the successor
     decision register named in clause 4, which keeps D-000 clause 3's
     entry fields and clause 4's rule '**Commit and push per decision**'
     (COORD:L36–L42, the commit-and-push clause at L39–L42)." Option (a)
     is the alternative: "This heading amends D-000 in four respects: the
     register's location — the register D-000 names as the place where
     every decision made under the delegation protocol is recorded
     ('Every decision made on the user's behalf under the delegation
     protocol is recorded here', COORD:L3–L4) is closed at this heading,
     and the recording obligation continues in the successor register
     named in clause 4; the end of the D-NNN series at this heading; the
     entry form, D-000's stated format (COORD:L9–L12) giving way to the
     ADR form of that successor, each new ADR carrying D-000 clause 3's
     reviewer verdict with digest (COORD:L36–L38); and the authority of
     the ADR set, whose pages carry the decisions made after this seal
     (§6.10(a)). D-000 clause 4's rule '**Commit and push per decision**'
     (COORD:L39–L42) is unchanged."]
  2. Path mapping. On the commit immediately following this entry's
     commit, the directory `docs/` is renamed to `<ARCHIVE>/` by `git mv`
     with history preserved. **Every path of the form `docs/<p>` that is
     itself a tracked path in the tree of the commit carrying this entry,
     immediately before that rename** resolves to `<ARCHIVE>/<p>` from the
     rename on, wherever it is cited by a citation written in or before
     this entry in a tracked repository file present in that tree — this
     register, file 08, a frozen artifact, or a tracked file outside
     `docs/`. A cited path absent from that tree is not remapped by this
     clause; clause 3 governs the one such path this record names. A
     citation first written after this entry is not mapped by this clause
     and
     names its target directly. No cited bytes change; every sha256 in
     this register remains verifiable at the mapped path.
  3. Condition-5 path. [Insert the option chosen in §6.5 verbatim.
     Default text, applicable when no reviewed amendment of file 08's
     condition-5 wording was recorded before <P>: "Condition 5 is MET at
     the measured commit <P> — quoted verbatim in the Measured at field
     above, which names the authorizing entry — so the authorization it
     requires (08:L392–L393) has been given, and the path
     `docs/v2/implementation/` is authorized but not yet created. It is
     absent from the sealed tree — at <P> and in the tree of the commit
     carrying this entry — is not remapped by clause 2, and is preserved
     literally as the prospective live path the sealed text names. The
     register's earlier sentence 'Until then, `docs/v2/implementation/`
     remains reserved and absent' (08:L395) states the position before
     that authorization; it is quoted as history and is not this entry's
     statement of current standing. This seal creates no directory, stub,
     pointer or successor path for it." Text when such an amendment was
     recorded before <P> (the 5-C
     form, whose mechanism is D-010's: "Per D-001's new-row rule, C-D010
     amends file 08's condition-2 wording", COORD:L1003–L1004): quote the
     amended condition 5 and name the amending entry and its commit.]
  4. Successor register. [Insert the option chosen in §6.10 verbatim;
     e.g. option (b): "Decisions after this seal are recorded in
     `<SUCCESSOR-REGISTER>` in this register's entry form, continuing the
     D-series at the next unused D-NNN identifier measured at that time,
     with D-000's review, reversibility, overturn and commit-and-push
     fields intact." Option (a) is the alternative: "Decisions after this
     seal are recorded in `docs/decisions/` (ADR form) with a running
     index", which additionally amends D-000's entry form and the
     authority of the ADR set (§6.10).] Whichever entry that register
     records first — the sign-off of the derived documentation, a
     decision made after this seal, or the disposition of a page that
     dual review left contested — cites this heading and the commit <P>.
  5. Derived documentation. A new `docs/` tree is derived from the sealed
     record under the fidelity rule and dual review recorded in
     `DECISION-PACKETS/F-docs-rewrite.md` §4.6–§4.7 as adopted by the
     owner. It is created in commits after the rename commit that
     immediately follows this entry's commit, never in that rename commit
     itself; no derived page changes any token, version, owner, or
     standing of the sealed record; on conflict the archive governs.
  6. Does not edit file 08. Does not edit, move, or re-freeze any frozen
     artifact (the rename is a path move with identical bytes). Does not
     mark any row SATISFIED. Does not open D-056 Class A. Does not pin
     QUALIFIED or DEMONSTRATED. Amends D-000 exactly as clause 1 and
     clause 4 state — [under §6.10 option (b): this register closed at
     this heading and the recording obligation continuing in the named
     successor register; under option (a): that, plus the end of the
     D-NNN series, the ADR entry form, and the authority of the ADR set]
     — and in no other respect; changes no other term of D-000, clause
     4's commit-and-push rule included; does not amend D-056. Does not
     decide any reserved number, list, owner, or Class A question. Does
     not invent fixture bytes.
- **Readiness effect:** None — records the measured MET state; changes no
  condition.
- **Reversibility:** By `git revert`, in this order: first the front-door
  and metadata commits that follow the rename, then the rename commit
  that immediately follows this entry's commit, then this entry's commit.
  The rename and this entry are separate commits, so this entry can be
  reverted without reverting the rename; the rename cannot be reverted
  while a new `docs/README.md` occupies the live path it restores. That
  order is a total overturn only while no dependent post-move work
  exists: once derived pages, or decisions recorded in the successor
  register of clause 4, exist, those are reversed or superseded first.
  Overturn: C-DSEAL. Overturning reopens this register for headings and
  restores `docs/` as the live path.
- **Commit:** the commit carrying this entry; its parent is <R>, the
  commit that recorded the measurement heading cited in the Subject
  above. This entry cites neither its own commit nor the rename commit
  that immediately follows it — neither exists while the entry is being
  written. Committed and pushed per D-000 clause 4 (COORD:L39–L42) before
  the rename. The new front door, the seal metadata and the archive
  manifest are created in commits after the rename (§4.3, §4.4).
```

Everything in `<…>` above is unknown at HEAD and must be measured at sealing time, and every one of those values is already known when the entry is written: the measured commit `<P>`, the measurement-record commit `<R>` and its artifact path and digest, the dates, and the condition cells. Nothing above asserts any condition is MET today. The seal commit `<S>` and the rename commit `<M>` appear nowhere in the sealed bytes: they do not exist while the entry is being written, and they could not be filled in afterwards either, because this register is closed at this heading and the archive is read-only — they are recorded only in `docs/ARCHIVE.md` (§4.4), which is written after both exist. The **Status:** field above is written in the user-made form (§6.7 option (a)) with the D-000 cycle as the bracketed ALTERNATIVE (§6.7 option (b)); the form the sealing entry actually takes is §6.7's option, whose labelled Orchestrator recommendation is (c). The measurement heading that the Decision type and the Subject cite is the penultimate heading; D-SEAL is the last.

### 4.3 The `git mv` step (mechanical; the rename commit `<M>` contains renames only)

Order of acts, each commit pushed before the next act begins (D-000 clause 4, "**Commit and push per decision**", COORD:L39–L42): the D-000 measurement cycle is committed and pushed as `<R>` — the measurement artifact plus the penultimate COORD heading, both pinned to `<P>`, plus that cycle's own draft, review-prompt and reviewer-verdict artifacts under `docs/coop/artifacts/`; then D-SEAL is committed and pushed as `<S>` — parent `<R>`, `docs/coop/COORDINATOR-DECISIONS.md` the only file it touches; then the pure move is committed and pushed as `<M>` — renames only; then the front door `docs/README.md`, the seal metadata `docs/ARCHIVE.md` and the external `docs/archive-manifest.v1.json` follow in one or more later commits.

Preconditions: `git status --porcelain --ignored -- docs` reports nothing under `docs/` (§4.1 precondition 3 — plain `--porcelain` cannot see gitignored paths); `<R>` and `<S>` committed and pushed; `origin/main` a fast-forward of local (E2).

```
git mv docs <ARCHIVE>                              # history preserved; verify with: git log --follow -- <ARCHIVE>/coop/COORDINATOR-DECISIONS.md
git commit -m "rename docs/ -> <ARCHIVE>/ (path move only; bytes unchanged; the docs/ tree of <S>, measured at <P>)"   # this commit is <M>
```
`<M>` contains that rename and nothing else. `<ARCHIVE>/README.md` is the old `docs/README.md` (tracked: `git ls-files docs/README.md`), carried across by the rename and left untouched; `<M>` adds, replaces or edits no file inside the archive. A `git mv` of a directory also carries any untracked **or gitignored** file that sits under it, which is why precondition 3 requires `git status --porcelain --ignored -- docs` to report nothing before the measurement.

Then, in one or more commits after `<M>` (never in `<M>`):

```
mkdir docs && cp <template> docs/README.md         # the front door; points at the archive until the derived tree lands
<write docs/ARCHIVE.md>                            # seal metadata: the D-SEAL heading, <P>, <R>, <S>, <M>, the path mapping, the rules (§4.4)
<generate docs/archive-manifest.v1.json>           # one path + sha256 per file under <ARCHIVE>/, terminal COORD bytes included
<open docs/DECISIONS.md>                           # the successor decision register D-SEAL clause 4 names (§6.10 (b) form); whichever entry it records first cites D-SEAL and <P>; not one of the 128 derived review pages (§5.1, §4.8)
git add docs
git commit -m "front door, archive metadata, external archive manifest and successor decision register for <ARCHIVE>/"
```
The manifest is written outside the tree it hashes, so it can hash every archived file — including the terminal `<ARCHIVE>/coop/COORDINATOR-DECISIONS.md` — without hashing itself and without any archived file carrying its digest. `docs/DECISIONS.md` is the successor decision register D-SEAL clause 4 names (§6.10 (b): COORD form, continuing the D-series at the next unused D-NNN identifier measured at that time; under §6.10 (a) the same content is ADRs in `decisions/`); it is created outside `<ARCHIVE>/`, like the front door and the manifest, and it is not one of the 128 derived review pages of §5.1 — those pages are derived from the sealed record, whereas this register holds decisions made after the seal (§4.8 items 1 and 9).

Verification, in the order the commits land. `git diff --name-only <P> <R>` returns `docs/coop/COORDINATOR-DECISIONS.md`, the measurement artifact `<MEASUREMENT-PATH>`, and that D-000 cycle's own draft, review-prompt and reviewer-verdict artifacts under `docs/coop/artifacts/` — each of them enumerated by path in the measurement entry's Status field, which is what makes this check exact — and nothing else. A D-000 cycle commit is never two files: measured on this record's own decision commits, `git show --name-only --format= 4abb961` (D-292) lists **13** files — COORD, `coordinator-decisions.D-292.draft.md` and `coordinator-decisions.D-292.turn2.draft.md`, the two matching `review-prompt.md`, four `review-adversarial.{claude2,codex}[.turn2].json` verdicts, the measured artifact `g21-leftover-join.v13.json`, its two `review-independent` verdicts and its review prompt — while `cb8bd16` (D-291), `20e6d2d` (D-290) and `8d0cf09` (D-288) list **9** files each on the same pattern; everything but COORD is under `docs/coop/artifacts/`. The record's existing entries name the subject artifact and the reviewer verdicts with their digests, but not the review prompts and not the artifact's own `review-independent` verdicts (D-292: Status COORD:L16038–L16050, Subject COORD:L16072–L16073; that entry, COORD:L16035–L16165, contains no `review-independent` string), so the measurement entry's Status field enumerates the whole file list of `<R>` in order for this check to be exact. `git diff --name-only <R> <S>` returns exactly `docs/coop/COORDINATOR-DECISIONS.md`, and `git diff --numstat <R> <S>` shows zero deleted lines, so the seal removes nothing (that the addition sits at the end follows from D-SEAL being the last heading and from the prefix digest covering every byte before the measurement heading, not from `--numstat`); that one-file form of the check assumes the user-made seal of §6.7 option (a) — under the bracketed §6.7 (b) ALTERNATIVE the seal is itself a D-000 cycle, so `<S>` carries that cycle's review artifacts too and its check takes the same enumerated form as the `<P>`→`<R>` one. The whole delta between the measured tree at `<P>` and the archived tree is therefore what `<R>` adds — the measurement artifact, the penultimate heading appended to COORD, and that cycle's draft, prompts and verdicts — plus the single D-SEAL heading `<S>` appends. On `<M>`, `git diff --stat HEAD~1 HEAD -M100%` shows renames only (100 % similarity, zero content changes) and `git diff --numstat -M100% HEAD~1 HEAD` shows no added or deleted lines; `git status --porcelain --ignored -- <ARCHIVE>` reports nothing under `<ARCHIVE>/` (the `--ignored` form, for the reason in §4.1 precondition 3); `git log --follow` on three sample files (file 08, COORD, one artifact) shows pre-move history. On the following commit, every path in `docs/archive-manifest.v1.json` exists under `<ARCHIVE>/` and its sha256 recomputes, and each digest quoted in the measurement artifact of `<P>` recomputes at its mapped path — the COORD prefix digest of D-SEAL's Subject by extracting from `<ARCHIVE>/coop/COORDINATOR-DECISIONS.md` the byte range the artifact records (the first byte through the last byte preceding the measurement heading's `## ` line, whose length the artifact states) and hashing that prefix, never the whole file.

### 4.4 Archive metadata — DRAFT (`docs/ARCHIVE.md`, in the new tree; created in a commit after `<M>`; the archive itself gains no new file)

```markdown
# `<ARCHIVE>/` — the sealed OpenSIP design record (read-only)

`<ARCHIVE>/` is the repository's `docs/` tree as it stood at the seal commit `<S>` — the tree
measured at `<P>`, plus what the measurement commit `<R>` added (the measurement
artifact under `<ARCHIVE>/coop/artifacts/`, the penultimate heading of the register, and that
D-000 cycle's own draft, review-prompt and reviewer-verdict artifacts under the same
directory), plus the single `D-SEAL` heading that
`<S>` appended to `docs/coop/COORDINATOR-DECISIONS.md` — moved unchanged to this path by the
rename commit `<M>`. It is the provenance record; nothing in it is edited, moved, re-versioned,
or added to after the authorized pure move — including this page, which lives in the derived
`docs/` tree, not in the archive.
`<ARCHIVE>/README.md` is the sealed tree's own `docs/README.md`, unchanged by the move.

| Field | Value |
|---|---|
| Sealing entry | `## D-SEAL — Seal the design record at the measured commit <P>` (`<ARCHIVE>/coop/COORDINATOR-DECISIONS.md`, last heading) |
| Measured commit | `<P full sha>` — the already-known commit the measurement artifact measures; not the parent of the seal commit |
| Measurement commit | `<R full sha>` — the D-000 cycle that added `<MEASUREMENT-PATH>` and the penultimate heading of the register, both pinned to `<P>`, together with that cycle's own draft, review-prompt and reviewer-verdict artifacts under `<ARCHIVE>/coop/artifacts/`, enumerated in that heading's Status field; committed and pushed before the seal |
| Measurement | `<MEASUREMENT-PATH>` sha256 `<64 hex>` — reviewed by that D-000 cycle, recorded as the penultimate heading of the sealed register |
| Seal commit | `<S full sha>` — parent `<R>`; appends D-SEAL and changes no other file; committed and pushed before the move; not cited by D-SEAL itself |
| Rename commit | `<M full sha>`: `git mv docs <ARCHIVE>`; 100 % rename similarity; renames only; zero content changes; the tree it moves is the `docs/` tree of `<S>` |
| Register at seal | `<ARCHIVE>/v2/architecture/08-decision-and-readiness-register.md` sha256 `<64 hex>` (unchanged since `<P>`) |
| Decision register at seal | `<ARCHIVE>/coop/COORDINATOR-DECISIONS.md` sha256 `<64 hex>`, <n> headings (<k> CONTESTED, parked), the last being `D-SEAL` |
| Manifest | `docs/archive-manifest.v1.json` — external to the archive; one path + sha256 per file under `<ARCHIVE>/` at `<M>`, terminal COORD bytes included |

## Path mapping
A citation of the form `docs/<p>` **written in or before the sealing entry, in any tracked repository file present
at `<S>`** — file 08, COORD, any frozen artifact, or a tracked file outside `docs/` such as one
under `DECISION-PACKETS/` — resolves to `<ARCHIVE>/<p>` **when `docs/<p>` is itself a tracked path
in the `<S>` tree, immediately before the move**. A path absent from that tree is not remapped, and
a citation written after the seal is not mapped by this rule: it names its target directly. That is
D-SEAL clause 2's rule restated; this page states no wider rule than the sealed entry does.
Examples:
- `docs/v2/architecture/08-decision-and-readiness-register.md` → `<ARCHIVE>/v2/architecture/08-decision-and-readiness-register.md`
- `docs/coop/COORDINATOR-DECISIONS.md` → `<ARCHIVE>/coop/COORDINATOR-DECISIONS.md`
- `docs/coop/artifacts/<file>` → `<ARCHIVE>/coop/artifacts/<file>`
- `<MEASUREMENT-PATH>`, which is under `docs/coop/artifacts/` — added by `<R>`, absent at `<P>`, present at `<S>` → the same path under `<ARCHIVE>/`
- `docs/v2/implementation/` (condition 5) → <the §6.5 option, verbatim from D-SEAL clause 3; under that clause's default text the path is absent from the sealed tree at `<S>`, is not remapped, and no directory, stub or pointer is created for it; condition 5 being MET, it is described there as authorized but not yet created, preserved literally as the prospective live path>

## What is where (unchanged from the sealed tree)
- `<ARCHIVE>/coop/COORDINATOR-DECISIONS.md` — the decision register D-000 … D-SEAL
- `<ARCHIVE>/v2/architecture/` — the V2 working surface; file 08 is the readiness register
- `<ARCHIVE>/coop/artifacts/` — frozen contracts, harness occupancies, corpora, leftover-joins, reviews, drafts, dispatch texts, checkers, fixtures
- `<ARCHIVE>/coop/` (rest) — V1 authority: `IMPLEMENTATION-FREEZE.md`, `IMPLEMENTER-BLUEPRINT.md`, `v1-slice.md`, `product-dispositions.md`, narrative `architecture/`, `steering/`, `cleansheet/`, `deltas/`, logs
- `<ARCHIVE>/README.md` — the sealed tree's own front door, as it stood at `<S>` (unchanged since `<P>`)

## Rules
1. Read-only: nothing changes after the authorized pure move. A change to any file under `<ARCHIVE>/` is a defect; fix it by reverting. Nothing is added to the archive either: this page, the front door `docs/README.md` and `docs/archive-manifest.v1.json` all live in `docs/`.
2. The derived `docs/` tree cites the archive by path and sha256; on conflict the archive governs.
3. `docs/archive-manifest.v1.json` is the archive's digest list, pinned to the archive as it stood at `<M>`. It is never regenerated from changed bytes: a mismatch between a listed digest and the file under `<ARCHIVE>/` is the defect of rule 1, and is repaired by restoring the archived bytes — or, if the manifest itself was altered, by restoring the original manifest — never by minting digests that match the changed bytes, which would make the detector agree with the defect. An intentional new archive state is a different act, not this repair: it requires an explicit authorization recorded in the successor register of rule 4 and a new manifest version (`docs/archive-manifest.v2.json`, and so on), leaving the `v1` manifest as the pin on `<M>`.
4. Decisions after the seal are recorded in the successor register named in D-SEAL clause 4 ([the option chosen in §6.10]), never in the archive and never on this page.
```

### 4.5 Condition 5's literal path `docs/v2/implementation/` — how it is carried (options; owner chooses in §6.5)

The problem: condition 5 (08:L392–L393; D-001 §1 quoted "byte-for-byte", COORD L116–L117) and the reservation sentence (08:L395; v2 README L94) name `docs/v2/implementation/` literally; COORD contains 219 lines mentioning it and every "authorize" hit is negated or conditional (other-docs §3.2). After `git mv docs <ARCHIVE>`, the literal path would denote a directory under the *new* tree (`docs/v2/implementation/`), which the restructure otherwise does not create.

| Option | What the new register says | Consequence |
|---|---|---|
| 5-A **Literal**: create `docs/v2/implementation/` in the new tree exactly as named | Condition 5 and the reservation sentence copied verbatim; no mapping clause | Zero wording change; the new tree carries a `v2/` directory that exists only for this path (inconsistent with §2's layout); the archive's `v2/architecture/` and the live `v2/implementation/` sit under different roots — readers must learn that `docs/v2/` and `<ARCHIVE>/v2/` are siblings |
| 5-A **as amended** (Codex round 1, amendment 3, as re-scoped by Codex round 2, amendment 1 and Codex round 3, amendment 2; §0.3): the archive path mapping is limited to the tracked paths present in the sealed tree at the seal commit `<S>`, immediately before the move, and `docs/v2/implementation/` — authorized by condition 5, which is MET at `<P>` (§4.1 precondition 1), but not yet created, and absent at `<P>` and at `<S>` — is preserved literally as the prospective live path the sealed text names; no directory, stub or pointer is created in either tree | Condition 5 and the reservation sentence copied verbatim; the mapping clause states which paths it covers, and D-SEAL clause 3 states that this one is not among them and describes it as authorized but not yet created | Zero wording change, and nothing is created at a path the authorization has not yet caused to exist; 08:L395 ("Until then, `docs/v2/implementation/` remains reserved and absent") and v2 README L94–L95 ("remains reserved and absent until the central register explicitly reaches blueprint-ready and product/architecture authorities approve") state the position before that authorization and are quoted as history, not as standing at the seal; readers learn one rule with one stated exception; the directory is created, when it is created, wherever the live tree then puts it, with no stub to remove |
| 5-B **Mapping clause in D-SEAL** (the sealed text stays verbatim; D-SEAL records "`docs/v2/implementation/` denotes `docs/implementation/`", or another name) | Register page quotes condition 5 verbatim **and** the D-SEAL mapping clause beneath it | One reviewed sentence carries the path; consistent layout; but the D-010 precedent cited for this row in earlier drafts is of 5-C's form, not of this one: C-D010 amended file 08 itself ("Per D-001's new-row rule, C-D010 amends file 08's condition-2 wording", COORD:L1003–L1004, within D-010 L1003–L1012; the historical range in D-001's §1 blockquote is handled by the pin-note at COORD:L119–L122), whereas 5-B leaves file 08 unchanged and maps its words from a later heading (§0.3, Codex refutation 7) |
| 5-C **MF-6 edit of file 08 before the seal**: a D-000 cycle amends condition 5's path text in file 08 (as D-010/C-D010 did for condition 2), then D-SEAL seals the amended file 08 | Register page quotes the amended condition 5 | Cleanest sealed text; costs one more D-000 cycle and a file 08 edit before sealing; changes D-001's "byte-for-byte" quote — D-001 already carries one such pin-note, so a second is in form |
| 5-D **Symlink/pointer**: keep `docs/v2/implementation/` as a one-line pointer directory (`README.md` → real location) | Verbatim + pointer | Satisfies the literal path and the layout, but a pointer directory in a design tree is a permanent oddity; Git symlinks behave differently per platform (DR-002-platform list is itself a record concern) |
| 5-E **Sequence the authorization before the mv and keep the implementation tree outside `docs/`** (e.g. authorize `docs/v2/implementation/` → it is created → mv moves it into `<ARCHIVE>/v2/implementation/`) | — | Incoherent: the authorized implementation directory would be archived at birth. Listed to show it was considered; not recommended (see the Orchestrator recommendation line below) |

Orchestrator recommendation (labelled, not a decision): **5-A as amended by default; 5-C if the owner wants a different live path for the implementation tree; 5-B withdrawn as a D-010-style act; 5-D and 5-E not recommended.** Reason: the amended 5-A leaves the sealed text verbatim, creates nothing at a path the record reserves as absent, and needs no per-path exception beyond the one clause 3 states; the mechanism the record actually shows for changing a condition's wording is D-010's pre-seal amendment of file 08 (COORD:L1003–L1004), which is 5-C's form, so an owner who wants a different live path runs that cycle before `<P>` rather than mapping the sealed words afterwards.

### 4.6 Fidelity rule (the standard every review applies)

A derived page is **faithful** iff, for every sentence: (a) it cites an archival source per §3.0 or is a permitted `[editorial]` sentence; (b) every token, version, digest, owner, date, obligation id, verdict, and count appears verbatim in the cited bytes; (c) it asserts nothing the cited bytes do not assert (no inference presented as record; inferences are marked `(inventory inference)` and are REJECT grounds in design/contract/gate/register pages, tolerated only in `README.md` navigation prose); (d) it omits nothing load-bearing from the cited entry's "Does not …" negations, riders, and remainder lists; (e) it does not upgrade standing (`CANDIDATE-NOT-APPLIED` stays so; `OPEN` stays so); (f) it does not use deictic version references; (g) its Sources section lists every path/digest cited. Reviewer verdict vocabulary: `ACCEPT` (0 MUST-FIX, 0 SHOULD-FIX), `ACCEPT-WITH-ADVISORIES` (advisories only, travel as honesty work in the page's front matter), `REJECT` (≥1 MUST-FIX). A `REJECT` on (b), (c) or (e) is a fidelity defect; on (a), (f), (g) a form defect. Both kinds block publication.

Automated pre-checks run before any human/agent review (must pass, or the dispatch is refused): every `[<ARCHIVE>/…]` path exists; every `sha256:` recomputes; every `L<n>` is within the file; every `D-NNN` heading exists in the archived COORD; every `DR-xxx` / `DR-Gxx` id exists in the archived file 08; every version string `v<N>` resolves to a file; no sentence lacks a citation or `[editorial]`.

### 4.7 Review cadence — one dual-review cycle per doc

- **Cycle** = the D-000 form (COORD L26–L36): one dispatch to two independent reviewers (Claude in a fresh pane; Codex `--yolo` in a fresh pane — `herdr-topology` memory), both prompted to refute; up to **three turns**; consensus = both `ACCEPT` (0/0); no consensus after three turns → the page is `CONTESTED`, parked, not published, batched to the owner.
- **Unit** = one page (one design doc, one contract page, one ADR, one gate page, one register page, the glossary, each README). Batching the *dispatch* of homogeneous pages (e.g. eight gate pages) is allowed; the verdict is still per page, and a REJECT on one page does not block the others.
- **Order** (dependencies first): `AUTHORITY.md` + `GLOSSARY.md` → `register/*` → `contracts/*` → `gates/*` → `decisions/*` → `design/*` → READMEs. A page may be dispatched only when every page it links to is ACCEPTed or explicitly marked "pending" in its front matter.
- **Inputs frozen per dispatch**: the page bytes (sha256 in the dispatch text) and the sealed archive; a page edited after dispatch is re-dispatched as a new turn.
- **Record of review**: each ACCEPT is written to `docs/.review/<page>.<reviewer>.turn<n>.json` (or a single `docs/REVIEW-LEDGER.md` table) with the page sha256 and verdict digest; this ledger is the rewrite's equivalent of the archive's `review-independent` files and is the only process material allowed in the new tree.
- **Owner touchpoints**: after `register/*` (structure is proven), after `contracts/*` + `gates/*` (the design core is proven), and at the end (done check §4.8). CONTESTED pages are surfaced at each touchpoint.

### 4.8 What "done" means

All of the following, verifiable by script and by the review ledger:

1. Every planned page (count per §5) is `ACCEPT` 0/0 from both reviewers within three turns, or is listed as `CONTESTED` with the owner's disposition recorded as an entry of the successor decision register (D-SEAL clause 4; under §6.10 (b) the COORD-form `docs/DECISIONS.md` of §2) (a CONTESTED page is never silently dropped). A disposition recorded there before the sign-off of item 9 precedes it in that register, so the sign-off is then not the register's first entry.
2. Automated pre-checks (§4.6) pass on the whole tree: 100 % of citations resolve; 100 % of digests recompute; zero uncited sentences. The archive's digest list is the **external** `docs/archive-manifest.v1.json` (§4.3–§4.4), never a manifest inside `<ARCHIVE>/`: every path it lists exists under `<ARCHIVE>/` and its sha256 recomputes, terminal COORD bytes included. That manifest is validated by this script rather than dual-reviewed, and is not one of the pages counted in §5; validation compares its pinned digests against the bytes under `<ARCHIVE>/` and never rewrites the manifest to match them — a mismatch is repaired by restoring the archived bytes or the original manifest (§4.4 rule 3); `docs/ARCHIVE.md` is a page and is dual-reviewed under item 1 (§5.1 counts it as the fifth root page).
3. `register/*` tokens equal the sealed file 08's leading labels row for row and the sealed snapshot's counts (the script diffs them).
4. Every artifact of §1.5a–c is reachable from exactly one page (no orphan; no duplicate home) — or is explicitly listed as "archive only" in `contracts/README.md` / `gates/README.md`. The two artifacts that appear in both §1.5a and §1.5c — `component-manifest-fixture-corpus.v6` and `identity-namespace-negative-test-corpus.v1` (§1.5a 31/32 rule) — have their single home under `gates/corpora/` and are cross-referenced, not duplicated, from `contracts/DR-103.component-manifest-schemas.md` and `contracts/DR-104.identity-namespace.md` (§8 Q22).
5. Every BINDING-DESIGN COORD entry (72) is condensed by exactly one ADR; every PARKED entry is listed in `decisions/README.md` with its resolver; every CUSTODY entry is cited from at least one contract or gate page (its fact is not lost).
6. The rename commit `<M>` shows renames only (100 % similarity, zero content changes); `<ARCHIVE>/README.md` is the sealed tree's own `docs/README.md`, byte-identical to its pre-move bytes; the front door `docs/README.md`, the seal metadata `docs/ARCHIVE.md`, `docs/archive-manifest.v1.json` and the successor decision register `docs/DECISIONS.md` (D-SEAL clause 4) are created in commits after `<M>` (§4.3–§4.4), never in `<M>`.
7. Repo-root `README.md` points at `docs/` and `docs/README.md` points at `<ARCHIVE>/README.md`.
8. A CI job (or a documented script) re-runs the pre-checks on every change to `docs/` (protects against drift; TREE-ENDSTATE §7.2 step 9 proposed the same for the old tree). It reports any `docs/archive-manifest.v1.json` mismatch as a defect and never regenerates the manifest from the changed bytes (§4.4 rule 3).
9. The owner's sign-off, recorded in the successor decision register (D-SEAL clause 4; its location and form are the option chosen in §6.10 — under (b) the COORD-form `docs/DECISIONS.md` of §2). It is that register's **first** entry only if no post-seal decision and no CONTESTED-page disposition (item 1) was recorded there earlier; otherwise it is recorded after those entries. Whichever entry is first cites D-SEAL and `<P>` (D-SEAL clause 4). That register is not one of the pages counted in §5 and is not dual-reviewed under item 1: it holds decisions made after the seal, not content derived from the sealed record (§2, §4.3).

---

## 5. Sizing

### 5.1 Docs per type (baseline = options at their orchestrator-recommended values; alternatives in parentheses)

| Doc type | Count | Derivation |
|---|---|---|
| Root pages (`README.md`, `ARCHIVE.md`, `AUTHORITY.md`, `GLOSSARY.md`, `v1/README.md`) | 5 | §2; `docs/ARCHIVE.md` is the seal-metadata page of §4.4. `docs/archive-manifest.v1.json` is in the tree but is not a page: it is validated by script, not dual-reviewed (§4.8 item 2) |
| Subsystem design docs | 7 | `design/00–06` (8 DESIGN-SOURCE v2 files condensed into 6 + one scope page) |
| Contract companion pages | 26 | one per row carrying a contract (§1.5a: DR-101–114, 116–118, 120–122, 124–127, 131, 133); 31 artifacts (§1.5a 31/32 rule: 32 artifact rows less the condition-4 naming candidate `dr117-ee-gate-naming.v3`) |
| Gate pages | 32 | one per gate row incl. G06/G11/G13/G17 (condition 4 counts 32 of 32, 08:L417) |
| Register pages | 6 | `register/README, inherited-v1-prerequisites, v2-decisions, review-findings, release-gates, readiness` |
| ADRs | 49 (§6.3 (b); 72 if one per BINDING-DESIGN entry, §6.3 (a); 70 only if the owner also selects the 21 candidate-ADR groups of §5b as an expansion of §6.3 — §6.4 (b) does not select them) | decisions inventory §5 groups (+ §5b) |
| Index pages (`contracts/README`, `gates/README`, `decisions/README`) | 3 | §2 |
| Glossary entries | — (in Root pages) | §3.6 seed list, ~40 terms; the page is `GLOSSARY.md`, already counted in Root pages, so this row adds nothing to the sum |
| **Total pages to review** | **128** (149 only if the 21 candidate-ADR groups are selected as the §6.3 expansion; not a consequence of §6.4 (b)) | 5 + 7 + 26 + 32 + 6 + 49 + 3 = 128; + 21 = 149 |

### 5.2 Effort in review cycles (assumptions stated)

- **A1.** One cycle per page; a cycle is up to three turns (D-000 clause 2). Observed in the record: 28 occupancy recordings D-208–D-235 all `ADOPTED 2026-08-22`; 18 entries `ADOPTED 2026-08-23`; 27 entries `ADOPTED 2026-08-24` (Status lines, decisions inventory §2) — i.e. 18–28 mechanical dual-review cycles per day were achieved for *structured JSON recordings*. Prose fidelity review is heavier; assume **6–12 pages per working day** for contract/gate/ADR pages and **2–4 per day** for design docs.
- **A2.** First-pass REJECT rate: the record shows turn-1 OBJECT/REJECT is common (e.g. D-292 turn-1 Claude OBJECT, COORD L16047; DR-202 turn 1 REJECTED, 08:L321). Assume 40 % of pages need a second turn and 10 % a third; assume 3–5 % end CONTESTED and go to the owner.
- **A3.** Pre-check automation exists before the first dispatch (a day of scripting; not a review cycle).
- **A4.** The archive is sealed and stable; no re-pinning mid-rewrite (E1 note in `DECISIONS-NEEDED.md`: a mid-act commit forced a re-pin once).

| Phase | Pages | Cycles (1 per page) | Turns expected (A2) | Working days (A1) |
|---|---|---|---|---|
| Root + register | 11 | 11 | ~17 | 2–3 |
| Contracts | 26 | 26 | ~39 | 3–5 |
| Gates | 32 | 32 | ~48 | 3–6 |
| ADRs (49) | 49 | 49 | ~74 | 5–9 |
| Design docs + indexes | 10 | 10 | ~15 | 3–5 |
| **Total (baseline)** | **128** | **128** | **~192** | **16–28** |
| Candidate ADRs (the §6.3 expansion; not selected by §6.4 (b)) | +21 | +21 | ~32 | +2–4 |
| Copy-JSON verification (option §6.2 copy) | — | 0 (script) | — | +1 |

These are estimates from the assumptions above, not measurements; the record contains no throughput figure for prose review.

---

## 6. Options the owner must choose

Each row: options → consequences → an **Orchestrator recommendation** line (clearly labelled; not a decision).

### 6.1 Archive directory name

| Option | Consequence |
|---|---|
| (a) `docs-old/` (owner's working name) | Short; sibling of `docs/`; "old" reads as deprecated rather than authoritative — but the archive *is* the authority on conflict (§4.6) |
| (b) `docs-sealed/` or `docs-record/` | Names the property (sealed, provenance) rather than age; same mechanics |
| (c) `docs/archive/` (inside the new tree) | One tree; but `git mv docs docs/archive` is a self-move (needs a temp name), the archive then sits under the tree that cites it, and every `docs/<p>` citation maps to `docs/archive/<p>` — the mapping is still one rule |
| (d) TREE-ENDSTATE's `docs/architecture/` + `history/` layout (§2.2, §7.2) | Moves files *within* the tree to new sub-paths (contracts/, instruments/, history/) — breaks the single-rule path mapping (each artifact gets a per-file new path), contradicts "frozen provenance record", and its own §7.1 forbids moves "during multi-agent contract churn" |

**Orchestrator recommendation:** (b) `docs-sealed/`, or (a) if the owner prefers the name already used in F1; not (c)/(d). The name appears in D-SEAL clause 2 and in every citation; choose once.

### 6.2 Contract / occupancy / corpus JSON: copied or linked

| Option | Consequence |
|---|---|
| (a) **Link only**: pages cite `<ARCHIVE>/coop/artifacts/<file>` + sha256; no JSON under `docs/` | Single copy of every byte; zero drift risk; readers open the archive for the contract itself; the new tree is prose-only |
| (b) **Copy final versions** (the 31 §1.5a artifacts + 28 occupancies + 43 corpora [+26] + naming parents; `component-manifest-fixture-corpus.v6` and `identity-namespace-negative-test-corpus.v1` are in both the 31 and the 43, so the distinct count is 29 + 28 + 43 = 100 [+26] + naming parents) into `docs/contracts/json/`, `docs/gates/occupancy/`, `docs/gates/corpora/`, byte-identical, same file names | Self-contained design tree; two copies of ~130 files; a CI digest check (§4.8 item 2) must assert copy = archive forever; any later contract successor (post-seal) creates a *third* place |
| (c) Copy contracts only, link occupancies/corpora | Middle path; two rules for readers |

**Orchestrator recommendation:** (a) link only, with the sha256 on every page and a script that verifies them — the archive is frozen, so links cannot rot; one byte home means zero drift and no standing CI obligation that a copy still equals the archive. Not on D-033: that entry's Subject is "DR-001 citation form only" (COORD:L1815) and its form is `(path, named section or selector, segment hash)` (COORD:L1823) — a citation-form rule for DR-001-style standing pins, not a repository-wide full-file path + sha256 convention (§0.3, Codex refutation 8).

### 6.3 ADR granularity

| Option | Count | Consequence |
|---|---|---|
| (a) One ADR per BINDING-DESIGN COORD entry | 72 | 1:1 traceability; 30 near-duplicate ADRs for select/record/owner-record triplets (ADR-RB-DR002 … DR-011) |
| (b) One ADR per ADR group (decisions inventory §5) | 49 | Each disposition triplet, the SATISFIED-rule pair (D-056 + D-133), the gate-naming trio (D-086, D-145, D-159), and D-134 + D-135 become one ADR each; every member still listed and cited |
| (c) One ADR per register row | ~35 | Loses cross-row decisions (D-001, D-002, D-056, D-133, D-018) or forces "global" ADRs anyway |

**Orchestrator recommendation:** (b) 49 groups, with the ADR index carrying the D-NNN → ADR reverse map so 1:1 lookup survives; the 21 candidate-ADR groups of §1.2/§5b are a separate expansion of this option and are not recommended — §6.4's labelled candidates belong on the contract, gate and design pages, not in 21 further ADRs — so the ADR count stays 49 and the §5.1 page total stays 128 (selecting the expansion would make them 70 and 149).

### 6.4 Whether candidates (`CANDIDATE-NOT-APPLIED`) appear in the new docs

| Option | Consequence |
|---|---|
| (a) **Exclude**: only ACCEPTED (SATISFIED-grade) rows and accepted design contracts (D-013/D-015/D-035/D-038) get contract pages; candidates are archive-only | New tree carries 5 SATISFIED rows + 4 accepted contracts; 22 of the 26 contract lineages, all 28 occupancies and all 43 corpora vanish from the design view even though they are the only recorded design for those rows — the tree would not describe the system |
| (b) **Include, labelled**: every final candidate gets its page with `CANDIDATE-NOT-APPLIED — "binds NOTHING"` in the standing field and a banner; §3.1 design docs may summarise them only under "Candidate design (not applied)" | Complete picture; standing is honest on every page; readers must read the label (mitigated by the banner and the glossary) |
| (c) **Include only rows whose Class A/B question is answered at sealing** (after B1–B3 and any later SATISFIED cycles) | Depends on how many rows reach SATISFIED before the seal — not in the record today (condition 2 is 5 of 32); if all five conditions are MET at sealing, condition 2 requires every slice-affecting row `SATISFIED`, which would make (c) ≈ (b) for those rows anyway |

**Orchestrator recommendation:** (b) — which governs how candidates appear on the contract, gate and design pages and adds no ADRs: the 21 candidate-ADR groups are the separate expansion of §6.3 (§5.1: 70 ADRs, 149 pages), which (b) here neither selects nor implies. Note the logical point in (c): sealing presupposes condition 2 MET, i.e. every slice-affecting row `SATISFIED`; at that time most "candidates" of this packet will have been re-recorded under D-056/D-133 and the label question shrinks to the deferred rows (DR-106/108/109/110/113/116 and DR-128/129/130) and to gate occupancies (which stay `CANDIDATE-NOT-APPLIED` until QUALIFIED — condition 4 does not require QUALIFIED, 08:L390–L391).

### 6.5 Condition-5 path handling — see §4.5 (options 5-A … 5-E)

**Orchestrator recommendation:** 5-A as amended (§4.5) by default — archive mapping limited to the tracked paths present in the sealed tree at `<S>` immediately before the move, `docs/v2/implementation/` — authorized by the MET condition 5 but not yet created — preserved literally and absent as the prospective live path, no stub; 5-C if the owner wants a different live path; 5-B withdrawn as a D-010-style act; 5-D and 5-E not recommended.

### 6.6 Fixture bytes and DR-join-named corpora

| Option | Consequence |
|---|---|
| (a) Link only (as §6.2a) for `fixtures/**`, the 14 `permission-fx*` corpora and the 12 `doctor-fc-*` corpora not already among the 43 | Consistent with 6.2(a); gate pages list them with their naming join |
| (b) Copy the fixture directories enumerated in the `gates/` row of §2.1 into `docs/gates/fixtures/` | Binary/non-JSON payloads (18 `.bin`, 2 `.onebyte`, 2 `.empty`, 1 `.sh`, 1 `.log`) duplicated; the record pins them by digest inside corpus JSON — a copy adds nothing |
| Home for the 26 DR-join-named corpora | either under the gate page (G09/G12) or under the row page (DR-105/DR-114) — gates open question 3. The twelve/thirteen `doctor-fc-*` split is settled by the bytes: `doctor-actor-leftover-join.v12.json` names 13 `doctor-fc-*-input-corpus` files, 12 of them not already among the 43 (the 13th is `doctor-fc-join-input-corpus.v2`, already in the 43); `permission-leftover-join.v12.json` names 14 `permission-fx*-input-corpus` files |

**Orchestrator recommendation:** (a); and one canonical catalog of the 26 join-named corpora on the row pages `contracts/DR-105.*` and `contracts/DR-114.*` — their joins are what name the corpora (`permission-leftover-join.v12`, D-283; `doctor-actor-leftover-join.v12`, D-285) — with the gate pages G09/G12 carrying a cross-reference to that catalog rather than a second listing, so each corpus keeps the exactly-one-home rule of §4.8 item 4 and neither page invents an owner.

### 6.7 Form of the sealing entry

| Option | Consequence |
|---|---|
| (a) User-made entry (D-000 / D-054 / D-132 class, "recorded verbatim rather than made on their behalf") | Fast; the owner's own words seal the record; no reviewer verdict digests |
| (b) D-000 cycle (dual adversarial review, up to three turns) | Independent check that the measured snapshot in D-SEAL matches file 08 bytes; costs one cycle; a CONTESTED outcome would block sealing |
| (c) Both, as two distinct decision acts over three distinct repository states: a D-000 cycle records the measurement of the already-known measured commit `<P>` as the penultimate heading and is itself committed and pushed as `<R>`, then the owner's verbatim seal cites that heading, its digest and `<P>` as the last heading and is committed and pushed as `<S>` | Strongest, and non-circular: the seal cites a commit, a heading and a digest that already exist rather than its own commit id, and no all-files manifest sits inside the tree it hashes (such a manifest would have to hash itself and hash COORD while COORD carries its digest); the seal commit's parent is `<R>`, not `<P>`, so the measurement act keeps D-000 clause 4's "**Commit and push per decision**" (COORD:L39–L42); costs one D-000 cycle and two headings; the archive's manifest is produced outside the archive after the move (§4.3) |

**Orchestrator recommendation:** (c), as two distinct decision acts over three states (§4.2–§4.3) — the measurement must be reviewed (it is the last snapshot anyone will verify against live bytes) and is pinned to `<P>`, and its own commit `<R>` is pushed before the seal is written; the seal itself is the owner's act, cites `<P>`, the measurement heading and its digest, and self-pins neither its own commit nor an in-tree manifest; `<S>` is pushed before the move.

### 6.8 Untracked dispatch texts and working files before the mv

| Option | Consequence |
|---|---|
| (a) Commit the 31 untracked `_dispatch.*.txt` before the seal (the other 729 are tracked) | Complete provenance; E4 note in `DECISIONS-NEEDED.md` calls them "the protocol's never-committed dispatch texts" — but 729 of 760 *are* committed, so (a) restores consistency |
| (b) Leave untracked; delete after the mv | `git mv` carries them into `<ARCHIVE>/` as untracked files, and carries gitignored paths the same way (controlled test, §4.1 precondition 3), so until they are deleted there the byte-identical archive holds an overlay the measurement never covered; deleting them after the move loses the 31 dispatch texts for D-282–D-292 |
| Repo-root working files (`DECISIONS-NEEDED.md`, `DECISIONS-RECOMMENDED.md`, `DECISION-PACKETS/`, `PROPOSAL.cross-citation-convention.md`, `STATUS.2026-08-26.md`) | Outside `docs/`; unaffected by the mv; once committed they are tracked repository files present at `<S>`, so a `docs/<p>` citation written in them in or before the sealing entry becomes an `<ARCHIVE>/<p>` citation under D-SEAL clause 2 — which maps such a citation when `docs/<p>` is itself a tracked path in the `<S>` tree, and maps no citation written after the seal. `DECISION-PACKETS/` is untracked at HEAD `4abb961` (`git ls-files DECISION-PACKETS` returns no files), so committing it at the repository root before the measurement is what makes the seal's justification tracked; putting it under `<ARCHIVE>/packets/` instead would add bytes that were never members of the moved tree (§0.3, Codex refutation 14) |

**Orchestrator recommendation:** (a), after the owner checks what the 31 texts contain, on the untracked-overlay ground rather than the orphan ground: `git mv` of a directory carries untracked files — and gitignored files, which plain `git status --porcelain` does not show — with it (§4.1 precondition 3, whose guard is `git status --porcelain --ignored -- docs`), so the risk is not loss at the old path but a sealed archive carrying bytes the measurement never covered. Separately: commit `DECISION-PACKETS/` **at the repository root** before the measurement — it is untracked at HEAD `4abb961` — and keep it out of `<ARCHIVE>/`, which stays the sealed tree as it stood at `<S>`, moved byte for byte.

### 6.9 Treatment of V1 prose (`docs/coop/architecture/00–11`, freeze, blueprint) in the new tree

| Option | Consequence |
|---|---|
| (a) Pointers only (`docs/v1/README.md`) | New tree is V2-only; V1 authority stays exact and byte-pinned in the archive (v1-authority-baseline.json: 49/49 MATCH) |
| (b) Rewrite V1 narrative too | Doubles the sizing (10 more design docs + freeze/blueprint condensation); V1 prose is `SEALED unless noted` already (`01-product-boundary.md` L3) and the claim-register/checkers, not prose, are its authority |

**Orchestrator recommendation:** (a).

### 6.10 Post-seal decision register location and form

| Option | Consequence |
|---|---|
| (a) `docs/decisions/` ADRs continue the numbering (ADR-0050 …), each new ADR carrying the D-000 review digests | One register; ADR form for both condensed history and new decisions; the D-NNN series ends at D-SEAL. It also amends D-000 in three respects beyond location: D-000 requires every decision made under the delegation protocol to be recorded "here", in this register (COORD:L3–L4), in its stated entry format (COORD:L9–L12), with the clause-3 fields and clause 4's "**Commit and push per decision**" (COORD:L36–L42; the commit-and-push clause at L39–L42); ending the D-NNN series, changing the entry form, and seating new authoritative decisions among the derived, non-authoritative ADRs of §6.3 are substantive amendments that D-SEAL clause 6 would otherwise negate, so they must be stated explicitly in clause 1/clause 4 (§4.2) |
| (b) A new COORD-form register (working name `docs/DECISIONS.md`) continuing the D-series at the next unused D-NNN identifier measured at that time | Keeps D-000's entry form, review, reversibility, overturn and commit-and-push fields intact — clause 4 stays "**Commit and push per decision**" (COORD:L39–L42), so the seal's amendment of D-000 is confined to the register's location; two registers (derived ADRs for condensed history, COORD-form for live decisions); the D-NNN → ADR reverse map of §6.3 keeps history reachable |

**Orchestrator recommendation:** (b) — the COORD-form successor keeps D-000's entry form and its clause-4 commit-and-push rule intact (COORD:L39–L42), so D-SEAL's amendment of D-000 is confined to the register's location (clause 1, §4.2), and the 49 historical ADRs stay derived and non-authoritative (§6.3).

---

## 7. Risks and mitigations

| # | Risk | Mitigation |
|---|---|---|
| R1 | **Silent standing upgrade** — a derived page reads as if a `CANDIDATE-NOT-APPLIED` contract binds, or an `OPEN` row is settled | §3.0 rule 6; banner on every candidate page; reviewer checklist item (e) in §4.6; glossary entry for every standing token |
| R2 | **Lost negations** — the record's "Does not …" sentences (e.g. D-137 "D-056 Class A is not opened", D-292's 20+ "Does not" clauses) are load-bearing and easy to drop in condensation | ADR template has a mandatory "Does not" section quoted verbatim; contract/gate pages carry the recording entry's negations in the Standing field |
| R3 | **Version drift** — cell versions (v2/v8) vs COORD-current versions (v11/v9/v25) for DR-103/DR-105/DR-114 (contracts §5 Q2) are conflated | Every page states the Rule column (COORD/cell/DIVERGENT) and lists the history versions; the register page keeps the cell's own words |
| R4 | **Citation rot after the mv** — pre-seal citations use `docs/…` | D-SEAL clause 2's single mapping rule — a `docs/<p>` citation written in or before the sealing entry, in any tracked repository file present at `<S>`, resolves to `<ARCHIVE>/<p>` **when `docs/<p>` is itself a tracked path in the `<S>` tree, immediately before the move** (a path absent from that tree is not remapped; clause 3 carries the one such path the record names; a citation written after the seal is not mapped by the clause and names its target directly); the path-mapping table in `docs/ARCHIVE.md`; pre-check script rewrites and verifies; no per-file re-pathing (§6.1's Orchestrator recommendation line does not recommend the TREE-ENDSTATE-style scatter of option (d)) |
| R5 | **Condition-5 path incoherence** (§4.5) | Owner chooses among §4.5's options before sealing; the clause is quoted in `register/readiness.md`; §4.5's Orchestrator recommendation line does not recommend 5-E |
| R6 | **Untracked overlay inside the archive** — `git mv` of a directory carries untracked files with it, and gitignored files too (controlled test, §4.1 precondition 3), so anything left untracked or ignored under `docs/` at any point up to `<M>` (31 dispatch texts; `docs/coop/artifacts/__pycache__/`, 29 `.pyc` files at HEAD `4abb961` — and a fresh `.pyc` can appear at `<R>` or `<S>` just as easily, since `.gitignore` L1–L3 records that any `.pyc` present "is the residue of an invocation that omitted -B") is moved into the byte-identical archive without ever having been measured | §4.1 precondition 3; §6.8; `git status --porcelain --ignored -- docs` reports nothing before the measurement and `git status --porcelain --ignored -- <ARCHIVE>` reports nothing after the rename commit `<M>` — the `--ignored` form is required, because `.gitignore` L4–L5 (`__pycache__/`, `*.pyc`) make those paths invisible to plain `git status --porcelain`. The one addition to the measured tree that the archive is designed to carry is the `<R>` cycle's own **tracked** artifacts — the measurement artifact and that cycle's draft, review prompts and reviewer verdicts under `docs/coop/artifacts/`, committed by `<R>` and enumerated in the measurement entry's Status field (§4.3) — which are tracked, reviewed and named, not an unmeasured overlay |
| R7 | **Reviewer contamination** — the same reviewer session that wrote a page reviews it | Fresh pane per review (herdr topology memory); Claude authoring vs Claude-2/Codex review kept separate; verdict files carry the page sha256 |
| R8 | **Scope creep into design** — a rewrite "clarifies" a mechanism the record left reserved (e.g. OD-112-1..4, G02 tree accounting, OD-101-1 language) | §4.6 (c): no inference presented as record; reserved values are quoted as `RESERVED`/`UNDECIDED` with the artifact path; C1–C9 recommendations (AGREED) are decisions to record *before* the seal, not in the rewrite |
| R9 | **Cross-lineage citation staleness inside sealed joins** (A4 subject: eight current joins name superseded siblings as "current") | If A4 is adopted, the new register's "How to read" quotes the content-based reading (draft D-293 Decision 1); if not, gate/contract pages state the version-number reading and the recorded successor for each such sentence — either way the page quotes the join's sentence verbatim and adds the recorded successor, never edits the join |
| R10 | **Mid-rewrite record motion** — a new D-NNN or artifact lands after the seal | D-SEAL clause 1 closes COORD; post-seal decisions go to the successor register chosen in §6.10, whose labelled recommendation is (b) — a COORD-form successor continuing the D-series at the next unused identifier measured at that time, with D-000 clause 4's commit-and-push rule intact (COORD:L39–L42); the rewrite never cites anything outside the sealed tree at `<S>` (the tree measured at `<P>`, plus what `<R>` adds — the measurement artifact, the penultimate COORD heading, and that cycle's own draft, review-prompt and reviewer-verdict artifacts under `docs/coop/artifacts/` — plus the D-SEAL append) |
| R11 | **Two DR-117 lineages** (`product-boundary-successor-contract.v8` D-116 vs `preview-product-boundary-successor.v8` D-207; B3 agreed path authors v9 and "states its relationship to contract.v8") | The DR-117 page carries both until the B3 opening entry lands; if it lands before the seal, the page cites that entry's stated relationship verbatim |
| R12 | **Snapshot heading date stale** (08:L397 says 2026-08-15 while DR-104's cell is dated 2026-08-23 — contracts §5 Q7) | D-SEAL's measured snapshot supersedes; `register/readiness.md` cites D-SEAL's date and notes the archived heading date as-is |
| R13 | **Unrecorded higher versions on disk** (`gate-harness-naming.v7/v8`, `core-gate-harness-specifications.v1–v4`, `g01..g05-input-corpus.*`, `g21-fixture-corpus.v3–v6`, `g23-fixture-corpus.v1–v2`) mistaken for current | `contracts/README.md` and `gates/README.md` carry an explicit "on disk, not recorded — archive only" list (from contracts §5 Q1, gates Appendix A) |
| R14 | **Reviewer fatigue on 128+ near-identical pages** leads to rubber-stamp ACCEPTs | Pre-check automation removes form defects before dispatch; batches ≤ 8 pages; each dispatch requires the reviewer to name one concrete byte check performed per page; owner touchpoints (§4.7) |
| R15 | **Glossary invents meanings** | Every entry cites a defining source line; terms with no defining sentence in the record are listed as "used, not defined in the record" |
| R16 | **Deleting deliberation corpus** (TREE-ENDSTATE §1.1 anti-goal) | Nothing is deleted; `git mv` only; read-only rule 1 of `docs/ARCHIVE.md` (§4.4) |

---

## 8. Open questions for the owner (deduplicated from the four inventories plus this synthesis)

1. **DR-117's two lineages** — which is "the" DR-117 design candidate for the rewrite: `product-boundary-successor-contract.v8` (D-116) or `preview-product-boundary-successor.v8` (D-207)? Not in the record; B3's agreed path (v9 + opening entry) would answer it if executed before the seal. (contracts §5 Q3)
2. **Cell/COORD divergence** — confirm the rewrite carries the COORD-highest version as the candidate (v11 / v9 / v25 / actor-join v8) and shows the cell version as history. (contracts §5 Q2; decisions §5 correction)
3. **Unrecorded higher versions on disk** — archive-only, or does any (e.g. `gate-harness-naming.v7/v8`, `core-gate-harness-specifications.v4`, which the C5–C9 rationale cites for MB/G02 accounting) carry standing the rewrite must honour? (contracts §5 Q1)
4. **DR-107 / DR-122 token** — show the cell token `PROPOSED-CLOSED-FOR-REVIEW` (D-285 L15327–L15328: "Does not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`") with the candidate standing beneath it? (contracts §5 Q5) — the templates do both.
5. **D-096 deferral candidates (`CANDIDATE-NOT-RECORDED`)** — list them on DR-106/108/109/110/113/116 pages, or only the T2-02 contracts? (contracts §5 Q8)
6. **Rows with no leftover-join lineage** (DR-106, 108, 109, 110, 113, 116, 131, 133) — state "never measured" or omit the Remainder section? (contracts §5 Q6)
7. **DR-201–DR-205 provenance** — the cells are self-recording with verdict digests and no COORD entry; acceptable as archival source, or must the review-findings page cite the verdict artifacts directly (digests in contracts §3)? (contracts §5 Q9)
8. **Harness cell wording vs occupancy** — every file 08 harness cell says "not authored; not QUALIFIED" while 28 occupancies exist; the gate page shows both (cell verbatim + occupancy line). Confirm, or require an MF-6 before sealing. (gates Q1)
9. **Standing of the 43 named corpora** — "named by a recorded artifact" as sufficient to appear on gate pages? (gates Q2)
10. **Home of the DR-join-named corpora** — G09/G12 vs DR-105/DR-114. The count is settled by the bytes (§1.5c, §6.6): `doctor-actor-leftover-join.v12.json` names 13 `doctor-fc-*-input-corpus` files, 12 of them not already among the 43 (the 13th is `doctor-fc-join-input-corpus.v2`, already in the 43); `permission-leftover-join.v12.json` names 14. (gates Q3; §6.6)
11. **Fixture corpora named only by joins** (`g21-fixture-corpus.v1/v2/v7/v8`, `g23-fixture-corpus.v3/v4`) — treat fixture bytes as a separate class? (gates Q5)
12. **Uncharacterized predecessor versions** (D-233 G03 v2/v3; D-234 G04 v2; D-235 G05 v2; D-214 G15 v1–v6; D-208 G31 v1) — pages write "not in the record"; confirm no inference from review files. (gates Q6)
13. **Contract candidates as ADRs** — 49 vs 70 ADRs. (decisions §6.1; §6.3/§6.4)
14. **Transition brief** — derive from it or treat as superseded by files 02/03/04? Classified DESIGN-SOURCE (secondary); "Authority: NONE." (other-docs Q2)
15. **`docs/coop/deltas/*.delta-draft.v1.md`** (UNKNOWN) — carry as REFERENCE pointer or leave archive-only? (other-docs Q8)
16. **`freeze-payload-manifest.txt`** — retire (STALE) or regenerate at seal as part of the external `docs/archive-manifest.v1.json` (§4.3)? (other-docs Q4)
17. **Missing `06` in `docs/v2/architecture/`** — no history at any ref; the new `design/06-scope…` reuses the number; acceptable? (other-docs Q7)
18. **31 untracked `_dispatch.*.txt`** — commit before the seal? (other-docs Q6; §6.8)
19. **A4 adoption before sealing** — determines the "How to read" text for cross-lineage citations in the new register (§1.5b note; R9).
20. **A3 identity-namespace v7** — if performed before the seal (agreed: lowest priority, after the owner's decisions), the G31/DR-104 pages cite v7 rather than v6.
21. **Which of B1–B3, C1–C9, D1 are recorded before the seal** — each changes tokens/standing on the corresponding pages; the rewrite starts only after the seal, so the answer is "all that the owner chooses to do", but the packet's counts (5 DESIGN-FINAL, 52 DESIGN-CANDIDATE) will differ at sealing.
22. **Single home for the two artifacts listed in both §1.5a and §1.5c** — `component-manifest-fixture-corpus.v6` (DR-103) and `identity-namespace-negative-test-corpus.v1` (DR-104): confirm `gates/corpora/` as the home with a cross-reference from the contract page (§2, §2.1, §4.8 item 4), or invert it. (§1.5a 31/32 rule)
23. **`docs/MAP-VS-CONTROL.md`** (REFERENCE; 20200 bytes; L3 `**Status:** product boundary (guidance)`; 0 matches in file 08 and COORD) — carry as a REFERENCE pointer in the new tree or leave archive-only? (other-docs row 2)

---

## 9. Citations (record locations used in this packet)

- **file 08** (`docs/v2/architecture/08-decision-and-readiness-register.md`, sha256 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`): L12–L28 "How to use the register" and status vocabulary; L30–L45 inherited prerequisites (DR-001 L34 … DR-012 L45); L69–L91 DR-011 residual subledger; L207/L280 V2 decisions table (DR-101 L283 … DR-133 L314; DR-103 L285, DR-105 L287, DR-114 L296, DR-117 L299, DR-118 L300, DR-107 L289, DR-122 L304); L316–L324 five-review findings; L326–L368 release gate registry (DR-G01 L337 … DR-G32 L368); L370–L395 blueprint-readiness decision (condition 4 L390–L391; condition 5 L392–L393; reservation L395); L397 snapshot heading (dated 2026-08-15); L401–L404 leading-label rule; L414–L418 condition rows (condition 2 "5 of 32" L415; condition 4 "32 of 32 owners named … 29 `OPEN`, 3 `HARD-BLOCKED`" L417; condition 5 `**NOT MET**` L418).
- **COORD** (`docs/coop/COORDINATOR-DECISIONS.md`, sha256 `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466`): D-000 L20 (recording obligation L3–L4; entry format L9–L12; Decision L26–L45 (clauses 1–5 L29–L45); clause 2 L32–L35; clause 3 L36–L38; clause 4 "**Commit and push per decision**" L39–L42); D-001 L60 (§1 blockquote; pin-note L119–L122); D-002 L342; D-003 L514; D-005 L596; D-006 L698; D-007 L820; D-008 L923; D-009 L960; D-010 L984 (L1004 C-D010 amends condition-2 wording); D-011 L1024; D-012 L1050; D-013 L1150; D-014 L1296 (L1377–L1381 manifest measurement); D-015 L1201; D-018 L1415 (L1455 "Route selection is D-019 and D-020"); D-033 L1801 (clause 1 L1820–L1825; the property-pin tuple `(path, named section or selector, segment hash)` at L1823); D-035 L1603; D-038 L1744; D-042 L1954; D-054 L2361 (user-made form); D-056 L3343 (Decision L3363); D-085 L3508; D-086 L3428; D-089 L3545; D-091 L3611; D-092 L3650; D-093 L3692; D-096 L3802 (L3818 "the five preview-deferral v2 artifacts"); D-100 L3998; D-102 L3963; D-103 L4036 (Decision L4060–L4068); D-104 L4076 (L4102–L4112); D-105 L4122 (L4146–L4158); D-106 L4169 (L4202–L4213); D-107 L4224 (L4251–L4260); D-108 L4271 (L4298–L4305); D-109 L4317 (L4342–L4350); D-110 L4362 (L4396 "The candidate binds NOTHING"); D-111–D-131 as listed in §1.5a; D-132 L5554; D-133 L5621; D-134 L5674; D-135 L5711; D-136 L5748; D-137 L5779 (L5812–L5813 "D-056 Class A is not opened"; L5815–L5816 "v8 remains the D-116 leftover T2-02 candidate"); D-138 L5836; D-145 L6066; D-159 L6682; D-167 L7001; D-168 L7061 (L7092–L7093); D-169 L7113; D-175 L7432; D-207 L9062 (L9096–L9097); D-208–D-235 L9125–L11041 (all `ADOPTED 2026-08-22`); D-236 L11125; D-273 L14047; D-282 L14864; D-283 L14986; D-284 L15130; D-285 L15261 (L15327–L15328); D-286 L15387; D-287 L15495; D-288 L15624; D-289 L15746; D-290 L15841; D-291 L15938; D-292 L16035 (turn-1 Claude OBJECT L16047; "The candidate binds NOTHING" L16076–L16077). CONTESTED headings: L1490, L2469, L2640, L2733, L3738, L3772, L3870, L3901, L3932, L13963.
- **Other docs**: `docs/v2/architecture/README.md` L3–L5 status, L18–L20 "only active checklist", L44–L61 "Architecture at a glance", L63–L74 "Claim labels" (bullets L65–L71), L76–L88 "Stable terms" (rows L80–L88), L90–L95 "Directory boundary" (reservation sentence L94); `docs/README.md` L10 (A→I plan link), L13 (claim-register pointer); `docs/coop/TREE-ENDSTATE.md` §1.1 anti-goals (L30–L32), §2.2 rename (L46–L54), §5.5 "Graduate conclusions" (L230), §6 front-door README (L234–L263), §7.1–§7.2 migration timing and steps (L267–L289); `docs/coop/GORTEX-BORROW-REGISTER.md` L4; `docs/coop/architecture/01-product-boundary.md` L3; `docs/coop/architecture/11-traceability.md` L7–L8, L175; `docs/OPENSIP-DISTRIBUTION-AND-COMPONENT-TRANSITION-BRIEF.md` L3–L5; `docs/coop/deltas/gortex-borrow-triage.delta-draft.v1.md` L3 and `docs/coop/deltas/gortex-graph-lanes.delta-draft.v1.md` L3 (two different sentences — quoted separately in §1.4).
- **Artifacts** (sha256 recomputed by the inventories at HEAD `4abb961`, and by this packet for the five `deferral.*.preview.v2.json` prefixes and `claim-register.v1.json` `767dc210d4fa8b6d…`): every digest in §1.5a–c.
- **Inventories and their verifier findings**: `DECISION-PACKETS/F-inventory-contracts.md` (§0, §1–§4c, §5 Q1–Q9); `F-inventory-gates.md` (Rules 1–7, Summary, Table 1, Table 2 per gate, Appendix A/B, open questions 1–7); `F-inventory-decisions.md` (§1, §2 rows 1–277, §3, §4, §5, §5b, §6, §7); `F-inventory-other-docs.md` (§0–§6). Verifier findings as quoted in the dispatch (applied in §0.2).
- **Owner decision files**: `DECISIONS-NEEDED.md` (F1 text; A3, A4, E1, E2, E4 notes); `DECISIONS-RECOMMENDED.md` (all items AGREED; F1 NOT STARTED); `PROPOSAL.cross-citation-convention.md` (draft D-293 Decision 1–5); `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md`.
- **Git / disk measurements made here**: `git rev-parse HEAD` = `4abb961aad98525ca8b992a24609a6286964a451`; `git status --porcelain | wc -l` = 36 (1 modified + 35 untracked, of which 31 under `docs/coop/artifacts/_dispatch.*`); `ls docs/coop/artifacts/*.json | wc -l` = 3205 (top level; the inventory's 3411 counts `fixtures/` recursively); 353 `harness.DR-G*` files; 262 non-review `*leftover-join*` files; 1338 `review-independent`, 1093 `review-prompt`, 368 `coordinator-decisions.D-*draft` files; `check-versioning.py` + `-v5…-v14` = 11 files; `shasum -a 256` of cleansheet-a/c `decisions.json` = `f813693cc910581d…`, `5949bb3c6c944581…`.
