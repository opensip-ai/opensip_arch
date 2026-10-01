# Law X2 r8 — system Git sources stay outside item 1's admission

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `project-root-x2/PROPOSAL.md` is 39036 bytes, sha256 `c31d9a020f91650fb1c85f6697bffac1902bf3607d501e5821f48cd8c4b301b5`, matching `hashes.txt`. Preserved r7 is `PROPOSAL-r7.md`, 38368 bytes, sha256 `724c33d6b411217add1138142d1d2e5199d23c051bd0846420e7a07eefd14ba8`. Live product HEAD is `46b1d60faef4ca004170ae3cbcff7c9b29ad3f7c`.

The diff against r7 is the title, the r8 provenance sentence, and item 1. Item 6a is unchanged.

## What holds

The no-follow premise admission now hangs under "How the Git evidence in scope is admitted," and that bullet names the `.git` evidence and the global files. Each of those is admitted through its own retained no-follow descriptor, under the premise and the H-volume constraints. A `.git` counts only when it is strictly below H. The `commondir` and `config.worktree` lookups stay custody-free negative lookups. The omitted-ACL alternative stays rejected.

The system files are a separate bullet. They are outside the custody scope. Item 6a opens each fixed path following symbolic links, charged and capped at 64 KiB, with no custody, no premise, and no H-volume constraint. Absence is `ENOENT` anywhere on the path. A present file is parsed with the same closed parse. Item 1 refuses one only when it is unreadable, not a regular file, oversized, or fails that parse. A location above H or off H's volume is not a refusal. The never-covers list says the same: the location refusal is a `.git` at or above H or off H's volume, and the system files are listed on their own as refusal-only evidence.

That matches item 6a. System sources cannot admit, select, or relax a root, a repository, a marker, or a custody decision. The union check only adds the existing `vcs-unsupported` refusals. Global and repository sources stay no-follow under item 1. The recheck of a system source is a re-read: the same absence or the same bytes. Following `/etc` to `private/etc` remains how the bytes Git would read are obtained. The forbidden substitute that withholds the premise from any object off H's volume agrees with leaving these files unjudged. The rest of accepted r6, including the fence-free `recover` exception, is unchanged.

## Verdict

ACCEPT. r7 RF-1 is closed.
