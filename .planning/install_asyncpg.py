import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'asyncpg'], capture_output=True, text=True, timeout=120)
print('STDOUT:', result.stdout[-500:])
print('STDERR:', result.stderr[-500:])
print('Return:', result.returncode)
