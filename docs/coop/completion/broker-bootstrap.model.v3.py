"""Closed bootstrap successor parser for the typed SDK reference design.
Launch and predecessor host-admission evidence remain frozen in bootstrap v2;
current request admission is broker-host-security-join.v1.py, not a second helper.
"""
import base64, json, re
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
KEY='OPENSIP_BROKER_CONTEXT'
FIXED={'LC_ALL':'C','LANG':'C','TZ':'UTC','UV_THREADPOOL_SIZE':'4'}
VALIDATOR=Draft202012Validator(json.loads((HERE/'broker-bootstrap.schema.v3.json').read_text()))
class StartupFailure(Exception):pass
def fail():raise StartupFailure('BROKER-BOOTSTRAP-INVALID')
def pairs(items):
 d={}
 for k,v in items:
  if k in d:fail()
  d[k]=v
 return d
def integer(s):
 if s!='1':fail()
 return 1
def reject_number(s):fail()
def encode(value):return base64.urlsafe_b64encode(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).rstrip(b'=').decode('ascii')
def parse(value):
 if not isinstance(value,str) or not 0<len(value)<=16384 or re.fullmatch('[A-Za-z0-9_-]+',value) is None:fail()
 try:raw=base64.b64decode(value+'='*((-len(value))%4),altchars=b'-_',validate=True)
 except (ValueError,TypeError):fail()
 if len(raw)>12288 or base64.urlsafe_b64encode(raw).rstrip(b'=').decode()!=value:fail()
 try:text=raw.decode('utf-8')
 except UnicodeError:fail()
 # Admission scanner bounds containers before the recursive JSON implementation.
 depth=0;quoted=False;escape=False
 for c in text:
  if quoted:
   if escape:escape=False
   elif ord(c)==92:escape=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c in '[{':
   depth+=1
   if depth>8:fail()
  elif c in ']}':depth-=1
 try:v=json.loads(text,object_pairs_hook=pairs,parse_int=integer,parse_float=reject_number,parse_constant=reject_number)
 except (ValueError,TypeError,RecursionError):fail()
 pending=[v]
 while pending:
  x=pending.pop()
  if isinstance(x,str):
   try:x.encode('utf-8')
   except UnicodeError:fail()
  elif isinstance(x,dict):pending.extend(x.keys());pending.extend(x.values())
  elif isinstance(x,list):pending.extend(x)
 if not VALIDATOR.is_valid(v) or type(v['bootstrapVersion']) is not int:fail()
 if 'resultScratchRoot' in v:
  root=v['resultScratchRoot']
  if len(root.encode('utf-8'))>4096 or not root.startswith('/') or '\x00' in root or any(part in ('','.','..') for part in root.split('/')[1:]):fail()
 handles=v['handles']
 for key in ('authorizationRef',):
  if len({h[key] for h in handles})!=len(handles):fail()
 return v
