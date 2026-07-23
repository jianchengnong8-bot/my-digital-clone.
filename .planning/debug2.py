import subprocess, sys, os

os.chdir(r'C:\Users\1\my-digital-clone\backend')

# First check uvicorn version
r = subprocess.run([sys.executable, '-m', 'uvicorn', '--version'], capture_output=True, text=True, timeout=5)
print('uvicorn version:', r.stdout.strip(), r.stderr.strip())

# Try starting uvicorn with more verbose output to see the full error
cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000', '--log-level', 'debug']
print('Command:', ' '.join(cmd))
r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
print('STDOUT:', r2.stdout[:3000])
print('STDERR:', r2.stderr[:3000])
