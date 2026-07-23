"""
Prompt 加载器 — YAML 模板 + 变量注入

prompts/
├── system/base.yaml       # 基础人设（所有 Agent 共享）
├── routing/classifier.yaml # 意图分类（关键词匹配，不调 LLM）
└── agents/
    ├── persona.yaml       # 性格 Agent
    ├── interest.yaml      # 兴趣 Agent
    └── experience.yaml    # 经历 Agent

变量注入:
  {owner_name} → 农建晟
  {persona_context} → RAG 检索结果拼接
"""
import os
from pathlib import Path

import yaml

# prompts 目录（相对于 backend/）
PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "prompts"

OWNER_NAME = "农建晟"


def _load_yaml(relative_path: str) -> dict:
    """加载 YAML 文件，返回 dict"""
    filepath = PROMPTS_DIR / relative_path
    if not filepath.exists():
        raise FileNotFoundError(f"Prompt 模板不存在: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_raw_text(relative_path: str) -> str:
    """直接读取文件原始文本（当 YAML 解析失败时回退）"""
    filepath = PROMPTS_DIR / relative_path
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def build_system_prompt(persona_context: str) -> str:
    """
    构建完整的 system prompt

    兼容两种 base.yaml 格式：
      A) 有 YAML key 的旧格式 (role:, tone:, format:)
      B) 无 key 的纯文本新格式 (直接作为 system prompt 正文)

    Args:
        persona_context: RAG 检索到的相关人格数据文本
    """
    # 先尝试 YAML 解析，失败则回退为纯文本读取
    try:
        base = _load_yaml("system/base.yaml")
    except Exception:
        base = None

    # 格式 A: YAML 有 role key
    if isinstance(base, dict) and "role" in base:
        prompt = base["role"].strip()
        if "tone" in base:
            prompt += "\n\n" + base["tone"].strip()
        if "format" in base:
            prompt += "\n\n" + base["format"].strip()
    else:
        # 格式 B: 纯文本（无 YAML key，直接当 system prompt）
        prompt = _read_raw_text("system/base.yaml")
        # 去掉 YAML 注释行
        lines = prompt.split("\n")
        content_lines = [l for l in lines if not l.strip().startswith("#")]
        prompt = "\n".join(content_lines).strip()

    # 注入 RAG 检索到的上下文
    if persona_context:
        prompt += (
            "\n\n## 你的真实个人信息（严格据此回答，但用自然语言表达，不要暴露数据来源）\n\n"
            + persona_context
        )

    # 注入聊天风格参考（如果存在）
    style_ref = _load_chat_style()
    if style_ref:
        prompt += "\n\n" + style_ref

    return prompt


def _load_chat_style() -> str:
    """
    加载 data/chat_examples.txt 中的对话风格参考。
    如果文件不存在或为空，返回空字符串。
    """
    filepath = PROMPTS_DIR.parent / "chat_examples.txt"
    if not filepath.exists():
        return ""

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 提取所有「我：」开头的示例
    examples = [
        l.strip()[2:].strip()  # 去掉「我：」前缀
        for l in lines
        if l.strip().startswith("我：") and len(l.strip()) > 3
    ]

    if not examples:
        return ""

    # 最多取 30 条
    examples = examples[:30]

    style_block = "## 你的真实对话风格参考\n"
    style_block += "以下是农建晟本人真实的聊天记录。请严格模仿这种语气、用词习惯、句子长度和标点方式：\n\n"
    for i, ex in enumerate(examples, 1):
        style_block += f"{i}. {ex}\n"

    return style_block.strip()


def build_messages(
    persona_context: str,
    user_query: str,
    history: list[dict] | None = None,
    mode_hint: str = "casual",
) -> list[dict]:
    """
    构建发给 LLM 的完整 messages 数组

    Args:
        persona_context: RAG 检索上下文
        user_query: 用户当前问题
        history: 历史对话 [{"role": "user/assistant", "content": "..."}]
        mode_hint: "professional" | "casual" — 模式提示

    Returns:
        [{"role": "system", "content": "..."}, ...]
    """
    system_prompt = build_system_prompt(persona_context)

    # 注入模式提示（正经模式 vs 真实模式）
    if mode_hint == "professional":
        system_prompt = (
            "【当前模式：正经模式】对方是面试官/老师/长辈级别的对话对象。"
            "保持专业、认真、有分寸。不要用口头禅、不要爆粗、不要太随意。\n\n"
            + system_prompt
        )

    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    # 附加历史对话（最近 6 轮 = 12 条消息）
    if history:
        messages.extend(history[-12:])

    # 当前问题
    messages.append({"role": "user", "content": user_query})

    return messages


# ============================================================
# 意图分类 — 关键词匹配（零 LLM 调用）
# ============================================================
INTENT_KEYWORDS: dict[str, list[str]] = {
    "persona": [
        "性格", "人格", "MBTI", "沟通", "内向", "外向",
        "价值观", "思维", "认知功能", "ISTP", "宜人性",
        "开放性", "尽责性", "情绪稳定", "大五", "性格特征",
        "说话风格", "幽默", "脾气",
    ],
    "interest": [
        "喜欢", "爱好", "兴趣", "音乐", "书", "电影", "推荐",
        "咖啡", "健身", "运动", "编程", "技术", "R&B",
        "喜欢什么", "平时做什么", "业余", "擅长", "技能",
    ],
    "experience": [
        "经历", "为什么", "工作", "实习", "大学", "毕业",
        "职业", "什么时候", "怎么开始", "怎么想到", "之前",
        "以前", "学校", "学习", "专业", "生病", "休学",
        "项目", "计划", "未来", "目标", "当初",
    ],
}
BOUNDARY_KEYWORDS: list[str] = [
    "微信", "电话", "手机号", "地址", "身份证", "密码",
    "银行卡", "账号", "照片", "视频", "裸", "sex",
]


def classify_intent(query: str) -> str:
    """
    对用户问题进行意图分类

    Returns:
        "persona" | "interest" | "experience" | "multi" | "boundary"
    """
    text = query.lower()

    # 1. 先检测越界（小写比较）
    for kw in BOUNDARY_KEYWORDS:
        if kw.lower() in text:
            return "boundary"

    # 2. 计算各意图命中分数（统一小写比较）
    scores: dict[str, int] = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(1 for kw in keywords if kw.lower() in text)

    # 3. 如果有明显优势的单个意图 → 直接返回
    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        return "multi"

    top_intents = [k for k, v in scores.items() if v == max_score]
    if len(top_intents) == 1:
        return top_intents[0]

    # 4. 多个意图并列 → multi
    return "multi"
