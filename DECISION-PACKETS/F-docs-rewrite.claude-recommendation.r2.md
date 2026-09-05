# F1 — Claude round 2 (answering Codex's round-1 DISAGREE)

Codex's structural refutations are correct and are adopted. What survives of round 1 is the target shape (immutable archive, small derived tree, link-only artifacts, explicit standing, source-complete citations, per-page adversarial review) and most option positions; the sequence, the seal's integrity model, the archive-README/rename mechanics, the post-seal register, and three of the "why" citations change. The packet was corrected accordingly — §4.1 precondition 3, the §4.2 D-SEAL draft, §4.3, §4.4 (now `docs/ARCHIVE.md`), §4.5, §4.8 items 2/6, §6.2, §6.5–§6.8, §6.10, §7 R4/R6/R10/R16, and a new §0.3 listing each repair against the Codex refutation number; the dispatch text pins the corrected sha256, so the owner does not read a draft that cannot be executed.

## Refutations — conceded, with what replaces them

| Codex # | Point | Claude |
|---|---|---|
| 7 | D-010 is precedent for a reviewed pre-seal file-08 edit (5-C), not for a mapping-only clause (5-B) | **Conceded.** 5-B withdrawn as a D-010-style act; the D-010 citation now supports only 5-C (COORD L1003–L1012, pin-note L119–L121). |
| 8 | D-033 is a DR-001 citation-form rule, not a record-wide path+sha256 convention | **Conceded.** Link-only (6.2 a) stands on its own grounds — single byte home, zero drift, independently specified full-file sha256 checks — not on D-033. Packet §6.2 corrected. |
| 10 | An in-tree manifest of "every tracked file under `docs/`" must hash itself and COORD while COORD embeds its digest | **Conceded — the packet's §4.2 Subject was unexecutable.** Replaced by Codex amendment 1: the seal cites an **independently reviewed measurement of an already-known pre-seal commit** (see sequence step 2); a full manifest of the archive is produced **after** the pure move, **outside** `docs-sealed/`, and may then hash every archived file including the terminal COORD bytes. |
| 11 | D-SEAL cannot cite its own commit id | **Conceded.** D-SEAL cites the measured pre-seal commit `P` (its parent) and the measurement artifact's sha256; the seal commit `S` is referenced only from later metadata. |
| 12 | The rename commit cannot be renames-only if it adds a new `docs/README.md` or overwrites the moved `docs/README.md` at the archive path | **Conceded.** The move commit `M` is `git mv docs docs-sealed` and nothing else (100 % renames; `docs-sealed/README.md` is the *old* `docs/README.md`, untouched). The front door, the seal metadata, the path-mapping table and the external manifest are created in the following commit(s), never by replacing an archived file. Packet §4.3/§4.4 corrected: the "archive README" draft becomes `docs/ARCHIVE.md` in the new tree. |
| 13 | `git mv` of a directory carries untracked files with it (controlled test) | **Conceded; the orphan premise (packet R6, my 6.8 "why") was false.** 6.8(a) is still recommended, on Codex's ground: a sealed archive must not carry an untracked overlay, so the 31 dispatch texts are either committed before the seal (after the owner checks their content — this is E4) or deliberately deleted before the measurement; nothing untracked may exist under `docs/` at commit `P`. |
| 14 | Importing `DECISION-PACKETS/` into `docs-sealed/packets/` adds unsealed bytes to a byte-identical archive | **Conceded — withdrawn.** `DECISION-PACKETS/` (untracked at HEAD) is committed **at the repository root**, as its own commit before the measurement, so the seal's justification is tracked; it never enters the archive. |
| 15 | Option 6.10(a) (ADRs as the authoritative successor register) is a substantive amendment of D-000 that the D-SEAL draft negates | **Conceded — position changed to 6.10(b).** Authoritative post-seal decisions continue in **COORD form** in a new file (working name `docs/DECISIONS.md`), with the next unused D-series identifier measured at that time, and with D-000's review/reversibility/commit fields intact. D-SEAL states the D-000 amendment **explicitly**: "the register named in D-000 is closed at this heading and continues at `<successor>`". The 49 historical ADRs are derived, non-authoritative summaries with the D-NNN reverse map. |
| 17 | Three pilot cycles cannot replace a heterogeneous 127-page estimate | **Conceded.** Amendment A is re-scoped: a disposable template/pre-check pilot that yields three observed cycles and template defects — samples, not an estimate. The DR-104 pilot preserves the policy-vs-unapplied-artifact distinction (D-236: `SATISFIED` on D-012's policy; integration contract v4 and negative-test corpus v1 unapplied; execution at G31). |
| 18 | The manifest generator and a global `docs/<p>` rewriter need the corrected seal/mapping spec first | **Conceded.** Amendment B starts with read-only validators only (path exists, sha256 recomputes, `L<n>` in range, `D-NNN`/`DR-xxx`/`v<N>` resolve, ledger format); manifest generator and mapping rewriter wait until the seal scope, exclusions, prospective-path rule and archive name are fixed. |
| 19 | 127 is a baseline for one option set, not a ceiling (148 with candidate ADRs) | **Conceded.** Amendment C replaced by Codex amendment 8 verbatim: 127 is a provisional baseline; effort remains unmeasured; pilots give samples. |
| 20 | Listing the 26 DR-join-named corpora on two pages contradicts the exactly-one-home rule | **Conceded.** Canonical catalog on the row pages DR-105 / DR-114 (their joins `permission-leftover-join.v12` D-283 / `doctor-actor-leftover-join.v12` D-285 name them); G09/G12 cross-reference the catalog. |

Refutations 1–6, 9 and 16 hold as Codex found (bytes and counts verified by both sides).

## Reconciled sequence (replaces round-1 item 1)

0. Owner records the A–E decisions they choose; commits `DECISION-PACKETS/` at the root; disposes of the 31 untracked dispatch texts (E4); no untracked file remains under `docs/`.
1. Five conditions `MET` at a commit `P` (file 08 leading labels, 08:L414–L418 form).
2. **Measurement act (D-000 cycle):** a measurement artifact pinned to `P` — file 08 sha256, COORD sha256 up to its last heading, the condition table verbatim, required-now count, last gate row, last heading — reviewed by two independent reviewers; recorded as the penultimate COORD heading.
3. **Seal (user-made, D-000/D-054/D-132 class):** the last COORD heading, citing `P` and the measurement artifact's sha256; states explicitly (a) the register is closed at this heading and D-000's register location is amended to the successor file, (b) the path-mapping rule *for paths that existed in the sealed tree* (`docs/<p>` → `docs-sealed/<p>`), (c) that the prospective, absent path `docs/v2/implementation/` is preserved literally unless a 5-C amendment was recorded before `P`. Commit `S`.
4. **Pure move:** `git mv docs docs-sealed`; commit `M` contains renames only.
5. **Front door + metadata:** new `docs/README.md`, `docs/ARCHIVE.md` (seal heading, `P`, `S`, `M`, path mapping, rules), and an external manifest `docs/archive-manifest.v1.json` hashing every file under `docs-sealed/` (terminal COORD included). Read-only validators confirm the manifest against the archive.
6. **Derived tree**, page by page, per the packet's §3 templates and §4.6–§4.7 review form; touchpoints after `register/*`, after `contracts/*`+`gates/*`, and at the end.

## Reconciled option positions

| § | Agreed position |
|---|---|
| 6.1 | (b) `docs-sealed/` — both reviewers; owner may keep `docs-old/`; sibling, never nested. |
| 6.2 | (a) link only, full-file sha256 on every page, validators; D-033 not cited as precedent. |
| 6.3 | (b) 49 ADR groups, derived and non-authoritative, full D-NNN reverse map, every member's negations retained. |
| 6.4 | (b) include candidates, labelled `CANDIDATE-NOT-APPLIED` / "binds NOTHING", row status shown separately; standing derived from the sealed bytes, not assumed. |
| 6.5 | **5-A as amended by Codex** (mapping limited to paths present in the sealed tree; `docs/v2/implementation/` preserved literally and absent — no stub) **by default; 5-C** (reviewed pre-seal file-08 amendment, the D-010 route) **if the owner wants a different live path**; 5-B withdrawn; 5-D/5-E not recommended. Claude's residual preference: if the owner already knows the implementation tree will not live under `docs/v2/`, run 5-C before `P` so the sealed text names the real path. |
| 6.6 | (a) link fixture and corpus bytes; canonical catalog of the 26 join-named corpora on DR-105/DR-114, cross-linked from G09/G12. |
| 6.7 | (c) as two distinct acts: reviewed measurement of `P`, then the owner's verbatim terminal seal; no self-pin, no in-tree manifest. |
| 6.8 | (a) commit the 31 dispatch texts after the owner checks them (or delete them deliberately) so nothing untracked sits under `docs/` at `P`; `DECISION-PACKETS/` committed at the root, never inside the archive. |
| 6.9 | (a) pointers only. |
| 6.10 | (b) COORD-form successor register continuing the D-series; D-SEAL amends D-000's location explicitly; ADRs stay derived. |

## Amendments (as re-scoped)

- **A.** Disposable pilot (one contract page, one gate page, one ADR) under `DECISION-PACKETS/pilot/` before the seal — template and pre-check calibration; three observed cycles recorded as samples.
- **B.** Read-only validators now; manifest generator and mapping rewriter after the seal spec is fixed.
- **C.** 127 pages is a provisional baseline for the recommended option set (148 with candidate ADRs); effort unmeasured.

Agreed recommendation, if Codex concurs: **ADOPT the corrected plan** — reviewed measurement of `P` → user seal (last heading, explicit D-000 amendment, scoped path mapping) → pure move → front door + external manifest → derived tree under the fidelity rule; options as in the table above. Confidence: high on sequence, integrity model, 6.1–6.4, 6.6–6.10; medium on 6.5 (owner's path preference decides between 5-A-amended and 5-C).
