import datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event
from event.permissions import IsOrganizer
from event.serializers import EventSerializer
from user_profile.models import UserProfile


class ListCreateEventAPIView(APIView):
    permission_classes = (IsOrganizer, )

    def post(self, request: Request):
        request_data = request.data

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"})

        self.check_object_permissions(request, user_profile)

        request_data['organizer_id'] = user_profile.pk

        event_sr = EventSerializer(data=request_data)

        if event_sr.is_valid(raise_exception=True):
            event_sr.save()

            return Response(data=event_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def get(self, request: Request):
        events = Event.objects.filter(deleted_at__isnull=True)

        return Response(data=EventSerializer(events, many=True).data)


class RetrieveUpdateDestroyEventAPIView(APIView):
    permission_classes = (IsOrganizer, )

    def get(self, request: Request, event_id: int):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': f'Event with {event_id=} does not exist'}, status=400)

        return Response(EventSerializer(event).data)

    def patch(self, request: Request, event_id: int):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': f'Event with {event_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        if event.organizer_id.id != user_profile.pk:
            return Response({'error': f"You don't have permission"}, status=400)

        event_sr = EventSerializer(event, data=request.data, partial=True)

        if event_sr.is_valid(raise_exception=True):
            event_sr.save()

            return Response(data=event_sr.data)

        return Response(data={'error': 'Wrong parameters'}, status=400)

    def put(self, request: Request, event_id: int):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': f'Event with {event_id=} does not exist'}, status=400)

        request_data = request.data

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        self.check_object_permissions(request, user_profile)

        if event.organizer_id.id != user_profile.pk:
            return Response({'error': f"You don't have permission"}, status=400)

        request_data['organizer_id'] = user_profile.pk

        event_sr = EventSerializer(event, data=request_data)

        if event_sr.is_valid(raise_exception=True):
            event_sr.save()

            return Response(data=event_sr.data)

        return Response(data={'error': 'Wrong parameters'}, status=400)

    def delete(self, request: Request, event_id: int):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': f'Event with {event_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        if event.organizer_id.id != user_profile.pk:
            return Response({'error': f"You don't have permission"}, status=400)

        event.deleted_at = datetime.datetime.now()
        event.save()

        return Response(data={'success': f'Event with {event_id=} was successfully deleted at {event.deleted_at}'})


class SubscribeAPIView(APIView):
    def post(self, request: Request, event_id: int):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': f'Event with {event_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        event.participants.add(user_profile)
        event.save()

        return Response({'success': 'You was successfully subscribed'})


class UnsubscribeAPIView(APIView):
    def post(self, request: Request, event_id: int):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': f'Event with {event_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        event.participants.remove(user_profile)
        event.save()

        return Response({'success': 'You was successfully unsubscribed'})


class MyEventsAPIView(APIView):
    def get(self, request: Request):
        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        try:
            events = Event.objects.filter(participants__id=user_profile.pk)
        except Event.DoesNotExist:
            return Response({'error': f'Events does not exist'}, status=400)

        return Response(data=EventSerializer(events, many=True).data)
