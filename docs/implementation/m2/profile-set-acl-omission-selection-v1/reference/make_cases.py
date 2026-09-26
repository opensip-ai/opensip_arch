"""Generate the 458b V2 case files (SYNTHETIC; public test-only seeds only).

Run: python3 -I -B make_cases.py --product <opensip checkout> --packages <dir with jsonschema> [--also <dir>]
Reads, read-only and sha256-pinned, three product fixtures: the V1 shape corpus (its first valid row is the
base payload), profile-roots.json (root "2" keys and TR-PROFILE role) and the V1 platform corpus (observed
bases). Writes ../cases/*.v2.ndjson (and a byte-identical copy into --also when given). Existing V1
fixtures are never modified, re-signed or re-projected.

Row formats follow the V1 files:
  profile-shape-cases.v2.ndjson       {label, hex, valid, validV1}: `valid` = V2 shape (profile_shape_v2 plus
                                      metadata bytes); `validV1` = the unchanged V1 shape (profile_shape).
  profile-signature-cases.v2.ndjson   V1 fields {label, root, stored, envelope, corePin, revoked, expected}
                                      where `expected` is the V1-only verifier (verify_profile_set), plus
                                      `expectedV2` for the opt-in V1-or-V2 reader.
  platform-admission-cases.v2.ndjson  {label, profileSet, observed, expected}; `expected` has the V1 corpus
                                      fields plus `matchedInstallAclOmission` ("no-acl-stored" or null).
"""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
PINS = {
    'crates/security/tests/fixtures/profile-shape-cases.ndjson': 'c289c5a7298f5ab5da2c39312ec945245af1819d8eec0be830b465709940456a',
    'crates/security/tests/fixtures/profile-roots.json': '1a95f7bf62525bc6f63b73a840df9f0ef3a758f24df15ddfda062d11b015d2ff',
    'crates/security/tests/fixtures/platform-admission-cases.ndjson': 'f8a51a0fa47da17183c5c0629d4749ef16418dfc8d1d86c9ca651e3e3e05793a',
}
MEMBER = 'installAclOmission'
VALUE = 'no-acl-stored'
MAC = 'macos-aarch64'


def read_pinned(product, rel):
    raw = (product / rel).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINS[rel]:
        raise SystemExit('pinned product fixture changed: ' + rel)
    return raw


def ndjson(rows):
    return b''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')).encode('utf-8') + b'\n' for r in rows)


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def inputs(product):
    shape_rows = [json.loads(l) for l in read_pinned(product, 'crates/security/tests/fixtures/profile-shape-cases.ndjson').splitlines() if l]
    base_row = next(r for r in shape_rows if r['valid'] is True)
    assert base_row['label'] == 'base'
    base_raw = bytes.fromhex(base_row['hex'])
    roots = json.loads(read_pinned(product, 'crates/security/tests/fixtures/profile-roots.json'))
    platform_rows = [json.loads(l) for l in read_pinned(product, 'crates/security/tests/fixtures/platform-admission-cases.ndjson').splitlines() if l]
    observed = {}
    for r in platform_rows:
        e = r['expected']
        if e['result'] == 'ADMIT' and e['tier'] == 'EXACT-MEASURED' and e['platform'] not in observed:
            observed[e['platform']] = r['observed']
    return base_raw, roots, observed


def with_member(body, platform=MAC, row=0, value=VALUE):
    b = copy.deepcopy(body)
    b['platforms'][platform]['measuredProfiles'][row][MEMBER] = value
    return b


def v2(body):
    b = copy.deepcopy(body)
    b['profileSetSchema'] = 2
    return b


# ------------------------------------------------------------------------------------------------ shape
def shape_cases(M, base_v1):
    v2_base = with_member(v2(base_v1))
    rows = []

    def add(label, body=None, raw=None):
        raw = compact(body) if raw is None else raw
        try:
            value = M.decode_metadata(raw)
            valid = M.v2_only_shape_valid(value)
            valid_v1 = M.shape_valid(value, 'v1-only')
        except M.Reject:
            valid = valid_v1 = False
        rows.append({'label': '458b:' + label, 'hex': raw.hex(), 'valid': valid, 'validV1': valid_v1})

    add('v2:base', v2_base)
    add('v2:member-absent', v2(base_v1))
    add('v2:member-on-both-macos', with_member(v2_base, 'macos-x86_64'))
    two = copy.deepcopy(v2(base_v1))
    rows_mac = two['platforms'][MAC]['measuredProfiles']
    rows_mac.append(dict(rows_mac[0], **{MEMBER: VALUE}))
    add('v2:duplicate-build-last-row-member', two)
    for name, value in [('empty', ''), ('other-string', 'no-acl'), ('case', 'No-Acl-Stored'), ('trailing-space', VALUE + ' '),
                        ('trailing-lf', VALUE + '\n'), ('acl-stored', 'acl-stored'), ('present-empty', 'present-empty')]:
        add('v2:wrong-value:' + name, with_member(v2(base_v1), value=value))
    for name, value in [('null', None), ('true', True), ('false', False), ('zero', 0), ('one', 1), ('array-empty', []),
                        ('array-value', [VALUE]), ('object-empty', {}), ('object-value', {'value': VALUE})]:
        add('v2:wrong-type:' + name, with_member(v2(base_v1), value=value))
    for platform in ('linux-x86_64-gnu', 'linux-aarch64-gnu'):
        add('v2:on-linux-row:' + platform, with_member(v2(base_v1), platform=platform))
        b = v2(base_v1)
        b['platforms'][platform][MEMBER] = VALUE
        add('v2:on-linux-platform-object:' + platform, b)
    b = v2(base_v1)
    b['platforms'][MAC]['supportedMajors']['25'][MEMBER] = VALUE
    add('v2:on-supportedMajors-entry', b)
    b = v2(base_v1)
    b['platforms'][MAC]['supportedMajors'][MEMBER] = VALUE
    add('v2:on-supportedMajors-map', b)
    b = v2(base_v1)
    b['platforms'][MAC][MEMBER] = VALUE
    add('v2:on-macos-platform-object', b)
    b = v2(base_v1)
    b['platforms'][MEMBER] = VALUE
    add('v2:on-platforms-map', b)
    b = v2(base_v1)
    b[MEMBER] = VALUE
    add('v2:at-top-level', b)
    add('v1:base-no-member', base_v1)
    add('v1:with-member', with_member(base_v1))
    add('v1:with-member-both-macos', with_member(with_member(base_v1), 'macos-x86_64'))
    for schema in (3, 0, -1):
        b = copy.deepcopy(base_v1)
        b['profileSetSchema'] = schema
        add('schema-%d:no-member' % schema, b)
        add('schema-%d:with-member' % schema, with_member(b))
    for name, value in [('true', True), ('string', '2'), ('null', None)]:
        b = with_member(copy.deepcopy(base_v1))
        b['profileSetSchema'] = value
        add('schema-type:' + name + ':with-member', b)
    b = with_member(v2(base_v1))
    del b['platforms'][MAC]['measuredProfiles'][0]['lane']
    add('v2:member-row-missing-lane', b)
    add('v2:duplicate-member-key', raw=compact(v2(base_v1)).replace(
        b'"lane":"macos-15"}', b'"lane":"macos-15","installAclOmission":"no-acl-stored","installAclOmission":"no-acl-stored"}', 1))
    return rows


# -------------------------------------------------------------------------------------------- signature
def signature_cases(M, E, base_v1, roots):
    root2 = roots['2']
    k0, k1, k2 = root2['roles']['TR-PROFILE']['keys']
    body_member = with_member(v2(base_v1))
    body_plain = v2(base_v1)
    rows = []

    def add(label, body, signers, *, root='2', corrupt=(), pin='self', revoked=(), strip_member=False):
        stored, envelope = E.sign_envelope(root2, body, signers, corrupt)
        if strip_member:  # presented bytes differ from the signed bytes
            stripped = copy.deepcopy(body)
            for r in stripped['platforms'][MAC]['measuredProfiles']:
                r.pop(MEMBER, None)
            stored = E.stored_bytes(stripped)
        core_pin = M.profile_set_digest(body) if pin == 'self' else pin
        row = {'label': '458b:' + label, 'root': root, 'stored': stored.hex(), 'envelope': envelope,
               'corePin': core_pin, 'revoked': list(revoked)}
        row['expected'] = E.reference_verify(roots[root], stored, envelope, core_pin, list(revoked), 'v1-only')
        row['expectedV2'] = E.reference_verify(roots[root], stored, envelope, core_pin, list(revoked), 'v1-or-v2')
        rows.append(row)

    add('admit:v2-member:keys01', body_member, [k0, k1])
    add('admit:v2-no-member:keys01', body_plain, [k0, k1])
    add('v1-reader:v2-member:keys012', body_member, [k0, k1, k2])
    add('control:v1-body:keys01', base_v1, [k0, k1])
    add('bad-signature:v2-member:key1-corrupt', body_member, [k0, k1], corrupt={k1})
    add('bad-signature:v2-member:all-corrupt', body_member, [k0, k1, k2], corrupt={k0, k1, k2})
    add('bad-signature:v2-member:one-key', body_member, [k2])
    add('shape:v2-wrong-value', with_member(v2(base_v1), value='no-acl'), [k0, k1])
    add('shape:v2-wrong-type', with_member(v2(base_v1), value=True), [k0, k1])
    add('shape:v2-member-on-linux-row', with_member(v2(base_v1), platform='linux-x86_64-gnu'), [k0, k1])
    add('shape:v1-body-with-member', with_member(base_v1), [k0, k1])
    b3 = with_member(copy.deepcopy(base_v1))
    b3['profileSetSchema'] = 3
    add('shape:schema-3-with-member', b3, [k0, k1])
    add('pin:v2-member:v1-base-digest', body_member, [k0, k1], pin=M.profile_set_digest(base_v1))
    add('pin:v2-member:none', body_member, [k0, k1], pin=None)
    add('pin:v2-member:v2-no-member-digest', body_member, [k0, k1], pin=M.profile_set_digest(body_plain))
    add('revoked:v2-member:key1', body_member, [k0, k1], revoked=[k1])
    add('root1:v2-member', body_member, [k0, k1], root='1')
    add('stored:v2-member-stripped-after-signing', body_member, [k0, k1], strip_member=True)
    return rows


# ---------------------------------------------------------------------------------------------- platform
def platform_cases(M, base_v1, observed):
    mac = observed[MAC]
    other_uuid = '00000000-0000-4000-8000-000000000001'
    rows = []

    def add(label, profile, obs):
        rows.append({'label': '458b:' + label, 'profileSet': profile, 'observed': obs,
                     'expected': M.projected_decision(profile, obs, 'v1-or-v2')})

    def mac_rows(*specs):
        b = v2(base_v1)
        first = b['platforms'][MAC]['measuredProfiles'][0]
        out = []
        for member, kern in specs:
            r = {k: first[k] for k in ('build', 'kernUuid', 'dyldCdhash', 'lane')}
            if kern is not None:
                r['kernUuid'] = kern
            if member:
                r[MEMBER] = VALUE
            out.append(r)
        b['platforms'][MAC]['measuredProfiles'] = out
        return b

    add('exact:member', with_member(v2(base_v1)), mac)
    add('exact:no-member', v2(base_v1), mac)
    add('exact:x86_64-member', with_member(v2(base_v1), 'macos-x86_64'), observed['macos-x86_64'])
    add('exact:member-on-other-platform-only', with_member(v2(base_v1), 'macos-x86_64'), mac)
    add('duplicate:last-carries', mac_rows((False, None), (True, None)), mac)
    add('duplicate:first-carries', mac_rows((True, None), (False, None)), mac)
    add('duplicate:last-other-identity-first-matches-with-member', mac_rows((True, None), (False, other_uuid)), mac)
    add('duplicate:first-other-identity-last-matches-with-member', mac_rows((False, other_uuid), (True, None)), mac)
    add('duplicate:last-other-identity-with-member', mac_rows((False, None), (True, other_uuid)), mac)
    add('baseline:member-on-measured-row', with_member(v2(base_v1)), dict(mac, osversion='25A200'))
    add('identity:kernUuid-mismatch', with_member(v2(base_v1)), dict(mac, kernUuid=other_uuid))
    add('identity:dyldCdhash-mismatch', with_member(v2(base_v1)), dict(mac, dyldCdhash='0' * 40))
    add('refusal:sip-off', with_member(v2(base_v1)), dict(mac, sip=False))
    add('refusal:fs-type', with_member(v2(base_v1)), dict(mac, fsType='hfs'))
    b = with_member(v2(base_v1))
    b['platforms'][MAC]['measuredProfiles'][0]['lane'] = 'macos-15-intel'
    add('refusal:unlisted-lane', b, mac)
    add('refusal:major-outside-population', with_member(v2(base_v1)), dict(mac, osversion='26A100'))
    add('v1:exact', base_v1, mac)
    add('v1:baseline', base_v1, dict(mac, osversion='25A200'))
    add('linux:exact-v2', v2(base_v1), observed['linux-x86_64-gnu'])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', required=True, type=Path)
    ap.add_argument('--packages', required=True, type=Path)
    ap.add_argument('--also', type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.packages.resolve()))
    sys.path.insert(0, str(D))
    import profile_set_v2_model as M
    import profile_envelope as E
    base_raw, roots, observed = inputs(args.product.resolve())
    base_v1 = M.decode_metadata(base_raw)
    assert M.shape_valid(base_v1, 'v1-only') and not M.v2_only_shape_valid(base_v1)
    E.check_root_keys(roots['2'])
    files = {
        'profile-shape-cases.v2.ndjson': ndjson(shape_cases(M, base_v1)),
        'profile-signature-cases.v2.ndjson': ndjson(signature_cases(M, E, base_v1, roots)),
        'platform-admission-cases.v2.ndjson': ndjson(platform_cases(M, base_v1, observed)),
    }
    out = {}
    for name, raw in files.items():
        for directory in [D.parent / 'cases'] + ([args.also] if args.also else []):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / name).write_bytes(raw)
        out[name] = {'rows': raw.count(b'\n'), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
