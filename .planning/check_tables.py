import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from supabase import create_client
from app.core.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_anon_key)

# Check tables
tables = ['persona_dimensions', 'interests', 'life_events']
for table in tables:
    try:
        resp = supabase.table(table).select('*', count='exact').limit(1).execute()
        print(f'TABLE {table}: exists (count={getattr(resp, "count", "?")})')
    except Exception as e:
        print(f'TABLE {table}: {str(e)[:120]}')

# Check RPCs
rpc_funcs = ['match_persona_dimensions', 'match_interests', 'match_life_events']
for func in rpc_funcs:
    try:
        supabase.rpc(func, {'query_embedding': [0.0]*512, 'match_threshold': 0.0, 'match_count': 1}).execute()
        print(f'RPC {func}: exists and works')
    except Exception as e:
        print(f'RPC {func}: {str(e)[:120]}')
