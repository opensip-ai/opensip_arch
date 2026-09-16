**Verdict: ACCEPT-UNIT.** RF1 is closed on the subject-04 bytes and there are no new required findings. The acceptance covers only this adapter and its fixed macOS development host profile. It is not integration, install, hermeticity, release qualification or M1 acceptance.

Subject-04 hashes to `d25b7713…d3f2f` and all 87 files matched exactly before and after probing. Nothing was written outside `m1-generator-adapter-review-04`, and nothing was committed or pushed.

**What changed from subject-03.** No files were added or removed.
- **Code:** only `tools/generate_contracts.py` changed:
  - Node/Rust write grants exclude the root literal.
  - The device/inode of output, scratch and home is checked before each profile is built and after each child exits.
  - `owners.json` must equal the parent's own options byte-for-byte.
- **Tests:** three new ones.
- **Pins:** the closure and registry each have one updated digest.
- **Outputs:** the 8 generated files differ only in their provenance header; the bodies are byte-identical to subject-03.

**RF1, rerun end to end with the real parent and real steps:**
- **Subject-03:** the same generator stub still performs the exploit. The TS step read an outside file, created a file and overwrote the canary.
- **Subject-04:** the stub's own report shows chmod, rename, rmdir and symlink of the root all denied. The same TS step was denied every victim operation and nothing changed.
- **Controls:** with the real generator, the TS step is denied on both subjects. Run outside the sandbox, the stub does turn the root into a symlink, so it can do the attack.
- **Direct profile probe:** root rmdir and chmod are now denied, and every review03 denial still holds.
- **Parent guard:** a child can no longer replace a root, so I simulated a sandbox failure by mutating the roots outside the sandbox. In all four cases (output symlinked or replaced after the generator, scratch symlinked, home replaced) the parent refused straight away. No later step ran and the victim was untouched. My first run of this harness had a bug that stacked wrappers across scenarios; the logged results are from the isolated rerun.

**Other checks:**
- **Tests and drift:** all 78 tests pass with none skipped. A fresh drift check is clean at registry `4b1b4915…`.
- **Publishing:** `--write` restores corrupted outputs to the exact subject-04 bytes.
- **ADV3 (closed):** changed owner mappings from the sandboxed Python step are refused end to end, including identical data with different formatting.
- **ADV1 (closed):** the exports are documented as inert.
- **ADV6 (closed):** the correction record's hashes match the actual files.
- **ADV2:** accepted as the frozen-manifest route. I did not review binding4, and install still needs an accepted integration manifest that selects closure `2d64a8d8…`.

**New non-blocking advisories:**
- **DA1:** the real-sandbox regression test skips silently if there is no C compiler or `sandbox-exec`. A qualification run should treat that skip as a failure.
- **DA2:** the Python output root isn't in the identity check. No later grant depends on it, so this is only for consistency.

**Still required before product install:** an accepted integration manifest selecting the registry, closure and architecture anchor; complete protocol/report source owners; the inventory/design bootstrap binding; and other platform, resource-limit and release qualification.

Files are in `/tmp/opensip-implementation/m1-generator-adapter-review-04`:
- review.md
- review.json
- logs/
- work/
