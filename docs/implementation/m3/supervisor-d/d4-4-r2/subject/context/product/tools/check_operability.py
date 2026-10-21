"""Operability enforcement checks (M3-O1 items 4, 10 and 19).

Standard library only. Read-only. `source` counts pattern lines under
crates/ and apps/, skipping test-only paths, and compares them to
tools/operability/exceptions.json. `lock` refuses a Cargo.lock package
named tracing or log, or any tracing-* package, unless
tools/host/dependency-policy.json names it on a row that cites an accepted
M3 law. `release-absence` refuses the development-sink and harness-sink
marker strings in a featureless release binary.

A class count is the number of source lines that contain at least one of
that class's patterns. One spawn written as process::Command::new is one
line. Swallowed lines use owner "none": each moves to dispose in O1-S.
"""
import argparse
import json
import tomllib
import re
from pathlib import Path

EXCEPTIONS = Path('tools/operability/exceptions.json')
POLICY = Path('tools/host/dependency-policy.json')
CLASSES = ('stdio', 'environment', 'process', 'swallowed')
PATTERNS = {
    'stdio': (
        'println!', 'eprintln!', 'eprint!', 'print!', 'dbg!',
        'io::stdout(', 'io::stderr(', 'libc::write(',
    ),
    'environment': ('env::var_os(', 'env::vars_os(', 'env::vars(', 'env::var('),
    'process': (
        'Command::new(', 'process::Command', 'process::exit(', 'process::abort(',
        'libc::_exit(', 'libc::abort(',
    ),
    'swallowed': ('let _ =',),
}
OWNERS = (
    'output and terminal',
    'termination',
    'crash path',
    "operability's development sink",
    'the configuration resolver',
    'platform owners that read process state',
    'supervision',
    'platform custody owners',
    'platform',
    'none',
)
# Item 10. Present only in the feature-gated sink code, never in a featureless binary.
RELEASE_MARKERS = (
    'opensip.operability.dev-sink',
    'opensip.operability.harness-sink',
)
TERMINATION_FILES = (
    'apps/cli/src/bootstrap.rs',
    'crates/host/src/outcomes.rs',
    'crates/host/src/doctor_ingress.rs',
    'crates/platform/src/crash_barrier.rs',
    'crates/platform/src/crash_barrier/driver.rs',
)


class OperabilityError(Exception):
    pass


def test_only(rel):
    parts = rel.split('/')
    return 'tests' in parts or 'benches' in parts or parts[-1].endswith('_tests.rs')


def owner_for(path, kind):
    """Lead assignment of item 19's owner class for one census row."""
    if kind == 'swallowed':
        return 'none'
    if kind == 'stdio':
        if path == 'apps/cli/src/terminal.rs':
            return 'output and terminal'
        if path == 'apps/cli/src/bootstrap.rs':
            return 'termination'
        if 'crash_barrier' in path or 'crash_matrix' in path or path.endswith('_census.rs'):
            return 'crash path'
        if path.startswith('crates/operability/'):
            return "operability's development sink"
        return 'platform'
    if kind == 'environment':
        if 'configuration' in path:
            return 'the configuration resolver'
        return 'platform owners that read process state'
    if kind == 'process':
        if 'crash_barrier' in path or 'crash_matrix' in path:
            return 'crash path'
        if path.startswith('crates/platform/') or path.startswith('crates/security/'):
            return 'platform custody owners'
        return 'supervision'
    raise OperabilityError('unknown class ' + kind)


def rust_files(repository):
    for base in ('crates', 'apps'):
        root = repository / base
        if not root.is_dir():
            continue
        for path in root.rglob('*.rs'):
            rel = path.relative_to(repository).as_posix()
            if not test_only(rel):
                yield rel, path


def scan(repository):
    counts = {}
    dispositions = []
    termination = set(TERMINATION_FILES)
    support = set()
    # The committed list may name further termination or test-support files.
    if (repository / EXCEPTIONS).is_file():
        record = json.loads((repository / EXCEPTIONS).read_text())
        termination.update(record.get('terminationFiles', ()))
        support.update(record.get('testSupportModules', ()))
    for rel, path in rust_files(repository):
        lines = path.read_text(encoding='utf-8').splitlines()
        for kind, patterns in PATTERNS.items():
            count = sum(1 for line in lines if any(pattern in line for pattern in patterns))
            if count:
                counts[(rel, kind)] = count
        text_lines = lines
        if rel not in support and any('Disposition::TestOnly' in line for line in text_lines):
            dispositions.append(rel + ': Disposition::TestOnly outside a test-only file')
        if rel not in termination and any('Disposition::ShutdownPath' in line for line in text_lines):
            dispositions.append(rel + ': Disposition::ShutdownPath outside the termination files')
    return counts, dispositions


def load_record(repository):
    path = repository / EXCEPTIONS
    if not path.is_file():
        raise OperabilityError('missing ' + EXCEPTIONS.as_posix())
    record = json.loads(path.read_text())
    rows = {}
    for row in record['rows']:
        key = (row['path'], row['class'])
        if key in rows:
            raise OperabilityError('duplicate row ' + row['path'] + ' ' + row['class'])
        if row['class'] not in CLASSES:
            raise OperabilityError('unknown class ' + row['class'])
        if row['owner'] not in OWNERS:
            raise OperabilityError('unknown owner ' + row['owner'])
        if not isinstance(row['count'], int) or row['count'] < 1:
            raise OperabilityError('count must be a positive integer')
        rows[key] = row
    ordered = [(row['path'], row['class']) for row in record['rows']]
    if ordered != sorted(ordered):
        raise OperabilityError('rows are not sorted')
    return rows


# Conservative unexpanded-source census. Ambiguous same-named calls are
# retained too: this does not infer receiver types or grant provenance.
MINT_MEMBERS = (
    'from', 'into', 'issue', 'minted', 'request_scope', 'project_scope', 'plan_scope',
    'attempt_scope', 'plan_attempt_scope', 'committed_run_scope',
    'stored_run_scope', 'owned_identity', 'held_path', 'admitted_path',
    'admitted_entry', 'declared_entry', 'pid', 'line', 'line_column',
    'test_request_scope', 'test_project_scope', 'test_committed_run_scope',
    'test_stored_run_scope',
)
MINT_OWNER_FILES = (
    'crates/operability/src/transport.rs', 'crates/operability/src/scope.rs',
    'crates/operability/src/kinds.rs', 'crates/operability/src/catalog.rs',
    'crates/operability/src/kinds/registry.rs',
    'crates/operability/src/kinds/identity_digest.rs',
    'crates/operability/src/kinds/path_ref.rs',
    'crates/operability/src/kinds/project_path.rs',
    'crates/operability/src/kinds/names.rs',
)


def rust_code(text):
    """Mask comments and string/character literals, retaining line offsets.

    This is a lexical census, including inline test modules and macro bodies.
    Lifetimes remain code; raw strings and nested block comments are masked.
    """
    out = list(text)
    raw_pattern = re.compile(r'(?:br|r)(#*)"')
    char_pattern = re.compile(r"'(?:[^'\\\n]|\\(?:u\{[0-9a-fA-F_]+\}|x[0-9a-fA-F]{2}|.))'")
    i = 0
    def mask(start, end):
        for at in range(start, end):
            if text[at] != '\n':
                out[at] = ' '
    while i < len(text):
        start = i
        if text.startswith('//', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
            mask(start, i)
        elif text.startswith('/*', i):
            i += 2
            depth = 1
            while i < len(text) and depth:
                if text.startswith('/*', i):
                    depth += 1; i += 2
                elif text.startswith('*/', i):
                    depth -= 1; i += 2
                else:
                    i += 1
            if depth:
                raise OperabilityError('unterminated Rust block comment')
            mask(start, i)
        else:
            raw = raw_pattern.match(text, i)
            if raw:
                close = '"' + raw.group(1)
                end = text.find(close, i + len(raw.group(0)))
                if end < 0:
                    raise OperabilityError('unterminated Rust raw string')
                i = end + len(close); mask(start, i)
            elif text[i] == '"':
                i += 1
                while i < len(text):
                    if text[i] == '\\':
                        i += 2
                    elif text[i] == '"':
                        i += 1; break
                    else:
                        i += 1
                mask(start, min(i, len(text)))
            elif text[i] == "'" and (char := char_pattern.match(text, i)):
                i += len(char.group(0)); mask(start, i)
            else:
                i += 1
    return ''.join(out)


def mint_inventory(repository):
    rows = []
    members = '|'.join(MINT_MEMBERS)
    call = re.compile(r'(?<![A-Za-z0-9_])(' + members + r')\s*(?:::<[^;{}]*>)?\s*\(')
    declaration = re.compile(r'\bfn\s+([A-Za-z_][A-Za-z0-9_]*)')
    for rel, path in sorted(rust_files(repository)):
        code = rust_code(path.read_text(encoding='utf-8'))
        declarations = {match.start(1): match.group(1) for match in declaration.finditer(code)}
        found = {}
        for match in call.finditer(code):
            if match.start(1) not in declarations:
                key = (match.group(1), 'call')
                found[key] = found.get(key, 0) + 1
        if rel in MINT_OWNER_FILES:
            for name in declarations.values():
                key = (name, 'definition')
                found[key] = found.get(key, 0) + 1
        for (member, kind), count in sorted(found.items()):
            rows.append({'path': rel, 'member': member, 'kind': kind, 'count': count})
    return rows


def mint_audit(repository):
    record = json.loads((repository / EXCEPTIONS).read_text())
    actual = mint_inventory(repository)
    expected = record.get('mintAudit', {}).get('rows', [])
    return [] if expected == actual else [{'class': 'mint-audit', 'reason': 'constructor and mint source census differs from audited exceptions'}]


def source_check(repository):
    repository = repository.resolve()
    counts, dispositions = scan(repository)
    rows = load_record(repository)
    missing = sorted(set(counts) - set(rows))
    extra = sorted(set(rows) - set(counts))
    changed = sorted(
        key for key in set(counts) & set(rows) if counts[key] != rows[key]['count'])
    details = []
    for path, kind in missing:
        details.append({'path': path, 'class': kind, 'reason': 'no row', 'count': counts[(path, kind)]})
    for path, kind in extra:
        details.append({'path': path, 'class': kind, 'reason': 'count below its row', 'count': 0,
                        'row': rows[(path, kind)]['count']})
    for path, kind in changed:
        have, want = counts[(path, kind)], rows[(path, kind)]['count']
        reason = 'count above its row' if have > want else 'count below its row'
        details.append({'path': path, 'class': kind, 'reason': reason, 'count': have, 'row': want})
    for item in dispositions:
        details.append({'reason': item})
    details.extend(mint_audit(repository))
    return {'passed': not details, 'rows': len(rows), 'findings': details}


def lock_check(repository):
    repository = repository.resolve()
    lock = tomllib.loads((repository / 'Cargo.lock').read_text())
    policy_path = repository / POLICY
    policy = json.loads(policy_path.read_text()) if policy_path.is_file() else {'rows': []}
    admitted = set()
    for row in policy.get('rows', ()):
        law = row.get('law')
        if row.get('name') and isinstance(law, dict) and law.get('path'):
            admitted.add(row['name'])
    found = []
    for package in lock['package']:
        name = package['name']
        if name in ('tracing', 'log') or name.startswith('tracing-'):
            if name not in admitted:
                found.append(name)
    return {'passed': not found, 'found': sorted(found)}


def release_absence(binary):
    data = Path(binary).read_bytes()
    found = [marker for marker in RELEASE_MARKERS if marker.encode() in data]
    return {'passed': not found, 'bytes': len(data), 'found': found, 'strings': list(RELEASE_MARKERS)}


def proposed_rows(repository):
    """The census this tree would commit. Used to write the list, not to bypass it."""
    counts, _ = scan(repository.resolve())
    rows = []
    for (path, kind), count in sorted(counts.items()):
        rows.append({'path': path, 'class': kind, 'count': count, 'owner': owner_for(path, kind)})
    return {
        'schemaVersion': 1,
        'terminationFiles': list(TERMINATION_FILES),
        'testSupportModules': [],
        'rows': rows,
        'mintAudit': {'schemaVersion': 1, 'standing': 'Conservative lexical call census and complete owner-file definitions; not receiver type inference or mint authority', 'rows': mint_inventory(repository)},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    source = commands.add_parser('source', help='count production pattern lines against the exception list')
    source.add_argument('--repository', required=True, type=Path)
    lock = commands.add_parser('lock', help='refuse tracing and log in Cargo.lock')
    lock.add_argument('--repository', type=Path, default=Path('.'))
    absence = commands.add_parser('release-absence', help='refuse sink markers in a featureless release binary')
    absence.add_argument('--binary', required=True, type=Path)
    absence.add_argument('--repository', type=Path, default=Path('.'))
    args = parser.parse_args()
    try:
        if args.command == 'source':
            result = source_check(args.repository)
        elif args.command == 'lock':
            result = lock_check(args.repository)
        else:
            result = release_absence(args.binary)
    except (OSError, ValueError, KeyError, TypeError, tomllib.TOMLDecodeError, OperabilityError) as exc:
        parser.exit(1, 'operability check refused: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
