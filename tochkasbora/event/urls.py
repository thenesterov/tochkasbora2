from django.urls import path

from event.views import (
    ListCreateEventAPIView, RetrieveUpdateDestroyEventAPIView,
    SubscribeAPIView, UnsubscribeAPIView,
    MyEventsAPIView
)

urlpatterns = [
    path('v1/events/', ListCreateEventAPIView.as_view()),
    path('v1/events/<int:event_id>/', RetrieveUpdateDestroyEventAPIView.as_view()),
    path('v1/events/<int:event_id>/subscribe/', SubscribeAPIView.as_view()),
    path('v1/events/<int:event_id>/unsubscribe/', UnsubscribeAPIView.as_view()),
    path('v1/events/my/', MyEventsAPIView.as_view())
]
