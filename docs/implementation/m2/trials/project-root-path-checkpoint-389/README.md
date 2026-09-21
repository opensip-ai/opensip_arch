# Project root raw path capture389 — proposed source

One platform source change relative selected runtime29/source386 at product526a186;591 product files,590 unchanged including historical design lock. No package/dependency/inventory addition. No live code change or independent acceptance yet.

Adds RetainedDirectoryPath::open_project_root for existing native project paths under registry-v2 raw POSIX spelling: absolute1..4096bytes, no NUL/empty/dot components or trailing slash except root, preserves literal backslash and staging-like project names. Shared private parser stops at caller component cap before collecting more components. Existing open still rejects backslash and internal staging names. Both paths use identical descriptor retention, readonly/no-follow/nonblocking/CLOEXEC opens and full root-to-leaf recheck; no normalization or symlink traversal. Pure syntax acceptance does not promise filesystem name support.

This public platform mechanism grants no registry/native custody/profile/UUID/current authority or initialization permission. It does not establish the authoritative shared resource budget: callers must precharge before capture and retain/recheck original owners. No production caller is switched to the new method in this unit. Native project admission remains pending. Internal staging rules are unchanged.

Fresh serial development macOS arm64 replay:15 path-binding tests (12 existing plus3 new),0failed/ignored,95 other platform tests filtered. New tests exercise literal backslash/staging-like names with actual native retention and exact-name checks, relocation/replacement preserving original readable bytes, malformed/raw byte/4096boundary/component grammar, symlink refusal and mid-capture relocation. Existing path tests all remain. Fresh offline workspace all-targets check passed. No full platform/workspace test claim; unchanged32identity provider sources need no new provider build. Historical archive lock is provenance only, never a current design selection.

Independent substantive review and formal integration are still required. No S9.3/initialization writer/new-root restore law is selected by this mechanism. M2–M6 remain open.
