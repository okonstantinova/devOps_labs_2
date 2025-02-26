# Используем легковесный образ Python на базе Alpine
FROM python:3.11-alpine

# Создаем непривилегированного пользователя
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Устанавливаем зависимости системы
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Устанавливаем права доступа для пользователя
RUN chown -R appuser:appgroup /app

# Запускаем контейнер от непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "main.py"]

