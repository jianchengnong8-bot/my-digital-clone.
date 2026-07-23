/**
 * 后台管理路由组布局
 * 侧边栏 + 内容区
 */
import Link from "next/link";

const SIDEBAR_ITEMS = [
  { href: "/admin", label: "概览", icon: "📊" },
  { href: "/admin/persona", label: "人格数据", icon: "🧠" },
  { href: "/admin/prompts", label: "Prompt 管理", icon: "📝" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-[calc(100vh-3.5rem)]">
      {/* 侧边栏 */}
      <aside className="w-56 border-r border-zinc-200 dark:border-zinc-800 p-4 flex-shrink-0">
        <nav className="space-y-1">
          {SIDEBAR_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      {/* 内容区 */}
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
