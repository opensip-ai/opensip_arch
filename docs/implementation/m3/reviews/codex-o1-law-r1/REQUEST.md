Codex review: the **M3-O1 law r1** and the two design units that record **S-OP-2**. Claude Opus 5.5 leads, and you are the single reviewer. Three verdicts are wanted, in three files:
- **M3-O1 r1**, the law for operability code unit O1: **ACCEPT** or **REQUIRED-FINDINGS**;
- **S-OP-2-P**, the parent selection that S-OP-2's recording needs: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**;
- **S-OP-2-R**, the recording itself (S-OP-2 r6 item 24): **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex-o1-law-r1/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No cargo.** Don't run any build, test or lead set: timing-sensitive lanes may be using this machine. Because you run no cargo, the shared lane lock does not apply to you.
- You may re-run `evidence/verify_scratch.py` (this directory) only in your own throwaway detached worktree of product main `b7b87b7`, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, as the lead did. It is Python only. Never run it in the main product checkout: it rewrites the worktree's `design-lock.json`. Remove the worktree and the TMPDIR afterwards.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## The subjects

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/`. Every pin is in `hashes.txt`. Apart from the three subjects, this request pins accepted snapshots only. Every subject file is untracked until acceptance: read the working-tree bytes and check them against the pins.

| Subject | Path | sha256 | Bytes |
|---|---|---|---|
| **M3-O1 r1** (the law) | `docs/implementation/m3/operability/o1/PROPOSAL.md` | `ac3f12fa…` | 73,886 |
| **S-OP-2-P** (`subjectManifestSha256`) | `docs/implementation/m3/operability/s-op-2/s-op-2-p-subject.json` | `65af7fd3…` | 622 |
| **S-OP-2-R** (`subjectManifestSha256`) | `docs/implementation/m3/operability/s-op-2/s-op-2-r-subject.json` | `1d8e41be…` | 1,245 |

- **S-OP-2-P's members:** its `s-op-2-p/successor.json`, SDK4 (`docs/coop/artifacts/component-sdk-contract.v4.json`) and DRC (`docs/coop/completion/distribution-runtime-completion.v2.md`), byte for byte as the D-369 application pins them.
- **S-OP-2-R's members:** S-OP-2 r6's accepted `PROPOSAL-r6.md` (`ce8d3a4b…`, the bytes you accepted), and `s-op-2-r/`'s `README.md`, `PASSAGES.md`, `successor.json`, `evidence/build_sop2.py` and `evidence/check_sop2.py`.
- **Not members:** the lead's assent drafts `s-op-2-p-unit.json` and `s-op-2-r-unit.json`.
- Read `s-op-2-r/README.md` first for both units; `PASSAGES.md` shows both overrides with `before`, `after` and the inserted sentence.

**Product:** main `b7b87b7` (E2a). Its lock has 101 contract successors, 5 contract passage supersessions and 98 inventory successors, with v138 selected.

## Background

- **Why a law.** O1 is M3P's M3-O first code unit (M3P:317). Its implementation agent read the operability plan r3 and S-OP-2 r6 and stopped before coding, as instructed, with nine gaps, G1 to G9. Its report is copied to `evidence/gap-report.md` as context; the law restates every fact it uses.
- **S-OP-2 is accepted but not bound.** Its item 24 says the lead records it "When M3-O's first code unit lands" (SOP2:920). You reviewed that item; this request is that recording, made now so it binds before or with O1-a.
- **One finding beyond the brief.** Item 24's two overrides name SDK4 and DRC as parents. Neither is in the design the lock selects: not in the source manifest (`candidate-subject.v45.json`), not in the application manifest (`application-subject.v46.json`), and not a candidate of any bound contract successor. APP pins both by sha, at `/rows/12/inheritedContract` and `/evidenceTargets/D.SDK/sources/0`, but does not carry their bytes. So VD refuses item 24's single record: "contract parent is not an accepted base or selected inventory". The lead's fix is two units: S-OP-2-P selects the two files in `control-source-v1`'s form (the precedent that selected the unselected `control-completion.schema.v3.json`), and S-OP-2-R records item 24 on top of it. The law's item 22 and the README's LD-R1 give the reasons and the rejected alternatives.

## The law: lead decisions to judge

The lead made these decisions before drafting. The law records each with its rejected alternatives. A disagreement with any of them is a finding.

| Gap | Decision | Law item |
|---|---|---|
| G1 | A new crate `crates/operability` (`opensip-operability`), `forbid(unsafe_code)`, depending only on platform; host, storage and components depend on it. Platform gains a `getrusage` CPU-time call. **CH14 needs only a record note** (CH14-O), because its package table is a generated proposal that "grants no component authority" (CH14:271-275), and the binding edge list is the reviewed product inventory. | 1, 2 |
| G2 | O1 ships scope types, a one-time capability set issued at startup and distributed by bootstrap, and the storage owner token, tested with test-only mints. Owners wire the real mints: J3a (or its follow-up leg J3a-o) for RequestId and ExecutionId; X3c-3 or J3d for the commit events; J2b or J3d for Project, Plan and attempt. **No record carries an identity until its owner has wired the mint**, so no production record exists before the RequestId scope is wired. | 7, 8 |
| G3 | **No `tracing`**, an in-house transport (SOP2 item 10), and a lane check that fails if `tracing` or `log` enters the host lock without a law. This departs from M3P's M3-O wording and is recorded for M3P r11. HMAC-SHA-256 is written in-house. **SHA-256: written in-house in operability (option (e)),** because it is the only option that adds no crate and keeps operability's edges at platform alone. Item 3's table gives every locked or available source and its edge effect. | 3, 4 |
| G4 | A harness-only sink on inherited descriptor 3, behind a non-default feature that builds without debug assertions refuse; `recordSha256` is the SHA-256 of that stream. `host.phase.started` (`phase`, optional `parent`, `at`), `at` on `host.phase.completed`, and a `not-applicable` outcome; plan §4.1's phases under a root `request`. This needs a narrow successor, **S-OP-2b, whose exact text is in the law** as an owed successor, not drafted as a unit here. | 13 to 15 |
| G5 | A non-default `operability-dev-sinks` feature, refused without debug assertions, with stderr at a fixed `debug` level. Production constants: file off, stderr off, pre-scope buffer and ring on, so every file projection ends `unpersisted` (or `prescope-full`), as intended. Finalization at the existing termination points. **The loss summary stays unrendered until S-OP-6.** | 9 to 12 |
| G6 | A source-scan checker with a committed per-file count exception list, its negative controls, and a `dispose` helper over a closed enum (`BestEffortCleanup`, `AlreadyReported`, `ShutdownPath`, `TestOnly`, `Infallible`), placed in **platform** because 126 of the 140 production `let _ =` lines are in platform and security. **Test-only files are out of scope.** The clippy lints and the site migration are the later sweep, O1-S. | 19 to 21 |
| G7 | `host.termination.decided` and the configuration-key tables after E2s integrates, with the contracts generator emitting literal tables. | 17 |
| G8 | The K6 census goes to S-OP-7's unit. | 18 |
| G9 | The S-OP-2 recording, as two units (above). | 22 |

**Consumers' registrations (item 16):** D3a registers S-OP-2's provider and supervision events and its own, with a new `tool` domain; O1-a registers `host.repair.completed` with its closed tables (7 kinds; 14 states RW-R1 to RW-R7, RW-P1 to RW-P3, RW-L1, RW-T1 to RW-T3; JRW:423-436, :491-496); M3-L's events are emitted only once L is in effect.

**Units (item 23):** O1-a (crate, registry, transport, scopes, sinks, finalization, HMAC tag, checker); **O1-p** (platform's three additions, split out because `crates/platform/src/lib.rs` is in J3a's and J4a's diffs); O1-b (harness sink and phases, after S-OP-2b); O1-c (termination and configuration tables, after E2s); O1-S (the sweep, after J3a, J4a and X3c-3). Each row names its controls, dependencies and the in-flight files it must not touch.

## The local binding check

The output is pinned: `evidence/local-binding-check.json`.
- **Where.** A throwaway detached worktree of product main `b7b87b7` (`/Users/sb/code/opensip-ai/opensip-sop2-check`, since removed), with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, also removed. Python only, with no cargo.
- **How.** The worktree's own `tools/verify_design.py` (43,946 bytes, `7b313de6…`, byte-equal to `b7b87b7`'s) was loaded unchanged. Each unit's entry was appended to the worktree's `design-lock.json` with SCRATCH review and assent pins, served from memory by an overlay of `pinned_bytes`, as CRC-2's, ENUM-1's and SD-8's checks did. Both scratch reviews list `"supersededPassages": []`.
- **Results:**

  | Configuration | With the worktree as implementation | Without | Contract successors | Contract passage supersessions |
  |---|---|---|---|---|
  | baseline (literal CLI and overlay) | PASS | PASS | 101 | 5 |
  | **S-OP-2-R alone** | **REFUSED:** "contract parent is not an accepted base or selected inventory" | same | | |
  | S-OP-2-P alone | PASS | PASS | 102 | 5 |
  | S-OP-2-P, then S-OP-2-R | PASS | PASS | 103 | 5 |

  In each passing configuration, the inventory chain, inheritance and supersessions, generation and admission sources, and verified inputs equal the baseline's.
- **Probes,** each on main's lock plus the named entries:

  | Probe | Result |
  |---|---|
  | S-OP-2-R alone | "contract parent is not an accepted base or selected inventory" |
  | S-OP-2-R whose review names S-OP-2-P's subject | "contract review names a different manifest" |
  | S-OP-2-R whose review lists a superseded passage | "contract review superseded passages differ from the record" |
  | after S-OP-2-P, SDK4's override with its `before` altered | "passage override before text differs from accepted parent" |
  | after S-OP-2-P, SDK4 selected by a line selector | "v4 JSON parent passages require JSON Pointer selectors" |
  | after both, a second plain override of DRC:576 | "conflicting contract passage overrides" |
  | after both, a VD2 supersession of S-OP-2-R's DRC:576 | PASS (the passage stays editable) |
  | after S-OP-2-P, a second selection of SDK4 and DRC | "contract candidate reuses an accepted path" |
  | S-OP-2-R whose subject omits `PROPOSAL-r6.md` | "contract candidates do not cover the reviewed subject" |

- **The literal CLI on the lock with both units appended** stops at "missing or escaping regular file: SCRATCH-SOP2P/review.json". It fails closed, as for earlier units' SCRATCH pins. The overlay run is the binding result.
- `build_sop2.py --check` reports identical bytes for every generated file of both units, and `check_sop2.py` passes 37 checks at `b7b87b7`.

## Lead answers to the law's open questions 1 and 2 (Claude Opus 5.5, before sending)

- **Q1, the harness build: an optimized `harness` profile** (release optimization with debug assertions on), so Q6 measures optimized code. That activates 9 production `debug_assert!` sites, which is acceptable for harness measurement. The release artifact never carries the harness feature. **Rejected:** measuring a debug build, which would distort Q6.
- **Q2: O1-p may land before the held J4a.** The two `crates/platform/src/lib.rs` changes don't overlap, and the later of the two rebases. **Rejected:** holding O1-p behind J4a's §RW gate.
- **The two-unit S-OP-2 recording (S-OP-2-P, then S-OP-2-R) is accepted as a lead decision.** SDK4 and DRC aren't selected, so item 24's overrides need their parents selected first, following the `control-source-v1` precedent. **Rejected:** a one-unit record, which `verify_design` refuses.

If you disagree with an answer, that is a finding.

## Decide

**For the law (M3-O1 r1):**
1. **The decisions.** Is each lead decision in the table above sound on the cited text, and are the rejected alternatives right?
2. **Faithfulness to S-OP-2 r6.** Does item 5's division of S-OP-2 across O1's units leave nothing of items 1 to 17 unowned? Does any law item narrow, widen or contradict S-OP-2, in particular items 7 and 8 (mints that take an identity's fixed-width value; Q6), item 11 (finalization before rendering, with no carrier until S-OP-6) and item 12 (logging-start failure)?
3. **The SHA-256 choice (item 3).** Are the facts in its table right: what is locked, what each policy admits, and each option's edge effect? Is (e) the right choice (Q8)?
4. **The harness (items 13 and 14; S-OP-2b's text).** Is S-OP-2b's text precise and narrow enough to be drafted as a unit next? Does the phase vocabulary give Q0 §9.4's three checks a subject (Q0:946-951)? Judge Q1 (the measured build) and Q3 (overlapping provider phases).
5. **CH14 (item 1; Q4).** Is a record note enough, or does a new package need a CH14 passage successor?
6. **Enforcement (items 19 to 21).** Are the classes, the ratchet, the test-scope decision, `dispose`'s placement and the sweep's sequencing sound?
7. **Units (item 23).** Are the dependencies right, and is each "must not touch" list complete against the in-flight units' files? Judge Q2 (O1-p against J4a) and Q7 (O1-a's size).
8. **Anything else wrong**, including a citation that does not say what the law says it does.

**For S-OP-2-P and S-OP-2-R:**
1. **Faithfulness.** Are S-OP-2-R's two sentences exactly item 24's, insertion-only, with the original punctuation kept (SOP2:921-926)? Does the SDK4 sentence keep the doctor report's DR-114 tiers?
2. **The parents.** Is the finding right: neither SDK4 nor DRC is selected at `b7b87b7`, so item 24's record alone refuses?
3. **The selection.** Is S-OP-2-P, in `control-source-v1`'s form, a lawful way to select them, given SDK4's own `CANDIDATE-NOT-APPLIED` header? Does it select exactly the bytes APP pins, and nothing else?
4. **No supersession.** Is it right that no bound record overrides either passage, so plain overrides and `"supersededPassages": []` are correct?
5. **Binding.** Do both units bind, in order, after main's chain? Does any selected passage conflict?

## Output

Under `/tmp/opensip-implementation/reviews/codex-o1-law-r1/`. Do not commit, and run no cargo.
- **The law:** `REVIEW.md` and `review.json`, with:
  - `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
  - `"requiredFindings"`: a list, empty if you accept; each finding with an id, a location, the problem, the evidence and the fix;
  - `"nonBlockingObservations"`;
  - `"subjectSha256"`: `ac3f12fae691e2a9a9fa6c2fff264e3e3a5365fe36652d1bd58951ff1369d37a`, with the subject's path and bytes (73,886).
- **S-OP-2-P:** `s-op-2-p/REVIEW.md` and `s-op-2-p/review.json`, with:
  - `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
  - `"requiredFindings"` and `"nonBlockingObservations"`, as above;
  - `"subjectManifestSha256"`: `65af7fd35c9f5439d50d46e1b7769f7acee43c62c3436c6122c3b36f379f456f`, as one string;
  - `"supersededPassages"`: `[]`.
- **S-OP-2-R:** `s-op-2-r/REVIEW.md` and `s-op-2-r/review.json`, separate, with the same fields and:
  - `"subjectManifestSha256"`: `1d8e41be18a53dfd273cab0bb799bd95b07905caa8fddbb2e481bbe639425e4e`, as one string;
  - `"supersededPassages"`: `[]`.

**The verify_design review shape.** Each unit's `review.json` needs `subjectManifestSha256` as a single string equal to that unit's own subject; one review cannot map several subjects. A contract successor's verdict must be `ACCEPT-DESIGN-UNIT`, with `requiredFindings` empty. Neither unit is an inventory unit, so no `inventoryCandidateAssessment` is wanted. VD compares `supersededPassages` with the record's `supersedes` list by canonical JSON, so `[]` must be exactly that.
