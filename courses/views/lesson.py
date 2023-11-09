from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses.models import Lesson
from courses.paginators import CoursesPaginator
from users.permissions import IsOwner, IsModerator
from courses.serializers.lesson import LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """APIView для создания урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """APIView для просмотра списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]
    pagination_class = CoursesPaginator

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)

        return qs


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """APIView для получения просмотра урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """APIView для редактирования урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """APIView для удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
