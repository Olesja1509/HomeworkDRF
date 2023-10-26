from rest_framework import serializers

from users.models import User
from wallet.models import Payment
from wallet.serializers import PaymentSerializer


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'payment')


class UserCreateSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        payment = validated_data.pop('payment')

        user_item = User.objects.create(**validated_data)

        for p in payment:
            Payment.objects.create(**p, user=user_item)

        return user_item
