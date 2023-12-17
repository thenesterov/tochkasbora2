import datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from interest_group.models import InterestGroup
from interest_group.permissions import IsOrganizer
from interest_group.serializers import InterestGroupSerializer
from user_profile.models import UserProfile


class ListCreateInterestGroupAPIView(APIView):
    permission_classes = (IsOrganizer, )

    def post(self, request: Request):
        request_data = request.data

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"})

        self.check_object_permissions(request, user_profile)

        request_data['organizer'] = user_profile.pk

        interest_group_sr = InterestGroupSerializer(data=request_data)

        if interest_group_sr.is_valid(raise_exception=True):
            interest_group_sr.save()

            return Response(data=interest_group_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def get(self, request: Request):
        interest_groups = InterestGroup.objects.filter(deleted_at__isnull=True)

        return Response(data=InterestGroupSerializer(interest_groups, many=True).data)


class RetrieveUpdateDestroyInterestGroupAPIView(APIView):
    permission_classes = (IsOrganizer, )

    def get(self, request: Request, interest_group_id: int):
        try:
            interest_group = InterestGroup.objects.get(id=interest_group_id)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup with {interest_group_id=} does not exist'}, status=400)

        return Response(InterestGroupSerializer(interest_group).data)

    def patch(self, request: Request, interest_group_id: int):
        try:
            interest_group = InterestGroup.objects.get(id=interest_group_id)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup with {interest_group_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f'User with user_id={request.user.id} does not have profile'}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        if interest_group.organizer.id != user_profile.pk:
            return Response({'error': f"You don't have permission"}, status=400)

        interest_group_sr = InterestGroupSerializer(interest_group, data=request.data, partial=True)

        if interest_group_sr.is_valid(raise_exception=True):
            interest_group_sr.save()

            return Response(data=interest_group_sr.data)

        return Response(data={'error': 'Wrong parameters'}, status=400)

    def put(self, request: Request, interest_group_id: int):
        try:
            interest_group = InterestGroup.objects.get(id=interest_group_id)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup with {interest_group_id=} does not exist'}, status=400)

        request_data = request.data

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        self.check_object_permissions(request, user_profile)

        if interest_group.organizer.id != user_profile.pk:
            return Response({'error': f"You don't have permission"}, status=400)

        request_data['organizer'] = user_profile.pk

        interest_group_sr = InterestGroupSerializer(interest_group, data=request.data)

        if interest_group_sr.is_valid(raise_exception=True):
            interest_group_sr.save()

            return Response(data=interest_group_sr.data)

        return Response(data={'error': 'Wrong parameters'}, status=400)

    def delete(self, request: Request, interest_group_id: int):
        try:
            interest_group = InterestGroup.objects.get(id=interest_group_id)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup with {interest_group_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        if interest_group.organizer.id != user_profile.pk:
            return Response({'error': f"You don't have permission"}, status=400)

        interest_group.deleted_at = datetime.datetime.now()
        interest_group.save()

        return Response(
            data={
                'success': f'InterestGroup with {interest_group_id=} '
                           f'was successfully deleted at {interest_group.deleted_at}'
            }
        )


class SubscribeAPIView(APIView):
    def post(self, request: Request, interest_group_id: int):
        try:
            interest_group = InterestGroup.objects.get(id=interest_group_id)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup with {interest_group_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        interest_group.participants.add(user_profile)
        interest_group.save()

        return Response({'success': 'You was successfully subscribed'})


class UnsubscribeAPIView(APIView):
    def post(self, request: Request, interest_group_id: int):
        try:
            interest_group = InterestGroup.objects.get(id=interest_group_id)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup with {interest_group_id=} does not exist'}, status=400)

        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        interest_group.participants.remove(user_profile)
        interest_group.save()

        return Response({'success': 'You was successfully unsubscribed'})


class MyInterestGroupsAPIView(APIView):
    def get(self, request: Request):
        try:
            user_profile = UserProfile.objects.get(user_id=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': f"User with user_id={request.user.id} doesn't have profile"}, status=400)
        except TypeError:
            return Response({'error': f"You don't specify token"}, status=400)

        try:
            interest_groups = InterestGroup.objects.filter(participants__id=user_profile.pk)
        except InterestGroup.DoesNotExist:
            return Response({'error': f'InterestGroup does not exist'}, status=400)

        return Response(data=InterestGroupSerializer(interest_groups, many=True).data)
