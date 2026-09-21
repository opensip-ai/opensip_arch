"""Proposed371 pure reference checks. Supplied observations are NOT native authority."""
import json
import re

CAP = 4_194_304
MAX_ROWS = 4096
U64_MAX = (1 << 64) - 1
I64_MAX = (1 << 63) - 1
PID = re.compile(r'prj1-[0-9a-f]{64}')
NID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')
LIVE = {'RESERVED', 'ACTIVE'}
STATES = LIVE | {'RETIRED', 'ABANDONED'}
ROOT_FIELDS = {'platform', 'canonicalPathBytesHex', 'deviceId', 'inodeId', 'birthSeconds', 'birthNanoseconds'}

class Refused(ValueError):
    """Internal reference-model reason; not a new public error vocabulary."""

def require(condition, reason):
    if not condition:
        raise Refused(reason)

def closed(value, keys):
    require(type(value) is dict and set(value) == keys, 'shape')

def exact_int(value, lo, hi):
    require(type(value) is int and lo <= value <= hi, 'integer')

def spelling(pattern, value):
    require(type(value) is str and pattern.fullmatch(value) is not None, 'spelling')

def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def root_key(root):
    return tuple(root[k] for k in ('platform','deviceId','inodeId','birthSeconds','birthNanoseconds'))

def locator_key(root):
    return root['platform'], root['canonicalPathBytesHex']

def validate_root(root):
    closed(root, ROOT_FIELDS)
    require(root['platform'] in ('macos','linux'), 'platform')
    raw = root['canonicalPathBytesHex']
    require(type(raw) is str and len(raw) <= 8192 and re.fullmatch(r'(?:[0-9a-f]{2})+',raw), 'path-hex')
    path = bytes.fromhex(raw)
    require(path.startswith(b'/') and b'\0' not in path and b'//' not in path, 'absolute-path')
    require(path == b'/' or not path.endswith(b'/'), 'path-tail')
    require(not any(p in (b'.',b'..') for p in path.split(b'/')), 'path-components')
    for name in ('deviceId','inodeId'):
        number = root[name]
        require(type(number) is str and len(number) <= 20 and re.fullmatch(r'(?:0|[1-9][0-9]*)',number), 'decimal')
        require(int(number) <= U64_MAX, 'u64')
    exact_int(root['birthSeconds'], -(1 << 63), I64_MAX)
    exact_int(root['birthNanoseconds'],0,999_999_999)

def validate(document):
    closed(document, {'schemaVersion','entries'})
    exact_int(document['schemaVersion'],1,1)
    rows=document['entries']; require(type(rows) is list and len(rows) <= MAX_ROWS,'rows')
    prev=None; ids=set(); roots=set(); paths=set()
    for row in rows:
        closed(row, {'projectId','namespaceId','root','status','allocationKind'})
        spelling(PID,row['projectId']); spelling(NID,row['namespaceId'])
        validate_root(row['root'])
        require(type(row['status']) is str and row['status'] in STATES,'status')
        require(row['allocationKind'] in ('random','adopt'),'allocation-kind')
        n=row['namespaceId']; require(prev is None or n > prev,'namespace-order-unique'); prev=n
        if row['status'] in LIVE:
            p=row['projectId']; r=root_key(row['root']); l=locator_key(row['root'])
            require(p not in ids and r not in roots and l not in paths,'live-uniqueness')
            ids.add(p); roots.add(r); paths.add(l)
    require(len(encode(document)) <= CAP,'bytes')
    return document

def decode(raw):
    require(type(raw) is bytes and len(raw) <= CAP,'bytes')
    # Bound nesting before the JSON decoder allocates nested values. Strings do
    # not contribute bracket depth; the decoder still checks complete JSON syntax.
    depth=0; in_string=False; escaped=False
    for octet in raw:
        if in_string:
            if escaped: escaped=False
            elif octet==92: escaped=True
            elif octet==34: in_string=False
        elif octet==34: in_string=True
        elif octet in (91,123):
            depth+=1; require(depth <= 32,'depth')
        elif octet in (93,125): depth-=1
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'duplicate-key'); result[k]=v
        return result
    def integer(token):
        require(token != '-0','negative-zero')
        require(len(token) <= 20,'integer-width')
        n=int(token); require(-(1 << 63) <= n <= U64_MAX,'integer-range'); return n
    def forbidden(token):
        raise Refused('non-integer')
    try:
        parsed=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_int=integer,parse_float=forbidden,parse_constant=forbidden)
        validate(parsed)
        require(encode(parsed) == raw,'canonical')
        return parsed
    except (UnicodeError,RecursionError,json.JSONDecodeError) as e:
        raise Refused('encoding') from e

def marker(project_id):
    spelling(PID,project_id)
    return b'opensip-project-id-v1\n'+project_id.encode('ascii')+b'\n'

def marker_id(raw):
    require(type(raw) is bytes and len(raw)==92,'marker-length')
    require(raw[:22]==b'opensip-project-id-v1\n' and raw[-1:]==b'\n','marker-frame')
    try: value=raw[22:-1].decode('ascii')
    except UnicodeError as e: raise Refused('marker-ascii') from e
    spelling(PID,value); return value

def classify(document, root, marker_observation, tracking='untracked'):
    """Pure predicate over COMPLETE supplied observations, no host admission token."""
    validate(document); validate_root(root)
    if tracking != 'untracked': return 'TRACKING_REFUSAL'
    if marker_observation == 'unavailable': return 'UNAVAILABLE'
    pid=None
    if marker_observation != 'absent':
        try: pid=marker_id(marker_observation)
        except Refused: return 'MALFORMED'
    relevant=[r for r in document['entries'] if r['status'] in LIVE and
              (locator_key(r['root'])==locator_key(root) or root_key(r['root'])==root_key(root) or
               (pid is not None and r['projectId']==pid))]
    if not relevant: return 'FIRST_USE_CANDIDATE' if pid is None else 'ONE_SIDED'
    if len(relevant)!=1: return 'CONTRADICTION'
    row=relevant[0]
    if row['root']!=root or (pid is not None and pid!=row['projectId']): return 'CONTRADICTION'
    if row['status']=='RESERVED': return 'RECOVERY_REQUIRED'
    return 'ONE_SIDED' if pid is None else 'MATCHED_ACTIVE'

def namespace_list(document):
    validate(document)
    require(not any(r['status']=='RESERVED' for r in document['entries']),'pending-reservation')
    return [r['namespaceId'] for r in document['entries'] if r['status'] in {'ACTIVE','RETIRED'}]

def transition(before, after, kind):
    """Check only exact registry delta. Authorization/native guards are external."""
    validate(before); validate(after)
    old={r['namespaceId']:r for r in before['entries']}; new={r['namespaceId']:r for r in after['entries']}
    require(set(old) <= set(new),'no-delete')
    if kind in {'reserve-random','reserve-adopt'}:
        added=set(new)-set(old)
        require(len(added)==1 and all(old[n]==new[n] for n in old),'insertion-only')
        row=new[added.pop()]; require(row['status']=='RESERVED','must-reserve')
        require(row['allocationKind']==('random' if kind=='reserve-random' else 'adopt'),'reservation-kind')
        if kind=='reserve-random':
            require(all(r['projectId']!=row['projectId'] for r in old.values()),'historical-id-reuse')
    else:
        require(set(old)==set(new),'same-namespaces')
        changed=[n for n in old if old[n]!=new[n]]; require(len(changed)==1,'one-row-delta')
        a=old[changed[0]]; b=new[changed[0]]
        require(a['projectId']==b['projectId'],'immutable-project')
        require(a['allocationKind']==b['allocationKind'],'immutable-allocation-kind')
        if kind=='move':
            require(a['status']==b['status']=='ACTIVE' and a['root']!=b['root'],'active-move')
        else:
            require(a['root']==b['root'],'immutable-root')
            edges={'activate':('RESERVED','ACTIVE'),'abandon':('RESERVED','ABANDONED'),'retire':('ACTIVE','RETIRED')}
            require(kind in edges and (a['status'],b['status'])==edges[kind],'state-edge')
    return after


def allocation_candidate(document, project_candidates, namespace_candidates, occupied_namespaces):
    """Given independent OS draws as an EXTERNAL assumption, choose bounded values.
    Does not draw entropy, reserve, observe paths, publish, or authorize allocation.
    occupied_namespaces is a supplied complete observation for offered candidates.
    """
    validate(document)
    old_ids={r['projectId'] for r in document['entries']}
    old_ns={r['namespaceId'] for r in document['entries']}
    project=None; namespace=None
    for p in project_candidates[:8]:
        spelling(PID,p)
        if p not in old_ids: project=p; break
    require(project is not None,'project-candidates-exhausted')
    for n in namespace_candidates[:8]:
        spelling(NID,n)
        if n not in old_ns and n not in occupied_namespaces: namespace=n; break
    require(namespace is not None,'namespace-candidates-exhausted')
    return project,namespace

def reservation_completion(document, namespace_id, namespace_observation, marker_observation, durable_registry, stopped, mode, adoption_project_id=None):
    """Conditional recovery plan ONLY, after external explicit authorization,
    admitted RESERVED/root/custody/start-gate prerequisites. No native authority.
    Namespace absent must mean positively observed final-directory absence.
    """
    validate(document)
    rows=[r for r in document['entries'] if r['namespaceId']==namespace_id]
    require(len(rows)==1 and rows[0]['status']=='RESERVED','reserved-row-required')
    row=rows[0]
    if stopped or durable_registry is not True: return 'STOP'
    if mode not in ('ordinary-recovery','admitted-adoption'): return 'NO_COMPLETION_AUTHORITY'
    if row['allocationKind']=='adopt':
        if mode!='admitted-adoption': return 'ADOPTION_CONTEXT_REQUIRED'
        if adoption_project_id!=row['projectId']: return 'ADOPTION_PROJECT_MISMATCH'
    elif mode!='ordinary-recovery': return 'CONTEXT_KIND_MISMATCH'
    if row['allocationKind']=='random' and namespace_observation=='absent' and marker_observation=='exact':
        return 'ORDINARY_PREFIX_REFUSED'
    if namespace_observation not in ('absent','complete-initial'): return 'UNAVAILABLE'
    if marker_observation not in ('absent','exact'): return 'UNAVAILABLE'
    effects=[]
    if namespace_observation=='absent': effects.append('publish-namespace')
    else: effects.append('reconfirm-namespace-durability')
    if marker_observation=='absent': effects.append('create-marker')
    else: effects.append('reconfirm-marker-durability')
    effects.append('publish-ACTIVE')
    return effects


def initial_namespace_footprint(directory_mode, entries):
    """Complete SUPPLIED native-observation value only, not capture/custody proof."""
    if type(directory_mode) is not int or directory_mode != 0o700: return False
    if type(entries) is not list or len(entries)!=2: return False
    names=set()
    for entry in entries:
        if type(entry) is not dict or set(entry)!={'name','kind','mode','bytes','links'}: return False
        if entry['name'] not in ('writer.lease','readers.lease') or entry['name'] in names: return False
        names.add(entry['name'])
        if entry['kind']!='regular': return False
        for field,required in (('mode',0o600),('bytes',0),('links',1)):
            if type(entry[field]) is not int or entry[field]!=required: return False
    return names=={'writer.lease','readers.lease'}
