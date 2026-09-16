A confined Python child now runs `source/prepare.py` under the same deny-default + `system.sb` profile shape as trial-01. Its three prepared files are byte-identical to the unconfined results. I ran the whole pipeline end to end three times with the same results. Nothing was written outside the trial directory, and nothing was committed or pushed. The details are in `profile.md` and `logs/summary.md`.

**Interpreter.** The child is Homebrew Python 3.14.6, run as `Resources/Python.app/Contents/MacOS/Python` with `-I -B -S`, an empty environment and piped stdio.
- **Why not the other two:** Homebrew's `bin/python3.14` is only a launcher that starts that binary as a second process, which the sandbox refuses. `/usr/bin/python3` is a shim that re-execs the Command Line Tools Python.
- **Exact grants:** the executable and framework dylib (both pinned), 25 stdlib `.py` files, 3 extensions (`_json`, `fcntl`, `grp`, each linking only libSystem), and directory listings for 7 stdlib directories.
- **Also granted:** metadata on the `os.py` landmark (without it every run printed a prefix warning) and on ancestor directories.
- **Not reachable:** site-packages, `__pycache__`, and any other stdlib file.
- **Derivation:** `scripts/pin_python.py` finds the list by running the real entry confined and tracing its imports. It fails if anything resolves outside the pinned stdlib.

**Entry (`prepare-inputs.py`).**
- It refuses to run unless the isolation flags are set.
- It reads the raw schemas and options without following symlinks, and indexes the schemas by `$id`.
- It executes `prepare.py` directly from its bytes and runs `prepare.prepare`.
- It creates only `owners.json`, `rust-projection.json` and `ts-projection.json` in the empty output root.

I checked the filenames: `prepare.prepare` also writes `targets.json`, but nothing reads it, so the entry drops it. The entry's in-memory interception is not a security boundary; your collector is.

**Positive result.** Two confined runs and one unconfined run each exit 0 and pass candidate-03's `collect_outputs`. Their outputs are byte-identical to a direct `prepare.prepare` reference and to trial-01's prepared inputs. The work tree was unchanged afterwards.

**Negative result.** Each confined denial below was ALLOWED in an unconfined control. The exception is four paths outside the trial, which I only tried confined and then confirmed were not created.
- **Reads denied:** the canary, the `source/` copy, candidate-03, the unselected `runtime/patterns.ts`, unimported stdlib, `.pyc` files, site-packages, `/etc/passwd`.
- **Writes denied:** inputs, code, the entry, the output root itself (rmdir/chmod), `/tmp`, and the stdlib.
- **Processes and links denied:** fork, spawn and `exec /bin/sh`, and hard links.
- **Network:** with `_socket` deliberately granted, loopback TCP/UDP was denied and the test listeners saw nothing.
- **Collector:** after a probe planted a symlink and an extra file in the output root, candidate-03's collector refused the output.

**Remaining limitations:**
- **Output root:** the child can create symlinks and extra files there. Only your lstat/`O_NOFOLLOW` collection of the three names makes that safe.
- **Self re-exec:** the child can re-exec the interpreter, because the sandbox needs that exec grant to start it. I showed the new process is still confined.
- **Syslog socket:** connecting to `/private/var/run/syslog` is allowed by Apple's `system.sb`. The child can't reach it with the exact grants only because no socket module is readable.
- **Executable-mapping grant:** `file-map-executable` is not enforced on this OS build (macOS 26.6.2, 25G83). What actually stops other native code from loading is the read grants.
- **Native closure not proven complete:** I trust the pinned dylib, CoreFoundation and the system library cache.
- **Homebrew files:** they are writable by your user, and pins are checked before the run, not atomically at exec. The framework can't simply be copied, because its library paths are absolute.
- **Script mode only:** `-c` fails under these grants, because Python 3.14 imports `linecache` for it.
- **Evidence:** kernel denial logs are deduplicated, so the conclusions rest on return codes and parent-side checks, not on the logs.
- **Brittleness:** the grants break on any Homebrew or OS update, or if `prepare.py` gains an import. That fails closed, and you need to re-run `pin_python.py`. `sandbox-exec` is deprecated.
- **No resource limits:** only a timeout applies.

This is not an approval claim, and external bootstrap anchoring stays with you. `profile.md` §6 proposes how to integrate it, including no unconfined fallback; I haven't applied it.

To reproduce, from the trial directory:
```sh
python3 -I -B scripts/build_work.py
python3 -I -B scripts/pin_python.py
python3 -I -B scripts/run_trial.py
python3 -I -B scripts/summarize.py
```
