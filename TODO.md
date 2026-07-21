# Repo cleanup to-do

## Critical — leaked credentials
- [ ] Rotate the Postgres password (Heroku dashboard/provider console) — assume compromised, it's been public
- [ ] Check whether `OdietamO@85` (old plaintext password found in git history, commit `98cb789`) was reused anywhere else; change it if so
- [ ] Move `SECRET_KEY` and `DATABASES` values into environment variables (`os.environ.get(...)`) in `portfolio/settings.py`
- [ ] Scrub git history of the credentials (`git filter-repo` or BFG), then force-push — confirm with yourself before doing this, it rewrites history

## Broken working-tree edits (site won't render as-is)
- [ ] Fix `jobs/templates/jobs/home.html`: `{% logos 'linkedin_logo.jpeg' %}` → `{% static 'logos/linkedin_logo.jpeg' %}`
- [ ] Fix `jobs/templates/jobs/home.html`: `{{job.static.image.url}}` → `{{job.image.url}}`
- [ ] Remove stray `ß` character before `<body>` in `jobs/templates/jobs/detail.html`
- [ ] Fix typo: "Previous Jobs ands Projects" → "Previous Jobs and Projects"

## Model/migration mismatch
- [ ] Run `makemigrations` to generate the missing migration for the new `Skill` model

## Repo hygiene
- [ ] Add a `.gitignore` (cover `db.sqlite3`, `.DS_Store`, `__pycache__/`, `*.pyc`)
- [ ] `git rm --cached` the currently tracked `db.sqlite3`, `.DS_Store` files, and `__pycache__`/`*.pyc` files
- [ ] Remove unused dependencies from `requirements.txt` (`django-allauth`, `stripe`, `oauthlib`, `PyJWT`, `python3-openid` — none are imported anywhere in the code)

## Once the above is done
- [ ] Push the 2 local commits currently ahead of `origin/main`
`