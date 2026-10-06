# S-P preliminary feasibility r1 — ACCEPT

This accepts the architecture-only S-P record dated 2026-10-05. The `rustc_driver` callback shape and the TypeScript compiler API work on this host when each one is paired with one coherent retained prototype toolchain. The record does not change a product file, a contract, an inventory, or the production toolchain, and it does not sign off an owner item.

## Subject

The staged report is `/tmp/opensip-implementation/s-p-report/docs/implementation/m3/spikes/s-p-2026-10-05`. All 30 architecture files match `subject.json`. The subject manifest is 6337 bytes, sha256 `6b59c0b7d46895c954466712137bec1ea24ae5f6e4145d129e192637ed71e3e2`, and it lists the same 30 files. Authorities match: `M3-PLAN-r10.md` `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`, provider L r5 `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`, `FETCH-SPEC.md` `4ebe90a491721e48d252f11e6378b6c73312b506b59af89b24c03829416f8858`, and the T2 documentary manifest `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`.

M3-S asks whether the pinned toolchain can host a `rustc_driver` sidecar and whether Node and TypeScript can load from a closure path. It is preliminary and makes no Q6 claim. G2 authoring follows S-P; G2-v remains the later launch. P5-8 keeps lead run sets serialized, with S-P between sets. Provider L item 9 uses S-P only as the condition for SM-3's callback readiness. This record does not fill an S-M figure.

## Acquisition

The retained official `rustc`, `rust-std`, and `rustc-dev` archives match the hashes in `evidence/rust-component-pins.json`. The rustc-dev hash equals the channel pin. Node 24.21.0, TypeScript 6.0.3, and the unused TypeScript 7.0.2 archive match their pins. The executed API package is TypeScript 6.0.3. No command in the verified set names 7.0.2.

The two inputs are development entries, `heldOut` false: `rs-small-http-body` at `929ff1c456c6cfe7a984e8d4bd70f506cbd9c78c` and `ts-small-constructs` at `8264e196c3593a192dc79991f4d97c22ab4c08bf`. Their admission receipts name the accepted manifest digest. Offline `store.verify` on the retained trees matched both the QD-22 digest and the content digest. The analyzed bytes match the report: `http-body/src/size_hint.rs` is 5628 bytes, sha256 `896ec9bfb8fdecd94b33c2d235db1811dc2c1274524741fc09a6264e9440c3c6`, and `src/metadata.ts` is 422 bytes, sha256 `dafb83aa6fba98073b877cca10aba0558c3dbf4a8af259b912164e7b72e7de34`. The report tree does not vendor corpus source.

## Rust profiles

The installed Homebrew compiler is Rust 1.95.0, commit `59807616e1fa2540724bfbac14d7976d7e4a3860`, LLVM 22.1.3. Its import probe, run at nice 10, reports E0463 and E0554 with no bootstrap override, and E0463 again when `RUSTC_BOOTSTRAP` is set. The minimal pin has no `rustc-dev` libraries. That profile does not host the wrapper.

The coherent official distribution reports the same commit and LLVM 22.1.2. `probe/s-p-exclusive.py` removes `RUSTC_BOOTSTRAP` from the base environment and sets it only on the wrapper compilation. That compilation exits 0 with an empty log after `SDKROOT` is set to the recorded macOS SDK. The later analysis processes use the base environment. They reach `after_expansion` and `after_analysis` on the local positive control and on the exact `size_hint.rs` module, then stop. The negative control prints `after_expansion`, then E0308, and exits 101 without `after_analysis`. The TypeScript program's library files are separate; the Rust run's only repository input is that one module.

The mixed profile compiles the same wrapper with the Homebrew `rustc` and the official sysroot. `probe/homebrew-mixed-build.log` is the recorded output and begins with E0514: crate `std` was compiled by an incompatible rustc. The build exits 1, and `callbackPassed` is false. The shared version and commit do not make those components interchangeable.

## Node and TypeScript

The verified Node binary prints `v24.21.0`. It loads `typescript-api/package/lib/typescript.js`. The probe log for the local positive control and for `metadata.ts` reports compiler 6.0.3, `createProgram`, and no diagnostics. The constructs program has 64 source files: that module plus 63 compiler libraries. The negative control reports diagnostic 2322 and the command exits 1.

## Lane

The verified set held `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock` from 2026-10-06T06:56:22Z to 06:56:24Z, recorded no other build, and wrapped every invocation with `nice -n 10`. The mixed-build control held the same directory from 06:58:00.878Z to 06:58:00.916Z, also with no other build, and its recorded command starts with `nice -n 10`. Each script removes the directory only when that process created it. The directory is absent now. This review did not create or remove a lock and did not run Cargo. `~/Library/Application Support/OpenSIP` is absent.

## Consequence

The demonstrated API is the callback pair on one coherent official 1.95.0 compiler, stdlib, and dev distribution, and `createProgram` on Node 24.21.0 with TypeScript 6.0.3. G2 authoring can target that shape and has to specify the matching build and runtime packaging in its own review, including component byte pins and the private-feature setting used to compile the wrapper. This record does not accept G2, change the production Rust pin, measure S-M, approve D13, O7, or D12, release L, or qualify a language cell.
