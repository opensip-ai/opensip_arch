"""Exact product identity graph and lifecycle reference. Not a production evidence store."""
import copy,hashlib,importlib.util,json,re,unicodedata
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('identity_canonical',HERE/'canonical.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
SCHEMA=json.loads((HERE/'identity-schemas.v2.json').read_text())
DIGESTS=SCHEMA['x-opensip-digest-domains']
PAYLOADS=SCHEMA['x-opensip-payload-registry']
RELATION_SCHEMA_DOCUMENT=PAYLOADS['classes']['relation']['document']
RELATION_DOCUMENT=json.loads((HERE/'relation-payload-schemas.v2.json').read_text())
RELATIONS=RELATION_DOCUMENT['x-opensip-relation-registry']['relations']
RELATION_DIGEST_LAW=RELATION_DOCUMENT['x-opensip-digest-law']
PREFIX={'fact':'fact2','snapshot':'snapshot2','closure':'closure2','import':'import2','plan':'plan2','subject-scope':'scope2','coverage':'coverage2','view':'view2','execution-plan':'exec-plan2','finding-fingerprint':'finding-key2','finding':'finding2','proof-bundle':'proof2','semantic-evidence':'evidence2','evaluation-seal':'seal2','run':'run2','cache-key':'cache2','regeneration-key':'regen2','policy-derivation':'policy-derivation2'}
DOMAIN_OF={v:k for k,v in PREFIX.items()}
FRAME_PREFIX=b'opensip.product.v1\0'

_WORKFLOWS=None
def workflow_admission():
    """The workflow unit's own pinned-schema admission function. Identity does not restate a
    second policy/compiler language: the rule program, policy, waiver set, correspondence,
    build identity and observation records are admitted by their owning contract's schemas."""
    global _WORKFLOWS
    if _WORKFLOWS is None:
        spec=importlib.util.spec_from_file_location('identity_workflow_admission',HERE.parent/'workflows/workflows_model.v1.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);_WORKFLOWS=module
    return _WORKFLOWS

_NATIVE=None
def native_admission():
    """The native unit's own context admission and universe binding. Run closure re-runs them over
    the RETAINED frame and the RETAINED closure descriptors; it reads no producer ADMIT flag and
    re-executes no compiler, provider or filesystem. Loaded lazily so that the native model, which
    itself loads this module for `identifier`, does not create an import cycle."""
    global _NATIVE
    if _NATIVE is None:
        spec=importlib.util.spec_from_file_location('identity_native_admission',HERE.parent/'native/native_evidence_model.v2.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);_NATIVE=module
    return _NATIVE

_LOCAL_REGISTRY=None
def validate_registered_record(document,selector,value):
    """Validate a payload or record against a document + selector through a PINNED LOCAL registry
    closure with no network retrieval. Foundation-owned documents are resolved here; every other
    unit's documents are admitted by that unit's own admission function, so one record law has one
    implementation."""
    if not document.startswith('foundation/'):
        W=workflow_admission()
        try:W.validate_import_record(document,selector,value)
        except W.Refusal as exc:raise C.AdmissionError('REGISTERED_RECORD:'+selector) from exc
        return value
    global _LOCAL_REGISTRY
    if _LOCAL_REGISTRY is None:
        from referencing import Registry,Resource
        from referencing.jsonschema import DRAFT202012
        documents=[HERE/'identity-schemas.v2.json',HERE/'relation-payload-schemas.v2.json',
                   HERE/'import-source-context.schema.json']
        parsed=[json.loads(path.read_text()) for path in documents]
        _LOCAL_REGISTRY=(Registry().with_resources(
            (d['$id'],Resource(contents=d,specification=DRAFT202012)) for d in parsed),
            {str(path.relative_to(HERE.parent)):d for path,d in zip(documents,parsed)})
    registry,by_path=_LOCAL_REGISTRY
    if document not in by_path:raise C.AdmissionError('UNREGISTERED_DOCUMENT:'+document)
    C.typed(value)
    try:C.ExactValidator({'$ref':by_path[document]['$id']+selector},registry=registry).validate(value)
    except C.ValidationError as exc:raise C.AdmissionError('REGISTERED_RECORD:'+selector) from exc
    return value

def ordered(value,path=()):
    if type(value) is dict:
        for key,child in value.items():
            if key in ['path','logicalPath'] and type(child) is str:
                if child.startswith('/') or '\\' in child or '\x00' in child or any(x in ['', '.', '..'] for x in child.split('/')):raise C.AdmissionError('LOGICAL_PATH')
            ordered(child,path+(key,))
    elif type(value) is list:
        name=path[-1] if path else ''
        if name=='allowedScopes':keys=list(range(len(value)))
        elif name in ['sourceInventory','tree','blobs']:
            keys=[v['path'].encode('utf8') for v in value]
            for v in value:
                p=v['path']
                if p.startswith('/') or '\\' in p or '\x00' in p or any(x in ['', '.', '..'] for x in p.split('/')):raise C.AdmissionError('LOGICAL_PATH')
        elif name=='requires':keys=value
        elif name=='owner-source-set':keys=[v['ownerKey'].encode('utf8') for v in value]
        elif name=='stages':
            keys=[v['ordinal'] for v in value]
            if keys!=list(range(len(value))):raise C.AdmissionError('STAGE_ORDINAL')
            for v in value:
                if any(n>=v['ordinal'] for n in v['requires']):raise C.AdmissionError('STAGE_DAG')
        elif name=='predicateProofs':keys=[(v['ruleId'],v['subjectId'],v['predicateId']) for v in value]
        else:keys=[C.canonical(v) for v in value]
        if keys!=sorted(keys) or len(keys)!=len(set(keys)):raise C.AdmissionError('ORDER_OR_DUPLICATE')
        for i,child in enumerate(value):ordered(child,path+(str(i),))

ROOT_ORDER_PATH={'source-inventory':('sourceInventory',),'owner-source-set':('owner-source-set',)}

def identifier(domain,value):
    if domain not in PREFIX:raise C.AdmissionError('IDENTITY_DOMAIN')
    schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/'+domain
    C.validate(schema,value);ordered(value)
    _r=PREFIX[domain]+':'+C.identity(domain,value)
    import os as _os
    with open(_os.environ['CLAUDE_ID_TAP'],'a') as _f:_f.write(domain+'|'+_r+'\n')
    return _r


# --------------------------------------------------------------------------- digest law
# identity-and-evidence section 3 gives every 64-hex field in this bundle exactly one
# representation, declared by its `x-opensip-digest` schema annotation. Nothing below infers a
# representation from a field NAME: a `*Digest` spelling carries no meaning, and neither does a
# bare hex string. A field with no annotation is inadmissible.

def h_preimage_frame(domain,descriptor):
    """The exact H preimage. SHA256(frame) == H(domain,descriptor), so one content-addressed
    store keyed by raw SHA-256 retains raw artifacts, canonical records AND H identities."""
    raw=C.canonical(descriptor)
    if not domain or not all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-.' for c in domain):raise C.AdmissionError('DOMAIN')
    return FRAME_PREFIX+domain.encode('ascii')+b'\0'+len(raw).to_bytes(8,'big')+raw

def retain_h_identity(domain,descriptor,blobs):
    """Public API for a host or a sibling unit: retain the frame for a bare-hex h-identity field
    (plan.nativeContextDigests, fact/subject-scope source/targetUniverse) and return the bare hex."""
    frame=h_preimage_frame(domain,descriptor);digest=hashlib.sha256(frame).hexdigest()
    if digest!=C.identity(domain,descriptor):raise C.AdmissionError('H_FRAME_RECIPE')
    blobs[digest]=frame
    return digest

def parse_h_frame(frame,domain_set):
    """Exact frame parsing. A frame is admissible ONLY where the annotation says h-identity, and a
    raw canonical payload is never admissible there: C(X) does not start with the framing prefix,
    and SHA256(C(X)) is not H(D,X). This is a typed representation, not a blob escape."""
    registry=DIGESTS['domainSets'][domain_set]
    if type(frame) is not bytes or not frame.startswith(FRAME_PREFIX):raise C.AdmissionError('H_FRAME_PREFIX')
    rest=frame[len(FRAME_PREFIX):];cut=rest.find(b'\0')
    if cut<=0:raise C.AdmissionError('H_FRAME_DOMAIN')
    try:domain=rest[:cut].decode('ascii','strict')
    except UnicodeError as exc:raise C.AdmissionError('H_FRAME_DOMAIN') from exc
    if domain not in registry:raise C.AdmissionError('H_FRAME_DOMAIN_UNREGISTERED:'+domain)
    body=rest[cut+1:]
    if len(body)<8:raise C.AdmissionError('H_FRAME_LENGTH')
    declared=int.from_bytes(body[:8],'big');payload=body[8:]
    if declared!=len(payload):raise C.AdmissionError('H_FRAME_LENGTH')
    value=C.parse(payload)
    if C.canonical(value)!=payload:raise C.AdmissionError('H_FRAME_NONCANONICAL')
    row=registry[domain]
    W=workflow_admission()
    try:W.validate_import_record(row['document'],row['selector'],value)
    except W.Refusal as exc:raise C.AdmissionError('H_FRAME_RECORD:'+domain) from exc
    if C.identity(domain,value)!=hashlib.sha256(frame).hexdigest():raise C.AdmissionError('H_FRAME_IDENTITY')
    return domain,value,row

def parse_body_frame(raw):
    """The INHERITED fact-identity body frame, parsed exactly as
    fact-identity-policy.v2#/canonicalisationSchema/byteGrammar/domainSeparatedPreimage writes it:

        u8 len || domainTag | levelId | levelVersion (RAW 32 bytes) | languageId | languageVersion
        u32be len || payload

    Unframed concatenation is forbidden by that policy, so a frame with trailing bytes, a short
    field or a length that overruns is refused rather than tolerated."""
    if type(raw) is not bytes:raise C.AdmissionError('BODY_FRAME_BYTES')
    fields=[];position=0
    for _ in range(5):
        if position>=len(raw):raise C.AdmissionError('BODY_FRAME_TRUNCATED')
        length=raw[position];position+=1
        if position+length>len(raw):raise C.AdmissionError('BODY_FRAME_TRUNCATED')
        fields.append(raw[position:position+length]);position+=length
    if position+4>len(raw):raise C.AdmissionError('BODY_FRAME_TRUNCATED')
    declared=int.from_bytes(raw[position:position+4],'big');position+=4
    payload=raw[position:position+declared];position+=declared
    if len(payload)!=declared or position!=len(raw):raise C.AdmissionError('BODY_FRAME_TRAILING')
    return fields+[payload]

def parse_token_stream(raw):
    """The inherited framedTokenStream: `u32be token_count || token*`, each token
    `u16be kind_id_len || kind_id || u32be value_len || value`. Parsing it proves the retained L1-L3
    payload is a well-formed stream in the pinned framing and is held in full. It judges no
    tokenisation: what a token kind MEANS is the provider's, and this closure never grades it."""
    if len(raw)<4:raise C.AdmissionError('BODY_TOKEN_STREAM_TRUNCATED')
    count=int.from_bytes(raw[:4],'big');position=4;tokens=[]
    for _ in range(count):
        if position+2>len(raw):raise C.AdmissionError('BODY_TOKEN_STREAM_TRUNCATED')
        kind_length=int.from_bytes(raw[position:position+2],'big');position+=2
        if position+kind_length+4>len(raw):raise C.AdmissionError('BODY_TOKEN_STREAM_TRUNCATED')
        kind=raw[position:position+kind_length];position+=kind_length
        value_length=int.from_bytes(raw[position:position+4],'big');position+=4
        if position+value_length>len(raw):raise C.AdmissionError('BODY_TOKEN_STREAM_TRUNCATED')
        tokens.append((kind,raw[position:position+value_length]));position+=value_length
    if position!=len(raw):raise C.AdmissionError('BODY_TOKEN_STREAM_TRAILING')
    return tokens

def body_language_version(universe,context,row,anchor,retained=None):
    """Build the `body-language-version` record for one body span.

    The inherited policy requires the frame's languageVersion component to be "canonical identity
    bytes supplied by ResolvedInputs/PlanId, not a human display string", for "the provider
    interpreting the body span". That provider is the COMPILER, and its identity is not missing and
    never was: the universe's own `nativeContextId` - a reference Run closure already requires to be
    Plan-selected - reaches the admitted retained context, whose `toolchain` carries
    `rustcVersion`/`rustCommitHash` for Rust and `compilerName`/`compilerVersion`/
    `compilerPackageDigest` for TypeScript. Following an existing admitted reference needed no new
    universe field, and the compiler half of this added none.

    What goes in is the compiler identity plus the selected source DIALECT. What stays out is
    operational platform, paths, names, resolution inputs, build tooling and option synthesis; the
    registry row lists every exclusion with its reason. Dialect is body specific and is SELECTED,
    never collected: Rust's is the edition of the compilation unit that owns this body's path,
    TypeScript's is the source variant that body's own suffix denotes. Paths and crate names
    establish that selection and then do not enter the record.

    Every branch that cannot determine a dialect REFUSES with a distinct cause. None guesses.

    Pure: it reads already-retained records, the enclosing fact's own anchor and the registry row,
    and touches no Run state."""
    binding=row.get('languageVersionBinding')
    if binding is None:raise C.AdmissionError('BODY_LANGUAGE_UNIVERSE_UNBOUND:'+row['language'])
    record={'schemaVersion':1}
    for name,source in binding['fields'].items():
        if 'const' in source:record[name]=source['const'];continue
        node=context if source['source']=='native-context' else universe
        for step in source['path']:node=node[step]
        record[name]=node
    dialect=binding['dialect']
    if dialect['form']=='closed-suffix-table':
        # The source VARIANT the body's own file suffix denotes. Longest matching suffix wins, so
        # `.d.ts` is never read as `.ts`; an unlisted suffix refuses rather than being folded into a
        # neighbouring variant. Deliberately conservative: distinct variants are kept distinct, so
        # this can fail to equate two bodies a language expert would call the same, and can never
        # equate two the language reads differently. Collapsing variants is a claim about a parser
        # and belongs to the level specification, not here.
        matches=[suffix for suffix in dialect['table'] if anchor['path'].endswith(suffix)]
        if not matches:raise C.AdmissionError(dialect['onUnknown']+':'+anchor['path'])
        variant=dialect['table'][max(matches,key=len)]
        record['dialect']={dialect['key']:variant}
        # The BODY language, from the same selector over the same anchor. The universe language is
        # the ENGINE that reads the body; one TypeScript engine produces typescript AND javascript
        # bodies, and native 6.3 requires each to carry its own identifier.
        record['languageId']=binding['bodyLanguageByVariant'][variant]
    elif dialect['form']=='selected-compilation-target-edition':
        record['languageId']=binding['bodyLanguage']
        node=universe
        for step in dialect['path']:node=node[step]
        if not node:raise C.AdmissionError(dialect['onEmpty']+':'+record['languageId'])
        # NO fast path. A target may override its package default edition, so package defaults that
        # all agree still do not determine the body's dialect; the committed ownership relation does.
        spec=dialect['ownership'];ownership=(retained or {}).get(spec['retainedAs'])
        if ownership is None:raise C.AdmissionError(dialect['onOwnershipMissing']+':'+str(len(node)))
        # Enumeration FIRST, before any row is looked at. Under `partial` an owner inside the
        # selected scope may exist that was never listed and could contradict a listed one, so
        # incomplete discovery can never act as an implicit edition selection by hiding it.
        if ownership[spec['enumerationField']]!='complete':
            raise C.AdmissionError(dialect['onOwnerUnenumerated']+':'+anchor['path'])
        units={unit[spec['unitField']]:unit for unit in ownership[spec['unitsField']]}
        rows=[r for r in ownership['ownership'] if r[spec['pathField']]==anchor['path']]
        if not rows:raise C.AdmissionError(dialect['onOwnerNotCompiled']+':'+anchor['path'])
        # The EXPLICIT selection. A path compiled only by unselected targets refuses rather than
        # borrowing an out-of-scope edition, and a selection is committed in this record's identity,
        # so choosing differently is a different universe rather than a different reading of one.
        selected=set(ownership[spec['selectionField']])
        chosen=[r for r in rows if r[spec['unitField']] in selected]
        if not chosen:raise C.AdmissionError(dialect['onOwnerNotSelected']+':'+anchor['path'])
        unknown=sorted({r[spec['unitField']] for r in chosen if r[spec['unitField']] not in units})
        if unknown:raise C.AdmissionError(dialect['onOwnerAmbiguous']+':unknown-unit:'+','.join(unknown))
        # EFFECTIVE edition per selected target: its own when it states one, the package default when
        # it does not. Selected owners that AGREE are admissible - the ordinary shared-file and
        # lib-plus-test-target case. Selected owners that DISAGREE are an ambiguous unselected
        # request: one body identity cannot represent two dialects, so it refuses.
        effective=set()
        for row in chosen:
            unit=units[row[spec['unitField']]]
            if unit[spec['targetEditionField']] is not None:effective.add(unit[spec['targetEditionField']])
            elif unit[spec['crateField']] not in node:
                raise C.AdmissionError(dialect['onOwnerAmbiguous']+':unknown-crate:'+unit[spec['crateField']])
            else:effective.add(node[unit[spec['crateField']]])
        if len(effective)>1:
            raise C.AdmissionError(dialect['onOwnerAmbiguous']+':'+anchor['path']+':'+str(len(effective)))
        record['dialect']={dialect['key']:next(iter(effective))}
    else:raise C.AdmissionError('BODY_LANGUAGE_DIALECT_FORM:'+str(dialect.get('form')))
    schema=copy.deepcopy(SCHEMA);schema['$ref']=binding['record']
    C.validate(schema,record)
    return record

# The three scalar forms the relation document GOVERNS. They are the exact counterpart of the native
# bundle's hexish/refs pair: a field of one of these forms carries a digest or a repository path, so
# the closing digest law requires it to declare a representation, a retention and an authority.
GOVERNED_RELATION_FORMS=('DigestHex','Sha256Text','CanonicalPath')

def annotation_already_collected(annotation,collected):
    """The ONE equality rule for annotations, used at every stage that compares them.

    Annotation equality is TYPED CANONICAL equality, which is what the contract says and what the
    conflict limb has always used. Python `==` is not that rule: `1 == True` is true while
    `C({...ordinal: 1})` and `C({...ordinal: true})` are different registered bytes. An earlier
    revision used `C.equal_typed` only in the same-path merge while collection and alias inheritance
    still used `not in`, so a typed-DISTINCT annotation could be dropped during collection and the
    conflict check never saw the pair. Collection, alias inheritance, branch and container
    propagation, the same-path merge and the conflict check now all route through here, so they
    cannot drift apart again."""
    return any(C.equal_typed(annotation,other) for other in collected)

def relation_digest_annotation_coverage(document=None):
    """The relation counterpart of native_digest_annotation_coverage, and the THIRD limb of the
    residue rule made consumable.

    The law states three inadmissible conditions: an annotated field with no join, a join naming a
    field the selector does not have, and AN UNANNOTATED DIGEST OR PATH FIELD. The first two are
    decidable by walking the annotations; the third is not, by construction - a function that
    iterates the fields which already carry `x-opensip-digest` can never see a field that carries
    none. That is why this sweep exists and why it walks the SCHEMA rather than the annotations.

    A governed field is recognised two ways, because either would otherwise be a hole: a `$ref` to
    one of the governed `$defs`, resolved TRANSITIVELY so an alias `$def` that itself refs a governed
    form is still governed; and an inline `pattern` equal to a governed form's own, so copying the
    pattern instead of referencing it does not evade the sweep.

    An `x-opensip-digest` anywhere on the path to a governed leaf covers it. Both shipped documents
    need that: this one annotates the PARENT property that carries the `$ref`, while the native
    bundle annotates the BRANCH inside a nullable `oneOf`. Descending `oneOf`/`anyOf`/`allOf`,
    `items` and nested `properties` is what makes nullable, array-valued and nested governed fields
    visible rather than silently uncovered.

    Pure and schema-only, like its neighbour: it decides LAW COHERENCE, never snapshot truth."""
    document=RELATION_DOCUMENT if document is None else document
    defs=document.get('$defs',{})
    governed_patterns={name:defs[name].get('pattern') for name in GOVERNED_RELATION_FORMS if name in defs}
    def governed_form(node,chain=()):
        """The governed form this schema node denotes, and every annotation on the $REF CHAIN that
        reaches it.

        The chain is part of the path, so the stated rule - an `x-opensip-digest` anywhere on the
        path to a governed leaf is that leaf's annotation - has to include an INTERMEDIATE alias
        `$def`. An annotation on the terminal governed `$def` itself deliberately does NOT count:
        that would be a blanket exemption for every field of that form in every relation, which is
        the very hole this law closes, rather than a declaration about one field."""
        if type(node) is not dict:return None,[]
        here=[node['x-opensip-digest']] if 'x-opensip-digest' in node else []
        reference=node.get('$ref')
        if isinstance(reference,str) and reference.startswith('#/$defs/'):
            target=reference.split('/')[-1]
            if target in governed_patterns:return target,here
            if target in defs and target not in chain:
                form,inherited=governed_form(defs[target],chain+(target,))
                if form is not None:return form,here+inherited
        pattern=node.get('pattern')
        if isinstance(pattern,str):
            for name,governed in governed_patterns.items():
                if governed is not None and pattern==governed:return name,here
        return None,[]
    seen={}
    def record(path,form,field,joinable,annotations):
        """One sighting. If ANY schema that reaches this path declares no annotation, the path is
        unannotated - whichever order the walker happened to visit them in.

        `missing` is that fact, carried explicitly and MONOTONICALLY: once some sighting arrived
        with no annotation, no later sighting can undo it. The earlier version tried to express this
        by testing the annotation list, but it REBOUND that list to the merged one before testing it,
        so `not annotations` was true only when both sides were empty and the rule collapsed to
        "poison iff the FIRST-recorded sighting was unannotated" - a visit-order dependence, which is
        the opposite of what this docstring claimed. Keeping the merged list and the missing flag as
        separate facts is what makes "no new annotation" distinguishable from "already merged".

        The merged list itself is still accumulated rather than discarded, so a conflict between two
        annotations at one path stays diagnosable even when the path is also poisoned."""
        missing=not annotations
        previous=seen.get(path)
        merged=list(previous['annotations']) if previous is not None else []
        for annotation in annotations:
            if not annotation_already_collected(annotation,merged):merged.append(annotation)
        if previous is not None:
            form=previous['form'] or form
            joinable=previous['joinable'] and joinable
            missing=previous['missing'] or missing
        seen[path]={'path':path,'form':form,'field':field,'joinable':joinable,
                    'annotations':merged,'missing':missing}
    def walk(node,path,inherited,field,joinable,chain=()):
        if type(node) is list:
            for item in node:walk(item,path,inherited,field,joinable,chain)
            return
        if type(node) is not dict:return
        if 'x-opensip-digest' in node and not annotation_already_collected(node['x-opensip-digest'],inherited):
            inherited=inherited+[node['x-opensip-digest']]
        form,on_chain=governed_form(node)
        if form is not None:
            record(path,form,field,joinable,
                   inherited+[a for a in on_chain if not annotation_already_collected(a,inherited)])
            return
        # A $ref that is not a governed scalar may name a CONTAINER, and its members are governed
        # fields of this selector just as an inline object's are. Following it is what makes an
        # unannotated leaf behind an alias visible; the chain guard keeps a recursive $def finite.
        reference=node.get('$ref')
        if isinstance(reference,str) and reference.startswith('#/$defs/'):
            target=reference.split('/')[-1]
            if target in defs and target not in chain:
                walk(defs[target],path,inherited,field,joinable,chain+(target,))
        for key,child in node.items():
            if key=='properties' and type(child) is dict:
                for name,schema in child.items():
                    # The FIRST properties step names the selector property a join row can address.
                    # Any deeper one is a nested member: `value[field]` yields an object there, so no
                    # join reaches it and the sighting is unjoinable.
                    walk(schema,path+'.'+name,inherited,field if field is not None else name,
                         joinable and field is None,chain)
            elif key in ('items','additionalProperties'):
                # `value[field]` yields a list or a map here, not a scalar, so no join addresses it.
                walk(child,path+'[]',inherited,field,False,chain)
            elif key in ('oneOf','anyOf','allOf') and type(child) is list:
                # Each branch gets its own path, because branches are ALTERNATIVES rather than one
                # value: an annotated branch must not cover an unannotated one beside it. A parent
                # annotation still reaches every branch through `inherited`, which is the nullable
                # `oneOf` shape both shipped documents use. Taking a branch still yields the scalar
                # at `value[field]`, so a branch sighting stays joinable.
                for index,branch in enumerate(child):
                    walk(branch,path+'|'+key+'['+str(index)+']',inherited,field,joinable,chain)
            elif key in ('oneOf','anyOf','allOf'):walk(child,path,inherited,field,joinable,chain)
    for name,row in document['x-opensip-relation-registry']['relations'].items():
        selector=document['$defs'][row['selector'].split('/')[-1]]
        walk(selector,name,[],None,True,())
        # A DIRECTLY annotated property is a sighting whether or not it is governed: the law's
        # residue and retention limbs are triggered by the annotation, not by the form. This is what
        # keeps `file.byteLength` - annotated, but a UInt64 - inside those two limbs while correctly
        # outside the governed count.
        for field,schema in selector.get('properties',{}).items():
            if type(schema) is dict and 'x-opensip-digest' in schema:
                path=name+'.'+field
                if path not in seen:
                    seen[path]={'path':path,'form':None,'field':field,'joinable':True,
                                'annotations':[schema['x-opensip-digest']],'missing':False}
    by_relation={}
    for path,sighting in seen.items():
        relation=path.split('.')[0].split('|')[0].split('[')[0]
        entry=by_relation.setdefault(relation,{'annotated':0,'unannotated':[],'sightings':[]})
        entry['sightings'].append(sighting)
        if sighting['form'] is None:continue
        if sighting['annotations'] and not sighting['missing']:entry['annotated']+=1
        else:entry['unannotated'].append(path+':'+sighting['form'])
    governed=[s for s in seen.values() if s['form'] is not None]
    return {'total':len(governed),
            'annotated':sum(1 for s in governed if s['annotations'] and not s['missing']),
            'unannotated':sorted(s['path']+':'+s['form'] for s in governed
                                 if s['missing'] or not s['annotations']),
            'governedForms':list(GOVERNED_RELATION_FORMS),'byRelation':by_relation,
            'sightings':sorted(seen.values(),key=lambda s:s['path'])}

_RELATION_LAW_CLOSURE={}
def relation_annotation_closure(name,document=None):
    """Consume the relation digest law rather than declare it.

    All THREE limbs of the residue rule, each with its own cause. Every governed digest or path
    field of a relation's selector must carry an `x-opensip-digest` at all; every annotated field
    must be reachable from that relation's registry joins, or must declare `retention: not-joined`
    with its stated reason; and every field a join names must exist in the selector. The law leaves
    no residue and has no default, and the third limb is checked FIRST because an unannotated field
    is by construction invisible to the other two.

    This is decidable from the SCHEMA alone, which is why it lives here as a pure function: a helper
    holding only the payload and the registry can decide LAW COHERENCE. It can never decide SNAPSHOT
    TRUTH, and the closure below - which owns the snapshot, the retained blobs and the owning fact -
    is the only place that does.

    `document` is the registered relation document; it is a parameter rather than a global read so
    that a caller can ask the question of a HYPOTHETICAL document without mutating this module."""
    registered=document is None
    document=RELATION_DOCUMENT if registered else document
    if registered and name in _RELATION_LAW_CLOSURE:return _RELATION_LAW_CLOSURE[name]
    law=document['x-opensip-digest-law']
    row=document['x-opensip-relation-registry']['relations'][name]
    properties=document['$defs'][row['selector'].split('/')[-1]]['properties']
    # ONE ACCOUNT OF EFFECTIVE ANNOTATIONS, used by every limb. v7 gave the coverage limb an
    # inherited notion of "annotated" - property, enclosing branch parent, or intermediate alias
    # $def - while retention and residue still read properties[field]['x-opensip-digest'] directly.
    # So exactly at the locations the traversal newly accepted, a field escaped both earlier limbs:
    # a dangling `preimage` with no join and an invented retention value were both admitted. Every
    # limb now reads the same sightings.
    sightings=relation_digest_annotation_coverage(document)['byRelation'].get(name,{}).get('sightings',[])
    named=set();exempt=set()
    for join in row['snapshotJoins']:
        named|={join[key] for key in ('pathField','digestField','lengthField','anchorPathField') if key in join}
        if 'unless' in join:named.add(join['unless']['field'])
    body=row.get('bodyIdentityJoin')
    if body:named|={body['field'],body['levelField'],body['levelVersionField']}
    # A path is unannotated if ANY schema reaching it declared none - the monotonic `missing` fact -
    # even when another schema at the same path did annotate it.
    uncovered=sorted(s['path']+':'+s['form'] for s in sightings
                     if s['form'] is not None and (s['missing'] or not s['annotations']))
    if uncovered:raise C.AdmissionError('RELATION_DIGEST_UNANNOTATED:'+name+':'+','.join(uncovered))
    for sighting in sorted(sightings,key=lambda s:s['path']):
        if sighting.get('missing'):continue
        distinct=[]
        for annotation in sighting['annotations']:
            if not annotation_already_collected(annotation,distinct):distinct.append(annotation)
        if not distinct:continue
        # The law states no precedence between an annotation on a property and one on the alias it
        # refs, so none is invented: two that DISAGREE are a conflict, not a silent winner. Two that
        # are identical are not a conflict.
        if len(distinct)>1:
            raise C.AdmissionError('RELATION_DIGEST_ANNOTATION_CONFLICT:'+name+':'+sighting['path'])
        retention=distinct[0].get('retention')
        if retention not in law['retention']:
            raise C.AdmissionError('RELATION_DIGEST_RETENTION:'+name+'.'+sighting['field'])
        if retention=='not-joined':
            exempt.add(sighting['field']);continue
        # A join row reads value[field]. That reaches a scalar at a property, and a scalar inside a
        # `oneOf` branch of that property, but never a member of a nested object or an array element,
        # where value[field] yields an object or a list. Rather than let a join row appear to address
        # something it cannot reach, an unjoinable location must declare `not-joined`.
        if not sighting['joinable']:
            raise C.AdmissionError('RELATION_DIGEST_UNJOINABLE_LOCATION:'+name+':'+sighting['path'])
        if sighting['field'] not in named:
            raise C.AdmissionError('RELATION_DIGEST_LAW_RESIDUE:'+name+':'+sighting['field'])
    unknown=named-set(properties)
    if unknown:raise C.AdmissionError('RELATION_JOIN_FIELD_UNKNOWN:'+name+':'+','.join(sorted(unknown)))
    if registered:_RELATION_LAW_CLOSURE[name]=row
    return row

def native_context_frame(domain,descriptor,blobs):
    """Exact API for the integration host: retain an admitted native context so a Plan that names
    its bare hex in nativeContextDigests can close. `descriptor` is the retained context bytes the
    native admission was minted from; no caller-supplied ADMIT flag is read here or later."""
    if domain not in DIGESTS['domainSets']['native-context']:raise C.AdmissionError('NATIVE_CONTEXT_DOMAIN')
    return retain_h_identity(domain,descriptor,blobs)

def native_universe_frame(domain,descriptor,blobs):
    if domain not in DIGESTS['domainSets']['native-semantic-universe']:raise C.AdmissionError('NATIVE_UNIVERSE_DOMAIN')
    return retain_h_identity(domain,descriptor,blobs)


# --------------------------------------------------------------------------- rule-program addressing
def predicate_child_addresses(node,address):
    if node['op'] in ('and','or'):return [address+'.'+str(i) for i in range(len(node['operands']))]
    if node['op']=='not':return [address+'.0']
    return []

def predicate_node_at(root,address):
    """`p` is the rule's emitWhen root; `a.i` is the i-th operand of the and/or node at `a`;
    `a.0` is the operand of the not node at `a`. Shortest decimal, no leading zero."""
    parts=address.split('.')
    if parts[0]!='p':raise C.AdmissionError('PREDICATE_ADDRESS')
    node=root
    for part in parts[1:]:
        if not part.isdigit() or (len(part)>1 and part[0]=='0'):raise C.AdmissionError('PREDICATE_ADDRESS')
        children=predicate_child_addresses(node,'p')
        if not children:raise C.AdmissionError('PREDICATE_ADDRESS_LEAF')
        index=int(part)
        operands=node['operands'] if node['op'] in ('and','or') else [node['operand']]
        if index>=len(operands):raise C.AdmissionError('PREDICATE_ADDRESS_RANGE')
        node=operands[index]
    return node


class EvidenceUnavailable(C.AdmissionError):
    """Missing bytes promised by an admitted closure are retention/custody loss, not a false predicate."""
    def __init__(self, reference):
        self.reference = reference
        self.termination = {'class':'operational-failed', 'errorCode':'HOST.IO_FAILURE', 'faultCause':'host-io',
            'domainDetail':{'code':'evidence.missing','remedy':'Restore the exact retained closure bytes or report their unavailability.','subject':reference}}
        super().__init__('EVIDENCE_UNAVAILABLE:' + reference)

class RegenerationMismatch(C.AdmissionError):
    def __init__(self, run_id):
        self.termination = {'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io',
            'domainDetail':{'code':'evidence.regeneration-mismatch','remedy':'Retain the sealed Run and investigate the differing regeneration result.','subject':run_id}}
        super().__init__('REGENERATION_MISMATCH')


def close_run(run,objects,blobs):
    """objects maps exact typed identity to (domain, descriptor). No caller ID is trusted."""
    return open_run_closure(run,objects,blobs)[0]


def open_run_closure(run,objects,blobs):
    """close_run, plus the admitted closure's own resolvers. Callers that must admit something
    ELSE against exactly the Run's closure (a cache or regeneration hit) use these rather than a
    second, weaker implementation."""
    run_id=identifier('run',run)
    def get(key,domain):
        if key not in objects:raise EvidenceUnavailable(key)
        actual_domain,value=objects[key]
        if actual_domain!=domain or identifier(domain,value)!=key:raise C.AdmissionError('REFERENCE_IDENTITY')
        return value
    seen=set();parsed={};native_contexts={};native_universes={};capability_ids=set()

    # ----------------------------------------------------------------- schema-driven closure walk
    def deref(node):
        depth=0
        while type(node) is dict and '$ref' in node:
            ref=node['$ref']
            if not ref.startswith('#/$defs/'):raise C.AdmissionError('EXTERNAL_SCHEMA_REF')
            merged=dict(SCHEMA['$defs'][ref.split('/')[-1]])
            merged.update({k:v for k,v in node.items() if k!='$ref'})
            node=merged;depth+=1
            if depth>8:raise C.AdmissionError('SCHEMA_REF_DEPTH')
        return node
    scalar={'string':str,'integer':int,'boolean':bool,'object':dict,'array':list}
    def branch_matches(node,value):
        kind=node.get('type')
        if kind=='null':return value is None
        if kind in scalar:
            if kind=='integer' and type(value) is bool:return False
            return type(value) is scalar[kind]
        return True
    def carries_digest(node):
        if type(node) is dict:
            if 'x-opensip-digest' in node:return True
            if type(node.get('pattern')) is str and node['pattern'].split(':')[0][1:] in DOMAIN_OF:return True
            if '$ref' in node and node['$ref'].startswith('#/$defs/'):return carries_digest(SCHEMA['$defs'][node['$ref'].split('/')[-1]])
            return any(carries_digest(v) for v in node.values())
        if type(node) is list:return any(carries_digest(v) for v in node)
        return False
    def walk(node,value,siblings=None):
        node=deref(node)
        if 'oneOf' in node:
            options=[deref(x) for x in node['oneOf']]
            hits=[x for x in options if branch_matches(x,value)]
            if len(hits)!=1:
                if any(carries_digest(x) for x in options):raise C.AdmissionError('AMBIGUOUS_DIGEST_BRANCH')
                return
            node={**{k:v for k,v in node.items() if k!='oneOf'},**hits[0]}
        annotation=node.get('x-opensip-digest')
        if value is None:return
        if type(value) is str:
            if annotation is not None:return digest_field(annotation,value,siblings)
            head=value.split(':',1)[0]
            if head in DOMAIN_OF and str(node.get('pattern','')).startswith('^'+head+':'):visit(value,DOMAIN_OF[head])
            return
        if type(value) is list:
            items=node.get('items')
            if items is None:
                if carries_digest(node):raise C.AdmissionError('UNTYPED_DIGEST_ARRAY')
                return
            for item in value:walk(items,item,siblings)
            return
        if type(value) is dict:
            properties=node.get('properties',{});extra=node.get('additionalProperties')
            for name,item in value.items():
                child=properties.get(name)
                if child is None:child=extra if type(extra) is dict else None
                if child is None:
                    if carries_digest(node):raise C.AdmissionError('UNDECLARED_PROPERTY:'+name)
                    continue
                walk(child,item,value)
            if set(value)=={'path','sha256','bytes'} and len(blob(value['sha256']))!=value['bytes']:raise C.AdmissionError('BLOB_LENGTH')
            return
    def digest_field(annotation,value,siblings):
        representation=annotation['representation']
        retention=annotation.get('retention','preimage')
        if retention not in DIGESTS['retention']:raise C.AdmissionError('DIGEST_RETENTION')
        if retention in ('fragment','owner-retained'):
            # fragment: recomputed at its stated location by an explicit join below.
            # owner-retained: the named owning contract retains and admits the bytes.
            return
        if representation=='raw-artifact':blob(value);return
        if representation=='capability-manifest-id':capability_ids.add(value);return
        if representation=='by-domain':
            if type(siblings) is not dict or 'domain' not in siblings:raise C.AdmissionError('REF_DOMAIN_MISSING')
            row=DIGESTS['byDomain'].get(siblings['domain'])
            if row is None:raise C.AdmissionError('REF_DOMAIN_UNREGISTERED:'+str(siblings['domain']))
            return digest_field(row,value,siblings)
        if representation=='h-identity':
            if 'domain' in annotation:return visit(PREFIX[annotation['domain']]+':'+value,annotation['domain'])
            return admit_frame(value,annotation['domainSet'])
        if representation=='canonical-record':
            record=annotation['record']
            if 'bundle' in record:return payload(value,record['selector'].split('/')[-1])
            if 'document' in record:return foreign_payload(value,record['document'],record['selector'])
            if 'payloadClass' in record:
                if 'resolvedThrough' in record:raise C.AdmissionError('PAYLOAD_DOMAIN_REF_NOT_A_ROOT:'+record['payloadClass'])
                if type(siblings) is not dict:raise C.AdmissionError('PAYLOAD_CONTEXT_MISSING')
                return registered_payload(value,record,siblings)

        raise C.AdmissionError('DIGEST_REPRESENTATION')
    def blob(digest):
        if digest not in blobs:raise EvidenceUnavailable(digest)
        raw=blobs[digest]
        if type(raw) is not bytes or hashlib.sha256(raw).hexdigest()!=digest:raise C.AdmissionError('BLOB_DIGEST')
        return raw
    def canonical_bytes(digest,fault):
        raw=blob(digest);value=C.parse(raw)
        if C.canonical(value)!=raw:raise C.AdmissionError(fault)
        return value
    def payload(digest,kind):
        """A canonical-record digest under a record registered in THIS bundle."""
        if ('local',digest,kind) in parsed:return parsed[('local',digest,kind)]
        value=canonical_bytes(digest,'NONCANONICAL_AUXILIARY')
        schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/'+kind;C.validate(schema,value)
        if kind!='semantic-configuration':ordered(value,ROOT_ORDER_PATH.get(kind,()))
        if kind=='scope-descriptor':
            for name in ['workspaceRoots','pathPrefixes','excludedPathPrefixes']:
                for path in value[name]:
                    if path!='.' and (path.startswith('/') or '\\' in path or '\x00' in path or any(v in ['', '.', '..'] for v in path.split('/'))):raise C.AdmissionError('SCOPE_LOGICAL_PATH')
        parsed[('local',digest,kind)]=value
        walk(SCHEMA['$defs'][kind],value)
        return value
    def foreign_payload(digest,document,selector):
        """A canonical-record digest under a record registered by another unit's pinned schema."""
        if ('foreign',digest,document,selector) in parsed:return parsed[('foreign',digest,document,selector)]
        value=canonical_bytes(digest,'NONCANONICAL_FOREIGN_RECORD')
        W=workflow_admission()
        try:W.validate_import_record(document,selector,value)
        except W.Refusal as exc:raise C.AdmissionError('FOREIGN_RECORD:'+selector) from exc
        parsed[('foreign',digest,document,selector)]=value
        return value
    def registry_row(payload_class,key,siblings,value):
        """The closed x-opensip-payload-registry row for a payload. There is no default row, no
        caller-selected schema and no guess: a key with no row refuses. `payloadSchemaDigest` is the
        raw SHA-256 of the row document's EXACT FULL bytes and validation is by the row SELECTOR, so
        a multi-record bundle is admitted through its row and never needs a root type."""
        registry=PAYLOADS['classes'][payload_class]
        if payload_class=='relation':
            if key[0] not in RELATIONS:raise C.AdmissionError('PAYLOAD_RELATION_UNREGISTERED:'+str(key[0]))
            row=relation_annotation_closure(key[0])
            return {'document':registry['document'],'selector':row['selector'],'relation':row}
        if payload_class=='import':
            W=workflow_admission()
            owner=W.registry_row(key[0],key[1])
            declared=registry['rows'].get(str(key[0])+'|'+str(key[1]))
            if owner is None or declared is None:raise C.AdmissionError('PAYLOAD_IMPORT_UNREGISTERED:'+str(key))
            if owner['schemaDocument']!=declared['document'] or owner['selector']!=declared['selector']:
                raise C.AdmissionError('PAYLOAD_IMPORT_REGISTRY_DRIFT:'+str(key))
            return {'document':declared['document'],'selector':declared['selector']}
        if payload_class=='parameter':
            # Keyed by the cited schema DIGEST: the document must be one on the closed list, so a
            # caller cannot cite a permissive or unregistered schema for a Plan parameter.
            for row in registry['rows'].values():
                if hashlib.sha256((HERE.parent/row['document']).read_bytes()).hexdigest()==key[0]:
                    return {'document':row['document'],'selector':row['selector']}
            raise C.AdmissionError('PAYLOAD_PARAMETER_UNREGISTERED:'+str(key[0]))
        row=registry['rows'].get(str(key[0]))
        if row is None:raise C.AdmissionError('PAYLOAD_'+payload_class.upper()+'_UNREGISTERED:'+str(key[0]))
        return {'document':row['document'],'selector':row['selector']}
    def registered_payload(digest,record,siblings):
        """A payload admitted through the closed payload registry.

        The DECODE is cacheable; the ADMISSION is not. Registry-row selection, the schema-document
        digest, the relation rung and the universe rule are all context sensitive - two facts can
        share one canonical payload and still owe different admissions - so every one of them runs
        on every reference, and only the parsed canonical bytes are memoized."""
        schema_digest=siblings[record['schemaDigestField']]
        memo=('payload-decode',digest)
        if memo in parsed:value=parsed[memo]
        else:
            value=canonical_bytes(digest,'NONCANONICAL_REGISTERED_PAYLOAD');parsed[memo]=value
        key=[]
        for name in record['keyedBy']:
            if name.startswith('payload.'):
                key.append(value.get(name[len('payload.'):]) if type(value) is dict else None)
            elif name in siblings:key.append(siblings[name])
            else:raise C.AdmissionError('PAYLOAD_KEY_MISSING:'+name)
        row=registry_row(record['payloadClass'],key,siblings,value)
        document=HERE.parent/row['document']
        if hashlib.sha256(document.read_bytes()).hexdigest()!=schema_digest:
            raise C.AdmissionError('PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT:'+row['document'])
        blob(schema_digest)
        try:validate_registered_record(row['document'],row['selector'],value)
        except C.AdmissionError as exc:raise C.AdmissionError('PAYLOAD_RECORD:'+row['selector']) from exc
        if record['payloadClass']=='relation':relation_payload_rules(value,row['relation'],siblings)
        return value
    def relation_payload_rules(value,row,fact):
        """The inherited relation laws, now schema-expressed and re-checked here: the rung ladder,
        each rung's required/forbidden fields, the universe rule, and the no-negative-integer and
        NFC text restrictions the superseded CBOR profile carried."""
        if fact['resolution'] not in row['rungs'] and row['rungs']:
            raise C.AdmissionError('RELATION_RUNG_NOT_IN_LADDER:'+fact['relation']+'@'+fact['resolution'])
        rung=row['rungs'].get(fact['resolution'],{'required':[],'forbidden':[]})
        for name in rung['required']:
            if name not in value:raise C.AdmissionError('RELATION_RUNG_REQUIRED_FIELD:'+name)
        for name in rung['forbidden']:
            if name in value:raise C.AdmissionError('RELATION_RUNG_FORBIDDEN_FIELD:'+name)
        if row['universeRule']=='same-only' and fact['sourceUniverse']!=fact['targetUniverse']:
            raise C.AdmissionError('RELATION_UNIVERSE_RULE:same-only')
        def scan(node):
            if type(node) is bool:return
            if type(node) is int and node<0:raise C.AdmissionError('RELATION_PAYLOAD_NEGATIVE_INTEGER')
            if type(node) is str and unicodedata.normalize('NFC',node)!=node:raise C.AdmissionError('RELATION_PAYLOAD_NOT_NFC')
            if type(node) is dict:
                for name,child in node.items():scan(name);scan(child)
            if type(node) is list:
                for child in node:scan(child)
        scan(value)
        relation_source_joins(value,row,fact)
    def coverage_dialect_prerequisite(scope,coverage_payload):
        """A Coverage claim about a relation whose payload needs a body dialect must be consistent
        with whether this universe can produce one AT ALL.

        Payload-only validation cannot see this and neither can the producer boundary: both judge one
        record, while the question is about the universe the scope names. Without this join a
        universe whose ownership is absent or only partially enumerated - so that NO body in it has
        an admissible dialect, and body_language_version is therefore never even reached because
        there are no facts - could still claim `complete` with no deficiency and seal a determinate
        verdict on an empty view. That is a contradictory claim, not a finding of no clones.

        The prerequisite is deliberately UNIVERSE level, and that is the whole of it. A per-body
        refusal - an unowned path, or an owner outside the selection - is perfectly compatible with
        `complete`: the host examined that subject and correctly produced no fact for it. What is not
        compatible is claiming a complete examination when nothing in the universe could have been
        examined for a dialect in the first place."""
        row=RELATIONS.get(scope['relation'])
        if row is None or 'bodyIdentityJoin' not in row:return
        admit_frame(scope['sourceUniverse'],'native-semantic-universe')
        domain,universe,universe_row,universe_retained=native_universes[scope['sourceUniverse']]
        dialect=universe_row.get('languageVersionBinding',{}).get('dialect')
        if not isinstance(dialect,dict) or 'ownership' not in dialect:return
        spec=dialect['ownership'];ownership=(universe_retained or {}).get(spec['retainedAs'])
        if ownership is None:unavailable='no-committed-ownership'
        elif ownership[spec['enumerationField']]!='complete':unavailable='enumeration-'+ownership[spec['enumerationField']]
        else:return
        entry=coverage_payload['entry']
        if entry['coverage']=='complete':
            raise C.AdmissionError('COVERAGE_DIALECT_PREREQUISITE:'+scope['relation']+':'+unavailable)
        if entry.get('deficiency') is None:
            raise C.AdmissionError('COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED:'+scope['relation']+':'+unavailable)
    def relation_source_joins(value,row,fact):
        """The per-relation snapshot-join registry, enforced on EVERY owning fact.

        A payload's content claim is joined to something: the path it names must be in the inventory
        of the snapshot THE ENCLOSING FACT names, the digest it claims must be that inventory row's
        digest, the length must be that row's length, and the bytes must actually be retained under
        the claimed digest. The payload decode above is memoized; this is not, because the truth of
        the claim is a property of the owner, not of the bytes: the same admissible payload under a
        second fact with different anchors or a different snapshot owes this admission again and can
        fail it."""
        snapshot=get(fact['snapshotId'],'snapshot')
        inventory={item['path']:item for item in snapshot['sourceInventory']}
        for join in row['snapshotJoins']:
            exemption=join.get('unless')
            if exemption is not None and C.equal_typed(value.get(exemption['field']),exemption['equals']):continue
            path=value[join['pathField']]
            item=inventory.get(path)
            if item is None:raise C.AdmissionError('RELATION_PATH_NOT_INVENTORIED:'+fact['relation']+':'+path)
            if join['form']=='inventoried-file':
                if item['sha256']!=value[join['digestField']]:raise C.AdmissionError('RELATION_FILE_CONTENT_JOIN:'+path)
                if not C.equal_typed(item['bytes'],value[join['lengthField']]):raise C.AdmissionError('RELATION_FILE_LENGTH_JOIN:'+path)
                # Retained, and re-hashed by blob(): an inventory row alone is a claim about bytes,
                # not custody of them, and a Run that cannot produce the bytes has not closed.
                if len(blob(value[join['digestField']]))!=value[join['lengthField']]:raise C.AdmissionError('RELATION_FILE_RETAINED_LENGTH:'+path)
            if 'anchorPathField' in join:
                for anchor in fact['anchors']:
                    if anchor['path']!=value[join['anchorPathField']]:
                        raise C.AdmissionError('RELATION_ANCHOR_FOREIGN_PATH:'+anchor['path'])
        if 'bodyIdentityJoin' in row:body_identity_join(value,row['bodyIdentityJoin'],fact)
    def body_identity_join(value,join,fact):
        """The INHERITED normalized-body recipe of fact-identity-policy.v2, reused exactly.

        `normalisationVersion` is the raw SHA-256 of the RETAINED canonical level specification, so
        it is re-hashed here and not accepted as an opaque caller hash. `bodyIdentity` is
        `sha256:` + SHA-256 of the RETAINED fully framed preimage, so the frame is fetched, re-hashed
        by blob() and parsed, and each component is joined to something this Run already admitted:
        the domain tag to the policy, the level to the payload, the level version to the retained
        specification, and the language identity to the fact's own semantic universe.

        The honest split, which the contract states and this code follows: at L0 the canonical
        payload IS the raw body-span bytes, so it is RECOMPUTED from the enclosing fact's own
        anchor - a real source join. At L1-L3 it is a versioned normalizer's output that no host can
        recompute, so what is required is exact retained custody plus well-formed framing. This
        qualifies no normalizer and grades no tokenisation.

        FACT-ID-V1 and bodyIdentity are never equated: the fact identity wraps the whole clone fact,
        this identity is over one normalized body span, and they differ by type and by domain."""
        text=value[join['field']]
        if not text.startswith('sha256:'):raise C.AdmissionError('BODY_IDENTITY_FORM')
        frame=blob(text.removeprefix('sha256:'))
        level=value[join['levelField']];level_version=value[join['levelVersionField']]
        blob(level_version)
        tag,level_id,version_bytes,language_id,language_version,payload=parse_body_frame(frame)
        if tag!=join['domainTag'].encode('ascii'):raise C.AdmissionError('BODY_IDENTITY_DOMAIN')
        if level_id!=level.encode('utf8'):raise C.AdmissionError('BODY_IDENTITY_LEVEL_JOIN')
        # The RAW 32 digest bytes, never the hexadecimal display text: a frame carrying the 64-byte
        # hex form is a different preimage and is refused here rather than silently accepted.
        if version_bytes!=bytes.fromhex(level_version):raise C.AdmissionError('BODY_IDENTITY_LEVEL_VERSION_JOIN')
        admit_frame(fact['sourceUniverse'],'native-semantic-universe')
        domain,record,universe_row,universe_retained=native_universes[fact['sourceUniverse']]
        # The frame's languageId is the BODY's language, checked against the derived projection
        # below, not against the provider universe's engine language: native 6.3 closes the
        # normalized-body languageId to {typescript, javascript, rust}, and one TypeScript engine
        # universe lawfully produces both typescript and javascript bodies.
        if language_id.decode('utf8') not in universe_row['languageVersionBinding']['bodyLanguages']:
            raise C.AdmissionError('BODY_IDENTITY_LANGUAGE_JOIN:'+language_id.decode('utf8','replace'))
        # Follow the universe's OWN committed reference to its admitted context. This is the same
        # nativeContextId close_run already requires to be Plan-selected; nothing here elects a
        # context by position or display.
        reference=record
        for step in universe_row['contextField']:reference=reference[step]
        if universe_row['contextForm']!='sha256-text':raise C.AdmissionError('BODY_LANGUAGE_CONTEXT_FORM')
        context_digest=reference.removeprefix('sha256:')
        admit_frame(context_digest,'native-context')
        context_domain,context,_admission,_retained=native_contexts[context_digest]
        if context_domain!=universe_row['contextDomain']:raise C.AdmissionError('BODY_LANGUAGE_UNIVERSE_CONTEXT_DOMAIN:'+context_domain)
        anchors=fact['anchors']
        if len(anchors)!=join['anchorCardinality']:raise C.AdmissionError('BODY_IDENTITY_ANCHOR_CARDINALITY')
        # DERIVED, not accepted: the projection is rebuilt from the universe, its admitted context,
        # THIS body's own anchor and the retained records the universe commits, and its RAW 32 digest
        # bytes are what the frame must carry. Fixed width, so an ordinary large workspace stays
        # representable inside the inherited u8 component length.
        projection=body_language_version(record,context,universe_row,anchors[0],universe_retained)
        # One selector, one anchor: the frame's languageId and the projection's cannot disagree.
        if language_id.decode('utf8')!=projection['languageId']:
            raise C.AdmissionError('BODY_IDENTITY_LANGUAGE_JOIN:'+language_id.decode('utf8','replace'))
        if language_version!=hashlib.sha256(C.canonical(projection)).digest():
            raise C.AdmissionError('BODY_IDENTITY_LANGUAGE_VERSION_JOIN')
        if level in join['recomputableAt']:
            anchor=anchors[0];span=blob(anchor['blobDigest'])[anchor['startByte']:anchor['endByte']]
            if payload!=len(span).to_bytes(4,'big')+span:raise C.AdmissionError('BODY_IDENTITY_BODY_SPAN')
        else:parse_token_stream(payload)
    def snapshot_joins(value,row,label):
        """Native-context and native-universe source correspondence: every repository path a record
        names must be in the analysed snapshot's inventory, and a named lockfile's content digest
        must be that inventory row's digest."""
        for join in row.get('snapshotJoins',[]):
            node=value
            for step in join['path']:node=node[step]
            if node is None:
                if not join.get('nullable'):raise C.AdmissionError(label+'_SNAPSHOT_JOIN_REQUIRED')
                continue
            inventory={item['path']:item for item in get(run['snapshotId'],'snapshot')['sourceInventory']}
            if join['form']=='inventoried-paths':
                # Either a list of path strings, or, when the row declares pathField, a list of
                # records carrying one. A record that names a path still names a repository source.
                for item in node:
                    path=item[join['pathField']] if 'pathField' in join else item
                    if path not in inventory:raise C.AdmissionError(label+'_PATH_NOT_INVENTORIED:'+path)
            else:
                item=inventory.get(node[join['pathField']])
                if item is None or item['sha256']!=node[join['digestField']]:raise C.AdmissionError(label+'_SOURCE_MISMATCH:'+str(node.get(join['pathField'])))
    def path_values(value,path):
        """Resolve a registry path; the step `[]` means every element of a list."""
        current=[value]
        for step in path:
            following=[]
            for item in current:
                if step=='[]':following.extend(item)
                else:following.append(item[step])
            current=following
        return current
    def admit_frame(digest,domain_set):
        if ('frame',digest,domain_set) in parsed:return parsed[('frame',digest,domain_set)]
        label=DIGESTS['domainSetLabels'][domain_set]
        domain,value,row=parse_h_frame(blob(digest),domain_set)
        parsed[('frame',digest,domain_set)]=value
        snapshot_joins(value,row,label)
        # Raw member bytes a semantic record names are part of the closure, not opaque strings:
        # dependency file-manifest members and inert prepared-output rows are retained and re-hashed.
        for join in row.get('blobJoins',[]):
            for node in path_values(value,join['path']):
                raw=blob(node[join['digestField']])
                if 'lengthField' in join and len(raw)!=node[join['lengthField']]:raise C.AdmissionError(label+'_MEMBER_LENGTH:'+join['digestField'])
        retained={}
        # Nested RECORDS: a raw canonical-record digest inside a frame (not an H identity). The record
        # is retained, validated under the document+selector its row names, and handed to the owning
        # binding, so a universe key like tsconfigGraphHash is never a semantically consumed opaque id.
        for join in row.get('nestedRecords',[]):
            for reference in path_values(value,join['path']):
                if reference is None:
                    if not join.get('nullable'):raise C.AdmissionError(label+'_NESTED_RECORD_REQUIRED:'+'.'.join(join['path']))
                    continue
                child=canonical_bytes(reference,label+'_NESTED_RECORD_NONCANONICAL')
                validate_registered_record(join['document'],join['selector'],child)
                for blob_join in join.get('blobJoins',[]):
                    for node in path_values(child,blob_join['path']):blob(node[blob_join['digestField']])
                if 'retainedAs' in join:retained[join['retainedAs']]=child
        # Nested semantic identities are H identities over registered records, admitted the same way.
        for join in row.get('nestedIdentities',[]):
            for reference in path_values(value,join['path']):
                if reference is None:
                    if not join.get('nullable'):raise C.AdmissionError(label+'_NESTED_IDENTITY_REQUIRED:'+'.'.join(join['path']))
                    continue
                if join['form']=='sha256-text':
                    if not reference.startswith('sha256:'):raise C.AdmissionError(label+'_NESTED_IDENTITY_FORM:'+'.'.join(join['path']))
                    reference=reference.removeprefix('sha256:')
                child=admit_frame(reference,join['domainSet'])
                if 'retainedAs' in join:retained[join['retainedAs']]=child
        if domain_set=='native-context':
            for join in row['closureJoins']:
                node=value
                for step in join['path']:node=node[step]
                key=node if join['form']=='closure2-identity' else PREFIX['closure']+':'+node
                closure=get(key,'closure')
                if closure['kind']!=join['kind']:raise C.AdmissionError('NATIVE_CONTEXT_CLOSURE_KIND:'+join['kind'])
                visit(key,'closure')
            # The owning contract's ACTUAL admission, re-run over the retained bytes and the
            # retained closure descriptors. A frame proves retention, never admission: without this
            # a claimant could re-frame a context the native boundary refuses and still mint a Run.
            N=native_admission()
            admission=N.admit_native_context(row['language'],value,{k:v for k,(d,v) in objects.items() if d=='closure'})
            if admission['refusals']:raise C.AdmissionError('NATIVE_CONTEXT_ADMISSION:'+','.join(admission['refusals']))
            if admission['planNativeContextDigest']!=digest or admission['domain']!=domain:raise C.AdmissionError('NATIVE_CONTEXT_ADMITTED_IDENTITY')
            native_contexts[digest]=(domain,value,admission,retained)
        if domain_set=='native-semantic-universe':
            native_universes[digest]=(domain,value,row,retained)
        return value
    def visit(key,domain):
        if key in seen:return
        value=get(key,domain)
        if domain in ['snapshot','fact','subject-scope'] and (value.get('snapshotId',run['snapshotId'])!=run['snapshotId'] or value.get('projectId',run['projectId'])!=run['projectId']):raise C.AdmissionError('REFERENCE_SOURCE_JOIN')
        if domain in ['view','proof-bundle','semantic-evidence','evaluation-seal','execution-plan'] and value['planId']!=run['planId']:raise C.AdmissionError('REFERENCE_PLAN_JOIN')
        seen.add(key);walk(SCHEMA['$defs'][domain],value)

    walk(SCHEMA['$defs']['run'],run)
    snapshot=get(run['snapshotId'],'snapshot');plan=get(run['planId'],'plan')
    evidence=get(run['evidenceId'],'semantic-evidence');seal=get(run['evaluationSealId'],'evaluation-seal')
    proof=get(seal['proofBundleId'],'proof-bundle');execution=get(seal['executionPlanId'],'execution-plan')
    if run['projectId']!=snapshot['projectId'] or plan['snapshotId']!=run['snapshotId']:raise C.AdmissionError('PROJECT_SNAPSHOT_JOIN')
    if any(x['planId']!=run['planId'] for x in [evidence,seal,proof,execution]):raise C.AdmissionError('PLAN_JOIN')
    if run['capabilityManifestId']!=plan['capabilityManifestId']:raise C.AdmissionError('CAPABILITY_JOIN')
    cap_bytes=blob(plan['capabilityManifestBytesDigest'])
    if hashlib.sha256(b'opensip.capability-manifest.v1\0'+cap_bytes).hexdigest()!=plan['capabilityManifestId']:raise C.AdmissionError('CAPABILITY_BYTES_JOIN')
    # Verifying the raw hash is not admission. The manifest is a PlanId input, so the owning
    # contract's CURRENT ADM-DOMAIN successor admits it: an unknown relation or a rung from another
    # relation's ladder refuses here rather than being carried into a Plan.
    capability=native_admission().admit_capability_manifest(cap_bytes)
    if capability['result']!='ADMIT':raise C.AdmissionError('CAPABILITY_MANIFEST_ADMISSION:'+','.join(capability['refusals']))
    if capability['capabilityManifestId']!=plan['capabilityManifestId']:raise C.AdmissionError('CAPABILITY_MANIFEST_IDENTITY')
    if capability_ids-{plan['capabilityManifestId']}:raise C.AdmissionError('FOREIGN_CAPABILITY_MANIFEST')
    if seal['evidenceId']!=run['evidenceId'] or evidence['proofBundleId']!=seal['proofBundleId']:raise C.AdmissionError('PROOF_JOIN')
    if proof['executionPlanId']!=seal['executionPlanId'] or proof['evaluatorClosure']!=seal['evaluatorClosure']:raise C.AdmissionError('EVALUATOR_JOIN')
    if proof['findingIds']!=evidence['findingIds'] or proof['verdict']!=seal['verdict'] or plan['policyDigest']!=seal['policyDigest']:raise C.AdmissionError('VERDICT_JOIN')
    if evidence['importIds']!=plan['importIds']:raise C.AdmissionError('IMPORT_JOIN')
    if any(snapshot[field]!=plan[field] for field in ['resolvedConfigDigest','scopeDigest']):raise C.AdmissionError('SNAPSHOT_INPUT_JOIN')
    # ADV-B1: the deterministic budget appears in two committed places. Neither silently wins: the
    # Plan's budget must be exactly the resolved configuration's analysis budget, so a legitimate
    # override has to be in the resolved configuration first and both then agree.
    resolved_configuration=payload(plan['resolvedConfigDigest'],'semantic-configuration')
    if not C.equal_typed(plan['budget'],resolved_configuration['analysis']['budget']):raise C.AdmissionError('PLAN_BUDGET_CONFIG_JOIN')
    if seal['evaluatorClosure'] not in plan['semanticClosures']:raise C.AdmissionError('UNSELECTED_EVALUATOR')
    analysis_spec=payload(plan['analysisSpecDigest'],'analysis-spec')
    grant=payload(plan['semanticGrantDigest'],'semantic-grant')
    if any((p['kind']=='first-party')!=(p['ownerSourceDigest'] is None) for p in grant['principals']):raise C.AdmissionError('PRINCIPAL_OWNER_BINDING')
    if grant['projectId']!=run['projectId'] or grant['scopeDigest']!=plan['scopeDigest']:raise C.AdmissionError('SEMANTIC_GRANT_JOIN')
    has_preparation_principal=any(p['kind']=='trusted-repository-code' for p in grant['principals'])
    if ('prepare-code' in grant['analysisOperations']) != has_preparation_principal:raise C.AdmissionError('PREPARATION_OPERATION_JOIN')
    if plan['importIds'] and 'read-import' not in grant['analysisOperations']:raise C.AdmissionError('IMPORT_OPERATION_JOIN')
    vcs=payload(snapshot['vcsDigest'],'vcs-observation')
    inventory_record=payload(vcs['sourceInventoryDigest'],'source-inventory')
    if not C.equal_typed(inventory_record,snapshot['sourceInventory']):raise C.AdmissionError('VCS_INVENTORY_JOIN')
    if (vcs['kind']=='none') != (vcs['commitId'] is None):raise C.AdmissionError('VCS_KIND_JOIN')

    # ------------------------------------------------------- native contexts and semantic universes
    if sorted(native_contexts)!=sorted(set(plan['nativeContextDigests'])):raise C.AdmissionError('NATIVE_CONTEXT_SET_JOIN')
    # The Plan's requested language modes own which semantic universes may appear. A universe of a
    # language nothing requested is not analysis this Plan asked for, and a prepared resolution is a
    # different requested mode from a non-prepared one (native section 1).
    modes=DIGESTS['languageModes']
    requested=set()
    for capability in analysis_spec['requestedCapabilities']:
        if capability['languageMode'] not in modes['map']:raise C.AdmissionError('ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED:'+capability['languageMode'])
        requested.add(capability['languageMode'])
    requested_languages={modes['map'][m] for m in requested}-{None}
    selected_contexts={'sha256:'+digest for digest in plan['nativeContextDigests']}
    for digest,(domain,universe,row,retained) in native_universes.items():
        if row['language'] not in requested_languages:raise C.AdmissionError('UNIVERSE_LANGUAGE_NOT_REQUESTED:'+row['language'])
        if universe.get('preparedResolution','none')!='none':
            prepared_mode=modes['preparedModes'].get(row['language'])
            if prepared_mode is None or prepared_mode not in requested:raise C.AdmissionError('PREPARED_RESOLUTION_MODE_NOT_REQUESTED:'+str(prepared_mode))
        bound=universe
        for step in row['contextField']:bound=bound[step]
        if row['contextForm']!='sha256-text' or bound not in selected_contexts:raise C.AdmissionError('UNIVERSE_CONTEXT_NOT_SELECTED')
        context_domain,context,admission,context_retained=native_contexts[bound.removeprefix('sha256:')]
        if context_domain!=row['contextDomain']:raise C.AdmissionError('NATIVE_UNIVERSE_CONTEXT_LANGUAGE:'+context_domain)
        for field in row.get('contextAgreementFields',[]):
            if not C.equal_typed(universe[field],context[field]):raise C.AdmissionError('NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH:'+field)
        # The owning contract's ACTUAL universe binding, over the retained universe, the retained
        # context bytes, the retained nested input records and the admission re-derived above.
        # A domain the owning contract registers but supplies no binding for refuses with a typed
        # cause; it is never admitted unbound, and the obligation is named rather than deferred.
        entry=getattr(native_admission(),row['binding']['entryPoint'],None)
        if entry is None:raise C.AdmissionError('NATIVE_UNIVERSE_BINDING_UNAVAILABLE:'+row['binding']['entryPoint'])
        available={'universe':universe,'admission':admission,'context':context,
                   'retained':{**context_retained,**retained},'snapshotInventory':snapshot['sourceInventory']}
        binding=entry(*[available[name] for name in row['binding']['arguments']])
        if binding['result']!='ADMIT':raise C.AdmissionError('NATIVE_UNIVERSE_BINDING:'+','.join(binding['refusals']))
        if binding['sourceUniverse']!=digest:raise C.AdmissionError('NATIVE_UNIVERSE_ADMITTED_IDENTITY')
        # Prepared products are inert data. Consuming them projects the operational grant operation
        # the owning contract names; retained prepared bytes never imply execution authority, and a
        # universe that consumed them without the projected operation refuses.
        operation=row.get('preparedResolutionGrantOperations',{}).get(universe.get('preparedResolution'))
        if operation is not None and operation not in grant['analysisOperations']:
            raise C.AdmissionError('PREPARED_RESOLUTION_GRANT_JOIN:'+operation)
    universe_digests=set()
    for key in list(seen):
        domain=objects[key][0]
        if domain in ('fact','subject-scope'):
            for field in ('sourceUniverse','targetUniverse'):universe_digests.add(objects[key][1][field])
    if not universe_digests<=set(native_universes):raise C.AdmissionError('UNIVERSE_FRAME_UNRETAINED')

    # ------------------------------------------------------------------ policy / compiled program
    policy=foreign_payload(plan['policyDigest'],'workflows/schemas/policy-document.schema.json','#/$defs/PolicyDocumentV1')
    foreign_payload(plan['waiverDigest'],'workflows/schemas/policy-document.schema.json','#/$defs/WaiverSetV1')
    program=foreign_payload(proof['ruleProgramDigest'],'workflows/schemas/policy-document.schema.json','#/$defs/RuleProgramV1')
    W=workflow_admission()
    if program['policyDigest']!=plan['policyDigest']:raise C.AdmissionError('RULE_PROGRAM_POLICY_JOIN')
    if W.rule_program_digest(policy)!=proof['ruleProgramDigest']:raise C.AdmissionError('RULE_PROGRAM_COMPILATION_JOIN')
    rules={rule['ruleId']:rule for rule in program['rules']}

    # ---------------------------------------------------------------- derivation stages and specs
    for stage in execution['stages']:
        spec=payload(stage['stageSpecDigest'],'stage-spec')
        if spec['planId']!=run['planId']:raise C.AdmissionError('STAGE_SPEC_PLAN_JOIN')
        if spec['producerClosure'] not in plan['semanticClosures']:raise C.AdmissionError('STAGE_SPEC_UNSELECTED_PRODUCER')
        if not C.equal_typed(spec['outputDomains'],stage['outputDomains']):raise C.AdmissionError('STAGE_SPEC_OUTPUT_DOMAIN_JOIN')
        if any(row not in analysis_spec['parameters'] for row in spec['parameters']):raise C.AdmissionError('STAGE_SPEC_HIDDEN_PARAMETER')

    def payload_of_coverage(coverage):
        return registered_payload(coverage['payloadDigest'],
            {'payloadClass':'coverage','keyedBy':['payload.schemaVersion'],'schemaDigestField':'payloadSchemaDigest'},coverage)
    def unresolved_edge_payloads(view):
        """The admitted unresolved-edge facts of this view, as the Coverage bijection needs them."""
        out=[]
        for fact_id in view['facts']:
            fact=get(fact_id,'fact')
            if fact['relation']!='unresolved-edge':continue
            out.append(registered_payload(fact['payloadDigest'],
                {'payloadClass':'relation','keyedBy':['relation'],'schemaDigestField':'payloadSchemaDigest'},fact))
        return out
    evaluation_refs={C.canonical(r) for r in proof['evaluationInputRefs']}
    view_roots={PREFIX['view']+':'+r['digest'] for r in proof['evaluationInputRefs'] if r['domain']=='view'}
    if set(evidence['viewIds'])!=view_roots:raise C.AdmissionError('EVALUATION_VIEW_ROOTS')
    coverage_roots={c for v in view_roots for c in get(v,'view')['coverageIds']}
    if set(evidence['coverageIds'])!=coverage_roots:raise C.AdmissionError('EVALUATION_COVERAGE_ROOTS')
    evaluated_imports={PREFIX['import']+':'+r['digest'] for r in proof['evaluationInputRefs'] if r['domain']=='import'}
    if not evaluated_imports<=set(plan['importIds']):raise C.AdmissionError('UNSELECTED_EVALUATION_IMPORT')
    finding_evidence_roots={
        'fact': {f.split(':',1)[1] for v in view_roots for f in get(v,'view')['facts']},
        'coverage': {c.split(':',1)[1] for c in coverage_roots},
        'import': {i.split(':',1)[1] for i in evaluated_imports},
        'predicate-witness': {p['witnessDigest'] for p in proof['predicateProofs']},
        'blob': {r['digest'] for r in proof['evaluationInputRefs'] if r['domain']=='blob'},
    }
    for fid in evidence['findingIds']:
        finding=get(fid,'finding')
        if any(r['digest'] not in finding_evidence_roots[r['domain']] for r in finding['evidenceRefs']):
            raise C.AdmissionError('HIDDEN_FINDING_EVIDENCE')
        parameters=payload(finding['parameterDigest'],'finding-parameters')
        if parameters['messageCode']!=finding['messageCode']:raise C.AdmissionError('FINDING_PARAMETER_MESSAGE_JOIN')
        if finding['ruleClosure'] not in plan['semanticClosures']:raise C.AdmissionError('FINDING_RULE_CLOSURE_UNSELECTED')
    proof_predicates={(p['ruleId'],p['subjectId']):set() for p in proof['predicateProofs']}
    for p in proof['predicateProofs']:proof_predicates[(p['ruleId'],p['subjectId'])].add(p['predicateId'])
    for pred in proof['predicateProofs']:
        if not {C.canonical(r) for r in pred['inputRefs']}<=evaluation_refs:raise C.AdmissionError('HIDDEN_PREDICATE_INPUT')
        views=[get(PREFIX['view']+':'+r['digest'],'view') for r in pred['inputRefs'] if r['domain']=='view']
        if not set(pred['scopeIds'])<={s for v in views for s in v['scopeIds']}:raise C.AdmissionError('PREDICATE_SCOPE_ROOTS')
        witness=payload(pred['witnessDigest'],'predicate-witness')
        if not set(witness['matchingFactIds'])<={f for v in views for f in v['facts']}:raise C.AdmissionError('WITNESS_FACT_ROOTS')
        if not set(witness['coverageIds'])<={c for v in views for c in v['coverageIds']}:raise C.AdmissionError('WITNESS_COVERAGE_ROOTS')
        # The witness's program predicate is an ADDRESS into the admitted rule program, not a free digest.
        addressed=payload(witness['programPredicateDigest'],'program-predicate')
        if addressed['ruleProgramDigest']!=proof['ruleProgramDigest']:raise C.AdmissionError('PROGRAM_PREDICATE_PROGRAM_JOIN')
        if addressed['ruleId']!=pred['ruleId'] or addressed['predicateId']!=pred['predicateId']:raise C.AdmissionError('PROGRAM_PREDICATE_ADDRESS_JOIN')
        if addressed['operation']!=pred['operation']:raise C.AdmissionError('PROGRAM_PREDICATE_OPERATION_JOIN')
        if pred['ruleId'] not in rules:raise C.AdmissionError('PROGRAM_PREDICATE_RULE_UNKNOWN')
        node=predicate_node_at(rules[pred['ruleId']]['emitWhen'],addressed['predicateId'])
        if node['op']!=addressed['operation']:raise C.AdmissionError('PROGRAM_PREDICATE_NODE_OPERATION')
        if hashlib.sha256(C.canonical(node)).hexdigest()!=addressed['nodeDigest']:raise C.AdmissionError('PROGRAM_PREDICATE_NODE_DIGEST')
        children=predicate_child_addresses(node,addressed['predicateId'])
        if sorted(witness['childPredicateIds'])!=sorted(children):raise C.AdmissionError('WITNESS_CHILD_ADDRESS_JOIN')
        if not set(children)<=proof_predicates[(pred['ruleId'],pred['subjectId'])]:raise C.AdmissionError('WITNESS_CHILD_NOT_PROVEN')
        limit=node.get('n') if node['op']=='count-at-most' else None
        if not C.equal_typed(witness['countLimit'],limit):raise C.AdmissionError('WITNESS_COUNT_LIMIT_JOIN')
    for key in evidence['viewIds']:
        view=get(key,'view')
        if view['planId']!=run['planId']:raise C.AdmissionError('VIEW_PLAN_JOIN')
        if view['producerClosure'] not in plan['semanticClosures']:raise C.AdmissionError('UNSELECTED_PRODUCER')
        for scope_id in view['scopeIds']:
            scope=get(scope_id,'subject-scope')
            if scope['snapshotId']!=run['snapshotId']:raise C.AdmissionError('SCOPE_SOURCE_JOIN')
            if scope['enumeratorClosure'] not in plan['semanticClosures']:raise C.AdmissionError('UNSELECTED_ENUMERATOR')
            if get(scope['enumeratorClosure'],'closure')['kind']!=DIGESTS['closureKinds']['byField']['subject-scope.enumeratorClosure']:
                raise C.AdmissionError('ENUMERATOR_CLOSURE_KIND')
        for fact_id in view['facts']:
            fact=get(fact_id,'fact')
            if fact['snapshotId']!=run['snapshotId'] or fact['producerClosure']!=view['producerClosure']:raise C.AdmissionError('FACT_SOURCE_PRODUCER_JOIN')
            join=['relation','resolution','sourceUniverse','targetUniverse']
            if not any(all(fact[k]==get(sid,'subject-scope')[k] for k in join) for sid in view['scopeIds']):raise C.AdmissionError('FACT_SCOPE_JOIN')
            for anchor in fact['anchors']:
                inventory={v['path']:v for v in snapshot['sourceInventory']}
                item=inventory.get(anchor['path'])
                if not item or item['sha256']!=anchor['blobDigest']:raise C.AdmissionError('ANCHOR_SOURCE')
                raw=blob(anchor['blobDigest']);a,b=anchor['startByte'],anchor['endByte']
                if not 0<=a<=b<=len(raw):raise C.AdmissionError('ANCHOR_RANGE')
                try:raw[:a].decode('utf8');raw[a:b].decode('utf8')
                except UnicodeError as exc:raise C.AdmissionError('ANCHOR_UTF8') from exc
        if any(cid not in evidence['coverageIds'] for cid in view['coverageIds']):raise C.AdmissionError('VIEW_COVERAGE_JOIN')
        for cid in view['coverageIds']:
            coverage=get(cid,'coverage')
            if coverage['scopeId'] not in view['scopeIds']:raise C.AdmissionError('COVERAGE_SCOPE_JOIN')
            # The owning contract's ACTUAL Coverage producer admission, re-run over the RETAINED
            # scope descriptor and the RETAINED unresolved-edge facts of this view. Validating the
            # payload under its registered selector proves shape, never admission: a self-rehashed
            # schema-valid payload with a wrong subjectCount, a wrong commitment or a contradictory
            # RC-2 claim is refused here, exactly as it would have been at the producer boundary.
            coverage_payload=payload_of_coverage(coverage)
            scope=get(coverage['scopeId'],'subject-scope')
            unresolved=[{'relation':row['relation'],'referrer':row['referrer'],'edgeKind':row['edgeKind']}
                        for row in unresolved_edge_payloads(view)]
            admitted=native_admission().admit_coverage_result_v3(coverage_payload,scope,unresolved,coverage['payloadSchemaDigest'])
            if admitted['result']!='ADMIT':
                raise C.AdmissionError('COVERAGE_PRODUCER_ADMISSION:'+','.join(admitted['refusals']+[str(f) for f in admitted['faults']]))
            if admitted['coverageId']!=cid:raise C.AdmissionError('COVERAGE_ADMITTED_IDENTITY')
            coverage_dialect_prerequisite(scope,coverage_payload)
    # Reuse the actual typed import/mapping admission rules at the host closure boundary.
    # This is reference composition, not a dependency on a renderer or input-supplied code.
    if plan['importIds']:
        imports=workflow_admission()
        context_schema_raw=(HERE/'import-source-context.schema.json').read_bytes()
        context_schema_digest=hashlib.sha256(context_schema_raw).hexdigest()
        context_rows=[p for p in analysis_spec['parameters'] if p['schemaDigest']==context_schema_digest]
        if len(context_rows)>1:raise C.AdmissionError('IMPORT_SOURCE_CONTEXT_MULTIPLE')
        declared_builds=[]
        if context_rows:
            context=registered_payload(context_rows[0]['payloadDigest'],
                {'payloadClass':'parameter','keyedBy':['schemaDigest'],'schemaDigestField':'schemaDigest'},
                context_rows[0])
            ordered(context);declared_builds=context['declaredBuildIds']

        for iid in plan['importIds']:
            imp=get(iid,'import')
            corr=foreign_payload(imp['sourceCorrespondenceDigest'],'workflows/schemas/common.schema.json','#/$defs/SourceCorrespondence')
            try:
                if corr['kind']=='exact-snapshot':
                    if corr['snapshotId']!=run['snapshotId']:raise C.AdmissionError('IMPORT_SOURCE_JOIN')
                else:
                    if not corr['sourceMappingDigest']:raise C.AdmissionError('IMPORT_SOURCE_MAPPING_REQUIRED')
                    mapping=foreign_payload(corr['sourceMappingDigest'],'workflows/schemas/imported-evidence.schema.json','#/$defs/SourceMappingV1')
                    mapping_digest=imports.admit_source_mapping(mapping,snapshot['sourceInventory'],run['snapshotId'])
                    binding={'snapshotId':run['snapshotId'],'vcsRevision':None if vcs['kind']=='none' else {'system':'git','commit':vcs['commitId'],'dirty':vcs['dirty']},'declaredBuildIds':declared_builds,'admittedSourceMappings':[mapping_digest]}
                    if imports.classify_staleness(corr,binding)['usable']!='consumable':raise C.AdmissionError('IMPORT_VCS_JOIN')
            except imports.Refusal as exc:
                raise C.AdmissionError('IMPORT_CORRESPONDENCE_SHAPE') from exc
    for field,domain in [('coverageIds','coverage'),('importIds','import'),('findingIds','finding')]:
        for key in evidence[field]:get(key,domain)
    get(seal['evaluatorClosure'],'closure')
    return run_id,{'plan':plan,'snapshot':snapshot,'grant':grant,'analysisSpec':analysis_spec,'execution':execution,
                   'get':get,'visit':visit,'blob':blob,'payload':payload,'foreign_payload':foreign_payload,
                   'registered_payload':registered_payload,'registry_row':registry_row,
                   'admit_frame':admit_frame,'digest_field':digest_field,
                   'nativeContexts':native_contexts,'nativeUniverses':native_universes}


def cache_key(domain,key):
    """PURE deterministic key construction: exact schema admission and canonical order only.

    It reads no bytes and resolves no reference, so a host may compute it before loading anything
    and MISS cheaply. It is a lookup key and nothing else: it grants no authority, admits no bytes
    and says nothing about whether an entry found under it may be used. `cache-key` and
    `regeneration-key` share one schema and one stage-spec record and differ only by H domain."""
    if domain not in ('cache-key','regeneration-key'):raise C.AdmissionError('CACHE_DOMAIN')
    return identifier(domain,key)


def admit_cache_entry(domain,key,run,objects,blobs):
    """Admit a cache or regeneration HIT against a CONSTRUCTED Run. Finding bytes under a matching
    key is not authority.

    BOUNDARY, stated exactly. This is a post-construction conformance check, not the product's
    pre-analysis cache scheduling API. A host schedules with `cache_key`, provisionally loads
    producer bytes on a match, and those bytes then face ordinary stage and closure admission before
    anything gains Run authority; nothing here requires a Run to consume an intermediate hit, and
    there is no dependency cycle. What this function answers is the later question: given a Run and
    its admitted closure, was this entry consumable under exactly that closure?

    It therefore opens the Run's closure first and resolves the key's own references through it: the
    stage must be one the execution plan actually carries, its spec must join this Plan, the
    producing closure must be retained and Plan-selected, every scope must be a retained
    subject-scope of this snapshot, the output schema document must be retained, and every consumed
    input reference is dispatched through the SAME x-opensip-digest-domains registry the Run uses.
    So nothing is admitted under a guessed payload-domain schema, a bare payload-domain reference is
    refused as an authoritative root rather than resolved by guesswork, and a foreign view or scope
    refuses on the ordinary Plan/source joins rather than on its shape alone.

    What it does NOT do: it does not model a miss (a miss is not a failure — the host recomputes),
    it does not fetch or validate the cached OUTPUT bytes, and it does not decide reuse policy. It
    validates the lookup key and its consumed input closure against an admitted Run; it is not a
    complete cache subsystem.
    """
    run_id,closure=open_run_closure(run,objects,blobs)
    identity=cache_key(domain,key)
    plan=closure['plan']
    if key['planId']!=run['planId']:raise C.AdmissionError('CACHE_PLAN_JOIN')
    if key['stageSpecDigest'] not in {stage['stageSpecDigest'] for stage in closure['execution']['stages']}:
        raise C.AdmissionError('CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN')
    spec=closure['payload'](key['stageSpecDigest'],'stage-spec')
    if spec['planId']!=run['planId']:raise C.AdmissionError('CACHE_STAGE_SPEC_PLAN_JOIN')
    if spec['producerClosure']!=key['producerClosure']:raise C.AdmissionError('CACHE_STAGE_SPEC_PRODUCER_JOIN')
    if spec['outputSchemaDigest']!=key['outputSchemaDigest']:raise C.AdmissionError('CACHE_OUTPUT_SCHEMA_JOIN')
    if key['producerClosure'] not in plan['semanticClosures']:raise C.AdmissionError('CACHE_UNSELECTED_PRODUCER')
    closure['visit'](key['producerClosure'],'closure')
    closure['blob'](key['outputSchemaDigest'])
    for scope_id in key['scopeIds']:
        scope=closure['get'](scope_id,'subject-scope')
        if scope['snapshotId']!=run['snapshotId']:raise C.AdmissionError('CACHE_SCOPE_SOURCE_JOIN')
        closure['visit'](scope_id,'subject-scope')
    consumed=[]
    for reference in key['inputRefs']:
        row=DIGESTS['byDomain'].get(reference['domain'])
        if row is None:raise C.AdmissionError('CACHE_INPUT_DOMAIN_UNREGISTERED:'+str(reference['domain']))
        record=row.get('record',{})
        if 'resolvedThrough' in record:
            raise C.AdmissionError('CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT:'+reference['domain'])
        closure['digest_field'](row,reference['digest'],reference)
        if row['representation']=='h-identity' and 'domainSet' in row:
            if reference['digest'] not in plan['nativeContextDigests']:raise C.AdmissionError('CACHE_INPUT_CONTEXT_NOT_SELECTED')
        if reference['domain']=='import' and PREFIX['import']+':'+reference['digest'] not in plan['importIds']:
            raise C.AdmissionError('CACHE_INPUT_IMPORT_NOT_SELECTED')
        consumed.append(reference)
    return {'identity':identity,'runId':run_id,'stageSpec':spec,'consumedRefs':consumed,
            'grantsEvidenceAuthority':False,
            'note':'A hit is reusable producer output under an admitted closure; it never becomes '
                   'evidence authority and never replaces a sealed Run.'}


def commit_inventory(run_id,objects,blobs):
    """The closed record digested by commit-receipt.inventoryDigest."""
    record={'schemaVersion':2,'runId':run_id,'objects':sorted(objects,key=C.canonical),'blobDigests':sorted(blobs,key=C.canonical)}
    schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/commit-inventory';C.validate(schema,record);ordered(record)
    return record,hashlib.sha256(C.canonical(record)).hexdigest()


def predicate(operation,matching_facts,coverage,limit=None):
    """Reference finite-relation proof rule. Only already validated matching facts enter.
    COMPLETE must mean resolution-complete at the requested rung, not merely examined.
    Native evidence unit owns the producer's proof of that coverage state.
    """
    if operation not in ['exists','none','count-at-most','all-covered']:raise C.AdmissionError('PREDICATE')
    if type(matching_facts) is not list or len(matching_facts)!=len(set(matching_facts)):raise C.AdmissionError('FACT_SET')
    if coverage not in ['complete','unknown']:raise C.AdmissionError('COVERAGE')
    if operation=='exists':return 'true' if matching_facts else ('false' if coverage=='complete' else 'indeterminate')
    if operation=='none':return 'false' if matching_facts else ('true' if coverage=='complete' else 'indeterminate')
    if operation=='all-covered':return 'true' if coverage=='complete' else 'indeterminate'
    if type(limit) is not int or limit<0:raise C.AdmissionError('COUNT_LIMIT')
    if len(matching_facts)>limit:return 'false'
    return 'true' if coverage=='complete' else 'indeterminate'


def boolean(operation,values):
    if not values or any(v not in ['true','false','indeterminate'] for v in values):raise C.AdmissionError('BOOL_INPUT')
    if operation=='not':
        if len(values)!=1:raise C.AdmissionError('NOT_ARITY')
        return {'true':'false','false':'true','indeterminate':'indeterminate'}[values[0]]
    if operation not in ['and','or']:raise C.AdmissionError('BOOL_OPERATION')
    dominant='false' if operation=='and' else 'true'
    return dominant if dominant in values else ('indeterminate' if 'indeterminate' in values else ('true' if operation=='and' else 'false'))


class EvidenceStore:
    """Reference state transitions only. Native fsync/SQLite behavior specified in prose."""
    def __init__(self):
        self.runs={};self.objects={};self.receipts=[];self.availability={};self.pins=set();self.prepared={};self.attempts={};self.blobs={}
    def prepare(self,run,objects,blobs,execution_id,replay):
        if not re.fullmatch(r'exec1_[0-9a-f]{32}',execution_id):raise C.AdmissionError('EXECUTION_ID')
        if execution_id in self.attempts:raise C.AdmissionError('EXECUTION_ID_REUSED')
        rid=close_run(run,objects,blobs)
        # replay is the authenticated first-party pure evaluator, supplied by the host,
        # never a caller-supplied function or JSON flag. Its code is a TCB assumption.
        # The reference checks supply an independent finite-relation evaluator.
        if not callable(replay):raise C.AdmissionError('EVALUATOR_REQUIRED')
        seal=objects[run['evaluationSealId']][1]
        proof=objects[seal['proofBundleId']][1]
        plan=objects[run['planId']][1]
        computed=replay(copy.deepcopy(plan),copy.deepcopy(objects),copy.deepcopy(blobs),copy.deepcopy(proof['evaluationInputRefs']))
        if not C.equal_typed(computed,proof):raise C.AdmissionError('PROOF_REPLAY_MISMATCH')
        self.prepared[execution_id]=(rid,copy.deepcopy(run),copy.deepcopy(objects),copy.deepcopy(blobs));self.attempts[execution_id]='prepared';return rid
    def commit(self,execution_id,fault=None):
        if fault=='before-blobs':self.attempts[execution_id]='failed';self.prepared.pop(execution_id,None);return 'operational-failed'
        rid,run,objects,blobs=self.prepared[execution_id];self.objects.update(objects);self.blobs.update(blobs)
        if fault=='before-ledger':self.attempts[execution_id]='failed';self.prepared.pop(execution_id,None);return 'operational-failed'
        self.runs[rid]=run
        self.set_availability(rid,'retained',[],'commit')
        inventory,inventory_digest=commit_inventory(rid,objects,blobs)
        self.inventories=getattr(self,'inventories',{});self.inventories[rid]=inventory
        receipt={'schemaVersion':2,'runId':rid,'executionId':execution_id,'namespaceId':'reference-private-namespace','commitSequence':len(self.receipts)+1,'inventoryDigest':inventory_digest,'sealedAssurance':'replayable','signerKeyId':'reference-host-signer'}
        schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/commit-receipt';C.validate(schema,receipt)
        self.receipts.append(receipt);self.attempts[execution_id]='committed';self.prepared.pop(execution_id,None)
        return 'durability-undetermined' if fault=='after-ledger-before-ack' else 'committed'
    def purge(self,rid,force=False):
        if rid in self.pins and not force:return 'pinned'
        if force:self.pins.discard(rid)
        self.set_availability(rid,'purged',[],'explicit-purge')
        # Keep sealed manifest and tombstone; reachability GC separately deletes unshared blobs.
        return 'purged'
    def query(self,rid,requires_evidence=False):
        if rid not in self.runs:return 'not-found'
        if requires_evidence and self.availability[rid]['state']!='retained':return 'precondition-failed'
        return copy.deepcopy(self.runs[rid])

    def set_availability(self,rid,state,missing,reason):
        if rid not in self.runs:raise C.AdmissionError('RUN_MISSING')
        old=self.availability.get(rid,{'generation':-1})
        value={'schemaVersion':2,'runId':rid,'generation':old['generation']+1,'state':state,'missingRefs':missing,'reason':reason}
        schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/availability';C.validate(schema,value);ordered(value)
        if state=='retained' and missing:raise C.AdmissionError('RETAINED_WITH_MISSING')
        self.availability[rid]=value
        return copy.deepcopy(value)
    def recover(self,execution_id):
        state=self.attempts.get(execution_id,'not-found')
        receipt=next((r for r in self.receipts if r['executionId']==execution_id),None)
        return {'state':'committed' if receipt else ('failed' if state=='failed' else 'uncommitted' if state=='prepared' else state),'receipt':copy.deepcopy(receipt),'effectsRepeated':False}
    def restore(self,rid,objects,blobs,replay):
        run=self.runs[rid]
        if close_run(run,objects,blobs)!=rid:raise RegenerationMismatch(rid)
        seal=objects[run['evaluationSealId']][1];proof=objects[seal['proofBundleId']][1]
        if not C.equal_typed(replay(objects[run['planId']][1],objects,blobs,proof['evaluationInputRefs']),proof):raise RegenerationMismatch(rid)
        self.objects.update(copy.deepcopy(objects));self.blobs.update(copy.deepcopy(blobs))
        return self.set_availability(rid,'retained',[],'verified-restoration')


def project_identity_admit(carrier,registry,action='open',new_id=None):
    """Trusted custody observations, no filesystem operation or credential transfer."""
    valid=lambda x: type(x) is str and re.fullmatch('prj1-[0-9a-f]{64}',x)
    if action not in ['open','adopt','fork','move']:raise C.AdmissionError('PROJECT_ACTION')
    if any(x is not None and not valid(x) for x in [carrier,registry,new_id]):raise C.AdmissionError('PROJECT_ID')
    if action=='fork':
        if not valid(new_id) or new_id in [carrier,registry]:raise C.AdmissionError('PROJECT_FORK_ID')
        return {'projectId':new_id,'action':'create-both','importsCredentials':False,'importsOperationalState':False}
    if carrier is None and registry is None:
        if action!='open' or not valid(new_id):raise C.AdmissionError('PROJECT_NEW_ID_REQUIRED')
        return {'projectId':new_id,'action':'create-both','importsCredentials':False,'importsOperationalState':False}
    if carrier==registry:return {'projectId':carrier,'action':'reuse','importsCredentials':False,'importsOperationalState':False}
    if action in ['adopt','move'] and carrier is not None and registry is None:
        return {'projectId':carrier,'action':'register-existing','importsCredentials':False,'importsOperationalState':False}
    raise C.AdmissionError('PROJECT_IDENTITY_CONFLICT')


def subject_discriminator(signature_tokens,colliding_signatures):
    """Native supplies normalized declaration-signature tokens, never body/location offsets."""
    raw=C.canonical(signature_tokens);key=hashlib.sha256(raw).hexdigest()
    if sum(C.canonical(s)==raw for s in colliding_signatures)!=1:raise C.AdmissionError('SUBJECT_KEY_AMBIGUOUS')
    return key


def storage_admission(backup_state,explicit_backup_choice=False,ephemeral=False):
    """TM V17 custody join; backup_state is the trusted storage detector observation.
    Other upload/permissions/native filesystem admission runs independently first.
    """
    if backup_state not in ['detected','not-detected','unknown'] or type(explicit_backup_choice) is not bool or type(ephemeral) is not bool:raise C.AdmissionError('STORAGE_ADMISSION_TYPE')
    if backup_state=='detected' and not explicit_backup_choice and not ephemeral:
        return {'admitted':False,'exit':2,'detail':'storage.backup-choice-required','sourceWrite':False}
    return {'admitted':True,'backupDisclosure':backup_state,'authority':'ephemeral' if ephemeral else 'durable','policyWritten':False}
