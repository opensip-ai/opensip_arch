"""Exploratory finite 2020-12 meta-schema projection, formats annotation-only.
Not selected, not product, not a general instance validator or regex compiler.
Domain: JSON values parsed under current OpenSIP integer-only canonical profile.
"""
def valid(v):
 if type(v)is bool:return True
 if type(v)is not dict:return False
 def anchor(x):
  if type(x)is not str:return False
  # Exact fixed Python meta-pattern ^[A-Za-z_][-A-Za-z0-9._]*$ semantics.
  x=x[:-1]if x.endswith('\n')else x
  return bool(x)and x[0]in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789.-'for c in x[1:])
 def ident(x):
  if type(x)is not str:return False
  # Exact fixed ^[^#]*#?$; its first class also consumes newlines.
  return '#'not in x or x.count('#')==1 and (x.endswith('#')or x.endswith('#\n'))
 def strs(x):return type(x)is list and all(type(i)is str for i in x)and len(set(x))==len(x)
 for k,x in v.items():
  if k=='$id':
   if not ident(x):return False
  elif k in ['$schema','$ref','$dynamicRef','$recursiveRef','$comment','title','description','format','contentEncoding','contentMediaType','pattern']:
   if type(x)is not str:return False
  elif k in ['$anchor','$dynamicAnchor','$recursiveAnchor']:
   if not anchor(x):return False
  elif k=='$vocabulary':
   if type(x)is not dict or any(type(t)is not bool for t in x.values()):return False
  elif k in ['$defs','definitions','properties','patternProperties','dependentSchemas']:
   if type(x)is not dict or not all(valid(t)for t in x.values()):return False
  elif k in ['items','contains','additionalProperties','propertyNames','if','then','else','not','unevaluatedItems','unevaluatedProperties','contentSchema']:
   if not valid(x):return False
  elif k in ['prefixItems','allOf','anyOf','oneOf']:
   if type(x)is not list or not x or not all(valid(t)for t in x):return False
  elif k=='dependencies':
   if type(x)is not dict or not all(valid(t)or strs(t)for t in x.values()):return False
  elif k=='dependentRequired':
   if type(x)is not dict or not all(strs(t)for t in x.values()):return False
  elif k=='type':
   kinds={'array','boolean','integer','null','number','object','string'}
   if not(type(x)is str and x in kinds or type(x)is list and bool(x)and strs(x)and all(t in kinds for t in x)):return False
  elif k in ['enum','examples']:
   if type(x)is not list:return False
  elif k in ['maximum','exclusiveMaximum','minimum','exclusiveMinimum','multipleOf']:
   if type(x)is not int or k=='multipleOf'and x<=0:return False
  elif k in ['maxLength','minLength','maxItems','minItems','maxContains','minContains','maxProperties','minProperties']:
   if type(x)is not int or x<0:return False
  elif k in ['uniqueItems','deprecated','readOnly','writeOnly']:
   if type(x)is not bool:return False
  elif k=='required':
   if not strs(x):return False
 return True
