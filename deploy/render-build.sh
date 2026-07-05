#!/usr/bin/env bash
# Render build script: install, collect static, migrate.
# Optionally creates the first admin user when DJANGO_SUPERUSER_* env vars are set.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]]; then
    python manage.py createsuperuser --noinput || true
fi
