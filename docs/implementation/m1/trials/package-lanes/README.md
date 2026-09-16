# Package-lane trials — incomplete

The pnpm11.10.0 per-lane experiment materializes pinned dependencies and repeats
frozen offline installs in separate source copies. Locked dependency drift is
refused. Trial04 now passes both provider/report compiler builds and emitted BigInt execution;
no package-manager/version or final lock topology is selected by these receipts.
No TS package/configuration has been added to the product repository.

Observed sequence, with the original failed calls retained:

-01: `pnpm run build` performs an implicit install after the explicitly prepared
  store differs from the default invocation store, then executes the deliberately
  failing postinstall sentinel. An install-only `--ignore-scripts` is insufficient
  to keep a later build from acquiring dependencies/running lifecycle scripts.
-02: lane-local `verifyDepsBeforeRun: error` and `ignoreScripts: true` are read by
  config inspection, but `install --ignore-workspace` skips that local configuration
  too; the sentinel executes. Use an explicit lane-local workspace boundary, and
  do not discard the configuration by blindly adding that flag.
-03: explicit install flags and a local empty-membership workspace give successful
  frozen offline installs. The first build syntax used a store option unsupported
  by `pnpm run`; the fixed invocation uses `--config.store-dir`. That reaches a
  pnpm internal failure: `opts3.currentPnpmfiles is not iterable` with
  `verifyDepsBeforeRun: error` and `ignorePnpmfile: true`. No compiler build success
  is claimed, and negative build refusal alone is not a valid drift proof when the
  unchanged positive build also fails.

Next: trial a compatible pinned manager/version or an explicitly justified build
adapter, then prove both positive isolated builds and meaningful negative controls,
including root/sibling input rejection. Compare the shared-lock alternative before
selecting the final policy. Materialization used registry acquisition; offline
install mode and scripts sentinels are bounded observations, not OS-level egress
tracing or sealed toolchain evidence. Official current settings documentation
redirects11.x to12.x; actual installed11.10 behavior governs these trials.

Trial04 disables the broken automatic pre-run check and requires an explicit
frozen offline install followed by the requested build. The initial compiler call
then reports TypeScript7's requirement for an explicit rootDir. After setting
rootDir to src, both builds pass and their emitted JS preserves9007199254740993n.
A deliberately changed dependency refuses at the explicit frozen-install step.
Original failed04 commands and before-rootDir configurations remain retained.
This supports a candidate explicit install/build adapter; it does not establish
that plain `pnpm run build` independently checks dependency drift. Root/sibling
rejection, full isolated-source closure and shared-lock comparison remain pending.
