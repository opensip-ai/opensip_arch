**Verdict: changes-required.** I found four new required findings and nine advisories. The write-up is in `m1-native-wire-owner-review-03/review.json` and `review.md`, with probes and outputs under `scratch/`.

**My mistake, now fixed:** while checking custody at the start, I ran two subject tool modules with plain `python3` and bytecode writing still on. That wrote two `.pyc` files into the frozen subject, which the after-check caught (66 files). Their timestamps matched my scripts, so I deleted just those two files and the empty `__pycache__`. A re-check that loads nothing from the subject shows 64/64 files and 36/36 pins, and no manifest-listed byte changed. None of my test runs read those files. The review records this.

Separately, one oversized probe of mine was moved to the background automatically when it hit the command timeout. I stopped it and reran a smaller version normally; nothing from the background run is used.

**Reproduction:** I copied only the 35 declared inputs, without `subject-files.json`, and ran them in isolation with the reference Python (`-I -B`) and my own TMPDIR.
- `check.py` gives 373 checks, 0 failed, identical to the frozen output.
- `selftest.py` catches 78/78. That is my own run; root's run isn't claimed.
- Custody before and after: all 64 files, all 36 pins (12 modified and 11 untracked against HEAD `c3856824`) and the Node pin match. The 24 `prior/` files are byte-equal to their originals.

**Prior findings:** the six review-01 fixes and review-02's RF-1 to RF-3 and A-1 to A-7 are resolved, some with leftovers that feed the new findings.

**Independently confirmed:**
- **Pattern sites:** my own walker finds exactly 54 sites (13 patterns) and 53 lowerings, and the lowering rule is correct for those patterns.
- **Byte arithmetic:** my own CBOR length code matches the owner encoder on 216 real frames. It reproduces 67108864, 9663676416 (9222 frames), the 6834-byte small request and the 796198 frame bound, without allocating GiBs.
- **Excluding the 40-byte prefix** is written owner law in rust2, not an author choice.
- **Reserving one Cancel** is justified: only one Cancel is allowed, it counts toward request totals, and reserving it keeps an interrupt at exit 130.
- **The two new detail codes are needed.** The owner's failure-envelope code requires a registered detail code even when the termination carries none, and no existing code fits honestly.
- **The new `admitted-plan-input` origin is also needed:** none of the five existing values describes repository or lockfile input.

**New required findings:**
1. **Hidden `..` segment in wire paths.** The owner path pattern can't see past a newline, so `x\n/../../escape.rs` passes. The owner prepared-set admission and the carrier both admit it (generated-file path, and `crateRootPaths` in OpenUniverse). The segment rule covers only one of the six places this pattern is used.
2. **ECMA vs owner Python `re`.** `a/..\n` and `..\n` are legal dependency file names that the declared rules and the carrier accept. The owner's dependency-set and prepared-set admission crash with an untyped `ValidationError` on them, and the new wrapper inherits the crash: no admission, no refusal, no route. One final owner must be chosen.
3. **Prepared route row contradicts the code.** The row says "explicitly selected", but an over-limit set is refused in defaulted mode too. Changing the code to refuse only in explicit mode fails 0 checks.
4. **Planner chunking doesn't bind the sender.** Nothing requires the host to send the greedy chunks it planned, so a host using smaller legal chunks could exceed the totals after acceptance. Greedy chunking also isn't the smallest in bytes: the owner encoder gives `[6,24]` 457 bytes against greedy's 458.

**Advisories include:**
- **A-1:** the two limit keys use `REQUEST.PRECONDITION_FAILED`, while the owner's existing over-limit routes use `REQUEST.UNSATISFIABLE`.
- **A-2:** four of my mutants fail 0 checks: swapping the two envelope codes, a wrong remedy text, moving the dependency refusal's timing, and changing the origin's meaning.
- **A-4 to A-6:** three more untested gaps, each shown by a 0-fail mutant: the TS2 frame boundary, the Seal's chunk count, and a newline plus `..` dependency path at set admission.

**Limits:** no generator or production codec was run. The Rust regex crate isn't available offline, so lowering needs were judged from its documentation. The P3 race model, commitment classes, scope2 and field coverage were not re-derived.
