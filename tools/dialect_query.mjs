// Minimal stdio MCP client for sicilian-dialect-mcp.
// Usage: node dialect_query.mjs <tool_name> '<json args>'
import { spawn } from 'node:child_process';

const [tool, rawArgs = '{}'] = process.argv.slice(2);
const server = spawn('node', ['F:\\Progetti\\sicilian-dialect-mcp\\dist\\server.js'], { stdio: ['pipe', 'pipe', 'inherit'] });
let buf = '';
const pending = new Map();
server.stdout.on('data', (chunk) => {
    buf += chunk.toString('utf8');
    let nl;
    while ((nl = buf.indexOf('\n')) >= 0) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line) continue;
        const msg = JSON.parse(line);
        if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
    }
});
let nextId = 1;
const send = (method, params, isNotification = false) => new Promise((resolve) => {
    const msg = { jsonrpc: '2.0', method, params };
    if (!isNotification) { msg.id = nextId++; pending.set(msg.id, resolve); }
    server.stdin.write(JSON.stringify(msg) + '\n');
    if (isNotification) resolve();
});
await send('initialize', { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'trinacria-cli', version: '1.0.0' } });
await send('notifications/initialized', {}, true);
const res = tool === 'list'
    ? await send('tools/list', {})
    : await send('tools/call', { name: tool, arguments: JSON.parse(rawArgs) });
if (res.result && res.result.content) {
    for (const c of res.result.content) process.stdout.write((c.text ?? JSON.stringify(c)) + '\n');
} else {
    process.stdout.write(JSON.stringify(res.result ?? res.error, null, 2) + '\n');
}
server.kill();
