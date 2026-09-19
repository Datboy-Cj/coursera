# Final-project lab audit

Compared against the complete Skills Network guide, “Final Project: Add a New Assessment Feature to an Online Course App,” on September 19, 2026.

| Lab task | Implementation and validation |
| --- | --- |
| 1. Build new models | Question, Choice, Submission, relationships and migrations; exact-set multiple-selection scoring. |
| 2. Register model changes | Seven models registered; QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin; working admin screenshot. |
| 3. Course detail template | Ordered lessons, enrollment, Start Exam collapse, multiple-selection form and CSRF-protected POST. |
| 4. Test data | Learning Django course, supplied cover image, admin instructor, What is Django lesson, 100-point Yes/No question. Reproducible with seed_lab. |
| 5. Submission and evaluation views | Persist selected choices, calculate weighted results, redirect through named routes, restrict access to the submission owner. |
| 6. Result template | Congratulations and score on success; green correct, yellow missed, red incorrect selections; working retake link. |

## Reproduce the lab example

After installing dependencies and migrating:

```sh
python manage.py createsuperuser --username admin
python manage.py seed_lab
python manage.py runserver
```

The seed command creates the specified sample data without embedding credentials. Use `/admin/` to inspect/edit the course, lesson, instructor, question and choices. Enroll in Learning Django, click Start Exam, and submit Yes for the successful mock result. Submitting No demonstrates the failure feedback and retake flow.

The cover image in `onlinecourse/demo_assets/question.png` comes from the lab's supplied IBM Skills Network asset:
https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DB0211EN-edX/images/question.png

## Submission artifacts

All seven items are present: models.py, admin.py, screenshots/03-admin-site.png, course_details_bootstrap.html, views.py, urls.py, and screenshots/07-final.png. Screenshots show the running local application; the exam result is from a real form submission.

## Differences from the guided procedure

- Uses the official IBM starter in the user's `coursera` repository, rather than a GitHub fork named `tfjzl-final-cloud-app-with-database`.
- Runs in a local Mac virtual environment rather than `/home/project` in Cloud IDE. The Cloud IDE workspace has not been synchronized.
- Sample data was provisioned using a management command and inspected in the admin UI, rather than entered manually through every admin form.
- Uses Django 5.2 and Bootstrap 5, with equivalent updated syntax. Choice inputs share a list field; views read that list rather than scanning prefixed input names.
- Normalizes weighted points to a percentage; the guide's 100-point example produces the same 100/100 result. Enforces enrollment and submission ownership.

Validation: 11 automated tests, Django system checks, and browser checks for admin access, the collapsed exam, incorrect/missed feedback, retake, and successful 100% submission. This audit verifies implementation and artifacts, not an evaluator's future grade.
