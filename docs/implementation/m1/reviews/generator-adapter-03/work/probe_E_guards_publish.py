"""(E) Malformed profile guards, NR1 through the real parent/child, closure guards, publish preflight."""
import copy, importlib.util, json, os, shutil, sys
from rebind import *

assert sys.flags.isolated
spec = importlib.util.spec_from_file_location('g', WORK / 'base/tools/generate_contracts.py')
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
report = {}

def outcome(f):
    try:
        f(); return 'ACCEPTED'
    except G.GenerationError as e:
        return 'GenerationError: ' + str(e)[:120]
    except Exception as e:
        return 'OTHER ' + type(e).__name__ + ': ' + str(e)[:120]

profile = json.loads((WORK / 'base/tools/contracts/python-profile.json').read_text())
PFX = str(Path(profile['library']['path']).parent)
py_mut = {
    'executable-via-opt-symlink-path': lambda d: d['executable'].update(path=d['executable']['path'].replace('/opt/homebrew/Cellar/python@3.14/3.14.6', '/opt/homebrew/opt/python@3.14')),
    'library-renamed': lambda d: d['library'].update(path=PFX + '/Python2'),
    'file-dotdot-path': lambda d: d['files'][0].update(path=PFX + '/lib/python3.14/json/../contextlib.py'),
    'file-pyc-suffix': lambda d: d['files'][1].update(path=PFX + '/lib/python3.14/__pycache__/contextlib.cpython-314.pyc'),
    'file-site-packages': lambda d: d['files'][1].update(path=PFX + '/lib/python3.14/site-packages/x.py'),
    'file-duplicate-row': lambda d: d['files'].__setitem__(1, copy.deepcopy(d['files'][0])),
    'file-row-extra-key': lambda d: d['files'][0].update(mode=420),
    'file-bytes-bool': lambda d: d['files'][0].update(bytes=True),
    'files-27': lambda d: d['files'].pop(),
    'files-object': lambda d: d.update(files={}),
    'directories-extra-parent': lambda d: d['directories'].insert(0, PFX + '/lib'),
    'directories-unsorted': lambda d: d['directories'].reverse(),
    'landmark-other': lambda d: d.update(metadataLandmark=PFX + '/lib/python3.14/json/__init__.py'),
    'profile-name': lambda d: d.update(profile='cpython-3.14.6-macos-preparation-2'),
    'extra-top-level-key': lambda d: d.update(extraGrant='/'),
    'schemaVersion-float-like-bool': lambda d: d.update(schemaVersion=True),
}
report['pythonProfileBaseline'] = outcome(lambda: G.verify_python_profile(copy.deepcopy(profile)))
report['pythonProfileMutations'] = {}
for name, m in py_mut.items():
    d = copy.deepcopy(profile); m(d)
    report['pythonProfileMutations'][name] = outcome(lambda: G.verify_python_profile(d))

conf = json.loads((WORK / 'base/tools/contracts/generator-closure.json').read_text())['confinement']
conf_mut = {
    'timeout-bool': lambda d: d.update(timeoutSeconds=True),
    'timeout-299': lambda d: d.update(timeoutSeconds=299),
    'runtime-reordered': lambda d: d['runtimeFiles'].reverse(),
    'sandbox-path-other': lambda d: d['sandboxExecutable'].update(path='/private/tmp/sandbox-exec'),
    'profile-name': lambda d: d.update(profile='macos-seatbelt-development-2'),
    'extra-key': lambda d: d.update(extra=1),
    'runtime-row-extra-key': lambda d: d['runtimeFiles'][0].update(x=1),
}
report['confinementMutations'] = {}
for name, m in conf_mut.items():
    d = copy.deepcopy(conf); m(d)
    report['confinementMutations'][name] = outcome(lambda: G.verify_confinement(d))

# Closure-level guards through the real CLI (rebound closure/registry).
for name, mutate in {'hostProfile-scope': lambda cl: cl.update(hostProfile={'os': 'darwin', 'scope': 'release'}),
                     'nativeLibraries-nonempty': lambda cl: cl.update(nativeLibraries=[{'path': '/usr/lib/libz.dylib'}]),
                     'python-profile-extra-dir-rebound': None}.items():
    if mutate is None:
        d = copy.deepcopy(profile); d['directories'].append('/private/tmp')
        c = case('E-' + name, files={'tools/contracts/python-profile.json': (json.dumps(d, indent=2) + '\n').encode()})
    else:
        c = case('E-' + name, closure_mutate=mutate)
    before = snapshot(c); r = generate(c, write=True)
    report['closure:' + name] = {**r, 'outputsUnchanged': snapshot(c) == before}

# NR1 P5 through the CLI: option-level superseded subpath entrypoint.
options = json.loads((WORK / 'base/tools/contracts/options.json').read_text())
denied = next(x for x in options['deniedRefs'] if x.endswith('/HelloV3'))
owner = next(o for o in options['owners'] if o['schemaId'] == denied.split('#')[0])
p5 = copy.deepcopy(options)
p5['entryPoints'].append({'ref': denied + '/properties/protocolMajor', 'typeName': owner['namespace'] + 'ReviewerHelloV3ProtocolMajor', 'module': owner['module']})
p5['entryPoints'].sort(key=lambda row: row['ref'])
c = case('E-NR1-P5-options', options=p5); before = snapshot(c)
report['NR1-P5-options-write'] = {**generate(c, write=True), 'outputsUnchanged': snapshot(c) == before}

# NR1 through the confined Python child: a selected native definition gains a $ref into HelloV3.
reg = json.loads((WORK / 'base/schemas/registry.json').read_text())
row = next(r for r in reg['sources'] if r['schemaId'] == owner['schemaId'])
doc = json.loads((WORK / 'base' / row['sourcePath']).read_text())
selected = next(e['ref'] for e in options['entryPoints'] if e['ref'].startswith(owner['schemaId'] + '#/$defs/')
                and isinstance(doc['$defs'].get(e['ref'].split('/')[-1]), dict) and 'properties' in doc['$defs'][e['ref'].split('/')[-1]]
                and e['ref'].count('/') == 2)
doc['$defs'][selected.split('/')[-1]]['properties']['reviewerProbe'] = {'$ref': '#/$defs/HelloV3/properties/protocolMajor'}
c = case('E-NR1-nested-ref', sources={row['sourcePath']: (json.dumps(doc, indent=2) + '\n').encode()}); before = snapshot(c)
report['NR1-nested-ref-write'] = {'selectedDefinitionMutated': selected, **generate(c, write=True), 'outputsUnchanged': snapshot(c) == before}

# Publish preflight 1: hard-linked destination to outside bytes + one modified destination, real binaries.
c = case('E-publish-hardlink'); outside = WORK / 'cases/publish-outside.txt'; outside.write_text('outside bytes must survive\n')
dest = c / 'apps/report/src/generated/report.ts'; dest.unlink(); os.link(outside, dest)
prot = c / 'providers/typescript/src/generated/protocol.ts'; prot.write_bytes(prot.read_bytes() + b'// local edit\n')
w = generate(c, write=True); clean = generate(c)
report['publish-hardlink'] = {'write': w, 'afterDriftCheck': clean, 'outsideUnchanged': outside.read_text() == 'outside bytes must survive\n',
                              'destinationNlink': dest.stat().st_nlink,
                              'outputsEqualSubject': all((c / p).read_bytes() == (SUBJECT / p).read_bytes() for p in outputs(c))}

# Publish preflight 2: generated directory is a symlink to an outside directory; nothing may be written.
c = case('E-publish-dirlink'); outdir = WORK / 'cases/publish-outside-dir'; shutil.rmtree(outdir, ignore_errors=True)
shutil.move(str(c / 'crates/contracts/src/generated'), outdir); (c / 'crates/contracts/src/generated').symlink_to(outdir, target_is_directory=True)
for p in outdir.iterdir(): p.write_bytes(b'outside dir bytes\n')
prot = c / 'providers/typescript/src/generated/protocol.ts'; prot.write_bytes(b'locally modified\n')
w = generate(c, write=True)
report['publish-dirlink'] = {**w, 'outsideDirUnchanged': all(p.read_bytes() == b'outside dir bytes\n' for p in outdir.iterdir()),
                             'otherDestinationNotWritten': prot.read_bytes() == b'locally modified\n'}
print(json.dumps(report, indent=1))
