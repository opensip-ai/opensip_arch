"""v12-A2: reproduce each application reproduction argv from the original executed command record by normalizing the historical absolute source prefix and output bindings."""
import json, hashlib, os
R = '/Users/sb/code/opensip-ai/opensip_arch/'
S = '/private/tmp/opensip-design-corrections/application-stage.v46/files/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v45/'
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
app = json.load(open(S + 'docs/coop/design-corrections/application.v1.json'))
rep = app['acceptedDesignReproduction']
orig_p = R + rep['originalExecutedCommandRecord']['path']
orig = json.load(open(orig_p))
out = {'originalRecordHash': h(orig_p) == rep['originalExecutedCommandRecord']['sha256'], 'commands': []}
ob = {c['name']: c for c in orig['commands']}
for c in rep['commands']:
    o = ob.get(c['name'])
    row = {'name': c['name'], 'sourceHashSnapshot': h(SNAP + c['source']) == c['sourceSha256'], 'inOriginal': o is not None}
    if o:
        row['sourceHashOriginal'] = o.get('sourceSha256') == c['sourceSha256']
        argv = list(o['command'])
        # normalize absolute source path to relative
        prefixes = set()
        for i, a in enumerate(argv):
            if a.endswith('/' + c['source']):
                prefixes.add(a[: -len(c['source'])]); argv[i] = c['source']
        for b in c.get('outputBindings', []):
            argv = [b['reproductionOutput'] if a == b['recordedOutput'] else a for a in argv]
        row['historicalSourcePrefixes'] = sorted(prefixes)
        row['argvReproduced'] = argv == c['argv']
        row['recordedOutputsAbsolute'] = all(b['recordedOutput'].startswith('/') for b in c.get('outputBindings', []))
        row['reproductionOutputsRelative'] = all(not b['reproductionOutput'].startswith('/') and '..' not in b['reproductionOutput'] for b in c.get('outputBindings', []))
    out['commands'].append(row)
outs = [b['reproductionOutput'] for c in rep['commands'] for b in c.get('outputBindings', [])]
out['reproductionOutputsDistinct'] = len(outs) == len(set(outs))
out['count'] = len(rep['commands'])
print(json.dumps(out, indent=1))
