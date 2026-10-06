# X3c-3 clean-assembly integration verification r1

Verdict: ACCEPT-UNIT.

This is evidence for the pending clean-assembly RC verification on accepted descendant `1968cd6871333e3faed061f8c8ed627733321cfe`. It is not evidence that these tests ran on original commit `43ea32a6419c961cec1e0ba30d7dd791acbd7f49`. That commit is an ancestor of the current product HEAD. The accepted X3c-3 product unit, O1-p, prior G2 and K1 units, and the X9 metadata follow-up stay closed. No product path changes, so no inventory successor is required.

## What was verified

The subject manifest is 4321 bytes, sha256 `3589f8f8b025a24c6a21c8fa9c1235d70fd3ca6a1a18b6447ae944b07c38460b`. All 20 members match their byte counts and digests. The architecture HEAD is `83536c99d447b47393080dd7c31df13897489145`. The product HEAD is `1968cd6871333e3faed061f8c8ed627733321cfe` and the worktree is clean. Pinned authorities, product inputs, `design-lock.json`, and the featureless release binary match `source.json`.

Fresh `census.json` files for storage and host are byte-identical to the accepted RC censuses (`b4c6553fe04f5f7e089a947d4a407437dee6e507fb7716edeabe2e6378fd5958`, 21527 bytes; `2492cbd0e796712de3011ecbfc9253fdfabc821c45614c9eb4ed32d0802498ee`, 18020 bytes). The required-run fixtures contain 403 storage rows and 98 host rows.

`checks.py` holds one lane lock across each phase, waits until named compilers and test binaries are idle, uses a private mode `0700` TMPDIR, and checks HEAD and a clean worktree around every command. It does not assign `HOME`. Recorded commands are sequential: featureless `cargo build --release -p opensip-cli` at nice 10, exit 0; release-absence scan at nice 10, `passed` true and `found` empty; both release `--features crash-matrix` builds at nice 10, exit 101, each log carrying the test-only `compile_error`; census-only storage then host at nice 0; two whole lead repetitions at nice 0, storage then host in each, with the lock held for both targets of a repetition; then the real checker at nice 0. The recorded scratch directory is still mode `0700`. The OpenSIP support directory is absent. The four lead output directories and both census directories are present. Each lead `matrix.json` records this clean commit, with 403 storage runs and 98 host runs, and limits L1 through L11.

The archive was streamed and not extracted. Its 1020 regular members match `matrix-evidence-members.json` exactly. Every name is under `runs/` or `census/`. No scratch database, source file, test binary, or installation member is present.

The pinned Python 3.14 checker was rerun read-only with `-I -B` at nice 10 over the four lead directories and the pinned commit. Its stdout is byte-identical to `matrix-check.log` (59428 bytes). The report is `passed` and `matrixPass` true, `productQualification` false, commit `1968cd6871333e3faed061f8c8ed627733321cfe`, 501 runs, repetitions agreeing, 323 union census points, kill set 389, and killed points outside that set exactly `x3c.object/file-barrier.before#41` and `x3c.object/file-barrier.after#41`. Limits are L1 through L11.

## Boundary

No new code is accepted. J4a and RW were not integrated. O1-a law completion, S-OP binds, and owner decisions stay open. The design lock is unchanged. Provider launch did not occur. Whole-product qualification remains false.
