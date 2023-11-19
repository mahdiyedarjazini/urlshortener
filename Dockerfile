FROM python:3.11.6-slim-bullseye

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

WORKDIR /urlshortener

# Allows docker to cache installed dependencies between builds
COPY ./requirements ./requirements
RUN pip install -r ./requirements/base.txt

# Adds our application code to the image
COPY . .

EXPOSE 8000

# Run the production server
CMD gunicorn --bind 0.0.0.0:8000 --access-logfile - urlshortener.wsgi:application
