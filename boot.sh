#!/bin/bash
cd /home/webhooks
source venv/bin/activate
exec gunicorn -b :5050 --access-logfile - --error-logfile - webhooks:app
