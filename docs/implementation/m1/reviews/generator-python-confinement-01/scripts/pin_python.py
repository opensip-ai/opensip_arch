"""Derive and pin the exact host interpreter grants for the confined preparation child.

1. Run the real entry confined under a discovery profile (stdlib subpath readable,
   lib-dynload mappable) with -X importtime, recording every imported module name.
2. Resolve each name to its origin with the same interpreter (-I -B -S, find_spec only).
3. Write logs/python-grants.json: exact stdlib sources, extension modules (with
   linkage), directories listed by the path finder, and sha256 pins.
"""
import json, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confine as C

RESOLVE = r'''
import importlib.util, json, sys
out = {}
for name in json.loads(sys.argv[1]):
    spec = importlib.util.find_spec(name)
    if spec is None:
        out[name] = None
        continue
    out[name] = {'origin': spec.origin, 'hasLocation': spec.has_location,
                 'search': list(spec.submodule_search_locations or [])}
print(json.dumps(out))
'''


def main():
    if not sys.flags.isolated:
        raise SystemExit('run with python3 -I')
    C.verify_host()
    output = C.RUNS / 'discovery/output'
    if output.parent.exists():
        shutil.rmtree(output.parent)
    output.mkdir(parents=True)
    text = C.profile(None, reads=C.child_reads(), output=output, discovery=True)
    record = C.run('discovery', [C.EXECUTABLE, *C.FLAGS, '-X', 'importtime', C.ENTRY, C.INPUTS / 'raw-schemas.json',
                                 C.INPUTS / 'options.json', C.CODE, output], text=text)
    if record['exitCode'] != 0:
        raise SystemExit('discovery run failed: ' + record['stderr'][-2000:])
    names = []
    for line in record['stderr'].splitlines():
        if line.startswith('import time:') and '|' in line and 'self [us]' not in line:
            name = line.rsplit('|', 1)[1].strip()
            if name not in names:
                names.append(name)
    resolved = json.loads(subprocess.run([str(C.EXECUTABLE), *C.FLAGS, '-c', RESOLVE, json.dumps(names)], env={},
                                         capture_output=True, text=True, check=True).stdout)
    sources, extensions, internal = [], [], {}
    directories = {str(C.STDLIB), str(C.STDLIB / 'lib-dynload')}
    for name, spec in resolved.items():
        if spec is None:
            internal[name] = 'not-found'  # optional platform imports (e.g. nt, _winapi) attempted and absent
            continue
        origin = spec['origin']
        if not spec['hasLocation']:
            internal[name] = origin  # 'built-in' / 'frozen': compiled into the pinned framework dylib
            continue
        path = Path(origin)
        if not path.is_relative_to(C.STDLIB) or 'site-packages' in path.parts or path.is_symlink():
            raise SystemExit('import outside pinned stdlib: ' + name + ' ' + origin)
        row = {'module': name, 'path': origin, 'sha256': C.sha(path)}
        if origin.endswith('.so'):
            linkage = subprocess.run(['/usr/bin/otool', '-L', origin], capture_output=True, text=True, check=True).stdout
            row['linkage'] = [l.strip().split(' (')[0] for l in linkage.splitlines()[1:]]
            extensions.append(row)
        else:
            sources.append(row)
        directories.update(spec['search'])
        directories.add(str(path.parent))
    grants = {'standing': 'explicit trusted host interpreter profile for this trial host; not a native closure proof',
              'interpreter': {'executable': {'path': str(C.EXECUTABLE), 'sha256': C.HOST_PINS[str(C.EXECUTABLE)]},
                              'library': {'path': str(C.LIBRARY), 'sha256': C.HOST_PINS[str(C.LIBRARY)]},
                              'version': subprocess.run([str(C.EXECUTABLE), *C.FLAGS, '-c', 'import sys;print(sys.version)'],
                                                        env={}, capture_output=True, text=True).stdout.strip()},
              'importOrder': names, 'builtinOrFrozen': internal,
              'sources': sorted(sources, key=lambda r: r['path']),
              'extensions': sorted(extensions, key=lambda r: r['path']),
              'directories': sorted(directories),
              'discoveryDenials': record['sandboxDenials']}
    C.GRANTS.write_text(json.dumps(grants, indent=1) + '\n')
    print(json.dumps({'modules': len(names), 'sources': len(sources), 'extensions': [r['module'] for r in extensions],
                      'directories': len(directories), 'discoveryDenials': record['sandboxDenials']}, indent=1))


if __name__ == '__main__':
    main()
