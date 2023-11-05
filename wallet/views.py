from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses.permissions import IsOwner, IsModerator
from wallet.models import Payment
from wallet.serializers import PaymentSerializer


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('date',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

