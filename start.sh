#!/bin/bash
export PORT=${PORT:-8080}
echo "Starting server on port $PORT"
gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -