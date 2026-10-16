"""S10b checks: the TypeScript configuration remedy successor (M3-B r10, item 25 row S10b).

Run from the architecture checkout root:

    python3 -I -B docs/implementation/m3/config-discovery-b/s10b-remedy/evidence/check.py

It reads only the two S10 native-model copies (the parents) and this unit's two successor copies, as text and
as Python syntax trees; it executes neither model. It checks that each successor copy is its parent with exactly
two edits (the remedy string keyed by `native.typescript-config-unresolved` and one comment line), that the
remedy names every item 14a bound and stays true for all four internal keys, and that every other remedy,
`D9_MAP` and the rest of each file are byte-identical. Then it plants negative controls (mutants), each of which
must fail. It writes `checks.json` beside itself.
"""
from pathlib import Path
import ast
import hashlib
import json
import sys

UNIT = Path('docs/implementation/m3/config-discovery-b')
PARENT = UNIT / 's10-tsc/reference'
SUCCESSOR = UNIT / 's10b-remedy/reference'
COPIES = ('native_evidence_model.py', 'native_evidence_model.v2.py')
# The accepted S10 copies (contract successor 167), pinned.
PARENT_PINS = {
    'native_evidence_model.py': (321895, '0e05bbf08b801009d786fec86a35aca83feb972a9f995b59ed64fe1edff59af5'),
    'native_evidence_model.v2.py': (321775, '4b88aebb493232a0e51957c4fd899cd9b4f1a2fe3e74fbae4f7734eb25038d63'),
}
KEY = 'native.typescript-config-unresolved'
OLD = 'keep each file within 64 KiB and the graph within 32 files;'
NEW = ('keep each file within 64 KiB and 64 extends entries, each configuration file path within 4,096 characters, '
       'and the graph within 32 files;')
COMMENT_AFTER = '    # alias, context-free, to this one public detail, so this one string is true for every one of them.\n'
COMMENT = ('    # M3-B r10 (successor S10b): the bounds clause also names item 14a\'s 64-entry extends and 4,096-character '
           'path bounds.\n')
# Item 14a's bounds (r8 and r10), each of which the remedy must name.
BOUNDS = ('64 KiB', '64 extends entries', '4,096 characters', '32 files')
# Each internal key and the remedy clause that answers it (the remedy is one string true for all four).
CLAUSES = {
    'native.typescript-config-extends-unresolved': 'make every extends base of the named configuration file present as a regular file inside the project',
    'native.typescript-config-extends-cycle': 'break any extends cycle',
    'native.typescript-config-bound': NEW,
    'native.typescript-config-malformed': "or correct the file's syntax, so that it is JSONC",
}


class Fail(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Fail(message)


def remedies(text, name):
    """The literal `PUBLIC_ROUTE_REMEDIES` dict of one model copy, from its syntax tree."""
    tree = ast.parse(text, name)
    found = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PUBLIC_ROUTE_REMEDIES' for t in n.targets)]
    require(len(found) == 1 and isinstance(found[0].value, ast.Dict), name + ': one literal PUBLIC_ROUTE_REMEDIES')
    out = {}
    for k, v in zip(found[0].value.keys, found[0].value.values):
        key, value = ast.literal_eval(k), ast.literal_eval(v)
        require(key not in out, name + ': duplicate remedy key ' + key)
        out[key] = value
    return out


def check(parents, successors, clauses=None):
    """Every check over {copy name: text}; raises Fail on the first violation.

    `clauses` maps each copy to the bounds clause it claims (NEW unless a negative control supplies another), so a
    control can build a consistent successor and reach the later checks rather than stopping at the first."""
    clauses = clauses or {}
    results = []
    news = []
    for name in COPIES:
        parent, successor = parents[name], successors[name]
        new = clauses.get(name, NEW)
        # 1. Exactly the two edits.
        require(parent.count(OLD) == 1 and parent.count(COMMENT_AFTER) == 1, name + ': parent anchors')
        expected = parent.replace(OLD, new).replace(COMMENT_AFTER, COMMENT_AFTER + COMMENT)
        require(successor == expected, name + ': the successor is not its parent with exactly the remedy and comment edits')
        results.append(name + ': parent with exactly two edits')
        # 2. The remedies table: only the one key's value changes.
        before, after = remedies(parent, name), remedies(successor, name)
        require(sorted(before) == sorted(after), name + ': remedy keys changed')
        require(all(before[k] == after[k] for k in before if k != KEY), name + ': another remedy changed')
        require(after[KEY] == before[KEY].replace(OLD, new) and after[KEY] != before[KEY], name + ': the remedy is not the S10 text with the bounds clause rewritten')
        results.append(name + ': only the ' + KEY + ' remedy changes')
        # 3. It names every bound and answers every internal key.
        for bound in BOUNDS:
            require(bound in after[KEY], name + ': the remedy omits ' + bound)
        for internal, clause in CLAUSES.items():
            wanted = new if internal == 'native.typescript-config-bound' else clause
            require(wanted in after[KEY], name + ': no clause for ' + internal)
        results.append(name + ': names ' + ', '.join(BOUNDS) + ' and answers all four internal keys')
        news.append(after[KEY])
    # 4. One string in both copies.
    require(len(set(news)) == 1, 'the two copies register different remedies')
    results.append('both copies register one remedy string')
    return results, news[0]


def build(parents, clause_for, drop=None):
    """A consistent successor set: each parent with `clause_for[name]` as its bounds clause and the comment, and
    with `drop` removed from both parent and successor (so only the semantic checks can see it)."""
    ps = {n: parents[n].replace(drop, '') if drop else parents[n] for n in COPIES}
    ss = {n: ps[n].replace(OLD, clause_for.get(n, NEW)).replace(COMMENT_AFTER, COMMENT_AFTER + COMMENT) for n in COPIES}
    return ps, ss, clause_for


def mutants(parents, successors):
    """Negative controls. Each runs `check` on a planted fault and must fail at the named check."""
    def edit(name, old, new):
        def apply():
            out = dict(successors)
            require(out[name].count(old) >= 1, 'mutant anchor: ' + old[:40])
            out[name] = out[name].replace(old, new, 1)
            return parents, out, {}
        return apply

    py, v2 = COPIES
    planted = {
        # Consistent successors: the whole-file check passes, so the named semantic check must catch them.
        'entries-bound-dropped': (lambda: build(parents, {n: NEW.replace(' and 64 extends entries', '') for n in COPIES}), 'omits 64 extends entries'),
        'path-bound-dropped': (lambda: build(parents, {n: NEW.replace(' each configuration file path within 4,096 characters,', '') for n in COPIES}), 'omits 4,096 characters'),
        'cycle-clause-dropped': (lambda: build(parents, {}, drop='break any extends cycle; '), 'no clause for native.typescript-config-extends-cycle'),
        'v2-copy-differs': (lambda: build(parents, {v2: NEW.replace('4,096 characters', '4096 characters,').replace('4096 characters,,', '4096 characters,')}), 'omits 4,096 characters'),
        'copies-disagree': (lambda: build(parents, {v2: NEW.replace('64 KiB and 64', '64 KiB and at most 64')}), 'different remedies'),
        # Inconsistent edits: the whole-file check catches them.
        'v2-copy-left-at-parent': (lambda: (parents, dict(successors, **{v2: parents[v2]}), {}), 'exactly the remedy and comment edits'),
        'another-remedy-altered': (edit(py, '"install or enable the provider"', '"install, enable or update the provider"'), 'exactly the remedy and comment edits'),
        'd9-map-altered': (edit(py, '"code": "CONFIG.INVALID"', '"code": "CONFIG.UNREADABLE"'), 'exactly the remedy and comment edits'),
        'comment-only-no-remedy-change': (lambda: (parents, {n: parents[n].replace(COMMENT_AFTER, COMMENT_AFTER + COMMENT) for n in COPIES}, {}), 'exactly the remedy and comment edits'),
    }
    out = []
    for mid, (make, expect) in planted.items():
        ps, ss, clauses = make()
        try:
            check(ps, ss, clauses)
        except Fail as error:
            out.append(dict(id=mid, failed=True, expected=expect, reason=str(error), atExpectedCheck=expect in str(error)))
        else:
            out.append(dict(id=mid, failed=False, expected=expect, reason='check passed', atExpectedCheck=False))
    return out


def main():
    root = Path.cwd()
    parents, successors, pins = {}, {}, []
    for name in COPIES:
        for label, base, store in (('parent', PARENT, parents), ('successor', SUCCESSOR, successors)):
            raw = (root / base / name).read_bytes()
            store[name] = raw.decode('utf-8')
            pins.append(dict(role=label, path=str(base / name), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    for name, (size, digest) in PARENT_PINS.items():
        row = next(p for p in pins if p['role'] == 'parent' and p['path'].endswith('/' + name))
        require(row['bytes'] == size and row['sha256'] == digest, name + ': the parent is not the accepted S10 copy')
    results, remedy = check(parents, successors)
    planted = mutants(parents, successors)
    passed = all(m['failed'] and m['atExpectedCheck'] for m in planted)
    body = dict(schemaVersion=1, unit='S10b', standing='Design evidence for the S10b remedy successor (M3-B r10); not qualification.',
                pins=pins, checks=results, remedy=remedy, mutants=planted, allPassed=passed)
    (root / UNIT / 's10b-remedy/evidence/checks.json').write_text(json.dumps(body, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(checks=len(results), mutants=len(planted), mutantsFailed=sum(m['failed'] for m in planted), allPassed=passed)))
    return 0 if passed else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (Fail, OSError, ValueError) as error:
        print('S10b check failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
