# Fresh blind consumer B — OpenSIP M1 development subject

**Verdict: `ACCEPT-M1-DEVELOPMENT`**

This is not M6 release, platform, performance, or full-product qualification. The frozen tree is a development snapshot. Required M1 findings: none.

Subject manifest `docs/implementation/m1/trials/fresh-consumer-01/subject.json` SHA-256 `b2af45c40e54418daef5e005f4306d15fce313e598963764bcfbde4aad22f0e7` (33837 bytes). Archive pin `subject.tar.gz` SHA-256 `d0402feb4bc7e023d0bbacee0ea0c0d538e500f208acb3d483a579799cbef84f` (1306057 bytes). All 185 frozen files matched; no extras. Frozen product left unmodified. Work and mutations were confined to `/tmp/opensip-implementation/m1-grok-fresh-consumer-01/review`.

## Fresh session and blindness

`fresh-session.json` records Actual Grok 4.6 xhigh, `/Users/sb/.grok/bin/grok`, `newInteractiveSession: true`, no resume/continue flags, no prior findings supplied.

Not read: prior agent transcripts, author gap lists, ACTIVE-WORK, `docs/implementation` README/status/checkpoints, or previous consumer/review narratives.

`tools/verify_design.py` mechanically loaded lock-pinned approval/review/assent JSON and checked `ACCEPT` / empty required findings / pin joins. That is byte authentication, not a reread of those reviews' opinions. Selected successor records, coverage, inventory, metadata, and current-dispatch were read as current design. A workspace grep for UR-1 goldens accidentally printed one line of an M2 review file; that file was not opened and was not used.

## Reconstructed M1 obligations

Primary completion text is build-plan line 885 as overridden by `docs/implementation/m1/metadata-v2/successor.json`:

> Each build lane selects only declared inputs; help/version human and JSON metadata share the pure envelope projection without project/provider/store/network effects; version closure IDs come from the build-embedded metadata covered by the enclosing signed host/release artifact, not loaded components; independent identity vectors pass.

Deliverable: independent workspaces, generation registry/drift, minimal CLI parsing and command-scoped bootstrap. Commands: `help`, `version`, `completion`.

Current producer envelope is **command-envelope:7** (`current-dispatch.json` and product `schemas/sources/command-envelope-v7.schema.json`, SHA-256 `2cb6c8adaeeed4fc1b52573a291c1de5da512c0cf9ec1b1e0faa68313c4d436f`). metadata-v2's envelope4 remains a retained overlay; emitting major 7 is the later selected current dispatch, not a waiver of metadata semantics. Development metadata must use package version, `buildChannel=development`, empty `closureIds`, and no env/caller release switch.

Coverage still routes DR-G03/G15/G16/G31 to M1 *implementation owners* with `qualificationMilestone: M6`. Gate *execution* is not an M1 duty. Chapter 14 and the product README treat the 333-row inventory as a naming guide; missing later files are not empty-file M1 failures.

## Design lock

```
python3 -I -B tools/verify_design.py \
  --architecture /Users/sb/code/opensip-ai/opensip_arch \
  --implementation $PRIVATE_PRODUCT
```

Passed. 46 inputs, inventory successor chain to `repository-file-inventory.v10.json`, 10 contract successors, 40 generation sources bound. `productQualification: false`. Design-lock SHA-256 `11ec338400697dfb3e07288735b34bbbf6f3a0a6cbf38ba4f0d084d3ddbb200c`.

## Lanes

### Host / CLI

Host workspace members: `opensip-cli`, `opensip-contracts`, `opensip-host`, `opensip-identity`, `opensip-platform`, `opensip-reporting`. Rust provider is excluded. `cargo test --locked --offline --workspace --all-targets` passed (6 CLI startup, 2 request-authority, 15 identity, 3 platform filesystem, 4 reporting).

Independent CLI probes (cleared env, invalid `.opensip/config.json`, missing HOME/store/providers, `OPENSIP_*` release/closure spoofs):

| Control | Result |
|---|---|
| `version` / `--version` / `-V` JSON | envelope7 `kind=meta`, `hostRelease=0.1.0`, `buildChannel=development`, `closureIds=[]`, no project/run/errors |
| `help` / `--help` / `-h` JSON | catalogue `completion`, `help`, `version` sorted; `topic: null` at top level |
| `help version` / `help --help` | single-row topic projection |
| `help analyze` / `help default` | exit 2, `REQUEST.UNKNOWN_OPTION`, `errors=[]`, nonempty diagnostics, no `meta` |
| empty argv / `analyze` | development refusal, same D9 carrier |
| `completion bash\|zsh\|fish` | human-only scripts naming the three commands plus `# Termination: success` |
| `completion … --format=json` / `--format=html\|sarif` | `OUTPUT.FORMAT_NOT_APPLICABLE` |
| `--build-channel=release`, `--request-id`, env spoofs | ignored or refused; still development 0.1.0 |
| correlation 1..128 | projected; empty/129 refused; never replaces `req1_` |
| stdout EBADF | exit 4, `OUTPUT.SERIALIZATION_FAILED` on stderr, no second envelope |
| no HOME/store/provider files created | confirmed |

JSON envelopes shape-validate against envelope7 (Draft 2020-12; not the exact OpenSIP dialect). Human/JSON share the same catalogue and version fields.

Bootstrap allocates request identity before parse, opens no project/store/provider, and writes through a cloned stdout `File` so EBADF is visible. That is the M1 required-output path; `crates/host/src/delivery.rs` is not present and is a later full-product owner.

### Identity

`crates/identity` is `no_std`, canonical parse/encode plus H framing `opensip.product.v1 || 00 || D || 00 || u64BE(len(C(X))) || C(X)`. Independent goldens from identity-and-evidence §3 / admission UR-1–UR-5 matched `foundation/canonical.py` and hashlib, including non-BMP key order, integer bounds, combining vs precomposed é, escapes, surrogate refusal, and the four H vectors used in crate tests. `descriptors.rs` / `closure.rs` are absent; those are G31/M2–M6 descriptor admission, not the M1 canonical/digest demonstration.

### Generation

Selected generator `/tmp/opensip-implementation/m1-generator-build-05/opensip-contract-generator` and child Python `.../Python.app/Contents/MacOS/Python` hashed to `tools/contracts/toolchain.json`. Five wheels from `m1-python-wheel-provision-01/wheels` hashed to `python-wheels.json` and were materialized with `tools/provision_python.py` into the private copy (not the frozen tree).

```
python3 -I -B tools/generate_contracts.py \
  --architecture $ARCH --output $FRESH \
  --node $NODE24 --generator $GENERATOR --python $CHILD_PYTHON
```

Passed: 40 sources, 8 outputs, `changed: []`. Outputs are the six generated Rust modules, `apps/report/src/generated/report.ts`, and `providers/typescript/src/generated/protocol.ts`.

### TypeScript lanes

Node 24.16.0 pin matched `tools/typescript-lanes.json`. Offline `npm ci --ignore-scripts --no-audit --no-fund` on `apps/report`, `providers/typescript`, `tools/contracts`, and `tools/typescript-boundary` using the supplied cache. All 160 checker-closure files matched. `check_typescript.py` passed report, provider, and generator. A disposable copy with undeclared `apps/report/src/stray.ts` refused `config-include` and `undeclared-local`.

Report lane is bootstrap-only (`help-view.ts`, CSS, generated `report.ts`, TS 6.0.3, esbuild 0.28.2). TypeScript provider is generated protocol only. Full report UI and TS analysis are M4/M3.

Checker regression `node tests/run.mjs`: 233/234. The failing case is `.bin` shebang execution of `bin/check-boundary.mjs` (mode 0644). `check_typescript.py` does not use that path. Advisory, not an M1 blocker.

### Rust provider

Independent workspace/lock, path deps to contracts and identity, host lock unchanged. Offline build succeeded. Binary writes one stderr line, exit 1, empty stdout, does not wait on stdin, reads no project files. Native analysis remains M3.

### Cargo edges and contracts policy

Host and rust-provider `cargo metadata --locked --offline` plus `check_package_edges.py` against **inventory v10** (not the v8 example in `tools/README.md`) passed. Observed host edges are a subset of the inventory DAG (`cli→host→{contracts,platform,reporting}`, `reporting→contracts`). Extra inventory edges to unimplemented crates are not required to exist yet. Contracts dependency policy passed (11 checksums, 8 local source pins). Entropy backend override refusals: 5/5.

## Required findings

None. M1 isolated-build/contracts, declared-input lanes, identity vectors, and metadata CLI human+JSON behavior are present and independently reproduced.

## Later-milestone obligations (do not block M1)

- **M2:** replay, security session, storage commit/recovery.
- **M3:** real TS/Rust provider protocol and analysis; replace the Rust stub.
- **M4:** remaining commands/formats, report views, `delivery.rs` as artifact/browser owner.
- **M5:** remaining ~42 commands, lifecycle/trust/store.
- **M6:** all 32 gates, including G03 measurements, G15/G16, G31 `descriptors.rs` identity-namespace classes, signed release, performance.

## Advisories

1. Checker regression CLI-alias `.bin`/shebang case fails because `check-boundary.mjs` is 0644; Node-path invocations work.
2. `tools/README.md` Cargo-edge example still cites inventory v8; lock selects v10.
3. Coverage names `delivery.rs`, `projection_tests.rs`, and `descriptors.rs` at M1; behavior lives in other present files. Inventory is a naming guide.
4. CLI JSON was shape-checked, not exact-profile-checked. Renderer JSON is not identity `C(X)` (it has a trailing newline and a 4 MiB bound).

## What was not verified

No socket/NS proof of network silence; no G03/G15/G16/G31 harnesses; no Windows; no native analysis; no browser report; no release assembly; no claim that serde_json encoding is canonical identity JSON; no source-purity or complete dynamic TS closure.

Evidence lives under `/tmp/opensip-implementation/m1-grok-fresh-consumer-01/review/evidence/`. Machine record: `review.json`.
