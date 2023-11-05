from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Course)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


@admin.register(Lesson)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')
    list_filter = ('course',)
