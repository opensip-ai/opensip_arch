"""a5_amendment rerun with a byte-preserving native-cases edit.

a5_amendment exited 1 (receipt retained): native-cases.v2.json does not round-trip through json.dumps(indent=1), so
re-serializing it would rewrite unrelated bytes. This probe executes a5_amendment's exact source with three asserted
changes: the stale case object is replaced by splicing the serialized new cases into the raw text at that object's
span (every other byte kept); output goes to a5-review/amended.r2, proposed-amendment.r2.diff and
receipts/a5-amendment.r2.json; the round-trip flag is replaced by a check that only the intended span changed.
"""
from pathlib import Path

src = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1/probes/a5_amendment.py').read_text()
old_nc = """doc = json.loads(nc_root)
fmt = None
for ensure in (False, True):
    if (json.dumps(doc, indent=1, ensure_ascii=ensure) + '\\n').encode('utf-8') == nc_root:
        fmt = ensure
out['nativeCasesRoundTrip'] = fmt is not None
ids = [c['id'] for c in doc['cases']]
if 'ts-tsconfig-without-allowjs-excludes-js' not in ids:
    problems.append('stale case not found')
else:
    at = ids.index('ts-tsconfig-without-allowjs-excludes-js')
    doc['cases'][at:at + 1] = NEW_CASES
nc = json.dumps(doc, indent=1, ensure_ascii=bool(fmt)) + '\\n'
"""
new_nc = """raw_nc = nc_root.decode('utf-8')
anchor = '   "id": "ts-tsconfig-without-allowjs-excludes-js",\\n'
idx = raw_nc.find(anchor)
if raw_nc.count(anchor) != 1:
    problems.append('stale case anchor count %d' % raw_nc.count(anchor))
start = raw_nc.rfind('\\n  {\\n', 0, idx) + 1
end = raw_nc.find('\\n  },\\n', idx) + len('\\n  },\\n')
span = json.loads(raw_nc[start:end].rstrip().rstrip(','))
if span.get('id') != 'ts-tsconfig-without-allowjs-excludes-js':
    problems.append('span is not the stale case')
block = ''.join('\\n'.join('  ' + line for line in json.dumps(c, indent=1, ensure_ascii=False).split('\\n')) + ',\\n'
                for c in NEW_CASES)
nc = raw_nc[:start] + block + raw_nc[end:]
before_doc, after_doc = json.loads(nc_root), json.loads(nc)
at = [c['id'] for c in before_doc['cases']].index('ts-tsconfig-without-allowjs-excludes-js')
expected_doc = dict(before_doc, cases=before_doc['cases'][:at] + NEW_CASES + before_doc['cases'][at + 1:])
out['nativeCasesRoundTrip'] = (after_doc == expected_doc and nc.startswith(raw_nc[:start]) and nc.endswith(raw_nc[end:]))
"""
edits = [
    (old_nc, new_nc),
    ("AM = OUTDIR / 'amended'", "AM = OUTDIR / 'amended.r2'"),
    ("(OUTDIR / 'proposed-amendment.diff')", "(OUTDIR / 'proposed-amendment.r2.diff')"),
    ("(BASE / 'receipts' / 'a5-amendment.json')", "(BASE / 'receipts' / 'a5-amendment.r2.json')"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit('edit anchor count %d: %r' % (src.count(old), old[:60]))
    src = src.replace(old, new)
exec(compile(src, 'a5_amendment.py (byte-preserving native-cases splice)', 'exec'), {'__name__': '__main__'})
