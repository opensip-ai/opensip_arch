"""Outside-product RPP snapshot receiver; harness validation, not source admission.

Semantic payloads must come from a separately validating frame decoder. The
snapshot2 descriptor, complete workload and dependency-source joins remain caller
work. Symlinks are retained as raw declarations; no filesystem links are made.
"""
import hashlib
import re
import types
import unicodedata

UINT64_MAX=2**64-1
MAX_ENTRIES=200_000
MAX_TOTAL_BYTES=2**33
MAX_CHUNK_BYTES=2**20

class HarnessRefusal(ValueError):
    pass

def uint(value):
    if type(value) is not int or not 0 <= value <= UINT64_MAX:
        raise HarnessRefusal('uint64')
    return value

def exact(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise HarnessRefusal('closed payload shape')

def path(value):
    if type(value) is not str or not value or unicodedata.normalize('NFC',value)!=value:
        raise HarnessRefusal('canonical path text')
    value.encode('utf8','strict')
    if '\\' in value or '\0' in value or re.match(r'^[A-Za-z]:',value) or any(x in ('','.', '..') for x in value.split('/')):
        raise HarnessRefusal('canonical path segments')
    return value

def digest(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}',value) is None:
        raise HarnessRefusal('digest hex')
    return value

class Receiver:
    def __init__(self, cbor_encoder):
        self.encode=cbor_encoder
        self.state='manifest'
        self.files={}
        self.links={}
        self.regular=[]
        self.position=0
        self.chunk_index=0
        self.current=bytearray()
        self.total=0
        self.chunks=0

    def manifest(self, value):
        try:
            if self.state!='manifest':raise HarnessRefusal('manifest phase')
            exact(value, ['snapshotId','manifestSha256','entries'])
            sid=value['snapshotId']
            if type(sid) is not str or not sid.startswith('snapshot2:'):raise HarnessRefusal('snapshot shape')
            digest(sid[10:]);digest(value['manifestSha256'])
            entries=value['entries']
            if type(entries) is not list or not 1<=len(entries)<=MAX_ENTRIES:raise HarnessRefusal('manifest count')
            if hashlib.sha256(self.encode(entries)).hexdigest()!=value['manifestSha256']:raise HarnessRefusal('manifest digest')
            previous=None;declared=0;names=set()
            for row in entries:
                exact(row,['path','kind','byteLength','contentSha256','executable','targetBytes'])
                name=path(row['path']);order=name.encode('utf8')
                if previous is not None and order<=previous:raise HarnessRefusal('path order/duplicate')
                previous=order
                parts=name.split('/')
                if any('/'.join(parts[:i]) in names for i in range(1,len(parts))):raise HarnessRefusal('VFS entry ancestor collision')
                names.add(name)
                if row['kind']=='file':
                    size=uint(row['byteLength']);digest(row['contentSha256'])
                    if type(row['executable']) is not bool or row['targetBytes'] is not None:raise HarnessRefusal('file variant')
                    declared+=size
                    if declared>MAX_TOTAL_BYTES:raise HarnessRefusal('snapshot total bytes')
                    self.regular.append(dict(row))
                elif row['kind']=='symlink':
                    if any(row[k] is not None for k in ['byteLength','contentSha256','executable']) or type(row['targetBytes']) is not bytes or not row['targetBytes']:raise HarnessRefusal('symlink variant')
                    self.links[name]=row['targetBytes']
                else:raise HarnessRefusal('entry variant')
            self.snapshot_id=sid;self.manifest_sha=value['manifestSha256'];self.entry_count=len(entries)
            self.state='chunks';self._finish_empty()
        except Exception:
            self.state='failed';raise

    def _finish_empty(self):
        while self.position<len(self.regular) and self.regular[self.position]['byteLength']==0:
            row=self.regular[self.position]
            if row['contentSha256']!=hashlib.sha256(b'').hexdigest():raise HarnessRefusal('empty file digest')
            self.files[row['path']]=b'';self.position+=1

    def chunk(self, value):
        try:
            if self.state!='chunks' or self.position>=len(self.regular):raise HarnessRefusal('chunk phase/order')
            exact(value,['snapshotId','path','chunkIndex','byteOffset','bytes'])
            row=self.regular[self.position]
            if value['snapshotId']!=self.snapshot_id or value['path']!=row['path'] or uint(value['chunkIndex'])!=self.chunk_index or uint(value['byteOffset'])!=len(self.current):raise HarnessRefusal('chunk association/order')
            raw=value['bytes']
            if type(raw) is not bytes or not 1<=len(raw)<=MAX_CHUNK_BYTES:raise HarnessRefusal('chunk bytes')
            if len(raw)>row['byteLength']-len(self.current):raise HarnessRefusal('file overrun')
            if self.total+len(raw)>MAX_TOTAL_BYTES or self.chunks==UINT64_MAX or self.chunk_index==UINT64_MAX:raise HarnessRefusal('aggregate bound')
            self.current.extend(raw);self.total+=len(raw);self.chunks+=1;self.chunk_index+=1
            if len(self.current)==row['byteLength']:
                if hashlib.sha256(self.current).hexdigest()!=row['contentSha256']:raise HarnessRefusal('file digest')
                self.files[row['path']]=bytes(self.current);self.current=bytearray();self.position+=1;self.chunk_index=0;self._finish_empty()
        except Exception:
            self.state='failed';raise

    def seal(self,value):
        try:
            if self.state!='chunks' or self.position!=len(self.regular) or self.current:raise HarnessRefusal('incomplete snapshot')
            exact(value,['snapshotId','manifestSha256','entryCount','totalFileBytes','totalChunkCount'])
            for key in ['entryCount','totalFileBytes','totalChunkCount']:uint(value[key])
            expected=dict(snapshotId=self.snapshot_id,manifestSha256=self.manifest_sha,entryCount=self.entry_count,totalFileBytes=self.total,totalChunkCount=self.chunks)
            if value!=expected:raise HarnessRefusal('seal aggregate/association')
            self.state='accepted'
            return dict(expected),types.MappingProxyType(dict(self.files)),types.MappingProxyType(dict(self.links))
        except Exception:
            self.state='failed';raise
