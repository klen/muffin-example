from horneds/muffin:latest

# Install python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy whole application
COPY . /app

ENV SETUP_SCRIPT=/app/devops/setup.sh
ENV APP_MODULE=example:app
