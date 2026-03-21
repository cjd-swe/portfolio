# Cameron J. Davis — Portfolio

Personal portfolio website for Cameron J. Davis, built with Django. The repo supports **two deployment paths**:

| Path | Platform | Backend | Database | Best for |
|---|---|---|---|---|
| **Static** | GitHub Pages | None (pure HTML/CSS/JS) | None | Free, instant, no server needed |
| **Full app** | Render | Django + Gunicorn | PostgreSQL | Admin panel, dynamic content |

---

## Option 1: GitHub Pages (Static)

The `docs/` folder contains a self-contained static version of the portfolio — no Python, no database, no server required. GitHub Pages serves it for free directly from this repo.

### First-time setup

1. **Push this branch to GitHub**

   ```bash
   git push -u origin claude/gh-pages-static-kCpfd
   ```

2. **Enable GitHub Pages**
   - Go to your repo on GitHub → **Settings** → **Pages**
   - Under *Source*, select:
     - Branch: `claude/gh-pages-static-kCpfd`
     - Folder: `/docs`
   - Click **Save**

3. **Wait ~60 seconds**, then visit:
   ```
   https://<your-github-username>.github.io/<repo-name>/
   ```

That's it. Your site is live.

---

### Updating your projects

All project content lives in one place — the `projects` array near the bottom of `docs/index.html`:

```js
var projects = [
  {
    summary: "GTP — Add a short description of this project here.",
    image:   "images/GTP.png"
  },
  {
    summary: "Versa — Add a short description of this project here.",
    image:   "images/Versa.png"
  }
];
```

**To edit from your phone:**
1. Open `docs/index.html` in GitHub's web editor (tap the pencil icon on the file)
2. Find the `projects` array and update the `summary` text
3. Commit directly to the branch — the site updates within ~60 seconds

**To add a new project:**
1. Upload your project image to `docs/images/` via GitHub's **Add file** button
2. Add a new entry to the `projects` array in `docs/index.html`:
   ```js
   ,{
     summary: "My new project — brief description of what it does.",
     image:   "images/yourimage.png"
   }
   ```
3. Commit the change

**To update your bio or skills:**
- Open `docs/index.html` and edit the About section text or the `<span class="skill-badge">` list directly

---

### File structure (docs/)

```
docs/
├── index.html       ← Main page — edit projects array and bio here
├── portfolio.css    ← Styles (auto dark/light mode)
├── portfolio.js     ← Scroll-reveal animation
└── images/
    ├── Cam.jpeg     ← Profile photo
    ├── GTP.png      ← Project image
    └── Versa.png    ← Project image
```

---

## Option 2: Render (Full Django App)

Use this if you want the Django admin panel, database-backed projects, and the full dynamic site.

### Prerequisites

- A [Render](https://render.com) account (free tier available)
- Your code pushed to GitHub

### Setup

1. **Push to GitHub**

   ```bash
   git push -u origin main
   ```

2. **Create a PostgreSQL database on Render**
   - Dashboard → **New** → **PostgreSQL**
   - Choose a name (e.g. `portfolio-db`), select the free plan
   - After it's created, copy the **Internal Database URL**

3. **Create a Web Service on Render**
   - Dashboard → **New** → **Web Service**
   - Connect your GitHub repo
   - Configure:

   | Setting | Value |
   |---|---|
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn portfolio.wsgi` |
   | **Plan** | Free |

4. **Set environment variables** (under *Environment* in your Render service):

   | Key | Value |
   |---|---|
   | `DATABASE_URL` | The Internal Database URL from step 2 |
   | `SECRET_KEY` | A long random string — generate one at djecrety.ir |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-service-name.onrender.com` |

5. **Update `portfolio/settings.py`** to read from environment variables:

   ```python
   import os
   import dj_database_url

   SECRET_KEY = os.environ.get('SECRET_KEY', 'your-local-dev-key')
   DEBUG = os.environ.get('DEBUG', 'True') == 'True'
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   ```

   Install the helper library and freeze dependencies:
   ```bash
   pip install dj-database-url
   pip freeze > requirements.txt
   ```

6. **Deploy** — Render auto-deploys on every push to your connected branch

7. **Run migrations** (one-time, via the Render Shell tab in your service dashboard):
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

8. **Add projects** via the Django admin at:
   ```
   https://your-service-name.onrender.com/admin/
   ```

---

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

To preview the static GitHub Pages version locally, serve the `docs/` folder:

```bash
cd docs
python -m http.server 8080
# Visit http://localhost:8080
```
