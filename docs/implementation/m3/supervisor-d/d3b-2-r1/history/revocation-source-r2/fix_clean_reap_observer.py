from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor.rs';s=p.read_text()
def one(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,b)
one('''        if self.first_cause.is_none() && ended && self.death_appended {
            self.first_cause = Some(Cause::Clean);
            self.clean_at = Some(Instant::now());
            self.state = State::Reaping;
        }''','''        if self.first_cause.is_none() && ended && self.death_appended {
            // This join is provisional while the gate is open. An observer
            // consumed during a held reap must still be the first teardown
            // cause. Mint Clean only when this reap can actually settle.
            self.clean_at.get_or_insert_with(Instant::now);
            self.state = State::Reaping;
        }''')
one('''        if self.state == State::Settled || self.first_cause.is_none() {
            return;
        }
        if self.ladder.is_some() {''','''        if self.state == State::Settled || (self.first_cause.is_none() && self.clean_at.is_none()) {
            return;
        }
        if self.ladder.is_some() {''')
one('''        let ladder_done = self.ladder.is_none_or(|l| l.kill_at.is_some())
            || self.first_cause == Some(Cause::Clean);''','''        let ladder_done = self.ladder.is_none_or(|l| l.kill_at.is_some());''')
one('''        let mut cause = self.first_cause.unwrap_or(Cause::Abandoned);''','''        let mut cause = self.first_cause.unwrap_or(if self.clean_at.is_some() { Cause::Clean } else { Cause::Abandoned });''')
# An already-cancelled cooperative join also holds a provisional reap;
# later faults retain its immutable UserCancel cause but still own cleanup.
one('''        if let Some(observed) = observed
            && !self.observer_seen''','''        if cause != Cause::UserCancel && self.clean_at.take().is_some() && self.ladder.is_none() && self.child.is_some() {
            self.ladder = Some(Ladder {
                t1_done: from_t2 || self.class == Class::Tool,
                reason: if cause == Cause::Deadline { CancelReason::Deadline } else { CancelReason::SupervisorFault },
                term_at: None, kill_at: None,
            });
        }
        if let Some(observed) = observed
            && !self.observer_seen''')
# Clearing the provisional deadline prevents an older clean-reap timer
# from pre-empting a newly forced cancellation ladder.
one('''        self.normal_end_signal = None;
        if let Some(participant) = &mut self.participant {''','''        self.normal_end_signal = None;
        self.clean_at = None;
        if let Some(participant) = &mut self.participant {''')
one('''        let settlement = Settlement {
            first_cause: cause,''','''        self.first_cause = Some(cause);
        let settlement = Settlement {
            first_cause: cause,''')
p.write_text(s)
F=Path(__file__).parent;s=(F/'marks_lane_r1.py').read_text().replace("'marks-r1'","'marks-r2'");s=s.replace("('new-mark-controls',[str(binary),'d3b2_marks_']),", "('clean-reap-review-controls',[str(binary),'d3b2_clean_reap_']),");(F/'marks_lane_r2.py').write_text(s)
print('Provisional clean join defers final Clean; consumed observer owns its required ladder')
