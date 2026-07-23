/**
 * 首页 — 人格画像全景
 * Server Component：服务端直接读取 YAML 数据，SEO 友好
 */
import Link from "next/link";
import type { Metadata } from "next";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { DimensionRadar } from "@/components/chart/DimensionRadar";
import { getPersonaData } from "@/lib/data";
import { formatDate, levelToStars } from "@/lib/utils";

export const metadata: Metadata = {
  title: "数字分身 — 了解我的性格、爱好与人格",
  description:
    "一个基于真实人格数据驱动的数字分身。浏览人格画像、兴趣爱好、人生经历，或与 AI 对话深入了解。",
};

export default async function HomePage() {
  const persona = await getPersonaData();

  return (
    <div className="min-h-screen">
      {/* ======== 首屏 Hero ======== */}
      <section className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
        <ScrollReveal>
          <p className="text-sm font-medium text-indigo-500 mb-3 tracking-wider uppercase">
            Digital Clone
          </p>
          <h1 className="text-4xl md:text-5xl font-bold text-zinc-900 dark:text-zinc-100 mb-4 leading-tight">
            你好，我是农建晟的
            <span className="text-indigo-500">数字分身</span>
          </h1>
          <p className="text-lg text-zinc-500 dark:text-zinc-400 max-w-lg mx-auto mb-8">
            {persona.communication_style.description}
          </p>
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {[
              persona.mbti.type,
              ...persona.mbti.cognitive_functions.slice(0, 2).map((cf) => cf.name),
              persona.communication_style.mode,
            ].map((tag) => (
              <span
                key={tag}
                className="px-3 py-1 rounded-full text-sm bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-800"
              >
                {tag}
              </span>
            ))}
          </div>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-indigo-500 text-white font-medium hover:bg-indigo-600 transition-colors"
          >
            💬 与数字分身对话
          </Link>
        </ScrollReveal>
      </section>

      {/* ======== 人格雷达图 ======== */}
      <section className="max-w-4xl mx-auto px-6 py-16 border-t border-zinc-200 dark:border-zinc-800">
        <ScrollReveal>
          <h2 className="text-2xl font-bold text-center text-zinc-900 dark:text-zinc-100 mb-2">
            人格画像
          </h2>
          <p className="text-center text-zinc-500 dark:text-zinc-400 mb-8 text-sm">
            {persona.mbti.type} · {persona.mbti.description}
          </p>
        </ScrollReveal>
        <DimensionRadar dimensions={persona.dimensions} />
        <ScrollReveal delay={0.2}>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-3 mt-8">
            {persona.dimensions.map((dim) => (
              <div
                key={dim.name}
                className="text-center p-3 rounded-xl bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800"
              >
                <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                  {dim.name}
                </p>
                <p className="text-lg font-bold text-indigo-500">
                  {(dim.score * 100).toFixed(0)}%
                </p>
              </div>
            ))}
          </div>
        </ScrollReveal>
      </section>

      {/* ======== 兴趣爱好 ======== */}
      <section className="max-w-4xl mx-auto px-6 py-16 border-t border-zinc-200 dark:border-zinc-800">
        <ScrollReveal>
          <h2 className="text-2xl font-bold text-center text-zinc-900 dark:text-zinc-100 mb-8">
            兴趣爱好
          </h2>
        </ScrollReveal>
        <div className="space-y-4">
          {persona.interests.map((interest, i) => (
            <ScrollReveal key={interest.name} delay={i * 0.1}>
              <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 hover:border-indigo-300 dark:hover:border-indigo-700 transition-colors">
                {/* 头栏：名称 + 分类 + 热度 */}
                <div className="flex items-center gap-3 mb-3 flex-wrap">
                  <h3 className="font-semibold text-zinc-900 dark:text-zinc-100">
                    {interest.name}
                  </h3>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-800">
                    {interest.category}
                  </span>
                  <span className="text-xs text-zinc-400">
                    {levelToStars(interest.level)}
                  </span>
                </div>

                {/* 正文：完整 narrative */}
                <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                  {interest.narrative}
                </p>

                {/* 关键词标签 */}
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {interest.keywords.map((kw) => (
                    <span
                      key={kw}
                      className="text-xs px-2 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-500"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </section>

      {/* ======== 人生时间线 ======== */}
      <section className="max-w-4xl mx-auto px-6 py-16 border-t border-zinc-200 dark:border-zinc-800">
        <ScrollReveal>
          <h2 className="text-2xl font-bold text-center text-zinc-900 dark:text-zinc-100 mb-8">
            人生轨迹
          </h2>
        </ScrollReveal>
        <div className="relative">
          {/* 时间线竖线 */}
          <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-px bg-zinc-200 dark:bg-zinc-800 md:-translate-x-px" />

          <div className="space-y-8">
            {persona.events.map((event, i) => (
              <ScrollReveal key={event.title} delay={i * 0.1}>
                <div
                  className={`relative flex items-start gap-6 ${
                    i % 2 === 0
                      ? "md:flex-row"
                      : "md:flex-row-reverse"
                  }`}
                >
                  {/* 时间点 */}
                  <div className="absolute left-4 md:left-1/2 w-2 h-2 rounded-full bg-indigo-500 ring-4 ring-white dark:ring-zinc-950 -translate-x-1/2 mt-1.5" />

                  {/* 内容卡片 */}
                  <div
                    className={`ml-10 md:ml-0 md:w-[calc(50%-2rem)] ${
                      i % 2 === 0 ? "md:pr-8 md:text-right" : "md:pl-8"
                    }`}
                  >
                    <p className="text-xs font-medium text-indigo-500 mb-1">
                      {formatDate(event.date)}
                    </p>
                    <h3 className="font-semibold text-zinc-900 dark:text-zinc-100">
                      {event.title}
                    </h3>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
                      {event.impact}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2 justify-start md:justify-end">
                      {event.tags.map((tag) => (
                        <span
                          key={tag}
                          className="text-xs px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-500"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  {/* 对面占位 */}
                  <div className="hidden md:block md:w-[calc(50%-2rem)]" />
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* ======== CTA ======== */}
      <section className="max-w-4xl mx-auto px-6 py-16 border-t border-zinc-200 dark:border-zinc-800 text-center">
        <ScrollReveal>
          <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
            想了解更多？
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400 mb-6">
            直接与我的数字分身对话，问任何你想了解的问题
          </p>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-indigo-500 text-white font-medium hover:bg-indigo-600 transition-colors"
          >
            💬 开始对话
          </Link>
        </ScrollReveal>
      </section>

      {/* ======== 页脚 ======== */}
      <footer className="border-t border-zinc-200 dark:border-zinc-800 py-8 text-center text-sm text-zinc-400">
        <p>
          这是 AI 数字分身，不是本人。如需联系本人，请通过其他渠道。
        </p>
      </footer>
    </div>
  );
}
