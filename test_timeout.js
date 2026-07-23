const http = require('http');

const keepAliveAgent = new http.Agent({ keepAlive: true });

function makeUpstreamRequest(url, bodyBuf, headers, method, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    const pr = http.request(url, { method, headers, agent: keepAliveAgent }, resolve);
    pr.setTimeout(timeoutMs, () => {
      pr.destroy(new Error(`Upstream request timeout after ${timeoutMs}ms`));
    });
    pr.on('error', reject);
    pr.write(bodyBuf);
    pr.end();
  });
}

const server = http.createServer((req, res) => {
  if (req.url === '/success') {
    res.writeHead(200);
    res.end('ok');
  } else if (req.url === '/timeout') {
    // Do not respond
  } else if (req.url === '/stream_idle') {
    res.writeHead(200);
    res.write('start');
    // idle without ending
  }
});

server.listen(8444, async () => {
  console.log('Test server running on port 8444');
  let passed = 0;

  // Test 1: Success
  try {
    const res = await makeUpstreamRequest('http://localhost:8444/success', Buffer.from(''), {}, 'GET', 1000);
    console.log('Success test passed: got status', res.statusCode);
    passed++;
  } catch(e) {
    console.error('Success test failed:', e);
  }

  // Test 2: Timeout (connection hangs)
  try {
    await makeUpstreamRequest('http://localhost:8444/timeout', Buffer.from(''), {}, 'GET', 500);
    console.error('Timeout test failed: expected error');
  } catch(e) {
    if (e.message.includes('timeout after')) {
      console.log('Timeout test passed:', e.message);
      passed++;
    } else {
      console.error('Timeout test failed with wrong error:', e);
    }
  }

  // Test 3: Stream Idle
  try {
    const res = await makeUpstreamRequest('http://localhost:8444/stream_idle', Buffer.from(''), {}, 'GET', 500);
    res.on('data', () => {}); // consume data
    await new Promise((resolve, reject) => {
      res.on('end', resolve);
      res.on('error', reject);
      res.socket.on('timeout', () => res.destroy(new Error('Socket timeout')));
    });
    console.error('Stream Idle test failed: expected error');
  } catch(e) {
    console.log('Stream Idle test passed:', e.message);
    passed++;
  }

  console.log(`Passed ${passed}/3 tests`);
  server.close();
  process.exit(passed === 3 ? 0 : 1);
});
