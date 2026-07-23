import subprocess, sys, os

os.chdir(r'C:\Users\1\my-digital-clone\backend')

cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']
print('Starting uvicorn (timeout=120s)...')

r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print('STDOUT:', r.stdout[:3000])
print('STDERR:', r.stderr[:3000])
print('Return code:', r.returncode)
