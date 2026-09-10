"""Shared library for the security completion unit v2 (design evidence only).

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
    'policy': 'opensip.metadata.policy.1',
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


def verify_envelope(stored_bytes, env, root, expected_kind, publisher_namespace=None):
    """Section 2.2 verification order. Returns (outcome, detail)."""
    # step 1: presence / structural
    if env is None:
        return 'RJ-4 UNSIGNED', 'no envelope'
    try:
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


_SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'security-schemas.v2')


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


def locator(project_key, grant_generation, seq):
    """gj:<base64url(projectKey bytes, no padding)>:<grantGeneration>:<seq> — projectKey is the paired lock
    schema's opaque host-owned key; base64url contains no ':' so the locator is unambiguous."""
    import base64
    return 'gj:%s:%d:%d' % (base64.urlsafe_b64encode(project_key.encode('utf-8')).decode('ascii').rstrip('='), grant_generation, seq)


SEQ_MAX = 9007199254740991           # JSON uint53 carried by control effectResult decisionSeq/outcomeSeq
SEQ_LAST_ORDINARY = SEQ_MAX - 1      # the last value an ordinary record may take; SEQ_MAX is the terminal slot
GRANT_GENERATION_MAX = I64MAX        # string-encoded in the locator, so the full signed-i64 range is representable


def genesis_prev(project_key, grant_generation):
    return sha256_hex(b'opensip.journal.genesis.1' + b'\x00' + project_key.encode('utf-8') + b'\x00' + str(grant_generation).encode('ascii'))


def record_body_sha(body):
    d, _ = domain_digest(DOMAIN_TAGS['journal'], body)
    return d
