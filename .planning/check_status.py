import subprocess

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='gbk', errors='replace', timeout=30)
        return r.stdout.strip()
    except:
        return 'N/A'

# Check features via PowerShell (no admin needed)
print('=== VirtualMachinePlatform ===')
r = subprocess.run(
    'powershell -Command "Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform | Select-Object State"',
    shell=True, capture_output=True, text=True, timeout=30
)
print(r.stdout.strip())

print('\n=== WSL Subsystem ===')
r2 = subprocess.run(
    'powershell -Command "Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux | Select-Object State"',
    shell=True, capture_output=True, text=True, timeout=30
)
print(r2.stdout.strip())

print('\n=== Docker ===')
print(run('where docker 2>nul') or 'Not found')
print(run('docker --version 2>nul') or 'Not installed')

print('\n=== WSL ===')
print(run('where wsl 2>nul') or 'Not found')
print(run('wsl --version 2>nul') or 'Not installed')
