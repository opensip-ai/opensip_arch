from pathlib import Path
import json,hashlib,shutil,difflib
B=Path('/tmp/opensip-design-corrections');R=Path('/Users/sb/code/opensip-ai/opensip_arch');T=B/'claude-return-successor.v1';O=B/'root-independent27-advisory-corrections.v1';assert not O.exists();O.mkdir();rel='docs/coop/design-corrections/foundation/check-enumeration.v1.py';p=T/rel;s=p.read_text();(O/'check-enumeration.before.py').write_text(s)
needle='    rec("missing-expected-inventory", admit(ep, [inv("file", "complete", files, file_ext)], memb, sc, universes, retained, source))\n'
addition='''    # Internal root representation is admitted before path slicing / program binding.
    # Keep a valid enumeration baseline, change only the host membership root spelling,
    # and rebind its digest so a digest mismatch cannot mask the root-specific refusal.
    # This exercises the enumeration boundary, not structural custody or a whole Run.
    unit_root_cases = []
    for label, root, members, expected, diagnostic in [
        ("project-empty", "", [], "ADMIT", None),
        ("project-dot", ".", [], "REFUSE", "units[0].rootPath:#/$defs/InternalUnitRootV1"),
        ("project-dot-slash", "./", [], "REFUSE", "units[0].rootPath:#/$defs/InternalUnitRootV1"),
        ("member-dot", "", ["."], "REFUSE", "units[0].memberPackageRoots[0]:#/$defs/CanonicalRelativeDirV1"),
        ("member-empty", "", [""], "REFUSE", "units[0].memberPackageRoots[0]:#/$defs/CanonicalRelativeDirV1"),
    ]:
        changed_membership = copy.deepcopy(memb)
        changed_membership["units"][0].update(rootPath=root, memberPackageRoots=members)
        changed_plan = copy.deepcopy(ep)
        changed_plan["membershipDigest"] = M.raw_digest(changed_membership)
        native_refusal = None
        try:
            M.NV.admit_unit_roots(changed_membership["units"])
            native_result = "ADMIT"
        except M.NV.AdmissionError as exc:
            native_result = "REFUSE"
            native_refusal = str(exc)
        result = admit(changed_plan, [
            inv("file", "complete", copy.deepcopy(files), file_ext),
            inv("package", "complete", copy.deepcopy(pkgs), pkg_ext),
        ], changed_membership, sc, universes, retained, source)
        exact_faults = [] if expected == "ADMIT" else ["ENUMERATION_MEMBERSHIP_UNIT_ROOT"]
        passed = (native_result == expected and result["result"] == expected
                  and result["refusals"] == exact_faults
                  and (native_refusal is None if diagnostic is None else
                       native_refusal == "NATIVE_UNIT_ROOT_REPRESENTATION:" + diagnostic))
        unit_root_cases.append({"case": label, "expected": expected,
                               "nativeResult": native_result, "nativeRefusal": native_refusal,
                               "enumerationResult": result["result"], "refusals": result["refusals"],
                               "passed": passed})

'''
assert s.count(needle)==1;s=s.replace(needle,addition+needle);needle='    historical = [c["case"] for c in cases if c["case"] in HISTORICAL_BOUNDED]\n';assert s.count(needle)==1;s=s.replace(needle,'    mismatches.extend({"case": "internal-root-" + row["case"], "observed": row}\n                      for row in unit_root_cases if not row["passed"])\n'+needle);needle='        "cases": cases, "expected": want, "mismatches": mismatches,\n';assert s.count(needle)==1;s=s.replace(needle,'        "internalUnitRootControls": unit_root_cases,\n'+needle);p.write_text(s);(O/'check-enumeration.after.py').write_text(s);(O/'check-enumeration.diff').write_text(''.join(difflib.unified_diff((O/'check-enumeration.before.py').read_text().splitlines(True),s.splitlines(True),fromfile=rel,tofile=rel)))
rows=[]
for rel in ['docs/coop/artifacts/evaluation-proof.v13.json','docs/coop/artifacts/ep13.review-independent.json']:
 src=R/rel;dst=T/rel;assert src.is_file() and not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);rows.append({'path':rel,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size,'standing':'Exact existing live historical artifact copied into successor snapshot inputs; not repaired/regraded/authenticated as original measurement.'})
(O/'assessment.json').write_text(json.dumps({'standing':'Actual independent27 advisories addressed prospectively. New freeze and actual successor review required.','A-4':'Five discriminating native and enumeration-boundary controls: valid empty internal root plus four wrong project/member spellings, exact fault and early-refusal attribution. Digest is rebound so the root guard is actually reached. These are join controls, not whole-Run structural/semantic checks.','A-5':rows,'A-6':'Will explicitly document separate query/property commands in the final author package; existing final30 rebuild already executed all four probe commands successfully.','changedSourceFiles':[str(p.relative_to(T))]+[r['path'] for r in rows]},indent=2)+'\n');print('One checker extended; two historical inputs copied unchanged.')
