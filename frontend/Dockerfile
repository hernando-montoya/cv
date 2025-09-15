# Frontend Dockerfile - Fixed version for compatibility
FROM node:16-alpine AS builder

# Build arguments
ARG REACT_APP_BACKEND_URL=http://localhost:8001

# Set working directory
WORKDIR /app

# Install Python and build tools for native dependencies
RUN apk add --no-cache python3 make g++

# Copy package files first
COPY package.json ./

# Clean install without lockfile to resolve version conflicts
RUN rm -f yarn.lock package-lock.json

# Install dependencies with legacy peer deps and ignore engines
RUN yarn install --legacy-peer-deps --ignore-engines --network-timeout 300000

# Copy source code
COPY . .

# Set environment variables for build
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
ENV GENERATE_SOURCEMAP=false
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV CI=true

# Try building with different methods
RUN yarn docker:build || npx react-scripts build || (echo "Build failed" && exit 1)

# Production stage
FROM nginx:alpine

# Install wget for health checks
RUN apk add --no-cache wget

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create directories and set permissions
RUN mkdir -p /var/cache/nginx/client_temp \
    && mkdir -p /var/cache/nginx/proxy_temp \
    && mkdir -p /var/cache/nginx/fastcgi_temp \
    && mkdir -p /var/cache/nginx/uwsgi_temp \
    && mkdir -p /var/cache/nginx/scgi_temp

# Create non-root user
RUN addgroup -g 1001 -S nodejs \
    && adduser -S nextjs -u 1001

# Set ownership but run as root (nginx needs root for port binding)
RUN chown -R nextjs:nodejs /usr/share/nginx/html

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]