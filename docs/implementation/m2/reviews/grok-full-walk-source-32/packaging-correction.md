# SOURCE-32 packaging correction (archive representation only)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Packaging-only check of the frozen SOURCE-32 evidence archive. **Not a re-acceptance of source-32. Not runtime-16.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-full-walk-source-32-review/review`. Original `report.md` / `report.json` are **not rewritten**. Live/frozen/history not edited.

## Unchanged source

`docs/implementation/m2/trials/full-walk-32/subject.json` **97191** / `c52cf367757970cb072e8ae72e6c29fe8b60741719709eafda2cd5a6f464ec96`. **508** members, paths sorted unique. Export `/tmp/opensip-implementation/m2-full-walk-subject-32`: **508/508**, 0 extra, 0 hash mismatches.

Original SOURCE-32 reports remain:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `report.md` | 6354 | `7cf175b73a8a7f5eafa51cdd09e2fe9fd8f5022149a9d606eded132f857255bd` |
| `report.json` | 5478 | `89a13ee25297b39c9a4819849401600b15458222d885c6159e57635473c584a1` |

Tests, references, and product bytes are unaffected.

## Historical gzip (not rewritten)

`archive-pin.json` is still the gzip pin (**176** / `179c96b70ee270b9b446eb213ca918d4c63aed8bd867620958da098d6119a14c`):

`docs/implementation/m2/trials/full-walk-32/subject.tar.gz` **154403601** / `a4fd601f23b8f5f0cfea50c171f69e031d1c4c8dceefbb631a396cbb63ae9f3e`

That gzip is preserved privately at `/tmp/opensip-implementation/m2-full-walk-gzip-packing-32/subject.tar.gz` with the same pin file. Independently: **508** members, 0 hash mismatches vs the subject. It was caught **before commit** (exceeds a 100 MiB GitHub file limit because repeated explicit oracle packets compress poorly under gzip).

## New xz representation

`archive-pin.v2.json` (**174** / `e98128e3515f23b14021ada5a4182c1b69442a60b6735df3e781ad0c8806064f`):

`docs/implementation/m2/trials/full-walk-32/subject.tar.xz` **3240476** / `70587750cc19bc4deb446d88852fbef726426265a3c5360d56625f8942a8a9bd`

Independently: **508** unique sorted members, set-equal to the subject, **0** hash mismatches. Member set equals the preserved gzip.

`packaging-correction.json` **932** / `d643b7aa695c4d4d4bdd26ebb155130bb3082f26bdaee1f36e93a95adee098d0` names v2 as the selected archive pin and does not claim source acceptance.

## Binding

Eventual formal runtime-16 must bind **`archive-pin.v2.json` / `subject.tar.xz`**, not the historical gzip. History was not removed; the gzip pin remains as a historical record.

## requiredFindings

None.
