import datetime
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile, ActivationCode
from user_profile.permissions import IsUserOneself, IsUserProfileOneself
from user_profile.serializers import UserSerializer, UserProfileSerializer


class ListCreateUserAPIView(APIView):
    def post(self, request: Request):
        user_sr = UserSerializer(data=request.data)

        if user_sr.is_valid(raise_exception=True):
            user_sr.save()

            user = User.objects.get(id=user_sr['id'].value)
            user.is_active = 0
            user.save()

            return Response(data=user_sr.data)

    def get(self, request: Request):
        users = User.objects.all()

        return Response(data=UserSerializer(users, many=True).data)


class RetrieveUpdateDestroyUserAPIView(APIView):
    permission_classes = (IsUserOneself,)

    def get(self, request: Request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        self.check_object_permissions(request, user)

        return Response(UserSerializer(user).data)

    def patch(self, request: Request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        user_sr = UserSerializer(user, data=request.data, partial=True)

        if user_sr.is_valid(raise_exception=True):
            self.check_object_permissions(request, user)
            user_sr.save()

            return Response(data=user_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def put(self, request: Request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        user_sr = UserSerializer(user, data=request.data)

        if user_sr.is_valid(raise_exception=True):
            self.check_object_permissions(request, user)
            user_sr.save()

            return Response(data=user_sr.data)

        return Response(data={'error': 'Wrong parameters'})


class ListCreateUserProfileAPIView(APIView):
    def post(self, request: Request):
        user_profile_sr = UserProfileSerializer(data=request.data)

        if user_profile_sr.is_valid(raise_exception=True):
            user_profile_sr.save()

            try:
                user: User = User.objects.get(id=request.data.get('user_id'))  #TODO: maybe error if user_id != id
            except User.DoesNotExist:
                return Response({'error': f'User with user_id={request.data.get("user_id")} does not exist'}, status=400)

            code = random.randint(1000, 9999)
            ActivationCode.objects.create(
                code=code,
                user_id=user
            )

            send_mail(
                'Точка сбора. Активация аккаунта',
                f'Перейдите по ссылке, чтобы активировать аккаунт: '
                f'http://{settings.SERVER_HOST}/api/v1/users_profile/{user_profile_sr["user_id"].value}/{code}',
                settings.EMAIL_HOST_USER,
                (request.data.get('email'), ),
                fail_silently=False,
            )

            return Response(data=user_profile_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def get(self, request: Request):
        users_profile = UserProfile.objects.all()

        return Response(data=UserProfileSerializer(users_profile, many=True).data)


class RetrieveUpdateDestroyUserProfileAPIView(APIView):
    permission_classes = (IsUserProfileOneself, )

    def get(self, request: Request, profile_id: int):
        try:
            profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response({'error': f'Profile with {profile_id=} does not exist'}, status=400)

        self.check_object_permissions(request, profile)

        return Response(UserProfileSerializer(profile).data)

    def patch(self, request: Request, profile_id: int):
        try:
            profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response({'error': f'Profile with {profile_id=} does not exist'}, status=400)

        profile_sr = UserProfileSerializer(profile, data=request.data, partial=True)

        if profile_sr.is_valid(raise_exception=True):
            self.check_object_permissions(request, profile)
            profile_sr.save()

            return Response(data=profile_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def put(self, request: Request, profile_id: int):
        try:
            profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response({'error': f'Profile with {profile_id=} does not exist'}, status=400)

        profile_sr = UserProfileSerializer(profile, data=request.data)

        if profile_sr.is_valid(raise_exception=True):
            self.check_object_permissions(request, profile)
            profile_sr.save()

            return Response(data=profile_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def delete(self, request: Request, profile_id: int):
        try:
            profile: UserProfile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response({'error': f'Profile with {profile_id=} does not exist'}, status=400)

        profile.deleted_at = datetime.datetime.now()
        profile.save()

        return Response(data={'success': f'Profile with {profile_id=} was successfully deleted at {profile.deleted_at}'})


class ActivateUserProfile(APIView):
    def get(self, request: Request, user_id: int, activation_code: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        try:
            activation: ActivationCode = ActivationCode.objects.filter(user_id=user_id).last()
        except ActivationCode.DoesNotExist:
            return Response({'error': f'Incorrect activation code'}, status=400)

        if activation.code != activation_code:
            return Response({'error': f'Incorrect activation code'}, status=400)

        user.is_active = 1
        user.save()

        return Response({'success': f'Profile was successfully activated'})
