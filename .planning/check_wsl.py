import subprocess, sys
# Check Windows version
r = subprocess.run('ver', shell=True, capture_output=True, text=True)
print('Version:', r.stdout.strip())

# Check if Hyper-V / virtualization is available
r2 = subprocess.run('systeminfo', shell=True, capture_output=True, text=True, encoding='gbk', errors='replace')
for line in r2.stdout.split('\n'):
    if any(k in line for k in ['Hyper-V', '虚拟化', 'Virtualization', '固件', 'BIOS']):
        print(line.strip())

# Check if we can enable features via DISM
print('\nChecking DISM...')
r3 = subprocess.run('dism /online /get-features /format:table', shell=True, capture_output=True, text=True, encoding='gbk', errors='replace')
for line in r3.stdout.split('\n'):
    if 'VirtualMachinePlatform' in line or 'WSL' in line or 'Microsoft-Windows-Subsystem-Linux' in line:
        print(line.strip())
