from rest_framework import serializers
from .models import FriendRequest, UserBlock
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']

class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlock
        fields = ['id', 'blocker', 'blocked', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Adjust fields as needed

class FriendRequestSerializer(serializers.ModelSerializer):
    friend = UserSerializer(source='receiver')

    class Meta:
        model = FriendRequest
        fields = ('friend', 'created_at', 'status')


class PendingFriendRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')
    sender_id = serializers.IntegerField(source='sender.id')

    class Meta:
        model = FriendRequest
        fields = ('sender_username', 'sender_id', 'created_at', 'status')
