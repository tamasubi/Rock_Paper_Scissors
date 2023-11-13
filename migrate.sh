#!/bin/bash

echo "Starting database migration..."

python manage.py makemigrations
python manage.py migrate

echo "Database migration complete!"