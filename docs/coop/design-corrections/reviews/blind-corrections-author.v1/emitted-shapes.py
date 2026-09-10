"""Disposable: produce the representative public terminations for the eleven pending codes, first against
the CURRENT shared registry/enum (which must refuse them) and then against a /tmp copy patched with the
eleven records (which must admit them). The repository registry and enum are never modified."""
import copy, importlib.util, json, shutil, sys
from pathlib import Path

SRC = Path(sys.argv[1]); WORK = Path(sys.argv[2])
if WORK.exists():
    shutil.rmtree(WORK)
shutil.copytree(SRC / 'docs', WORK / 'docs')

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

S = load('sec', SRC / 'docs/coop/design-corrections/security/security_lifecycle_model_v1.py')
PENDING = sorted(S.PENDING_PUBLIC_DETAIL_REGISTRATIONS)

REMEDY = {
 'ENVELOPE.SHAPE': 'Present an opensip-signature-envelope.2 with exactly envelopeSchema, kind, body and bodyDigest.',
 'ENVELOPE.KIND': 'Present the envelope kind this operation admits.',
 'ENVELOPE.BODY_DIGEST': 'Recompute bodyDigest as the metadata-profile digest of the canonical body under its domain.',
 'PROFILE_SET.SCHEMA_SHAPE': 'Present a PlatformProfileSetV1 body that satisfies the closed envelope schema.',
 'PROFILE_SET.SCHEMA': 'Set profileSetSchema to the exact integer 1.',
 'PROFILE_SET.CANON': 'Re-encode the profile-set body under opensip-metadata-canonical.1.',
 'PROFILE_SET.CORE_PIN_MISMATCH': 'Import the profile set pinned by the current admitted core release, or update the core release.',
 'PROFILE_SET.NO_TR_PROFILE_ROLE': 'Under a schema-1 root only the copy embedded in the signed core release is used; adopt a schema-2 root with an active TR-PROFILE first.',
 'PROFILE_SET.SIGNATURE_THRESHOLD': 'Present signatures reaching the accepted root TR-PROFILE threshold, excluding revoked keys.',
 'ROOT.TR_REPAIR_THRESHOLD_POLICY': 'An active TR-REPAIR needs threshold >= 2, keys >= threshold + 1 and non-empty namespaces.',
 'ROOT.TR_PROFILE_THRESHOLD_POLICY': 'An active TR-PROFILE needs threshold >= 2, keys >= threshold + 1 and non-empty namespaces.',
}
SUBJECT = {'PROFILE_SET.NO_TR_PROFILE_ROLE': 'core-release-embedded-copy-only',
           'PROFILE_SET.CANON': 'NON_NFC_KEY',
           'ROOT.TR_REPAIR_THRESHOLD_POLICY': 'TR-REPAIR',
           'ROOT.TR_PROFILE_THRESHOLD_POLICY': 'TR-PROFILE'}
# the D9 branch each code travels under, from the security model's own projection
BRANCH = {}
for code in PENDING:
    refusal = 'ROOT.SCHEMA_UNSUPPORTED' if code == 'PROFILE_SET.NO_TR_PROFILE_ROLE' else 'PAYLOAD-NOT-ADMISSIBLE'
    BRANCH[code] = S.public_detail(refusal, code + (':' + SUBJECT[code] if code in SUBJECT else ''))

def run(root, label):
    H = load('host_' + label, root / 'docs/coop/design-corrections/integration-host-model.py')
    shapes, refused = {}, {}
    for code in PENDING:
        item = BRANCH[code]
        try:
            shapes[code] = H.public_termination(item['d9'], code, REMEDY[code], SUBJECT.get(code))
        except Exception as e:
            refused[code] = '%s: %s' % (type(e).__name__, e)
    return shapes, refused

before_shapes, before_refused = run(SRC, 'before')

reg_path = WORK / 'docs/coop/design-corrections/public-detail-registry.v1.json'
reg = json.loads(reg_path.read_text())
for code in PENDING:
    reg['records'].append({'code': code, 'owner': 'security',
                           'selector': 'security/security_lifecycle_model_v1.py (D9 and typed refusal declarations)'})
reg['records'].sort(key=lambda r: r['code'])
reg['internalAliases'].append({'internalCode': 'RF-6:AUTHORIZATION.GRANT_NOT_CURRENT',
                               'publicCode': 'TRUST.COMPONENT_REVOKED_DURING_OPERATION'})
reg['internalAliases'].sort(key=lambda r: r['internalCode'])
reg_path.write_text(json.dumps(reg, indent=1) + '\n')

common_path = WORK / 'docs/coop/design-corrections/workflows/schemas/common.schema.json'
common = json.loads(common_path.read_text())
common['$defs']['DomainDetailCode']['enum'] = sorted(set(common['$defs']['DomainDetailCode']['enum']) | set(PENDING))
common_path.write_text(json.dumps(common, indent=1) + '\n')

after_shapes, after_refused = run(WORK, 'after')

out = {'pendingCodes': PENDING,
       'registryBefore': len(json.loads((SRC / 'docs/coop/design-corrections/public-detail-registry.v1.json').read_text())['records']),
       'registryAfter': len(reg['records']),
       'enumBefore': len(json.loads((SRC / 'docs/coop/design-corrections/workflows/schemas/common.schema.json').read_text())['$defs']['DomainDetailCode']['enum']),
       'enumAfter': len(common['$defs']['DomainDetailCode']['enum']),
       'currentBytesRefuseEveryPendingCode': sorted(before_refused) == PENDING and not before_shapes,
       'currentRefusals': before_refused,
       'afterRegistrationAllAdmit': sorted(after_shapes) == PENDING and not after_refused,
       'afterRefusals': after_refused,
       'representativeTerminations': after_shapes,
       'aliasAdded': {'internalCode': 'RF-6:AUTHORIZATION.GRANT_NOT_CURRENT',
                      'publicCode': 'TRUST.COMPONENT_REVOKED_DURING_OPERATION'}}
print(json.dumps(out, indent=1))
