"""Independent reconstruction of the five NEW-MUST-1 recipes from CONTRACT PROSE
alone. Implements C and H from identity-and-evidence.md section 3 without
importing canonical.py or identity-model. Then checks the author's model lands
on exactly these digests for the SAME inputs, and that my own fresh vectors
(different from the author's) also agree. A recipe that were underspecified
could not be hit independently."""
import json, hashlib, sys, importlib.util, copy
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')

# ---------- my C, written from the prose ----------
def C(v):
    if v is True: return b'true'
    if v is False: return b'false'
    if v is None: return b'null'
    if isinstance(v, int): return str(v).encode()            # shortest ordinary decimal
    if isinstance(v, str):
        o = bytearray(b'"')
        for ch in v:
            c = ord(ch)
            if ch == '"': o += b'\\"'
            elif ch == '\\': o += b'\\\\'
            elif c == 8: o += b'\\b'
            elif c == 9: o += b'\\t'
            elif c == 10: o += b'\\n'
            elif c == 12: o += b'\\f'
            elif c == 13: o += b'\\r'
            elif c < 0x20: o += ('\\u%04x' % c).encode()      # lowercase \u00xx
            else: o += ch.encode('utf-8')                     # unescaped scalars; slash not escaped
        return bytes(o + b'"')
    if isinstance(v, list): return b'[' + b','.join(C(x) for x in v) + b']'   # admitted order
    if isinstance(v, dict):
        items = sorted(v.items(), key=lambda kv: kv[0].encode('utf-8'))       # UTF-8 byte-ordered keys
        return b'{' + b','.join(C(k) + b':' + C(x) for k, x in items) + b'}'
    raise TypeError(type(v))

def H(D, X):
    c = C(X)
    return hashlib.sha256(b'opensip.product.v1' + b'\x00' + D.encode('ascii') + b'\x00'
                          + len(c).to_bytes(8, 'big') + c).hexdigest()

def rawrec(X): return hashlib.sha256(C(X)).hexdigest()

# ---------- load the author's units from subject bytes, unmodified ----------
sys.path.insert(0, str(SUB / 'foundation'))
spec = importlib.util.spec_from_file_location('idm', SUB / 'foundation' / 'identity-model.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
import canonical as CA

R = {}

# ---- my C vs theirs on adversarial values ----
cases = [
    {'b': 1, 'a': 2}, [3, 1, 2], 'a b',
    'q"\\' + chr(8) + chr(9) + chr(10) + chr(12) + chr(13) + chr(1) + 'z',
    {'': 0}, {chr(0xe9): chr(0xe9)}, [{'z': 1}, {'a': 2}], {'k': [1, [2, [3]]]},
    0, -1, 2 ** 64 - 1, -(2 ** 63), True, False, None,
    {'Z': 1, 'a': 2}, {'A': 1, chr(0xff21): 2},
    chr(0x1f600), chr(0x7f), chr(0x2028), 'a/b',
]
R['encoderAgreesOnAdversarialValues'] = all(C(x) == CA.canonical(x) for x in cases)
R['encoderDisagreements'] = [[repr(x), C(x).decode('utf-8', 'replace'),
                              CA.canonical(x).decode('utf-8', 'replace')]
                             for x in cases if C(x) != CA.canonical(x)]
R['myFrameEqualsTheirs'] = (H('native.context.typescript.v2', {'a': 1})
                            == CA.identity('native.context.typescript.v2', {'a': 1}))

# ---- MY OWN vectors, distinct from the author's, for each of the 5 records ----
MY = {}
MY['program-predicate'] = {'schemaVersion': 2, 'ruleProgramDigest': 'ab' * 32,
                           'ruleId': 'rule.independent', 'predicateId': 'p.2.0',
                           'operation': 'count-at-most', 'nodeDigest': 'cd' * 32}
MY['finding-parameters'] = {'schemaVersion': 2, 'messageCode': 'MSG.IND',
                            'parameters': {'zeta': True, 'alpha': -7, 'mid': 'v' + chr(0xe9) + 'l'}}
MY['stage-spec'] = {'schemaVersion': 2, 'planId': 'plan2:' + '1f' * 32,
                    'producerClosure': 'closure2:' + '2e' * 32,
                    'operation': 'derive-independent',
                    'parameters': [{'schemaDigest': '3d' * 32, 'payloadDigest': '4c' * 32}],
                    'outputDomains': ['fact', 'view'], 'outputSchemaDigest': '5b' * 32}
MY['commit-inventory'] = {'schemaVersion': 2, 'runId': 'run2:' + '6a' * 32,
                          'objects': ['fact2:' + '70' * 32, 'view2:' + '81' * 32],
                          'blobDigests': ['92' * 32, 'a3' * 32]}
MY['owner-source-set'] = [{'ownerKey': 'alpha', 'source': 'repository',
                           'ownerFileManifestSha256': 'b4' * 32},
                          {'ownerKey': 'beta', 'source': 'first-party',
                           'ownerFileManifestSha256': 'c5' * 32}]

R['myVectors'] = {}
for name, val in MY.items():
    mine = rawrec(val)
    theirs = hashlib.sha256(CA.canonical(val)).hexdigest()
    sch = copy.deepcopy(M.SCHEMA); sch['$ref'] = '#/$defs/' + name
    try:
        CA.validate(sch, val); valid, err = True, None
    except Exception as e:
        valid, err = False, str(e)[:300]
    R['myVectors'][name] = {'myDigest': mine, 'authorEncoderDigest': theirs,
                            'agree': mine == theirs,
                            'validatesUnderRegisteredRecord': valid, 'validationError': err,
                            'myPreimage': C(val).decode('utf-8', 'replace')[:500]}
R['allFiveMyVectorsAgreeAndValidate'] = all(
    v['agree'] and v['validatesUnderRegisteredRecord'] for v in R['myVectors'].values())

# ---- author literals must reproduce under MY encoder ----
AUTHOR = {'program-predicate': 'd0402034ed9f6e2c4e113e36760a4889ec54b349b0a7951fcceb5bec8f591e09',
          'finding-parameters': 'ec8b5959e7d27b01817b6eb830787c8dc02281cf8758f74bcfdf336b25d6a73e',
          'stage-spec': '056a6dbac737e36856e7e6cd6c27aae85869f058bc2ec436511fdf09256553c8',
          'commit-inventory': 'd87ef7db470cd9d8531141beddaba1bb0d5ae3b82a07452e1ba7cab0f34c9a0b',
          'owner-source-set': 'c6190a240894608b027e9c85ea4079a55847e66cd010b2090b84b50475a02975'}
AV = {'program-predicate': {'schemaVersion': 2, 'ruleProgramDigest': '0' * 64, 'ruleId': 'r',
                            'predicateId': 'p.1', 'operation': 'and', 'nodeDigest': '1' * 64},
      'finding-parameters': {'schemaVersion': 2, 'messageCode': 'm',
                             'parameters': {'b': 1, 'a': 'x', 'c': False}},
      'stage-spec': {'schemaVersion': 2, 'planId': 'plan2:' + '2' * 64,
                     'producerClosure': 'closure2:' + '3' * 64, 'operation': 'derive',
                     'parameters': [], 'outputDomains': ['view'], 'outputSchemaDigest': '4' * 64},
      'commit-inventory': {'schemaVersion': 2, 'runId': 'run2:' + '5' * 64,
                           'objects': ['view2:' + '6' * 64], 'blobDigests': ['7' * 64]},
      'owner-source-set': [{'ownerKey': 'a', 'source': 'repository',
                            'ownerFileManifestSha256': '8' * 64},
                           {'ownerKey': 'b', 'source': 'repository',
                            'ownerFileManifestSha256': '9' * 64}]}
R['authorLiteralsReproducedByMyEncoder'] = {k: (rawrec(AV[k]) == AUTHOR[k]) for k in AUTHOR}
R['allAuthorLiteralsReproduced'] = all(R['authorLiteralsReproducedByMyEncoder'].values())
R['noCollisionMineVsAuthor'] = len({rawrec(v) for v in MY.values()}
                                   | {rawrec(v) for v in AV.values()}) == 10

# ---- H identity is never the raw payload sha, in either direction ----
s = {'schemaVersion': 2, 'x': 'y'}
R['hNeverEqualsRaw'] = H('native.context.typescript.v2', s) != rawrec(s)
R['hDomainSeparated'] = H('native.context.rust.v2', s) != H('native.context.typescript.v2', s)
R['lengthFieldIsLoadBearing'] = (
    H('a', {'x': 'y'})
    != hashlib.sha256(b'opensip.product.v1\x00a\x00' + C({'x': 'y'})).hexdigest())

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
