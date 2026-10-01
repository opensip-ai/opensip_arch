# Review: ACL omission unreadable 461a r2

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of the descriptor-observation choke point after the r1 comment finding. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-461a` at `d4239a540e37cbc2f1415e0e5edd040fb7a3fbfc`. `subject.diff` is 60787 bytes, sha256 `fcad31ebf4ba3ba15842bf3944a1840ab2905b4e97ff5f0799774f05e60a524c`, and it matches `git diff HEAD`. Every pin in `hashes.txt` matches the worktree. The real OpenSIP directory is absent.

## Verdict

**ACCEPT.**

RF-1 is closed. The eighteen files other than `crates/platform/src/filesystem.rs` are byte-identical to the r1 pins.

## What holds

`DescriptorAcl::Omitted` now says that on macOS 27 an ACL whose last entry was removed is observed as `Omitted`, citing law 461 item 6. That is the `filesec` observation: `present == 0`. The bounded capture of that same file stays `Entries(0)`, and the comment does not move that fact onto `Present`. `DescriptorAcl::Present` now says an empty writer list is a present ACL whose entries grant no write. The removed-last-entry case is no longer an example of `Present`.

The mapping is unchanged. `present == 0` returns `Omitted`. A null ACL and the NOACL sentinel stay errors. A readable ACL with no mutation right returns `Present` of an empty vector. `check_descriptor_observation` maps `Omitted` to `AclWrite::Unreadable` and `Present` to `AclWrite::Known`. The refusal order and the `check_external_ancestor` placeholder stay. No `acl-unreadable` arm was added. The test horizon stays `#[cfg(test)]`, opt-in, and keyed by the thread-local device and inode of the ancestors above the scratch base. The v80 descriptions of the nineteen files stay true.

## Required findings

None.
