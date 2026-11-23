# AGENTS.md — muffin-example

Demo chat app for Muffin. It is its own git repository (default branch `main`), checked
out inside the Muffin workspace but built against released PyPI packages, not `../core`.
Managed with uv: `pyproject.toml` + committed `uv.lock`, `uv_build`, Python >= 3.11.
CI covers 3.11–3.15.

## Repository overview

- `example/` — the import package and application:
  - `__init__.py` builds `app = Application(...)` and plugins (`jinja2`, `oauth`, `db`
    (muffin-peewee), `session`), then calls `app.import_submodules()`. Any new top-level
    module is imported at startup, so imports must be side-effect safe.
  - `config/defaults.py` — paths, sqlite DSN, OAuth/session/admin settings; `debug.py`
    (used by the Makefile), `tests.py`, `production.py` star-import and override it.
  - `models.py` — peewee models `User`, `Token`, `Message`, `Test`.
  - `manage.py` — CLI commands (`hello`, `example-users` seeds two users).
  - `api.py` — REST API at `/api`, `PWRESTHandler` + marshmallow schemas.
  - `admin.py` — muffin-admin handlers; `views/` — HTML, login/logout, OAuth, websocket.
  - `templates/`, `assets/` — Jinja templates and static files.
- `pyproject.toml` — metadata, runtime dependencies, `dev` group (pytest, pytest-aio,
  mixer), build backend and pytest settings. `uv.lock` is committed; regenerate it with
  `uv lock`, never by hand.
- `migrations/` — peewee migration scripts (`000_initial.py` creates tables; `001_auto.py`
  is a commented demo). Run by `peewee-migrate` through `make db` / `make run`.
- `tests/` — pytest + pytest-aio. `conftest.py` provides `app`, `client`, `db`, `mixer`,
  `user`, `admin` fixtures; `example/config/tests.py` switches Peewee to in-memory sqlite.
- `main.py` — imports the app for old ASGI deployments; Docker uses `example:app` instead.
- `devops/Dockerfile` + `.github/workflows/` — container image (base
  `horneds/muffin:latest`, installs the project with `uv pip install --system`) and CI
  workflows. Dependabot auto-merges minor and critical (CVSS >= 9) dependency PRs
  with a squash merge once `tests` is green; other updates stay manual.
- `Makefile` — `sync`, `test`, `db`, `run`, `shell`, `clean`, `docker`, `docker-run`; all
  Python targets go through `uv run`.
- `example.sqlite` — local dev database, gitignored; delete it to start clean.

## High-risk commands

- `make run` / `make db` — run every migration and seed `user@muffin.io` /
  `admin@muffin.io` (password `pass`) into `example.sqlite`; `run` also starts uvicorn on
  port 5000 with reload. CLI commands are hyphenated: `peewee-migrate`, `example-users`.
- Pushing to `main` or `develop` triggers `.github/workflows/tests.yml`. Commit/push
  only when explicitly asked; never push just to test.
- `git checkout -- .` / `git reset --hard` discards the local edits in `Makefile` and
  `example/config/defaults.py`. Check `git -C . status` first and preserve them.
- `make docker` / `make docker-run` build from the latest public Muffin image and bind
  host port 5000. Not a validation step.
- `uv lock` rewrites `uv.lock`; run it after editing dependencies and include the result in
  the same change.

## Safe validation

```bash
uv sync --locked
uv run pytest tests
uv run pytest tests/test_views.py::test_basic_views
uv run python -m compileall -q example tests
git -C . diff --check
make test                    # uv sync --locked + uv run pytest tests
```

The full suite is fast and needs no services (in-memory sqlite). There is no ruff,
pyrefly or other lint/type setup here; don't add one as a side effect. `make run` plus a
manual visit to `/`, `/api/messages` and `/admin` is the end-to-end smoke check.

## Editing guidelines

- Keep changes inside `example/`. Dependencies resolve to released PyPI packages, not
  `../core`; framework changes must be made and validated in `core/` separately.
- Adding a new view/model module under `example/` auto-registers it via
  `app.import_submodules()`. Use `@app.route`, `@api.route` + `PWRESTHandler`,
  `@admin.route`, or `@app.manage` as the surrounding code does.
- New settings go in `config/defaults.py`; per-environment overrides go in the matching
  config module. Keep the sqlite `:memory:` override in `tests.py` working.
- Tests rely on the session-scoped `db` fixture and roll back each test; create rows via
  `mixer`/fixtures and use `save(force_insert=True)`, don't commit.
- Schema changes need a new numbered file in `migrations/` (or a real edit if the demo
  migration hasn't been applied); `example.sqlite` itself is never committed.
- Dependencies: `uv add <pkg>`, `uv add --dev <pkg>`, then `uv lock`; don't maintain a
  parallel requirements file or edit `uv.lock`.
- `tests/conftest.py` pins the `aiolib` fixture to asyncio (pytest-aio 2 expects a string,
  not the old `(name, params)` tuple). Keep it that way unless the app is made trio-safe.
- No changelog, versioning or release target exists here. Package metadata lives in
  `pyproject.toml`.

## Files and directories to avoid

- Generated/stale: `.venv/`, `.tox/`, `.mypy_cache/`, `.pytest_cache/`,
  `muffin_example.egg-info/`, `build/`, `dist/`, `__pycache__/`, `example.sqlite`.
- `devops/` — container image; ask before touching.
- `example/config/debug.py` contains a committed GitHub OAuth client secret; don't copy
  secrets into new files or logs.

## Good defaults for agents

- Read `pyproject.toml`, `Makefile`, and the relevant `example/` module before changing
  behaviour; this repo has no lint/type safety net.
- Check `git -C . status` first and leave the pre-existing local edits alone.
- Use `uv run ...` for every Python command so the locked environment is used.
- Do not start Docker or commit/push unless explicitly asked.
