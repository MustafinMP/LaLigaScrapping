FROM ubuntu:latest
LABEL authors="musta"

FROM python:3.12

# установка рабочей директории в контейнере
WORKDIR .

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей
RUN pip install -r requirements.txt

# копирование содержимого локальной директории fastapi_app в рабочую директорию
COPY . .

EXPOSE 8000
EXPOSE 4000

CMD [ "python", "backend/main.py" ]