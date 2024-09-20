from rest_framework import serializers
from .models import User, FriendRequest, ActivityLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Adjust this based on how you want to represent the sender
    receiver = serializers.StringRelatedField()  # Adjust this based on how you want to represent the receiver

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Adjust this based on how you want to represent the user

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action', 'timestamp']


