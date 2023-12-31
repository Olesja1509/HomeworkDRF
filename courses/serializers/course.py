from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.serializers.lesson import LessonSerializer
from courses.tasks import send_email_course_update


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        return Subscription.objects.filter(course=course, user=self.context['request'].user).exists()

    def save(self, **kwargs):
        send_email_course_update.delay(id)
        return super().save(**kwargs)

    class Meta:
        model = Course
        fields = ('id', 'title', 'body', 'is_subscribed', 'lessons_count', 'lessons')
