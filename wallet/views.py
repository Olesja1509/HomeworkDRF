import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsOwner, IsModerator
from wallet.models import Payment
from wallet.serializers import PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentCreateAPIView(generics.CreateAPIView):
    """APIView для создания платежа"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payment_id = request.data.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe.Charge.create(
                amount=int(payment.price),
                currency="usd",
                source=request.data.get("stripeToken"),
                description=f"Payment for {payment.user}"
            )
            return Response({"message": "Payment successful"}, status=status.HTTP_201_CREATED)
        except stripe.error.CardError as e:
            return Response({"message": e.user_message}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError:
            return Response({"message": "Something went wrong. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentListAPIView(generics.ListAPIView):
    """APIView для просмотра всех платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('date',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """APIView для просмотра одного платежа"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """APIView для редактирования платежа"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """APIView для удаления платежа"""
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
