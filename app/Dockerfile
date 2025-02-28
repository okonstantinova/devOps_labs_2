# --- Этап 1: Сборка ---
FROM node:18-alpine AS builder 

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json package-lock.json ./
RUN npm install --only=production && npm cache clean --force

# Копируем исходный код
COPY . .

# Собираем приложение (если требуется)
RUN npm run build

# --- Этап 2: Запуск приложения ---
FROM node:18-alpine  

WORKDIR /app

# Копируем собранное приложение из builder
COPY --from=builder /app /app

# Создаём непривилегированного пользователя
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app

# Запускаем контейнер от непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 3000

# Запускаем сервер
CMD ["node", "server.js"]
