from pathlib import Path
w=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover/crates/components/src/provider_protocol/rust3');p=w/'receive.rs';s=p.read_text()
def replace(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:100]);s=s.replace(old,new,1)
replace('pub struct Rust3DispatchContext {\n','pub struct Rust3DispatchContext {\n    /// C4-selected owed census closure, or None; signed token is in Hello.\n    pub symbol_census: Option<String>,\n')
replace('    pub spool_entries: Vec<Vec<u8>>,\n','''    pub spool_entries: Vec<Vec<u8>>,
    /// Generated census from an admitted CompleteV3. Original full bytes
    /// remain in the one-shot candidate handoff for H settlement.
    pub census: Option<opensip_contracts::generated::protocol::SymbolCensus1SymbolCensusV1>,
''')
replace('struct Law {\n','struct Law {\n    census: super::census::Law,\n')
replace('''        Ok(Self {
            max_snapshot_entries,
''','''        Ok(Self {
            census: super::census::Law::load()?,
            max_snapshot_entries,
''')
replace('    target_attribution: bool,\n','    target_attribution: bool,\n    census_token: bool,\n')
start=s.index('        // The census path is wired as part of the same complete4c unit;');end=s.index('        let open =',start)
s=s[:start]+'''        let census_token = array_of(hello, "expectedCapabilities")
            .iter().any(|x| matches!(x, Value::Text(s) if s=="symbol-census-v1"));
        if !census_token && context.symbol_census.is_some() {
            return Err(Context("census owed without selected token".to_owned()));
        }
        if let Some(closure) = &context.symbol_census {
            super::admit_extern("opensip.product.symbol-census.1#/$defs/SymbolCensusRequestV1",
                &Value::Map(vec![("enumeratorClosure".to_owned(),Value::Text(closure.clone()))]))
                .map_err(Context)?;
        }
'''+s[end:]
replace('''                let key = RequestedKey {
                    relation: get("relation")?,''','''                let relation = get("relation")?;
                let subject_count = if census_token && law.census.is_symbol(&relation) {
                    0
                } else { subject_count };
                let key = RequestedKey {
                    relation,''')
replace('''        let live = vec![StageLive::default(); stages.len()];
''','''        let mut request_keys = Vec::new();
        for stage in &context.stages {
            let d=map_of(&stage.analysis_domain).ok_or_else(||Context("analysis domain".to_owned()))?;
            request_keys.extend(array_of(d,"requestedCoverageDomain").iter());
        }
        law.census.request_keys(
            text_of(open,"snapshotId").ok_or_else(||Context("snapshotId".to_owned()))?,
            request_keys.into_iter(), census_token, context.symbol_census.as_deref(),
        ).map_err(Context)?;
        let live = vec![StageLive::default(); stages.len()];
''')
replace('''            target_attribution,
            accounting:''','''            target_attribution,
            census_token,
            accounting:''')
replace('''        let payload = match build::convert(&name, payload, self.target_attribution, &phase) {
''','''        let census = if self.census_token && name == "Complete" {
            match get_census(payload).and_then(super::super::ts2::build::census) {
                Ok(census) => census,
                Err(e) => return self.refused(Rust3Refusal::Admission(e)),
            }
        } else { None };
        let payload = match build::convert(&name, payload, self.target_attribution, &phase) {
''')
replace('''            payload,
            spool_entries,
''','''            payload,
            spool_entries,
            census,
''')
replace('''            .check_payload(&name, payload, self.phase(), self.target_attribution)
''','''            .check_selected_payload(&name, payload, self.phase(), self.target_attribution, self.census_token)
''')
replace('''            "Complete" => self.complete(f).map_err(Admission)?,''','''            "Complete" => {
                if self.census_token {
                    self.law.census.returned(frame, node, payload, self.context.symbol_census.is_some())
                        .map_err(Admission)?;
                }
                self.complete(f).map_err(Admission)?;
            }''')
replace('''    fn entry_echoes(entry: &Value, key: &RequestedKey) -> Result<(), String> {''','''    fn entry_echoes(entry: &Value, key: &RequestedKey, census_decided: bool) -> Result<(), String> {''')
replace('''            && text_of(k, "subjectScopeCommitment") == Some(&key.subject_scope_commitment)
''','''            && (census_decided || text_of(k, "subjectScopeCommitment") == Some(&key.subject_scope_commitment))
''')
replace('''            && text_of(examined, "subjectScopeCommitment") == Some(&key.subject_scope_commitment)
            && u64_of(examined, "subjectCount") == Some(key.subject_count);''','''            && (census_decided || text_of(examined, "subjectScopeCommitment") == Some(&key.subject_scope_commitment))
            && (census_decided || u64_of(examined, "subjectCount") == Some(key.subject_count));''')
old='''            Self::entry_echoes(e, k)?;''';assert s.count(old)==2;s=s.replace(old,'''            let census_decided = self.context.symbol_census.is_some() && self.law.census.is_symbol(&k.relation);
            Self::entry_echoes(e, k, census_decided)?;''',1);s=s.replace(old,'''            Self::entry_echoes(e, k, false)?;''',1)
replace('''fn suffix(id: &str) -> Option<&str> {''','''fn get_census(payload: &Value) -> Result<&Value, String> {
    map_of(payload).and_then(|f| field(f,"symbolCensus")).ok_or_else(||"symbolCensus".to_owned())
}
fn suffix(id: &str) -> Option<&str> {''')
p.write_text(s)
p=w/'receive_tests.rs';s=p.read_text();needle='    Rust3DispatchContext {\n';assert s.count(needle)==1;p.write_text(s.replace(needle,needle+'        symbol_census: None,\n',1))
print('Wired census response schema/context/generated handoff and exact H boundary; no test claim yet.')
