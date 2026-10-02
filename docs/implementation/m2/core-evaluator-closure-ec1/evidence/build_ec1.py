"""Build the EC1 contract successor (the core evaluator closure), its test vector and the
subject manifest. Run with python3 -I -B from any directory, giving the product checkout as
the one argument (default /Users/sb/code/opensip-ai/opensip, main a36da7c). Deterministic:
rerunning reproduces the same bytes. Reads the product read-only."""
import hashlib, json, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip')
M = 'docs/implementation/m2/'
D = M + 'core-evaluator-closure-ec1/'
SCHEMAS = 'docs/coop/design-corrections/foundation/identity-schemas.v3.json'
CONTRACT = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
FIXTURE = 'crates/security/tests/fixtures/core-inventory318.ndjson'
LABEL = 'baseline-macos'


def pin(p, root=A):
    b = (root / p).read_bytes()
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def C(x):
    # The product canonical form for these values: sorted keys, no whitespace, ASCII strings,
    # small integers (checked against the fixture's own expected closure below).
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def H(domain, x):
    c = C(x)
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode() + b'\x00'
                          + len(c).to_bytes(8, 'big') + c).hexdigest()


# --- The vector: one accepted core inventory case, both closures. -----------------------------
case = None
for line in (W / FIXTURE).read_bytes().decode('utf-8').splitlines():
    q = json.loads(line)
    if q['label'] == LABEL:
        case = q
assert case is not None and case['expected']['ok'] is True
raw = bytes.fromhex(case['raw'])
core = case['expected']['descriptor']
assert core['kind'] == 'core' and core['manifestDigest'] == hashlib.sha256(raw).hexdigest()
assert 'closure2:' + H('closure', core) == case['expected']['closure']
evaluator = dict(core, kind='evaluator')
vector = {
    'schemaVersion': 1,
    'standing': 'EC1 test vector. The core closure and the core evaluator closure of one authenticated core inventory: the two descriptors differ only by kind, and so do the two ids. X3d-3 reproduces it byte for byte in a Rust test.',
    'source': {'product': 'a36da7c', 'fixture': pin(FIXTURE, W), 'label': LABEL, 'platform': case['platform']},
    'inventoryBody': {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'hex': raw.hex()},
    'coreDescriptor': core,
    'coreClosure': 'closure2:' + H('closure', core),
    'coreDescriptorCanonicalSha256': hashlib.sha256(C(core)).hexdigest(),
    'evaluatorDescriptor': evaluator,
    'evaluatorClosure': 'closure2:' + H('closure', evaluator),
    'evaluatorDescriptorCanonicalSha256': hashlib.sha256(C(evaluator)).hexdigest(),
}
assert vector['coreClosure'] != vector['evaluatorClosure']
(A / D / 'evidence/vector.json').write_text(json.dumps(vector, indent=2, sort_keys=True) + '\n')

# --- The passage overrides. -------------------------------------------------------------------
ART_BEFORE = 'the admitted component manifest body bytes under the security metadata profile, excluding the signature envelope'
ART_AFTER = (ART_BEFORE + '; for kind evaluator, the TR-CORE-signed core inventory body bytes (opensip.metadata.inventory.1)'
             ' under the same profile, excluding its signature envelope (contract successor EC1, the core evaluator closure)')
schemas = json.loads((A / SCHEMAS).read_bytes())
NOTE_BEFORE = schemas['x-opensip-digest-domains']['closureKinds']['note']
NOTE_AFTER = NOTE_BEFORE + (
    ' The evaluator kind names no separately delivered component, because the evaluator is the pure core'
    ' (contract successor EC1). A core release\'s evaluator closure is closure2: + H("closure", D), where D is the'
    ' authenticated core inventory\'s selected-platform closure descriptor that security projects for the core'
    ' closure, with kind set to "evaluator" and every other member unchanged. Its manifestDigest is the raw SHA-256'
    ' of the TR-CORE-signed inventory body and its tree is that platform\'s regular files. The core closure and the'
    ' core evaluator closure therefore differ only by kind.')
assert schemas['$defs']['closure']['properties']['manifestDigest']['x-opensip-digest']['artifact'] == ART_BEFORE

lines = (A / CONTRACT).read_bytes().decode('utf-8').splitlines()
L273 = 'admitted component manifest body bytes encoded with the security metadata'
L273_AFTER = ('admitted component manifest body bytes (for kind `evaluator`, the TR-CORE-signed core inventory body;'
              ' see the core evaluator closure below, EC1) encoded with the security metadata')
L278 = 'and digest for every selected file. A semantic version alone is not a closure.'
L278_AFTER = L278 + (
    ' **Core evaluator closure (contract successor EC1, 2026-10-02).** The evaluator is the pure core, so a core'
    ' release\'s evaluator closure is not a separately delivered component. It is `closure2:` + H("closure", D),'
    ' where D is the authenticated core inventory\'s selected-platform closure descriptor `{schemaVersion: 2, kind,'
    ' manifestDigest, tree, semanticVersion, protocolMajor, platform}` that security projects for the core closure'
    ' (`kind: "core"`), with `kind` set to `"evaluator"` and every other member unchanged. For this kind'
    ' `manifestDigest` is raw SHA256 of the TR-CORE-signed core inventory body (`opensip.metadata.inventory.1`),'
    ' excluding its signature envelope, and `tree` is the projection of that platform\'s regular files. The core'
    ' closure and the core evaluator closure of one release therefore differ only by `kind`. Security derives both'
    ' from the same authenticated inventory; neither is read from a Run, a worker claim or a build-time string. As for'
    ' every closure, the inventory body and every tree member are retained preimages of a Run that names it. A new'
    ' core release is a new evaluator closure, so the Plans and Runs it evaluates have new identities. Historical'
    ' closures, Plans and Runs keep their bytes and are not re-read under this law.')
L455 = ('| `raw-artifact` | raw SHA256 of the **exact retained artifact bytes** — a source or closure-tree file, a'
        ' committed capability-manifest artifact, a component manifest body, or a complete registered schema document.'
        ' Not of a canonicalization of anything. |')
L455_AFTER = L455.replace('a component manifest body,', 'a component manifest body (for kind `evaluator`, the TR-CORE-signed core inventory body, EC1),')
assert lines[272] == L273 and lines[277] == L278 and lines[454] == L455 and L455_AFTER != L455

sp, cp = pin(SCHEMAS), pin(CONTRACT)
overrides = [
    {'parent': sp, 'selector': {'jsonPointer': '/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact'},
     'before': ART_BEFORE, 'after': ART_AFTER},
    {'parent': sp, 'selector': {'jsonPointer': '/x-opensip-digest-domains/closureKinds/note'},
     'before': NOTE_BEFORE, 'after': NOTE_AFTER},
    {'parent': cp, 'selector': {'line': 273}, 'before': L273, 'after': L273_AFTER},
    {'parent': cp, 'selector': {'line': 278}, 'before': L278, 'after': L278_AFTER},
    {'parent': cp, 'selector': {'line': 455}, 'before': L455, 'after': L455_AFTER},
]
EVIDENCE = ['evidence/build_ec1.py', 'evidence/check_ec1.py', 'evidence/vector.json', 'evidence/verify_scratch.py']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED EC1 identity contract successor (the core evaluator closure; law X3d r8 item 3 step 1): a core release\'s evaluator closure is closure2: + H("closure", the authenticated core descriptor with kind "evaluator"), and for kind evaluator manifestDigest is the raw SHA-256 of the TR-CORE-signed inventory body. Text-only overrides of the identity schema bundle\'s closure annotations and the identity contract; no schema shape, kind, domain, recipe, registry, generated code, inventory or product change. Exact frozen candidate requires actual independent review and root assent.',
    'parents': sorted([sp, cp], key=lambda r: r['path']),
    'passageOverrides': overrides,
    'candidates': sorted([pin(D + 'README.md')] + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path']),
}
(A / D / 'successor.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
subject = {'schemaVersion': 1, 'files': sorted([pin(D + 'README.md'), pin(D + 'successor.json')]
           + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path'])}
(A / M / 'core-evaluator-closure-ec1-subject.json').write_text(json.dumps(subject, indent=2) + '\n')
print(json.dumps({'overrides': len(overrides), 'coreClosure': vector['coreClosure'],
                  'evaluatorClosure': vector['evaluatorClosure']}))
