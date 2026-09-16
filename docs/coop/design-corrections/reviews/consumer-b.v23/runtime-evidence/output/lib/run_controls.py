import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import controls as C

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
export = sys.argv[1]
label = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(export).split('.')[0]
outdir = OUT + '/runs/controls-' + label
os.makedirs(outdir, exist_ok=True)

tamper = C.run_tamper(export, outdir)
ident = C.run_identity_controls(export, outdir)
doc = {'standing': ('Discriminating negative controls over the exported positive Run. '
                    'TAMPERED-RESULT controls remint every enclosing identity and preserve '
                    'citation membership, so only semantic replay can refuse them. '
                    'IDENTITY/RETENTION controls are refused at retained-closure admission, '
                    'before replay. Neither family is a future-authentication claim.'),
       'positiveExport': export,
       'tamperedResultControls': tamper,
       'identityAndRetentionControls': ident}
p = OUT + '/runs/%s.controls.json' % label
with open(p, 'w') as f:
    json.dump(doc, f, indent=1)

print('=== tampered-result controls (reminted, citation-preserving)')
bad = []
for r in tamper:
    print('%-32s closureAdmitted=%-5s replay=%-28s refused=%s'
          % (r['case'], r['closureAdmitted'], r['replayVerdict'], r['refused']))
    if not r['refused']:
        bad.append(r['case'])
print('=== identity / retention controls')
for r in ident:
    fr = (r['firstRefusal'] or {}).get('check')
    print('%-40s refused=%-5s firstRefusal=%s' % (r['case'], r['refused'], fr))
    if not r['refused']:
        bad.append(r['case'])
print('controls written to', p)
if bad:
    print('CONTROLS THAT FAILED TO REFUSE:', bad)
    sys.exit(1)
print('all %d controls refused as required' % (len(tamper) + len(ident)))
