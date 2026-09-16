/** Trial interpreter for the selected schema vocabulary. Shape is not semantic authority. */
import { selectedPattern } from "./patterns.js";
import { canonical, parseExact, type Json, utf8Compare } from "./exact-json.js";
type ObjectValue = { [key: string]: Json };
const object = (v: Json | undefined): v is ObjectValue => v !== null && typeof v === "object" && !Array.isArray(v);
const equal = (a: Json, b: Json): boolean => {
  if (typeof a !== typeof b) return false;
  if (a === b) return true;
  if (Array.isArray(a)) return Array.isArray(b) && a.length === b.length && a.every((v, i) => equal(v, b[i]!));
  if (!object(a) || !object(b)) return false;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every(k => Object.hasOwn(b, k) && equal(a[k]!, b[k]!));
};
export class SchemaError extends Error {}
export class ShapeLimit extends Error {}
const known = new Set(["$id", "$schema", "$defs", "definitions", "$ref", "title", "description", "default", "type", "const", "enum", "allOf", "anyOf", "oneOf", "not", "if", "then", "else", "properties", "patternProperties", "additionalProperties", "propertyNames", "required", "minProperties", "maxProperties", "items", "minItems", "maxItems", "uniqueItems", "contains", "minLength", "maxLength", "pattern", "minimum", "maximum", "x-opensip-order", "x-maxUtf8Bytes"]);
const annotations = new Set(["x-opensip-admission-precedence", "x-opensip-config-node-kind-law", "x-opensip-deficiency-cause-registry", "x-opensip-digest", "x-opensip-digest-domains", "x-opensip-digest-law", "x-opensip-evaluator-deficiency-registry", "x-opensip-evaluator-profile", "x-opensip-evaluator-registry", "x-opensip-evaluator3-repair-target-law", "x-opensip-evidence-relation-registry", "x-opensip-fixture-representation", "x-opensip-grammar-capability-registry", "x-opensip-imported-requirement-law", "x-opensip-mirror", "x-opensip-mutation-operation-map", "x-opensip-negotiation", "x-opensip-order-vocabulary", "x-opensip-output-profile", "x-opensip-ownership-attribute", "x-opensip-payload-registry", "x-opensip-profile-major-law", "x-opensip-public-route-registry", "x-opensip-startup-law", "x-opensip-uniqueness", "x-opensip-vocabulary", "x-opensip-wire", "x-opensip-wire-law"]);
const maps = new Set(["$defs", "definitions", "properties", "patternProperties"]);
const singles = new Set(["additionalProperties", "propertyNames", "items", "not", "if", "then", "else", "contains"]);
const arrays = new Set(["allOf", "anyOf", "oneOf"]);

const strings = new Set(["$id", "$schema", "$ref", "title", "description", "pattern"]);
const counts = new Set(["minProperties", "maxProperties", "minItems", "maxItems", "minLength", "maxLength", "x-maxUtf8Bytes"]);
const allowed = new Set(["null", "boolean", "integer", "string", "array", "object"]);

export class SchemaRegistry {
  private readonly documents = new Map<string, Json>();
  private readonly patterns = new Map<string, RegExp>();
  private readonly checkedRefs = new Set<string>();
  constructor(documents: readonly Json[]) {
    for (const document of documents) {
      const owned = parseExact(canonical(document));
      if (!object(owned) || typeof owned.$id !== "string" || this.documents.has(owned.$id)) throw new SchemaError("duplicate or missing schema ID");
      if (owned.$schema !== "https://json-schema.org/draft/2020-12/schema") throw new SchemaError("unsupported schema dialect");
      this.documents.set(owned.$id, owned);
    }
  }
  private regex(pattern: string): RegExp {
    let result = this.patterns.get(pattern);
    if (!result) {
      const translated = selectedPattern(pattern);
      if (translated === undefined) throw new SchemaError("pattern outside selected profile");
      result = new RegExp(translated, "u"); this.patterns.set(pattern, result);
    }
    return result;
  }
  private resolve(ref: string, owner: string): [Json, string] {
    const split = ref.indexOf("#");
    const id = (split < 0 ? ref : ref.slice(0, split)) || owner;
    const fragment = split < 0 ? "" : ref.slice(split + 1);
    let value = this.documents.get(id);
    if (value === undefined) throw new SchemaError("unregistered schema ID: " + id);
    if (fragment && !fragment.startsWith("/")) throw new SchemaError("unsupported reference anchor");
    for (const segment of fragment.split("/").slice(1)) {
      if (/~(?![01])/.test(segment)) throw new SchemaError("invalid pointer escape");
      const key = segment.replaceAll("~1", "/").replaceAll("~0", "~");
      if (!object(value) || !Object.hasOwn(value, key)) throw new SchemaError("missing schema pointer: " + ref);
      value = value[key]!;
    }
    if (typeof value !== "boolean" && !object(value)) throw new SchemaError("reference does not select a schema");
    return [value, id];
  }
  /** Explicit entry point closure; unused historical declarations are not selected. */
  checkEntryPoints(refs: readonly string[]): void {
    const visited = new Set<string>();
    const visitRef = (ref: string, owner: string): void => {
      const [schema, id] = this.resolve(ref, owner);
      const key = id + "#" + (ref.split("#")[1] ?? "");
      if (visited.has(key)) return;
      visited.add(key); visit(schema, id);
    };
    const visit = (schema: Json, owner: string): void => {
      if (typeof schema === "boolean") return;
      if (!object(schema)) throw new SchemaError("invalid schema node");
      for (const [key, value] of Object.entries(schema)) {
        if (!known.has(key) && !annotations.has(key)) throw new SchemaError("unsupported keyword: " + key);
        if (strings.has(key) && typeof value !== "string") throw new SchemaError("string keyword required: " + key);
        if (counts.has(key) && (typeof value !== "bigint" || value < 0n)) throw new SchemaError("nonnegative integer keyword required: " + key);
        if ((key === "minimum" || key === "maximum") && typeof value !== "bigint") throw new SchemaError("integer bound required");
        if (key === "uniqueItems" && typeof value !== "boolean") throw new SchemaError("boolean uniqueItems required");
        if (key === "enum" && (!Array.isArray(value) || value.length === 0 || value.some((v, i) => value.slice(0, i).some(x => equal(x, v))))) throw new SchemaError("unique nonempty enum required");
        if (key === "required" && (!Array.isArray(value) || value.some(v => typeof v !== "string") || new Set(value).size !== value.length)) throw new SchemaError("unique required strings required");
        if (key === "type") {
          const types = Array.isArray(value) ? value : [value];
            if (types.length === 0 || types.some(v => typeof v !== "string" || !allowed.has(v)) || new Set(types).size !== types.length) throw new SchemaError("unsupported type vocabulary");
        }
        if (key === "$id" && value !== owner) throw new SchemaError("nested schema ID unsupported");
        if (key === "$schema" && value !== "https://json-schema.org/draft/2020-12/schema") throw new SchemaError("unsupported nested schema dialect");
        if (key === "$ref") visitRef(value as string, owner);
        // Definitions are visited only when explicitly selected/referenced.
        else if (maps.has(key) && key !== "$defs" && key !== "definitions") {
          if (!object(value)) throw new SchemaError("invalid schema map");
          for (const item of Object.values(value)) visit(item, owner);
        } else if (singles.has(key)) visit(value, owner);
        else if (arrays.has(key)) {
          if (!Array.isArray(value) || value.length === 0) throw new SchemaError("invalid applicator array");
          value.forEach(item => visit(item, owner));
        }
        if (key === "x-opensip-order") {
          const named = new Set(["sequence", "utf8", "canonical-set", "canonical-order", "path", "ruleId", "waiverId", "predicate", "numeric", "ordinal", "candidateOrdinal"]);
          const by = object(value) ? value.by : undefined;
          if (!(typeof value === "string" && named.has(value)) && !(object(value) && Object.keys(value).length === 1 && Array.isArray(by) && by.length > 0 && by.every(k => typeof k === "string" && k.length > 0) && new Set(by).size === by.length)) throw new SchemaError("unsupported ordering annotation");
        }
        if (key === "pattern") this.regex(value as string);
        if (key === "patternProperties") for (const pattern of Object.keys(value as ObjectValue)) this.regex(pattern);
      }
    };
    refs.forEach(ref => { if (!this.checkedRefs.has(ref)) { visitRef(ref, ""); this.checkedRefs.add(ref); } });
  }
  matches(ref: string, value: Json, limit = 1_000_000): boolean {
    this.checkEntryPoints([ref]);
    // Own the data before evaluation; never read the caller again after serialization.
    // Native Proxy effects during serialization are outside this inert-data API.
    const owned = parseExact(canonical(value));
    let work = 0, callDepth = 0;
    if (!Number.isSafeInteger(limit) || limit < 1) throw new SchemaError("positive work limit required");
    const spend = (): void => { if (++work > limit) throw new ShapeLimit("schema work limit"); };
    const bound = (length: number, schema: ObjectValue, low: string, high: string): boolean =>
      (schema[low] === undefined || BigInt(length) >= (schema[low] as bigint)) &&
      (schema[high] === undefined || BigInt(length) <= (schema[high] as bigint));
    const check = (schema: Json, item: Json, owner: string): boolean => {
      if (++callDepth > 256) throw new ShapeLimit("schema call-depth limit");
      try { return evaluate(schema, item, owner); }
      finally { callDepth--; }
    };
    const evaluate = (schema: Json, item: Json, owner: string): boolean => {
      spend();
      if (typeof schema === "boolean") return schema;
      if (!object(schema)) throw new SchemaError("invalid schema node");
      if (typeof schema.$ref === "string") {
        const [target, id] = this.resolve(schema.$ref, owner);
        if (!check(target, item, id)) return false;
      }
      if (Object.hasOwn(schema, "const") && !equal(item, schema.const!)) return false;
      if (Array.isArray(schema.enum) && !schema.enum.some(v => equal(item, v))) return false;
      if (schema.type !== undefined) {
        const types = Array.isArray(schema.type) ? schema.type : [schema.type];
        const type = item === null ? "null" : Array.isArray(item) ? "array" : typeof item === "bigint" ? "integer" : typeof item;
        if (!types.includes(type)) return false;
      }
      if (Array.isArray(schema.allOf) && !schema.allOf.every(s => check(s, item, owner))) return false;
      if (Array.isArray(schema.anyOf) && !schema.anyOf.some(s => check(s, item, owner))) return false;
      if (Array.isArray(schema.oneOf) && schema.oneOf.filter(s => check(s, item, owner)).length !== 1) return false;
      if (schema.not !== undefined && check(schema.not, item, owner)) return false;
      if (schema.if !== undefined) {
        const branch = check(schema.if, item, owner) ? schema.then : schema.else;
        if (branch !== undefined && !check(branch, item, owner)) return false;
      }
      if (typeof item === "bigint" && ((schema.minimum !== undefined && item < (schema.minimum as bigint)) || (schema.maximum !== undefined && item > (schema.maximum as bigint)))) return false;
      if (typeof item === "string") {
        if (!bound([...item].length, schema, "minLength", "maxLength")) return false;
        if (schema["x-maxUtf8Bytes"] !== undefined && BigInt(new TextEncoder().encode(item).byteLength) > (schema["x-maxUtf8Bytes"] as bigint)) return false;
        if (typeof schema.pattern === "string" && !this.regex(schema.pattern).test(item)) return false;
      }
      if (Array.isArray(item)) {
        if (!bound(item.length, schema, "minItems", "maxItems")) return false;
        if (schema.items !== undefined && !item.every(v => check(schema.items!, v, owner))) return false;
        if (schema.contains !== undefined && !item.some(v => check(schema.contains!, v, owner))) return false;
        if (schema.uniqueItems === true) {
          const seen = new Set<string>();
          for (const v of item) { spend(); const key = new TextDecoder().decode(canonical(v)); if (seen.has(key)) return false; seen.add(key); }
        }
        const order = schema["x-opensip-order"];
        if (order !== undefined && order !== "sequence" && !ordered(item, order)) return false;
      }
      if (object(item)) {
        const keys = Object.keys(item);
        if (!bound(keys.length, schema, "minProperties", "maxProperties")) return false;
        if (Array.isArray(schema.required) && !schema.required.every(k => typeof k === "string" && Object.hasOwn(item, k))) return false;
        for (const key of keys) {
          spend(); const child = item[key]!; let matched = false;
          if (schema.propertyNames !== undefined && !check(schema.propertyNames, key, owner)) return false;
          if (object(schema.properties) && Object.hasOwn(schema.properties, key)) { matched = true; if (!check(schema.properties[key]!, child, owner)) return false; }
          if (object(schema.patternProperties)) for (const [pattern, rule] of Object.entries(schema.patternProperties)) {
            if (this.regex(pattern).test(key)) { matched = true; if (!check(rule, child, owner)) return false; }
          }
          if (!matched && schema.additionalProperties !== undefined && !check(schema.additionalProperties, child, owner)) return false;
        }
      }
      return true;
    };
    const [schema, owner] = this.resolve(ref, "");
    return check(schema, owned, owner);
  }
}

function ordered(items: Json[], order: Json): boolean {
  const compare = (a: string | bigint, b: string | bigint): number =>
    typeof a === "string" && typeof b === "string" ? utf8Compare(a, b) : a < b ? -1 : a > b ? 1 : 0;
  let keys: (string | bigint)[][] = [];
  const numeric = order === "numeric" || order === "ordinal" || order === "candidateOrdinal";
  const fields = object(order) ? order.by : order === "predicate" ? ["ruleId", "subjectId", "predicateId"] : [order];
  for (const item of items) {
    let key: Json[];
    if (order === "utf8" || order === "numeric") key = [item];
    else if (order === "canonical-set" || order === "canonical-order") key = [new TextDecoder().decode(canonical(item))];
    else {
      if (!object(item) || !Array.isArray(fields) || fields.some(k => typeof k !== "string" || !Object.hasOwn(item, k))) return false;
      key = fields.map(k => item[k as string]!);
    }
    if (!key.every(v => typeof v === (numeric ? "bigint" : "string"))) return false;
    keys.push(key as (string | bigint)[]);
  }
  if (order === "ordinal" && !keys.every((k, i) => k[0] === BigInt(i))) return false;
  for (let i = 1; i < keys.length; i++) {
    const a = keys[i - 1]!, b = keys[i]!;
    let c = 0;
    for (let j = 0; j < a.length && c === 0; j++) c = compare(a[j]!, b[j]!);
    if (c > 0 || (c === 0 && order !== "canonical-order")) return false;
  }
  return true;
}
