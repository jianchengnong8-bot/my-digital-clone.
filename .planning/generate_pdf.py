# -*- coding: utf-8 -*-
from fpdf import FPDF
import os

# Find Chinese font
def get_font():
    for path in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simsun.ttc','C:/Windows/Fonts/simhei.ttf']:
        if os.path.exists(path): return path
    raise FileNotFoundError('No Chinese font found')

FONT = get_font()

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('CN', '', FONT, uni=True)
        self.add_font('CN', 'B', FONT, uni=True)

    def header(self):
        self.set_font('CN', 'B', 14)
        self.set_text_color(79, 70, 229)
        self.cell(0, 10, 'AI Agent 开发 - 7天学习计划', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(79, 70, 229)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('CN', '', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'第{self.page_no()}页', align='C')

    def stitle(self, title):
        self.set_font('CN', 'B', 12)
        self.set_text_color(79, 70, 229)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def txt(self, text, indent=0):
        self.set_font('CN', '', 9)
        self.set_text_color(50, 50, 50)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5, text)

    def bul(self, text, indent=5):
        self.set_font('CN', '', 9)
        self.set_text_color(50, 50, 50)
        self.set_x(self.l_margin + indent)
        self.cell(4, 5.5, '-')
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent - 4, 5.5, text)

    def day(self, d, title, items):
        self.set_fill_color(79, 70, 229)
        self.set_text_color(255, 255, 255)
        self.set_font('CN', 'B', 11)
        self.cell(self.w - self.l_margin - self.r_margin, 7, f'  {d}: {title}', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)
        for it in items:
            self.bul(it, 3)
        self.ln(3)


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

# ===== 封面 =====
pdf.ln(8)
pdf.set_font('CN', 'B', 24)
pdf.set_text_color(79, 70, 229)
pdf.cell(0, 12, 'AI Agent 开发工程师', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('CN', '', 14)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 10, '7 天学习计划', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(5)
pdf.set_font('CN', '', 9)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 7, '适配岗位：Agent 开发 / LLM 应用开发 / AI 全栈工程师', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 7, '数据来源：Boss 直聘 + 实习僧 2025 年 Agent 开发岗位 JD 汇总', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 7, '难度等级：中级（需要 Python 基础） | 每天 3-5 小时', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(12)

# ===== 一、JD 要求 =====
pdf.stitle('一、招聘岗位 JD 核心技术要求')
pdf.ln(1)
pdf.txt('以下根据 2025 年 Boss 直聘 / 实习僧 AI Agent 开发岗位高频技术词整理，按面试出现频率分级。')
pdf.ln(3)

# Table
pdf.set_font('CN', 'B', 10)
pdf.set_fill_color(220, 38, 38)
pdf.set_text_color(255, 255, 255)
pdf.cell(90, 7, '  必须掌握 (面试必问)', fill=True)
pdf.set_fill_color(217, 119, 6)
pdf.cell(90, 7, '  加分项 (拉开差距)', fill=True, new_x='LMARGIN', new_y='NEXT')

must = [
    'Python 异步编程 (asyncio + FastAPI)',
    'LangChain / LangGraph 框架',
    'OpenAI API / Function Calling',
    'RAG 检索增强生成 (原理+实战)',
    'Prompt Engineering (System/CoT)',
    '向量数据库 (ChromaDB/pgvector)',
    'Docker 容器化部署',
    'Git 版本控制 + RESTful API',
]
good = [
    'CrewAI / AutoGen 多 Agent 协作',
    'MCP 协议 (Model Context Protocol)',
    'LangSmith / 可观测性',
    'LoRA/QLoRA 模型微调',
    'Embedding 模型选型与评估',
    'SSE 流式 / WebSocket 实时通信',
    'RAGAS / LLM 评估体系',
    'CI/CD (GitHub Actions)',
]

for i in range(8):
    pdf.set_font('CN', '', 8)
    pdf.set_text_color(50, 50, 50)
    if i % 2 == 0:
        pdf.set_fill_color(254, 242, 242)
        pdf.cell(90, 6, f'  - {must[i]}', fill=True)
        pdf.set_fill_color(255, 251, 235)
        pdf.cell(90, 6, f'  - {good[i]}', fill=True, new_x='LMARGIN', new_y='NEXT')
    else:
        pdf.cell(90, 6, f'  - {must[i]}')
        pdf.cell(90, 6, f'  - {good[i]}', new_x='LMARGIN', new_y='NEXT')

pdf.ln(8)

# ===== 二、7天计划 =====
pdf.stitle('二、7 天学习计划')
pdf.ln(2)

days = [
    ('第 1 天', 'Python 异步 + FastAPI 基础', [
        '安装 Python 3.10+ 和 VS Code，配置虚拟环境 (venv)',
        '学习 asyncio：async/await、事件循环、Task 并发',
        '搭建第一个 FastAPI 项目：路由、Path/Query 参数、Pydantic 模型',
        '练习：写一个带异步 sleep 模拟耗时操作的 API',
        '输出：一个包含 /health + /echo 的 FastAPI 服务']),
    ('第 2 天', 'LLM API 调用 + Prompt Engineering', [
        '注册 DeepSeek / OpenAI 账号，获取 API Key',
        '用 Python openai 库调用 Chat Completions API',
        '调参实验：temperature、top_p、max_tokens 的效果',
        '学习 Prompt Engineering：System Prompt、Few-shot、Chain-of-Thought',
        '输出：一个命令行聊天机器人，支持多轮对话记忆']),
    ('第 3 天', 'RAG 检索增强生成', [
        '理解 RAG 原理：Embedding → 向量检索 → 上下文注入',
        '安装 ChromaDB，学习文档分块 (chunk_size / overlap)',
        '用 sentence-transformers (BGE 模型) 生成文本向量',
        '搭建完整 RAG 管道：文档摄入 → 语义搜索 → LLM 生成回答',
        '输出：一个能回答"你的简历里写了什么"的 RAG 机器人']),
    ('第 4 天', 'LangChain + Function Calling', [
        '安装 LangChain 和 LangChain-OpenAI',
        '学习核心概念：Chain、Agent、Tool、Memory 的关系',
        '掌握 OpenAI Function Calling：定义 Tool Schema，让 LLM 自主调用',
        '练习：写一个查天气 + 算数学的组合工具调用 Agent',
        '输出：一个能根据用户意图自主选择工具的 Agent']),
    ('第 5 天', 'LangGraph + 多步推理', [
        '理解 Agent 工作流：状态图、条件分支、循环迭代',
        '搭建 LangGraph 图：定义 State、Nodes、Edges、ConditionalEdge',
        '实现 ReAct 模式：Thought → Action → Observation 循环',
        '练习：写一个能拆解复杂问题、分步骤执行的旅游规划 Agent',
        '输出：一个多步骤推理 Agent，每步结果可见']),
    ('第 6 天', '多 Agent 协作 + MCP 协议', [
        '学习多 Agent 架构：Orchestrator 模式 vs 去中心化',
        '用 CrewAI 实现双 Agent 协作：Planner + Writer 分工',
        '了解 MCP (Model Context Protocol)：标准化 Agent-工具连接',
        '了解主流 Agent 框架对比：LangGraph vs CrewAI vs AutoGen vs Dify',
        '输出：一个 Planner + Executor 双 Agent 协作系统']),
    ('第 7 天', '全栈集成 + 项目部署', [
        '搭建 Next.js + FastAPI 的完整全栈 Agent 项目',
        '实现 SSE 流式：前端 EventSource + 后端 StreamingResponse',
        'Docker Compose 编排：前端 + 后端 + 向量数据库一键启动',
        '可选：接入 LangSmith 追踪，观察 Agent 的完整决策链路',
        '输出：一个可演示的 AI Agent 全栈项目，推送到 GitHub']),
]

for d, t, items in days:
    pdf.day(d, t, items)

# ===== 三、推荐项目 =====
pdf.stitle('三、推荐实战项目（可直接放简历）')
pdf.ln(1)
projects = [
    '数字分身 (Digital Clone) — RAG + 多 Agent 编排 + 人格数据驱动对话，全栈项目',
    '智能简历助手 — 上传 PDF 简历，LLM 自动优化措辞，根据 JD 打分匹配',
    '知识库问答系统 — 基于公司内部文档的 RAG 问答，支持引用溯源',
    'Agent 工作流引擎 — LangGraph 搭建可视化 Agent 流程编辑器',
]
for p in projects:
    pdf.bul(p)
pdf.ln(5)

# ===== 四、资源 =====
pdf.stitle('四、推荐学习资源')
pdf.ln(1)
res = [
    'LangChain 官方文档: https://python.langchain.com',
    'LangGraph 教程: https://langchain-ai.github.io/langgraph/',
    'DeepSeek API 文档: https://platform.deepseek.com/api-docs',
    'OpenAI Cookbook: https://cookbook.openai.com',
    'FastAPI 官方中文: https://fastapi.tiangolo.com/zh/',
    'ChromaDB 向量数据库: https://docs.trychroma.com',
    'BGE Embedding: https://huggingface.co/BAAI/bge-small-zh-v1.5',
]
for r in res:
    pdf.set_font('CN', '', 8)
    pdf.set_text_color(79, 70, 229)
    pdf.set_x(pdf.l_margin + 5)
    pdf.cell(w=pdf.w - pdf.l_margin - pdf.r_margin - 5, text=f'- {r}', new_x='LMARGIN', new_y='NEXT')

output = 'C:/Users/1/Desktop/AI_Agent_7天学习计划.pdf'
pdf.output(output)
print(f'Done: {output}')
