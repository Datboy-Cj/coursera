from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


class AssessmentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('learner', password='test-password')
        self.course = Course.objects.create(name='Practice', description='Practice course')
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        self.question = Question.objects.create(course=self.course, content='Select both', grade=2)
        self.a = Choice.objects.create(question=self.question, content='A', is_correct=True)
        self.b = Choice.objects.create(question=self.question, content='B', is_correct=True)
        self.c = Choice.objects.create(question=self.question, content='C', is_correct=False)
        self.url = reverse('onlinecourse:submit', args=[self.course.pk])
        self.client.force_login(self.user)

    def test_exact_answer_set(self):
        self.assertTrue(self.question.is_get_score([self.a.pk, self.b.pk]))
        self.assertFalse(self.question.is_get_score([self.a.pk]))
        self.assertFalse(self.question.is_get_score([self.a.pk, self.b.pk, self.c.pk]))
        self.assertFalse(self.question.is_get_score([]))

    def test_submission_and_success_page(self):
        response = self.client.post(self.url, {'choices': [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, 'Congratulations')
        self.assertEqual(response.context['grade'], 100)
        self.assertEqual(Submission.objects.get().choices.count(), 2)

    def test_blank_submission_is_zero(self):
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.context['grade'], 0)
        self.assertNotContains(response, 'Congratulations')

    def test_foreign_choice_rejected(self):
        other = Course.objects.create(name='Other')
        question = Question.objects.create(course=other, content='Other question')
        choice = Choice.objects.create(question=question, content='Foreign')
        self.assertEqual(self.client.post(self.url, {'choices': [choice.pk]}).status_code, 400)
        self.assertEqual(Submission.objects.count(), 0)

    def test_invalid_choice_rejected(self):
        self.assertEqual(self.client.post(self.url, {'choices': ['invalid']}).status_code, 400)

    def test_post_only_and_login_required(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_enrollment_required(self):
        self.enrollment.delete()
        self.assertEqual(self.client.post(self.url).status_code, 404)

    def test_result_private(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        other = User.objects.create_user('other')
        self.client.force_login(other)
        url = reverse('onlinecourse:show_exam_result', args=[self.course.pk, submission.pk])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_weighted_score_and_pass_boundary(self):
        self.question.grade = 4
        self.question.save()
        Question.objects.create(course=self.course, content='Unanswered', grade=1)
        response = self.client.post(self.url, {'choices': [self.a.pk, self.b.pk]}, follow=True)
        self.assertEqual(response.context['grade'], 80)
        self.assertFalse(response.context['passed'])

    def test_detail_and_admin(self):
        self.assertContains(self.client.get(reverse("onlinecourse:index")), "Practice")
        self.assertContains(self.client.get(reverse('onlinecourse:course_details', args=[self.course.pk])), 'Select both')
        self.user.is_staff = self.user.is_superuser = True
        self.user.save()
        self.assertContains(self.client.get('/admin/'), 'OnlineCourse')
        self.assertContains(self.client.get('/admin/'), 'Authentication and Authorization')

    def test_failed_feedback_and_retake(self):
        response = self.client.post(self.url, {'choices': [self.a.pk, self.c.pk]}, follow=True)
        self.assertContains(response, 'Correct answer: A')
        self.assertContains(response, 'Not selected: B')
        self.assertContains(response, 'Wrong answer: C')
        self.assertContains(response, 'Retake exam')
        self.assertEqual(response.context['grade'], 0)
        response = self.client.post(self.url, {'choices': [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, 'Congratulations')
        self.assertEqual(Submission.objects.count(), 2)
