"""
Start FastAPI backend and test the full chat pipeline.
"""
import subprocess
import sys
import time
import threading
import json
import urllib.request
import urllib.error

os_module = __import__('os')

# Change to backend directory
os_module.chdir(r'C:\Users\1\my-digital-clone\backend')

# Start uvicorn with explicit args (no empty strings)
cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']
print('Starting:', ' '.join(cmd))

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding='utf-8',
    errors='replace',
    bufsize=1,
)

# Capture startup output
lines = []
def reader():
    for line in iter(proc.stdout.readline, ''):
        lines.append(line.strip())
        print('[uvicorn]', line.strip())
        if len(lines) > 5:
            break

t = threading.Thread(target=reader, daemon=True)
t.start()

# Wait for startup
time.sleep(6)

# Check if process died
if proc.poll() is not None:
    print('\n=== uvicorn FAILED (process exited with code', proc.returncode, ') ===')
    for line in lines:
        print('  ', line)
    sys.exit(1)

print('\n=== Testing chat API ===')

# Test chat
body = json.dumps({'query': '你好，请问你叫什么名字？', 'history': []}).encode('utf-8')
req = urllib.request.Request(
    'http://localhost:8000/api/chat',
    data=body,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    resp = urllib.request.urlopen(req, timeout=30)
    print('Status:', resp.status)
    print('Response:')
    chunk = resp.read(1024).decode('utf-8', errors='replace')
    print(chunk)
except urllib.error.URLError as e:
    print('Chat FAILED:', e)
except Exception as e:
    print('Chat ERROR:', e)

# Shutdown
print('\nDone. Shutting down...')
proc.terminate()
proc.wait(timeout=5)
