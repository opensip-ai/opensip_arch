"""Signed profile-set envelopes for PUBLIC TEST-ONLY fixtures, and a reference of the product verifier order.

Reproduces crates/security/src/trust/native_census.rs `sign_synthetic_profile` and trust.rs
`envelope_message` exactly:
  stored          = opensip-metadata-canonical.1 bytes of the body (V1 model `canon`)
  preimageSha256  = SHA256("opensip.metadata.platform-profile-set.1" || 0x00 || stored)
  storedSha256    = SHA256(stored)
  message         = SHA256("opensip.metadata.envelope.2" || 0x00 || canon({kind, domain, storedSha256,
                    preimageSha256, role, namespace}))            (32 raw bytes are what is signed)
  key i of root "2" = Ed25519 secret SHA256(b"opensip-public-test-only-quorum62-seed-" || bytes([i])), i being
                    the key's index in that root's `keys` array; signers are the TR-PROFILE role keys.

`reference_verify` mirrors the order of admitted_profiles.rs `verify_profile_set_with` over envelopes
this module builds (carrier -> stored digest -> preimage -> raw quorum -> shape by reader -> core pin
-> TR-PROFILE role -> revocation). It is a fixture-expectation reference, not the product verifier.
"""
import hashlib

import ed25519_rfc8032 as ed
import profile_set_v2_model as M

PROFILE_DOMAIN = M.PROFILE_DOMAIN
ENVELOPE_DOMAIN = 'opensip.metadata.envelope.2'
SEED_PREFIX = b'opensip-public-test-only-quorum62-seed-'


def seed(index):
    return hashlib.sha256(SEED_PREFIX + bytes([index])).digest()


def stored_bytes(body):
    return M.V1.canon(body).encode('utf-8')


def envelope_message(envelope):
    s = envelope['subject']
    projected = {k: s[k] for k in ('kind', 'domain', 'storedSha256', 'preimageSha256')}
    projected['role'] = envelope['role']
    projected['namespace'] = envelope['namespace']
    return hashlib.sha256(ENVELOPE_DOMAIN.encode('ascii') + b'\x00' + M.V1.canon(projected).encode('utf-8')).digest()


def key_index(root, key_id):
    ids = [k['keyId'] for k in root['keys']]
    return ids.index(key_id)


def check_root_keys(root):
    """Every derived public key equals the root's; keyId is SHA256(publicKey). Returns the count checked."""
    for i, k in enumerate(root['keys']):
        pk = ed.public_key(seed(i))
        if pk.hex() != k['publicKey'] or hashlib.sha256(pk).hexdigest() != k['keyId']:
            raise AssertionError('derived public key %d differs from profile-roots.json' % i)
    return len(root['keys'])


def sign_envelope(root, body, signer_ids, corrupt=()):
    """Envelope over canon(body), signed by `signer_ids` (TR-PROFILE key ids) in the given order.
    A key id in `corrupt` gets a well-formed but wrong signature (last S byte changed, still < L)."""
    stored = stored_bytes(body)
    envelope = {
        'envelopeSchema': 2,
        'subject': {'kind': 'platform-profile-set', 'domain': PROFILE_DOMAIN,
                    'storedSha256': hashlib.sha256(stored).hexdigest(),
                    'preimageSha256': M.profile_set_digest(body)},
        'role': 'TR-PROFILE', 'namespace': 'opensip', 'signatures': []}
    message = envelope_message(envelope)
    for kid in signer_ids:
        sig = bytearray(ed.sign(seed(key_index(root, kid)), message))
        if kid in corrupt:
            sig[32] ^= 0x01
        envelope['signatures'].append({'keyId': kid, 'alg': 'ed25519', 'signature': bytes(sig).hex()})
    return stored, envelope


def reference_verify(root, stored, envelope, core_pin, revoked, reader):
    """Expected product result in the corpus field style: {'error': X} or the admit record."""
    subject = envelope['subject']
    if subject.get('kind') != 'platform-profile-set' or subject.get('domain') != PROFILE_DOMAIN \
            or envelope.get('role') != 'TR-PROFILE':
        return {'error': 'Envelope'}  # carrier routing
    if hashlib.sha256(stored).hexdigest() != subject['storedSha256']:
        return {'error': 'Envelope'}
    try:
        body = M.decode_metadata(stored)
        preimage = M.profile_set_digest(body)
    except M.Reject:
        return {'error': 'Envelope'}
    if preimage != subject['preimageSha256']:
        return {'error': 'Envelope'}
    role = (root.get('roles') or {}).get('TR-PROFILE')
    if root.get('rootSchema') != 2 or not role or role.get('standing') != 'active':
        return {'error': 'Envelope'}  # verify_quorum RoleUnavailable -> EnvelopeError -> ProfileError::Envelope
    # A namespace outside the role selects no keys, so no signature counts.
    selected = role['keys'] if envelope.get('namespace') in role.get('namespaces', []) else []
    public = {k['keyId']: bytes.fromhex(k['publicKey']) for k in root['keys'] if k['keyId'] in selected}
    message = envelope_message(envelope)
    valid = set()
    for s in envelope['signatures']:
        pk = public.get(s['keyId'])
        if pk is not None and ed.verify(pk, message, bytes.fromhex(s['signature'])):
            valid.add(s['keyId'])
    if not valid or len(valid) < role['threshold']:
        return {'error': 'SignatureThreshold'}
    try:
        M.admit_profile_set_shape(body, reader)
    except M.Reject:
        return {'error': 'Shape'}
    if core_pin != preimage:
        return {'error': 'CorePin'}
    valid -= set(revoked)
    if len(valid) < role['threshold']:
        return {'error': 'SignatureThreshold'}
    return {'admit': True, 'bodyDigest': preimage, 'valid': sorted(valid), 'required': role['threshold']}
