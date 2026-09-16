"""CAP-MANIFEST-ID-V1 admission, independently implemented from:

  docs/coop/design-corrections/native/capability-manifest-domains.v2.json
      recipe / gateOrder / admission / registries / recordShape / declaredOPEN /
      traversalOrder / decoderBounds           (the SELECTED current registry)
  docs/coop/artifacts/delivery.v4.json  derivedFrom.operations[8].value
      DL-ORD-1 / DL-ORD-2 / declaredSortKeys   (the retained ADM-ORDER recipe)
  docs/coop/artifacts/delivery.v2.json  capabilityManifestSchema
      the inherited required key sets          (reproduced by the successor)
  docs/coop/artifacts/resolved-inputs.v2.json planIdContract.canonicalValueEncoding
      CVE1

Admission runs BEFORE encoding: the four gates are applied to the parsed JSON value,
and only an admitted value is CVE1-encoded and hashed.
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K

KIT = '/tmp/opensip-design-corrections/consumer-b.v23/subject'
REG_PATH = 'docs/coop/design-corrections/native/capability-manifest-domains.v2.json'
DELIVERY4 = 'docs/coop/artifacts/delivery.v4.json'


class CapRefusal(Exception):
    def __init__(self, gate, code, position, detail=None):
        super().__init__('%s/%s at %s: %s' % (gate, code, position, detail))
        self.gate = gate
        self.code = code
        self.position = position
        self.detail = detail


def _reg():
    return json.load(open(KIT + '/' + REG_PATH))


def sort_keys():
    d = json.load(open(KIT + '/' + DELIVERY4))
    for op in d['derivedFrom']['operations']:
        v = op.get('value')
        if isinstance(v, dict) and 'declaredSortKeys' in v:
            return v
    raise RuntimeError('declaredSortKeys not found in delivery.v4')


class CapabilityManifestAdmitter:
    def __init__(self):
        r = _reg()
        self.reg = r
        self.gate_order = r['gateOrder']
        self.registries = r['registries']
        self.record_shape = r['recordShape']
        self.declared_open = set(r['declaredOPEN'])
        self.traversal = r['traversalOrder']
        self.sortkeys = sort_keys()['declaredSortKeys']
        self.ladders = self.registries['RELATION-LADDER-DOMAIN-V2']['ladders']
        self.relations = set(self.registries['RELATION-DOMAIN-V2']['members'])
        self.platforms = set(self.registries['PLATFORM-ID-DOMAIN-V1']['members'])
        self.deficiencies = set(self.registries['DEFICIENCY-DOMAIN-V1']['members'])
        self.coverage_states = set(self.registries['COVERAGE-STATE-DOMAIN-V1']['members'])
        # every declared scalar position, with its binding. ADM-DOMAIN: bound or
        # declared-open, with no third state.
        self.bound = {
            'ProviderCapability.relations key': self.relations,
            'ProviderCapability.relations value': None,      # per-key ladder
            'ProviderCapability.platformIds[]': self.platforms,
            'AbsentCapability.relationIds[]': self.relations,
            'AbsentCapability.coverageState': self.coverage_states,
            'AbsentCapability.deficiency': self.deficiencies,
        }

    # ---------------- ADM-TYPE
    #
    # HELPER CORRECTION (consumer-b.v14, recorded in checkpoints/phase-2.json):
    # the first draft type-checked every DECLARED key whether or not it was PRESENT, so
    # popping AbsentCapability.deficiency refused at ADM-TYPE instead of ADM-CLOSED.
    # Corrected from the kit only:
    #   ADM-TYPE  -- "Every SCALAR is admitted by EXACT JSON TYPE before its content is
    #                 compared." A key that is absent contributes no scalar to type.
    #   ADM-CLOSED -- "A RECORD declares a KEY SET: it carries EXACTLY that key set, each
    #                 key exactly once, with no undeclared member."
    # So a MISSING required key is ADM-CLOSED's fault and an undeclared key is too;
    # ADM-TYPE now types only declared keys that are present.
    def _adm_type(self, m):
        def typ(v):
            if isinstance(v, bool):
                return 'boolean'
            if isinstance(v, int):
                return 'integer'
            if isinstance(v, float):
                return 'number'
            if isinstance(v, str):
                return 'string'
            if v is None:
                return 'null'
            if isinstance(v, list):
                return 'array'
            if isinstance(v, dict):
                return 'object'
            return 'other'
        def want(obj, key, expected, position):
            """Type a DECLARED key only when it is PRESENT; absence is ADM-CLOSED's."""
            if key not in obj:
                return
            if typ(obj[key]) != expected:
                kind = {'integer': 'SCALAR', 'string': 'SCALAR', 'array': 'COLLECTION',
                        'object': 'RECORD'}[expected]
                raise CapRefusal('ADM-TYPE', kind + '_WRONG_JSON_TYPE', position,
                                 'expected %s, got %s' % (expected, typ(obj[key])))

        if typ(m) != 'object':
            raise CapRefusal('ADM-TYPE', 'ROOT_NOT_OBJECT', 'CapabilityManifestV1', typ(m))
        want(m, 'schemaVersion', 'integer', 'CapabilityManifestV1.schemaVersion')
        want(m, 'profile', 'string', 'CapabilityManifestV1.profile')
        for key in ('providers', 'coverageForAbsent'):
            want(m, key, 'array', 'CapabilityManifestV1.' + key)
        for i, p in enumerate(m.get('providers', []) if isinstance(m.get('providers'), list) else []):
            if typ(p) != 'object':
                raise CapRefusal('ADM-TYPE', 'RECORD_NOT_OBJECT', 'providers[%d]' % i, typ(p))
            for f in ('providerId', 'language', 'providerVersionSource',
                      'toolchainIdentitySource'):
                want(p, f, 'string', 'providers[%d].%s' % (i, f))
            want(p, 'relations', 'object', 'providers[%d].relations' % i)
            if isinstance(p.get('relations'), dict):
                for k, v in p['relations'].items():
                    if typ(v) != 'string':
                        raise CapRefusal('ADM-TYPE', 'SCALAR_WRONG_JSON_TYPE',
                                         'providers[%d].relations[%s]' % (i, k), typ(v))
            want(p, 'platformIds', 'array', 'providers[%d].platformIds' % i)
            if isinstance(p.get('platformIds'), list):
                for j, x in enumerate(p['platformIds']):
                    if typ(x) != 'string':
                        raise CapRefusal('ADM-TYPE', 'SCALAR_WRONG_JSON_TYPE',
                                         'providers[%d].platformIds[%d]' % (i, j), typ(x))
        ca = m.get('coverageForAbsent')
        for i, a in enumerate(ca if isinstance(ca, list) else []):
            if typ(a) != 'object':
                raise CapRefusal('ADM-TYPE', 'RECORD_NOT_OBJECT',
                                 'coverageForAbsent[%d]' % i, typ(a))
            for f in ('providerId', 'language', 'coverageState', 'deficiency'):
                want(a, f, 'string', 'coverageForAbsent[%d].%s' % (i, f))
            want(a, 'relationIds', 'array', 'coverageForAbsent[%d].relationIds' % i)
            if isinstance(a.get('relationIds'), list):
                for j, x in enumerate(a['relationIds']):
                    if typ(x) != 'string':
                        raise CapRefusal('ADM-TYPE', 'SCALAR_WRONG_JSON_TYPE',
                                         'coverageForAbsent[%d].relationIds[%d]' % (i, j), typ(x))

    # ---------------- ADM-CLOSED
    def _closed(self, obj, shape_name, position):
        req = set(self.record_shape[shape_name]['requiredKeys'])
        got = set(obj.keys())
        if got != req:
            extra, missing = sorted(got - req), sorted(req - got)
            raise CapRefusal('ADM-CLOSED', 'RECORD_KEY_SET_NOT_EXACT', position,
                             'undeclared=%s missing=%s' % (extra, missing))

    def _adm_closed(self, m):
        self._closed(m, 'CapabilityManifestV1', 'CapabilityManifestV1')
        for i, p in enumerate(m.get('providers', [])):
            self._closed(p, 'ProviderCapability', 'providers[%d]' % i)
            # relations is a MAP: closure does not apply; a map whose values are
            # scalars closes nothing, and its KEYS are admitted by ADM-DOMAIN.
        for i, a in enumerate(m.get('coverageForAbsent', [])):
            self._closed(a, 'AbsentCapability', 'coverageForAbsent[%d]' % i)

    # ---------------- ADM-DOMAIN
    def _adm_domain(self, m):
        for i, p in enumerate(m['providers']):
            for k in p['relations']:
                if k not in self.relations:
                    raise CapRefusal('ADM-DOMAIN', 'SCALAR_NOT_IN_REGISTRY',
                                     'providers[%d].relations key' % i,
                                     '%r not in RELATION-DOMAIN-V2' % k)
                v = p['relations'][k]
                if v not in self.ladders[k]:
                    raise CapRefusal('ADM-DOMAIN', 'RUNG_NOT_IN_THIS_RELATION_LADDER',
                                     'providers[%d].relations[%s] value' % (i, k),
                                     '%r not a rung of %s ladder %s' % (v, k, self.ladders[k]))
            for j, x in enumerate(p['platformIds']):
                if x not in self.platforms:
                    raise CapRefusal('ADM-DOMAIN', 'SCALAR_NOT_IN_REGISTRY',
                                     'providers[%d].platformIds[%d]' % (i, j),
                                     '%r not in PLATFORM-ID-DOMAIN-V1' % x)
        for i, a in enumerate(m['coverageForAbsent']):
            for j, x in enumerate(a['relationIds']):
                if x not in self.relations:
                    raise CapRefusal('ADM-DOMAIN', 'SCALAR_NOT_IN_REGISTRY',
                                     'coverageForAbsent[%d].relationIds[%d]' % (i, j),
                                     '%r not in RELATION-DOMAIN-V2' % x)
            if a['coverageState'] not in self.coverage_states:
                raise CapRefusal('ADM-DOMAIN', 'SCALAR_NOT_IN_REGISTRY',
                                 'coverageForAbsent[%d].coverageState' % i, a['coverageState'])
            if a['deficiency'] not in self.deficiencies:
                raise CapRefusal('ADM-DOMAIN', 'SCALAR_NOT_IN_REGISTRY',
                                 'coverageForAbsent[%d].deficiency' % i, a['deficiency'])

    # ---------------- ADM-ORDER (declared traversal order)
    def _ascending(self, seq, keyfn, position, sortkey):
        prev = None
        for i, it in enumerate(seq):
            k = keyfn(it).encode('utf-8')
            if prev is not None and not prev < k:
                raise CapRefusal('ADM-ORDER', 'RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL',
                                 position + '[%d]' % i,
                                 'declared sort key %r: %r not strictly after %r'
                                 % (sortkey, k.decode(), prev.decode()))
            prev = k

    def _adm_order(self, m, collect_all=False):
        violations = []

        def run(fn):
            try:
                fn()
            except CapRefusal as e:
                if not collect_all:
                    raise
                violations.append({'gate': e.gate, 'code': e.code,
                                   'position': e.position, 'detail': e.detail})
        # declared traversal order: (1) each providers[i] platformIds, (2) each
        # coverageForAbsent[i] relationIds, (3) providers, (4) coverageForAbsent
        for i, p in enumerate(m['providers']):
            run(lambda i=i, p=p: self._ascending(
                p['platformIds'], lambda s: s, 'providers[%d].platformIds' % i,
                self.sortkeys['ProviderCapability.platformIds']))
        for i, a in enumerate(m['coverageForAbsent']):
            run(lambda i=i, a=a: self._ascending(
                a['relationIds'], lambda s: s, 'coverageForAbsent[%d].relationIds' % i,
                self.sortkeys['AbsentCapability.relationIds']))
        run(lambda: self._ascending(m['providers'], lambda p: p['providerId'],
                                    'providers',
                                    self.sortkeys['CapabilityManifestV1.providers']))
        run(lambda: self._ascending(m['coverageForAbsent'], lambda a: a['providerId'],
                                    'coverageForAbsent',
                                    self.sortkeys['CapabilityManifestV1.coverageForAbsent']))
        return violations

    # ---------------- entry point
    def admit(self, m, collect_order_violations=False):
        """Gates in the inherited order; returns {committedBytes, capabilityManifestId}."""
        trace = []
        for gate in self.gate_order:
            if gate == 'ADM-TYPE':
                self._adm_type(m)
            elif gate == 'ADM-CLOSED':
                self._adm_closed(m)
            elif gate == 'ADM-DOMAIN':
                self._adm_domain(m)
            elif gate == 'ADM-ORDER':
                vs = self._adm_order(m, collect_all=collect_order_violations)
                if vs:
                    return {'admitted': False, 'orderViolations': vs, 'gatesPassed': trace}
            else:
                raise RuntimeError('unknown gate ' + gate)
            trace.append(gate)
        committed = K.cve1(m)
        return {'admitted': True, 'gatesPassed': trace,
                'committedBytes': committed,
                'committedBytesSha256': K.raw_sha256(committed),
                'committedByteLength': len(committed),
                'capabilityManifestId': K.capability_manifest_id(committed)}
