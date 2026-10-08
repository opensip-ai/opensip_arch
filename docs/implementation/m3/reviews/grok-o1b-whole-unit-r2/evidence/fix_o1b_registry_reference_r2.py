from pathlib import Path
p=Path('/tmp/opensip-implementation/o1b-authoring-r1/product/crates/operability/src/kinds/registry_tests.rs');s=p.read_text();s=s.replace('BuildProfile, CapabilitySet, CodeEnum, CommitNotPublished, Event, HostRepairCompleted,','BuildProfile, CapabilitySet, CodeEnum, CommitNotPublished, Event, HostRepairCompleted, HostPhaseStarted, HostPhaseCompleted,').replace('PathAnchor, Phase,\n','PathAnchor, Phase, PhaseOutcome,\n',1)
s=s.replace('        Table {\n            name: "PathAnchor",','        Table { name: "PhaseOutcome", role: "code", cap: PhaseOutcome::CAP, members: PhaseOutcome::TEXT },\n        Table {\n            name: "PathAnchor",',1)
s=s.replace('    push_event::<StorageCommitNotPublished>(&mut out);','    push_event::<StorageCommitNotPublished>(&mut out);\n    out.push_str(",\\n");\n    push_event::<HostPhaseStarted>(&mut out);\n    out.push_str(",\\n");\n    push_event::<HostPhaseCompleted>(&mut out);',1)
s=s.replace('    push_markdown_event::<StorageCommitNotPublished>(&mut out);','    push_markdown_event::<StorageCommitNotPublished>(&mut out);\n    push_markdown_event::<HostPhaseStarted>(&mut out);\n    push_markdown_event::<HostPhaseCompleted>(&mut out);',1)
s=s.replace(r'\n    {\"name\": \"ring\",',r'\n    {\"name\": \"harness\", \"classes\": [\"P0\", \"P1\"]},\n    {\"name\": \"ring\",',1)
s=s.replace(r'\n- ring: P0, P1',r'\n- harness: P0, P1\n- ring: P0, P1',1)
s+='''
// Independent completeness control against declarations in the unexpanded
// registry, rather than only comparing files with a manually enumerated renderer.
fn quoted_values<'a>(text: &'a str, marker: &str) -> std::collections::BTreeSet<&'a str> {
    text.split(marker).skip(1).map(|tail| tail.split('"').next().unwrap()).collect()
}
fn reference_is_complete(source: &str, json: &str, markdown: &str) -> bool {
    let mut events = quoted_values(source, "name: \\\"");
    events.extend(quoted_values(source, "const NAME: &'static str = \\\""));
    for tail in source.split("loss_event!(").skip(1) {
        if let Some((_, name)) = tail.split_once(", \\\"") { events.insert(name.split('"').next().unwrap()); }
    }
    let declared_tables: std::collections::BTreeSet<_> = source.split("code_table!(").skip(1)
        .map(|tail| tail.split(',').next().unwrap().trim()).collect();
    let json_events = quoted_values(json.split("\\\"codeTables\\\"").next().unwrap(), "\\\"name\\\": \\\"");
    let Some((_, table_section)) = json.split_once("\\\"codeTables\\\"") else { return false; };
    let json_tables = quoted_values(table_section.split("\\\"retired\\\"").next().unwrap(), "\\\"name\\\": \\\"");
    let md_events: std::collections::BTreeSet<_> = markdown.split("### `").skip(1)
        .map(|tail| tail.split('`').next().unwrap()).collect();
    let Some((_, md_tables)) = markdown.split_once("## Code tables") else { return false; };
    let md_tables: std::collections::BTreeSet<_> = md_tables.split("## Retired").next().unwrap()
        .split("### ").skip(1).map(|tail| tail.lines().next().unwrap()).collect();
    events == json_events && events == md_events && declared_tables == json_tables && declared_tables == md_tables
        && json.contains("{\\\"name\\\": \\\"harness\\\", \\\"classes\\\": [\\\"P0\\\", \\\"P1\\\"]}")
        && markdown.contains("- harness: P0, P1\\n")
}

#[test]
fn reference_covers_every_declared_event_table_and_the_bound_harness_sink() {
    let source = include_str!("registry.rs");
    let json = render_json(); let markdown = render_markdown();
    assert!(reference_is_complete(source, &json, &markdown));
    for omitted in ["host.phase.started", "host.phase.completed", "PhaseOutcome", "harness"] {
        let missing_json = json.replace(omitted, "omitted");
        assert!(!reference_is_complete(source, &missing_json, &markdown), "JSON omission escaped: {omitted}");
        let missing_markdown = markdown.replace(omitted, "omitted");
        assert!(!reference_is_complete(source, &json, &missing_markdown), "Markdown omission escaped: {omitted}");
    }
}
'''
p.write_text(s)
