from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from courses.models import Lesson, Course
from courses.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'course', 'body', 'user', 'video_url')
        validators = [VideoUrlValidator(field='video_url')]
