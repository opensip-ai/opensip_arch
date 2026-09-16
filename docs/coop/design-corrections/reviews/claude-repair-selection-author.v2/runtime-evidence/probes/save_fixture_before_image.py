"""Before-image for the AUTHORIZED bounded fixture-construction extension.

Root authorized a narrow extension to foundation/evaluator_graph_fixture.v3.py if materially
needed for the full-Run asymmetric control, with an exact before-image and a SEPARATE handoff
entry. This file is not one of the eight owned files and is tracked separately.
"""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = 'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py'

src = os.path.join(SRC, REL)
dst = os.path.join(RT, 'before-images', REL)
os.makedirs(os.path.dirname(dst), exist_ok=True)
if os.path.exists(dst):
    print('already saved:', REL)
else:
    shutil.copy2(src, dst)
raw = open(src, 'rb').read()
row = {'path': REL, 'category': 'authorized-bounded-fixture-extension',
       'beforeSha256': hashlib.sha256(raw).hexdigest(), 'beforeBytes': len(raw),
       'beforeImage': 'before-images/' + REL}
json.dump([row], open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'fixture-before-image.json'), 'w'), indent=2)
print(row['beforeBytes'], row['beforeSha256'], REL)
