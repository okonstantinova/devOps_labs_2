# Используем легковесный Alpine-образ
FROM alpine:latest

# Устанавливаем Nginx и необходимые утилиты
RUN apk add --no-cache nginx

# Проверяем, существует ли пользователь nginx, если нет – создаем
RUN getent group nginx || addgroup -S nginx && \
    getent passwd nginx || adduser -S -G nginx nginx

# Создаём необходимые папки и даём права
RUN mkdir -p /var/www/html /var/log/nginx && \
    chown -R nginx:nginx /var/www/html /var/log/nginx

# Копируем наш конфиг nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Открываем порт
EXPOSE 8080

# Запускаем nginx от непривилегированного пользователя
USER nginx
CMD ["nginx", "-g", "daemon off;"]
