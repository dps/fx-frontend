#!/bin/bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_KEY=
export REDIS_DB=0
export PORT=8000
export OER_KEY=4930451afa05443999faa94c9abb1394
gunicorn -b 0.0.0.0:$PORT --log-file=- app:app