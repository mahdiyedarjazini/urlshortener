# URLShortener

A URL shortener is a tool that allows you to create a shortened version of a long URL. This can be particularly useful
when sharing links on social media, in emails, or in any situation where a long URL might be unwieldy or take up too
much space.

License: MIT

## Settings

You need to create a directory called **envs** and put in it 2 files called **.django**, and **.postgres**. These are
the files that will hold your environment variables.

### .django file

You have to set: PYTHONUNBUFFERED=1

### .postgres

You have to provide the following variables:<br>

POSTGRES_HOST=<br>
POSTGRES_PORT=<br>
POSTGRES_DB=<br>
POSTGRES_USER=<br>
POSTGRES_PASSWORD=<br>

## Basic Commands

#### Running tests with pytest

    $ pytest

#### Running the project

    $ docker-compose up -d --build