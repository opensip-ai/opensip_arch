# Independent Grok advisory: M2 schema-engine trial 03 (48-source current-alias registry)

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement. Not the separate Grok session.
**Kind:** Advisory technical review. **NOT ACCEPT-DESIGN-UNIT.** Not runtime selection. Not M2 complete.
**Work tree:** `/tmp/opensip-implementation/m2-grok-schema-registry-review-03/review`. Frozen 03, live repos, history, and prior review reports were not edited.

## Standing (from live `design-lock.json`)

Source-selection-v3 **is a live contract successor** (record `e638c55c…4ae4`, subject `ea4bb9bf…53ed`, Grok review `d7e5fccf…a100`, assent `docs/implementation/m1/source-selection-unit.v3.json` `757cf7c0…117a`). That is current lock authority. Frozen trial labels that still say “PROPOSED” (e.g. this trial’s `admission-registry.json`) are **not** current product authority. Live **generation** registry remains **40** rows. This trial is an unselected 48-source **admission** helper.

A previous source-closure advisory last sentence that treated source-selection-v3 as uninstalled is **incorrect** relative to the live lock. That report is left archived; this review uses the lock.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 15239 | `f241b52f4718b65429e604e8a256057e59fc3ba7a25fb02b126aaa8bf1aa7347` |
| Archive | 554894 | `08cb7aad3368e284ddff7f78a1da4895da7cda15cbf2feec34546ca261fdaa00` |
| `probe/src/registry.rs` | 6328 | `4d40a176fd51d4854df5ee5bac8b3931aa44d8ba08ed23752a12117b39180ae5` |
| `probe/src/registry_pins.rs` | 15571 | `59fe6bf566821d60ee3578d5e78444adb4d70a15623bba80746dc1e88959fa15` |
| `probe/src/patterns.rs` | 8884 | `a306bd98894c24dba4ebeb0c4db9eddd9fa7880ea1b44dd798d8592ee2b4b91e` |
| `probe/src/table.rs` | 6285 | `bcb612faf7afec2fdf7355799bc74ae919c0cf01c3065ae7970ee05f4625d4b9` |
| `schemas/admission-registry.json` | 26180 | `fc81079b3cee17118a15752882461c199069e6879a40c340312d810cf6f32ce2` |
| Identity pins (combined staged) | — | lib.rs `da6f4bdc…3eb7` / descriptors `868d7c37…97d3` |

Original `/tmp/opensip-implementation/m2-schema-engine-trial-03` **90/90**. `registered-cases.jsonl` verified in place (2833393 / `86b31b9c…19fc`). Private `Cargo.toml` rewritten to included identity-source, not live.

Oracle reference (this trial): `docs/implementation/m2/exact-schema-profile-selection-v1/reference/canonical.py` 8995 / `ad88e58f…96f7` — **accepted exact-profile**, not frozen foundation `canonical.py` `d47f25db…`.

## What the API does

- **48** positional full-document pins; length then SHA then `$id`; owned preflight. **909** root + direct `$defs` entries. **15** `DOCUMENT_ALIASES` (logical path → current `$id` only).
- `record_schema(document, digest, selector)` resolves alias, then **refuses if digest ≠ current pin SHA** (`SourceBytes`). No URI/major fallback.
- `schema(id, "")` for report-projection:1 returns **`UnsupportedCodec` before any instance parse**. `/$defs/ReportViewId` still compiles as a C-shaped def.
- `Program` is **not** in the public crate API (`mod schema` private; `pub use` only registry types). External `use …::Program` is E0432. `RegisteredSchemas` remains public.
- `ShapeValue` still opaque; `into_value()` drops the shape account. Not descriptor/replay.

## Independent reproduction

Private copy + extra review-only tests (not in the frozen tree):

| Check | Result |
| --- | --- |
| fmt / clippy `-D warnings` / build `--bins` | exit 0 |
| Frozen 10 tests + 2 extra boundary tests | **12/12** |
| External `Program` import | E0432 |
| External `RegisteredSchemas::source_requirements` | compiles |
| Pin files vs `admission-registry.json` vs `SOURCE_PINS` | 48/48, **909** entries |
| Native current vs historical SHA | `e5834d37…` ≠ `2d37b810…`; `record_schema` with historical digest → `SourceBytes` |
| Policy-v2 current vs historical | `b221b5ed…` ≠ `c8b0a907…`; same refusal |
| Recognition alias | maps to already-selected 40 file `49aacd86…` |
| New pattern samples vs Python `re.search` | 10/10 (empty `*`, `+` nonempty, no trailing LF, no C0/C1, SubjectId `a:b` vs `A:b` / `a:\n`) |

Did **not** re-run 26540 / 8337 / 30 archived corpora. Archived: 0 mismatches vs exact-profile oracle; 30 report-root lines `E:UnsupportedCodec`.

## Findings

**Current vs retained.** Construction pins **current** bytes only. Historical same-`$id` files cannot enter `from_sources` (length/SHA). `record_schema` with the historical digest is `SourceBytes`, not a handle on retained bytes. This helper does **not** implement historical readers (source-selection README: retained exact descriptor, separate owner). That is honest, not a missing fallback inside this trial.

**Codec selectors.** Report-root refuse is `id` + **empty** selector only, before `admit_json`. A 5 MiB buffer is never parsed for that path. Report defs remain C + identity 4 MiB/32. Do not treat this as profile-6 (27 829 365 / 39). Wrong error would have been `Json`/byte-limit or `Mismatch`; `UnsupportedCodec` is the right category.

**Patterns.** New CanonicalText/SubjectId use `(?![\\s\\S])` (absolute end) and exclude U+0000–001F and U+007F–009F. Trailing LF is **false**, unlike Python `$`. That matches these schema strings. `^.+$` still allows one final LF (NonLfFinal strip). Do not unify those accidentally.

**Private API.** Removing public `Program` closes the trial-02 forge path. Empty `Program::compile` still exists `#[cfg(test)]` inside the crate — acceptable. Production identity modules must keep `Program` crate-private.

**Limits still open (root is preparing; not demanded as this trial’s job):** host source provider; inventory file rows for 8 sources + 2 maps + identity `schema*.rs`; generation map stays 40; contracts leaf; resource 200 000 000 / eval depth 128 not M6; no ReplayedRun.

## Remaining integration duties

1. Inventory successor (20-package DAG unchanged) for admission-registry/map, eight `schemas/sources/*`, identity schema modules.
2. Host provider supplies 48 raw documents in pin order.
3. Historical **readers** remain a different owner; do not later “fix” `record_schema` to accept `2d37b810…` / `c8b0a907…` as current.
4. Reporting implements profile 6; identity C helper stays 4 MiB/32 and `UnsupportedCodec` on report-root.
5. Exact-profile oracle (`ad88e58f…`) is this trial’s comparison class; foundation `canonical.py` `d47f25db…` is not silently substituted.

## Limits

- Advisory only. Not ACCEPT-DESIGN-UNIT, not runtime/M2.
- Did not re-run 26540 cases; did not execute original tmp checkers against original trees.
- Did not read the other Grok session.
- Did not edit the previous source-closure report that misstated v3 lock standing.

## Evidence

- `review/results/probes.json` — SHA `81dffaaf360013d95dd08b44f9249fdde8abbce0c2b811d6f0a8a93ec932da7b`
- `review/copy/` private reconstruction; extra `probe/tests/boundary.rs` is review-only
- `review/probes/run_probes.py`
