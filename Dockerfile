# Универсальный Dockerfile для всех сервисов
ARG SERVICE_TYPE=frontend

# Секция для фронтенда
FROM node:18-alpine AS frontend
WORKDIR /app
COPY ./front-end/tg-app-shop/package*.json ./
RUN npm install
COPY ./front-end/tg-app-shop/ ./
RUN npm run build
EXPOSE 3478
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3478"]

# Секция для бэкенда
FROM node:18-alpine AS backend
WORKDIR /app
COPY ./back-end/package*.json ./
RUN npm install
COPY ./back-end/ ./
EXPOSE 7770
CMD ["npm", "start"]

# Секция для бота
FROM python:3.10-slim AS bot
WORKDIR /app
COPY ./bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./bot/ ./
CMD ["python", "miniappbot.py"]

# Финальный образ, выбирается на основе SERVICE_TYPE
FROM ${SERVICE_TYPE} AS final 