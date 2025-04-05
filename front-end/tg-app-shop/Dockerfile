FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3478

# Добавляем создание vite.config.js при запуске контейнера
#RUN echo 'import { defineConfig } from "vite"\nimport vue from "@vitejs/plugin-vue"\n\nexport default defineConfig({\n  plugins: [vue()],\n  server: {\n    host: "0.0.0.0",\n    port: 3478,\n    strictPort: true,\n    hmr: {\n      clientPort: 3478\n    },\n    watch: {\n      usePolling: true\n    }\n  }\n})' > vite.config.js

CMD ["npm", "run", "dev"] 