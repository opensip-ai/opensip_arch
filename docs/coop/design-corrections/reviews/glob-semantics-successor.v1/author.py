from pathlib import Path
import json,hashlib
root=Path(__file__).parent;src=root/'source';changes=[]
def put(p,text):
 f=src/p;old=f.read_bytes() if f.exists() else None
 if old is not None:
  b=root/'before-images'/p;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(old)
 new=text.encode();f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(new)
 changes.append({'path':p,'beforeSha256':hashlib.sha256(old).hexdigest() if old is not None else None,'sha256':hashlib.sha256(new).hexdigest(),'bytes':len(new)})
f='docs/coop/design-corrections/foundation/'
w='docs/coop/design-corrections/workflows/'
put(f+'glob-pattern-contract.v1.md','''# Portable glob matching — version 1

This normative owner specifies the matching predicate used by `GlobPattern`,
ScopeDocument path matching, and string field filters with `cmp: glob`. It makes
matching reconstructable without reference source code. The owning schema still
admits each pattern and candidate value; this predicate neither coerces values nor
changes those admission rules.

## Matching law

Matching is case sensitive and anchored to the entire candidate string. There is
no implicit prefix, suffix, recursive search, filesystem lookup, directory test,
or exclusion of dotfiles. Split both pattern and candidate at every literal `/`,
preserving empty segments. Do not resolve `.` or `..`, remove separators, rebase,
case-fold, or normalize Unicode in this predicate. A LogicalPath candidate must
already satisfy its owner; other admitted string fields need not be paths.

An ordinary pattern segment matches exactly one candidate segment, in full:

- `*` matches zero or more Unicode scalar values within that segment.
- `?` matches exactly one Unicode scalar value within that segment, not one byte
  or one displayed grapheme. Neither wildcard consumes `/`.
- Every other character matches itself. Braces and brackets have no expansion or
  character-class meaning. There is no escape syntax; the GlobPattern schema
  excludes backslash and NUL. Consecutive stars in an ordinary segment have the
  same matching power as one star.

A pattern segment that is exactly `**` instead matches zero or more whole
candidate segments. This rule applies at the beginning, middle, and end, and may
consume the final filename segment. It does not require a directory. A segment
such as `a**b` is ordinary, and cannot consume a separator.

Equivalently, let `P` and `S` be the split sequences. A match at `(i,j)` succeeds
at the end of `P` exactly when `j` is also at the end of `S`. For `P[i] = **`, it
succeeds if any `k` from `j` through `len(S)`, inclusive, makes `(i+1,k)` succeed.
Otherwise it succeeds exactly when `j < len(S)`, the ordinary segment matches
`S[j]`, and `(i+1,j+1)` succeeds. The predicate begins at `(0,0)`. This defines
results, not an implementation algorithm or a requirement to use recursion.

## Required examples

| Pattern | Candidate | Matches |
|---|---|---|
| `**/*.ts` | `a.ts` | true |
| `**/*.ts` | `src/nested/a.ts` | true |
| `*.ts` | `src/a.ts` | false |
| `src/**` | `src` | true |
| `src/**` | `src/legacy.js` | true |
| `src/**` | `src/nested/legacy.js` | true |
| `src/**/*` | `src` | false |
| `src/**/*` | `src/legacy.js` | true |
| `a/**/b` | `a/b` | true |
| `a/**/b` | `a/x/y/b` | true |
| `a/*/b` | `a/b` | false |
| `a**b` | `a/x/b` | false |
| `a**b` | `axxb` | true |
| `*` | `.hidden` | true |
| `a.ts` | `A.ts` | false |
| `a.ts` | `a.ts.extra` | false |
| `?.ts` | `é.ts` (one scalar before the dot) | true |
| `?.ts` | `é.ts` (`e` plus combining acute accent) | false |
| `[ab].ts` | `a.ts` | false |
| `[ab].ts` | `[ab].ts` | true |
| `{a,b}.ts` | `a.ts` | false |
| `{a,b}.ts` | `{a,b}.ts` | true |

A trailing slash in a pattern is an empty final segment, not a directory flag.
For example `src/` does not match the admitted LogicalPath `src`. These rules do
not make an otherwise invalid LogicalPath admissible.

## Composition and authority

For a ScopeDocument, a candidate is selected if at least one `include` pattern
matches and no `exclude` pattern matches. Exclusion wins a matching inclusion.
Other owners continue to specify their own defaults, absent/empty-list behavior,
and non-glob prefix predicates; the matching law does not replace those rules.
In particular, scope selection is not evidence of exhaustive extraction or native
coverage. This contract grants no repair authorization and changes no identity
recipe. The reference `workflows_model.v1.glob_match` implements this predicate;
the normative law and examples above are sufficient to reconstruct it.
''')
for p in [w+'schemas/common.schema.json',w+'schemas/evaluator3/common.schema.json']:
 t=(src/p).read_text();old="Closed glob over LogicalPath: literal characters plus '*', '?' and a whole-segment '**'. No brace, class or escape syntax."
 new="Portable glob matching is normative in docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md: full-string, case-sensitive matching; '*' and '?' stay within a segment; whole-segment '**' matches zero or more segments including a final filename. Braces and brackets are literal; no escape syntax. Candidate admission remains owned by its field."
 assert old in t;put(p,t.replace(old,new))
p=f+'atom-evaluation-contract.v1.md';t=(src/p).read_text();old='Glob matching reuses `workflows_model.v1.glob_match` (so `**/*.ts` matches root `a.ts`).';new='Glob matching follows the normative [portable glob contract](glob-pattern-contract.v1.md), including terminal `**` and Unicode scalar matching. The reference implements it with `workflows_model.v1.glob_match`.';assert old in t;put(p,t.replace(old,new))
# Workflow projection and chapter links are deferred until the repair coauthor releases ownership.
p=f+'check-atoms.v1.py';t=(src/p).read_text();marker='def test_glob_root():'
code='''def test_portable_glob_contract():
    # Prescribed normative examples and boundary controls, not generated expected results.
    vectors = [
        ("**/*.ts", "a.ts", True), ("**/*.ts", "src/nested/a.ts", True),
        ("*.ts", "src/a.ts", False), ("src/**", "src", True),
        ("src/**", "src/legacy.js", True), ("src/**", "src/nested/legacy.js", True),
        ("src/**/*", "src", False), ("src/**/*", "src/legacy.js", True),
        ("a/**/b", "a/b", True), ("a/**/b", "a/x/y/b", True),
        ("a/*/b", "a/b", False), ("a**b", "a/x/b", False),
        ("a**b", "axxb", True), ("*", ".hidden", True),
        ("a.ts", "A.ts", False), ("a.ts", "a.ts.extra", False),
        ("?.ts", "é.ts", True), ("?.ts", "e\\u0301.ts", False),
        ("[ab].ts", "a.ts", False), ("[ab].ts", "[ab].ts", True),
        ("{a,b}.ts", "a.ts", False), ("{a,b}.ts", "{a,b}.ts", True),
        ("src/", "src", False), ("src/*", "src/a/b", False),
        ("a*b", "ab", True), ("a?b", "ab", False),
        ("?.ts", "🙂.ts", True), ("é.ts", "e\\u0301.ts", False),
        ("a/./b", "a/b", False), ("/a", "a", False),
    ]
    for pattern, candidate, expected in vectors:
        actual = AM.W.glob_match(pattern, candidate)
        if actual is not expected:
            fail(f"portable glob {pattern!r} / {candidate!r}: {actual!r} != {expected!r}")
    scope = {"include": ["**/*.ts"], "exclude": ["src/**"]}
    if not AM.W.in_scope(scope, "a.ts") or AM.W.in_scope(scope, "src/a.ts"):
        fail("ScopeDocument exclusion must win inclusion")


'''
assert marker in t;t=t.replace(marker,code+marker);t=t.replace('    test_glob_root,','    test_glob_root,\n    test_portable_glob_contract,');put(p,t)
(root/'changed-files.json').write_text(json.dumps({'standing':'AUTHOR_PENDING_REVIEW','files':changes,'deferredLinks':['workflows/workflow-projection-contract.v3.md','docs/v2/contracts/product-v1/workflows-and-surfaces.md']},indent=2)+'\n')
print(len(changes),'authored files')
