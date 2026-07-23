"use client";

import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import { ChatBubble } from "./ChatBubble";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Array<{
    table: string;
    name: string;
    description: string;
    similarity: number;
  }>;
}

/**
 * AI 对话面板
 * SSE 流式接收 FastAPI 的 /api/chat 响应
 */
export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [streaming, setStreaming] = useState("");
  const [streamingSources, setStreamingSources] = useState<
    Message["sources"]
  >([]);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streaming]);

  async function send() {
    const query = input.trim();
    if (!query || loading) return;

    setInput("");
    setLoading(true);
    setStreaming("");

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: query,
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          history: messages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let fullContent = "";
      let sources: Message["sources"] = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          if (line === "data: [DONE]") continue;

          try {
            const data = JSON.parse(line.slice(6));
            if (data.token) {
              fullContent += data.token;
              setStreaming(fullContent);
            }
            if (data.sources) {
              sources = data.sources;
              setStreamingSources(sources);
            }
          } catch {
            // 跳过无法解析的行
          }
        }
      }

      // 流结束，写入完整消息
      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: fullContent,
        sources,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setStreaming("");
      setStreamingSources([]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "抱歉，连接出现了一些问题。请稍后重试。",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <div className="flex flex-col h-[600px] max-w-2xl mx-auto">
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-2">
        {messages.length === 0 && !streaming && (
          <div className="text-center text-zinc-400 dark:text-zinc-500 mt-20">
            <p className="text-lg mb-2">👋 你好，我是数字分身</p>
            <p className="text-sm">
              你可以问我关于性格、爱好、经历的任何问题
            </p>
          </div>
        )}

        {messages.map((m) => (
          <ChatBubble key={m.id} {...m} />
        ))}

        {/* 流式渲染中的消息 */}
        {streaming && (
          <ChatBubble
            role="assistant"
            content={streaming}
            streaming
            sources={streamingSources}
          />
        )}

        <div ref={bottomRef} />
      </div>

      {/* 输入框 */}
      <div className="border-t border-zinc-200 dark:border-zinc-800 p-4">
        <div className="flex gap-2 items-end">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="问我任何关于 '我' 的问题..."
            rows={2}
            className="flex-1 resize-none rounded-xl border border-zinc-300 dark:border-zinc-700 bg-transparent px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder:text-zinc-400"
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            className="p-3 rounded-xl bg-indigo-500 text-white hover:bg-indigo-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            aria-label="发送"
          >
            <Send size={18} />
          </button>
        </div>
        <p className="text-xs text-zinc-400 mt-2 text-center">
          按 Enter 发送，Shift + Enter 换行
        </p>
      </div>
    </div>
  );
}
