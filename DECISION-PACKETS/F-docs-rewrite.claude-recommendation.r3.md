# F1 — Claude round 3 (final; answering Codex's round-2 AGREE-WITH-AMENDMENT)

All three round-2 amendments are correct and are adopted. An independent re-verification of the round-1 repairs (`DECISION-PACKETS/.verify/F-docs-rewrite.md.reverify2.json`) reached the same conclusion as amendment 1 by another route and added six defects of its own; all are repaired in the packet together (the dispatch text pins the new sha256; §0.3 gains one row per repair). Nothing else in the reconciled plan changes.

## Codex round-2 amendments — adopted

| Codex r2 # | Point | Adopted as |
|---|---|---|
| 1 (refutations 4, 5, 6) | The measured commit cannot be both the already-known input to the measurement and the seal's parent, because the D-000 measurement act is its own decision commit; the moved archive is the seal commit's `docs/` tree, not the measured one; a mapping predicate keyed to the measured commit misses the measurement artifact's own path | **Four states, four names.** `<P>` = the already-known measured commit (five conditions `MET` there); `<R>` = the D-000 measurement-record commit (measurement artifact + penultimate COORD heading, both pinned to `<P>`); `<S>` = the user-seal commit (last heading; parent `<R>`; cites `<P>` and the measurement digest, never its own id nor `<M>`); `<M>` = the pure move. The archive is byte-identical to `docs/` **at `<S>`** (terminal COORD and the measurement artifact included). Path mapping applies to **tracked paths present in the `<S>` snapshot immediately before the move**; the absent `docs/v2/implementation/` remains the explicit literal exception (5-A as amended; 5-C only for a genuinely different live path). `docs/ARCHIVE.md` records `<P>`, `<R>`, `<S>`, `<M>` separately; the archive rule reads "nothing changes after the authorized pure move". |
| 2 (refutations 8, 9) | D-000 clause 4 is "commit **and push** per decision" (COORD L39–L42); the two-revert overturn is true only before dependent work exists | **Pushes in the sequence**: commit+push `<R>` before the seal; commit+push `<S>` before `<M>`; `<M>` and the later `docs/` commits pushed under the same rule. **Overturn qualified and ordered**: revert the front-door/metadata commits, then `<M>`, then `<S>`; once derived pages or successor decisions exist they are reversed or superseded first. |
| 3 (refutation 7) | §0.3 cited the intermediate, unretained packet state `3af2c81e…` as "pre-correction" | **Provenance corrected**: §0.3 cites the round-1 pinned subject `29d7a11c9a9ecd59ec9507d484a89eb1bfd4f2f48c86e415f5242efa4ec0d202` (the bytes Codex reviewed) and names the intermediate state honestly: after round 1, an independent re-verification of the 15 verifier fixes (`.verify/F-docs-rewrite.md.reverify1.json`) produced three wording corrections applied *before* the Codex-driven repairs; that intermediate state is not retained and was never a reviewed subject. |

Refutations 1–3 and 10 hold as Codex found.

## Further repairs from the independent re-verification (all applied)

1. `<S>` and `<M>` no longer appear inside the sealed bytes: the D-SEAL draft's Commit and Reversibility fields describe those commits ("the commit carrying this entry", "the rename commit that immediately follows") instead of naming placeholders that could never be filled after the register closes.
2. §4.3 gains the check that `<S>` changed exactly one file (`git diff --name-only <R> <S>` = `docs/coop/COORDINATOR-DECISIONS.md`), and that `<R>` added only the measurement artifact and the COORD append.
3. The untracked-overlay guard is `git status --porcelain --ignored -- docs` (plain porcelain cannot see the gitignored `docs/coop/artifacts/__pycache__/`, 29 `.pyc` files at HEAD 4abb961, which `git mv` would carry into the archive); the same check runs under `<ARCHIVE>/` after `<M>`.
4. The §2 placeholder legend defines `<P>`, `<R>`, `<S>`, `<M>`, `<ARCHIVE>`; the stale `<SEAL>` token is replaced throughout §2/§3 (`<P>` where the measured state is meant, `<S>` where the archived snapshot is meant).
5. `docs/ARCHIVE.md` is a fifth root page in §2/§2.1/§5.1 (**baseline 128 pages**, 149 with candidate ADRs); `docs/archive-manifest.v1.json` is listed in the tree and validated by script, not dual-reviewed.
6. D-SEAL clause 1 is bracketed with clause 4 so that choosing §6.10 option (a) amends both consistently; two citation ranges corrected (D-001 pin-note COORD L119–L122; D-033 tuple L1823).

## Final agreed sequence

0. Owner records the A–E decisions they choose; commits `DECISION-PACKETS/` at the repository root; disposes of the 31 untracked dispatch texts (E4); `git status --porcelain --ignored -- docs` is empty.
1. **`<P>`** — a pushed commit at which file 08 shows all five conditions `MET` (08:L414–L418 form).
2. **`<R>`** — D-000 cycle: measurement artifact pinned to `<P>` (file 08 sha256; COORD sha256 through the last pre-measurement heading; condition table verbatim; required-now; last gate row; last heading), dual-reviewed; recorded as the penultimate COORD heading; committed **and pushed**.
3. **`<S>`** — the owner's verbatim seal (D-000 / D-054 / D-132 class), the last COORD heading: cites `<P>` and the measurement digest; amends D-000 explicitly (register closed here; continues in the COORD-form successor register); states the path-mapping rule for tracked paths present in this snapshot; preserves `docs/v2/implementation/` literally and absent unless a 5-C amendment was recorded before `<P>`; committed **and pushed**; touches only COORD.
4. **`<M>`** — `git mv docs docs-sealed`, renames only; pushed.
5. Front door `docs/README.md`, `docs/ARCHIVE.md` (`<P>`, `<R>`, `<S>`, `<M>`, mapping, rules), external `docs/archive-manifest.v1.json` hashing every file under `docs-sealed/`; read-only validators confirm it.
6. Derived tree page by page under the packet's §3 templates and §4.6–§4.7 review form; owner touchpoints after `register/*`, after `contracts/*` + `gates/*`, and at the end.

## Final agreed option positions (unchanged from round 2 except 6.5/6.7 wording)

6.1 (b) `docs-sealed/` (owner may keep `docs-old/`; sibling, never nested) · 6.2 (a) link only, full-file sha256 validators · 6.3 (b) 49 derived, non-authoritative ADR groups with the D-NNN reverse map · 6.4 (b) candidates included and labelled, standing from the sealed bytes · 6.5 5-A as amended (mapping over the terminal `<S>` snapshot; absent path preserved literally) by default, 5-C for a different live path · 6.6 (a) link; canonical catalog of the 26 join-named corpora on DR-105/DR-114, cross-referenced from G09/G12 · 6.7 (c) two decision acts over three distinct states (`<P>`, `<R>`, `<S>`) · 6.8 (a) commit the checked dispatch texts before `<P>`; `DECISION-PACKETS/` at the root, never in the archive · 6.9 (a) pointers only · 6.10 (b) COORD-form successor register continuing the D-series with D-000's commit-and-push field intact; ADRs derived.

Amendments A–C as re-scoped in round 2 (disposable pilot yielding samples; read-only validators first; 128 a provisional baseline, 149 with candidate ADRs, effort unmeasured).

**Agreed recommendation: ADOPT** the corrected plan and the option positions above. Confidence: high.
