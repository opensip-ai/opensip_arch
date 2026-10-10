"""Throwaway native CBOR/frame byte validation. Not whole protocol conformance."""
import hashlib

MAX_FRAME_PAYLOAD=2**26
MAX_REQUEST_PAYLOAD=9663676416
MAX_REQUEST_FRAMES=1_000_000

class WireRefusal(ValueError):
    pass

def decode_canonical(raw, encode):
    at=0
    def take(n):
        nonlocal at
        if n>len(raw)-at:raise WireRefusal('truncated CBOR')
        result=raw[at:at+n];at+=n;return result
    def argument(additional):
        if additional<24:return additional
        widths={24:1,25:2,26:4,27:8}
        if additional not in widths:raise WireRefusal('indefinite/reserved argument')
        width=widths[additional];value=int.from_bytes(take(width),'big')
        minimum={1:24,2:256,4:65536,8:2**32}[width]
        if value<minimum:raise WireRefusal('non-shortest argument')
        return value
    def value():
        tag=take(1)[0];major=tag>>5;additional=tag&31
        if major==7:
            if tag==0xf4:return False
            if tag==0xf5:return True
            if tag==0xf6:return None
            raise WireRefusal('forbidden simple/float value')
        if major not in (0,2,3,4,5):raise WireRefusal('forbidden CBOR major')
        n=argument(additional)
        if major==0:return n
        if major==2:return take(n)
        if major==3:
            try:return take(n).decode('utf8','strict')
            except UnicodeError as e:raise WireRefusal('invalid UTF8') from e
        if major==4:
            if n>len(raw)-at:raise WireRefusal('impossible array cardinality')
            return [value() for _ in range(n)]
        if n>(len(raw)-at)//2:raise WireRefusal('impossible map cardinality')
        result={};previous=None
        for _ in range(n):
            begin=at;key=value();encoded_key=raw[begin:at]
            if type(key) is not str:raise WireRefusal('nontext map key')
            order=(len(encoded_key),encoded_key)
            if previous is not None and order<=previous:raise WireRefusal('map order/duplicate')
            previous=order;result[key]=value()
        return result
    result=value()
    if at!=len(raw):raise WireRefusal('trailing CBOR bytes')
    if encode(result)!=raw:raise WireRefusal('noncanonical CBOR')
    return result

class Reader:
    def __init__(self, stream, encoder):
        self.stream=stream;self.encode=encoder;self.payload_bytes=0;self.frames=0;self.failed=False
    def _exact(self,n):
        parts=[];remaining=n
        while remaining:
            part=self.stream.read(remaining)
            if not part or len(part)>remaining:raise WireRefusal('truncated frame')
            parts.append(part);remaining-=len(part)
        return b''.join(parts)
    def next(self):
        try:
            if self.failed:raise WireRefusal('failed reader reuse')
            length=int.from_bytes(self._exact(8),'big')
            if length>MAX_FRAME_PAYLOAD:raise WireRefusal('frame payload bound before allocation')
            if length>MAX_REQUEST_PAYLOAD-self.payload_bytes or self.frames>=MAX_REQUEST_FRAMES:raise WireRefusal('request aggregate bound')
            claimed=self._exact(32);raw=self._exact(length)
            if hashlib.sha256(raw).digest()!=claimed:raise WireRefusal('frame digest')
            decoded=decode_canonical(raw,self.encode)
            self.payload_bytes+=length;self.frames+=1
            return decoded,raw
        except Exception:
            self.failed=True;raise

def frame(value,encode):
    raw=encode(value)
    if len(raw)>MAX_FRAME_PAYLOAD:raise WireRefusal('frame payload bound')
    return len(raw).to_bytes(8,'big')+hashlib.sha256(raw).digest()+raw
