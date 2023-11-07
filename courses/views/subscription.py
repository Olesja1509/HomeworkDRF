from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses.models import Subscription
from courses.serializers.subscription import SubscriptionSerializer
from users.permissions import IsOwner


# class SubscriptionViewSet(viewsets.ModelViewSet):
#     serializer_class = SubscriptionSerializer
#     queryset = Subscription.objects.all()
#     permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
