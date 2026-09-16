import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B
import run_ts as RT

g = RT.build()
ctx = g['st'].objects['native.context.typescript.v2#' + g['ctx_hex']]
kw, sites = S.walk_keywords(B.NATIVE_DOC, '#/$defs/TypeScriptNativeContextV2', ctx)
print('keyword refusals:', kw)
print('sites:', len(sites))
for s in sites:
    print('  %-70s ret=%-20s rep=%s' % (s['instancePath'],
                                        s['annotation'].get('retention', 'preimage'),
                                        s['annotation'].get('representation')))
