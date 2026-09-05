# Orchestrator tooling (D-000 acts), copied from the Claude orchestrator's session scratchpad on 2026-08-28

These scripts drove D-282 through D-294 and the in-flight D-295. They are working tools, not record
artifacts: nothing under `tools/` is cited by COORD or file 08, and nothing here binds anything.

## Path convention (read first)

Every script carries a hard-coded scratch directory constant
`SCR` / `S` = `/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-…/scratchpad/`
(the previous session's scratchpad, which no longer exists). Before use, copy the directory to your own
scratch location and rewrite that constant, e.g.

```sh
cp -R tools/orchestrator /tmp/orch && cd /tmp/orch
grep -rl 'dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad' . | xargs sed -i '' 's#/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad#/tmp/orch/scratch#g'
mkdir -p /tmp/orch/scratch
```

All scripts `os.chdir` to the repo root and read/write `docs/coop/artifacts/` only in their freeze /
stageb / entry modes; drafts and dry runs go to the scratch directory.

## Leftover-join acts — `act.py` + `act-configs/act.<lineage>.json`

`python3 act.py act.<lineage>.json draft|stageb|entry [--apply]` with `TURN=<n>` in the environment.
`draft` prints the Stage B COORD draft; `stageb` freezes the draft (0444), the review prompt and the
`_dispatch.<D>.txt` text into `docs/coop/artifacts/`; `entry` builds (and with `--apply` appends) the
condensed ADOPTED entry after both Stage B reviews are CONSENT 0/0, and writes `commit-files.<D>.txt`.
Successor generators for the joins recorded at D-288..D-292 (`make-g09-v12.py` …) show the transform
pattern: read the frozen predecessor, rewrite (never string-patch) speaker sentences, re-pin at run time,
audit for `[Tt]his v\d`, bare `v\d+`, `{…}` tokens and "unchanged" claims.

## Convention act (D-294) — `make-convention.py`, `make-D294-entry.py`, `record-D294.sh`

`TURN=<n> python3 make-convention.py [--freeze]` computes every citation pair from bytes and writes the
draft; `--freeze` writes draft + prompt + dispatch. `NEW_OVERRIDE=D-NNN` sets the number when COORD is
ahead of HEAD. Recorded at `f345657`.

## DR-117 successor (in flight, D-295) — `ppbs/`

`make-ppbs-v10.py [out]` regenerates `preview-product-boundary-successor.v10.json` (re-pins HEAD, file 08,
COORD, all digests; verifies the twelve current joins; asserts the fourteen classes equal v8's after
normalizing the 42 refreshed sites). `freeze-ppbs.py <V>` freezes the artifact + Stage A prompt +
dispatch. `TURN=<n> PPBS_V=10 python3 make-D295.py draft|stageb|entry [--apply]` for Stage B and the
ADOPTED entry (`LANDS="…"` env adds the landed-identifier sentence to the Protocol line).
`../record-act.sh D-295 <turn> ppbs/make-D295.py "<commit subject>" ../commit-body.D-295.txt` freezes the
reviews, appends, commits only the act's files (never `_dispatch.*`), and pushes.

## Recommendation phase — `compile-recommendations.py`, `dispatch-F1.sh`

Compiles `DECISIONS-RECOMMENDED.md` from `DECISION-PACKETS/` round files; `dispatch-F1.sh <pane> <round>`
shows the Codex dispatch form used for the recommendation reviews.

## Reviewer dispatch (Herdr)

Claude reviewer: a fresh `claude` pane per review (`herdr tab create --workspace wD --no-focus`, rename,
`herdr pane run <pane> claude`, wait idle, `herdr pane run <pane> "$(cat docs/coop/artifacts/_dispatch.<act>.txt)"`,
`send-keys Enter` if not `working` within 30 s; wait with `herdr wait agent-status <pane> --status done
--timeout 590000`, re-issued after the cap). Codex reviewer: a `codex --yolo` pane in `wC`
(`/status` shows context left; open a new pane below ~20%). Close Claude tabs after their review file
is frozen (chmod 0444).
