// Expectation revisions and category aliases used ONLY when grading the author-03
// checker. The frozen author02 baseline is always graded against the original
// author/reviewer expectations. Every revision states why the original expectation
// encoded a restriction of the old design rather than the build-plan boundary.
export const ALIASES = {
  symlink: ['input-path'],
  'external-parse-failure': ['parse-failure'],
};

export const REVISIONS = {
  'author:P13-accepted-unresolved-external': {
    expect: 'refuse', refuse: ['lane-record-invalid'],
    rationale: 'Root correction04 for actual review03 X02/X03: a caller lane record cannot grant trusted loader or missing-module exceptions to a bound product package. The prior positive fixture relied on precisely that permission. Refusal is intentionally stricter; an independently selected tool exception policy remains required before such use in a real bound package.',
  },
  'author:N62-cts-static-and-dynamic-same-specifier': {
    expect: 'accept', refuse: [],
    rationale: 'Valid code: a value-used static import (emitted as require in .cts) and import() with both exports branches present. The old refusal worked around dependency-cruiser request dedup; TypeScript reports a mode per usage location and the emitter keeps both requests, so each is resolved with its own condition.',
  },
  'reviewer:RV-T01-lane-record-declares-browser-src-as-node': {
    expect: 'exit2', refuse: [],
    rationale: 'Review-02 A6: platforms are checker-owned policy keyed by the design-lock-bound inventory package. A caller record that tries to choose platforms or browser roots is invalid input (exit 2), not trusted.',
  },
  'reviewer:RV-F03-external-cts-static-plus-dynamic': {
    expect: 'refuse', refuse: ['unresolved'],
    rationale: 'The reached external entry is a .cts file under node_modules; Node 24 refuses to type-strip it (ERR_UNSUPPORTED_NODE_MODULES_TYPE_STRIPPING), so the runtime edge is refused as not loadable. The mixed-mode dedup restriction no longer exists.',
  },
  'reviewer:RV-N01-relative-path-undeclared-external': {
    expect: 'refuse', refuse: ['undeclared-external', 'lane-escape', 'unresolved', 'external-by-path'],
    rationale: 'Review-02 R5. The candidate refuses own-source requests that reach materialized dependency files by path with a specific category, external-by-path; the original accepted categories are kept and the new specific one is added.',
  },
  'reviewer:RV-N02-relative-path-bypasses-exports': {
    expect: 'refuse', refuse: ['unresolved', 'undeclared-external', 'lane-escape', 'external-by-path'],
    rationale: 'Review-02 R5, as RV-N01: the exports bypass is refused as external-by-path.',
  },
  'reviewer:RV-N23-provider-runtime-imports-devdependency': {
    expect: 'refuse', refuse: ['runtime-dev-dependency'],
    rationale: 'Review-02 A5 left the policy open. This candidate proposes: provider/browser runtime groups may reach only dependencies/optionalDependencies/peerDependencies; build scripts and tooling may also reach devDependencies. Proposal for root/reviewer decision, not a settled product rule.',
  },
};

export function expectationFor(set, testCase) {
  const original = {
    expect: testCase.expect === 'accept' ? 'accept' : testCase.expect === 'exit2' ? 'exit2' : testCase.kind === 'trust' ? 'trust' : 'refuse',
    refuse: testCase.refuse ?? [],
  };
  const revision = REVISIONS[`${set}:${testCase.id}`];
  return { original, forNew: revision ? { expect: revision.expect, refuse: revision.refuse } : original, revision };
}

export function grade(expectation, run, { legacy = false } = {}) {
  const report = run.report;
  if (expectation.expect === 'exit2') return run.status === 2 ? 'correct' : 'missed';
  if (expectation.expect === 'trust') return run.status === 2 ? 'trust-refused-exit2' : report?.passed ? 'trusted-input-accepted' : 'trust-refused';
  if (!report) return run.status === 2 ? 'invalid-invocation' : 'tool-error';
  const categories = report.refusals.map(r => r.category);
  if (categories.includes('tool-error')) return 'tool-error';
  if (expectation.expect === 'accept') return report.passed ? 'correct' : 'false-refusal';
  if (report.passed) return 'missed';
  const acceptable = new Set(expectation.refuse.flatMap(c => [c, ...(legacy ? [] : ALIASES[c] ?? [])]));
  return categories.some(c => acceptable.has(c)) ? 'correct' : 'wrong-reason';
}
