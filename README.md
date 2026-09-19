# Online Course Assessment App

A Django course application with lessons, enrollment, multiple-choice exams, and scored results. Based on IBM Developer Skills Network's [official starter](https://github.com/ibm-developer-skills-network/tfjzl-final-cloud-app-with-database), under its Apache 2.0 license.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open `/onlinecourse/` for courses and `/admin/` for administration. Sign in, enroll in the demo course, select answers, and submit the exam. The seed command creates sample lessons and questions, not accounts or passwords.

## Assessment implementation

- `onlinecourse/models.py`: Question, Choice, and Submission models.
- `onlinecourse/admin.py`: seven model imports, lesson/question/choice inline editing and admin registration.
- `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`: course, lessons, enrollment, and exam form.
- `onlinecourse/views.py`: submission persistence and owner-restricted result evaluation.
- `onlinecourse/urls.py`: named submit and result routes.
- `screenshots/03-admin-site.png`: running Django admin.
- `screenshots/07-final.png`: real successful mock-exam submission in the local app.

All correct choices and no incorrect choices must be selected to earn a question's points. Unanswered questions earn zero. Grades are weighted by each question's points; the starter's greater-than-80% passing rule is retained.

## Validation

```sh
python manage.py check
python manage.py test
```

Ten tests cover exact-choice scoring, weighted scoring, successful and blank submissions, invalid/foreign choices, enrollment, login, HTTP method restrictions, private results, and admin rendering. A browser smoke test covered enrollment, answering questions, submission, and the displayed 100% result.

This is a local educational application. Production deployment requires a private secret key, DEBUG=False, configured hostnames, HTTPS, and static/media hosting. The local database and session credentials are not included.
