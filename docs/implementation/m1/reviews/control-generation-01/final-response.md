**Verdict: ACCEPT-UNIT** for carriers and shape only, with no required findings and 5 advisories. It is not integration, and not M1, product or release qualification. The review is in `m1-control-generation-review-01/review.json` and `review.md`, and my probe scripts and results are under `work/`.

**One mistake to flag first:** my naming scan loaded the frozen `prepare.py` without `-B`, which wrote `tools/contracts/__pycache__/prepare.cpython-314.pyc` into the read-only subject. The after-check caught it. Its timestamp matched my scan to the second, so I deleted only that file and its empty folder. The subject is back to exactly 88/88 files with matching hashes and no extras, and the manifest SHA is still `c4d3c10d…`. The review's limits section records this.

**What I reproduced:**
- **What changed:** only the claimed files differ from adapter04. The Rust modules for the other roots differ only in their two header hash lines, and `report.ts` keeps all 28 earlier embedded schemas byte-for-byte and adds `control.v3` exactly.
- **Source:** `control.v3` matches the architecture schema byte-for-byte. All 29 rows agree across source-map, registry and options, with 587 roots, 14 provider roots, and no duplicate type names or namespaces.
- **Naming transform:** across all 587 definitions it changes only `Control3Root`, adding 16 unique titles that clash with nothing. My scan for Typify name collisions finds 1 without the transform and 0 with it.
- **Generation and builds:** fresh generation shows 8 outputs and no drift. All 78 tests, Clippy with `-D warnings`, and strict `tsc` on both TS outputs pass.
- **Corpus:** rerunning the corpus builder gave byte-identical files (194 cases: 79 positive, 115 negative).
- **TS:** 0 mismatches against my Python reference over the 194 corpus cases plus 858 new cases. The new cases cover all 21 UTF‑8 sites at 1–4 bytes per character at and past each limit, integer bounds for all 16 variants, all 240 cross-variant body swaps, and 14 malformed frames. A zero bound works, lone surrogates are refused, and malformed bounds are refused.
- **Rust:** all 79 positive frames across the 16 variants roundtrip exactly. No schema-valid case is rejected, and all 232 invalid body swaps are rejected, so bodies are no longer mixed up. Integer and optional-field handling loses nothing.
- **Old witnesses:** 1338 of 1343 pass on the new TS runtime. The other 5 are the three deliberately excluded refs, which matches review 04.
- **Live source preflight:** the binding4 checker refuses the subject ("generation source is not selected by accepted design"). With only the control row removed it passes, and adapter04 passes too.

**Advisories:**
1. **Missing preflight receipt:** the validation `source-preflight.json` is empty, so I produced the refusal evidence myself. The subject's own `verify_design.py` has no source preflight and passes. Integration must use the binding4 checker and promote the exact raw schema through a reviewed unit, without weakening the checker.
2. **Narrow naming fix:** it only covers object-typed properties directly under a top-level `oneOf`. Enums, constrained strings, arrays or nested unions in a future schema could collide the same way. Adding a check in `prepare.py` that refuses any remaining collision would close this.
3. **No in-tree tests:** nothing in the tree tests the collision fix or the new UTF‑8 keyword.
4. **Loose Rust carrier:** it accepts many schema-invalid cases, by design. `Control3Root` must not be treated as admission, and the declared owner `control_protocol.rs` doesn't exist yet.
5. **Stale metadata and untracked route:** `openObligations` still lists control owner selection, and `control-source-route.v1.json` is untracked in the architecture repo.

**Not covered:** framing, state, sequence, permission and effects semantics; adapter04's confinement and dependency algorithms, which this change doesn't touch; native IDL; and the final report owner. My collision scan is a heuristic, not a proof.
