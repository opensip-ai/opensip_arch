# Directory enumeration qualification: bounded investigation337

Investigation for independent review; no code/design selection, qualified profile, authority or completed M2 claimed. Root is checking whether repeated “libc holes / enduring exclusion” reminders have become broader requirements than the incorporated threat model. Existing historical330–336 reports remain unchanged.

## Source standing

The retained local security-completion.v8.md has SHA54f3a6901d4192c5b6af82d4aad4414a84ee3b7748aa67cae06272a481e38c2d. Its historical PROPOSED header is preserved. architecture-application.v1.json pins security-freeze.v8.json at33dad5ec1692ccbee859ead54d17d9730999a2d61012e2e48cbd1d2ad27e44ca; the application/supplement files are retained, not rewritten. Reviewer must check this incorporation context rather than infer current standing from an old header alone. No new threat-model exception is proposed.

Section1 assumes the kernel, distribution signing chain, platform loader/libc and first-party code with user authority as TCB; hostile kernel/local root are explicitly outside scope. Section8.8 describes the macOS verify/spawn residual same-UID window under that declared boundary. This does NOT make a passing permission sample an enduring guarantee; actual first-party locking, correct lifecycle, no other write-capable principals, and retaining the right objects through consumption remain implementation obligations. It does mean we should not invent a requirement to defeat malicious privileged TCB code.

## Public API evidence

POSIX defines the directory stream in terms of directory entries representing files; mutation after opening can make returned membership unspecified. Reset/check errno and drain the stream; a cooperative installation fence plus actual custody is necessary for a stable authoritative use. This is an API contract, not a measurement of this host or an RSS/time promise. [Open Group readdir](https://pubs.opengroup.org/onlinepubs/007904875/functions/readdir_r.html). The newer Issue8 URL was unavailable to the browser tool; no claim it was read.

Apple's archived raw-directory manual identifies inode-zero entries as remnants of deleted files and instructs callers to skip them. Thus raw unused slots are not automatically additional live candidates. The page is historical and does not establish the modern ABI. [Apple getdirentries manual](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/getdirentries.2.html).

Pinned upstream readdir.c skips inode-zero records and whiteouts and has malformed-buffer exits that do not set errno. Its public wrapper uses its internal skip mode. Those source facts remain true; they do not alone demonstrate omission of a live canonical regular file on a qualified non-union filesystem. Neither should they be silently dismissed if a supported, valid filesystem state can actually trigger such an omission. [Pinned Apple readdir source](https://github.com/apple-oss-distributions/Libc/blob/71bbe350ab79eef58113991d817ccc6165061a64/gen/FreeBSD/readdir.c).

Pinned upstream opendir.c uses whole-directory loading for union stacks.330 already rejects MNT_UNION before fdopendir and requires fstatfs success; ordinary non-union buffering differs. This source is NOT established as the exact installed binary. [Pinned Apple opendir source](https://github.com/apple-oss-distributions/Libc/blob/71bbe350ab79eef58113991d817ccc6165061a64/gen/FreeBSD/opendir.c).

Local CLT dirent.h gives getdirentries an intentional link-error spelling in64-bit inode mode and contains no public getdirentries64 declaration. Therefore do not “fix” the concern by introducing a private syscall ABI or by substituting scandir's whole-directory allocation. The installed header pin and independent read-only probe are recorded. No raw-directory implementation was authored.

## Actual observations and limits

Read-only fs_probe opens only /private/tmp/opensip-implementation and calls fstatfs/dladdr. Observed: macOS26.6.2 build25G83; Darwin25.6.0 arm64; local non-union APFS; readdir resolved to /usr/lib/system/libsystem_c.dylib. xcrun reports SDK27.0. This is a local development observation, not release-runner measurement, a verified libc binary match, full loader closure, boot attestation, ancestor custody or publication durability. No global mounts/permissions/configuration were changed.

## Proposed disposition for review

1. Preserve public fdopendir/readdir/closedir and explicit330 error/cap/union checks. Qualification targets complete live namespace enumeration under a declared trusted OS/libc and properly held installation protocol, not every deleted on-disk slot.
2. Treat concurrent namespace mutation as an actual missing precondition: join root-to-leaf native policy, selected supported filesystem/profile and held installation fence through all enumeration/content/dependency consumption. Existing sampled rechecks remain checks, not the exclusion mechanism.
3. Determine whether whiteouts or malformed internal records can suppress a live canonical descriptor in a valid supported non-union APFS state. If yes, provide a concrete reachable state and keep that profile unavailable until repaired. If only compromised TCB/raw corruption is hypothesized, distinguish that from an unimplemented product check and from existing filesystem-error behavior. Do not assert either answer without evidence.
4. Do not require a universal theorem against hostile root/kernel/libc as a prerequisite to implementing the declared product. Equally, never mark current dev observations as release qualification. Actual four-class release/TCB/failure-barrier tests and native constructor/admission code remain owed.
5. Continue full following-bucket structural composition independently; its output remains non-authoritative until the native producers and qualification gates are joined.

Requested independent assessment: validate the source standing/threat-boundary reading; identify any omitted in-scope counterexample; give a concrete minimum native qualification/constructor checklist without silently extending or weakening the design. In particular separate protocol-owned exclusion, OS API guarantees, measurable supported-profile checks, and actual unsupported environments. This is assistance to scope the next implementation, not blanket approval.
