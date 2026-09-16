import os,shutil,hashlib,re
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
PKG='/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2/author-helpers'
DST=S+'/output/files/helpers-successor'
os.makedirs(DST,exist_ok=True)
src=open(PKG+'/ts_pilot.py',encoding='utf-8').read()
before=hashlib.sha256(src.encode()).hexdigest()
NL=chr(10)
old_sig='def _binding(provider_id, ctx_hex, uhex, program_entry, extents, candidate_paths=None) -> dict:'+NL
new_sig=('def _default_unit_binding(provider_id, ctx_hex, uhex, extents, candidate_paths=None) -> dict:'+NL+
         '    """Build THE default-unit program binding for a TS cell.'+NL+
         ''+NL+
         '    Successor note (author reference helper, isolated): the predecessor took a'+NL+
         '    `program_entry` argument and then ignored it, because U-1 requires the default-unit'+NL+
         '    binding to carry `programEntry: null` (enumeration_model admits a non-null entry only'+NL+
         '    when provenance is not `default-unit`). The dead argument is removed rather than'+NL+
         '    silently tolerated, and the name now states what this constructor actually builds.'+NL+
         '    This helper deliberately cannot express an additional-program binding; that needs its'+NL+
         '    own constructor with a non-default provenance and a selected config path.'+NL+
         '    """'+NL)
assert src.count(old_sig)==1, src.count(old_sig)
src=src.replace(old_sig,new_sig,1)
old_call='_binding(provider_id, ctx_hex, uhex, "tsconfig.json", extents, cand)'
new_call='_default_unit_binding(provider_id, ctx_hex, uhex, extents, cand)'
assert src.count(old_call)==1, src.count(old_call)
src=src.replace(old_call,new_call,1)
rem=re.findall(r'(?<![A-Za-z_])_binding\(', src)
assert not rem, rem
open(DST+'/ts_pilot.py','w',encoding='utf-8').write(src)
print('predecessor ts_pilot.py sha (preserved, unmodified):',before)
print('successor    ts_pilot.py sha:',hashlib.sha256(src.encode()).hexdigest())
print('remaining _binding( call sites:',len(rem),')')
