
# Student Performance Tracker

A Python + Flask web application for tracking student performance across subjects, with a menu-driven CLI option and SQLite persistence.

## Features
- Add students (unique roll numbers)
- Add/update grades per subject (validated 0–100)
- View student details and per-student average
- Bonus: subject-wise topper and class average
- Backup data to a text file
- Flask web UI with HTML templates
- SQLite database created automatically on first run

## Project Structure
```text
student-performance-tracker/
├─ app.py
├─ cli.py
├─ student_tracker/
│  ├─ __init__.py
│  └─ tracker.py
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ add_student.html
│  ├─ add_grades.html
│  ├─ student_detail.html
│  └─ class_reports.html
├─ static/
│  └─ style.css
├─ requirements.txt
├─ Procfile
└─ README.md
```

## Quickstart (Local)
1. **Create and activate a virtual environment (recommended).**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2. **Install dependencies.**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the web app.**
   ```bash
   python app.py
   # visit http://localhost:5000
   ```
   Or run the CLI:
   ```bash
   python cli.py
   ```

## Deployment (Heroku or similar)
- This repo includes a `Procfile` and `requirements.txt` for platforms like Heroku, Render, or Railway.
- For Heroku-style deploy:
  ```bash
  heroku create
  git add .
  git commit -m "Initial deploy"
  git push heroku main
  # or master, depending on your branch
  ```
  Ensure a `SECRET_KEY` config var is set if deploying publicly.

## Configuration
- `SECRET_KEY`: Flask secret (optional; defaults to a dev key).
- SQLite file `student_tracker.db` is created in the working directory automatically.

## Notes
- All grade inputs are validated to be between 0 and 100.
- Roll numbers must be unique; attempts to add a duplicate roll are ignored with a message.
- Backups can be downloaded from **Backup (TXT)** in the navbar.

## License
MIT (add your chosen license if needed)
