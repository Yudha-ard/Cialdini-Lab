# Multi-stage build for optimized production
# UPDATE: Menggunakan node:20-alpine karena react-router-dom v7 butuh Node >= 20
FROM node:20-alpine AS builder

WORKDIR /app/frontend

# Copy package files
# Karena context build nanti adalah folder ./frontend, kita tidak perlu prefix 'frontend/' lagi
COPY package.json yarn.lock* ./

# Install dependencies
RUN yarn install --frozen-lockfile --production=false

# Copy source code
COPY . .

# Build for production
RUN yarn build

# Production stage
FROM nginx:alpine

# Copy build files
# Path sumber tetap dari /app/frontend/build (di dalam container builder)
COPY --from=builder /app/frontend/build /usr/share/nginx/html

# Copy nginx config (Langsung inject konfigurasi di sini)
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen 3000;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Proxy ke backend container
    location /api {
        # Pastikan nama host sesuai dengan nama service di docker-compose (backend)
        proxy_pass http://backend:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]