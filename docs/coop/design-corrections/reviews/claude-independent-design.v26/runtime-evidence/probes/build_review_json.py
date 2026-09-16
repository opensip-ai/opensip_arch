"""Emit review.json with MEASURED hashes for every completely-read document."""
import hashlib, json, os

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v26/review.json'

READ = [
    # five consolidated contracts + README
    ('docs/v2/contracts/product-v1/README.md', 'contract-index'),
    ('docs/v2/contracts/product-v1/identity-and-evidence.md', 'consolidated-contract'),
    ('docs/v2/contracts/product-v1/security-and-lifecycle.md', 'consolidated-contract'),
    ('docs/v2/contracts/product-v1/native-evidence.md', 'consolidated-contract'),
    ('docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'consolidated-contract'),
    ('docs/v2/contracts/product-v1/admission-and-qualification.md', 'consolidated-contract'),
    # incorporated evaluator3 contracts
    ('docs/coop/design-corrections/foundation/enumeration-contract.v1.md', 'incorporated-evaluator3'),
    ('docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md', 'incorporated-evaluator3'),
    ('docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md', 'incorporated-evaluator3'),
    ('docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md', 'incorporated-evaluator3'),
    ('docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md', 'incorporated-evaluator3'),
    # incorporated projections
    ('docs/coop/design-corrections/workflows/query-projection-contract.v3.md', 'incorporated-projection'),
    ('docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md', 'incorporated-projection'),
    # selected provider-return / attribution schemas
    ('docs/coop/design-corrections/foundation/target-attribution.schema.v2.json', 'selected-schema'),
    ('docs/coop/design-corrections/native/fact-batch.schema.v3.json', 'selected-schema'),
    ('docs/coop/design-corrections/native/occupancy-companion.schema.v1.json', 'selected-schema'),
    ('docs/coop/design-corrections/native/dispatch-binding.schema.v1.json', 'selected-schema'),
    # hydradb dispositions
    ('docs/coop/design-corrections/hydradb-dispositions.proposed.md', 'disposition-map'),
    # planning layer
    ('docs/v2/architecture/14-repository-and-module-layout.md', 'planning'),
    ('docs/v2/architecture/implementation-boundaries-and-build-plan.md', 'planning'),
    ('docs/v2/architecture/prototype-report-inventory.md', 'planning'),
    ('docs/v2/architecture/implementation-normative-inputs.v1.json', 'planning'),
    ('docs/v2/architecture/implementation-planning-sources.v1.json', 'planning'),
    # incorporated companions
    ('docs/v2/architecture/store-instance-lineage.v1.json', 'companion'),
    ('docs/v2/architecture/report-asset-binding.v1.json', 'companion'),
    ('docs/v2/architecture/attempt-custody.schema.v1.json', 'companion'),
    ('docs/v2/architecture/commit-recovery-readonly.v3.md', 'companion'),
    ('docs/coop/design-corrections/security/carrier-format.v3.md', 'companion'),
    ('docs/coop/design-corrections/security/carrier-dispatch.v3.json', 'companion'),
    ('docs/coop/design-corrections/security/carrier-migration.v1.md', 'companion'),
    ('docs/coop/design-corrections/security/carrier-highwater.schema.v1.json', 'companion'),
    ('docs/coop/design-corrections/security/grant-journal.carrier.v3.sql', 'companion'),
    # disposition source maps
    ('docs/coop/design-corrections/correction-crosswalk.proposed.json', 'disposition-map'),
    ('docs/coop/design-corrections/inherited-residuals.proposed.md', 'disposition-map'),
    ('docs/coop/design-corrections/current-source-map.proposed.md', 'disposition-map'),
    ('docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'disposition-map'),
    ('docs/coop/design-corrections/qualification-gates.proposed.json', 'disposition-map'),
]
TRAVERSED = [
    ('docs/v2/architecture/repository-file-inventory.v1.json', 'planning-data'),
    ('docs/v2/architecture/implementation-coverage.v1.json', 'planning-data'),
    ('docs/v2/architecture/commit-recovery-plan.v1.json', 'planning-data'),
    ('docs/coop/design-corrections/foundation/identity-schemas.v3.json', 'schema-data'),
    ('docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json', 'schema-data'),
    ('docs/coop/design-corrections/native/capability-manifest-domains.v2.json', 'schema-data'),
    ('docs/coop/design-corrections/workflows/command-inventory.v3.json', 'schema-data'),
]


def rows(items, mode):
    out = []
    for rel, kind in items:
        p = os.path.join(ROOT, rel)
        b = open(p, 'rb').read()
        t = b.decode('utf-8', 'replace')
        out.append({'path': rel, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b),
                    'lines': t.count('\n') + (0 if t.endswith('\n') else 1),
                    'kind': kind, 'coverage': mode})
    return out


BASE = os.path.dirname(OUT)
doc = json.load(open(os.path.join(BASE, 'review.body.json'), encoding='utf-8'))
disp = json.load(open(os.path.join(BASE, 'dispositions.json'), encoding='utf-8'))
doc['dispositionVocabulary'] = disp['dispositionVocabulary']
doc['dispositionStandingForEveryRow'] = disp['standingForEveryRow']
doc['arDispositions'] = disp['arDispositions']
doc['fwDispositions'] = disp['fwDispositions']
doc['inheritedResidualDispositions'] = dict(disp['inheritedResidualDispositions'])
doc['inheritedResidualDispositions'].update(disp['dr011ResidualDispositions'])
doc['scopedReviewOwnerDispositions'] = disp['scopedReviewOwnerDispositions']
doc['dispositionCounts'] = {
    'arDispositions': len(doc['arDispositions']),
    'fwDispositions': len(doc['fwDispositions']),
    'inheritedResidualDispositions': len(doc['inheritedResidualDispositions']),
    'scopedReviewOwnerDispositions': len(doc['scopedReviewOwnerDispositions']),
}
doc['contractsReadCompletely'] = rows(READ, 'read-completely-every-line')
doc['machineDataTraversedCompletely'] = rows(TRAVERSED, 'traversed-programmatically-every-record')
doc['readCompletelyCount'] = len(doc['contractsReadCompletely'])
doc['readCompletelyLines'] = sum(r['lines'] for r in doc['contractsReadCompletely'])
json.dump(doc, open(OUT, 'w'), indent=1)
print('wrote', OUT, 'readCompletely=%d docs / %d lines' %
      (doc['readCompletelyCount'], doc['readCompletelyLines']))
