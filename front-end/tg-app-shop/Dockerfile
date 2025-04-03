FROM node:18-alpine

WORKDIR /app

# Копируем только необходимые файлы для сервера
COPY ./public /app/public
COPY ./server.js /app/server.js

# Экспонируем порт 3478
EXPOSE 3478

# Запускаем простой сервер
CMD ["node", "server.js"] 