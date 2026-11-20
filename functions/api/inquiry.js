// Keep the email and rate-limit bindings in the private EVS Worker.
export async function onRequest({ request, env }) {
  const headers = { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" };
  if (request.method !== "POST") {
    return Response.json({ ok: false, error: "Use POST for inquiries." }, {
      status: 405,
      headers: { ...headers, Allow: "POST" },
    });
  }

  try {
    if (env.INQUIRY_WORKER) return await env.INQUIRY_WORKER.fetch(request);
    console.error(JSON.stringify({ event: "evs_inquiry_failure", phase: "pages_service_binding_missing" }));
  } catch {
    console.error(JSON.stringify({ event: "evs_inquiry_failure", phase: "pages_service_binding" }));
  }

  return Response.json({
    ok: false,
    error: "Online submission is temporarily unavailable. Please email hello@enhancevisualstudio.com.",
  }, { status: 503, headers });
}
