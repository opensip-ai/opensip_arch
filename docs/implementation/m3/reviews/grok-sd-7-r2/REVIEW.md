# SD-7 r2 — ACCEPT-DESIGN-UNIT

Subject manifest `docs/implementation/m3/supervisor-d/sd-7-subject.json`, 1408 bytes, sha256 `74c9d407942b93950ec42e141d4e491b68c0f9bbb2d390fc528c824041fa8955`. Successor `sd-7/successor.json`, 14706 bytes, sha256 `350a249afaa001fc97292c2837395d930cc7bdc0d6b62b594b04df55d9767c04`. All 33 pins in `hashes.txt` match. Read-only. No cargo. `~/Library/Application Support/OpenSIP` was absent. GROK2 reviewed the request written for Grok; the output path stays `grok-sd-7-r2`.

r2 is VD2's contract passage supersession of SD-5's NE:3540 row, a fresh override of NE:3539 for item 25, and the two line-1159 remedy overrides. The texts are r1's. NE stays the selected contract.

## R1 — the supersession

The record is VD2 rule items 1–2 and the "SD-7 r2" section.

The one `passageSupersessions` entry names SD-5's record by the lock pin: 5805 bytes, `5e11581804098116a4afa5052ff27ed426beaebcc6e0a38607d1628ea8a595e7`. `check_sd7.py` places that record at position 85 of 94 at `4c761e8`. The parent pin is NE (329013 bytes, `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`) and the selector is `{"line": 3540}`, the same passage SD-5 overrides. `before` equals SD-5's `after` byte for byte. No bound supersession names NE:3540, so this is the chain's first link. `supersededPassages` in this review is that one `supersedes` object, equal to `fold-report.json`'s `reviewSupersededPassages`.

NE:3539 is the right home for item 25's row. The raw line is the NOT-SELECTED row, and no bound successor overrides it. The override's `after` keeps that row and adds item 25's row under it. NE:3540 stays SD-5's meaning, superseded in place.

## R2 — the conformed row

The class, exit and code cells stay SD-5's: `request-rejected` (2), `EXTENSION.ADMISSION_REJECTED`, `PAYLOAD-NOT-ADMISSIBLE`, subject `excluded-form:<class>:<manifestDigest>`. The detail cell changes one phrase, to MD5:1182's words: "claim a project hook, a reserved or additional root command, or a probe". The sentences from "No Plan, Coverage, Run or closure selection follows" through the end are SD-5's.

EE-3b keeps only the capability form. The r3 residue (`commands` entry for role `analyzer`; "a project hook, root command or contribution-granted probe"; "declare a project hook, root command or probe") is gone. The row states item 24's predicate: (a) a closure-only manifest (`toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`) that declares `commands` at all; (b) an `analyzer` tree without exactly one parentless entry, or whose parentless entry's `name` differs from the manifest's `name`; (c) a reserved root-command name among `name`, `aliases`, and, for `analyzer`, the parentless entry's aliases. An analyzer's own name-bound mounted root, at any declared depth, is admitted. A command tree is never an EE-3b form. A manifest the security owner's manifest admission refuses first keeps that route.

## R3 — item 25 and the remedy

The request-class row is LD-R4-2. It is `request-rejected` (2), `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`, the first of EE-2, EE-4, EE-6a. The three class texts are MD5:833–835. The envelope's `errors` is that detail, every `ExcludedForm` goes to the operational record, and there is no runId or executionId. The route reuses the NOT-SELECTED cell's class and code for a well-formed request outside D-371.

The widened remedy is 254 ASCII characters, identical in both B-S9 model copies at line 1159. Both original clauses are kept: "this capability is not selected for that language mode" and "no promise is made for it". The added clause names the three request-class forms, and "restate the request without it" is the next step MD5:839 gives both conditions. Every other `PUBLIC_ROUTE_REMEDIES` entry is unchanged, and the two copies stay identical. The request row quotes that string. NES's route registry sends only `native.requested-capability-mode-not-selected` to `PROVIDER.NOT_SELECTED`; the public-detail registry aliases that same key. The row adds no code. NES's route registry is not extended.

## R4 — the effective NE

Folding the 39 bound NE entries in lock order, then SD-7's supersession and NE:3539 override, yields 380848 bytes, sha256 `0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3`. That equals r1's NE7 snapshot byte for byte. Before SD-7 the fold is 378351 bytes, `03b498b7f4c4f2f10638fb4c128829981bd418d6b6c9ea253494d3bbcb1bad70`. In the effective §10 run the rows are the NOT-SELECTED row, item 25's row, the release-declaration row, the conformed row, the producer cause and carrier row, then SYN-1's row. `build_sd7.py --check`, `check_sd7.py` and `verify_scratch.py` each reproduce that fold.

## Form and binding

The record has three parents (NE and the two model copies), one supersession, three overrides and six candidates, which are the subject members other than the record. `build_sd7.py --check` matches the generated files, the record and the subject manifest.

`verify_scratch.py` on the VD2-a worktree's tool (`c01488fd…`, 43630 bytes) and staged lock: the staged lock passes at 95 with `contractPassageSupersessions` 0, and the SCRATCH-F8C review and assent pins match the staged row. With SD-7 r2 the same tool passes, 95 → 96, `contractPassageSupersessions` 1. Inventory selection, inheritance, the 21 inventory supersessions, the 40 generation sources and the 48 admission sources with 15 aliases are unchanged. The five refusals come back as "not listed by its review", "differ from the record", "restates a superseded contract meaning", "double supersession" and "conflicting contract passage overrides".

The plain tool at `4c761e8` (`c13d231e…`, 40714 bytes) passes main's lock at 94. SD-7 r2 is refused over main's lock and over the staged lock: "passage supersession must select an inventory row description". Binding waits until VD2-a and F8c are integrated.

## Non-blocking

NBO-1. The conformed row names the live-name collision and the security-owner-first sentence. Item 24 also names an in-tree name, alias or parent collision as not EE-5a. The exact predicate and the security-owner sentence already keep that collision on the security owner's route.
