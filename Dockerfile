ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

# Copies the local code to the container image
WORKDIR /app
COPY . .

# Install dependencies and run migrations
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python manage.py collectstatic --noinput && \ 
    python manage.py migrate && \
    rm -rf /root/.cache/


# Run the app using Gunicorn
EXPOSE 8000
CMD gunicorn rock_project.wsgi:application --bind 0.0.0.0:8000