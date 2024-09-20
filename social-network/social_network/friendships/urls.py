from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FriendRequestViewSet,
    FriendsListView,
    PendingFriendRequestView
    )

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-requests')

urlpatterns = [
    path('', include(router.urls)),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-friend-requests/', PendingFriendRequestView.as_view(), name='pending-friend-requests'),
]
