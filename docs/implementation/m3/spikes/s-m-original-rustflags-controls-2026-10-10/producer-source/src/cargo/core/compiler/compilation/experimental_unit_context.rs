//! Unadmitted experiment DATA only; no commands are executed here.
use super::*;
use crate::core::compiler::BuildContext;

pub(crate) fn capture(bcx: &BuildContext<'_, '_>, root: &Path) -> CargoResult<()> {
    let mut compilation = Compilation::new(bcx)?;
    // Explicit prototype metadata search output, not a real Cargo layout claim.
    compilation
        .deps_output
        .insert(CompileKind::Host, root.join("prototype-host-deps"));
    let mut units: Vec<_> = bcx.unit_graph.iter().collect();
    units.sort_unstable(); // Exactly the same ordering as the pinned unit graph serializer.
    let mut rows = Vec::new();
    for (index, (unit, _)) in units.iter().enumerate() {
        // Primary-package handling and real output layout remain separate duties.
        let mut command = compilation.rustc_process(unit, false, bcx.ws.is_member(&unit.pkg))?;
        super::super::add_cap_lints(bcx, unit, &mut command);
        let arguments = command
            .get_args()
            .map(|s| {
                s.to_str()
                    .map(str::to_owned)
                    .ok_or_else(|| anyhow::anyhow!("non UTF8 argument DATA"))
            })
            .collect::<CargoResult<Vec<_>>>()?;
        let mut env = std::collections::BTreeMap::new();
        let mut removed = Vec::new();
        for (name, value) in command.get_envs() {
            match value {
                Some(value) => {
                    env.insert(
                        name.clone(),
                        value
                            .to_str()
                            .ok_or_else(|| anyhow::anyhow!("non UTF8 environment DATA"))?
                            .to_owned(),
                    );
                }
                None => removed.push(name.clone()),
            }
        }
        rows.push(serde_json::json!({"index":index,"packageId":unit.pkg.package_id().to_spec(),"target":unit.target,"profile":unit.profile,"platform":unit.kind,"mode":unit.mode,"features":unit.features,"cargoUnitRustflags":unit.rustflags.as_ref(),"cwd":command.get_cwd(),"constructedEnvironment":env,"removedEnvironmentKeys":removed,"capLintArguments":arguments,"localPackageByActualCargo":unit.is_local(),"showWarningsByActualCargo":unit.show_warnings(bcx.gctx),"primaryPackageMaterialized":false,"realCargoOutputLayoutMaterialized":false,"completeCompilerCommand":false}));
    }
    std::fs::write(
        root.join("unit-context-data.json"),
        serde_json::to_vec_pretty(
            &serde_json::json!({"version":1,"standing":"EXPERIMENTAL ACTUAL CARGO PACKAGE ENV/CWD/CAP-LINT DATA; NOT COMPLETE COMMAND OR NATIVE PROFILE","units":rows,"nativeAdmission":false,"BuildRunnerUsed":false,"fixtureOrCorpusCodeExecuted":false,"completeCompilerCommand":false,"fullCargoProfileEnvironment":false}),
        )?,
    )?;
    Ok(())
}
