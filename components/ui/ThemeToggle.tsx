"use client";

import { useState, useEffect } from "react";
import { Moon, Sun } from "lucide-react";

/**
 * 主题切换按钮
 * 首次加载跟随系统偏好，手动切换覆盖
 */
export function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    setDark(document.documentElement.classList.contains("dark") || mq.matches);
  }, []);

  function toggle() {
    const next = !dark;
    document.documentElement.classList.toggle("dark", next);
    setDark(next);
  }

  return (
    <button
      onClick={toggle}
      className="p-2 rounded-full hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
      aria-label={dark ? "切换到浅色模式" : "切换到深色模式"}
    >
      {dark ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}
