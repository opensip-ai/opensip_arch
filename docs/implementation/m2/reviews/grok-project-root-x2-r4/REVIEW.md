# Review: project root X2 r4

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/project-root-x2/PROPOSAL.md` is 35239 bytes, sha256 `8c188ad548e1a0896da37e031e501e433274366e340d9ef0e50c5ceb87706574`, matching hashes.txt. `PROPOSAL-r3.md` is the r3 subject: 29703 bytes, sha256 `b4bca0afd75222262b257cc610f0e701bc3de9a6c19bc59bbe133904a843e5b3`. Product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo.

## r3

RF-1 is not closed. The replacement primitive, item 5, item 7, and the forbidden-substitutes line now name the current owner. Step 6 still rechecks the original observations. See the finding below.

RF-2 is closed. Item 6a reads a fixed source list and refuses the closed set. On this host `/usr/bin/git` is Apple Git 2.54.0, and `git config --list --show-origin --show-scope` shows one file, `unknown` scope: `/Library/Developer/CommandLineTools/usr/share/git-core/gitconfig` (64 bytes, root, mode 644, one link, same device as `/Users/sb`). Its keys are `credential.helper` and `init.defaultBranch`. `/etc/gitconfig`, the Xcode share path, `/opt/homebrew/etc/gitconfig`, and `/usr/local/etc/gitconfig` are absent, as are `H/.gitconfig` and `H/.config/git/config`. The five system paths plus both global files cover the Apple and Homebrew builds the law names. An unlisted system prefix stays the disclosed limit.

The union is checked, section and key names fold ASCII case, and any refused key in any source refuses. That is fail-closed relative to Git's last-wins. `include` and `includeIf` in any case refuse. `core.bare` set to anything but `false` refuses Git's other boolean-false spellings and is fail-closed. `extensions.*`, a format version other than 0, and `core.precomposeunicode` set to false refuse. Any `GIT_*`, `XDG_CONFIG_HOME`, or a `HOME` spelling other than the account-database home refuses, and the environment is read only to refuse. A present system file on H's volume is custody-checked on its own retained descriptor: root-owned, no group or other write, one link. Positive absence is a custody-free negative lookup. A higher file off H's volume refuses as `vcs-unsupported`. This repository stays admissible: local `repositoryformatversion` is 0, `bare` is false, `precomposeunicode` is true, and there is no include and no `core.worktree`. The index is `DIRC` version 2.

RF-3 is closed. Versions 2 and 3 take the 62-byte fixed part, refuse a version-2 extended flag, and for version 3 read the 16-bit extended flags when bit 0x4000 is set. The 12-bit name length matches the path, or is 0xFFF when the path is that long or longer. The path is NUL-terminated and padded with 1 to 8 NULs so the entry length is a multiple of 8. Version 4 uses Git's offset encoding (`value = b & 0x7f`, then while `b & 0x80`: `value = ((value + 1) << 7) | (next & 0x7f)`), strips that many bytes from the previous path, appends the NUL-terminated suffix, uses no padding, refuses an overlong strip, and starts from an empty previous path. The entry count accounts for every entry. Extensions are skipped by a 4-byte signature and a 32-bit size. `link`, `sdir`, and an unknown extension whose signature starts with a lowercase letter refuse. The trailing 20-byte SHA-1 must match, and a parse that does not consume the file is `vcs-unsupported`, never untracked. A native-endian misread fails the version check or the checksum and takes that refusal.

## What holds

The r3 dependency sentence is fixed. Item 10 says X2e depends on X2d and X3a-1, and X3a's store binding and X3b depend on X2e. Item 7a says the same. X4's monitor insertion stays with X4.

Item 7a step 3 is the new defect. It is X2's ordering of X3b's two steps. The contents of those steps stay X3b's law. This review does not judge X3b r2.

## Required findings

### RF-1 — Step 6 still rechecks the original registry

The primitive reconfirms R0 before RESERVED and R1 before ACTIVE, and it says R0 is never reconfirmed after RESERVED is confirmed. Item 5's one content read now feeds R, and item 7 takes N from R's ACTIVE row (R0 on reuse, R2 after this admission's registration). The forbidden-substitutes line forbids reconfirming R0 after RESERVED. After each confirmed publication, R advances and the replaced capture is provenance.

Step 6 is unchanged: recheck every original root, `.opensip`, marker, namespace, registry, chain and tracking observation, then call the primitive. The primitive runs only after that recheck.

Failure scenario: RESERVED is confirmed, so the name holds R1 and R0 is provenance. Step 6 rechecks the original registry sample. The name's metadata is R1's, the recheck fails, and ACTIVE never runs. The primitive's R1 reconfirm is never reached. The same sentence rechecks the original `.opensip`, marker and namespace observations after steps 3, 4 and 5 have published those names.

Step 6 rechecks the current owners: root, `.opensip`, marker, namespace, R1, chain and tracking. R0 stays provenance. The single content read stands; the recheck is the current owner's retained descriptor and metadata.

### RF-2 — The floor step is inside the handoff that already holds the lease

Item 7a is X2e, after X2d. Step 1 joins `FencedNamespace`, which item 7 returns with the lease held and the fence still borrowed. Step 3 then places both X3b steps inside that hold. One bullet says the floor step runs before X2d takes the lease. The other says the carrier start runs here, after the transfer and before the release. Step 4 releases the fence.

S7 writes trust state only under the fence and never under a lease (`security-and-lifecycle.md`). The floor is trust state. A numbered step that starts after the lease exists cannot also run before the lease is taken. X2 says this records X3b r2 item 1, whose order is the floor before item 7 and only the carrier start inside this handoff.

Failure scenario: an implementer follows the numbered hold. Item 7 has the lease. Step 3 writes the floor while that lease is held. S7 forbids the write, and the bullet that places it before the lease has no step to live in.

X2's ordering sentence places the floor step after R is current and before item 7 takes the lease, with the fence held and no project lock. The carrier start stays inside item 7a, after the transfer and before the fence release. The floor step's own contents stay X3b's law.
