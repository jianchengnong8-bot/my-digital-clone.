"""Install missing Python dependencies"""
import subprocess
import sys

packages = ["pgvector", "supabase", "sentence-transformers"]

for pkg in packages:
    print(f"Installing {pkg}...", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  [OK] {pkg}")
    else:
        print(f"  [FAIL] {pkg}: {result.stderr.strip()[:100]}")

print("Done")
