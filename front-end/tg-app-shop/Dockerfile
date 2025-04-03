FROM nginx:alpine

COPY ./dist /usr/share/nginx/html

EXPOSE 3478

# Настройка Nginx для прослушивания порта 3478
RUN echo 'server { \
    listen 3478; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"] 