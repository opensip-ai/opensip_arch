# Independent bounded review — read-only evidence failure routes 165 (reference, prose + machine-readable observations)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: received as a chat message; subject README read in full. Scope: the delta of frozen
`reader-routes-reference-checkpoint-165` over frozen 160 — `carrier-format.v3.md` (§8.1 row, §9), the normative
observation/phase lists of `carrier-dispatch.v3.json`, one contract wording fix, five manifest rebindings. Answers my
160 F-1/F-2/N-1/W and records the required host behaviour for 150 F-2. **No host mapper exists and none is claimed.**
Scratch only, `-I -B`; no frozen/selected/product edit, commit, push or delegation; no cumulative approval. No
cryptographic corpus repeated.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,090,180 bytes, SHA-256 `16a346c9a791031d9ee3ca56c42bb35c3ff8f19081328b62cf6971ef035e0014` = request = `archive-pin.json` |
| Members | 1,360/1,360 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after all runs |
| Candidate pins | 1,287/1,287; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 160 extraction (1,287/1,287) |
| Changed | exactly eight = the declared list: three owner documents + five manifests (every changed manifest line is a SHA-256 value); before-images equal my 160 bytes |
| Python | 84/84 byte-identical to 160 (hence 145) |
| Lanes, fresh scratch | all seven exit 0, counts unchanged |
| Binding | `carrier-dispatch.v3.json` is pinned in all five manifests, parses, and a one-byte change is refused by the security and native lanes (`probes/pin-binding.txt`; my scripted loop mis-reported and is preserved as FAILED-r1) |

## 2. The route, checked across all three places
| Place | Text | Agreement |
|---|---|---|
| §8.1 table | the `unknown-custody` row gains "an inherited generation is unavailable to the typed reader under §9's mirror policy; or the required quarantine marker cannot be admitted (`MarkerUnavailable`)" → operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, no `domainDetail` | ✔ |
| §9 | "report `unknown-custody` on the read-only path (§8.1: …)"; "Neither … is `unavailable-busy` or an `unknown-quarantine-condition`" | ✔ same standing, same projection, both wrong neighbours excluded by name |
| dispatch JSON | two observations under the `unknown-custody` standing; two phase laws (not busy / not quarantine-condition / not not-committed; writer disposition undecided) | ✔ |

It uses only existing vocabulary, adds no public code, and says the route "does not replace a higher-priority
independently admitted binding/dispatch refusal". **160 F-1: closed. 150 F-2: the required mapping is now normative;
its implementation stays open, as stated.**

**160 F-2** — "This read-only profile does not decide the public disposition of a writer or maintenance open … must be
selected and tested before enabling that writer path … may not be inferred from the migration-corruption rows … not a
default success route." Exactly the second of the two options I offered; **closed as an explicit prerequisite.**
**160 N-1** — mandatory mirrors, recomputed selected-domain digest, `prev_sha256` retained and diagnostic: matches the
154 reader clause for clause. **Closed.** **W** — "in the v8 preview". **Closed.**

## 3. Findings
- **F-1 (low–medium) — the contract still states the *other* treatment of a malformed marker on the read-only path.**
  `security-and-lifecycle.md`, projection table (l. 943, unchanged): "read-only `quarantine_present` is true **even for
  a malformed marker**". Under that sentence the kernel continues with `quarantine_present = true`; under 165 (and in
  Rust 150/156) a malformed marker means **no capture at all** → `unknown-custody`. Usually both end in unknown custody,
  but not always: with a malformed marker **and** a malformed (or foreign-project) witness, stable over two captures,
  the kernel's order gives `candidate: witnessMalformed` → `unknown-quarantine-condition` → `LEDGER.CORRUPT`, whereas
  165's route gives `unknown-custody` → `HOST.IO_FAILURE`. Two documents of one reference now prescribe two public
  outcomes for the same observation, and 165's own sentence ("does not replace a higher-priority … binding/dispatch
  refusal") does not settle it, because a witness condition is neither. 156's README already noted that the Python
  kernel's projected flag "differs from production"; the contract row is where that difference has to be reconciled —
  e.g. "a present marker that cannot be admitted makes the capture unavailable (`unknown-custody`, carrier-format
  §8.1); `quarantine_present` is built only from admitted markers". (The neighbouring writer sentences — l. 875 "a
  malformed marker is unavailable custody", l. 949 — already agree with 165.)
- **W-1 (low, wording)** "the **required** quarantine marker cannot be admitted" reads as "the marker of the queried
  generation". Production refuses the capture for a malformed marker in **any** retained generation (pinned by 156's
  test, stated in 156's README). "a present quarantine marker in any retained generation" says what happens.
- **N-1 (note, no action needed)** Precedence between F46 (`unknown-carrier-incompatible`, "decided from the object
  names alone") and a capture failure is not stated: in Rust a mirror-refused inherited generation fails the capture
  before the below-boundary test is reached. The two standings have the **same public projection**
  (operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, no `domainDetail`), so nothing observable depends on it; a
  host that logs internal standings should expect either.

## 4. Closure
| My item | Status |
|---|---|
| mirrors160 **F-1** "unavailable custody" not a standing | **Closed** |
| mirrors160 **F-2** writer/maintenance disposition unstated | **Closed** — explicitly undecided, with a do-not-infer rule |
| mirrors160 **N-1**, **W** | **Closed** |
| anchor150 **F-2** host mapping of capture failures | normative route **stated**; implementation open (as the README says) |

## 5. Bounded verdict
**165: reviewed, no blocking finding. Eight files changed — three owner documents and five hash rebindings; all
executable reference bytes are identical to 160/145; all seven lanes pass; the changed dispatch JSON is pinned and
enforced. The `unknown-custody` route for a mirror-policy refusal and for `MarkerUnavailable` is stated identically in
the §8.1 table, §9 and the machine-readable list, in existing vocabulary, with busy and quarantine-condition excluded
by name; the writer disposition is explicitly left undecided with a rule against inferring corruption. F-1: the
contract's projection row still says a malformed marker yields `quarantine_present = true` on the read-only path, which
in one reachable combination (malformed marker + stable malformed witness) prescribes `LEDGER.CORRUPT` where 165
prescribes `HOST.IO_FAILURE` — reconcile that row.** Not approval of any host mapper (none exists), of the Rust
candidates, or of any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (eight), `owner/`
(seven lanes + `exits.txt`), `probes/{lanes.sh, pin-binding.txt, pin-binding-FAILED-r1.txt}`, `hashes.txt`.
