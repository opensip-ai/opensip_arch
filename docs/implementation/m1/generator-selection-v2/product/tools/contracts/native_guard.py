"""Closed native carrier profile for the inert renderer, not native admission.

The caller verifies source pins and selects generated extern names first. Only
wire type declarations are resolved; prose/preimage annotations are not code.
Recursive native declarations are unselected in this finite carrier profile.
"""
import copy,re
from jsonschema import Draft202012Validator

class IdlRefusal(ValueError):pass

def refuse(code):raise IdlRefusal(code)
def identifier(value,pattern):
    if type(value) is not str or re.fullmatch(pattern,value) is None:refuse('IDL_NAME')

def admit(owner,meta,options):
    # Defensive copy gives the renderer a stable owned tree after validation.
    owner=copy.deepcopy(owner)
    if next(Draft202012Validator(meta).iter_errors(owner),None) is not None:refuse('IDL_SCHEMA')
    names=set(owner['scalars'])|set(owner['records'])
    if len(names)!=len(owner['scalars'])+len(owner['records']):refuse('IDL_NAME')
    for name in names:identifier(name,r'(Ts2|Rust3)[A-Z][A-Za-z0-9]*')
    selected={};selected_names={}
    for entry in options['entryPoints']:
        reference=entry['ref'];name=entry['typeName'];identifier(name,r'[A-Z][A-Za-z0-9]*')
        if reference in selected or name in selected_names:refuse('IDL_EXTERN_REGISTRY')
        selected[reference]=name;selected_names[name]=reference
    edges={name:set() for name in names};externs={}
    def visit(ty,origin,frame_slot=False):
        tag=ty['t']
        if tag=='ref':
            if ty['ref'] not in names:refuse('IDL_REFERENCE')
            if origin is not None:edges[origin].add(ty['ref'])
        elif tag=='extern':
            identifier(ty['generatedType'],r'[A-Z][A-Za-z0-9]*')
            if selected.get(ty['schemaRef'])!=ty['generatedType']:refuse('IDL_EXTERN')
            if ty['generatedType'] in names:refuse('IDL_EXTERN')
            externs[ty['schemaRef']]=ty['generatedType']
        elif tag=='nullable':visit(ty['of'],origin)
        elif tag=='array':visit(ty['items'],origin)
        elif tag=='frame-payload':
            # This marker is an inline envelope slot, not a reusable record type.
            # Protocol-loop edges below expand its actual payload declarations.
            # Adding origin->envelope here would self-cycle every valid frame.
            if ty['protocol'] not in owner['protocols']:refuse('IDL_PROTOCOL')
            if not frame_slot or origin!=owner['protocols'][ty['protocol']]['envelope']:refuse('IDL_PROTOCOL')
        elif tag not in ['uint64','text','bytes','bool','null']:refuse('IDL_TYPE')
    def field(name):identifier(name,r'[a-z][A-Za-z0-9]*')
    for name,row in owner['scalars'].items():visit(row['type'],name)
    for name,row in owner['records'].items():
        if row['kind']=='alias':visit(row['target'],name)
        elif row['kind']=='record':
            seen=set()
            for member in row['members']:
                field(member['name'])
                if member['name'] in seen:refuse('IDL_NAME')
                seen.add(member['name']);visit(member['type'],name,frame_slot=member['name']=='payload')
        else:
            field(row['discriminator'])
            for member in row['memberOrder']:field(member)
            for variant in row['variants'].values():
                for member,ty in variant.items():field(member);visit(ty,name)
    for protocol in owner['protocols'].values():
        if protocol['envelope'] not in owner['records']:refuse('IDL_PROTOCOL')
        for frame in protocol['frames']:
            payload=frame['payload']
            if 't' in payload:visit(payload,protocol['envelope'])
            else:
                for ty in payload['alternatives'].values():visit(ty,protocol['envelope'])
    active=set();done=set()
    def acyclic(name):
        if name in active:refuse('IDL_CYCLE')
        if name in done:return
        active.add(name)
        for target in sorted(edges[name]):acyclic(target)
        active.remove(name);done.add(name)
    for name in sorted(names):acyclic(name)
    return owner,{'nativeTypes':len(names),'externalTypes':dict(sorted(externs.items())),'recursiveDeclarationsSelected':False}
