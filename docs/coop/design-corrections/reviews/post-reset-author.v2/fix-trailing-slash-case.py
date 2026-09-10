"""A-4: the Config2 trailing-slash fixture claimed a Config2 value the foundation resolver refuses (CONFIG_LOGICAL_PATH) reaches
security. Re-labelled as the CLI --workspace-root path, which IS normalized by the shared rule; Config2 values with a trailing
slash never reach either instrument. Idempotent; round-trip json.dumps(indent=2, ensure_ascii=False)."""
import json
from pathlib import Path
P = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/security/discovery-cases.v1.json')
raw = P.read_bytes(); doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw
OLD = 'config2-workspace-root-with-trailing-slash-normalizes-like-the-native-instrument'
NEW = 'cli-workspace-root-with-trailing-slash-normalizes-like-the-native-instrument-config2-refuses-it-earlier'
for c in doc['cases']:
    if c['id'] in (OLD, NEW):
        c['id'] = NEW
        roots = c['input'].pop('configWorkspaceRoots', None) or c['input'].get('explicitJoins')
        c['input']['explicitJoins'] = roots
        c['expect']['provenance.unitSource'] = 'explicit-joins'
        for u in c['expect']['provenance.units']:
            u['kind'] = 'explicit-join'
        c['note'] = ('CLI --workspace-root values are normalized by the shared rule (one trailing `/` dropped). A Config2 discovery.workspaceRoots value '
                     'spelled `packages/web/` is refused by the foundation product-configuration resolver (CONFIG_LOGICAL_PATH) before either instrument sees it '
                     '(post-reset review v2 A-4); this case therefore models the CLI path only.')
        break
else:
    raise SystemExit('case not found')
P.write_bytes((json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode()); print('renamed', NEW)
