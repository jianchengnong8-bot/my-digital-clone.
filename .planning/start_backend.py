import subprocess, sys, time, os, threading

os.chdir('C:\\Users\\1\\my-digital-clone\\backend')

# Start uvicorn
proc = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding='utf-8',
    errors='replace',
)

# Wait for startup
print('Starting backend...')
started = False
start_time = time.time()
output_lines = []

def read_output():
    global started
    while True:
        line = proc.stdout.readline()
        if line:
            output_lines.append(line.strip())
            print(line.strip())
            if 'Uvicorn running' in line or 'Application startup complete' in line or 'Started' in line:
                started = True
        elif proc.poll() is not None:
            break

reader = threading.Thread(target=read_output, daemon=True)
reader.start()

time.sleep(8)

# Check if it started
if started or proc.poll() is None:
    print('\n=== Backend should be running. Testing... ===')
    import urllib.request
    try:
        resp = urllib.request.urlopen('http://localhost:8000/health')
        print('Health check:', resp.status, resp.read().decode()[:200])
    except Exception as e:
        print('Health check failed:', e)
else:
    print('\n=== Backend FAILED to start ===')
    for line in output_lines[-10:]:
        print(line)
