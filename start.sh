#!/bin/bash
gunicorn wsgi:app --bind 0.0.0.0:${PORT:-8000}