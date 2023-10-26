from django.urls import path

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name


urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('', UserListAPIView.as_view(), name='list_user'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='get_user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
]
