import unittest
from reference import Candidate,FileEvent,Field,Bound,GIB,replay_acquisition,final_population,final_overflow

def c(name,events,admitted=True,activated=True):
    return Candidate((name,"1.0.0","registry+declared"),tuple(FileEvent(*e) for e in events),admitted,activated)
class Controls(unittest.TestCase):
    def test_protocol_boundary_is_not_an_acquisition_shortcut(self):
        values=[c("a",[(1,8*GIB+1)])]
        self.assertEqual(replay_acquisition(values),(1,1,8*GIB+1))
        self.assertEqual(final_overflow(values),(Bound(Field.CONTENT,8*GIB+1,8*GIB),))
    def test_inactive_and_late_rejected_still_count_acquisition(self):
        for admitted,activated in [(True,False),(False,True),(False,False)]:
            values=[c("a",[(1,8*GIB+1)],admitted,activated)]
            self.assertEqual(replay_acquisition(values),(1,1,8*GIB+1))
            self.assertEqual(final_population(values),(0,0,0))
            self.assertEqual(final_overflow(values),())
    def test_file_overflow_is_final_only_for_selected_admitted(self):
        for admitted,activated in [(True,True),(True,False),(False,True)]:
            values=[c("a",[(1_000_001,0)],admitted,activated)]
            self.assertEqual(replay_acquisition(values),(1,1_000_001,0))
            self.assertEqual(bool(final_overflow(values)),admitted and activated)
    def test_exact_acquisition_bound_then_one_more(self):
        values=[c("a",[(4_000_000,8*1024)])]
        self.assertEqual(replay_acquisition(values),(1,4_000_000,4_000_000*8*1024))
        # Content at32GiB exactly, independently of the file count.
        self.assertEqual(replay_acquisition([c("a",[(1,32*GIB)])]),(1,1,32*GIB))
        self.assertEqual(replay_acquisition([c("a",[(1,32*GIB),(1,0)])]),(1,2,32*GIB))
        self.assertEqual(replay_acquisition([c("a",[(1,32*GIB),(1,1)])]),Bound(Field.CONTENT,32*GIB+1,32*GIB))
    def test_same_file_crossing_prefers_files(self):
        values=[c("a",[(4_000_000,0),(1,32*GIB+1)])]
        self.assertEqual(replay_acquisition(values),Bound(Field.FILES,4_000_001,4_000_000))
    def test_canonical_candidate_order_controls_first_field(self):
        values=[c("a",[(1,8*GIB)]),c("b",[(1,8*GIB)]),c("c",[(1,8*GIB)]),c("d",[(1,8*GIB)]),c("e",[(1_000_000,1)]),c("f",[(1_000_000,1)]),c("g",[(1_000_000,1)]),c("h",[(1_000_000,1)])]
        expected=Bound(Field.CONTENT,32*GIB+1,32*GIB)
        for shifted in [values,values[::-1],values[3:]+values[:3]]:
            self.assertEqual(replay_acquisition(shifted),expected)
    def test_canonical_file_candidates_can_cross_files_first(self):
        values=[c(f"a{i}",[(1_000_000,1)]) for i in range(4)]+[c(f"z{i}",[(1,8*GIB)]) for i in range(4)]
        for supplied in [values,values[::-1],values[4:]+values[:4]]:
            self.assertEqual(replay_acquisition(supplied),Bound(Field.FILES,4_000_001,4_000_000))
    def test_source_boundary_precedes_any_file_event(self):
        values=[c(f"p{i:05}",[]) for i in range(16384)]+[c("z",[(4_000_001,32*GIB+1)])]
        self.assertEqual(replay_acquisition(values),Bound(Field.SOURCES,16385,16384))
    def test_final_fields_remain_distinct_without_invented_precedence(self):
        values=[c("a",[(1,8*GIB+1),(1_000_000,0)])]
        self.assertEqual(replay_acquisition(values),(1,1_000_001,8*GIB+1))
        self.assertEqual({b.field for b in final_overflow(values)},{Field.FILES,Field.CONTENT})
    def test_declaration_errors_grant_nothing(self):
        with self.assertRaises(ValueError):replay_acquisition([c("a",[]),c("a",[])])
        for events in [[(-1,0)],[(1,-1)],[(False,0)],[(1,1.0)]]:
            with self.assertRaises(ValueError):replay_acquisition([c("a",events)])
            with self.assertRaises(ValueError):final_population([c("a",events)])
    def test_utf8_tuple_order_uses_version_then_source(self):
        a=Candidate(("same","1","é"),(FileEvent(1,32*GIB),),True,True)
        b=Candidate(("same","2","a"),(FileEvent(4_000_001,0),),True,True)
        # Version controls ordering before source bytes.
        for supplied in [(a,b),(b,a)]:
            self.assertEqual(replay_acquisition(supplied),Bound(Field.FILES,4_000_001,4_000_000))
        a=Candidate(("same","1","é"),(FileEvent(4_000_001,0),),True,True)
        b=Candidate(("same","1","z"),(FileEvent(1,32*GIB+1),),True,True)
        # UTF-8 z sorts before the multibyte é source component.
        for supplied in [(a,b),(b,a)]:
            self.assertEqual(replay_acquisition(supplied),Bound(Field.CONTENT,32*GIB+1,32*GIB))
    def test_final_package_and_source_exact_boundaries(self):
        values=[c(f"p{i:05}",[]) for i in range(16384)]
        self.assertEqual(replay_acquisition(values),(16384,0,0))
        self.assertEqual(final_overflow(values[:4096]),())
        self.assertEqual(final_overflow(values[:4097]),(Bound(Field.SOURCES,4097,4096),))
    def test_exact_protocol_files_and_content_without_truncation(self):
        values=[c("a",[(1,8*GIB),(999999,0),(0,10**30)])]
        self.assertEqual(final_population(values),(1,1_000_000,8*GIB))
        self.assertEqual(final_overflow(values),())
        self.assertEqual(replay_acquisition(values),(1,1_000_000,8*GIB))
if __name__=="__main__":unittest.main()
