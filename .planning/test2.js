const http = require('http');

const req = http.get('http://localhost:8000/health', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log('Backend health:', res.statusCode, data.substring(0, 300));
    });
});
req.on('error', (e) => {
    console.log('Backend NOT running:', e.message);
    console.log('\nNeed to start backend:');
    console.log('  cd backend');
    console.log('  uvicorn app.main:app --reload --port 8000');
});
req.setTimeout(5000, () => { req.destroy(); console.log('TIMEOUT'); });
