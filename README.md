# Example Muffin Application

![](https://raw.github.com/klen/muffin/develop/docs/static/logo-h200.png)

[![Tests Status](https://github.com/klen/muffin-example/workflows/tests/badge.svg)](https://github.com/klen/muffin-example/actions)

## Run locally

Install [uv](https://docs.astral.sh/uv/) and run:

    $ make run

And open http://127.0.0.1:5000 in your browser.

## Run tests

    $ make test

Or directly:

    $ uv sync --locked
    $ uv run pytest tests
