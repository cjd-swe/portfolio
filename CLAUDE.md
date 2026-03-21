# Portfolio

Personal portfolio website for Cameron J. Davis, built with Django. Displays a gallery of projects ("jobs") with images and summaries.

## Common Commands

```bash
# Run local dev server
python manage.py runserver

# Apply database migrations
python manage.py migrate

# Create a superuser for the admin panel
python manage.py createsuperuser

# Install dependencies
pip install -r requirements.txt

# Collect static files (for production)
python manage.py collectstatic
```

## Architecture

- **`portfolio/`** — Django project config (settings, root URLs, WSGI/ASGI)
- **`jobs/`** — Main app: models, views, templates, migrations
- **`static/`** — Static assets (CSS, logos)
- **`images/`** — User-uploaded project images

## Data Model

`Job` (in `jobs/models.py`):
- `image` — uploaded project image (stored in `images/`)
- `summary` — short description (max 200 chars)

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | `jobs.views.homepage` | Lists all projects |
| `/jobs/<id>` | `jobs.views.detail` | Project detail page |
| `/admin/` | Django admin | Content management |

## Environment

- **Local DB:** SQLite (`db.sqlite3`)
- **Production DB:** PostgreSQL on AWS (credentials in `portfolio/settings.py`)
- **Deployment:** Heroku via `Procfile` (Gunicorn)
- **Key dependencies:** Django 3.1.2, Pillow, psycopg2, Gunicorn, Stripe, django-allauth
