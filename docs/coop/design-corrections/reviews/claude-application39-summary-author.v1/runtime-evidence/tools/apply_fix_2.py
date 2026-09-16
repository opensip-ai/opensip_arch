"""Fix 2 after failed controls attempt 1 (receipts/boundary-controls.attempt1-failed.json, sha 08aa5933...).

Diagnosis: the corrected helper refused on the actual frozen39 receipts at
    assert workflow['failed'] == [] and integration['failed'] == [] and integration['checks'] == integration['passed']
because integration.json 'checks' is the list of the 412 executed checks, not a count. The guard is corrected to
compare its length. One exact-once replacement in the captured helper; receipt appended to receipts/edits.jsonl.
"""
import hashlib, json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-application39-summary-author.v1')
path = RT / 'work/application-successor-root.v2/current_reference_summary.py'
old = "assert workflow['failed'] == [] and integration['failed'] == [] and integration['checks'] == integration['passed']"
new = "assert workflow['failed'] == [] and integration['failed'] == [] and len(integration['checks']) == integration['passed']"
raw = path.read_bytes()
text = raw.decode()
assert text.count(old) == 1
text = text.replace(old, new)
compile(text, path.name, 'exec')
path.write_bytes(text.encode())
row = {'path': path.name, 'replacements': 1, 'beforeSha256': hashlib.sha256(raw).hexdigest(),
       'afterSha256': hashlib.sha256(text.encode()).hexdigest(), 'dry': False, 'label': 'fix2 integration checks is a list'}
with open(RT / 'receipts/edits.jsonl', 'a') as f:
    f.write(json.dumps(row) + '\n')
print(json.dumps(row, indent=1))
