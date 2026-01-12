#!/usr/bin/env bash
set -euo pipefail
echo ">>> startup: running migrations and fixture load"

# Apply migrations
python manage.py migrate --noinput

# Load fixture (ignore if it errors)
python manage.py loaddata RM/fixtures/industry.json || true

# Collect static
python manage.py collectstatic --noinput || true

echo ">>> startup: starting gunicorn"
exec gunicorn RecycleMate.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers=1
