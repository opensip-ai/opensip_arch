# Independent review — frozen `account-temp-contract-checkpoint-217` (documentation-only)

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 217 product bytes — comment-only successor of 216 answering my 216 W-1 / N-1 / T-1 / N-2. No code, test, dependency, schema or API-shape change is claimed, and the owner requested no behavioural rerun; parent 216 evidence is *inherited*, not relabelled as a 217 exact-byte run. Scoped documentation disposition only — no cumulative, native or admission approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `2c8762c58f853351f95d684efb58c2e4d31434e17f3136b9de24c50d1f598f93`, 4,099,924 B = request = `archive-pin.json` |
| Members | 364, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 355/355 rehash; none unpinned, none missing |
| Delta vs **my own verified 216 extraction** | exactly two files differ: `platform/src/lib.rs`, `platform/src/macos.rs`; 353 byte-identical; none added/removed |
| **Comments-only, checked independently** (`io/check217.txt`) | with `//`-comments (outside string literals) and blank lines stripped, both files are **line-for-line identical** to 216 (45 and 285 code lines). So every executable and test token is the 216 one, and 216's evidence — mine: 172 security / 44 platform / Clippy, 12/12 public-wiring mutants, the FFI measurements — legitimately carries over by construction rather than by assertion |

No build or test was run for 217; none is needed to establish the above.

## 2. Disposition of my 216 points
| 216 | 217 text | Disposition |
|---|---|---|
| **W-1** the OS call creates the directory | public `lib.rs`: "Obtain the macOS per-account temporary location… **The OS may create the directory as a side effect. Never call on a write-free admission or report-only path; current callers are test fixtures only.**"; adapter: "confstr may CREATE the directory; never call on a write-free admission or report-only path"; the verb changed from "Query" to "Obtain", and the test comment from "observation" to "call (possibly creating it)" | **closed.** Accurate against `confstr(3)` ("The directory will be created it if does not already exist"). The "current callers are test fixtures only" claim checked: the only uses are the platform's own unit test and the `#[cfg(all(test, target_os="macos"))]` policy test in `security/lib.rs` (l.398) |
| **N-1** raw, non-canonical value | "The returned path may contain symlinked components or a trailing separator. It is not canonical or admitted custody… Resolve its location, then separately admit every retained directory component." | **closed** — matches what I measured (`/var/…/T/`) |
| **T-1** no-fallback unpinned on failure | beside the return: "Return the parser result directly. No environment or alternate-path fallback is permitted on failure; healthy-host tests cannot exercise every OS failure." No synthetic source-mirroring test added | **accepted as documented.** This is the honest form: the property is a reading-level invariant of a three-statement function, the comment forbids the combinator, and nothing pretends a healthy host proved the failure path |
| **N-2** one `InvalidData` for zero-return and over-bound | README: remains a documented limitation; "no new production consumer or error-mapping promise" | **accepted** — appropriate while the only callers are tests |

## 3. Findings
None. Two remarks:
- **N-1** the prohibition is now in words only; the item is still `pub` in `opensip-platform`. That is a reasonable choice for a test-support need spanning two crates, and the doc comment is explicit. If a production need for an account-scoped location ever appears, it deserves its own reviewed owner (and a decision about the creation side effect) rather than reuse of this helper.
- **N-2** the README states the inherited-evidence boundary precisely ("not tests on 217 exact source hashes") and restates the three parser/FFI mutation limits from my 216 review without softening them. Nothing to add.

## 4. Limits
Documentation review plus an independent byte/token comparison; no compile, test, mutation or host run on 217 bytes (none requested; none needed for a change proven comment-only). My comment stripper treats `//` outside double-quoted strings as a comment start; neither file contains raw strings or `//` inside character literals that would defeat it (the stripped outputs are equal, which a false strip on only one side could not produce). Linux not in scope.

## 5. Verdict (bounded)
**217 is a comment-only successor of 216 — proven by token-level comparison, not taken from the README — and its comments correctly state that the macOS call may create the directory, forbid write-free and report-only use, describe the value as non-canonical, and record the no-fallback rule with its testing limit. 216 W-1 and N-1 are closed; T-1 and N-2 are accepted as documented limitations. No finding.** No approval of behaviour beyond what 216's evidence already covered, and none cumulative.
