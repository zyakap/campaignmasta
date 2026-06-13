#!/usr/bin/env bash
set -e

VENV="/root/.local/share/virtualenvs/campaignmasta-ivyJ71lt"
PYTHON="$VENV/bin/python"
MANAGE="$PYTHON /root/campaignmasta/manage.py"
LOG_DIR="/var/log/gunicorn"

echo "==> Creating log directory..."
mkdir -p "$LOG_DIR"

echo "==> Installing/updating dependencies..."
cd /root/campaignmasta && pipenv install --deploy 2>/dev/null || pipenv install

echo "==> Running migrations..."
$MANAGE migrate --noinput

echo "==> Collecting static files..."
$MANAGE collectstatic --noinput

echo "==> Reloading systemd and restarting gunicorn..."
systemctl daemon-reload
systemctl enable campaignmasta
systemctl restart campaignmasta

echo "==> Testing nginx config and reloading..."
nginx -t && systemctl reload nginx

echo "==> Done. Service status:"
systemctl status campaignmasta --no-pager
