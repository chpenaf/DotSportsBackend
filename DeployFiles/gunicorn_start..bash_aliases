#!/bin/bash

NAME="DotSports"                                  # Name of the application
DJANGODIR=/webapps/dotsports/DotSportsBackend             # Django project directory
SOCKFILE=/webapps/dotsports/run/gunicorn.sock  # we will communicte using this unix socket
USER=root                                        # the user to run as
GROUP=root                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=DotSports.settings.prd             # which settings file should Django use
DJANGO_WSGI_MODULE=DotSports.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_SECRET_KEY="django-insecure-94qzkxs#_)xf8)z6kax71aanr)my5&tcgj)b8^pj$#&2w-_-*i"
export EMAIL_HOST_USER="dotsports.noresponder@gmail.com"
export EMAIL_HOST_PASSWORD="Chris.2022"
export FRONTEND_URL="http://localhost:4200/"

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
