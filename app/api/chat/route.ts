/**
 * Chat API Route — BFF 代理层
 * 前端 → /api/chat (Next.js) → FastAPI /api/chat
 * 透传流式 SSE 响应，解决跨域问题
 */
import { NextRequest } from "next/server";

const BACKEND_URL =
  process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  const body = await request.json();

  try {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return new Response(
        JSON.stringify({ error: "Backend request failed" }),
        {
          status: response.status,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    // 透传流式 SSE 响应
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    });
  } catch (error) {
    console.error("Chat proxy error:", error);
    return new Response(
      JSON.stringify({ error: "Backend unreachable" }),
      {
        status: 502,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}
