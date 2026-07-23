import sys, os
sys.path.insert(0, 'C:\\Users\\1\\my-digital-clone\\backend')
from app.core.config import settings
print('Supabase URL:', settings.supabase_url)
print('LLM Provider:', settings.llm_provider)
print('DeepSeek Key:', 'SET' if settings.deepseek_api_key else 'NOT SET')
print('Config OK')
