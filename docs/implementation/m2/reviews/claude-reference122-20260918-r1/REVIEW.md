# Independent bounded review — platform-bound reference 122

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-18. Request: `REQUEST.md`.
Subject: frozen `platform-bound-reference-checkpoint-122`, exact successor of 120, addressing my carrier119
I-2 (reference side) and reference120 F-1, F-3, F-4. Scoped verdict only; inherited approval is not
assumed. No frozen/selected/product edit; scratch copies with bytecode writing disabled; no commit, push
or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,093,928 bytes, SHA-256 `05d5b446e08d94cf4e7873e81f47dc5f7da733e6c9654531d15b30fbc0e549d1` = request and `archive-pin.json` |
| Members | 1,371/1,371 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Candidate | 1,284/1,284 pins equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 120 extraction |
| Delta | the 10 declared: model (one condition), envelope model binding, checker (+1 sweep, +4 open cases), `generation-dispatch-cases.v1.json`, contract (two paragraphs), five pin inventories |

**Owner checks reproduced, required order, fresh output**: envelope receipt 168 / 145 / 1,803 / 6,000
passed → integration **423 / 0** with that receipt → security **581 / 0, 20 sweeps** (dispatch/floor/open
145, new `linux-release-identity-and-diagnostics-bounded` 13). I did not rerun carrier, foundation,
workflows or native (unchanged apart from pins).

## 2. The change
`platform_admit`: `LINUX_OSRELEASE_RE.fullmatch(release)` is attempted only when `release` is a `str` of
at most 256; otherwise the existing fixed `NT-TCB-IDENTITY:OSRELEASE_GRAMMAR`. The grammar is explicit
ASCII (`[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-[a-z0-9]+`), so a code-point count equals a byte count for every
string that can match, and the contract's "at most 256 bytes" is accurate. The contract also states the
Linux (line/flavor/lane, ABI as drift) versus macOS (kernel UUID + dyld cdhash) policy difference, and the
two composed-open limits I raised in 120.

## 3. Evidence

**Boundary probe through the public `platform_admit`** (`probes/osrelease.py`, 32 cases):
- each of ABI, flavor and line padded to **255 / 256 / 257 / 5,000**: 255 and 256 take ordinary
  population selection (ABI-padded releases are ADMITTED with the ABI as drift; an unlisted long line or
  flavor gets the ordinary `KERNEL_LINE_OR_FLAVOR_…` refusal); **257 and 5,000 give the fixed grammar
  refusal with no reflection and no drift**, in both tiers (checked separately at EXACT-MEASURED);
- Unicode and grammar: Arabic-Indic and full-width digits, trailing newline, leading space, upper-case
  flavor, four-part line, empty ABI, embedded NUL, 200 CJK code points (600 bytes), emoji flavor, `+1`
  ABI — all the fixed grammar refusal; `None`, int, list, dict, bool — likewise;
- precedence: a boot refusal (`nsUnchanged` false) still wins over a 5,000-character release; no grammar
  refusal is added to it.
- **Longest refusal anywhere 302 characters (was 5,055 in 116/120); longest drift value 244 (was 4,002).**

**Mutation** (owner sweeps called directly; no pin gate in that path): bound removed, 257, strict `< 256`,
over-long input truncated instead of refused, bound applied to the ABI only — **all killed**; "bound counts
UTF-8 bytes" survives and is **equivalent** (ASCII grammar). Both of my real 120 generation-selection
survivors — floor of generation 1 always selected; floor checked against the highest generation key's
rows — are now **killed** by the four added open cases.

## 4. Closure

| Finding | Status |
|---|---|
| **119 I-2** unbounded kernel-release reflection (reference side) | **Closed in the reference.** The Rust port is pending, as stated; until it lands the Rust still mirrors 116's behaviour. |
| **120 F-1** generation selection unpinned | **Closed** — both mutants killed. |
| **120 F-3** malformed floor suppresses a tail-loss marker | **Closed as a disclosed limit** ("permanent refusal in the current profile, not an automatic floor reconstruction path"). |
| **120 F-4** absent floor: never-created vs deleted | **Closed as a disclosed limit**, with the read-only asymmetry stated. |
| 120 F-2 (`dispatch` alone still acts without a floor check) | Unchanged; it was a note for the Rust integration (make the lower-level function private to the composed entry). |

## 5. Remaining notes
- **N-1 (note)** — the refusal that reflects line and flavor is now bounded by construction at about
  `27 + 256` characters, not by an explicit limit on the refusal itself. If any consumer stores refusals
  in a 256-bounded field, 302 is over it; `BoundedText` is 1,024, so nothing breaks today. Worth stating
  the derived maximum next to the bound.
- **N-2 (note, Rust port)** — port it as a length check **before** `kernel_release_parts`, on bytes, and
  carry the same boundary set (`probes/osrelease.py` constructs all 32 inputs deterministically from a
  frozen fixture case; `osrelease.json` records the reference outcomes) so the 255/256/257 edges and the
  Unicode refusals are pinned on both sides. The same port should
  include 119 I-1 (verified-profile type for `platform_decision`), which the request says is next.
- **N-3 (note)** — the model still names `NT-TCB-BOOT:BOOT_ATTESTATION_UNKNOWN`, which Rust cannot emit
  because `profile_shape` closes `bootAttestation` to two values. Unreachable behind the shape gate in
  both; harmless, but it is one more place where the reference accepts a wider profile than Rust admits.

## 6. Bounded verdict
**Reference 122: reviewed, no finding against the change. 119 I-2 is closed on the reference side and
120 F-1, F-3, F-4 are closed; the Rust port of the bound (with 119 I-1) remains to be done and reviewed.**
Not approval of SQL admission, physical capture, marker writing, caller integration, or any cumulative,
OS or target qualification.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `model.diff`, `checks/*`,
`probes/osrelease.{py,json}`, `probes/mutation.{py,json}`, `hashes.txt`.
