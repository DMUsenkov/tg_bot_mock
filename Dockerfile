FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
RUN pip install --no-cache-dir flask gunicorn

# Копирование файла приложения
COPY app.py .

# Порт для работы приложения
EXPOSE 8080

# Запуск сервера через gunicorn для production-окружения
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]