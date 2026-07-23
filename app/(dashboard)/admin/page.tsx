/**
 * 后台管理首页 — 数据概览
 * 路由: /admin
 */
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "管理后台 — 数字分身",
};

export default function AdminPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-6">
        管理后台
      </h1>

      {/* 数据看板占位 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {[
          { label: "人格维度", value: "5", sub: "五大人格 + MBTI" },
          { label: "兴趣爱好", value: "6", sub: "覆盖 4 个类别" },
          { label: "人生事件", value: "5", sub: "关键时间节点" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-zinc-200 dark:border-zinc-800 p-4"
          >
            <p className="text-sm text-zinc-500">{stat.label}</p>
            <p className="text-3xl font-bold text-zinc-900 dark:text-zinc-100 mt-1">
              {stat.value}
            </p>
            <p className="text-xs text-zinc-400 mt-1">{stat.sub}</p>
          </div>
        ))}
      </div>

      <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 text-center text-zinc-400">
        更多管理功能即将上线：数据编辑、Prompt 调优、访客分析
      </div>
    </div>
  );
}
