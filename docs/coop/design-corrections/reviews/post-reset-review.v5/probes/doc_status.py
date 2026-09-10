import json,hashlib,os
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
docs=[
 'docs/v2/contracts/product-v1/README.md',
 'docs/v2/contracts/product-v1/identity-and-evidence.md',
 'docs/v2/contracts/product-v1/native-evidence.md',
 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
 'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
 'docs/v2/contracts/product-v1/host-and-configuration.md',
 'docs/coop/design-corrections/D-372-corrections.proposed.md',
 'docs/coop/design-corrections/current-source-map.proposed.md',
 'docs/coop/design-corrections/inherited-residuals.proposed.md',
 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json',
 'docs/coop/design-corrections/qualification-gates.proposed.json',
 'docs/coop/design-corrections/correction-crosswalk.proposed.json',
 'docs/coop/design-corrections/inherited-row-sources.proposed.json',
 'docs/coop/design-corrections/post-reset-dispositions.v5.proposed.json',
 'docs/coop/design-corrections/historical-preservation-report.v5.json',
 'docs/coop/design-corrections/validation-summary.v1.json',
 'docs/coop/design-corrections/README.md',
]
for d in docs:
    a=os.path.join(SUB,d); b=os.path.join(V4,d)
    if not os.path.exists(a): print('ABSENT     ',d); continue
    if not os.path.exists(b): print('NEW-IN-V5  ',d,os.path.getsize(a)); continue
    print(('UNCHANGED  ' if sha(a)==sha(b) else 'CHANGED    ')+d,os.path.getsize(a))
print()
import glob
print('product-v1 dir:',sorted(os.path.basename(x) for x in glob.glob(SUB+'/docs/v2/contracts/product-v1/*')))
