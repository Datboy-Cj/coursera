from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice

class Command(BaseCommand):
    help = 'Create a small mock course for testing the assessment feature.'

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(name='Django & SQL Essentials', defaults={
            'description': 'A short practice course on models, database queries, and Django views.'})
        lessons = [
            ('Models and tables', 'A Django model describes a database table. Each model instance represents a row.'),
            ('Reading data', 'SELECT reads SQL data. Django QuerySets let you query models using Python.'),
            ('Views and templates', 'A view receives a request and returns a response. Templates format the page shown to the learner.')]
        for order, (title, content) in enumerate(lessons):
            Lesson.objects.get_or_create(course=course, order=order, defaults={'title': title, 'content': content})
        questions = [
            ('What does a Django model instance represent?', ['A database row', 'An entire database'], [0]),
            ('Which SQL command reads data?', ['SELECT', 'DELETE'], [0]),
            ('What does a Django view return?', ['An HTTP response', 'A database server'], [0])]
        for content, answers, correct in questions:
            question, _ = Question.objects.get_or_create(course=course, content=content, defaults={'grade': 1})
            for index, text in enumerate(answers):
                Choice.objects.get_or_create(question=question, content=text, defaults={'is_correct': index in correct})
        self.stdout.write(self.style.SUCCESS('Demo course is ready. Create a user, enroll, and take its exam.'))
