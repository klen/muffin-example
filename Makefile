VIRTUAL_ENV=$(shell echo "$${VIRTUAL_ENV:-'.env'}")

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

$(VIRTUAL_ENV): requirements-local.txt
	@[ -d $(VIRTUAL_ENV) ] || virtualenv --no-site-packages --python=python3 $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install -r requirements-local.txt
	@touch $(VIRTUAL_ENV)

$(VIRTUAL_ENV)/bin/py.test: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install pytest webtest
	@touch $(VIRTUAL_ENV)/bin/py.test

.PHONY: test
# target: test - Runs tests
test: $(VIRTUAL_ENV)/bin/py.test
	@$(VIRTUAL_ENV)/bin/py.test -xs example/tests.py

.PHONY: t
t: test

.PHONY: db
db: $(CURDIR)/example.sqlite

$(CURDIR)/example.sqlite: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug migrate
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug example_data

.PHONY: run
run: $(CURDIR)/example.sqlite
	@$(VIRTUAL_ENV)/bin/muffin example --config=example.config.debug run --timeout=600 --pid=$(CURDIR)/pid
