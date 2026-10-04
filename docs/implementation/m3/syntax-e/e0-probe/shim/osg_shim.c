/*
 * osg_shim.c -- E0 first-party shim (throwaway probe; never product code).
 *
 * Linked into each grammar module with the pinned tree-sitter runtime (lib/src/lib.c),
 * tree-sitter's wasm-stdlib (libc.c, stdio.c) and one grammar's parser.c/scanner.c.
 * Built for wasm32-unknown-unknown with no libc; the module must import nothing (P2).
 *
 * Exports exactly E1 item 5 A10's set:
 *   memory; osg_abi_version, osg_symbols_ptr, osg_symbols_len, osg_result_ptr,
 *   osg_result_len, osg_alloc_failed : [] -> [i32]; osg_alloc : [i32] -> [i32];
 *   osg_parse : [i32, i32] -> [i32].
 *
 * The native leg of P3 is the harness's own Rust serializer over the tree-sitter crate,
 * written independently of this file, so P3 also cross-checks the two serializers.
 *
 * SyntaxTreeV1 as E0 encodes it (E1 item 2 names the fields; the byte layout is E0's):
 *   header 16 bytes: "OSGT", u32 version = 1, u32 node_count, u32 max_depth
 *   node_count records of 20 bytes, preorder over the visible nodes of the tree-sitter
 *   API view (the TSTreeCursor walk), little-endian:
 *     u16 symbol      ts_node_symbol (public symbol after aliasing; ERROR = 0xFFFF)
 *     u16 field       ts_tree_cursor_current_field_id (0 = none)
 *     u16 flags       bit0 named, bit1 extra, bit2 error (ts_node_is_error), bit3 missing
 *     u16 reserved    0
 *     u32 start_byte, u32 end_byte, u32 child_count (ts_node_child_count)
 *   Depth: the root is depth 1.
 *
 * SymbolTable blob (decoded by the host into canonical SymbolTableV1, A11):
 *   "OSGS", u32 version = 1, u32 language_abi, u32 symbol_count, u32 field_count,
 *   per symbol id 0..symbol_count-1: u8 named, u8 visible, u16 name_len, name bytes
 *   per field id 1..field_count:      u16 name_len, name bytes
 *   named   = ts_language_symbol_type == TSSymbolTypeRegular
 *   visible = ts_language_symbol_type <= TSSymbolTypeAnonymous   (as the Rust binding)
 */
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "tree_sitter/api.h"

#ifndef OSG_LANGUAGE_FN
#error "OSG_LANGUAGE_FN must name the grammar's language function"
#endif
const TSLanguage *OSG_LANGUAGE_FN(void);

#define OSG_SHIM_ABI   1u
#define OSG_MAX_NODES  4194304u   /* E1 item 11 maxNodes */
#define OSG_MAX_DEPTH  4096u      /* E1 item 11 maxDepth */

enum {
  OSG_OK = 0,
  OSG_TRUNC_NODES = 1,
  OSG_TRUNC_DEPTH = 2,
  OSG_FAULT_PARSE_NULL = 3,
  OSG_FAULT_LANGUAGE = 4,
};

#ifndef __wasm__
#error "osg_shim.c is built for wasm32 only"
#endif
#define OSG_EXPORT(name) __attribute__((visibility("default"), export_name(name)))

/* ------------------------------------------------------------------------------------
 * Allocator. tree-sitter's wasm-stdlib allocator (external_scanner_allocator.c) is a
 * scanner-only allocator with a hard 4 MiB heap and a linear first-fit free list, so it
 * cannot serve the runtime. This is a deterministic O(1) segregated-fit allocator:
 * 8-byte header holding the class, 16-byte classes up to 256, then powers of two.
 * No splitting, no coalescing. Exhaustion records osg_alloc_failed and traps; it never
 * returns NULL for a non-zero request (a NULL dereference does not trap in wasm).
 * ---------------------------------------------------------------------------------- */
extern unsigned char __heap_base;

#define OSG_PAGE 65536u
#define OSG_HDR 8u                               /* payloads stay 8-aligned: need = class + 8, classes are 16k */
#define OSG_SMALL_CLASSES 16u                    /* 16, 32, ..., 256 */
#define OSG_NCLASSES (OSG_SMALL_CLASSES + 22u)   /* 512 .. 2^30 */
#define OSG_MAX_BLOCK 0x40000000u                /* 1 GiB; larger is exhaustion */

static uint32_t osg_alloc_failed_flag;
static uint64_t osg_bump;    /* 64-bit: 65,536 pages is exactly 2^32 bytes */
static uint64_t osg_limit;
static void *osg_free_list[OSG_NCLASSES];

static __attribute__((noreturn)) void osg_exhausted(void) {
  osg_alloc_failed_flag = 1;
  __builtin_trap();
}

static inline uint32_t osg_class_of(size_t n) {          /* 1 <= n <= OSG_MAX_BLOCK */
  if (n <= 256u) return (uint32_t)((n + 15u) / 16u) - 1u;
  uint32_t lg = 32u - (uint32_t)__builtin_clz((uint32_t)(n - 1u));   /* ceil(log2 n) */
  return OSG_SMALL_CLASSES + (lg - 9u);                              /* 512 -> class 16 */
}

static inline uint64_t osg_class_size(uint32_t c) {
  if (c < OSG_SMALL_CLASSES) return (uint64_t)(c + 1u) * 16u;
  return (uint64_t)1u << (c - OSG_SMALL_CLASSES + 9u);
}

static void *osg_raw_alloc(size_t n) {
  if (n == 0 || n > OSG_MAX_BLOCK) osg_exhausted();
  uint32_t c = osg_class_of(n);
  void *p = osg_free_list[c];
  if (p) {
    osg_free_list[c] = *(void **)p;
    return p;
  }
  if (osg_bump == 0) {
    osg_bump = ((uint64_t)(uintptr_t)&__heap_base + 15u) & ~(uint64_t)15u;
    osg_limit = (uint64_t)__builtin_wasm_memory_size(0) * OSG_PAGE;
  }
  uint64_t hdr = osg_bump;
  uint64_t end = hdr + OSG_HDR + osg_class_size(c);
  if (end > (uint64_t)1u << 32) osg_exhausted();
  if (end > osg_limit) {
    uint64_t pages = (end - osg_limit + OSG_PAGE - 1u) / OSG_PAGE;
    if (__builtin_wasm_memory_grow(0, (size_t)pages) == (size_t)-1) osg_exhausted();
    osg_limit = (uint64_t)__builtin_wasm_memory_size(0) * OSG_PAGE;
  }
  *(uint32_t *)(uintptr_t)hdr = c;
  osg_bump = end;
  return (void *)(uintptr_t)(hdr + OSG_HDR);
}

void *malloc(size_t n) {
  if (n == 0) return NULL;
  return osg_raw_alloc(n);
}

void free(void *p) {
  if (!p) return;
  uint32_t c = *(uint32_t *)((uintptr_t)p - OSG_HDR);
  *(void **)p = osg_free_list[c];
  osg_free_list[c] = p;
}

void *calloc(size_t count, size_t size) {
  if (count == 0 || size == 0) return NULL;
  if (size > (size_t)-1 / count) osg_exhausted();
  size_t n = count * size;
  void *p = osg_raw_alloc(n);
  memset(p, 0, n);   /* recycled blocks are dirty */
  return p;
}

void *realloc(void *p, size_t n) {
  if (!p) return malloc(n);
  if (n == 0) { free(p); return NULL; }
  uint32_t c = *(uint32_t *)((uintptr_t)p - OSG_HDR);
  uint64_t have = osg_class_size(c);
  if ((uint64_t)n <= have) return p;
  void *q = osg_raw_alloc(n);
  memcpy(q, p, (size_t)have);
  free(p);
  return q;
}

__attribute__((noreturn)) void abort(void) {
  __builtin_trap();
}


/* ------------------------------------------------------------------------------------
 * Byte buffer helpers.
 * ---------------------------------------------------------------------------------- */
typedef struct { uint8_t *p; uint32_t len, cap; } OsgBuf;

static void osg_buf_reserve(OsgBuf *b, uint32_t extra) {
  uint32_t want = b->len + extra;
  if (want <= b->cap) return;
  if (want > 0x40000000u) osg_exhausted();
  uint32_t cap = b->cap ? b->cap : 4096u;
  while (cap < want) cap *= 2u;
  b->p = (uint8_t *)realloc(b->p, cap);
  b->cap = cap;
}
static inline void osg_put_u8(OsgBuf *b, uint8_t v) { b->p[b->len++] = v; }
static inline void osg_put_u16(OsgBuf *b, uint16_t v) {
  b->p[b->len++] = (uint8_t)v; b->p[b->len++] = (uint8_t)(v >> 8);
}
static inline void osg_put_u32(OsgBuf *b, uint32_t v) {
  b->p[b->len++] = (uint8_t)v;         b->p[b->len++] = (uint8_t)(v >> 8);
  b->p[b->len++] = (uint8_t)(v >> 16); b->p[b->len++] = (uint8_t)(v >> 24);
}
static inline void osg_set_u32(OsgBuf *b, uint32_t at, uint32_t v) {
  b->p[at] = (uint8_t)v; b->p[at + 1] = (uint8_t)(v >> 8);
  b->p[at + 2] = (uint8_t)(v >> 16); b->p[at + 3] = (uint8_t)(v >> 24);
}

/* ------------------------------------------------------------------------------------
 * State. A product instance parses exactly one file; the previous-parse release below
 * exists only for E0's instance-reuse control (forbidden in the product).
 * ---------------------------------------------------------------------------------- */
static OsgBuf osg_result;
static OsgBuf osg_symbols;
static uint8_t *osg_input;
static TSParser *osg_last_parser;
static TSTree *osg_last_tree;

OSG_EXPORT("osg_abi_version") uint32_t osg_abi_version(void) { return OSG_SHIM_ABI; }
OSG_EXPORT("osg_alloc_failed") uint32_t osg_alloc_failed(void) { return osg_alloc_failed_flag; }
OSG_EXPORT("osg_result_ptr") uint32_t osg_result_ptr(void) { return (uint32_t)(uintptr_t)osg_result.p; }
OSG_EXPORT("osg_result_len") uint32_t osg_result_len(void) { return osg_result.len; }

static void osg_build_symbols(void) {
  if (osg_symbols.p) return;
  const TSLanguage *lang = OSG_LANGUAGE_FN();
  uint32_t sc = ts_language_symbol_count(lang);
  uint32_t fc = ts_language_field_count(lang);
  osg_buf_reserve(&osg_symbols, 20u);
  osg_put_u8(&osg_symbols, 'O'); osg_put_u8(&osg_symbols, 'S');
  osg_put_u8(&osg_symbols, 'G'); osg_put_u8(&osg_symbols, 'S');
  osg_put_u32(&osg_symbols, 1u);
  osg_put_u32(&osg_symbols, ts_language_abi_version(lang));
  osg_put_u32(&osg_symbols, sc);
  osg_put_u32(&osg_symbols, fc);
  for (uint32_t id = 0; id < sc; id++) {
    TSSymbolType t = ts_language_symbol_type(lang, (TSSymbol)id);
    const char *name = ts_language_symbol_name(lang, (TSSymbol)id);
    uint32_t n = name ? (uint32_t)strlen(name) : 0u;
    if (n > 0xFFFFu) n = 0xFFFFu;   /* the host bounds names at 1,024 bytes and refuses */
    osg_buf_reserve(&osg_symbols, 4u + n);
    osg_put_u8(&osg_symbols, t == TSSymbolTypeRegular ? 1u : 0u);
    osg_put_u8(&osg_symbols, t <= TSSymbolTypeAnonymous ? 1u : 0u);
    osg_put_u16(&osg_symbols, (uint16_t)n);
    if (n) { memcpy(osg_symbols.p + osg_symbols.len, name, n); osg_symbols.len += n; }
  }
  for (uint32_t id = 1; id <= fc; id++) {
    const char *name = ts_language_field_name_for_id(lang, (TSFieldId)id);
    uint32_t n = name ? (uint32_t)strlen(name) : 0u;
    if (n > 0xFFFFu) n = 0xFFFFu;
    osg_buf_reserve(&osg_symbols, 2u + n);
    osg_put_u16(&osg_symbols, (uint16_t)n);
    if (n) { memcpy(osg_symbols.p + osg_symbols.len, name, n); osg_symbols.len += n; }
  }
}

OSG_EXPORT("osg_symbols_ptr") uint32_t osg_symbols_ptr(void) {
  osg_build_symbols();
  return (uint32_t)(uintptr_t)osg_symbols.p;
}
OSG_EXPORT("osg_symbols_len") uint32_t osg_symbols_len(void) {
  osg_build_symbols();
  return osg_symbols.len;
}

/* Input buffer for the host to fill; never zero (an empty file still gets a pointer). */
OSG_EXPORT("osg_alloc") uint32_t osg_alloc(uint32_t len) {
  if (osg_input) { free(osg_input); osg_input = NULL; }   /* reuse control only */
  osg_input = (uint8_t *)malloc(len ? len : 1u);
  return (uint32_t)(uintptr_t)osg_input;
}

static void osg_emit(OsgBuf *b, TSNode node, TSFieldId field) {
  uint16_t flags = (uint16_t)((ts_node_is_named(node) ? 1u : 0u) |
                              (ts_node_is_extra(node) ? 2u : 0u) |
                              (ts_node_is_error(node) ? 4u : 0u) |
                              (ts_node_is_missing(node) ? 8u : 0u));
  osg_buf_reserve(b, 20u);
  osg_put_u16(b, ts_node_symbol(node));
  osg_put_u16(b, field);
  osg_put_u16(b, flags);
  osg_put_u16(b, 0u);
  osg_put_u32(b, ts_node_start_byte(node));
  osg_put_u32(b, ts_node_end_byte(node));
  osg_put_u32(b, ts_node_child_count(node));
}

/* Serialize a tree into b (cleared first). Returns OSG_OK or a truncation status. */
static uint32_t osg_serialize(OsgBuf *b, TSTree *tree) {
  b->len = 0;
  osg_buf_reserve(b, 16u);
  osg_put_u8(b, 'O'); osg_put_u8(b, 'S'); osg_put_u8(b, 'G'); osg_put_u8(b, 'T');
  osg_put_u32(b, 1u);
  osg_put_u32(b, 0u);   /* node_count, patched below */
  osg_put_u32(b, 0u);   /* max_depth, patched below */
#ifdef OSG_DIAG_ROOT_ONLY
  /* Phase-2 diagnostic build only (never gated): the root record alone, with child count 0,
   * so the parse can be timed without the full serialization walk. */
  {
    TSNode root = ts_tree_root_node(tree);
    osg_buf_reserve(b, 20u);
    osg_put_u16(b, ts_node_symbol(root)); osg_put_u16(b, 0u); osg_put_u16(b, 0u); osg_put_u16(b, 0u);
    osg_put_u32(b, ts_node_start_byte(root)); osg_put_u32(b, ts_node_end_byte(root)); osg_put_u32(b, 0u);
    osg_set_u32(b, 8u, 1u);
    osg_set_u32(b, 12u, 1u);
    return OSG_OK;
  }
#endif
  TSTreeCursor c = ts_tree_cursor_new(ts_tree_root_node(tree));
  uint32_t n = 0, depth = 1, max_depth = 1, status = OSG_OK;
  for (;;) {
    if (depth > OSG_MAX_DEPTH) { status = OSG_TRUNC_DEPTH; break; }
    if (n == OSG_MAX_NODES) { status = OSG_TRUNC_NODES; break; }
    osg_emit(b, ts_tree_cursor_current_node(&c), ts_tree_cursor_current_field_id(&c));
    n++;
    if (ts_tree_cursor_goto_first_child(&c)) {
      depth++;
      if (depth > max_depth) max_depth = depth;
      continue;
    }
    for (;;) {
      if (ts_tree_cursor_goto_next_sibling(&c)) goto next;
      if (!ts_tree_cursor_goto_parent(&c)) goto done;
      depth--;
    }
  next:;
  }
done:
  ts_tree_cursor_delete(&c);
  osg_set_u32(b, 8u, n);
  osg_set_u32(b, 12u, max_depth);
  return status;
}

OSG_EXPORT("osg_parse") uint32_t osg_parse(uint32_t ptr, uint32_t len) {
  if (osg_last_tree) { ts_tree_delete(osg_last_tree); osg_last_tree = NULL; }        /* reuse control only */
  if (osg_last_parser) { ts_parser_delete(osg_last_parser); osg_last_parser = NULL; }
  TSParser *parser = ts_parser_new();
  osg_last_parser = parser;
  if (!ts_parser_set_language(parser, OSG_LANGUAGE_FN())) return OSG_FAULT_LANGUAGE;
  TSTree *tree = ts_parser_parse_string(parser, NULL, (const char *)(uintptr_t)ptr, len);
  if (!tree) return OSG_FAULT_PARSE_NULL;
  osg_last_tree = tree;
  return osg_serialize(&osg_result, tree);
}
