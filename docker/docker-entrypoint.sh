#!/bin/bash
# python manage.py migrate      # Apply database migrations
# if [ "$APP_ENV" == "local" ]        # Collect static files on in DEV
# then
#    python manage.py collectstatic --noinput
# fi
python manage.py collectstatic --noinput
# Launch supervisor
/usr/local/bin/supervisord -n
# gunicorn api.wsgi:application --bind 0.0.0.0:8000
