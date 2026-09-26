# Loaded-slice selection for the Mach-O locator — proposal 348a r1

2026-09-26. Claude Opus 5.5, implementation lead. Successor to the selection rule of the private system-loader observation 348 (`trials/macos-loader-checkpoint-348/README.md`). Not code, not creator authority, and no change to any selected record shape. Everything else in 348 stands.

## Problem

348 selects, from a fat file, "exactly one matching CPU family, with matching selected Mach-O CPU/subtype", and it refuses a second slice of that family rather than guess Apple's preference. `locate_as` implements this by comparing `cputype` only. 463a reuses `locate_as` for the running executable.

On macOS 27.0 (26A428), `/usr/lib/dyld` has three slices:

| slice | cputype | cpusubtype |
|---|---|---|
| x86_64 | 0x01000007 | 0x00000003 |
| arm64e | 0x0100000c | 0x80000002 |
| arm64e.x1 | 0x0100000c | 0x8000000c |

`capture_system_loader` therefore refuses every run on an Apple-silicon Mac with `Malformed("ambiguous architecture")`. The refusal is lawful under 348, but it leaves no loader observation on a current OS. On this host (Apple M5 Max, `hw.cpusubtype` 2), the kernel mapped the arm64e slice: the dyld header at `dyld_all_image_infos.dyldImageLoadAddress` reads cputype 0x0100000c and cpusubtype 0x80000002. Picking by family order, by "newest" subtype or by `hw.cpusubtype` would each be a guess about the kernel's grading, which 348 correctly forbids.

## Rule

1. **Observed selector.** The selector is the full 32-bit (cputype, cpusubtype) pair read from the Mach-O header the kernel actually mapped for the corresponding image in this process:
   - for `/usr/lib/dyld`, the header at `dyld_all_image_infos.dyldImageLoadAddress`, located via `task_info(mach_task_self(), TASK_DYLD_INFO)`;
   - for the running main executable (463a), the header of image 0 (the `MH_EXECUTE` image).

   The observed header must have magic MH_MAGIC_64 and the expected file type (MH_DYLINKER or MH_EXECUTE). Its cputype must equal the compiled process CPU family. Otherwise the locator refuses. No sysctl, compile-time subtype, path or environment value selects the slice.
2. **Exact match.** In a fat file, exactly one slice must equal the observed (cputype, cpusubtype) pair in all 32 bits of each field, capability bits included. Zero matches refuse ("loaded architecture absent"). Two exact matches refuse ("ambiguous architecture"). Other slices of the same family with a different subtype are not candidates and do not make the file ambiguous. The selected slice's own Mach-O header must equal the same pair, as today.
3. **Thin files.** A thin file's header must equal the observed pair.
4. **No proof of loaded bytes.** The selector binds which slice is measured to the kernel's choice. It does not prove that the on-disk bytes equal the mapped image. 348's disclaimer "not proof of the loaded image" stands for dyld. For the main executable, 463's kernel CodeDirectory-hash equality remains the identity join.

## Forbidden substitutes

`hw.cpusubtype` or `hw.cputype`; the first, last or highest-subtype slice of a family; a compile-time `cfg` subtype; masking capability bits before comparison; retrying another slice after a later parse or hash failure; choosing the slice whose CodeDirectory hash happens to match the kernel hash.

## Evidence obligations

- Tests:
  - A synthetic fat file with arm64e 0x80000002 and arm64e.x1 0x8000000c slices selects each one only under its observed pair.
  - A pair absent from the file refuses; a duplicated exact pair refuses; a capability-bit-only difference is not a match.
  - A thin file whose header differs from the observed pair refuses.
  - The actual system artifact passes on macOS 27.
- The observation seam is private, like the existing after-read hook. Production always reads the live header. Tests may supply a pair only under `#[cfg(test)]`.
- The observed-header read is a bounded read of 32 bytes from an address the kernel reports. Its cost is charged like the existing fixed reads.

## Still owed by the implementation unit

The exact FFI declarations (`task_info`, `TASK_DYLD_INFO`, the `dyld_all_image_infos` offset for `dyldImageLoadAddress`, `_dyld_get_image_header`) pinned to the SDK headers; the refusal detail strings; the inventory successor if a new file is added; and a macOS 26 re-measurement if a macOS 26 host becomes available.
