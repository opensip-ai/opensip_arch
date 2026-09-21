# Native runtime selection28 + source383 — design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

One bounded task with two distinguished assessments:

1. **Source383** (not previously approved): inert identity `schemaVersion` 2 codec matches selected registry-v2 owner/schema/model. Independent 56 identity tests and 41532 differential cases against exact selected v2 model, 0 mismatches.
2. **Formal integration**: those exact three identity files onto selected runtime27 + inventory57 + registry-owner-v2. No passage overrides.

Not release, M2 completion, current authority, writers, five-member binding, S9.3, native profile qualification, analyzer implementation, or live installation. Native helper 384 is **excluded**. Root assent is **not** manufactured. Live product was **not** written (`HEAD` `2944f35`; 587 tracked files; live codec remains v1 `f3bb0fb6…`).

**subjectManifestSha256** `826cae6671fbd229d21435322b6da5667c3c20a53e7e64c71940a6cf4dee3482`  
`docs/implementation/m2/native-runtime-selection-v28-subject.json` **2541** B, **12** members, paths **sorted unique**, **0** pin mismatches. `passageOverrides`: []. `pin_rows` accepts subject (12), candidates (11), parents (3). Candidates cover the subject minus the successor. Parents are not members.

---

## Selected parents (live lock 33 inventory / 49 contract)

Live `design-lock.json` **95044** B `43d502ea…3098`. Last selected contract is registry-owner-v2 (`cf91319a…4f04`). This v28 record is **not** on the lock.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| runtime27 successor | 6885 | `8fdf8fea3d87a2fed875a912797e8990178e6747b265286b6c8e04a25c44c5d7` | selected contract record |
| registry-owner-v2 successor | 24230 | `cf91319a7e83c339000895e11460c3168436d67e5bd35a29289a2f5d87674f04` | selected contract record |
| inventory57 | 278524 | `f16422c6c4cc2f7dff272e5f25cfbbdf3b74cd01f334103eb57d09789560eb1e` | selected inventory candidate |

Parent paths are lexicographic. All three match accepted sha256/bytes. Inventory57 already lists the three identity paths; no inventory row or DAG edge is added.

---

## Source383 assessment (inert v2 codec)

Archive `aa77c8b1…56aa` / **6902688 B / 628 members** (587 product); subject.json **117538** B `da34d656…5ab7`; archive-pin matched before private extract; **0** member digest mismatches. Delta vs accepted 380: **exactly 3** identity files.

| Path | Before (live/373) | After (383) |
| --- | ---: | ---: |
| `crates/identity/src/lib.rs` | 2373 `0158775c…60cc` | 2426 `f427e633…d1b0` |
| `crates/identity/src/project_registry.rs` | 10940 `f3bb0fb6…8fe5` | 12368 `0805e375…80bc` |
| `crates/identity/src/project_registry_tests.rs` | 7047 `68df88f6…a8b7` | 10630 `8c7cc2de…6add` |

`lib.rs` adds `VolumeIdentityKind as ProjectVolumeIdentityKind` to the existing private-module re-exports. Comments retain: decoded values never establish custody, registration, lease, or authority.

Codec vs selected v2 owner/schema/model (`owner.md` `2d4b65c9…`, schema `b7d8340e…`, model `3eb3741d…`):

- Whole canonical document or nothing: closed `{schemaVersion:2, entries}`, cap 4 194 304 / 4096 rows, extra members refuse, `canonical_bytes == raw`.
- `NativeProjectRootV2`: macos only; `volumeIdentity` kind `macos-apfs-volume-uuid-v1`; 32 lowercase hex → 16 raw bytes; all-zero UUID refuses; no `deviceId` field (legacy version/device-root Shape/Version).
- Locator uniqueness `(platform, path)` separate from incarnation `(platform, kind, uuid, inode, birth)`; live only for RESERVED/ACTIVE; terminal rows may repeat PID/locator/incarnation; **all** statuses keep strict N order.
- Marker **92-byte** PROJECT-ID-V1 frame unchanged.
- Both allocation kinds decode; states and ACTIVE∪RETIRED projection unchanged; `has_reservations` is visible and is **not** the S9 start gate.
- Typed getters reconstruct the canonical input in the probe. Values do **not** observe old-name absence, profile, custody, tracking, registration, lease, or current authority.

Independent replay on a **private staged copy**, rustc **1.95.0**, verified 368 vendor, own `CARGO_TARGET_DIR`, `HOME=/Users/sb`, Darwin `TMPDIR`, `RUST_TEST_THREADS=1`: **56 passed**, 0 failed, 0 ignored (13 `project_registry_tests::`). Fresh identity rlib `libopensip_identity-fc04d2ac9153253a.rlib` **13041304** B `ce064b36…0f1f` (independent binary; crate fingerprint matches author). Fresh probe compiled from exact `probe.rs` `1e55fd06…0ed0`. Private differential runner path-adapted only (selected v2 model hash asserted `3eb3741d…`): **41532** cases, **17972/23560** registry/marker, **2138/1052** accepted, **0** failures. Corpus `338b0af3…621be` and outcomes `1b91dc33…01379` **byte-equal** author evidence.

Author workspace `cargo check --workspace --all-targets` 17.81s and provider boundary (**28** sources / **19** archives; three unavailable probes expected-exit 1, stderr “native analysis is not implemented”, empty stdout) were **inspected**. Provider identity pins match extract. Not rerun. No new mutation-fault evidence. Frozen 373 invalid r1 faults and corrected 373-r2 remain historical. Native 6 birth + 4 volume filters are carried from runtime27, not rerun.

**Source383 requiredFindings:** none. This is this review’s source assessment, not a prior lock unit.

---

## Formal integration (map v2 and independent restage)

`stage.py` **5719** B `3a71d80a…b1c4` is byte-identical to selected27. Map schemaVersion 2: **3** writes + **583** unchanged non-lock; archive `design-lock.json` excluded. `baseProductHead` `2944f35e797f80fe9d85713a283c740d1361d6bd` (587 baseline files).

Independent restage to `grok-out/staged-product`: verified **628** members before output; mapped 3; unchanged non-lock 583; non-lock source **586**; staged lock **byte-equal** live lock; live product unchanged; `runtimeAcceptance: false`. Staged identity files equal extract after-pins.

This unit inherits selected registry-v2 law (ten overrides, historical v1 schema, no silent migration, native qualification still outstanding). It does not modify those passages.

---

## requiredFindings

None.

---

## Scope / limits

Does not install source. Does not grant writers, S9.3, full binding, native APFS/Linux qualification, or helper 384. Runtime28 binding still needs root assent on this subject. M2–M6 remain open. No Claude concurrence. Root remains lead.
