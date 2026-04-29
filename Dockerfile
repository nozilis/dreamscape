FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG SECRET_KEY=dummy-secret-key-for-build
ARG DEBUG=False
ARG DB_HOST=localhost
ARG DB_PORT=5432
ARG DB_NAME=dummy
ARG DB_USER=dummy
ARG DB_PASSWORD=dummy
ARG ALLOWED_HOSTS=*

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "dreamscape_site.wsgi:application", "--bind", "0.0.0.0:8000"]