All preserved. Here is the follow-up.

---

# v2 follow-up — F-04 selector segment law + guard bound agreement

**Standing:** author-assisted reference work by a reviewer acting as author. Not independent acceptance, not blind reconstruction, not implementation or readiness. Final new-byte independent review remains required; I do not accept my own work.

**Preserved (re-verified after all writes):** frozen25 **12869/12869**, author97 **97/97**, completed v1 authored evidence **158/158** — all unmodified. Every write is inside v2 scratch. v1's F-05/F-06 exports (18 `fcontrols` files) are byte-unchanged.

## 1. Root is right — reproduced exactly

I reproduced all six rows from `root-counterexamples.json` against the completed v1 selectors, with the law decided by splitting on `/` rather than by regex behaviour:

| value | segments | v1 accepts | exact dot segment? | defect |
|---|---|---|---|---|
| `a\n/../b` | `['a\n', '..', 'b']` | yes | **yes** | accepts forbidden segment |
| `a\n/./b` | `['a\n', '.', 'b']` | yes | **yes** | accepts forbidden segment |
| `a/.\n` | `['a', '.\n']` | **no** | no | rejects lawful segment |
| `a/..\n` | `['a', '..\n']` | **no** | no | rejects lawful segment |
| `a\n/b`, `a/b` | — | yes | no | correct |

Both causes confirmed: `.*` does not cross `\n`, so the whole-string lookahead never sees `/../` after a newline; and the inner `$` matches before a trailing newline, so `/.` + `$` fires on a final segment that is actually `.\n`. Reusing CanonicalPath's lookahead verbatim carried its text, not its law.

## 2. Who owns segment characters — checked before deciding

Root told me to establish ownership rather than let regex accident decide, and the answer is unambiguous. Two independent frozen implementations make the *same* decision:

- `identity-model.v3.py` `ordered()` line 138/147: `child.startswith('/') or '\\' in child or '\x00' in child or any(x in ['', '.', '..'] for x in child.split('/'))`
- `discovery-defaults.py` `normalize_explicit_root()` lines 77-81: same four tests over `body.split('/')`

Both **split on `/` and test exact segment equality**, and both exclude **only** `/`, backslash and NUL. Neither excludes newlines. Neither imposes a per-segment length cap.

So I did **not** forbid newlines. `identity-schemas.v3 #/$defs/LogicalPath` also records explicitly that "THREE DIFFERENT ENFORCEMENTS EXIST AND THEY ARE NOT EQUIVALENT", that the declarative 255-per-segment bound reaches only two Blob path fields, and that `ordered()` "does NOT enforce the per-segment 255 maximum" — so I deliberately did not import that bound either. Importing it would have been exactly the unrequested widening. `WorkspaceRootText` independently confirms the other edge: it "MAY be `.`… NOT LogicalPath, which forbids a dot segment." NFC turned out to be owned by CVE1's codec, not by path admission, so it is not imported.

## 3. The fix — per-segment negative test with strict end assertion

```
SEG  = (?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+
DIR  = ^SEG(/SEG)*(?![\s\S])
ROOT = ^(?:|SEG(/SEG)*)(?![\s\S])
```

The negative test is attached **per segment**, at the segment boundary, and terminates with `(?![\s\S])` rather than `$`. `CanonicalPath` is **byte-unchanged** (asserted in the apply script).

**Exhaustive differential** against a reference implementation of the stated law, over a corpus of 9354 strings (all strings of length 0-5 over `{a, ., /, \n, \\, \x00}` plus hand-built cases):

- v1 selectors: **96 disagreements** with the stated law, in both directions
- corrected selectors: **0 disagreements**

## 4. Guard: bounds and the absent/null distinction

The v1 guard checked only the regex, and used `u.get("memberPackageRoots")`, which conflates absent with explicitly null. Both fixed:

- All selector bounds are now **read from the schema**, not just the pattern: `_UNIT_ROOT_BOUNDS` / `_MEMBER_ROOT_BOUNDS` take `minLength`/`maxLength` from the same `$defs` entries the patterns come from. A pattern alone cannot see length.
- `"memberPackageRoots" not in u` → **permitted** (the model's own `_cargo_roots_of_units` already reads it as `.get(..., [])`, so a minimal caller naming no member roots is lawful). Present-and-null → refused as `explicit-null`.
- Type / length / grammar are reported as three distinct details, because they are three different defects.
- Scope is documented and held: no `unitKind`, `markerSha256`, `provenance` or ordinal checks; the reverted `default_capability_selection` guard is **not** reintroduced (the file still has exactly two call sites, `assign_membership` and `unit_scope_descriptor`).

Diagnostics now distinguish every case, each naming the exact selector and location:

```
…units[0].rootPath:#/$defs/InternalUnitRootV1:absent
…units[0].rootPath:#/$defs/InternalUnitRootV1:explicit-null
…units[0].rootPath:#/$defs/InternalUnitRootV1:not-a-string
…units[0].rootPath:#/$defs/InternalUnitRootV1:length=4097:bounds=0..4096
…units[0].memberPackageRoots:explicit-null
…units[0].memberPackageRoots:not-a-list
…units[0].memberPackageRoots[0]:#/$defs/CanonicalRelativeDirV1:length=0:bounds=1..4096
…units[0].memberPackageRoots[0]:#/$defs/CanonicalRelativeDirV1:'.'
```

## 5. Controls — executable before/after (56 cases, same matrix both trees)

| group | v1 → v2 |
|---|---|
| `a\n/../b`, `a\n/./b`, `\n/.`, `\n/..` | **ADMIT → REFUSE** (exact dot segments) |
| `a/.\n`, `a/..\n`, `.\n`, `..\n` | **REFUSE → ADMIT** (lawful newline-bearing segments) |
| `a\n/b`, `a\n`, `a/b\n`, `a\u2028/b`, `a\r/../b` | unchanged |
| rootPath at 4096 / at 4097 | ADMIT / **ADMIT → REFUSE** |
| member at 4096 / 4097 / empty | ADMIT / **ADMIT → REFUSE** / REFUSE |
| `memberPackageRoots` **absent** | **ADMIT** (unchanged — permitted minimal caller) |
| `memberPackageRoots` **null** | **ADMIT → REFUSE** |
| null/int/bool/list rootPath, `[null]`, `[123]`, `["."]`, non-list members, container shapes | unchanged REFUSE |
| 19 settled cases (`''`, `crates/foo#bar`, `.hidden`, `..a`, `a//b`, `/abs`, `a\b`, `a\x00b`, …) | unchanged |

Summary: v1 **9 law mismatches + 2 selector/guard disagreements** → v2 **0 and 0**. Exactly eleven intended behaviour changes, nothing else.

**Three-way agreement** (stated law / declarative jsonschema validation of the selector / early guard), including declared length bounds, over the full 9351-string corpus: v1 **98 disagreements**, v2 **0**. That is the direct evidence for "pattern/schema and early guard must agree for the representation being claimed" — and note it also shows v1's guard and schema agreed *with each other* while both deviated from the law, which is why only a law-referenced test could catch it.

**Core F-04 preserved:** v1's own 13-case `demo_f04.py`, run unmodified against v2, returns results **identical to v1** in all 13 cases.

## 6. Deliverable

`scratch/output/` — manifest `evidence-manifest-v2.json` sha256 `d4de3783d924dbd8d742417f6cfc348118cc13f7cde03aaf4569784a6a495bd9`, 11 evidence files, `REPRODUCE-v2.md`.

**One patch, 108 lines, two files** (`patch-10-f04-selector-segment-law-and-guard-bounds.diff`, sha256 `4b266ec790dcb9aa0eb97f3b6f1389ff4e41d7c9b3bf858034915deef226fd4c`):

| file | frozen25 | v1 | v2 |
|---|---|---|---|
| `native/native-evidence.schemas.v2.json` | `d8e9a1fcaa98` | `3f03ded5fabb` | `ea8ef7fc8432` |
| `native/native_evidence_model.v2.py` | `2b57bfc34af4` | `6bf606bf7f7b` | `d9a2daca30a8` |

Confirmed: only these two files differ between v1/src25 and v2/src25.

**Deliberately not done here:** pins and the six fixture/pin dependencies are **not** rebound, and the ~6-minute reference/evaluator suites are **not** re-run, since the native schema bytes move again and you merge with completed discovery v2 and run the integrated suites once. Intermediate failures from v1 are preserved in v1's evidence, unchanged.

## 7. Wording correction I am carrying forward

You are right about my v1 phrasing. Identical `check-identity.py` report bytes showed **unchanged results for the tested fixtures**, not unchanged behaviour overall. My correction changes behaviour by design — that is its point — and the v1 suites simply contained no fixture exercising the changed roots. In this turn the behaviour change is stated as such: eleven enumerated admit/refuse transitions, with the before/after matrix rather than a "no change" claim. I have not repeated the overreaching phrasing.

## 8. Open

The two-binding cell (default at ordinal 0 alongside an explicit binding at ordinal 1, with its own universe, per-`programOrdinal` inventories and coverage accounts) remains **untested** — unchanged from v1. All seven author Runs and three controls still need reminting against the final merged native schema; you are tracking that and I make no replay claim for them against this successor.
