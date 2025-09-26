from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, Profile, Comment
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'username', 'email']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'ticket', 'author', 'comment', 'created_at']
        read_only_fields = ['author', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only= True)
    assigned_to = UserSerializer(read_only = True)

    class Meta:
        model = Ticket
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only= True)
    class Meta:
        model = User
        fields= ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data.get('email'),
            password= validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username =serializers.CharField()
    password= serializers.CharField(write_only=True)

