#!/usr/bin/env python3
"""Retained checker for security-vectors.v1.json (opensip-metadata-canonical.1).

Recomputes every canonical encoding, every domain-separated digest and every
rejection in the vector file from the rules stated in security-completion.v1.md
section 2, and verifies the Ed25519 example signature with OpenSSL. Exit 0 only
when every vector reproduces byte-exactly. Design evidence only: this checker
qualifies nothing and is not the production implementation.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unicodedata

I64MIN, I64MAX = -2**63, 2**63 - 1


class Reject(Exception):
    pass


def canon(v):
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if v is None:
        return 'null'
    if isinstance(v, int):
        if v < I64MIN or v > I64MAX:
            raise Reject('INTEGER_OUT_OF_RANGE')
        return str(v)
    if isinstance(v, float):
        raise Reject('FLOAT_FORBIDDEN')
    if isinstance(v, str):
        try:
            v.encode('utf-8')
        except UnicodeEncodeError:
            raise Reject('LONE_SURROGATE')
        if unicodedata.normalize('NFC', v) != v:
            raise Reject('NON_NFC_STRING')
        out = ['"']
        for ch in v:
            o = ord(ch)
            if ch == '"':
                out.append('\\"')
            elif ch == '\\':
                out.append('\\\\')
            elif ch == '\b':
                out.append('\\b')
            elif ch == '\t':
                out.append('\\t')
            elif ch == '\n':
                out.append('\\n')
            elif ch == '\f':
                out.append('\\f')
            elif ch == '\r':
                out.append('\\r')
            elif o < 0x20:
                out.append('\\u%04x' % o)
            else:
                out.append(ch)
        out.append('"')
        return ''.join(out)
    if isinstance(v, list):
        return '[' + ','.join(canon(x) for x in v) + ']'
    if isinstance(v, dict):
        keys = list(v.keys())
        for k in keys:
            if not isinstance(k, str):
                raise Reject('NON_STRING_KEY')
        nfc = [unicodedata.normalize('NFC', k) for k in keys]
        if len(set(nfc)) != len(nfc):
            raise Reject('NFC_KEY_COLLISION')
        ks = sorted(keys, key=lambda k: [ord(c) for c in k])
        return '{' + ','.join(canon(k) + ':' + canon(v[k]) for k in ks) + '}'
    raise Reject('OUTSIDE_DATA_MODEL')


def digest(domain, v):
    b = canon(v).encode('utf-8')
    return hashlib.sha256(domain.encode('utf-8') + b'\x00' + b).hexdigest(), b


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    vec = json.load(open(os.path.join(here, 'security-vectors.v1.json'), encoding='utf-8'))
    failures = []

    def check(name, ok, detail=''):
        if not ok:
            failures.append('%s: %s' % (name, detail))

    d, b = digest(vec['V-MAN-1']['domain'], vec['V-MAN-1']['input'])
    check('V-MAN-1', d == vec['V-MAN-1']['sha256'] and b.decode() == vec['V-MAN-1']['canonical'], 'digest or canonical mismatch')
    d, b = digest('opensip.metadata.test.1', {"": 1, "\U00010000": 2})
    check('V-UR1', d == vec['V-UR1']['sha256'] and b.hex() == vec['V-UR1']['canonicalHex'])
    d, b = digest('opensip.metadata.test.1', {"a": 0, "b": -1, "c": I64MAX, "d": I64MIN})
    check('V-UR2', d == vec['V-UR2']['sha256'] and b.decode() == vec['V-UR2']['canonical'])
    for bad, lab in ((2**63, 'V-UR2-REJECT-OVER'), (-2**63 - 1, 'V-UR2-REJECT-UNDER')):
        try:
            canon({"x": bad}); check(lab, False, 'accepted')
        except Reject as e:
            check(lab, str(e) == vec[lab]['reject'], str(e))
    try:
        canon({"s": "é"}); check('V-UR3-REJECT', False, 'accepted')
    except Reject as e:
        check('V-UR3-REJECT', str(e) == vec['V-UR3-REJECT']['reject'], str(e))
    d, b = digest('opensip.metadata.test.1', {"s": "é"})
    check('V-UR3-NFC', d == vec['V-UR3-NFC']['sha256'] and b.hex() == vec['V-UR3-NFC']['canonicalHex'])
    d, b = digest('opensip.metadata.test.1', {"s": "a\"b\\c/de\tfég\U0001f600"})
    check('V-UR4', d == vec['V-UR4']['sha256'] and b.hex() == vec['V-UR4']['canonicalHex'])
    try:
        canon({"s": "\ud800"}); check('V-UR5-REJECT', False, 'accepted')
    except Reject as e:
        check('V-UR5-REJECT', str(e) == vec['V-UR5-REJECT']['reject'], str(e))
    try:
        canon({"a": 1, "b": 2.0}); check('V-FLOAT-REJECT', False, 'accepted')
    except Reject as e:
        check('V-FLOAT-REJECT', str(e) == vec['V-FLOAT-REJECT']['reject'], str(e))
    try:
        canon({"é": 1, "é": 2}); check('V-NFC-KEY-COLLISION', False, 'accepted')
    except Reject as e:
        check('V-NFC-KEY-COLLISION', str(e) == vec['V-NFC-KEY-COLLISION']['reject'], str(e))

    # Ed25519 example: verify with OpenSSL from the raw 32-byte public key.
    s = vec['V-SIG-1']
    pub = bytes.fromhex(s['publicKeyHex'])
    check('V-SIG-1.keyId', hashlib.sha256(pub).hexdigest() == s['keyId'])
    der = bytes.fromhex('302a300506032b6570032100') + pub
    with tempfile.TemporaryDirectory() as td:
        pem = os.path.join(td, 'pub.der')
        open(pem, 'wb').write(der)
        msg = os.path.join(td, 'msg.bin')
        open(msg, 'wb').write(bytes.fromhex(vec['V-MAN-1']['sha256']))
        sig = os.path.join(td, 'sig.bin')
        open(sig, 'wb').write(bytes.fromhex(s['signatureHex']))
        r = subprocess.run(['openssl', 'pkeyutl', '-verify', '-rawin', '-pubin', '-keyform', 'DER', '-inkey', pem,
                            '-in', msg, '-sigfile', sig], capture_output=True, text=True)
        check('V-SIG-1.verify', r.returncode == 0 and 'Verified Successfully' in r.stdout, r.stdout + r.stderr)

    # Full schema-valid manifest + envelope pair (security-completion.v1.md 2.2).
    def verify_sig(pub_hex, msg_hex, sig_hex):
        der = bytes.fromhex('302a300506032b6570032100') + bytes.fromhex(pub_hex)
        with tempfile.TemporaryDirectory() as td:
            pem = os.path.join(td, 'pub.der'); open(pem, 'wb').write(der)
            msg = os.path.join(td, 'msg.bin'); open(msg, 'wb').write(bytes.fromhex(msg_hex))
            sg = os.path.join(td, 'sig.bin'); open(sg, 'wb').write(bytes.fromhex(sig_hex))
            r = subprocess.run(['openssl', 'pkeyutl', '-verify', '-rawin', '-pubin', '-keyform', 'DER', '-inkey', pem,
                                '-in', msg, '-sigfile', sg], capture_output=True, text=True)
            return r.returncode == 0 and 'Verified Successfully' in r.stdout

    full = vec['V-MAN-FULL-1']
    stored = open(os.path.join(here, full['storedFile']), 'rb').read()
    check('V-MAN-FULL-1.stored', hashlib.sha256(stored).hexdigest() == full['storedSha256'])
    obj = json.loads(stored.decode('utf-8'))
    pre, cb = digest(full['domain'], obj)
    check('V-MAN-FULL-1.preimage', pre == full['preimageSha256'] and len(cb) == full['canonicalLength'])
    check('V-MAN-FULL-1.canonicalFile', hashlib.sha256(open(os.path.join(here, full['canonicalFile']), 'rb').read()).hexdigest() == full['canonicalSha256'] and hashlib.sha256(cb).hexdigest() == full['canonicalSha256'])
    check('V-MAN-FULL-1.schemaShape', obj['role'] == 'analyzer' and all(isinstance(p['tree'], dict) for p in obj['platforms'])
          and all('permission' in p for p in obj['permissions']) and obj['compatibility']['hostCore'] == {"min": "0.1.0", "max": "0.2.0", "includeMin": True, "includeMax": False})
    pub_hex = vec['V-SIG-1']['publicKeyHex']
    env = json.load(open(os.path.join(here, vec['V-ENV-1']['file']), encoding='utf-8'))
    check('V-ENV-1.subject', env['subject']['storedSha256'] == full['storedSha256'] and env['subject']['preimageSha256'] == pre)
    check('V-ENV-1.signature', all(verify_sig(pub_hex, env['subject']['preimageSha256'], s['signature']) and s['keyId'] == vec['V-ENV-1']['keyId'] for s in env['signatures']))
    bad = json.load(open(os.path.join(here, vec['V-ENV-MISMATCH-1']['file']), encoding='utf-8'))
    check('V-ENV-MISMATCH-1.stored-matches', bad['subject']['storedSha256'] == full['storedSha256'])
    check('V-ENV-MISMATCH-1.preimage-differs', bad['subject']['preimageSha256'] != pre and bad['subject']['preimageSha256'] == vec['V-ENV-MISMATCH-1']['carriedPreimage'])
    check('V-ENV-MISMATCH-1.signature-valid-over-carried', all(verify_sig(pub_hex, bad['subject']['preimageSha256'], s['signature']) for s in bad['signatures']))
    # Verification order 2.2: step 2 passes, step 3 fails -> the only lawful outcome is ENVELOPE_MISMATCH.

    if failures:
        print('FAIL'); [print(' ', f) for f in failures]; sys.exit(1)
    print('PASS: %d vectors reproduce; Ed25519 example verifies; full manifest pair verifies and the mismatch pair fails at step 3 only' % (len(vec)))


if __name__ == '__main__':
    main()
