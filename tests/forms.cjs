#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const { chromium } = require(process.env.EVS_PLAYWRIGHT_MODULE ||
  'playwright');

const BASE_URL = new URL(process.env.EVS_FORM_TEST_URL || 'http://127.0.0.1:8000');
const CHROME = process.env.EVS_CHROME_EXECUTABLE;
const FIXTURE = {
  name: 'Local Form Test',
  email: 'local-form-test@example.invalid',
  location: 'Local test venue',
  message: 'This request exists only inside the local form test.',
};
const SUCCESS_MESSAGE = 'The local test accepted this request.';
const scenarios = [
  { name: 'accepted', status: 200, payload: { ok: true, message: SUCCESS_MESSAGE }, success: true },
  { name: 'unavailable', status: 503, payload: { ok: false, error: 'Local test submission unavailable.' } },
  { name: 'html-200', status: 200, contentType: 'text/html', body: '<!doctype html><title>Static fallback</title>' },
  { name: 'ok-false-200', status: 200, payload: { ok: false, error: 'Local test declined the request.' } },
  { name: 'unconfirmed-200', status: 200, payload: { message: 'Acceptance was omitted.' } },
  { name: 'timeout', timeout: true },
];

if (BASE_URL.protocol !== 'http:' || !['127.0.0.1', 'localhost', '[::1]'].includes(BASE_URL.hostname)) {
  throw new Error('Form tests require a local HTTP server.');
}

async function runScenario(browser, pagePath, scenario) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  let attempts = 0;
  let requestPayload;
  const pageErrors = [];

  try {
    await context.route('**/*', async (route) => {
      const target = new URL(route.request().url());
      if (target.origin !== BASE_URL.origin) {
        await route.abort('blockedbyclient');
        return;
      }
      if (target.pathname !== '/api/inquiry') {
        await route.continue();
        return;
      }
      attempts += 1;
      assert.equal(route.request().method(), 'POST');
      requestPayload = route.request().postDataJSON();
      if (scenario.timeout) return; // The browser's AbortController must end this pending fetch.
      await route.fulfill({
        status: scenario.status,
        contentType: scenario.contentType || 'application/json',
        body: scenario.body || JSON.stringify(scenario.payload),
      });
    });

    const page = await context.newPage();
    page.on('pageerror', (error) => pageErrors.push(error.message));
    await page.clock.install();
    const response = await page.goto(new URL(pagePath, BASE_URL).href, { waitUntil: 'domcontentloaded' });
    assert.equal(response.status(), 200, pagePath + ' must load locally');
    const form = page.locator('.request-form');
    await form.waitFor({ state: 'visible' });
    await page.locator('#name').fill(FIXTURE.name);
    await page.locator('#email').fill(FIXTURE.email);
    await page.locator('#message').fill(FIXTURE.message);
    const booking = pagePath.includes('book');
    await page.locator('#service').selectOption(booking ? 'events' : 'portraits');
    if (booking) {
      await page.locator('#package').selectOption('custom');
      await page.locator('#location').fill(FIXTURE.location);
    }
    const button = form.locator('button[type="submit"]');
    const submittedRequest = page.waitForRequest((request) => new URL(request.url()).pathname === '/api/inquiry' && request.method() === 'POST');
    await button.click();
    await submittedRequest;
    await page.waitForFunction(() => document.querySelector('.form-status').textContent.length > 0);

    if (scenario.timeout) {
      assert.equal(await button.isDisabled(), true, 'Submit stays disabled while pending');
      await page.clock.fastForward(20001);
    }
    await page.waitForFunction(() => {
      const button = document.querySelector('.request-form button[type="submit"]');
      const status = document.querySelector('.form-status');
      return !button.disabled && status.textContent !== 'Sending your request…';
    }, null, { polling: 20, timeout: 5000 });

    assert.equal(attempts, 1, 'Exactly one submission');
    assert.equal(requestPayload.kind, booking ? 'booking' : 'contact');
    assert.equal(requestPayload.name, FIXTURE.name);
    assert.equal(requestPayload.email, FIXTURE.email);
    assert.equal(requestPayload.message, FIXTURE.message);
    assert.equal(requestPayload.website, '');
    assert.equal(requestPayload.service, booking ? 'events' : 'portraits');
    if (booking) {
      assert.equal(requestPayload.package, 'custom');
      assert.equal(requestPayload.location, FIXTURE.location);
    }

    const status = form.locator('.form-status');
    const statusText = await status.textContent();
    assert.equal(await button.isEnabled(), true, 'Submit re-enabled after completion');
    if (scenario.success) {
      assert.equal(statusText, SUCCESS_MESSAGE);
      assert.equal(await status.getAttribute('data-state'), null);
      assert.equal(await page.locator('#name').inputValue(), '');
      assert.equal(await page.locator('#email').inputValue(), '');
      assert.equal(await page.locator('#message').inputValue(), '');
    } else {
      assert.equal(await status.getAttribute('data-state'), 'error');
      assert.notEqual(statusText, SUCCESS_MESSAGE);
      assert.equal(await page.locator('#name').inputValue(), FIXTURE.name);
      assert.equal(await page.locator('#email').inputValue(), FIXTURE.email);
      assert.equal(await page.locator('#message').inputValue(), FIXTURE.message);
      assert.equal(await page.locator('#service').inputValue(), booking ? 'events' : 'portraits');
      if (booking) {
        assert.equal(await page.locator('#location').inputValue(), FIXTURE.location);
        assert.equal(await page.locator('#package').inputValue(), 'custom');
      }
      if (scenario.timeout) {
        assert.match(statusText, /could not be confirmed in time/i);
        assert.match(statusText, /may still have arrived/i);
        assert.match(statusText, /email hello@enhancevisualstudio\.com before sending it again/i);
      }
    }

    // Also proves the completed request's timer cannot overwrite its final status.
    await page.clock.fastForward(60000);
    assert.equal(attempts, 1, 'The form never resends automatically');
    assert.equal(await status.textContent(), statusText, 'Final status stays stable');
    assert.equal(await button.isEnabled(), true);
    assert.deepEqual(pageErrors, [], 'No uncaught page errors');
    return { page: pagePath, scenario: scenario.name, requests: attempts };
  } finally {
    await context.close();
  }
}

async function run() {
  const browser = await chromium.launch({ ...(CHROME ? { executablePath: CHROME } : {}), headless: true });
  const results = [];
  try {
    for (const pagePath of ['/book.html', '/contact.html']) {
      for (const scenario of scenarios) results.push(await runScenario(browser, pagePath, scenario));
    }
  } finally {
    await browser.close();
  }
  return { ok: true, cases: results.length, mockedSubmissions: results.length, remoteEmails: 0, results };
}

module.exports = { run };
if (require.main === module) {
  run().then((summary) => console.log(JSON.stringify(summary))).catch((error) => {
    console.error('Local form audit failed: ' + error.message);
    process.exitCode = 1;
  });
}
