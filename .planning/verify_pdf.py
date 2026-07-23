import os
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
for f in os.listdir(desktop):
    if f.endswith('.pdf'):
        path = os.path.join(desktop, f)
        size = os.path.getsize(path)
        print(f'Found: {f} ({size:,} bytes)')
