#!/bin/sh

# Stops the execution if a command has an error 
set -e

export PORT=${PORT:-8080}

# Setup defaults
export GAPP=${GAPP:-"main:app"}
export GBIND=${GBIND:-"0.0.0.0:$PORT"}
export SETUP=${SETUP:-"/app/devops/setup.sh"}

# Check for 'setup.sh' script
if [ -f $SETUP ]; then
    . $SETUP
fi

# Run the application with gunicorn
exec /usr/local/bin/gunicorn -k uvicorn.workers.UvicornWorker -b $GBIND $GAPP $GARGS
