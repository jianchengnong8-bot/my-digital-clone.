"use client";

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";

interface Dimension {
  name: string;
  score: number;
}

interface DimensionRadarProps {
  dimensions: Dimension[];
}

/**
 * 人格维度雷达图
 * 基于 Recharts 实现，直观展示性格各维度的评分
 */
export function DimensionRadar({ dimensions }: DimensionRadarProps) {
  const data = dimensions.map((d) => ({
    dimension: d.name,
    score: d.score * 100, // 0~1 转为 0~100
    fullMark: 100,
  }));

  return (
    <div className="w-full max-w-md mx-auto h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
          <PolarGrid stroke="currentColor" opacity={0.15} />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fontSize: 13, fill: "currentColor" }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={false}
            axisLine={false}
          />
          <Radar
            name="人格画像"
            dataKey="score"
            stroke="#6366f1"
            fill="#6366f1"
            fillOpacity={0.3}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
