/**
 * AI 对话页
 * 路由: /chat
 */
import type { Metadata } from "next";
import { ChatPanel } from "@/components/chat/ChatPanel";

export const metadata: Metadata = {
  title: "与我对话 — 数字分身",
  description: "通过 AI 对话了解我的性格、爱好和经历",
};

export default function ChatPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="text-center mb-6">
        <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
          与数字分身对话
        </h1>
        <p className="text-zinc-500 dark:text-zinc-400 mt-1 text-sm">
          基于真实性格数据驱动的 AI 回答
        </p>
      </div>
      <ChatPanel />
    </div>
  );
}
