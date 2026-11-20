import { catalog } from "../assets/booking-catalog.mjs";

const INBOX = "hello@enhancevisualstudio.com";
const MAX_BYTES = 16 * 1024;

const EMAIL_ERROR_CODES = new Set([
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
]);

function logFailure(phase, error) {
  const receivedCode = error?.code;
  const code = EMAIL_ERROR_CODES.has(receivedCode) ? receivedCode : "UNEXPECTED";
  console.error(JSON.stringify({ event: "evs_inquiry_failure", phase, code }));
}

function reply(status, payload, extra = {}) {
  return Response.json(payload, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", ...extra },
  });
}

function failure(status, error, extra) {
  return reply(status, { ok: false, error }, extra);
}

async function readPayload(request) {
  const reader = request.body?.getReader();
  if (!reader) throw new SyntaxError("Empty body");
  const buffer = new Uint8Array(MAX_BYTES);
  let size = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      if (size + value.byteLength > MAX_BYTES) {
        await reader.cancel();
        throw new RangeError("Request too large");
      }
      buffer.set(value, size);
      size += value.byteLength;
    }
  } finally {
    reader.releaseLock();
  }
  return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(buffer.subarray(0, size)));
}

function validDate(value, today) {
  if (value === "") return true;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value) || value < today) return false;
  const date = new Date(value + "T12:00:00Z");
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

function validate(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { error: "Enter the requested project details and try again." };
  }

  const fields = {
    kind: 16, name: 120, email: 254, service: 64, package: 48, message: 3000,
    location: 200, preferredDate: 10, alternateDate: 10, website: 200,
  };
  const data = {};
  for (const [key, limit] of Object.entries(fields)) {
    const value = Object.hasOwn(input, key) ? input[key] : "";
    if (typeof value !== "string" || value.length > limit ||
        (key === "message" ? /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/ : /[\x00-\x1F\x7F]/).test(value)) {
      return { error: "One or more fields contain invalid characters or exceed the allowed length." };
    }
    data[key] = value.trim();
  }

  if (data.website || !["booking", "contact"].includes(data.kind)) {
    return { error: "This request could not be accepted." };
  }
  if (!data.name || !/^[^\s@<>(),:;"\x00-\x1F]+@[a-z\d-]+(?:\.[a-z\d-]+)+$/i.test(data.email) ||
      data.message.length < 10) {
    return { error: "Enter a name, valid email address and a message of at least 10 characters." };
  }
  if (data.service && !Object.hasOwn(catalog.services, data.service)) {
    return { error: "Choose a service from the list." };
  }

  if (data.kind === "booking") {
    if (!data.service || !data.location) return { error: "Choose a service and enter the project location." };
    const available = catalog.packageServices[data.service] || [];
    if (data.package !== "custom" && !available.includes(data.package)) {
      return { error: "Choose a package available for this service or request a custom quote." };
    }
    const components = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(new Date());
    const { year, month, day } = Object.fromEntries(components.map(({ type, value }) => [type, value]));
    const today = year + "-" + month + "-" + day;
    if (!validDate(data.preferredDate, today) || !validDate(data.alternateDate, today)) {
      return { error: "Use valid dates on or after today." };
    }
    if (data.preferredDate && data.preferredDate === data.alternateDate) {
      return { error: "Choose different preferred and alternate dates." };
    }
  }

  return { data };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/inquiry") return failure(404, "Endpoint not found.");
    if (request.method !== "POST") return failure(405, "Use POST for inquiries.", { Allow: "POST" });

    const origins = (env.ALLOWED_ORIGINS || "").split(",").map((origin) => origin.trim());
    if (!origins.includes(url.origin) || request.headers.get("Origin") !== url.origin) {
      return failure(403, "Submit requests from the Enhance Visual Studio website.");
    }
    if (request.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase() !== "application/json") {
      return failure(415, "Use JSON to submit this request.");
    }
    if (Number(request.headers.get("Content-Length")) > MAX_BYTES) {
      return failure(413, "This request is too large.");
    }

    const unavailable = "Online submission is temporarily unavailable. Please email " + INBOX + ".";
    const ip = request.headers.get("CF-Connecting-IP");
    if (!ip || !env.BOOKING_FROM || typeof env.EMAIL?.send !== "function" ||
        typeof env.INQUIRY_LIMITER?.limit !== "function") {
      logFailure("worker_configuration");
      return failure(503, unavailable);
    }

    try {
      const { success } = await env.INQUIRY_LIMITER.limit({ key: ip });
      if (!success) return failure(429, "Too many requests. Please wait a minute and try again.", { "Retry-After": "60" });
    } catch (error) {
      logFailure("rate_limiter", error);
      return failure(503, unavailable);
    }

    let input;
    try {
      input = await readPayload(request);
    } catch (error) {
      if (error instanceof RangeError) return failure(413, "This request is too large.");
      return failure(400, "This request could not be read.");
    }

    const { data, error } = validate(input);
    if (error) return failure(400, error);

    const booking = data.kind === "booking";
    const subject = booking ? "New Enhance Visual Studio booking request" : "New Enhance Visual Studio inquiry";
    const lines = [
      subject, "", "Name: " + data.name, "Email: " + data.email,
      "Service: " + (catalog.services[data.service] || "General inquiry"),
    ];
    if (booking) lines.push(
      "Package: " + catalog.packages[data.package],
      "Location: " + data.location,
      "Preferred date: " + (data.preferredDate || "Not provided"),
      "Alternate date: " + (data.alternateDate || "Not provided"),
    );
    lines.push("", data.message);

    try {
      const receipt = await env.EMAIL.send({
        from: env.BOOKING_FROM,
        to: INBOX,
        replyTo: data.email,
        subject,
        text: lines.join("\n"),
      });
      if (!receipt?.messageId) {
        logFailure("email_receipt");
        return failure(502, "Delivery could not be confirmed. Please email " + INBOX + ".");
      }
    } catch (error) {
      logFailure("email_send", error);
      return failure(502, "Delivery could not be confirmed. Please email " + INBOX + ".");
    }

    return reply(200, {
      ok: true,
      message: booking
        ? "Your request was sent. The studio will reply by email to discuss availability and next steps."
        : "Your inquiry was sent. The studio will reply to the email address you provided.",
    });
  },
};
