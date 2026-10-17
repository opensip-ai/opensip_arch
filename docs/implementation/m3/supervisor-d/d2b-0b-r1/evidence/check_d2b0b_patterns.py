"""D2b-0b's pattern-profile check. (1) The candidate's patterns.ts table is the M1 rendering of the profile's rows plus
the base table's three entries the profile does not list, with every base entry unchanged and one entry added.
(2) The differential: the M1 value set (prefixes, terminators, path segments, identity endings) plus SubjectIdV1's
targeted values, each recorded by the Python `re.search` reference for every profile row, then compared with Node's
`u`-flag RegExp over the translations (pattern_differential.mjs). Usage: <out dir>."""
from pathlib import Path
import json, re, subprocess, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d2b0b'); P = W.parent / 'opensip'; EV = Path(__file__).resolve().parent
O = Path(sys.argv[1]); O.mkdir(parents=True, exist_ok=True)
NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
PF = 'tools/contracts/runtime/pattern-profile.json'; PT = 'tools/contracts/runtime/patterns.ts'
def table_of(text):
    m = text[text.index('new Map<string, string>(') + len('new Map<string, string>('):]; return json.loads(m[:m.index(']);') + 1])
profile = json.loads((W / PF).read_bytes()); base_profile = json.loads((P / PF).read_bytes())
table = table_of((W / PT).read_text()); base_table = table_of((P / PT).read_text())
rows = [[r['source'], r['ecma262Unicode']] for r in profile['patterns']]
outside = [t for t in base_table if t[0] not in {r[0] for r in rows}]
added = [t for t in table if t not in base_table]
ok_table = (sorted(rows + outside) == table and all(t in table for t in base_table) and len(added) == 1
            and added[0][0] == '^[a-z][a-z0-9-]*:[^\\u0000-\\u001f\\u007f-\\u009f]+(?![\\s\\S])' and added[0][0] == added[0][1]
            and [r for r in profile['patterns'] if r in base_profile['patterns']] == base_profile['patterns'])
# The M1 value set (trials/ts-runtime-02/subject/pattern-profile.py), then SubjectIdV1's targeted values.
values = {'', '.', '..', '/', '//', '/a', 'a//b', 'a/./b', 'a/../b', 'a/b', 'a\\b', 'a\x00b'}
terminators = ['\n', '\r', '\u2028', '\u2029', '\x85', '\r\n']
fragments = ['a', '.', '..', '/..', '../a', 'a/..', '/../../etc/passwd', 'x/y',
             'exec1_' + 'a' * 32, 'req1_' + 'a' * 32, 'closure2:' + 'a' * 64,
             'security.repo-execution-grant.v2:' + 'a' * 64, '1.2.3', '\u00a0', '\u2003', '\U0001f600']
fragments += ['ts:a', 'rs:crate::module::Item', 'a:b', 'a-b0:c', 'a:', ':a', 'A:b', '0a:b', 'a_b:c', 'a b:c', 'a:\x00', 'a:\x1f', 'a:\x7f',
              'a:\x80', 'a:\x9f', 'a:\xa0', 'a:\U0001f600', 'a:b c', 'a::b', 'sym:' + 'x' * 64]
for text in fragments:
    values.add(text)
    for end in terminators:
        values.update([end + text, text + end, 'a' + end + text, text + end + '/..', text + '/' + end + '../x', text + end + end])
values = sorted(values)
expected = [[bool(re.search(r['source'], v)) for v in values] for r in profile['patterns']]
(O / 'pattern-cases.json').write_text(json.dumps(dict(patterns=[r['source'] for r in profile['patterns']], values=values, expected=expected), indent=2) + '\n')
r = subprocess.run([NODE, str(EV / 'pattern_differential.mjs'), str(W / PF), str(O / 'pattern-cases.json'), str(O / 'pattern-differential.json')], capture_output=True)
(O / 'pattern-differential.log').write_bytes(r.stdout + r.stderr)
diff = json.loads((O / 'pattern-differential.json').read_bytes()) if r.returncode == 0 else None
sid = profile['patterns'].index(next(x for x in profile['patterns'] if x['source'] == added[0][0])) if added else None
out = dict(tableIsProfileRenderingPlusOutside=ok_table, tableEntries=len(table), baseTableEntries=len(base_table), profileRows=len(rows),
           entriesOutsideProfile=[t[0] for t in outside], added=added, differential=dict(exit=r.returncode, comparisons=diff and diff['comparisons'],
           mismatches=diff and len(diff['mismatches'])), subjectIdAccepts=sum(expected[sid]) if sid is not None else None)
(O / 'pattern-check.json').write_text(json.dumps(out, indent=2) + '\n'); print(json.dumps(out))
sys.exit(0 if ok_table and r.returncode == 0 else 1)
