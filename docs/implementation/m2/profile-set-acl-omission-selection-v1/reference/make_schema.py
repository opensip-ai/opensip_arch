"""Derive PlatformProfileSetV2 (law 458b decision 1) mechanically from the pinned V1 bundle.

Run: python3 -I -B make_schema.py [--check]
Reads the pinned security-lifecycle.schemas.v1.json (never edits it), extracts PlatformProfileSetV1 and
the one bundle $def it references (Hex64), rewrites bundle-relative $refs to document-local ones, then
applies exactly two edits:
  1. /properties/profileSetSchema/const 1 -> 2
  2. /$defs/macos/properties/measuredProfiles/items/properties/installAclOmission = {"const":"no-acl-stored"}
     (optional: `required` is untouched)
It then asserts, by a full structural diff against the ref-normalised V1, that these are the ONLY
differences, and writes ../schema/platform-profile-set-v2.schema.json. With --check it only compares.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[4]
BUNDLE = ROOT / 'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'
BUNDLE_SHA256 = 'f66d2c617084825e3cdb9a855a151c10aa66625968b40ef91fc6bb3be39423f4'
OUT = D.parent / 'schema/platform-profile-set-v2.schema.json'
V1_PREFIX = '#/schemas/PlatformProfileSetV1/$defs/'
META = {'$schema', '$id', '$comment'}
MEMBER_PATH = ('$defs', 'macos', 'properties', 'measuredProfiles', 'items', 'properties', 'installAclOmission')


def load_v1():
    raw = BUNDLE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BUNDLE_SHA256, 'pinned V1 bundle changed'
    bundle = json.loads(raw)
    return bundle, copy.deepcopy(bundle['schemas']['PlatformProfileSetV1'])


def localise(node, bundle, needed):
    """Rewrite V1 bundle refs to document-local refs; collect bundle-level $defs used."""
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == '$ref':
                if v.startswith(V1_PREFIX):
                    v = '#/$defs/' + v[len(V1_PREFIX):]
                elif v.startswith('#/$defs/'):
                    name = v[len('#/$defs/'):]
                    assert name in bundle['$defs'], v
                    needed.add(name)
                else:
                    raise AssertionError('unexpected ref ' + v)
                out[k] = v
            else:
                out[k] = localise(v, bundle, needed)
        return out
    if isinstance(node, list):
        return [localise(x, bundle, needed) for x in node]
    return node


def normalised_v1():
    bundle, v1 = load_v1()
    needed = set()
    doc = localise(v1, bundle, needed)
    assert needed == {'Hex64'}, needed
    for name in sorted(needed):
        assert name not in doc['$defs'], name
        doc['$defs'][name] = copy.deepcopy(bundle['$defs'][name])
    return doc


def derive():
    v1 = normalised_v1()
    v2 = copy.deepcopy(v1)
    assert v2['properties']['profileSetSchema'] == {'const': 1}
    v2['properties']['profileSetSchema'] = {'const': 2}
    row = v2['$defs']['macos']['properties']['measuredProfiles']['items']
    assert row['additionalProperties'] is False and 'installAclOmission' not in row['properties']
    row['properties']['installAclOmission'] = {'const': 'no-acl-stored'}
    doc = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
           '$id': 'urn:opensip:proposed:platform-profile-set-v2',
           '$comment': ('PlatformProfileSetV2 (law 458b). Derived by make_schema.py from the pinned '
                        'security-lifecycle.schemas.v1.json PlatformProfileSetV1 (sha256 ' + BUNDLE_SHA256 + '). '
                        'Identical to V1 except profileSetSchema const 2 and the optional macOS measured-row member '
                        'installAclOmission const "no-acl-stored". Digest domain unchanged: '
                        'opensip.metadata.platform-profile-set.1. Reader opt-in only; V1 readers keep refusing it. '
                        'Values in fixtures are SYNTHETIC. No schema result qualifies a boot identity.')}
    doc.update(v2)
    return v1, doc


def diff(a, b, path=()):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(path + (k,))
            else:
                out.extend(diff(a[k], b[k], path + (k,)))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(diff(x, y, path + (i,)))
        return out
    return [] if a == b else [path]


def assert_two_differences(v1, doc):
    body = {k: v for k, v in doc.items() if k not in META}
    got = diff(v1, body)
    assert got == [MEMBER_PATH, ('properties', 'profileSetSchema', 'const')], got
    assert body['properties']['profileSetSchema']['const'] == 2 and type(body['properties']['profileSetSchema']['const']) is int
    assert body['$defs']['macos']['properties']['measuredProfiles']['items']['properties']['installAclOmission'] == {'const': 'no-acl-stored'}
    assert body['$defs']['macos']['properties']['measuredProfiles']['items']['required'] == ['build', 'kernUuid', 'dyldCdhash', 'lane']
    return got


def main():
    v1, doc = derive()
    got = assert_two_differences(v1, doc)
    raw = (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    if '--check' in sys.argv[1:]:
        assert OUT.read_bytes() == raw, 'schema file differs from mechanical derivation'
    else:
        OUT.write_bytes(raw)
    print(json.dumps({'schema': str(OUT.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'bytes': len(raw), 'differencesFromV1': ['/' + '/'.join(map(str, p)) for p in got]}))


if __name__ == '__main__':
    main()
