from django.conf import settings
from django.apps import apps
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import FriendRequest, Cooldown, UserBlock
from .serializers import FriendRequestSerializer, PendingFriendRequestSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework import generics, permissions
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination


def get_user_model():
    return apps.get_model(settings.AUTH_USER_MODEL)

class FriendRequestRateThrottle(UserRateThrottle):
    rate = '3/min'

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    throttle_classes = [FriendRequestRateThrottle]

    def create(self, request, *args, **kwargs):
        User = get_user_model()  # Get the user model dynamically
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if on cooldown
        if Cooldown.is_on_cooldown(sender, receiver):
            return Response({"error": "Cooldown active."}, status=status.HTTP_403_FORBIDDEN)

        # Create or get friend request
        with transaction.atomic():
            friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
            if not created:
                return Response({"error": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()

        with transaction.atomic():
            friend_request.status = 'accepted'
            friend_request.save()

        return Response({"message": "Friend request accepted."})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        friend_request = self.get_object()

        with transaction.atomic():
            friend_request.status = 'rejected'
            friend_request.save()
            Cooldown.objects.create(
                sender=friend_request.sender, 
                receiver=friend_request.receiver, 
                cooldown_until=timezone.now() + timedelta(hours=24)
            )

        return Response({"message": "Friend request rejected, cooldown applied."})

    @action(detail=True, methods=['post'])
    def block(self, request, blocked_user_id):
        User = get_user_model()  # Get the user model dynamically
        blocker = request.user
        try:
            blocked = User.objects.get(id=blocked_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if UserBlock.objects.filter(blocker=blocker, blocked=blocked).exists():
            return Response({"error": "User already blocked."}, status=status.HTTP_400_BAD_REQUEST)

        UserBlock.objects.create(blocker=blocker, blocked=blocked)
        return Response({"message": "User blocked."})

    @action(detail=True, methods=['post'])
    def unblock(self, request, blocked_user_id):
        User = get_user_model()  # Get the user model dynamically
        blocker = request.user
        try:
            blocked = User.objects.get(id=blocked_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        UserBlock.objects.filter(blocker=blocker, blocked=blocked).delete()
        return Response({"message": "User unblocked."})


class FriendsListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f'friends_list_{user.id}'
        
        # Check if the data is cached
        friends_list = cache.get(cache_key)
        if friends_list is not None:
            return friends_list
        
        # Query to get accepted friend requests
        friends = FriendRequest.objects.filter(receiver=user, status='accepted').select_related('receiver')
        
        # Cache the result for future queries
        cache.set(cache_key, friends, timeout=60 * 15)  # Cache for 15 minutes
        
        return friends
    

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PendingFriendRequestView(generics.ListAPIView):
    serializer_class = PendingFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        # Fetch pending friend requests for the authenticated user
        return FriendRequest.objects.filter(receiver=user, status='pending').order_by('-created_at')
