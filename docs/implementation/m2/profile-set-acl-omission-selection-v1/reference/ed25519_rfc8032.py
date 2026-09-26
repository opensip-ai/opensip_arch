"""Pure-Python Ed25519 (RFC 8032 section 5.1) for PUBLIC TEST-ONLY fixture signing and checking.

Design evidence only. Not constant time, not a product primitive, never used with operational keys.
It exists because the reference interpreter has no `cryptography` package. check_cases.py proves it
against the public keys in the product fixture profile-roots.json and against the existing signed
V1 corpus before any new signature is trusted.
"""
import hashlib

P = 2 ** 255 - 19
L = 2 ** 252 + 27742317777372353535851937790883648493
D = -121665 * pow(121666, P - 2, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)


def _sha512(data):
    return hashlib.sha512(data).digest()


def _add(a, b):
    x1, y1, z1, t1 = a
    x2, y2, z2, t2 = b
    A = (y1 - x1) * (y2 - x2) % P
    B = (y1 + x1) * (y2 + x2) % P
    C = 2 * t1 * t2 * D % P
    Dd = 2 * z1 * z2 % P
    E, F, G, H = B - A, Dd - C, Dd + C, B + A
    return (E * F % P, G * H % P, F * G % P, E * H % P)


def _mul(s, p):
    q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            q = _add(q, p)
        p = _add(p, p)
        s >>= 1
    return q


def _equal(a, b):
    x1, y1, z1, _ = a
    x2, y2, z2, _ = b
    return (x1 * z2 - x2 * z1) % P == 0 and (y1 * z2 - y2 * z1) % P == 0


def _recover_x(y, sign):
    if y >= P:
        return None
    x2 = (y * y - 1) * pow(D * y * y + 1, P - 2, P)
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P != 0:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P != 0:
        return None
    if (x & 1) != sign:
        x = P - x
    return x


_GY = 4 * pow(5, P - 2, P) % P
_GX = _recover_x(_GY, 0)
G = (_GX, _GY, 1, _GX * _GY % P)


def _compress(p):
    x, y, z, _ = p
    zinv = pow(z, P - 2, P)
    x, y = x * zinv % P, y * zinv % P
    return int.to_bytes(y | ((x & 1) << 255), 32, 'little')


def _decompress(s):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, 'little')
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % P)


def _secret_expand(secret):
    if len(secret) != 32:
        raise ValueError('bad secret length')
    h = _sha512(secret)
    a = int.from_bytes(h[:32], 'little')
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def public_key(secret):
    a, _ = _secret_expand(secret)
    return _compress(_mul(a, G))


def sign(secret, msg):
    a, prefix = _secret_expand(secret)
    A = _compress(_mul(a, G))
    r = int.from_bytes(_sha512(prefix + msg), 'little') % L
    R = _compress(_mul(r, G))
    h = int.from_bytes(_sha512(R + A + msg), 'little') % L
    s = (r + h * a) % L
    return R + int.to_bytes(s, 32, 'little')


def verify(public, msg, signature):
    """RFC 8032 verification with the canonical-S check (s < L), as strict readers require."""
    if len(public) != 32 or len(signature) != 64:
        return False
    A = _decompress(public)
    if A is None or _compress(A) != public:
        return False
    Rs = signature[:32]
    R = _decompress(Rs)
    if R is None:
        return False
    s = int.from_bytes(signature[32:], 'little')
    if s >= L:
        return False
    h = int.from_bytes(_sha512(Rs + public + msg), 'little') % L
    return _equal(_mul(s, G), _add(R, _mul(h, A)))


# RFC 8032 section 7.1 TEST 1 (empty message); checked on import so a broken copy fails closed.
_T1_SK = bytes.fromhex('9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60')
_T1_PK = bytes.fromhex('d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a')
_T1_SIG = bytes.fromhex('e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155'
                        '5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b')
assert public_key(_T1_SK) == _T1_PK and sign(_T1_SK, b'') == _T1_SIG and verify(_T1_PK, b'', _T1_SIG)
