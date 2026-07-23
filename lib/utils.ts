/**
 * 通用工具函数
 */

/** 拼接 class 名，过滤 falsy 值 */
export function cn(...classes: (string | undefined | false | null)[]): string {
  return classes.filter(Boolean).join(" ");
}

/** 格式化日期显示 */
export function formatDate(dateStr: string): string {
  if (dateStr === "未来") return "🔮 未来";
  // "2019-09" → "2019年9月"
  const [year, month] = dateStr.split("-");
  return month ? `${year}年${month}月` : `${year}年`;
}

/** 根据 level (1-5) 返回星级文本 */
export function levelToStars(level: number): string {
  return "⭐".repeat(level) + "☆".repeat(5 - level);
}
