import sys
deps = ['pgvector', 'supabase', 'sentence_transformers', 'fastapi', 'sqlalchemy', 'openai', 'yaml']
for dep in deps:
    try:
        __import__(dep)
        print(f'OK: {dep}')
    except ImportError:
        print(f'MISSING: {dep}')
