from pathlib import Path
import hashlib,json
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-doctor-gate-repair');p=W/'apps/cli/tests/doctor_tests.rs';s=p.read_text();assert hashlib.sha256(p.read_bytes()).hexdigest()==json.loads((F/'owning-r7/report.json').read_text())['source']['sha256']
s=s.replace('fn strip_known_test_tail(text: &str) -> &str {\n    for tail in KNOWN_TEST_TAILS {\n        if let Some(before) = text.strip_suffix(tail) {','''const OUTCOMES_PATH: &str = "crates/host/src/outcomes.rs";
const MAIN_PATH: &str = "apps/cli/src/main.rs";
const SOURCE_PATHS: [&str; 7] = [
    "apps/cli/src/arguments.rs", "apps/cli/src/bootstrap.rs", MAIN_PATH,
    "apps/cli/src/terminal.rs", OUTCOMES_PATH,
    "crates/host/src/doctor_ingress.rs", "crates/host/src/request.rs",
];
const TEST_TAIL_PATHS: [&str; 3] = [
    OUTCOMES_PATH, "crates/host/src/doctor_ingress.rs", "crates/host/src/request.rs",
];
fn source_site_is(path: &str, expected: &str) -> bool { path == expected }
fn strip_known_test_tail<'a>(text: &'a str, path: &str) -> &'a str {
    for (owner, tail) in TEST_TAIL_PATHS.into_iter().zip(KNOWN_TEST_TAILS) {
        if source_site_is(path, owner) && let Some(before) = text.strip_suffix(tail) {''')
s=s.replace('fn production_source(text: &str, outcomes: bool) -> String {','fn production_source(text: &str, path: &str) -> String {\n    let outcomes = source_site_is(path, OUTCOMES_PATH);')
s=s.replace('strip_known_test_tail(&text);','strip_known_test_tail(&text, path);')
s=s.replace('let outcomes = path.ends_with("crates/host/src/outcomes.rs");','''let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..").canonicalize().unwrap();
    let canonical = path.canonicalize().unwrap();
    let site = canonical.strip_prefix(&root).unwrap().to_str().unwrap();
    assert!(SOURCE_PATHS.contains(&site), "unaccepted doctor source path: {site}");''')
s=s.replace('production_feature_sites_are_closed(&text, outcomes),\n        "unapproved feature selector in {}"','production_feature_sites_are_closed(&text, site),\n        "unapproved feature selector in {}"').replace('production_source(&text, outcomes)\n}', 'production_source(&text, site)\n}')
# Replace bool call sites with exact owner identities.
s=s.replace('production_source(&accepted, true)','production_source(&accepted, OUTCOMES_PATH)').replace('production_source(&expected, true)','production_source(&expected, OUTCOMES_PATH)').replace('production_source(&format!("{KNOWN_LOGGING_PREFIX}{altered}"), true)','production_source(&format!("{KNOWN_LOGGING_PREFIX}{altered}"), OUTCOMES_PATH)').replace('production_source(&accepted, false)','production_source(&accepted, "apps/cli/src/bootstrap.rs")').replace('production_source(&nested, true)','production_source(&nested, OUTCOMES_PATH)').replace('production_source(&debug, true)','production_source(&debug, OUTCOMES_PATH)').replace('production_source(&text, true)','production_source(&text, OUTCOMES_PATH)')
s=s.replace('for tail in KNOWN_TEST_TAILS {\n        let accepted_tail', 'for (owner, tail) in TEST_TAIL_PATHS.into_iter().zip(KNOWN_TEST_TAILS) {\n        let accepted_tail').replace('production_source(&accepted_tail, false)','production_source(&accepted_tail, owner)').replace('production_source(&after, false)','production_source(&after, owner)')
s=s.replace('fn production_feature_sites_are_closed(text: &str, outcomes: bool) -> bool {\n    if !outcomes && text == KNOWN_CLI_MAIN_SOURCE {','fn production_feature_sites_are_closed(text: &str, path: &str) -> bool {\n    let outcomes = source_site_is(path, OUTCOMES_PATH);\n    if source_site_is(path, MAIN_PATH) && text == KNOWN_CLI_MAIN_SOURCE {').replace('strip_known_test_tail(text))','strip_known_test_tail(text, path))')
s=s.replace('production_feature_sites_are_closed(&trusted, true)','production_feature_sites_are_closed(&trusted, OUTCOMES_PATH)').replace('"#[cfg(unix)]\\nfn ordinary() {}",\n        false','"#[cfg(unix)]\\nfn ordinary() {}",\n        "apps/cli/src/bootstrap.rs"').replace('production_feature_sites_are_closed(data, false)','production_feature_sites_are_closed(data, "apps/cli/src/bootstrap.rs")')
s=s.replace('for (text, outcomes) in [\n            (format!("{gate}\\nfn alternate() {{}}"), false),\n            (format!("{trusted}\\n{gate}\\nfn alternate() {{}}"), true),','for (text, path) in [\n            (format!("{gate}\\nfn alternate() {{}}"), "apps/cli/src/bootstrap.rs"),\n            (format!("{trusted}\\n{gate}\\nfn alternate() {{}}"), OUTCOMES_PATH),').replace('production_feature_sites_are_closed(&text, outcomes)','production_feature_sites_are_closed(&text, path)')
control='''#[test]
fn accepted_source_exceptions_are_bound_to_their_exact_paths() {
    for (owner, tail) in TEST_TAIL_PATHS.into_iter().zip(KNOWN_TEST_TAILS) {
        let text = if owner == OUTCOMES_PATH {
            format!("{KNOWN_LOGGING_PREFIX}{KNOWN_LOGGING_TESTS}fn ordinary() {{}}\\n{tail}")
        } else { format!("fn ordinary() {{}}\\n{tail}") };
        assert!(production_feature_sites_are_closed(&text, owner));
        assert!(!production_source(&text, owner).contains("cfg(test)"));
        for path in SOURCE_PATHS.into_iter().chain(["unaccepted/source.rs"]) {
            if path == owner { continue; }
            assert_eq!(strip_known_test_tail(&text, path), text,
                "each exact test tail must remain visible at foreign paths");
            assert!(production_source(&text, path).contains("cfg(test)"),
                "each exact test tail must remain visible at foreign paths");
            assert!(!production_feature_sites_are_closed(&text, path),
                "copied or swapped exact test tails must not gain source authority");
        }
    }
    assert!(production_feature_sites_are_closed(KNOWN_CLI_MAIN_SOURCE, MAIN_PATH));
    for path in SOURCE_PATHS.into_iter().chain(["unaccepted/source.rs"]) {
        if path == MAIN_PATH { continue; }
        assert!(!production_feature_sites_are_closed(KNOWN_CLI_MAIN_SOURCE, path),
            "exact main source must not gain authority at another path");
    }
}

'''
s=s.replace('fn feature_metadata_fixture(root: &Path) -> Value {',control+'fn feature_metadata_fixture(root: &Path) -> Value {')
(F/'next-source-r3/apps/cli/tests').mkdir(parents=True);(F/'next-source-r3/apps/cli/tests/doctor_tests.rs').write_text(s)
# All source installation and checks happen under the owning lane.
d=(F/'check_r7.py').read_text().replace("B = F/'owning-r7'","B = F/'owning-r8'").replace("prepared = json.loads((F/'PREPARED.json').read_text())","prepared = json.loads((F/'post-base-r2/report.json').read_text())").replace("(F/'owning-r6/report.json')","(F/'owning-r7/report.json')").replace("F/'next-source'/path","F/'next-source-r3'/path").replace("b'7 passed; 0 failed'","b'8 passed; 0 failed'").replace('doctorTests=7','doctorTests=8').replace('strip_known_test_tail(&text);','strip_known_test_tail(&text, path);')
d=d.replace("mutants=[\n", "mutants=[\n    ('source-site-binding-skipped', 'path == expected', 'true || path == expected', 'each exact test tail must remain visible at foreign paths'),\n")
d=d.replace("'--exact','doctor_feature_declarations_keep_the_accepted_opt_in_graph' if", "'--exact','accepted_source_exceptions_are_bound_to_their_exact_paths' if name == 'source-site-binding-skipped' else 'doctor_feature_declarations_keep_the_accepted_opt_in_graph' if")
d=d.replace('ALL7 DOCTOR TESTS/CLIPPY PASS;11COMPILED','ALL8 DOCTOR TESTS/CLIPPY PASS;12COMPILED')
(F/'check_r8.py').write_text(d)
print('Prepared path-aware source and owning-r8 driver; original R2 frozen unchanged')
