#!/bin/bash

export PORT=8000
export OER_KEY=4930451afa05443999faa94c9abb1394
gunicorn -b 0.0.0.0:$PORT --log-file=- app:app