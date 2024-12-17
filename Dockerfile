FROM ubuntu:latest
LABEL authors="musta"

FROM python:3.12

# установка рабочей директории в контейнере
WORKDIR /app

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt /app

# установка зависимостей
RUN pip install -r requirements.txt

# копирование содержимого локальной директории src в рабочую директорию
COPY . /app

EXPOSE 8000

CMD [ "python", "backend/main.py" ]