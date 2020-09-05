#!/bin/bash

if [ -z $WORKERS ]; then
    WORKERS=4
fi


if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    gunicorn -b 0.0.0.0 matching:app -w $WORKERS --worker-class gevent --reload --log-level=DEBUG --timeout 240
else
    gunicorn -b 0.0.0.0 matching:app -w $WORKERS --worker-class gevent 
fi