from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'username', 'email']

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only= True)
    assigned_to = UserSerializer(read_only = True)

    class Meta:
        model = Ticket
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only= True)
    class meta:
        model = User
        fields= ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data.get('email'),
            password= validated_data['password']
        )
        return user
