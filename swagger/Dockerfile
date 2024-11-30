# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY src/. /app/.

# Открываем порт для доступа к приложению
EXPOSE 7072

# Запускаем приложение с помощью Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7072"]