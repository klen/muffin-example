FROM horneds/muffin:latest

# Copy the project and install it with uv
COPY . /app
WORKDIR /app
RUN pip install uv && uv pip install --system --no-cache-dir .

ENV SETUP_SCRIPT=/app/devops/setup.sh
ENV APP_MODULE=example:app
