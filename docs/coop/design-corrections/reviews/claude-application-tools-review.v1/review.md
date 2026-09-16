Bounded review complete. `review.md` and `review.json` are written; probe sources and results are under `scratch/`.

## Verdict: CHANGES_REQUIRED — tooling review only, never an application ACCEPT

**Custody verified.** Manifest SHA256 matches `e25995b7…f32a`; all 19 input files verified byte-exact (SHA256 and byte length), no extras, none missing, all read completely. `check-retain-public.v2.report.json` treated strictly as historical evidence — I re-derived equivalent coverage independently rather than trusting its counts.

**What holds up.** Bind refused all 24 boundary cases I put to it, including each of the four excluded Claude author origins in *both* design and blind roles. The finalizer passed its shipped selftest 20/20 against the frozen bytes plus 7 extra before-image cases I added, all refusing with zero writes; activation is written last and never replaced. Source-pin adaptation admits exactly one opening paragraph with the inherited body byte-preserved (8/8). Staged grades stay conditioned on activation; 32 gates keep all authority flags false; condition 5 NOT MET throughout.

**Four MAJOR findings**, all in the stages *after* binding:

- **F1** — `retain-…successor.v1.py:87` uses `KNOWN_GROK_COAUTHOR_SESSIONS`, not the union. The four Claude author origins are retained as the **final application review** — and since the finalizer does no origin check at all, that line is the only origin guard on the review that authorizes activation. Executed reproducer.
- **F2** — coauthor-standing and `--resume` refusal sit inside the grok branch; the claude path has neither. Executed reproducer.
- **F4** — `verify-applied.py` reimplements the subject-digest selector and diverges in 4 of 8 shapes; an `inputKit.parentSubjectSha256` design review binds and assembles, then fails verification *after* activation.
- **F5** — the assembler consumes the Codex design assent by path and never compares its bound digest, though it compares all four other bound artefacts. AST-confirmed; static only, no end-to-end reproducer claimed.

Each has a one-to-two-line remedy. I did not modify any reviewed input.

**Two things to flag directly.** Six inputs could not be run end-to-end — they need the full successor root, which isn't among the inputs — so F5–F8 are static and labelled as such; F3 is latent (synthetic envelope, real CLI shape unverified). And I introduced one side effect: in-process imports under host `python3` without `-B` created `inputs/__pycache__`. No manifest-listed file was altered; I removed it and re-verified `inputs/` holds exactly the 19 files. Both are disclosed in the outputs.
