# Independent bounded review — population wording 153 (reference, prose only)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: the user's message of 2026-09-19 (no request file for 153 was named; scope taken from that message and the
subject README). Scope: the delta of frozen `population-wording-reference-checkpoint-153` over frozen 151 — a rewording
of one contract paragraph plus five manifest rebindings. No executable behaviour. Scratch only, `-I -B`; no
frozen/selected/product edit, commit, push or delegation; no cumulative approval. No cryptographic corpus repeated: no
byte it exercises changed.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,067,008 bytes, SHA-256 `7d3478fa64db6431423bce3922f72b99ca96fa9175649bef513630a840e195df` = request = `archive-pin.json` |
| Members | 1,358/1,358 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after all runs |
| Candidate pins | 1,287/1,287; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 151 extraction (1,287/1,287) |
| Changed | exactly six = the declared list: the contract (`25acd5b8…17bfc` → `d8022f4b…d52af`) and five manifests; every manifest line changed is a SHA-256 value; before-image equals my 151 bytes |
| Python | 84/84 byte-identical to 151 (hence to 145) |
| Lanes, fresh scratch | envelope 168+145+6,000+1,803 · integration 423 · security 581 · carrier 435 · workflows 2,193 · foundation 231 · native 477+66 — all exit 0, counts unchanged |
| Binding | one byte appended to the contract in a scratch copy: security and native refuse; foundation and workflows still pass — as the README now says (151 N-2 stated, not closed) |

## 2. The wording against its sources
**W-1.** "A purged generation remains admissible as the final generation of the historical population." This is the
fact the law establishes (dispatch grid of my 151 review: purge, no successor → admitted; Rust 148: `ProjectPurge`
end, readable population) and no more; the README adds that it promises no successful query after purge. **Closed.**

**W-2.** The cited owner exists and says what is attributed to it. Frozen `security-completion.v8.md` §5.4
(ll. 289–294; file `54f3a690…8c2d`, byte-identical to 151 and pinned in all five manifests):

> Project purge and retirement are user operations deferred with DR-113 by the lead's foundation decisions; the v2
> "project purge" cause is unreachable in the preview and is retained as a typed reserved cause for that slice, whose
> ordering across registry entries, selection, journal namespace and tombstone is that slice's design.

| Clause in 153 | Frozen owner | Result |
|---|---|---|
| "reserves the project-purge and retirement lifecycle transition … to that lifecycle slice" | "deferred with DR-113 … retained as a typed reserved cause for that slice" | faithful |
| "including ordering across the namespace registry, selection, journal namespace and tombstone" | "ordering across registry entries, selection, journal namespace and tombstone is that slice's design" | faithful ("namespace registry" for "registry entries" is a harmless paraphrase) |
| "This population rule adds no such transition" | 84/84 Python identical; dispatch documented inert | true |
| "the inert `continuation-eligible` disposition is not authorization to continue or recreate a purged project namespace" | contract l. 877 "Eligibility to continue never grants an execution permission"; dispatch docstring "Only an independently authorized writer may act on continuation-eligible" | true; a restatement for this state, not a new rule |

It invents **no permanent ban** (it does not say a purged project can never be continued — it says this rule does not
decide it and names who does) and **no writer transition**. **Closed.**

## 3. Findings
No defect. Two small wording observations, neither blocking:

- **W-3 (very low)** "to that lifecycle slice" has no antecedent inside the contract paragraph; in v8 "that slice" is
  the *DR-113-deferred* purge/retirement slice. Naming DR-113 ("to the deferred DR-113 lifecycle slice") would let a
  reader find the owner without opening v8.
- **W-4 (very low, optional)** v8 also says the purge cause is *unreachable in the preview*. The paragraph is correct
  without it, but one clause would tell the reader that a `projectPurge` TERMINAL is, today, only ever typed reserved
  *input* to population admission, never something this product wrote — which is why the rule can be purely about
  admission.

Carried unchanged and now stated in the README: 151 N-1 (whole-population admission is executable only in Rust),
151 N-2 (three of seven lanes enforce the contract hash).

## 4. Closure
| My item | Status |
|---|---|
| population151 **W-1** "readable" undefined | **Closed** |
| population151 **W-2** prohibition without a named owner | **Closed** — existing frozen owner named accurately; nothing invented |
| population151 **N-1**, **N-2** | acknowledged in README; open by the owner's choice |

## 5. Bounded verdict
**153: reviewed, no finding of substance. Exactly one paragraph and five hash rebindings changed; all executable
reference bytes are identical to 151/145; all seven lanes pass with unchanged counts. Both sentences are accurate
against their sources: the first states only what population admission establishes, the second attributes the
purge/retirement transition to the frozen v8 §5.4 reservation in that text's own terms and adds neither a permanent
prohibition nor a transition.** Not approval of any other content of the reference, of any Rust candidate, or of any
cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (six), `owner/`
(seven lanes + `exits.txt`), `probes/pin-binding.txt`, `hashes.txt`. The executable grid that grounds §2 W-1 is in my
151 review (`claude-population151-20260919-r1/claude-out/probes/`), valid here because all Python bytes are identical.
