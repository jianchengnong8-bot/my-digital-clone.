# Next.js Standalone 模式 — 生产构建
# 参考: https://nextjs.org/docs/app/api-reference/config/next-config-js/output

FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# 复制 data/ 目录供服务端读取
COPY --from=builder /app/data ./data

EXPOSE 3000
CMD ["node", "server.js"]
