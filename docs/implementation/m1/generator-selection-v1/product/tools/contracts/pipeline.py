"""Development staging of all eight contracts with confined child processes.

All subprocess tools are explicit and pinned. The native Python child binds its package snapshot and disables site loading.
System native loader and runtime remain trusted; portable release qualification is separate.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys


def load(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n')


def run(args, *, selected_closure=None, provenance=None):
    if not sys.flags.isolated or sys.flags.optimize:
        raise ValueError('use isolated Python without optimization')
    root=args.root.resolve(strict=True);code=root/'tools/contracts'
    tools={name:getattr(args,name).resolve(strict=True) for name in ['node','generator','python']}
    expected=load(code/'toolchain.json')['executables']
    for name,path in tools.items():
        if pin(path)!=expected[name]:raise ValueError('tool bytes differ: '+name)
    # Snapshot verified regular input bytes before invoking any child. This
    # observed closure is still a development candidate, not source authority.
    original_root=root
    source_paths=[]
    if selected_closure is None:
        candidates=[path for directory in (root/'schemas',root/'tools') for path in directory.rglob('*')]
    else:
        candidates=[root/row['path'] for row in selected_closure]
    for path in candidates:
            if '__pycache__' in path.parts:continue
            info=path.lstat()
            if stat.S_ISLNK(info.st_mode):raise ValueError('linked generator input')
            if stat.S_ISDIR(info.st_mode):continue
            if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1:raise ValueError('nonregular or hardlinked generator input')
            source_paths.append(path)
    source_bytes={p.relative_to(root).as_posix():p.read_bytes() for p in source_paths}
    closure=[{'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for name,raw in sorted(source_bytes.items())]
    if selected_closure is not None and closure != selected_closure:
        raise ValueError('generation snapshot differs from selected closure')
    out=args.output.resolve();out.mkdir(exist_ok=False)
    root=out/'snapshot';root.mkdir()
    for name,raw in source_bytes.items():
        dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    code=root/'tools/contracts'
    original_tools=dict(tools)
    for name in ('node','generator'):
        raw=tools[name].read_bytes()
        if {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}!=expected[name]:raise ValueError('tool changed during snapshot')
        dest=out/('tool-'+name);dest.write_bytes(raw);dest.chmod(0o700);tools[name]=dest
    collector=module(code/'admission.py','pipeline_collector')
    confine=module(code/'confine.py','pipeline_confine')
    confinement=load(code/'confinement-profile.json');collector.verify_confinement(confinement)
    roots={}
    def owned(path):
        path.mkdir();roots[path]=collector.directory_identity(path);return path
    scratch=owned(out/'runtime')
    # Generated runtime validators are CommonJS regardless of any surrounding
    # repository's package.json. Do not inherit an ambient module kind.
    write(scratch/'package.json',{'private':True,'type':'commonjs'})
    home=owned(out/'home')
    def step(name,argv,reads,writes,policy=None):
        collector.verify_directory_roots(roots)
        if policy is None:policy=collector.child_profile(argv[0],reads,writes)
        policy_path=out/(name+'-profile.sb');policy_path.write_text(policy)
        status,stdout,stderr,failure=confine.capture_child(['/usr/bin/sandbox-exec','-f',str(policy_path),*[str(x) for x in argv]],cwd=scratch,env={'PATH':'/usr/bin:/bin','HOME':str(home),'LANG':'C','LC_ALL':'C','TZ':'UTC'})
        (out/(name+'.stdout')).write_bytes(stdout)
        (out/(name+'.stderr')).write_bytes(stderr)
        collector.verify_directory_roots(roots)
        collector.verify_confinement(confinement)
        if failure:raise ValueError(f'{name}: {failure}; see retained bounded logs')
        if status:raise ValueError(f'{name} failed with exit {status}; see retained logs')
    # Every source path is fixed by the selected map; input digest is raw bytes.
    rows=load(root/'schemas/source-map.json')['sources'];sources={}
    for row in rows:
        name=row['implementationPath']
        if name.startswith('/') or '..' in Path(name).parts or '\\' in name:raise ValueError('source path')
        p=root/name;raw=p.read_bytes();architecture=row['architectureSource']
        if pin(p)!={k:architecture[k] for k in ['bytes','sha256']}:raise ValueError('source bytes differ: '+name)
        schema=json.loads(raw)
        if schema['$id']!=row['schemaId'] or row['schemaId'] in sources:raise ValueError('source identity')
        registry={k:row[k] for k in ['schemaId','declaredMajor','profile','semanticValidatorOwner']}
        registry.update(sourcePath=name,sourceSha256=architecture['sha256'])
        sources[row['schemaId']]=(registry,raw,schema)
    options=load(code/'options.json');adapter=module(code/'adapter.py','pipeline_adapter')
    adapter.validate_options(options,sources);adapter.validate_source_map(load(root/'schemas/source-map.json'),sources,options)
    profile=load(root/'schemas/profiles/report-codec.json')
    if profile['reportRoot']!=options['reportEntryPoint'] or profile['rawSchemaSha256']!=sources[profile['schemaId']][0]['sourceSha256']:raise ValueError('report profile source mismatch')
    runtime=(code/'runtime/exact-json.ts').read_text()
    for name,value in [('REPORT_BYTE_LIMIT',profile['documentMaxBytes']),('REPORT_DEPTH_LIMIT',profile['maxContainerDepth'])]:
        if f'const {name} = {value};' not in runtime:raise ValueError('report profile runtime mismatch')
    prepared=owned(out/'prepared')
    raw_inputs=owned(out/'raw-inputs')
    write(raw_inputs/'options.json',options);write(raw_inputs/'raw-schemas.json',[row[1].decode() for row in sources.values()])
    prepare_out=owned(out/'prepared-output')
    preparation_profile=load(code/'python-profile.json')
    if Path(preparation_profile['executable']['path'])!=tools['python']:raise ValueError('preparation executable mismatch')
    policy=collector.python_child_profile(preparation_profile,code/'prepare-inputs.py',raw_inputs/'raw-schemas.json',raw_inputs/'options.json',code,prepare_out)
    step('prepare',[tools['python'],'-I','-B','-S',code/'prepare-inputs.py',raw_inputs/'raw-schemas.json',raw_inputs/'options.json',code,prepare_out],[],[],policy)
    collector.verify_python_profile(preparation_profile)
    prepared_bytes=collector.collect_outputs(prepare_out,{'owners.json','rust-projection.json','ts-projection.json'})
    if prepared_bytes['owners.json']!=(json.dumps(options['owners'],indent=2)+'\n').encode():raise ValueError('prepared owner mismatch')
    for name,raw in prepared_bytes.items():(prepared/name).write_bytes(raw)
    write(prepared/'options.json',options);write(prepared/'raw-schemas.json',[row[1].decode() for row in sources.values()])
    write(out/'input-closure.json',{'files':closure,'executables':expected})
    write(prepared/'provenance.json',provenance if provenance is not None else {'registrySha256':pin(root/'schemas/source-map.json')['sha256'],'generatorClosureSha256':pin(out/'input-closure.json')['sha256']})
    base=owned(out/'base')
    step('validate',[tools['node'],code/'validate-schemas.cjs',prepared,scratch],[code,prepared],[scratch])
    step('rust',[tools['generator'],prepared,base],[prepared],[base])
    step('typescript',[tools['node'],code/'generate-ts.cjs',prepared,base],[code,prepared],[base])
    # Native renderer gets the explicit package/runtime files and one owned
    # output root. Each pipeline child uses its own deny-default profile.
    confine=module(code/'confine.py','pipeline_confine')
    confinement=load(code/'confinement-profile.json')
    collector=module(code/'admission.py','pipeline_collector')
    collector.verify_confinement(confinement)
    python_profile=load(code/'native-python-profile.json')
    if Path(python_profile['executable']['path']) != tools['python']:
        raise ValueError('Python runtime executable differs from selected tool')
    lane=owned(out/'native-work')
    identity=collector.directory_identity(lane)
    native_out=lane/'generated'
    policy=confine.python_profile(python_profile,[code,root/'schemas',code/'options.json'],lane)
    step('native-python',[tools['python'],'-I','-B','-S',code/'render-native.py',root/'schemas/wire/native-carriers-v1.json',root/'schemas/wire/native-carriers-meta.schema.json',code/'options.json',native_out],[],[],policy)
    collector.verify_directory_roots({lane:identity})
    collector.verify_confinement(confinement)
    confine.verify_runtime(python_profile)
    collector.collect_outputs(native_out,{'native.rs','wire.ts','render-result.json'})
    receipt=load(native_out/'render-result.json')
    expected_outputs={f'crates/contracts/src/generated/{name}.rs' for name in ['evidence','identity','invocation','output','protocol','mod']}|{'apps/report/src/generated/report.ts','providers/typescript/src/generated/protocol.ts'}
    base_bytes=collector.collect_outputs(base,expected_outputs)
    assembly=owned(out/'assembly');final=owned(assembly/'output')
    for name,raw_bytes in base_bytes.items():
        dest=final/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw_bytes)
    protocol=final/'crates/contracts/src/generated/protocol.rs';raw=out/'protocol-unformatted.rs'
    raw.write_text(protocol.read_text()+'\n// Native07 inert carrier integration.\n'+(native_out/'native.rs').read_text())
    step('format',[tools['generator'],'--format-rust',raw,protocol],[raw],[final])
    step('native-typescript',[tools['node'],code/'assemble-native.cjs',base,native_out,final,prepared],[code,base,native_out,prepared],[assembly])
    expected_outputs={f'crates/contracts/src/generated/{name}.rs' for name in ['evidence','identity','invocation','output','protocol','mod']}|{'apps/report/src/generated/report.ts','providers/typescript/src/generated/protocol.ts'}
    collector=module(code/'admission.py','pipeline_collector')
    outputs=collector.collect_outputs(final,expected_outputs)
    for row in closure:
        if pin(original_root/row['path'])!={k:row[k] for k in ['bytes','sha256']}:raise ValueError('input changed during generation')
    for name,path in original_tools.items():
        if pin(path)!=expected[name]:raise ValueError('executable changed during generation')
    result={'passed':True,'sources':len(sources),'entryPoints':len(options['entryPoints']),
            'outputs':[{'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for name,raw in sorted(outputs.items())],
            'inputClosure':pin(out/'input-closure.json'),'nativeTypes':receipt['nativeTypes'],
            'standing':'Observed combined development generation only; no source approval, package provisioning/confinement or release qualification',
            'sourceApproved':False,'confinementQualified':False,'allChildrenSeatbelt':True,'verifiedInputSnapshot':True,'outputRoot':str(final.relative_to(out)),'productModified':False}
    write(out/'result.json',result);print(json.dumps({'passed':True,'sources':len(sources),'outputs':len(outputs)}))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['root','output','node','generator','python']:p.add_argument('--'+name,required=True,type=Path)
    run(p.parse_args())
