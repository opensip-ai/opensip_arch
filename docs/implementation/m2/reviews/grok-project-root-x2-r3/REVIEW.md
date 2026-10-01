# Review: project root X2 r3

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/project-root-x2/PROPOSAL.md` is 29703 bytes, sha256 `b4bca0afd75222262b257cc610f0e701bc3de9a6c19bc59bbe133904a843e5b3`, matching hashes.txt. `PROPOSAL-r2.md` is the r2 subject Codex reviewed: 24117 bytes, sha256 `445d30286948bc60524b5adc60a941f97e5f042a42627b73d94cba83e9bf0771`. Product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo.

At this HEAD the gate still judges `project-registry.v2` with no byte cap (`installation_admission.rs`), and the observation session does the same (`installation_session.rs`). `RetainedDirectory::observe_birth` is the sampler item 4 names. `PROJECT.ROOT_CUSTODY_REFUSED` is request-rejected, exit 2, `CONFIG.INVALID`. `PROJECT.SCOPE_LIMIT` is request-rejected, exit 2, `REQUEST.UNSATISFIABLE`.

## Codex r2

RF-1 is closed. Every enclosing `.git` from the selected root up to `/` is examined. A `.git` at or above H, or off H's volume, refuses as `vcs-unsupported`. A gitlink (on-disk mode octal `0160000`, the value Git prints as `160000`) is not a match for the marker path and does not clear the rest of that index. The marker path is tracked when any other entry matches it, with the worktree file present or absent. Every consulted `.git`, `config`, `index`, `commondir` absence, `config.worktree` absence, and negative VCS lookup joins the recheck set on the same ledger.

RF-3 is closed. Item 1 admits each enclosing `.git` directory strictly below H, and its `config` and `index`, each through its own retained no-follow descriptor, under the same premise and H-volume rule. `commondir` and `config.worktree` stay custody-free negative lookups and are never admitted objects. Other objects under `.git` stay outside the premise.

RF-2 is not closed. The R0/R1/R2 paragraph says the right thing, and the numbered procedure still reconfirms the original capture. See the finding below.

RF-4 is not closed. The local checks name `core.worktree`, version 0, and 20-byte hashes. Those checks are not Git's effective configuration, and index versions 3 and 4 do not by themselves fix the path bytes. See the findings below.

## What holds

The omission premise, root placement, chain walk, `ProjectRootAdmission`, the first registry capture, `.opensip` and marker barriers, the lease order, the scope-limit row, and the budget caps are the r2 text Codex had already accepted, plus the premise lines above.

Item 10 is the unit graph: X2e depends on X2d and X3a-1, and X3a's store binding and X3b depend on X2e. Item 7a's join consumes an endpoint X3a-1 has already produced. Line 210 still says X3a-1's endpoint depends on X2e. That sentence is the dependency wording Codex left as nonblocking.

This repository's own `.git` is the ordinary layout the law wants to admit. The config is 355 bytes, tab-indented, `[core]` with `repositoryformatversion = 0` and `bare = false`, subsections, no `core.worktree`, no include, and no continuation. `commondir` and `config.worktree` are absent. The index is `DIRC` version 2. On this host `$(prefix)/etc/gitconfig`, `~/.gitconfig`, and `~/.config/git/config` are absent. A parser of the stated subset that accepts Git's discarded whitespace admits this file.

ASCII case-insensitive comparison of the marker path is the right fold on this case-insensitive APFS volume. Refusing a non-ASCII relative component avoids Unicode-normalization aliasing. `core.ignorecase` being false would still be the same directory on this volume, so the fold stays the custody match.

Version 0 plus a refusal of any `extensions.objectFormat` keeps SHA-256 widths out of the index. Git's own rule is a little tighter than "ignores extensions": unless an extension says otherwise, specifying one when `repositoryformatversion` is not 1 is an error. The law's refusal of version 1 and of `objectFormat` still keeps the hash width at 20 bytes.

## Required findings

### RF-1 — ACTIVE still reconfirms the original registry capture

The replacement primitive is used for both RESERVED and ACTIVE, and step 1 reconfirms item 5's full sample. After RESERVED is confirmed, that file is no longer the name `project-registry.v2`. The next paragraph says R1 is the predecessor ACTIVE reconfirms, and that R2's ACTIVE row is the only source of Eligible and of the handoff. Item 5 still says item 7 and the handoff use item 5's capture. Item 7 still takes N from the ACTIVE row in that capture. Step 6 rechecks the original marker, namespace, and registry observations. The absence transfers say those names belong to the published owners after steps 3, 4, and 5.

Failure scenario: an empty established registry is R0. RESERVED is confirmed and the name now holds R1. ACTIVE's replacement reconfirms R0 and stops, so the new namespace never becomes Eligible. If the paragraph is followed and the numbered step is left behind, item 7 still looks for an ACTIVE row in R0. A FirstUseCandidate's R0 has no such row, so the published R2 grants no lease.

The primitive's predecessor has to be the current owner R: R0 for RESERVED, R1 for ACTIVE. Item 7 and the handoff take the ACTIVE row from R, which is R0 on reuse and R2 after ACTIVE is confirmed. Step 6 rechecks those current owners. Item 5's single content read still means no second read of registry bytes.

### RF-2 — The layout proof is not Git's effective configuration

Item 6a proves the worktree by spelling checks in the local `config`: `core.worktree` absent, `core.bare` absent or false, `core.repositoryformatversion` absent or 0, and no `[include]` or `[includeIf …]` section. Git matches section and variable names case-insensitively, and the last value wins. It reads `$(prefix)/etc/gitconfig`, then `$XDG_CONFIG_HOME/git/config`, then `~/.gitconfig`, then `$GIT_DIR/config`. A local omission does not prove the effective key is absent. `core.bare` is a boolean: `no`, `off`, `false`, `0`, and the empty string, in any case.

Failure scenario: the local file is this repository's ordinary config, and `~/.gitconfig` sets `core.worktree` to a subdirectory. Or the local file itself contains `[core]` / `Worktree = subproject`, or `[Include]` of a file that sets it. The canonical-spelling checks see no `core.worktree`. The index tracks `.opensip/project-id.v1` relative to the relocated worktree, which is not the path computed from the `.git` parent. The marker is reported untracked, and registration or the lease proceeds. The same fold misses `RepositoryFormatVersion = 1`.

The constraints have to apply to the effective keys after case-folding, with last value winning, across those files in Git's order. Any include section, in any case, refuses. `core.bare`'s effective value is Git's boolean false, or the key is absent; any other value refuses. A present higher file on H's volume is custody-checked through item 1, on its own retained descriptor. Positive absence of a higher file is a custody-free negative lookup. A higher file off H's volume, or one the premise cannot admit, refuses as `vcs-unsupported`. This repository stays admissible: its local file parses, and the three higher files are absent here.

### RF-3 — Index versions 3 and 4 do not identify the path bytes

Item 6a admits index version 2, 3, or 4 with 20-byte hashes, and refuses a split index or a sparse-directory extension. Version 3 inserts a second flag half when the extended bit is set. Version 4 stores each path as a prefix strip count plus a suffix against the previous path. The file ends with a 20-byte checksum of the preceding bytes. None of that is stated. A parser that accepts the version field and then reads version-2 paths will not see a version-4 marker path, and nothing in the law turns that miss into a malformed index.

Failure scenario: the index is version 4, the hash width is 20 bytes, and there is no `link` or sparse-directory extension. The marker path is prefix-compressed. The scan compares the version-2 path bytes, finds no match, and reports the marker untracked. Registration or the lease proceeds.

A version-3 or version-4 index is parsed with that version's entry layout, and the trailing checksum must verify. A parse that does not consume the file refuses as `vcs-unsupported`. It is never an untracked result.
