from .models import FriendRequest, ActivityLog, User
from .serializers import FriendRequestSerializer
from django.db.models import Q
from .serializers import ActivityLogSerializer
from rest_framework import generics, permissions
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass



class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__icontains=query) | Q(name__icontains=query))


class FriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer


class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(friends__in=[user])

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user, status='sent')


class ActivityLogView(generics.ListCreateAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer


class UserSearchPagination(PageNumberPagination):
    page_size = 10

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            # Use Q objects to search first_name and last_name
            return User.objects.filter(
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).distinct()  # Use distinct to avoid duplicates

        return User.objects.none()  # Return an empty queryset if no query


