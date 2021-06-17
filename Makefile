VIRTUAL_ENV ?= env

all: $(VIRTUAL_ENV)

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Display callable targets
clean:
	rm -rf build/ dist/ docs/_build *.egg-info
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR)/$(MODULE) -name "__pycache__" | xargs rm -rf

# =============
#  Development
# =============

$(VIRTUAL_ENV): requirements.txt
	@[ -d $(VIRTUAL_ENV) ] || python -m venv $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install -e .
	@touch $(VIRTUAL_ENV)

.PHONY: t test
# target: test - Runs tests
t test: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pytest -xsv tests

.PHONY: db
db:
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug pw_migrate
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug example_users

.PHONY: run
run: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug pw_migrate
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug example_users
	@$(VIRTUAL_ENV)/bin/uvicorn --reload --reload-dir $(CURDIR)/example --port 5000 example:app

.PHONY: shell
shell: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug shell

.PHONY: docker
docker:
	docker build -f $(CURDIR)/devops/Dockerfile -t muffin-example:latest $(CURDIR)

docker-run: docker
	@docker run --rm -it -p 5000:80 --env GWORKERS=1 --name muffin-example muffin-example:latest $(RUN)
