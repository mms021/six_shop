# Базовый образ
FROM python:3.10 AS base

# Секция для бэкенда
FROM base AS backend
WORKDIR /app
COPY ./back-end/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./back-end/ .

# Установка supervisor и cron
RUN apt-get update && apt-get install -y supervisor cron

# Создаем директорию для логов и настраиваем права
RUN mkdir -p /var/log/cron && touch /var/log/cron.log && chmod 0666 /var/log/cron.log

# Создаем пользовательский crontab
RUN echo "20 * * * * root python /app/importProducts.py >> /var/log/cron.log 2>&1" > /etc/cron.d/import-products
RUN chmod 0644 /etc/cron.d/import-products

# Создаем конфигурацию supervisor
RUN echo "[supervisord]\nnodaemon=true\nuser=root\n\n[program:cron]\ncommand=cron -f\n\n[program:main]\ncommand=uvicorn main:app --host 0.0.0.0 --port 8080\ndirectory=/app\nuser=root\nautorestart=true\nstartretries=10\nstartsecs=5\nstdout_logfile=/var/log/main.log\nstderr_logfile=/var/log/main.error.log" > /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

# Запускаем supervisor вместо прямого запуска cron
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


# Секция для бота
FROM base AS bot
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

#EXPOSE 7771

# Запуск бота с отключенным буферированием вывода
CMD ["python", "miniappbot.py"]


FROM bot AS final-bot


FROM backend AS final-backend


