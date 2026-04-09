# -----------------------------
# 1) Build VueJS SPA
# -----------------------------
FROM node:25-alpine AS frontend-build

WORKDIR /app

# Install dependencies
COPY spa/package*.json ./spa/
RUN cd spa && npm install

# Build SPA
COPY spa ./spa
RUN cd spa && npm run build


# -----------------------------
# 2) Build Python Backend
# -----------------------------
FROM python:3.13-alpine AS backend-build

WORKDIR /app

# Install build dependencies (if needed for wheels)
RUN apk add --no-cache build-base

# Copy backend code
COPY src ./src

# Copy built SPA into backend static folder
COPY --from=frontend-build /app/spa/dist ./src/static

# Install Python dependencies
COPY src/requirements.txt .
RUN pip install --prefix=/install -r requirements.txt


# -----------------------------
# 3) Minimal Runtime Image
# -----------------------------
FROM python:3.13-alpine AS runtime

WORKDIR /app

# Copy installed Python packages
COPY --from=backend-build /install /usr/local

# Copy backend including static files
COPY --from=backend-build /app/src .

# Expose FastAPI port
EXPOSE 5000

# Start FastAPI app
CMD ["python", "app.py"]
