# Dockerfile from https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /code/

CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --preload
