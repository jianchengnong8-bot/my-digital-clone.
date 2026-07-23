/**
 * 访客反馈 API Route
 * 收集对话的 👍/👎 反馈，写回 FastAPI
 */
import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL =
  process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { conversation_id, feedback } = body;

    if (!conversation_id || !feedback) {
      return NextResponse.json(
        { error: "Missing conversation_id or feedback" },
        { status: 400 }
      );
    }

    if (!["like", "dislike"].includes(feedback)) {
      return NextResponse.json(
        { error: "Feedback must be 'like' or 'dislike'" },
        { status: 400 }
      );
    }

    // 转发到 FastAPI
    const response = await fetch(`${BACKEND_URL}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conversation_id, feedback }),
    });

    return NextResponse.json(await response.json(), {
      status: response.status,
    });
  } catch (error) {
    console.error("Feedback proxy error:", error);
    return NextResponse.json(
      { error: "Backend unreachable" },
      { status: 502 }
    );
  }
}
