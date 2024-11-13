# Вибираємо базовий образ з Python
FROM python:3.11-slim

# Встановлюємо змінну оточення для коректного відображення повідомлень
ENV PYTHONUNBUFFERED 1

# Встановлюємо робочу директорію для контейнера
WORKDIR /app

# Копіюємо файли вимог і встановлюємо залежності
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіюємо решту коду застосунку в робочу директорію
COPY user /app

# Відкриваємо порт для Django-сервера
EXPOSE 8000

# Команда для запуску Django-сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
