"""Reference model for PlatformProfileSetV2 (law 458b) over the pinned V1 security-lifecycle model.

Design evidence only. Pure functions over JSON-shaped inputs; SYNTHETIC fixtures; no OS reads, no
cryptography (signatures are checked in check_cases.py with the public test-only seeds), no
qualification of any boot identity and no Evidence B minted.

What this adds, and nothing else (458b decisions 1-5):
  admit_profile_set_v1_shape(body)   the unchanged V1 shape (pinned bundle PlatformProfileSetV1 + metadata canon)
  admit_profile_set_v2_shape(body)   the V2 shape: ../schema/platform-profile-set-v2.schema.json, validated the
                                     same way V1 validates (foundation exact validator, then metadata canon)
  admit_profile_set_shape(body, reader)
                                     reader 'v1-only' (every existing caller) or 'v1-or-v2' (the opt-in reader)
  profile_set_digest(body)           metadata digest under the UNCHANGED domain opensip.metadata.platform-profile-set.1
  platform_admit_v2(profile_set, observed)
                                     V2 shape, then the V1 decision unchanged, plus the matched measured row index
  matched_install_acl_omission(profile_set, observed)
                                     'no-acl-stored' only for V2 + ADMIT + EXACT-MEASURED + no refusals and the
                                     SAME last-duplicate row V1 platform_admit selects; otherwise None

The V1 model is imported by path after its sha256 is checked; it is never edited or re-implemented.
Run under python3 -I -B with jsonschema importable (the product's pinned tools/contracts/python-packages).
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

_D = Path(__file__).resolve().parent
_ROOT = _D.parents[4]
V1_MODEL_PATH = _ROOT / 'docs/coop/design-corrections/security/security_lifecycle_model_v1.py'
V1_MODEL_SHA256 = 'd0ef9814d27b86f10bdc1aa9a9a4781124c93c3dd92eeecdfe3090fe21d18bb9'
V1_BUNDLE_PATH = _ROOT / 'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'
V1_BUNDLE_SHA256 = 'f66d2c617084825e3cdb9a855a151c10aa66625968b40ef91fc6bb3be39423f4'
V2_SCHEMA_PATH = _D.parent / 'schema/platform-profile-set-v2.schema.json'
PROFILE_DOMAIN = 'opensip.metadata.platform-profile-set.1'
ACL_OMISSION_MEMBER = 'installAclOmission'
ACL_OMISSION_VALUE = 'no-acl-stored'
READERS = ('v1-only', 'v1-or-v2')


def _load_v1():
    for path, digest in ((V1_MODEL_PATH, V1_MODEL_SHA256), (V1_BUNDLE_PATH, V1_BUNDLE_SHA256)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError('pinned V1 input changed: %s' % path.name)
    spec = importlib.util.spec_from_file_location('security_lifecycle_model_v1', V1_MODEL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V1 = _load_v1()
Reject = V1.Reject
_V2_SCHEMA = json.loads(V2_SCHEMA_PATH.read_bytes())


def _strict_object(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Reject('METADATA.DUPLICATE_KEY')
        out[k] = v
    return out


def decode_metadata(raw):
    """Strict JSON decode (duplicate keys refuse; floats refuse at canon). Not the product parser."""
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_strict_object)
    except (UnicodeDecodeError, ValueError) as exc:
        if isinstance(exc, Reject):
            raise
        raise Reject('METADATA.PARSE')


def admit_profile_set_v1_shape(body):
    """Exactly the pinned V1 rule: PlatformProfileSetV1 from the bundle, then metadata canon."""
    try:
        V1.validate_input('PlatformProfileSetV1', body)
        V1.canon(body)
    except (ValueError, Reject, V1._C.ValidationError, V1._C.AdmissionError):
        raise Reject('PROFILE_SET.SCHEMA_SHAPE')
    return body


def admit_profile_set_v2_shape(body):
    """PlatformProfileSetV2: the unit's closed schema through the same foundation exact validator
    (type-exact const, i64/UTF-8 typing) the V1 model uses, then the same metadata canon."""
    try:
        V1._C.validate(copy.deepcopy(_V2_SCHEMA), body)
        V1.canon(body)
    except (ValueError, Reject, V1._C.ValidationError, V1._C.AdmissionError):
        raise Reject('PROFILE_SET.SCHEMA_SHAPE')
    if type(body.get('profileSetSchema')) is not int or body['profileSetSchema'] != 2:
        raise Reject('PROFILE_SET.SCHEMA_SHAPE')
    return body


def admit_profile_set_shape(body, reader):
    """Reader opt-in (decision 3). 'v1-only' is every existing caller and refuses profileSetSchema 2."""
    if reader not in READERS:
        raise ValueError('unknown reader')
    try:
        admit_profile_set_v1_shape(body)
        return 1
    except Reject:
        if reader == 'v1-only':
            raise
    admit_profile_set_v2_shape(body)
    return 2


def shape_valid(body, reader):
    try:
        admit_profile_set_shape(body, reader)
        return True
    except Reject:
        return False


def v2_only_shape_valid(body):
    try:
        admit_profile_set_v2_shape(body)
        return True
    except Reject:
        return False


def profile_set_digest(body):
    """Decision 4: one domain for both versions; profileSetSchema inside the canonical body separates them."""
    return V1.metadata_sha(PROFILE_DOMAIN, body)


def _matched_row_index(profile_set, observed):
    """The row V1 platform_admit selects: `{m['build']: m for m in rows}[build]`, i.e. the LAST row whose
    build equals the observed osversion. kernUuid/dyldCdhash are then compared against that row only."""
    plat = observed.get('platform')
    if not isinstance(plat, str) or not plat.startswith('macos'):
        return None
    rows = profile_set['platforms'][plat]['measuredProfiles']
    build = observed.get('osversion')
    for i in range(len(rows) - 1, -1, -1):
        if rows[i]['build'] == build:
            return i
    return None


SELECTED_CORPUS = 'crates/security/tests/fixtures/platform-admission-cases.ndjson'
SELECTED_CORPUS_SHA256 = 'f8a51a0fa47da17183c5c0629d4749ef16418dfc8d1d86c9ca651e3e3e05793a'
_INSTALL_ROOT_FS = 'NT-TCB-BOOT:INSTALL_ROOT_FS'


def selected_refusal_spelling(refusal):
    """Refusal spelling of the SELECTED product corpus (SELECTED_CORPUS, sha256 above), which is authoritative
    over the pinned V1 model for this string. The pinned model appends `_<fsType>` to the install-root
    filesystem refusal (`NT-TCB-BOOT:INSTALL_ROOT_FS_hfs`); the selected corpus (31 rows) and the Rust decision
    use the plain `NT-TCB-BOOT:INSTALL_ROOT_FS`. check_cases.py proves this is the only refusal SPELLING that
    differs between the two over the whole corpus. The pinned V1 model is not edited."""
    if refusal.startswith(_INSTALL_ROOT_FS + '_'):
        return _INSTALL_ROOT_FS
    return refusal


def _selected_spelling(decision):
    return dict(decision, refusals=[selected_refusal_spelling(r) for r in decision['refusals']])


def platform_admit_v2(profile_set, observed):
    """V2 shape, then the V1 decision (the V1 function ignores the extra row member) with the selected
    corpus refusal spelling, plus the matched measured row, recorded only on a macOS EXACT-MEASURED
    decision (decision 5)."""
    admit_profile_set_v2_shape(profile_set)
    decision = _selected_spelling(V1.platform_admit(profile_set, observed))
    decision = dict(decision, profileSetSchema=2, matchedMeasuredRow=None)
    if decision['tier'] == 'EXACT-MEASURED' and decision['platform'].startswith('macos'):
        decision['matchedMeasuredRow'] = _matched_row_index(profile_set, observed)
    return decision


def platform_admit_for_reader(profile_set, observed, reader):
    version = admit_profile_set_shape(profile_set, reader)
    if version == 2:
        return platform_admit_v2(profile_set, observed)
    return dict(_selected_spelling(V1.platform_admit(profile_set, observed)), profileSetSchema=1, matchedMeasuredRow=None)


def matched_install_acl_omission(profile_set, observed):
    """The ONLY read of installAclOmission Evidence B may use (458b decision 5, 458 section 3).

    Returns 'no-acl-stored' iff the profile set is V2, the decision is ADMIT at EXACT-MEASURED with no
    refusals, and the last-duplicate matched row carries the member. BASELINE-ATTESTED, REFUSE, V1, Linux
    and any other duplicate row yield None. Never scans rows for the member."""
    if not isinstance(profile_set, dict) or type(profile_set.get('profileSetSchema')) is not int \
            or profile_set['profileSetSchema'] != 2:
        return None
    decision = platform_admit_v2(profile_set, observed)
    if decision['result'] != 'ADMIT' or decision['tier'] != 'EXACT-MEASURED' or decision['refusals']:
        return None
    index = decision['matchedMeasuredRow']
    if index is None:
        return None
    row = profile_set['platforms'][decision['platform']]['measuredProfiles'][index]
    if row.get('build') != observed.get('osversion') or row.get('kernUuid') != observed.get('kernUuid') \
            or row.get('dyldCdhash') != observed.get('dyldCdhash'):
        return None
    return ACL_OMISSION_VALUE if row.get(ACL_OMISSION_MEMBER) == ACL_OMISSION_VALUE else None


def projected_decision(profile_set, observed, reader='v1-or-v2'):
    """The field set the product platform-admission corpus compares, plus the accessor result."""
    d = platform_admit_for_reader(profile_set, observed, reader)
    return {'result': d['result'], 'platform': d['platform'], 'tier': d['tier'], 'lane': d['lane'],
            'refusals': d['refusals'], 'drift': d['drift'],
            'matchedInstallAclOmission': matched_install_acl_omission(profile_set, observed)}
