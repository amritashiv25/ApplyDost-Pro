# ApplyDost

A full-stack job application tracker built with Flask, SQLite, HTML, CSS and vanilla JavaScript.

## Included
- Account registration/login with hashed passwords and per-user records
- Add/edit/delete applications, status and priority
- SQLite persistence across browser refreshes
- Search, status filter and sorting
- Dashboard counts, interview/offer rates and goal progress
- Drag-and-drop Kanban board
- Interview calendar list
- CSV export
- Resume/job-description keyword overlap helper
- Recruiter, notes, job URL, resume version and application history fields
- Dark mode

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended):
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Start: `python app.py`
6. Open `http://127.0.0.1:5000`

Create an account in the app. Data is stored in `instance/jobtracker.db`.

## Important before public deployment
- Set a long random `SECRET_KEY` environment variable.
- Use HTTPS and secure cookie settings.
- Add CSRF protection, rate limiting, password reset/email verification and production server configuration.
- Use PostgreSQL for a hosted multi-user deployment and configure backups.
- The resume matcher is a basic keyword-overlap tool, not an ATS score or hiring prediction.
- The app does not send real push/email reminders; interview dates are displayed in the calendar view.
