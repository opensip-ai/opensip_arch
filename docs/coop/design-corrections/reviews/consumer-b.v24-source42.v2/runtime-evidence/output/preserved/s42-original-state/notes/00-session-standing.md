# Session standing — consumer-b.v24, runtime consumer-b.v24-source42.v1

- **Origin.** 9d3dfb70-b2d3-498c-a3c1-f8de9e488514, continued in a new runtime. Independence is not claimed anew. No subagents, other consumers, coauthors, LIVE, author models, fixtures, reports, root results or other runtimes are read. Harness files (`launch.py`, `prompt.md`, `preparation.json`, `process.json`, `public-events.jsonl`) are not read.
- **Inputs.**
  - The kit is this runtime's `subject/`: `consumer-input-manifest.json` SHA-256 `9c90a1e849b1a33fb1aec507d6a4f59632fc3497922c99de847e4802fb89db05`, 104 members; parent frozen manifest `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307`.
  - Also read: `charter.md`, `requirements.json` (both identical to source41 apart from runtime paths and kit hashes), the installed standard library and jsonschema, and my own old and new outputs.
- **Kit delta against my own source41 custody rows (orientation only).** Two documents changed: `foundation/enumeration-contract.v1.md` and `foundation/execution-inputs-contract.v1.md`. Both were read in full.
- **Scope.** Unchanged: 123 requirements, 8 standing rules, 3 future qualification items. No design acceptance or expected result is supplied, and none is implied.
- **Own history, read-only.**
  - consumer-b.v24; source39.v1–v3.
  - source41.v1: copied non-store files plus a full hash manifest at `preserved/source41-v1/` (its verdict was ACCEPT-RECONSTRUCTABLE on the source41 kit; root admission unobserved).
  - None of it establishes source42 conformance.
- **Helper provenance.**
  - My source41 `*.py` were ported with only the runtime root rebound (`port-manifest.json`).
  - The unchanged port is executed against source42 first (logs `s42-original*`) and the output tree is preserved before any correction.
  - Every later code change is a numbered helper correction (HC-47 onward; HC-1..HC-46 remain history), with its kit selector, the original measured behaviour and the re-executed result.
- **Execution.** Every script runs as `/tmp/opensip-architecture-review-env/bin/python -I -B` through `tools/seq.py`, with retained logs; the shell prefix is `python3` only. Reused prior measurements are labelled and never counted as source42 execution.
- **Boundaries.** Write only this runtime's `output/`. No product, commit or push, activation or root acceptance. A verdict is written only after every subprocess has finished and every charter condition has been evaluated.
