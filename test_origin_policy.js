const assert = require('assert');
const { spawn } = require('child_process');
const https = require('https');

async function makeRequest(headers, method = 'POST') {
  return new Promise((resolve) => {
    const req = https.request('https://localhost:8443/ping', {
      method,
      headers,
      rejectUnauthorized: false
    }, (res) => {
      resolve(res.statusCode);
    });
    req.on('error', () => resolve(500));
    req.end();
  });
}

async function runTests() {
  console.log("Testing origin policies (POST & OPTIONS)...");
  let passed = 0;
  let total = 0;

  async function testCase(name, headers, method, expected) {
    total++;
    const status = await makeRequest(headers, method);
    if (status === expected) {
      console.log(`[PASS] ${name}`);
      passed++;
    } else {
      console.log(`[FAIL] ${name} (Expected ${expected}, Got ${status})`);
    }
  }

  // POST Tests
  await testCase('Authorized origin (POST)', { 'Origin': 'https://localhost:8443' }, 'POST', 200);
  await testCase('Malicious origin (POST)', { 'Origin': 'https://evil.com' }, 'POST', 403);
  await testCase('Deceptive subdomain (POST)', { 'Origin': 'https://microsoft.com.evil.com' }, 'POST', 403);
  await testCase('Missing origin (POST)', {}, 'POST', 200);
  await testCase('Null origin without API key (POST)', { 'Origin': 'null' }, 'POST', 403);
  await testCase('Null origin with API key (POST)', { 'Origin': 'null', 'x-api-key': 'valid-key-12345' }, 'POST', 200);

  // OPTIONS Tests
  await testCase('Authorized origin (OPTIONS)', { 'Origin': 'https://localhost:8443' }, 'OPTIONS', 200);
  await testCase('Malicious origin (OPTIONS)', { 'Origin': 'https://evil.com' }, 'OPTIONS', 403);
  await testCase('Missing origin (OPTIONS)', {}, 'OPTIONS', 200);
  await testCase('Null origin without API key (OPTIONS)', { 'Origin': 'null' }, 'OPTIONS', 200);

  console.log(`\nTests completed: ${passed}/${total} passed.`);
  if (passed !== total) process.exit(1);
}

const proxy = spawn('node', ['.office-addin-dev-certs/.app/proxy-cors.js']);

setTimeout(() => {
  runTests().then(() => {
    proxy.kill();
  });
}, 2000);
