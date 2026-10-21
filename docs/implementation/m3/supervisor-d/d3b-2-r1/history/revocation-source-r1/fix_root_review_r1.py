from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor.rs';s=p.read_text();a='''        let started = self.stage1.map(|s| s.started).or(self.normal_end_signal);''';assert s.count(a)==1;s=s.replace(a,'''        let normal_end_force = self.normal_end_signal.is_some() && self.stage1.is_none();
'''+a);a='''        self.queue_control_cancel(reason);
        if let (Some(trigger), Some(at)) = (forced, started) {''';assert s.count(a)==1;s=s.replace(a,'''        // A normal-end signal never creates a cancellation leg. Preserve
        // its already-logically-queued shutdown behind any older frame.
        if !normal_end_force { self.queue_control_cancel(reason); }
        if let (Some(trigger), Some(at)) = (forced, started) {''')
start=s.index('        if let Some(stage1) = self.stage1.filter(|s| s.active)',s.index('    fn timers(&mut self)'))
end=s.index('        let Some(spawned) = self.spawned_at else {',start)
s=s[:start]+'        self.stage1_timers(now);\n'+s[end:]
idx=s.index('    /// Fire every expired wait')
s=s[:idx]+'''    /// At a delayed wake, consume the earliest pending Stage1 deadline
    /// from one snapshot. A prior fault must not be erased by later grace
    /// expiry; ties also prefer faults. Consuming it deactivates Stage1,
    /// so no later grace-expired force can be manufactured in this turn.
    fn stage1_timers(&mut self, now: Instant) {
        let Some(stage1) = self.stage1.filter(|s| s.active) else { return; };
        let Some(protocol) = self.protocol else { return; };
        let mut due = Vec::with_capacity(4);
        if let Some(spawned) = self.spawned_at {
            if !self.handshake_done { due.push((spawned + self.waits.handshake, BoundedWait::Handshake)); }
            if self.terminal.is_none() { due.push((spawned + self.waits.wall_clock, BoundedWait::WallClock)); }
        }
        if let Some(at) = self.health_due { due.push((at, BoundedWait::LivenessWindow)); }
        due.push((stage1.started + protocol.stage1_cancel_grace, BoundedWait::Stage1CancelGrace));
        let Some((_, wait)) = due.into_iter().filter(|(at,_)| now >= *at)
            .min_by_key(|(at,wait)| (*at, usize::from(*wait == BoundedWait::Stage1CancelGrace))) else { return; };
        self.append(SupervisionEvent::WaitExpired(wait));
        match wait {
            BoundedWait::Handshake => self.trigger(Cause::HandshakeDeadline),
            BoundedWait::WallClock => { self.trigger(Cause::Deadline); self.deliver(ProcessEvent::Fault(ProcessFault::Deadline)); }
            BoundedWait::LivenessWindow => {
                self.health_due = None;
                self.append(SupervisionEvent::LivenessMissed(LivenessMiss::WindowExpired));
                self.trigger(Cause::Liveness);
            }
            BoundedWait::Stage1CancelGrace => self.force_user_stage2(Some(opensip_operability::ForceTrigger::GraceExpired), CancelReason::User),
            _ => unreachable!("only the four pending Stage1 waits are collected"),
        }
    }

'''+s[idx:]
# Table companion owns the five exact SL S6 bounds.
start=s.index('fn revocation_bound(');end=s.index('struct RevocationTracking',start);s=s[:start]+'''fn revocation_bound(mark: opensip_operability::RevocationMark) -> Duration { mark.bound() }
'''+s[end:];p.write_text(s)
p=W/'crates/operability/src/kinds/registry.rs';s=p.read_text();a='''code_table!(ElapsedStatus, cap 64, {''';assert s.count(a)==1;s=s.replace(a,'''impl RevocationMark {
    /// SL S6:492-494. The mark observes its action; it never truncates it.
    pub const fn bound(self) -> std::time::Duration {
        std::time::Duration::from_secs(match self {
            Self::RequestsRefused => 0, Self::ProtocolCancel => 2,
            Self::Sigterm => 3, Self::KillAndReap => 5, Self::ScratchCleanup => 10,
        })
    }
}
'''+a);p.write_text(s)
F=Path(__file__).parent;s=(F/'revocation_lane_r1.py').read_text().replace("'revocation-r1'","'revocation-r2'");s=s.replace("('revocation-controls',[str(binary),'d3b2_revocation_']),", "('review-rf-controls',[str(binary),'d3b2_review_']),('all-d3b2-controls',[str(binary),'d3b2_']),");(F/'revocation_lane_r2.py').write_text(s)
print('Both root RF corrections applied, exact pre-fix runtime evidence preserved')
