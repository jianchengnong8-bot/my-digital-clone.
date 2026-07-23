import subprocess, sys, os, time, threading, urllib.request, urllib.error, json

os.chdir(r'C:\Users\1\my-digital-clone\backend')

# ---- Start uvicorn ----
cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']
print('[1/4] Starting backend...')
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace', bufsize=1)

started = False
def read():
    global started
    for line in iter(proc.stdout.readline, ''):
        print('  [backend]', line.strip())
        if 'Application startup complete' in line:
            started = True

t = threading.Thread(target=read, daemon=True)
t.start()

deadline = time.time() + 60
while not started and time.time() < deadline:
    if proc.poll() is not None: break
    time.sleep(0.3)

if not started:
    print('FAILED to start backend!')
    proc.terminate()
    sys.exit(1)

print('[2/4] Backend running. Testing health...')
try:
    resp = urllib.request.urlopen('http://localhost:8000/health', timeout=5)
    print('  Health OK:', resp.read().decode()[:200])
except Exception as e:
    print('  Health FAIL:', e)

print('[3/4] Testing chat API (DeepSeek streaming)...')
body = json.dumps({'query': '你好，你叫什么名字？', 'history': []}).encode('utf-8')
req = urllib.request.Request('http://localhost:8000/api/chat', data=body, 
                             headers={'Content-Type': 'application/json'}, method='POST')

try:
    resp = urllib.request.urlopen(req, timeout=60)
    print('  Status:', resp.status)
    full = ''
    while True:
        chunk = resp.readline()
        if not chunk: break
        line = chunk.decode('utf-8', errors='replace').strip()
        if line.startswith('data: '):
            data = line[6:]
            if data == '[DONE]':
                print('\n  [DONE]')
                break
            try:
                obj = json.loads(data)
                if 'token' in obj:
                    full += obj['token']
                if 'sources' in obj:
                    print(f'\n  [Sources: {len(obj["sources"])} results]')
            except:
                pass
    print(f'  Full response: {full[:500]}')
except Exception as e:
    print('  Chat FAIL:', e)

# Cleanup
print('[4/4] Shutting down...')
proc.terminate()
proc.wait(timeout=5)
print('Done!')
