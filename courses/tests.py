from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(email='test_user@sky.pro',
                                        role='moderator',
                                        phone='0615557766',
                                        city='City'
                                        )

        self.user.set_password('test')
        self.user.save()

        # Создание курса для тестирования
        self.course = Course.objects.create(title='test_course',
                                            body='test',
                                            user=self.user)

        # Создание урока для тестирования
        self.lesson = Lesson.objects.create(title='test_lesson',
                                            course=self.course,
                                            body='test',
                                            video_url='https://www.youtube.com/',
                                            user=self.user
                                            )

        # Запрос токена
        response = self.client.post('/users/token/', data={'email': self.user.email, 'password': 'test'})

        self.access_token = response.data.get('access')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_retrieve_lesson(self):
        """Тестирование получение одного урока"""

        response = self.client.get(
            reverse('courses:get_lesson', kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': self.lesson.title,
                'course': self.lesson.course.title,
                'body': self.lesson.body,
                'user': self.lesson.user_id,
                'video_url': self.lesson.video_url
            }
        )

    def test_list_lesson(self):
        """Тестирование списка уроков"""

        response = self.client.get(
            reverse('courses:list_lesson')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{
                'id': self.lesson.id,
                'title': self.lesson.title,
                'course': self.lesson.course.title,
                'body': self.lesson.body,
                'user': self.lesson.user_id,
                'video_url': self.lesson.video_url
            }]
        )

    def test_update_lesson(self):
        """Тестирование изменения урока"""

        data = {
            'title': 'test_lesson_1',
            'course': 'test_course',
            'body': 'test_test',
            'video_url': 'https://www.youtube.com/1'
        }

        response = self.client.put(
            reverse('courses:update_lesson', kwargs={'pk': self.lesson.id}), data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'test_lesson_1',
                'course': self.lesson.course.title,
                'body': 'test_test',
                'user': self.lesson.user_id,
                'video_url': 'https://www.youtube.com/1'
            }
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            'title': 'test_lesson_2',
            'course': 'test_course',
            'body': 'test',
            'video_url': 'https://www.youtube.com/2'
        }

        response = self.client.post(
            reverse('courses:create_lesson'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        response = self.client.delete(
            reverse('courses:delete_lesson', kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(Lesson.objects.all().count(), 0)

    def tearDown(self):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()


class SubscriptionTestCase(LessonTestCase):

    def test_subscribe_course(self):
        """Тестирование подписки на обновление курса"""

        data = {
            'user': self.user.pk,
            'course': self.course.pk,
        }

        response = self.client.post(reverse('courses:subscribe'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).exists(), True)

        response = self.client.delete(reverse('courses:unsubscribe', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).exists(), False)
