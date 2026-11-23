# Example Muffin Application

![](https://raw.github.com/klen/muffin/develop/docs/static/logo-h200.png)

[![Tests Status](https://github.com/klen/muffin-example/workflows/tests/badge.svg)](https://github.com/klen/muffin-example/actions)
[![Build Status](https://github.com/klen/muffin-example/actions/workflows/heroku.yml/badge.svg)](https://github.com/klen/muffin-example/actions/workflows/heroku.yml)

The application is deployed on Heroku: https://muffin-py.herokuapp.com

## Run locally

Install [uv](https://docs.astral.sh/uv/) and run:

    $ make run

And open http://localhost:5000 in your browser.

## Run tests

    $ make test

Or directly:

    $ uv sync --locked
    $ uv run pytest tests
