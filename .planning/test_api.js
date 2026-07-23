const http = require('http');

function test(url, path) {
    return new Promise((resolve) => {
        const req = http.get(url + path, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                console.log(`=== ${path} ===`);
                console.log('Status:', res.statusCode);
                console.log('Body:', data.substring(0, 500));
                resolve({ status: res.statusCode, body: data });
            });
        });
        req.on('error', (e) => {
            console.log(`=== ${path} ===`);
            console.log('ERROR:', e.message);
            resolve({ status: 0, body: e.message });
        });
        req.setTimeout(5000, () => {
            req.destroy();
            console.log(`=== ${path} ===`);
            console.log('ERROR: timeout');
            resolve({ status: 0, body: 'timeout' });
        });
    });
}

async function main() {
    // Test backend health
    await test('http://localhost:8000', '/health');
    await test('http://localhost:8000', '/');
    
    // Test frontend
    await test('http://localhost:3000', '/');
    
    // Test chat API with a real question
    console.log('\n=== Testing Chat API ===');
    const body = JSON.stringify({
        query: '你好，请问你叫什么名字？',
        history: []
    });
    
    const req = http.request('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
        timeout: 30000
    }, (res) => {
        console.log('Status:', res.statusCode);
        let data = '';
        res.on('data', chunk => {
            const text = chunk.toString();
            process.stdout.write(text);
            data += text;
        });
        res.on('end', () => {
            console.log('\n=== Chat END ===');
        });
    });
    req.on('error', (e) => console.log('Chat ERROR:', e.message));
    req.write(body);
    req.end();
}

main();
