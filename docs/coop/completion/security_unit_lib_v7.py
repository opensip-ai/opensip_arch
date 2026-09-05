"""Shared library for the security completion unit v5 (design evidence only): the bounded corrective successor of v4 under the D-368 case addendum.

Implements opensip-metadata-canonical.1 (security-completion.v2.md section 2.1), the
domain-separated digest, the opensip-signature-envelope.2 signed-subject message, Ed25519
verification through OpenSSL, a minimal JSON-Schema-subset validator (no third-party module
is available in the reference environment), and the grant-journal DDL. Nothing here is the
production implementation; it exists so the vectors and fixtures are machine-checked.
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unicodedata

I64MIN, I64MAX = -2**63, 2**63 - 1
HEX64 = re.compile(r'^[0-9a-f]{64}$')

DOMAIN_TAGS = {
    'manifest': 'opensip.metadata.manifest.1',
    'catalog': 'opensip.metadata.catalog.1',
    'registry': 'opensip.metadata.registry.1',
    'lock': 'opensip.metadata.lock.1',
    'root': 'opensip.metadata.root.1',
    'revocation': 'opensip.metadata.revocation.1',
    'inventory': 'opensip.metadata.inventory.1',
    'payload': 'opensip.metadata.payload.1',
    'registry-view': 'opensip.metadata.registry-view.1',
    'envelope': 'opensip.metadata.envelope.2',
    'journal': 'opensip.metadata.journal.1',
    'policy': 'opensip.metadata.policy.1', 'policy-effective': 'opensip.metadata.policy-effective.1',
    'test': 'opensip.metadata.test.1',
}
# Closed kind -> (domain, role) routing table for enveloped documents (section 2.2).
KIND_ROUTING = {
    'manifest': ('opensip.metadata.manifest.1', 'TR-COMPONENT'),
    'catalog': ('opensip.metadata.catalog.1', 'TR-INDEX'),
    'root': ('opensip.metadata.root.1', 'ROOT'),
    'revocation': ('opensip.metadata.revocation.1', 'ROOT'),
    'inventory': ('opensip.metadata.inventory.1', 'TR-CORE'),
    'payload': ('opensip.metadata.payload.1', 'TR-BUNDLE'),
}


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


def canonical_bytes(v):
    return canon(v).encode('utf-8')


def domain_digest(domain, v):
    b = canonical_bytes(v)
    return hashlib.sha256(domain.encode('utf-8') + b'\x00' + b).hexdigest(), b


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


MAX_METADATA_BYTES = 4194304   # paired draft section 4 manifest/index/lock byte ceiling
MAX_JSON_NESTING = 64          # paired draft section 4


def json_nesting_depth(text):
    """Bracket depth outside strings; refuses before any recursive parse can hit an interpreter limit."""
    depth = 0; mx = 0; in_str = False; esc = False
    for ch in text:
        if in_str:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch in '[{':
            depth += 1
            if depth > mx: mx = depth
            if depth > MAX_JSON_NESTING:
                raise Reject('NESTING_TOO_DEEP')
        elif ch in ']}':
            depth -= 1
    return mx


def load_json_strict(b, max_bytes=MAX_METADATA_BYTES):
    """Parse metadata JSON to controlled refusals: size, UTF-8, nesting, huge integers, duplicate
    keys, floats. Every failure is a named Reject, never an interpreter exception."""
    if not isinstance(b, (bytes, bytearray)):
        raise Reject('NOT_BYTES')
    if len(b) > max_bytes:
        raise Reject('METADATA_TOO_LARGE')
    try:
        text = b.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        raise Reject('INVALID_UTF8')
    if text.startswith('\ufeff'):
        raise Reject('BOM_FORBIDDEN')
    json_nesting_depth(text)

    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise Reject('DUPLICATE_JSON_KEY:' + k)
            d[k] = v
        return d

    def parse_int(t):
        if len(t.lstrip('-')) > 19:
            raise Reject('INTEGER_OUT_OF_RANGE')
        v = int(t)
        if v < I64MIN or v > I64MAX:
            raise Reject('INTEGER_OUT_OF_RANGE')
        return v
    try:
        return json.loads(text, object_pairs_hook=hook, parse_int=parse_int,
                          parse_float=lambda t: (_ for _ in ()).throw(Reject('FLOAT_FORBIDDEN')),
                          parse_constant=lambda t: (_ for _ in ()).throw(Reject('NON_FINITE_FORBIDDEN')))
    except Reject:
        raise
    except RecursionError:
        raise Reject('NESTING_TOO_DEEP')
    except (ValueError, TypeError) as e:
        raise Reject('MALFORMED_JSON')


# --- signature envelope 2 ------------------------------------------------------------
def signed_subject(env):
    s = env['subject']
    return {'kind': s['kind'], 'domain': s['domain'], 'storedSha256': s['storedSha256'],
            'preimageSha256': s['preimageSha256'], 'role': env['role'], 'namespace': env['namespace']}


def envelope_message_hex(env):
    d, _ = domain_digest(DOMAIN_TAGS['envelope'], signed_subject(env))
    return d


def ed25519_verify(pub_hex, msg_hex, sig_hex):
    der = bytes.fromhex('302a300506032b6570032100') + bytes.fromhex(pub_hex)
    with tempfile.TemporaryDirectory() as td:
        pem = os.path.join(td, 'pub.der'); open(pem, 'wb').write(der)
        msg = os.path.join(td, 'msg.bin'); open(msg, 'wb').write(bytes.fromhex(msg_hex))
        sg = os.path.join(td, 'sig.bin'); open(sg, 'wb').write(bytes.fromhex(sig_hex))
        r = subprocess.run(['openssl', 'pkeyutl', '-verify', '-rawin', '-pubin', '-keyform', 'DER', '-inkey', pem,
                            '-in', msg, '-sigfile', sg], capture_output=True, text=True)
        return r.returncode == 0 and 'Verified Successfully' in r.stdout


def key_id(pub_hex):
    return sha256_hex(bytes.fromhex(pub_hex))


ROLE_NAMES = ('TR-CORE', 'TR-INDEX', 'TR-COMPONENT', 'TR-BUNDLE', 'TR-REPAIR')


def admit_root(root):
    """Semantic admission of a root document (security-completion.v3.md section 3.1). Returns a
    list of refusal strings; empty means admitted. Shape validity alone never admits a root."""
    r = []
    keys = root.get('keys', [])
    ids = [k['keyId'] for k in keys]; pubs = [k['publicKey'] for k in keys]
    if len(set(ids)) != len(ids): r.append('ROOT.DUPLICATE_KEY_ID')
    if len(set(pubs)) != len(pubs): r.append('ROOT.DUPLICATE_PUBLIC_KEY')
    for k in keys:
        if key_id(k['publicKey']) != k['keyId']: r.append('ROOT.KEY_ID_MISMATCH:' + k['keyId'][:8])
    known = set(ids)
    def refs(lst, where):
        for i in lst:
            if i not in known: r.append('ROOT.UNKNOWN_KEY_REF:%s:%s' % (where, i[:8]))
    refs(root.get('rootKeys', []), 'rootKeys')
    rk = root.get('rootKeys', [])
    if len(set(rk)) != len(rk): r.append('ROOT.DUPLICATE_ROOT_KEY')
    if not (2 <= root.get('rootThreshold', 0) <= len(rk)) or len(rk) < 3: r.append('ROOT.ROOT_THRESHOLD_POLICY')
    ra = root.get('recoveryAuthority', {})
    refs(ra.get('keys', []), 'recoveryAuthority')
    if len(ra.get('keys', [])) < 5 or not (3 <= ra.get('threshold', 0) <= len(ra.get('keys', []))): r.append('ROOT.RECOVERY_THRESHOLD_POLICY')
    if set(ra.get('keys', [])) & set(rk): r.append('ROOT.RECOVERY_NOT_DISJOINT_FROM_ROOT')
    roles = root.get('roles', {})
    if set(roles) != set(ROLE_NAMES): r.append('ROOT.ROLE_SET_NOT_EXACT')
    used = set(rk) | set(ra.get('keys', []))
    for name in ROLE_NAMES:
        d = roles.get(name)
        if not d: continue
        refs(d.get('keys', []), name)
        ks = d.get('keys', [])
        if len(set(ks)) != len(ks): r.append('ROOT.DUPLICATE_ROLE_KEY:' + name)
        if set(ks) & used: r.append('ROOT.KEY_REUSED_ACROSS_ROLES:' + name)
        used |= set(ks)
        if name == 'TR-REPAIR':
            if not (d.get('standing') == 'typed-absence-DR-110' and ks == [] and d.get('threshold') == 0 and d.get('namespaces') == []):
                r.append('ROOT.TR_REPAIR_MUST_BE_TYPED_ABSENCE')
        else:
            if d.get('standing') != 'active': r.append('ROOT.ACTIVE_ROLE_WITHOUT_ACTIVE_STANDING:' + name)
            if not (d.get('threshold', 0) >= 2 and len(ks) >= d.get('threshold', 0) + 1): r.append('ROOT.ROLE_THRESHOLD_POLICY:' + name)
            if not d.get('namespaces'): r.append('ROOT.ROLE_WITHOUT_NAMESPACE:' + name)
    kak = root.get('kernelAttestationKeys', None)
    if kak != []: r.append('ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY')   # preview: typed absence, exactly []
    for where, lst in (('recoveryAuthority', ra.get('keys', [])),) + tuple((n, d.get('keys', [])) for n, d in root.get('roles', {}).items()):
        if len(set(lst)) != len(lst): r.append('ROOT.DUPLICATE_KEY_IN_LIST:' + where)
    rv = root.get('rootVersion'); pv = root.get('previousRootVersion')
    if not (isinstance(rv, int) and not isinstance(rv, bool) and 1 <= rv <= I64MAX): r.append('ROOT.VERSION_RANGE')
    if pv is not None and not (isinstance(pv, int) and not isinstance(pv, bool) and 1 <= pv < (rv if isinstance(rv, int) else 0)): r.append('ROOT.PREVIOUS_VERSION_RANGE')
    if (rv == 1) != (pv is None): r.append('ROOT.CHAIN_ORIGIN_INCONSISTENT')
    if not (root.get('issuedAt', '') < root.get('expiresAt', '')): r.append('ROOT.EXPIRY_NOT_AFTER_ISSUE')
    return r


def _strict_int(v, lo, hi):
    return isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi


def witness_shape_refusals(w):
    """SEC3-M3 closed witness shape: witnessSchema 1; projectKeyDigest hex64; grantGeneration 1..2^63-1;
    seq int (never bool) 0..2^53-1; state PENDING|COMMITTED; bodySha256 hex64 when seq >= 1 and null only at
    COMMITTED 0; PENDING requires seq >= 1; no unknown member. Any refusal maps to QUARANTINE."""
    if not isinstance(w, dict):
        return ['NOT_AN_OBJECT']
    r = []
    allowed = {'witnessSchema', 'projectKeyDigest', 'grantGeneration', 'seq', 'bodySha256', 'state'}
    if set(w) - allowed: r.append('UNKNOWN_MEMBER')
    if not _strict_int(w.get('witnessSchema'), 1, 1): r.append('SCHEMA')
    if not (isinstance(w.get('projectKeyDigest'), str) and re.fullmatch(r'[0-9a-f]{64}', w['projectKeyDigest'])): r.append('DIGEST')
    if not _strict_int(w.get('grantGeneration'), 1, I64MAX): r.append('GENERATION')
    if not _strict_int(w.get('seq'), 0, SEQ_MAX): r.append('SEQ')
    if w.get('state') not in ('PENDING', 'COMMITTED') or not isinstance(w.get('state'), str): r.append('STATE')
    if 'bodySha256' not in w:
        r.append('HASH_MEMBER_ABSENT')             # absent and null are different: the member must be present
    if 'SEQ' not in r and 'STATE' not in r and 'HASH_MEMBER_ABSENT' not in r:
        sha_ = w['bodySha256']
        if w['seq'] == 0:
            if w['state'] != 'COMMITTED' or sha_ is not None: r.append('GENESIS')
        elif not (isinstance(sha_, str) and re.fullmatch(r'[0-9a-f]{64}', sha_)): r.append('HASH')
    return r


def _valid_journal_tail(t):
    return t is None or (isinstance(t, (tuple, list)) and len(t) == 2 and _strict_int(t[0], 1, SEQ_MAX) and isinstance(t[1], str) and re.fullmatch(r'[0-9a-f]{64}', t[1]) is not None)


def reconcile_witness(journal_tail, witness, project_key, grant_generation, terminal=False):
    """Enforcing boundary (SEC3-M3 corrective): validates the tail and the witness shape first; any
    exception inside is QUARANTINE, never an uncaught error."""
    try:
        if not (isinstance(project_key,str) and 1 <= len(project_key.encode('utf-8')) <= 1024 and '\x00' not in project_key and _strict_int(grant_generation, 1, I64MAX) and type(terminal) is bool):
            return 'QUARANTINE', 'carrier context malformed'
        if not _valid_journal_tail(journal_tail):
            return 'QUARANTINE', 'journal tail malformed'
        return _reconcile_witness_checked(journal_tail, witness, project_key, grant_generation, terminal)
    except Exception as e:
        return 'QUARANTINE', 'witnessMalformed: exception %s' % type(e).__name__


def _reconcile_witness_checked(journal_tail, witness, project_key, grant_generation, terminal=False):
    """Section 5.4 witness reconciliation on open (pure; doctor reports its result without writing). journal_tail = (seq, bodySha256) or None for an
    empty carrier; witness = dict or None (absent) or 'MALFORMED'. Returns (action, detail)."""
    tail_seq, tail_sha = journal_tail if journal_tail else (0, None)
    if witness is None:
        if tail_seq == 0:
            return 'INIT', 'genesis carrier; witness created at COMMITTED 0'
        return 'QUARANTINE', 'witness absent with non-empty journal: witnesslessRestore'
    bad = witness_shape_refusals(witness)
    if bad:
        return 'QUARANTINE', 'witnessMalformed: ' + ','.join(bad)
    if witness['projectKeyDigest'] != project_key_digest(project_key) or witness['grantGeneration'] != grant_generation:
        return 'QUARANTINE', 'witness names another carrier'
    w_seq, w_sha, w_state = witness['seq'], witness['bodySha256'], witness['state']
    if w_state == 'COMMITTED':
        if w_seq == tail_seq and (w_seq == 0 or w_sha == tail_sha):
            return 'OK', 'consistent'
        if w_seq > tail_seq:
            return 'QUARANTINE', 'uncertainTailLoss: committed %d beyond tail %d' % (w_seq, tail_seq)
        if w_seq == tail_seq:
            return 'QUARANTINE', 'uncertainTailLoss: equal seq, different body hash'
        return 'QUARANTINE', 'journal ahead of committed witness: protocol violation'
    # PENDING
    if w_seq == tail_seq + 1:
        return 'REVERT', 'append never became durable; witness -> COMMITTED %d' % tail_seq
    if w_seq == tail_seq:
        if w_sha == tail_sha:
            return 'ADVANCE', 'commit completed before the witness update; witness -> COMMITTED %d' % w_seq
        return 'QUARANTINE', 'pending seq equals tail with a different body hash'
    return 'QUARANTINE', 'pending witness inconsistent with tail (%d vs %d)' % (w_seq, tail_seq)


def verify_envelope(stored_bytes, env, root, expected_kind, publisher_namespace=None):
    try:
        if not isinstance(stored_bytes, bytes) or not isinstance(expected_kind, str) or expected_kind not in KIND_ROUTING or (publisher_namespace is not None and not _is_str(publisher_namespace, 4194304)):
            return 'RJ-4 ENVELOPE_MISMATCH', 'malformed verification context'
        return _verify_envelope_checked(stored_bytes, env, root, expected_kind, publisher_namespace)
    except Exception as e:
        return 'RJ-4 ENVELOPE_MISMATCH', 'boundary exception ' + type(e).__name__


def _verify_envelope_checked(stored_bytes, env, root, expected_kind, publisher_namespace=None):
    """Section 2.2 verification order. Returns (outcome, detail). root MUST be an AdmittedRoot (SEC3-M1):
    an unadmitted dictionary is refused before any step, so no caller can label a root admitted."""
    root, why = recheck_admitted_root(root)
    if root is None:
        return 'ROOT-NOT-ADMITTED', why
    # step 1: presence / structural
    if env is None:
        return 'RJ-4 UNSIGNED', 'no envelope'
    try:
        canonical_bytes(env)  # Full boundary: floats/NFD are forbidden even where JSON Schema const equates them.
        validate(env, load_schema('envelope'))
    except SchemaError as e:
        return 'RJ-4 UNSIGNED', 'malformed envelope: %s' % e
    s = env['subject']
    domain, role = KIND_ROUTING[s['kind']]
    if s['kind'] != expected_kind or s['domain'] != domain or env['role'] != role:
        return 'RJ-4 ENVELOPE_MISMATCH', 'kind/domain/role routing mismatch'
    # step 2
    if sha256_hex(stored_bytes) != s['storedSha256']:
        return 'RJ-4 DIGEST_MISMATCH', 'stored digest'
    # step 3
    try:
        obj = load_json_strict(stored_bytes)
        pre, _ = domain_digest(domain, obj)
    except Reject as e:
        return 'RJ-4 ENVELOPE_MISMATCH', 'canonicalization refused: %s' % e
    if pre != s['preimageSha256']:
        return 'RJ-4 ENVELOPE_MISMATCH', 'preimage recomputed %s != carried %s' % (pre[:12], s['preimageSha256'][:12])
    # namespace binding
    if publisher_namespace is not None and env['namespace'] != publisher_namespace:
        return 'RJ-4 ENVELOPE_MISMATCH', 'namespace %s != publisher %s' % (env['namespace'], publisher_namespace)
    # step 4
    msg = envelope_message_hex(env)
    authorized = root_keys_for_role(root, role, env['namespace'])
    valid = []
    for sig in env['signatures']:
        kid = sig['keyId']
        if kid not in authorized:
            continue
        if ed25519_verify(authorized[kid], msg, sig['signature']):
            valid.append(kid)
    if not valid:
        return 'RJ-4 ENVELOPE_MISMATCH', 'no valid signature from an authorized key'
    # step 5 (threshold is DR-112's; reported, not refused here)
    thr = role_threshold(root, role)
    return ('VERIFIED' if len(set(valid)) >= thr else 'THRESHOLD-SHORTFALL'), 'valid=%d threshold=%d' % (len(set(valid)), thr)


def root_keys_for_role(root, role, namespace):
    keys = {k['keyId']: k['publicKey'] for k in root['keys']}
    if role == 'ROOT':
        ids = root['rootKeys']
    else:
        rd = root['roles'].get(role)
        if not rd or namespace not in rd.get('namespaces', []):
            return {}
        ids = rd['keys']
    return {i: keys[i] for i in ids if i in keys}


def role_threshold(root, role):
    return root['rootThreshold'] if role == 'ROOT' else root['roles'][role]['threshold']


# --- minimal JSON-Schema-subset validator -------------------------------------------
class SchemaError(Exception):
    pass


_SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'security-schemas.v7')


def load_schema(name):
    return json.load(open(os.path.join(_SCHEMA_DIR, name + '.schema.json'), encoding='utf-8'))


def _resolve(ref, root):
    assert ref.startswith('#/'), ref
    node = root
    for part in ref[2:].split('/'):
        node = node[part]
    return node


def _typed_eq(a, b):
    """JSON-Schema equality: booleans are never equal to integers (Python's True == 1 is not)."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_typed_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_typed_eq(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b


def validate(inst, schema, root=None, path='$'):
    root = root if root is not None else schema
    if '$ref' in schema:
        return validate(inst, _resolve(schema['$ref'], root), root, path)
    if 'const' in schema and not _typed_eq(inst, schema['const']):
        raise SchemaError('%s: const %r' % (path, schema['const']))
    if 'enum' in schema and not any(_typed_eq(inst, e) for e in schema['enum']):
        raise SchemaError('%s: not in enum %r' % (path, inst))
    if 'oneOf' in schema:
        ok = 0
        errs = []
        for i, alt in enumerate(schema['oneOf']):
            try:
                validate(inst, alt, root, path); ok += 1
            except SchemaError as e:
                errs.append(str(e))
        if ok != 1:
            raise SchemaError('%s: oneOf matched %d (%s)' % (path, ok, '; '.join(errs)[:300]))
    if 'anyOf' in schema:
        for alt in schema['anyOf']:
            try:
                validate(inst, alt, root, path); break
            except SchemaError:
                continue
        else:
            raise SchemaError('%s: anyOf failed' % path)
    t = schema.get('type')
    if t is not None:
        types = t if isinstance(t, list) else [t]
        ok = False
        for tt in types:
            if tt == 'object' and isinstance(inst, dict): ok = True
            elif tt == 'array' and isinstance(inst, list): ok = True
            elif tt == 'string' and isinstance(inst, str): ok = True
            elif tt == 'integer' and isinstance(inst, int) and not isinstance(inst, bool): ok = True
            elif tt == 'boolean' and isinstance(inst, bool): ok = True
            elif tt == 'null' and inst is None: ok = True
        if not ok:
            raise SchemaError('%s: type %s' % (path, t))
    if 'type' not in schema and 'const' not in schema and 'enum' not in schema and isinstance(inst, bool) and schema.get('minimum') is not None:
        raise SchemaError('%s: boolean where a number is constrained' % path)
    if isinstance(inst, str):
        if 'pattern' in schema and not re.search(schema['pattern'], inst):
            raise SchemaError('%s: pattern %s' % (path, schema['pattern']))
        if 'maxLength' in schema and len(inst) > schema['maxLength']:
            raise SchemaError('%s: maxLength' % path)
        if 'minLength' in schema and len(inst) < schema['minLength']:
            raise SchemaError('%s: minLength' % path)
    if isinstance(inst, int) and not isinstance(inst, bool):
        if 'minimum' in schema and inst < schema['minimum']:
            raise SchemaError('%s: minimum' % path)
        if 'maximum' in schema and inst > schema['maximum']:
            raise SchemaError('%s: maximum' % path)
    if isinstance(inst, list):
        if 'minItems' in schema and len(inst) < schema['minItems']:
            raise SchemaError('%s: minItems' % path)
        if 'maxItems' in schema and len(inst) > schema['maxItems']:
            raise SchemaError('%s: maxItems' % path)
        if schema.get('uniqueItems') and len(set(json.dumps(x, sort_keys=True) for x in inst)) != len(inst):
            raise SchemaError('%s: uniqueItems' % path)
        if 'items' in schema:
            for i, x in enumerate(inst):
                validate(x, schema['items'], root, '%s[%d]' % (path, i))
    if isinstance(inst, dict):
        props = schema.get('properties', {})
        for r in schema.get('required', []):
            if r not in inst:
                raise SchemaError('%s: missing required %s' % (path, r))
        if schema.get('additionalProperties', True) is False:
            extra = [k for k in inst if k not in props]
            if extra:
                raise SchemaError('%s: additional properties %s' % (path, extra))
        for k, v in inst.items():
            if k in props:
                validate(v, props[k], root, path + '.' + k)
            elif 'additionalProperties' in schema and isinstance(schema['additionalProperties'], dict):
                validate(v, schema['additionalProperties'], root, path + '.' + k)
    return True


# --- grant journal ------------------------------------------------------------------
GRANT_JOURNAL_DDL = """
CREATE TABLE grant_journal (
  grantGeneration INTEGER NOT NULL,
  seq          INTEGER NOT NULL CHECK (seq >= 1 AND seq <= 9007199254740991),
  record_type  TEXT    NOT NULL CHECK (record_type IN
                 ('GRANT','NARROW','EXPIRY','RA','RCI','RCO','ICI','ICO','REV','CLN','AUD',
                  'CHECKPOINT','MIGRATION','TERMINAL')),
  operation_ref TEXT   NOT NULL CHECK (operation_ref GLOB 'op-[0-9a-f]*' AND length(operation_ref) = 35),
  request_ref  TEXT,
  token        TEXT,
  install_generation_id TEXT,
  manifest_digest TEXT CHECK (manifest_digest IS NULL OR length(manifest_digest) = 64),
  platform     TEXT CHECK (platform IS NULL OR platform IN ('macos-arm64','macos-x86_64','linux-x86_64','linux-arm64')),
  body         TEXT    NOT NULL,
  body_sha256  TEXT    NOT NULL CHECK (length(body_sha256) = 64),
  prev_sha256  TEXT    NOT NULL CHECK (length(prev_sha256) = 64),
  CHECK (record_type <> 'GRANT' OR (install_generation_id IS NOT NULL AND manifest_digest IS NOT NULL AND platform IS NOT NULL AND token IS NOT NULL)),
  PRIMARY KEY (grantGeneration, seq)
) WITHOUT ROWID;
CREATE TRIGGER gj_no_update BEFORE UPDATE ON grant_journal
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj_no_delete BEFORE DELETE ON grant_journal
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj_seq_contiguous BEFORE INSERT ON grant_journal
  BEGIN
    SELECT CASE WHEN NEW.seq <> (SELECT COALESCE(MAX(seq), 0) + 1 FROM grant_journal WHERE grantGeneration = NEW.grantGeneration)
      THEN RAISE(ABORT, 'grant journal sequence must be tail+1') END;
    SELECT CASE WHEN EXISTS (SELECT 1 FROM grant_journal WHERE grantGeneration = NEW.grantGeneration AND record_type = 'TERMINAL')
      THEN RAISE(ABORT, 'grant journal carrier is TERMINAL') END;
    SELECT CASE WHEN NEW.seq = 9007199254740991 AND NEW.record_type <> 'TERMINAL'
      THEN RAISE(ABORT, 'grant journal seq 9007199254740991 is the reserved terminal slot; roll the grant generation') END;
  END;
CREATE TABLE carrier_quarantine (
  grantGeneration INTEGER PRIMARY KEY,
  reason     TEXT NOT NULL CHECK (reason IN ('uncertainTailLoss','witnesslessRestore')),
  observed_tail_seq INTEGER,
  body       TEXT NOT NULL
);
CREATE TABLE carrier_capacity_pause (
  grantGeneration INTEGER PRIMARY KEY,
  proven_tail_seq INTEGER NOT NULL,
  reserved_terminal_slot INTEGER NOT NULL DEFAULT 1
);
"""


SEQ_MAX = 9007199254740991            # JSON uint53 cap; the last value is the reserved terminal slot


def project_key_digest(project_key):
    """Host-internal, disclosure-safe carrier identity: SHA-256 over the projectKey's UTF-8 bytes (no tag)."""
    return sha256_hex(project_key.encode('utf-8'))


LOCATOR_RE = re.compile(r'^gj:[0-9a-f]{64}:[1-9][0-9]{0,18}:[1-9][0-9]{0,15}$')
LOCATOR_MIN_BYTES, LOCATOR_MAX_BYTES = 71, 104


def locator(project_key, grant_generation, seq):
    """gj:<projectKeyDigest hex64>:<grantGeneration>:<seq>. HOST-INTERNAL ONLY (journal, audit, doctor);
    never a control-plane body member. projectKey bytes are never disclosed; fixed 71..104 bytes."""
    if not (1 <= grant_generation <= I64MAX and 1 <= seq <= SEQ_MAX):
        raise ValueError('locator counters out of range')
    loc = 'gj:%s:%d:%d' % (project_key_digest(project_key), grant_generation, seq)
    assert LOCATOR_RE.fullmatch(loc) and LOCATOR_MIN_BYTES <= len(loc.encode('ascii')) <= LOCATOR_MAX_BYTES
    return loc


def parse_locator(loc):
    """Host-side parse. Returns (projectKeyDigest, grantGeneration, seq) or None when not in the grammar."""
    if not isinstance(loc, str) or not LOCATOR_RE.fullmatch(loc):
        return None
    _, d, g, s = loc.split(':')
    g, s = int(g), int(s)
    if not (1 <= g <= I64MAX and 1 <= s <= SEQ_MAX):
        return None
    return d, g, s


HANDLE_RE = re.compile(r'^ah:[0-9a-f]{32}$')          # wire authorizationRef: opaque, per spawn
OPERATION_REF_RE = re.compile(r'^op-[0-9a-f]{32}$')   # wire operationRef: host-minted per operation
EFFECT_CLASSES = ('HE-1', 'HE-2')


def mint_handle(rng_bytes16):
    """ah:<32 lowercase hex> from 16 CSPRNG bytes supplied by the host at spawn."""
    if len(rng_bytes16) != 16:
        raise ValueError('handle entropy must be 16 bytes')
    return 'ah:' + rng_bytes16.hex()


EFFECT_UNDERLYING_TOKEN = {'HE-1': 'PT-FS-WRITE-HOST-STATE', 'HE-2': 'PT-FS-READ-PROJECT'}   # both grants required with PT-HOST-EFFECT-BROKERED
RESULT_REF_RE = re.compile(r'^rr:[0-9a-f]{32}:[0-9a-f]{64}:(0|[1-9][0-9]{0,7})$')
RESULT_BYTES_MAX_PER_RESULT = 16777216     # 16 MiB per result
RESULT_BYTES_MAX_PER_SPAWN = 67108864      # 64 MiB per spawn scratch directory


MEMBER_PATH_MAX_BYTES = 1024


def normalized_member_path(path):
    """A sealed-snapshot member path or policy path prefix: relative, NFC, '/'-separated, no empty, '.' or
    '..' segment, no backslash or NUL, at most 1024 UTF-8 bytes. True only for the exact normalized spelling."""
    if not isinstance(path, str) or not path or len(path.encode('utf-8')) > MEMBER_PATH_MAX_BYTES:
        return False
    if unicodedata.normalize('NFC', path) != path or '\\' in path or '\x00' in path or path.startswith('/'):
        return False
    return all(seg not in ('', '.', '..') for seg in path.split('/'))


PLATFORMS = ('macos-arm64', 'macos-x86_64', 'linux-x86_64', 'linux-arm64')
PERMISSION_TOKENS = ('PT-FS-READ-PROJECT', 'PT-FS-READ-COMPONENT', 'PT-FS-WRITE-HOST-STATE', 'PT-PROC-EXEC-DECLARED', 'PT-NET-EGRESS', 'PT-ENV-READ', 'PT-HOST-EFFECT-BROKERED')
_UUID_RE = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
_HEX64_RE = re.compile(r'[0-9a-f]{64}')
BINDING_KEYS = ('installGenerationId', 'manifestDigest', 'platform', 'stableId')


def _is_hex64(v): return isinstance(v, str) and _HEX64_RE.fullmatch(v) is not None
def _is_str(v, mx): return isinstance(v, str) and 1 <= len(v.encode('utf-8')) <= mx and unicodedata.normalize('NFC', v) == v


def valid_binding(b):
    """Closed identity binding: exactly the four members, each strictly typed and non-empty (SEC3-M4 corrective:
    an empty or partial binding never compares equal to anything)."""
    return (isinstance(b, dict) and set(b) == set(BINDING_KEYS) and _is_str(b['installGenerationId'], 128)
            and _is_hex64(b['manifestDigest']) and b['platform'] in PLATFORMS and isinstance(b['stableId'], str) and _UUID_RE.fullmatch(b['stableId']) is not None)


def valid_snapshot_members(m):
    """A sealed snapshot manifest member set: a list/tuple/set of normalized member-path strings, no duplicates,
    validated element by element BEFORE any set is built (the protocol author's [{}] probe)."""
    if not isinstance(m, (list, tuple, set, frozenset)):
        return False
    items = list(m)
    if len(items)>100000: return False
    if not all(isinstance(x, str) and normalized_member_path(x) for x in items):
        return False
    return len(set(items)) == len(items)


def valid_target_shape(ec, t):
    if not isinstance(t,dict): return False
    if ec == 'HE-2':
        return set(t)=={'snapshotDigest','memberPath'} and _is_hex64(t['snapshotDigest']) and _is_str(t['memberPath'],1024)
    if ec == 'HE-1':
        return set(t)=={'stateClass','byteCap'} and t['stateClass'] in ('SC-CACHE','SC-OPS') and _strict_int(t['byteCap'],0,2**63-1)
    return False


def valid_connection_entry(e):
    return (isinstance(e, dict) and {'operationRef', 'effectClass', 'brokerLocator', 'underlyingLocator', 'grantGeneration', 'seq', 'binding', 'target'} == set(e)
            and isinstance(e['operationRef'], str) and OPERATION_REF_RE.fullmatch(e['operationRef']) is not None and e['effectClass'] in EFFECT_CLASSES
            and isinstance(e['brokerLocator'], str) and isinstance(e['underlyingLocator'], str) and _strict_int(e['grantGeneration'], 1, I64MAX) and _strict_int(e['seq'], 1, SEQ_MAX)
            and valid_binding(e['binding']) and valid_target_shape(e['effectClass'],e['target']))


def valid_grant_scope(scope):
    # A closed host projection. snapshotDigest binds the operation snapshot and
    # is attached by the host; it is NOT an extra member of a journal GRANT body.
    if not isinstance(scope, dict) or set(scope) - {'pathPrefixes', 'variables', 'programs', 'endpoints', 'stateClass', 'snapshotDigest'}:
        return False
    for name, (count, bound) in {'pathPrefixes': (256,1024), 'variables': (256,256), 'programs': (64,1024), 'endpoints': (64,512)}.items():
        if name in scope:
            v = scope[name]
            if not isinstance(v,list) or len(v)>count or not all(_is_str(x,bound) for x in v) or len(set(v)) != len(v):
                return False
            if name == 'pathPrefixes' and not all(normalized_member_path(x) for x in v):
                return False
    return (('stateClass' not in scope or scope['stateClass'] in ('SC-CACHE','SC-OPS'))
            and ('snapshotDigest' not in scope or _is_hex64(scope['snapshotDigest'])))


def valid_grant_state(g):
    return (isinstance(g, dict) and set(g) == {'status','token','binding','scope'}
            and g['status'] in ('GRANT', 'REVOKED', 'CLOSED') and g['token'] in PERMISSION_TOKENS
            and valid_binding(g['binding']) and valid_grant_scope(g['scope']))


def valid_stat(st, kind):
    """A closed stat record. Directory: type, uid and mode required (mode 0..0o7777; compared as exactly 0700
    later). File: type, nlink, uid and size required. Every present integer member is a strict non-negative
    integer (never a boolean); unknown members refuse."""
    if not isinstance(st, dict) or st.get('type') not in ('regular', 'directory', 'symlink', 'fifo', 'socket', 'device', 'other'):
        return False
    if set(st) - {'type', 'nlink', 'uid', 'size', 'mode'}:
        return False
    need = ('uid', 'mode') if kind == 'directory' else ('nlink', 'uid', 'size')
    if any(k not in st for k in need):
        return False
    for k in ('nlink', 'uid', 'size'):
        if k in st and not _strict_int(st[k], 0, 2 ** 63 - 1):
            return False
    if 'mode' in st and not _strict_int(st['mode'], 0, 0o7777):
        return False
    return True


def valid_effect_result(er):
    required = {'requestSeq','decisionSeq','outcomeSeq','commitClass','effectOutcome'}
    return (isinstance(er, dict) and required <= set(er) <= required | {'resultRef'}
            and er['effectOutcome'] in ('COMPLETED','FAILED','INDETERMINATE')
            and er['commitClass'] in ('REVERSIBLE','IRREVERSIBLE')
            and all(_strict_int(er[k],1,SEQ_MAX) for k in ('requestSeq','decisionSeq','outcomeSeq'))
            and ('resultRef' not in er or _is_str(er['resultRef'],1024)))


REQUEST_CONTEXT_KEYS = ('connectionMap', 'currentBinding', 'journalState', 'snapshotMembers')


def verify_effect_request(body, ctx):
    """Section 7.4 ENFORCING BOUNDARY (SEC3-M4 corrective). ctx is one required record
    {connectionMap, currentBinding, journalState, snapshotMembers}. Order: absent member -> CONTEXT_ABSENT;
    malformed member (wrong type, empty or partial binding, non-string or non-normalized snapshot member,
    malformed map entry or grant record) -> CONTEXT_MALFORMED; then the request rules. Any exception inside
    the boundary is CONTEXT_MALFORMED, never an uncaught error. Returns None (proceed to RA) or an RF-6 reason."""
    try:
        return _verify_effect_request_checked(body, ctx)
    except Exception as e:
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:exception ' + type(e).__name__


def _verify_effect_request_checked(body, ctx):
    if not isinstance(ctx, dict) or any(k not in ctx or ctx[k] is None for k in REQUEST_CONTEXT_KEYS):
        return 'RF-6:AUTHORIZATION.CONTEXT_ABSENT'
    if set(ctx) != set(REQUEST_CONTEXT_KEYS):
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:unknown member'
    connection_map, current_binding, journal_state, snapshot_members = (ctx[k] for k in REQUEST_CONTEXT_KEYS)
    if not (isinstance(connection_map, dict) and isinstance(journal_state, dict) and isinstance(body, dict)):
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED'
    if set(body) != {'effectClass','authorizationRef','operationRef'}:
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:request shape'
    if not valid_binding(current_binding):
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:currentBinding'
    if not valid_snapshot_members(snapshot_members):
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:snapshotMembers'
    snapshot_members = set(snapshot_members)
    if len(connection_map) > 4 or not all(isinstance(k, str) and HANDLE_RE.fullmatch(k) and valid_connection_entry(v) for k, v in connection_map.items()):
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:connectionMap'
    if not all(isinstance(k, str) and parse_locator(k) is not None and valid_grant_state(v) for k, v in journal_state.items()):
        return 'RF-6:AUTHORIZATION.CONTEXT_MALFORMED:journalState'
    ar, opr, ec = body.get('authorizationRef'), body.get('operationRef'), body.get('effectClass')
    if not isinstance(ar, str) or not HANDLE_RE.fullmatch(ar):
        return 'RF-6:AUTHORIZATION.HANDLE_GRAMMAR'
    if not isinstance(opr, str) or not OPERATION_REF_RE.fullmatch(opr):
        return 'RF-6:AUTHORIZATION.OPERATION_REF_GRAMMAR'
    entry = connection_map.get(ar)
    if entry is None:
        return 'RF-6:AUTHORIZATION.UNKNOWN_HANDLE'
    if entry['operationRef'] != opr:
        return 'RF-6:AUTHORIZATION.OPERATION_MISMATCH'
    if ec not in EFFECT_CLASSES or entry['effectClass'] != ec:
        return 'RF-6:AUTHORIZATION.EFFECT_CLASS_MISMATCH'
    if entry['binding'] != current_binding:
        return 'RF-6:AUTHORIZATION.BINDING_DRIFT'
    grants = {}
    for which, want_token in (('brokerLocator', 'PT-HOST-EFFECT-BROKERED'), ('underlyingLocator', EFFECT_UNDERLYING_TOKEN[ec])):
        loc = entry.get(which)
        parsed = parse_locator(loc)
        if parsed is None or parsed[1] != entry['grantGeneration']:
            return 'RF-6:AUTHORIZATION.LOCATOR_INTEGRITY'
        grant = journal_state.get(loc)
        if grant is None or grant['status'] != 'GRANT':
            return 'RF-6:AUTHORIZATION.GRANT_NOT_CURRENT'
        if grant['token'] != want_token:
            return 'RF-6:AUTHORIZATION.TOKEN_MISMATCH'
        if grant['binding'] != current_binding:
            return 'RF-6:AUTHORIZATION.GRANT_BINDING_MISMATCH'
        grants[which] = grant
    for which in ('brokerLocator', 'underlyingLocator'):
        scope = grants[which]['scope']
        if not scope:
            return 'RF-6:AUTHORIZATION.GRANT_SCOPE_EMPTY'
        ok, why = _target_within_scope(ec, entry['target'], scope, snapshot_members)
        if not ok:
            return 'RF-6:AUTHORIZATION.' + why
    return None


def _target_within_scope(effect_class, target, scope, snapshot_members):
    """Pure helper, NOT the enforcing boundary (call verify_effect_request). Returns (bool, reason).
    HE-2 order: (1) normalized member path, (2) the grant scope names the sealed snapshot and the target
    names the same one, (3) exact membership in that snapshot's manifest, (4) whole-segment prefix
    containment. HE-1: state class equal and 0 < byteCap <= per-result cap."""
    if not valid_grant_scope(scope):
        return False, 'SCOPE_MALFORMED'
    if not isinstance(target, dict):
        return False, 'TARGET_ABSENT'
    if effect_class == 'HE-2':
        if set(target) != {'snapshotDigest','memberPath'}:
            return False, 'TARGET_MALFORMED'
        path = target.get('memberPath')
        if not normalized_member_path(path):
            return False, 'TARGET_PATH_NOT_NORMALIZED'
        sd = scope.get('snapshotDigest')
        if not (isinstance(sd, str) and re.fullmatch(r'[0-9a-f]{64}', sd)) or target.get('snapshotDigest') != sd:
            return False, 'SNAPSHOT_BINDING_MISSING_OR_MISMATCH'
        if path not in snapshot_members:
            return False, 'TARGET_NOT_SEALED_MEMBER'
        prefixes = [p for p in scope.get('pathPrefixes', []) if normalized_member_path(p)]
        if not prefixes or not _prefix_within(path, prefixes):
            return False, 'TARGET_OUTSIDE_SCOPE'
        return True, ''
    if effect_class == 'HE-1':
        if set(target) != {'stateClass','byteCap'}:
            return False, 'TARGET_MALFORMED'
        if target.get('stateClass') is None or target.get('stateClass') != scope.get('stateClass'):
            return False, 'TARGET_OUTSIDE_SCOPE'
        if not _strict_int(target.get('byteCap'), 1, RESULT_BYTES_MAX_PER_RESULT):
            return False, 'TARGET_OUTSIDE_SCOPE'
        return True, ''
    return False, 'EFFECT_CLASS_UNKNOWN'


# ---- Section 7.5 scratch lifecycle: stage-file admission (HE-1) and result resolution (HE-2) -------
def stage_file_admission(st, host_uid, byte_cap):
    try:
        if not valid_stat(st, 'file') or not _strict_int(host_uid,0,2**31-1) or not _strict_int(byte_cap,1,RESULT_BYTES_MAX_PER_RESULT):
            return 'STAGE.CONTEXT_MALFORMED'
        return _stage_file_admission_checked(st,host_uid,byte_cap)
    except Exception:
        return 'STAGE.CONTEXT_MALFORMED'


def _stage_file_admission_checked(st, host_uid, byte_cap):
    """Host-side admission of <resultScratchRoot>/stage/<handle hex>.bin opened with
    openat(heldScratchFd, ..., O_RDONLY|O_NOFOLLOW|O_CLOEXEC). st = {'type', 'nlink', 'uid', 'size'}.
    Returns None (admit) or the FAILED reason. The bytes are then read ONCE from that fd into a buffer of
    exactly st.size (bounded before allocation) and digested; the ordered HE-1 algorithm (HE1_ORDER) then
    records durable RA and intent before any commit from that buffer; the stage file is consumed after the
    outcome record and the handle is single-use for HE-1."""
    if st.get('type') != 'regular':
        return 'STAGE.NOT_REGULAR'
    if st.get('nlink', 0) != 1:
        return 'STAGE.HARD_LINKED'
    if st.get('uid') != host_uid:
        return 'STAGE.WRONG_OWNER'
    if not _strict_int(st.get('size'), 0, byte_cap):
        return 'STAGE.OVER_CAP'
    return None


def make_result_ref(result_id16, data):
    """Section 7.5 self-authenticating result reference carried in effectResult.resultRef (<= 108 bytes):
    rr:<resultId 32 hex>:<sha256 of the bytes>:<byte length>. The bytes live at <resultScratchRoot>/<resultId>.bin."""
    if len(result_id16) != 16 or len(data) > RESULT_BYTES_MAX_PER_RESULT:
        raise ValueError('result id or size out of bounds')
    return 'rr:%s:%s:%d' % (result_id16.hex(), sha256_hex(data), len(data))


RESULT_CONTEXT_KEYS = ('effectResult', 'expectedRequestSeq', 'scratchDirSt', 'selfUid', 'fileSt', 'spawnBytesSoFar')


def resolve_result(result_ref, read_scratch, ctx):
    """SDK-side ENFORCING BOUNDARY (SEC3-M4 corrective). ctx is one required record with every member of
    RESULT_CONTEXT_KEYS present (CONTEXT_ABSENT otherwise) and of closed shape and strict type
    (CONTEXT_MALFORMED otherwise: requestSeq and expectedRequestSeq are integers 1..2^53-1, never strings or
    booleans; stat records are typed; the scratch directory mode must be exactly 0700). Any exception inside
    the boundary is CONTEXT_MALFORMED. Returns ('OK', bytes) or ('RESULT.<reason>', None)."""
    try:
        return _resolve_result_checked(result_ref, read_scratch, ctx)
    except Exception as e:
        return 'RESULT.CONTEXT_MALFORMED:exception ' + type(e).__name__, None


def _resolve_result_checked(result_ref, read_scratch, ctx):
    if not isinstance(ctx, dict) or any(k not in ctx or ctx[k] is None for k in RESULT_CONTEXT_KEYS):
        return 'RESULT.CONTEXT_ABSENT', None
    if set(ctx) != set(RESULT_CONTEXT_KEYS) or not callable(read_scratch):
        return 'RESULT.CONTEXT_MALFORMED:context', None
    er, want_seq, dst, uid, fst, so_far = (ctx[k] for k in RESULT_CONTEXT_KEYS)
    if not valid_effect_result(er):
        return 'RESULT.CONTEXT_MALFORMED:effectResult', None
    if not _strict_int(want_seq, 1, SEQ_MAX):
        return 'RESULT.CONTEXT_MALFORMED:expectedRequestSeq', None
    if not valid_stat(dst, 'directory') or not valid_stat(fst, 'file') or not _strict_int(uid, 0, 2 ** 31 - 1) or not _strict_int(so_far, 0, RESULT_BYTES_MAX_PER_SPAWN):
        return 'RESULT.CONTEXT_MALFORMED:stat', None
    if er['effectOutcome'] != 'COMPLETED':
        return 'RESULT.EFFECT_NOT_COMPLETED', None
    if er['requestSeq'] != want_seq:
        return 'RESULT.REQUEST_SEQ_MISMATCH', None
    if er.get('resultRef') != result_ref:
        return 'RESULT.REF_NOT_FROM_RESULT', None
    if dst['type'] != 'directory' or dst['uid'] != uid or (dst['mode'] & 0o7777) != 0o700:
        return 'RESULT.SCRATCH_NOT_OWNED', None
    if not isinstance(result_ref, str) or not RESULT_REF_RE.fullmatch(result_ref):
        return 'RESULT.REF_GRAMMAR', None
    _, rid, digest, length = result_ref.split(':')
    length = int(length)
    if length > RESULT_BYTES_MAX_PER_RESULT:
        return 'RESULT.OVER_CAP', None
    if so_far + length > RESULT_BYTES_MAX_PER_SPAWN:
        return 'RESULT.SPAWN_CAP_EXCEEDED', None
    if fst['type'] != 'regular' or fst['nlink'] != 1 or fst['uid'] != uid or fst['size'] != length:
        return 'RESULT.FILE_NOT_ADMITTED', None
    data = read_scratch(rid)
    if data is None:
        return 'RESULT.ABSENT', None
    if not isinstance(data, (bytes, bytearray)) or len(data) != length or sha256_hex(bytes(data)) != digest:
        return 'RESULT.INTEGRITY', None
    return 'OK', bytes(data)


# ---- SEC3-M5 (corrective): HE-1 ordered algorithm, lawful journal vocabulary, REV, recovery -----------
HE1_ORDER = {'REVERSIBLE': ('RA', 'RCI', 'EFFECT', 'RCO', 'UNLINK-STAGE', 'RESULT'),
             'IRREVERSIBLE': ('RA', 'ICI', 'EFFECT', 'ICO', 'UNLINK-STAGE', 'RESULT')}
JOURNAL_OUTCOMES = {'RCO': ('COMPLETED', 'FAILED'), 'ICO': ('COMPLETED', 'FAILED', 'INDETERMINATE')}   # exactly the closed journal-record schema
CLN_RESIDUAL_DISPOSITIONS = ('not-begun', 'reverted', 'completed-irreversible', 'indeterminate')
_RECOVERY_RECORDS = ('RA', 'RCI', 'ICI', 'RCO', 'ICO', 'REV')


def he1_recover(commit_class, durable_records, footprint):
    try:
        return _he1_recover_checked(commit_class,durable_records,footprint)
    except Exception:
        return 'QUARANTINE', None, 'INVALID-INPUT'


def _he1_recover_checked(commit_class, durable_records, footprint):
    """Recovery after a crash during HE-1 (SEC3-M5 corrective). Inputs are validated first: commit_class in
    HE1_ORDER; durable_records a list of journal record types for this request in journal order; footprint
    in present|absent|unknown for the committed object. Returns (action, record, reported) where record is
    None, ('RCO'|'ICO', <outcome in JOURNAL_OUTCOMES>) or ('CLN', '<requestRef>:<disposition>') and action is:
      QUARANTINE      the record sequence violates the lawful order (an intent without RA, an outcome without
                      its intent, a record after REV other than CLN, a duplicate): the carrier is quarantined
                      under the existing reason uncertainTailLoss; nothing is appended and nothing is inferred
      NOTHING         nothing to recover (no RA, or the outcome is already recorded)
      APPEND          append the given lawful record
      INVERSE-FIRST   REVERSIBLE intent with the effect footprint present: execute the recorded inverseRef,
                      then re-run recovery with the new footprint (a revert is proven by the footprint, never
                      by the missing outcome record)
      RETRY-LATER     the footprint cannot be determined for a reversible effect: no record is appended, no
                      outcome is claimed; the operation reports HOST.IO_FAILURE and recovery runs again
    Only COMPLETED/FAILED (RCO) and COMPLETED/FAILED/INDETERMINATE (ICO) are ever emitted. After REV the
    in-flight request is closed through the CLN residual string, never through a post-REV RCO/ICO."""
    if not isinstance(commit_class,str) or commit_class not in HE1_ORDER or not isinstance(footprint,str) or footprint not in ('present', 'absent', 'unknown'):
        return 'QUARANTINE', None, 'INVALID-INPUT'
    if not isinstance(durable_records, (list, tuple)) or not all(isinstance(r,str) and r in _RECOVERY_RECORDS for r in durable_records):
        return 'QUARANTINE', None, 'INVALID-RECORD'
    recs = list(durable_records)
    intent, outcome = ('RCI', 'RCO') if commit_class == 'REVERSIBLE' else ('ICI', 'ICO')
    wrong_intent, wrong_outcome = ('ICI', 'ICO') if commit_class == 'REVERSIBLE' else ('RCI', 'RCO')
    # lawful order for one request: RA? intent? outcome? with REV allowed only after RA and nothing after REV
    if len(set(recs)) != len(recs) or wrong_intent in recs or wrong_outcome in recs:
        return 'QUARANTINE', None, 'INVALID-ORDER'
    lawful_prefixes = [[], ['RA'], ['RA', intent], ['RA', intent, outcome], ['RA', 'REV'], ['RA', intent, 'REV'], ['RA', intent, outcome, 'REV']]
    if recs not in lawful_prefixes:
        return 'QUARANTINE', None, 'INVALID-ORDER'
    if 'RA' not in recs:
        return 'NOTHING', None, 'NOT-ACCEPTED'
    revoked = 'REV' in recs
    if outcome in recs:
        return 'NOTHING', None, 'ALREADY-RECORDED'
    if intent not in recs:                                   # accepted, never begun
        return ('APPEND', ('CLN', 'not-begun'), 'FAILED') if revoked else ('REVOKE-FIRST', ('REV', 'process-death'), 'PENDING')
    if commit_class == 'REVERSIBLE':
        if footprint == 'present':
            return 'INVERSE-FIRST', None, 'PENDING'
        if footprint == 'absent':
            return ('APPEND', ('CLN', 'reverted'), 'FAILED') if revoked else ('APPEND', ('RCO', 'FAILED'), 'FAILED')
        return 'RETRY-LATER', None, 'HOST.IO_FAILURE'
    # IRREVERSIBLE: the durable footprint decides; INDETERMINATE is a lawful ICO outcome
    if footprint == 'present':
        return ('APPEND', ('CLN', 'completed-irreversible'), 'COMPLETED') if revoked else ('APPEND', ('ICO', 'COMPLETED'), 'COMPLETED')
    if footprint == 'absent':
        return ('APPEND', ('CLN', 'not-begun'), 'FAILED') if revoked else ('APPEND', ('ICO', 'FAILED'), 'FAILED')
    return ('APPEND', ('CLN', 'indeterminate'), 'INDETERMINATE') if revoked else ('APPEND', ('ICO', 'INDETERMINATE'), 'INDETERMINATE')


def cln_residual(request_ref, disposition):
    """The CLN residuals[] entry (closed schema: strings <= 256 bytes) closing an in-flight request after REV."""
    if disposition not in CLN_RESIDUAL_DISPOSITIONS or not _is_str(request_ref, 64):
        raise ValueError('residual')
    return '%s:%s' % (request_ref, disposition)


def receipt_id(project_key_digest, grant_generation, outcome_seq):
    """The 32-hex commit id of an HE-1 receipt, derived from the OUTCOME record's position (RCO or ICO), so the
    receipt is tied to that record without adding any member to the closed journal shapes."""
    if not (_is_hex64(project_key_digest) and _strict_int(grant_generation, 1, I64MAX) and _strict_int(outcome_seq, 1, SEQ_MAX)):
        raise ValueError('receipt id inputs')
    return sha256_hex(b'opensip.journal.receipt.1' + b'\x00' + project_key_digest.encode() + b'\x00' + str(grant_generation).encode() + b'\x00' + str(outcome_seq).encode())[:32]


GRANT_GENERATION_MAX = I64MAX        # string-encoded in the locator, so the full signed-i64 range is representable


def genesis_prev(project_key, grant_generation):
    return sha256_hex(b'opensip.journal.genesis.1' + b'\x00' + project_key.encode('utf-8') + b'\x00' + str(grant_generation).encode('ascii'))


def record_body_sha(body):
    d, _ = domain_digest(DOMAIN_TAGS['journal'], body)
    return d


# ---- Section 5.6 durability primitives and I/O failure classes (WA-9) ------------------------------
DURABILITY_PRIMITIVE = {
    'macos': {'file': 'fcntl(F_FULLFSYNC)', 'directory': 'fcntl(F_FULLFSYNC) on the directory fd, fsync(2) if refused',
              'sqlite': 'PRAGMA synchronous=FULL; PRAGMA fullfsync=ON; PRAGMA checkpoint_fullfsync=ON'},
    'linux': {'file': 'fsync(2)', 'directory': 'fsync(2) on the directory fd',
              'sqlite': 'PRAGMA synchronous=FULL'},
}
DURABILITY_BOUNDARIES = ('witness-write', 'evalHighWater-write', 'journal-append', 'quarantine-marker',
                         'sc-trust-high-water-copy', 'lifecycle-publication', 'selection-commit')
IO_FAILURE_CLASSES = {
    'ENOSPC': 'IO.NO_SPACE', 'EDQUOT': 'IO.NO_SPACE', 'EIO': 'IO.DEVICE_ERROR', 'EROFS': 'IO.READ_ONLY',
    'SHORT_WRITE': 'IO.SHORT_WRITE', 'RENAME_FAILED': 'IO.DURABILITY_FAILED',
    'FSYNC_FAILED': 'IO.DURABILITY_UNDETERMINED', 'COMMIT_FAILED': 'IO.DURABILITY_UNDETERMINED',
}
PRE_VISIBILITY = ('ENOSPC', 'EDQUOT', 'EIO', 'EROFS', 'SHORT_WRITE', 'RENAME_FAILED')   # fail before the new state is visible


def io_failure_disposition(boundary, errclass):
    """Every durability boundary fails closed with a typed refusal. Errors before visibility (write to the temp
    file, the rename itself) leave the previous durable state in place. A failed fsync or SQLite commit may
    FOLLOW a visible rename or commit, so durability is UNDETERMINED: the writer refuses every further effect
    of the operation, reopens the carrier, reconciles the exact state (witness reconciliation, tail re-read)
    and only then decides; it never assumes either the old or the new state. D9: operational-failed / 4 /
    HOST.IO_FAILURE."""
    if boundary not in DURABILITY_BOUNDARIES or errclass not in IO_FAILURE_CLASSES:
        raise ValueError('unknown boundary or error class')
    pre = errclass in PRE_VISIBILITY
    return {'refusal': IO_FAILURE_CLASSES[errclass],
            'partialState': 'none (previous durable state retained)' if pre else 'UNDETERMINED (a visible rename or commit may precede the failed sync); refuse further effects, reopen and reconcile the exact state before any use',
            'reconcile': None if pre else ('reconcile_witness on reopen' if boundary in ('witness-write', 'journal-append') else 're-read the carrier after reopen; treat a readable, self-consistent new state as the state and re-sync it'),
            'd9': {'class': 'operational-failed', 'exit': 4, 'code': 'HOST.IO_FAILURE'},
            'retryable': errclass in ('ENOSPC', 'EDQUOT')}


# ---- Section 4.8 doctor report-only evaluation (WA-5) ----------------------------------------------
EXPIRY_BOUNDARY = {'catalogExpiresAt': 'expired iff tEval >= expiresAt', 'rootExpiresAt': 'expired iff tEval >= expiresAt',
                   'revocationFreshUntil': 'stale iff tEval > freshUntil (age exactly 90 d is fresh; 90 d + 1 s is stale)'}


def evaluation_time(recorded, wall_clock):
    """Section 4.2 evaluation instant for report-only and decision evaluation alike:
    max(recorded evalHighWater, wall clock, last accepted document time). The raw wall clock is kept separately."""
    cands = [c for c in (recorded.get('evalHighWater'), wall_clock, recorded.get('lastAccepted')) if c is not None]
    return max(cands)


def doctor_trust_report(recorded, wall_clock):
    """Non-persisting evaluation. recorded = {'evalHighWater': str|None, 'lastAccepted': str|None,
    'catalogExpiresAt': str, 'rootExpiresAt': str, 'revocationFreshUntil': str}. Never writes; labels itself;
    evaluates at evaluation_time; a raw clock below the recorded high-water is a finding, not a silent pass."""
    t = evaluation_time(recorded, wall_clock)
    out = {'evaluationMode': 'report-only', 'rawWallClock': wall_clock, 'evaluationTime': t,
           'recordedEvalHighWater': recorded.get('evalHighWater'), 'lastAccepted': recorded.get('lastAccepted'), 'boundaries': EXPIRY_BOUNDARY, 'findings': []}
    hw = recorded.get('evalHighWater')
    if hw is not None and wall_clock < hw:
        out['findings'].append({'check': 'clock', 'status': 'CLOCK-REGRESSION', 'wouldRefuse': True})
    for k in ('catalogExpiresAt', 'rootExpiresAt'):
        if k in recorded:
            bad = t >= recorded[k]
            out['findings'].append({'check': k, 'status': 'EXPIRED' if bad else 'VALID', 'wouldRefuse': bad})
    if 'revocationFreshUntil' in recorded:
        bad = t > recorded['revocationFreshUntil']
        out['findings'].append({'check': 'revocationFreshUntil', 'status': 'STALE-REVOCATION' if bad else 'FRESH', 'wouldRefuse': bad})
    out['writes'] = []
    return out


# ---- Section 8.8 observed-event admission (G22 hostile events; G07 loader crosswalk) --------------
NT_TCB = ('NT-TCB-IDENTITY', 'NT-TCB-UNDECLARED', 'NT-TCB-ALT-LOADER', 'NT-TCB-ENV-INFLUENCE', 'NT-TCB-TRACE-MISSING', 'NT-TCB-BOOT', 'NT-TCB-PROFILE-UNQUALIFIED')


def admit_observed_events(profile, observed):
    """Pure admission over a retained observation: profile = a validated tcb-profile-template; observed =
    {'trace': None | {'complete': bool, 'images': [{'class', 'origin', 'identity'}]}, 'environment': {name: value},
     'osAbi': {'predicate': 'pass'|'fail'|'undetermined'}}. Returns the sorted refusal list ([] = admitted).
    Missing or partial traces refuse: no profile match is ever asserted without a complete observation."""
    r = set()
    declared = {e['class']: e for e in profile['signedEntries']}
    inapplicable = {pf['class'] for pf in profile['inapplicabilityProofs']}
    trace = observed.get('trace')
    if not trace or not trace.get('complete'):
        r.add('NT-TCB-TRACE-MISSING')
    if observed.get('osAbi', {}).get('predicate') != 'pass':
        r.add('NT-TCB-BOOT')
    for e in profile['signedEntries']:
        for var, rule in e['originSearchPolicy']['environmentInfluence'].items():
            if rule['standing'] == 'FORBIDDEN' and var in observed.get('environment', {}):
                r.add('NT-TCB-ENV-INFLUENCE')
    seen = set()
    for img in (trace or {}).get('images', []):
        cls = img['class']; seen.add(cls)
        if cls == 'OS ABI':
            continue
        if cls in inapplicable or cls not in declared:
            r.add('NT-TCB-UNDECLARED'); continue
        d = declared[cls]
        allowed = d['originSearchPolicy']['allowedLoaderOrSearchOrder']
        if allowed and img.get('origin') not in allowed:
            r.add('NT-TCB-ALT-LOADER')
        want = d['identityEvidence']['value']
        want_id = want['authenticityCore']['payload'] if d['identityEvidence']['tag'] == 'PLATFORM-ATTESTED' else {'digest': want['digest']}
        got = img.get('identity', {})
        for k, v in want_id.items():
            if isinstance(v, dict) and '$releaseMeasured' in v:
                r.add('NT-TCB-PROFILE-UNQUALIFIED'); continue   # an unmeasured member can never admit: the template is not a qualified profile
            if got.get(k) != v:
                r.add('NT-TCB-IDENTITY')
    if trace and trace.get('complete'):
        for cls, d in declared.items():
            if cls != 'OS ABI' and cls not in seen and d['originSearchPolicy']['volumeConstraint']['tag'] == 'EXTERNAL-ORIGIN':
                r.add('NT-TCB-IDENTITY')     # a declared external member that never loaded: the observed process is not the profiled one
    return sorted(r)


G07_LOADER_CROSSWALK = {
    'G07.loader.path-substitution': 'NT-TCB-ENV-INFLUENCE (PATH forbidden) / NT-TCB-ALT-LOADER (origin outside allowedLoaderOrSearchOrder)',
    'G07.loader.loader-replacement': 'NT-TCB-IDENTITY (loader member identity differs) or NT-TCB-ALT-LOADER',
    'G07.loader.shell-substitution': 'no shell is ever spawned (child-process-only execution with fixed argv; FC-C1); a shell image in the trace is NT-TCB-UNDECLARED',
    'G07.loader.live-project-substitution': 'components execute from the immutable generation directory, never from the project; a project-origin image is NT-TCB-ALT-LOADER',
    'G07.loader.system-runtime-substitution': 'NT-TCB-IDENTITY for libc/framework members; NT-TCB-UNDECLARED for an unprofiled system class',
    'G07.loader.install-time-substitution': 'open-then-verify on the opened fd against the signed inventory before exec (digest mismatch refuses before any trace exists)',
    'G07.loader.entrypoint-replacement': 'the entrypoint is a signed inventory member verified on its opened fd; Linux executes that fd (fexecve); macOS executes the canonical absolute path inside the immutable generation directory under the held generation lease with fstat(fd) dev/ino equal to stat(path) immediately before posix_spawn and the loaded text image vnode (libproc PROC_PIDREGIONPATHINFO on the child) equal to the verified dev/ino before hello, or the child is killed (execve of /dev/fd/N fails with EACCES on macOS: measured by the lead)',
}
G07_TOCTOU_CROSSWALK = {
    'G07.toctou.extract': 'extract into a fresh directory under the per-user operational root, verify every member on its opened fd, then rename the directory into the generation slot; nothing under a live path is ever verified in place',
    'G07.toctou.canonicalize': 'openat chains with O_NOFOLLOW from a pinned root fd; no string canonicalization is trusted after the open',
    'G07.toctou.verify-to-spawn': 'Linux: the verified fd is executed (fexecve), no path re-resolution. macOS: scoped guarantee, not an fd exec: the generation directory is immutable and the host mutates nothing under the held generation lease; the exec path is canonical and absolute inside the per-user 0700 root; fstat(verified fd) dev/ino equals stat(path) immediately before posix_spawn and the child text image vnode equals it after spawn (killed before hello otherwise); the residual window can be raced only by same-UID code, which is inside the explicitly trusted first-party boundary',
    'G07.toctou.concurrent-update-remove': 'generation directories are immutable after publication; removal only by the fence-held GC census that skips any generation a live lease names',
    'G07.toctou.directory-inode-swap': 'the root fd is pinned at operation start and fstat device/inode/birth are compared after every step; a difference refuses (the lead\'s project-root identity rule)',
}


# ---- Section 6.11 effective permission policy (lock permissionPolicyDigest identifies both source files) ----
def _prefix_within(child, parents):
    """Whole-segment containment over ALREADY-NORMALIZED prefixes (SEC3-M2): the caller refuses any
    non-normalized member before this comparison is reached."""
    cs = child.split('/')
    return any(cs[:len(p.split('/'))] == p.split('/') for p in parents)


def admit_policy_paths(doc):
    """SEC3-M2 source admission: every pathPrefixes member of every grant must be a normalized member path."""
    bad = []
    for g in doc.get('grants', []):
        for pth in g.get('scope', {}).get('pathPrefixes', []):
            if not normalized_member_path(pth):
                bad.append('POLICY.PATH_PREFIX_NOT_NORMALIZED:' + g.get('token', '?') + ':' + pth[:64])
    return bad


def _empty_effective_policy():
    return {'policySchema':1,'policyScope':'effective','sources':{'global':None,'project':None},'grants':[],'denies':[],'consents':[]}


def merge_policy(global_doc, project_doc):
    """Raw-policy admission AND narrowing boundary, independent of caller validation.
    A refusal returns no effective grants. None is permitted only for absent
    project context (global/core); missing files are explicit empty documents.
    """
    try:
        for doc in (global_doc,) if project_doc is None else (global_doc,project_doc):
            validate(doc, load_schema('permission-policy'))
            canonical_bytes(doc)
        result, refusals = _merge_policy_checked(global_doc,project_doc)
        return (_empty_effective_policy(),refusals) if refusals else (result,[])
    except Exception:
        return _empty_effective_policy(), ['POLICY.SHAPE']


def _merge_policy_checked(global_doc, project_doc):
    """Pure merge of the global policy and the project-private policy (both opensip.metadata.policy.1 shaped,
    policyScope global/project). Returns (effective_doc, refusals). Rules: a deny in either layer denies;
    a grant is effective only when the global layer grants the same (stableId, token) and the project layer
    (when present) also grants it with a scope inside the global scope; the project layer can only narrow;
    unknown tokens or a widening project scope refuse the whole policy; consents are the intersection;
    ordering is stable (stableId, token) so the digest is canonical. The effective document records both
    source digests, so the lock's permissionPolicyDigest changes when either file changes."""
    refusals = []
    tokens = {'PT-FS-READ-PROJECT', 'PT-FS-READ-COMPONENT', 'PT-FS-WRITE-HOST-STATE', 'PT-PROC-EXEC-DECLARED', 'PT-NET-EGRESS', 'PT-ENV-READ', 'PT-HOST-EFFECT-BROKERED'}
    if global_doc.get('policyScope') != 'global' or (project_doc is not None and project_doc.get('policyScope') != 'project'):
        refusals.append('POLICY.SCOPE_LABEL')
    def key(g): return (g['stableId'], g['token'])
    for doc in (global_doc, project_doc or {'grants': [], 'denies': []}):
        for g in doc.get('grants', []) + doc.get('denies', []):
            if g.get('token') not in tokens:
                refusals.append('POLICY.UNKNOWN_TOKEN:' + str(g.get('token')))
        refusals += admit_policy_paths(doc)
        gk = [(g.get('stableId'), g.get('token')) for g in doc.get('grants', [])]
        dk = [(d.get('stableId'), d.get('token')) for d in doc.get('denies', [])]
        if len(set(gk)) != len(gk): refusals.append('POLICY.DUPLICATE_GRANT_PAIR')
        if len(set(dk)) != len(dk): refusals.append('POLICY.DUPLICATE_DENY_PAIR')
    if refusals:
        return {'policySchema': 1, 'policyScope': 'effective', 'sources': {'global': None, 'project': None}, 'grants': [], 'denies': [], 'consents': []}, sorted(set(refusals))
    denies = {}
    for doc in (global_doc, project_doc or {'denies': []}):
        for d in doc.get('denies', []):
            denies[key(d)] = d
    g_grants = {key(g): g for g in global_doc.get('grants', [])}
    effective = []
    if project_doc is None:
        for k in sorted(g_grants):
            if k not in denies:
                effective.append(g_grants[k])
    else:
        for g in project_doc.get('grants', []):
            k = key(g)
            if k in denies:
                continue
            if k not in g_grants:
                refusals.append('POLICY.PROJECT_WIDENS_GRANT:' + g['token']); continue
            gs, ps = g_grants[k].get('scope', {}), g.get('scope', {})
            narrowed = {}
            for field in sorted(set(gs) | set(ps)):
                gv, pv = gs.get(field), ps.get(field)
                if field == 'stateClass':
                    if pv is not None and pv != gv:
                        refusals.append('POLICY.PROJECT_WIDENS_SCOPE:' + g['token'] + ':' + field)
                    narrowed[field] = pv if pv is not None else gv
                    continue
                gl, pl = gv or [], pv if pv is not None else (gv or [])
                if field == 'pathPrefixes':
                    if not all(_prefix_within(x, gl) for x in pl):
                        refusals.append('POLICY.PROJECT_WIDENS_SCOPE:' + g['token'] + ':' + field)
                elif not set(pl) <= set(gl):
                    refusals.append('POLICY.PROJECT_WIDENS_SCOPE:' + g['token'] + ':' + field)
                narrowed[field] = sorted(pl)
            effective.append({'stableId': g['stableId'], 'token': g['token'], 'scope': narrowed})
        effective.sort(key=key)
    def ckey(c): return json.dumps(c, sort_keys=True)
    g_cons = {ckey(c): c for c in global_doc.get('consents', [])}
    consents = [g_cons[k] for k in sorted(g_cons)] if project_doc is None else [g_cons[k] for k in sorted(g_cons) if k in {ckey(c) for c in project_doc.get('consents', [])}]
    eff = {'policySchema': 1, 'policyScope': 'effective',
           'sources': {'global': domain_digest(DOMAIN_TAGS['policy'], global_doc)[0], 'project': domain_digest(DOMAIN_TAGS['policy'], project_doc)[0] if project_doc is not None else None},
           'grants': effective, 'denies': [denies[k] for k in sorted(denies)], 'consents': consents}
    return eff, sorted(set(refusals))


EMPTY_GLOBAL_POLICY = {'policySchema': 1, 'policyScope': 'global', 'grants': [], 'denies': [], 'consents': []}
EMPTY_PROJECT_POLICY = {'policySchema': 1, 'policyScope': 'project', 'grants': [], 'denies': [], 'consents': []}


def effective_policy_digest(eff):
    """The lock's permissionPolicyDigest: the domain digest of the effective document under its OWN tag
    (opensip.metadata.policy-effective.1), never a raw file's digest."""
    return domain_digest(DOMAIN_TAGS['policy-effective'], eff)[0]


def effective_policy_for_operation(global_doc, project_doc, selected_project):
    """Foundation rule (deny by absence): an operation with a selected project whose private policy file
    is missing evaluates merge(global, EMPTY_PROJECT_POLICY), never merge(global, None). merge(global, None)
    is exclusively the global/core operation without a selected project namespace. Doctor never creates the
    project namespace to represent an empty policy; it reports the absence."""
    if type(selected_project) is not bool:
        return _empty_effective_policy(), ['POLICY.SHAPE']
    if global_doc is None:
        global_doc = EMPTY_GLOBAL_POLICY
    if selected_project:
        return merge_policy(global_doc, project_doc if project_doc is not None else EMPTY_PROJECT_POLICY)
    return merge_policy(global_doc, None)


# ---- SEC3-M1: one admission boundary for a root document -------------------------------------------
class AdmittedRoot(object):
    """Immutable carrier of an admitted root (SEC3-M1 corrective). Construction is NOT a trust anchor: the
    carrier holds a canonical copy and a claimed digest, exposes only fresh copies, and verify_envelope
    re-runs the complete admission boundary (shape -> semantic) on the held copy and re-derives the digest
    before any use. A direct construction over an invalid document, or with a wrong digest, is refused
    there; a mutation of a returned copy never reaches the held state."""
    __slots__ = ('_canon', '_digest')
    def __init__(self, doc, digest):
        object.__setattr__(self, '_canon', json.dumps(doc, sort_keys=True, separators=(',', ':'), ensure_ascii=False))
        object.__setattr__(self, '_digest', digest)
    def __setattr__(self, name, value):
        raise AttributeError('AdmittedRoot is immutable')
    @property
    def doc(self):
        return json.loads(self._canon)          # a fresh copy every time
    @property
    def digest(self):
        return self._digest


def recheck_admitted_root(root):
    """The use-side half of the boundary: returns (root_doc, None) or (None, refusal_detail)."""
    if not isinstance(root, AdmittedRoot):
        return None, 'verify_envelope requires an AdmittedRoot'
    try:
        doc = root.doc
        adm, refusals = admit_root_document(doc)
    except Exception as e:                      # any exception inside the boundary is a refusal
        return None, 'recheck raised %s' % type(e).__name__
    if adm is None:
        return None, 'recheck: ' + ';'.join(refusals)[:160]
    if adm.digest != root.digest:
        return None, 'recheck: digest mismatch'
    return doc, None


def admit_root_document(root_obj):
    """parse/shape -> schema -> semantic rules, in that order; returns (AdmittedRoot, []) or (None, refusals)."""
    try:
        if isinstance(root_obj, bytes):
            root_obj = load_json_strict(root_obj)
        validate(root_obj, load_schema('root'))
    except SchemaError as e:
        return None, ['ROOT.SHAPE:' + str(e)[:120]]
    except Exception as e:
        return None, ['ROOT.SHAPE:exception ' + type(e).__name__]
    try:
        sem = admit_root(root_obj)
    except Exception as e:
        return None, ['ROOT.SEMANTIC:exception ' + type(e).__name__]
    if sem:
        return None, sem
    try:
        return AdmittedRoot(root_obj, domain_digest(DOMAIN_TAGS['root'], root_obj)[0]), []
    except Exception as e:
        return None, ['ROOT.CANONICAL']


# ---- SEC3-M6: Linux OS-ABI launch predicate over unprivileged observations --------------------------
def linux_os_abi_predicate(payload, observed):
    """payload = the profile's publisher-signed-boot payload with MEASURED values for kernelFlavor,
    kernelSeries (major.minor.patch line + flavor, e.g. 6.17.0-azure), bootAttestation, archiveSigningKeyDigest,
    uefiSignerDigest. observed = {'osrelease', 'procVersionUbuntu': bool, 'dpkgInstalled': bool,
    'dpkgMaintainerUbuntu': bool, 'archiveKeyDigest', 'secureBoot': 0|1|None, 'lockdown': 'none'|'integrity'|
    'confidentiality'|None, 'uefiSignerPresent': bool|None, 'fsType', 'nsUnchanged': bool}.
    Returns ('pass', []) or ('fail', [reasons]); an unmeasured placeholder in the payload is 'undetermined'."""
    def placeholder(v): return isinstance(v, dict) and '$releaseMeasured' in v
    if any(placeholder(payload.get(k)) for k in ('kernelFlavor', 'kernelSeries', 'bootAttestation', 'archiveSigningKeyDigest')):
        return 'undetermined', ['PROFILE-UNQUALIFIED: release-measured placeholder in the OS ABI identity']
    r = []
    series = payload['kernelSeries']                        # e.g. '6.17.0-azure' or '6.8.0-generic'
    line, flavor = series.rsplit('-', 1)
    rel = observed.get('osrelease') or ''
    m = re.fullmatch(r'(\d+\.\d+\.\d+)-(\d+)-([a-z0-9]+)', rel)
    if not m or m.group(1) != line or m.group(3) != flavor or flavor != payload['kernelFlavor']:
        r.append('KERNEL_SERIES_OR_FLAVOR:' + rel)
    if not observed.get('procVersionUbuntu'):
        r.append('PROC_VERSION_NOT_UBUNTU')
    if not (observed.get('dpkgInstalled') and observed.get('dpkgMaintainerUbuntu')):
        r.append('KERNEL_PACKAGE_NOT_INSTALLED_BY_UBUNTU')
    if observed.get('archiveKeyDigest') != payload['archiveSigningKeyDigest']:
        r.append('ARCHIVE_KEY_DIGEST')
    if payload['bootAttestation'] == 'secure-boot-lockdown':
        if observed.get('secureBoot') != 1: r.append('SECURE_BOOT_OFF')
        if observed.get('lockdown') not in ('integrity', 'confidentiality'): r.append('LOCKDOWN_NONE')
        if observed.get('uefiSignerPresent') is not True: r.append('UEFI_SIGNER_ABSENT')
    elif payload['bootAttestation'] != 'package-db-declared':
        r.append('BOOT_ATTESTATION_UNKNOWN')
    if observed.get('fsType') != 'ext4':
        r.append('INSTALL_ROOT_NOT_EXT4')
    if observed.get('nsUnchanged') is not True:
        r.append('MOUNT_NAMESPACE_CHANGED_DURING_READ')
    return ('pass', []) if not r else ('fail', r)
