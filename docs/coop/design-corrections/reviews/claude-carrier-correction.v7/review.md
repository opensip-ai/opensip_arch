v7 is complete and frozen. Full documented sequence reproduces end to end, all green.

## Corrected selected files (9, at stable repo-relative paths)

| file | v6 → v7 sha256[:16] |
|---|---|
| `docs/v2/architecture/attempt-custody.schema.v1.json` | `c7e22e9e…` → `37f1445c573a31be` (moved from flat path) |
| `docs/v2/architecture/carrier-fault-cases.v1.json` | `475a9233…` → `d510662ce455b851` (moved) |
| `docs/v2/architecture/commit-recovery-readonly.v3.md` | `c6009030…` → `a60b048c82db55e6` |
| `…/security/carrier-dispatch.v3.json` | `00c31e17…` → `e3ce0d5f6172cead` |
| `…/security/carrier-format.v3.md` | `e58676b5…` → `ecbe4362332f67a2` |
| `…/security/carrier-migration.v1.md` | `dcfdc509…` → `227fb89c7159700f` |
| `…/security/check-carrier-v3.py` | `464aa4e4…` → `137f5cb77eaf9859` |
| `…/security/carrier-highwater.schema.v1.json`, `grant-journal.carrier.v3.sql` | unchanged |

Patches: 2 owner files + 2 planning inputs in `scratch/patches/`; both owner before-digests match the frozen manifest, F32 preserved.

## Executed results (over these bytes)

`C4b 87/0` · `C10 95/0` · `C17 73/0` · `C18 20/0` · `C12 42/0` · `C13 50/0` · `C14 57/0` · `C15 7/0` (v5 act B left `["carrier_format"]`, corrected leaves `[]`) · `C16 22/0` · `C6 78 653 schedules / 0 violations` · `C7 132 / 0` · `C19 20 drifts, 20 detected, 19 clean`.

The strict check is proven able to fail: it rejects the v6 attempt-custody bytes with `DUPLICATE KEY: admitted`. **The v6 control results do not cover these bytes and are not reused** — v6 passed *because* `json.load` is last-wins.

## What my new checks found in my own work

1. **A real law-deferral leak**: carrier-migration §6 said the PS-01 lineage allocation "is in `owner-correction.v3`" — exactly the dependency finding 6 prohibits. Fixed to cite the stable owner path; C19's new **N20** reintroduces the original sentence and the validator rejects it.
2. **A misplaced lookup in my own new check**: I asserted `detectionIsKeyedOnTheFormatRow` under `openDispatch`; it lives under `migration`. Corrected, and the two orders now cross-check.

## Remaining limitations (admitted, not closed)

- Nothing here is a qualification gate; all sixteen F38–F53 are `not-executed`.
- The no-run-directory-for-LAW scan uses a **lexical** evidence-vs-law classifier. It caught the real leak above, but a deferral phrased as an ordinary evidence citation would pass it.
- C18 drives in-memory SQLite; it says nothing about a real file under a concurrent foreign writer.
- Act B atomicity is in-memory transaction behaviour only — no fsync, `F_FULLFSYNC` or real crashes.
- C6 interleaves a model, not OS processes; F42 remains unmodelled.
- The settlement sweep is specified with a reference-executed decision matrix; its execution remains.
- `prev_sha256` byte compatibility with a real format 1/2 instance is unestablished — no such fixture exists in the corpus.
- F00–F37, final sourcepins, normativekit and integrated checks are root-owned and untouched.

Standing: **NOT-SELF-ACCEPTED**. Frozen at `scratch/output-manifest.json`; narrative in `scratch/REPORT.md`; commands in `scratch/REPRODUCE.md`.
