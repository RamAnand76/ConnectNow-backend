# authentication/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Interest, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class InterestSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Interest
        fields = ['id', 'sender', 'receiver', 'message', 'is_accepted', 'is_rejected', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']