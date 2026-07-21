# Repo cleanup to-do

## Hosting — moving off Heroku to Render (free tier + sqlite)
Heroku account (`camdavis` app) got a final inactivity notice and is presumed
already deleted (2026, over a year of no logins). Decided: Render free tier,
production database is sqlite (not Postgres) — accepted tradeoff: Render's
free tier has an ephemeral disk, so the sqlite file resets on every deploy.
A data migration (`jobs/migrations/0004_seed_experience_and_projects.py`)
re-seeds the Experience/Projects content automatically every time `migrate`
runs, so a fresh deploy always comes back populated — just note that anything
edited by hand via `/admin` (not in that migration) won't survive a redeploy.

- [x] Prep repo for Render: `render.yaml` blueprint, whitenoise for static
      files, unconditional media serving, seed data migration
- [ ] You: create a Render account, connect this GitHub repo, deploy via
      "New > Blueprint" (picks up `render.yaml` automatically)
- [ ] You: in Render's dashboard, add a custom domain (`cjdswe.dev` and
      `www.cjdswe.dev`) to the service, then update DNS at your domain
      registrar per Render's instructions (usually a CNAME/ALIAS record)
- [ ] Push this branch to `origin/main` first (Render deploys from GitHub)

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
- [ ] Deploy on Render (see Hosting section above)
