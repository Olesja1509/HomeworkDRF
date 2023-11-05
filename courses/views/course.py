from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from courses.models import Course
from courses.permissions import IsOwner, IsModerator
from courses.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)

        return qs
