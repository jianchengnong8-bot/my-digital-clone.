import subprocess, sys
r = subprocess.run([sys.executable, '-m', 'pip', 'install', 'fpdf2'], capture_output=True, text=True, timeout=60)
print(r.stdout[-200:])
print(r.stderr[-200:])
