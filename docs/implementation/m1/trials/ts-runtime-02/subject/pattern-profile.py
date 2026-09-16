"""Build the bounded selected-pattern compatibility table, not a Python re port."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).parent
ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
sources = json.loads((ARCH / 'docs/implementation/m1/metadata-v2/sources.json').read_bytes())
patterns = set()

def visit(schema):
    if not isinstance(schema, dict):
        return
    if 'pattern' in schema:
        patterns.add(schema['pattern'])
    patterns.update(schema.get('patternProperties', {}))
    for key in ('properties', 'patternProperties', '$defs', 'definitions'):
        for child in schema.get(key, {}).values():
            visit(child)
    for key in ('additionalProperties', 'propertyNames', 'items', 'contains', 'if', 'then', 'else', 'not'):
        if key in schema:
            visit(schema[key])
    for key in ('allOf', 'anyOf', 'oneOf'):
        for child in schema.get(key, []):
            visit(child)

for pin in sources['schemas']:
    raw = (ARCH / pin['path']).read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
    visit(json.loads(raw))

def translate(pattern):
    # Selected patterns use no isolated \s/\S or other shorthand classes whose
    # Unicode definitions differ. Paired [\s\S] denotes every code point.
    # Preserve the existing reference dialect: '.' excludes LF only; bare '$'
    # also matches before exactly one final LF. Absolute (?![\s\S]) stays exact.
    result = []
    escaped = False
    in_class = False
    for char in pattern:
        if escaped:
            result.append(char)
            escaped = False
        elif char == '\\':
            result.append(char)
            escaped = True
        elif char == '[':
            in_class = True
            result.append(char)
        elif char == ']':
            in_class = False
            result.append(char)
        elif not in_class and char == '.':
            result.append('[^\\n]')
        elif not in_class and char == '$':
            result.append('(?=\\n?(?![\\s\\S]))')
        else:
            result.append(char)
    assert not escaped and not in_class
    return ''.join(result)

rows = [dict(source=pattern, ecma262Unicode=translate(pattern)) for pattern in sorted(patterns)]
profile = dict(schemaVersion=1, profile='opensip-selected-pattern-reference-compatibility-1',
               standing='PROPOSED; exact finite pattern table, not generic Python regex support',
               sources=sources['schemas'], patterns=rows)
(HERE / 'pattern-profile.json').write_text(json.dumps(profile, indent=2) + '\n')
table = [[row['source'], row['ecma262Unicode']] for row in rows]
(HERE / 'patterns.ts').write_text('/** Generated trial table from pattern-profile.py; reviewed source profile required. */\n'
    + 'const patterns = new Map<string, string>(' + json.dumps(table, indent=2) + ');\n'
    + 'export const selectedPattern = (pattern: string): string | undefined => patterns.get(pattern);\n')

# Terminators, Unicode space/alphabet, path segments and exact identity endings.
values = {'', '.', '..', '/', '//', '/a', 'a//b', 'a/./b', 'a/../b', 'a/b', 'a\\b', 'a\x00b'}
terminators = ['\n', '\r', '\u2028', '\u2029', '\x85', '\r\n']
fragments = ['a', '.', '..', '/..', '../a', 'a/..', '/../../etc/passwd', 'x/y',
             'exec1_' + 'a' * 32, 'req1_' + 'a' * 32, 'closure2:' + 'a' * 64,
             'security.repo-execution-grant.v2:' + 'a' * 64, '1.2.3', '\u00a0', '\u2003', '\U0001f600']
for text in fragments:
    values.add(text)
    for end in terminators:
        values.update([end + text, text + end, 'a' + end + text, text + end + '/..',
                       text + '/' + end + '../x', text + end + end])
values = sorted(values)
expected = [[bool(re.search(row['source'], value)) for value in values] for row in rows]
(HERE / 'pattern-cases.json').write_text(json.dumps(dict(values=values, expected=expected), indent=2) + '\n')
print(json.dumps(dict(patterns=len(rows), values=len(values), comparisons=len(rows) * len(values))))
