# Independent bounded review — marker routes 167 (reference, prose + machine-readable observation)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: received as a chat message; subject README read. Scope: the delta of frozen
`marker-routes-reference-checkpoint-167` over frozen 165 — one contract table row plus one reconciling paragraph, one
§8.1 cell in `carrier-format.v3.md`, one observation string in `carrier-dispatch.v3.json`, five manifest rebindings.
Answers my 165 F-1 and W-1. No host mapper, no writer disposition, no executable change. Scratch only, `-I -B`; no
frozen/selected/product edit, commit, push or delegation; no cumulative approval. No cryptographic corpus repeated.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,090,716 bytes, SHA-256 `48608156abb79ecffab1a4d014ea594e82a74220e24f0b23720df10e71ccfc6f` = request = `archive-pin.json` |
| Members | 1,360/1,360 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after the lanes |
| Candidate pins | 1,287/1,287; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 165 extraction (1,287/1,287) |
| Changed | exactly eight = the declared list: three owner documents + five manifests; before-images equal my 165 bytes |
| Python | 84/84 byte-identical to 165 (hence 145) |
| Lanes, fresh scratch | all seven exit 0, counts unchanged (168+145+6,000+1,803 · 423 · 581 · 435 · 2,193 · 231 · 477+66) |

## 2. The reconciliation
| 165 item | 167 text | Result |
|---|---|---|
| **F-1** contract row said "read-only `quarantine_present` is true even for a malformed marker" | "a present marker in any retained generation that cannot be admitted makes the entire read-only capture unavailable (`unknown-custody`, carrier-format.v3 §8.1); `quarantine_present` is built only from admitted markers" | one treatment across contract, §8.1, §9 and the dispatch JSON |
| the diverging combination (malformed marker + stable malformed/foreign witness → kernel `LEDGER.CORRUPT` vs route `HOST.IO_FAILURE`) | new paragraph: "a malformed marker in any retained generation supplies no capture, so neither a bare quarantine flag nor a witness-malformed/foreign-project witness projection is evaluated from that failed capture. The result is `unknown-custody` … not a kernel-derived quarantine condition or busy retry." | the precedence I asked for is stated explicitly and names that exact case |
| kernel vs producer | "Pure model probes accepting caller-supplied marker flags exercise projected kernel behavior only; they do not establish that a real producer may admit a malformed marker." | honest and sufficient: the kernel stays a function of its inputs; the producer rule lives at population admission |
| **W-1** "the required quarantine marker" | "a present quarantine marker in any retained generation" in §8.1 **and** the machine-readable observation | matches production (156's test, 150/156 Rust) |

This agrees with the executable boundary I measured: in Rust 150/156 a malformed marker in the queried *or another*
generation, before the first *or* the second capture, yields `CaptureError::Population(MarkerUnavailable)` and no
assessment; the reference kernel has one marker case (`closed-generation-quarantine`, a supplied flag) and none with a
malformed marker, so no lane contradicts the new sentence. "Already-admitted higher-priority binding/dispatch refusals
remain separate" keeps 165's precedence.

## 3. Findings
No finding of substance.
- **W-1 (very low, for the next executable revision)** `generation_reference.py` l. 46 still documents its input as
  "`quarantine_present` (including malformed marker)". Python is deliberately byte-identical here, and the new
  paragraph tells the reader how to take such probes, so the reference is no longer contradictory in effect — but the
  docstring is the one remaining place that states the old producer rule. Fix it when that file next changes; do not
  spend a prose-only cycle on it.
- Unchanged and disclosed: 151 N-2 (three of seven lanes enforce the document hashes); the 150 F-2 host mapper does not
  exist; the writer/maintenance disposition remains explicitly undecided (165).

## 4. Closure
| My item | Status |
|---|---|
| routes165 **F-1** two treatments of a malformed marker on the read-only path | **Closed** |
| routes165 **W-1** "required" marker | **Closed** |
| routes165 N-1 (F46 vs capture failure: same public projection) | no action was needed; unchanged |

## 5. Bounded verdict
**167: reviewed, no finding of substance. Eight files changed — three owner documents and five hash rebindings; all
executable reference bytes are identical to 165/145; all seven lanes pass unchanged. The contract, the §8.1 route table
and the machine-readable observation now say the same thing: a present marker that cannot be admitted, in any retained
generation, means no capture and `unknown-custody`, before and instead of any witness-kernel projection;
`quarantine_present` is built only from admitted markers; pure flag probes prove kernel behaviour only. One Python
docstring still carries the old wording, to be fixed with that file's next real change.** Not approval of a host mapper
(none exists), of any writer disposition, of the Rust candidates, or of any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (three documents),
`owner/` (seven lanes + `exits.txt`), `probes/lanes.sh`, `hashes.txt`.
