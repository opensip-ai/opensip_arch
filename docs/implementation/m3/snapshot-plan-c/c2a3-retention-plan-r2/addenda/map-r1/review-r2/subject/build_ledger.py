"""Build CALL-TREE.json and LEDGER.json for the C2a-3 map/local/slot price addendum r1.

Same node format and cost rule as the accepted funding-price-r3 checker: a call
costs ceil(2*argumentBytes/64) + ceil(2*resultBytes/64) plus its body; a
primitive costs its visits; a ref costs its definition. A move of a w-byte value
that is not a call argument or result is a `move` primitive of ceil(2w/64)
visits. Accepted funding-r3 definitions are imported by value (pinned by hash).
Where a later SOURCE-AUDIT scoped model counted the same route higher, its
count is used as an `inherited` primitive naming its subject manifest.
"""
from pathlib import Path
import hashlib, json

B = Path(__file__).parent
FUND = B / 'FUNDING-R3-CALL-TREE.json'
FUND_SHA = '3bd71196fa33873bf25085a9047466ac8ad33826b2afa527ac4a088b237abb9a'
assert hashlib.sha256(FUND.read_bytes()).hexdigest() == FUND_SHA
D = dict(json.loads(FUND.read_text())['definitions'])
IMPORTED = sorted(D)


def call(name, arg, res, *body):
    return {'kind': 'call', 'name': name, 'argumentBytes': arg, 'resultBytes': res, 'body': list(body)}


def prim(name, visits=1):
    return {'kind': 'primitive', 'name': name, 'visits': visits}


def move(name, width):
    return {'kind': 'primitive', 'name': f'move {width}-byte {name}', 'visits': (2 * width + 63) // 64, 'moveBytes': width}


def inherited(name, visits, subject, note):
    return {'kind': 'primitive', 'name': name, 'visits': visits, 'inheritedFrom': subject, 'note': note}


def ref(name):
    assert name in D, name
    return {'kind': 'ref', 'name': name}


def define(name, node):
    assert name not in D, name
    D[name] = node


# Audited scoped subjects whose counts are inherited (control continuation r272 CURRENT.json).
BLOB_ITER_R2 = 'local-blob-iterator-source-r2 c76cfba6c26b314de17426b9a25fc8569f3bb479f873f9e7ae3ebb379c02aada SOURCE-AUDIT'
ZIP_LOOPS_R1 = 'local-zip-loops-source-r1 6f3f58a5e6c38a1cb7ab02be6112b07128d4739cd4ef94e9a0373cc0237aa893 SOURCE-AUDIT'

# ---- assert_unsafe_precondition! expansion (check_language_ub / check_library_ub) ----
define('ub_kind', call('check_{language,library}_ub kind query', 0, 1,
                       prim('intrinsics::ub_checks'),
                       call('const_eval_select runtime arm', 0, 1, prim('literal true')),
                       prim('and')))


def precondition(name, arg, *predicate):
    return call(f'assert_unsafe_precondition {name}', 0, 0,
                ref('ub_kind'), prim('kind branch'),
                call(f'{name} precondition_check', arg, 0, *predicate, prim('negated predicate branch to panic_nounwind')))


# ---- small shared std leaves ----
define('layout_size', call('Layout::size', 8, 8, prim('load size field')))
define('alignment_as_usize', call('Alignment::as_usize', 8, 8,
                                  call('Alignment::as_nonzero', 8, 8, prim('transmute to NonZero<usize>')),
                                  call('NonZero<usize>::get', 8, 8, prim('transmute to usize'))))
define('layout_align', call('Layout::align', 8, 8, ref('alignment_as_usize')))
define('layout_alignment', call('Layout::alignment', 8, 8, prim('load align field')))
define('cap_as_inner', call('UsizeNoHighBit::as_inner', 8, 8, prim('transmute')))
define('cap_new_unchecked', call('UsizeNoHighBit::new_unchecked', 8, 8, prim('transmute')))
define('ptr_is_null', call('pointer::is_null', 8, 1, prim('address compare with null')))
define('is_power_of_two', call('usize::is_power_of_two', 8, 1, prim('count_ones'), prim('== 1')))
define('nonnull_as_ptr', call('NonNull::as_ptr', 8, 8, prim('transmute')))
define('option_is_some', call('Option::is_some', 8, 1, prim('match tag')))
define('vec_len', call('Vec::len', 8, 8, prim('load len'), prim('T::MAX_SLICE_LEN query'),
                       prim('len <= MAX_SLICE_LEN'), prim('intrinsics::assume')))
define('max_size_for_alignment', call('Layout::max_size_for_alignment', 8, 8,
                                      ref('alignment_as_usize'), prim('isize::MAX as usize + 1'), prim('unchecked_sub')))
define('size_alignment_valid', call('Layout::is_size_alignment_valid', 16, 1,
                                    ref('max_size_for_alignment'), prim('size <= max')))
define('alignment_new', call('Alignment::new', 8, 16, ref('is_power_of_two'), prim('branch'),
                             call('Alignment::new_unchecked', 8, 8,
                                  precondition('Alignment::new_unchecked', 8, ref('is_power_of_two')),
                                  prim('transmute')),
                             prim('Some tag'), prim('Some payload')))
define('size_align_valid', call('Layout::is_size_align_valid', 16, 1, ref('alignment_new'),
                                prim('let-else match'), ref('size_alignment_valid')))
define('from_size_align_unchecked', call('Layout::from_size_align_unchecked', 16, 16,
                                         precondition('Layout::from_size_align_unchecked', 16, ref('size_align_valid')),
                                         prim('transmute align'), prim('construct size field'), prim('construct align field')))
define('unchecked_mul', call('usize::unchecked_mul', 16, 8,
                             precondition('unchecked_mul', 16, prim('overflowing_mul'), prim('negate overflow flag')),
                             prim('intrinsics::unchecked_mul')))
define('nonnull_new_unchecked', call('NonNull::new_unchecked', 8, 8,
                                     precondition('NonNull::new_unchecked', 8, ref('ptr_is_null'), prim('not')),
                                     prim('transmute')))
define('raw_add_debug_guard', inherited(
    'raw *mut T::add debug runtime_add_nowrap precondition chain', 65, BLOB_ITER_R2,
    'debug constructor 143 minus release constructor 78: the raw mut pointer add guard chain'))
define('raw_mut_add', call('*mut T::add', 16, 8, ref('raw_add_debug_guard'), prim('intrinsics::offset')))
define('aligned_and_not_null', call('ub_checks::maybe_is_aligned_and_not_null', 17, 1,
                                    ref('ptr_is_null'), prim('not'), prim('is_zst branch'),
                                    call('ub_checks::maybe_is_aligned', 17, 1, prim('is_zst branch'),
                                         call('pointer::is_aligned_to', 16, 1, ref('is_power_of_two'), prim('panic branch'),
                                              prim('addr'), prim('align - 1'), prim('and'), prim('== 0'))),
                                    prim('and')))


def ptr_write(width):
    return call(f'ptr::write {width}-byte T', 8 + width, 0,
                precondition('ptr::write', 17, prim('align_of query'), prim('IS_ZST query'), ref('aligned_and_not_null')),
                move('value by intrinsics::write_via_move', width))


# ---- Vec<T>::with_capacity(n), selected nonzero-layout allocation route (dominates the zero-layout route) ----
define('layout_array', call('raw_vec::layout_array', 24, 24,
                            ref('layout_size'),
                            call('Layout::pad_to_align', 8, 16,
                                 call('Layout::size_rounded_up_to_custom_alignment', 16, 8,
                                      prim('load align field argument'), ref('alignment_as_usize'),
                                      prim('intrinsics::unchecked_sub'), prim('load size'),
                                      prim('intrinsics::unchecked_add'), prim('not mask'), prim('and')),
                                 ref('layout_alignment'),
                                 call('Layout::from_size_alignment_unchecked', 16, 16,
                                      precondition('Layout::from_size_alignment_unchecked', 16, ref('size_alignment_valid')),
                                      prim('construct size'), prim('construct align'))),
                            ref('layout_size'), prim('debug_assert size equality'), prim('debug_assert branch'),
                            call('Layout::repeat_packed', 24, 24,
                                 prim('checked_mul including Option output'), prim('let-Some match'),
                                 call('Layout::from_size_alignment', 16, 24, ref('size_alignment_valid'),
                                      prim('branch'), prim('construct size'), prim('construct align'), prim('Ok tag'))),
                            prim('match Ok'), prim('Ok tag'), prim('Ok payload')))
define('alloc_runtime', call('Global::alloc_impl_runtime', 17, 24,
                             ref('layout_size'), prim('match size'), prim('zeroed branch'),
                             call('alloc::alloc', 16, 8,
                                  call('__rust_no_alloc_shim_is_unstable_v2', 0, 0,
                                       prim('external shim body: trusted allocator boundary, unpriced')),
                                  ref('layout_size'), ref('layout_alignment'),
                                  call('__rust_alloc', 16, 8,
                                       prim('external allocator body: trusted allocator boundary, unpriced'))),
                             call('NonNull::new', 8, 16, ref('ptr_is_null'), prim('not'), prim('branch'),
                                  ref('nonnull_new_unchecked'), prim('Some tag')),
                             call('Option::ok_or', 16, 16, prim('match tag'), prim('Ok tag'), prim('Ok payload')),
                             ref('try_success'),
                             call('NonNull::slice_from_raw_parts', 16, 16, ref('nonnull_as_ptr'),
                                  call('ptr::slice_from_raw_parts_mut', 16, 16, prim('aggregate raw slice')),
                                  ref('nonnull_new_unchecked')),
                             prim('Ok tag'), prim('Ok payload')))
define('global_allocate', call('Global::allocate', 24, 24,
                               call('Global::alloc_impl', 25, 24,
                                    call('const_eval_select (layout, zeroed)', 17, 24, ref('alloc_runtime')))))
define('needs_to_grow', call('RawVecInner::needs_to_grow', 40, 1,
                             call('RawVecInner::capacity', 16, 8, prim('elem_size == 0'), prim('branch'), ref('cap_as_inner')),
                             ref('layout_size'), prim('wrapping_sub'), prim('additional > remaining')))
define('vec_with_capacity', call('Vec::with_capacity', 8, 24,
                                 call('Vec::with_capacity_in', 8, 24,
                                      call('RawVec::with_capacity_in', 8, 16, prim('T::LAYOUT const query'),
                                           call('RawVecInner::with_capacity_in', 24, 16,
                                                call('RawVecInner::try_allocate_in', 32, 24,
                                                     ref('layout_array'), prim('match layout result'),
                                                     ref('layout_size'), prim('size == 0'), prim('branch'),
                                                     prim('match AllocInit'), ref('global_allocate'),
                                                     prim('match allocation result'), prim('bind ptr'),
                                                     call('NonNull<[u8]>::cast', 16, 8, prim('cast')),
                                                     call('Unique::from(NonNull)', 8, 8, prim('construct pointer'), prim('construct PhantomData')),
                                                     ref('cap_new_unchecked'),
                                                     prim('construct ptr'), prim('construct cap'), prim('construct alloc ZST'),
                                                     prim('Ok tag')),
                                                prim('match Ok'), ref('needs_to_grow'), prim('not'),
                                                call('hint::assert_unchecked', 1, 0,
                                                     precondition('hint::assert_unchecked', 1, prim('cond')),
                                                     prim('intrinsics::assume')),
                                                prim('return this')),
                                           prim('construct inner'), prim('construct PhantomData')),
                                      prim('construct buf'), prim('construct len 0'))))


# ---- Vec<T>::push without growth (with_capacity reserved exactly the pushed count) ----
def vec_push(width, label):
    return call(f'Vec<{label}>::push', 8 + width, 0,
                call(f'Vec<{label}>::push_mut', 8 + width, 8,
                     prim('load len'), prim('bind len'),
                     call('RawVec::capacity', 8, 8, prim('size_of::<T> query'),
                          call('RawVecInner::capacity', 16, 8, prim('elem_size == 0'), prim('branch'), ref('cap_as_inner'))),
                     prim('len == capacity'), prim('branch (no growth on the selected route)'),
                     call('Vec::as_mut_ptr', 8, 8, ref('raw_ptr')),
                     ref('raw_mut_add'), prim('bind end'),
                     ptr_write(width),
                     prim('len + 1'), prim('store len'), prim('&mut *end')),
                prim('discard let _ = &mut T'))


# ---- RawVec deallocation and Vec drop glue ----
define('current_memory', call('RawVecInner::current_memory', 24, 32,
                              ref('layout_size'), prim('elem size == 0'), ref('cap_as_inner'), prim('cap == 0'), prim('or branch'),
                              ref('layout_size'), ref('cap_as_inner'), ref('unchecked_mul'),
                              ref('layout_align'), ref('from_size_align_unchecked'),
                              call('NonNull::from(Unique)', 8, 8, prim('field')),
                              prim('Some tag'), move('(NonNull, Layout) payload', 24)))
define('inner_deallocate', call('RawVecInner::deallocate', 24, 0,
                                ref('current_memory'), prim('if-let match'), prim('bind ptr and layout'),
                                call('Global::deallocate', 32, 0,
                                     call('Global::deallocate_impl', 32, 0,
                                          call('const_eval_select (ptr, layout)', 24, 0,
                                               call('Global::deallocate_impl_runtime', 24, 0,
                                                    ref('layout_size'), prim('size != 0'), ref('nonnull_as_ptr'),
                                                    call('alloc::dealloc', 24, 0, ref('layout_size'), ref('layout_alignment'),
                                                         call('__rust_dealloc', 24, 0,
                                                              prim('external deallocator body: trusted allocator boundary, unpriced')))))))))
define('rawvec_drop', call('drop_in_place::<RawVec<T>>', 8, 0,
                           call('<RawVec<T> as Drop>::drop', 8, 0, prim('T::LAYOUT const query'), ref('inner_deallocate'))))


def vec_drop_glue(label, element_glue):
    """drop_in_place::<Vec<T>>: Vec's Drop over its raw element slice, then RawVec's.

    The per-element loop body is `element_glue`; its count is the caller's row."""
    return call(f'drop_in_place::<Vec<{label}>>', 8, 0,
                call(f'<Vec<{label}> as Drop>::drop', 8, 0,
                     call('Vec::as_mut_ptr', 8, 8, ref('raw_ptr')), prim('load len'),
                     call('ptr::slice_from_raw_parts_mut', 16, 16, prim('aggregate raw slice')),
                     call(f'drop_in_place::<[{label}]>', 16, 0, prim('loop init'), prim('terminal compare'),
                          *element_glue)),
                ref('rawvec_drop'), prim('len field: no glue'))


define('u8_vec_drop', vec_drop_glue('u8', [prim('u8 has no glue: empty slice loop')]))
define('tuple_element_drop', call('per element of drop_in_place::<[(&str, Vec<u8>)]>', 0, 0,
                                  prim('index compare'), prim('element pointer add'), prim('index increment'),
                                  call('drop_in_place::<(&str, Vec<u8>)>', 8, 0, prim('&str field: no glue'),
                                       ref('u8_vec_drop'))))

# ---- per-Blob local work (one successful Blob of the first and only loop) ----
define('m_iteration', inherited('first-loop scaffold per Blob (Map::next Some 110 plus loop controls)', 115, ZIP_LOOPS_R1,
                                'debug-source caller scaffold first115F+190, excluding the loop body'))
define('collector_new', call('Collector construction', 0, 0,
                             ref('vec_with_capacity'), prim('write expected'), move('Vec<u8> header into collector', 24),
                             prim('write begun false'), prim('write finished false'), prim('write fault None tag')))
define('transfer_boundary', call('RetainedTree::transfer call boundary (body is CI transfer T)', 40, 8,
                                 prim('bind transfer result')))
define('begin_body', call('Collector::begin (state and length only)', 48, 0,
                          ref('option_is_some'), prim('fault branch'), prim('load begun'), prim('load finished'),
                          prim('load expected'), prim('usize as u64'), prim('length != expected'), prim('or branch'),
                          prim('store begun')))
define('finish_body', call('Collector::finish(true)', 9, 0,
                           ref('option_is_some'), prim('fault branch'), prim('not begun'), prim('load finished'),
                           prim('not verified'), ref('vec_len'), prim('load expected'), prim('len != expected'),
                           prim('or branch'), prim('store finished')))
define('into_verified', call('Collector::into_verified', 42, 32,
                             prim('fault tag test'), prim('branch'), prim('not begun'), prim('not finished'),
                             ref('vec_len'), prim('load expected'), prim('len != expected'), prim('or branch'),
                             prim('Ok tag'), move('Vec<u8> header into Ok', 24), prim('remaining fields: no glue')))
define('map_err_vec', call('Result<Vec<u8>, CollectorFault>::map_err Ok', 32, 32,
                           prim('match tag'), prim('Ok tag'), move('Vec<u8> header', 24), prim('unused closure: no glue')))
define('try_vec', call('Result<Vec<u8>, Failure> Try::branch Ok and caller bind', 32, 32,
                       prim('match tag'), prim('Continue tag'), move('Vec<u8> header', 24),
                       prim('caller match Continue'), move('Vec<u8> header into binding', 24)))
define('push_tuple', vec_push(40, '(&str, Vec<u8>)'))
define('per_blob_local', call('per-Blob local work', 0, 0,
                              ref('m_iteration'), ref('length'), ref('collector_new'),
                              ref('blob_path'), prim('bind path'),
                              ref('transfer_boundary'), ref('map_err_ok'), ref('try_success'),
                              ref('begin_body'), ref('finish_body'),
                              ref('into_verified'), ref('map_err_vec'), ref('try_vec'),
                              prim('construct tuple path'), move('Vec<u8> header into tuple', 24),
                              ref('push_tuple'),
                              ref('tuple_element_drop')))

# ---- per-component fixed local work, charged by the new constant debit at admit_component_inner's top ----
RT, ADM = 256, 264  # native size_of RetainedTree and AdmittedComponent (proto build; published by G-4)
define('open_boundary', call('open_retained_tree call boundary (body is CI B_open)', 65, RT + 8,
                             prim('bind open result')))
define('map_err_tree_ok', call('Result<RetainedTree, TreeReadFailure>::map_err(tree_input) Ok', RT + 8, RT + 8,
                               prim('match tag'), prim('Ok tag'), move('RetainedTree', RT)))
define('try_tree', call('Try::branch Ok RetainedTree and caller bind', RT + 8, RT + 8,
                        prim('match tag'), prim('Continue tag'), move('RetainedTree', RT),
                        prim('caller match Continue'), move('RetainedTree into binding', RT)))
define('fund_first_debit', call('fund_representation entry and first constant debit (funding-r3 bootstrap, now paid)', 0, 0,
                                call('fund_representation argument transport', 16, 0),
                                prim('construct first WorkCost', 3), ref('meter_call')))
define('kernel_boundary', call('verify_retained_tree call boundary (body is K)', 48, 8, prim('bind result')))
define('outer_drop', call('core::mem::drop(retained_bytes)', 24, 0,
                          prim('drop glue dispatch at end of drop body'),
                          vec_drop_glue('(&str, Vec<u8>)', [])))
define('component_return', call('Ok(AdmittedComponent { candidate, retained })', 0, 0,
                                prim('candidate field'), move('RetainedTree into AdmittedComponent', RT), prim('Ok tag'),
                                call('admit_component_inner result transport', 0, ADM + 8)))
define('component_fixed_local', call('per-component fixed local work', 0, 0,
                                     ref('open_boundary'), ref('map_err_tree_ok'), ref('try_tree'),
                                     ref('fund_first_debit'),
                                     ref('vec_with_capacity'), prim('bind retained_bytes'),
                                     inherited('first-loop fixed scaffold (constructor, IntoIterator, final None, controls)',
                                               190, ZIP_LOOPS_R1, 'debug-source caller scaffold first115F+190'),
                                     call('AuthenticatedComponent::body', 8, 16, prim('load body field')), prim('bind body'),
                                     ref('kernel_boundary'), ref('map_err_ok'), ref('try_success'),
                                     ref('outer_drop'), ref('component_return')))

# ---- operation frame: AdmittedSet::prepare_slots and AdmittedSet::admit (G-3) ----
SC = 128
define('slot_fill_iteration', call('one slot fill: while slots.len() < count { slots.push(None) }', 0, 0,
                                   ref('vec_len'), prim('len < count'), prim('loop branch'),
                                   prim('construct None tag'), vec_push(SC, 'Option<ClosureCandidate>')))
D['slot_fill_iteration']['body'].append({'kind': 'ref', 'name': 'slot_element_drop'})
define('prepare_fixed', call('prepare_slots fixed frame after its first debit', 0, 0,
                             ref('helper_try'), ref('helper_try'), ref('helper_try'), ref('helper_try'), ref('helper_try'),
                             prim('construct WorkCost', 3), ref('meter_call'),
                             ref('vec_with_capacity'), prim('bind slots inside the nonzero branch'),
                             ref('vec_len'), prim('final len < count false'), prim('loop exit'),
                             move('Vec<Option<ClosureCandidate>> out of the nonzero branch into slots', 24),
                             prim('construct PreparedCandidateSlots', 3), prim('Ok tag'),
                             call('scope closure result transport', 0, 48),
                             call('Result::map_err(public_failure) Ok', 48, 48, prim('match tag'), prim('Ok tag'), move('prepared', 40)),
                             call('prepare_slots result transport', 0, 48),
                             call('claim: one successful and one refused call', 0, 0,
                                  call('claim Some', 8, 40, prim('available test'), prim('branch'), prim('store false'),
                                       prim('component slice'), prim('slot slice deref'), prim('Some tag')),
                                  call('claim None', 8, 8, prim('available test'), prim('branch'), prim('None tag')))))
define('zip_iteration', inherited('Zip(components.iter(), slots) next Some per component', 237, ZIP_LOOPS_R1,
                                  'specialized-route scaffold 237F+484 for Zip(Map, slice::Iter); dominates two plain slice iterators'))
define('admit_per_component', call('admit loop body per component', 0, 0,
                                   ref('zip_iteration'),
                                   call('component_candidate call boundary (body is C2a-1)', 48, SC + 8, prim('bind')),
                                   call('map_err(closure_input) Ok', SC + 8, SC + 8, prim('match tag'), prim('Ok tag'), move('candidate', SC)),
                                   call('Try::branch Ok candidate', SC + 8, SC + 8, prim('match tag'), prim('Continue tag'),
                                        move('candidate', SC), prim('caller match')),
                                   call('Option::insert', 8 + SC, 8,
                                        prim('drop old slot value: None tag test (no glue)'), prim('Some tag'), move('candidate into slot', SC),
                                        call('Option::as_mut', 8, 16, prim('match'), prim('Some tag'), prim('reference')),
                                        call('Option::unwrap_unchecked', 16, 8,
                                             precondition('Option::unwrap_unchecked', 1, prim('is_some')), prim('match'), prim('payload'))),
                                   prim('bind candidate reference'),
                                   call('admit_component_inner argument transport', 65, 0),
                                   call('Try::branch Ok AdmittedComponent', ADM + 8, ADM + 8, prim('match tag'), prim('Continue tag'),
                                        move('AdmittedComponent', ADM), prim('caller match'), move('payload binding', ADM)),
                                   vec_push(ADM, 'AdmittedComponent')))
D['admit_per_component']['body'].append({'kind': 'ref', 'name': 'admitted_element_drop'})
CORE = 136
define('admit_fixed', call('admit fixed frame after its first debit', 0, 0,
                           prim('destructure claim', 2), prim('count'),
                           ref('helper_try'), ref('helper_try'), ref('helper_try'), ref('helper_try'), ref('helper_try'),
                           prim('construct WorkCost', 3), ref('meter_call'),
                           ref('vec_with_capacity'), prim('bind admitted'),
                           inherited('Zip constructor, terminal None and loop controls', 484, ZIP_LOOPS_R1,
                                     'specialized-route fixed scaffold'),
                           prim('construct Self components'), move('core roles into Self', CORE), prim('Ok tag'),
                           call('scope closure result transport', 0, 24 + CORE + 8),
                           call('Result::map_err(public_failure) Ok', 24 + CORE + 8, 24 + CORE + 8,
                                prim('match tag'), prim('Ok tag'), move('AdmittedSet', 24 + CORE)),
                           call('admit result transport', 0, 24 + CORE + 8)))


# ---- funding (FIXED 1024, SCAN 256F): explicit roots for the proposed fund_representation (RF-3) ----
# The rows follow funding-r3's LEDGER.json, with the removed arithmetic gone and the same-source candidate.blobs()
# loop replaced by the larger audited counts used for the transfer loop.
define('fund_fixed', call('fund_representation fixed work after its first debit', 0, 0,
                          *[ref('helper_try')] * 18, *[ref('sub_try')] * 2,
                          inherited('candidate.blobs() loop fixed scaffold (constructor, IntoIterator, final None, controls)',
                                    190, ZIP_LOOPS_R1, 'replaces funding-r3 candidate_blobs+into_iter+final_none (57)'),
                          ref('blob_count'), ref('meter_call'), ref('meter_call'),
                          prim('count zero predicate and bool-to-usize', 3),
                          prim('two later WorkCost records, three word writes each', 6),
                          prim('fixed variable writes and constant arithmetic, allowance 25', 25),
                          prim('zero accumulator initializations', 3),
                          prim('final Ok tag/value', 2), prim('fund return transport', 1),
                          prim('one post-first-debit error substitution and borrowed cleanup (funding-r3 ceiling 77)', 128),
                          ref('fund_caller_success')))
define('fund_scan_blob', call('fund_representation scan per Blob', 0, 0,
                              inherited('candidate.blobs() loop scaffold per Blob', 115, ZIP_LOOPS_R1,
                                        'replaces funding-r3 iteration (55)'),
                              ref('length'), *[ref('helper_try')] * 5,
                              prim('divide/rem/nonzero/bool conversion', 4),
                              prim('bytes/chunks/envelopes assignments', 3)))

# ---- drops of operation-owned vectors (each happens exactly once: on failure inside, or later by the owner) ----
define('slot_element_drop', call('per element of drop_in_place::<[Option<ClosureCandidate>]>', 0, 0,
                                 prim('index compare'), prim('element pointer add'), prim('index increment'),
                                 call('drop_in_place::<Option<ClosureCandidate>>', 8, 0, prim('tag test'),
                                      call('ClosureCandidate drop glue boundary (field cleanup is C2a-1 owner work)', 8, 0))))
define('admitted_element_drop', call('per element of drop_in_place::<[AdmittedComponent]>', 0, 0,
                                     prim('index compare'), prim('element pointer add'), prim('index increment'),
                                     call('drop_in_place::<AdmittedComponent>', 8, 0, prim('candidate reference: no glue'),
                                          call('RetainedTree drop glue boundary (cleanup is CI owner work)', 8, 0))))
define('slots_vec_drop', vec_drop_glue('Option<ClosureCandidate>', []))
define('admitted_vec_drop', vec_drop_glue('AdmittedComponent', []))

# ---- explicit failure ceilings (one failure per frame; partial element drops are covered by their own rows) ----
TRY_ERROR = prim('failed Try::branch, Break residual and FromResidual identity (funding-r3 ERROR-CALL-TREE try_error)', 24)
define('component_error', call('component admission failure ceiling after its first debit', 0, 0,
                               call('Result::map_err Err', 32, 32, prim('match tag'),
                                    call('tree_input / closure_input / collector closure', 32, 32, prim('match'), prim('construct Operation'), prim('construct Fault')),
                                    prim('Err tag')),
                               TRY_ERROR, prim('admit_component_inner Err return transport'),
                               prim('loop exit and terminating control', 16)))
define('frame_error', call('prepare_slots or admit failure ceiling after its first debit', 0, 0,
                           TRY_ERROR, prim('scope closure Err return'),
                           call('Result::map_err(public_failure) Err', 32, 32, prim('match tag'),
                                call('public_failure', 32, 32, prim('match'), prim('construct variant')), prim('Err tag')),
                           prim('function Err return'), prim('loop exit and terminating control', 16)))

def cost(node, stack=()):
    if node['kind'] == 'primitive':
        return node['visits']
    if node['kind'] == 'ref':
        assert node['name'] not in stack
        return cost(D[node['name']], stack + (node['name'],))
    return sum((2 * node[k] + 63) // 64 for k in ('argumentBytes', 'resultBytes')) + sum(cost(x, stack) for x in node['body'])


def p2(x):
    return 1 << (x - 1).bit_length()


per_blob = cost(D['per_blob_local'])
component_fixed = cost(D['component_fixed_local'])
slot_per = cost(D['slot_fill_iteration'])
admit_per = cost(D['admit_per_component'])
prepare_fixed = cost(D['prepare_fixed'])
admit_fixed = cost(D['admit_fixed'])
D['prepare_fixed']['body'] += [{'kind': 'ref', 'name': 'slots_vec_drop'}, {'kind': 'ref', 'name': 'frame_error'}]
D['admit_fixed']['body'] += [{'kind': 'ref', 'name': 'admitted_vec_drop'}, {'kind': 'ref', 'name': 'frame_error'}]
D['component_fixed_local']['body'].append({'kind': 'ref', 'name': 'component_error'})
prepare_fixed = cost(D['prepare_fixed'])
admit_fixed = cost(D['admit_fixed'])
component_fixed = cost(D['component_fixed_local'])
slot_per = cost(D['slot_fill_iteration'])
admit_per = cost(D['admit_per_component'])
ERROR_RESERVE = 0
fund_fixed = cost(D['fund_fixed'])
fund_scan = cost(D['fund_scan_blob'])
ledger = {
    'perBlobLocal': {'node': 'per_blob_local', 'visits': per_blob, 'selected': p2(per_blob)},
    'componentFixedLocal': {'node': 'component_fixed_local', 'visits': component_fixed,
                            'errorReserve': ERROR_RESERVE,
                            'selected': p2(component_fixed + ERROR_RESERVE)},
    'slotPerComponent': {'nodes': ['slot_fill_iteration'], 'visits': slot_per, 'selected': p2(slot_per)},
    'admitPerComponent': {'nodes': ['admit_per_component'], 'visits': admit_per, 'selected': p2(admit_per)},
    'prepareFixed': {'node': 'prepare_fixed', 'visits': prepare_fixed, 'errorReserve': ERROR_RESERVE,
                     'selected': p2(prepare_fixed + ERROR_RESERVE)},
    'fundFixed': {'node': 'fund_fixed', 'visits': fund_fixed, 'selected': 1024, 'accepted': 'funding-price-r3'},
    'fundScanPerBlob': {'node': 'fund_scan_blob', 'visits': fund_scan, 'selected': 256, 'accepted': 'funding-price-r3'},
    'admitFixed': {'node': 'admit_fixed', 'visits': admit_fixed, 'errorReserve': ERROR_RESERVE,
                   'selected': p2(admit_fixed + ERROR_RESERVE)},
}
tree = {'scope': 'C2a-3 map retirement and local/slot price addendum r1 call trees; funding-r3 definitions imported by value',
        'importedFundingR3CallTreeSha256': FUND_SHA, 'importedDefinitions': IMPORTED,
        'definitions': D, 'nativeSizes': {'RetainedTree': RT, 'AdmittedComponent': ADM,
                                          'OptionClosureCandidate': SC, 'AuthenticatedCoreRoles': CORE,
                                          'indexEntry': 40, 'Collector': 40, 'Failure': 32},
        'primitiveContractsEstablished': False, 'completeMBoundEstablished': False}
(B / 'CALL-TREE.json').write_text(json.dumps(tree, indent=1) + '\n')
(B / 'LEDGER.json').write_text(json.dumps(ledger, indent=1) + '\n')
print(json.dumps(ledger, indent=1))
for k in ['vec_with_capacity', 'push_tuple', 'tuple_element_drop', 'u8_vec_drop', 'inner_deallocate', 'outer_drop',
          'begin_body', 'finish_body', 'into_verified', 'open_boundary', 'map_err_tree_ok', 'try_tree', 'component_return']:
    print(k, cost(D[k]))
