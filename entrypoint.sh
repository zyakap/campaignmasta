#!/usr/bin/env bash
set -e

# Apply database migrations before serving.
python manage.py migrate --noinput

# Optionally seed demo data on first boot (set SEED_DEMO=1).
if [ "${SEED_DEMO:-0}" = "1" ]; then
    python manage.py seed_demo || true
fi

# Launch the WSGI server. Honour $PORT (default 8031) and $WEB_CONCURRENCY.
exec gunicorn campaignmasta.wsgi:application \
    --bind "0.0.0.0:${PORT:-8031}" \
    --workers "${WEB_CONCURRENCY:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-60}" \
    --access-logfile - \
    --error-logfile -
