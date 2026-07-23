import sys
sys.path.insert(0, r'C:\Users\1\my-digital-clone\backend')

# Test each import step by step
print('1. Testing pgvector.sqlalchemy...')
try:
    from pgvector.sqlalchemy import Vector
    print('   OK')
except Exception as e:
    print('   FAIL:', e)

print('2. Testing app.core.database...')
try:
    from app.core.database import Base
    print('   OK')
except Exception as e:
    print('   FAIL:', e)

print('3. Testing app.models.orm...')
try:
    from app.models.orm import PersonaDimensionORM
    print('   OK')
except Exception as e:
    print('   FAIL:', type(e).__name__, e)

print('4. Testing app.models.persona...')
try:
    from app.models.persona import ChatRequest
    print('   OK')
except Exception as e:
    print('   FAIL:', type(e).__name__, e)

print('5. Testing full app.main...')
try:
    import app.main
    print('   OK')
except Exception as e:
    print('   FAIL:', type(e).__name__, e)
