import subprocess, sys, os

os.chdir(r'C:\Users\1\my-digital-clone\backend')

# Try just uvicorn --help first to check it works
cmd = [sys.executable, '-m', 'uvicorn', '--help']
r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
print('uvicorn --help OK' if r.returncode == 0 else f'uvicorn --help FAILED: {r.returncode}')

# Now try to import and run directly - this gives better error messages
cmd2 = [sys.executable, '-c', 'import uvicorn; uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info")']
print('\nTrying direct run...')
r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=15, cwd=r'C:\Users\1\my-digital-clone\backend')
print('STDOUT:', r2.stdout[:2000])
print('STDERR:', r2.stderr[:2000])
print('Return code:', r2.returncode)
