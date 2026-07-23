import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "数字分身 — 了解我的性格、爱好与人格",
    template: "%s — 数字分身",
  },
  description:
    "一个基于真实人格数据驱动的数字分身。浏览人格画像、兴趣爱好、人生经历，或与 AI 对话深入了解。",
};

/**
 * 根布局 — 全局 HTML 骨架
 * 字体、暗色模式支持、最小高度全屏
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="zh-CN"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
        {children}
      </body>
    </html>
  );
}
