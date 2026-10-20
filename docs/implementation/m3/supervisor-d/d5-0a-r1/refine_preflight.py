from pathlib import Path
import json
F=Path(__file__).parent;Q=Path('/tmp/opensip-implementation/reviews/codex-d5-waits-preflight-r1');v=json.loads((Q/'review.json').read_text());assert v['verdict']=='REQUIRED-FINDINGS'
p=Path('/Users/sb/code/opensip-ai/opensip-d5-0-takeover/crates/components/src/supervisor_tests.rs');s=p.read_text()
s=s.replace("/// D5-0's outer cap: the largest retained wait plus drain and reap ceilings.","/// The outer cap retains the trigger, then sequential TERM, drain and reap budgets.\n/// Each term is an existing law wait; none is a new shortened duration.")
s=s.replace('        + waits.drain\n        + waits.reap_ceiling','        + waits.term_to_kill\n        + waits.drain\n        + waits.reap_ceiling')
s=s.replace('WALL_CLOCK_PROVIDER + DRAIN + REAP_CEILING','WALL_CLOCK_PROVIDER + TERM_TO_KILL + DRAIN + REAP_CEILING').replace('WALL_CLOCK_TOOL + DRAIN + REAP_CEILING','WALL_CLOCK_TOOL + TERM_TO_KILL + DRAIN + REAP_CEILING')
# The max can be the trigger, so TERM is a sequential phase, not only a competing maximum.
needle='    for (waits, field) in ['
s=s.replace(needle,'''    let deadline_then_escalation = Waits::TOOL.wall_clock + TERM_TO_KILL + REAP_CEILING;
    assert!(control_cap(Waits::TOOL) > deadline_then_escalation);
    assert_eq!(control_cap(Waits::TOOL) - deadline_then_escalation, DRAIN);
    for (waits, field) in [''',1)
# Every sampled hang must prove its shortened trigger, not simply sample facts.
needle='''        wall_clock_expiry_waits(),
    );
    let incomplete: Vec<_>'''
assert s.count(needle)==1;s=s.replace(needle,'''        wall_clock_expiry_waits(),
    );
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    let incomplete: Vec<_>''')
needle='''        wall_clock_expiry_waits(),
    );
    assert_eq!(
        out.facts'''
assert s.count(needle)==1;s=s.replace(needle,'''        wall_clock_expiry_waits(),
    );
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert_eq!(
        out.facts''')
# Both direct cancel-write loops need to have reached the chosen wall deadline.
needle='''    supervision.seams.control_bytes_left = Some(3);''';assert s.count(needle)==1;s=s.replace(needle,'''    assert!(events.borrow().iter().any(|(_, e)| {
        *e == SupervisionEvent::WaitExpired(BoundedWait::WallClock)
    }));
    supervision.seams.control_bytes_left = Some(3);''')
needle='''    supervision.seams.control_write_fails = true;''';assert s.count(needle)==1;s=s.replace(needle,'''    assert!(events.borrow().iter().any(|(_, e)| {
        *e == SupervisionEvent::WaitExpired(BoundedWait::WallClock)
    }));
    supervision.seams.control_write_fails = true;''')
# The native provider-bound scenario bypasses tool_deadline_run: observe it explicitly.
needle='''        supervision.seams.process_count_off = true;
        let mut root = root_in(&dir);'''
# This exact code exists only in provider-bound control.
assert s.count(needle)==1;s=s.replace(needle,'''        supervision.seams.process_count_off = true;
        let observed: Rc<RefCell<Vec<SupervisionEvent>>> = Rc::default();
        let sink = Rc::clone(&observed);
        supervision.observer = Some(Box::new(move |event| sink.borrow_mut().push(event.clone())));
        let mut root = root_in(&dir);''')
needle='''        let settlement = supervision.take_settlement().expect("settlement");
        assert!(matches!(settlement.exit(), ExitClass::Signaled(9)));''';assert s.count(needle)==1;s=s.replace(needle,'''        let settlement = supervision.take_settlement().expect("settlement");
        assert!(observed.borrow().contains(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
        assert!(matches!(settlement.exit(), ExitClass::Signaled(9)));''')
p.write_text(s)
