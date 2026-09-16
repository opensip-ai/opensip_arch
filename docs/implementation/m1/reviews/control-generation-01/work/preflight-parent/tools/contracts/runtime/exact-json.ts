/** Trial exact JSON codec: inert values, no semantic admission authority. */
export type Json = null | boolean | bigint | string | Json[] | { [key: string]: Json };
export const MAX_BYTES = 4 * 1024 * 1024;
export const MAX_DEPTH = 32;
const MIN_INTEGER = -(1n << 63n);
const MAX_INTEGER = (1n << 64n) - 1n;
const encoder = new TextEncoder();
export class JsonError extends Error {}
const fail = (message: string): never => { throw new JsonError(message); };

function scalarString(value: string): void {
  for (const ch of value) {
    const cp = ch.codePointAt(0)!;
    if (cp >= 0xd800 && cp <= 0xdfff) fail("UNICODE_SCALAR_REQUIRED");
  }
}

export function utf8Compare(a: string, b: string): number {
  const left = encoder.encode(a), right = encoder.encode(b);
  for (let i = 0; i < Math.min(left.length, right.length); i++) {
    if (left[i] !== right[i]) return left[i]! < right[i]! ? -1 : 1;
  }
  return left.length - right.length;
}

export function parseExact(raw: Uint8Array): Json {
  if (!(raw instanceof Uint8Array)) fail("BYTE_INPUT_REQUIRED");
  if (typeof SharedArrayBuffer !== "undefined" && raw.buffer instanceof SharedArrayBuffer) fail("SHARED_BYTES_FORBIDDEN");
  if (raw.length > MAX_BYTES) fail("BYTE_LIMIT");
  let text: string;
  try { text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(raw); }
  catch { return fail("INVALID_UTF8"); }
  let offset = 0;
  const space = () => { while (offset < text.length && " \t\r\n".includes(text[offset]!)) offset++; };
  const string = (): string => {
    const start = offset++;
    let escaped = false;
    while (offset < text.length) {
      const ch = text[offset++]!;
      if (!escaped && ch === '"') {
        let value: string;
        try { value = JSON.parse(text.slice(start, offset)) as string; }
        catch { return fail("INVALID_STRING"); }
        scalarString(value);
        return value;
      }
      if (escaped) escaped = false;
      else if (ch === "\\") escaped = true;
    }
    return fail("UNTERMINATED_STRING");
  };
  const value = (depth: number): Json => {
    space();
    const ch = text[offset];
    if (ch === '"') return string();
    if (ch === "[" || ch === "{") {
      if (depth >= MAX_DEPTH) fail("DEPTH_LIMIT");
      offset++; space();
      if (ch === "[") {
        const result: Json[] = [];
        if (text[offset] === "]") { offset++; return result; }
        while (true) {
          result.push(value(depth + 1)); space();
          if (text[offset] === "]") { offset++; return result; }
          if (text[offset++] !== ",") return fail("ARRAY_DELIMITER");
        }
      }
      const result: { [key: string]: Json } = Object.create(null);
      if (text[offset] === "}") { offset++; return result; }
      while (true) {
        space(); if (text[offset] !== '"') return fail("OBJECT_KEY");
        const key = string();
        if (Object.hasOwn(result, key)) fail("DUPLICATE_KEY");
        space(); if (text[offset++] !== ":") return fail("OBJECT_COLON");
        result[key] = value(depth + 1); space();
        if (text[offset] === "}") { offset++; return result; }
        if (text[offset++] !== ",") return fail("OBJECT_DELIMITER");
      }
    }
    for (const [token, result] of [["true", true], ["false", false], ["null", null]] as const) {
      if (text.startsWith(token, offset)) { offset += token.length; return result; }
    }
    const match = /^-?(?:0|[1-9][0-9]*)/.exec(text.slice(offset));
    if (!match) return fail("INVALID_VALUE");
    const lexeme = match[0]; offset += lexeme.length;
    if (lexeme === "-0") fail("NEGATIVE_ZERO");
    if (text[offset] === "." || text[offset] === "e" || text[offset] === "E") fail("FLOAT_FORBIDDEN");
    // Reject overlong digits before allocating an unbounded BigInt.
    if (lexeme.length > 21) fail("INTEGER_RANGE");
    const number = BigInt(lexeme);
    if (number < MIN_INTEGER || number > MAX_INTEGER) fail("INTEGER_RANGE");
    return number;
  };
  const result = value(0); space();
  if (offset !== text.length) fail("TRAILING_DATA");
  return result;
}

export function canonical(value: Json): Uint8Array {
  const chunks: string[] = []; let bytes = 0;
  const put = (part: string) => {
    bytes += encoder.encode(part).length;
    if (bytes > MAX_BYTES) fail("BYTE_LIMIT");
    chunks.push(part);
  };
  const visit = (item: Json, depth: number): void => {
    if (item === null) { put("null"); return; }
    if (typeof item === "boolean") { put(item ? "true" : "false"); return; }
    if (typeof item === "bigint") {
      if (item < MIN_INTEGER || item > MAX_INTEGER) fail("INTEGER_RANGE");
      put(item.toString()); return;
    }
    if (typeof item === "string") { scalarString(item); put(JSON.stringify(item)); return; }
    if (typeof item !== "object") fail("EXACT_JSON_TYPE_REQUIRED");
    if (depth >= MAX_DEPTH) fail("DEPTH_LIMIT");
    if (Array.isArray(item)) {
      if (Object.getPrototypeOf(item) !== Array.prototype) fail("PLAIN_ARRAY_REQUIRED");
      if (Object.getOwnPropertySymbols(item).length || Object.getOwnPropertyNames(item).length !== item.length + 1) fail("PLAIN_ARRAY_REQUIRED");
      put("["); for (let i = 0; i < item.length; i++) {
        if (i) put(",");
        const descriptor = Object.getOwnPropertyDescriptor(item, String(i));
        if (!descriptor || !Object.hasOwn(descriptor, "value")) fail("ARRAY_DATA_PROPERTIES_REQUIRED");
        visit(descriptor!.value as Json, depth + 1);
      } put("]");
      return;
    }
    if (Object.getPrototypeOf(item) !== null && Object.getPrototypeOf(item) !== Object.prototype) fail("PLAIN_OBJECT_REQUIRED");
    if (Object.getOwnPropertySymbols(item).length) fail("STRING_KEY_REQUIRED");
    const keys = Object.keys(item).sort(utf8Compare);
    if (keys.length !== Object.getOwnPropertyNames(item).length) fail("ENUMERABLE_DATA_REQUIRED");
    put("{"); for (let i = 0; i < keys.length; i++) {
      if (i) put(","); const key = keys[i]!; scalarString(key);
      const descriptor = Object.getOwnPropertyDescriptor(item, key)!;
      if (!Object.hasOwn(descriptor, "value")) fail("DATA_PROPERTIES_REQUIRED");
      put(JSON.stringify(key)); put(":"); visit(descriptor.value as Json, depth + 1);
    } put("}");
  };
  visit(value, 0); return encoder.encode(chunks.join(""));
}
