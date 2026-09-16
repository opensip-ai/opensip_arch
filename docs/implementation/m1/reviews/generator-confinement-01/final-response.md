I have a working confinement profile. All three real generator steps finish under a deny-default sandbox, their output matches unconfined runs byte for byte, and every negative control is blocked. Two full harness runs gave the same results (runs 03 and 04). The write-up with reproduce commands is `m1-generator-confinement-trial-01/profile.md`.

**Why Node aborted before.** Every failing diagnosis profile blocked reading `/` itself, and the macOS loader needs that at startup. Apple's `dyld-support.sb` allows it explicitly. Blocking it kills even `/usr/bin/true` (exit 134), and allowing it fixes both (`logs/hypothesis/result.txt`). `diagnosis-03/root.sb` only passed because `subpath "/"` includes `/`. Under deny-default I also found two Node-specific needs:
- **Parent-folder metadata:** Node resolves its script path, which reads metadata on every parent folder. Granting that for each allowed root's ancestors (not their siblings) is enough.
- **Pipes for stdio:** Node aborts when stdio is redirected to a file, and starts fine with pipes and stdin from `/dev/null`. I didn't find which startup call causes this.

**Profile.** `(deny default)` plus Apple's `system.sb`. Each step may run only its own copied executable, reads only its listed folders and writes only its output or scratch folder. There is no network, fork or other exec, and `/etc/passwd`, `/etc/master.passwd` and `/cores` are blocked. Steps run with a minimal env, cwd set to scratch, and piped stdio.

| Step | Can read | Can write | Result |
|---|---|---|---|
| Node validate-schemas | snapshot `tools/contracts` | scratch copy of inputs (this fixes NA5) | exit 0, 586 entry points checked |
| prettyplease Rust generator (links only libSystem) | `inputs` | output | exit 0, 6 files |
| Node generate-ts | `tools/contracts`, `inputs` | output | exit 0, 45 and 586 exports |

**Negative controls.** Each was also run unconfined, where every one succeeded, so each denial is real.
- **Blocked reads:** outside files, `stat` and folder listings (the trial, `work/`, `/private/tmp`), and `/etc/passwd`.
- **Blocked writes:** the trial root, `/private/tmp`, `/private/var/tmp`, and the inputs and snapshot folders. The harness confirmed nothing was created.
- **Links:** a hard link to an outside file was denied.
- **Network:** loopback TCP connect, UDP send and listen were all denied, and the test listeners received nothing.
- **Processes:** starting `/bin/sh` or re-running Node was denied, and so was launching an undeclared `/bin/sh` directly (exit 71).
- **Rust generator:** pointed at an outside input or output folder, it failed with a permission error (exit 101).

**What confined code can still do:**
- read OS files that `system.sb` allows (`/System`, `/usr/lib`, `/usr/share`, timezone data, `/dev/urandom` and similar);
- read metadata on parent folders of its allowed paths;
- learn the hostname, username and CPU count through system services;
- use more CPU, memory, disk or time than intended (only a timeout applies);
- create symlinks inside its write folders.

The symlink case is a **real bug in the candidate-03 parent.** A confined child wrote `generated/mod.rs` as a symlink to an outside file. candidate-03's output collection at `generate_contracts.py:255` follows links, and it returned the secret file's contents as generated output (`runs/symlink-exfil/`). The sandbox can't prevent this. The parent must refuse symlinks, hard-linked files and anything else that isn't a regular file before reading output.

**Limits of this trial:**
- **Mid-edit snapshot:** you were changing candidate-03 while I worked. Six closure pins were stale and `rustfmt.toml` was missing, so my snapshot is the working tree at that moment, not a verified closure. The Node hash was verified.
- **Different generator binary:** I used the format-trial prettyplease binary; its `main.rs` is identical to candidate-03's current source. The pinned `ec6bb9d8…` generator still depends on rustfmt, so I didn't use it.
- **Mechanism durability:** `sandbox-exec` is marked deprecated, and Apple labels `system.sb` as private and subject to change. The profile only holds for this OS build (macOS 26.6.2, 25G83) and should be re-tested after updates.

**Proposal for generator03** (details in `profile.md` §5):
1. Refuse non-regular output entries before collecting, and open files without following links.
2. Run each step under the per-step profile, built from real paths, with pipes, a timeout and a minimal env. Fail if the sandbox tooling is missing.
3. Switch to the prettyplease generator, which removes rustfmt and the four Homebrew libraries from the closure.
4. Optionally run the probe as a per-host self-test before generating.

`adapter.py` and `prepare.py` still run inside the unconfined Python parent. I propose moving `prepare` into its own confined Python child, but that is untested and needs a separate trial. The external verifier anchor stays with you.

Everything is inside `m1-generator-confinement-trial-01`: `profile.md`, `scripts/` (snapshot prep, harness, probe), `logs/` and `runs/`. Nothing was written outside it, and there were no commits or pushes.
