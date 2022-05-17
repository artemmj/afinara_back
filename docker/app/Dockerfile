FROM registry/templates/image/python:3-8

RUN apt update &&\
    apt install -y --no-install-recommends\
    ttf-dejavu &&\
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY project/requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/dev.txt

WORKDIR /app
COPY project /app
