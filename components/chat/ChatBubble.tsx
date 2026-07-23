"use client";

import ReactMarkdown from "react-markdown";

interface ChatBubbleProps {
  role: "user" | "assistant";
  content: string;
  streaming?: boolean;
  sources?: Array<{
    table: string;
    name: string;
    description: string;
    similarity: number;
  }>;
}

/**
 * 对话气泡组件
 * 支持 Markdown 渲染和来源引用折叠展示
 */
export function ChatBubble({
  role,
  content,
  streaming = false,
  sources,
}: ChatBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div className="group max-w-[80%]">
        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
            isUser
              ? "bg-indigo-500 text-white rounded-br-md"
              : "bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 rounded-bl-md"
          } ${streaming ? "animate-pulse" : ""}`}
        >
          {isUser ? (
            <p>{content}</p>
          ) : (
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* 来源引用 — 仅 AI 回答且非流式中显示 */}
        {!isUser && !streaming && sources && sources.length > 0 && (
          <details className="mt-1 text-xs text-zinc-400 dark:text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity">
            <summary className="cursor-pointer hover:text-zinc-600 dark:hover:text-zinc-300">
              查看引用来源 ({sources.length})
            </summary>
            <ul className="mt-1 space-y-0.5 pl-4">
              {sources.map((s, i) => (
                <li key={i}>
                  [{s.table}] {s.name} — 相似度 {(s.similarity * 100).toFixed(0)}%
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </div>
  );
}
