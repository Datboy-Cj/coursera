from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.timezone import localdate

from onlinecourse.models import Choice, Course, Instructor, Lesson, Question


class Command(BaseCommand):
    help = 'Create the Learning Django example from Task 4 of the final-project lab.'

    def add_arguments(self, parser):
        parser.add_argument('--instructor', default='admin', help='Existing instructor username')

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            user = get_user_model().objects.get(username=options['instructor'])
        except get_user_model().DoesNotExist:
            raise CommandError('Create the instructor account with createsuperuser first.')
        instructor, _ = Instructor.objects.get_or_create(user=user, defaults={'total_learners': 0})
        course, _ = Course.objects.get_or_create(name='Learning Django', defaults={
            'description': 'Django is an extremely popular and fully featured server-side web framework, written in Python',
            'pub_date': localdate(),
        })
        course.instructors.add(instructor)
        if not course.image:
            asset = Path(__file__).resolve().parents[2] / 'demo_assets' / 'question.png'
            with asset.open('rb') as image:
                course.image.save('question.png', File(image))
        Lesson.objects.get_or_create(course=course, title='What is Django', defaults={
            'order': 0,
            'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It is free and open source.',
        })
        question, _ = Question.objects.get_or_create(course=course, content='Is Django a Python framework', defaults={'grade': 100})
        Choice.objects.get_or_create(question=question, content='Yes', defaults={'is_correct': True})
        Choice.objects.get_or_create(question=question, content='No', defaults={'is_correct': False})
        self.stdout.write(self.style.SUCCESS(f'Learning Django is ready at /onlinecourse/{course.pk}/'))
