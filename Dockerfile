FROM node:18-alpine

WORKDIR /app

COPY front-end/tg-app-shop/package*.json ./

RUN npm install

COPY front-end/tg-app-shop/ .

EXPOSE 3478

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3478"] 