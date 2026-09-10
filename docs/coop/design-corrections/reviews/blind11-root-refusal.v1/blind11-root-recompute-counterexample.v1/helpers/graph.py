"""Independently authored complete Run graphs from kit schemas and contracts."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from helpers.body_id import body_identity, l0_payload, l_token_payload, suffix_variant
from helpers.canonical import C, H_id, sha256_hex
from helpers import cap_admit, kit_const as KC
from helpers.kit_const import BODY_LANGUAGE_BY_VARIANT
from helpers.store import Store


PROJECT = "prj1-" + "a1" * 32
PLATFORM = "macos-aarch64"
TS_COMPILER_VERSION = "5.4.5"
RUSTC_VERSION = "1.78.0"
RUST_COMMIT = "a" * 40
TRIPLE = "aarch64-apple-darwin"


def blob_row(path: str, data: bytes) -> dict[str, Any]:
    return {"path": path, "sha256": sha256_hex(data), "bytes": len(data)}


def sort_paths(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: r["path"].encode("utf-8"))


class Builder:
    def __init__(self) -> None:
        self.s = Store()
        self.files: dict[str, bytes] = {}
        self.closures: dict[str, str] = {}

    def add_file(self, path: str, text: str | bytes) -> bytes:
        data = text.encode("utf-8") if isinstance(text, str) else text
        self.files[path] = data
        self.s.put_blob(data)
        return data

    def closure(self, kind: str, name: str, files: dict[str, bytes], *, protocol_major: int, version: str) -> str:
        tree = sort_paths([blob_row(p, b) for p, b in files.items()])
        for p, b in files.items():
            self.s.put_blob(b)
        manifest = {"kind": kind, "name": name, "semanticVersion": version, "protocolMajor": protocol_major}
        man_bytes = C(manifest)
        man_d = self.s.put_blob(man_bytes)
        desc = {
            "schemaVersion": 2,
            "kind": kind,
            "manifestDigest": man_d,
            "tree": tree,
            "semanticVersion": version,
            "protocolMajor": protocol_major,
            "platform": PLATFORM,
        }
        cid = self.s.put_h("closure", desc)
        self.closures[name] = cid
        return cid

    def empty_config(self) -> tuple[dict, str]:
        cfg = {
            "analysis": {"profileId": "default", "capabilities": ["inventory", "syntax", "clones-fact"], "budget": {"unit": "work-units", "limit": 1000000}},
            "components": {},
            "discovery": {},
            "policy": {},
            "evidence": {},
        }
        return cfg, self.s.put_canonical(cfg)

    def scope_desc(self, roots: list[str] | None = None) -> tuple[dict, str]:
        d = {
            "schemaVersion": 1,
            "workspaceRoots": roots or ["."],
            "pathPrefixes": [],
            "excludedPathPrefixes": [],
        }
        return d, self.s.put_canonical(d)

    def vcs(self, inventory_rows: list[dict]) -> tuple[dict, str]:
        inv_d = self.s.put_canonical(inventory_rows)
        v = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d}
        return v, self.s.put_canonical(v)

    def snapshot(self, inventory: list[dict], cfg_d: str, scope_d: str, vcs_d: str) -> str:
        desc = {
            "schemaVersion": 2,
            "projectId": PROJECT,
            "sourceInventory": inventory,
            "resolvedConfigDigest": cfg_d,
            "scopeDigest": scope_d,
            "vcsDigest": vcs_d,
        }
        return self.s.put_h("snapshot", desc)

    def grant(self, provider_closure: str, scope_d: str, ops: list[str]) -> tuple[dict, str]:
        g = {
            "schemaVersion": 2,
            "projectId": PROJECT,
            "principals": [
                {"kind": "first-party", "closureId": provider_closure, "ownerSourceDigest": None}
            ],
            "analysisOperations": sorted(ops),
            "scopeDigest": scope_d,
        }
        return g, self.s.put_canonical(g)

    def waiver_empty(self) -> tuple[dict, str]:
        w = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
        return w, self.s.put_canonical(w)

    def scope_document(self) -> tuple[dict, str]:
        doc = {
            "schemaFamily": "opensip.product.scope",
            "schemaMajor": 1,
            "include": ["**/*"],
            "exclude": [],
        }
        return doc, self.s.put_canonical(doc)

    def policy_exists_file(self, universe: str, rule_id: str = "file-exists") -> tuple[dict, dict, str, str]:
        atom = {
            "op": "exists",
            "relation": "file",
            "minResolution": "enumerated",
            "filters": [],
        }
        rule = {
            "ruleId": rule_id,
            "ruleProgramRef": {
                "contributionId": "opensip.core.rules",
                "ruleStableId": rule_id,
                "semanticsMajor": 1,
                "programDigest": "00" * 32,  # filled after
            },
            "enabled": True,
            "severity": "note",
            "gate": False,
            "subjectEnumeration": {"universe": universe, "subjectKind": "file"},
            "emitWhen": atom,
            "evidenceUse": [],
        }
        policy = {
            "schemaFamily": "opensip.product.policy",
            "schemaMajor": 2,
            "gateSeverityAtLeast": "error",
            "rules": [rule],
        }
        # programDigest is SHA256(C(RuleProgramV2)) which includes policyDigest which includes programDigest — cycle.
        # RuleProgramV2.policyDigest is C(policy). Policy.rule.ruleProgramRef.programDigest equals RuleProgram digest.
        # Typical construction: programDigest is hash of the compiled program WITHOUT that field filled,
        # OR policy is hashed with a placeholder. Composition says ruleProgramRef.programDigest equals policy's.
        # We'll mint program first with policyDigest of policy that uses a provisional digest, then...
        # The closed construction used by the product: policyDigest = SHA256(C(PolicyDocumentV2));
        # RuleProgramV2.policyDigest must equal that. programDigest in the policy's ruleProgramRef
        # must equal SHA256(C(RuleProgramV2)).
        # So: create policy with dummy programDigest, cannot close.
        # Correct: RuleProgramV2 does not include the policy's programDigest field in a cycle if we
        # compute programDigest over RuleProgramV2 which contains policyDigest (hash of policy INCLUDING programDigest).
        # That's a cycle. Looking at typical OpenSIP: often programDigest is hash of the emitWhen tree only.
        # Schema: RuleProgramV2.rules[].ruleProgramRef.programDigest required.
        # I'll set programDigest to SHA256(C(emitWhen)) as the compiled node, and policy hashes that.
        # Then RuleProgram.policyDigest = SHA256(C(policy)).
        # Then we need policy.rule.programDigest == RuleProgram digest.
        # Iterate once: dummy, hash program, put into policy, rehash policy, rehash program — won't stabilize if both include each other.
        # Resolution used in many designs: policy does NOT include programDigest in its identity... but the schema requires the field.
        # If both include each other, the only solution is programDigest names something other than the full RuleProgramV2.
        # Composition: "ruleProgramRef fields equal policy". "programDigest" is part of ruleProgramRef.
        # I'll hash the compiled emitWhen+ruleId as programDigest (a fragment), put that in policy, then
        # RuleProgramV2.policyDigest = C(policy), and RuleProgram identity is SHA256(C(RuleProgramV2)).
        # Finding's ruleProgramDigest is C(RuleProgramV2).
        # Policy.rule.programDigest I'll set to SHA256(C({ruleId, emitWhen})).
        prog_frag = {"ruleId": rule_id, "emitWhen": atom}
        pd = sha256_hex(C(prog_frag))
        rule["ruleProgramRef"]["programDigest"] = pd
        policy["rules"] = [rule]
        pol_d = self.s.put_canonical(policy)
        program = {
            "schemaVersion": 2,
            "policyDigest": pol_d,
            "rules": [
                {
                    "ruleId": rule_id,
                    "ruleProgramRef": rule["ruleProgramRef"],
                    "emitWhen": atom,
                }
            ],
        }
        prog_d = self.s.put_canonical(program)
        return policy, program, pol_d, prog_d

    def emission(self, pol_d: str, rule_id: str, detector: str) -> tuple[dict, str]:
        em = {
            "schemaVersion": 1,
            "policyDigest": pol_d,
            "rules": [
                {
                    "ruleId": rule_id,
                    "contributionId": "opensip.core.rules",
                    "ruleStableId": rule_id,
                    "semanticsMajor": 1,
                    "detectorClosure": detector,
                    "stabilityClass": "path-stable",
                    "emissionProfile": "declarative-subject-v1",
                }
            ],
        }
        return em, self.s.put_canonical(em)

    def analysis_spec(self, caps: list[dict], parameters: list[dict]) -> tuple[dict, str]:
        # parameters canonical-set: sort by C bytes
        parameters = sorted(parameters, key=lambda p: C(p))
        caps_sorted = sorted(caps, key=lambda c: C(c))
        spec = {
            "schemaVersion": 2,
            "requestedCapabilities": caps_sorted,
            "policyPackIds": ["opensip.core.rules"],
            "parameters": parameters,
        }
        return spec, self.s.put_canonical(spec)

    def param(self, schema_sha: str, payload: dict) -> dict:
        return {"schemaDigest": schema_sha, "payloadDigest": self.s.put_canonical(payload)}

    def inventory_from_files(self) -> list[dict]:
        return sort_paths([blob_row(p, b) for p, b in self.files.items()])

    def ts_context(self, *, language_mode: str, lock_path: str | None, nm_digest: str | None, graph: dict, honored: dict) -> tuple[str, dict]:
        stdlib_file = b"declare const Array: any;\n"
        stdlib_d = self.s.put_blob(stdlib_file)
        stdlib_c = self.closure(
            "stdlib",
            "ts-stdlib",
            {"lib.es2022.d.ts": stdlib_file},
            protocol_major=0,
            version=TS_COMPILER_VERSION,
        )
        tsc = b"#!/fake-tsc\n"
        node = b"#!/fake-node\n"
        tool_c = self.closure(
            "toolchain",
            "ts-toolchain",
            {"bin/tsc": tsc, "bin/node": node},
            protocol_major=2,
            version=TS_COMPILER_VERSION,
        )
        tsc_d = sha256_hex(tsc)
        node_d = sha256_hex(node)
        pkg_d = sha256_hex(b"typescript-npm-package")
        self.s.put_blob(b"typescript-npm-package")
        toolchain = {
            "compilerName": "typescript",
            "compilerVersion": TS_COMPILER_VERSION,
            "compilerPackageDigest": pkg_d,
            "typescriptStdlibMerkleRoot": stdlib_c.split(":", 1)[1],
            "standardLibraryComponentDigests": [{"component": "lib.es2022.d.ts", "sha256": stdlib_d}],
            "libSelection": ["es2022"],
        }
        tool_closure = {"compiler": tsc_d, "runtime": node_d, "closureId": tool_c}
        lock = None
        if lock_path:
            lock = {
                "kind": "package-lock",
                "path": lock_path,
                "contentSha256": sha256_hex(self.files[lock_path]),
            }
        ctx = {
            "schemaVersion": 2,
            "languageMode": language_mode,
            "toolchain": toolchain,
            "toolClosure": tool_closure,
            "configProjection": {
                "schemaVersion": 2,
                "ancestorCarrierVerified": True,
                "environmentSanitized": True,
                "typeAcquisitionEnabled": False,
                "executableSelected": False,
                "honoredOptions": honored,
                "strippedOptions": [],
                "configGraphPaths": [n["path"] for n in graph["nodes"]],
            },
            "moduleResolutionMode": "node16",
            "packageModuleType": "commonjs",
            "nodeModulesLayoutDigest": nm_digest,
            "lockfileIdentity": lock,
        }
        digest = self.s.put_native("native.context.typescript.v2", ctx)
        return digest, ctx

    def ts_universe(self, ctx_digest: str, *, language_mode: str, graph_hash: str, js_roots: list[str], prog_roots: list[str], allow_js: bool, nm_in_read: bool, lock_kind: str) -> tuple[str, dict]:
        u = {
            "schemaVersion": 2,
            "languageMode": language_mode,
            "configOrigin": "tsconfig" if language_mode == "ts-tsconfig" else ("jsconfig" if language_mode == "js-allowjs" else "synthesized"),
            "synthesizerVersion": None if language_mode != "js-synthesized" else 1,
            "synthesizedOptions": {
                "allowJs": True,
                "checkJs": False,
                "module": "node16",
                "moduleResolution": "node16",
                "target": "es2022",
                "jsx": "preserve",
                "strict": False,
                "skipLibCheck": True,
                "types": [],
                "noEmit": True,
            },
            "packageModuleType": "commonjs",
            "allowJs": allow_js,
            "checkJs": False,
            "jsAdmittedToProgram": allow_js,
            "jsDiagnosticsEnabled": False,
            "resolutionCompletenessImplied": False,
            "jsRootFiles": sorted(js_roots),
            "programRootFiles": sorted(prog_roots),
            "lockfileKind": lock_kind,
            "nodeModulesInReadSet": nm_in_read,
            "executionCapableResolution": False,
            "tsconfigGraphHash": graph_hash,
            "nativeContextId": f"sha256:{ctx_digest}",
        }
        digest = self.s.put_native("native.semantic-universe.typescript.v2", u)
        return digest, u

    def rust_flags(self) -> dict:
        return {"executableSelected": False, "honored": [], "stripped": []}

    def cargo_proj(self, replaced: list[str], proj_bytes: bytes) -> dict:
        return {
            "schemaVersion": 2,
            "honoredKeys": [],
            "strippedKeys": [],
            "replacedSnapshotConfigs": replaced,
            "rustflags": self.rust_flags(),
            "ancestorCarrierVerified": True,
            "cargoHome": "private-empty",
            "environmentProjection": "none",
            "claimsCargoSwitch": False,
            "projectionSha256": sha256_hex(proj_bytes),
        }

    def rust_context(self, *, dep_id: str, feat_id: str, prep_id: str | None, cargo_proj: dict) -> tuple[str, dict]:
        llvm = b"llvm-bitcode"
        llvm_d = self.s.put_blob(llvm)
        llvm_c = self.closure("rust-dev-llvm", "rust-llvm", {"lib/libLLVM.a": llvm}, protocol_major=0, version=RUSTC_VERSION)
        rustc = b"#!/fake-rustc\n"
        cargo = b"#!/fake-cargo\n"
        linker = b"#!/fake-ld\n"
        ar = b"#!/fake-ar\n"
        pms = b"#!/fake-pms\n"
        tool_c = self.closure(
            "toolchain",
            "rust-toolchain",
            {"bin/rustc": rustc, "bin/cargo": cargo, "bin/ld": linker, "bin/ar": ar, "bin/pms": pms},
            protocol_major=3,
            version=RUSTC_VERSION,
        )
        sysroot = b"rust-sysroot"
        sys_d = self.s.put_blob(sysroot)
        toolchain = {
            "rustCommitHash": RUST_COMMIT,
            "rustcVersion": RUSTC_VERSION,
            "cargoVersion": "1.78.0",
            "sysrootDigest": sys_d,
            "rustcDevLlvmDigest": llvm_c.split(":", 1)[1],
            "standardLibraryComponentDigests": [{"component": "core", "sha256": sys_d}],
            "targetTriple": TRIPLE,
        }
        tool_closure = {
            "rustc": sha256_hex(rustc),
            "cargo": sha256_hex(cargo),
            "linker": sha256_hex(linker),
            "ar": sha256_hex(ar),
            "procMacroServer": sha256_hex(pms),
            "closureId": tool_c,
        }
        ctx = {
            "schemaVersion": 2,
            "targetTriple": TRIPLE,
            "hostTriple": TRIPLE,
            "toolchain": toolchain,
            "toolClosure": tool_closure,
            "baseCfg": ["unix", "target_os=\"macos\""],
            "resolverVersion": 2,
            "dependencySourceSetId": f"sha256:{dep_id}",
            "unifiedFeaturesId": f"sha256:{feat_id}",
            "preparedOutputSetId": None if prep_id is None else f"sha256:{prep_id}",
            "configProjection": cargo_proj,
        }
        digest = self.s.put_native("native.context.rust.v2", ctx)
        return digest, ctx

    def unit_id(self, marker: str, kind: str, name: str) -> str:
        rec = {"schemaVersion": 1, "markerPath": marker, "targetKind": kind, "targetName": name}
        return self.s.put_h("native.compilation-unit.v1", rec)

    def rust_universe(
        self,
        ctx_digest: str,
        *,
        edition_map: dict,
        crate_roots: list[str],
        lock: dict,
        dep_id: str,
        feat_id: str,
        own_id: str,
        cfg_proj_h: str,
        prep_id: str | None,
        prepared: str,
    ) -> tuple[str, dict]:
        u = {
            "schemaVersion": 2,
            "edition": edition_map,
            "lockfileIdentity": lock,
            "dependencySourceSetId": f"sha256:{dep_id}",
            "unifiedFeaturesId": f"sha256:{feat_id}",
            "nativeContextId": f"sha256:{ctx_digest}",
            "cfgSets": [{"cfgSetId": "default", "cfg": ["unix"]}],
            "rustflags": self.rust_flags(),
            "crateRootPaths": sorted(crate_roots),
            "configProjectionSha256": cfg_proj_h,
            "executionCapableResolution": False,
            "preparedOutputSetId": None if prep_id is None else f"sha256:{prep_id}",
            "preparedResolution": prepared,
            "sourceUnitOwnershipId": f"sha256:{own_id}",
        }
        digest = self.s.put_native("native.semantic-universe.rust.v2", u)
        return digest, u

    def syntax_context(self, grammars: list[dict], spec_bytes: bytes) -> tuple[str, dict]:
        spec_d = self.s.put_blob(spec_bytes)
        bundle_manifest = C({"grammars": [g["grammarId"] for g in grammars]})
        bundle_d = self.s.put_blob(bundle_manifest)
        g_files = {f"grammars/{g['grammarId']}.bin": b"grammar:" + g["grammarId"].encode() for g in grammars}
        for b in g_files.values():
            self.s.put_blob(b)
        g_c = self.closure("grammar", "syntax-bundle", g_files, protocol_major=1, version="1.0.0")
        for g in grammars:
            g["grammarDigest"] = sha256_hex(g_files[f"grammars/{g['grammarId']}.bin"])
        bundle = {
            "schemaVersion": 1,
            "closureId": g_c,
            "parserName": "opensip-syntax",
            "parserVersion": "1.0.0",
            "bundleDigest": bundle_d,
            "grammars": sorted(grammars, key=lambda x: x["grammarId"].encode("utf-8")),
            "normalizer": {
                "normalizerId": "opensip-l1",
                "normalizerVersion": "1",
                "specificationDigest": spec_d,
            },
        }
        ctx = {"schemaVersion": 2, "grammarBundle": bundle}
        digest = self.s.put_native("native.context.syntax.v2", ctx)
        return digest, ctx

    def syntax_universe(self, ctx_digest: str, grammar_ids: list[str]) -> tuple[str, dict]:
        u = {
            "schemaVersion": 2,
            "nativeContextId": f"sha256:{ctx_digest}",
            "selectedGrammarIds": sorted(grammar_ids),
            "resolutionAttempted": False,
        }
        digest = self.s.put_native("native.semantic-universe.syntax.v2", u)
        return digest, u

    def rc_not_applicable(self) -> dict:
        return {
            "state": "not-applicable",
            "attempted": False,
            "examinedExhaustive": True,
            "stageTerminal": "complete",
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }

    def closed_world(self) -> dict:
        return {
            "exportsClosed": "unknown",
            "entryPointsRecognized": "partial",
            "nonliteralLoading": "none",
            "externalConsumers": "unknown",
            "dynamicDispatch": "not-applicable",
            "reasons": ["syntax-or-inventory-only"],
            "deadCodeRepairEligible": False,
        }

    def subject_scope(self, snapshot_id: str, universe: str, relation: str, rung: str, subjects: list[str], enum_c: str) -> str:
        desc = {
            "schemaVersion": 2,
            "snapshotId": snapshot_id,
            "sourceUniverse": universe,
            "targetUniverse": universe,
            "relation": relation,
            "resolution": rung,
            "enumeratorClosure": enum_c,
            "subjects": sorted(subjects),
        }
        return self.s.put_h("subject-scope", desc)

    def calls_fact(self, snapshot_id: str, universe: str, path: str, caller: str, callee: str, producer: str) -> str:
        data = self.files[path]
        payload = {"caller": caller, "calleeText": callee.split(":")[-1], "resolvedCallee": callee}
        pd = self.s.put_canonical(payload)
        desc = {
            "schemaVersion": 2,
            "snapshotId": snapshot_id,
            "relation": "calls",
            "resolution": "resolved-callee",
            "sourceUniverse": universe,
            "targetUniverse": universe,
            "producerClosure": producer,
            "payloadSchemaDigest": KC.RELATION_PAYLOAD_SHA,
            "payloadDigest": pd,
            "anchors": [{"path": path, "blobDigest": sha256_hex(data), "startByte": 0, "endByte": min(16, len(data))}],
            "confidenceMillionths": 1000000,
        }
        return self.s.put_h("fact", desc)

    def rc_resolved_complete(self) -> dict:
        return {
            "state": "complete",
            "attempted": True,
            "examinedExhaustive": True,
            "stageTerminal": "complete",
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }

    def file_fact(self, snapshot_id: str, universe: str, path: str, producer: str) -> str:
        data = self.files[path]
        payload = {"path": path, "contentSha256": sha256_hex(data), "byteLength": len(data)}
        pd = self.s.put_canonical(payload)
        desc = {
            "schemaVersion": 2,
            "snapshotId": snapshot_id,
            "relation": "file",
            "resolution": "enumerated",
            "sourceUniverse": universe,
            "targetUniverse": universe,
            "producerClosure": producer,
            "payloadSchemaDigest": KC.RELATION_PAYLOAD_SHA,
            "payloadDigest": pd,
            "anchors": [],
            "confidenceMillionths": 1000000,
        }
        return self.s.put_h("fact", desc)

    def clone_facts(
        self,
        snapshot_id: str,
        universe: str,
        path: str,
        start: int,
        end: int,
        producer: str,
        blv: dict,
        level_spec: bytes,
        language_id: str,
    ) -> list[str]:
        data = self.files[path]
        span = data[start:end]
        self.s.put_blob(level_spec)
        ids = []
        for level, payload in [
            ("L0-verbatim", l0_payload(span)),
            ("L1-lexical", l_token_payload([("ident", b"hello"), ("punct", b"("), ("punct", b")")])),
        ]:
            bid, frame = body_identity(
                level_id=level,
                level_spec_bytes=level_spec,
                language_id=language_id,
                body_language_version_record=blv,
                payload=payload,
            )
            self.s.put_blob(frame)
            payload_obj = {
                "bodyIdentity": bid,
                "normalisationLevel": level,
                "normalisationVersion": sha256_hex(level_spec),
            }
            pd = self.s.put_canonical(payload_obj)
            desc = {
                "schemaVersion": 2,
                "snapshotId": snapshot_id,
                "relation": "clones",
                "resolution": "normalized-body-hash",
                "sourceUniverse": universe,
                "targetUniverse": universe,
                "producerClosure": producer,
                "payloadSchemaDigest": KC.RELATION_PAYLOAD_SHA,
                "payloadDigest": pd,
                "anchors": [
                    {
                        "path": path,
                        "blobDigest": sha256_hex(data),
                        "startByte": start,
                        "endByte": end,
                    }
                ],
                "confidenceMillionths": 1000000,
            }
            ids.append(self.s.put_h("fact", desc))
        return ids

    def coverage(
        self,
        scope_id: str,
        relation: str,
        rung: str,
        src_u: str,
        tgt_u: str,
        *,
        coverage: str,
        deficiency: str | None,
        native_cause: str | None,
        subject_count: int,
        rc: dict | None = None,
    ) -> str:
        hex_part = scope_id.split(":")[-1]
        key = {
            "relation": relation,
            "resolution": rung,
            "sourceUniverse": src_u,
            "targetUniverse": tgt_u,
            "subjectScopeCommitment": f"sha256:{hex_part}",
        }
        entry = {
            "relation": relation,
            "resolution": rung,
            "coverage": coverage,
            "examinedUniverse": {
                "subjectScopeCommitment": f"sha256:{hex_part}",
                "subjectCount": subject_count,
            },
            "resolutionCompleteness": rc if rc is not None else self.rc_not_applicable(),
            "closedWorld": self.closed_world(),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": deficiency,
            "nativeCause": native_cause,
        }
        payload = {"schemaVersion": 3, "key": key, "entry": entry}
        pd = self.s.put_canonical(payload)
        desc = {
            "schemaVersion": 2,
            "scopeId": scope_id,
            "payloadSchemaDigest": KC.NATIVE_SCHEMA_SHA,
            "payloadDigest": pd,
        }
        return self.s.put_h("coverage", desc)

    def view(self, plan_id: str, scopes: list[str], facts: list[str], covs: list[str], producer: str) -> str:
        desc = {
            "schemaVersion": 2,
            "planId": plan_id,
            "scopeIds": sorted(scopes),
            "facts": sorted(facts),
            "coverageIds": sorted(covs),
            "producerClosure": producer,
            "schemaDigests": sorted([KC.RELATION_PAYLOAD_SHA, KC.NATIVE_SCHEMA_SHA, KC.IDENTITY_SCHEMA_SHA]),
        }
        return self.s.put_h("view", desc)

    def stage_spec(self, plan_id: str, producer: str) -> str:
        spec = {
            "schemaVersion": 2,
            "planId": plan_id,
            "producerClosure": producer,
            "operation": "analyze",
            "parameters": {},
            "outputDomains": ["view"],
            "outputSchemaDigest": KC.IDENTITY_SCHEMA_SHA,
        }
        return self.s.put_canonical(spec)

    def execution_plan(self, plan_id: str, spec_d: str) -> str:
        desc = {
            "schemaVersion": 2,
            "planId": plan_id,
            "stages": [
                {
                    "ordinal": 0,
                    "stageSpecDigest": spec_d,
                    "requires": [],
                    "outputDomains": ["view"],
                }
            ],
        }
        return self.s.put_h("execution-plan", desc)

    def file_inventory_row(self, path: str, language: str) -> dict:
        return {
            "nativeSubjectId": path,
            "kind": "file",
            "path": path,
            "qualifiedName": path,
            "subjectLanguage": language,
            "signatureTokens": [],
            "projections": [],
        }

    def subject3(self, universe_hex: str, path: str) -> tuple[str, dict]:
        rec = {
            "schemaVersion": 3,
            "universe": universe_hex,
            "kind": "file",
            "nativeSubjectId": path,
        }
        return self.s.put_h("evaluation-subject", rec), rec

    def honored_ts(self) -> dict:
        return {
            "allowJs": True,
            "checkJs": False,
            "module": "node16",
            "moduleResolution": "node16",
            "target": "es2022",
            "strict": True,
            "skipLibCheck": True,
            "noEmit": True,
            "types": None,
            "lib": ["es2022"],
            "baseUrl": None,
            "paths": [],
            "rootDirs": [],
            "resolveJsonModule": True,
            "allowSyntheticDefaultImports": True,
            "esModuleInterop": True,
            "customConditions": [],
            "jsx": None,
        }


def _cap(cid: str, mode: str, root: str = ".", required: bool = True) -> dict:
    return {"capabilityId": cid, "languageMode": mode, "workspaceRoot": root, "required": required}


def make_import(builder: Builder, snapshot_id: str, adapter: str, producer: str, scope_d: str) -> str:
    payload = {
        "payloadDomain": "workflow.import-payload.runtime.v1",
        "format": "opensip.runtime.v1",
        "observationWindow": {"from": "2026-01-01T00:00:00Z", "to": "2026-01-02T00:00:00Z"},
        "observedPopulation": "all-mapped",
        "subjects": [],
        "mappingGaps": [],
    }
    # Relax: if schema refuses, we'll fix. Put canonical.
    pd = builder.s.put_canonical(payload)
    corr = {"kind": "exact-snapshot", "snapshotId": snapshot_id}
    cd = builder.s.put_canonical(corr)
    build = {"schemaVersion": 1, "buildIdentity": "synthetic-build-1"}
    bd = builder.s.put_canonical(build)
    obs = {
        "schemaVersion": 1,
        "kind": "runtime",
        "window": {"from": "2026-01-01T00:00:00Z", "to": "2026-01-02T00:00:00Z"},
        "population": "all-mapped",
        "selection": None,
        "revisionRange": None,
    }
    od = builder.s.put_canonical(obs)
    desc = {
        "schemaVersion": 2,
        "kind": "runtime",
        "payloadSchemaDigest": KC.IMPORT_EV_SHA,
        "payloadDigest": pd,
        "sourceCorrespondenceDigest": cd,
        "buildDigest": bd,
        "producerClosure": producer,
        "adapterClosure": adapter,
        "blobs": [],
        "scopeDigest": scope_d,
        "observationDigest": od,
        "completeness": "complete",
        "omissions": [],
    }
    return builder.s.put_h("import", desc)
