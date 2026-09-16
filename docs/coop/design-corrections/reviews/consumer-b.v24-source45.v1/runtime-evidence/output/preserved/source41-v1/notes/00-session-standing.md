# Session standing — consumer-b.v24, runtime consumer-b.v24-source41.v1

- **Origin.** 9d3dfb70-b2d3-498c-a3c1-f8de9e488514. This runtime continues that same blind origin; independence is not claimed anew. No subagents, other consumers, coauthors, LIVE, author models, fixtures, reports, root results or other runtimes are read.
- **Inputs.**
  - The kit is this runtime's `subject/`: `consumer-input-manifest.json` SHA-256 `31369cc8c3b71e559c50f107104daff4d6d428e20fb75dc1e3914a2acc1ec6dd`, 104 members; parent frozen manifest `eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236`.
  - Also read: `charter.md`, `requirements.json`, the installed standard library and jsonschema, and my own old and new outputs.
- **Scope.** Unchanged: 123 requirements, 8 standing rules, 3 future qualification items. No design acceptance or expected result is supplied, and none is implied.
- **Own history, read-only.**
  - consumer-b.v24: hash manifest at `preserved/consumer-b.v24-output.manifest.json`.
  - source39.v1, v2 and v3: copied non-store files and a full hash manifest at `preserved/source39-v3/` (v3 verdict CHANGES_REQUIRED, MUST s39-M1).
  - None of it establishes source41 conformance.
- **Helper provenance.**
  - My own source39.v3 `*.py` were ported with only the runtime root rebound (`port-manifest.json`).
  - The unchanged port was executed against source41 first: logs `s41-original.*`, `s41-original-mut.*`, `s41-original-disc.*`. The whole output tree was then preserved byte-for-byte at `preserved/s41-original-state/`, before any correction.
  - That unchanged state is re-executable at `preserved/pre-s41/` (`tools/make_pre_s41.py`, root rebinding only).
  - Every later code change is a numbered helper correction (HC-39 onward; HC-1..HC-38 remain history). Each names its source41 selector, the original measured behaviour and the re-executed result: `tools/hc_source41.py`, `notes/01-source41-law-deltas.md`.
- **Execution.**
  - Every script runs as `/tmp/opensip-architecture-review-env/bin/python -I -B` through `tools/seq.py`, with complete retained logs under `logs/`. The shell prefix is `python3` only.
  - Current-source claims are re-executed. A reused prior measurement is labelled as such and is never counted as source41 execution.
- **Boundaries.** Write only this runtime's `output/`. No product, commit or push, activation or root acceptance. A verdict is written only after every subprocess has finished and every charter condition has been evaluated.
