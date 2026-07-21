# Repo cleanup to-do

## Hosting — Heroku account presumed dead, need a new host
- [ ] Heroku account (`camdavis` app) got a final inactivity notice and is presumed already deleted (2026, over a year of no logins) — confirm, then pick a new host (Render/Railway/Fly.io/etc.) for the Django app + Postgres
- [ ] Point cjdswe.dev (newly purchased domain) at whatever the new host is

## Critical — leaked credentials
- [x] Move `SECRET_KEY` and `DATABASES` values into environment variables (`.env` locally via python-dotenv, `DATABASE_URL`/`DJANGO_SECRET_KEY` config vars in production via dj-database-url)
- [x] Check whether `OdietamO@85` (old plaintext password found in git history, commit `98cb789`) was reused anywhere else — confirmed not reused
- [ ] Rotate the Postgres password — moot if the Heroku app/DB is already deleted, but confirm before considering this closed
- [ ] Scrub git history of the credentials (`git filter-repo` or BFG), then force-push — confirm with yourself before doing this, it rewrites history. Still worth doing even if the DB is gone, since the password/host pattern could still be reused as a phishing/recon target

## Broken working-tree edits (site won't render as-is)
- [x] Fix `jobs/templates/jobs/home.html`: `{% logos 'linkedin_logo.jpeg' %}` → `{% static 'logos/linkedin_logo.jpeg' %}`
- [x] Fix `jobs/templates/jobs/home.html`: `{{job.static.image.url}}` → `{{job.image.url}}`
- [x] Remove stray `ß` character before `<body>` in `jobs/templates/jobs/detail.html`
- [x] Fix typo: "Previous Jobs ands Projects" → "Previous Jobs and Projects"

## Model/migration mismatch
- [ ] Run `makemigrations` to generate the missing migration for the new `Skill` model (still unused/unmigrated — separate from the Job/Project model work happening now)

## Repo hygiene
- [x] Add a `.gitignore` (cover `db.sqlite3`, `.DS_Store`, `__pycache__/`, `*.pyc`)
- [x] `git rm --cached` the currently tracked `db.sqlite3`, `.DS_Store` files, and `__pycache__`/`*.pyc` files
- [ ] Remove unused dependencies from `requirements.txt` (`django-allauth`, `stripe`, `oauthlib`, `PyJWT`, `python3-openid` — none are imported anywhere in the code)

## Once the above is done
- [ ] Push the local commits ahead of `origin/main`
- [ ] Deploy to Heroku (production DB will need the new Job/Project data repopulated via `/admin` after migrating)
