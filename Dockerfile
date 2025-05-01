
# Секция для фронтенда
FROM node:18-alpine AS frontend
WORKDIR /app
# Копируем только package.json сначала
COPY ./front-end/tg-app-shop/package*.json ./
RUN npm install
# Копируем остальные файлы
COPY ./front-end/tg-app-shop/ ./
# Устанавливаем переменные окружения для сборки
ENV NODE_ENV=production
# Собираем приложение
RUN npm run build
# Установка express для продакшн-сервера
RUN npm install express
EXPOSE 3478
CMD ["node", "server.js"] 



# Секция для бэкенда
FROM python:3.10 AS backend
WORKDIR /app
COPY ./back-end/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./back-end/ .

# Установка supervisor и cron
RUN apt-get update && apt-get install -y supervisor cron

# Добавляем задание в crontab
RUN echo "5 * * * * python /app/importProducts.py >> /var/log/cron.log 2>&1" > /etc/crontab

# Создаем конфигурацию supervisor
RUN echo "[supervisord]\nnodaemon=true\nuser=root\n\n[program:cron]\ncommand=cron -f\n\n[program:main]\ncommand=python main.py\ndirectory=/app\nuser=root\nautorestart=true\nstartretries=10\nstartsecs=5\nstdout_logfile=/var/log/main.log\nstderr_logfile=/var/log/main.error.log" > /etc/supervisor/conf.d/supervisord.conf

EXPOSE 7770

# Запускаем supervisor вместо прямого запуска cron
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


# Секция для бота
FROM python:3.10-slim AS bot
WORKDIR /app
# Установка необходимых системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY ./bot/ ./

# Запуск бота с отключенным буферированием вывода
CMD ["python", "miniappbot.py"]


FROM backend AS final_backend
FROM bot AS final_bot
