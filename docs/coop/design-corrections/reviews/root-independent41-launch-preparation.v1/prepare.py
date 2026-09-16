from pathlib import Path
import json,hashlib,subprocess,ast,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');P=Path(__file__).parent;A=B/'claude-independent-design.v40';N=B/'claude-independent-design.v41';H=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0 and (A/'review.md').is_file() and (A/'review.json').is_file()
assert (L/A.name/'final-public-artifact-manifest.json').is_file()
ps=subprocess.run(['ps','-axo','pid,ppid,command'],capture_output=True,text=True).stdout;assert not any('/claude ' in s and '85a08aec-9d22-4ac6-8ec2-c10170e727d7' in s for s in ps.splitlines())
mf=L/'candidate-subject.v41.json';s=B/'candidate-subject.v41';archive=L/'candidate-source.v41.tar.gz';pkg=B/'claude-author-package-successor.v18';v=B/'author-package-final41-verification.v1/verification.json';ref=L/'codex-post-reset.v1/final-reference.v41/reference-checks.json'
assert H(mf.read_bytes())=='eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236'
assert H(archive.read_bytes())=='c12aa7dbe6730443aa39db04d46a0ab6b2c72393725be56284cd9ed6ab099db8'
assert H((pkg/'artifact-manifest.json').read_bytes())=='10bafe77c0e1e4201243784ed0a4524f3f96c9f6e1a83da93fabcacaef37e139'
assert H(v.read_bytes())=='c0baa73ed8f92c11731d47607315fffc69e1e6f36eb8e8f9e7155c420bb226cf' and json.loads(v.read_bytes())['passed']
assert H(ref.read_bytes())=='ea842a6d205edde513274f7b3c895c98ab9abfcfc25fc37a31e04e389484bbf2'
assert not N.exists();N.mkdir();scope=(P/'review-scope.md').read_text();header=f"""Current exact binding header. Frozen source41 {s}; manifest {mf} SHA {H(mf.read_bytes())}; archive {archive} SHA {H(archive.read_bytes())};12912members737732367bytes. Parent40 manifest SHA3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072 preserved. Current final root reference {ref} SHA{H(ref.read_bytes())}; actual execution /tmp/opensip-design-corrections/root-source41-final-reference.v1. Package18 {pkg}, artifact manifest SHA{H((pkg/'artifact-manifest.json').read_bytes())}, files-only projection SHA0b18409dc0bb1b01da841e004d124411111c263258d569793e24fce548e71600. Completed final package verification {v} SHA{H(v.read_bytes())}. Rebuild report /tmp/opensip-design-corrections/root-author-package-final41-rebuild.v1/rebuild-report.json SHA1a860350750ca04f9fda8839df7c773e7e332fd0a712d26b8f6d564c12e1beec. Planning input layer10 SHA{H((s/'docs/v2/architecture/implementation-normative-inputs.v10.json').read_bytes())}. Your completed40 report {A/'review.json'} SHA{H((A/'review.json').read_bytes())}; preserve it as history. Bounded author proposal /tmp/opensip-design-corrections/claude-view-attribution-assessment.v1/review.json SHAa06602738c29bd923cf2c1d0a9d47b6a011a819d5f49ef1ac43a366be8cd23de; integrated exact patch SHA f795b00609b4479dc09e5608d9d16cd5d06cf8531f0f324d57f06039d79d91b8. Root integration /tmp/opensip-design-corrections/root-view-attribution-integration.v1/integration.json. These are review inputs, never an acceptance direction or blind evidence.\n\n"""
(N/'prompt.md').write_text(header+scope)
text=(A/'launch.py').read_text();tree=ast.parse(text);node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='cmd' for x in n.targets));cmd=ast.literal_eval(node.value)
for path in [s,pkg,v.parent,B/'root-author-package-final41-rebuild.v1',A,B/'claude-view-attribution-assessment.v1',B/'root-view-attribution-integration.v1',B/'root-view-attribution-controls.v1',B/'root-source41-final-reference.v1']:
 if str(path) not in cmd:cmd+=['--add-dir',str(path)]
lines=text.splitlines(True);lines[node.lineno-1:node.end_lineno]=['cmd='+repr(cmd)+'\n'];(N/'launch.py').write_text(''.join(lines))
d={'standing':'PREPARED UNLAUNCHED original non-author85 current41 source review. Prior40 report complete, sameSIDidle. No blind inputs, no acceptance prescribed.','sourceManifestSha256':H(mf.read_bytes()),'parentReviewSha256':H((A/'review.json').read_bytes()),'promptSha256':H((N/'prompt.md').read_bytes()),'launcherSha256':H((N/'launch.py').read_bytes()),'runtime':str(N)};(N/'preparation.json').write_text(json.dumps(d,indent=2)+'\n')
D=L/(N.name+'-dispatch');D.mkdir()
for name in ['prompt.md','launch.py','preparation.json']:shutil.copy2(N/name,D/name)
print(json.dumps(d))
