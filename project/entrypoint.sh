#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z web-db 5432; do
    sleep
done

echo "PostgreSQL started"

exec "$@"
