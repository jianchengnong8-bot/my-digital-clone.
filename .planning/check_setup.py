# -*- coding: utf-8 -*-
import sys, os

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Fix GBK issue
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# 1. Check Python deps
deps = ['fastapi', 'sqlalchemy', 'pgvector', 'supabase', 'sentence_transformers', 'openai', 'yaml']
print("=== Python Dependency Check ===")
for dep in deps:
    try:
        __import__(dep.replace('-', '_').replace('.', ''))
        print(f"  [OK] {dep}")
    except ImportError:
        print(f"  [FAIL] {dep} - not installed")

# 2. Try to check Supabase tables
print("\n=== Supabase Table Check ===")
try:
    from supabase import create_client
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
    from app.core.config import settings
    
    supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
    
    tables = ['persona_dimensions', 'interests', 'life_events']
    for table in tables:
        try:
            resp = supabase.table(table).select('count', count='exact').limit(0).execute()
            count = getattr(resp, 'count', '?')
            print(f"  [OK] {table} - {count} rows")
        except Exception as e:
            print(f"  [FAIL] {table} - {str(e)[:80]}")
except Exception as e:
    print(f"  [WARN] Connection failed: {str(e)[:100]}")

# 3. Check Supabase RPC functions
print("\n=== Supabase RPC Function Check ===")
try:
    rpc_functions = ['match_persona_dimensions', 'match_interests', 'match_life_events']
    for func in rpc_functions:
        try:
            resp = supabase.rpc(func, {}).execute()
        except Exception as e:
            msg = str(e)
            if 'does not exist' in msg:
                print(f"  [FAIL] {func} - does not exist")
            elif 'function' in msg.lower() and ('argument' in msg.lower() or 'parameter' in msg.lower()):
                print(f"  [OK] {func} - exists")
            elif 'more than one function' in msg:
                print(f"  [OK] {func} - exists (overloaded)")
            else:
                print(f"  [?] {func} - {msg[:80]}")
except Exception as e:
    print(f"  [WARN] RPC check failed: {str(e)[:100]}")

print("\n=== Done ===")
