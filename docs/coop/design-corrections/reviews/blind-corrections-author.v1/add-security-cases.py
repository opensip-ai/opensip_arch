"""Author edit: S-2 strict end-anchor regressions through the actual host gate, and the M-5
public-detail projection corpus."""
import copy, json, sys
from pathlib import Path
R = Path(sys.argv[1]); S = R / 'docs/coop/design-corrections/security'

# ---- S-2: root admission boundary --------------------------------------------------------------
p = S / 'root-schema-cases.v1.json'
doc = json.loads(p.read_text())
r1 = doc['roots']['root1']
url_nl = copy.deepcopy(r1); url_nl['indexOrigin']['url'] = url_nl['indexOrigin']['url'] + '\n'
ns_nl = copy.deepcopy(r1); ns_nl['roles']['TR-CORE']['namespaces'] = [ns_nl['roles']['TR-CORE']['namespaces'][0] + '\n']
doc['roots']['root1TrailingNewlineUrl'] = url_nl
doc['roots']['root1TrailingNewlineNamespace'] = ns_nl
existing = {c['id'] for c in doc['rootCases']}
new = [
 {"id": "schema-1-root-with-a-trailing-newline-index-origin-url-refuses-at-the-product-boundary",
  "note": "S-2. The product admission boundary is RootV1 in this bundle, whose patterns end with the strict (?![\\s\\S]) assertion. The historical security-schemas.v8/root.schema.json is the preserved RULE SOURCE for schema 1; its bare `$` would admit these bytes, and it is not a second admission gate. Nothing in the historical file changes.",
  "input": {"root": "$root1TrailingNewlineUrl", "readerSchemas": [1, 2]},
  "expect": {"result": "REFUSE", "refusal": "PAYLOAD-NOT-ADMISSIBLE", "detail": "ROOT.SCHEMA_SHAPE",
             "d9": {"class": "request-rejected", "exit": 2, "code": "EXTENSION.ADMISSION_REJECTED"}},
  "inputSchemas": {"root": "RootV1"}, "inputValid": False},
 {"id": "schema-1-root-with-a-trailing-newline-role-namespace-refuses-at-the-product-boundary",
  "note": "S-2, second selector: the same strict end anchor governs role `namespaces` items.",
  "input": {"root": "$root1TrailingNewlineNamespace", "readerSchemas": [1, 2]},
  "expect": {"result": "REFUSE", "refusal": "PAYLOAD-NOT-ADMISSIBLE", "detail": "ROOT.SCHEMA_SHAPE",
             "d9": {"class": "request-rejected", "exit": 2, "code": "EXTENSION.ADMISSION_REJECTED"}},
  "inputSchemas": {"root": "RootV1"}, "inputValid": False},
]
for c in new:
    if c['id'] in existing:
        raise SystemExit('duplicate ' + c['id'])
doc['rootCases'].extend(new)
doc['standing'] = doc['standing'] + (
 ' The product admission boundary for both schemas is this bundle (`RootV1`/`RootV2` with strict'
 ' end-anchored patterns), reached only through admit_root_document; the retained v8 root.schema.json'
 ' is the historical rule source, never a second gate.')
p.write_text(json.dumps(doc, indent=1) + '\n')
print('rootCases now', len(doc['rootCases']))

# ---- M-5: public detail projection --------------------------------------------------------------
envelope = doc['envelope']
pd = {
 "standing": "S12 projection of ACTUAL model outcomes onto the ONE closed public DomainDetail vocabulary "
             "(blind consumer M-5). Every case runs an inner model and projects what it really emitted; no "
             "outcome is hand-written. `pendingRegistrationCodes` names members the shared "
             "public-detail-registry.v1.json does not yet carry; that registry and the typed workflow enum "
             "are owned elsewhere and are not edited by this unit.",
 "model": "public-detail",
 "roots": {"root1": r1, "root2": doc['roots']['root2']},
 "envelope": envelope,
 "cases": [
  {"id": "standalone-profile-set-under-a-schema-1-root-emits-PROFILE_SET.NO_TR_PROFILE_ROLE",
   "note": "S9.1 mandates this refusal by name. The public code is the DETAIL base, the sub-detail is subject "
           "data, and the D9 branch comes from the REFUSAL (ROOT.SCHEMA_UNSUPPORTED), not from the detail.",
   "input": {"source": {"model": "profile-set-envelope",
                        "input": {"envelope": "$envelope", "acceptedRoot": "$root1",
                                  "signers": ["fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1",
                                              "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff2"],
                                  "selected_profile_digest": "df98424c474c505144d59dae09b185507bde849525cfc6396985f50edc7af9b9"}}},
   "expect": {"codes": ["PROFILE_SET.NO_TR_PROFILE_ROLE"],
              "pendingRegistrationCodes": ["PROFILE_SET.NO_TR_PROFILE_ROLE"],
              "items.0.code": "PROFILE_SET.NO_TR_PROFILE_ROLE",
              "items.0.subject": "core-release-embedded-copy-only",
              "items.0.d9": {"class": "request-rejected", "exit": 2, "code": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED"}}},
  {"id": "profile-set-not-pinned-by-the-current-core-emits-PROFILE_SET.CORE_PIN_MISMATCH",
   "input": {"source": {"model": "profile-set-envelope",
                        "input": {"envelope": "$envelope", "acceptedRoot": "$root2",
                                  "signers": ["fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1",
                                              "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff2"],
                                  "selected_profile_digest": None}}},
   "expect": {"codes": ["PROFILE_SET.CORE_PIN_MISMATCH"],
              "pendingRegistrationCodes": ["PROFILE_SET.CORE_PIN_MISMATCH"],
              "items.0.subject": None,
              "items.0.d9": {"class": "request-rejected", "exit": 2, "code": "EXTENSION.ADMISSION_REJECTED"}}},
  {"id": "malformed-signature-envelope-emits-ENVELOPE.SHAPE",
   "input": {"source": {"model": "profile-set-envelope",
                        "input": {"envelope": {"envelopeSchema": 2, "kind": "platform-profile-set",
                                               "body": {"profileSetSchema": 1}},
                                  "acceptedRoot": "$root2", "signers": [], "selected_profile_digest": None}}},
   "expect": {"codes": ["ENVELOPE.SHAPE"], "pendingRegistrationCodes": ["ENVELOPE.SHAPE"],
              "items.0.d9": {"class": "request-rejected", "exit": 2, "code": "EXTENSION.ADMISSION_REJECTED"}}},
  {"id": "root-document-defect-emits-the-specific-ROOT-code-not-the-generic-refusal",
   "note": "Why the ENVELOPE.* / PROFILE_SET.* families must be registered: they occupy exactly the "
           "position the 38 registered ROOT.* codes occupy, for exactly the same reason.",
   "input": {"source": {"model": "root-document",
                        "input": {"root": "$root1TrailingNewlineUrl", "readerSchemas": [1, 2]}}},
   "expect": {"codes": ["ROOT.SCHEMA_SHAPE"], "pendingRegistrationCodes": [],
              "items.0.subject": None,
              "items.0.d9": {"class": "request-rejected", "exit": 2, "code": "EXTENSION.ADMISSION_REJECTED"}}},
  {"id": "unsupported-reader-set-carries-free-prose-as-subject-under-the-registered-refusal",
   "note": "Rule 3: a detail that is not a registered base code travels whole as subject data. This is the "
           "existing reading for RECOVERY.REFUSED, CONFIG.CUSTODY_REFUSED and PROJECT.EXPLICIT_PATH_INVALID "
           "sub-details, and it is why those sub-details are deliberately not registry members.",
   "input": {"source": {"model": "root-document", "input": {"root": "$root2", "readerSchemas": [1]}}},
   "expect": {"codes": ["ROOT.SCHEMA_UNSUPPORTED"], "pendingRegistrationCodes": [],
              "items.0.subject": "rootSchema 2 not in reader set [1]",
              "items.0.d9": {"class": "request-rejected", "exit": 2, "code": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED"}}},
  {"id": "backup-custody-refusal-projects-the-registered-lowercase-detail-with-its-own-branch",
   "input": {"source": {"model": "storage-write",
                        "input": {"backupStatus": "BACKED_UP", "ci": True}}},
   "expect": {"codes": ["storage.backup-choice-required"], "pendingRegistrationCodes": [],
              "items.0.d9": {"class": "request-rejected", "exit": 2, "code": "REQUEST.PRECONDITION_FAILED"}}},
 ]}
q = S / 'public-detail-cases.v1.json'
if q.exists():
    raise SystemExit('public-detail-cases.v1.json already exists')
q.write_text(json.dumps(pd, indent=1) + '\n')
print('wrote', q.name, len(pd['cases']), 'cases')
