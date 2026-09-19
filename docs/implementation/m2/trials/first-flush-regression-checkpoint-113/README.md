# Private first-flush regression113

Exact112 parent, one test-only change in platform/filesystem.rs: the existing native wiring test now invokes NATIVE_PUBLICATION on its deliberately non-directory socket and requires the actual F_FULLFSYNC EBADF. This implements actualClaude110 N1 and prevents replacing the production first flush with fsync while reporting FullFlush. The existing injected fallback EINVAL and real-directory controls remain. No production behavior, dependency, fixture or inventory change.

29platform tests pass; the compiled wrong-first-flush mutant is killed by the named test. No new whole-workspace/isolated-host qualification is claimed for this test-only addition.112 host66 remains exact112 evidence, not relabelled113. All other112 inherited findings/standing remain. One macOS development lane; no Linux/musl/hardware/power-loss claim. Actual independent113 scoped review still required; not installed or selected.

109 N3 wording: its embedded143 cases are value-equal to reference108; the compact constant is not byte-equal to the source JSON. The historical archive is preserved. Capture integration must distinguish admitted Absent from Present(empty bytes), which is malformed, and Unreadable, which is unavailable; codec errors cannot manufacture presence evidence. No capture integration is implemented in113.
