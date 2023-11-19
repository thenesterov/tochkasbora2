from django.urls import path

from interest.views import ListInterestAPIView, RetrieveInterestAPIView

urlpatterns = [
    path('v1/interests/', ListInterestAPIView.as_view()),
    path('v1/interests/<int:interest_id>/', RetrieveInterestAPIView.as_view()),
]
