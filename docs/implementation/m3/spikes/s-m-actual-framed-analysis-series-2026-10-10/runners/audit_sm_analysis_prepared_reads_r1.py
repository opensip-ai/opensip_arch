"""Offline audit of observed FileLoader reads; not snapshot2/plan2 or full FS sealing."""
from pathlib import Path
import json,hashlib,struct
def digest(raw):return hashlib.sha256(raw).hexdigest()
def decode_map(raw):
 assert raw.startswith(b'OPSMRUST1\0');at=10
 def number():
  nonlocal at
  assert at+8<=len(raw);n=struct.unpack_from('>Q',raw,at)[0];at+=8;return n
 def take(n):
  nonlocal at
  assert at+n<=len(raw);b=raw[at:at+n];at+=n;return b
 count=number();assert count<=100000;files={};total=0
 for _ in range(count):
  path=take(number()).decode('utf8');assert path.startswith('/') and path not in files
  content=take(number());total+=len(content);assert total<=8*1024**3
  files[path]=dict(path=path,bytes=len(content),sha256=digest(content))
 assert at==len(raw);return files
def audit(source_map_pin,unit_results):
 raw=Path(source_map_pin['path']).read_bytes();assert len(raw)==source_map_pin['bytes'] and digest(raw)==source_map_pin['sha256'];files=decode_map(raw);units=[];union={}
 for unit in unit_results:
  if not unit['compilerLaunched']:continue
  rows={};denied=[];reads=[e for e in unit['events'] if e['event']=='prepared_source_read']
  for event in reads:
   path=event['normalizedPath'];row=files.get(path)
   if event['preparedMapEntryPresent']:
    assert row is not None and row['bytes']==event['contentBytes'];rows[path]=row;union[path]=row
   else:
    assert row is None and event['contentBytes'] is None;denied.append(path)
  ordered=[rows[k] for k in sorted(rows,key=lambda p:p.encode('utf8'))];encoded=json.dumps(ordered,ensure_ascii=False,separators=(',',':')).encode('utf8');assert len(encoded)<=4*1024**2
  units.append(dict(unitIndex=unit['index'],observedReadCalls=len(reads),distinctMappedSourceFiles=len(ordered),mappedSourceContentBytes=sum(r['bytes'] for r in ordered),mappedSourceFilePins=ordered,experimentalAbsolutePathDescriptorBytes=len(encoded),experimentalAbsolutePathDescriptorSha256=digest(encoded),deniedReadPaths=denied,snapshot2Plan2Equivalent=False,metadataSysrootRuntimeReadsSealed=False))
 ordered=[union[k] for k in sorted(union,key=lambda p:p.encode('utf8'))]
 return dict(sourceMapPin=source_map_pin,unitReadSets=units,distinctMappedSourceFiles=len(ordered),mappedSourceContentBytes=sum(r['bytes'] for r in ordered),mappedSourceFilePins=ordered,sourceAuthentication=False,nativeAdmission=False,fullReadSetSealed=False,snapshot2Plan2Equivalent=False)
