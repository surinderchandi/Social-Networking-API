from django.shortcuts import render
from django.urls import path
from .views import (
    MyTokenObtainPairView,
    MyTokenRefreshView,
    UserSearchView,
    SignupView
    )


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
]
