from rest_framework import serializers
from django.contrib.auth import get_user_model

from faker import Faker
from catalog.models import Representative


User = get_user_model()


class Human:
    def __init__(self, name, surname, phone):
        self.name=name
        self.surname=surname
        self.phone=phone

f = Faker()

human_list = [Human(f.first_name(), f.last_name(), f.phone_number()) for _ in range(10)]

class HumanSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    phone = serializers.CharField()


class RepresentativeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Representative
        fields = ['id','full_name', 'email']

    def get_full_name(self, obj):
        return f'{obj.name} {obj.surname}'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserOverViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']     