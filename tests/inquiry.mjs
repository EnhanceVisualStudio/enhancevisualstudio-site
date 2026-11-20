import assert from "node:assert/strict";
import { fileURLToPath, pathToFileURL } from "node:url";
import { resolve } from "node:path";

const DEFAULT_REPO_ROOT = fileURLToPath(new URL("../", import.meta.url));
const ORIGIN = "https://codex-evs-redesign.enhancevisualstudio-site.pages.dev";
const PROVIDER_CODES = [
  "E_VALIDATION_ERROR",
  "E_FIELD_MISSING",
  "E_TOO_MANY_RECIPIENTS",
  "E_TOO_MANY_ATTACHMENTS",
  "E_SENDER_NOT_VERIFIED",
  "E_SENDER_DOMAIN_NOT_AVAILABLE",
  "E_SENDER_DOMAIN_NOT_CONFIGURED",
  "E_EMAIL_SENDING_NOT_READY",
  "E_RECIPIENT_NOT_ALLOWED",
  "E_RECIPIENT_PLAN_RESTRICTED",
  "E_RECIPIENT_SUPPRESSED",
  "E_ACCOUNT_SUSPENDED",
  "E_CONTENT_TOO_LARGE",
  "E_DELIVERY_FAILED",
  "E_RATE_LIMIT_EXCEEDED",
  "E_DAILY_LIMIT_EXCEEDED",
  "E_INTERNAL_SERVER_ERROR",
  "E_HEADER_NOT_ALLOWED",
  "E_HEADER_USE_API_FIELD",
  "E_HEADER_VALUE_INVALID",
  "E_HEADER_VALUE_TOO_LONG",
  "E_HEADER_NAME_INVALID",
  "E_HEADERS_TOO_LARGE",
  "E_HEADERS_TOO_MANY"
];
const PHASES = new Set([
  "worker_configuration", "rate_limiter", "email_receipt", "email_send",
  "pages_service_binding_missing", "pages_service_binding",
]);
const PRIVATE_MARKER = "PRIVATE_TEST_ERROR_DO_NOT_LOG";

// Uses only local source and injected mocks. No network, email, or file writes.
export async function run({ repoRoot = DEFAULT_REPO_ROOT, requireStructuredLogs = true } = {}) {
  const { default: worker } = await import(pathToFileURL(repoRoot + "/worker/inquiry.mjs").href + "?localAudit=" + Date.now());
  const { onRequest } = await import(pathToFileURL(repoRoot + "/functions/api/inquiry.js").href + "?localAudit=" + Date.now());
  const capturedMessages = [];
  const records = [];
  let guardChecks = 0;
  let loggerChecks = 0;
  const savedConsoleError = console.error;
  console.error = (...args) => records.push(args);

  const payload = {
    kind: "booking", name: "Private Test Person", email: "private-test@example.com",
    service: "studio", package: "essential", location: "Private Test Location",
    preferredDate: "2096-02-29", alternateDate: "",
    message: "Private test project details should never appear in logs.", website: "",
  };
  function environment(overrides = {}) {
    return {
      ALLOWED_ORIGINS: ORIGIN,
      BOOKING_FROM: "bookings@enhancevisualstudio.com",
      EMAIL: { send: async (message) => {
        capturedMessages.push(message);
        return { messageId: "local-test-only" };
      } },
      INQUIRY_LIMITER: { limit: async ({ key }) => {
        assert.equal(key, "192.0.2.41");
        return { success: true };
      } },
      ...overrides,
    };
  }
  function request(body = payload, options = {}) {
    const { headers, ...other } = options;
    return new Request(ORIGIN + "/api/inquiry", {
      method: "POST",
      body: typeof body === "string" ? body : JSON.stringify(body),
      headers: {
        Origin: ORIGIN, "Content-Type": "application/json",
        "CF-Connecting-IP": "192.0.2.41", ...headers,
      },
      ...other,
    });
  }
  function parsedLogs(since) {
    return records.slice(since).map((args) => {
      assert.equal(args.length, 1, "Log exactly one structured JSON value");
      assert.equal(typeof args[0], "string", "Structured log must be JSON text");
      const record = JSON.parse(args[0]);
      assert.equal(record.event, "evs_inquiry_failure");
      assert.ok(PHASES.has(record.phase), "Use a fixed failure phase");
      assert.ok(Object.keys(record).every((key) => ["event", "phase", "code"].includes(key)));
      if (Object.hasOwn(record, "code")) {
        assert.ok(record.code === "UNEXPECTED" || PROVIDER_CODES.includes(record.code));
      }
      return record;
    });
  }
  async function verify(label, response, expectedStatus, start, expectedPhase) {
    assert.equal(response.status, expectedStatus, label);
    assert.equal(response.headers.get("Cache-Control"), "no-store", label);
    const body = await response.json();
    assert.equal(body.ok, expectedStatus === 200, label);
    assert.ok(!JSON.stringify(body).includes(PRIVATE_MARKER), label + " response redaction");
    const logs = parsedLogs(start);
    if (requireStructuredLogs && expectedPhase) {
      assert.ok(logs.some((record) => record.phase === expectedPhase), label + " failure phase");
    }
    guardChecks += 1;
  }

  try {
    const cases = [
      ["booking", payload, {}, 200],
      ["contact", { kind: "contact", name: payload.name, email: payload.email, message: payload.message }, {}, 200],
      ["custom event", { ...payload, service: "events", package: "custom" }, {}, 200],
      ["incompatible event price", { ...payload, service: "events" }, {}, 400],
      ["prototype service", { ...payload, service: "__proto__" }, {}, 400],
      ["bad date", { ...payload, preferredDate: "2097-02-29" }, {}, 400],
      ["duplicate date", { ...payload, alternateDate: payload.preferredDate }, {}, 400],
      ["past date", { ...payload, preferredDate: "2000-01-01" }, {}, 400],
      ["honeypot", { ...payload, website: "bot.example" }, {}, 400],
      ["email header injection", { ...payload, email: "x@example.com\nBcc: x@example.org" }, {}, 400],
      ["invalid field type", { ...payload, name: [] }, {}, 400],
      ["cross origin", payload, { headers: { Origin: "https://example.org" } }, 403],
      ["content type", payload, { headers: { "Content-Type": "text/plain" } }, 415],
      ["bounded stream", JSON.stringify({ ...payload, message: "a".repeat(20000) }), {}, 413],
      ["invalid JSON", "{", {}, 400],
    ];
    for (const [label, body, options, expected] of cases) {
      const start = records.length;
      const response = await worker.fetch(request(body, options), environment());
      await verify(label, response, expected, start);
    }
    const failures = [
      ["missing sender", { BOOKING_FROM: "" }, 503, "worker_configuration"],
      ["missing mail binding", { EMAIL: null }, 503, "worker_configuration"],
      ["missing limiter", { INQUIRY_LIMITER: null }, 503, "worker_configuration"],
      ["rate limited", { INQUIRY_LIMITER: { limit: async () => ({ success: false }) } }, 429],
      ["limiter exception", { INQUIRY_LIMITER: { limit: async () => { throw new Error(PRIVATE_MARKER); } } }, 503, "rate_limiter"],
      ["mail exception", { EMAIL: { send: async () => { throw new Error(PRIVATE_MARKER); } } }, 502, "email_send"],
      ["mail receipt missing", { EMAIL: { send: async () => ({}) } }, 502, "email_receipt"],
    ];
    for (const [label, overrides, expected, phase] of failures) {
      const start = records.length;
      const response = await worker.fetch(request(), environment(overrides));
      await verify(label, response, expected, start, phase);
    }
    const adapterCases = [
      ["adapter method", new Request(ORIGIN + "/api/inquiry"), {}, 405],
      ["adapter missing binding", request(), {}, 503, "pages_service_binding_missing"],
      ["adapter binding exception", request(), { INQUIRY_WORKER: { fetch: async () => { throw new Error(PRIVATE_MARKER); } } }, 503, "pages_service_binding"],
      ["adapter forwarding", request(), { INQUIRY_WORKER: { fetch: (value) => worker.fetch(value, environment()) } }, 200],
    ];
    for (const [label, input, env, expected, phase] of adapterCases) {
      const start = records.length;
      const response = await onRequest({ request: input, env });
      await verify(label, response, expected, start, phase);
    }
    assert.equal(capturedMessages.length, 4);
    assert.equal(capturedMessages[0].to, "hello@enhancevisualstudio.com");
    assert.equal(capturedMessages[0].replyTo, payload.email);
    assert.ok(capturedMessages[0].text.includes("Essential · $200"));
    assert.ok(capturedMessages[2].text.includes("Custom quote"));

    if (requireStructuredLogs) {
      for (const code of [...PROVIDER_CODES, PRIVATE_MARKER, "E_UNDOCUMENTED", null, { unsafe: PRIVATE_MARKER }]) {
        const start = records.length;
        const error = Object.assign(new Error(PRIVATE_MARKER), { code, name: PRIVATE_MARKER });
        const response = await worker.fetch(request(), environment({ EMAIL: { send: async () => { throw error; } } }));
        assert.equal(response.status, 502);
        const logs = parsedLogs(start);
        assert.equal(logs.length, 1, "One log per mail failure");
        assert.equal(logs[0].phase, "email_send");
        assert.equal(logs[0].code, PROVIDER_CODES.includes(code) ? code : "UNEXPECTED");
        loggerChecks += 1;
      }
    }
    const serializedLogs = JSON.stringify(records);
    for (const forbidden of [payload.name, payload.email, payload.location, payload.message, "192.0.2.41", PRIVATE_MARKER]) {
      assert.ok(!serializedLogs.includes(forbidden), "Logs leaked customer or exception data");
    }
    return { guardChecks, loggerChecks, capturedMockEmails: capturedMessages.length, requireStructuredLogs, remoteCalls: 0 };
  } finally {
    console.error = savedConsoleError;
  }
}

const invokedDirectly = typeof process !== "undefined" && process.argv[1] &&
  pathToFileURL(resolve(process.argv[1])).href === import.meta.url;

if (invokedDirectly) {
  try {
    const summary = await run({ repoRoot: process.env.EVS_TEST_ROOT || DEFAULT_REPO_ROOT });
    console.log(JSON.stringify({ ok: true, ...summary }));
  } catch (error) {
    console.error("Inquiry audit failed: " + error.message);
    process.exitCode = 1;
  }
}
