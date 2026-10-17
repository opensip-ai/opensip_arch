# Review request: S-OP-2c r1 (the four record tables, a contract successor to S-OP-2 r6), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-s-op-2c-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not run `tools/verify_design.py` with any append or bind.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - running the unit's checker: `python3.14 -I -B docs/implementation/m3/operability/s-op-2c/evidence/check_sop2c.py`, from `/Users/sb/code/opensip-ai/opensip_arch`.

    The checker reads product files with `git show` at `5de9fd4`. It also reads the `libc` 0.2.189 crate archive in `~/.cargo/registry/cache/` and verifies it against `Cargo.lock`'s checksum. It writes nothing.

## Subject

- **Manifest:** `docs/implementation/m3/operability/s-op-2c-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1001 bytes, SHA-256 `5aec6280e1bd463679b9b453d8af881c3ac7083875b255a1d63358a1b8ec8ac8`. It has five members; rehash all five:
  - `s-op-2c/PROPOSAL.md` (the subject: gap, item 23a's law text between markers, LD-OPT-1 to LD-OPT-5, Q1 to Q7);
  - `s-op-2c/PASSAGES.md` (the two overrides);
  - `s-op-2c/README.md`;
  - `s-op-2c/evidence/check_sop2c.py` (the read-only checker);
  - `s-op-2c/successor.json` (the contract successor record).
- **Parent:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, 130,001 bytes, SHA-256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`. S-OP-2-R selected it; S-OP-2b, bound, overrides its line 429.
- **Bases:** product main `5de9fd4740ea17018d0bd3fbff9496c94ddacda9` (`/Users/sb/code/opensip-ai/opensip`). Architecture `dc96415fa` plus the uncommitted subject.
- **What raised it:** D3a-3's cross-law memo, `docs/implementation/m3/supervisor-d/d3a-3-r2/BLOCKED-TABLES.md`, with SCOPE LD-D3A3-2 and LD-D3A3-11. Also the D3a plan r4's LD-D3A-10 (`supervisor-d/d3a/PLAN-r4.md`:143-150).

## Authority

- S-OP-2 r6:
  - item 3, provenance classes, ordinary registration and successor-requiring changes (:206-239);
  - item 5, K1 (:269);
  - items 22 and 23 (:831-915).
- The S-OP-2b precedent: `operability/s-op-2b/`, and `reviews/codex-s-op-2b-r1/`.
- LD-D3A-10.
- M3-D r5 (`supervisor-d/PROPOSAL-r5.md`): items 10, 12 (:440), 18, 19 (:582-640), 21 (:681-704) and 27 (:889).
- M3-L r7 (`provider-protocol-l/PROPOSAL-r7.md`): items 10 and 13.
- M3-C r8 (`snapshot-plan-c/PROPOSAL-r8.md`): :41, :992 and :1271.
- OPP (`operability/PLAN.md`): :88 and :329.
- The D2b plan r3's LD-D2B-4.
- The pinned sources the checker reads:
  - P3T, T2O and `provider-startup.schemas.v1.json` under `docs/coop/design-corrections/native/`;
  - the product carriers, `common-v4`, `startup-v1`, `identity-v3` and `native-v2` schemas, the generated `protocol.rs` and `evidence.rs`, `crates/components/data/`, `Cargo.lock` and `crates/platform/Cargo.toml`;
  - `crates/platform/src/process.rs`:403-407 and `crates/components/src/supervisor.rs`:354, :965-966, :2569.
- POSIX.1-2017 `<signal.h>`, the default-action table, cited as LD-OPT-4's criterion.

## What to review

1. **Form.**
   - Is the record a well-formed contract successor? Check the parent pin; the line 881 override, which replaces one field's table; the line 894 override, which is insertion-only; empty supersessions; and candidates covering the subject.
   - Does the inserted text equal the `PROPOSAL.md` passage byte for byte?
   - Run the checker and report its result.
2. **Necessity and scope.** Does choosing these sources and members need an S-OP-2 successor, rather than ordinary registration? Does the successor change nothing outside its stated scope: no kind, class, provenance class, sink, bound, event, level, identity, or field other than SOP2:881's table?
3. **Each table's source and members, rederived independently.**
   - `StageKind` (LD-OPT-1): the stage `operator` const of both protocols, `semantic-provider`. Also judge the rejected alternatives, and the rule that blocks `host.reuse.disclosed`'s syntax and inventory stages until their operators are pinned.
   - `ProviderState` (LD-OPT-2): P3T's 22 `phases`, with T2O's 16 a subset.
   - `Signal` (LD-OPT-3): COMMON4 `D9Signal`, for `host.signal.received` only, and the split from `provider.process.reaped`.
   - `ChildSignal` (LD-OPT-4): the 20 members; the T-or-A criterion less `SIGPOLL`; the mapping by `libc` constant; and the absent rule for any other number. Are the per-platform numbers the checker prints right for macOS and Linux x86_64 and aarch64 gnu?
   - `ProviderReason` (LD-OPT-5): the union of the three admitted `Unavailable` reasons, 11 members, present only for `unavailable`.
4. **Faithfulness.**
   - Are the citations right?
   - Is any member invented?
   - Is any claim stronger than its source, for example the "NORMATIVE and CLOSED" standing of P3T and T2O, or "smallest closed set" in LD-OPT-4?
5. **Rule on Q1 to Q7** (`PROPOSAL.md`, "Open questions for review"). Q3 is the union-provenance question, and Q7 is the `supervision.child.settled` placement.
6. **Binding.** Can the record bind directly once accepted, with its parent already an accepted base and no overlap with S-OP-2b's line 429? State any precondition.

## Output

Write `review.json` as `{"schemaVersion": 1, "reviewer": "Codex", "unit": "S-OP-2c", "round": 1, "verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "5aec6280e1bd463679b9b453d8af881c3ac7083875b255a1d63358a1b8ec8ac8", "supersededPassages": [], "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", "Q2": "...", "Q3": "...", "Q4": "...", "Q5": "...", "Q6": "...", "Q7": "..."}, "summary": "..."}`.
- Use ids `SOP2C-R1-RF-n` and `SOP2C-R1-NBO-n`.
- `subjectManifestSha256` is a single string.
- Write `REVIEW.md` with the verdict, subject verification, each finding with its file:line and the required change, and the rulings.
