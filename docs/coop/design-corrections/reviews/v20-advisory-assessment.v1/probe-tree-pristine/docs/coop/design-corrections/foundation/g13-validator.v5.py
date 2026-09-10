"""Authenticated G13 report reference boundary; external observations remain trusted inputs.
No product measurements are produced by this module. Ed25519 verifies report custody,
not the truth of the measured machine; the qualification host owns those observations.
"""
import base64, copy, hashlib, importlib.util, json, subprocess, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
COMP=HERE.parents[1]/'completion'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
C=load('g13_canonical',HERE/'canonical.py')
OLD=load('g13_prior',COMP/'check_g13_result_design_v4.py')
CORPUS=json.loads((COMP/'quality-corpus-manifest.v1.json').read_text())
SCHEMA=json.loads((HERE/'g13-result-schema.v5.json').read_text())
M=OLD.M


def oracle(row,project):
    """Expected atoms come only from the independently pinned corpus, never the report."""
    p=CORPUS['projects'][project]
    result=[{'kind':'coverage','value':p['coverage']}]
    if p['coverage']=='unknown':
        result.append({'kind':'deficiency','value':p['deficiency']})
    if row['capability']=='typescript.imports':
        result.extend({'kind':'import-edge','value':v} for v in p['expectedProjectImportEdges'])
    elif row['capability']=='host.integration':
        if p['expectedCycles'] is not None:
            result.extend({'kind':'cycle','value':sorted(v)} for v in p['expectedCycles'])
            result.append({'kind':'verdict','value':'fail' if p['expectedCycles'] else 'pass'})
        else:
            result.append({'kind':'verdict','value':'indeterminate'})
    else:
        fields={'typescript.references':['returnValueBindsTo','returnValueDoesNotBindTo'],
                'typescript.calls':['resolvedCall'],'typescript.types':['checkedType'],
                'typescript.reachability':['reachable']}[row['capability']]
        result.extend({'kind':k,'value':p['observations'][k]} for k in fields if k in p.get('observations',{}))
    return sorted(result,key=C.canonical)


def signature_message(raw,context):
    return (b'opensip.qualification.report.2\0'+bytes.fromhex(context['hostDigest'])+
            bytes.fromhex(context['providerClosureDigest'])+bytes.fromhex(context['harnessDigest'])+
            hashlib.sha256(raw).digest())


def verify_signature(raw,signature,context):
    """Pinned key is supplied by authenticated release-gate context, never by report."""
    if len(raw)>C.MAX_BYTES or len(signature)!=64:return False
    with tempfile.TemporaryDirectory(prefix='opensip-g13-verify-') as td:
        p=Path(td);(p/'key.pem').write_text(context['producerPublicKeyPem'])
        (p/'message').write_bytes(signature_message(raw,context));(p/'sig').write_bytes(signature)
        result=subprocess.run(['openssl','pkeyutl','-verify','-pubin','-inkey',str(p/'key.pem'),
                               '-rawin','-in',str(p/'message'),'-sigfile',str(p/'sig')],
                              stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
        return result.returncode==0


def admit(raw,signature,context):
    """context is obtained from release invocation/verified producer inventory, not CLI JSON.
    Returning True accepts a well-formed truthful-to-trusted-inputs report, including FAIL.
    Promotion separately requires report.result==PASS and all required cells/platform lanes.
    """
    try:
        if not verify_signature(raw,signature,context):return False
        x=C.parse(raw);C.validate(SCHEMA,x)
        for field in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest']:
            if x[field]!=context[field]:return False
        if context['matrixDigest']!=OLD.SHA(COMP/'language-quality-matrix.completed.v2.json'):return False
        if context['corpusDigest']!=OLD.SHA(COMP/'quality-corpus-manifest.v1.json'):return False
        cells={x['cellId']:x for x in x['cells']}
        if len(cells)!=len(M['rows']):return False
        legacy=copy.deepcopy(x);legacy.pop('harnessDigest');legacy['schemaMajor']=1
        for row in M['rows']:
            cell=cells[row['id']]
            for f in cell['fixtureResults']:
                expected=oracle(row,f['fixtureId']);actual=f['actualObservations']
                expected_keys=[C.canonical(v) for v in expected];actual_keys=[C.canonical(v) for v in actual]
                if actual_keys!=sorted(actual_keys):return False
                missing=len(set(expected_keys)-set(actual_keys));extra=len(set(actual_keys)-set(expected_keys))
                duplicates=len(actual_keys)-len(set(actual_keys));match=not(missing or extra or duplicates)
                if (f['expectedCount'],f['actualCount'],f['missingCount'],f['extraCount'],f['duplicateCount'],f['expectationMatched'])!=(len(expected),len(actual),missing,extra,duplicates,match):return False
                diff=None if match else C.identity('quality-difference',{'expected':expected,'actual':actual})
                if f['differenceArtifactDigest']!=diff:return False
        for cell in legacy['cells']:
            for f in cell['fixtureResults']:f.pop('actualObservations')
        return OLD.valid(legacy,context['baseline'],context['trustedRunners'])
    except (ValueError,KeyError,TypeError,OverflowError,subprocess.SubprocessError,OSError,C.ValidationError):
        return False
