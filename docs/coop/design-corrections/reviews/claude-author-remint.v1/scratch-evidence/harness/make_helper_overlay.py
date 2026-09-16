"""Build the portable helpers overlay.

MINIMAL CORRECTION, one line per constant: every hardcoded historical path constant becomes
environment-resolvable with its historical value as the default, so unset behaviour is
byte-identical to today and a declared construction can point them at real inputs.

  OPENSIP_AUTHOR_KIT  -> KIT   (builder, cap_admit, kit_schemas, law_admit, protocol3,
                                runs, schema_admit)
  OPENSIP_AUTHOR_OUT  -> OUT   (runs [dead constant], status)
  OPENSIP_AUTHOR_REQS -> REQS  (status)

Also carries the completed root-binding v1 `_default_unit_binding` naming fix for ts_pilot.py,
which was proven output-identical there and is not part of root's runs.py change.
"""
import difflib
import hashlib
import json
import os
import shutil

R = '/private/tmp/opensip-design-corrections/claude-author-remint.v1'
PKG = R + '/package/author-helpers'
OVERLAY = R + '/scratch/helpers-overlay'
DELIVER = R + '/scratch/portable/helpers-successor'
TS_FIX = '/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch/output/files/helpers-successor/ts_pilot.py'

KIT_OLD = 'KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")'
KIT_NEW = ('KIT = Path(os.environ.get("OPENSIP_AUTHOR_KIT",\n'
           '                          "/tmp/opensip-design-corrections/consumer-b.v13/subject"))')
OUT_OLD = 'OUT = Path("/tmp/opensip-design-corrections/codex-author-followup.v1/output")'
OUT_NEW = ('OUT = Path(os.environ.get("OPENSIP_AUTHOR_OUT",\n'
           '                          "/tmp/opensip-design-corrections/codex-author-followup.v1/output"))')
REQS_OLD = 'REQS = Path("/tmp/opensip-design-corrections/consumer-b.v13/requirements.json")'
REQS_NEW = ('REQS = Path(os.environ.get("OPENSIP_AUTHOR_REQS",\n'
            '                           "/tmp/opensip-design-corrections/consumer-b.v13/requirements.json"))')

TARGETS = {
    'builder.py': [(KIT_OLD, KIT_NEW)],
    'cap_admit.py': [(KIT_OLD, KIT_NEW)],
    'kit_schemas.py': [(KIT_OLD, KIT_NEW)],
    'law_admit.py': [(KIT_OLD, KIT_NEW)],
    'protocol3.py': [(KIT_OLD, KIT_NEW)],
    'schema_admit.py': [(KIT_OLD, KIT_NEW)],
    'runs.py': [(KIT_OLD, KIT_NEW), (OUT_OLD, OUT_NEW)],
    'status.py': [(OUT_OLD, OUT_NEW), (REQS_OLD, REQS_NEW)],
}


def ensure_import_os(src):
    if '\nimport os\n' in src or src.startswith('import os\n'):
        return src, False
    lines = src.splitlines(keepends=True)
    # place beside the existing stdlib imports, before `from pathlib import Path`
    for i, l in enumerate(lines):
        if l.startswith('from pathlib import Path'):
            lines.insert(i, 'import os\n')
            return ''.join(lines), True
    for i, l in enumerate(lines):
        if l.startswith('import '):
            lines.insert(i, 'import os\n')
            return ''.join(lines), True
    raise AssertionError('no import anchor')


def main():
    if os.path.isdir(OVERLAY):
        shutil.rmtree(OVERLAY)
    shutil.copytree(PKG, OVERLAY)
    os.makedirs(DELIVER, exist_ok=True)

    rows = []
    for name, subs in sorted(TARGETS.items()):
        orig = open(os.path.join(PKG, name), encoding='utf-8').read()
        src = orig
        for old, new in subs:
            assert src.count(old) == 1, (name, old, src.count(old))
            src = src.replace(old, new, 1)
        src, added = ensure_import_os(src)
        open(os.path.join(OVERLAY, name), 'w', encoding='utf-8').write(src)
        shutil.copy2(os.path.join(OVERLAY, name), os.path.join(DELIVER, name))
        d = list(difflib.unified_diff(orig.splitlines(keepends=True), src.splitlines(keepends=True),
                                      fromfile='package/author-helpers/' + name,
                                      tofile='successor/author-helpers/' + name, n=2))
        rows.append({'file': name, 'substitutions': len(subs), 'addedImportOs': added,
                     'beforeSha256': hashlib.sha256(orig.encode()).hexdigest(),
                     'afterSha256': hashlib.sha256(src.encode()).hexdigest(),
                     'diffLines': len(d)})
        open(os.path.join(DELIVER, name + '.diff'), 'w', encoding='utf-8').write(''.join(d))

    # ts_pilot naming fix from completed root-binding v1 (does not touch runs.py)
    ts_before = hashlib.sha256(open(os.path.join(PKG, 'ts_pilot.py'), 'rb').read()).hexdigest()
    shutil.copy2(TS_FIX, os.path.join(OVERLAY, 'ts_pilot.py'))
    shutil.copy2(TS_FIX, os.path.join(DELIVER, 'ts_pilot.py'))
    ts_after = hashlib.sha256(open(TS_FIX, 'rb').read()).hexdigest()
    rows.append({'file': 'ts_pilot.py', 'substitutions': 0, 'addedImportOs': False,
                 'beforeSha256': ts_before, 'afterSha256': ts_after,
                 'note': '_default_unit_binding naming fix carried from completed root-binding v1'})

    for r in rows:
        print('%-16s subs=%-2s importOs=%-6s %s -> %s'
              % (r['file'], r['substitutions'], r['addedImportOs'],
                 r['beforeSha256'][:12], r['afterSha256'][:12]))
    unchanged = [f for f in sorted(os.listdir(PKG)) if f.endswith('.py') and f not in TARGETS
                 and f != 'ts_pilot.py']
    print('helper modules left byte-identical:', len(unchanged))
    json.dump({'standing': 'Minimal portability overlay for the bundled author helpers.',
               'changed': rows, 'unchanged': unchanged},
              open(DELIVER + '/helpers-overlay.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
