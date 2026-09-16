"""(C) Real parent + pinned Python child with probe prepare.py (rebound).

C1 reports attempted effects on stderr and exits 1. C2 leaves link/special outputs and exits 0.
"""
import json
from rebind import *

victim = WORK / 'victim-python'; victim.mkdir(exist_ok=True)
canary = victim / 'canary.txt'; canary.write_text('python victim canary\n')
STDLIB = '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14'

C1 = r'''import os, sys
def prepare(documents, options, destination):
    r = []
    def t(name, f):
        try:
            v = f(); r.append(name + '=ALLOWED' + ('' if v is None else ':' + repr(v)[:60]))
        except BaseException as e:
            r.append(name + '=' + type(e).__name__ + ':' + str(e)[:90])
    out = sys.argv[4]
    t('rmdir-output-root', lambda: os.rmdir(out))
    t('chmod-output-root', lambda: os.chmod(out, 0o700))
    t('read-outside-canary', lambda: open(OUTSIDE).read())
    t('create-outside', lambda: open(VICTIM + '/py-written', 'w').write('x'))
    t('write-code-dir', lambda: open(sys.argv[3] + '/py-written', 'w').write('x'))
    t('append-raw-schema-input', lambda: open(sys.argv[1], 'a').write('x'))
    t('read-unpinned-stdlib-csv.py', lambda: len(open(STDLIB + '/csv.py').read()))
    t('import-unpinned-csv', lambda: __import__('csv') and None)
    t('import-socket', lambda: __import__('socket') and None)
    t('listdir-home', lambda: os.listdir('/Users/sb'))
    t('read-etc-passwd', lambda: len(open('/private/etc/passwd').read()))
    t('fork', lambda: os._exit(0) if os.fork() == 0 else os.wait() and None)
    t('symlink-in-output', lambda: os.symlink(OUTSIDE, out + '/owners.json'))
    t('read-through-symlink', lambda: open(out + '/owners.json').read())
    t('hardlink-outside-into-output', lambda: os.link(OUTSIDE, out + '/hl'))
    t('hardlink-granted-input-into-output', lambda: os.link(sys.argv[1], out + '/hl2'))
    t('mkfifo-in-output', lambda: os.mkfifo(out + '/fifo'))
    t('sys.path', lambda: sys.path)
    sys.stderr.write('\n' + '\n'.join(r) + '\n'); sys.stderr.flush()
    try:
        os.execv('/bin/sh', ['sh', '-c', 'echo exec-bin-sh=ALLOWED >&2; exit 1'])
    except BaseException as e:
        sys.stderr.write('exec-bin-sh=' + type(e).__name__ + ':' + str(e)[:80] + '\n')
    raise SystemExit(1)
'''
C2 = r'''import os, sys
def prepare(documents, options, destination):
    out = sys.argv[4]
    os.symlink(OUTSIDE, out + '/owners.json')
    os.mkfifo(out + '/rust-projection.json')
    open(out + '/ts-projection.json', 'w').write('{}')
    os._exit(0)
'''
def render(src):
    return src.replace('OUTSIDE', json.dumps(str(canary.resolve()))).replace('VICTIM', json.dumps(str(victim.resolve()))).replace('STDLIB', json.dumps(STDLIB)).encode()

report = {}
for label, src in [('C1-effects', C1), ('C2-link-special-outputs-exit0', C2)]:
    c = case(label, files={'tools/contracts/prepare.py': render(src)})
    before = snapshot(c)
    r = generate(c)
    report[label] = {**r, 'victimFiles': sorted(p.name for p in victim.iterdir()), 'canary': canary.read_text(),
                     'caseOutputsUnchanged': snapshot(c) == before}
print(json.dumps(report, indent=1))
