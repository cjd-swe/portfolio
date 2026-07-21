# Portfolio

A Django portfolio site for displaying work experience, projects, and skills.

## Prerequisites

- Python 3.12 or newer
- `pip`

## Start locally

For a one-command setup on macOS or Linux, run:

```bash
bash start.sh
```

The script creates `.venv` and `.env` when needed, installs dependencies,
applies database migrations, and starts Django at <http://127.0.0.1:8000/>. It
preserves an existing `.env`. Stop the server with `Ctrl+C`.

To use another address or port, pass it to the script, for example:

```bash
bash start.sh 0.0.0.0:8080
```

### Manual setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Open `.env` and configure it for local development:

```dotenv
DJANGO_SECRET_KEY=replace-this-with-a-local-development-key
DJANGO_DEBUG=True
```

Remove the sample `DATABASE_URL` line from `.env` unless you intend to use
PostgreSQL. When `DATABASE_URL` is unset, the app uses a local SQLite database.

Prepare the database and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

Then open <http://127.0.0.1:8000/>.

Stop the server with `Ctrl+C`. On later runs, reactivate the virtual environment
and run `python manage.py runserver` again.

## Optional admin access

Create an administrator account:

```bash
python manage.py createsuperuser
```

After starting the server, visit <http://127.0.0.1:8000/admin/> to manage the
portfolio content.

## Run checks and tests

```bash
python manage.py check
python manage.py test
```

## PostgreSQL

To use PostgreSQL instead of SQLite, keep `DATABASE_URL` in `.env` and replace
the example value with a working connection URL:

```dotenv
DATABASE_URL=postgres://user:password@host:5432/database_name
```

Run `python manage.py migrate` after changing databases.
