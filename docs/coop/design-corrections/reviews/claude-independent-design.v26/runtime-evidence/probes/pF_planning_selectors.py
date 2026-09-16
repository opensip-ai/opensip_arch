"""PROBE F — selector integrity across the planning companions.
The design's own discipline (current-source-map row on security-completion.v8) is that
"review selectors use exact paths/heading text/content hashes, never ambiguous section
number alone". I test whether the successor companions obey it in their own bytes:
duplicate anchor ids, dangling anchor citations, and duplicate JSON keys."""
import json, os, re, collections

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
R = {}


def strict(path):
    """Parse rejecting duplicate JSON keys, as the kit's own canonical.parse does."""
    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                raise ValueError('DUPLICATE KEY: ' + k)
            seen.add(k)
        return dict(pairs)
    return json.load(open(path, encoding='utf-8'), object_pairs_hook=hook)


DOCS = {
    'report-asset-binding.v1.json': 'docs/v2/architecture/report-asset-binding.v1.json',
    'store-instance-lineage.v1.json': 'docs/v2/architecture/store-instance-lineage.v1.json',
    'commit-recovery-plan.v1.json': 'docs/v2/architecture/commit-recovery-plan.v1.json',
    'attempt-custody.schema.v1.json': 'docs/v2/architecture/attempt-custody.schema.v1.json',
    'carrier-dispatch.v3.json': 'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'carrier-highwater.schema.v1.json': 'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
}
for name, rel in DOCS.items():
    p = os.path.join(ROOT, rel)
    try:
        d = strict(p)
        R.setdefault('strictJsonAdmission', {})[name] = 'ADMIT'
    except ValueError as e:
        R.setdefault('strictJsonAdmission', {})[name] = 'REFUSE: ' + str(e)
        continue
    anchors = d.get('frozenSourceAnchors')
    if isinstance(anchors, list):
        ids = [a.get('id') for a in anchors]
        dup = [k for k, v in collections.Counter(ids).items() if v > 1]
        R.setdefault('anchorIds', {})[name] = {'count': len(ids), 'duplicates': dup}
        if dup:
            R.setdefault('duplicateAnchorDetail', {})[name] = [
                {'id': a['id'], 'path': a.get('path'), 'selector': str(a.get('selector'))[:70]}
                for a in anchors if a['id'] in dup]
        text = json.dumps(d)
        cited = sorted(set(re.findall(r'\b([A-Z]\d{1,2}[a-z]?)\b', text)))
        declared = set(ids)
        R.setdefault('citedButUndeclared', {})[name] = sorted(
            c for c in cited if re.fullmatch(r'[AB]\d{1,2}[a-z]?', c) and c not in declared)
        # which duplicated ids are actually cited by id somewhere
        R.setdefault('duplicateIdsCitedByIdElsewhere', {})[name] = sorted(
            k for k in dup if len(re.findall(r'"[^"]*\b%s\b[^"]*"' % re.escape(k), text)) > len(
                [a for a in anchors if a['id'] == k]))

print(json.dumps(R, indent=1))
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeF.json', 'w'), indent=1)
