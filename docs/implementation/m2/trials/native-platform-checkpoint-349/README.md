# Native macOS profile observation integration — private candidate349

This candidate connects verified signed-profile evidence to actual native boot, loader and installation-root filesystem measurements. The constructor accepts the verified profile and a borrowed retained installation fence. It does not accept observation JSON, a replacement loader path, an asserted platform name or caller boot flags. The original loader File/path and profile remain owned; the same installation fence is borrowed through consumption.

**Standing:** conditional native measurements, not selected installation/current authority, independent SSV or loaded-image proof, release qualification or a writer grant. The profile verifier still relies on supplied root/core-pin/revocation provenance. The existing signed test profile explicitly remains SYNTHETIC even where its measured values match this development host. M2–M6 remain open; product fa72e50 remains unchanged/uninstalled. No pushes.

## Changes

- `platform/macos_process.rs`: fixed read-only `sysctl.proc_translated` with a four-byte integer buffer. Exactly0=reported native,1=translated; Apple's documented ENOENT fallback is separately represented as native-selector-absent. Unexpected size/value/return/error fails. No helper or subprocess.
- `security/trust/native_platform.rs`: refuse translated processes and mismatched loader/process CPU family; gather native347 boot and348 fixed system loader; sample346 actual I-root and loader descriptors. Require local nonunion installation root and local nonunion read-only APFS loader. The existing verified-profile decision checks the exact installation-root FS name and boot/identity fields.
- Native evidence owns the derived seven-field observation and decision and rechecks original fence/loader, boot, process and both descriptor filesystem samples before return and on later consumption. Read-only filesystem flags are an acquisition precondition for the accepted sealed-volume premise, not proof of a seal. These sequential observations are not an atomic snapshot or protection against hostile trusted code/ABA.
- Existing caller-assertion `ConditionalPlatformEvidence` stays explicitly conditional and unchanged. Presence of `ExactMeasured` tier alone is not admission: refusals may remain populated and lane absent.

Four source deltas relative348: platform/lib.rs,new platform/macos_process.rs,security/trust.rs,new trust/native_platform.rs.499 product pins;495 unchanged348. Existing128 fixture files unchanged. No new Cargo dependency. macOS-only integration; no Linux or native Intel execution claim.

## Tests and evidence

Platform95 passed (two translation tests). Native security tests cover actual signed synthetic-profile/native seven-field projection, translated/wrong CPU, real carrier mutation during acquisition, later carrier/root changes, preserved profile refusal semantics even with a tier, actual devfs/writable-loader rejection and saved sample mismatches. Final security-r2:337 passed,0failed,2ignored; platform-r1:95passed; Clippy-r2 passes. Twelve compiled controls plus six-test security and two-test process baselines all produce their expected outcomes in mutation-r3. Full workspace-r1:681 passed,0failed,2ignored on unchanged final source, with no overlapping rebuilds in its target. Workspace and28 include-module format checks are required by the freeze.

Apple's official Rosetta article is captured and SHA-pinned in process-api-source-pin.json. It documents the specific ENOENT fallback; no general missing-observation fallback is introduced. Accepted security-completion.v8 §8.3 supplies the launch acquisition contract.347/348 retain the sysctl/CSR/CommonCrypto/Mach-O ABI evidence.

Failure history is retained: security-r1 did not compile because the added devfs TEST used nonexistent RetainedDirectory::open; changed TEST to existing RetainedDirectoryPath::open(...).directory(), production unchanged. Mutation-r1 SETUP stopped before any compiler because a replacement text also occurred in an assertion; helper now targets only production text. Mutation-r2 process baseline/four controls passed but security baseline/eight controls did not compile because they copied the same pre-fix TEST. They are not passes or caught faults. Fresh mutation-r3 tests final corrected source. Clippy-r1 and native-platform-r1 refer to the earlier five-test source; final validations must refer to the six-test source.

The02:30PDT actual Claude request was quota-refused again. No Claude agreement is claimed. Its integration review request remains pending; actual Grok is the authorized fallback.

## Remaining

Selected installation/actor/core/profile authority; all contributing census descriptor filesystems (root-only observation is insufficient); full current authority and independently proven durability; original T/action authentication; native writers and recovery; source selection, report/provider/workflow implementation and release qualification. Do not promote an OS observation, a matching synthetic fixture, a bounded review or a test count into those claims.
