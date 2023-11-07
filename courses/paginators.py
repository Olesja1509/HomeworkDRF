from rest_framework.pagination import PageNumberPagination


class CoursesPaginator(PageNumberPagination):
    page_size = 10
