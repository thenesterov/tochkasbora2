from django.urls import path

from interest_group.views import ListCreateInterestGroupAPIView, RetrieveUpdateDestroyInterestGroupAPIView, \
    SubscribeAPIView, UnsubscribeAPIView, MyInterestGroupsAPIView

urlpatterns = [
    path('v2/interest_groups/', ListCreateInterestGroupAPIView.as_view()),
    path('v2/interest_groups/<int:interest_group_id>/', RetrieveUpdateDestroyInterestGroupAPIView.as_view()),
    path('v2/interest_groups/<int:interest_group_id>/subscribe/', SubscribeAPIView.as_view()),
    path('v2/interest_groups/<int:interest_group_id>/unsubscribe/', UnsubscribeAPIView.as_view()),
    path('v2/interest_groups/my/', MyInterestGroupsAPIView.as_view())
]
