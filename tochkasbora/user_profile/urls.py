from django.urls import path

from user_profile.views import (
    ListCreateUserAPIView, RetrieveUpdateDestroyUserAPIView,
    ListCreateUserProfileAPIView, RetrieveUpdateDestroyUserProfileAPIView,
    ActivateUserProfile
)

urlpatterns = [
    path('v1/users/', ListCreateUserAPIView.as_view()),
    path('v1/users/<int:user_id>/', RetrieveUpdateDestroyUserAPIView.as_view()),
    path('v1/users_profile/', ListCreateUserProfileAPIView.as_view()),
    path('v1/users_profile/<int:profile_id>/', RetrieveUpdateDestroyUserProfileAPIView.as_view()),
    path('v1/users_profile/<int:user_id>/<int:activation_code>/', ActivateUserProfile.as_view())
]
