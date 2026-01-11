FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libsndfile1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements then install (cache-friendly)
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# set Django settings env var if you rely on it; change if different
ENV DJANGO_SETTINGS_MODULE=RecycleMate.settings

# collect static (ignore failure if STATIC not configured)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn RecycleMate.wsgi:application --bind 0.0.0.0:$PORT --workers 3"]

