#!/usr/bin/env bash
# Render build script: install, collect static, migrate.
# While DJANGO_SUPERUSER_* env vars are set, ensures that admin account exists
# and matches the configured password. Remove the vars once you've logged in.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': os.environ.get('DJANGO_SUPERUSER_EMAIL', '')},
)
user.is_staff = True
user.is_superuser = True
user.set_password(os.environ['DJANGO_SUPERUSER_PASSWORD'])
user.save()
print(f"Superuser {'created' if created else 'password reset'}: {username}")
PY
fi
