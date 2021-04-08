from python:3.9-slim

MAINTAINER Kirill Klenov <horneds@gmail.com>

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        build-essential \
        curl \
        gnupg2 \
        libncurses5-dev \
        wget && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/requirements.txt
RUN /usr/local/bin/pip install -r /app/requirements.txt

# Copy whole application
COPY . /app

WORKDIR /app

# Default command
CMD ["/app/devops/entrypoint.sh"]

