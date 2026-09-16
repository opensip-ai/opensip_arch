**Verdict: CHANGES-REQUIRED.** There is one required finding, and it is a small confinement fix. With it fixed and a real-sandbox regression test added, the evidence supports **ACCEPT-UNIT** for the concrete adapter and the fixed macOS host profile after a narrow delta review. I don't claim the host is hermetic or that the unit is product-, runtime- or release-ready.

The frozen subject hashes to `ff8c3985…4ef` and all 87 files matched exactly before, during and after probing. Nothing was written outside `m1-generator-adapter-review-03`, and nothing was committed or pushed.

**RF1: the TypeScript step's sandbox grant can be redirected by the Rust generator step.**
- **Cause:** in `generate_contracts.py:72-81` and `:394-405`, the Node/Rust profile lets a child delete its own output root. The parent then builds the next step's profile from `Path(output).resolve()`.
- **Demonstrated:** I used a generator stub that replaces `work/output` with a symlink to an outside folder. A TypeScript child that targets that folder then read an outside file, created a file and overwrote the file. Under the real generator the same child got EPERM on all three.
- **Limits:** the parent still refused to publish, but only after the outside write had happened. The unmodified `generate-ts.cjs` got EPERM, so this needs a hostile TypeScript step, not just a hostile generator.
- **Fix:** exclude the root literal from the write grant, as the Python profile already does, and check each root is still the directory the parent created before building the next profile. Separate roots per step are better still. I tested the one-line `require-not literal` change in a copy: it blocks the escape, and real generation still produces the frozen output bodies.

**NR1 and NR2 are resolved.** NR1 is refused through the real `--write`, including a nested `$ref` caught inside the sandboxed Python step. NR2 is refused with real `cargo metadata`.

**Everything else checked out:**
- **Tests:** 75 pass: the claimed 46 plus 29 design-binding tests. A fresh drift check of the 8 outputs is clean and prints one JSON line.
- **Sandboxed steps:** in the native probe, the Python step and Node step 2, outside reads and writes, writes to inputs, hardlinks, network (including syslog and DNS), fork and exec were all denied. Symlinks and FIFOs a child can create in its output are refused by the parent. The Python step can't import unpinned modules and has no fallback.
- **Guards and publishing:** 23 malformed Python-profile and sandbox-config mutations refuse before any step runs, as do bad host-profile, native-library and extra-directory changes. A hardlinked destination is replaced without touching outside bytes, and a symlinked output directory refuses before any write.
- **Build:** a Cargo config in an ancestor directory is refused. A clean offline build with network denied succeeds and records the same receipt fields. Its binary hash differs, as disclosed, but its 8 output bodies are byte-identical to the frozen ones. All 25 crate archives match; prettyplease is benign.
- **Report facade and witnesses:** every unselected or superseded ref is refused. Strict `tsc` passes, 1338/1338 witnesses match in TypeScript, and the Rust roundtrip has 0 failures.

**Selected-input generation obligations** are met within the explicit trusted base (parent Python, kernel, `sandbox-exec`, system libraries, pinned Python and Node), apart from RF1.

**Bootstrap check still needed before integration:** a reviewed design-lock/inventory successor has to select these hashes:
- registry `4cf6dbd5…`
- generator closure `3473abef…`
- options `1719ef18…`
- source map `561cf9ef…`
- generator binary `0a49cfc4…`

It also has to pin the 28 architecture sources to a committed revision. All 28 match the checkout's current files, but at HEAD `c3856824…` 22 of them are untracked and 3 are modified.

**Advisories (6):** `report.ts` still exports the general `SchemaRegistry`; the parent doesn't check the Python step's `owners.json` against its own options; the build-receipt check is narrow; there are no CPU, memory or disk limits; the witness record names the wrong corpus hash. The sixth is the uncommitted architecture sources above.

**Not covered:** the timeout was reviewed in code but never triggered, Clippy/fmt weren't re-run, NA4 wasn't re-checked, and no platform other than this Mac was examined.

Files are in `/tmp/opensip-implementation/m1-generator-adapter-review-03`:
- review.md
- review.json
- logs/
- work/
