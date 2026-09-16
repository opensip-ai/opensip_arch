# Independent Grok review: combined generator03

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-combined-generation-subject-03`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/combined-generation-03/subject.json`
**Manifest SHA-256:** `bfdfcdc0e123fabf5ed67c0cab5056044a04b261e06e8cefbeef16e902236527`
**Members:** 506
**Archive:** `f9b10761594d2dd8dd17e352b77d10b201870f822ee112758b8463d65452db43` / 6323800 bytes
**Verdict:** **ACCEPT-UNIT**

This accepts only the frozen combined-generator03 development pipeline: seven confined child phases, snapshot of regular unlinked inputs plus copied Node/generator/formatter bytes, pinned Python 3.14.6 `-I -B -S` native/prep profiles, bounded 8MiB/300s capture with process-group kill, and eight generated contract files. It does **not** select a product generator/registry, approve source semantics, qualify portable hermetic release, close package-archive provisioning, or activate product bytes. Existing product generated files came from generator02 and are not replaced by this review. Mutable04 (remove 15 installer-metadata files; fold formatter into the generator) is a later subject and is not approved here.

## Custody

506/506 listed files and the adjacent `status.json` archive digest match before and after. Frozen subject was not executed against. Private exact copy of listed files only under `review/copy`. Product and architecture trees were not edited.

`local-tools.json` was used as explicit pinned existing tool paths, not as provisioning authority. Live bytes matched `toolchain.json`:

| Tool | Path | SHA-256 |
| --- | --- | --- |
| node | `/Users/sb/.nvm/versions/node/v24.16.0/bin/node` | `1ee75375…c4b8` / 120573328 |
| generator | `/tmp/opensip-implementation/m1-generator-build-04/opensip-contract-generator` | `0a49cfc4…768e` / 7201824 |
| formatter | `m1-native-wire-integration-candidate-01/formatter/.../opensip-native-integration-format` | `76cc5946…aca7` / 3686800 |
| python | Homebrew CPython 3.14.6 framework executable | `0c9a9857…a3af` / 51392 |

## What this unit is

`tools/generate_all.py` stages 40 current source-v3 schemas / 857 roots into six Rust and two TypeScript files. Inputs under `schemas/` and `tools/` are snapshotted as regular, unlinked, nlink=1 files before any child runs. Node/generator/formatter executable bytes are copied after pin check (`chmod 0700`). Python is the selected installed framework with explicit file/library/alias pins; no package install or network provisioning occurs.

Seven Seatbelt children, deny-default, cleared env (`PATH=/usr/bin:/bin`, owned `HOME`, `LANG/LC_ALL/TZ`):

1. Python preparation (`-I -B -S`, 28-file prep profile)
2. Node schema guard
3. Rust generator
4. TS generator
5. Native Python renderer (`-I -B -S`, 142 observed stdlib files + 5 native libraries + 6 canonical alias pins; 143 vendored package files verified inside the child)
6. Standalone Rust formatter (this freeze’s old formatter binary)
7. Node native TS assembler

Parent-created output-root identities are checked before/after each child. The inherited nofollow collector refuses linked/nonregular/undeclared/oversized outputs. Observing the input closure is not external semantic approval (`sourceApproved: false`). System dyld/kernel/loader remain trusted. Malicious same-process trusted parent/compiler/kernel is outside this boundary.

## Capture (`tools/contracts/confine.py`)

`capture_child` uses parent-owned pipes (`close_fds=True`, `start_new_session=True`), one 8MiB combined budget and 300s default. Overflow or timeout sets a failure, SIGKILLs the process group, and reaps. Retained logs are bounded prefixes. This is the run04→run05 fix: run02/03 aborted Node initialization because inherited parent log-file FDs were outside the child’s grants; HOME did not fix it; pipes did. That abort stack is preserved in freeze `run02`/`run03`.

Native alias refusal01 is preserved (`native-confined01`: OpenSSL `libcrypto.3.dylib` loader alias blocked). Exact verified alias + ancestor-metadata grants are in the current native profile (six aliases including `/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib` → cellar target).

## Reproduction (private copy)

Python 3.14.6 `-I -B` (isolated, not optimized). Node v24.16.0. TypeScript 6.0.3 from `m1-joint-generation-candidate-03`.

```
Python -I -B copy/tools/generate_all.py \
  --root copy --output review/generation-01 \
  --node <pinned> --generator <pinned> --formatter <pinned> --python <pinned>
```

**Result:** `{"passed": true, "sources": 40, "outputs": 8}`. Input-closure digest `fc281ef8…7c83` / 69879 bytes **equals** freeze `run05`. All **eight** output SHA-256/bytes **equal** freeze `run05/assembly/output` (including `report.ts` `fa224b23…08c6`). No provenance-only split was required because the input closure matched. `sourceApproved`/`confinementQualified` remain false. `allChildrenSeatbelt` true.

Strict `tsc --exactOptionalPropertyTypes` of both generated TypeScript files: exit 0.

Supplied `check-capture.py` writes `capture-controls01.json` beside the subject; supplied `check-node-boundary.py` assumes `run05/tool-node`, `run05/runtime`, and `outside-secret.txt` (not in the 506 listed files). Private harnesses were used instead, writing only under `review/results` and `review/generation-01`.

## Independent probes

**Capture (8/8)** including the original six plus: grandchild in the same process group is killed on timeout; child environment is only what the parent passed (no `HOME`/`PYTHONPATH`/`PYTHONHOME` unless provided).

**Collector/root identity (8/8):** extra file, symlink output, missing declared path, byte limit, and replacing a parent-created root with a symlink all refuse.

**Node validation profile (5/5 + outside write absent):** outside read/write/network/`/bin/sh` spawn refuse with EPERM; owned `runtime/` write allowed.

**Native python profile:** unselected `sqlite3`/`logging` absent; network and outside read EPERM; owned `native-work/` write allowed; `sys.path` has no `site-packages` and `PYTHONPATH` is unset. `import site` succeeds because CPython 3.14 ships **frozen** `site` (`spec.origin == frozen`) while `-S` still disables site initialization (`ENABLE_USER_SITE is None`). That is trusted-interpreter behavior, not an ambient site-packages load. Probe `native-site-module-absent` was a false expectation and is not a product defect.

Live `confine.verify_runtime` of the native profile: 148 unique canonical files. Vendored `python-packages/` **143/143** match `python-packages.json` (5 distributions: attrs, jsonschema, jsonschema-specifications, referencing, rpds-py), including installer metadata this freeze deliberately keeps.

All seven generated `*-profile.sb` files contain `(deny network*)` and no `(allow network`. No `/Users/` paths. Homebrew literals appear only on the pinned Python/OpenSSL/xz/zstd cellar/opt aliases. Confinement runtime pins (`SystemVersion.plist`, `dyld-support.sb`, `system.sb`, `/usr/bin/sandbox-exec`) match live bytes.

## Must-fix / should-fix

None in this development-pipeline scope.

## Advisories (non-blocking)

- **C-01:** Native Seatbelt grants `subpath` of the whole `tools/contracts` snapshot, which is wider than the 143 package files. The child still verifies the package snapshot byte-for-byte before `sys.path.insert`. Not ambient site-packages.
- **C-02:** CPython 3.14 frozen modules (e.g. `site`) remain importable under `-I -B -S`; disk-unpinned stdlib such as `logging`/`sqlite3` does not. `-S` still prevents site initialization.
- **C-03:** This is a macOS development host profile (Homebrew CPython 3.14.6, system.sb, dyld). It is not portable hermetic release qualification.
- **C-04:** Parent `generate_all.py` is trusted and unsandboxed by design. Same-process malicious parent/compiler/kernel is out of scope.

## Preserved failures

- `native-confined01`: OpenSSL loader alias blocked despite canonical target pin; fixed in profile02.
- `run02`/`run03`: Node abort while initializing stdio against inherited parent log FDs; run04 first full success; run05 adds bounded capture.
- `run01` confined only native Python.
- `metadata`/installer files in the 143-file snapshot are intentional for 03; 04’s later deletion is not this subject.

## Remaining (not completed, not disguised)

Package/tool build provisioning receipts; exact product schema registry and approved tooling filenames/bootstrap/policy integration; folding the formatter into the generator (04); fresh blind consumer B; M1; release; replacing product generated bytes. Codex may continue final provisioning/registry integration separately. This bounded foundation can feed that work; it is not product activation.
