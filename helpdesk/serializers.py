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