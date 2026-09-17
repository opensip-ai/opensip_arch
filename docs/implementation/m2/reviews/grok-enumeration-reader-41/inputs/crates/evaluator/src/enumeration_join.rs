//! Private draft: reconstruct enumeration inputs from retained bytes. The
//! complete join, oracle checks and public API are not yet implemented.
#![allow(dead_code)]
use alloc::{collections::{BTreeMap, BTreeSet}, format, string::String, vec::Vec};
use opensip_identity::{GraphError, IdentityDomain as D, JsonValue as V, NativeFrameSet,
    RetainedInputs, TraversalBudget, digest_hex, parse_json};
use crate::native_universe::{array, field, text, sha256_text};
use crate::{NativeUniverseError, NativeRetentionError, PlanNativeError};

#[derive(Debug, PartialEq, Eq)]
pub(crate) enum JoinError {
    Record(GraphError), Native(NativeUniverseError), Retention(NativeRetentionError),
    Plan(PlanNativeError), Refused(String), Limit, Law,
}
impl From<NativeUniverseError> for JoinError { fn from(e: NativeUniverseError) -> Self { Self::Native(e) } }
fn bare(v: &V) -> Result<[u8;32], JoinError> { Ok(sha256_text(&format!("sha256:{}",text(v)?))?) }
fn object(inputs: &RetainedInputs<'_>, id: &str, domain: D, work: usize) -> Result<V,JoinError> {
    Ok(inputs.object(id,domain,work).map_err(|e|JoinError::Record(GraphError::Input(e)))?.descriptor().clone())
}
fn record(inputs: &RetainedInputs<'_>, digest: [u8;32]) -> Result<V,JoinError> {
    inputs.blob(digest).and_then(|b|b.canonical_record()).map_err(|e|JoinError::Record(GraphError::Input(e)))
}
fn step(remaining: &mut usize) -> Result<(),JoinError> {
    *remaining=remaining.checked_sub(1).ok_or(JoinError::Limit)?;Ok(())
}
/// Private maps produced only by the retained reader. No constructor or public
/// caller-supplied ADMIT, bindResult or membership derivation witness.
struct JoinInputs {
    plan: V, analysis: V, scope: V, enumeration: V, membership: V,
    snapshot_inventory: V, snapshot_paths: Vec<String>,
    snapshot_index: BTreeMap<String,V>, source_blobs: BTreeMap<String,Vec<u8>>,
    contexts: BTreeMap<String,V>, universes: BTreeMap<String,V>,
    universe_domains: BTreeMap<String,String>, retained: BTreeMap<String,V>,
    closures: BTreeMap<String,V>, inventories: Vec<V>,
}
/// Local reader budget counts visits; each native owner/schema receives a
/// separate copied bound. This is not a global CPU or Plan work-unit bound.
fn read_inputs(inputs: &RetainedInputs<'_>, plan_id: &str,
    inventory_refs: &[[u8;32]], budget: TraversalBudget) -> Result<JoinInputs,JoinError> {
    if budget.depth==0 {return Err(JoinError::Limit)}
    let mut remaining=budget.steps;step(&mut remaining)?;
    let plan=object(inputs,plan_id,D::Plan,budget.descriptor_work)?;
    let snapshot_id=text(field(&plan,"snapshotId")?)?;
    let snapshot=object(inputs,snapshot_id,D::Snapshot,budget.descriptor_work)?;
    let analysis=inputs.identity_record_shape(bare(field(&plan,"analysisSpecDigest")?)?,"analysis-spec",budget.descriptor_work).map_err(JoinError::Record)?;
    let scope=record(inputs,bare(field(&plan,"scopeDigest")?)?)?;
    // Registry bytes are source-bound, shared with the already selected
    // parameter owner; unknown/duplicate rows cannot supply an enum payload.
    let registry=parse_json(include_bytes!("import-registry.json")).map_err(|_|JoinError::Law)?;
    let mut selected=BTreeMap::new();
    for parameter in array(field(&analysis,"parameters")?)? {
        step(&mut remaining)?;
        let mut matched=None;
        for row in array(field(&registry,"rows")?)? {
            step(&mut remaining)?;
            if field(row,"sha256")?==field(parameter,"schemaDigest")? {
                if matched.is_some(){return Err(JoinError::Law)}
                matched=Some(row);
            }
        }
        let row=matched.ok_or_else(||JoinError::Refused("EVALUATOR_PARAMETER_UNREGISTERED".into()))?;
        let key=text(field(row,"key")?)?;
        if selected.contains_key(key){return Err(JoinError::Refused("EVALUATOR_PARAMETER_DUPLICATE".into()))}
        let value=inputs.registered_record_shape(bare(field(parameter,"payloadDigest")?)?,
            bare(field(parameter,"schemaDigest")?)?,text(field(row,"document")?)?,
            text(field(row,"selector")?)?,budget.descriptor_work).map_err(JoinError::Record)?;
        selected.insert(String::from(key),value);
    }
    let enumeration=selected.remove("foundation/enumeration-plan.schema.v1.json")
        .ok_or_else(||JoinError::Refused("EVALUATOR_REQUIRED_PARAMETER_MISSING:foundation/enumeration-plan.schema.v1.json".into()))?;
    // Emission/policy binding belongs to complete reconstruct, not this join.
    let membership=inputs.current_record_shape(bare(field(&enumeration,"membershipDigest")?)?,
        "native/native-evidence.schemas.v2.json","#/$defs/UnitMembershipV1",budget.descriptor_work).map_err(JoinError::Record)?;
    let snapshot_inventory=field(&snapshot,"sourceInventory")?.clone();
    let mut snapshot_paths=Vec::new();let mut snapshot_index=BTreeMap::new();let mut source_blobs=BTreeMap::new();
    for row in array(&snapshot_inventory)? {
        step(&mut remaining)?;let path=text(field(row,"path")?)?;
        if snapshot_index.insert(String::from(path),row.clone()).is_some(){return Err(JoinError::Refused("ENUMERATION_ADMISSION_PRECONDITION".into()))}
        snapshot_paths.push(String::from(path));
        // Reconstruct requires all source bytes; no host-claimed path->bytes
        // table and no missing-manifest fallback enter the evaluator.
        let blob=inputs.blob(bare(field(row,"sha256")?)?).map_err(|e|JoinError::Record(GraphError::Input(e)))?;
        let V::Integer(n)=field(row,"bytes")? else{return Err(JoinError::Law)};
        blob.require_length(u64::try_from(n.get()).map_err(|_|JoinError::Law)?).map_err(|e|JoinError::Record(GraphError::Input(e)))?;
        source_blobs.insert(String::from(path),blob.bytes().to_vec());
    }
    let mut contexts=BTreeMap::new();let mut context_digests=Vec::new();
    for value in array(field(&plan,"nativeContextDigests")?)? {
        step(&mut remaining)?;let d=bare(value)?;
        crate::inspect_native_retention(inputs,d,NativeFrameSet::Context,snapshot_id,budget).map_err(JoinError::Retention)?;
        let frame=inputs.frame_candidate(d,NativeFrameSet::Context,budget.descriptor_work).map_err(JoinError::Record)?;
        context_digests.push(d);contexts.insert(digest_hex(&d),frame.descriptor().clone());
    }
    let mut universe_digests=Vec::new();let mut seen=BTreeSet::new();
    for cell in array(field(&enumeration,"cells")?)? {
        step(&mut remaining)?;
        for binding in array(field(cell,"programBindings")?)? {
            step(&mut remaining)?;let value=field(binding,"universe")?;
            if value!=&V::Null {let d=bare(value)?;if seen.insert(d){universe_digests.push(d)}}
        }
    }
    // Selection precedes universe binding in this fixed composition. The census
    // is derived from Plan/enum refs, not supplied by the API caller. Complete
    // Run traversal must still account for other retained universe references.
    crate::inspect_plan_native(inputs,plan_id,&context_digests,&universe_digests,budget).map_err(JoinError::Plan)?;
    let mut universes=BTreeMap::new();let mut universe_domains=BTreeMap::new();let mut retained=BTreeMap::new();
    for d in universe_digests {
        step(&mut remaining)?;
        crate::inspect_native_retention(inputs,d,NativeFrameSet::SemanticUniverse,snapshot_id,budget).map_err(JoinError::Retention)?;
        let frame=inputs.frame_candidate(d,NativeFrameSet::SemanticUniverse,budget.descriptor_work).map_err(JoinError::Record)?;
        let V::Object(value)=frame.descriptor()else{return Err(JoinError::Law)};
        if value.contains_key("bindResult"){return Err(JoinError::Refused("ENUMERATION_ADMISSION_PRECONDITION".into()))}
        let mut nested=BTreeMap::new();
        let pair=match frame.domain(){
            "native.semantic-universe.typescript.v2"=>Some(("configGraph",crate::native_universe::nested_record(inputs,frame.descriptor(),frame.registry_row(),"configGraph",budget.descriptor_work)?)),
            "native.semantic-universe.rust.v2"=>Some(("sourceUnitOwnership",crate::native_universe::nested_frame(inputs,frame.descriptor(),frame.registry_row(),"sourceUnitOwnership","native.source-unit-ownership.v1",budget.descriptor_work)?)),
            "native.semantic-universe.syntax.v2"=>None,
            _=>return Err(JoinError::Law),
        };
        if let Some((key,Some(value)))=pair{nested.insert(String::from(key),value);}
        let key=digest_hex(&d);universe_domains.insert(key.clone(),String::from(frame.domain()));
        retained.insert(key.clone(),V::Object(nested));universes.insert(key,frame.descriptor().clone());
    }
    let mut closures=BTreeMap::new();
    for reference in array(field(&plan,"semanticClosures")?)? {
        step(&mut remaining)?;let id=text(reference)?;
        closures.insert(String::from(id),object(inputs,id,D::Closure,budget.descriptor_work)?);
    }
    let mut inventories=Vec::new();
    for digest in inventory_refs {step(&mut remaining)?;inventories.push(record(inputs,*digest)?);}
    Ok(JoinInputs{plan,analysis,scope,enumeration,membership,snapshot_inventory,snapshot_paths,
        snapshot_index,source_blobs,contexts,universes,universe_domains,retained,closures,inventories})
}
