"""Final sweep for hidden recipe/identity collisions and excluded semantic
inputs: every x-opensip-digest annotation must resolve to a record/registry that
exists; every Ref domain enum member must be registered; and every H domain in
the contract's domain table must have a schema whose required fields carry the
semantic inputs that table row names."""
import json, re, sys, hashlib, importlib.util
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/candidate-subject.v7')
DC = ROOT / 'docs/coop/design-corrections'
IDS = json.loads((DC / 'foundation/identity-schemas.v2.json').read_text())
REG = IDS['x-opensip-digest-domains']
DEFS = IDS['$defs']
R = {}

# ---- 1. every annotation resolves
sites = []
def walk(n, p):
    if isinstance(n, dict):
        if 'x-opensip-digest' in n: sites.append((p, n['x-opensip-digest']))
        for k, v in n.items(): walk(v, p + '/' + k)
    elif isinstance(n, list):
        for i, v in enumerate(n): walk(v, p + '/' + str(i))
walk(IDS, '')
unresolved = []
for p, a in sites:
    rep = a.get('representation')
    if rep == 'canonical-record':
        rec = a.get('record')
        if not isinstance(rec, dict): unresolved.append((p, 'no record')); continue
        if rec.get('bundle') == 'identity':
            sel = rec.get('selector', '')
            name = sel.replace('#/$defs/', '')
            if name not in DEFS: unresolved.append((p, 'identity selector missing: ' + sel))
        elif 'document' in rec:
            doc = DC / rec['document']
            if not doc.is_file(): unresolved.append((p, 'document missing: ' + rec['document']))
            else:
                j = json.loads(doc.read_text())
                sel = rec.get('selector')
                if sel:
                    node = j
                    for part in [x for x in sel.replace('#', '').split('/') if x]:
                        node = node.get(part) if isinstance(node, dict) else None
                        if node is None: break
                    if node is None: unresolved.append((p, 'selector missing in doc: ' + sel))
        elif 'registeredBy' in rec or 'ownerRegistry' in rec or 'ownerRegistered' in rec:
            pass
        else:
            unresolved.append((p, 'unrecognised record form: ' + json.dumps(rec)[:120]))
    elif rep == 'h-identity':
        ds = a.get('domainSet')
        if ds not in REG['domainSets']: unresolved.append((p, 'domainSet missing: ' + str(ds)))
    elif rep == 'by-domain':
        if a.get('registry') != 'x-opensip-digest-domains.byDomain':
            unresolved.append((p, 'unexpected registry: ' + str(a.get('registry'))))
    elif rep in ('raw-artifact', 'capability-manifest-id'):
        if rep == 'raw-artifact' and not a.get('artifact'):
            unresolved.append((p, 'raw-artifact without artifact description'))
    else:
        unresolved.append((p, 'unregistered representation: ' + str(rep)))
R['annotationSites'] = len(sites)
R['unresolvedAnnotations'] = unresolved

# ---- 2. Ref domain enums fully registered, and payload domains excluded from proof inputs
for name in ('Ref', 'ProofInputRef', 'FindingEvidenceRef'):
    enum = DEFS[name]['properties']['domain']['enum']
    R[name + 'DomainCount'] = len(enum)
    R[name + 'UnregisteredDomains'] = [d for d in enum if d not in REG['byDomain']]
R['payloadDomainsInRef'] = [d for d in DEFS['Ref']['properties']['domain']['enum']
                            if d.endswith('-payload')]
R['payloadDomainsInProofInputRef'] = [d for d in DEFS['ProofInputRef']['properties']['domain']['enum']
                                      if d.endswith('-payload')]
R['proofInputVocabularyExcludesPayloadDomains'] = not R['payloadDomainsInProofInputRef']
for name in ('ProofInputRef', 'FindingEvidenceRef'):
    R[name + 'ExcludesRunEvidenceSealProof'] = not (
        {'run', 'semantic-evidence', 'evaluation-seal', 'proof-bundle'}
        & set(DEFS[name]['properties']['domain']['enum']))

# ---- 3. each contract domain-table row's named inputs appear in the schema's required fields
md = (ROOT / 'docs/v2/contracts/product-v1/identity-and-evidence.md').read_text()
table = {}
for line in md.splitlines():
    m = re.match(r'^\|\s*([a-z\-]+)\s*/\s*([a-z0-9\-]+)\s*\|\s*(.+?)\s*\|$', line)
    if m: table[m.group(1)] = m.group(3)
R['domainTableRows'] = len(table)
KEYWORDS = {
    'snapshot': ['projectId', 'sourceInventory', 'resolvedConfigDigest', 'scopeDigest', 'vcsDigest'],
    'closure': ['kind', 'manifestDigest', 'tree', 'semanticVersion', 'protocolMajor', 'platform'],
    'plan': ['snapshotId', 'capabilityManifestId', 'semanticClosures', 'analysisSpecDigest',
             'resolvedConfigDigest', 'nativeContextDigests', 'importIds', 'policyDigest',
             'waiverDigest', 'scopeDigest', 'budget', 'semanticGrantDigest'],
    'subject-scope': ['snapshotId', 'relation', 'sourceUniverse', 'targetUniverse',
                      'enumeratorClosure', 'subjects'],
    'fact': ['snapshotId', 'relation', 'sourceUniverse', 'targetUniverse', 'producerClosure',
             'payloadDigest', 'payloadSchemaDigest', 'anchors', 'confidenceMillionths'],
    'coverage': ['scopeId', 'payloadDigest', 'payloadSchemaDigest'],
    'view': ['planId', 'scopeIds', 'facts', 'coverageIds', 'producerClosure', 'schemaDigests'],
    'execution-plan': ['planId', 'stages'],
    'finding': ['fingerprint', 'ruleClosure', 'subjectId', 'messageCode', 'parameterDigest',
                'severity', 'evidenceRefs'],
    'proof-bundle': ['planId', 'executionPlanId', 'evaluatorClosure', 'ruleProgramDigest',
                     'evaluationInputRefs', 'predicateProofs', 'findingIds', 'verdict'],
    'semantic-evidence': ['planId', 'viewIds', 'coverageIds', 'importIds', 'findingIds',
                          'proofBundleId'],
    'evaluation-seal': ['planId', 'executionPlanId', 'evidenceId', 'evaluatorClosure',
                        'policyDigest', 'proofBundleId', 'verdict'],
    'run': ['projectId', 'snapshotId', 'planId', 'evidenceId', 'evaluationSealId',
            'capabilityManifestId'],
    'cache-key': ['planId', 'producerClosure', 'stageSpecDigest', 'scopeIds', 'inputRefs',
                  'outputSchemaDigest'],
    'policy-derivation': ['planId', 'proofBundleId', 'policyDigest', 'waiverDigest', 'verdict'],
}
missing = {}
for dom, fields in KEYWORDS.items():
    req = set(DEFS[dom].get('required', []))
    gap = [f for f in fields if f not in req]
    if gap: missing[dom] = gap
R['domainsCheckedAgainstContractRow'] = len(KEYWORDS)
R['domainsMissingANamedSemanticInput'] = missing
R['everyNamedInputIsARequiredField'] = not missing

# ---- 4. acyclicity: proof must not reach Run/evidence/seal
R['proofDoesNotCarryEvidenceOrRunId'] = not (
    {'evidenceId', 'runId', 'evaluationSealId'} & set(DEFS['proof-bundle']['properties']))
R['evidenceMayCarryProof'] = 'proofBundleId' in DEFS['semantic-evidence']['properties']
R['sealCarriesBoth'] = ({'evidenceId', 'proofBundleId'}
                        <= set(DEFS['evaluation-seal']['properties']))
R['runCarriesSeal'] = 'evaluationSealId' in DEFS['run']['properties']

# ---- 5. recipe collision: no two DISTINCT representations share one field spelling
byname = {}
for p, a in sites:
    leaf = p.rsplit('/', 1)[-1]
    byname.setdefault(leaf, set()).add(json.dumps(a, sort_keys=True))
R['fieldNamesWithMoreThanOneRecipe'] = {k: sorted(v) for k, v in byname.items() if len(v) > 1}
R['noFieldSpellingHasTwoRecipes'] = not R['fieldNamesWithMoreThanOneRecipe']

# ---- 6. every registered nested/native domain's selector exists in the native document
nat = json.loads((DC / 'native/native-evidence.schemas.v2.json').read_text())
bad = []
for setname, doms in REG['domainSets'].items():
    for dom, row in doms.items():
        doc = json.loads((DC / row['document']).read_text())
        node = doc
        for part in [x for x in row['selector'].replace('#', '').split('/') if x]:
            node = node.get(part) if isinstance(node, dict) else None
            if node is None: break
        if node is None: bad.append((setname, dom, row['selector']))
R['domainSetSelectorsUnresolved'] = bad
R['domainSetDomainCount'] = sum(len(v) for v in REG['domainSets'].values())

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
