import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // standalone 模式 — Docker 生产构建
  output: "standalone",

  // 允许从 data/ 目录读取 YAML（服务端）
  serverExternalPackages: ["yaml"],
};

export default nextConfig;
