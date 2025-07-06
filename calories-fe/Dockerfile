# ---- Base image ----
FROM node:20-alpine AS base
WORKDIR /app

# Enable and install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# ---- Builder stage ----
FROM base AS builder

# Copy lock and manifest files
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

# Copy the rest of the source
COPY . .

# Build Next.js app
RUN pnpm build

# ---- Production runner ----
FROM base AS runner

# Install just production deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --prod

# Copy .next and public files from builder
COPY --from=builder /app/.next .next
COPY --from=builder /app/public public
COPY --from=builder /app/node_modules node_modules
COPY --from=builder /app/package.json .
COPY --from=builder /app/next.config.ts .

EXPOSE 3000

CMD ["pnpm", "start"]