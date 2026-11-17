# Notes for coding agents

Django 6 portfolio site: app `jobs`, project package `portfolio`, deployed on Render.

## Rules

- Change only what your brief asks for. Do not swap icons, rename things, restyle or "tidy"
  code outside the task, even if it looks like an improvement. List suggestions in your summary
  instead.
- Never point `MEDIA_ROOT` at `BASE_DIR` or any folder holding source, the database or
  secrets. `/media/` is served publicly.
- Do not read `.env` or `db.sqlite3`.
- Production data is rebuilt from migrations on every deploy (SQLite on an ephemeral disk), so
  seed content lives in `jobs/migrations/0004_seed_experience_and_projects.py`.
- Run tests with:
  `DJANGO_SECRET_KEY=test-only DJANGO_DEBUG=False .venv/bin/python manage.py test`
  (from a worktree, use the main checkout's `.venv`).
- Tests must pass with exactly the command above, in any order (`--shuffle`, `--reverse`).
  Do not report a pass from a custom bootstrap or wrapper command.
- Put new tests in their own `jobs/test_<topic>.py` file so parallel work does not collide in
  `jobs/tests.py`.
