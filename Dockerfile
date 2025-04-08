ARG SERVICE_TYPE=frontend

# Выбор нужного образа на основе SERVICE_TYPE
FROM node:18-alpine AS base_image
ONBUILD RUN echo "Неверное значение SERVICE_TYPE"

# Секция для фронтенда
FROM node:18-alpine AS frontend
WORKDIR /app
COPY ./front-end/tg-app-shop/package*.json ./
RUN npm install
COPY ./front-end/tg-app-shop/ ./
#RUN npm run build
EXPOSE 3478
CMD ["npm", "run", "dev"]

# Секция для бэкенда
FROM python:3.10 AS backend
WORKDIR /app
COPY ./back-end/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./back-end/ .


# Установка cron
RUN apt-get update && apt-get install -y cron
# Копирование скрипта и добавление задания в кронтаб
COPY ./back-end/importProducts.py /app/importProducts.py
RUN echo "0 18 * * * python /app/importProducts.py" >> /etc/crontab
EXPOSE 7770
# Запуск cron в фоновом режиме
CMD cron && ./start.sh



# Секция для бота
FROM python:3.10-slim AS bot
WORKDIR /app
COPY ./bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./bot/ ./
CMD ["python", "miniappbot.py"]

# Правильный способ выбора образа
FROM frontend AS final_frontend
FROM backend AS final_backend
FROM bot AS final_bot

# Финальный образ, выбираем нужный образ на основе SERVICE_TYPE
FROM final_${SERVICE_TYPE} AS final 