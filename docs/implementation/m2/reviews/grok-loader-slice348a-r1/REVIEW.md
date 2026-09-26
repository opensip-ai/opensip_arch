# Review: loaded-slice selection 348a r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/loader-slice-selection-348a/PROPOSAL.md`. No repository edits. No product cargo.

The proposal hash is `054b6126bf2f7befe850d0703f2e97d2cb5a72237d3c65cd4cbdedbd180f5f4c`, 4389 bytes, matching `hashes.txt`. It replaces only 348's fat-slice selection rule. The rest of `trials/macos-loader-checkpoint-348/README.md` stands, including the CodeDirectory rules and the sentence that Rosetta qualification belongs to the platform join.

Host probe (this process, not the product suite): macOS 27.0 (26A428), Apple M5 Max. `task_info(TASK_DYLD_INFO)` returned format 1 (64-bit infos), size 368. `dyld_all_image_infos.version` is 17, `dyldPath` is `/usr/lib/dyld`, `aotInfoCount` is 0.

| source | cputype | cpusubtype | filetype | notes |
| --- | --- | --- | --- | --- |
| mapped `dyldImageLoadAddress` | `0x0100000c` | `0x80000002` | `MH_DYLINKER` | read-only shared-cache mapping, `ncmds` 17 |
| `/usr/lib/dyld` fat arm64e and its Mach-O header | `0x0100000c` | `0x80000002` | `MH_DYLINKER` | file offset 1179648, `ncmds` 20 |
| `/usr/lib/dyld` fat arm64e.x1 and its Mach-O header | `0x0100000c` | `0x8000000c` | `MH_DYLINKER` | file offset 2670592 |
| `_dyld_get_image_header(0)` and `infoArray[0]` | `0x0100000c` | `0x00000000` | `MH_EXECUTE` | this probe binary |

SDK `mach/machine.h` names the low subtypes `CPU_SUBTYPE_ARM64E` (2) and `CPU_SUBTYPE_ARM64E_X1` (12). Both on-disk arm64 slices also carry `0x80000000` (`CPU_SUBTYPE_LIB64` / `CPU_SUBTYPE_PTRAUTH_ABI`). The fat entry and the slice Mach-O header store the same 32 bits. `hw.cpusubtype` on this host is 2, the low bits only.

## Verdict

**ACCEPT.**

## Answers

The selector is a read of the header the kernel mapped, and it is the right binding. `task_dyld_info` has no load address of its own. It reports `all_image_info_addr`. At version 17 that struct's `dyldImageLoadAddress` points at a read-only `MH_MAGIC_64` / `MH_DYLINKER` header whose pair is `0x0100000c` / `0x80000002`, the same pair as the arm64e slice of `/usr/lib/dyld` and not the arm64e.x1 slice. The infos page is writable. The header page is not. The observation is those header fields. For the main executable, image 0 is the `MH_EXECUTE` image: `_dyld_get_image_header(0)` and `infoArray[0]` agreed here, and its subtype is `0x00000000`, so dyld's pair cannot select the executable. 463 keeps the kernel CodeDirectory hash as the executable's identity join.

`macho_best_slice("/usr/lib/dyld")` returned that same arm64e pair today, from the file slice (`ncmds` 20). Its contract is the slice a new load would pick. Rule 1 already excludes it, along with `NXFindBestFatArch`: the selector is the header this process mapped. The denylist covers the same guess by behavior (family order, newest subtype, `hw.cpusubtype`, a compile-time subtype, masked capability bits, a later retry, a CodeDirectory hunt). Naming `macho_best_slice` and `NXFindBestFatArch` on that list would make the trap obvious. The hash hunt stays forbidden, so 463's equality check remains a join and not a search.

The exact 32-bit match is the right comparison. On this file the capability bits are part of the stored subtype, in the fat entry and in the inner header, and the mapped dyld header uses them too. A same-family slice with a different subtype is a different pair. arm64e.x1 does not make arm64e ambiguous, and a value that differs only in the high capability bits does not match. A duplicated exact pair still refuses. The slice's own Mach-O header still has to equal the pair, which these three slices already do.

What 348a gives up is family-level uniqueness: a second slice of the same cputype is no longer itself a refusal. Pair-level uniqueness stays. So do the single primary SHA-256 CodeDirectory, the bounds, the no-follow file measurement, and the disclaimer that the dyld measurement is not proof of the mapped bytes. That disclaimer is load-bearing here: the mapped dyld header and the file slice share the cpu pair and differ in `ncmds` (17 in the shared cache, 20 in the file). Full-header equality with the file would not hold. The rule does not require it.

Rosetta is not installed on this host (`arch -x86_64` returned `Bad CPU type`), and `aotInfoCount` is 0 for this native process. The rule stays inside 348's split. It reads the running image's mapped pair and refuses when that cputype is not the compiled family. It does not consult host `hw.cputype`. Whether a translated process may run remains the platform join.

The evidence list is enough to implement the selection change. The synthetic fat, absent, duplicate, capability-bit, and thin-mismatch cases are the new rule, and the macOS 27 system artifact has a pair that matches the arm64e slice. The private test seam matches 348's private hook: production reads the live header. The still-owed FFI pin is the right place for `task_info`, the versioned `dyldImageLoadAddress` field (the SDK defines it only at infos version 2 and later; this host is 17), `_dyld_get_image_header(0)`, and the 64-bit infos format. The 32-byte bound is `mach_header_64`. Charging it like the existing fixed reads, including the `task_info` call, is enough for the unit to price.

## Replay

Read-only host probe and a direct read of `/usr/lib/dyld`. No product cargo.

Do not commit.
