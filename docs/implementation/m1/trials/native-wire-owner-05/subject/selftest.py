#!/usr/bin/env python3
"""Mutation controls for check.py (candidate 05). Each control copies exactly tools/filelist.py INPUTS into its own
tmp/selftest/<control>/ directory, seeds one defect, runs check.py there as a subprocess with that copy's own TMPDIR and
bytecode prefix, and requires that at least one of the control's EXPECTED checks fails (not merely any failure).
Includes the reviewer-01 mutants, the reviewer-02, reviewer-03 and reviewer-04 mutants adapted to candidate 05 structures, and
controls for every review-02, review-03 and review-04 finding and material advisory. Proves the reference check can fail; not approval.

Run: OPENSIP_ARCH=... TMPDIR=<subject>/tmp PYTHONDONTWRITEBYTECODE=1 \
       /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B selftest.py
"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import filelist as FL  # noqa: E402

PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
DEP = "native.dependency-source-not-wire-representable"
PREP = "native.prepared-output-exceeds-wire-limit"
REQ = "native.provider-request-exceeds-wire-limit"
PREP_PATH = "native.prepared-output-not-wire-representable"


def J(path):
    return json.loads(path.read_text())


def W(path, obj):
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def mem(d, rec, name):
    return next(m for m in d["records"][rec]["members"] if m["name"] == name)


def rule(d, rid):
    return next(r for r in d["admission"] if r["id"] == rid)


def dialect(d):
    return d["privateRepresentation"]["patternDialect"]


def on_file(name, fn):
    def apply(root):
        d = J(root / name)
        fn(d)
        W(root / name, d)
    return apply


def on_wire(fn):
    return on_file("wire-carriers.v1.json", fn)


def on_routes(fn):
    return on_file("public-route-successor.v1.json", fn)


def on_owner(fn):
    return on_file("owner-pattern-successor.v1.json", fn)


def first_ne_site(d):
    return next(x for x in d["pathSites"] if x["kind"] == "schema-string" and x["location"]["pointer"] == "#/$defs/ExpansionSiteV1/properties/path")


def on_text(name, old, new):
    def apply(root):
        s = (root / name).read_text()
        if old not in s:
            raise RuntimeError("control anchor missing: " + old[:60])
        (root / name).write_text(s.replace(old, new, 1))
    return apply


def both(*fns):
    def apply(root):
        for fn in fns:
            fn(root)
    return apply


def drop_remedy_phrase(routes, code, phrase):
    member = next(m for m in routes["addDomainDetailCodes"] if m["code"] == code)
    if phrase not in member["remedy"]:
        raise RuntimeError("control anchor missing: " + phrase)
    member["remedy"] = member["remedy"].replace(phrase, "")


def write_file(name, text):
    def apply(root):
        (root / name).write_text(text)
    return apply


CONTROLS = {
    # ---- reviewer-01 mutants, adapted
    "r_prepared_total_widened": (on_wire(lambda d: (mem(d, "Rust3PreparedOutputManifestV3", "entries")["type"].update(maxItems="2000256"),
                                                    mem(d, "Rust3PreparedOutputEntryV3", "outputOrdinal")["type"].update(max="2000255"))), ["limit-literals"]),
    "r_canonical_path_native_pattern": (on_wire(lambda d: d["scalars"]["Rust3CanonicalPath"]["type"].update(
        pattern="^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])", lexical=None) or d["scalars"]["Rust3CanonicalPath"]["type"].pop("lexical")),
        ["path-scalars-lexical-no-pattern", "wire-rust3-path-newline-dotdot"]),
    "r_exec_minlength1": (on_wire(lambda d: d["scalars"].__setitem__("Ts2ExecutionIdText", dict(d["scalars"]["Ts2ExecutionIdText"], type={"t": "text", "nfc": True, "minScalars": "1"}))), ["wire-ts2-execution-id-grammar"]),
    "r_anchor_4096": (on_wire(lambda d: (mem(d, "Rust3FactCandidateV1", "anchors")["type"].update(maxItems="4096"), rule(d, "ANCHOR-WIRE-SPAN")["params"].update(maxCount="4096"))), ["limit-literals"]),
    "r_ts_path_bytes": (on_wire(lambda d: (d["scalars"]["Ts2ProjectPath"]["type"].pop("maxScalars"), d["scalars"]["Ts2ProjectPath"]["type"].update(maxUtf8Bytes="4096"))), ["scalar-shapes-match-externs", "ts2-path-bound-matches-owner"]),
    "r_fault_phase_host_receipt": (on_wire(lambda d: rule(d, "RUST3-PROVIDER-FAULT")["params"].update(phaseSemantics="host-receipt")), ["vectors:RUST3-PROVIDER-FAULT", "provider-fault-semantics-declared"]),
    "r_cancel_in_start_allowed": (on_wire(lambda d: d["protocols"]["rust-semantic"]["transitions"]["cancel"].update(hostMaySendInStart=True)), ["cancel-in-start-consistent-with-p3", "vectors:P3-OVERLAY"]),
    "r_depsrc_order_path_first": (on_wire(lambda d: rule(d, "DEPSRC-CUSTODY")["params"].update(entryOrder=["path", "name", "version", "sourceId"])), ["vectors:DEPSRC-CUSTODY", "depsrc-order-derived-from-owner"]),
    "r_scope2_drop_closure": (on_wire(lambda d: rule(d, "PER-KEY-SCOPE2")["params"]["descriptorMembers"].remove("enumeratorClosure")), ["vectors:PER-KEY-SCOPE2", "scope2-descriptor-members-match-owner"]),
    "r_identitytext_no_bytes": (on_wire(lambda d: d["scalars"]["Rust3IdentityText"]["type"].pop("maxUtf8Bytes")), ["json-schema-maxlength-not-byte-bound"]),
    "r_package_key_min5": (on_wire(lambda d: d["scalars"]["Rust3PackageKey"]["type"].update(minScalars="5")), ["package-key-bounds-derived-from-owner", "wire-depsrc-chunk-empty-sourceid-key"]),
    "r_outputseen_not_reset": (on_wire(lambda d: d["protocols"]["rust-semantic"]["transitions"].update(stateUpdateAdditions=[{"onFrames": ["FactBatch", "CoverageV3"], "sets": {"outputSeen": True}}])), ["p3-overlay-updates-match-rust2"]),
    "r_prepared_count_directives_only": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"].update(countScope="build-script-directives-only")), ["vectors:PREPARED-V3-WIRE-LIMIT", "prepared-refusal-row-family"]),
    "r_commit_unavailable_stagecoverage": (on_wire(lambda d: next(r for r in d["commitmentMap"]["rows"] if r["field"] == "Startup1UnavailableV3.coverageCommitment").update(domain="opensip.rust-provider.stage-coverage.v2", valueClass="stage-entries")),
                                           ["commit-map-value-classes-match-owner", "vectors:COMMIT-MAP"]),
    # ---- reviewer-02 mutants (scratch/mutants.py), adapted to candidate-03 structures
    "r2_prep_detail": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"]["route"].update(routeKey="native.totally-unregistered-detail", successor="public-route-successor.v1.json#/addKeys/native.totally-unregistered-detail")),
                       ["route-rule-references", "vectors:PREPARED-V3-WIRE-LIMIT"]),
    "r2_depsrc_detail": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"]["route"].update(routeKey="native.totally-unregistered-detail", successor="public-route-successor.v1.json#/addKeys/native.totally-unregistered-detail")),
                         ["route-rule-references", "vectors:DEPSRC-SET-KEY-CONSTRAINTS"]),
    "r2_depsrc_class": (on_routes(lambda r: r["addKeys"][DEP]["route"].update({"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE"})), ["route-join:" + DEP]),
    "r2_prep_when": (on_routes(lambda r: r["selectors"][PREP].update(timing="after-spawn-at-worker-admission")), ["route-timing-anchored:" + PREP]),
    "r2_hello_first_off": (on_wire(lambda d: rule(d, "RUST3-PROVIDER-FAULT")["params"].update(readHelloFirst=False)), ["vectors:RUST3-PROVIDER-FAULT"]),
    "r2_space_allowed": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"].update(forbidInNameVersionAtOrBelow="31")), ["vectors:DEPSRC-SET-KEY-CONSTRAINTS", "package-key-bounds-derived-from-owner"]),
    "r2_keylen": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"].update(maxKeyScalars="4610")), ["vectors:DEPSRC-SET-KEY-CONSTRAINTS", "package-key-bounds-derived-from-owner"]),
    "r2_drop_chunk_path": (on_wire(lambda d: rule(d, "CANONICAL-PATH-ADMISSION")["params"]["members"].remove("Rust3DependencySourceChunkV3.path")), ["path-members-match-carrier-graph"]),
    "r2_lexical_text_drive": (on_wire(lambda d: d["privateRepresentation"]["lexicalRules"]["canonical-path-segments"].update(
        text=d["privateRepresentation"]["lexicalRules"]["canonical-path-segments"]["text"].split("; the first segment")[0])), ["lexical-rule-text-rendered"]),
    "r2_dialect_s": (on_wire(lambda d: dialect(d).update(flags="us")), ["ecma-review-probe-replayed", "pattern-dialect-structured"]),
    "r2_lowering_scalars_only": (on_wire(lambda d: dialect(d).update(loweringRequired=[x for x in dialect(d)["loweringRequired"] if "/scalars/" in x["location"]["pointer"]])), ["pattern-lowering-closed"]),
    "r2_depsrc_order": (on_wire(lambda d: rule(d, "DEPSRC-CUSTODY")["params"].update(entryOrder=["name", "version", "path", "sourceId"])), ["vectors:DEPSRC-CUSTODY", "depsrc-order-derived-from-owner"]),
    "r2_prep_ordinal": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"].update(maxOrdinal="256")), ["limit-literals"]),
    # ---- RF-1 public route join
    "rf1_domain_detail_present": (on_routes(lambda r: r["addKeys"][PREP]["route"].update(domainDetail="native.provider-input-exceeds-wire-limit")), ["route-join:" + PREP]),
    "rf1_envelope_detail_unregistered": (on_routes(lambda r: r["addKeys"][REQ]["route"].update(envelopeDetail="native.not-a-registered-detail")), ["route-join:" + REQ]),
    "rf1_error_code_changed": (on_routes(lambda r: r["addKeys"][REQ]["route"].update(errorCode="REQUEST.INVALID_ARGUMENT")), ["route-join:" + REQ]),
    "rf1_route_row_exit": (on_routes(lambda r: r["routeTableRows"][0].update(exitCode="4")), ["route-join-owner-family"]),
    "rf1_origin_widened": (on_routes(lambda r: r["addKeys"][DEP]["possibleOrigins"].append("external-configuration")), ["route-origin-closed"]),
    "rf1_owner_source_digest": (on_routes(lambda r: r["selectors"][DEP].update(ownerFunctionSourceSha256="0" * 64)), ["route-selectors-owner-source"]),
    "rf1_timing_anchor_moved": (on_routes(lambda r: r["selectors"][REQ]["timingAnchor"].update(line=2849)), ["route-timing-anchored:" + REQ]),
    "rf1_literal_refusal_restored": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"].update(refusal={"class": "request-rejected", "code": "REQUEST.PRECONDITION_FAILED"})), ["input-grammar", "route-rule-references"]),
    "rf1_remedy_reused": (on_routes(lambda r: r["addDomainDetailCodes"][0].update(code="native.release-declaration-invalid")), ["route-remedy-not-reused"]),
    # ---- RF-2 representability and accounting
    "rf2_nfc_sourceid_dropped": (on_wire(lambda d: rule(d, "DEPSRC-WIRE-REPRESENTABILITY")["params"]["nfcFields"].remove("sourceId")), ["vectors:DEPSRC-WIRE-REPRESENTABILITY", "depsrc-representability-fields-derived-from-owner"]),
    "rf2_path_max_4095": (on_wire(lambda d: rule(d, "DEPSRC-WIRE-REPRESENTABILITY")["params"].update(maxPathScalars="4095")), ["vectors:DEPSRC-WIRE-REPRESENTABILITY", "limit-literals"]),
    "rf2_depsrc_path_rule_logical": (on_wire(lambda d: rule(d, "DEPSRC-WIRE-REPRESENTABILITY")["params"].update(pathLexical="logical-path-segments")), ["vectors:DEPSRC-WIRE-REPRESENTABILITY"]),
    "rf2_prefix_included": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"].update(prefixIncluded=True)), ["request-accounting-law-matches-owner", "vectors:REQUEST-WIRE-ACCOUNTING"]),
    "rf2_inner_payload_scope": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"].update(lengthScope="inner-payload")), ["request-accounting-law-matches-owner", "vectors:REQUEST-WIRE-ACCOUNTING"]),
    "rf2_totals_dropped": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"].update(totalsApplyTo=[])), ["request-accounting-law-matches-owner", "vectors:REQUEST-WIRE-ACCOUNTING"]),
    "rf2_chunking_changed": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"].update(chunking="equal-split")), ["vectors:REQUEST-WIRE-ACCOUNTING"]),
    "rf2_reserve_cancel_off": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"].update(reserveCancel=False)), ["vectors:REQUEST-WIRE-ACCOUNTING"]),
    "rf2_chunk_offset_formula": (on_text("tools/representability.py", "hl(i) + hl(i * max_chunk) + hl(n)", "hl(i) + hl(i) + hl(n)"), ["request-accounting-closed-form-matches-owner-encoder"]),
    "rf2_boundary_vector_shifted": (on_file("admission-vectors.json", lambda v: next(x for x in v["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == "request-payload-bytes-exactly-at-limit")["input"]["plan"]["snapshot"][1].update(byteLength=next(x for x in v["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == "request-payload-bytes-exactly-at-limit")["input"]["plan"]["snapshot"][1]["byteLength"] + 1)),
                                    ["vectors:REQUEST-WIRE-ACCOUNTING"]),
    # ---- RF-3 dialect and pattern closure
    "rf3_site_removed": (on_wire(lambda d: dialect(d)["patternSites"].pop()), ["pattern-sites-closed"]),
    "rf3_site_negation_flipped": (on_wire(lambda d: next(x for x in dialect(d)["patternSites"] if x["negated"]).update(negated=False)), ["pattern-sites-closed"]),
    "rf3_translator_dollar": (on_text("tools/wirecodec.py", 'if c == "$":', 'if c == "$$":'), ["ecma-differential", "ecma-newline-counterexamples"]),
    "rf3_translator_dot": (on_text("tools/wirecodec.py", 'dot = "[\\\\s\\\\S]" if "s" in flags else "[^" + _cls(ECMA_LINE_TERMINATORS) + "]"', 'dot = "."'), ["ecma-owner-differential", "ecma-review03-probe-replayed"]),
    "rf3_node_pin": (on_text("tools/common.py", "1ee75375e33b94fc34b3b19aede049e11dae90efb63b374dc96d6bdace70c4b8", "0" * 64), ["ecma-engine-pinned", "pattern-dialect-structured"]),
    # ---- review-02 advisories
    "a2_subject_files_read": (both(write_file("subject-files.json", "{}\n"), on_text("tools/check_static.py", 'self.cov = rd("field-coverage.json")', 'self.cov = rd("field-coverage.json"); rd("subject-files.json")')),
                              ["closure-execution-inputs-listed"]),
    "a3_extern_members_dropped": (on_wire(lambda d: rule(d, "CANONICAL-PATH-ADMISSION")["params"].update(externMembers=[])), ["path-members-match-carrier-graph", "wire-depsrc-manifest-native-pattern-bypass-refused"]),
    "a3_lexical_structure_drive_dropped": (on_wire(lambda d: d["privateRepresentation"]["lexicalRules"]["canonical-path-segments"].pop("firstSegmentForbiddenPattern")),
                                           ["vectors:CANONICAL-PATH-ADMISSION", "lexical-rules-derived-from-owner"]),
    "a4_del_forbidden": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"].update(forbidInNameVersionAtOrBelow="127")), ["vectors:DEPSRC-SET-KEY-CONSTRAINTS", "package-key-bounds-derived-from-owner"]),
    "a5_d9_equivalence": (on_wire(lambda d: rule(d, "RUST3-PROVIDER-FAULT")["params"]["d9Equivalence"].update(refusedPayloadTerminalKind="cancelled")), ["provider-fault-refusal-same-d9"]),
    "a6_wrapper_bypasses_owner": (on_text("tools/representability.py", "out = NE.prepared_output_set_admit(prepared, context, explicit_prepared_mode)", "out = {\"outcome\": \"admitted\"}"),
                                  ["route-selectors-owner-source", "vectors:PREPARED-V3-WIRE-LIMIT"]),
    "a7_g19_remapped": (on_file("field-coverage.json", lambda c: c["recordLevelGaps"].update({"R3-G19": "falseGaps[R3-G18]"})), ["gap-r3-g19-is-citation-defect"]),
    # ---- candidate-02 controls retained
    "rf4_fault_nulls_independent": (on_wire(lambda d: rule(d, "RUST3-PROVIDER-FAULT")["params"].update(jointConsistency=False)), ["vectors:RUST3-PROVIDER-FAULT", "provider-fault-semantics-declared"]),
    "rf5_dependency_path_native_only": (on_wire(lambda d: rule(d, "CANONICAL-PATH-ADMISSION")["params"].update(lexical="logical-path-segments")), ["vectors:CANONICAL-PATH-ADMISSION"]),
    "rf5_lowering_text_weakened": (on_wire(lambda d: dialect(d).update(lowering="patterns are used as-is")), ["pattern-dialect-structured"]),
    "adv6_linktarget_bound_restored": (on_wire(lambda d: d["records"]["Ts2SnapshotEntryV1"]["variants"]["symlink"]["linkTarget"].update(maxScalars="4096")), ["path-members-bound-to-lexical-rules", "ts2-manifest-digest-raw"]),
    "adv7_anchor_order_swapped": (on_wire(lambda d: rule(d, "ANCHOR-WIRE-SPAN")["params"].update(order={"typescript-semantic": "cve1-bytes-strict", "rust-semantic": "cbor-bytes-strict"})), ["anchor-order-tokens-follow-language-owner", "vectors:ANCHOR-WIRE-SPAN"]),
    "adv3_gap_detached": (on_file("field-coverage.json", lambda c: c["recordLevelGaps"].pop("R3-G19")), ["field-coverage-gaps-resolved"]),
    "adv2_vector_removed": (on_file("admission-vectors.json", lambda v: v["vectors"].pop("PACKAGE-KEY-JOIN")), ["vectors-cover-every-rule"]),
    "c2_architecture_pin_dropped": (on_text("tools/common.py", '    "capabilityMatrix": ("docs/coop/design-corrections/native/native-capability-matrix.v2.json", "4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14", 36595),\n', ""),
                                    ["closure-architecture-reads-pinned"]),
    "c2_architecture_pin_tampered": (on_text("tools/common.py", "7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be", "0" * 64), ["architecture-pins-verified-before-import"]),
    "c2_registry_pin_dropped": (on_text("tools/common.py", '    "publicDetailRegistry": ("docs/coop/design-corrections/public-detail-registry.v1.json", "2702e6ca97b6d8095cbcef0b0a219048b1ffdc434e0d8bb8c4bff247cda70e68", 59547),\n', ""),
                                ["step:routes"]),
    "c2_frozen_input_changed": (on_file("inputs/rust3-fields.json", lambda r: r["gaps"].pop("R3-G19")), ["subject-inputs-pinned:rustFields"]),
    "c2_reference_env_version": (on_file("reference-environment.json", lambda e: e["packages"].update(jsonschema="0.0.0")), ["reference-environment-matches"]),
    # ---- reviewer-03 mutants (scratch/mutants.py), adapted to candidate-04 structures
    "r3_swap_envelope_details": (on_routes(lambda r: (r["addKeys"][DEP]["route"].update(envelopeDetail="native.provider-input-exceeds-wire-limit"), r["addKeys"][REQ]["route"].update(envelopeDetail="native.provider-input-not-representable"))), ["route-remedy-keying"]),
    "r3_wrong_remedy_text": (on_routes(lambda r: r["addDomainDetailCodes"][1].update(remedy="the provider emitted a defect; report it")), ["route-remedy-keying"]),
    "r3_dep_timing_plan_time": (on_routes(lambda r: r["selectors"][DEP].update(timing="plan-time-no-spawn", timingAnchor={"pin": "nativeMd", "line": 2848, "needle": "1. **Plan time (no spawn).**"})), ["route-timing-anchored:" + DEP]),
    "r3_origin_meaning_host_invariant": (on_routes(lambda r: r["newOrigin"].update(actor="host-generated-internal-layer", meaning="a host invariant fault")), ["route-origin-closed"]),
    "r3_prepared_refuse_only_explicit": (on_text("tools/representability.py", "    faults = prepared_limit_faults(doc, prepared)\n", "    faults = prepared_limit_faults(doc, prepared) if explicit_prepared_mode else []\n"),
                                         ["vectors:PREPARED-V3-WIRE-LIMIT", "route-prepared-modes"]),
    "r3_seal_zero_length_counts_chunk": (on_text("tools/representability.py", "    chunks = sum(-(-entry_len(e) // max_chunk) for e in entries)", "    chunks = sum(max(1, -(-entry_len(e) // max_chunk)) for e in entries)"), ["vectors:REQUEST-WIRE-ACCOUNTING", "vectors:HOST-SEND-SCHEDULE"]),
    "r3_depsrc_newline_skip": (on_text("tools/representability.py", '            if not owner_schema_ok(NE, rep["ownerPathSchema"], path):', '            if "\\n" not in path and not owner_schema_ok(NE, rep["ownerPathSchema"], path):'), ["vectors:DEPSRC-WIRE-REPRESENTABILITY", "owner-successor-no-untyped-exception"]),
    "r3_ts2_frame_limit_2x": (on_text("tools/representability.py", 'acc = Accountant(doc, ts2_envelope, int(limits["maxFramePayloadBytes"]), total_limit, frames_limit)', 'acc = Accountant(doc, ts2_envelope, int(limits["maxFramePayloadBytes"]) * 2, total_limit, frames_limit)'), ["vectors:REQUEST-WIRE-ACCOUNTING"]),
    # ---- review-03 RF-1 path sites
    "rf1_path_site_removed": (on_wire(lambda d: d["pathSites"].pop()), ["path-sites-closed"]),
    "rf1_binding_rule_wrong": (on_wire(lambda d: first_ne_site(d)["bindings"][0].update(rule="canonical-path-segments")), ["path-site-bindings-executed"]),
    "rf1_owner_row_reverted": (on_owner(lambda o: next(r for r in o["schemaPatternRows"] if "crateRootPaths" in r["pointer"]).update(to=next(r for r in o["schemaPatternRows"] if "crateRootPaths" in r["pointer"])["from"])),
                               ["owner-successor-rows-closed", "vectors:PATH-SITE-SEGMENT-LAW"]),
    "rf1_owner_row_dropped": (on_owner(lambda o: o["schemaPatternRows"].remove(next(r for r in o["schemaPatternRows"] if "GeneratedFileV1" in r["pointer"]))), ["owner-successor-rows-closed", "vectors:PATH-SITE-SEGMENT-LAW"]),
    # ---- review-03 RF-2 selected owner
    "rf2_evaluator_python": (on_text("tools/owner_successor.py", "            if isinstance(schema, dict) and schema.get(NODE_MARK) is True:", "            if False:"), ["owner-successor-evaluates-ecma", "vectors:OWNER-PATTERN-EVALUATION"]),
    "rf2_logical_re_kept": (on_text("tools/owner_successor.py", '            setattr(mod, r["name"], re.compile(W.ecma_to_python(r["ecmaPattern"], flags)))', "            pass"), ["vectors:OWNER-PATTERN-EVALUATION", "vectors:PREPARED-V3-PATH-REPRESENTABILITY"]),
    "rf2_phase_a_removed": (on_text("tools/representability.py", '    if phase_a:\n        return {"admitted": False', '    if False:\n        return {"admitted": False'), ["vectors:DEPSRC-WIRE-REPRESENTABILITY", "owner-successor-no-untyped-exception"]),
    "rf2_regex_inventory_row_dropped": (on_owner(lambda o: o["modelRegexInventory"].pop()), ["owner-successor-regex-inventory-closed"]),
    "rf2_selector_source_digest": (on_owner(lambda o: o["selectorSources"]["nativeModel"].update(validate_native="0" * 64)), ["owner-successor-selector-sources"]),
    # ---- review-03 RF-3 prepared modes and route semantics
    "rf3_defaulted_refuse": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"]["modes"].update(defaulted="refuse")), ["prepared-modes-follow-owner-po1", "vectors:PREPARED-V3-WIRE-LIMIT"]),
    "rf3_route_row_mode_text": (on_routes(lambda r: next(x for x in r["routeTableRows"] if x["routeKey"] == PREP).update(condition="explicitly selected prepared output set over the limits")), ["route-prepared-modes"]),
    "rf3_selector_modes_diverge": (on_routes(lambda r: r["selectors"][PREP]["modes"].update(defaulted="refuse")), ["route-prepared-modes"]),
    "rf3_bound_code_precondition": (on_routes(lambda r: r["addKeys"][REQ]["route"].update(errorCode="REQUEST.PRECONDITION_FAILED")), ["route-join:" + REQ]),
    "rf3_prep_path_class_bound": (on_routes(lambda r: r["addKeys"][PREP_PATH].update(conditionClass="bound")), ["route-join:" + PREP_PATH]),
    # ---- review-03 RF-4 send schedule
    "rf4_sender_accepts_alternate_chunking": (on_text("tools/sender_ref.py", '                    raise _div("chunk-schedule", "slot %d" % slot)', "                    pass"), ["vectors:HOST-SEND-SCHEDULE", "schedule-not-byte-minimal"]),
    "rf4_second_cancel_allowed": (on_text("tools/sender_ref.py", '            raise _div("frame-after-cancel", f["frameType"])', "            pass"), ["vectors:HOST-SEND-SCHEDULE"]),
    "rf4_byte_minimal_claim": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING").update(rule=rule(d, "REQUEST-WIRE-ACCOUNTING")["rule"].replace("not byte-minimal", "byte-minimal"))), ["request-schedule-claims"]),
    "rf4_byte_minimal_param": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"].update(byteMinimal=True)), ["request-schedule-claims"]),
    "rf4_realize_not_canonical": (on_text("tools/sender_ref.py", "                n = min(max_chunk, length - offset)", "                n = min(max(1, max_chunk // 2), length - offset)"), ["schedule-realization-agrees", "vectors:HOST-SEND-SCHEDULE"]),
    # ---- review-03 advisories
    "a3_plan_id_fate_removed": (on_routes(lambda r: r["selectors"][REQ].pop("planIdFate")), ["route-timing-anchored:" + REQ]),
    "a7_cancel_law_text": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING").update(rule=rule(d, "REQUEST-WIRE-ACCOUNTING")["rule"].replace("P3-29", "P3-99"))), ["request-schedule-claims"]),
    "a9_callee_digest": (on_routes(lambda r: r["selectors"][DEP]["calleeClosureSha256"].update(parse_cargo_lock="0" * 64)), ["route-selectors-owner-source"]),
    # ---- reviewer-04 mutants (scratch/mutants.py), adapted to candidate-05 structures
    "r4_patch_native_only_not_other_scopes": (on_owner(lambda o: o.update(scope=[x for x in o["scope"] if x["id"] == "native-evidence-model"])),
                                              ["owner-successor-scope-declared", "owner-successor-scope-installed", "vectors:RELATION-PAYLOAD-PATH-LAW"]),
    "r4_sender_no_payload_bytes_check": (on_text("tools/sender_ref.py", '                raise _div("payload-bytes", "slot %d: %d!=%d" % (slot, n, s["payloadBytes"]))', "                pass"), ["vectors:HOST-SEND-SCHEDULE"]),
    "r4_sender_no_request_limit_recheck": (on_text("tools/sender_ref.py", '            raise _div("request-limit", "%d bytes %d frames" % (total, frames))', "            pass"), ["vectors:HOST-SEND-SCHEDULE"]),
    "r4_remedy_drop_generated_phrase": (on_routes(lambda r: drop_remedy_phrase(r, "native.provider-input-not-representable", " or generated-file logical path")), ["route-remedy-keying"]),
    # ---- review-04 RF-1 prepared bound over every non-rejected outcome; planner entry bounds
    "rf1_fallback_outcome_limit_skipped": (on_text("tools/representability.py", '    if out["outcome"] not in ("admitted", "fallback-non-prepared"):', '    if out["outcome"] != "admitted":'),
                                           ["vectors:PREPARED-V3-WIRE-LIMIT", "route-prepared-modes"]),
    "rf1_only_fresh_rows_counted": (on_text("tools/representability.py", "    faults = prepared_limit_faults(doc, prepared)\n",
                                            '    faults = prepared_limit_faults(doc, dict(prepared, rows=[r for r in prepared["rows"] if r["inputBinding"]["toolchainDigest"] == context["toolchainDigest"]]))\n'),
                                    ["vectors:PREPARED-V3-WIRE-LIMIT", "route-prepared-modes"]),
    "rf1_entry_bound_removed": (on_text("tools/representability.py", '    acc.entry_bound(manifest_type, len(manifest["entries"]), limits)\n', ""), ["vectors:REQUEST-WIRE-ACCOUNTING"]),
    "rf1_entry_bounds_param_dropped": (on_wire(lambda d: rule(d, "REQUEST-WIRE-ACCOUNTING")["params"]["entryBounds"].pop("PreparedOutputManifest")), ["vectors:REQUEST-WIRE-ACCOUNTING", "request-schedule-claims"]),
    "rf1_limit_text_admitted_only": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT").update(rule=rule(d, "PREPARED-V3-WIRE-LIMIT")["rule"].replace("EVERY non-rejected owner outcome", "the admitted owner outcome"))), ["prepared-precedence-and-scope-stated"]),
    # ---- review-04 RF-2 closed evaluator scope, both directions
    "rf2_scope_widened_global_ecma": (on_text("tools/owner_successor.py", "            if isinstance(schema, dict) and schema.get(NODE_MARK) is True:", "            if True:"),
                                      ["owner-successor-no-change:identitySchemas3", "owner-successor-no-change:c2v3", "owner-successor-no-change:rust2"]),
    "rf2_scope_widened_identity_documents_marked": (on_text("tools/owner_successor.py", "            mark_patterns(doc)\n            mod._LOCAL_REGISTRY = ", "            mark_patterns(doc)\n            [mark_patterns(d) for d in by_path.values()]\n            mod._LOCAL_REGISTRY = "),
                                                    ["owner-successor-scope-installed", "owner-successor-no-change:identitySchemas3", "owner-successor-no-change:identitySchemas2"]),
    "rf2_scope_narrowed_startup": (on_owner(lambda o: o.update(scope=[x for x in o["scope"] if x["id"] != "provider-startup-model"])), ["owner-successor-scope-installed", "vectors:OWNER-PATTERN-EVALUATION"]),
    "rf2_scope_narrowed_wire": (on_owner(lambda o: o.update(scope=[x for x in o["scope"] if x["id"] != "provider-wire-model"])), ["owner-successor-scope-installed", "vectors:PATH-SITE-SEGMENT-LAW"]),
    "rf2_no_change_document_dropped": (on_owner(lambda o: o["noChangeDocuments"].pop()), ["owner-successor-scope-declared", "owner-successor-no-change-set-closed"]),
    # ---- review-04 RF-3 relation-payload CanonicalPath
    "rf3_relation_row_dropped": (on_owner(lambda o: o.update(schemaPatternRows=[x for x in o["schemaPatternRows"] if x["document"] != "opensip.product.relation-payload.2"])),
                                 ["owner-successor-rows-closed", "vectors:RELATION-PAYLOAD-PATH-LAW"]),
    "rf3_relation_site_dropped": (on_owner(lambda o: o["relationPayloadPathSites"].pop()), ["relation-payload-sites-closed"]),
    "rf3_relation_previous_path_vectors_dropped": (on_file("admission-vectors.json", lambda v: v["vectors"].__setitem__("RELATION-PAYLOAD-PATH-LAW", [x for x in v["vectors"]["RELATION-PAYLOAD-PATH-LAW"] if x["input"]["relation"]["property"] != "previousPath"])),
                                                   ["relation-payload-sites-covered-and-pinned-divergence"]),
    # ---- review-04 RF-4 Cancel law
    "rf4_cancel_before_hello_allowed": (on_text("tools/sender_ref.py", '    if slots_consumed <= echo["helloSlot"]:\n        return None', "    if False:\n        return None"), ["vectors:HOST-SEND-SCHEDULE", "sender-cancel-echo-matches-cancel-nullability"]),
    "rf4_cancel_echo_unchecked": (on_text("tools/sender_ref.py", '            if f["payload"] != want:', "            if False:"), ["vectors:HOST-SEND-SCHEDULE", "sender-cancel-echo-matches-cancel-nullability"]),
    "rf4_cancel_ordinal_echoed_before_analyze": (on_text("tools/sender_ref.py", '"analysisOrdinal": echo["analysisOrdinal"] if slots_consumed > echo["analyzeSlot"] else None,', '"analysisOrdinal": echo["analysisOrdinal"],'),
                                                 ["vectors:HOST-SEND-SCHEDULE", "sender-cancel-echo-matches-cancel-nullability"]),
    "rf4_cancel_law_text_any_point": (on_wire(lambda d: rule(d, "HOST-SEND-SCHEDULE").update(rule=rule(d, "HOST-SEND-SCHEDULE")["rule"].replace("never before the Hello slot", "at any point"))), ["request-schedule-claims"]),
    # ---- review-04 advisories
    "a2_sender_no_frame_limit_recheck": (on_text("tools/sender_ref.py", '            raise _div("frame-limit", str(n))', "            pass"), ["vectors:HOST-SEND-SCHEDULE"]),
    "a3_precedence_text_dropped": (on_wire(lambda d: rule(d, "PREPARED-V3-PATH-REPRESENTABILITY").update(rule=rule(d, "PREPARED-V3-PATH-REPRESENTABILITY")["rule"].replace("outranks the owner non-inert and stale refusals", "follows the owner refusals"))),
                                   ["prepared-precedence-and-scope-stated"]),
    "a4_duty_dropped": (on_file("successor.json", lambda x: x.update(futureQualification=[f for f in x["futureQualification"] if "relation-payload" not in f])), ["integration-duties-declared"]),
    # ---- carried over from candidate 01
    "c_member_rename": (on_wire(lambda d: mem(d, "Rust3PreparedOutputEntryV3", "planRow").update(name="setRow")), ["carrier-member-lists"]),
    "c_bare_name": (on_wire(lambda d: d["records"].__setitem__("CoverageKeyV2", d["records"].pop("Rust3CoverageKeyV2"))), ["namespaced-type-names"]),
    "c_frame_terminal": (on_wire(lambda d: next(f for f in d["protocols"]["rust-semantic"]["frames"] if f["frameType"] == "Cancel").update(workerTerminal=True)), ["rust3-frame-directions-terminals"]),
    "c_bytes_as_text": (on_wire(lambda d: mem(d, "Rust3SnapshotFileChunkV2", "bytes").update(type={"t": "text", "nfc": True})), ["wire-bytes-as-json-array", "wire-bytes-empty"]),
    "c_fact_ref_dropped": (on_wire(lambda d: d["records"]["Ts2AnchorRefV1"]["variants"].pop("fact-ref")), ["input-grammar"]),
    "c_selector": (on_wire(lambda d: next(f for f in d["protocols"]["rust-semantic"]["frames"] if f["frameType"] == "Unavailable")["payload"].update(alternatives={
        "READY_ANALYZE": {"t": "extern", "schemaRef": "opensip.product.provider-startup.1#/$defs/UnavailableV3", "generatedType": "Startup1UnavailableV3"},
        "WAIT_NATIVE_CONTEXT_VERIFIED": {"t": "extern", "schemaRef": "opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1", "generatedType": "Startup1PreAnalyzeUnavailableV1"}})),
        ["unavailable-selector-phases"]),
    "c_nullable_to_optional": (on_wire(lambda d: mem(d, "Ts2CancelV1", "executionId").update(presence="optional")), ["wire-ts2-cancel-null-omitted-refused"]),
    "c_successor_check": (on_file("successor.json", lambda s: s["rows"][0]["referenceChecks"].append("nonexistent-check")), ["successor-check-exists:nonexistent-check"]),
}


def run_control(name):
    apply, expected = CONTROLS[name]
    root = HERE / "tmp" / "selftest" / name
    shutil.rmtree(root, ignore_errors=True)
    for f in FL.INPUTS:
        dst = root / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / f, dst)
    try:
        apply(root)
    except Exception as exc:  # noqa: BLE001
        return {"control": name, "caught": False, "error": "apply failed: " + repr(exc)}
    (root / "tmp").mkdir(exist_ok=True)
    env = dict(os.environ, TMPDIR=str(root / "tmp"), PYTHONDONTWRITEBYTECODE="1", PYTHONPYCACHEPREFIX=str(root / "tmp" / "pycache"))
    proc = subprocess.run([PY, "-I", "-B", "check.py", "--out", str(root / "tmp" / "result.json")], cwd=root, env=env,
                          capture_output=True, text=True, timeout=3000)
    try:
        failed = [f["id"] for f in J(root / "tmp" / "result.json")["failures"]]
    except Exception:  # noqa: BLE001
        failed = ["no-result:" + proc.stdout[-300:] + proc.stderr[-300:]]
    hit = [e for e in expected if e in failed]
    shutil.rmtree(root, ignore_errors=True)
    return {"control": name, "expected": expected, "caught": bool(hit), "expectedFailed": hit, "failedChecks": failed[:12]}


def main():
    workers = int(os.environ.get("SELFTEST_WORKERS", "4"))
    only = [a for a in sys.argv[1:] if a in CONTROLS]
    names = only or sorted(CONTROLS)
    with ThreadPoolExecutor(workers) as ex:
        controls = list(ex.map(run_control, names))
    baseline = [] if only else run_control_baseline()
    out = {"standing": "AUTHOR candidate 05 mutation controls; not approval", "baselineFailures": baseline,
           "controls": controls, "caught": sum(c["caught"] for c in controls), "total": len(controls),
           "reviewer01MutantsAdapted": sum(1 for c in controls if c["control"].startswith("r_")),
           "reviewer02MutantsAdapted": sum(1 for c in controls if c["control"].startswith("r2_")),
           "reviewer03MutantsAdapted": sum(1 for c in controls if c["control"].startswith("r3_")),
           "reviewer04MutantsAdapted": sum(1 for c in controls if c["control"].startswith("r4_")),
           "allCaught": all(c["caught"] for c in controls) and not baseline}
    if not only:
        W(HERE / "selftest-result.json", out)
    print(json.dumps({k: out[k] for k in ("baselineFailures", "caught", "total", "reviewer01MutantsAdapted", "reviewer02MutantsAdapted", "reviewer03MutantsAdapted", "reviewer04MutantsAdapted", "allCaught")} |
                     {"missed": [c for c in controls if not c["caught"]]}, indent=1)[:12000])
    return 0 if out["allCaught"] else 1


def run_control_baseline():
    CONTROLS["baseline"] = (lambda root: None, [])
    res = run_control("baseline")
    del CONTROLS["baseline"]
    shutil.rmtree(HERE / "tmp" / "selftest", ignore_errors=True)
    return res["failedChecks"]


if __name__ == "__main__":
    sys.exit(main())
