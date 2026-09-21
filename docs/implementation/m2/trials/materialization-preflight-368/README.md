# Read-only materialization preflight368

Compare the live product atfa72e50 with frozen native-lineage368:271 tracked live files,583 candidate files;256 identical,15 changed and312 added. No live tracked file is missing from the candidate. The audit was taken just before368 freeze; no source changed afterward. Its historical candidate label remains unedited. The freeze pins583 files independently.

All32 checks pass across host and isolated Rust-provider lanes for four metadata targets (macOS/Linux, arm64/x86_64): locked offline Cargo metadata, exact contracts profile, exact identity source/dependency pins, and package edges against proposed inventory55. Host explicitly chooses security-crypto-workspace; provider explicitly chooses toml-workspace. No automatic profile fallback or feature union is used. These are read-only metadata/source checks, not target execution or independent acceptance of changed dependency policies.

The cumulative delta includes28 external and three local Cargo packages beyond the selected runtime24. No lock package was removed; serde_derive's existing syn dependency spelling becomes unambiguous alongside the newly added syn2. All exact rows and commands/output hashes are preserved. The selected design-lock and actual product tree were not changed.

Before materialization: actual inventory55 acceptance/root assent, cumulative exact source/runtime unit and map, dependency/source closure review, appropriate cumulative tests and explicit preserved-file checks remain required. No installation, runtime authority, platform qualification or M2 completion is claimed.
