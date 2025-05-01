
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

