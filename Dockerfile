# Multi-stage build for production
FROM node:20-alpine AS builder

WORKDIR /app

# Copy all source files first (node_modules excluded by .dockerignore)
COPY frontend/ ./
COPY items.json ./public/

# Install dependencies (including devDependencies needed for build like TypeScript)
# NODE_ENV is not set to production, so devDependencies will be installed for the build
RUN npm ci

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Install wget for healthcheck
RUN apk add --no-cache wget

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

