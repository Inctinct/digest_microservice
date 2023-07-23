FROM python:3.11

ENV PYTHONBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD=12345Ad@
ENV DJANGO_SETTINGS_MODULE=settings.settings

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

