#!/bin/sh

if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for PostgreSQL database..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 0.1
    done

    echo "PostgreSQL database started"
fi

python manage.py flush --no-input
python manage.py migrate --no-input

exec "$@"