import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from supabase import create_client
from app.core.config import settings
from app.retrieval.embedder import EmbeddingService

supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
embedder = EmbeddingService()

def test_search(query, top_k=3):
    print(f'\n=== Query: {query} ===')
    query_vec = embedder.embed_query(query)
    
    for rpc_name in ['match_persona_dimensions', 'match_interests', 'match_life_events']:
        resp = supabase.rpc(rpc_name, {
            'query_embedding': query_vec,
            'match_threshold': 0.3,
            'match_count': top_k,
        }).execute()
        if resp.data:
            for r in resp.data:
                sim = r['similarity']
                label = r.get('label_text', r.get('title', ''))
                source = r['source_type']
                content = r['content_text'][:80]
                print(f'  [{source}] {label} (sim={sim:.2f}): {content}...')
        else:
            print(f'  {rpc_name}: no results')

test_search('你喜欢什么音乐？')
test_search('你的性格怎么样？')
test_search('你以前经历过什么重要的事情？')

print('\n=== All tests done ===')
