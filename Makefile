.PHONY: all help
all: sync

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Remove build artefacts
clean:
	rm -rf build/ dist/ docs/_build *.egg-info
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR) -name "__pycache__" -type d -prune -exec rm -rf {} +

# =============
#  Development
# =============

.PHONY: sync
# target: sync - Install/sync dependencies with uv
sync:
	uv sync --locked

.PHONY: t test
# target: test - Runs tests
t test: sync
	uv run pytest tests

.PHONY: db
# target: db - Apply migrations and create example users
db: sync
	uv run muffin example --config=example.config.debug peewee-migrate
	uv run muffin example --config=example.config.debug example-users

.PHONY: run
# target: run - Run the application on port 5000
run: db
	uv run uvicorn --reload --reload-dir $(CURDIR)/example --port 5000 example:app

.PHONY: shell
# target: shell - Open the application shell
shell: sync
	uv run muffin example --config=example.config.debug shell

.PHONY: docker
docker:
	docker build -f $(CURDIR)/devops/Dockerfile -t muffin-example:latest $(CURDIR)

docker-run: docker
	@docker run --rm -it -p 5000:80 --env GWORKERS=1 --name muffin-example muffin-example:latest $(RUN)
