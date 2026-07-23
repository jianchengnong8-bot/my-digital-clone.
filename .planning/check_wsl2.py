import subprocess, sys

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return r.stdout, r.stderr, r.returncode
    except Exception as e:
        return '', str(e), -1

print('=== wsl --status ===')
out, err, code = run('wsl --status')
print('stdout:', out[:500])
print('stderr:', err[:500])
print('code:', code)

print('\n=== wsl -l -v ===')
out2, err2, code2 = run('wsl -l -v')
print('stdout:', out2[:500])
print('stderr:', err2[:500])
print('code:', code2)
