# -*- coding: utf-8 -*-
"""
初始化 Supabase 数据库：
1. 创建表 (persona_dimensions, interests, life_events)
2. 创建 pgvector 向量检索 RPC 函数
3. 注入 YAML 数据到数据库
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client
from app.core.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_anon_key)

# ===== 1. 创建表 =====
CREATE_TABLES_SQL = """
-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 人格维度表
CREATE TABLE IF NOT EXISTS persona_dimensions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    score FLOAT NOT NULL,
    description TEXT NOT NULL,
    source VARCHAR(255),
    embedding vector(512),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 兴趣爱好表
CREATE TABLE IF NOT EXISTS interests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    level INTEGER DEFAULT 3,
    keywords JSONB DEFAULT '[]',
    narrative TEXT NOT NULL,
    embedding vector(512),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 人生事件表
CREATE TABLE IF NOT EXISTS life_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    impact TEXT NOT NULL,
    tags JSONB DEFAULT '[]',
    embedding vector(512),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

# ===== 2. 创建 RPC 函数 =====
CREATE_RPCS_SQL = """
CREATE OR REPLACE FUNCTION match_persona_dimensions(
    query_embedding vector(512),
    match_threshold float DEFAULT 0.6,
    match_count int DEFAULT 5
)
RETURNS TABLE(id uuid, label_text text, content_text text, source_type text, similarity float)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT pd.id, pd.name::text, pd.description::text,
           '性格与价值观'::text AS source_type,
           (1 - (pd.embedding <=> query_embedding))::float AS similarity
    FROM persona_dimensions pd
    WHERE pd.embedding IS NOT NULL
      AND 1 - (pd.embedding <=> query_embedding) > match_threshold
    ORDER BY pd.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

CREATE OR REPLACE FUNCTION match_interests(
    query_embedding vector(512),
    match_threshold float DEFAULT 0.6,
    match_count int DEFAULT 5
)
RETURNS TABLE(id uuid, label_text text, content_text text, source_type text, similarity float)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT i.id, i.name::text, i.narrative::text,
           '兴趣爱好'::text AS source_type,
           (1 - (i.embedding <=> query_embedding))::float AS similarity
    FROM interests i
    WHERE i.embedding IS NOT NULL
      AND 1 - (i.embedding <=> query_embedding) > match_threshold
    ORDER BY i.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

CREATE OR REPLACE FUNCTION match_life_events(
    query_embedding vector(512),
    match_threshold float DEFAULT 0.6,
    match_count int DEFAULT 5
)
RETURNS TABLE(id uuid, label_text text, content_text text, source_type text, similarity float)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT le.id, le.title::text, le.impact::text,
           '人生经历'::text AS source_type,
           (1 - (le.embedding <=> query_embedding))::float AS similarity
    FROM life_events le
    WHERE le.embedding IS NOT NULL
      AND 1 - (le.embedding <=> query_embedding) > match_threshold
    ORDER BY le.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
"""

print("Step 1: Creating tables...")
try:
    resp = supabase.rpc('exec_sql', {'sql': CREATE_TABLES_SQL}).execute()
    print("  [OK] Tables created")
except Exception as e:
    if 'function "exec_sql" does not exist' in str(e):
        print("  [!] 'exec_sql' RPC not available - need to run SQL via Supabase Dashboard")
        print("  [!] Please go to https://supabase.com/dashboard and run SQL manually")
        print("  [!] SQL file: backend/supabase_rpc_functions.sql")
    else:
        print(f"  [?] {str(e)[:100]}")

print("\nStep 2: Creating RPC functions...")
try:
    resp = supabase.rpc('exec_sql', {'sql': CREATE_RPCS_SQL}).execute()
    print("  [OK] RPC functions created")
except Exception as e:
    if 'function "exec_sql" does not exist' in str(e):
        print("  [!] Need to run RPC SQL via Supabase Dashboard")
        full_sql = CREATE_TABLES_SQL + "\n" + CREATE_RPCS_SQL
        output_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'setup_all.sql')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_sql)
        print(f"  [!] SQL saved to: {output_path}")
        print(f"  [!] Copy this SQL into Supabase Dashboard -> SQL Editor and run it")
    else:
        print(f"  [?] {str(e)[:100]}")

print("\nDone!")
