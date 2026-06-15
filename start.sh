#!/bin/sh

# stop script immediately if command fails
set -e

alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8000