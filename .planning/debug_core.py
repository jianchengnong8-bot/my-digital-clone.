import sys
sys.path.insert(0, r'C:\Users\1\my-digital-clone\backend')

print('1. database...')
from app.core.database import Base
print('   OK')

print('2. orm...')
from app.models.orm import PersonaDimensionORM
print('   OK')

print('3. persona...')
from app.models.persona import ChatRequest
print('   OK')

print('4. config...')
from app.core.config import settings
print('   OK')

print('5. supabase...')
from app.core.supabase_client import get_supabase
print('   OK')

print('All core imports OK!')
