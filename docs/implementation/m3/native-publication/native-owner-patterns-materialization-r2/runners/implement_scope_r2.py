"""Prepare isolated scoped-owner implementation; no pins, integration or acceptance."""
from pathlib import Path
import os,subprocess,json,hashlib,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover'
assert not W.exists()
base=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=P,text=True).strip()
subprocess.run(['/usr/bin/git','worktree','add','--detach',str(W),base],cwd=P,check=True)
for p in sorted((F/'proposed').rglob('*')):
 if p.is_file():shutil.copyfile(p,W/p.relative_to(F/'proposed'))
inputs=json.loads((F/'ecma-scope-differential-r1/inputs.json').read_text())
def rust_string(s):
 # Raw literals preserve regex backslashes without another decoding step.
 assert '"##' not in s
 return 'r##"'+s+'"##'
forms=sorted(inputs['forms'])
p=W/'crates/identity/src/schema_patterns.rs';code=p.read_text()
assert 'matches_native_owner' not in code
code+='''
/// Closed selected native-owner ECMA-u pattern forms. The schema registry
/// invokes this only for a pinned native owner document; all other schemas
/// retain `matches`, including identical literal text in an unrelated owner.
pub(crate) fn matches_native_owner(pattern: &str, value: &str) -> Result<bool, &'static str> {
    const FORMS: &[&str] = &[
'''+''.join('        '+rust_string(s)+',\n' for s in forms)+'''    ];
    if !FORMS.contains(&pattern) {
        return Err("unselected native owner pattern");
    }
    // ECMA-u without m: `$` is the actual end of input, not a position
    // before a final LF. This exact pattern is occupancy's `not` child.
    if pattern == r##"(^|/)\.\.?(/|$)"## {
        return Ok(value.split('/').any(|part| matches!(part, "." | "..")));
    }
    matches(pattern, value)
}
''';p.write_text(code)
p=W/'crates/identity/src/schema.rs';code=p.read_text()
old='    entries: BTreeSet<String>,\n';assert code.count(old)==1
code=code.replace(old,old+'''    // Enabled only by the exact registered source-set constructor. Public
    // arbitrary-schema compilation keeps its inherited pattern semantics.
    native_owner_patterns: bool,
''')
old='''    pub fn compile(documents: Vec<V>, entries: &[&str], budget: usize) -> Result<Self, Error> {
        let mut meter = Meter { remaining: budget };'''
new='''    pub fn compile(documents: Vec<V>, entries: &[&str], budget: usize) -> Result<Self, Error> {
        Self::compile_profile(documents, entries, budget, false)
    }

    /// The selected registry calls this only after every raw source has
    /// passed its complete document pin. No caller-selected owner or pattern
    /// list crosses the public RegisteredSchemas boundary.
    pub(crate) fn compile_registered_native_owners(
        documents: Vec<V>, entries: &[&str], budget: usize,
    ) -> Result<Self, Error> {
        Self::compile_profile(documents, entries, budget, true)
    }

    fn compile_profile(documents: Vec<V>, entries: &[&str], budget: usize, native_owner_patterns: bool) -> Result<Self, Error> {
        let mut meter = Meter { remaining: budget };'''
assert code.count(old)==1;code=code.replace(old,new)
old='''            entries: selected,
        };''';assert code.count(old)==1;code=code.replace(old,'''            entries: selected,
            native_owner_patterns,
        };''')
old='''                    crate::schema_patterns::matches(text(v)?, "").map_err(|_| Error::Pattern)?;'''
assert code.count(old)==1;code=code.replace(old,'''                    self.pattern_matches(owner, text(v)?, "").map_err(|_| Error::Pattern)?;''')
old='''!crate::schema_patterns::matches(crate_text(p)?, text)''';assert code.count(old)==1;code=code.replace(old,'''!self.pattern_matches(owner, crate_text(p)?, text)''')
at='''    fn resolve(&self, reference: &str, owner: &str) -> Result<(&V, &str), Error> {'''
assert code.count(at)==1;code=code.replace(at,'''    /// `owner` is the actual resolved document, including after an external
    /// $ref. The startup owner reaches the native evidence document this way;
    /// foreign documents reached from it do not acquire native semantics.
    fn pattern_matches(&self, owner: &str, pattern: &str, value: &str) -> Result<bool, &'static str> {
        if self.native_owner_patterns && matches!(owner,
            "urn:opensip:product-v1:native:evidence-schemas:v2"
            | "opensip.product.occupancy-companion.1"
            | "opensip.product.relation-payload.2") {
            crate::schema_patterns::matches_native_owner(pattern, value)
        } else {
            crate::schema_patterns::matches(pattern, value)
        }
    }

'''+at)
p.write_text(code)
p=W/'crates/identity/src/schema_registry.rs';code=p.read_text();old='''let program = Program::compile(documents, &refs, 200_000_000)?;''';assert code.count(old)==1;code=code.replace(old,'''let program = Program::compile_registered_native_owners(documents, &refs, 200_000_000)?;''');p.write_text(code)
paths=subprocess.check_output(['/usr/bin/git','diff','--name-only'],cwd=W,text=True).splitlines()
report=dict(standing='ISOLATED SOURCE IMPLEMENTATION ONLY; SOURCE PINS NOT UPDATED; NOT BUILDABLE REGISTERED CANDIDATE OR ACCEPTED UNIT',productBase=base,worktree=str(W),changedFiles=paths,patternLiteralForms=26,closedNativeDocuments=['urn:opensip:product-v1:native:evidence-schemas:v2','opensip.product.occupancy-companion.1','opensip.product.relation-payload.2'],genericProgramCompileUnchanged=True,patternPropertiesUnchanged=True,sourcePinsUpdated=False,generatorRun=False,blindRefreshComplete=False,productQualification=False)
(F/'scope-implementation-r2.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
