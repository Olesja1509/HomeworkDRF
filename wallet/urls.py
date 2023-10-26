from django.urls import path

from wallet.views import *
from wallet.apps import WalletConfig


app_name = WalletConfig.name


urlpatterns = [
    path('create/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('', PaymentListAPIView.as_view(), name='list_payment'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='get_payment'),
    path('update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='update_payment'),
    path('delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='delete_payment'),
]
