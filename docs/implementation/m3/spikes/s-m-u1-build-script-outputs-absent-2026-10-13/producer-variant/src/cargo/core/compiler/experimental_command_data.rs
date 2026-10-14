//! Static Cargo command DATA only. No unit is compiled or executed.
//! VARIANT (U-1, build-script outputs absent): unavailability does not spread through build-script units
//! (custom-build targets and run-custom-build units); every other block is unchanged. For a unit constructed
//! only because of this, Cargo's own prepare_rustc command is kept and OUT_DIR / *_OUT_DIR are removed, so the
//! build-script expansion is disclosed as unavailable. No build script runs.
use super::*;
pub(crate) fn capture(bcx: &BuildContext<'_, '_>, root: &Path) -> CargoResult<()> {
    let mut runner = BuildRunner::new(bcx)?;
    runner.lto = lto::generate(bcx)?;
    runner.prepare_units()?;
    runner.prepare()?;
    let mut units: Vec<_> = bcx.unit_graph.iter().collect();
    units.sort_unstable();
    let mut unavailable: HashSet<&Unit> = HashSet::new();
    for (unit, _) in &units {
        let t = serde_json::to_value(&unit.target)?;
        let supported = (t["kind"] == serde_json::json!(["lib"])
            && (t["crate_types"] == serde_json::json!(["lib"])
                || t["crate_types"] == serde_json::json!(["rlib"])))
            || (t["kind"] == serde_json::json!(["bin"])
                && t["crate_types"] == serde_json::json!(["bin"]));
        if !supported || !unit.mode.is_check() {
            unavailable.insert(*unit);
        }
    }
    let build_script = |u: &Unit| u.mode.is_run_custom_build() || u.target.is_custom_build();
    let seed = unavailable.clone();
    let mut parent_rule = seed.clone();
    loop {
        let mut changed = false;
        for (unit, deps) in &units {
            if deps.iter().any(|dep| parent_rule.contains(&dep.unit)) {
                changed |= parent_rule.insert(*unit);
            }
        }
        if !changed {
            break;
        }
    }
    loop {
        let mut changed = false;
        for (unit, deps) in &units {
            if deps
                .iter()
                .any(|dep| unavailable.contains(&dep.unit) && !build_script(&dep.unit))
            {
                changed |= unavailable.insert(*unit);
            }
        }
        if !changed {
            break;
        }
    }
    let mut rows = Vec::new();
    for (index, (unit, _)) in units.iter().enumerate() {
        let mut row = serde_json::json!({"index":index,"packageId":unit.pkg.package_id().to_spec(),"target":unit.target,"profile":unit.profile,"platform":unit.kind,"mode":unit.mode,"features":unit.features,"staticCargoCommandConstructed":false,"compilerLaunched":false,"completeRuntimeCommand":false});
        if unavailable.contains(unit) {
            row["standing"] = serde_json::json!("expansion-or-target-context-unavailable");
        } else {
            let mut command = super::prepare_rustc(&runner, unit)?;
            let outputs_absent = parent_rule.contains(unit);
            if outputs_absent {
                let keys: Vec<String> = command
                    .get_envs()
                    .iter()
                    .filter(|(k, v)| {
                        v.is_some() && (k.as_str() == "OUT_DIR" || k.ends_with("_OUT_DIR"))
                    })
                    .map(|(k, _)| k.clone())
                    .collect();
                for k in keys {
                    command.env_remove(&k);
                }
            }
            let args = command
                .get_args()
                .map(|s| {
                    s.to_str()
                        .map(str::to_owned)
                        .ok_or_else(|| anyhow::anyhow!("non UTF8 static command DATA"))
                })
                .collect::<CargoResult<Vec<_>>>()?;
            let mut env = std::collections::BTreeMap::new();
            let mut removed = Vec::new();
            for (name, value) in command.get_envs() {
                match value {
                    Some(v) => {
                        env.insert(
                            name.clone(),
                            v.to_str()
                                .ok_or_else(|| anyhow::anyhow!("non UTF8 static environment DATA"))?
                                .to_owned(),
                        );
                    }
                    None => removed.push(name.clone()),
                }
            }
            row["standing"] = serde_json::json!(if outputs_absent {
                "actual-static-cargo-command-data-build-script-outputs-absent"
            } else {
                "actual-static-cargo-command-data"
            });
            row["buildScriptOutputsAbsent"] = serde_json::json!(outputs_absent);
            row["staticCargoCommandConstructed"] = serde_json::json!(true);
            row["arguments"] = serde_json::json!(args);
            row["constructedEnvironment"] = serde_json::json!(env);
            row["removedEnvironmentKeys"] = serde_json::json!(removed);
            row["cwd"] = serde_json::json!(command.get_cwd());
            row["primaryPackageByActualCargo"] = serde_json::json!(runner.is_primary_package(unit));
        }
        rows.push(row);
    }
    std::fs::write(
        root.join("unit-command-data.json"),
        serde_json::to_vec_pretty(
            &serde_json::json!({"version":1,"standing":"EXPERIMENTAL ACTUAL STATIC CARGO COMMAND DATA; NO UNIT EXECUTION OR NATIVE ADMISSION","units":rows,"BuildRunnerConstructedForStaticData":true,"BuildRunnerCompileOrDryRunCalled":false,"fixtureOrCorpusCodeExecuted":false,"completeRuntimeCommand":false,"fullCargoProfileEnvironment":false,"nativeAdmission":false}),
        )?,
    )?;
    Ok(())
}
