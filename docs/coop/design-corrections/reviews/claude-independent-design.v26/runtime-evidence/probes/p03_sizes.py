import os, hashlib, json
ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
FILES = [
    'docs/v2/architecture/14-repository-and-module-layout.md',
    'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
    'docs/v2/architecture/commit-recovery-readonly.v3.md',
    'docs/v2/architecture/repository-file-inventory.v1.json',
    'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/v2/architecture/implementation-planning-sources.v1.json',
    'docs/v2/architecture/store-instance-lineage.v1.json',
    'docs/v2/architecture/report-asset-binding.v1.json',
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/v2/architecture/commit-recovery-plan.v1.json',
    'docs/coop/design-corrections/security/carrier-format.v3.md',
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'docs/coop/design-corrections/security/carrier-migration.v1.md',
    'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
    'docs/coop/design-corrections/hydradb-dispositions.proposed.md',
]
for f in FILES:
    p = os.path.join(ROOT, f)
    b = open(p, 'rb').read()
    t = b.decode('utf-8', 'replace')
    print('%-70s bytes=%-8d lines=%-6d %s' % (os.path.basename(f), len(b), t.count('\n') + 1, hashlib.sha256(b).hexdigest()[:16]))
