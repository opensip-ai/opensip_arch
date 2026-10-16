# B3-B3A2-r1 pre-run review

Verdict: **ACCEPT-UNIT**. **runAuthorized: true**, conditional on B3-b3a2's code and lock being on main at the reviewed bytes and all RUN-PLAN preconditions being met. This review does not execute the run.

Required findings: none. Non-blocking observations: none.

The subject manifest independently matches 14119 bytes and SHA-256 `afa0e3a3c4fcf0bc1e0f4b1ad4223d2c59d415781c5ceae39ae08f3ad4989651`. All 59 members match their sizes and hashes. The four candidate files match their product-map parent/candidate/archive pins and are exactly the worktree changes. Product main is clean and the candidate is at `2dd54bae4afa0f6494ff2c4208982af5fcd7ff41`; architecture is at `abbf48fb0992b48178bf3de0aac2c42015e48b4e`. All source authority and product-lock pins match.

## Confidentiality and equivalence

The extended blind path keeps carrier text in memory only. It passes the verified tree through the walker/reference population and the shared `repository_terms`, then reduces the result to full-ledger margins and a verdict. No carrier, directory, population, term breakdown or exception string is serialized into the measured/error row. The admitted-member check uses a fixed blind label; even its exception message is discarded.

Integrity exceptions are reduced to INTEGRITY or IO. Exceptions and SystemExit from measurement, including D15 parsing, requests and the no-member requirement, are reduced to MODEL; OSError is reduced to IO. Full-ledger/arithmetic/verdict-check exceptions and SystemExit are reduced to MODEL. A population disagreement yields POPULATION. The top-level blind-mode BaseException boundary converts exits, interrupts and otherwise escaping failures to the existing fixed generic failure line and exit 1. Argument parsing precedes store access. The pure parsing/model code adds no logging or printing of held-out values. The existing ordinary-mode access guard and separate blind digest join remain intact.

The real-term canary controls exercise valid Cargo and npm carriers, placement/listing requests, malformed TOML/JSON, invalid UTF-8 and oversized input. They check both the closed receipt and stdout/stderr. The synthetic rule is appropriate for these confidentiality/wiring controls: it does not replace the real-rule fidelity evidence or equivalence run. Existing controls cover exception reduction, SystemExit, top-level interruption redaction, invalid receipts, coverage and lifecycle. Together with source inspection, these cover the extended gate without opening real held-out data.

Both readable rows and blind rows now call `repository_terms`. It requires no admitted member and equal walker population. `full_ledger` supplies identical objects, edges and affine bytes, with the blind byte margin taken at R=4096. The additional verdict check requires agreement between the full-ledger boolean and all three floored margins being at least 2000.

The archived equivalence program filters the manifest for `heldOut is False` before calling `blind_row` with a copied flag set to true. Consequently it presents only readable stores to the guarded blind join. Its recorded 39 rows all exactly equal the corresponding readable `d15.fullLedger` margins and verdicts. No held-out store is opened by that program.

## Format, binding and stale receipt

LD-1 is sound. The format remains the same closed schema-version-1 receipt and the same measured/error row keys and error classes. Its standing now identifies full-ledger margins. Since the terms are non-negative, a full-ledger pass implies a walker pass; its single verdict equals the conjunction used by readable-row failure classification. Adding a second set of margins would unnecessarily widen A5's allowlist.

Bindings cover the tool, member model, every closure file, manifest, sizes, caps, root lengths and reference-loading/reference inputs. The model pin closes the new dependency introduced by the D15 calculation; the tool pin covers composition/envelope formulas. No new source dependency of the calculation is left outside that binding scheme. Existing pinned runtime/platform assumptions remain those of B3-b3a1.

The committed receipt remains well-formed schema version 1 with ten measured rows and no memberModel binding. It is correctly stale against the changed tool/closure/model bindings, rather than malformed. Its old walker-only result cannot satisfy the new gate. I verified that neither the candidate receipt nor the census record changes in this unit, and that the vectors change only at `/memberModel/bytes` and `/memberModel/sha256`.

The model's executable AST is unchanged; only read_envelope's docstring changes. It now correctly distinguishes no-follow carrier/provider/member/global evidence from refusal-only system sources that follow symbolic links to a regular final file. B3-b3a1 NBO-1 is resolved without changing the envelope.

## Run authorization

The reviewed script's pinned bytes are:

- `tools/security/discovery_census.py`: `6e52bd5bed8599071fb595bd4050e1cad93307987107238cbfad58b1f7fc99c6`.
- `tools/security/discovery_member_model.py`: `582bad12d1e04e95089a7c965b6c542f10da412fb0efe22c4b4758db4cf421f1`.

These equal the candidate. Under the lane lock, the script sets nice 10, creates/chmods a private 0700 TMPDIR, uses the fixed interpreter with isolation/no-bytecode flags and PATH=/usr/bin:/bin, and checks equal clean main/run-worktree HEADs and both files' hashes in both trees. RUN-PLAN additionally requires the code and lock integrated and a clean detached worktree of main; those are conditions of this authorization, not permission to substitute another checkout or tool.

The script reads the old public receipt/census, removes only the receipt path in the run worktree, and has exactly one blind-mode invocation. Ordinary write/check follow; they compose held-out rows from the receipt and open only readable stores. Nothing outside blind mode inspects held-out stores or overlays. The script records blind exit/stdout/stderr status, receipt pin, ordinary exit codes, ids/state, margin comparisons, changed bindings and census keys, readable-row equality and workspace equality. It commits nothing.

The recorded comparisons are evidence for post-run review, not automatic acceptance assertions. The caller must apply RUN-PLAN's outcomes to run.json and the receipt: any run error, error row, nonempty stderr or unsuccessful ordinary regeneration leaves the margin outstanding and commits nothing. Every measured row proceeds to post-run review and lead assent; a below-2x result returns caps to law and is not a reason to rerun. The script's completion alone does not establish a passing margin.

The owner's mechanical-blind-run decision, B2-b4 plan r6 lifecycle and A5's single gated refresh therefore support B3-b3b proceeding exactly once as RUN-PLAN states, after integration at the reviewed bytes. This authorization does not waive the post-run review or authorize another run on failure.

## Verification

I independently ran the two expressly permitted commands in the candidate: all 25 synthetic/hermetic blind controls passed, and the vector-only census check passed. Neither command reads a real T2 store.

The final archived evidence has equal named security failure sets (14 at base and candidate), equal total passes (1166 each), and no Rust changes or new Rust test. The full suites retain those base failures. The final projection is exactly the two member-model pin fields; the census is byte-identical. Recorded D15 soundness, focused tests, census controls, cache census check, readable-store blind equivalence, environment/operability checks and verify_design all pass. The cache/equivalence executions are reviewed evidence, not independent reruns here.

All three mutations fail the intended synthetic controls: ignoring terms fails full-ledger arithmetic, real-term equivalence and failing-cap lifecycle; omitting the model binding fails drift staleness; removing the no-member requirement fails silent MODEL reduction. Attempt 1 failed only the runner's overly narrow projection allowlist; the final attempt corrects that allowlist to the actual nested pin fields, with no other record change.

Only REVIEW.md and review.json are written. Neither repository, worktree nor control files were edited. No Cargo, rustc, builds, lane, network, cache census, blind run, run script, private fixture/installation/key/held-tree access, held-out store or overlay, other pane or delegation was used. No held-out margin, workspace margin, qualification or project completion is claimed.
