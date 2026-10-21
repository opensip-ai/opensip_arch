# CODEX2 review — NATIVE-OWNER-C1B-POSTCHECK-REMEDY-r1

**Verdict: REQUIRED-FINDINGS**  
**Supplement authorized: no**  
**Product qualification: no**

The manifest is byte-exact at `396ad431e690c831dc3e2ab844142f3d00c89173cfc451b7dd04936a82bb55f1`. All 23 subject members and all 20 existing-gate pins rehash exactly. Product main and the detached run worktree are both at `66eed0289f40bfc24e3991d9788c3d94c31daab1`; main is clean; the worktree has exactly the four preserved receipt/census changes; those four files, the parent test, the candidate test, the original `run.json`, and the failed `checks.json` match their pins. Architecture HEAD is currently the declared `c0b7bf315c5f8ed6592a17071de49d55bff4a411`.

## Required finding

### OWNPAT-CBRPC-R1-RF-1 — The executable does not bind the architecture checkout used by the supplement

`run_supplement.py` binds product main and the detached product worktree to `productBase`, but it never checks the architecture checkout HEAD against the subject manifest's `architectureBase`. It also executes `A/tools/verify_design.py` without pinning that checker. The 20 gate pins do not include `tools/verify_design.py`, and the frozen binding list covers only five selected architecture inputs. Consequently, after this review the architecture checkout or verifier can move while every runner guard still passes, and the resulting design evidence would no longer be demonstrably from the reviewed subject at `c0b7bf315c5f8ed6592a17071de49d55bff4a411`.

Before authorization, freeze a corrected runner that, before test execution, binds the architecture checkout used by the supplement to `manifest["architectureBase"]` and prevents an unpinned working-tree verifier from being used. A clean detached architecture checkout at that commit is sufficient; alternatively, add an exact checker/dependency pin and an equivalent tracked-state guard. Rebuild the subject manifest and request review of the corrected frozen package.

## Rulings

- **Failure diagnosis — ACCEPT.** The preserved Rust log has eight passes and one setup failure at `UnixListener::bind`; the actual socket pathname is 109 bytes, while Darwin requires it to be shorter than 104 bytes. The proposed `/private/tmp/ncb-*` location checks the actual 13-byte socket basename under the short root. The companion log has all 21 tests erroring in `Fixture.setUp` before assertions because the bound synthetic product omits the two paths named by `model.VCS_ANCHORS`: `snapshot_vcs.rs` and `snapshot_vcs_tests.rs`. The 25 discovery controls and design verifier passed.
- **Existing-gate compatibility — ACCEPT IN PRINCIPLE, NOT AUTHORIZED HERE.** A separately reviewed public/synthetic supplement can satisfy the remaining verification without retrying either real blind mode or expanding private-data permission. It must retain the original terminal postchecker failure and real outputs. Because the original gate returned failures to the owner protocol and authorized no retry, a new owner decision is required: exact root substantive assent to the corrected supplement manifest, runner, review, and live pins. This independent review cannot supply that assent.
- **Synthetic fixture parity — ACCEPT.** The candidate differs from the pinned parent by exactly one additive line unioning `{p for _, p, _ in model.VCS_ANCHORS}` into the synthetic copy set. Both files contain the same 21 test methods; no test body, assertion, expected result, model, mode, receipt, cost, population, or disclosure rule changes. The adapter preserves the original helper/import root and asserts discovery of 21 tests.
- **Executable guards — REQUIRED-FINDINGS.** Self, manifest, independent-review, root-assent, interpreter, gate-member, product-head, common-repository, detached-worktree, four-file, parent/candidate, frozen-binding, short-TMPDIR, before/after, and stop-on-failure guards are present. The missing architecture checkout/verifier binding is material under the exact-subject requirement.
- **Deferred product repair — ACCEPT.** Even a successful corrected supplement would require a complete independent post-run review and root assent before any exact-four-file commit. The one-line companion fixture correction remains a separate product test-only unit requiring its own validation, acceptance, integration, and metadata/status work. No receipt acceptance or product/project qualification follows from this review.

No build, test, Cargo command, lane, runner, postchecker, census mode, blind mode, network access, private-data access, or repository/worktree/stage edit was performed.
