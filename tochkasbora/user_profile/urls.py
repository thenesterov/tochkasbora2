from django.urls import path

from user_profile.views import ListCreateUserAPIView, RetrieveUpdateDestroyAPIView

urlpatterns = [
    path('v1/users/', ListCreateUserAPIView.as_view()),
    path('v1/users/<int:user_id>/', RetrieveUpdateDestroyAPIView.as_view())
]
