import subprocess, sys, os, time, threading

os.chdir(r'C:\Users\1\my-digital-clone\backend')

cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']
print('Starting uvicorn...')

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    errors='replace',
    bufsize=1,
)

output = []
started = False

def read_output():
    global started
    for line in iter(proc.stdout.readline, ''):
        output.append(line)
        print(line, end='', flush=True)
        if 'Uvicorn running' in line or 'started server process' in line.lower():
            started = True

t = threading.Thread(target=read_output, daemon=True)
t.start()

# Wait up to 120 seconds for startup
deadline = time.time() + 120
while not started and time.time() < deadline:
    if proc.poll() is not None:
        break
    time.sleep(0.5)

if started:
    print('\n=== SERVER IS RUNNING ===')
    # Keep running for a few seconds then kill
    time.sleep(2)
elif proc.poll() is not None:
    print('\n=== SERVER DIED (code=%d) ===' % proc.returncode)
else:
    print('\n=== SERVER STARTUP TIMED OUT ===')
    print('Last 10 lines:')
    for line in output[-10:]:
        print('  ' + line.rstrip())

proc.terminate()
proc.wait(timeout=5)
