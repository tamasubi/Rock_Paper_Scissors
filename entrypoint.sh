   #!/usr/bin/env bash
   
   set -ex
   
   python manage.py migrate --noinput
   
   # Run the default gunicorn command
   exec gunicorn --bind :8000 --workers 2 rock_project.wsgi:application